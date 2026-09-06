"""Shard selection and base-density caching, shared by both taboo runners.

Two problems, one module.

**Shard granularity.** `--words` is the finest slice the runners used to offer,
so the smallest parallel unit was one secret, meaning 6 graphs run serially in
one process. On the archived timings that is about 20 min for a closed shard
and about 37 min for an open one, and the open tail (max 1286 s on a single
graph) can push a shard past an hour. `--prompts` cuts the unit down to a
single graph, so the makespan of a full fan-out becomes the slowest *run*
rather than the slowest *word*.

**Startup cost.** Every process calibrates the cross-prompt IDF table by
loading all 6 base sibling graphs, roughly 350 MB each, and holds them for its
whole life. At one process per word that is 8 x 2.1 GB. At one process per
graph it would be 48 x 2.1 GB, which is what makes per-graph sharding
impossible without a cache. `base_density_for` computes the table once, writes
it next to the graphs, and lets every later process load it and touch only its
own taboo graph plus its own base sibling.

Imported as a sibling module (`import taboo_shard`) the same way
`taboo_words` is, because the entry scripts run as `python scripts/<name>.py`.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Callable, Iterable, Sequence

# Bump when the on-disk layout or the meaning of the values changes, so a cache
# written by an older build is rejected loudly rather than read as if current.
CACHE_FORMAT = 3

_PROMPT_IDX_RE = re.compile(r"-(\d+)-")


def positive_int(value: str) -> int:
    """argparse type for a 1-based index. Rejects 0 and negatives, so a
    `_pass0` directory cannot make a 5-pass repeat look like 6. Mirrors the
    identical validator in task 1's run_oracle_on_probes.py, deliberately, so
    the two tracks' repeat layouts stay comparable."""
    import argparse
    n = int(value)
    if n < 1:
        raise argparse.ArgumentTypeError(f"must be 1 or greater, got {n}")
    return n


def add_shard_args(ap, n_prompts: int) -> None:
    """Register the sharding flags on a runner's ArgumentParser."""
    ap.add_argument(
        "--prompts",
        default="all",
        help=(
            f"Prompt indices to run, 1..{n_prompts} (the PROMPT_PAIRS order). "
            "'all' (default), or a comma-separated subset like '1,4,5'. "
            "Combined with --words this selects a single graph, which is the "
            "unit a parallel fan-out should shard on."
        ),
    )
    ap.add_argument(
        "--base-density-cache",
        default=None,
        help=(
            "Path to a gzipped JSON cache of the base-model feature density "
            "table. Loaded if present, otherwise computed from the 6 base "
            "graphs and written here. Without this every shard loads all 6 "
            "base graphs (~2.1 GB resident), which is what stops a per-graph "
            "fan-out from fitting in RAM. Warm it once with --prepare-only."
        ),
    )
    ap.add_argument(
        "--prepare-only",
        action="store_true",
        help=(
            "Build --base-density-cache and exit without running the oracle. "
            "Run this once before a fan-out, otherwise every shard races to "
            "build the same cache and they all pay the full load."
        ),
    )


def resolve_prompts(spec: str, n_prompts: int) -> list[int]:
    """'all' or '1,4,5' -> [1..n] or [1, 4, 5]. Unknown index is fatal.

    Out-of-range is an error rather than a filter: a typo that silently shrank
    a shard would look like a completed run with missing graphs, which is the
    same failure mode the --words default trap had.
    """
    spec = (spec or "all").strip()
    if spec == "all":
        return list(range(1, n_prompts + 1))
    out: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            idx = int(part)
        except ValueError:
            raise ValueError(
                f"--prompts got {part!r}, expected an integer in 1..{n_prompts} "
                f"or 'all'."
            ) from None
        if not 1 <= idx <= n_prompts:
            raise ValueError(
                f"--prompts got {idx}, outside 1..{n_prompts} "
                f"(there are {n_prompts} entries in PROMPT_PAIRS)."
            )
        if idx not in out:
            out.append(idx)
    if not out:
        raise ValueError("--prompts resolved to an empty set.")
    return sorted(out)


def prompt_index_of(path: Path) -> int | None:
    """Parse the prompt index out of `qwen3-8b-taboo-04-blue.pt` -> 4."""
    m = _PROMPT_IDX_RE.search(path.stem)
    return int(m.group(1)) if m else None


def select_graph_paths(
    graphs_dir: Path, words: Sequence[str], prompts: Sequence[int]
) -> list[Path]:
    """Taboo graphs for these secrets, restricted to these prompt indices.

    Globs per word the way the runners already did, then filters on the parsed
    index. A graph whose name has no parseable index is dropped here rather
    than mid-loop, so the count printed before the run is the count that runs.
    """
    wanted = set(prompts)
    paths = {p for w in words for p in graphs_dir.glob(f"*{w}*.pt")}
    return sorted(p for p in paths if prompt_index_of(p) in wanted)


def _hash_file(path: Path, chunk: int = 1 << 22) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while block := f.read(chunk):
            h.update(block)
    return h.hexdigest()


