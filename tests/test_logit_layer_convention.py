"""The output-logit layer convention has to be one number, everywhere.

Three places quote it and they must agree for a given subject: the system
prompt ("declare the output node at layer=N"), the build_circuit tool
description, and the build_circuit validator's featureless-node exemption. It
was hardcoded to 36 (Qwen3-4B) in the last two, which is invisible while the
prompt also says 36 and becomes a BUILD-time rejection the moment the prompt is
parameterized for a shallower subject like Gemma-2-2B.
"""

from __future__ import annotations

import pytest
from conftest import make_ctx, make_graph

from circuit_oracle.tool_schemas import build_orchestrator_tools
from circuit_oracle.tools import build_circuit

GEMMA_LAYERS = 26
QWEN_LAYERS = 36


def _logit_node(layer: int) -> dict:
    return {"id": "Out", "label": "output logits", "layer": layer, "features": []}


def _build(n_layers: int, node_layer: int):
    ctx = make_ctx(make_graph(n_layers=n_layers))
    return build_circuit(ctx, nodes=[_logit_node(node_layer)], edges=[])


@pytest.mark.parametrize("n_layers", [QWEN_LAYERS, GEMMA_LAYERS])
def test_featureless_logit_node_is_accepted_at_the_subjects_own_depth(n_layers):
    assert "error" not in _build(n_layers, n_layers)


def test_a_gemma_graph_rejects_the_qwen_logit_layer():
    """The regression that motivated this: 36 is not a layer of a 26-layer model."""
    result = _build(GEMMA_LAYERS, QWEN_LAYERS)
    assert "error" in result
    assert f"layer={GEMMA_LAYERS}" in result["error"], (
        "the rejection must name the layer this subject actually uses"
    )


def test_embedding_nodes_stay_exempt_at_layer_zero():
    assert "error" not in _build(GEMMA_LAYERS, 0)


def test_a_featureless_node_elsewhere_is_still_rejected():
    assert "error" in _build(GEMMA_LAYERS, 7)


def test_missing_graph_config_raises_rather_than_assuming_36():
    ctx = make_ctx()
    ctx.graph = None
    with pytest.raises(RuntimeError, match="n_layers"):
        build_circuit(ctx, nodes=[_logit_node(36)], edges=[])


# ---------------------------------------------------------------------------
# The tool description the agent reads
# ---------------------------------------------------------------------------


def _build_circuit_description(**kwargs) -> str:
    (tool,) = [t for t in build_orchestrator_tools(**kwargs) if t["name"] == "build_circuit"]
    return tool["description"]


def test_description_defaults_to_the_qwen_convention():
    assert "output logit nodes (layer=36, features=[])" in _build_circuit_description()


def test_description_follows_the_subject_depth():
    text = _build_circuit_description(n_layers=GEMMA_LAYERS)
    assert "output logit nodes (layer=26, features=[])" in text
    assert "layer=36" not in text


def test_retargeting_does_not_disturb_the_other_schemas():
    plain = {t["name"]: t for t in build_orchestrator_tools()}
    retargeted = {t["name"]: t for t in build_orchestrator_tools(n_layers=GEMMA_LAYERS)}
    assert plain.keys() == retargeted.keys()
    differing = [n for n in plain if plain[n] != retargeted[n]]
    assert differing == ["build_circuit"]


# ---------------------------------------------------------------------------
# Excluded-tool names
# ---------------------------------------------------------------------------


def test_a_stale_excluded_tool_name_is_rejected():
    """A plain set difference makes a typo a silent no-op, which is how the
    retired get_diff_specific_features stayed in the ELK exclusion lists for
    months while every ELK run still exposed the tools it meant to remove."""
    with pytest.raises(ValueError, match="get_diff_specific_features"):
        build_orchestrator_tools(excluded_tools=["get_diff_specific_features"])


def test_a_real_excluded_tool_name_still_works():
    names = {t["name"] for t in build_orchestrator_tools(excluded_tools=["inspect_feature"])}
    assert "inspect_feature" not in names
    assert "build_circuit" in names
