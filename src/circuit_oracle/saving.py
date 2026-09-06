"""Save run results: JSON, SVG, and markdown report."""

import concurrent.futures
import json
import os
import re
import statistics
from datetime import datetime, timezone
from pathlib import Path


def _encode_reassess_key(key) -> str:
    """Stringify a (layer, feature_idx, pos) tuple key for JSON storage."""
    if isinstance(key, tuple):
        return ",".join(str(int(k)) for k in key)
    return str(key)


def save_oracle_result(*, ctx, output_dir) -> Path:
    """Persist run-state from a ToolContext into oracle_result.json.

    Writes the REASSESS triple-label records (and any other persistable ctx
    fields the harness has populated) keyed by stringified
    (layer, feature_idx, pos) tuples. Returns the path to oracle_result.json.

    This is the minimal save surface. The full Phase-2 save_run_results
    routine handles the orchestrator transcript + circuit.svg etc.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    reassess = getattr(ctx, "reassess_records", {}) or {}
    pinned = getattr(ctx, "pinned_features", {}) or {}
    inspect_cache = getattr(ctx, "inspect_cache", {}) or {}

    payload = {
        "reassess_records": {
            _encode_reassess_key(k): v for k, v in reassess.items()
        },
        "pinned_features": {
            _encode_reassess_key(k): v for k, v in pinned.items()
        },
        "inspect_cache_keys": [_encode_reassess_key(k) for k in inspect_cache.keys()],
    }
    out_path = output_dir / "oracle_result.json"
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2, default=str)
    return out_path


def _strip_emoji(text: str) -> str:
    """Remove emoji characters that may not render properly in some viewers.

    Targets common emoji ranges that cause rendering issues (showing as boxes
    or replacement characters). Preserves standard ASCII and most Unicode text.
    """
    if not text:
        return text
    # Remove emoji: Emoticons, Dingbats, Symbols, Pictographs, Transport, Misc Symbols, Flags.
    # U+FFFD (replacement char) signals an encoding error upstream and breaks markdown
    # parsing when it lands next to headings/fences, so strip it too.
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"  # dingbats
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U0001FA00-\U0001FA6F"  # chess symbols, etc.
        "\U0001FA70-\U0001FAFF"  # symbols extended-A
        "\U00002600-\U000026FF"  # misc symbols
        "�"                  # replacement character (corrupted byte)
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub("", text)


def _fence_for(text: str) -> str:
    """Pick a backtick fence one longer than any run of backticks in `text`.

    Markdown allows fences of arbitrary length (≥3) so a longer outer fence
    safely wraps content that contains its own ``` blocks (common in model
    output that quotes JSON snippets or code).
    """
    if not text:
        return "```"
    longest_run = 0
    current = 0
    for ch in text:
        if ch == "`":
            current += 1
            if current > longest_run:
                longest_run = current
        else:
            current = 0
    return "`" * max(3, longest_run + 1)

from .viz import build_attribution_data, create_circuit_svg
from .llm_client import shorten_model_name, LLMClient, preflight_providers
from .judge_rubric import apply_refusal_transport, grade_completion
from .neuronpedia_link import feature_link, feature_url


# ---------------------------------------------------------------------------
# Pricing ($ per million tokens)
# ---------------------------------------------------------------------------
# Default cache read = 0.1× input price, cache write = 1.25× input price (Anthropic).
# Per-entry "cache_read_mult" / "cache_write_mult" override those defaults for providers
# that price caching differently (Gemini cache read 0.25×, Grok cache read 0.16×).
# Anthropic, Google, and OpenAI prices are stable across providers.
# Community/open model prices are OpenRouter listed rates as of March 2026
# (Gemini 3.5 Flash + Grok 4.3 looked up 2026-06-01, arm and judge models
# looked up 2026-07-26 against the live /api/v1/models catalog) and may differ
# from actual charges.
MODEL_PRICING = {
    # --- Anthropic native IDs (direct API) ---
    "claude-opus-4-6":   {"input":  5.00, "output": 25.00},
    "claude-sonnet-4-6": {"input":  3.00, "output": 15.00},
    "claude-haiku-4-5":  {"input":  1.00, "output":  5.00},
    # --- OpenRouter IDs ---
    # Anthropic models
    "anthropic/claude-opus-4.6":   {"input":  5.00, "output": 25.00},
    "anthropic/claude-sonnet-4.6": {"input":  3.00, "output": 15.00},
    "anthropic/claude-haiku-4.5":  {"input":  1.00, "output":  5.00},
    # eval judge (current panel). Cache read $0.20/M = 0.10x, the Anthropic default.
    "anthropic/claude-sonnet-5":   {"input":  2.00, "output": 10.00},
    # Google models
    "google/gemini-3.1-pro-preview":        {"input": 2.00, "output": 12.00},
    "google/gemini-3-flash-preview":        {"input": 0.50, "output":  3.00},
    "google/gemini-3.1-flash-lite-preview": {"input": 0.25, "output":  1.50},
    # eval judge. Gemini implicit caching: read 0.25×, no Anthropic-style write premium.
    "google/gemini-3.5-flash":              {"input": 1.50, "output":  9.00, "cache_read_mult": 0.25, "cache_write_mult": 1.0},
    # xAI models
    # eval judge. Cached input $0.20/M vs $1.25/M input = 0.16× read; auto-cache, no write premium.
    "x-ai/grok-4.3":                        {"input": 1.25, "output":  2.50, "cache_read_mult": 0.16, "cache_write_mult": 1.0},
    # OpenAI models
    "openai/gpt-5.4":       {"input": 2.50, "output": 15.00},
    # Spurious-probes feature-count eval judge. Added 2026-07-28 from the live catalog:
    # it was absent, so compute_cost returned None and that eval's judging cost
    # recorded as nothing at all rather than as a wrong number.
    "openai/gpt-5.4-mini":  {"input": 0.75, "output":  4.50},
    # arm model. Same list price as gpt-5.4. >272K prompt tokens bills 5.00/22.50.
    "openai/gpt-5.6-terra": {"input": 2.50, "output": 15.00},
    "openai/gpt-5.3-codex": {"input": 1.75, "output": 14.00},
    # Groq's rate, not the cheapest-endpoint rate (0.037/0.17 as of 2026-07-26).
    # This became an UPPER BOUND on 2026-07-28, when allow_fallbacks flipped to
    # True in OPENROUTER_MODEL_ROUTING: `order` still tries Groq first, but a
    # throttled call can now be served by a cheaper host and billed at its rate
    # while compute_cost still charges Groq's. Overstating cost is the safe
    # direction, and usage["providers"] records the actual split per run if an
    # exact figure is ever needed.
    "openai/gpt-oss-120b":  {"input": 0.15, "output": 0.60},
    # arm 3. Repriced 2026-07-28 from the 0.14/0.40 cheapest-endpoint
    # rate to Cerebras's 0.99/1.49, because the model is now ORDERED onto
    # Cerebras for throughput (389 tok/s vs 22 on kilo, see
    # OPENROUTER_MODEL_ROUTING). Pricing is per model here, not per endpoint, so
    # this is deliberately the DEAREST host in the order: SambaNova (0.38/1.15)
    # and any fallback host are cheaper, which makes arm 3's recorded cost an
    # upper bound rather than an undercount. Roughly 7x the old figure, so do not
    # compare arm 3's dollars against the earlier runs.
    "google/gemma-4-31b-it":       {"input": 0.99,  "output": 1.49},
    # Other models
    "moonshotai/kimi-k2.5":        {"input": 0.45,  "output": 2.20},
    # eval judge (current panel). Cache read $0.109/M = 0.17x, auto-cache, no write premium.
    "moonshotai/kimi-k2.6":        {"input": 0.646, "output": 2.72, "cache_read_mult": 0.17, "cache_write_mult": 1.0},
    "minimax/minimax-m2.5":        {"input": 0.295, "output": 1.20},
    "minimax/minimax-m2.7":        {"input": 0.30,  "output": 1.20},
    # arm model. Cache read $0.06/M = 0.20x, auto-cache, no write premium.
    "minimax/minimax-m3":          {"input": 0.30,  "output": 1.20, "cache_read_mult": 0.20, "cache_write_mult": 1.0},
    # eval judge (current panel).
    "z-ai/glm-5.2":                {"input": 0.6692, "output": 2.1032},
    "deepseek/deepseek-v3.2":     {"input": 0.26,  "output": 0.38},
    "qwen/qwen3.5-397b-a17b":     {"input": 0.39,  "output": 2.34},
}

CACHE_READ_MULTIPLIER = 0.10   # cache reads cost 10% of input price
CACHE_WRITE_MULTIPLIER = 1.25  # cache writes cost 125% of input price


def compute_cost(usage: dict) -> float | None:
    """Compute dollar cost from a usage dict.

    Returns None if the model is not in MODEL_PRICING.
    """
    model = usage.get("model", "")
    pricing = MODEL_PRICING.get(model)
    if pricing is None:
        return None

    input_price = pricing["input"] / 1_000_000
    output_price = pricing["output"] / 1_000_000
    cache_read_price = input_price * pricing.get("cache_read_mult", CACHE_READ_MULTIPLIER)
    cache_write_price = input_price * pricing.get("cache_write_mult", CACHE_WRITE_MULTIPLIER)

    cost = (
        usage.get("input_tokens", 0) * input_price
        + usage.get("output_tokens", 0) * output_price
        + usage.get("cache_read_input_tokens", 0) * cache_read_price
        + usage.get("cache_creation_input_tokens", 0) * cache_write_price
    )
    return cost


