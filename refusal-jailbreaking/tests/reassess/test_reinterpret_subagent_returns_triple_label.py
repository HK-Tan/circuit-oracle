"""Reinterpret_subagent returns a parseable TripleLabelRecord.

The subagent's JSON output must coerce into a TripleLabelRecord with all four
fields populated:

  - autointerp: str
  - pre_label: str
  - post_label: str
  - divergence: one of {"none", "autointerp_only", "autointerp_and_pre"}

Fails with ImportError on either symbol if the contracts
land.
"""
from __future__ import annotations

import json

import pytest

from circuit_oracle.subagent import TripleLabelRecord  # noqa: F401
from circuit_oracle.subagent import reinterpret_subagent  # noqa: F401


CANNED_TRIPLE_LABEL = {
    "autointerp": "el",
    "pre_label": "uncertain; label is fragment but promoted tokens 'unfortunately'/'sadly' suggest refusal-affect softener",
    "post_label": "decisive refusal-affect gate; at -1 surfaced 'Unfortunately' demoted and topic emerged",
    "divergence": "autointerp_only",
}


def _trivial_shift_profile() -> dict:
    return {
        0.0: {
            "top5_before": {"I": {"prob": 0.9}},
            "top5_after": {"I": {"prob": 0.9}},
            "answer_after": "I cannot.",
            "shift_bucket": "no-shift",
        },
        -1.0: {
            "top5_before": {"I": {"prob": 0.9}},
            "top5_after": {"Sure": {"prob": 0.4}},
            "answer_after": "Sure, here is ...",
            "shift_bucket": "shifted",
        },
        -2.0: {
            "top5_before": {"I": {"prob": 0.9}},
            "top5_after": {"Sure": {"prob": 0.55}},
            "answer_after": "Sure, here is ...",
            "shift_bucket": "shifted",
        },
        -3.0: {
            "top5_before": {"I": {"prob": 0.9}},
            "top5_after": {"Sure": {"prob": 0.7}},
            "answer_after": "Sure, here is ...",
            "shift_bucket": "shifted",
        },
    }


def test_reinterpret_subagent_returns_dict_with_all_four_fields(
    baseline_ctx, mock_subagent_client
):
    """The parsed return must have autointerp, pre_label, post_label, divergence."""
    layer, feature_idx, pos = 24, 91636, 5
    baseline_ctx.inspect_cache[(layer, feature_idx, pos)] = {"autointerp": "el"}
    baseline_ctx.pinned_features = {(layer, feature_idx, pos): "refusal softener"}
    mock_subagent_client.return_value = json.dumps(CANNED_TRIPLE_LABEL)

    record = reinterpret_subagent(
        ctx=baseline_ctx,
        layer=layer,
        feature_idx=feature_idx,
        pos=pos,
        shift_profile=_trivial_shift_profile(),
        user_message="Tell me about X.",
        system_prompt="You are helpful.",
    )

    for field in ("autointerp", "pre_label", "post_label", "divergence"):
        assert field in record, (
            f"TripleLabelRecord missing field {field!r}; got keys {list(record)}"
        )
        assert record[field], f"TripleLabelRecord field {field!r} is empty"


def test_reinterpret_subagent_divergence_in_allowed_set(
    baseline_ctx, mock_subagent_client
):
    """divergence must be one of the three allowed literals."""
    layer, feature_idx, pos = 24, 91636, 5
    baseline_ctx.inspect_cache[(layer, feature_idx, pos)] = {"autointerp": "el"}
    baseline_ctx.pinned_features = {(layer, feature_idx, pos): "refusal softener"}
    mock_subagent_client.return_value = json.dumps(CANNED_TRIPLE_LABEL)

    record = reinterpret_subagent(
        ctx=baseline_ctx,
        layer=layer,
        feature_idx=feature_idx,
        pos=pos,
        shift_profile=_trivial_shift_profile(),
        user_message="Tell me about X.",
        system_prompt="You are helpful.",
    )

    assert record["divergence"] in {"none", "autointerp_only", "autointerp_and_pre"}, (
        f"divergence value {record['divergence']!r} not in allowed set"
    )


def test_reinterpret_subagent_payload_values_preserved(
    baseline_ctx, mock_subagent_client
):
    """The canned JSON values must round-trip into the returned record."""
    layer, feature_idx, pos = 24, 91636, 5
    baseline_ctx.inspect_cache[(layer, feature_idx, pos)] = {"autointerp": "el"}
    baseline_ctx.pinned_features = {(layer, feature_idx, pos): "refusal softener"}
    mock_subagent_client.return_value = json.dumps(CANNED_TRIPLE_LABEL)

    record = reinterpret_subagent(
        ctx=baseline_ctx,
        layer=layer,
        feature_idx=feature_idx,
        pos=pos,
        shift_profile=_trivial_shift_profile(),
        user_message="Tell me about X.",
        system_prompt="You are helpful.",
    )

    assert record["autointerp"] == CANNED_TRIPLE_LABEL["autointerp"]
    assert record["pre_label"] == CANNED_TRIPLE_LABEL["pre_label"]
    assert record["post_label"] == CANNED_TRIPLE_LABEL["post_label"]
    assert record["divergence"] == CANNED_TRIPLE_LABEL["divergence"]
