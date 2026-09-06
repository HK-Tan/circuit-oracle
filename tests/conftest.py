"""Shared fixtures for the merged-package smoke suite.

Scope. This tree covers only what the package merge grafted (the nine new
ToolContext fields, the three ELK tools, the shim routing seam, the mode gate,
the ranking-parity switch, and the OpenAI-protocol LLMClient). The full causal
behavior suite still lives in `refusal-jailbreaking/tests/` and is not
duplicated here.

Everything is API-free. No network, no GPU, no model weights, no HF downloads.
The graphs are hand-built dataclasses duck-typed to `circuit_tracer.graph.Graph`
for exactly the attributes the tools read, following the same pattern as
`refusal-jailbreaking/tests/fixtures/tiny_model.py:TinyGraph` but without the toy
transformer (nothing here needs a forward pass).
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest
import torch


# Make the merged package importable without an editable install, mirroring
# refusal-jailbreaking/tests/conftest.py. Inserted at position 0, so it wins
# over PYTHONPATH and has to be correct.
_PACKAGE_ROOT = Path(__file__).resolve().parents[1] / "src"
if not (_PACKAGE_ROOT / "circuit_oracle").is_dir():
    raise RuntimeError(
        f"merged package not found at {_PACKAGE_ROOT / 'circuit_oracle'}. "
        "Run pytest from the repository root or install with "
        "`uv pip install -e .` from the repository root."
    )
if str(_PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(_PACKAGE_ROOT))


# ---------------------------------------------------------------------------
# Synthetic graph
# ---------------------------------------------------------------------------

# Node layout of the adjacency matrix, same as the real Graph and as TinyGraph.
#   [ features | error nodes (n_layers * n_pos) | embedding nodes (n_pos) | logit nodes ]


@dataclass
class SyntheticCfg:
    n_layers: int
    device: str = "cpu"


@dataclass
class SyntheticGraph:
    """Duck type for the Graph attributes the tools under test actually read."""

    input_tokens: torch.Tensor
    active_features: torch.Tensor      # [n_active, 3] rows of (layer, pos, feature_idx)
    activation_values: torch.Tensor    # [n_active]
    selected_features: torch.Tensor    # indices into active_features
    adjacency_matrix: torch.Tensor     # [n_nodes, n_nodes]
    logit_tokens: torch.Tensor
    logit_probabilities: torch.Tensor
    cfg: SyntheticCfg
    input_string: str = "synthetic"
    scan: str | None = "synthetic-fixture"
    n_pos: int = 0

    def __post_init__(self):
        self.n_pos = int(self.input_tokens.shape[0])


class FakeTokenizer:
    """Decodes an id to a fixed word. Enough for get_top_features / embeddings."""

    VOCAB = ["<bos>", "how", "do", "i", "?", "Sorry", "Sure", "apple", "banana"]

    def decode(self, ids, skip_special_tokens: bool = False) -> str:
        if isinstance(ids, int):
            ids = [ids]
        if isinstance(ids, torch.Tensor):
            ids = ids.tolist()
            if isinstance(ids, int):
                ids = [ids]
        return "".join(self.VOCAB[int(i) % len(self.VOCAB)] for i in ids)


# Four features. Row 0 is the upstream-tracing target, row 2 is the strongly
# inhibitory one the ranking-parity tests key on.
ACTIVE_FEATURES = [
    (1, 2, 100),
    (0, 0, 10),
    (0, 1, 20),
    (1, 1, 30),
]
ACTIVATIONS = [4.0, 5.0, 3.0, 2.0]
N_LAYERS = 2
N_POS = 3
N_LOGITS = 2


def make_graph(
    *,
    adjacency: torch.Tensor | None = None,
    active_features=ACTIVE_FEATURES,
    activations=ACTIVATIONS,
    n_layers: int = N_LAYERS,
    n_pos: int = N_POS,
    n_logits: int = N_LOGITS,
) -> SyntheticGraph:
    """Assemble a SyntheticGraph, defaulting to a dense deterministic adjacency."""
    n_features = len(active_features)
    n_nodes = n_features + n_layers * n_pos + n_pos + n_logits
    if adjacency is None:
        # Deterministic, dense, mixed sign, zero diagonal. Values are small and
        # irregular so no propagation result is accidentally degenerate.
        gen = torch.Generator().manual_seed(11)
        adjacency = torch.empty(n_nodes, n_nodes).uniform_(-1.0, 1.0, generator=gen)
        adjacency.fill_diagonal_(0.0)
    return SyntheticGraph(
        input_tokens=torch.arange(n_pos, dtype=torch.long),
        active_features=torch.tensor(active_features, dtype=torch.long),
        activation_values=torch.tensor(activations, dtype=torch.float32),
        selected_features=torch.arange(n_features, dtype=torch.long),
        adjacency_matrix=adjacency,
        logit_tokens=torch.tensor([5, 6][:n_logits], dtype=torch.long),
        logit_probabilities=torch.tensor([0.7, 0.2][:n_logits], dtype=torch.float32),
        cfg=SyntheticCfg(n_layers=n_layers),
    )


def make_ctx(graph: SyntheticGraph | None = None, **kwargs) -> Any:
    """A real ToolContext (not a stub) wrapping a synthetic graph."""
    from circuit_oracle.config import ToolContext

    return ToolContext(
        graph=graph if graph is not None else make_graph(),
        tokenizer=FakeTokenizer(),
        neuronpedia_model_id="tiny-toy",
        neuronpedia_sae_id="{layer}-toy-transcoder",
        **kwargs,
    )


@pytest.fixture()
def graph() -> SyntheticGraph:
    return make_graph()


@pytest.fixture()
def ctx(graph) -> Any:
    return make_ctx(graph)


# ---------------------------------------------------------------------------
# Fake FeatureCache (stands in for the on-disk transcoder features/ directory)
# ---------------------------------------------------------------------------


class FakeFeatureCache:
    """Same surface as `autointerp.FeatureCache`, backed by a dict.

    `records` is keyed by (layer, feature_idx). A missing key raises KeyError,
    which is what the real cache does and what `_diff_top_at_pos` catches.
    """

    def __init__(self, records: dict[tuple[int, int], dict]):
        self.records = dict(records)
        self.features_dir = "<fake>"

    def get(self, layer: int, feature_idx: int) -> dict:
        key = (int(layer), int(feature_idx))
        if key not in self.records:
            raise KeyError(f"feature {key} not in fake cache")
        return self.records[key]


FAKE_FEATURES_DIR = "/nonexistent/fake-features-dir"


@pytest.fixture()
def fake_feature_cache(monkeypatch):
    """Install a FakeFeatureCache under FAKE_FEATURES_DIR and hand it back.

    `elk_tools._get_feature_cache` memoizes per directory, so seeding the module
    dict is enough to keep the real FeatureCache (and its index.json.gz read) out
    of the test path entirely.
    """
    from circuit_oracle import elk_tools

    records = {
        # (layer, feature_idx) -> record. Frequencies must be strictly inside
        # (0, 1), the tools drop anything outside.
        (0, 10): {"activation_frequency": 0.001, "top_logits": ["apple", "apples", "fruit"]},
        (0, 20): {"activation_frequency": 0.01, "top_logits": ["banana", "yellow"]},
        (1, 30): {"activation_frequency": 0.02, "top_logits": ["apple", "orchard"]},
        (1, 100): {"activation_frequency": 0.05, "top_logits": ["the", "a"]},
    }
    cache = FakeFeatureCache(records)
    patched = dict(elk_tools._feature_caches)
    patched[FAKE_FEATURES_DIR] = cache
    monkeypatch.setattr(elk_tools, "_feature_caches", patched)
    return cache
