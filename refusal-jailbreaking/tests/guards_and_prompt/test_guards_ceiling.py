"""Top-of-stack ceiling guard.

`check_ceiling_guard` is the mirror of `check_floor_guard`. It fires when ANY
pinned feature sits above `n_layers - n_layers // 6` (layer 30 of 36 on
Qwen3-4B), because features that high are answer-preparation (wrapper text,
formatting, surface phrasing) sitting downstream of the decision about whether
to answer at all, so they are rarely a gate that can be flipped. The nudge tells
the orchestrator to re-nominate: trace through each offender, rebuild with the
upstream precursor in its place, and re-pin.

Two behaviours distinguish it from the floor guard and are asserted here:
  1. it fires on a single offender, not only when every pin is high, and
  2. its replacement candidates are drawn from BELOW the ceiling, so it never
     offers one top-of-stack feature as the fix for another.

Same fake-ctx + monkeypatched `get_upstream_features` setup as the floor guard
test, so this stays CPU-only and deterministic.
"""
from __future__ import annotations

from types import SimpleNamespace

import circuit_oracle.orchestrator as orch


class _Cfg:
    def __init__(self, n_layers: int) -> None:
        self.n_layers = n_layers


class _Graph:
    def __init__(self, n_layers: int) -> None:
        self.cfg = _Cfg(n_layers)


def _ctx(pinned: dict, n_layers: int = 36, inspect_cache: dict | None = None):
    return SimpleNamespace(
        graph=_Graph(n_layers),
        pinned_features=pinned,
        inspect_cache=inspect_cache or {},
    )


# One candidate below the ceiling, one above it (must be dropped), plus an
# embedding node (dropped by the shared candidate helper).
_CANNED_UPSTREAMS = [
    {"type": "feature", "layer": 17, "feature_idx": 111, "pos": 5, "direct_effect": 2.5},
    {"type": "feature", "layer": 33, "feature_idx": 222, "pos": 5, "direct_effect": 9.9},
    {"type": "embedding", "token": "x", "pos": 0, "direct_effect": 3.0},
]


def test_ceiling_guard_fires_on_a_single_high_pin(monkeypatch):
    monkeypatch.setattr(
        orch, "get_upstream_features",
        lambda ctx, layer, feature_idx, pos, k=10: list(_CANNED_UPSTREAMS),
    )
    # n_layers=36 -> ceiling=30. L14 is fine, L34 is not. One offender is enough.
    ctx = _ctx({(14, 100, 5): "h1", (34, 200, 5): "h2"})
    res = orch.check_ceiling_guard([], ctx=ctx)

    assert res.fired is True, "one pin above the ceiling must fire the guard"
    assert "L34:F200@5" in res.message, "the offender must be named"
    assert "L14:F100@5" not in res.message, "the compliant pin must not be named"
    assert "30 of 36" in res.message
    assert "re-pin" in res.message.lower()


def test_ceiling_guard_offers_only_candidates_below_the_ceiling(monkeypatch):
    monkeypatch.setattr(
        orch, "get_upstream_features",
        lambda ctx, layer, feature_idx, pos, k=10: list(_CANNED_UPSTREAMS),
    )
    ctx = _ctx({(34, 200, 5): "h2"})
    res = orch.check_ceiling_guard([], ctx=ctx)

    assert res.fired is True
    assert "L17:F111@5" in res.message
    # Highest direct_effect of the three, but it is above the ceiling itself, so
    # offering it would just move the problem sideways.
    assert "L33:F222@5" not in res.message
    assert "embedding" not in res.message.lower()


def test_ceiling_guard_silent_when_every_pin_is_below_the_ceiling(monkeypatch):
    monkeypatch.setattr(orch, "get_upstream_features", lambda *a, **k: [])
    ctx = _ctx({(14, 100, 5): "h1", (30, 200, 5): "h2"})  # 30 is not > 30
    res = orch.check_ceiling_guard([], ctx=ctx)
    assert res.fired is False


def test_ceiling_guard_silent_when_no_pins():
    # pin_features hasn't run yet -> the pin-coverage guard owns this turn.
    ctx = _ctx({})
    res = orch.check_ceiling_guard([], ctx=ctx)
    assert res.fired is False


def test_ceiling_guard_scales_with_layer_count(monkeypatch):
    """Gemma-2-2B has 26 layers, so the ceiling is 22, not a hardcoded 30."""
    monkeypatch.setattr(orch, "get_upstream_features", lambda *a, **k: [])
    assert orch.check_ceiling_guard([], ctx=_ctx({(23, 1, 0): "h"}, n_layers=26)).fired
    assert not orch.check_ceiling_guard([], ctx=_ctx({(22, 1, 0): "h"}, n_layers=26)).fired


def test_ceiling_guard_falls_back_when_no_candidates_survive(monkeypatch):
    monkeypatch.setattr(orch, "get_upstream_features", lambda *a, **k: [])
    ctx = _ctx({(35, 900, 2): "h"})
    res = orch.check_ceiling_guard([], ctx=ctx)
    assert res.fired is True
    assert "get_upstream_features" in res.message


def test_floor_and_ceiling_can_fire_together(monkeypatch):
    """A circuit pinned entirely at the top trips both, and the advice agrees:
    trace downward. Neither guard should suppress the other."""
    monkeypatch.setattr(
        orch, "get_upstream_features",
        lambda ctx, layer, feature_idx, pos, k=10: list(_CANNED_UPSTREAMS),
    )
    ctx = _ctx({(31, 100, 5): "h1", (34, 200, 5): "h2"})
    assert orch.check_floor_guard([], ctx=ctx).fired is True
    assert orch.check_ceiling_guard([], ctx=ctx).fired is True
