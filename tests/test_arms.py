"""The arm registry (circuit_oracle.arms).

The registry is the single source of a run's identity in the ablation grid:
16 arms across the three tasks, each owning its orchestrator, subagent, tool
surface, and discovery-annotation mode. These tests pin the grid's shape so the
registry and the runners cannot drift apart silently.
"""

from __future__ import annotations

import pytest

from circuit_oracle.arms import (
    ARMS,
    ELK_CLOSED_EXCLUDED_TOOLS,
    ELK_OPEN_EXCLUDED_TOOLS,
    NO_SUBAGENT,
    arm_names,
    get_arm,
    resolve_arm,
)
from circuit_oracle.llm_client import shorten_model_name
from circuit_oracle.orchestrator import TASK_MODES
from circuit_oracle.tool_schemas import TOOLS


EXPECTED_ARMS = {
    "probes-arm1", "probes-arm2", "probes-arm3", "probes-arm4", "probes-arm5",
    "elk-arm1-closed", "elk-arm1-open",
    "elk-arm2-closed", "elk-arm2-open",
    "elk-arm3-closed", "elk-arm3-open",
    "refusal-arm1", "refusal-arm2", "refusal-arm3", "refusal-arm4", "refusal-arm5",
}


def test_registry_covers_the_sixteen_arms():
    assert set(ARMS) == EXPECTED_ARMS


def test_keys_match_spec_names():
    for name, spec in ARMS.items():
        assert spec.name == name


def test_unknown_arm_raises_listing_options():
    with pytest.raises(KeyError, match="refusal-arm1"):
        get_arm("refusal-arm9")


def test_excluded_tool_names_all_exist():
    """A stale name in an exclusion list is a silent no-op downstream (plain
    set difference), which is how the dead get_diff_specific_features entry
    survived in the ELK scripts. The registry must never carry one."""
    known = {t["name"] for t in TOOLS}
    for spec in ARMS.values():
        assert set(spec.excluded_tools) <= known, spec.name


def test_arm_tasks_and_modes_agree_with_the_prompt_registry():
    for spec in ARMS.values():
        assert TASK_MODES[spec.task] == spec.mode, spec.name


def test_refusal_arm2_is_the_two_flag_label_leak_fix():
    spec = get_arm("refusal-arm2")
    assert spec.excluded_tools == ("inspect_feature",)
    assert spec.annotation == "shift_only"


def test_probes_arm2_drops_inspect_only():
    spec = get_arm("probes-arm2")
    assert spec.excluded_tools == ("inspect_feature",)
    # No causal discovery pass on an observational task, so no annotation
    # mode is needed there.
    assert spec.annotation == "full"


def test_oneshot_arms_are_flagged():
    oneshot = {name for name, spec in ARMS.items() if spec.pipeline == "oneshot"}
    assert oneshot == {"probes-arm3", "refusal-arm3"}


def test_elk_arms_have_no_subagent_layer():
    for name in arm_names(task="elk"):
        assert get_arm(name).subagent_model is None, name


# ── ELK protocols ────────────────────────────────────────────────────────────
# Closed and open are separate runs with separate scripts, prompts, and tool
# surfaces, so each orchestrator is two arms and a run has to be able to say
# which protocol produced it.

def test_each_elk_orchestrator_runs_both_protocols():
    by_protocol = {"closed": set(), "open": set()}
    for name in arm_names(task="elk"):
        spec = get_arm(name)
        by_protocol[spec.protocol].add(spec.orchestrator_model)
    assert by_protocol["closed"] == by_protocol["open"]
    assert len(by_protocol["closed"]) == 3


def test_protocol_is_elk_only_and_matches_the_name_suffix():
    for name, spec in ARMS.items():
        if spec.task == "elk":
            assert spec.protocol in ("closed", "open"), name
            assert name.endswith(f"-{spec.protocol}"), name
        else:
            assert spec.protocol is None, name


def test_open_protocol_hides_the_candidate_menu_tool():
    """get_candidate_vote_tally stems top_logits against the 20-word menu, so
    leaving it enabled in open mode would hand the oracle the closed-mode
    answer key through a tool call."""
    assert "get_candidate_vote_tally" in ELK_OPEN_EXCLUDED_TOOLS
    assert "get_candidate_vote_tally" not in ELK_CLOSED_EXCLUDED_TOOLS
    for name in arm_names(task="elk", protocol="open"):
        assert get_arm(name).excluded_tools == ELK_OPEN_EXCLUDED_TOOLS, name
    for name in arm_names(task="elk", protocol="closed"):
        assert get_arm(name).excluded_tools == ELK_CLOSED_EXCLUDED_TOOLS, name


