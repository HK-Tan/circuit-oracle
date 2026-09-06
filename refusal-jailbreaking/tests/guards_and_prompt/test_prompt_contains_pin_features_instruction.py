"""Assert new pin_features / pre_hypothesis instruction is in the rewritten prompt.

The rewritten ORACLE_SYSTEM_PROMPT must instruct the orchestrator to call
`pin_features` with a one-sentence `pre_hypothesis` per BUILD-pinned feature
before `batched_anchor_sweep`. The "no triage" phrasing is load-bearing: it
closes the agency-over-methodology failure mode documented in Section 2.2
where historical agents nominated only 20-42% of BUILD-pinned features for
anchor_pass.

The current prompt does NOT mention pin_features, pre_hypothesis, or
"no triage" anywhere, so the assertion below pins the rewritten wording.
"""
from __future__ import annotations

import pytest

from circuit_oracle.orchestrator import ORACLE_SYSTEM_PROMPT


def test_prompt_mentions_pin_features_tool():
    """Rewritten prompt must reference the `pin_features` tool by name."""
    assert "pin_features" in ORACLE_SYSTEM_PROMPT, (
        "Rewritten ORACLE_SYSTEM_PROMPT must mention `pin_features`. "
        "Without it the orchestrator has no instruction to call the new "
        "cognitive-commit tool."
    )


def test_prompt_mentions_pre_hypothesis_field():
    """Rewritten prompt must reference the `pre_hypothesis` field per feature."""
    assert "pre_hypothesis" in ORACLE_SYSTEM_PROMPT, (
        "Rewritten ORACLE_SYSTEM_PROMPT must mention `pre_hypothesis`. "
        "Per-feature prior-belief commitment is the cognitive piece that "
        "blocks the triage failure mode."
    )


def test_prompt_mentions_no_triage_rule():
    """Rewritten prompt must contain the load-bearing 'no triage' instruction."""
    assert "no triage" in ORACLE_SYSTEM_PROMPT.lower(), (
        "Rewritten ORACLE_SYSTEM_PROMPT must contain the phrase 'no triage' "
        "(case-insensitive). 'No triage: every "
        "feature in build_circuit must be pinned.'"
    )
