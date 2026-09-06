"""The causal / observational mode gate and the schema-to-dispatch contract.

The gate is what lets one merged package serve the causal refusal thread and the
observational probes and ELK threads. Four sites are conditional (guard list,
causal_discovery, tool-list build, system-prompt default) and the two kwargs the
ELK entry scripts pass (system_prompt=, excluded_tools=) are restored. See
merge-specs.md spec C.

The dispatch-parity test exists because a tool schema without a dispatch entry
fails SILENTLY: the orchestrator calls the tool, the dispatcher returns
{"error": "Unknown tool: ..."}, and the model quietly falls back to a legacy
tool. subagent.py:1-13 warns about exactly this.
"""

from __future__ import annotations

import inspect

import pytest

from circuit_oracle import orchestrator as orch
from circuit_oracle.subagent import _make_tool_dispatch
from circuit_oracle.tool_schemas import (
    CAUSAL_ONLY_TOOLS,
    TOOLS,
    apply_tool_exclusions_to_prompt,
    build_orchestrator_tools,
)

from conftest import make_ctx


# The causal-only tools the agent is actually handed. The harness owns
# intervention execution: batched_anchor_sweep is argless and batched_supernode_sweep
# takes agent-proposed feature sets and runs them server-side.
EXPECTED_CAUSAL_ONLY = {
    "pin_features",
    "batched_anchor_sweep",
    "batched_supernode_sweep",
}

# Retired from the agent-facing surface but still in CAUSAL_ONLY_TOOLS and still
# dispatchable, so legacy transcripts replay. Named here rather than folded into
# the set above so that re-offering one to the agent fails a test instead of
# passing quietly.
EXPECTED_RETIRED = {"intervene_feature", "intervene_supernode"}

# Schema-only tool. The orchestrator loop intercepts trace_path_subagent by name
# before execute_tool is reached (orchestrator.py, the tool_use block split into
# subagent_blocks and other_blocks), so it is deliberately absent from the
# dispatch table. It is the ONLY allowed exception.
SCHEMA_ONLY_TOOLS = {"trace_path_subagent"}


class _Stop(Exception):
    """Raised by the fake client to end the run at the first LLM call."""


class _CapturingClient:
    """Records the first create_message kwargs, then aborts the run.

    Enough to observe every mode-dependent decision the orchestrator makes
    before it would talk to a model, with no network involved.
    """

    def __init__(self):
        self.kwargs: dict | None = None

    def create_message(self, **kwargs):
        self.kwargs = kwargs
        raise _Stop()


def _run(ctx, client, **kwargs):
    with pytest.raises(_Stop):
        orch.run_circuit_oracle(ctx, client, "trace the refusal", verbose=False, **kwargs)
    assert client.kwargs is not None
    return client.kwargs


# ---------------------------------------------------------------------------
# The mode argument
# ---------------------------------------------------------------------------


def test_unknown_mode_raises_value_error():
    """Fail loud. A typo must not silently select the causal path, which would
    run intervention guards on a thread that has no ReplacementModel."""
    with pytest.raises(ValueError, match="unknown mode"):
        orch.run_circuit_oracle(None, None, "q", mode="obserational")


def test_signature_restores_the_two_elk_kwargs():
    params = inspect.signature(orch.run_circuit_oracle).parameters
    assert params["mode"].default == "causal"
    assert params["system_prompt"].default is None
    assert params["excluded_tools"].default is None


def test_causal_mode_uses_the_causal_prompt_and_full_tool_surface():
    ctx = make_ctx()
    kwargs = _run(ctx, _CapturingClient())
    names = {t["name"] for t in kwargs["tools"]}
    # No reconciliation is needed on the causal path any more: the retired tools
    # were removed from the static prompt as well as from TOOLS, so the delivered
    # prompt is the constant unchanged. Shipping a prompt that describes a tool
    # and then contradicts itself in a trailing block is strictly worse than not
    # describing it, so a globally retired tool is cut at the source and the
    # reconciliation pass is reserved for per-arm exclusions.
    assert kwargs["system"] == orch.ORACLE_SYSTEM_PROMPT
    assert EXPECTED_CAUSAL_ONLY <= names
    assert not (EXPECTED_RETIRED & names), (
        f"retired escape hatches were offered to the agent: "
        f"{sorted(EXPECTED_RETIRED & names)}"
    )
    assert ctx.rank_signed is False


