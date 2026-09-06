"""ToolContext accepts the nine grafted base fields plus rank_signed.

Why this matters. Before the merge the causal trunk's ToolContext had none of
these, so both ELK entry scripts died at construction with
`TypeError: unexpected keyword argument`. See merge-specs.md spec D section 1.1
(the nine-field graft set) and spec B section 4.3.
"""

from __future__ import annotations

import dataclasses

import pytest

from circuit_oracle.config import ToolContext

from conftest import FakeTokenizer, make_graph


GRAFTED_FIELDS = [
    "sibling_graphs",
    "candidate_words",
    "base_feature_density",
    "neuronpedia_base_url",
    "feature_source",
    "autointerp_features_dir",
    "autointerp_cache_dir",
    "autointerp_model",
    "autointerp_api_key",
]


def test_all_nine_grafted_fields_are_declared():
    names = {f.name for f in dataclasses.fields(ToolContext)}
    missing = [n for n in GRAFTED_FIELDS if n not in names]
    assert not missing, f"ToolContext is missing grafted fields: {missing}"
    assert "rank_signed" in names


def test_constructs_with_every_grafted_field():
    sibling = make_graph()
    ctx = ToolContext(
        graph=make_graph(),
        tokenizer=FakeTokenizer(),
        sibling_graphs=[sibling],
        candidate_words=["apple", "banana"],
        base_feature_density={(0, 10): 0.002},
        neuronpedia_base_url="http://127.0.0.1:8765",
        feature_source="local",
        autointerp_features_dir="/tmp/features",
        autointerp_cache_dir="/tmp/cache",
        autointerp_model="minimax/minimax-m2.7",
        autointerp_api_key="sk-not-a-real-key",
        rank_signed=False,
    )
    assert ctx.sibling_graphs == [sibling]
    assert ctx.candidate_words == ["apple", "banana"]
    assert ctx.base_feature_density == {(0, 10): 0.002}
    assert ctx.neuronpedia_base_url == "http://127.0.0.1:8765"
    assert ctx.feature_source == "local"
    assert ctx.autointerp_features_dir == "/tmp/features"
    assert ctx.autointerp_cache_dir == "/tmp/cache"
    assert ctx.autointerp_model == "minimax/minimax-m2.7"
    assert ctx.autointerp_api_key == "sk-not-a-real-key"
    assert ctx.rank_signed is False


def test_defaults():
    """feature_source defaults to neuronpedia (a locked decision, not base's "auto").

    Default "auto" would let a causal run silently fall through to the local
    autointerp branch when Neuronpedia returns an empty explanation.
    """
    ctx = ToolContext(graph=make_graph(), tokenizer=FakeTokenizer())
    assert ctx.feature_source == "neuronpedia"
    assert ctx.neuronpedia_base_url == "https://www.neuronpedia.org"
    assert ctx.sibling_graphs == []
    assert ctx.candidate_words == []
    assert ctx.base_feature_density == {}
    assert ctx.autointerp_features_dir is None
    assert ctx.autointerp_cache_dir is None
    assert ctx.autointerp_api_key is None
    # Magnitude ranking is the default in every mode.
    assert ctx.rank_signed is False


def test_mutable_defaults_are_not_shared():
    """The three container fields use default_factory, so two contexts do not
    share one list or dict."""
    a = ToolContext(graph=make_graph(), tokenizer=FakeTokenizer())
    b = ToolContext(graph=make_graph(), tokenizer=FakeTokenizer())
    a.sibling_graphs.append(object())
    a.candidate_words.append("apple")
    a.base_feature_density[(0, 1)] = 0.5
    assert b.sibling_graphs == []
    assert b.candidate_words == []
    assert b.base_feature_density == {}


@pytest.mark.parametrize("source", ["auto", "neuronpedia", "local"])
def test_all_three_feature_sources_accepted(source):
    ctx = ToolContext(
        graph=make_graph(), tokenizer=FakeTokenizer(), feature_source=source
    )
    assert ctx.feature_source == source
