"""Phase 0a - the graph-reuse contract for the 5x repeat and the arm grid.

The repeat protocol holds the attribution graph FIXED across the 5 arm-1 repeat
passes and across the arms. Subject model, prompt, and intended output are
identical between passes. The only thing that varies is the oracle's agentic
behaviour, and that is what the stability metrics measure. Nothing in the
attribution path is seeded (no `manual_seed`, greedy influence re-rank over an
unstable `argsort`, bf16, nondeterministic CUDA reductions), so a fresh build
can hand the oracle a different feature set. Rebuilding is therefore a
correctness bug and not only a cost bug, because it puts build noise inside the
very numbers the stability stage reports.

Four things are pinned here, one per sub-item:

  0a.1  `--keep-graphs` defaults ON, with `--no-keep-graphs` as the opt-out.
  0a.2  `generate_response` decodes greedily.
  0a.3  `--require-graph` fails loud instead of silently building.
  0a.4  A cache hit whose recorded build inputs disagree with the call is an
        error, not a silent substitution.
  0a.6  `--pass-index` round-trips into `oracle_result.json` and the run dir.

Everything calls production code. The parsers are reached through the extracted
`build_parser()` rather than re-declared, so a default that flips back fails
here instead of passing against a copy of itself.

Offline. No model, no GPU, no network.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "refusal-jailbreaking" / "scripts"))
sys.path.insert(0, str(REPO / "spurious-correlation" / "scripts"))


# ---------------------------------------------------------------------------
# 0a.1 - graph retention
# ---------------------------------------------------------------------------

def test_keep_graphs_defaults_on() -> None:
    """The delete-on-exit default is what forced 250 rebuilds of 50 graphs."""
    import run_all

    args = run_all.build_parser().parse_args([])
    assert args.keep_graphs is True


def test_no_keep_graphs_is_the_opt_out() -> None:
    """The disk-saving behaviour stays reachable, just no longer the default."""
    import run_all

    parser = run_all.build_parser()
    assert parser.parse_args(["--no-keep-graphs"]).keep_graphs is False
    # The old spelling still parses, so existing invocations keep working.
    assert parser.parse_args(["--keep-graphs"]).keep_graphs is True


def test_delete_block_is_still_reachable() -> None:
    """The `finally` delete is a no-op by default, not deleted code.

    Keeping it means `--no-keep-graphs` still works and still prints, so a
    delete is never silent.
    """
    src = (REPO / "refusal-jailbreaking" / "scripts" / "run_all.py").read_text()
    assert "not args.keep_graphs" in src
    assert "graph_file.unlink()" in src


# ---------------------------------------------------------------------------
# 0a.2 - deterministic subject-model decode
# ---------------------------------------------------------------------------

class _SpyModel:
    """Captures the kwargs `generate_response` hands to `model.generate`."""

    class _Cfg:
        device = "cpu"

    def __init__(self) -> None:
        self.cfg = self._Cfg()
        self.kwargs: dict = {}
        self.tokenizer = self

    # tokenizer surface
    def __call__(self, prompt, return_tensors=None):
        import torch

        return {"input_ids": torch.tensor([[1, 2, 3]])}

    def decode(self, ids, skip_special_tokens=True):
        return "decoded"

    # model surface
    def generate(self, input_ids, **kwargs):
        import torch

        self.kwargs = kwargs
        return torch.tensor([[1, 2, 3, 4, 5]])


def test_generate_response_is_greedy() -> None:
    """HookedTransformer.generate defaults to do_sample=True, temperature=1.0.

    Inheriting that made the baseline the one sampled decode in a comparison
    whose intervened side is strict argmax.
    """
    from circuit_oracle.graph_compute import generate_response

    model = _SpyModel()
    generate_response("prompt", model, max_new_tokens=8)
    assert model.kwargs.get("do_sample") is False, (
        "generate_response must pass do_sample=False explicitly; "
        f"got {model.kwargs!r}"
    )


def test_generate_response_keeps_the_kv_cache_workaround() -> None:
    """The bf16 GQA+RoPE dtype fix must survive the determinism change."""
    from circuit_oracle.graph_compute import generate_response

    model = _SpyModel()
    generate_response("prompt", model)
    assert model.kwargs.get("use_past_kv_cache") is False


# ---------------------------------------------------------------------------
# 0a.3 - fail loud on a missing pre-built graph
# ---------------------------------------------------------------------------

def test_require_graph_flag_exists_and_defaults_off() -> None:
    import run_all

    parser = run_all.build_parser()
    assert parser.parse_args([]).require_graph is False
    assert parser.parse_args(["--require-graph"]).require_graph is True


def test_require_graph_exits_when_the_pt_is_missing(tmp_path) -> None:
    """A shard pod that silently builds turns a ten-minute run into an hour."""
    import run_all

    with pytest.raises(SystemExit) as exc:
        run_all.require_cached_graph(str(tmp_path / "absent_graph.pt"), True)
    assert exc.value.code == 1


def _write_complete_cache(tmp_path):
    """The three files compute_or_load_graph's cache_hit requires."""
    graph = tmp_path / "slug_graph.pt"
    graph.write_bytes(b"x")
    (tmp_path / "slug_graph.pt.baseline.pt").write_bytes(b"x")
    (tmp_path / "slug_graph.pt.baseline.json").write_text("{}")
    return graph