def amortized_usage(usage: dict) -> dict:
    """Zeroed copy of a usage dict that keeps the model key.

    Shared LLM passes (relevance, grader, reassess) are paid once per slug but
    their usage blocks land in every stage dir of a multi-stage run. Summing
    compute_cost over all artifacts would double count. The fix (next-
    refactoring.md decision 4): the FIRST stage dir that carries the block keeps
    the real usage, every later stage dir carries this zeroed copy. The model
    key is preserved on purpose so compute_cost prices it as 0.0 rather than
    None (None blocks are filtered out by save_run_results, which would
    silently undercount). A usage dict without a model key raises for the same
    reason, a model-less zeroed copy would price to None and undercount.
    Mirrors judge_rubric._empty_usage.

    Callers pair the returned dict with a sibling "usage_amortized_from":
    "<owner mode>" marker, and the owner block with "usage_amortized_from": None,
    so the amortization is auditable from the artifacts.
    """
    model = usage.get("model") if usage else None
    if not model:
        raise ValueError(
            f"amortized_usage needs a usage dict with a model key, got {usage!r}"
        )
    return {
        "model": model,
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_read_input_tokens": 0,
        "cache_creation_input_tokens": 0,
        # Serving provenance is a property of the call, not of who is charged
        # for it, so it survives amortization. An empty histogram here would
        # read as "no provider recorded" instead of "charged to the owner".
        "providers": dict(usage.get("providers") or {}),
    }


# ---------------------------------------------------------------------------
# Harness grader: fresh-context oracle-model re-ranking of interventions
# ---------------------------------------------------------------------------
# The grader is the oracle model itself (config.orchestrator_model) but called once
# per UNIQUE completion in an independent context, so its pick does not inherit the
# distraction of the inline self-ranking emitted at the tail of a ~60-intervention
# transcript. Selecting with the oracle model and scoring with the external ensemble
# (exp_judge.py) is a clean train/test split, the diff-in-mean analogue. It always runs
# when there are interventions to grade.
_GRADER_MAX_WORKERS = 8


def _grader_intervention_id(iv: dict) -> str:
    """Compact id string for an intervention, matching the oracle_ranking id form.

    Single:    'L{layer}:F{feature}@{pos}, scale={s}'
    Supernode: 'supernode[L..:F..@.., ...], scale={s}'
    Same shape _parse_oracle_ranking parses and exp_judge.render_intervention_id emits.
    """
    spec = iv.get("intervention", {}) or {}
    scale = spec.get("scale")
    if spec.get("type") == "supernode" or "features" in spec:
        feats = spec.get("features", []) or []
        parts = [
            f"L{f.get('layer')}:F{f.get('feature_idx')}@{f.get('position', f.get('pos'))}"
            for f in feats
        ]
        return f"supernode[{', '.join(parts)}], scale={scale}"
    return f"L{spec.get('layer')}:F{spec.get('feature_idx')}@{spec.get('position')}, scale={scale}"


def grade_interventions(interventions: list[dict] | None, config, baseline_answer: str):
    """Fresh-context oracle-model grader over all non-screening interventions.

    Always runs when there are interventions to grade. The grader is the intervention
    selector, replacing the oracle's removed inline self-ranking. It grades each UNIQUE
    ``answer_after`` completion once with config.orchestrator_model using the shared
    judge rubric, maps the score back to every intervention sharing that completion
    (byte-identical output must not get two different temp-1 scores), then ranks by
    overall desc.

    Returns ``(grader_ranking, grader_usage)``:
      - grader_ranking: list of {intervention_id, rank, usability, plausibility, overall,
        grader_rank, top1}, one entry per intervention in run order. ``rank`` is the
        1-based run order (matches write_elicitation_outputs), so exp_judge can join the
        grader's pick back to a recorded intervention. None when there are no interventions.
      - grader_usage: accumulated usage dict (carries model=config.orchestrator_model so
        compute_cost prices it), or None when nothing was graded.
    """
    # An empty intervention list skips grading (no network call). Otherwise the harness
    # grader always runs, since it is the intervention selector now that the oracle's
    # inline self-ranking is removed.
    interventions = interventions or []
    if not interventions:
        return None, None

    model = config.orchestrator_model
    question = config.user_message

    # Dedup by answer_after. Empty / None completions collapse to "".
    unique_completions: list[str] = []
    seen: set[str] = set()
    for iv in interventions:
        comp = iv.get("answer_after") or ""
        if comp not in seen:
            seen.add(comp)
            unique_completions.append(comp)

    client = LLMClient(provider=getattr(config, "provider", "openrouter"))
    scores_by_comp: dict[str, dict | None] = {}
    usages: list[dict] = []

    def _grade(comp):
        return comp, grade_completion(client, model, question, comp)

    max_workers = max(1, min(_GRADER_MAX_WORKERS, len(unique_completions)))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(_grade, c) for c in unique_completions]
        for fut in concurrent.futures.as_completed(futures):
            comp, (score, usage) = fut.result()
            scores_by_comp[comp] = score
            if usage:
                usages.append(usage)

    # FAIL LOUD when nothing graded. grade_completion swallows transport errors and
    # returns None, so a misrouted model used to produce a run that looked complete
    # and carried a null score on every row. That happened on 2026-07-28: 87 of 87
    # calls 404'd under OpenRouter's require_parameters filter, and the run still
    # wrote oracle_result.json, elicitation.json and report.md with a full
    # grader_ranking whose usability/plausibility/overall were all null. Nothing in
    # the pipeline noticed for 45 minutes. A total wipeout is never grader noise, it
    # is a configuration or routing fault, so refuse to persist it.
    failed = [c for c, s in scores_by_comp.items() if s is None]
    if unique_completions and len(failed) == len(unique_completions):
        raise RuntimeError(
            f"Grading produced no scores: all {len(unique_completions)} completions "
            f"failed against grader model {model!r} via provider "
            f"{getattr(config, 'provider', 'openrouter')!r}. The per-call reason was "
            f"printed above as '[grade {model}] ERROR: ...'. This is a routing or "
            f"credentials fault, not grader noise, so the run is not being saved with "
            f"null scores."
        )
    if failed:
        # Partial failure still skews any mean taken over the survivors, so say so
        # rather than letting a quiet minority of nulls through unannounced.
        print(
            f"    [grade {model}] WARNING: {len(failed)}/{len(unique_completions)} "
            f"completions failed to grade and will carry null scores."
        )

    # Refusal transport. A safety-blocked grade arrives as {u:1, p:1, overall:1,
    # _refusal:True}, which is a PERFECT overall and would take grader_rank 1 purely
    # for having been blocked, i.e. the block would select the submission. This grader
    # is single-model with one draw per completion, so the imputation pool is the other
    # completions graded in this same pass (the cross-judge pool of the external
    # ensemble has no analogue here). Non-refused rows are returned unchanged.
    graded = {c: [s] for c, s in scores_by_comp.items() if s is not None}
    for comp, draws in apply_refusal_transport(graded).items():
        scores_by_comp[comp] = draws[0]

    grader_providers: dict[str, int] = {}
    for u in usages:
        served_by = u.get("provider") or "unknown"
        grader_providers[served_by] = grader_providers.get(served_by, 0) + 1
    grader_usage = {
        "model": model,
        "input_tokens": sum(u.get("input_tokens", 0) for u in usages),
        "output_tokens": sum(u.get("output_tokens", 0) for u in usages),
        "cache_read_input_tokens": sum(u.get("cache_read_input_tokens", 0) for u in usages),
        "cache_creation_input_tokens": sum(u.get("cache_creation_input_tokens", 0) for u in usages),
        # Serving provenance: host -> call count across the grading fan-out.
        "providers": grader_providers,
    }

    # One ranking entry per intervention (run order), score mapped from its completion.
    entries: list[dict] = []
    for i, iv in enumerate(interventions):
        comp = iv.get("answer_after") or ""
        score = scores_by_comp.get(comp)
        entries.append({
            "intervention_id": _grader_intervention_id(iv),
            "rank": i + 1,  # 1-based run order; matches write_elicitation_outputs
            "usability": score.get("usability") if score else None,
            "plausibility": score.get("plausibility") if score else None,
            "overall": score.get("overall") if score else None,
            # True when this completion's grade was a safety block whose plausibility
            # was imputed rather than scored. Kept so the analysis can separate
            # transported rows from directly graded ones.
            "refused": bool(score.get("_refusal")) if score else False,
        })

    # Assign grader_rank / top1 by sorting a view (None overalls last). The view holds
    # the same dict objects, so mutating them mutates `entries`.
    ordered = sorted(
        entries,
        key=lambda e: (e["overall"] is not None, e["overall"] if e["overall"] is not None else -1.0),
        reverse=True,
    )
    for gr, e in enumerate(ordered, start=1):
        e["grader_rank"] = gr
        e["top1"] = gr == 1

    return entries, grader_usage


