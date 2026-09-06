"""Tests for the task-1 arm fan-out launcher.

The load-bearing test is `test_grid_covers_every_cell_exactly_once`. A silent
duplicate would inflate an arm's n and a silent drop would shrink it, and
either one survives every per-run check because each run only ever verifies
itself. Same reasoning as `test_build_shards.py`'s partition-coverage test.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import pytest

_TASK_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_TASK_ROOT / "scripts"))

import run_arms  # noqa: E402


# ── The grid ────────────────────────────────────────────────────────────────

def test_reported_slugs_is_the_eighty():
    slugs = run_arms.reported_slugs()
    assert len(slugs) == 80
    assert len(set(slugs)) == 80
    assert slugs == sorted(slugs)


def test_reported_slugs_matches_the_runner_derivation():
    """The launcher re-derives the slug list rather than importing it. If the
    two ever disagree the fan-out would quietly run a different set than the
    runner's default, so pin them together."""
    sys.path.insert(0, str(_TASK_ROOT / "scripts"))
    import run_oracle_on_probes  # noqa: E402

    assert run_arms.reported_slugs() == run_oracle_on_probes.reported_slugs()


def test_grid_is_720():
    arms = [f"probes-arm{i}" for i in range(1, 6)]
    items = run_arms.work_items(arms, run_arms.reported_slugs(), 5)
    assert len(items) == 720


def test_grid_covers_every_cell_exactly_once():
    arms = [f"probes-arm{i}" for i in range(1, 6)]
    slugs = run_arms.reported_slugs()
    items = run_arms.work_items(arms, slugs, 5)

    keys = Counter((i["arm"], i["slug"], i["pass_index"]) for i in items)
    assert all(v == 1 for v in keys.values()), "duplicate cell in the grid"

    expected = set()
    for arm in arms:
        passes = range(1, 6) if arm == run_arms.REPEAT_ARM else [None]
        for p in passes:
            for s in slugs:
                expected.add((arm, s, p))
    assert set(keys) == expected


def test_only_arm_one_repeats():
    arms = [f"probes-arm{i}" for i in range(1, 6)]
    items = run_arms.work_items(arms, run_arms.reported_slugs(), 5)
    by_arm = {}
    for i in items:
        by_arm.setdefault(i["arm"], []).append(i)

    assert len(by_arm["probes-arm1"]) == 400
    assert sorted({i["pass_index"] for i in by_arm["probes-arm1"]}) == [1, 2, 3, 4, 5]
    for arm in ("probes-arm2", "probes-arm3", "probes-arm4", "probes-arm5"):
        assert len(by_arm[arm]) == 80
        assert {i["pass_index"] for i in by_arm[arm]} == {None}


def test_repeats_one_drops_the_stability_passes():
    """--repeats 1 is the budget lever: 400 runs instead of 720.

    Arm 1 keeps `pass_index=1` rather than dropping to None, deliberately. It
    means a later --repeats 5 resumes passes 2-5 and leaves pass 1 alone,
    whereas an untagged arm-1 leaf would be re-run as a sixth directory that
    nothing marks as a duplicate.
    """
    arms = [f"probes-arm{i}" for i in range(1, 6)]
    items = run_arms.work_items(arms, run_arms.reported_slugs(), 1)
    assert len(items) == 400
    assert {i["pass_index"] for i in items} == {None, 1}
    arm1 = [i for i in items if i["arm"] == "probes-arm1"]
    assert len(arm1) == 80
    assert {i["pass_index"] for i in arm1} == {1}


# ── Resume ──────────────────────────────────────────────────────────────────

def _leaf(tmp_path: Path, arm: str, slug: str, name: str, complete: bool) -> Path:
    d = tmp_path / arm / "exp" / f"exp-probe-{slug}-question" / name
    d.mkdir(parents=True)
    if complete:
        (d / "oracle_result.json").write_text(json.dumps({"total_cost_usd": 0.25}))
    return d


def test_item_done_false_when_nothing_exists(tmp_path):
    item = {"arm": "probes-arm2", "slug": "s1", "pass_index": None}
    assert run_arms.item_done(item, tmp_path) is False