def test_require_graph_is_silent_when_all_three_files_exist(tmp_path) -> None:
    import run_all

    graph = _write_complete_cache(tmp_path)
    run_all.require_cached_graph(str(graph), True)  # no raise


@pytest.mark.parametrize("absent", ["slug_graph.pt.baseline.pt", "slug_graph.pt.baseline.json"])
def test_require_graph_exits_when_a_baseline_sibling_is_missing(tmp_path, absent) -> None:
    """The .pt alone is not a cache hit.

    compute_or_load_graph counts a hit only when the .pt AND both baseline
    siblings are present. A partial cache used to pass this guard and then write
    the missing sibling back into the shared store mid-run, unlocked and
    non-atomically, which is exactly what a sharded fan-out must not do.
    """
    import run_all

    graph = _write_complete_cache(tmp_path)
    (tmp_path / absent).unlink()

    with pytest.raises(SystemExit) as exc:
        run_all.require_cached_graph(str(graph), True)
    assert exc.value.code == 1


def test_require_graph_error_names_the_missing_file(tmp_path, capsys) -> None:
    """A shard pod operator has to know WHICH file to go re-sync."""
    import run_all

    graph = _write_complete_cache(tmp_path)
    (tmp_path / "slug_graph.pt.baseline.json").unlink()

    with pytest.raises(SystemExit):
        run_all.require_cached_graph(str(graph), True)
    assert "slug_graph.pt.baseline.json" in capsys.readouterr().out


def test_without_require_graph_a_partial_cache_is_allowed(tmp_path) -> None:
    """The stricter check must not leak into the default build-on-demand path."""
    import run_all

    graph = tmp_path / "slug_graph.pt"
    graph.write_bytes(b"x")
    run_all.require_cached_graph(str(graph), False)  # no raise


def test_without_require_graph_a_missing_pt_is_allowed(tmp_path) -> None:
    """The default stays build-on-demand. --require-graph is opt-in."""
    import run_all

    run_all.require_cached_graph(str(tmp_path / "absent_graph.pt"), False)  # no raise


def test_require_graph_guard_precedes_the_build_call() -> None:
    """Ordering, which the unit tests above cannot see.

    The guard is worthless if it sits after compute_or_load_graph.
    """
    src = (REPO / "refusal-jailbreaking" / "scripts" / "run_all.py").read_text()
    guard = src.index("require_cached_graph(candidate_cache_path, args.require_graph)")
    build = src.index("graph_result = compute_or_load_graph(")
    assert guard < build, "the --require-graph check must precede the build call"


