"""apply_tool_exclusions_to_prompt: the prompt must match the tools on offer.

``excluded_tools`` only ever filtered the JSON schema list. The system prompts are
static text, so an excluded tool stayed advertised and the agent was told to call
something it was never handed. refusal-arm2 and probes-arm2 exclude
inspect_feature while the causal and generic prompts instruct the agent to call
it; the ELK arms exclude trace_path_subagent and, on the open protocol,
get_candidate_vote_tally.

The reconciliation deletes tool-inventory bullets and then appends an
authoritative block for whatever prose it cannot safely rewrite. Deletion is the
dangerous half: prompts mention tools in four structurally different ways and only
one of them is this tool's own entry. Every test below is written against the real
prompts rather than synthetic strings, because the shapes are what make the rule
safe and a synthetic fixture would drift away from them.
"""
from __future__ import annotations

import pytest

from circuit_oracle import orchestrator as orch
from circuit_oracle.subagent import SUBAGENT_SYSTEM_PROMPT_TEMPLATE
from circuit_oracle.tool_schemas import (
    ALL_KNOWN_TOOL_NAMES,
    RETIRED_TOOL_NAMES,
    TOOLS,
    _bullet_subject,
    _bullet_subject_span,
    apply_tool_exclusions_to_prompt,
    build_orchestrator_tools,
)

ALL_OFFERED = [t["name"] for t in TOOLS]


def _without(*names):
    return [n for n in ALL_OFFERED if n not in names]


# ---------------------------------------------------------------------------
# _bullet_subject: which bullets are a tool's own inventory entry
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "line, expected, why",
    [
        (
            "- `inspect_feature(layer, feature_idx)`, Neuronpedia label, top activating examples.",
            "inspect_feature",
            "inventory entry: the bullet opens with the tool name",
        ),
        (
            "   - Call `inspect_feature` to get the semantic label and promoted tokens.",
            None,
            "instruction, not an entry: opens with a capitalized verb",
        ),
        (
            "- Neuronpedia labels and inspect_feature top prompts are training-data signals.",
            None,
            "advice: opens with a capitalized word",
        ),
        (
            "- trace_path_subagent: dispatch a subagent ... calls get_upstream_features and "
            "inspect_feature across multiple hops.",
            "trace_path_subagent",
            "another tool's entry that merely mentions inspect_feature",
        ),
        (
            "- `usability` is not a tool name at all.",
            "usability",
            "returns the leading identifier whether or not it is a tool; the "
            "membership check against the unavailable set is what filters, so a "
            "lowercase non-tool subject is harmless",
        ),
        ("not a bullet at all", None, "only list items are candidates"),
    ],
)
def test_bullet_subject_classifies_the_four_shapes(line, expected, why):
    assert _bullet_subject(line) == expected, why


# ---------------------------------------------------------------------------
# _bullet_subject_span: co-subjects vs cross-references
# ---------------------------------------------------------------------------


def test_subject_span_stops_at_the_description():
    """A tool named in the description is a cross-reference, not a co-subject.

    This is the distinction that decides whether the open-ELK tally entry is
    deleted. Requiring every tool named anywhere on the line to be unavailable
    kept that entry alive because it cross-references rank_segment_features,
    which is still offered.
    """
    line = (
        "- get_candidate_vote_tally(min_layer=20): tallies votes against the menu. "
        "Useful when rank_segment_features alone is ambiguous."
    )
    span = _bullet_subject_span(line)
    assert "get_candidate_vote_tally" in span
    assert "rank_segment_features" not in span


def test_subject_span_keeps_genuine_co_subjects():
    line = "- `tool_a` / `tool_b`, both do the same thing."
    span = _bullet_subject_span(line)
    assert "tool_a" in span and "tool_b" in span


# ---------------------------------------------------------------------------
# The real prompts
# ---------------------------------------------------------------------------


def test_refusal_arm2_drops_the_entry_and_keeps_the_instruction():
    """refusal-arm2. The causal prompt carries the entry and the instruction."""
    out = apply_tool_exclusions_to_prompt(
        orch.ORACLE_SYSTEM_PROMPT, _without("inspect_feature")
    )

    assert "- `inspect_feature(layer, feature_idx)`. Neuronpedia label" not in out, (
        "inspect_feature's own inventory entry survived"
    )
    assert "Call `inspect_feature` to get the semantic label" in out, (
        "an imperative sentence was deleted; only inventory entries may be"
    )
    assert "must not be called: `inspect_feature`" in out


