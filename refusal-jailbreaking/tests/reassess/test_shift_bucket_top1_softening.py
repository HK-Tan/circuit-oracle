"""Shift_bucket truth table, top-1 softening case.

Top-1 token unchanged but its probability drops by more than the 0.05
threshold: classify as "shifted" (softening without swap). Example: "I" at
0.94 -> "I" at 0.10, delta = 0.84.

Fails with ImportError if the symbol is missing.
"""
from __future__ import annotations

import pytest

from circuit_oracle.tools import shift_bucket  # noqa: F401


def test_softening_i_094_to_010_is_shifted():
    """Top-1 token stays "I" but prob collapses from 0.94 -> 0.10 -> shifted."""
    top5_before = {
        "I": {"prob": 0.94},
        " I": {"prob": 0.03},
        "Hi": {"prob": 0.02},
        "Hello": {"prob": 0.005},
        "Sure": {"prob": 0.005},
    }
    top5_after = {
        "I": {"prob": 0.10},
        "Hello": {"prob": 0.09},
        "Sure": {"prob": 0.08},
        "Yes": {"prob": 0.07},
        "Okay": {"prob": 0.06},
    }
    assert shift_bucket(top5_before, top5_after) == "shifted", (
        "Same top-1 token with prob delta (0.94 - 0.10) = 0.84 must be 'shifted'."
    )


def test_softening_just_above_threshold_is_shifted():
    """delta = 0.06 (just above 0.05 threshold) must classify as shifted."""
    top5_before = {
        "I": {"prob": 0.50},
        "Hi": {"prob": 0.20},
        "Hello": {"prob": 0.15},
        "Sure": {"prob": 0.10},
        "Yes": {"prob": 0.05},
    }
    top5_after = {
        "I": {"prob": 0.44},  # 0.50 - 0.44 = 0.06 > 0.05
        "Hi": {"prob": 0.20},
        "Hello": {"prob": 0.16},
        "Sure": {"prob": 0.12},
        "Yes": {"prob": 0.08},
    }
    assert shift_bucket(top5_before, top5_after) == "shifted"
