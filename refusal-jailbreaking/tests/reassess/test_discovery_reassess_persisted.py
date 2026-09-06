"""Discovery_reassess survives into oracle_result.json.

save_run_results writes result["discovery_reassess"] into oracle_result.json (saving.py:966).
The only pre-existing persistence test uses the minimal save_oracle_result, which does NOT
write this field, so a regression dropping the save line (or the orchestrator return key)
would pass CI silently. B9 is the paper's headline evidence field, so this drives the real
save_run_results path (the heavy SVG / report / elicitation writers stubbed) and asserts the
log round-trips with its null oracle_pinned / became_win fields intact.
"""
from __future__ import annotations

import json
import os

import pytest

import circuit_oracle.saving as saving
from circuit_oracle.config import RunConfig
from circuit_oracle.saving import save_run_results


def test_discovery_reassess_persisted_into_oracle_result_json(monkeypatch, tmp_path):
    # Stub the heavy downstream writers so only the JSON assembly + dump runs.
    monkeypatch.setattr(saving, "write_elicitation_outputs", lambda *a, **k: None)
    monkeypatch.setattr(saving, "build_attribution_data", lambda *a, **k: None)
    monkeypatch.setattr(saving, "_build_report", lambda *a, **k: "")
    monkeypatch.setattr(saving, "_extract_pinned_ids", lambda *a, **k: [])
    # interventions=[] below, so grade_interventions short-circuits before any network call.

    rows = [{
        "feature": [17, 83241, 5],
        "autointerp": "Code/technical snippets",
        "post_label": "illicit-request / sensitivity detector",
        "divergence": "autointerp_only",
        "oracle_pinned": None,
        "became_win": None,
    }]
    result = {
        "response": "ANALYZE narrative",
        "tool_calls": [],
        "usage": {"orchestrator": {"input_tokens": 1, "output_tokens": 1}, "subagents": []},
        "turns": 1,
        "discovery_reassess": rows,
    }
    config = RunConfig(prompt_name="unit-test", system_prompt="sys", user_message="u",
                       experiment_prefix="unit")

    exp_dir = save_run_results(result, config, prompt="P", base_dir=str(tmp_path),
                               full_response="", interventions=[])

    with open(os.path.join(exp_dir, "oracle_result.json")) as f:
        saved = json.load(f)

    assert saved["discovery_reassess"] == rows, (
        "discovery_reassess must round-trip into oracle_result.json (B9 evidence field)"
    )
    # The null pinned/win fields must survive (joined post-hoc by the analysis script).
    assert saved["discovery_reassess"][0]["oracle_pinned"] is None
    assert saved["discovery_reassess"][0]["became_win"] is None


def test_save_run_results_defaults_discovery_reassess_to_empty(monkeypatch, tmp_path):
    """A result dict lacking discovery_reassess (e.g. a pre-Part-B run) serializes [] cleanly,
    not a KeyError - the .get default at saving.py:966."""
    monkeypatch.setattr(saving, "write_elicitation_outputs", lambda *a, **k: None)
    monkeypatch.setattr(saving, "build_attribution_data", lambda *a, **k: None)
    monkeypatch.setattr(saving, "_build_report", lambda *a, **k: "")
    monkeypatch.setattr(saving, "_extract_pinned_ids", lambda *a, **k: [])

    result = {
        "response": "x",
        "tool_calls": [],
        "usage": {"orchestrator": {"input_tokens": 1, "output_tokens": 1}, "subagents": []},
        "turns": 1,
        # no discovery_reassess key
    }
    config = RunConfig(prompt_name="unit-test-2", system_prompt="sys", user_message="u",
                       experiment_prefix="unit")
    exp_dir = save_run_results(result, config, prompt="P", base_dir=str(tmp_path),
                               full_response="", interventions=[])
    with open(os.path.join(exp_dir, "oracle_result.json")) as f:
        saved = json.load(f)
    assert saved["discovery_reassess"] == []


def test_committed_reassess_records_persisted_with_encoded_keys(monkeypatch, tmp_path):
    """The committed ANCHOR reassess_records (tuple-keyed on ctx, returned raw by the
    orchestrator) must round-trip into oracle_result.json under string-encoded keys.

    Guards the save_run_results persistence gap surfaced by the 2026-06-02 chlorine run:
    pre-fix, save_run_results wrote discovery_reassess but DROPPED reassess_records (only the
    unused save_oracle_result wrote it), so the committed pre_label / 3-way divergence data
    survived only inside the verbatim tool_calls copy and never reached the documented
    top-level key. This drives the REAL production save path (save_run_results)."""
    monkeypatch.setattr(saving, "write_elicitation_outputs", lambda *a, **k: None)
    monkeypatch.setattr(saving, "build_attribution_data", lambda *a, **k: None)
    monkeypatch.setattr(saving, "_build_report", lambda *a, **k: "")
    monkeypatch.setattr(saving, "_extract_pinned_ids", lambda *a, **k: [])

    record = {
        "autointerp": "Beginning of a word",
        "pre_label": "QA scaffold",
        "post_label": "Guides a safe refusal for hazardous chemistry queries",
        "divergence": "autointerp_and_pre",
    }
    result = {
        "response": "ANALYZE narrative",
        "tool_calls": [],
        "usage": {"orchestrator": {"input_tokens": 1, "output_tokens": 1}, "subagents": []},
        "turns": 1,
        # tuple keys, exactly as ctx.reassess_records carries them
        "reassess_records": {(19, 93429, 28): record},
    }
    config = RunConfig(prompt_name="unit-test-rr", system_prompt="sys", user_message="u",
                       experiment_prefix="unit")
    exp_dir = save_run_results(result, config, prompt="P", base_dir=str(tmp_path),
                               full_response="", interventions=[])
    with open(os.path.join(exp_dir, "oracle_result.json")) as f:
        saved = json.load(f)

    # tuple key encoded to the canonical comma-joined string (matches _encode_reassess_key),
    # record body intact including the committed-only 3-way divergence value.
    assert saved["reassess_records"] == {"19,93429,28": record}, (
        "committed reassess_records must round-trip into oracle_result.json with string keys"
    )
    assert saved["reassess_records"]["19,93429,28"]["divergence"] == "autointerp_and_pre"
    assert saved["reassess_records"]["19,93429,28"]["pre_label"] == "QA scaffold"


def test_save_run_results_defaults_reassess_records_to_empty(monkeypatch, tmp_path):
    """A result dict lacking reassess_records (a pre-anchor run, or a run where no pinned
    feature shifted) serializes {} cleanly via the .get(...) or {} default, not a KeyError."""
    monkeypatch.setattr(saving, "write_elicitation_outputs", lambda *a, **k: None)
    monkeypatch.setattr(saving, "build_attribution_data", lambda *a, **k: None)
    monkeypatch.setattr(saving, "_build_report", lambda *a, **k: "")
    monkeypatch.setattr(saving, "_extract_pinned_ids", lambda *a, **k: [])

    result = {
        "response": "x",
        "tool_calls": [],
        "usage": {"orchestrator": {"input_tokens": 1, "output_tokens": 1}, "subagents": []},
        "turns": 1,
        # no reassess_records key
    }
    config = RunConfig(prompt_name="unit-test-rr2", system_prompt="sys", user_message="u",
                       experiment_prefix="unit")
    exp_dir = save_run_results(result, config, prompt="P", base_dir=str(tmp_path),
                               full_response="", interventions=[])
    with open(os.path.join(exp_dir, "oracle_result.json")) as f:
        saved = json.load(f)
    assert saved["reassess_records"] == {}
