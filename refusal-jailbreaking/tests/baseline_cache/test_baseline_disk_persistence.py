"""Assert baseline artifacts persist to disk and round-trip on cache hit.

compute_or_load_graph must write two new files alongside the graph cache file:
  - `{cache_path}.baseline.pt`   - tensors (baseline_activations, baseline logits)
  - `{cache_path}.baseline.json` - JSON-serializable bits (baseline_top5, baseline_answer)

On a cache hit (second call with the same cache path), both files must be loaded
from disk without re-running the underlying model forward pass.

Without this, baseline_activations and baseline_answer would be recomputed on
every load and baseline_top5 would not survive a cache hit at all.
"""
from __future__ import annotations

import json
import os

import pytest
import torch


def test_baseline_pt_written_on_first_compute(tiny_model, tmp_path, monkeypatch):
    """First compute_or_load_graph call must write {cache_path}.baseline.pt to disk."""
    from circuit_oracle.graph_compute import compute_or_load_graph

    # TinyReplacementModel is not a real ReplacementModel; short-circuit attribute()
    # so the test exercises only the persistence path, not circuit_tracer attribution.
    monkeypatch.setattr(
        "circuit_oracle.graph_compute.attribute",
        lambda *a, **k: tiny_model.graph,
    )

    cache_path = tmp_path / "graph.pt"
    _ = compute_or_load_graph(
        prompt=tiny_model.baseline_prompt,
        model=tiny_model.replacement_model,
        cache_path=str(cache_path),
    )
    baseline_pt = tmp_path / "graph.pt.baseline.pt"
    assert baseline_pt.exists(), (
        f"{baseline_pt} not written. compute_or_load_graph must persist baseline tensors."
    )


def test_baseline_json_written_on_first_compute(tiny_model, tmp_path, monkeypatch):
    """First compute_or_load_graph call must write {cache_path}.baseline.json."""
    from circuit_oracle.graph_compute import compute_or_load_graph

    # TinyReplacementModel is not a real ReplacementModel; short-circuit attribute()
    # so the test exercises only the persistence path, not circuit_tracer attribution.
    monkeypatch.setattr(
        "circuit_oracle.graph_compute.attribute",
        lambda *a, **k: tiny_model.graph,
    )

    cache_path = tmp_path / "graph.pt"
    _ = compute_or_load_graph(
        prompt=tiny_model.baseline_prompt,
        model=tiny_model.replacement_model,
        cache_path=str(cache_path),
    )
    baseline_json = tmp_path / "graph.pt.baseline.json"
    assert baseline_json.exists(), (
        f"{baseline_json} not written. compute_or_load_graph must persist baseline_top5 "
        "and baseline_answer as JSON."
    )
    # Verify it parses and contains expected keys.
    with open(baseline_json) as fh:
        payload = json.load(fh)
    assert "baseline_top5" in payload, "baseline.json missing baseline_top5 key"
    assert "baseline_answer" in payload, "baseline.json missing baseline_answer key"


def test_baseline_loaded_from_disk_on_cache_hit(tiny_model, tmp_path, monkeypatch):
    """Second compute_or_load_graph call (cache hit) must read baseline from disk, not re-run model."""
    from circuit_oracle import graph_compute
    from circuit_oracle.graph_compute import compute_or_load_graph

    # TinyReplacementModel is not a real ReplacementModel; short-circuit attribute()
    # so the test exercises only the persistence path, not circuit_tracer attribution.
    monkeypatch.setattr(
        "circuit_oracle.graph_compute.attribute",
        lambda *a, **k: tiny_model.graph,
    )

    cache_path = tmp_path / "graph.pt"

    # First call populates the cache. Capture the fresh baseline_activations
    # tensor so we can byte-compare it against the cache-loaded copy below.
    fresh_result = compute_or_load_graph(
        prompt=tiny_model.baseline_prompt,
        model=tiny_model.replacement_model,
        cache_path=str(cache_path),
    )
    fresh_baseline_acts = fresh_result["baseline_activations"]

    # Spy on the forward-pass entry points: on a cache hit, neither
    # get_activations (used for baseline_acts) nor generate_response (used for
    # baseline_answer) should fire, both values now live on disk.
    activations_call_count = {"n": 0}
    generate_call_count = {"n": 0}

    original_get_activations = tiny_model.replacement_model.get_activations

    def spy_get_activations(*args, **kwargs):
        activations_call_count["n"] += 1
        return original_get_activations(*args, **kwargs)

    monkeypatch.setattr(
        tiny_model.replacement_model, "get_activations", spy_get_activations
    )

    if hasattr(graph_compute, "generate_response"):
        original_generate = graph_compute.generate_response

        def spy_generate(*args, **kwargs):
            generate_call_count["n"] += 1
            return original_generate(*args, **kwargs)

        monkeypatch.setattr(graph_compute, "generate_response", spy_generate)

    # Second call should be a cache hit.
    result = compute_or_load_graph(
        prompt=tiny_model.baseline_prompt,
        model=tiny_model.replacement_model,
        cache_path=str(cache_path),
    )

    assert activations_call_count["n"] == 0, (
        f"get_activations called {activations_call_count['n']} times on cache hit; "
        "must be 0 because baseline_activations is now loaded from {cache_path}.baseline.pt."
    )
    assert generate_call_count["n"] == 0, (
        f"generate_response called {generate_call_count['n']} times on cache hit; "
        "must be 0 because baseline_answer is now loaded from {cache_path}.baseline.json."
    )
    # Sanity: baseline_top5 must survive the round trip.
    assert result.get("baseline_top5") is not None, (
        "compute_or_load_graph return value missing baseline_top5 on cache hit."
    )
    # Tensor coherence: the loaded baseline_activations must be byte-identical
    # to the freshly-computed one. JSON-round-tripping baseline_answer is not
    # enough, the .baseline.pt tensor is what intervene_feature / intervene_supernode
    # use for scaled patching, and a silent dtype/shape drift here breaks every
    # downstream causal measurement.
    loaded_baseline_acts = result["baseline_activations"]
    assert torch.equal(loaded_baseline_acts, fresh_baseline_acts), (
        "baseline_activations loaded from {cache_path}.baseline.pt does not match "
        "the freshly-computed tensor. The baseline cache must round-trip "
        "the activations tensor byte-for-byte."
    )
