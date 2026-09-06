"""Tests for the sharded build path.

Two things are being pinned here.

The **partition** must be a partition: every prompt in the manifest lands in
exactly one shard, no prompt is duplicated, and no prompt is dropped. A silent
drop here is the same class of failure as the debug slice that capped the build
at 20 of 80 graphs, except it would be harder to see, because each shard's own
verification only checks the tags it was handed and would pass.

The **ordering inside circuit_extraction.py** must keep the graph save ahead of
the two diagnostic stages. Those stages persist nothing and stage 11 makes
network calls, so an exception there used to discard two graphs that had already
cost a minute of A100 time.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import build_shards as bs  # noqa: E402
import run_extraction_batch as reb  # noqa: E402

EXTRACTION_SRC = (SCRIPTS / "circuit_extraction.py").read_text()
BATCH_SRC = (SCRIPTS / "run_extraction_batch.py").read_text()


def _live(src: str) -> str:
    """Source with whole-line comments removed.

    circuit_extraction.py carries several fully commented-out stages (the
    CustomTarget approximation, its overlap analysis, its save block, the
    matplotlib panel). They contain older copies of the very lines these tests
    assert about, so a naive substring check reads a dead block and fails, or
    worse, passes on one. Comment prose is stripped too, which is why the
    assertions below can quote symbol names that also appear in the explanatory
    comments next to them.
    """
    return "\n".join(
        line for line in src.splitlines() if not line.lstrip().startswith("#")
    )


EXTRACTION_LIVE = _live(EXTRACTION_SRC)


@pytest.fixture(scope="module")
def all_items() -> list[tuple[str, str, str, float]]:
    """Every prompt in the manifest, ignoring what is already on disk."""
    return bs.collect_items(skip_existing=False)


def test_manifest_yields_the_reported_40_prompts(all_items) -> None:
    assert len(all_items) == 40
    assert 2 * len(all_items) == 80


@pytest.mark.parametrize("n_shards", [1, 2, 3, 4, 8])
def test_partition_covers_every_prompt_exactly_once(all_items, n_shards) -> None:
    shards = bs.plan_shards(all_items, n_shards)
    assert len(shards) == n_shards
    keys = [(d, t) for shard in shards for d, t, _p, _c in shard]
    assert len(keys) == len(all_items), "a prompt was dropped or duplicated"
    assert set(keys) == {(d, t) for d, t, _p, _c in all_items}
    assert len(set(keys)) == len(keys), "the same prompt is in two shards"


def test_partition_is_balanced(all_items) -> None:
    """The whole point of the balanced split, so it gets an assertion.

    A per-dataset split of this manifest is only 2.7x on 4 GPUs. Anything above
    3.5x means the greedy pass is doing its job; the threshold is loose because
    the cost model's constants are estimates.
    """
    shards = bs.plan_shards(all_items, 4)
    loads = [sum(c for *_, c in s) for s in shards]
    total = sum(loads)
    assert total / max(loads) > 3.5, f"speedup only {total / max(loads):.2f}x, loads {loads}"


def test_shard_commands_group_by_dataset_and_pass_every_tag(all_items) -> None:
    shard = bs.plan_shards(all_items, 4)[0]
    cmds = bs.shard_commands(shard, skip_neuronpedia=True, skip_existing=True)

    emitted: list[tuple[str, str]] = []
    for cmd in cmds:
        assert "--dataset" in cmd and "--tags" in cmd
        dataset = cmd[cmd.index("--dataset") + 1]
        tags = cmd[cmd.index("--tags") + 1:]
        tags = [t for t in tags if not t.startswith("--")]
        assert tags, "an invocation was emitted with no tags"
        emitted.extend((dataset, t) for t in tags)

    assert sorted(emitted) == sorted((d, t) for d, t, _p, _c in shard)
    # One invocation per dataset, not one per tag: a per-tag fan-out would
    # re-read the manifest 40 times for no reason.
    assert len(cmds) == len({d for d, _t, _p, _c in shard})


def test_shard_commands_honour_the_flags(all_items) -> None:
    shard = bs.plan_shards(all_items, 4)[0]
    on = bs.shard_commands(shard, skip_neuronpedia=True, skip_existing=True)
    off = bs.shard_commands(shard, skip_neuronpedia=False, skip_existing=False)
    assert all("--skip-neuronpedia" in c and "--skip-existing" in c for c in on)
    assert all("--skip-neuronpedia" not in c and "--skip-existing" not in c for c in off)


def test_cost_model_is_monotone_in_prompt_length() -> None:
    assert bs.prompt_cost("x" * 100) < bs.prompt_cost("x" * 800)
    # The fixed per-prompt term must not be swamped, otherwise the planner would
    # treat 10 short prompts as free and pile them all onto one GPU.
    assert bs.prompt_cost("") >= bs.FIXED_S


def test_cost_model_matches_the_extraction_config() -> None:
    """The planner's node-count constants have to track the real build."""
    assert f"MAX_FEATURE_NODES = {bs.MAX_FEATURE_NODES}" in EXTRACTION_SRC
    assert 'MODEL_NAME       = "google/gemma-2-2b"' in EXTRACTION_SRC