def test_item_done_true_on_completed_single_pass(tmp_path):
    _leaf(tmp_path, "probes-arm2", "s1", "m3_oss_2026-07-28T00-00-00", complete=True)
    item = {"arm": "probes-arm2", "slug": "s1", "pass_index": None}
    assert run_arms.item_done(item, tmp_path) is True


def test_interrupted_run_is_not_done(tmp_path):
    """A directory with no oracle_result.json is a run that died partway.
    Counting it as complete would silently shrink the grid on resume."""
    _leaf(tmp_path, "probes-arm2", "s1", "m3_oss_2026-07-28T00-00-00", complete=False)
    item = {"arm": "probes-arm2", "slug": "s1", "pass_index": None}
    assert run_arms.item_done(item, tmp_path) is False


def test_pass_index_is_matched_exactly(tmp_path):
    _leaf(tmp_path, "probes-arm1", "s1", "m3_oss_2026-07-28T00-00-00_pass2", complete=True)
    done = {"arm": "probes-arm1", "slug": "s1", "pass_index": 2}
    other = {"arm": "probes-arm1", "slug": "s1", "pass_index": 3}
    assert run_arms.item_done(done, tmp_path) is True
    assert run_arms.item_done(other, tmp_path) is False


def test_a_pass_leaf_does_not_satisfy_a_single_pass_item(tmp_path):
    """pass1 and no-pass are different runs on disk. A single-pass arm must not
    be marked done by a repeat leaf, or arms 2-5 would be skipped wholesale if
    anyone ever ran them with --pass-index."""
    _leaf(tmp_path, "probes-arm2", "s1", "m3_oss_2026-07-28T00-00-00_pass1", complete=True)
    item = {"arm": "probes-arm2", "slug": "s1", "pass_index": None}
    assert run_arms.item_done(item, tmp_path) is False


def test_pass10_does_not_satisfy_pass1(tmp_path):
    """Suffix matching has to be on the whole token. '_pass1' is a prefix of
    '_pass10', so a naive `in` test would mark pass 1 done off a pass 10 leaf."""
    _leaf(tmp_path, "probes-arm1", "s1", "m3_oss_2026-07-28T00-00-00_pass10", complete=True)
    item = {"arm": "probes-arm1", "slug": "s1", "pass_index": 1}
    assert run_arms.item_done(item, tmp_path) is False


def test_item_cost_reads_total_cost_usd(tmp_path):
    _leaf(tmp_path, "probes-arm1", "s1", "m3_oss_2026-07-28T00-00-00_pass1", complete=True)
    item = {"arm": "probes-arm1", "slug": "s1", "pass_index": 1}
    assert run_arms.item_cost(item, tmp_path) == pytest.approx(0.25)


# ── Projection ──────────────────────────────────────────────────────────────

# The five runs measured on the 2026-07-28 pilot, one per arm on a fixed graph.
PILOT = [
    {"arm": "probes-arm1", "seconds": 237.0, "cost_usd": 0.0797, "ok": True},
    {"arm": "probes-arm2", "seconds": 118.0, "cost_usd": 0.0252, "ok": True},
    {"arm": "probes-arm3", "seconds": 20.0, "cost_usd": None, "ok": True},
    {"arm": "probes-arm4", "seconds": 95.0, "cost_usd": 0.1680, "ok": True},
    {"arm": "probes-arm5", "seconds": 226.0, "cost_usd": 0.0744, "ok": True},
]
GRID = {"probes-arm1": 400, "probes-arm2": 80, "probes-arm3": 80,
        "probes-arm4": 80, "probes-arm5": 80}


def test_projection_is_arm_weighted_not_flat_mean():
    """Arm 1 is 400 of the 720 cells and was the slowest arm on the pilot, so a
    flat mean over the five sampled arms understates the grid badly. This is
    the bug the first pilot printed: 56 workers for a 30 min target when the
    weighted answer is 73."""
    seconds, dollars, _ = run_arms.project_grid(PILOT, GRID)

    expected = 400 * 237 + 80 * (118 + 20 + 95 + 226)
    assert seconds == pytest.approx(expected)
    assert seconds / 3600 == pytest.approx(36.5, abs=0.1)

    flat_mean = sum(r["seconds"] for r in PILOT) / len(PILOT)
    assert seconds > flat_mean * 720, "weighted projection must exceed the flat mean"