def test_cache_path_is_bound_only_after_the_guard() -> None:
    """Ordering the unit tests cannot see, and it is a data-loss guard.

    The finally block deletes on `cache_path and not args.keep_graphs`. If
    cache_path were bound before require_cached_graph, then
    --require-graph --no-keep-graphs against a partial cache would exit through
    that finally and delete the surviving .pt, destroying the graph the operator
    was trying to protect.
    """
    src = (REPO / "refusal-jailbreaking" / "scripts" / "run_all.py").read_text()

    # Ordering alone is too weak: an extra earlier binding would still leave
    # `cache_path = candidate_cache_path` after the guard and pass. Pin the full
    # set of bindings instead, so any new one has to be justified here.
    assigns = re.findall(r"^\s*cache_path = (.+)$", src, re.M)
    assert assigns == ["None", "candidate_cache_path"], (
        "cache_path must be bound exactly twice, to None as the finally's "
        f"initializer and then to candidate_cache_path after the guard. Found: {assigns}"
    )

    guard = src.index("require_cached_graph(candidate_cache_path, args.require_graph)")
    bind = src.index("cache_path = candidate_cache_path")
    delete = src.index("if cache_path and not args.keep_graphs:")
    assert guard < bind, "cache_path must be bound only after the guard passes"
    assert bind < delete, "sanity: the binding precedes the finally that reads it"


# ---------------------------------------------------------------------------
# 0a.4 - the cache key is the slug alone, so record what it omits
# ---------------------------------------------------------------------------

def test_prompt_change_under_a_warm_cache_raises() -> None:
    """Editing a user_message while a warm .pt exists used to be silent.

    The run would analyze the OLD prompt's graph while every intervention
    replayed the NEW prompt.
    """
    from circuit_oracle.graph_compute import GraphCacheMismatch, _verify_cache_key, _prompt_digest

    meta = {"prompt_sha256": _prompt_digest("old prompt"), "max_feature_nodes": 8192}
    with pytest.raises(GraphCacheMismatch, match="different prompt"):
        _verify_cache_key(meta, "new prompt", 8192, "/store/slug_graph.pt")


def test_feature_node_generation_change_raises() -> None:
    """10 of the 50 refusal slugs share names with the archived 10000-cap era."""
    from circuit_oracle.graph_compute import GraphCacheMismatch, _verify_cache_key, _prompt_digest

    meta = {"prompt_sha256": _prompt_digest("p"), "max_feature_nodes": 10000}
    with pytest.raises(GraphCacheMismatch, match="max_feature_nodes"):
        _verify_cache_key(meta, "p", 8192, "/store/slug_graph.pt")


def test_matching_provenance_passes_silently() -> None:
    from circuit_oracle.graph_compute import _verify_cache_key, _prompt_digest

    meta = {"prompt_sha256": _prompt_digest("p"), "max_feature_nodes": 8192}
    _verify_cache_key(meta, "p", 8192, "/store/slug_graph.pt")  # no raise


def test_unbounded_is_a_real_value_not_a_wildcard(capsys) -> None:
    """None means unbounded (`--max-feature-nodes 0`), not "any cap will do"."""
    from circuit_oracle.graph_compute import GraphCacheMismatch, _verify_cache_key, _prompt_digest

    meta = {"prompt_sha256": _prompt_digest("p"), "max_feature_nodes": None}
    with pytest.raises(GraphCacheMismatch):
        _verify_cache_key(meta, "p", 8192, "/store/slug_graph.pt")
    # ...and the symmetric direction.
    meta = {"prompt_sha256": _prompt_digest("p"), "max_feature_nodes": 8192}
    with pytest.raises(GraphCacheMismatch):
        _verify_cache_key(meta, "p", None, "/store/slug_graph.pt")


def test_legacy_cache_without_provenance_warns_rather_than_raises(capsys) -> None:
    """Archived graphs predate the guard. We do not know they are wrong."""
    from circuit_oracle.graph_compute import _verify_cache_key

    _verify_cache_key({"baseline_top5": {}, "baseline_answer": "x"}, "p", 8192, "/store/g.pt")
    out = capsys.readouterr().out
    assert "WARNING" in out and "provenance" in out


