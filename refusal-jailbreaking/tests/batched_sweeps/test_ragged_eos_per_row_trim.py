"""per-row EOS trimming after a ragged batched decode.

Asserts that when batched decode runs to `answer_max_tokens` (no early EOS break) and
different rows hit natural EOS at different positions, each row's post-EOS tokens are
trimmed in post-processing so that `answer_after` matches the single-call decode.

Comparing batched(B>=2)[i] vs batched(B=1) isolates ragged-batch trim logic without
relying on a hypothetical single-call decode helper (no such function is named in).
"""
from __future__ import annotations

import pytest


def test_ragged_eos_per_row_trim(tiny_model, baseline_ctx):
    # Test-pattern rule: feature_intervention* are bound methods on
    # ReplacementModel, not module-level functions.
    # Construct interventions that cause rows to hit EOS at different points on the toy.
    intervention_lists = [
        [{"layer": 1, "feature_idx": 3, "pos": 5, "value": -1.0}],
        [{"layer": 1, "feature_idx": 5, "pos": 4, "value": -2.0}],
        [{"layer": 0, "feature_idx": 1, "pos": 2, "value": -3.0}],
    ]

    batched = tiny_model.replacement_model.feature_intervention_batched(
        inputs="hello",
        intervention_lists=intervention_lists,
        answer_max_tokens=8,
    )

    for row_idx, single_list in enumerate(intervention_lists):
        single = tiny_model.replacement_model.feature_intervention_batched(
            inputs="hello",
            intervention_lists=[single_list],
            answer_max_tokens=8,
        )
        # `answer_after` per row is the post-EOS-trimmed decoded string.
        assert batched.answer_after[row_idx] == single.answer_after[0]
