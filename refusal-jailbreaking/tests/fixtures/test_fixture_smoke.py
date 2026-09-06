"""Smoke tests for the toy fixture itself.

They guard the substrate every other test stands on:

    pytest tests/fixtures/ -q  # exits 0 (the fixture itself works)

If the toy transformer build, the toy graph construction, or the
golden.json schema drifts out of sync with `tiny_model.py`, the fixture is
no longer trustworthy, and we want to know here rather than through
cascading failures across the rest of the tree.

Everything here is CPU-only, runs in well under a second, and depends on
nothing outside `tests/fixtures/`.
"""

from __future__ import annotations

import json
from pathlib import Path

from fixtures.tiny_model import (
    DEFAULT_PROMPT,
    SEED,
    build_tiny_fixture,
    capture_golden,
)


def test_build_tiny_fixture_returns_populated_ctx() -> None:
    ctx = build_tiny_fixture()
    # Required ToolContext fields downstream tests will read.
    assert ctx.graph is not None
    assert ctx.tokenizer is not None
    assert ctx.replacement_model is not None
    assert ctx.baseline_activations is not None
    assert ctx.baseline_answer is not None
    assert ctx.baseline_prompt == DEFAULT_PROMPT


def test_build_tiny_fixture_is_deterministic() -> None:
    """Two calls with the same seed must produce identical baseline outputs.

    Determinism is the load-bearing property for the cache-coherence and
    batched-vs-single determinism tests.
    """
    a = build_tiny_fixture()
    b = build_tiny_fixture()
    assert a.baseline_answer == b.baseline_answer
    assert a.baseline_activations.shape == b.baseline_activations.shape
    assert (a.baseline_activations == b.baseline_activations).all().item()


def test_golden_json_matches_capture_golden() -> None:
    """golden.json on disk must match `capture_golden()` at the current seed.

    If the toy model weights or wiring change, regenerate via
    `python tests/fixtures/tiny_model.py`.
    """
    expected = capture_golden(prompt=DEFAULT_PROMPT, seed=SEED)
    path = Path(__file__).with_name("golden.json")
    with open(path) as f:
        actual = json.load(f)
    assert actual == expected
