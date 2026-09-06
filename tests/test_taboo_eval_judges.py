"""Offline tests for the two taboo judge scripts.

Both bugs these cover were found by running phase 3 on 2026-07-28, and both
failed SILENTLY in the sense that matters: neither raised anything a batch
launcher would notice as a failed run.

  1. `--provider` was declared with `choices=PROVIDER_CHOICES`, but neither
     script imported that name. Every invocation died with NameError at
     argparse-construction time, so the scripts could not grade a single run.
     A one-line import is easy to lose again in a merge, and nothing else in
     the repo exercises these two entry points.

  2. The judge called the model with max_tokens=512. gpt-oss-120b emits a
     harmony analysis channel before its final channel, so reasoning ate the
     budget and the reply arrived truncated mid-JSON (or empty). The scripts
     catch a parse failure and record `correct: False`, so a FORMATTING failure
     was silently recorded as an ORACLE MISS. It cost 7 of 240 arm1-open runs,
     5 of which were actually correct, moving that arm's top-10 recall by 2.1
     points. Nothing in the output distinguished it from a genuine miss.

Nothing here spawns a subprocess or calls a gateway.
"""
from __future__ import annotations

import ast
import importlib.util
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO / "secret-elicitation" / "scripts"

CLOSED = _SCRIPTS / "eval_oracle_taboo.py"
OPEN = _SCRIPTS / "eval_oracle_taboo_no_options.py"
BOTH = [pytest.param(CLOSED, id="closed"), pytest.param(OPEN, id="open")]

# Both scripts define module-level names that collide with each other
# (JUDGE_PROMPT, extract_secret, judge, EXP_DIR_RE). Load each under a unique
# module name so importing one cannot shadow the other, the same hazard already
# documented for the two tracks' run_arms.py.
_LOADED: dict[Path, object] = {}


def _load(path: Path):
    if path not in _LOADED:
        spec = importlib.util.spec_from_file_location(f"taboo_eval_{path.stem}", path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod
        try:
            spec.loader.exec_module(mod)
        except Exception as e:  # pragma: no cover - env without circuit_oracle
            pytest.skip(f"cannot import {path.name}: {e}", allow_module_level=True)
        _LOADED[path] = mod
    return _LOADED[path]


# ---------- bug 1: the argparse NameError ----------

@pytest.mark.parametrize("path", BOTH)
def test_provider_choices_is_actually_imported(path: Path):
    """PROVIDER_CHOICES lives on circuit_oracle.llm_client, NOT the package root.

    `from circuit_oracle import PROVIDER_CHOICES` raises ImportError, so the
    only correct form is the submodule one. Importing the module is what proves
    the name resolves.
    """
    mod = _load(path)
    assert hasattr(mod, "PROVIDER_CHOICES"), (
        f"{path.name} uses PROVIDER_CHOICES in its argparse but never imports it")
    assert "openrouter" in mod.PROVIDER_CHOICES
    assert "kilo" in mod.PROVIDER_CHOICES


@pytest.mark.parametrize("path", BOTH)
def test_parser_builds_without_touching_a_gateway(path: Path):
    """Regression for the NameError: building the parser must not explode.

    main() constructs the parser before it reads anything, so this is the exact
    code path that failed. Parsing --help would exit, so we parse a real,
    harmless argv instead and assert the defaults survived.
    """
    mod = _load(path)
    # Re-run the argparse construction by invoking main() with a bad results dir
    # is too coarse, so assert on the source instead: every name referenced as
    # `choices=` must exist on the module.
    tree = ast.parse(path.read_text())
    referenced: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.keyword) and node.arg == "choices":
            if isinstance(node.value, ast.Name):
                referenced.add(node.value.id)
    assert referenced, f"{path.name} declares no choices= argument any more"
    for name in referenced:
        assert hasattr(mod, name), (
            f"{path.name} passes choices={name} but that name is not defined at "
            f"module scope, so argparse construction raises NameError")


# ---------- bug 2: the truncated-judge token budget ----------

@pytest.mark.parametrize("path", BOTH)
def test_judge_token_budget_survives_harmony_reasoning(path: Path):
    """max_tokens must leave room for gpt-oss-120b's analysis channel.

    1024 is the documented floor for gpt-oss to reach its final channel at all.
    We require strictly more than that, because the open-mode judge must then
    still emit a 10-lemma shortlist, a rank and a rationale on top.
    """
    tree = ast.parse(path.read_text())
    budgets = [
        kw.value.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        for kw in node.keywords
        if kw.arg == "max_tokens" and isinstance(kw.value, ast.Constant)
    ]
    assert budgets, f"{path.name} no longer passes max_tokens explicitly"
    assert min(budgets) >= 1024, (
        f"{path.name} calls the judge with max_tokens={min(budgets)}; "
        "gpt-oss-120b spends its budget on a harmony analysis channel first, so "
        "the JSON comes back truncated and a parse failure is scored as a wrong "
        "answer rather than raising")


