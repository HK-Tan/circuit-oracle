"""The task-keyed orchestrator prompt registry and the restored generic prompt.

The registry (orchestrator.resolve_system_prompt) exists so no task can
inherit another task's prompt by accident, the failure that put the
hallucination rubric in front of the published probe runs' successor script.
GENERIC_ORACLE_SYSTEM_PROMPT is the blob-level restoration of the prompt those
runs actually used (blob 8d84b6b), and
generic_oracle_system_prompt() parameterizes exactly its subject-model block.
"""

from __future__ import annotations

import pytest

from circuit_oracle import orchestrator as orch

from conftest import N_LAYERS, make_ctx, make_graph


class _Stop(Exception):
    """Raised by the fake client to end the run at the first LLM call."""


class _CapturingClient:
    def __init__(self):
        self.kwargs: dict | None = None

    def create_message(self, **kwargs):
        self.kwargs = kwargs
        raise _Stop()


def _run(ctx, client, **kwargs):
    with pytest.raises(_Stop):
        orch.run_circuit_oracle(ctx, client, "q", verbose=False, **kwargs)
    assert client.kwargs is not None
    return client.kwargs


# ---------------------------------------------------------------------------
# The restored generic prompt
# ---------------------------------------------------------------------------


def test_identity_round_trip_is_what_restored_means():
    """On the original subject the parameterization must be a byte-level no-op."""
    assert (
        orch.generic_oracle_system_prompt(36, "Qwen3-4B")
        == orch.GENERIC_ORACLE_SYSTEM_PROMPT
    )


def test_parameterization_rewrites_only_the_subject_block():
    text = orch.generic_oracle_system_prompt(26, "gemma-2-2b")
    assert "(gemma-2-2b)" in text
    assert "layer=26" in text
    assert "(e.g. L25)" in text
    assert "L25:F23398" in text
    assert "Qwen3-4B" not in text
    assert "layer=36" not in text
    assert "L35" not in text
    # The embedding-node instruction is layer-agnostic and must survive.
    assert "Use layer=0, features=[]" in text


def test_generic_prompt_matches_the_submitted_fingerprint():
    """102/102 archived probe reports echo this response format and zero
    contain the hallucination header. The constant must keep both properties."""
    text = orch.GENERIC_ORACLE_SYSTEM_PROMPT
    assert "**Analysis:**" in text
    assert "**Confidence:**" in text
    assert "Hallucination score" not in text
    for phase in ("SCOUT", "DISPATCH", "MERGE", "BUILD", "ANALYZE"):
        assert phase in text


def test_bad_parameters_raise():
    with pytest.raises(ValueError, match="n_layers"):
        orch.generic_oracle_system_prompt(1, "x")
    with pytest.raises(ValueError, match="subject_model"):
        orch.generic_oracle_system_prompt(36, "")


# ---------------------------------------------------------------------------
# resolve_system_prompt
# ---------------------------------------------------------------------------


def test_refusal_and_hallucination_resolve_to_their_constants():
    assert orch.resolve_system_prompt("refusal") is orch.ORACLE_SYSTEM_PROMPT
    assert (
        orch.resolve_system_prompt("hallucination")
        is orch.OBSERVATIONAL_SYSTEM_PROMPT
    )


def test_probes_requires_the_subject_parameters():
    with pytest.raises(ValueError, match="probes"):
        orch.resolve_system_prompt("probes")
    resolved = orch.resolve_system_prompt(
        "probes", n_layers=26, subject_model="gemma-2-2b"
    )
    assert resolved == orch.generic_oracle_system_prompt(26, "gemma-2-2b")


def test_elk_demands_an_explicit_prompt():
    with pytest.raises(ValueError, match="system_prompt"):
        orch.resolve_system_prompt("elk")


def test_unknown_task_raises():
    with pytest.raises(KeyError, match="unknown task"):
        orch.resolve_system_prompt("spurious")


# ---------------------------------------------------------------------------
# The task kwarg on run_circuit_oracle
# ---------------------------------------------------------------------------


