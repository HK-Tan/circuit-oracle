"""DEFAULT_SUBAGENT_MODEL exists and points at the standard subagent backend.

Both trace_path_subagent and reinterpret_subagent read from this one constant,
so the subagent model can be swapped in a single place.

Updated 2026-07-28: the pinned value is now 'openai/gpt-oss-120b', not the
earlier 'claude-sonnet-4-6'. This test exists to make an accidental drift back
loud, since nothing else would fail.
"""
from __future__ import annotations

import pytest


def test_default_subagent_model_importable():
    """DEFAULT_SUBAGENT_MODEL must be importable from circuit_oracle.subagent."""
    from circuit_oracle.subagent import DEFAULT_SUBAGENT_MODEL  # noqa: F401


def test_default_subagent_model_value():
    """Constant must equal 'openai/gpt-oss-120b'."""
    from circuit_oracle.subagent import DEFAULT_SUBAGENT_MODEL

    assert DEFAULT_SUBAGENT_MODEL == "openai/gpt-oss-120b", (
        f"DEFAULT_SUBAGENT_MODEL must be 'openai/gpt-oss-120b', the standard "
        f"subagent backend. Got {DEFAULT_SUBAGENT_MODEL!r}"
    )


def test_default_subagent_model_is_priced_and_routable():
    """The fallback must be a model the cost and routing paths both know.

    A bare slug (no vendor prefix) is the trap here. saving.MODEL_PRICING keys
    the arm models by full slug, and compute_cost returns None for an
    unpriced model rather than raising, so a prefix slip would silently record
    every subagent call as costing nothing.
    """
    from circuit_oracle.subagent import DEFAULT_SUBAGENT_MODEL
    from circuit_oracle.saving import MODEL_PRICING, compute_cost
    from circuit_oracle.llm_client import provider_for

    assert DEFAULT_SUBAGENT_MODEL in MODEL_PRICING
    cost = compute_cost({"model": DEFAULT_SUBAGENT_MODEL, "input_tokens": 1_000_000})
    assert cost is not None and cost > 0
    # Pinned to OpenRouter (for Groq) regardless of the run's gateway.
    assert provider_for(DEFAULT_SUBAGENT_MODEL, "kilo") == "openrouter"


def test_default_subagent_model_is_str():
    """Type check: constant must be a plain string."""
    from circuit_oracle.subagent import DEFAULT_SUBAGENT_MODEL

    assert isinstance(DEFAULT_SUBAGENT_MODEL, str), (
        f"DEFAULT_SUBAGENT_MODEL must be str, got {type(DEFAULT_SUBAGENT_MODEL).__name__}"
    )
