"""Assert ctx.baseline_top5 cached at graph compute time.

After compute_or_load_graph runs, the returned ToolContext (or the dict it
returns) must expose a populated `baseline_top5` field of shape
`dict[str, dict[str, float]]`, mirroring the _topk_from_logits return value
in tools.py (token_string -> {"prob": float}).

Fails with AttributeError if the field is gone, and with AssertionError if it
is present but None or the wrong type.
"""
from __future__ import annotations

import pytest


def test_baseline_top5_attribute_present(baseline_ctx):
    """ctx.baseline_top5 must exist as an attribute on ToolContext."""
    assert hasattr(baseline_ctx, "baseline_top5"), (
        "ToolContext is missing baseline_top5 field. "
        "config.py must declare it and compute_or_load_graph must populate it."
    )


def test_baseline_top5_populated_after_compute(baseline_ctx):
    """baseline_top5 must be populated (non-None) after compute_or_load_graph."""
    assert baseline_ctx.baseline_top5 is not None, (
        "ctx.baseline_top5 is None. compute_or_load_graph must compute the top-5 "
        "next-token distribution at graph build time, alongside baseline_activations."
    )


def test_baseline_top5_is_dict_of_dicts(baseline_ctx):
    """baseline_top5 shape: dict[str, dict[str, float]] per tools.py:_topk_from_logits."""
    top5 = baseline_ctx.baseline_top5
    assert isinstance(top5, dict), f"baseline_top5 must be a dict, got {type(top5).__name__}"
    assert len(top5) == 5, f"baseline_top5 must have 5 entries (top-5), got {len(top5)}"
    for token_str, entry in top5.items():
        assert isinstance(token_str, str), (
            f"baseline_top5 keys must be token strings, got {type(token_str).__name__}"
        )
        assert isinstance(entry, dict), (
            f"baseline_top5 values must be dicts, got {type(entry).__name__}"
        )
        assert "prob" in entry, (
            f"baseline_top5[{token_str!r}] missing 'prob' key; "
            "_topk_from_logits returns {token: {'prob': float}}"
        )
        assert isinstance(entry["prob"], float), (
            f"baseline_top5[{token_str!r}]['prob'] must be float, got {type(entry['prob']).__name__}"
        )


def test_baseline_top5_probabilities_descending(baseline_ctx):
    """top-5 entries should come out of topk() in descending probability order."""
    probs = [entry["prob"] for entry in baseline_ctx.baseline_top5.values()]
    assert probs == sorted(probs, reverse=True), (
        f"baseline_top5 probabilities must be in descending order, got {probs}"
    )
