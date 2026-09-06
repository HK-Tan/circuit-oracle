"""Task 2 - the builder must build the secrets the runner is going to run.

The bug this pins: `build_taboo_graphs.py --words` defaulted to `None`, which
meant all 20 trained secrets, while every runner and the plotter defaulted to
the reported 8. A default build was therefore 20 x 6 = 120 graphs where the
current config needs 8 x 6 = 48, silently, on a GPU pod, for hours.

The two lists had been copied into five scripts. Divergence between copies is
the actual failure mode, so the lists now live in `taboo_words.py` and the
strongest test here is that the builder's default set and the runner's default
set are the same object's contents rather than two lists that happen to agree
today.

Offline. No model, no GPU, no network. `build_taboo_graphs` imports torch and
peft, so it is imported lazily inside the tests that need it and skipped when
the GPU stack is absent.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "secret-elicitation" / "scripts"))

import taboo_words  # noqa: E402  (path set above)

# The reported configuration, asserted so a list edit that changes the headline
# denominator cannot pass silently.
REPORTED_SECRETS = 8
ALL_SECRETS = 20
PROMPTS_PER_SECRET = 6


def test_the_reported_eight_are_the_published_eight() -> None:
    """These 8 label the x axis of figures/elk_closed_results.pdf."""
    assert taboo_words.REPORTED_WORDS == [
        "smile", "leaf", "gold", "blue", "book", "salt", "chair", "clock",
    ]


def test_the_candidate_menu_is_twenty() -> None:
    """The closed-mode task is 1-of-20. Changing this changes chance level."""
    assert len(taboo_words.CANDIDATE_WORDS) == ALL_SECRETS
    assert len(set(taboo_words.CANDIDATE_WORDS)) == ALL_SECRETS


def test_the_reported_eight_are_a_prefix_of_the_menu() -> None:
    """REPORTED_WORDS is derived as a slice, so this guards the ordering it
    depends on rather than restating the slice."""
    assert taboo_words.CANDIDATE_WORDS[:REPORTED_SECRETS] == taboo_words.REPORTED_WORDS


def test_presets_cover_both_configurations() -> None:
    assert taboo_words.WORD_SETS["reported8"] == taboo_words.REPORTED_WORDS
    assert taboo_words.WORD_SETS["all20"] == taboo_words.CANDIDATE_WORDS


def test_every_script_shares_one_list() -> None:
    """The five scripts must not re-declare these lists.

    A second literal is how the builder and the runners drifted apart in the
    first place, so a new copy anywhere should fail here.
    """
    scripts = REPO / "secret-elicitation" / "scripts"
    offenders = []
    for path in sorted(scripts.glob("*.py")):
        if path.name == "taboo_words.py":
            continue
        text = path.read_text()
        # A literal list of secrets always starts with the first two in order.
        if '"smile", "leaf"' in text or "'smile', 'leaf'" in text:
            offenders.append(path.name)
    assert not offenders, f"word list re-declared in {offenders}, import taboo_words instead"


def _builder():
    return pytest.importorskip(
        "build_taboo_graphs",
        reason="build_taboo_graphs imports torch + peft (GPU stack)",
    )


def test_builder_defaults_to_the_reported_eight() -> None:
    """The whole point. Default used to be all 20."""
    builder = _builder()
    assert builder.parse_args.__defaults__ is None  # takes no args
    parser_default = _words_default(builder)
    assert parser_default == "reported8"
    assert builder.resolve_words(parser_default) == taboo_words.REPORTED_WORDS


def _words_default(builder) -> str:
    """Pull --words' default off the real parser, not off a re-declaration."""
    import argparse
    import contextlib
    import io

    # parse_args() builds and consumes the parser in one call, so run it with an
    # empty argv and read the resolved value back.
    with contextlib.redirect_stderr(io.StringIO()):
        old = sys.argv
        sys.argv = ["build_taboo_graphs.py"]
        try:
            args = builder.parse_args()
        finally:
            sys.argv = old
    assert isinstance(args, argparse.Namespace)
    return args.words


def test_default_build_is_48_graphs_not_120() -> None:
    builder = _builder()
    words = builder.resolve_words(_words_default(builder))
    assert len(words) * len(builder.PROMPT_PAIRS) == REPORTED_SECRETS * PROMPTS_PER_SECRET


def test_all20_is_still_reachable() -> None:
    builder = _builder()
    assert builder.resolve_words("all20") == taboo_words.CANDIDATE_WORDS


def test_a_comma_separated_subset_still_works() -> None:
    builder = _builder()
    assert builder.resolve_words("gold,clock") == ["gold", "clock"]
    assert builder.resolve_words(" gold , clock ") == ["gold", "clock"]


def test_an_unknown_secret_is_fatal() -> None:
    """Filtering a typo out would quietly shrink the build instead."""
    builder = _builder()
    with pytest.raises(SystemExit):
        builder.resolve_words("gold,silver")
    with pytest.raises(SystemExit):
        builder.resolve_words(",,,")


def test_builder_and_runner_agree_on_the_default_set() -> None:
    """The end-to-end invariant: build what the runner will look for.

    Both sides read the same module, so this cannot silently diverge again.
    """
    builder = _builder()
    runner = pytest.importorskip(
        "run_oracle_on_taboo",
        reason="run_oracle_on_taboo imports the circuit_oracle GPU stack",
    )
    assert builder.resolve_words(_words_default(builder)) == runner.WORD_SETS["reported8"]
    assert builder.WORDS == runner.CANDIDATE_WORDS
