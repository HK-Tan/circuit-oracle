"""Shift_bucket truth table, top-1 swap case.

When the top-1 token under intervention is different from the top-1 token at
baseline, shift_bucket must return "shifted" regardless of probability values.
Example: baseline top-1 is "I", intervened top-1 is "Sure".

Fails with ImportError if circuit_oracle.tools stops exporting shift_bucket.
"""
from __future__ import annotations

import pytest

from circuit_oracle.tools import shift_bucket  # noqa: F401  (import-time failure expected)


def test_top1_swap_i_to_sure_is_shifted():
    """Top-1 token swap from "I" -> "Sure" must be classified as "shifted"."""
    top5_before = {
        "I": {"prob": 0.94},
        " I": {"prob": 0.03},
        "Hi": {"prob": 0.02},
        "Hello": {"prob": 0.005},
        "Sure": {"prob": 0.005},
    }
    top5_after = {
        "Sure": {"prob": 0.50},
        "I": {"prob": 0.20},
        "Okay": {"prob": 0.15},
        "Yes": {"prob": 0.10},
        "Of": {"prob": 0.05},
    }
    assert shift_bucket(top5_before, top5_after) == "shifted", (
        "Top-1 swap (different argmax token) must always return 'shifted', "
        "regardless of probability magnitudes."
    )


def test_top1_swap_holds_even_when_probs_close():
    """A top-1 swap with near-equal probs is still a shift."""
    top5_before = {
        "I": {"prob": 0.30},
        "Sure": {"prob": 0.28},
        "Hello": {"prob": 0.20},
        "Yes": {"prob": 0.12},
        "Okay": {"prob": 0.10},
    }
    top5_after = {
        "Sure": {"prob": 0.31},
        "I": {"prob": 0.29},
        "Hello": {"prob": 0.20},
        "Yes": {"prob": 0.12},
        "Okay": {"prob": 0.08},
    }
    assert shift_bucket(top5_before, top5_after) == "shifted"