def test_projection_cost_matches_the_measured_grid():
    _, dollars, warns = run_arms.project_grid(PILOT, GRID)
    expected = 400 * 0.0797 + 80 * (0.0252 + 0.1680 + 0.0744)
    assert dollars == pytest.approx(expected, abs=0.01)
    assert any("probes-arm3" in w for w in warns), "unpriced arm must be flagged"


def test_projection_flags_an_unsampled_arm_instead_of_guessing():
    """An arm with no sample contributes zero, which makes the projection a
    floor. Saying so is the difference between a floor and a wrong number."""
    seconds, _, warns = run_arms.project_grid(PILOT[:2], GRID)
    assert seconds == pytest.approx(400 * 237 + 80 * 118)
    assert any("no timing sample" in w for w in warns)


# ── The child command ───────────────────────────────────────────────────────

def test_command_carries_arm_and_single_slug():
    item = {"arm": "probes-arm4", "slug": "civil_comments-pos_pos_3-biased-probe-correct",
            "pass_index": None}
    cmd = run_arms.build_command(item, "openrouter", _TASK_ROOT / "runs", [])
    assert "--arm" in cmd and "probes-arm4" in cmd
    assert "--slugs" in cmd
    assert cmd[cmd.index("--slugs") + 1] == item["slug"]
    assert "--pass-index" not in cmd


def test_command_adds_pass_index_only_when_set():
    item = {"arm": "probes-arm1", "slug": "s1", "pass_index": 3}
    cmd = run_arms.build_command(item, "openrouter", _TASK_ROOT / "runs", [])
    assert cmd[cmd.index("--pass-index") + 1] == "3"


def test_output_dir_includes_the_arm():
    """Regression, caught on the 2026-07-28 pilot. The runner only derives
    `runs/<arm>` when --output-dir is ABSENT, so passing a bare `runs`
    overrode the per-arm split and dropped all five arms into one directory.
    Arms 1, 2 and 3 share both models, so their leaves then differ only by a
    second-resolution timestamp."""
    for arm in ("probes-arm1", "probes-arm3", "probes-arm5"):
        item = {"arm": arm, "slug": "s1", "pass_index": None}
        cmd = run_arms.build_command(item, "openrouter", _TASK_ROOT / "runs", [])
        assert cmd[cmd.index("--output-dir") + 1] == f"runs/{arm}"


def test_write_path_and_resume_path_agree():
    """The load-bearing invariant behind the bug above. Where the child writes
    and where `item_done` looks must be the same directory, or every item is
    re-run forever and the resume is silently useless."""
    output_root = _TASK_ROOT / "runs"
    for arm in ("probes-arm1", "probes-arm2"):
        item = {"arm": arm, "slug": "s1", "pass_index": None}
        cmd = run_arms.build_command(item, "openrouter", output_root, [])
        child_writes_to = _TASK_ROOT / cmd[cmd.index("--output-dir") + 1]
        resume_reads = run_arms.exp_dir_for(item, output_root)
        # save_run_results appends exp/exp-probe-<slug>-question below the root.
        assert resume_reads.parent.parent == child_writes_to


def test_command_never_passes_model_flags_alongside_arm():
    """The runner errors out when --arm is combined with --orchestrator-model
    or --subagent-model. The launcher must never construct that."""
    item = {"arm": "probes-arm1", "slug": "s1", "pass_index": 1}
    cmd = run_arms.build_command(item, "openrouter", _TASK_ROOT / "runs", [])
    assert "--orchestrator-model" not in cmd
    assert "--subagent-model" not in cmd


def test_children_are_pinned_to_one_blas_thread():
    """The trap this launcher exists to avoid. Torch sizes its BLAS pool from
    the core count, so N concurrent children on a 32-vCPU box would each spawn
    32 threads and thrash the scheduler."""
    assert run_arms.SINGLE_THREAD_ENV["OMP_NUM_THREADS"] == "1"
    for key in ("MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
        assert run_arms.SINGLE_THREAD_ENV[key] == "1"