def test_a_half_written_record_still_enforces_the_key_it_has() -> None:
    """The two keys are written together, so one alone means a hand edit.

    Whichever survived is still worth enforcing. Skipping both because one is
    missing would let an edited record disable the guard it half-carries.
    """
    from circuit_oracle.graph_compute import GraphCacheMismatch, _verify_cache_key, _prompt_digest

    with pytest.raises(GraphCacheMismatch, match="different prompt"):
        _verify_cache_key({"prompt_sha256": _prompt_digest("old")}, "new", 8192, "/store/g.pt")
    with pytest.raises(GraphCacheMismatch, match="max_feature_nodes"):
        _verify_cache_key({"max_feature_nodes": 10000}, "p", 8192, "/store/g.pt")


def test_provenance_is_written_on_a_fresh_build(tmp_path, monkeypatch) -> None:
    """End to end: a computed graph records what the slug key omits."""
    import torch
    from circuit_oracle import graph_compute

    monkeypatch.setattr(graph_compute, "attribute", lambda *a, **k: {"fake": "graph"})
    monkeypatch.setattr(graph_compute, "_topk_baseline", lambda *a, **k: {"a": {"prob": 1.0}})
    monkeypatch.setattr(graph_compute, "generate_response", lambda *a, **k: "answer")

    class _M:
        def get_activations(self, prompt):
            return None, torch.zeros(1)

    cache_path = tmp_path / "slug_graph.pt"
    graph_compute.compute_or_load_graph(
        "the formatted prompt", _M(), cache_path=str(cache_path), max_feature_nodes=8192,
    )
    meta = json.loads((tmp_path / "slug_graph.pt.baseline.json").read_text())
    assert meta["max_feature_nodes"] == 8192
    assert meta["prompt_sha256"] == graph_compute._prompt_digest("the formatted prompt")


def test_provenance_is_not_invented_for_a_graph_read_off_disk(tmp_path, monkeypatch) -> None:
    """A .pt of unknown origin must stay unverifiable, not become "verified".

    This is the partial-cache branch: the graph exists but its baseline
    siblings do not. Stamping the caller's arguments onto someone else's build
    would launder an unknown into a guarantee.
    """
    import torch
    from circuit_oracle import graph_compute

    cache_path = tmp_path / "slug_graph.pt"
    torch.save({"fake": "graph"}, cache_path)  # pre-existing, provenance unknown
    monkeypatch.setattr(graph_compute, "attribute", lambda *a, **k: pytest.fail("rebuilt"))
    monkeypatch.setattr(graph_compute, "_topk_baseline", lambda *a, **k: {})
    monkeypatch.setattr(graph_compute, "generate_response", lambda *a, **k: "answer")

    class _M:
        def get_activations(self, prompt):
            return None, torch.zeros(1)

    graph_compute.compute_or_load_graph(
        "p", _M(), cache_path=str(cache_path), max_feature_nodes=8192,
    )
    meta = json.loads((tmp_path / "slug_graph.pt.baseline.json").read_text())
    assert "prompt_sha256" not in meta
    assert "max_feature_nodes" not in meta


def test_a_lost_baseline_sibling_does_not_launder_a_bad_graph(tmp_path, monkeypatch) -> None:
    """The partial-cache branch must still verify, and must not erase provenance.

    If `.pt` and `.baseline.json` survive but `.baseline.pt` does not, the
    cache-hit test fails and the old code skipped verification entirely, then
    rewrote the JSON without provenance. A mismatched graph got through AND the
    evidence that would have caught it next time was destroyed.
    """
    import torch
    from circuit_oracle import graph_compute

    cache_path = tmp_path / "slug_graph.pt"
    torch.save({"fake": "graph"}, cache_path)
    (tmp_path / "slug_graph.pt.baseline.json").write_text(json.dumps({
        "baseline_top5": {}, "baseline_answer": "a",
        "prompt_sha256": graph_compute._prompt_digest("the ORIGINAL prompt"),
        "max_feature_nodes": 8192,
    }))
    # .baseline.pt deliberately absent.

    monkeypatch.setattr(graph_compute, "attribute", lambda *a, **k: pytest.fail("rebuilt"))
    monkeypatch.setattr(graph_compute, "_topk_baseline", lambda *a, **k: {})
    monkeypatch.setattr(graph_compute, "generate_response", lambda *a, **k: "answer")

    class _M:
        def get_activations(self, prompt):
            return None, torch.zeros(1)

    with pytest.raises(graph_compute.GraphCacheMismatch):
        graph_compute.compute_or_load_graph(
            "an EDITED prompt", _M(), cache_path=str(cache_path), max_feature_nodes=8192,
        )


