"""Per-model gateway pinning (circuit_oracle.llm_client).

Runs spend Kilo credits on the main models while gpt-oss-120b keeps going to
OpenRouter, where it is served off Groq. That is a routing decision
about WHICH GATEWAY IS CALLED, and it is easy to confuse with
OPENROUTER_MODEL_ROUTING, which only tells OpenRouter which host to pick once
the request is already going there and is dropped on any other endpoint. These
tests pin the distinction: without the map below, a --provider kilo run would
send its highest-call-count model to Kilo and silently lose Groq.
"""

from __future__ import annotations

import pathlib
import re

import pytest

from circuit_oracle import llm_client as lc


PINNED = "openai/gpt-oss-120b"


@pytest.fixture(autouse=True)
def _keys(monkeypatch):
    """Both gateways credentialed, and no endpoint override in the way."""
    monkeypatch.setenv("OPENROUTER_API_KEY", "or-test")
    monkeypatch.setenv("KILO_API_KEY", "kilo-test")
    monkeypatch.delenv("LLM_BASE_URL", raising=False)
    monkeypatch.delenv("CIRCUIT_ORACLE_MODEL_PINS", raising=False)


def test_gpt_oss_is_pinned_to_openrouter_by_default():
    assert lc.model_pins()[PINNED] == "openrouter"
    assert lc.provider_for(PINNED, "kilo") == "openrouter"


def test_unpinned_models_follow_the_runs_provider():
    # gemma-4-31b-it left this list 2026-07-28: it is now pinned to OpenRouter
    # so it can be ordered onto Cerebras (389 tok/s vs kilo's 22). Arms 1 and 2
    # stay unpinned and follow the run's gateway.
    for model in ("openai/gpt-5.6-terra", "minimax/minimax-m3"):
        assert lc.provider_for(model, "kilo") == "kilo", model
        assert lc.provider_for(model, "openrouter") == "openrouter", model


def test_a_kilo_run_still_calls_openrouter_for_the_pinned_model():
    """The whole point: one run, two gateways, split per model."""
    client = lc.LLMClient(provider="kilo")
    main, main_is_or = client._backend_for("openai/gpt-5.6-terra")
    pinned, pinned_is_or = client._backend_for(PINNED)
    assert "kilo" in str(main.base_url)
    assert not main_is_or
    assert str(pinned.base_url).startswith("https://openrouter.ai/api/v1")
    assert pinned_is_or


def test_the_groq_routing_body_follows_the_destination_not_the_run():
    """is_openrouter travels with the handle, so the OpenRouter-only `provider`
    object is attached exactly when the request really is going to OpenRouter.
    A Kilo endpoint would reject the unknown field."""
    client = lc.LLMClient(provider="kilo")
    assert client._backend_for(PINNED)[1] is True
    assert client._backend_for("minimax/minimax-m3")[1] is False
    routing = lc.openrouter_provider_routing(PINNED)
    assert routing["order"] == ["groq"] and routing["allow_fallbacks"] is True


def test_delegates_are_built_once_per_gateway():
    client = lc.LLMClient(provider="kilo")
    first = client._backend_for(PINNED)[0]
    second = client._backend_for(PINNED)[0]
    assert first is second
    assert list(client._delegates) == ["openrouter"]


def test_an_openrouter_run_needs_no_delegate():
    """Pinning must not build a second client against the same URL."""
    client = lc.LLMClient(provider="openrouter")
    backend, is_openrouter = client._backend_for(PINNED)
    assert backend is client._client
    assert is_openrouter
    assert client._delegates == {}


def test_an_explicit_endpoint_disables_pinning(monkeypatch):
    """base_url / LLM_BASE_URL means the operator pointed this run at one
    specific server (a Modal vLLM). Quietly calling out to OpenRouter behind
    that instruction would be wrong."""
    monkeypatch.setenv("LLM_BASE_URL", "http://127.0.0.1:8000/v1")
    client = lc.LLMClient(provider="openrouter")
    backend, is_openrouter = client._backend_for(PINNED)
    assert backend is client._client
    assert not is_openrouter
    assert client._delegates == {}


def test_env_override_can_repin_or_disable(monkeypatch):
    monkeypatch.setenv("CIRCUIT_ORACLE_MODEL_PINS", "")
    assert lc.model_pins() == {}
    assert lc.provider_for(PINNED, "kilo") == "kilo"
    monkeypatch.setenv("CIRCUIT_ORACLE_MODEL_PINS", f"{PINNED}=kilo")
    assert lc.provider_for(PINNED, "openrouter") == "kilo"


@pytest.mark.parametrize("bad,match", [
    ("openai/gpt-oss-120b", "must be 'model=provider'"),
    ("openai/gpt-oss-120b=nowhere", "unknown provider"),
    ("openai/gpt-oss-120b=anthropic", "unknown provider"),
])
def test_env_override_rejects_nonsense(monkeypatch, bad, match):
    """Including the retired 'anthropic', which no longer resolves anywhere."""
    monkeypatch.setenv("CIRCUIT_ORACLE_MODEL_PINS", bad)
    with pytest.raises(ValueError, match=match):
        lc.model_pins()


def test_preflight_names_the_missing_key_and_who_needs_it(monkeypatch):
    """A kilo run still needs OPENROUTER_API_KEY because of the pin. Say so
    before the GPU work is paid for, not on an opaque 401 mid-batch."""
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    with pytest.raises(RuntimeError) as e:
        lc.preflight_providers(["openai/gpt-5.6-terra", PINNED], "kilo")
    message = str(e.value)
    assert "OPENROUTER_API_KEY" in message
    assert PINNED in message
    # The unpinned model is covered by the Kilo key, so it must not be blamed.
    assert "gpt-5.6-terra" not in message