def test_no_subagent_placeholder_survives_the_saving_path():
    """The ELK runners record NO_SUBAGENT instead of a real model name, because
    saving.py puts config.subagent_model in oracle_result.json, the report
    header, and the run directory name. It must therefore be a non-empty string
    shorten_model_name accepts, and it must not look like a real model."""
    assert shorten_model_name(NO_SUBAGENT) == NO_SUBAGENT
    assert "/" not in NO_SUBAGENT
    assert NO_SUBAGENT not in {spec.orchestrator_model for spec in ARMS.values()}


def test_no_subagent_is_only_safe_because_the_dispatch_tool_is_excluded():
    """NO_SUBAGENT is never a usable model ID, so it would fail at call time if
    anything dispatched. Nothing can: subagent_model reaches only
    trace_path_subagent, which every no-subagent arm excludes."""
    for name, spec in ARMS.items():
        if spec.subagent_model is None:
            assert "trace_path_subagent" in spec.excluded_tools, name


def test_both_elk_protocols_drop_the_output_side_tools():
    """The taboo LoRA steers its own logits away from the secret, so the
    output-side tools are misleading in either protocol."""
    for tools in (ELK_CLOSED_EXCLUDED_TOOLS, ELK_OPEN_EXCLUDED_TOOLS):
        assert {"get_top_logits", "get_top_features"} <= set(tools)
        assert "trace_path_subagent" in tools


# ── resolve_arm, the entry-script gate ───────────────────────────────────────

def test_resolve_arm_accepts_a_matching_arm():
    assert resolve_arm("refusal-arm1", task="refusal").name == "refusal-arm1"
    spec = resolve_arm("elk-arm2-open", task="elk", protocol="open")
    assert spec.name == "elk-arm2-open"


def test_resolve_arm_rejects_a_foreign_task():
    with pytest.raises(ValueError, match="refusal-only"):
        resolve_arm("probes-arm1", task="refusal")


def test_resolve_arm_rejects_the_wrong_protocol():
    """The two ELK runners share a registry, and this is what stops the open
    runner from writing results labelled with a closed arm."""
    with pytest.raises(ValueError, match="closed"):
        resolve_arm("elk-arm1-closed", task="elk", protocol="open")


def test_resolve_arm_rejects_a_oneshot_arm_on_an_agentic_only_runner():
    # Default pipeline="agentic": an entry script that serves only the loop
    # still rejects arm 3.
    with pytest.raises(ValueError, match="serves only"):
        resolve_arm("refusal-arm3", task="refusal")


def test_resolve_arm_accepts_oneshot_when_the_runner_serves_it():
    # run_all.py and run_oracle_on_probes.py pass both pipelines,
    # because one script now dispatches on arm.pipeline.
    spec = resolve_arm("refusal-arm3", task="refusal",
                       pipeline=("agentic", "oneshot"))
    assert spec.pipeline == "oneshot"
    spec = resolve_arm("probes-arm1", task="probes",
                      pipeline=("agentic", "oneshot"))
    assert spec.pipeline == "agentic"


def test_resolve_arm_dual_pipeline_still_rejects_foreign_task():
    with pytest.raises(ValueError, match="probes-only|task 'probes'"):
        resolve_arm("probes-arm3", task="refusal",
                    pipeline=("agentic", "oneshot"))


def test_resolve_arm_reports_unknown_names_without_key_error_quoting():
    with pytest.raises(ValueError, match="unknown arm 'elk-arm1'") as e:
        resolve_arm("elk-arm1", task="elk", protocol="closed")
    # The retired pre-split name should point at its replacements.
    assert "elk-arm1-closed" in str(e.value)


def test_arm_names_filters_by_task_and_protocol():
    assert arm_names(task="probes") == [
        "probes-arm1", "probes-arm2", "probes-arm3", "probes-arm4", "probes-arm5",
    ]
    assert arm_names(task="elk", protocol="closed") == [
        "elk-arm1-closed", "elk-arm2-closed", "elk-arm3-closed",
    ]
    assert arm_names() == sorted(ARMS)


def test_orchestrators_are_the_three_verified_slugs():
    """Exact OpenRouter IDs from model-ids.md (verified live 2026-07-26)."""
    orchestrators = {spec.orchestrator_model for spec in ARMS.values()}
    assert orchestrators == {
        "minimax/minimax-m3",
        "openai/gpt-5.6-terra",
        "google/gemma-4-31b-it",
    }


def test_non_elk_arms_use_the_standard_subagent():
    for spec in ARMS.values():
        if not spec.name.startswith("elk-"):
            assert spec.subagent_model == "openai/gpt-oss-120b", spec.name