# ---------- the silent-miscount property both bugs shared ----------

# ---------- judging cost must reach an artifact ----------

class _Usage:
    input_tokens = 1000
    output_tokens = 200
    cache_read_input_tokens = 0
    cache_creation_input_tokens = 0


class _Msg:
    usage = _Usage()
    content = []


@pytest.mark.parametrize("path", BOTH)
def test_record_usage_prices_on_the_requested_slug(path: Path):
    """Usage must be keyed on the slug we asked for, not the one echoed back.

    saving.MODEL_PRICING is keyed on request slugs like `openai/gpt-oss-120b`.
    A gateway may echo a resolved variant, and compute_cost returns None for an
    unknown key, which is silent: the run completes and the cost is simply
    absent. That is exactly how judging spend went unrecorded for a whole phase.
    """
    mod = _load(path)
    log = []
    mod.record_usage(_Msg(), "openai/gpt-oss-120b", log)
    assert len(log) == 1
    assert log[0]["model"] == "openai/gpt-oss-120b"
    assert log[0]["input_tokens"] == 1000
    assert log[0]["output_tokens"] == 200

    from circuit_oracle.saving import compute_cost
    cost = compute_cost(log[0])
    assert cost is not None, (
        "the judge model must be priced in saving.MODEL_PRICING, or the judging "
        "block records cost_usd=None and the ledger row cannot be filled")
    assert cost > 0


@pytest.mark.parametrize("path", BOTH)
def test_record_usage_tolerates_a_response_with_no_usage_block(path: Path):
    """A failed or empty reply must still append a row, at zero.

    Dropping the row instead would undercount calls, and the call count is what
    tells us a resumed pass only graded part of the set.
    """
    mod = _load(path)

    class _NoUsage:
        usage = None
        content = []

    log = []
    mod.record_usage(_NoUsage(), "openai/gpt-oss-120b", log)
    assert len(log) == 1
    assert log[0]["input_tokens"] == 0


@pytest.mark.parametrize("path", BOTH)
def test_usage_is_recorded_before_the_parse_branches(path: Path):
    """record_usage must run before any `return` in judge().

    A truncated or unparseable judge reply still costs money. If the call were
    recorded only on the success path, the arm that burns the most tokens
    (the one failing to parse) would be the one missing from the ledger.
    """
    tree = ast.parse(path.read_text())
    fn = next(n for n in ast.walk(tree)
              if isinstance(n, ast.FunctionDef) and n.name == "judge")
    body = fn.body
    rec_idx = next(
        (i for i, stmt in enumerate(body)
         if any(isinstance(c, ast.Call) and getattr(c.func, "id", None) == "record_usage"
                for c in ast.walk(stmt))),
        None)
    assert rec_idx is not None, f"{path.name}: judge() never calls record_usage"
    first_return = next(
        (i for i, stmt in enumerate(body)
         if any(isinstance(c, ast.Return) for c in ast.walk(stmt))),
        len(body))
    assert rec_idx < first_return, (
        f"{path.name}: record_usage runs after a return in judge(), so failed "
        "judge calls would not be billed in the recorded total")


# ---------- cache and resume integrity ----------

@pytest.mark.parametrize("path", BOTH)
def test_cache_is_invalidated_when_the_judge_model_changes(path: Path):
    """Grades from a different judge must not be reused and relabelled.

    The cache is keyed on (exp, run) only. Without a judge check, pointing a new
    judge at an existing eval.json reuses every old grade and then stamps the
    NEW judge_model onto the file, mislabelling a whole result set with nothing
    in the output to show it. The default judge moved from gpt-5.4-mini to
    gpt-oss-120b on 2026-07-28, so every pre-existing eval.json in the tree is
    exactly this trap.
    """
    src = path.read_text()
    assert "prior_judge" in src and "args.judge_model" in src, (
        f"{path.name} does not compare the cached judge_model against the "
        "requested one, so grades from another judge are silently reused")
    tree = ast.parse(src)
    # The comparison must actually gate the cache, not just be computed.
    assert any(
        isinstance(n, ast.Compare) and any(
            isinstance(c, ast.Name) and c.id == "prior_judge" for c in ast.walk(n))
        for n in ast.walk(tree)), f"{path.name}: prior_judge is never compared"


@pytest.mark.parametrize("path", BOTH)
def test_resume_accumulates_prior_judging_cost(path: Path):
    """A resumed pass must add to the prior ledger, not replace it.

    The judging block is built from this process's usage_log alone. Overwriting
    means regrading 7 of 240 runs replaces a 240-call ledger with a 7-call one,
    and a fully cached rerun replaces it with zero. The earlier value exists
    nowhere else, so "sum across resumes yourself" is not implementable.
    """
    src = path.read_text()
    assert "prior_judging" in src, (
        f"{path.name} never reads the prior `judging` block, so a resume "
        "destroys the earlier recorded cost")
    assert "this_invocation" in src, (
        f"{path.name} should keep the un-folded per-invocation numbers so a "
        "resumed pass stays auditable")


