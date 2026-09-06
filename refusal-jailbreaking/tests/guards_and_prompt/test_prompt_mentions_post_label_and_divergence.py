"""Assert post_label / divergence instruction is in the rewritten prompt.

The rewritten ORACLE_SYSTEM_PROMPT must instruct the orchestrator to use the
`post_label` and `divergence` fields (from the REASSESS subagent's triple-label
record, see Section 2.4) when grouping features into supernode tuples. These
fields carry the post-intervention judgment and the 3-way autointerp/pre/post
divergence flag, which are the load-bearing artifact for the paper's
`autointerp_and_pre` count.

The current prompt does NOT mention post_label or divergence anywhere, so this
assertion below pins the rewritten wording.
"""
from __future__ import annotations

import pytest

from circuit_oracle.orchestrator import ORACLE_SYSTEM_PROMPT


def test_prompt_mentions_post_label_field():
    """Rewritten prompt must reference the `post_label` field by name."""
    assert "post_label" in ORACLE_SYSTEM_PROMPT, (
        "Rewritten ORACLE_SYSTEM_PROMPT must mention `post_label`. "
        "The agent is instructed to use the "
        "post_label and divergence fields when grouping features into "
        "supernode tuples."
    )


def test_prompt_mentions_divergence_field():
    """Rewritten prompt must reference the `divergence` field by name."""
    assert "divergence" in ORACLE_SYSTEM_PROMPT, (
        "Rewritten ORACLE_SYSTEM_PROMPT must mention `divergence`. "
        "The agent is instructed to use the "
        "post_label and divergence fields when grouping features into "
        "supernode tuples."
    )
