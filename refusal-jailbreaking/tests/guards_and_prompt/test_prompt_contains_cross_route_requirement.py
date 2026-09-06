"""Assert the cross-route supernode requirement is in the prompt.

Round 1 of `batched_supernode_sweep` must include at least one tuple
combining features from distinct suppression routes. The five canonical
routes from the spec are: negation, affect, sensitivity-precursor,
opener-substitution, and topic-routing.

The test passes if the prompt either says "distinct suppression routes"
verbatim, or names at least 3 of the 5 routes in the route vocabulary --
either form is sufficient signal that the cross-route requirement made it
into the prompt rewrite.

Fails if the cross-route instruction leaves the prompt.
"""
from __future__ import annotations

import pytest

from circuit_oracle.orchestrator import ORACLE_SYSTEM_PROMPT


CANONICAL_ROUTES = [
    "negation",
    "affect",
    "sensitivity-precursor",
    "opener-substitution",
    "topic-routing",
]


def test_prompt_mentions_distinct_suppression_routes_or_route_vocabulary():
    """Either the phrase 'distinct suppression routes' or >=3 of the 5 route
    names must appear in the rewritten prompt."""
    prompt_lower = ORACLE_SYSTEM_PROMPT.lower()
    has_phrase = "distinct suppression routes" in prompt_lower
    route_hits = sum(1 for route in CANONICAL_ROUTES if route in prompt_lower)
    assert has_phrase or route_hits >= 3, (
        "ORACLE_SYSTEM_PROMPT does not communicate the cross-route supernode "
        "requirement. Expected either the literal phrase 'distinct suppression "
        f"routes' or at least 3 of the canonical route names "
        f"({CANONICAL_ROUTES}); found {route_hits} route name(s) and "
        f"phrase={has_phrase}."
    )
