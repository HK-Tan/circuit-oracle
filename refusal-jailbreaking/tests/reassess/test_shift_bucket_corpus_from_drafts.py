"""Shift_bucket against a hand-labeled corpus.

Loads a hand-labeled JSON fixture at tests/fixtures/shift_bucket_corpus.json
holding about 20 records sampled from real run dumps. Each record has the
form:

    {
        "case_id": "exp-7-criticize-xi-row-3",
        "top5_before": {"<token>": {"prob": <float>}, ...},
        "top5_after":  {"<token>": {"prob": <float>}, ...},
        "expected_bucket": "shifted" | "no-shift",
        "notes": "free-text rationale for the label"
    }

The corpus is not shipped, so these tests skip unless the file is there. When
it IS present, every record's shift_bucket(...) output must equal its
expected_bucket label.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from circuit_oracle.tools import shift_bucket  # noqa: F401


CORPUS_PATH = (
    Path(__file__).resolve().parent.parent / "fixtures" / "shift_bucket_corpus.json"
)


@pytest.mark.skipif(
    not CORPUS_PATH.exists(),
    reason=f"no hand-labeled corpus at {CORPUS_PATH}",
)
def test_shift_bucket_matches_hand_labels_for_full_corpus():
    """Every hand-labeled record in the corpus must yield the expected bucket."""
    records = json.loads(CORPUS_PATH.read_text())
    assert isinstance(records, list), (
        f"{CORPUS_PATH} must contain a JSON list of records, got {type(records).__name__}"
    )
    assert len(records) >= 1, f"corpus at {CORPUS_PATH} is empty"

    mismatches: list[str] = []
    for rec in records:
        case_id = rec.get("case_id", "<unknown>")
        top5_before = rec["top5_before"]
        top5_after = rec["top5_after"]
        expected = rec["expected_bucket"]
        actual = shift_bucket(top5_before, top5_after)
        if actual != expected:
            mismatches.append(
                f"  {case_id}: expected {expected!r}, got {actual!r}"
                + (f"  ({rec['notes']})" if rec.get("notes") else "")
            )

    assert not mismatches, (
        f"shift_bucket disagreed with hand-labels on {len(mismatches)}/{len(records)} "
        f"corpus records:\n" + "\n".join(mismatches)
    )


@pytest.mark.skipif(
    not CORPUS_PATH.exists(),
    reason=f"no hand-labeled corpus at {CORPUS_PATH}",
)
def test_corpus_covers_both_buckets():
    """The corpus must include both shifted and no-shift examples (sanity)."""
    records = json.loads(CORPUS_PATH.read_text())
    labels = {rec["expected_bucket"] for rec in records}
    assert "shifted" in labels, "corpus must include at least one 'shifted' example"
    assert "no-shift" in labels, "corpus must include at least one 'no-shift' example"
