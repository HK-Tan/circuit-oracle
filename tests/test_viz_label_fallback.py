"""The unlabelled-node crash that cost a run its report.md (2026-07-28).

viz.py:248 read n["label"] with a bare subscript while every other node read in
the module (lines 74, 85, 94) defaulted. One run in 176 of the task-2 grid hit
it. Because save_run_results writes oracle_result.json BEFORE the SVG and
report.md AFTER it, the crash left a directory that item_done() counts as
complete but that has no report.md for the eval scripts to read.
"""
from circuit_oracle.viz import create_circuit_svg


def _svg(nodes):
    return create_circuit_svg({"nodes": nodes, "edges": []}, [], {}, "prompt")


def test_node_without_a_label_does_not_raise():
    """A node with no 'label' key must render, falling back to its id."""
    svg = _svg([{"id": "sn1", "layer": 20, "features": []}])
    assert "sn1" in svg


# Note: "id" and "layer" stay bare subscripts in viz.py and that is fine, both
# are set by construction for every node (viz.py:173-177, and "id" is the dict
# key). "label" was the only genuinely optional one, which is why it was the
# only one that blew up.


def test_labelled_node_is_unaffected():
    svg = _svg([{"id": "x", "label": "refusal gate", "layer": 20, "features": []}])
    assert "refusal" in svg
