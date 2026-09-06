"""Assert obsolete methodology language has been stripped from the prompt.

The rewrite must remove every line that delegated methodology to the agent.
The 4-scale batched anchor sweep replaces manual escalation, so the
monotonicity rule, "anchor_pass exactly once", and "escalate -2 to -3"
instructions no longer apply.

Both ASCII (`->` / `to`) and unicode arrow (`→`) forms of the escalation
phrasing are checked, since the current prompt uses the unicode arrow but
either form would re-introduce the bug.

Fails if any of these phrases comes back into the prompt.
"""
from __future__ import annotations

import pytest

from circuit_oracle.orchestrator import ORACLE_SYSTEM_PROMPT


def test_prompt_drops_monotonicity_rule():
    """The monotonicity rule is now harness-enforced; prompt must not mention it."""
    assert "monotonicity" not in ORACLE_SYSTEM_PROMPT.lower(), (
        "ORACLE_SYSTEM_PROMPT still mentions 'monotonicity'. The 4-scale "
        "batched anchor sweep makes the monotonicity rule redundant; "
        "the current prompt must not carry it."
    )


def test_prompt_drops_anchor_pass_exactly_once_instruction():
    """`anchor_pass` is replaced by argless `batched_anchor_sweep`; the
    'exactly once' agent-side ordering instruction is obsolete."""
    assert "anchor_pass exactly once" not in ORACLE_SYSTEM_PROMPT, (
        "ORACLE_SYSTEM_PROMPT still says 'anchor_pass exactly once'. "
        "The new chain (pin_features -> batched_anchor_sweep) makes this "
        "instruction obsolete."
    )


def test_prompt_drops_escalation_ascii_arrow():
    """ASCII form '-2 to -3' of the manual escalation rule must be gone."""
    assert "escalate -2 to -3" not in ORACLE_SYSTEM_PROMPT.lower(), (
        "ORACLE_SYSTEM_PROMPT still contains the ASCII escalation phrase "
        "'escalate -2 to -3'. The 4-scale automatic sweep replaces this."
    )


def test_prompt_drops_escalation_unicode_arrow():
    """Unicode arrow form '-2 → -3' of the manual escalation rule must be gone."""
    assert "escalate -2 → -3" not in ORACLE_SYSTEM_PROMPT.lower() \
        and "-2 → -3" not in ORACLE_SYSTEM_PROMPT, (
        "ORACLE_SYSTEM_PROMPT still contains the unicode escalation phrase "
        "'-2 → -3'. Strip every form of manual escalation guidance "
        "."
    )


def test_prompt_drops_reinterpret_subagent_as_callable():
    """`reinterpret_subagent` is now harness-dispatched, not agent-callable."""
    assert "reinterpret_subagent" not in ORACLE_SYSTEM_PROMPT, (
        "ORACLE_SYSTEM_PROMPT still mentions 'reinterpret_subagent'. "
        "REASSESS is auto-dispatched by the "
        "harness from inside `batched_anchor_sweep`; the agent should no "
        "longer treat reinterpret_subagent as a callable."
    )


def test_prompt_drops_phase_2_numbering():
    """Old phase numbering ('Phase 2') is removed per Section 2.5 Strip list."""
    assert "Phase 2" not in ORACLE_SYSTEM_PROMPT, (
        "ORACLE_SYSTEM_PROMPT still mentions 'Phase 2'. The old "
        "phase-numbering scheme is obsolete under the three-tool chain "
        "."
    )


def test_prompt_drops_escalate_factor_guidance():
    """The 'escalate factor' methodology language is owned by the harness now."""
    assert "escalate factor" not in ORACLE_SYSTEM_PROMPT, (
        "ORACLE_SYSTEM_PROMPT still contains 'escalate factor'. The 4-scale "
        "batched anchor sweep owns scale escalation; the agent should no "
        "longer carry this methodology guidance."
    )


def test_prompt_drops_scale_sweep_guidance():
    """The 'scale sweep' methodology phrasing is harness-owned now."""
    assert "scale sweep" not in ORACLE_SYSTEM_PROMPT.lower(), (
        "ORACLE_SYSTEM_PROMPT still contains 'scale sweep'. The harness "
        "performs the 4-scale sweep server-side inside batched_anchor_sweep; "
        "the agent should no longer carry this methodology language "
        "."
    )