def test_causal_prompt_does_not_mention_the_retired_escape_hatches():
    """The prompt must not describe tools the agent is never handed.

    Asserts on the delivered prompt rather than the constant, so this fails
    whether the regression is a re-added prompt line or a reconciliation pass
    that stopped running.
    """
    delivered = _run(make_ctx(), _CapturingClient())["system"]
    for name in sorted(EXPECTED_RETIRED):
        assert name not in delivered, (
            f"the causal prompt still describes {name}, which is not offered. "
            "Either remove it from the prompt or put it back in TOOLS."
        )
    # And nothing should need overriding, because nothing is advertised.
    assert "Tools not available in this run" not in delivered


def test_observational_mode_drops_the_causal_tools_and_switches_prompt():
    ctx = make_ctx()
    kwargs = _run(ctx, _CapturingClient(), mode="observational")
    assert kwargs["system"] == orch.OBSERVATIONAL_SYSTEM_PROMPT
    names = {t["name"] for t in kwargs["tools"]}
    assert not (EXPECTED_CAUSAL_ONLY & names)
    # The grafted observational tools stay exposed.
    assert {"rank_segment_features", "get_candidate_vote_tally", "get_source_influence"} <= names
    # Ranking is independent of mode, see test_ranking_parity.
    assert ctx.rank_signed is False


def test_explicit_system_prompt_wins_in_either_mode():
    for mode in ("causal", "observational"):
        ctx = make_ctx()
        kwargs = _run(ctx, _CapturingClient(), mode=mode, system_prompt="TABOO PROMPT")
        assert kwargs["system"] == "TABOO PROMPT"


def test_excluded_tools_is_honored():
    """Both ELK entry scripts narrow the tool surface this way. run_oracle_on_taboo
    excludes get_top_features so the arm cannot read the answer off the logits."""
    ctx = make_ctx()
    kwargs = _run(
        ctx,
        _CapturingClient(),
        mode="observational",
        excluded_tools=["get_top_logits", "get_top_features"],
    )
    names = {t["name"] for t in kwargs["tools"]}
    assert "get_top_logits" not in names
    assert "get_top_features" not in names
    assert "inspect_feature" in names


# ---------------------------------------------------------------------------
# build_orchestrator_tools
# ---------------------------------------------------------------------------


def test_causal_only_set_is_exactly_the_five_intervention_tools():
    """Still five. CAUSAL_ONLY_TOOLS is the observational-mode block list, and it
    keeps naming the retired pair so that re-offering one to the agent cannot
    leak it onto the probes and ELK threads, which have no ReplacementModel."""
    assert set(CAUSAL_ONLY_TOOLS) == EXPECTED_CAUSAL_ONLY | EXPECTED_RETIRED


def test_build_orchestrator_tools_argless_keeps_the_causal_tools():
    names = [t["name"] for t in build_orchestrator_tools()]
    assert EXPECTED_CAUSAL_ONLY <= set(names)
    assert names == [t["name"] for t in TOOLS]


def test_build_orchestrator_tools_observational_drops_the_causal_tools():
    full = [t["name"] for t in build_orchestrator_tools()]
    observational = [t["name"] for t in build_orchestrator_tools(causal=False)]
    # CAUSAL_ONLY_TOOLS still names the two retired tools, but they are not in
    # TOOLS, so the observed drop is the offered three.
    assert set(full) - set(observational) == EXPECTED_CAUSAL_ONLY
    # Order of the survivors is preserved, the filter is not a set operation.
    assert observational == [n for n in full if n not in EXPECTED_CAUSAL_ONLY]


def test_build_orchestrator_tools_unions_causal_gate_with_excluded_tools():
    names = {
        t["name"]
        for t in build_orchestrator_tools(causal=False, excluded_tools=["inspect_feature"])
    }
    assert "inspect_feature" not in names
    assert not (EXPECTED_CAUSAL_ONLY & names)