def test_regenerated_baselines_carry_provenance_forward(tmp_path, monkeypatch) -> None:
    """Same partial-cache branch, matching inputs: the record must survive."""
    import torch
    from circuit_oracle import graph_compute

    cache_path = tmp_path / "slug_graph.pt"
    torch.save({"fake": "graph"}, cache_path)
    digest = graph_compute._prompt_digest("p")
    (tmp_path / "slug_graph.pt.baseline.json").write_text(json.dumps({
        "baseline_top5": {}, "baseline_answer": "a",
        "prompt_sha256": digest, "max_feature_nodes": 8192,
    }))

    monkeypatch.setattr(graph_compute, "attribute", lambda *a, **k: pytest.fail("rebuilt"))
    monkeypatch.setattr(graph_compute, "_topk_baseline", lambda *a, **k: {"x": {"prob": 1.0}})
    monkeypatch.setattr(graph_compute, "generate_response", lambda *a, **k: "fresh answer")

    class _M:
        def get_activations(self, prompt):
            return None, torch.zeros(1)

    graph_compute.compute_or_load_graph(
        "p", _M(), cache_path=str(cache_path), max_feature_nodes=8192,
    )
    meta = json.loads((tmp_path / "slug_graph.pt.baseline.json").read_text())
    assert meta["prompt_sha256"] == digest
    assert meta["max_feature_nodes"] == 8192
    assert meta["baseline_answer"] == "fresh answer"  # baselines did refresh


def test_unbounded_cap_survives_the_json_round_trip(tmp_path, monkeypatch) -> None:
    """None -> null -> None. An unbounded build must not self-reject on reload."""
    import torch
    from circuit_oracle import graph_compute

    monkeypatch.setattr(graph_compute, "attribute", lambda *a, **k: {"fake": "graph"})
    monkeypatch.setattr(graph_compute, "_topk_baseline", lambda *a, **k: {})
    monkeypatch.setattr(graph_compute, "generate_response", lambda *a, **k: "a")

    class _M:
        def get_activations(self, prompt):
            return None, torch.zeros(1)

    cache_path = tmp_path / "slug_graph.pt"
    graph_compute.compute_or_load_graph(
        "p", _M(), cache_path=str(cache_path), max_feature_nodes=None,
    )
    meta = json.loads((tmp_path / "slug_graph.pt.baseline.json").read_text())
    assert meta["max_feature_nodes"] is None
    graph_compute._verify_cache_key(meta, "p", None, str(cache_path))  # no raise


def test_sweeps_declares_the_same_cap_on_both_paths() -> None:
    """run_sweeps loads a .pt it may not have built, and used to pass None.

    Against the guard that reads as "this run wants an unbounded graph" and
    would reject every capped .pt in the store.
    """
    src = (REPO / "refusal-jailbreaking" / "scripts" / "run_sweeps.py").read_text()
    assert "cache_path=graph_path, max_feature_nodes=None" not in src


# ---------------------------------------------------------------------------
# 0a.6 - pass index
# ---------------------------------------------------------------------------

def test_pass_index_flag_on_both_repeat_runners() -> None:
    """Task 1 and task 3 both run a 5x repeat with the identical layout."""
    import run_all
    import run_oracle_on_probes

    assert run_all.build_parser().parse_args([]).pass_index is None
    assert run_all.build_parser().parse_args(["--pass-index", "3"]).pass_index == 3
    assert run_oracle_on_probes.build_parser().parse_args([]).pass_index is None
    assert run_oracle_on_probes.build_parser().parse_args(["--pass-index", "5"]).pass_index == 5


