"""Pytest fixtures shared across the Circuit Oracle test tree.

The named fixtures are:

    * tiny_model, built TinyTransformer + tokenizer + Graph
                              wrapped in a ToolContext.
    * baseline_ctx, same as tiny_model, named differently for tests
                              that want to emphasize "this is the baseline
                              context, untouched". Identical object.
    * golden, parsed `golden.json` dict.
    * mock_subagent_client, callable returning canned `TripleLabelRecord`
                              JSON when invoked. Used by the subagent tests
                              for `reinterpret_subagent`.

The fixtures intentionally do not depend on transformer_lens or any HF
weights; everything runs on CPU in <5s.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

import pytest


# Make sure the merged package is importable so tests can import
# `circuit_oracle.*` and `circuit_tracer.*` without a separate
# `pip install -e ..` from the repository root. The pyproject.toml setup is
# fine in CI, this is a developer-friendly fallback.
#
# This used to point at `refusal-jailbreaking/src/`, which held a thread-local
# fork of the package. That fork was merged into the repo-root `src/` and deleted,
# so the path moved up one level. Note it is inserted at position 0 and
# therefore wins over PYTHONPATH, which is why it has to be correct.
_REPO_ROOT = Path(__file__).resolve().parents[1]
_PACKAGE_ROOT = _REPO_ROOT.parent / "src"
if not (_PACKAGE_ROOT / "circuit_oracle").is_dir():
    raise RuntimeError(
        f"merged package not found at {_PACKAGE_ROOT / 'circuit_oracle'}. "
        "The test suite imports circuit_oracle and circuit_tracer from "
        "src/, install it with `uv pip install -e .` from the repository root "
        "or run pytest from the repository root."
    )
if str(_PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(_PACKAGE_ROOT))

# Also expose `tests/fixtures/...` as importable from `fixtures.tiny_model`.
_TESTS = _REPO_ROOT / "tests"
if str(_TESTS) not in sys.path:
    sys.path.insert(0, str(_TESTS))


@pytest.fixture(scope="session")
def tiny_model() -> Any:
    """Fresh ToolContext wrapping the toy transformer + transcoder + graph.

    Session-scoped because building the toy is deterministic and pure.
    Tests that need to mutate ctx state (intervention bookkeeping etc.)
    should copy fields they need or use the function-scoped `baseline_ctx`.
    """
    from fixtures.tiny_model import build_tiny_fixture
    return build_tiny_fixture()


@pytest.fixture()
def baseline_ctx() -> Any:
    """Function-scoped fresh ToolContext.

    Tests that mutate `ctx.anchor_passed`, `ctx.single_factors`, etc. should
    use this fixture so each test starts from a clean slate.
    """
    from fixtures.tiny_model import build_tiny_fixture
    return build_tiny_fixture()


@pytest.fixture(scope="session")
def golden() -> dict:
    """Frozen baseline outputs captured by `tiny_model.capture_golden`."""
    path = Path(__file__).parent / "fixtures" / "golden.json"
    with open(path) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Mock subagent client
# ---------------------------------------------------------------------------

_CANNED_TRIPLE_LABEL = {
    "autointerp": "el",
    "pre_label": (
        "uncertain; label is fragment but promoted tokens "
        "'unfortunately'/'sadly' suggest refusal-affect softener"
    ),
    "post_label": (
        "decisive refusal-affect gate; at -1 'Unfortunately' demoted and "
        "topic emerged"
    ),
    "divergence": "autointerp_only",
}


class _Call:
    """Lightweight record of a single mock invocation.

    Backs `_MockSubagentClient.call_args` (the LAST call). Mirrors the
    minimum surface tests exercise from `unittest.mock.Mock.call_args`:
    `.args` (positional tuple) and `.kwargs` (keyword dict).
    """

    __slots__ = ("args", "kwargs")

    def __init__(self, args: tuple, kwargs: dict) -> None:
        self.args = args
        self.kwargs = kwargs


class _MockSubagentClient:
    """Callable stand-in for the Sonnet client used by reinterpret_subagent.

    Each call records its inputs (so tests can assert prompt structure)
    and returns the canned `TripleLabelRecord` JSON string. The default
    record can be overridden per-instance via `set_response(...)`.

    Also exposes a subset of the `unittest.mock.Mock` surface so the subagent
    tests that prefer that idiom work without dragging in `unittest.mock`:
    `.return_value`, `.side_effect`, `.call_count`, `.called`, `.call_args`.
    """

    def __init__(self) -> None:
        self.calls: list[dict] = []
        self._response = dict(_CANNED_TRIPLE_LABEL)
        self._raise_n_times = 0
        self._exc: Exception | None = None
        self.return_value: object = None
        self.side_effect: object = None

    def set_response(self, record: dict) -> None:
        self._response = dict(record)

    def queue_failures(self, n: int, exc: Exception | None = None) -> None:
        """Make the next `n` calls raise `exc` (default RuntimeError) then
        succeed on call `n+1`. Used by `test_subagent_retry_twice`."""
        self._raise_n_times = n
        self._exc = exc or RuntimeError("mock subagent transient failure")

    @property
    def call_count(self) -> int:
        return len(self.calls)

    @property
    def called(self) -> bool:
        return len(self.calls) > 0

    @property
    def call_args(self) -> _Call | None:
        if not self.calls:
            return None
        last = self.calls[-1]
        return _Call(args=last["args"], kwargs=last["kwargs"])

    def __call__(self, *args, **kwargs):
        self.calls.append({"args": args, "kwargs": kwargs})
        # Precedence: side_effect -> queue_failures (legacy) -> return_value
        # -> set_response default.
        if self.side_effect is not None and callable(self.side_effect):
            return self.side_effect(*args, **kwargs)
        if self._raise_n_times > 0:
            self._raise_n_times -= 1
            assert self._exc is not None
            raise self._exc
        if self.return_value is not None:
            return self.return_value
        return json.dumps(self._response)


@pytest.fixture()
def mock_subagent_client(monkeypatch) -> _MockSubagentClient:
    """Fresh mock subagent per test (call log is not shared across tests).

    Also installs the mock as ``circuit_oracle.subagent._SUBAGENT_CLIENT`` so
    ``reinterpret_subagent`` picks it up without an explicit ``client=`` kwarg.
    The monkeypatch is torn down automatically at test teardown.
    """
    client = _MockSubagentClient()
    try:
        import circuit_oracle.subagent as _sub
        monkeypatch.setattr(_sub, "_SUBAGENT_CLIENT", client, raising=False)
    except ImportError:
        pass
    return client
