"""Ctx.inspect_cache deduplicates inspect_feature backend calls.

After two inspect_feature calls on the same (layer, feature_idx, pos) tuple
in the same run, the Neuronpedia backend must be hit exactly once, and
ctx.inspect_cache[(layer, feature_idx, pos)] must be populated with the
cached payload.

Current codebase does NOT have ctx.inspect_cache; inspect_feature in tools.py
re-hits Neuronpedia every call. Fails with AttributeError if the field is missing.
"""
from __future__ import annotations

from unittest.mock import patch

import pytest

from circuit_oracle.tools import inspect_feature


def test_inspect_cache_field_exists(baseline_ctx):
    """ctx.inspect_cache must exist on ToolContext."""
    assert hasattr(baseline_ctx, "inspect_cache"), (
        "ToolContext is missing inspect_cache field. "
        "config.py must declare it."
    )
    assert isinstance(baseline_ctx.inspect_cache, dict), (
        f"ctx.inspect_cache must be a dict, got {type(baseline_ctx.inspect_cache).__name__}"
    )


def test_inspect_feature_hits_backend_once_for_repeated_call(baseline_ctx):
    """Two inspect_feature calls on same (layer, feature_idx, pos) -> 1 backend hit."""
    layer, feature_idx, pos = 0, 7, 3

    # Patch the Neuronpedia HTTP path used by inspect_feature. The current
    # implementation in tools.py:78 reaches out via the neuronpedia_link
    # helpers, and every fetch routes through ctx.inspect_cache.
    with patch("circuit_oracle.tools._fetch_inspect_payload") as mock_fetch:
        mock_fetch.return_value = {
            "autointerp": "stub-label",
            "promoted_tokens": ["foo"],
            "suppressed_tokens": ["bar"],
            "top_activating_examples": [],
        }

        inspect_feature(baseline_ctx, layer=layer, feature_idx=feature_idx, pos=pos)
        inspect_feature(baseline_ctx, layer=layer, feature_idx=feature_idx, pos=pos)

        assert mock_fetch.call_count == 1, (
            f"inspect_feature must dedupe via ctx.inspect_cache; "
            f"backend was hit {mock_fetch.call_count} times for the same key."
        )


def test_inspect_cache_populated_after_call(baseline_ctx):
    """ctx.inspect_cache[(layer, feature_idx, pos)] must hold the payload."""
    layer, feature_idx, pos = 1, 11, 2

    with patch("circuit_oracle.tools._fetch_inspect_payload") as mock_fetch:
        payload = {
            "autointerp": "refusal-affect softener",
            "promoted_tokens": ["unfortunately", "sadly"],
            "suppressed_tokens": [],
            "top_activating_examples": [],
        }
        mock_fetch.return_value = payload

        inspect_feature(baseline_ctx, layer=layer, feature_idx=feature_idx, pos=pos)

        key = (layer, feature_idx, pos)
        assert key in baseline_ctx.inspect_cache, (
            f"ctx.inspect_cache missing key {key!r} after inspect_feature call. "
            "inspect_feature must populate the cache."
        )
        cached = baseline_ctx.inspect_cache[key]
        assert cached["autointerp"] == payload["autointerp"]
