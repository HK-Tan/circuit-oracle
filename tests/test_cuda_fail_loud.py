"""A poisoned CUDA context must abort the run, not degrade into a fake result.

Regression test for 2026-07-28: a device-side assert (out-of-bounds advanced
index in IndexKernel.cu) poisoned one process's CUDA context. Every later GPU
call raised, `execute_tool` converted each one into an ordinary
`{"error": ...}` dict, and the agent carried on and wrote seven complete
oracle_result.json files with no circuit evidence behind them. They were
indistinguishable from real results without reading the shard log.
"""

import pytest
import torch

from circuit_oracle.subagent import execute_tool, is_unrecoverable_cuda_error


class _Ctx:
    """Stand-in ToolContext. execute_tool only forwards it to the dispatch."""
    baseline_activations = None


# ── the detector ─────────────────────────────────────────────────────────────

@pytest.mark.parametrize("msg", [
    "CUDA error: device-side assert triggered",
    "RuntimeError: CUDA error: an illegal memory access was encountered",
    "CUDA error: misaligned address",
    "CUDA error: unspecified launch failure",
])
def test_fatal_markers_detected(msg):
    assert is_unrecoverable_cuda_error(RuntimeError(msg))


def test_detection_is_case_insensitive():
    assert is_unrecoverable_cuda_error(RuntimeError("Device-Side Assert Triggered"))


def test_oom_is_recoverable():
    """OOM leaves the context usable and the intervention path retries it after
    empty_cache(). Treating it as fatal would throw away working retry logic."""
    assert not is_unrecoverable_cuda_error(
        torch.cuda.OutOfMemoryError("CUDA out of memory. Tried to allocate 2.00 GiB")
    )


def test_oom_by_message_is_recoverable():
    """Some paths surface OOM as a plain RuntimeError, so the message must not
    match either. 'CUDA out of memory' contains 'CUDA' but not 'CUDA error'."""
    assert not is_unrecoverable_cuda_error(
        RuntimeError("CUDA out of memory. Tried to allocate 2.00 GiB")
    )


def test_ordinary_errors_are_recoverable():
    for exc in (ValueError("feature_idx 999999 is out of range"),
                KeyError("layer"),
                RuntimeError("feature not found at pos")):
        assert not is_unrecoverable_cuda_error(exc)


# ── the dispatch behaviour ───────────────────────────────────────────────────

def _dispatch_raising(exc, monkeypatch):
    monkeypatch.setattr(
        "circuit_oracle.subagent._make_tool_dispatch",
        lambda ctx, causal_discovery=False: {"get_top_logits": lambda args: (_ for _ in ()).throw(exc)},
    )


def test_cuda_fault_propagates_out_of_execute_tool(monkeypatch):
    """The whole point: the run must die rather than produce a narrative."""
    _dispatch_raising(RuntimeError("CUDA error: device-side assert triggered"), monkeypatch)
    with pytest.raises(RuntimeError, match="device-side assert"):
        execute_tool(_Ctx(), "get_top_logits", {})


def test_ordinary_failure_still_becomes_an_error_dict(monkeypatch):
    """Agent-recoverable failures must keep working, or every malformed tool
    call would kill a run."""
    _dispatch_raising(ValueError("k must be positive"), monkeypatch)
    out = execute_tool(_Ctx(), "get_top_logits", {})
    assert isinstance(out, dict) and "k must be positive" in out["error"]


def test_oom_still_becomes_an_error_dict(monkeypatch):
    _dispatch_raising(torch.cuda.OutOfMemoryError("CUDA out of memory"), monkeypatch)
    out = execute_tool(_Ctx(), "get_top_logits", {})
    assert isinstance(out, dict) and "error" in out


def test_unknown_tool_is_unaffected():
    out = execute_tool(_Ctx(), "no_such_tool", {})
    assert "Unknown tool" in out["error"]