# ---------------------------------------------------------------------------
# Sweep grader (deterministic multi-stage seed sweep)
# ---------------------------------------------------------------------------
# Unconditional grader for scripts/run_sweeps.py. Like grade_interventions for the
# agentic pipeline, this always runs (the deterministic sweep's whole point is to hold
# the outcome metric, the LLM grader, fixed across selection variants), but here it also
# grades the baseline regardless of how many measurements exist. It grades the baseline
# answer plus every unique answer_after across the K x 4 anchor-sweep measurements,
# attaches the score onto each measurement, ranks by overall desc, and flags the
# single top-1 (the run's self-nominated submission).


def grade_sweep(measurements, baseline_answer, config, *, question, n_repeats: int = 1):
    """Grade every unique anchor-sweep answer with the shared judge rubric.

    Args:
        measurements: the flat list of per (feature, scale) measurement dicts
            from batched_anchor_sweep (each carries answer_after, layer,
            feature_idx, pos, scale, shift_bucket). Mutated in place: a
            {usability, plausibility, overall, usability_std, plausibility_std,
            n_repeats} block is attached to each.
        baseline_answer: the no-intervention completion, graded as a reference row.
        config: an object carrying grader_model and provider (the run config the
            orchestrator builds). grade_completion is called with config.grader_model.
        question: the user question the rubric judges the completion against.
        n_repeats: how many independent temperature-1.0 draws to grade each
            unique completion with. The per-axis MEAN over the draws is the
            reported usability/plausibility, overall is recomputed from the two
            means, and the per-axis population std is stored alongside. Defaults
            to 1, which reproduces the single-draw behavior byte-for-byte (std
            0.0). The CLI passes a higher value (5) to average out temperature-1
            grader noise (next-refactoring.md decision 3).

    Returns:
        a grades record dict with keys:
          - grader_model: the model id used
          - question: the graded question
          - n_repeats: the draw count used
          - baseline: {answer, usability, plausibility, overall, usability_std,
            plausibility_std} for the baseline
          - ranking: list (one per measurement, in measurement order) of
            {intervention_id, layer, feature_idx, pos, scale, shift_bucket,
             usability, plausibility, overall, usability_std, plausibility_std,
             grader_rank, top1}
          - top1: the single ranking entry with top1 True (or None when there are
            no measurements)
          - usage: accumulated token-usage dict over ALL draws (carries
            grader_model so compute_cost prices it)

    FAIL-LOUD: raises RuntimeError if the grader model's gateway has no API key,
    if n_repeats is not a positive int, or if any of the n_repeats draws for a
    completion returns None (a parse/transport failure must not be silently
    averaged over the surviving draws). The grader runs unconditionally.
    """
    if not isinstance(n_repeats, int) or n_repeats < 1:
        raise ValueError(f"n_repeats must be a positive int, got {n_repeats!r}")

    measurements = measurements or []
    model = config.grader_model
    provider = getattr(config, "provider", "openrouter")
    # Check the key for the gateway this grader model will ACTUALLY be routed
    # to. This used to hardcode OPENROUTER_API_KEY while building
    # LLMClient(provider=provider) two lines down, so --provider kilo was wrong
    # in both directions: a Kilo-only run was rejected for lacking a key it
    # never needed, and an OpenRouter-only run passed the check and then 401'd
    # against Kilo. preflight_providers resolves the per-model pin, so a grader
    # pinned to OpenRouter is still checked against OPENROUTER_API_KEY even on
    # a Kilo run.
    preflight_providers([model], provider)

    # Dedup by answer_after (byte-identical output must not get two temp-1 scores).
    # The baseline answer is graded too, as a reference row. Each unique
    # completion is then graded n_repeats times below.
    base_comp = baseline_answer or ""
    unique_completions: list[str] = [base_comp]
    seen: set[str] = {base_comp}
    for m in measurements:
        comp = m.get("answer_after") or ""
        if comp not in seen:
            seen.add(comp)
            unique_completions.append(comp)

    client = LLMClient(provider=provider)
    # Per-completion list of the n_repeats raw draws (each a parse_scores dict).
    draws_by_comp: dict[str, list[dict]] = {c: [] for c in unique_completions}
    usages: list[dict] = []

    # One job per (completion, draw). Tag each job with its completion so the
    # draws scatter back. The executor width still floors at 1 and caps at
    # _GRADER_MAX_WORKERS, now over the full job list (unique x n_repeats).
    grade_jobs = [c for c in unique_completions for _ in range(n_repeats)]

    def _grade(comp):
        return comp, grade_completion(client, model, question, comp)

    max_workers = max(1, min(_GRADER_MAX_WORKERS, len(grade_jobs)))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(_grade, c) for c in grade_jobs]
        for fut in concurrent.futures.as_completed(futures):
            comp, (score, usage) = fut.result()
            # FAIL-LOUD: a None draw is a parse/transport failure. Averaging the
            # surviving draws would silently change the sample size, so raise.
            if score is None:
                raise RuntimeError(
                    "grade_sweep got a None score from grade_completion for a "
                    f"completion (model {model!r}). Refusing to average over a "
                    "partial draw set. Re-run after fixing the grader transport."
                )
            draws_by_comp[comp].append(score)
            # Usage accrues across every draw, that is the true bill.
            if usage:
                usages.append(usage)

    # Refusal transport, BEFORE the mean, so a safety-blocked draw does not enter the
    # average as a perfect 1.0/1.0 and take grader_rank 1 for having been blocked.
    # Two-level pool: a completion's own scored repeats first, then the sweep-wide
    # mean over every scored draw. The second level is the one that fires, because
    # blocks are all-or-nothing per (judge, completion) cell in both archives, so a
    # single-model grader that refused once has usually refused all n_repeats times.
    pool_vals = [
        float(d["plausibility"])
        for draws in draws_by_comp.values()
        for d in draws
        if not d.get("_refusal")
    ]
    pool_p = (sum(pool_vals) / len(pool_vals)) if pool_vals else None
    n_refused_draws = sum(
        1 for draws in draws_by_comp.values() for d in draws if d.get("_refusal")
    )
    if n_refused_draws:
        draws_by_comp = {
            comp: apply_refusal_transport(draws, pool_plausibility=pool_p)
            for comp, draws in draws_by_comp.items()
        }

    # Collapse the n_repeats draws per completion into a single mean score with
    # per-axis std. mean over a single draw reproduces that draw exactly.
    scores_by_comp: dict[str, dict] = {}
    for comp, draws in draws_by_comp.items():
        if len(draws) != n_repeats:
            # Defensive: every unique completion was scheduled n_repeats times
            # and a None draw already raised, so this should be unreachable.
            raise RuntimeError(
                f"grade_sweep expected {n_repeats} draws for a completion, "
                f"collected {len(draws)} (model {model!r})."
            )
        u_vals = [float(d["usability"]) for d in draws]
        p_vals = [float(d["plausibility"]) for d in draws]
        mean_u = round(statistics.fmean(u_vals), 2)
        mean_p = round(statistics.fmean(p_vals), 2)
        # The MEAN is over all draws (transported ones included, that is the point of
        # the transport), but the STD is over the DIRECTLY SCORED draws only. Imputed
        # draws all carry the same value by construction, so including them would
        # shrink the spread mechanically and, when every draw was blocked, report a
        # confident 0.0 for a completion the grader never actually scored. None says
        # "no grader-variability evidence", which 0.0 cannot say.
        scored = [d for d in draws if not d.get("_refusal")]
        u_scored = [float(d["usability"]) for d in scored]
        p_scored = [float(d["plausibility"]) for d in scored]
        std_u = round(statistics.pstdev(u_scored), 4) if len(u_scored) > 1 else (
            0.0 if u_scored else None)
        std_p = round(statistics.pstdev(p_scored), 4) if len(p_scored) > 1 else (
            0.0 if p_scored else None)
        scores_by_comp[comp] = {
            "usability": mean_u,
            "plausibility": mean_p,
            "overall": round((mean_u + mean_p) / 2, 2),
            "usability_std": std_u,
            "plausibility_std": std_p,
            # Draw accounting. n_refused counts this completion's safety blocks, whose
            # plausibility was imputed rather than scored (0 on the normal path).
            "n_scored": len(scored),
            "n_refused": len(draws) - len(scored),
        }

    sweep_providers: dict[str, int] = {}
    for u in usages:
        served_by = u.get("provider") or "unknown"
        sweep_providers[served_by] = sweep_providers.get(served_by, 0) + 1
    usage = {
        "model": model,
        "input_tokens": sum(u.get("input_tokens", 0) for u in usages),
        "output_tokens": sum(u.get("output_tokens", 0) for u in usages),
        "cache_read_input_tokens": sum(u.get("cache_read_input_tokens", 0) for u in usages),
        "cache_creation_input_tokens": sum(u.get("cache_creation_input_tokens", 0) for u in usages),
        # Serving provenance: host -> call count across the grading fan-out.
        "providers": sweep_providers,
    }

    # Attach scores onto each measurement (mutating) and build ranking rows.
    ranking: list[dict] = []
    for m in measurements:
        comp = m.get("answer_after") or ""
        score = scores_by_comp.get(comp)
        usability = score.get("usability") if score else None
        plausibility = score.get("plausibility") if score else None
        overall = score.get("overall") if score else None
        usability_std = score.get("usability_std") if score else None
        plausibility_std = score.get("plausibility_std") if score else None
        n_scored = score.get("n_scored") if score else None
        n_refused = score.get("n_refused", 0) if score else 0
        m["usability"] = usability
        m["plausibility"] = plausibility
        m["overall"] = overall
        m["usability_std"] = usability_std
        m["plausibility_std"] = plausibility_std
        m["n_repeats"] = n_repeats
        m["n_scored"] = n_scored
        m["n_refused"] = n_refused
        layer = m.get("layer")
        feature_idx = m.get("feature_idx")
        pos = m.get("pos")
        scale = m.get("scale")
        ranking.append({
            "intervention_id": f"L{layer}:F{feature_idx}@{pos}, scale={scale}",
            "layer": layer,
            "feature_idx": feature_idx,
            "pos": pos,
            "scale": scale,
            "shift_bucket": m.get("shift_bucket"),
            "usability": usability,
            "plausibility": plausibility,
            "overall": overall,
            "usability_std": usability_std,
            "plausibility_std": plausibility_std,
            "n_scored": n_scored,
            "n_refused": n_refused,
        })

    # Rank by overall desc (None overalls last). Sort a view of the same dicts so
    # mutating them mutates the ranking list.
    ordered = sorted(
        ranking,
        key=lambda e: (e["overall"] is not None, e["overall"] if e["overall"] is not None else -1.0),
        reverse=True,
    )
    for gr, e in enumerate(ordered, start=1):
        e["grader_rank"] = gr
        e["top1"] = gr == 1

    base_score = scores_by_comp.get(base_comp)
    baseline_block = {
        "answer": base_comp,
        "usability": base_score.get("usability") if base_score else None,
        "plausibility": base_score.get("plausibility") if base_score else None,
        "overall": base_score.get("overall") if base_score else None,
        "usability_std": base_score.get("usability_std") if base_score else None,
        "plausibility_std": base_score.get("plausibility_std") if base_score else None,
        "n_scored": base_score.get("n_scored") if base_score else None,
        "n_refused": base_score.get("n_refused", 0) if base_score else 0,
    }

    top1 = ordered[0] if ordered else None

    return {
        "grader_model": model,
        "question": question,
        "n_repeats": n_repeats,
        "baseline": baseline_block,
        "ranking": ranking,
        "top1": top1,
        # Safety blocks across every (completion, draw) in this pass, and the
        # run-wide plausibility the transport falls back to for a completion whose
        # every draw was blocked. Named "fallback" and not "imputed" on purpose: a
        # completion with SOME scored repeats imputes from its own repeats instead,
        # so this value is the second level of the pool, not necessarily the one used.
        "n_refused_draws": n_refused_draws,
        "refusal_fallback_plausibility": (
            round(pool_p, 2) if (n_refused_draws and pool_p is not None) else None
        ),
        "usage": usage,
    }


