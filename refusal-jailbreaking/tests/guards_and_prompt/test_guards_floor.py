"""Shallow-pin floor guard (Edit 2).

`check_floor_guard` fires when every pinned feature sits above the lower-third
floor (layer > n_layers // 3), so the L14-17-band refusal precursor was never
surfaced. It is a soft guard (nudge + retry then accept), mirroring the other
end-of-turn guards. The nudge must hand back a DE-ranked list of un-inspected
upstream candidates of the pinned gates and restate the anti-label-trust rule.

The guard reads layer count from ctx.graph.cfg.n_layers and the candidate list
from get_upstream_features (local, free). We feed a lightweight fake ctx and
monkeypatch get_upstream_features so the test stays CPU-only and deterministic.
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


# Two feature upstreams (one in the lower third, one above) plus an embedding node
# that must be dropped from the candidate list.
_CANNED_UPSTREAMS = [
    {"type": "feature", "layer": 8, "feature_idx": 111, "pos": 5, "direct_effect": 2.5},
    {"type": "feature", "layer": 15, "feature_idx": 222, "pos": 5, "direct_effect": 1.0},
    {"type": "embedding", "token": "x", "pos": 0, "direct_effect": 3.0},
]


def test_floor_guard_fires_when_all_pins_above_lower_third(monkeypatch):
    monkeypatch.setattr(
        orch, "get_upstream_features",
        lambda ctx, layer, feature_idx, pos, k=10: list(_CANNED_UPSTREAMS),
    )
    # n_layers=36 -> floor=12. Both pins at layer >= 20, so min layer 20 > 12.
    ctx = _ctx({(20, 100, 5): "h1", (25, 200, 5): "h2"})
    res = orch.check_floor_guard([], ctx=ctx)

    assert res.fired is True, "guard must fire when no pin reaches the lower third"
    # DE-ranked candidate list present; top candidate (de=2.5) surfaced.
    assert "L8:F111@5" in res.message
    assert "L15:F222@5" in res.message
    # embedding node dropped from candidates
    assert "embedding" not in res.message.lower()
    # anti-label-trust rule restated at the point of failure
    assert "label" in res.message.lower() and "promoted tokens" in res.message.lower()


def test_floor_guard_silent_when_pin_reaches_lower_third(monkeypatch):
    monkeypatch.setattr(orch, "get_upstream_features", lambda *a, **k: [])
    # min pinned layer 10 <= floor 12 -> a lower-third feature is present.
    ctx = _ctx({(10, 100, 5): "h1", (25, 200, 5): "h2"})
    res = orch.check_floor_guard([], ctx=ctx)
    assert res.fired is False


def test_floor_guard_silent_when_no_pins():
    # pin_features hasn't run yet -> the pin-coverage guard owns this turn.
    ctx = _ctx({})
    res = orch.check_floor_guard([], ctx=ctx)
    assert res.fired is False


def test_floor_guard_drops_already_pinned_and_inspected(monkeypatch):
    monkeypatch.setattr(
        orch, "get_upstream_features",
        lambda ctx, layer, feature_idx, pos, k=10: list(_CANNED_UPSTREAMS),
    )
    # L8:F111 is already inspected; L15:F222 is already pinned -> both excluded,
    # leaving no candidates, so the guard falls back to the generic trace nudge.
    ctx = _ctx(
        {(20, 100, 5): "h1", (15, 222, 5): "h2"},
        inspect_cache={(8, 111, 5): {"label": "x"}},
    )
    res = orch.check_floor_guard([], ctx=ctx)
    # min pinned layer is 15 > floor 12, so it still fires...
    assert res.fired is True
    # ...but the two known features are not offered as fresh candidates.
    assert "L8:F111@5" not in res.message
    assert "L15:F222@5" not in res.message
    assert "get_upstream_features" in res.message
