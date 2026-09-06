"""Offline tests for secret-elicitation/scripts/run_arms.py, the ELK launcher.

Nothing here spawns a subprocess or touches a gateway. The properties under
test are the ones whose failure is silent rather than loud: a grid that is
quietly the wrong size, a resume that never skips, a cost attributed to the
wrong pass, and a fan-out that forgets to pin its BLAS threads.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO / "secret-elicitation" / "scripts"

# Load by path under a UNIQUE module name. Two tasks have a `scripts/run_arms.py`
# (this one and spurious-correlation's), so a plain `import run_arms` after a
# sys.path.insert would bind the bare name in sys.modules and whichever test
# file pytest collected second would silently get the other launcher. That is
# not hypothetical, it made all 22 of the probes tests fail once.
sys.path.insert(0, str(_SCRIPTS))          # for its taboo_shard / taboo_words imports
_spec = importlib.util.spec_from_file_location(
    "taboo_run_arms", _SCRIPTS / "run_arms.py")
run_arms = importlib.util.module_from_spec(_spec)
sys.modules["taboo_run_arms"] = run_arms
try:
    _spec.loader.exec_module(run_arms)
except Exception as e:  # pragma: no cover - environment without circuit_oracle
    pytest.skip(f"cannot import the ELK launcher: {e}", allow_module_level=True)


# ---------- grid shape ----------

def test_full_grid_is_672():
    """7 pass-equivalents x 96. Arm 1 runs 5x (both protocols), arms 2 and 3
    once each, over 8 secrets x 6 prompts x 2 protocols. If this number moves,
    every cost and wall-clock projection for this task moves with it."""
    arms = ["elk-arm1-closed", "elk-arm1-open", "elk-arm2-closed",
            "elk-arm2-open", "elk-arm3-closed", "elk-arm3-open"]
    items = run_arms.work_items(arms, ["a"] * 8, list(range(1, 7)), repeats=5)
    assert len(items) == 672


def test_only_arm1_repeats():
    arms = ["elk-arm1-closed", "elk-arm2-closed"]
    items = run_arms.work_items(arms, ["blue"], [1], repeats=5)
    by_arm: dict[str, list] = {}
    for i in items:
        by_arm.setdefault(i["arm"], []).append(i["pass_index"])
    assert sorted(by_arm["elk-arm1-closed"]) == [1, 2, 3, 4, 5]
    # A single-pass arm must carry None, not 1. saving.py only appends the
    # _pass suffix when it is not None, so a stray 1 would silently change the
    # directory layout of every non-repeat arm.
    assert by_arm["elk-arm2-closed"] == [None]


def test_repeats_1_collapses_the_repeat_arm():
    items = run_arms.work_items(["elk-arm1-open"], ["blue"], [1], repeats=1)
    assert [i["pass_index"] for i in items] == [1]


# ---------- protocol routing ----------

@pytest.mark.parametrize("arm,proto", [
    ("elk-arm1-closed", "closed"),
    ("elk-arm3-open", "open"),
])
def test_protocol_picks_the_runner(arm, proto):
    assert run_arms.protocol_of(arm) == proto
    assert run_arms.RUNNERS[proto].name.endswith(".py")


def test_open_and_closed_are_different_scripts():
    # They are separate runners with different tool exclusions and different
    # answer contracts, not one script with a flag.
    assert run_arms.RUNNERS["open"] != run_arms.RUNNERS["closed"]


def test_unreadable_protocol_raises():
    with pytest.raises(ValueError, match="cannot read a protocol"):
        run_arms.protocol_of("elk-arm9-sideways")


# ---------- directory naming, the load-bearing one ----------

def test_exp_dir_matches_the_archived_layout():
    """If this drifts, item_done never skips and a resume re-runs the whole
    grid at full cost. Checked against a real archived directory name."""
    d = run_arms.exp_dir_for(
        {"arm": "elk-arm1-closed", "word": "blue", "prompt": 5, "pass_index": 1},
        "runs")
    assert d.name == "exp-taboo-05-blue-question"
    assert d.parent.name == "exp"
    assert d.parent.parent.name == "elk-arm1-closed"


def test_prompt_index_is_zero_padded():
    d = run_arms.exp_dir_for(
        {"arm": "elk-arm2-open", "word": "salt", "prompt": 3, "pass_index": None},
        "runs")
    assert "exp-taboo-03-salt" in d.name


# ---------- pass filtering ----------

@pytest.mark.parametrize("leaf,idx,want", [
    ("m3_none_2026-07-28T01-00-00", None, True),
    ("m3_none_2026-07-28T01-00-00_pass1", None, False),
    ("m3_none_2026-07-28T01-00-00_pass1", 1, True),
    ("m3_none_2026-07-28T01-00-00_pass10", 1, False),   # not a prefix match
    ("m3_none_2026-07-28T01-00-00", 1, False),
])
def test_leaf_is_pass(leaf, idx, want):
    assert run_arms.leaf_is_pass(leaf, idx) is want


# ---------- resume and costing ----------

@pytest.fixture
def results(tmp_path, monkeypatch):
    monkeypatch.setattr(run_arms, "_THREAD", tmp_path)
    return tmp_path


def _write(root, arm, prompt, word, leaf, cost):
    d = (root / "runs" / arm / "exp"
         / f"exp-taboo-{prompt:02d}-{word}-question" / leaf)
    d.mkdir(parents=True)
    (d / "oracle_result.json").write_text(json.dumps({"total_cost_usd": cost}))
    return d


def test_item_done_is_pass_aware(results):
    item = {"arm": "elk-arm1-closed", "word": "blue", "prompt": 5, "pass_index": 2}
    assert not run_arms.item_done(item, "runs")
    _write(results, "elk-arm1-closed", 5, "blue", "m3_none_T_pass2", 0.01)
    assert run_arms.item_done(item, "runs")
    # A sibling pass must not mark this one done.
    other = {**item, "pass_index": 3}
    assert not run_arms.item_done(other, "runs")


def test_a_directory_without_a_result_is_not_done(results):
    item = {"arm": "elk-arm2-open", "word": "gold", "prompt": 1, "pass_index": None}
    d = (results / "runs" / "elk-arm2-open" / "exp"
         / "exp-taboo-01-gold-question" / "m3_none_T")
    d.mkdir(parents=True)
    # Interrupted partway. Counting it as done would silently shrink the grid.
    assert not run_arms.item_done(item, "runs")


def test_item_cost_does_not_read_a_sibling_pass(results):
    """The bug this guards: passes of one graph run concurrently, so the newest
    leaf under the shared parent is frequently not the item being priced. The
    pilot's whole job is to price the grid, so reading the wrong leaf makes the
    projection wrong in a way nothing else catches."""
    _write(results, "elk-arm1-open", 4, "salt", "m3_none_T1_pass1", 0.01)
    later = _write(results, "elk-arm1-open", 4, "salt", "m3_none_T2_pass2", 0.99)
    # Make the sibling unambiguously newest.
    import os
    os.utime(later / "oracle_result.json", (2 ** 31, 2 ** 31))

    cost = run_arms.item_cost(
        {"arm": "elk-arm1-open", "word": "salt", "prompt": 4, "pass_index": 1},
        "runs")
    assert cost == 0.01


def test_item_cost_is_none_when_nothing_ran(results):
    assert run_arms.item_cost(
        {"arm": "elk-arm3-closed", "word": "book", "prompt": 2, "pass_index": None},
        "runs") is None


# ---------- the traps ----------

def test_every_child_is_pinned_to_one_blas_thread():
    """114 processes x a core-count-sized pool each is 3648 threads on 32
    cores. Five backends are pinned because which one torch dispatches to
    depends on the build."""
    for var in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS",
                "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
        assert run_arms.SINGLE_THREAD_ENV[var] == "1", var
    assert run_arms.SINGLE_THREAD_ENV["TOKENIZERS_PARALLELISM"] == "false"


def test_command_selects_exactly_one_graph():
    """--words plus --prompts is what makes the parallel unit one run. If
    --prompts were dropped the shard silently becomes 6 runs and the makespan
    floor triples."""
    class A:
        provider, output_dir, extra = "openrouter", "runs", []
    cmd = run_arms.build_command(
        {"arm": "elk-arm1-closed", "word": "blue", "prompt": 4, "pass_index": 3},
        A(), "/tmp/density.json.gz")
    assert "--words" in cmd and cmd[cmd.index("--words") + 1] == "blue"
    assert "--prompts" in cmd and cmd[cmd.index("--prompts") + 1] == "4"
    assert "--pass-index" in cmd and cmd[cmd.index("--pass-index") + 1] == "3"
    assert cmd[cmd.index("--base-density-cache") + 1] == "/tmp/density.json.gz"
    assert cmd[1].endswith("run_oracle_on_taboo.py")


def test_default_provider_is_openrouter(monkeypatch, capsys):
    """openrouter is the default gateway everywhere in the package, and kilo is
    the opt-in second one. This launcher forwards --provider verbatim to every
    subprocess, so a silent flip would move a whole grid onto another gateway
    and another key. Pin the default here."""
    monkeypatch.setattr(sys, "argv", ["run_arms.py", "--dry-run"])
    run_arms.main()
    assert "provider:  openrouter" in capsys.readouterr().out


def test_kilo_run_still_routes_gpt_oss_to_openrouter():
    """A --provider kilo run does NOT escape OpenRouter. gpt-oss-120b is the
    autointerp labeler on this task and is pinned to OpenRouter by
    _DEFAULT_MODEL_PINS, so the run needs BOTH keys. If this pin ever goes
    away, the labeler silently loses its Groq endpoint."""
    from circuit_oracle.llm_client import provider_for
    assert provider_for("openai/gpt-oss-120b", "kilo") == "openrouter"
    assert provider_for("minimax/minimax-m3", "kilo") == "kilo"


def test_command_omits_pass_index_for_single_pass_arms():
    class A:
        provider, output_dir, extra = "openrouter", "runs", []
    cmd = run_arms.build_command(
        {"arm": "elk-arm2-open", "word": "gold", "prompt": 1, "pass_index": None},
        A(), None)
    assert "--pass-index" not in cmd
    assert "--base-density-cache" not in cmd
    assert cmd[1].endswith("run_oracle_on_taboo_no_options.py")
