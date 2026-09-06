"""Arm 3 (gemma-4-31b-it) must route to Cerebras, not to whatever is default.

Measured 2026-07-28 on one prompt, ~260 completion tokens each:
kilo 22.0 tok/s, openrouter default 34.2 (CoreWeave), cerebras 389.0,
sambanova 47.1. Arm 3 was the slowest arm in the pilot (397s open) and this is
why. Both properties below are silent if broken: the run still completes, just
6-17x slower, and nothing in the output says which host served it.
"""
from circuit_oracle.llm_client import (
    OPENROUTER_MODEL_ROUTING, model_pins, provider_for, openrouter_provider_routing,
)

GEMMA = "google/gemma-4-31b-it"


def test_gemma4_is_pinned_to_openrouter():
    """The routing object is dropped on non-OpenRouter endpoints, so without
    this pin a --provider kilo run keeps gemma-4 on kilo at 22 tok/s and the
    ordering below never applies."""
    assert model_pins()[GEMMA] == "openrouter"
    assert provider_for(GEMMA, "kilo") == "openrouter"


def test_gemma4_prefers_cerebras_then_sambanova():
    r = openrouter_provider_routing(GEMMA)
    assert r["order"] == ["cerebras", "sambanova"]
    assert r["require_parameters"] is True


def test_gemma4_keeps_an_escape_valve_under_throttle():
    """allow_fallbacks must stay True.

    Reverted from False on 2026-07-28 before arm 3 ran, on the evidence already
    recorded for gpt-oss-120b: a restricted order at 37 concurrent put 62% of
    task-1 runs into a 429, and the retry ladder is too short for a sustained
    throttle. Arm 3 runs last, so all 64 workers hit Gemma 4 at once. Order
    still expresses the speed preference; this only stops a throttle from
    turning into missing runs.
    """
    assert OPENROUTER_MODEL_ROUTING[GEMMA]["allow_fallbacks"] is True


def test_gemma4_is_priced_at_the_host_it_prefers():
    """Cost must not be recorded at the old cheapest-endpoint rate once the
    model is ordered onto a dearer host, or arm 3's ledger row undercounts."""
    from circuit_oracle.saving import MODEL_PRICING
    assert MODEL_PRICING[GEMMA]["input"] == 0.99    # Cerebras, not 0.14
    assert MODEL_PRICING[GEMMA]["output"] == 1.49   # Cerebras, not 0.40
