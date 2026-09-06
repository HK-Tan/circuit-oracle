"""The two byte-copied base grafts: autointerp.py and autointerp_server.py.

autointerp.py is imported by 10 of the 10 secret_discovery scripts and by
elk_tools, so its surface is checked unconditionally. autointerp_server.py needs
fastapi, which is a real dependency of the package but is not installed on every
developer machine, so that half is skipped when the import is unavailable rather
than failing the suite.

No LLM call is ever made. describe_feature is not exercised, only construction
and the pure payload reshaping.
"""

from __future__ import annotations

import gzip
import json
import struct
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# autointerp.py
# ---------------------------------------------------------------------------


def test_autointerp_surface():
    from circuit_oracle import autointerp

    for name in ("FeatureCache", "AutointerpStore", "AutointerpConfig", "describe_feature"):
        assert hasattr(autointerp, name)


def test_autointerp_config_defaults():
    from circuit_oracle.autointerp import AutointerpConfig

    cfg = AutointerpConfig(features_dir="/f", cache_dir="/c")
    assert cfg.features_dir == "/f"
    assert cfg.cache_dir == "/c"
    assert isinstance(cfg.model, str) and cfg.model


def test_feature_cache_fails_loud_on_a_missing_index(tmp_path):
    """A missing index.json.gz means the transcoder feature dump was never
    downloaded. Raise, do not hand back an empty cache that would make every
    diff-specificity ranking silently empty."""
    from circuit_oracle.autointerp import FeatureCache

    with pytest.raises(FileNotFoundError, match="index.json.gz"):
        FeatureCache(str(tmp_path))


def _write_tiny_feature_dump(root: Path) -> None:
    """Build a one-feature features/ directory in the on-disk format.

    Layout per feature: a 4-byte little-endian length prefix followed by the
    gzipped JSON record, with byte offsets in index.json.gz.
    """
    record = {
        "activation_frequency": 0.004,
        "top_logits": ["apple", "apples"],
        "bottom_logits": ["banana"],
        "examples_quantiles": [
            {"examples": [{"tokens": ["the", " apple"], "tokens_acts_list": [0.0, 3.2]}]}
        ],
    }
    payload = gzip.compress(json.dumps(record).encode())
    blob = struct.pack("<I", len(payload)) + payload
    (root / "layer0.bin").write_bytes(blob)
    index = {
        "version": 1,
        "0": {"filename": "layer0.bin", "offsets": [0, len(blob)]},
    }
    with gzip.open(root / "index.json.gz", "wb") as f:
        f.write(json.dumps(index).encode())


def test_feature_cache_round_trips_a_record(tmp_path):
    from circuit_oracle.autointerp import FeatureCache

    _write_tiny_feature_dump(tmp_path)
    cache = FeatureCache(str(tmp_path))
    rec = cache.get(0, 0)
    assert rec["activation_frequency"] == 0.004
    assert rec["top_logits"] == ["apple", "apples"]
    with pytest.raises(KeyError):
        cache.get(9, 0)          # layer not in the index
    with pytest.raises(KeyError):
        cache.get(0, 99)         # feature out of range


# ---------------------------------------------------------------------------
# autointerp_server.py (the local Neuronpedia-shaped shim)
# ---------------------------------------------------------------------------


def test_server_app_construction(tmp_path):
    pytest.importorskip("fastapi")
    from circuit_oracle.autointerp_server import create_app

    _write_tiny_feature_dump(tmp_path)
    app = create_app(features_dir=str(tmp_path), cache_dir=str(tmp_path / "cache"))
    routes = {getattr(r, "path", None) for r in app.routes}
    # /healthz is what tools.check_feature_backend probes at run start.
    assert "/healthz" in routes
    assert "/api/feature/{model_id}/{sae_id}/{feature_idx}" in routes


def test_server_refuses_to_start_without_directories(monkeypatch):
    pytest.importorskip("fastapi")
    from circuit_oracle.autointerp_server import create_app

    monkeypatch.delenv("AUTOINTERP_FEATURES_DIR", raising=False)
    monkeypatch.delenv("AUTOINTERP_CACHE_DIR", raising=False)
    with pytest.raises(RuntimeError, match="features_dir and cache_dir"):
        create_app()


def test_layer_parsing_from_sae_id():
    pytest.importorskip("fastapi")
    from circuit_oracle.autointerp_server import _layer_from_sae_id

    assert _layer_from_sae_id("20-transcoder-hp") == 20
    with pytest.raises(Exception):
        _layer_from_sae_id("transcoder-hp")


def test_shim_payload_matches_what_the_client_parses():
    """The shim's JSON must line up field for field with what
    tools._http_inspect_payload reads back, or the round trip goes blind."""
    pytest.importorskip("fastapi")
    from circuit_oracle.autointerp_server import _to_neuronpedia_shape

    feature_data = {
        "top_logits": ["apple", "apples"],
        "bottom_logits": ["banana"],
        "activation_frequency": 0.004,
        "examples_quantiles": [
            {"examples": [{"tokens": ["the", " apple"], "tokens_acts_list": [0.0, 3.2]}]}
        ],
    }
    shaped = _to_neuronpedia_shape({"label": "apple mentions"}, feature_data)
    assert shaped["explanations"][0]["description"] == "apple mentions"
    assert shaped["pos_str"] == ["apple", "apples"]
    assert shaped["neg_str"] == ["banana"]
    assert shaped["frac_nonzero"] == 0.004
    assert shaped["activations"][0]["tokens"] == ["the", " apple"]


def test_client_parses_the_shim_payload_end_to_end(monkeypatch):
    """Feed the shim's own output through the HTTP parsing half, so the two
    sides of the shim contract are tested against each other."""
    pytest.importorskip("fastapi")
    from circuit_oracle import tools
    from circuit_oracle.autointerp_server import _to_neuronpedia_shape

    from conftest import make_ctx

    shaped = _to_neuronpedia_shape(
        {"label": "apple mentions"},
        {
            "top_logits": ["apple"],
            "bottom_logits": ["banana"],
            "activation_frequency": 0.004,
            "examples_quantiles": [
                {"examples": [{"tokens": ["the", " apple"], "tokens_acts_list": [0.0, 3.2]}]}
            ],
        },
    )

    class _Resp:
        def raise_for_status(self):
            return None

        def json(self):
            return shaped

    monkeypatch.setattr(tools.requests, "get", lambda url, **kw: _Resp())
    ctx = make_ctx(neuronpedia_base_url="http://127.0.0.1:8765")
    payload = tools._fetch_inspect_payload(ctx, layer=0, feature_idx=0)
    assert payload["label"] == "apple mentions"
    assert payload["autointerp"] == "apple mentions"
    assert payload["promoted_tokens"] == ["apple"]
    assert payload["suppressed_tokens"] == ["banana"]
    assert payload["frac_nonzero"] == 0.004
    assert payload["top_activating_examples"][0]["max_activation"] == 3.2
