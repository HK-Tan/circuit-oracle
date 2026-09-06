"""batched_anchor_sweep has no required args other than ctx.

Asserts the argless signature by introspecting parameter
defaults. Any parameter beyond `ctx` must have a default value, so the agent calls
`batched_anchor_sweep()` (in tool-call form, with `ctx` injected by the harness).
"""
from __future__ import annotations

import inspect

import pytest


def test_batched_anchor_sweep_argless():
    from circuit_oracle.tools import batched_anchor_sweep

    sig = inspect.signature(batched_anchor_sweep)
    params = list(sig.parameters.values())

    # Every parameter other than `ctx` must have a default.
    for p in params:
        if p.name == "ctx":
            continue
        assert p.default is not inspect.Parameter.empty, (
            f"batched_anchor_sweep parameter {p.name!r} has no default; "
            f"signature must be argless to the agent"
        )