# ---------------------------------------------------------------------------
# Process trace helpers
# ---------------------------------------------------------------------------

def _fmt_tool_input(tool: str, inp: dict) -> str:
    if tool == "inspect_feature":
        return f"L{inp.get('layer')}, F{inp.get('feature_idx')}"
    if tool == "get_upstream_features":
        return f"L{inp.get('layer')}:F{inp.get('feature_idx')}@{inp.get('pos')}, k={inp.get('k', 5)}"
    if tool == "get_top_features":
        return f'token="{inp.get("token", "")}", k={inp.get("k", 10)}'
    if tool == "get_top_logits":
        return f'k={inp.get("k", 5)}'
    return str(inp)[:80]


def _md_esc(s: str) -> str:
    """Escape characters that break GitHub-flavored markdown table cells."""
    if s is None:
        return ""
    return s.replace("|", "\\|").replace("\n", " ")


def _fmt_tool_output(tool: str, out) -> str:
    if isinstance(out, dict) and "error" in out:
        return f'❌ {_md_esc(str(out["error"])[:60])}'
    if tool == "inspect_feature":
        if isinstance(out, dict):
            return f'"{_md_esc(out.get("label", "?")[:70])}"'
    if tool == "get_upstream_features":
        if isinstance(out, list):
            if not out:
                return "no upstreams"
            top = out[0]
            if top.get("type") == "embedding":
                s = f'Emb:"{top.get("token")}"@{top.get("pos")} (de={top.get("direct_effect", 0):.2f})'
            else:
                s = f'L{top.get("layer")}:F{top.get("feature_idx")} (de={top.get("direct_effect", 0):.2f})'
            if len(out) > 1:
                s += f" +{len(out)-1} more"
            return s
    if tool == "get_top_logits":
        if isinstance(out, list):
            return ", ".join(f'"{e.get("token")}" ({e.get("probability", 0)*100:.0f}%)' for e in out[:3])
    if tool == "get_top_features":
        if isinstance(out, list) and out:
            top = out[0]
            return f'{len(out)} features; top: L{top.get("layer")}:{top.get("feature_idx")} de={top.get("direct_effect", 0):.3f}'
    return str(out)[:80]


def _build_process_trace(result: dict) -> str:
    """Build a ## Process Trace section from the flat tool_calls list."""
    tool_calls = result["tool_calls"]

    # Partition into phases:
    #   scout       = all direct calls before the first trace_path_subagent
    #   batches     = one or more consecutive groups of trace_path_subagent calls
    #   post        = direct calls after the last trace_path_subagent and before build_circuit
    #   build_call  = the build_circuit call
    scout_calls = []
    batches: list[list[dict]] = []
    post_calls = []
    build_call = None

    current_batch: list[dict] = []
    dispatched_any = False
    in_batch = False

    for tc in tool_calls:
        name = tc["tool"]
        if name == "trace_path_subagent":
            if not in_batch:
                if current_batch:  # flush any dangling post_calls into a previous post list
                    pass
                current_batch = []
                in_batch = True
            dispatched_any = True
            current_batch.append(tc)
        elif name == "build_circuit":
            if in_batch and current_batch:
                batches.append(current_batch)
                current_batch = []
                in_batch = False
            build_call = tc
        else:
            if in_batch and current_batch:
                batches.append(current_batch)
                current_batch = []
                in_batch = False
            if not dispatched_any:
                scout_calls.append(tc)
            else:
                post_calls.append(tc)

    if in_batch and current_batch:
        batches.append(current_batch)

    lines = ["## Process Trace\n"]

    # --- SCOUT ---
    if scout_calls:
        # Group consecutive inspect_feature calls to keep table compact
        grouped: list[tuple[str, list[dict]]] = []
        for tc in scout_calls:
            if grouped and grouped[-1][0] == tc["tool"] == "inspect_feature":
                grouped[-1][1].append(tc)
            else:
                grouped.append((tc["tool"], [tc]))

        lines.append("### Scout\n")
        lines.append("| # | Tool | Summary |")
        lines.append("|---|------|---------|")
        row = 0
        for tool, group in grouped:
            if tool == "inspect_feature" and len(group) > 1:
                row += 1
                labels_str = ", ".join(
                    f'L{tc["input"].get("layer")}:{tc["input"].get("feature_idx")}' for tc in group
                )
                lines.append(f"| {row} | `inspect_feature` ×{len(group)} | {labels_str} |")
            else:
                for tc in group:
                    row += 1
                    lines.append(f"| {row} | `{tc['tool']}` | {_fmt_tool_output(tc['tool'], tc['output'])} |")
        lines.append("")

    # --- DISPATCH BATCHES ---
    for batch_idx, batch in enumerate(batches):
        batch_label = "Dispatch" if batch_idx == 0 else f"Re-dispatch (round {batch_idx + 1})"
        lines.append(f"### {batch_label}: {len(batch)} subagent(s) (concurrent)\n")
        lines.append("| Label | Node | Outcome | Features | Edges | Objective |")
        lines.append("|-------|------|---------|----------|-------|-----------|")
        for tc in batch:
            inp = tc["input"]
            out = tc["output"]
            sa_label = tc.get("label") or inp.get("label") or f"L{inp['starting_layer']}:F{inp['starting_feature_idx']}@{inp['starting_pos']}"
            node = f"L{inp['starting_layer']}:F{inp['starting_feature_idx']}@{inp['starting_pos']}"
            obj = inp.get("objective", "")
            obj_short = obj[:80] + ("…" if len(obj) > 80 else "")
            if "error" in out:
                outcome = "❌ error"
                nf = ne = "n/a"
            elif "warning" in out:
                usage_turns = out.get("usage", {})
                # infer turn count from trace_log length
                tlog = out.get("trace_log", [])
                outcome = f"❌ no report ({len(tlog)} tool calls)"
                nf = ne = "n/a"
            else:
                nf = len(out.get("discovered_features", []))
                ne = len(out.get("discovered_edges", []))
                outcome = f"✅ reported"
            lines.append(f"| {sa_label} | `{node}` | {outcome} | {nf} | {ne} | {obj_short} |")
        lines.append("")

        # Per-subagent collapsible tool traces
        for tc in batch:
            inp = tc["input"]
            out = tc["output"]
            sa_label = tc.get("label") or inp.get("label") or f"L{inp['starting_layer']}:F{inp['starting_feature_idx']}@{inp['starting_pos']}"
            tlog = out.get("trace_log", [])
            if not tlog:
                continue
            lines.append(f"<details>")
            lines.append(f"<summary><b>{sa_label}</b>, tool trace ({len(tlog)} calls)</summary>\n")
            lines.append("| # | Tool | Input | Output |")
            lines.append("|---|------|-------|--------|")
            for j, entry in enumerate(tlog, 1):
                i_str = _fmt_tool_input(entry["tool"], entry["input"])
                o_str = _fmt_tool_output(entry["tool"], entry["output"])
                lines.append(f"| {j} | `{entry['tool']}` | {i_str} | {o_str} |")
            expl = out.get("explanation", "")
            if expl:
                lines.append(f"\n**Findings:** {expl[:400]}{'…' if len(expl) > 400 else ''}")
            lines.append("\n</details>\n")

    # --- POST-DISPATCH ---
    if post_calls:
        grouped_post: list[tuple[str, list[dict]]] = []
        for tc in post_calls:
            if grouped_post and grouped_post[-1][0] == tc["tool"] == "inspect_feature":
                grouped_post[-1][1].append(tc)
            else:
                grouped_post.append((tc["tool"], [tc]))

        lines.append("### Post-dispatch (orchestrator)\n")
        lines.append("| # | Tool | Summary |")
        lines.append("|---|------|---------|")
        row = 0
        for tool, group in grouped_post:
            if tool == "inspect_feature" and len(group) > 1:
                row += 1
                labels_str = ", ".join(
                    f'L{tc["input"].get("layer")}:{tc["input"].get("feature_idx")}' for tc in group
                )
                lines.append(f"| {row} | `inspect_feature` ×{len(group)} | {labels_str} |")
            else:
                for tc in group:
                    row += 1
                    lines.append(f"| {row} | `{tc['tool']}` | {_fmt_tool_input(tc['tool'], tc['input'])} → {_fmt_tool_output(tc['tool'], tc['output'])} |")
        lines.append("")

    # --- BUILD ---
    if build_call is not None:
        out = build_call["output"]
        n_nodes = len(out.get("nodes", []))
        n_edges = len(out.get("edges", []))
        lines.append("### Build\n")
        lines.append(f"`build_circuit` → {n_nodes} nodes, {n_edges} edges\n")

    return "\n".join(lines)


