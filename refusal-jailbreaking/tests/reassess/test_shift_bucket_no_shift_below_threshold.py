"""Shift_bucket truth table, no-shift case.

Top-1 token unchanged AND top-1 probability delta is below the 0.05 threshold
=> classify as "no-shift". Example: "I" at 0.94 -> "I" at 0.92, delta = 0.02.

Fails with ImportError if the symbol is missing.
"""
from __future__ import annotations

import pytest

from circuit_oracle.tools import shift_bucket  # noqa: F401


def test_no_shift_i_094_to_092_below_threshold():
    """delta = 0.02 < 0.05 with same top-1 token -> no-shift."""
    top5_before = {
        "I": {"prob": 0.94},
        " I": {"prob": 0.03},
        "Hi": {"prob": 0.02},
        "Hello": {"prob": 0.005},
        "Sure": {"prob": 0.005},
    }
    top5_after = {
        "I": {"prob": 0.92},
        " I": {"prob": 0.04},
        "Hi": {"prob": 0.025},
        "Hello": {"prob": 0.01},
        "Sure": {"prob": 0.005},
    }
    assert shift_bucket(top5_before, top5_after) == "no-shift", (
        "Same top-1 with delta 0.02 < 0.05 threshold must be 'no-shift'."
    )


def test_no_shift_at_exactly_threshold_minus_epsilon():
    """delta = 0.049 (just below 0.05) -> no-shift."""
    top5_before = {
        "I": {"prob": 0.500},
        "Hi": {"prob": 0.20},
        "Hello": {"prob": 0.15},
        "Sure": {"prob": 0.10},
        "Yes": {"prob": 0.05},
    }
    top5_after = {
        "I": {"prob": 0.451},  # delta = 0.049
        "Hi": {"prob": 0.22},
        "Hello": {"prob": 0.16},
        "Sure": {"prob": 0.11},
        "Yes": {"prob": 0.06},
    }
    assert shift_bucket(top5_before, top5_after) == "no-shift"


def test_no_shift_identical_distributions():
    """Identical top-5 dicts -> no-shift."""
    top5 = {
        "I": {"prob": 0.94},
        " I": {"prob": 0.03},
        "Hi": {"prob": 0.02},
        "Hello": {"prob": 0.005},
        "Sure": {"prob": 0.005},
    }
    assert shift_bucket(top5, dict(top5)) == "no-shift"
