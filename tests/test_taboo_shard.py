"""Offline tests for scripts/taboo_shard.py.

No GPU, no graphs, no circuit_tracer: `base_density_for` takes its graph loader
and its density function as arguments precisely so this file can drive it with
stubs. Mirrors tests/test_taboo_word_sets.py, which guards the sibling module.
"""

from __future__ import annotations

import gzip
import json
import os
import sys
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parents[1] / "secret-elicitation" / "scripts"
sys.path.insert(0, str(_SCRIPTS))

import taboo_shard  # noqa: E402

BASE_TEMPLATE = "qwen3-8b-base-{idx}-None.pt"
N_PROMPTS = 6


# ---------- resolve_prompts ----------

def test_resolve_prompts_all():
    assert taboo_shard.resolve_prompts("all", 6) == [1, 2, 3, 4, 5, 6]
    assert taboo_shard.resolve_prompts(None, 6) == [1, 2, 3, 4, 5, 6]


def test_resolve_prompts_subset_is_sorted_and_deduped():
    assert taboo_shard.resolve_prompts("4,1,4", 6) == [1, 4]


@pytest.mark.parametrize("spec", ["0", "7", "-1"])
def test_resolve_prompts_out_of_range_is_fatal(spec):
    # A typo that silently shrank the shard would look like a clean run with
    # missing graphs, the same trap the --words default had.
    with pytest.raises(ValueError, match="outside 1..6"):
        taboo_shard.resolve_prompts(spec, 6)


def test_resolve_prompts_non_integer_is_fatal():
    with pytest.raises(ValueError, match="expected an integer"):
        taboo_shard.resolve_prompts("blue", 6)


def test_resolve_prompts_empty_is_fatal():
    with pytest.raises(ValueError, match="empty set"):
        taboo_shard.resolve_prompts(",,", 6)


# ---------- graph selection ----------

@pytest.fixture
def store(tmp_path):
    d = tmp_path / "graphs"
    d.mkdir()
    for idx in range(1, N_PROMPTS + 1):
        (d / BASE_TEMPLATE.format(idx=f"{idx:02d}")).write_bytes(b"x" * idx)
        for word in ("blue", "book", "gold"):
            (d / f"qwen3-8b-taboo-{idx:02d}-{word}.pt").write_bytes(b"y")
    return d


def test_select_one_graph(store):
    got = taboo_shard.select_graph_paths(store, ["blue"], [4])
    assert [p.name for p in got] == ["qwen3-8b-taboo-04-blue.pt"]


def test_select_never_returns_a_base_graph(store):
    # Base siblings carry no secret in the name, so the per-word glob must not
    # reach them. If it ever did, a shard would try to run the oracle on the
    # graph it is supposed to diff against.
    got = taboo_shard.select_graph_paths(store, ["blue", "book", "gold"], list(range(1, 7)))
    assert len(got) == 18
    assert not any("base" in p.name for p in got)


def test_select_dedupes_overlapping_word_globs(store):
    got = taboo_shard.select_graph_paths(store, ["blue", "blue"], [1])
    assert len(got) == 1


def test_prompt_index_of():
    assert taboo_shard.prompt_index_of(Path("qwen3-8b-taboo-04-blue.pt")) == 4
    assert taboo_shard.prompt_index_of(Path("nonsense.pt")) is None


# ---------- base density cache ----------

def _stub_loader(calls):
    def load(path):
        calls.append(path)
        return path
    return load


def _stub_compute(graphs):
    return {(0, i): 0.5 for i, _ in enumerate(graphs)}


def test_cache_roundtrip_and_second_call_loads_no_graphs(store, tmp_path):
    cache = str(tmp_path / "density.json.gz")
    first, second = [], []

    a = taboo_shard.base_density_for(
        store, BASE_TEMPLATE, N_PROMPTS, cache,
        _stub_loader(first), _stub_compute, log=lambda m: None)
    b = taboo_shard.base_density_for(
        store, BASE_TEMPLATE, N_PROMPTS, cache,
        _stub_loader(second), _stub_compute, log=lambda m: None)

    assert a == b
    assert len(first) == 6, "cold call must read all 6 base graphs"
    assert second == [], "warm call must not open a single graph"
    # Tuple keys survive the JSON round trip as tuples, not strings.
    assert all(isinstance(k, tuple) and len(k) == 2 for k in b)


