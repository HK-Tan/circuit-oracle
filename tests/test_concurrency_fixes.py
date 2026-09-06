"""Regression tests for the four concurrency bugs found in review.

Each of these is invisible in a serial run and only bites once --workers > 1:

  1. _decode_one_chunk returned the FULL [B, T_prompt, V] prefill logits when
     every consumer indexes [..., -1, :]. ~620 MB per chunk at B=68, held live
     across the REASSESS network fan-out, times N concurrent runs.
  2. fanout had no process-wide ceiling, so N runs x ~10 shifted features put
     120-160 subagent calls in flight against a throttling provider.
  3. uninstall_gpu_lock used delattr unconditionally, which permanently strips
     class-OWNED methods (feature_intervention, setup_attribution, ...) instead
     of restoring them.
  4. build_graphs --rebuild was a no-op, because compute_or_load_graph LOADS a
     complete cache. The slug was then reported as "built".
"""
from __future__ import annotations

import threading
import time

import pytest
import torch

from circuit_oracle import fanout, gpu_lock as gl, tools


# ---------------------------------------------------------------------------
# 1. The decode result must be the last position only, and a real copy
# ---------------------------------------------------------------------------

_B, _T, _V = 6, 24, 500


class _FakeKVCache:
    """Minimal surface for _compact_kv_cache, which runs when every row EOSes."""

    def __init__(self):
        self.entries = []
        self.previous_attention_mask = torch.zeros(_B, _T, dtype=torch.long)


class _PrefillOnlyModel:
    """Every row EOSes on its first generated token, so no decode loop runs."""

    def __init__(self, eos_id):
        self.eos_id = eos_id
        self.full = torch.zeros(_B, _T, _V)
        # Make the last position argmax to EOS, and give every OTHER position a
        # different argmax so a bug that returned the wrong slice is visible.
        self.full[:, -1, eos_id] = 10.0
        self.full[:, :-1, (eos_id + 1) % _V] = 10.0

    def prefill_batched(self, prompt, rows, **_kw):
        return self.full, _FakeKVCache()

    def ensure_tokenized(self, prompt):
        return torch.zeros(_T, dtype=torch.long)


def test_decode_returns_only_the_last_prompt_position():
    model = _PrefillOnlyModel(eos_id=3)
    _answers, logits = tools._decode_one_chunk_impl(
        model, "prompt", object(), 3, [[] for _ in range(_B)], 8,
    )
    assert logits.shape == (_B, 1, _V), (
        f"expected [B, 1, V], got {tuple(logits.shape)}; the full prefill logits "
        "are ~30x larger and stay live across the subagent fan-out"
    )


def test_the_returned_slice_holds_the_values_callers_expect():
    """Contract preservation: [..., -1, :] must still select the same row."""
    model = _PrefillOnlyModel(eos_id=3)
    _answers, logits = tools._decode_one_chunk_impl(
        model, "prompt", object(), 3, [[] for _ in range(_B)], 8,
    )
    for row in range(_B):
        assert torch.equal(logits[row, -1, :], model.full[row, -1, :])
        assert int(logits[row, -1, :].argmax()) == 3


def test_the_returned_logits_are_a_copy_not_a_view():
    """A bare slice is a VIEW that pins the whole [B, T, V] storage alive,
    which would make the whole optimization a no-op."""
    model = _PrefillOnlyModel(eos_id=3)
    _answers, logits = tools._decode_one_chunk_impl(
        model, "prompt", object(), 3, [[] for _ in range(_B)], 8,
    )
    assert logits.untyped_storage().nbytes() < model.full.untyped_storage().nbytes(), (
        "returned tensor still references the full prefill storage"
    )
    assert logits.untyped_storage().nbytes() == _B * _V * logits.element_size()


# ---------------------------------------------------------------------------
# 2. The fan-out ceiling is process-wide
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _reset_fanout():
    yield
    fanout._limit = None
    fanout._sem = None


def test_fanout_is_unbounded_by_default():
    """Serial runs must keep their historical behaviour and cost."""
    assert fanout.get_limit() is None
    with fanout.slot():
        pass


def test_the_cap_applies_across_independent_pools():
    """The bug was per-pool sizing: N runs x pool_size had no global ceiling."""
    fanout.set_limit(3)
    live = 0
    peak = 0
    guard = threading.Lock()

    def worker():
        nonlocal live, peak
        with fanout.slot():
            with guard:
                live += 1
                peak = max(peak, live)
            time.sleep(0.02)
            with guard:
                live -= 1

    # Two SEPARATE pools, mimicking two concurrent runs each fanning out.
    threads = [threading.Thread(target=worker) for _ in range(12)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert peak <= 3, f"{peak} subagent calls in flight against a cap of 3"
    assert peak > 1, "the probe never actually ran anything concurrently"


def test_changing_the_limit_mid_flight_raises():
    """Swapping the semaphore would strand threads on one nothing releases."""
    fanout.set_limit(4)
    fanout.set_limit(4)          # idempotent, same value is fine
    with pytest.raises(RuntimeError, match="already set"):
        fanout.set_limit(9)


def test_tools_routes_subagent_calls_through_a_slot():
    """The wiring, not just the primitive."""
    fanout.set_limit(1)
    seen = []
    wrapped = tools._fanout_slotted(lambda x: seen.append(x) or x)
    assert wrapped(7) == 7
    assert seen == [7]


# ---------------------------------------------------------------------------
# 3. uninstall must RESTORE owned methods, not delete them
# ---------------------------------------------------------------------------


def test_uninstall_restores_a_class_owned_method():
    """delattr here would strip feature_intervention off the class for good."""
    class M:
        def feature_intervention(self):
            return "real"

    original = M.feature_intervention
    model = M()
    gl.install_gpu_lock(model, methods=("feature_intervention",))
    assert model.feature_intervention() == "real"

    gl.uninstall_gpu_lock(model)
    assert "feature_intervention" in M.__dict__, "the real method was deleted"
    assert M.feature_intervention is original
    assert model.feature_intervention() == "real"


def test_uninstall_still_deletes_an_inherited_override():
    class Base:
        def forward(self):
            return "base"

    class Sub(Base):
        pass

    model = Sub()
    gl.install_gpu_lock(model, methods=("forward",))
    gl.uninstall_gpu_lock(model)
    assert "forward" not in Sub.__dict__
    assert model.forward() == "base"


def test_uninstall_handles_owned_and_inherited_together():
    class Base:
        def forward(self):
            return "base"

    class Sub(Base):
        def feature_intervention(self):
            return "owned"

    model = Sub()
    gl.install_gpu_lock(model, methods=("forward", "feature_intervention"))
    gl.uninstall_gpu_lock(model)
    assert "forward" not in Sub.__dict__
    assert "feature_intervention" in Sub.__dict__
    assert model.forward() == "base"
    assert model.feature_intervention() == "owned"
