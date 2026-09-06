"""Integration entry point: replay a transcript against the real
tool surface and persist oracle_result.json.

This module wires the per-task tools together so the end-to-end smoke
test (tests/test_integration.py) can exercise the full pipeline on the
toy fixture without standing up a real LLM orchestrator. The transcript
is the script of which tools to call with what arguments; the actual
outputs come from the real tool functions running against ctx.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any

from .config import ToolContext
from .saving import _encode_reassess_key


def _parse_key(key):
    """Normalize a pin_features / supernode key into a (layer, feat_idx, pos) tuple.

    Accepts either a tuple/list (passed through after int-cast) or a JSON
    string like ``"(0, 1, 3)"`` (the wire format the orchestrator emits).
    """
    if isinstance(key, (tuple, list)) and len(key) == 3:
        return (int(key[0]), int(key[1]), int(key[2]))
    if isinstance(key, str):
        parsed = ast.literal_eval(key)
        if isinstance(parsed, (tuple, list)) and len(parsed) == 3:
            return (int(parsed[0]), int(parsed[1]), int(parsed[2]))
    raise ValueError(f"cannot parse pin/supernode key: {key!r}")


def run_oracle_pipeline(
    *,
    ctx: ToolContext,
    mock_transcript: list[dict],
    subagent_client: Any = None,  # noqa: ARG001, fixture already installs _SUBAGENT_CLIENT
    output_dir: Path,
) -> Path:
    """Replay a mock orchestrator transcript and persist oracle_result.json.

    Walks ``mock_transcript`` entries in order and dispatches each tool
    call to the real tool function. Side effects (pinned_features,
    reassess_records, etc.) accumulate on ``ctx`` exactly as they would
    in a real orchestrator run. Returns the path to oracle_result.json.

    Recognised tools (changes.md sec 2.2 three-tool chain + sec 2.5):
      - build_circuit: populate ctx.build_features from the input nodes
        (no real build_circuit call; the toy fixture has no Neuronpedia
        backing).
      - pin_features: dispatch with parsed tuple keys.
      - batched_anchor_sweep: dispatch; auto-REASSESS fires inside.
      - batched_supernode_sweep: dispatch; rounds counted for the result
        summary.
    """
    from . import tools as tools_mod

    supernode_rounds: list[dict] = []

    for entry in mock_transcript:
        tool = entry.get("tool", "")
        inputs = entry.get("input", {}) or {}

        if tool == "build_circuit":
            feats: set[tuple[int, int, int]] = set()
            for node in inputs.get("nodes", []) or []:
                for f in node.get("features", []) or []:
                    feats.add(
                        (int(f["layer"]), int(f["feature_idx"]), int(f["pos"]))
                    )
            ctx.build_features = feats
        elif tool == "pin_features":
            raw = inputs.get("pre_hypotheses", {}) or {}
            parsed = {_parse_key(k): v for k, v in raw.items()}
            tools_mod.pin_features(ctx, pre_hypotheses=parsed)
        elif tool == "batched_anchor_sweep":
            tools_mod.batched_anchor_sweep(ctx)
        elif tool == "batched_supernode_sweep":
            tuples = inputs.get("tuples", []) or []
            result = tools_mod.batched_supernode_sweep(ctx, tuples=tuples)
            supernode_rounds.append({
                "n_tuples": result.get("n_tuples", len(tuples)),
                "n_scales": result.get("n_scales", 0),
            })
        else:
            raise ValueError(f"unknown tool in transcript: {tool!r}")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    reassess = getattr(ctx, "reassess_records", {}) or {}
    pinned = getattr(ctx, "pinned_features", {}) or {}
    inspect_cache = getattr(ctx, "inspect_cache", {}) or {}
    build_features = getattr(ctx, "build_features", set()) or set()

    payload = {
        "reassess_records": {
            _encode_reassess_key(k): v for k, v in reassess.items()
        },
        "pinned_features": {
            _encode_reassess_key(k): v for k, v in pinned.items()
        },
        "build_features": [_encode_reassess_key(k) for k in build_features],
        "inspect_cache_keys": [_encode_reassess_key(k) for k in inspect_cache.keys()],
        "supernode_rounds": supernode_rounds,
    }
    out_path = output_dir / "oracle_result.json"
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2, default=str)
    return out_path