def test_probes_arm2_keeps_advice_and_other_tools_entries():
    """probes-arm2 runs the generic prompt; the observational prompt carries the
    remaining two shapes. Both mention inspect_feature and both must survive."""
    for prompt in (
        orch.OBSERVATIONAL_SYSTEM_PROMPT,
        orch.generic_oracle_system_prompt(26, "gemma-2-2b"),
    ):
        out = apply_tool_exclusions_to_prompt(prompt, _without("inspect_feature"))
        assert "- inspect_feature: look up" not in out, "its own entry survived"
        assert "- trace_path_subagent:" in out, (
            "another tool's entry was deleted because it mentions inspect_feature"
        )
        if "Neuronpedia labels and inspect_feature top prompts" in prompt:
            assert "Neuronpedia labels and inspect_feature top prompts" in out, (
                "advice prose was deleted"
            )


def test_open_elk_tally_entry_is_dropped_despite_its_cross_reference():
    """The defect codex caught: a cross-reference to an offered tool kept an
    excluded tool's own entry alive on the open-ELK arms."""
    # The ELK prompts live in the entry scripts, not the package, so put that
    # directory on the path rather than skipping. Skipping here would have hidden
    # exactly the defect this test exists for.
    import sys
    from pathlib import Path

    scripts = Path(__file__).resolve().parents[1] / "secret-elicitation" / "scripts"
    assert scripts.is_dir(), f"ELK entry scripts not found at {scripts}"
    sys.path.insert(0, str(scripts))
    try:
        from run_oracle_on_taboo import TABOO_SYSTEM_PROMPT as prompt
    finally:
        sys.path.remove(str(scripts))
    assert "get_candidate_vote_tally" in prompt, (
        "the taboo prompt no longer advertises get_candidate_vote_tally; this "
        "test's premise is gone, re-point it at whatever the open arms exclude"
    )

    out = apply_tool_exclusions_to_prompt(prompt, _without("get_candidate_vote_tally"))

    assert "- get_candidate_vote_tally" not in out, (
        "the excluded tool's inventory entry survived because its description "
        "cross-references rank_segment_features, which is still offered"
    )
    assert "rank_segment_features" in out, "the cross-referenced offered tool was lost"


def test_nothing_changes_when_every_tool_is_offered():
    for prompt in (
        orch.ORACLE_SYSTEM_PROMPT,
        orch.OBSERVATIONAL_SYSTEM_PROMPT,
        orch.generic_oracle_system_prompt(26, "gemma-2-2b"),
    ):
        assert apply_tool_exclusions_to_prompt(prompt, ALL_OFFERED) == prompt


def test_unmentioned_exclusions_produce_no_block():
    """Only tools the prompt actually advertises are named.

    The subagent blocks build_circuit and the intervention tools permanently. Its
    template never mentions them, so it must not carry a block about them.
    """
    template = SUBAGENT_SYSTEM_PROMPT_TEMPLATE
    out = apply_tool_exclusions_to_prompt(template, ["inspect_feature", "get_upstream_features"])
    assert "build_circuit" not in out.split("Tools not available in this run")[-1]


def test_retired_tools_are_absent_from_the_offered_surface():
    assert RETIRED_TOOL_NAMES <= ALL_KNOWN_TOOL_NAMES
    assert not (RETIRED_TOOL_NAMES & set(ALL_OFFERED))
    assert not (RETIRED_TOOL_NAMES & {t["name"] for t in build_orchestrator_tools()})


# ---------------------------------------------------------------------------
# The override block, asserted without calling the function that writes it
# ---------------------------------------------------------------------------


def test_override_block_names_every_unavailable_mentioned_tool():
    out = apply_tool_exclusions_to_prompt(
        orch.ORACLE_SYSTEM_PROMPT, _without("inspect_feature", "get_top_logits")
    )
    header = "## Tools not available in this run"
    assert out.count(header) == 1
    block = out.split(header, 1)[1]
    for name in ("inspect_feature", "get_top_logits"):
        assert f"`{name}`" in block, f"{name} missing from the override block"
    # The block has to actually override, not merely mention.
    assert "overrides any earlier text" in block
    assert "must not be called" in block