def _extract_pinned_ids(tool_calls: list) -> list[str]:
    """Extract Neuronpedia-style pinned IDs from tool call results.

    Each feature {layer, feature_idx, pos} becomes "{layer}_{feature_idx}_{pos}".

    Primary source: the last build_circuit call (curated by the orchestrator).
    Fallback: all discovered_features from trace_path_subagent calls (used when
    the model completes analysis without calling build_circuit).
    """
    # Primary: last build_circuit call
    circuit = None
    for tc in tool_calls:
        if tc["tool"] == "build_circuit" and isinstance(tc.get("output"), dict):
            circuit = tc["output"]
    if circuit is not None:
        pinned = []
        for node in circuit.get("nodes", []):
            for feat in node.get("features", []):
                pinned.append(f"{feat['layer']}_{feat['feature_idx']}_{feat['pos']}")
        return pinned

    # Fallback: aggregate all features reported by subagents
    seen = set()
    pinned = []
    for tc in tool_calls:
        if tc["tool"] == "trace_path_subagent" and isinstance(tc.get("output"), dict):
            for feat in tc["output"].get("discovered_features", []):
                key = (feat["layer"], feat["feature_idx"], feat["pos"])
                if key not in seen:
                    seen.add(key)
                    pinned.append(f"{feat['layer']}_{feat['feature_idx']}_{feat['pos']}")
    return pinned


def _format_features_short(intervention_block: dict) -> str:
    """Render the features touched by an intervention as a compact string."""
    if intervention_block.get("type") == "supernode":
        feats = intervention_block.get("features") or []
        return ", ".join(
            f"L{f['layer']}:F{f['feature_idx']}@{f['position']}" for f in feats
        )
    return (
        f"L{intervention_block['layer']}:"
        f"F{intervention_block['feature_idx']}@{intervention_block['position']}"
    )


def _truncate(text: str, n: int = 200) -> str:
    text = (text or "").replace("\n", " ").strip()
    return text if len(text) <= n else text[: n - 1] + "…"


def _collect_pinned_features(tool_calls: list) -> tuple[list[dict], list[dict]]:
    """Gather pinned features and connectivity edges from the last build_circuit call.

    Returns (features, edges):
      features = [{"layer", "feature_idx", "pos", "supernode_label", "autointerp", "frac_nonzero"}, ...]
      edges    = [{"from": "L:F@p", "to": "L:F@p"}, ...]
    """
    circuit = None
    for tc in tool_calls:
        if tc["tool"] == "build_circuit" and isinstance(tc.get("output"), dict):
            circuit = tc["output"]
    if circuit is None:
        return [], []

    # Pull autointerp labels and frac_nonzero from any prior inspect_feature calls.
    autointerp: dict[tuple[int, int], dict] = {}
    for tc in tool_calls:
        if tc["tool"] == "inspect_feature" and isinstance(tc.get("output"), dict):
            inp = tc["input"]
            key = (inp.get("layer"), inp.get("feature_idx"))
            out = tc["output"]
            autointerp[key] = {
                "label": out.get("label"),
                "frac_nonzero": out.get("frac_nonzero"),
            }
        if tc["tool"] == "trace_path_subagent" and isinstance(tc.get("output"), dict):
            for feat in tc["output"].get("discovered_features", []):
                key = (feat.get("layer"), feat.get("feature_idx"))
                if key not in autointerp:
                    autointerp[key] = {
                        "label": feat.get("label"),
                        "frac_nonzero": feat.get("frac_nonzero"),
                    }

    features: list[dict] = []
    seen: set[tuple[int, int, int]] = set()
    for node in (circuit.get("nodes") or []):
        node_label = node.get("label") or ""
        for feat in (node.get("features") or []):
            layer = feat.get("layer")
            idx = feat.get("feature_idx")
            pos = feat.get("pos")
            if (layer, idx, pos) in seen:
                continue
            seen.add((layer, idx, pos))
            ai = autointerp.get((layer, idx), {})
            features.append({
                "layer": layer,
                "feature_idx": idx,
                "pos": pos,
                "supernode_label": node_label,
                "autointerp": ai.get("label"),
                "frac_nonzero": ai.get("frac_nonzero"),
            })

    edges = circuit.get("edges", []) or []
    return features, edges


_RANK_FEAT_RE = re.compile(r"L(\d+):F(\d+)@(-?\d+)")


def _canon_iv_key(spec: dict):
    """Canonical (feature-set, scale) key from an intervention's param dict.

    Single and supernode collapse to a sorted tuple of (layer, feature, pos)
    plus scale, so the oracle's free-text id and the harness record join even
    if supernode features are listed in a different order.
    """
    scale = spec.get("scale")
    if spec.get("type") == "supernode" or "features" in spec:
        feats = spec.get("features", []) or []
        key = tuple(sorted((f.get("layer"), f.get("feature_idx"), f.get("position")) for f in feats))
    else:
        key = ((spec.get("layer"), spec.get("feature_idx"), spec.get("position")),)
    return (key, scale)


def _canon_iv_key_from_idstr(s: str):
    """Same canonical key, parsed from an oracle id string like
    'L12:F162475@34, scale=-2' or 'supernode[L23:F1@38, L22:F2@38], scale=-1'."""
    feats = [(int(l), int(f), int(p)) for l, f, p in _RANK_FEAT_RE.findall(s or "")]
    if not feats:
        return None
    m = re.search(r"scale\s*=\s*(-?\d+)", s)
    scale = int(m.group(1)) if m else None
    return (tuple(sorted(feats)), scale)


def _parse_oracle_ranking(oracle_response: str, interventions: list[dict]):
    """Extract the oracle's machine-readable intervention ranking from ANALYZE.

    Reads the last fenced ```json block in the ANALYZE text, joins each entry to
    a recorded intervention by canonical (feature-set, scale) key, recomputes
    overall = (u + p) / 2, sorts by overall desc, and flags the top 5. Returns
    None if no parseable block is present (exp_judge then falls back to scoring
    every intervention). Robust by design: a missing or malformed block never
    raises, it just yields None.
    """
    if not oracle_response:
        return None
    blocks = re.findall(r"```json\s*(.+?)```", oracle_response, re.S | re.I)
    parsed = None
    for b in reversed(blocks):
        try:
            obj = json.loads(b.strip())
        except (json.JSONDecodeError, ValueError):
            continue
        if isinstance(obj, list):
            parsed = obj
            break
    if not parsed:
        return None
    rec_index = {}
    for i, e in enumerate(interventions):
        rec_index[_canon_iv_key(e.get("intervention", {}))] = i + 1  # 1-based run order
    out = []
    for entry in parsed:
        if not isinstance(entry, dict):
            continue
        idstr = entry.get("intervention") or entry.get("intervention_id") or ""
        try:
            u = float(entry.get("usability"))
            p = float(entry.get("plausibility"))
        except (TypeError, ValueError):
            u = p = None
        overall = round((u + p) / 2, 3) if (u is not None and p is not None) else None
        key = _canon_iv_key_from_idstr(idstr)
        out.append({
            "intervention_id": idstr,
            "usability": u,
            "plausibility": p,
            "overall": overall,
            "label": entry.get("label"),
            "run_index": rec_index.get(key),
            "matched": key in rec_index,
        })
    out.sort(key=lambda r: (r["overall"] is not None, r["overall"] if r["overall"] is not None else -1.0),
             reverse=True)
    for i, r in enumerate(out):
        r["oracle_rank"] = i + 1
        r["top5"] = i < 5
    return out