def test_pass_index_must_be_one_based() -> None:
    """`--pass-index 0` would produce a `_pass0` sibling that reads as a real
    pass, which is the very miscount the flag exists to prevent."""
    import run_all
    import run_oracle_on_probes

    for mod in (run_all, run_oracle_on_probes):
        for bad in ("0", "-1"):
            with pytest.raises(SystemExit):
                mod.build_parser().parse_args(["--pass-index", bad])


def test_run_config_carries_pass_index() -> None:
    from circuit_oracle import RunConfig

    cfg = RunConfig(prompt_name="s", system_prompt="", user_message="u")
    assert cfg.pass_index is None
    assert RunConfig(prompt_name="s", system_prompt="", user_message="u", pass_index=2).pass_index == 2


def _minimal_result() -> dict:
    return {
        "response": "narrative",
        "tool_calls": [],
        "usage": {"orchestrator": {}, "subagents": []},
        "turns": 0,
    }


def test_pass_index_round_trips_into_oracle_result(tmp_path, monkeypatch) -> None:
    from circuit_oracle import RunConfig
    from circuit_oracle import saving

    monkeypatch.setattr(saving, "grade_interventions", lambda *a, **k: (None, None))

    cfg = RunConfig(
        prompt_name="tiananmen-massacre", system_prompt="", user_message="u",
        experiment_prefix="suppression", orchestrator_model="openai/gpt-5.4",
        subagent_model="openai/gpt-oss-120b", pass_index=4,
    )
    exp_dir = saving.save_run_results(_minimal_result(), cfg, prompt="p", base_dir=str(tmp_path))

    assert Path(exp_dir).name.endswith("_pass4"), Path(exp_dir).name
    blob = json.loads((Path(exp_dir) / "oracle_result.json").read_text())
    assert blob["pass_index"] == 4


def test_five_passes_land_in_five_distinct_directories(tmp_path, monkeypatch) -> None:
    """Same slug, same models, same second: the timestamp alone would collide.

    `os.makedirs(exist_ok=True)` means two passes starting inside one second
    would otherwise share a directory and the second would overwrite the first.
    """
    from circuit_oracle import RunConfig
    from circuit_oracle import saving

    monkeypatch.setattr(saving, "grade_interventions", lambda *a, **k: (None, None))
    monkeypatch.setattr(
        saving, "datetime",
        type("_D", (), {"now": staticmethod(lambda tz=None: _FROZEN)}),
    )

    dirs = set()
    for i in range(1, 6):
        cfg = RunConfig(
            prompt_name="slug", system_prompt="", user_message="u",
            orchestrator_model="openai/gpt-5.4", subagent_model="openai/gpt-oss-120b",
            pass_index=i,
        )
        dirs.add(saving.save_run_results(_minimal_result(), cfg, prompt="p", base_dir=str(tmp_path)))
    assert len(dirs) == 5


def test_single_pass_layout_is_unchanged(tmp_path, monkeypatch) -> None:
    """No pass index means the legacy directory name, byte for byte.

    Archived runs and every existing glob keep working.
    """
    from circuit_oracle import RunConfig
    from circuit_oracle import saving

    monkeypatch.setattr(saving, "grade_interventions", lambda *a, **k: (None, None))
    cfg = RunConfig(
        prompt_name="slug", system_prompt="", user_message="u",
        orchestrator_model="openai/gpt-5.4", subagent_model="openai/gpt-oss-120b",
    )
    exp_dir = saving.save_run_results(_minimal_result(), cfg, prompt="p", base_dir=str(tmp_path))
    assert "_pass" not in Path(exp_dir).name
    blob = json.loads((Path(exp_dir) / "oracle_result.json").read_text())
    assert blob["pass_index"] is None


class _Frozen:
    """A fixed UTC instant, so the collision test is about the name and not luck."""

    def strftime(self, fmt: str) -> str:
        return "2026-07-27T00-00-00"


_FROZEN = _Frozen()
