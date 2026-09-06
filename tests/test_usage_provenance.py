"""Serving provenance survives the bookkeeping, and a missing model name does not.

`providers` is a host -> call-count histogram written next to the token counts.
It exists so "all N runs of this arm landed on one OpenRouter host" is checkable
after the fact, which only works if the field survives every transformation a
usage record goes through on its way into oracle_result.json.
"""

from __future__ import annotations

import pytest

from circuit_oracle.llm_client import shorten_model_name
from circuit_oracle.saving import amortized_usage


def test_amortization_zeroes_tokens_but_keeps_the_serving_hosts():
    """A non-owner copy is charged zero tokens. It was still served by someone,
    and dropping the histogram there would read as 'no provider recorded'."""
    owner = {
        "model": "openai/gpt-5.4",
        "input_tokens": 1000,
        "output_tokens": 200,
        "providers": {"Fireworks": 3, "Together": 1},
    }
    amortized = amortized_usage(owner)
    assert amortized["input_tokens"] == 0
    assert amortized["output_tokens"] == 0
    assert amortized["providers"] == {"Fireworks": 3, "Together": 1}
    # A copy, not the same object: mutating one record must not edit the other.
    amortized["providers"]["Fireworks"] = 99
    assert owner["providers"]["Fireworks"] == 3


def test_amortization_of_a_record_without_provenance_is_empty_not_missing():
    amortized = amortized_usage({"model": "openai/gpt-5.4"})
    assert amortized["providers"] == {}


@pytest.mark.parametrize("bad", [None, "", 0])
def test_shorten_model_name_refuses_a_missing_name(bad):
    """ELK arms declare subagent_model=None to mean "runs no subagents". Passing
    that through would have built an `exp/..._None_...` directory via a TypeError
    on `"/" in None`; it has to say what to do instead."""
    with pytest.raises(ValueError, match="subagent_model=None"):
        shorten_model_name(bad)


def test_shorten_model_name_still_shortens():
    assert shorten_model_name("anthropic/claude-sonnet-4-6") == "sonnet-4-6"
    assert shorten_model_name("openai/gpt-oss-120b") == "gpt-oss-120b"