def test_task_probes_resolves_through_ctx():
    """The runner passes only task="probes"; layer count and subject name come
    from the graph cfg and the Neuronpedia model id already on ctx."""
    ctx = make_ctx()
    kwargs = _run(ctx, _CapturingClient(), mode="observational", task="probes")
    expected = orch.generic_oracle_system_prompt(N_LAYERS, "tiny-toy")
    assert kwargs["system"] == expected
    assert kwargs["system"] != orch.OBSERVATIONAL_SYSTEM_PROMPT


def test_task_refusal_is_identical_to_the_legacy_causal_default():
    # 36 layers: the causal prompt is written for Qwen3-4B and the resolver
    # rejects any other depth (see the test below).
    ctx = make_ctx(make_graph(n_layers=orch.FIXED_PROMPT_N_LAYERS))
    kwargs = _run(ctx, _CapturingClient(), mode="causal", task="refusal")
    # Both routes deliver the causal prompt reconciled against the offered tool
    # surface, so compare after the same reconciliation rather than against the
    # raw constant. The point of the test is that task="refusal" and the legacy
    # causal default resolve to the same prompt, and that still holds.
    from circuit_oracle.tool_schemas import apply_tool_exclusions_to_prompt
    expected = apply_tool_exclusions_to_prompt(
        orch.ORACLE_SYSTEM_PROMPT, [t["name"] for t in kwargs["tools"]]
    )
    assert kwargs["system"] == expected


@pytest.mark.parametrize("task", ["refusal", "hallucination"])
def test_fixed_prompts_reject_a_subject_of_another_depth(task):
    """Both fixed prompts quote the 36-layer convention (`layer=36` output
    nodes, `L35` examples). Handing one to a 26-layer Gemma would name layers
    that do not exist in its graph, so it raises instead of shipping."""
    with pytest.raises(ValueError, match="36-layer subject"):
        orch.resolve_system_prompt(task, n_layers=26, subject_model="gemma-2-2b")

    # Unknown depth (no graph cfg) still resolves: nothing contradicts the prompt.
    assert orch.resolve_system_prompt(task, n_layers=None) in (
        orch.ORACLE_SYSTEM_PROMPT,
        orch.OBSERVATIONAL_SYSTEM_PROMPT,
    )


def test_task_mode_mismatch_raises_before_any_work():
    with pytest.raises(ValueError, match="runs mode"):
        orch.run_circuit_oracle(None, None, "q", mode="observational", task="refusal")


def test_unknown_task_kwarg_raises_before_any_work():
    with pytest.raises(KeyError, match="unknown task"):
        orch.run_circuit_oracle(None, None, "q", task="spurious")


def test_explicit_system_prompt_wins_over_task():
    """The ELK pattern: the entry script passes its own prompt and the task
    key is provenance only."""
    ctx = make_ctx()
    kwargs = _run(
        ctx,
        _CapturingClient(),
        mode="observational",
        task="probes",
        system_prompt="TABOO PROMPT",
    )
    assert kwargs["system"] == "TABOO PROMPT"


# ---------------------------------------------------------------------------
# Provenance in the return dict
# ---------------------------------------------------------------------------


class _FakeUsage:
    input_tokens = 1
    output_tokens = 1


class _TextBlock:
    type = "text"
    text = "done"


class _FinalResponse:
    content = [_TextBlock()]
    usage = _FakeUsage()
    stop_reason = "end_turn"


class _OneTurnClient:
    def create_message(self, **kwargs):
        return _FinalResponse()


def test_result_carries_task_mode_and_the_resolved_prompt():
    """An earlier probe prompt had to be reconstructed by blob-level git
    archaeology because nothing persisted it. The return dict now carries it."""
    ctx = make_ctx()
    result = orch.run_circuit_oracle(
        ctx, _OneTurnClient(), "q", mode="observational", task="probes", verbose=False
    )
    assert result["task"] == "probes"
    assert result["mode"] == "observational"
    assert result["system_prompt_resolved"] == orch.generic_oracle_system_prompt(
        N_LAYERS, "tiny-toy"
    )