def write_elicitation_outputs(
    exp_dir: str,
    *,
    prompt: str,
    baseline_answer: str,
    interventions: list[dict],
    oracle_response: str,
    tool_calls: list | None = None,
    neuronpedia_model_id: str = "qwen3-4b",
    neuronpedia_sae_id: str = "{layer}-transcoder-hp",
    grader_ranking: list[dict] | None = None,
) -> None:
    """Emit elicitation.json and elicitation.md.

    Structure (no regex auto-classification, the Oracle's ANALYZE narrative is
    the source of truth for win/softened/swap classification):
      1. Prompt + baseline
      2. Pinned features (autointerp label + supernode role + Neuronpedia link)
      3. Connectivity (from BUILD edges)
      4. Oracle judgment (verbatim ANALYZE)
      5. All interventions raw, in run order
    """
    tool_calls = tool_calls or []
    pinned_features, pinned_edges = _collect_pinned_features(tool_calls)

    payload = {
        "prompt": prompt,
        "answer_baseline": baseline_answer,
        "pinned_features": [
            {
                **f,
                "neuronpedia_url": feature_url(
                    f["layer"], f["feature_idx"],
                    model_id=neuronpedia_model_id, sae_template=neuronpedia_sae_id,
                ) if f.get("layer") is not None and f.get("feature_idx") is not None else None,
            }
            for f in pinned_features
        ],
        "pinned_edges": pinned_edges,
        "all_interventions_count": len(interventions),
        "interventions": [
            {
                "rank": i + 1,
                "intervention_type": e["intervention"].get("type", "single"),
                "source": e.get("source"),
                "intervention": e["intervention"],
                "answer_before": e.get("answer_before"),
                "answer_after": e.get("answer_after"),
                "top5_before": e.get("top5_before"),
                "top5_after": e.get("top5_after"),
                "hypothesis": e.get("hypothesis"),
            }
            for i, e in enumerate(interventions)
        ],
        "oracle_judgment_text": oracle_response,
        "oracle_ranking": _parse_oracle_ranking(oracle_response, interventions),
        # Edit 1b: fresh-context oracle-model grader pick (None unless the harness
        # grader ran). Sibling to oracle_ranking; exp_judge scores the grader's top-1.
        "grader_ranking": grader_ranking,
    }

    with open(os.path.join(exp_dir, "elicitation.json"), "w") as f:
        json.dump(payload, f, indent=2, default=str)

    # --- Markdown ---
    lines = ["# Elicitation Report", ""]
    lines.append(f"**Prompt:** {prompt}")
    lines.append("")
    lines.append("**Baseline (no intervention):**")
    lines.append("")
    lines.append(f"> {(baseline_answer or '').strip()}")
    lines.append("")
    lines.append(f"**Total interventions tried:** {len(interventions)}")
    lines.append("")

    # --- Pinned features section (with Neuronpedia URLs) ---
    if pinned_features:
        lines.append("## Pinned Features")
        lines.append("")
        lines.append("Features pinned by the Oracle in BUILD, with their autointerp labels and the Oracle's proposed role (supernode label). Click the Neuronpedia link to inspect each feature.")
        lines.append("")
        lines.append("| Feature | Pos | Supernode role | Autointerp label | frac_nonzero | Neuronpedia |")
        lines.append("|---------|-----|----------------|------------------|--------------|-------------|")
        for f in pinned_features:
            layer = f["layer"]
            idx = f["feature_idx"]
            pos = f["pos"]
            if layer is None or idx is None:
                continue
            url = feature_url(layer, idx, model_id=neuronpedia_model_id, sae_template=neuronpedia_sae_id)
            ai_label = (f.get("autointerp") or "n/a").replace("|", "\\|")
            sn_label = (f.get("supernode_label") or "n/a").replace("|", "\\|")
            fnz = f.get("frac_nonzero")
            fnz_str = f"{fnz:.2e}" if isinstance(fnz, (int, float)) else "n/a"
            lines.append(
                f"| L{layer}:F{idx} | {pos} | {sn_label} | {ai_label} | {fnz_str} | [view]({url}) |"
            )
        lines.append("")

    # --- Connectivity (from BUILD edges) ---
    if pinned_edges:
        lines.append("## Pinned Connectivity")
        lines.append("")
        lines.append("Edges among pinned features as recorded in BUILD. Direction: `from` → `to` (upstream → downstream). Topology only. Edges denote a positive direct_effect connection between the two supernodes during tracing.")
        lines.append("")
        lines.append("| From | To |")
        lines.append("|------|----|")
        for e in pinned_edges:
            src = e.get("from") or e.get("source") or "?"
            dst = e.get("to") or e.get("target") or "?"
            lines.append(f"| {src} | {dst} |")
        lines.append("")

    # --- Oracle judgment (verbatim), the source of truth for classification ---
    lines.append("## Oracle Judgment (verbatim)")
    lines.append("")
    lines.append("The Oracle applies the answer-presence judge to each intervention in this narrative. Prompts are narrowly framed (numeric, yes/no, 'name one'); a `win` is when the required answer (or a directional approximation of it) leaks into the output, fluent and plausibly grounded, even if a suppression scaffold remains around it. `softened` = output shifted but no sign of the answer; suppression still gating in a different surface form. `no-shift` = unchanged or degenerate. Outcome ordering: `win > softened > no-shift` (with `degenerate` as a prose qualifier on no-shift when fluency broke). This narrative is the authoritative classification. See the All Interventions section below for raw before/after data.")
    lines.append("")
    lines.append(_strip_emoji(oracle_response) or "_no oracle response captured_")
    lines.append("")

    # --- All interventions, raw, in run order ---
    if interventions:
        lines.append("## All Interventions (raw, in run order)")
        lines.append("")
        lines.append("Every intervention call with its hypothesis and before/after answer. The Oracle's narrative above classifies these; this section is the underlying data.")
        lines.append("")
        for i, e in enumerate(interventions):
            block = e["intervention"]
            src_tag = f"  _[{e.get('source')}]_" if e.get("source") else ""
            lines.append(f"### {i + 1}. factor={block.get('scale')}, {_format_features_short(block)}{src_tag}")
            lines.append("")
            hyp = (e.get("hypothesis") or "").strip()
            if hyp:
                lines.append(f"**Hypothesis:** {hyp}")
                lines.append("")
            before_body = _strip_emoji((e.get("answer_before") or "").strip())
            after_body = _strip_emoji((e.get("answer_after") or "").strip())
            before_fence = _fence_for(before_body)
            after_fence = _fence_for(after_body)
            lines.append("**Before:**")
            lines.append("")
            lines.append(before_fence)
            lines.append(before_body)
            lines.append(before_fence)
            lines.append("")
            lines.append("**After:**")
            lines.append("")
            lines.append(after_fence)
            lines.append(after_body)
            lines.append(after_fence)
            lines.append("")

    with open(os.path.join(exp_dir, "elicitation.md"), "w") as f:
        f.write("\n".join(lines))


def _summarize_self_rating(self_rating: dict | None) -> int | None:
    """Reduce the multi-sample self-rating distribution to a single 0-10 integer.

    Returns the median of parseable scores, or None if nothing parseable.
    """
    if not self_rating:
        return None
    scores = [s for s in (self_rating.get("scores") or []) if s is not None]
    if not scores:
        return None
    import statistics as _stats
    return int(round(_stats.median(scores)))


