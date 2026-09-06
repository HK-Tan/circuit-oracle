"""GRAPH_STORE resolution in RunConfig.graph_cache_dir.

Precedence is explicit value > GRAPH_STORE env > weights/graphs, matching the
convention build_graph.py established (graphs live in $GRAPH_STORE/graphs).
The env read happens at instantiation, not import, so pod launchers that
export the var after the package is imported still win.
"""

from __future__ import annotations

import os

from circuit_oracle.config import RunConfig


def _cfg(**kwargs) -> RunConfig:
    return RunConfig(prompt_name="x", system_prompt="", user_message="u", **kwargs)


def test_default_without_env(monkeypatch):
    monkeypatch.delenv("GRAPH_STORE", raising=False)
    assert _cfg().graph_cache_dir == "weights/graphs"


def test_env_sets_the_store_root(monkeypatch):
    monkeypatch.setenv("GRAPH_STORE", "/mnt/vol")
    assert _cfg().graph_cache_dir == os.path.join("/mnt/vol", "graphs")


def test_env_is_read_at_instantiation_not_import(monkeypatch):
    monkeypatch.delenv("GRAPH_STORE", raising=False)
    assert _cfg().graph_cache_dir == "weights/graphs"
    monkeypatch.setenv("GRAPH_STORE", "/mnt/late")
    assert _cfg().graph_cache_dir == os.path.join("/mnt/late", "graphs")


def test_explicit_value_beats_env(monkeypatch):
    monkeypatch.setenv("GRAPH_STORE", "/mnt/vol")
    assert _cfg(graph_cache_dir="elsewhere").graph_cache_dir == "elsewhere"