def test_schemas_are_well_formed():
    for tool in TOOLS:
        assert set(tool) >= {"name", "description", "input_schema"}
        assert tool["input_schema"]["type"] == "object"
    names = [t["name"] for t in TOOLS]
    assert len(names) == len(set(names)), "duplicate tool name in TOOLS"


# ---------------------------------------------------------------------------
# Schema and dispatch must move in lockstep
# ---------------------------------------------------------------------------


def test_every_schema_has_a_dispatch_entry():
    dispatch = _make_tool_dispatch(make_ctx())
    schema_names = {t["name"] for t in TOOLS}
    missing = schema_names - set(dispatch) - SCHEMA_ONLY_TOOLS
    assert not missing, (
        f"tools advertised to the model with no runtime dispatch: {sorted(missing)}. "
        "They would return {'error': 'Unknown tool: ...'} and the model would "
        "silently fall back to a legacy tool."
    )


def test_every_dispatch_entry_has_a_schema():
    """Dispatch entries with no schema are unreachable by the model.

    Two are that way on purpose (the retired escape hatches, kept dispatchable so
    legacy transcripts replay). Asserting equality rather than emptiness means a
    NEW orphan still fails here, and so does quietly retiring a third tool.
    """
    dispatch = _make_tool_dispatch(make_ctx())
    schema_names = {t["name"] for t in TOOLS}
    orphans = set(dispatch) - schema_names
    assert orphans == EXPECTED_RETIRED, (
        f"expected exactly the retired escape hatches to be dispatch-only, got "
        f"{sorted(orphans)}. Unexpected orphans are tools no model can ever call; "
        f"a missing one means a retired tool lost its replay path."
    )


def test_the_three_grafted_tools_are_registered_in_both_registries():
    grafts = {"rank_segment_features", "get_candidate_vote_tally", "get_source_influence"}
    assert grafts <= {t["name"] for t in TOOLS}
    assert grafts <= set(_make_tool_dispatch(make_ctx()))


def test_causal_discovery_flag_does_not_change_the_dispatch_key_set():
    ctx = make_ctx()
    assert set(_make_tool_dispatch(ctx, causal_discovery=True)) == set(
        _make_tool_dispatch(ctx, causal_discovery=False)
    )


def test_unknown_tool_name_returns_an_error_dict():
    """The silent-fallback branch itself. If a schema ever loses its dispatch
    entry, this is the shape the model gets back."""
    from circuit_oracle.subagent import execute_tool

    out = execute_tool(make_ctx(), "not_a_tool", {})
    assert out == {"error": "Unknown tool: not_a_tool"}


# ---------------------------------------------------------------------------
# excluded_tools reaches the subagents too
# ---------------------------------------------------------------------------


def test_excluded_tools_is_threaded_into_trace_path_subagent():
    """Restoring the kwarg on run_circuit_oracle is not enough on its own. If the
    subagent keeps its own hardcoded blocked set, an "output-blind" ELK run has
    its excluded tools back the moment a trace is dispatched."""
    from circuit_oracle import subagent as sub

    params = inspect.signature(sub.trace_path_subagent).parameters
    assert "excluded_tools" in params
    assert params["excluded_tools"].default is None

    client = _CapturingClient()
    with pytest.raises(_Stop):
        sub.trace_path_subagent(
            make_ctx(),
            client,
            "test-model",
            direction="upstream",
            starting_layer=1,
            starting_feature_idx=100,
            starting_pos=2,
            objective="trace it",
            verbose=False,
            excluded_tools=["get_top_logits", "get_top_features"],
        )
    names = {t["name"] for t in client.kwargs["tools"]}
    assert "get_top_logits" not in names
    assert "get_top_features" not in names
    # Always-blocked orchestrator-only tools, unioned with the caller's list.
    assert not (EXPECTED_CAUSAL_ONLY & names)
    assert "build_circuit" not in names
    assert "trace_path_subagent" not in names
    # Subagents keep the investigation tools, including the grafted ones.
    assert "inspect_feature" in names
    assert "get_upstream_features" in names
    assert "rank_segment_features" in names
    assert "report_findings" in names