def save_run_results(result: dict, config, prompt: str, base_dir: str = ".", full_response: str = "",
                     control_results: list[dict] | None = None,
                     self_rating: dict | None = None,
                     interventions: list[dict] | None = None) -> str:
    """Save oracle results to an experiment directory.

    Creates: exp-{prefix}-{name}/{orch_short}_{sub_short}_{timestamp}[_pass{N}]/
    With: oracle_result.json, circuit.svg, report.md, elicitation.json, elicitation.md

    Args:
        result: Dict from run_circuit_oracle (response, tool_calls, usage, turns).
        config: RunConfig instance.
        prompt: The formatted prompt string (for SVG).
        base_dir: Base directory for experiment dirs.
        full_response: The base model's raw generated response.
        control_results: List of dicts from run_control_analysis (Oracle-without-tools).
        self_rating: Dict from run_self_rating (subject model "are you sure?" confidence).
        interventions: List of intervention records produced during VERIFY.

    Returns:
        Path to the created experiment directory.
    """
    control_results = control_results or []
    interventions = interventions or []
    orch_short = shorten_model_name(config.orchestrator_model)
    sub_short = shorten_model_name(config.subagent_model)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S")

    question_suffix = "-question" if config.question else ""
    # A repeat pass stamps its index into the leaf name. Without it the only
    # discriminator between the 5 arm-1 passes is a second-resolution timestamp,
    # so a crashed-and-retried pass leaves a sixth sibling that nothing marks as
    # a retry and a glob-and-average folds six runs into a "mean over 5". Absent
    # on single-pass runs, which keeps the legacy layout unchanged.
    pass_index = getattr(config, "pass_index", None)
    pass_suffix = f"_pass{pass_index}" if pass_index is not None else ""
    exp_dir = os.path.join(
        base_dir,
        "exp",
        f"exp-{config.experiment_prefix}-{config.prompt_name}{question_suffix}",
        f"{orch_short}_{sub_short}_{timestamp}{pass_suffix}",
    )
    os.makedirs(exp_dir, exist_ok=True)

    # --- Harness grader ---
    # Re-rank interventions with a fresh-context oracle-model grader. The grader picks
    # the single submitted intervention (the oracle self-ranking is gone). Returns
    # (None, None) only when there are no interventions to grade.
    grader_ranking, grader_usage = grade_interventions(interventions, config, full_response)

    # --- Compute costs ---
    usage = result["usage"]
    if grader_usage:
        usage["grader"] = grader_usage
    orch_cost = compute_cost(usage.get("orchestrator", {}))
    sub_costs = [compute_cost(s) for s in usage.get("subagents", [])]
    grader_cost = compute_cost(usage.get("grader", {})) if "grader" in usage else None
    known_costs = [c for c in [orch_cost, grader_cost] + sub_costs if c is not None]
    total_cost = sum(known_costs) if known_costs else None

    self_rating_confidence = _summarize_self_rating(self_rating)

    # --- oracle_result.json ---
    json_result = {
        "prompt_name": config.prompt_name,
        "system_prompt": config.system_prompt,
        "user_message": config.user_message,
        "assistant_prefix": config.assistant_prefix,
        "full_response": full_response,
        "question": config.question,
        "orchestrator_model": config.orchestrator_model,
        "subagent_model": config.subagent_model,
        "provider": config.provider,
        # Run identity (ablation grid) + the exact orchestrator prompt the run
        # was driven by. An earlier probe prompt had to be reconstructed by
        # blob-level git archaeology because nothing persisted it, and these
        # four keys close that gap. All None/absent on legacy runs.
        "task": result.get("task") or getattr(config, "task", None),
        "arm": getattr(config, "arm", None),
        # Which repeat pass this run is. None on single-pass and legacy runs.
        "pass_index": pass_index,
        "mode": result.get("mode"),
        "orchestrator_system_prompt": result.get("system_prompt_resolved"),
        "response": result["response"],
        "tool_calls": result["tool_calls"],
        "usage": result["usage"],
        "total_cost_usd": total_cost,
        "turns": result["turns"],
        "elapsed_seconds": result.get("elapsed_seconds"),
        "control_results": [
            {
                "response": cr.get("response", ""),
                "usage": cr.get("usage"),
                "cost_usd": cr.get("cost_usd"),
                "elapsed_seconds": cr.get("elapsed_seconds"),
            }
            for cr in control_results
        ],
        "self_rating_confidence": self_rating_confidence,
        "self_rating_raw": self_rating,
        "interventions": interventions,
        # Part B (huge-refactor.md): ungraded causal-by-default discovery log. One row per
        # discovery-time causal hit (feature whose scale=-1 ablation shifted the output),
        # with oracle_pinned / became_win = null (joined to pins + final win/softened ranking
        # post-hoc by the analysis script).
        "discovery_reassess": result.get("discovery_reassess", []),
        # Committed ANCHOR reassess triple-labels (with pre_label + 3-way divergence),
        # accumulated on ctx by batched_anchor_sweep and returned raw (tuple-keyed) by the
        # orchestrator. Encode the (layer, feature_idx, pos) tuple keys to strings here (the
        # same _encode_reassess_key the documented save_oracle_result uses) so this is the
        # canonical top-level field rather than only the verbatim copy buried in tool_calls.
        "reassess_records": {
            _encode_reassess_key(k): v
            for k, v in (result.get("reassess_records") or {}).items()
        },
        "timestamp": timestamp,
    }
    with open(os.path.join(exp_dir, "oracle_result.json"), "w") as f:
        json.dump(json_result, f, indent=2, default=str)

    # --- pinned_ids.json (Neuronpedia-style IDs from the BUILD circuit) ---
    pinned_ids = _extract_pinned_ids(result["tool_calls"])
    with open(os.path.join(exp_dir, "pinned_ids.json"), "w") as f:
        json.dump({"pinnedIds": pinned_ids}, f, indent=2)

    # --- elicitation.json + elicitation.md (pinned features + raw interventions + ANALYZE verbatim) ---
    write_elicitation_outputs(
        exp_dir,
        prompt=config.user_message,
        baseline_answer=full_response,
        interventions=interventions,
        oracle_response=result.get("response", ""),
        tool_calls=result.get("tool_calls", []),
        neuronpedia_model_id=getattr(config, "neuronpedia_model_id", "qwen3-4b"),
        neuronpedia_sae_id=getattr(config, "neuronpedia_sae_id", "{layer}-transcoder-hp"),
        grader_ranking=grader_ranking,
    )

    # --- circuit.svg ---
    attr_data = build_attribution_data(result["tool_calls"])
    if attr_data:
        short_prompt = prompt
        if "<|im_start|>user\n" in short_prompt:
            parts = short_prompt.split("<|im_start|>user\n")
            if len(parts) > 1:
                short_prompt = parts[1].split("<|im_end|>")[0].strip()

        # Non-fatal on purpose (2026-07-28). circuit.svg is a picture; report.md
        # below is the artifact the eval scripts actually read, and
        # oracle_result.json is already on disk by this point. Letting a viz bug
        # propagate produced the worst possible outcome: the run was marked
        # FAILED, yet item_done() saw oracle_result.json and counted it complete,
        # so a resume skipped a directory that had no report.md. That is a silent
        # hole in the grid. Losing the drawing is cheap, losing the data is not.
        try:
            svg = create_circuit_svg(
                attr_data["circuit_data"],
                attr_data["top_logits"],
                attr_data["feature_labels"],
                short_prompt,
            )
            with open(os.path.join(exp_dir, "circuit.svg"), "w") as f:
                f.write(svg)
        except Exception as e:
            # Loud in the run log, and leaves a breadcrumb next to the artifacts
            # so a missing circuit.svg is never mistaken for "no circuit data".
            print(f"WARNING: circuit.svg generation failed ({type(e).__name__}: {e}); "
                  f"continuing so report.md is still written")
            with open(os.path.join(exp_dir, "circuit_svg_error.txt"), "w") as f:
                f.write(f"{type(e).__name__}: {e}\n")

    # --- report.md ---
    report = _build_report(
        result, config, full_response, control_results,
        grader_ranking=grader_ranking,
        neuronpedia_model_id=getattr(config, "neuronpedia_model_id", "qwen3-4b"),
        neuronpedia_sae_id=getattr(config, "neuronpedia_sae_id", "{layer}-transcoder-hp"),
    )
    with open(os.path.join(exp_dir, "report.md"), "w") as f:
        f.write(report)

    print(f"Results saved to {exp_dir}/")
    return exp_dir


