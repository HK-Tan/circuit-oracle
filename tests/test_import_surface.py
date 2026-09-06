"""The import surface the three entry-script threads depend on.

merge-specs.md spec E section 0 lists exactly what the host scripts import from
the merged package. Nothing else. This file is the cheap early-warning that a
later refactor removed one of them, since the entry scripts themselves cannot be
run here (they need a GPU and model weights).
"""

from __future__ import annotations

import importlib
import inspect

import pytest


TOP_LEVEL = [
    "ToolContext",       # probes runner, both taboo runners
    "RunConfig",         # probes runner, both taboo runners
    "LLMClient",         # both runners plus both taboo evals
    "run_circuit_oracle",
    "save_run_results",
]

AUTOINTERP = [
    "FeatureCache",      # 9 of the 10 secret_discovery scripts
    "AutointerpStore",
    "AutointerpConfig",
    "describe_feature",
]


@pytest.mark.parametrize("name", TOP_LEVEL)
def test_top_level_exports(name):
    mod = importlib.import_module("circuit_oracle")
    assert hasattr(mod, name), f"circuit_oracle.{name} is gone"


@pytest.mark.parametrize("name", AUTOINTERP)
def test_autointerp_exports(name):
    mod = importlib.import_module("circuit_oracle.autointerp")
    assert hasattr(mod, name)


def test_llm_client_is_importable_by_submodule_path():
    """Two secret_discovery scripts import it this way, not from the top level."""
    from circuit_oracle.llm_client import LLMClient  # noqa: F401


def test_both_orchestrator_prompts_are_exported():
    """Both prompts stay exported. OBSERVATIONAL_SYSTEM_PROMPT is the dropped
    hallucination thread's prompt under its own task key. The published task-1
    runs used the restored generic prompt (GENERIC_ORACLE_SYSTEM_PROMPT), not
    this one (established blob-level 2026-07-26); an earlier version of this
    docstring claimed otherwise and was wrong."""
    import circuit_oracle

    assert isinstance(circuit_oracle.ORACLE_SYSTEM_PROMPT, str)
    assert isinstance(circuit_oracle.OBSERVATIONAL_SYSTEM_PROMPT, str)
    assert circuit_oracle.ORACLE_SYSTEM_PROMPT != circuit_oracle.OBSERVATIONAL_SYSTEM_PROMPT
    # The causal prompt drives the intervention phases, the observational one
    # must not mention them, or an observational run gets nudged toward tools it
    # was not given.
    for phase in ("PIN", "ANCHOR", "SUPERNODE"):
        assert phase in circuit_oracle.ORACLE_SYSTEM_PROMPT
    lowered = circuit_oracle.OBSERVATIONAL_SYSTEM_PROMPT
    for tool in ("intervene_feature", "batched_anchor_sweep", "batched_supernode_sweep"):
        assert tool not in lowered


def test_elk_tools_module_does_not_drag_in_the_causal_stack():
    """elk_tools is deliberately its own module. It owns the only import of the
    local autointerp stack, and the causal path must never pull that in."""
    import circuit_oracle.elk_tools as elk

    src = inspect.getsource(elk)
    assert "from .autointerp import" in src
    assert "circuit_tracer" not in src


def test_save_run_results_keeps_the_call_shape_every_host_script_uses():
    """All three entry scripts call it as

        save_run_results(result, cfg, prompt=..., base_dir=...)

    which is 2 positional plus 2 keyword (spec D section 4.2). The first three
    parameters must stay in that order, since the first two arrive positionally.
    """
    from circuit_oracle import save_run_results

    params = list(inspect.signature(save_run_results).parameters)
    assert params[:3] == ["result", "config", "prompt"]
    assert "base_dir" in params
