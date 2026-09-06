"""Reinterpret_subagent assembles the 4-item context payload.

The prompt sent to the Sonnet subagent must include, server-side:

  1. Cached inspect_feature blob from ctx.inspect_cache
  2. 4-scale shift profile for the feature: {scale: {top5_before, top5_after,
     answer_after, shift_bucket}} across {0, -1, -2, -3}
  3. Agent's pre_hypothesis from ctx.pinned_features[(layer, feature_idx, pos)]
  4. User prompt + system prompt for topical grounding
  (plus baseline_answer once, for reference)

Fails with ImportError until reinterpret_subagent ships in subagent.py.
"""
from __future__ import annotations

import json

import pytest

from circuit_oracle.subagent import reinterpret_subagent  # noqa: F401


def _make_shift_profile() -> dict:
    """4-scale shift profile fixture mirroring the spec's example."""
    return {
        0.0: {
            "top5_before": {"I": {"prob": 0.94}, "Hi": {"prob": 0.02}},
            "top5_after": {"I": {"prob": 0.94}, "Hi": {"prob": 0.02}},
            "answer_after": "I cannot help with that.",
            "shift_bucket": "no-shift",
        },
        -1.0: {
            "top5_before": {"I": {"prob": 0.94}, "Hi": {"prob": 0.02}},
            "top5_after": {"Sure": {"prob": 0.40}, "I": {"prob": 0.30}},
            "answer_after": "Sure, the events of June 4 1989 ...",
            "shift_bucket": "shifted",
        },
        -2.0: {
            "top5_before": {"I": {"prob": 0.94}, "Hi": {"prob": 0.02}},
            "top5_after": {"Sure": {"prob": 0.55}, "I": {"prob": 0.20}},
            "answer_after": "Sure, in 1989 in Beijing ...",
            "shift_bucket": "shifted",
        },
        -3.0: {
            "top5_before": {"I": {"prob": 0.94}, "Hi": {"prob": 0.02}},
            "top5_after": {"Sure": {"prob": 0.70}, "I": {"prob": 0.10}},
            "answer_after": "Sure, here is what happened ...",
            "shift_bucket": "shifted",
        },
    }


def test_reinterpret_subagent_prompt_contains_all_four_context_items(
    baseline_ctx, mock_subagent_client
):
    """The prompt body sent to the Sonnet client must include all 4 context items."""
    layer, feature_idx, pos = 24, 91636, 5

    # Seed inspect_cache and pinned_features as the upstream tools would.
    baseline_ctx.inspect_cache[(layer, feature_idx, pos)] = {
        "autointerp": "el",
        "promoted_tokens": ["unfortunately", "sadly"],
        "suppressed_tokens": ["Sure"],
        "top_activating_examples": [],
        "build_connectivity": {"upstream": [], "downstream": []},
    }
    baseline_ctx.pinned_features = {
        (layer, feature_idx, pos): (
            "uncertain - label is fragment, promoted tokens suggest refusal-affect softener"
        ),
    }

    # Configure the mock to return a syntactically valid triple-label JSON so
    # the call completes; we then inspect the prompt the client was called with.
    mock_subagent_client.return_value = json.dumps(
        {
            "autointerp": "el",
            "pre_label": "stub",
            "post_label": "stub",
            "divergence": "none",
        }
    )

    reinterpret_subagent(
        ctx=baseline_ctx,
        layer=layer,
        feature_idx=feature_idx,
        pos=pos,
        shift_profile=_make_shift_profile(),
        user_message="Tell me about Tiananmen Square June 4 1989.",
        system_prompt="You are a helpful assistant.",
    )

    assert mock_subagent_client.called, (
        "reinterpret_subagent must call the Sonnet client at least once."
    )
    # Collect every string argument passed to the mock so we can substring-check.
    call_args = mock_subagent_client.call_args
    sent_payload = json.dumps(
        {"args": list(call_args.args), "kwargs": call_args.kwargs}, default=str
    )

    # 1. Cached inspect_feature blob: autointerp label + promoted tokens.
    assert "unfortunately" in sent_payload, (
        "subagent prompt must include cached inspect_feature promoted tokens"
    )

    # 2. 4-scale shift profile: every scale and its shift_bucket must appear.
    for scale in (0.0, -1.0, -2.0, -3.0):
        assert str(scale) in sent_payload or f"{scale:g}" in sent_payload, (
            f"subagent prompt missing scale {scale} from 4-scale shift profile"
        )
    assert "shifted" in sent_payload and "no-shift" in sent_payload, (
        "subagent prompt must surface shift_bucket labels for each scale"
    )

    # 3. pre_hypothesis text.
    assert "refusal-affect softener" in sent_payload, (
        "subagent prompt must include the agent's pre_hypothesis"
    )

    # 4. User prompt for topical grounding.
    assert "Tiananmen" in sent_payload, (
        "subagent prompt must include the user_message for topical grounding"
    )