def test_preflight_passes_when_both_gateways_are_credentialed():
    lc.preflight_providers(["openai/gpt-5.6-terra", PINNED], "kilo")


def test_provider_choices_offers_every_reachable_gateway():
    assert lc.PROVIDER_CHOICES == ["openrouter", "kilo"]
    assert "anthropic" not in lc.PROVIDER_CHOICES


# --- one transport for everything -----------------------------------------------


def _live_python_files():
    """Every .py file that ships or runs, excluding vendored trees.

    circuit_tracer/ is vendored upstream code under its own licence, so it is
    not held to this package's transport rule.
    """
    root = pathlib.Path(__file__).resolve().parents[1]
    skip = {".venv", ".venv-judge", "__pycache__", "circuit_tracer", "node_modules"}
    for path in root.rglob("*.py"):
        if not skip.isdisjoint(path.relative_to(root).parts):
            continue
        yield path.relative_to(root), path.read_text(encoding="utf-8", errors="replace")


def test_no_live_module_imports_the_anthropic_sdk():
    """LLMClient is the only transport, and `anthropic` is not a declared
    dependency (see pyproject). A file importing it crashes on a clean install
    before it can do anything, which is how judge_sae_features.py broke: it drove
    the SDK against OpenRouter's Anthropic-compat endpoint, so it also silently
    opted out of the retry loop, the usage capture, and per-model pinning.

    Anthropic-SHAPED response objects are a different thing and are fine: that is
    llm_client's own adapter layer over the OpenAI protocol.
    """
    offenders = [
        str(rel) for rel, text in _live_python_files()
        if re.search(r"^\s*(from anthropic\b|import anthropic\b)", text, re.M)
    ]
    assert offenders == [], (
        f"these modules import the anthropic SDK: {offenders}. Use "
        "circuit_oracle.llm_client.LLMClient instead."
    )


def _add_argument_calls(text: str):
    """Each `add_argument(...)` argument list, paren-balanced.

    A non-greedy regex stops at the first ')', which for these declarations is
    the one inside os.environ.get("LLM_PROVIDER", "openrouter"), so it would
    report every multi-line flag as missing its choices=.
    """
    for m in re.finditer(r"add_argument\(", text):
        depth, i = 1, m.end()
        while i < len(text) and depth:
            depth += (text[i] == "(") - (text[i] == ")")
            i += 1
        yield text[m.end():i - 1]


def test_every_provider_flag_offers_the_same_gateways():
    """A --provider or --judge-provider that hardcodes its own choices silently
    locks that entry point out of a gateway the rest of the repo can reach.
    build_prompt_set.py is exempt: it keeps a literal copy on purpose (importing
    this package at argparse time pulls torch) and test_prompt_pipeline_stages
    guards that copy against PROVIDER_CHOICES.
    """
    bad = []
    for rel, text in _live_python_files():
        if "tests" in rel.parts or rel.name == "build_prompt_set.py":
            continue
        for decl in _add_argument_calls(text):
            if not re.match(r'\s*"--(?:judge-)?provider"', decl):
                continue
            if "choices=" not in decl:
                bad.append(f"{rel}: no choices=")
            elif "PROVIDER_CHOICES" not in decl:
                bad.append(f"{rel}: choices= is not PROVIDER_CHOICES")
    assert bad == [], bad


def test_preflight_runs_after_the_env_file_is_loaded():
    """Ordering guard, not style. preflight_providers reads OPENROUTER_API_KEY /
    KILO_API_KEY straight off os.environ, so calling it before the entry script
    loads .env reports every key as missing and kills a run that was correctly
    credentialed. Placing the call by eye is exactly how that happened once
    already: two ELK runners load .env well below the arm resolution, not at
    import time like the probes and judge scripts.
    """
    env_markers = ("load_env_file(", "load_dotenv(", "os.environ.setdefault(")
    checked, bad = [], []
    for rel, text in _live_python_files():
        if "tests" in rel.parts:
            continue
        call = text.find("preflight_providers(")
        if call == -1:
            continue
        # Last occurrence: a helper's `def load_env_file(` sits far above the
        # call site that actually populates the environment.
        loads = [text.rfind(m) for m in env_markers]
        if max(loads) == -1:
            continue  # keys come from the shell wrapper, nothing to order against
        checked.append(str(rel))
        if max(loads) > call:
            bad.append(f"{rel}: .env is loaded after preflight_providers()")
    assert bad == [], bad
    assert checked, "guard matched no entry script, the markers must have drifted"


def test_preflight_defers_to_an_explicit_endpoint(monkeypatch):
    """LLM_BASE_URL points the run at a Modal vLLM, where LLMClient disables
    pinning and authenticates with LLM_API_KEY (or "EMPTY"). Demanding a gateway
    key there would block a run that legitimately has neither, and this now
    matters in four entry scripts rather than nowhere."""
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("KILO_API_KEY", raising=False)
    monkeypatch.setenv("LLM_BASE_URL", "http://127.0.0.1:8000/v1")
    lc.preflight_providers(["openai/gpt-5.6-terra", PINNED], "openrouter")


def test_preflight_names_a_retired_provider_rather_than_a_missing_key(monkeypatch):
    """argparse does not validate `default=` against `choices=`, so
    LLM_PROVIDER=anthropic in the environment reaches here past the flag.
    Reporting it as a missing LLM_API_KEY would bury the real cause."""
    monkeypatch.setenv("LLM_PROVIDER", "anthropic")
    with pytest.raises(ValueError, match="retired"):
        lc.preflight_providers(["openai/gpt-5.6-terra"], "anthropic")
