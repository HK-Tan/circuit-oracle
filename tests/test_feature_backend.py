"""Feature-lookup routing and the run-start backend health check.

Two regressions are pinned here.

1. The hardcoded host. Pre-merge, the causal trunk built the Neuronpedia URL
   from a literal "https://www.neuronpedia.org" and ignored
   ctx.neuronpedia_base_url, so every ELK inspect_feature call silently queried
   public Neuronpedia for a transcoder set that is not hosted there, while the
   feature-directory tools kept working off local disk. That is the
   "half-healthy run" failure mode (merge-specs.md spec B section 3,
   inspect_feature).

2. The health check itself. It must fail loud when the configured shim is dead,
   and must stay a no-op on the public default, because public Neuronpedia
   serves no /healthz and an ungated check would break every refusal and probe
   run.

No sockets are opened. requests.get is monkeypatched in every test that could
reach one.
"""

from __future__ import annotations

import pytest
import requests

from circuit_oracle import tools

from conftest import make_ctx


SHIM = "http://127.0.0.1:9/x"
PUBLIC = "https://www.neuronpedia.org"


class _Resp:
    """Minimal stand-in for a requests.Response."""

    def __init__(self, payload: dict, status: int = 200):
        self._payload = payload
        self.status_code = status

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.HTTPError(f"status {self.status_code}")

    def json(self) -> dict:
        return self._payload


def _record_get(monkeypatch, payload: dict, *, urls: list):
    """Patch requests.get to record URLs and return `payload`, never a socket."""

    def fake_get(url, **kwargs):
        urls.append((url, kwargs))
        return _Resp(payload)

    monkeypatch.setattr(tools.requests, "get", fake_get)


def _forbid_get(monkeypatch):
    """Patch requests.get to fail the test if anything tries to call out."""

    def fake_get(url, **kwargs):
        raise AssertionError(f"unexpected HTTP call to {url}")

    monkeypatch.setattr(tools.requests, "get", fake_get)


# ---------------------------------------------------------------------------
# URL construction
# ---------------------------------------------------------------------------


def test_fetch_inspect_payload_builds_shim_url(monkeypatch):
    urls: list = []
    _record_get(monkeypatch, {"explanations": [{"description": "shim label"}]}, urls=urls)

    ctx = make_ctx(neuronpedia_base_url=SHIM, feature_source="neuronpedia")
    payload = tools._fetch_inspect_payload(ctx, layer=7, feature_idx=1234)

    assert len(urls) == 1
    url, kwargs = urls[0]
    assert url == f"{SHIM}/api/feature/tiny-toy/7-toy-transcoder/1234"
    assert not url.startswith(PUBLIC)
    # A shim may synthesize a description with an LLM call on a cache miss, which
    # does not finish inside the 15s the public host gets.
    assert kwargs.get("timeout") == 60
    assert payload["label"] == "shim label"


def test_fetch_inspect_payload_default_host_is_public(monkeypatch):
    urls: list = []
    _record_get(monkeypatch, {"explanations": []}, urls=urls)

    ctx = make_ctx()
    tools._fetch_inspect_payload(ctx, layer=3, feature_idx=42)

    url, kwargs = urls[0]
    assert url == f"{PUBLIC}/api/feature/tiny-toy/3-toy-transcoder/42"
    assert kwargs.get("timeout") == 15


def test_trailing_slash_does_not_double_up(monkeypatch):
    urls: list = []
    _record_get(monkeypatch, {"explanations": []}, urls=urls)

    ctx = make_ctx(neuronpedia_base_url="http://127.0.0.1:8765/")
    tools._fetch_inspect_payload(ctx, layer=1, feature_idx=2)
    assert urls[0][0] == "http://127.0.0.1:8765/api/feature/tiny-toy/1-toy-transcoder/2"


def test_inspect_feature_routes_through_the_same_seam(monkeypatch):
    """inspect_feature is the agent-facing entry point, and it must inherit the
    shim host rather than carrying a second URL build of its own."""
    urls: list = []
    _record_get(monkeypatch, {"explanations": [{"description": "shim label"}]}, urls=urls)

    ctx = make_ctx(neuronpedia_base_url=SHIM)
    out = tools.inspect_feature(ctx, layer=7, feature_idx=1234)
    assert urls[0][0].startswith(SHIM)
    assert out["layer"] == 7 and out["feature_idx"] == 1234
    assert out["label"] == "shim label"

    # Second call is served from ctx.inspect_cache, no second HTTP hit. The
    # REASSESS path depends on this cache.
    tools.inspect_feature(ctx, layer=7, feature_idx=1234)
    assert len(urls) == 1


def test_http_error_is_returned_not_raised(monkeypatch):
    def fake_get(url, **kwargs):
        raise requests.ConnectionError("shim is down")

    monkeypatch.setattr(tools.requests, "get", fake_get)
    ctx = make_ctx(neuronpedia_base_url=SHIM)
    out = tools._fetch_inspect_payload(ctx, layer=1, feature_idx=2)
    assert "error" in out
    # A per-call failure must not be cached as if it were a label.
    assert tools.inspect_feature(ctx, layer=1, feature_idx=2)["error"]
    assert ctx.inspect_cache == {}


# ---------------------------------------------------------------------------
# check_feature_backend
# ---------------------------------------------------------------------------


def test_check_feature_backend_raises_when_shim_unreachable(monkeypatch):
    def fake_get(url, **kwargs):
        assert url == f"{SHIM}/healthz"
        raise requests.ConnectionError("connection refused")

    monkeypatch.setattr(tools.requests, "get", fake_get)
    ctx = make_ctx(neuronpedia_base_url=SHIM, feature_source="neuronpedia")
    with pytest.raises(RuntimeError, match="unreachable"):
        tools.check_feature_backend(ctx)


def test_check_feature_backend_raises_on_unhealthy_body(monkeypatch):
    monkeypatch.setattr(
        tools.requests, "get", lambda url, **kw: _Resp({"ok": False, "why": "no cache dir"})
    )
    ctx = make_ctx(neuronpedia_base_url=SHIM)
    with pytest.raises(RuntimeError, match="unhealthy"):
        tools.check_feature_backend(ctx)


def test_check_feature_backend_passes_on_healthy_shim(monkeypatch):
    monkeypatch.setattr(tools.requests, "get", lambda url, **kw: _Resp({"ok": True}))
    ctx = make_ctx(neuronpedia_base_url=SHIM)
    assert tools.check_feature_backend(ctx) is None


def test_check_feature_backend_is_a_noop_on_the_public_default(monkeypatch):
    """Public Neuronpedia has no /healthz. Probing it would 404 and take down
    every refusal and probes run at start, so the check must not fire at all."""
    _forbid_get(monkeypatch)
    ctx = make_ctx()
    assert ctx.neuronpedia_base_url == PUBLIC
    assert tools.check_feature_backend(ctx) is None


def test_check_feature_backend_requires_features_dir_in_local_mode(monkeypatch):
    _forbid_get(monkeypatch)
    ctx = make_ctx(feature_source="local")
    with pytest.raises(RuntimeError, match="autointerp_features_dir"):
        tools.check_feature_backend(ctx)


def test_check_feature_backend_rejects_a_features_dir_without_an_index(monkeypatch, tmp_path):
    _forbid_get(monkeypatch)
    ctx = make_ctx(feature_source="local", autointerp_features_dir=str(tmp_path))
    with pytest.raises(RuntimeError, match="index.json.gz"):
        tools.check_feature_backend(ctx)
