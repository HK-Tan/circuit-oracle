"""GRAPH_STORE resolution in run_sweeps.py, the graph read path.

build_graph.py honors $GRAPH_STORE/graphs. run_sweeps.py used to hardcode
weights/graphs, so a pod that built onto a mounted volume and then swept from
the repo directory silently read a different, empty store. default_graph_dir()
closes that, with --graph-dir still winning over the env var.
"""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_run_sweeps():
    import sys

    scripts_dir = str(_REPO_ROOT / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    spec = importlib.util.spec_from_file_location(
        "run_sweeps", str(_REPO_ROOT / "scripts" / "run_sweeps.py")
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_default_without_env(monkeypatch):
    monkeypatch.delenv("GRAPH_STORE", raising=False)
    rs = _load_run_sweeps()
    assert rs.default_graph_dir() == "weights/graphs"


def test_env_sets_the_store_root(monkeypatch):
    monkeypatch.setenv("GRAPH_STORE", "/mnt/vol")
    rs = _load_run_sweeps()
    assert rs.default_graph_dir() == os.path.join("/mnt/vol", "graphs")


def test_parser_default_follows_env_and_flag_wins(monkeypatch):
    monkeypatch.setenv("GRAPH_STORE", "/mnt/vol")
    rs = _load_run_sweeps()
    args = rs.build_parser().parse_args(["--slug", "x"])
    assert args.graph_dir == os.path.join("/mnt/vol", "graphs")
    args = rs.build_parser().parse_args(["--slug", "x", "--graph-dir", "elsewhere"])
    assert args.graph_dir == "elsewhere"


def test_graph_path_for_composes_the_env_store(monkeypatch):
    monkeypatch.setenv("GRAPH_STORE", "/mnt/vol")
    rs = _load_run_sweeps()
    args = rs.build_parser().parse_args(["--slug", "tiananmen-massacre"])
    assert rs.graph_path_for(args, "tiananmen-massacre") == os.path.join(
        "/mnt/vol", "graphs", "tiananmen-massacre_graph.pt"
    )
