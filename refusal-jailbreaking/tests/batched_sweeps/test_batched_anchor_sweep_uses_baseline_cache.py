"""batched_anchor_sweep uses the cached baseline; no baseline forward.

Asserts the cache dependency: `batched_anchor_sweep` reads `ctx.baseline_top5`
instead of running an extra `_run([], prompt, freeze_attn=True)` pass for the
baseline. Monkeypatches the internal `_run` to count invocations.
"""
from __future__ import annotations

import pytest


def test_batched_anchor_sweep_uses_baseline_cache(tiny_model, baseline_ctx, monkeypatch):
    from circuit_oracle import tools as tools_mod
    from circuit_oracle.tools import (
        batched_anchor_sweep,
        build_circuit,
        pin_features,
    )

    run_calls = []
    original_run = tools_mod._run  # module-level, not a closure, so it can be monkeypatched

    def counting_run(interventions_list, prompt_arg, freeze_attn=True, **kwargs):
        run_calls.append({"interventions": interventions_list, "prompt": prompt_arg})
        return original_run(interventions_list, prompt_arg, freeze_attn=freeze_attn, **kwargs)

    monkeypatch.setattr(tools_mod, "_run", counting_run)

    nodes = [
        {"layer": 0, "feature_idx": 1, "pos": 3, "label": "a"},
        {"layer": 1, "feature_idx": 5, "pos": 4, "label": "b"},
    ]
    build_circuit(baseline_ctx, nodes=nodes, edges=[])
    pin_features(
        baseline_ctx,
        pre_hypotheses={(0, 1, 3): "x", (1, 5, 4): "y"},
    )

    batched_anchor_sweep(baseline_ctx)

    # No `_run` call may have an empty interventions list (which is the baseline-forward signature).
    baseline_runs = [c for c in run_calls if not c["interventions"]]
    assert baseline_runs == [], (
        f"batched_anchor_sweep ran {len(baseline_runs)} baseline forward(s); "
        f"must use ctx.baseline_top5 cache"
    )