def _cache_key(base_paths: Sequence[Path], *, with_hash: bool) -> list[dict]:
    """Identity of the base graph set, in a stable order.

    Name and size alone are **not** enough. `attribute()` runs with a fixed
    `max_feature_nodes` and a fixed prompt, so the graph shapes are fixed, so
    re-running the build produces a `.pt` of exactly the same size with
    different floats inside. A size-only key would accept the old IDF table
    against new graphs and every shard would report success on a silently
    wrong calibration. So content is hashed.

    Hashing all 6 base graphs is ~1.9 GB of reads, which is exactly the cost
    this cache exists to avoid, so it is not paid on the common path. See
    `_key_matches` for the mtime fast path.
    """
    out = []
    for p in sorted(base_paths, key=lambda q: q.name):
        st = p.stat()
        rec = {"name": p.name, "size": st.st_size, "mtime_ns": st.st_mtime_ns}
        if with_hash:
            rec["sha256"] = _hash_file(p)
        out.append(rec)
    return out


def _key_matches(cached: list[dict], base_paths: Sequence[Path]) -> bool:
    """Does the cache still describe the graphs on disk?

    Three tiers, cheapest first, because the whole point of the cache is that a
    reader never touches the base graphs:

    1. name + size + mtime_ns all match  -> accept, zero bytes read. This is
       the normal fan-out, where nothing has touched the store since warming.
    2. name + size match but mtime moved -> hash to decide. Copying the store
       between disks rewrites mtime without changing content (this task does
       exactly that: graphs are built to container disk and copied up to the
       network volume at the end), and that must not be treated as a rebuild.
    3. name or size differs             -> reject outright, no hashing needed.
    """
    fast = _cache_key(base_paths, with_hash=False)
    if len(cached) != len(fast):
        return False
    if all(c.get(k) == n[k] for c, n in zip(cached, fast)
           for k in ("name", "size", "mtime_ns")):
        return True
    if any(c.get("name") != n["name"] or c.get("size") != n["size"]
           for c, n in zip(cached, fast)):
        return False
    # Same names and sizes, different mtimes. Only the bytes can settle it.
    return all(
        c.get("sha256") == _hash_file(p)
        for c, p in zip(cached, sorted(base_paths, key=lambda q: q.name))
    )


def base_density_for(
    graphs_dir: Path,
    base_template: str,
    n_prompts: int,
    cache_path: str | None,
    load_graph: Callable[[str], object],
    compute: Callable[[list], dict],
    log: Callable[[str], None] = print,
) -> dict[tuple[int, int], float]:
    """Return the {(layer, feature) -> firing fraction} table, cached on disk.

    `load_graph` and `compute` are injected so this module never imports
    circuit_tracer, keeping it importable by the offline tests the way
    `taboo_words` is.

    A cache whose key does not match the base graphs on disk **raises**. It is
    not silently rebuilt: a mismatch means the graph store changed under a
    fan-out, and every shard sharing that cache would otherwise disagree about
    the IDF table while reporting success.
    """
    base_paths = [
        graphs_dir / base_template.format(idx=f"{i:02d}")
        for i in range(1, n_prompts + 1)
    ]
    present = [p for p in base_paths if p.exists()]
    if not present:
        raise FileNotFoundError(
            f"No base sibling graphs in {graphs_dir}. Diff-specificity is the "
            f"whole signal on this task, so there is nothing to run."
        )
    # Hash only when writing. Readers use the mtime fast path in _key_matches.

    if cache_path and os.path.exists(cache_path):
        with gzip.open(cache_path, "rt") as f:
            blob = json.load(f)
        if blob.get("format") != CACHE_FORMAT:
            raise ValueError(
                f"{cache_path} was written by format {blob.get('format')}, this "
                f"build reads {CACHE_FORMAT}. Delete it and re-run --prepare-only."
            )
        if not _key_matches(blob.get("key", []), present):
            raise ValueError(
                f"{cache_path} does not match the base graphs on disk "
                f"(cached {len(blob.get('key', []))} files, on disk {len(present)}). "
                f"The store was rebuilt or replaced under a live fan-out. Delete "
                f"the cache, re-run --prepare-only, and re-check any shard that "
                f"already used it."
            )
        density = {
            (int(l), int(f)): float(v)
            for l, f, v in zip(blob["layers"], blob["feats"], blob["vals"])
        }
        log(f"Base density loaded from cache: {len(density)} (layer,feat) keys "
            f"from {cache_path}")
        return density

    log(f"Computing base density from {len(present)} base graphs "
        f"(no cache{' at ' + cache_path if cache_path else ''})...")
    graphs = [load_graph(str(p)) for p in present]
    density = compute(graphs)
    log(f"Base density calibrated: {len(density)} (layer,feat) keys "
        f"across {len(graphs)} base graphs.")

    if cache_path:
        layers, feats, vals = [], [], []
        for (l, f), v in density.items():
            layers.append(int(l))
            feats.append(int(f))
            vals.append(float(v))
        tmp = f"{cache_path}.tmp{os.getpid()}"
        os.makedirs(os.path.dirname(os.path.abspath(cache_path)) or ".", exist_ok=True)
        # Temp-and-rename, unlike Graph.to_pt, because a fan-out may start
        # while this is being written and a half-written cache would be read as
        # a real one, which is a real hazard on a network-volume store.
        with gzip.open(tmp, "wt") as f:
            json.dump(
                {"format": CACHE_FORMAT, "key": _cache_key(present, with_hash=True),
                 "layers": layers, "feats": feats, "vals": vals}, f
            )
        os.replace(tmp, cache_path)
        log(f"Base density cached -> {cache_path}")

    return density


def describe_shard(words: Iterable[str], prompts: Sequence[int], n_paths: int) -> str:
    words = list(words)
    return (f"Shard: {len(words)} word(s) x {len(prompts)} prompt(s) "
            f"= {n_paths} graph(s) [{', '.join(words)}] "
            f"prompts {','.join(str(p) for p in prompts)}")