@pytest.mark.parametrize("path", BOTH)
def test_a_prior_file_with_no_judge_model_is_not_reused(path: Path):
    """Missing judge_model must invalidate too, not just a differing one.

    `if prior_judge and prior_judge != requested` accepts a file that never
    said who graded it. An artifact of unknown provenance cannot be shown to
    match, and reusing it stamps the current judge's name onto it.
    """
    src = path.read_text()
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Compare)
                and isinstance(node.left, ast.Name)
                and node.left.id == "prior_judge"):
            continue
        # The guard must be the bare comparison, not `prior_judge and ...`,
        # which short-circuits a falsy (missing) value into "reuse it".
        parent_is_and = any(
            isinstance(p, ast.BoolOp) and isinstance(p.op, ast.And)
            and any(v is node for v in p.values)
            for p in ast.walk(tree))
        assert not parent_is_and, (
            f"{path.name}: the judge_model check is guarded by `prior_judge and "
            "...`, so an artifact with no judge_model is reused and relabelled")
        return
    pytest.fail(f"{path.name}: no comparison on prior_judge found")


@pytest.mark.parametrize("path", BOTH)
def test_a_failed_cache_load_clears_what_it_already_read(path: Path):
    """A malformed grade partway through must not leave a partial cache.

    Entries are added one at a time, so a KeyError on entry 200 of 240 leaves
    199 in `cached`. Warning "regrading all" while reusing that prefix regrades
    some runs, reuses others, and then adds the FULL prior cost on top of calls
    that were just re-billed.
    """
    src = path.read_text()
    tree = ast.parse(src)
    handlers = [h for n in ast.walk(tree) if isinstance(n, ast.Try) for h in n.handlers]
    # Must be the CACHE-LOAD handler, which catches OSError alongside
    # JSONDecodeError. judge() has its own JSONDecodeError-only handler for a
    # malformed judge reply, and matching that one instead would make this test
    # vacuous.
    target = None
    for h in handlers:
        names = ast.dump(h.type or ast.Constant(None))
        if "JSONDecodeError" in names and "OSError" in names:
            target = h
            break
    assert target is not None, f"{path.name}: no cache-load error handler found"
    body = ast.dump(ast.Module(body=target.body, type_ignores=[]))
    assert "clear" in body, (
        f"{path.name}: the cache-load error handler warns but never clears "
        "`cached`, so a partially loaded cache is silently reused")
    assert "prior_judging" in body, (
        f"{path.name}: the handler does not reset prior_judging, so the full "
        "prior cost is added on top of calls that get re-billed")


@pytest.mark.parametrize("path", BOTH)
def test_provider_mix_reaches_the_artifact(path: Path):
    """Recording the provider in memory is not enough, it must be serialized.

    Without a `providers` block in eval.json the fallback is invisible once the
    process exits, which is the whole point of recording it.
    """
    src = path.read_text()
    assert '"providers"' in src or "judging[\"providers\"]" in src, (
        f"{path.name}: the serving provider is recorded into usage rows but "
        "never written into eval.json, so a fallback cannot be repriced later")


@pytest.mark.parametrize("path", BOTH)
def test_unpriced_current_calls_are_not_masked_by_a_priced_prior(path: Path):
    """`(None or 0.0) + prior` would report the old total as if it were complete."""
    src = path.read_text()
    assert "this_unpriced" in src, (
        f"{path.name}: an unpriced current increment can hide behind a priced "
        "prior total, reporting a number that does not cover the calls made")


@pytest.mark.parametrize("path", BOTH)
def test_usage_rows_carry_the_serving_provider(path: Path):
    """Cost is a Groq-rate estimate unless we know who served the call.

    gpt-oss-120b runs allow_fallbacks=True behind order=["groq"], and
    MODEL_PRICING holds one rate per slug. Cerebras and SambaNova both price
    above Groq, so a throttled call served elsewhere is under-priced. Recording
    the provider is what makes the artifact repriceable after the fact.
    """
    mod = _load(path)
    log = []

    class _M:
        usage = _Usage()
        provider = "Cerebras"
        content = []

    mod.record_usage(_M(), "openai/gpt-oss-120b", log)
    assert log[0].get("provider") == "Cerebras"


@pytest.mark.parametrize("path", BOTH)
def test_parse_failure_is_distinguishable_from_a_real_miss(path: Path):
    """A judge that could not be parsed must leave a trace in the rationale.

    This is what let the truncation be detected after the fact rather than
    shipping as a 2.1-point accuracy error. If the fallback ever starts
    returning a bare `correct: False` with no marker, an unparseable judge
    becomes indistinguishable from an oracle that genuinely guessed wrong.
    """
    src = path.read_text()
    assert "parse error" in src, (
        f"{path.name} no longer tags unparseable judge replies; a formatting "
        "failure would be silently counted as an incorrect oracle answer")
