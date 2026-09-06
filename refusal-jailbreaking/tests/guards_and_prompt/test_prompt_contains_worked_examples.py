"""The anti-label-trust worked examples, taught without the answer key.

asked for two cases that demonstrate the "don't trust the autointerp label"
lesson, and named them by coordinate:

  - L17:F83241 (autointerp 'Code/technical snippets', real role:
    illicit-request detector)
  - L24:F91636 (autointerp 'el', real role: refusal-affect softener)

The prompt teaches both cases, but describes them generically rather than
citing the coordinates. That is deliberate and these tests pin it. L17:F83241
is the refusal mono-gate the causal runs are scored on FINDING, so naming it in
the system prompt would hand the oracle its own answer key and void the result.
The lesson transfers without the identifiers; the leak does not.

Earlier versions of this file asserted the coordinates appeared verbatim and
had failed since the code was imported, against a prompt that never cited them
in any repo. The requirement, not the prompt, was wrong.
"""
from __future__ import annotations

import re

from circuit_oracle.orchestrator import ORACLE_SYSTEM_PROMPT


def test_prompt_teaches_the_illicit_request_detector_case():
    """The L17:F83241 lesson: an off-topic label hiding a sensitivity detector."""
    assert "Anti-label-trust hardening" in ORACLE_SYSTEM_PROMPT
    assert "illicit-request detector" in ORACLE_SYSTEM_PROMPT, (
        "the prompt no longer teaches the case where a sensitivity / "
        "illicit-request detector sits behind an off-topic autointerp label"
    )


def test_prompt_teaches_the_refusal_affect_softener_case():
    """The L24:F91636 lesson: a fragment label hiding an affect softener."""
    assert "refusal-affect softener" in ORACLE_SYSTEM_PROMPT, (
        "the prompt no longer teaches the case where a meaningless subword "
        "fragment label hides a refusal-affect softener"
    )
    assert "fragment" in ORACLE_SYSTEM_PROMPT


def test_prompt_names_no_feature_coordinates():
    """The leak guard. No worked example may cite a concrete L:F coordinate.

    The causal runs are evaluated on which features the oracle pins, so any
    coordinate in the system prompt is a candidate handed over for free.
    """
    leaked = sorted(set(re.findall(r"L\d+:F\d+", ORACLE_SYSTEM_PROMPT)))
    assert leaked == [], (
        f"ORACLE_SYSTEM_PROMPT names feature coordinates {leaked}. Worked "
        "examples must stay generic: the refusal gate is what the run is "
        "supposed to discover."
    )
