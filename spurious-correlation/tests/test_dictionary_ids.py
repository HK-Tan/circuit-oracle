"""Task 1 - the Gemma Scope dictionary ids are layer specific, not one template.

The 2026-07-27 coverage check found that the 16k
transcoder release publishes a different average-l0 suffix at every layer, so
the old single template ``layer_{layer}/width_16k/average_l0_15`` resolved only
at layer 22. At layers 12 and 17 it named a folder that does not exist and the
load would crash. Layer 22 working is exactly why the earlier
layer-22-everything runs never surfaced this.

The pinned values below were verified against two independent sources on
2026-07-27 and they agree byte for byte:
  - the SAELens registry (one curated 16k id per layer for the release
    ``gemma-scope-2b-pt-transcoders``), and
  - the ``hfFolderId`` Neuronpedia records for its
    ``{layer}-gemmascope-transcoder-16k`` sources.
The Neuronpedia half is the load-bearing one. The reader
(judge_sae_features.py) fetches hosted explanations by feature index, and the
indices only mean the same thing if the weights we encode with come from the
same folder Neuronpedia built its dashboards from.

Source-level with ``ast`` for the same reason as test_extraction_config.py,
the script imports torch and prints the device at module import.
"""
from __future__ import annotations

import ast
from pathlib import Path

TASK_ROOT = Path(__file__).resolve().parents[1]
RANKER = TASK_ROOT / "scripts" / "rank_sae_features_by_probe.py"

# Verified 2026-07-27, see the module docstring. Change only with a fresh
# check of both the SAELens registry and the Neuronpedia source metadata.
VERIFIED_TRANSCODER_L0 = {12: 6, 17: 12, 22: 15}
VERIFIED_SAE_RELEASE = "gemma-scope-2b-pt-res-canonical"
VERIFIED_SAE_ID_TEMPLATE = "layer_{layer}/width_16k/canonical"


def _module() -> ast.Module:
    return ast.parse(RANKER.read_text())


def _assignment(tree: ast.Module, name: str):
    values = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
            if name in targets:
                values.append(node.value)
    assert len(values) == 1, f"{name} must be assigned exactly once, got {len(values)}"
    return values[0]


def test_res_template_is_the_canonical_release() -> None:
    """Canonical exists at 12, 17, and 22 and matches Neuronpedia's res-16k."""
    tree = _module()
    assert ast.literal_eval(_assignment(tree, "SAE_RELEASE")) == VERIFIED_SAE_RELEASE
    assert (
        ast.literal_eval(_assignment(tree, "SAE_ID_TEMPLATE"))
        == VERIFIED_SAE_ID_TEMPLATE
    )


def test_transcoder_map_is_the_verified_alignment() -> None:
    value = ast.literal_eval(_assignment(_module(), "TRANSCODER_L0"))
    assert value == VERIFIED_TRANSCODER_L0, (
        f"TRANSCODER_L0 = {value} does not match the 2026-07-27 verified "
        f"SAELens/Neuronpedia alignment {VERIFIED_TRANSCODER_L0}. If this is "
        f"deliberate, re-verify both sources and update this test."
    )


def test_single_l0_template_is_gone() -> None:
    """The bug shape was one template string with a fixed l0. Keep it dead."""
    tree = _module()
    offenders = [
        t.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        for t in node.targets
        if isinstance(t, ast.Name) and t.id == "TRANSCODER_ID_TEMPLATE"
    ]
    assert not offenders, "TRANSCODER_ID_TEMPLATE is back, use TRANSCODER_L0"
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            assert "average_l0_15" not in node.value or "{" not in node.value, (
                "a template string carrying a fixed average_l0_15 reappeared"
            )


def test_every_probe_layer_has_a_transcoder_id() -> None:
    """A new dataset at an unmapped layer must fail here, not on the pod."""
    tree = _module()
    probe_layers = set(ast.literal_eval(_assignment(tree, "PROBE_LAYER")).values())
    mapped = set(ast.literal_eval(_assignment(tree, "TRANSCODER_L0")))
    missing = probe_layers - mapped
    assert not missing, (
        f"PROBE_LAYER uses layers {sorted(missing)} with no TRANSCODER_L0 entry. "
        f"Look up the curated 16k id for those layers and verify it against "
        f"Neuronpedia before adding it."
    )