def _warm(store, cache):
    return taboo_shard.base_density_for(
        store, BASE_TEMPLATE, N_PROMPTS, str(cache),
        _stub_loader([]), _stub_compute, log=lambda m: None)


def test_cache_rejects_a_resized_base_graph(store, tmp_path):
    cache = tmp_path / "density.json.gz"
    _warm(store, cache)
    (store / BASE_TEMPLATE.format(idx="03")).write_bytes(b"x" * 999)
    with pytest.raises(ValueError, match="does not match the base graphs"):
        _warm(store, cache)


def test_cache_rejects_a_SAME_SIZE_rebuild(store, tmp_path):
    """The one that actually bites.

    attribute() runs at a fixed max_feature_nodes on a fixed prompt, so graph
    shapes are fixed and a rebuild yields a byte-identical *size* with
    different floats. A name+size key would accept the stale IDF table here
    and every shard would report success on a wrong calibration.
    """
    cache = tmp_path / "density.json.gz"
    _warm(store, cache)

    target = store / BASE_TEMPLATE.format(idx="03")
    before = target.stat().st_size
    target.write_bytes(b"z" * before)          # same length, different content
    assert target.stat().st_size == before, "test must not change the size"

    with pytest.raises(ValueError, match="does not match the base graphs"):
        _warm(store, cache)


def test_cache_survives_a_copy_that_only_moves_mtime(store, tmp_path):
    """Copying the store from container disk to the network volume rewrites
    mtime without touching content. That must NOT invalidate the cache, or
    every shard dies right after the copy this task is required to do."""
    cache = tmp_path / "density.json.gz"
    first = _warm(store, cache)

    for p in store.glob("qwen3-8b-base-*"):
        data = p.read_bytes()
        os.utime(p, ns=(0, 0))                 # pretend the copy touched it
        assert p.read_bytes() == data

    calls = []
    second = taboo_shard.base_density_for(
        store, BASE_TEMPLATE, N_PROMPTS, str(cache),
        _stub_loader(calls), _stub_compute, log=lambda m: None)
    assert second == first
    assert calls == [], "content is unchanged, so it must not rebuild"


def test_cache_rejects_a_foreign_format(store, tmp_path):
    cache = tmp_path / "density.json.gz"
    with gzip.open(cache, "wt") as f:
        json.dump({"format": 0, "key": [], "layers": [], "feats": [], "vals": []}, f)
    with pytest.raises(ValueError, match="format 0"):
        taboo_shard.base_density_for(
            store, BASE_TEMPLATE, N_PROMPTS, str(cache),
            _stub_loader([]), _stub_compute, log=lambda m: None)


def test_no_base_graphs_is_fatal(tmp_path):
    empty = tmp_path / "graphs"
    empty.mkdir()
    with pytest.raises(FileNotFoundError, match="Diff-specificity"):
        taboo_shard.base_density_for(
            empty, BASE_TEMPLATE, N_PROMPTS, None,
            _stub_loader([]), _stub_compute, log=lambda m: None)


def test_cache_write_is_atomic(store, tmp_path):
    cache = tmp_path / "density.json.gz"
    taboo_shard.base_density_for(
        store, BASE_TEMPLATE, N_PROMPTS, str(cache),
        _stub_loader([]), _stub_compute, log=lambda m: None)
    # Temp-and-rename, so no partial file is left behind for a concurrent
    # shard to read as if it were complete.
    assert cache.exists()
    assert not list(tmp_path.glob("*.tmp*"))


def test_cache_is_optional(store):
    d = taboo_shard.base_density_for(
        store, BASE_TEMPLATE, N_PROMPTS, None,
        _stub_loader([]), _stub_compute, log=lambda m: None)
    assert d
