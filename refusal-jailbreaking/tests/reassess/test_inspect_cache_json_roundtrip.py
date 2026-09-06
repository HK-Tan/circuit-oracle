"""Ctx.inspect_cache survives JSON serialize/deserialize unchanged.

The cache is persisted to disk (e.g. embedded in oracle_result.json or in the
reassess_records section) so the subagent + downstream tooling can rehydrate
it. Tuple keys must be normalized to a JSON-safe shape (e.g. "layer:feature_idx:pos"
string keys, or a list-of-records form) and round-trip lossless-ly.

Fails if inspect_cache or its (de)serialization helpers are missing.
"""
from __future__ import annotations

import json

import pytest

from circuit_oracle.tools import (  # noqa: F401
    dump_inspect_cache,
    load_inspect_cache,
)


def _sample_cache() -> dict:
    """Fixture cache mimicking three real inspect_feature responses."""
    return {
        (17, 83241, 5): {
            "autointerp": "Code/technical snippets",
            "promoted_tokens": ["def", "class", "import"],
            "suppressed_tokens": ["the", "and"],
            "top_activating_examples": [
                {"prompt": "def foo():", "act": 8.4},
                {"prompt": "import os", "act": 7.1},
            ],
            "build_connectivity": {"upstream": [(16, 1024)], "downstream": [(18, 7700)]},
        },
        (24, 91636, 5): {
            "autointerp": "el",
            "promoted_tokens": ["unfortunately", "sadly"],
            "suppressed_tokens": ["Sure", "Yes"],
            "top_activating_examples": [],
            "build_connectivity": {"upstream": [], "downstream": []},
        },
        (12, 1, 0): {
            "autointerp": "",
            "promoted_tokens": [],
            "suppressed_tokens": [],
            "top_activating_examples": [],
            "build_connectivity": {"upstream": [], "downstream": []},
        },
    }


def test_dump_inspect_cache_produces_json_string():
    """dump_inspect_cache must return a string that json.loads can parse."""
    raw = _sample_cache()
    blob = dump_inspect_cache(raw)
    assert isinstance(blob, str), f"dump_inspect_cache must return str, got {type(blob).__name__}"
    parsed = json.loads(blob)
    assert isinstance(parsed, (dict, list)), (
        "dump_inspect_cache output must be a JSON object or list (got something else)."
    )


def test_inspect_cache_roundtrip_is_lossless():
    """raw -> dump -> load must reproduce the original cache dict exactly."""
    raw = _sample_cache()
    restored = load_inspect_cache(dump_inspect_cache(raw))
    assert restored == raw, (
        "inspect_cache roundtrip lost or mutated data.\n"
        f"  original keys: {sorted(raw)}\n"
        f"  restored keys: {sorted(restored)}\n"
    )


def test_inspect_cache_roundtrip_preserves_tuple_keys():
    """Keys must come back as (layer, feature_idx, pos) tuples of ints."""
    raw = _sample_cache()
    restored = load_inspect_cache(dump_inspect_cache(raw))
    for key in restored:
        assert isinstance(key, tuple), (
            f"restored key {key!r} must be a tuple, got {type(key).__name__}"
        )
        assert len(key) == 3, f"restored key {key!r} must have length 3"
        assert all(isinstance(part, int) for part in key), (
            f"restored key {key!r} must be a tuple of ints"
        )
