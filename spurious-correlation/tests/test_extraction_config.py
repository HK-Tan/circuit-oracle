"""Task 1 - the feature-node cap is a decision, not an incidental default.

Task 1 builds at **4096** while tasks 2 and 3 build at 8192, and that asymmetry
is deliberate: Gemma-2-2B is 26 layers at d_model 2304 against Qwen3-4B's 36 at
2560, and the archived graphs behind the numbers in `spurious_probes.tex` were
built at 4096. Raising it silently would create a new generation whose feature
counts are not comparable with the published ones, and feature count is the
headline quantity in that section. Decided 2026-07-27.

The cap used to appear as a bare `4096` literal in four places, so "change the
cap" meant "find all four". It is one named constant now, and these tests pin
both the value and the single-definition property.

Source-level by necessity. `circuit_extraction.py` executes top to bottom at
import (it loads Gemma-2-2B and asserts the probe checkpoints exist), so
there is nothing importable to assert against off-GPU. Parsed with `ast` rather
than matched as a substring, so a comment mentioning 4096 cannot satisfy it.
"""
from __future__ import annotations

import ast
from pathlib import Path

TASK_ROOT = Path(__file__).resolve().parents[1]
EXTRACTION = TASK_ROOT / "scripts" / "circuit_extraction.py"

# The reported task-1 generation. Not 8192, see the module docstring.
REPORTED_MAX_FEATURE_NODES = 4096


def _module() -> ast.Module:
    return ast.parse(EXTRACTION.read_text())


def _assignments(tree: ast.Module, name: str) -> list[ast.AST]:
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
            if name in targets:
                out.append(node.value)
    return out


def test_cap_is_the_reported_generation() -> None:
    values = _assignments(_module(), "MAX_FEATURE_NODES")
    assert len(values) == 1, "MAX_FEATURE_NODES must be defined exactly once"
    assert isinstance(values[0], ast.Constant)
    assert values[0].value == REPORTED_MAX_FEATURE_NODES


def test_cap_is_not_the_other_tracks_value() -> None:
    """Guards against a well-meaning "standardize the three tracks" edit."""
    values = _assignments(_module(), "MAX_FEATURE_NODES")
    assert values[0].value != 8192, (
        "8192 is tasks 2 and 3. Task 1 is Gemma-2-2B and its published feature "
        "counts were measured at 4096."
    )


def test_no_call_site_hardcodes_the_cap() -> None:
    """Every attribution call must read the constant, not a literal.

    Four call sites carried a bare 4096, which is how a cap change silently
    becomes a partial cap change.
    """
    offenders = []
    for node in ast.walk(_module()):
        if not isinstance(node, ast.Call):
            continue
        for kw in node.keywords:
            if kw.arg == "max_feature_nodes" and isinstance(kw.value, ast.Constant):
                offenders.append(kw.value.value)
    assert not offenders, (
        f"max_feature_nodes passed as a literal {offenders}; use MAX_FEATURE_NODES"
    )


def test_batch_size_is_also_named() -> None:
    """Kept next to the cap so the two are not confused.

    Batch size affects build speed only. The cap changes the graph contents.
    """
    values = _assignments(_module(), "ATTR_BATCH_SIZE")
    assert len(values) == 1
    assert isinstance(values[0], ast.Constant)
    assert values[0].value == 256