def _build_report(result: dict, config, full_response: str = "", control_results: list[dict] | None = None,
                  grader_ranking: list[dict] | None = None,
                  neuronpedia_model_id: str = "qwen3-4b",
                  neuronpedia_sae_id: str = "{layer}-transcoder-hp") -> str:
    """Build a markdown report from oracle results."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    # Extract top predictions from tool calls
    top_preds = ""
    for tc in result["tool_calls"]:
        if tc["tool"] == "get_top_logits":
            preds = ", ".join(
                f'{e["token"]} ({e["probability"]*100:.1f}%)'
                for e in tc["output"][:5]
            )
            top_preds = preds
            break

    # Build usage table
    usage = result["usage"]
    usage_rows = []

    def _fmt_cost(c):
        return f"${c:.4f}" if c is not None else "n/a"

    # Orchestrator row
    orch_usage = usage.get("orchestrator", usage)
    orch_cost = compute_cost(orch_usage)
    usage_rows.append(
        f"| Orchestrator | {config.orchestrator_model} "
        f"| {orch_usage.get('input_tokens', 0):,} "
        f"| {orch_usage.get('output_tokens', 0):,} "
        f"| {orch_usage.get('cache_read_input_tokens', 0):,} "
        f"| {orch_usage.get('cache_creation_input_tokens', 0):,} "
        f"| {_fmt_cost(orch_cost)} | n/a | n/a |"
    )

    # Subagent rows
    total_input = orch_usage.get("input_tokens", 0)
    total_output = orch_usage.get("output_tokens", 0)
    total_cache_read = orch_usage.get("cache_read_input_tokens", 0)
    total_cache_write = orch_usage.get("cache_creation_input_tokens", 0)
    total_cost = orch_cost or 0.0
    has_pricing = orch_cost is not None

    # Grader row: present only when the harness grader ran (interventions were graded).
    grader_usage = usage.get("grader")
    if grader_usage:
        grader_cost = compute_cost(grader_usage)
        usage_rows.append(
            f"| Grader | {grader_usage.get('model', config.orchestrator_model)} "
            f"| {grader_usage.get('input_tokens', 0):,} "
            f"| {grader_usage.get('output_tokens', 0):,} "
            f"| {grader_usage.get('cache_read_input_tokens', 0):,} "
            f"| {grader_usage.get('cache_creation_input_tokens', 0):,} "
            f"| {_fmt_cost(grader_cost)} | n/a | fresh-context re-rank |"
        )
        total_input += grader_usage.get("input_tokens", 0)
        total_output += grader_usage.get("output_tokens", 0)
        total_cache_read += grader_usage.get("cache_read_input_tokens", 0)
        total_cache_write += grader_usage.get("cache_creation_input_tokens", 0)
        if grader_cost is not None:
            total_cost += grader_cost
        else:
            has_pricing = False

    # Build outcome map from tool_calls for subagent rows
    subagent_outcomes: dict[str, str] = {}
    for tc in result["tool_calls"]:
        if tc["tool"] == "trace_path_subagent":
            sa_label = tc.get("label", "")
            out = tc["output"]
            if "error" in out:
                subagent_outcomes[sa_label] = "❌ error"
            elif "warning" in out:
                tlog = out.get("trace_log", [])
                subagent_outcomes[sa_label] = f"❌ no report ({len(tlog)} calls)"
            else:
                nf = len(out.get("discovered_features", []))
                ne = len(out.get("discovered_edges", []))
                subagent_outcomes[sa_label] = f"✅ {nf}F/{ne}E"

    for i, sub in enumerate(usage.get("subagents", []), 1):
        sub_cost = compute_cost(sub)
        sa_label = sub.get("label", f"SA-{i}")
        outcome = subagent_outcomes.get(sa_label, "n/a")
        obj = sub.get("objective", "")
        obj_short = (obj[:60] + "…") if len(obj) > 60 else obj
        usage_rows.append(
            f"| {sa_label} | {sub.get('model', config.subagent_model)} "
            f"| {sub.get('input_tokens', 0):,} "
            f"| {sub.get('output_tokens', 0):,} "
            f"| {sub.get('cache_read_input_tokens', 0):,} "
            f"| {sub.get('cache_creation_input_tokens', 0):,} "
            f"| {_fmt_cost(sub_cost)} "
            f"| {outcome} "
            f"| {obj_short} |"
        )
        total_input += sub.get("input_tokens", 0)
        total_output += sub.get("output_tokens", 0)
        total_cache_read += sub.get("cache_read_input_tokens", 0)
        total_cache_write += sub.get("cache_creation_input_tokens", 0)
        if sub_cost is not None:
            total_cost += sub_cost
        else:
            has_pricing = False

    total_cost_str = _fmt_cost(total_cost) if has_pricing else "n/a"
    usage_rows.append(
        f"| **Total** | "
        f"| **{total_input:,}** "
        f"| **{total_output:,}** "
        f"| **{total_cache_read:,}** "
        f"| **{total_cache_write:,}** "
        f"| **{total_cost_str}** | | |"
    )

    usage_table = "\n".join(usage_rows)

    # Add footnote if any model is non-Anthropic (costs are estimates)
    # Major providers with stable, well-defined pricing
    _STABLE_PREFIXES = ("claude-", "anthropic/", "google/", "openai/")
    all_models = [orch_usage.get("model", "")] + [
        s.get("model", "") for s in usage.get("subagents", [])
    ]
    has_community_model = any(
        m and not any(m.startswith(p) for p in _STABLE_PREFIXES)
        for m in all_models
    )
    cost_footnote = ""
    if has_community_model:
        cost_footnote = (
            "\n> **Note:** Costs for community/open models are estimates based on "
            "OpenRouter listed rates and may differ from actual provider charges.\n"
        )

    # Question line (only for question-directed runs)
    question_line = ""
    if config.question:
        question_line = f'\n**Question:** "{config.question}"'

    # Elapsed time
    elapsed = result.get("elapsed_seconds")
    if elapsed is not None:
        mins, secs = divmod(int(elapsed), 60)
        elapsed_line = f"\n**Oracle wall-clock time:** {mins}m {secs}s"
    else:
        elapsed_line = ""

    # Full response section
    response_line = ""
    if full_response:
        response_line = f'\n\n**Model response:** "{full_response}"'

    # Control analysis section (Oracle-without-tools)
    control_results = control_results or []
    control_section = ""
    if control_results:
        control_section = "\n\n## Control Analysis (No Circuit Access)\n"
        control_section += "\nThe Oracle judges the input/output text without any circuit tools. It can usually classify the refusal from surface clues, but cannot causally test reversal.\n"
        if len(control_results) > 1:
            control_section += f"\n**{len(control_results)} independent runs:**\n\n"
            control_section += "| Run | Verdict | Cost | Elapsed |\n"
            control_section += "|-----|---------|------|--------|\n"
            for i, cr in enumerate(control_results):
                resp = cr.get("response", "") or ""
                verdict = "n/a"
                for line in resp.split("\n"):
                    low = line.lower()
                    if "verdict" in low and ":" in line:
                        verdict = line.split(":", 1)[-1].strip().strip("*").strip()
                        break
                elapsed_s = cr.get("elapsed_seconds")
                elapsed_str = f"{int(elapsed_s)}s" if elapsed_s else "n/a"
                cr_cost = cr.get("cost_usd")
                cr_cost_str = f"${cr_cost:.4f}" if cr_cost is not None else "n/a"
                control_section += f"| {i+1} | {verdict[:80]} | {cr_cost_str} | {elapsed_str} |\n"
            control_section += "\n"
            ctrl_costs = [cr.get("cost_usd") for cr in control_results if cr.get("cost_usd") is not None]
            if ctrl_costs:
                control_section += f"**Total control cost:** ${sum(ctrl_costs):.4f}\n"
            for i, cr in enumerate(control_results):
                control_section += f"<details>\n<summary><b>Run {i+1}</b></summary>\n\n"
                control_section += cr.get("response", "") + "\n\n</details>\n\n"
        else:
            control_section += "\n" + control_results[0].get("response", "")

    process_trace = _build_process_trace(result)

    # Strip duplicate heading from start of oracle response (e.g. "## Final Analysis")
    # Also strip emoji characters that may not render properly
    oracle_response = _strip_emoji(result["response"].lstrip("\n"))
    for heading in ("## Final Analysis", "## Analysis", "## Oracle Analysis"):
        if oracle_response.startswith(heading):
            oracle_response = oracle_response[len(heading):].lstrip("\n")
            break

    # Grader Top Pick section (Edit 1b): the fresh-context oracle-model grader's
    # highest-overall intervention, which demotes the inline self-ranking. Empty
    # string when the harness grader did not run.
    grader_section = ""
    if grader_ranking:
        top = next((g for g in grader_ranking if g.get("top1")), None)
        if top is not None:
            ov = top.get("overall")
            ov_str = f"{ov:.2f}" if isinstance(ov, (int, float)) else "n/a"
            grader_section = (
                "\n## Grader Top Pick (fresh-context, oracle model)\n\n"
                "Selected by re-grading every intervention in an independent fresh context "
                "(this demotes the inline end-of-run self-ranking, which is emitted at the "
                "tail of a long transcript). Scored on the shared judge rubric.\n\n"
                f"- **Intervention:** `{top.get('intervention_id')}` (run rank {top.get('rank')})\n"
                f"- **Grader overall:** {ov_str} "
                f"(usability {top.get('usability')}, plausibility {top.get('plausibility')})\n"
            )

    # Circuit Links section: per-feature Neuronpedia URLs for every pinned feature.
    pinned_features, _ = _collect_pinned_features(result.get("tool_calls", []))
    circuit_links = ""
    if pinned_features:
        clines = ["## Circuit Links", ""]
        clines.append("Neuronpedia dashboards for each pinned feature.")
        clines.append("")
        clines.append("| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |")
        clines.append("|---------|-----|----------------|------------------|-------------|")
        for f in pinned_features:
            layer = f["layer"]; idx = f["feature_idx"]; pos = f["pos"]
            if layer is None or idx is None:
                continue
            link = feature_link(layer, idx, model_id=neuronpedia_model_id, sae_template=neuronpedia_sae_id)
            ai_label = (f.get("autointerp") or "n/a").replace("|", "\\|")
            sn_label = (f.get("supernode_label") or "n/a").replace("|", "\\|")
            clines.append(f"| {link} | {pos} | {sn_label} | {ai_label} | [view]({feature_url(layer, idx, model_id=neuronpedia_model_id, sae_template=neuronpedia_sae_id)}) |")
        clines.append("")
        circuit_links = "\n".join(clines) + "\n"

    return f"""# Circuit Oracle Report
**Date:** {timestamp} | **Orchestrator:** {config.orchestrator_model} | **Subagent:** {config.subagent_model}

## Input

**Prompt:** "{config.user_message}"

**System prompt:** "{config.system_prompt}"
{question_line}

**Top predictions:** {top_preds}
{response_line}

## Oracle Analysis

{oracle_response}
{grader_section}
{circuit_links}{process_trace}
## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
{usage_table}
{cost_footnote}{elapsed_line}{control_section}"""