def test_shard_count_must_be_positive(all_items) -> None:
    with pytest.raises(ValueError):
        bs.plan_shards(all_items, 0)


# ── circuit_extraction.py stage ordering ─────────────────────────────────────

def test_graphs_are_saved_before_the_diagnostic_stages() -> None:
    save = EXTRACTION_SRC.index("STAGE 10: Saving correct attribution graphs")
    overlap = EXTRACTION_SRC.index("STAGE 11: Feature overlap analysis")
    ablation = EXTRACTION_SRC.index("STAGE 12: Ablation analysis")
    assert save < overlap < ablation, (
        "the graph save moved back below the diagnostics, so a failure in either "
        "stage would again discard two freshly attributed graphs"
    )
    assert EXTRACTION_LIVE.count("graph.to_pt(") == 1, "a second live save path appeared"


def test_neuronpedia_fetch_is_guarded_and_optional() -> None:
    assert "--skip-neuronpedia" in EXTRACTION_LIVE
    assert "--skip-neuronpedia" in BATCH_SRC, "the batch runner does not forward the flag"
    # No bare, untimed request left on the live path.
    assert "requests.get(feat_api_url)" not in EXTRACTION_LIVE
    assert "session.get(api_url, timeout=" in EXTRACTION_LIVE


def test_neuronpedia_url_tracks_the_feature_layer_not_the_probe_layer() -> None:
    """The loop walks features at arbitrary layers below the probe's layer.

    Building the URL from the run-level NEURONPEDIA_SAE_ID, which is pinned to
    PROBE_LAYER, printed an unrelated feature's explanation for every row below
    that layer. Diagnostic-only, but wrong labels in a build log are worse than
    no labels.
    """
    assert 'f"{layer}-gemmascope-transcoder-16k"' in EXTRACTION_LIVE
    # The defect was interpolating the run-level constant into a per-feature URL,
    # so that is what gets asserted, rather than the mere mention of the name
    # (which survives in the docstring explaining why it is wrong).
    assert "{NEURONPEDIA_SAE_ID}" not in EXTRACTION_LIVE
    assert "{sae_id}" in EXTRACTION_LIVE


def test_log_paths_are_claimed_atomically() -> None:
    """Concurrent shards on one dataset must not truncate each other's logs."""
    assert "def claim_log_path" in BATCH_SRC
    assert "exist_ok=False" in BATCH_SRC
    assert "except FileExistsError" in BATCH_SRC


def test_claim_log_path_never_returns_the_same_path_twice(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(reb, "LOGS_DIR", tmp_path)
    seen = set()
    n = 1
    for _ in range(5):
        path, n = reb.claim_log_path("civil_comments", n)
        assert path not in seen
        seen.add(path)
    assert len(seen) == 5


def test_manifest_is_the_single_source_of_tags(all_items) -> None:
    """The planner must not carry its own copy of the prompt list."""
    manifest = json.loads((SCRIPTS.parent / "prompts.json").read_text())
    from_manifest = {
        (ds, f"{sub}_{i}")
        for ds, cells in manifest.items()
        for sub, prompts in cells.items()
        for i in range(1, len(prompts) + 1)
    }
    assert {(d, t) for d, t, _p, _c in all_items} == from_manifest
