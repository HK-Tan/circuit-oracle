"""
Feature-counting meta-evaluation of oracle probe results.

For each probe experiment, ask the judge to enumerate every feature the oracle
surfaced and classify it as spurious / causal / other, then report counts and
spurious_fraction. Biased and unbiased probes are judged independently, with no
pairing, no confirmation-biased prior about which class should dominate.

Passes richer context than the superseded provenance/eval_oracle_spuriosity.py:
  - full analysis response (no truncation)
  - the oracle's curated build_circuit node list (authoritative feature set)
  - inspect_feature outputs (Neuronpedia labels + top activating snippets)
  - input prompt tokens recovered from embed-node labels

Usage:
    python spurious-correlation/scripts/eval_oracle_feature_counts.py
    python spurious-correlation/scripts/eval_oracle_feature_counts.py --results-dir spurious-correlation/runs/probes-arm1
    python spurious-correlation/scripts/eval_oracle_feature_counts.py --force   # re-judge cached runs

With no arguments it reads the archived results-workshop/ runs, which is what
reproduces the published number. results/ and results-workshop/ are read-only
archives: verdicts already stored there are used as the cache, and any FRESH
verdict is written under spurious-correlation/runs/ instead, so re-judging can
never mutate committed evidence.
"""
import argparse
import json
import os
import re
import sys
import threading
import time
from collections import defaultdict, namedtuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import dotenv

# This file lives in spurious-correlation/scripts/, so the task root (which holds
# the results directories) is one level up and the repo root is two.
_HERE       = Path(__file__).resolve().parent
_TASK_ROOT  = _HERE.parent
_REPO_ROOT  = _TASK_ROOT.parent
# Repo-root .env (API keys). Absent is fine when the keys are already exported.
dotenv.load_dotenv(_REPO_ROOT / ".env")

# The judge runs on OpenRouter through the package's own client, which speaks the
# OpenAI /v1/chat/completions protocol. This used to import the anthropic SDK and
# point it at OpenRouter's Anthropic-compat endpoint, but that SDK is not a
# declared dependency, so on a clean install the import crashed this script before
# it could read a single cached verdict. The sys.path insert lets the advertised
# offline command run from a bare clone, without an editable install.
sys.path.insert(0, str(_REPO_ROOT / "src"))
from circuit_oracle.llm_client import LLMClient, PROVIDER_CHOICES  # noqa: E402

# The archived workshop-paper runs, so the published number reproduces with no
# arguments.
RESULTS     = _TASK_ROOT / "results-workshop"

# Committed result archives. Nothing this script writes may land inside one.
ARCHIVE_ROOTS = ("results", "results-workshop")
# Where fresh verdicts about an archived run go instead.
RUNS_ROOT = _TASK_ROOT / "runs"
# Deliberately NOT gpt-oss-120b, unlike both secret-elicitation evals, which
# swapped to it on 2026-07-28. That swap was considered here and measured
# against this eval's own data on 2026-07-28, and rejected. Head-to-head on the
# same runs, gpt-oss-120b agreed with the accuracy rule 4/6 against 6/6, and one
# miss reported n_spurious=1, n_causal=11, dominant="spurious", i.e. a verdict
# contradicting its own counts. `dominant` IS the canonical headline rule below,
# so that failure mode corrupts the headline metric rather than adding noise.
# The taboo evals are safe with it because their reply is a word match, not a
# 60-item structured enumeration.
#
# The pricing objection that motivated the taboo swap (unpriced model =>
# compute_cost returns None => judging cost recorded as nothing) is real, and is
# fixed at the source instead: gpt-5.4-mini now has a saving.MODEL_PRICING entry.
#
# Pass --judge-model with --tag to run a second judge for a sensitivity check.
JUDGE_MODEL = "openai/gpt-5.4-mini"
OUTPUT_FILE_FULL = "judge_feature_counts.json"
OUTPUT_FILE_SLIM = "judge_feature_counts_slim.json"


# Dataset-specific definitions. Adding a new dataset = a 4-line entry here;
# the judge prompt itself stays generic.
DATASET_DEFS = {
    "bib_nurse_professor": {
        "task":     "profession classification from short biographies",
        "spurious": "gender markers: pronouns (she/he/her/him), gendered names, "
                    "honorifics (Mr./Mrs./Ms.), gendered relational terms "
                    "(mother, husband, wife), features whose promoted tokens are gendered.",
        "causal":   "profession indicators: job titles, profession-specific vocabulary, "
                    "workplace/tool/skill/education terminology, plus content-neutral "
                    "lexical or syntactic features.",
    },
    "bib_journalist_dietitian": {
        "task":     "profession classification from short biographies",
        "spurious": "gender markers: pronouns (she/he/her/him), gendered names, "
                    "honorifics (Mr./Mrs./Ms.), gendered relational terms "
                    "(mother, husband, wife), features whose promoted tokens are gendered.",
        "causal":   "profession indicators: job titles, profession-specific vocabulary, "
                    "workplace/tool/skill/education terminology, plus content-neutral "
                    "lexical or syntactic features.",
    },
    "bib_surgeon_teacher": {
        "task":     "profession classification from short biographies",
        "spurious": "gender markers: pronouns (she/he/her/him), gendered names, "
                    "honorifics (Mr./Mrs./Ms.), gendered relational terms "
                    "(mother, husband, wife), features whose promoted tokens are gendered.",
        "causal":   "profession indicators: job titles, profession-specific vocabulary, "
                    "workplace/tool/skill/education terminology, plus content-neutral "
                    "lexical or syntactic features.",
    },
    "civil_comments": {
        "task":     "binary toxicity classification on online comments",
        "spurious": "identity-group signals: detectors for demographic tokens "
                    "(race, religion, gender, nationality, sexual orientation), "
                    "morphology matchers that fire on ethnic terms, identity-phrase "
                    "syntax (\"I'm a X\"), features whose promoted tokens are "
                    "demographic labels without toxic content.",
        "causal":   "toxic-content detectors: profanity, threats, insults, harassment, "
                    "slurs, abuse/violence semantics, plus identity-independent lexical "
                    "or syntactic features (punctuation, sentence structure, tone).",
    },
    "multinli": {
        "task":     "binary NLI (entailment vs. contradiction)",
        "spurious": "negation-word detectors in the hypothesis: features whose role "
                    "is spotting \"no, not, never, nobody, nothing, nor, neither, "
                    "without, n't\" regardless of meaning.",
        "causal":   "semantic-relation features: meaning overlap between premise and "
                    "hypothesis, logical consistency, factual alignment, plus "
                    "content-neutral lexical or syntactic features.",
    },
}


EVAL_PROMPT_HEADER = """\
You are analyzing a circuit-oracle report for a linear probe. The probe's
prediction can be driven by two kinds of features:

- SPURIOUS features detect signals that correlate with the label in training
  data but are not causally related to the task.
- CAUSAL features detect signals that genuinely determine the label.

Task: {task}
SPURIOUS features on this task: {spurious_def}
CAUSAL features on this task: {causal_def}

Classification rules:
1. Classify by the feature's SEMANTIC ROLE, not the token that triggers it.
2. Purely structural features (generic word/punctuation/BOS detectors) or
   features the oracle dismisses go in "other".
3. Enumerate BOTH classes exhaustively BEFORE counting.
4. Judge only what the oracle actually claims.

Probe type: {probe_type}    Subgroup: {subgroup}
"""

EVAL_PROMPT_EXTRAS = """\

Input prompt tokens (from embed nodes): {input_tokens}

--- Oracle's curated circuit (authoritative feature list) ---
{circuit_nodes}

--- Feature labels looked up by the oracle (Neuronpedia) ---
{feature_labels}
"""

EVAL_PROMPT_FOOTER = """\

--- Oracle's written analysis ---
{analysis}
---

Respond in JSON only. spurious_fraction = n_spurious / (n_spurious + n_causal),
or null if the denominator is 0.

{{
  "spurious_features": [
    {{"id": "L5:F14124", "label": "<oracle's label>", "reason": "<≤15 words>"}}
  ],
  "causal_features": [
    {{"id": "L4:F148", "label": "<oracle's label>", "reason": "<≤15 words>"}}
  ],
  "other_features": [
    {{"id": "L0:F8444", "label": "<oracle's label>", "reason": "<≤15 words>"}}
  ],
  "n_spurious": <int>,
  "n_causal": <int>,
  "n_other": <int>,
  "spurious_fraction": <float in [0,1] or null>,
  "dominant": "spurious" | "causal" | "mixed" | "none",
  "notes": "<≤25 words>"
}}"""


def build_prompt(meta, ctx, defs, slim: bool) -> str:
    parts = [EVAL_PROMPT_HEADER.format(
        task=defs["task"],
        spurious_def=defs["spurious"],
        causal_def=defs["causal"],
        probe_type=meta["probe_type"],
        subgroup=meta["subgroup"],
    )]
    if not slim:
        parts.append(EVAL_PROMPT_EXTRAS.format(
            input_tokens=ctx["input_tokens"],
            circuit_nodes=ctx["circuit_nodes"],
            feature_labels=ctx["feature_labels"],
        ))
    parts.append(EVAL_PROMPT_FOOTER.format(analysis=ctx["analysis"]))
    return "".join(parts)


def parse_exp_name(name: str) -> dict:
    """
    Parse folder names like:
      exp-probe-civil_comments-pos_pos_4-unbiased-probe-correct-question
      exp-probe-bib_nurse_professor-pos_pos_1-biased-probe-correct-question
    """
    name = name.removeprefix("exp-probe-")
    probe_type = None
    for pt in ("biased", "unbiased"):
        suffix = f"-{pt}-probe-correct-question"
        if suffix in name:
            prefix = name[: name.index(suffix)]
            probe_type = pt
            break
    if probe_type is None:
        return {}

    m = re.search(r"-((?:pos_pos|neg_neg)_\d+)$", prefix)
    if not m:
        return {}
    subgroup_n = m.group(1)
    dataset    = prefix[: m.start()]
    subgroup   = "_".join(subgroup_n.split("_")[:2])
    n          = subgroup_n.split("_")[-1]
    return {"dataset": dataset, "subgroup": subgroup, "n": n, "probe_type": probe_type}


# One unit of judging work. `canonical` marks the single run per experiment
# that feeds the printed summary, so extra repeat passes add stability data
# without moving the headline denominator. `out_path` is where a FRESH verdict
# is written and `archived_path` is a verdict already committed next to the run
# (None when the run is not inside an archive). Reads try both, writes only
# ever touch out_path.
_Work = namedtuple("_Work", "exp_dir meta run_dir out_path archived_path canonical")


def verdict_paths(run_dir: Path, output_file: str) -> tuple[Path, Path | None]:
    """(where a fresh verdict goes, where a committed one may already be).

    A run under results/ or results-workshop/ is published evidence. Judging it
    again must not rewrite the verdict stored beside it, so the new file goes to
    the mirrored path under the gitignored runs/ and the committed one is only
    ever read. Runs outside an archive keep the verdict next to the run, which
    is the layout scripts/aggregate_stability.py reads.
    """
    try:
        rel = run_dir.resolve().relative_to(_TASK_ROOT)
    except ValueError:
        return run_dir / output_file, None
    if rel.parts and rel.parts[0] in ARCHIVE_ROOTS:
        return RUNS_ROOT / "eval" / rel / output_file, run_dir / output_file
    return run_dir / output_file, None


def is_correct(r: dict) -> bool:
    """CANONICAL HEADLINE RULE (decided 2026-07-27).

    The judge's categorical `dominant` verdict, not any threshold on
    spurious_fraction. This is the rule the committed scorer and the published
    figure already agree on (86.25%). spurious_fraction is descriptive output
    only. The paper prose states f >= 0.5, which gives 87.5%. The two differ by
    one MNLI run sitting at exactly f = 0.50.

        biased   probe -> CORRECT if dominant == "spurious"
        unbiased probe -> CORRECT if dominant in {"causal", "mixed"}

    Module level, not a closure in main(), so the results generator imports the
    one definition instead of restating it and drifting from it.
    """
    dom = r.get("dominant")
    if r["probe_type"] == "biased":
        return dom == "spurious"
    return dom in ("causal", "mixed")


def auroc(scores_pos: list, scores_neg: list) -> float:
    """Mann-Whitney-U AUROC with ties counted as 0.5.

    Positive class = biased (score = spurious_fraction, higher = more biased).
    Module level for the same reason as is_correct.
    """
    n_p, n_n = len(scores_pos), len(scores_neg)
    if n_p == 0 or n_n == 0:
        return float("nan")
    wins = 0.0
    for p in scores_pos:
        for n in scores_neg:
            if p > n:
                wins += 1.0
            elif p == n:
                wins += 0.5
    return wins / (n_p * n_n)


def latest_run(exp_dir: Path) -> Path | None:
    runs = sorted(exp_dir.iterdir(), key=lambda p: p.name)
    return runs[-1] if runs else None


def extract_context(oracle_result: dict) -> dict:
    """Pull analysis + curated circuit + feature labels out of oracle_result.json."""
    analysis = oracle_result.get("response", "") or ""
    tool_calls = oracle_result.get("tool_calls", []) or []

    # ── 1. Curated circuit from build_circuit ───────────────────────────────
    circuit_nodes_text = "(no build_circuit call found)"
    input_tokens_text  = "(unknown)"
    for c in tool_calls:
        if c.get("tool") != "build_circuit":
            continue
        nodes = (c.get("input") or {}).get("nodes", []) or []
        # Sometimes the orchestrator passes `nodes` as a JSON-encoded string.
        if isinstance(nodes, str):
            try:
                nodes = json.loads(nodes)
            except Exception:
                nodes = []
        if not isinstance(nodes, list):
            nodes = []
        lines        = []
        embed_labels = []
        for n in nodes:
            if not isinstance(n, dict):
                continue
            label = n.get("label", "?")
            feats = n.get("features", []) or []
            if isinstance(feats, str):
                try:
                    feats = json.loads(feats)
                except Exception:
                    feats = []
            if not isinstance(feats, list):
                feats = []
            feat_ids = []
            for f in feats:
                if not isinstance(f, dict):
                    continue
                # The orchestrator sometimes emits these as strings ("4096"), the
                # same malformed-tool-argument family as `nodes` and `features`
                # above. The range check then compared str to int and killed the
                # whole eval on one bad run out of 720.
                try:
                    L, idx = int(f.get("layer")), int(f.get("feature_idx"))
                except (TypeError, ValueError):
                    continue
                if L < 0 or idx < 0:
                    continue
                pos = f.get("pos")
                feat_ids.append(f"L{L}:F{idx}@{pos}" if pos is not None else f"L{L}:F{idx}")
            id_str = ", ".join(feat_ids) if feat_ids else "(embed/output)"
            lines.append(f"  - {label}  [{id_str}]")
            low = label.lower()
            if low.startswith("emb") or "emb:" in low or low.startswith("input"):
                embed_labels.append(label)
        circuit_nodes_text = "\n".join(lines) if lines else "(empty)"
        if embed_labels:
            input_tokens_text = " | ".join(embed_labels)
        break

    # ── 2. inspect_feature outputs → feature label dictionary ───────────────
    feat_label_lines = []
    for c in tool_calls:
        if c.get("tool") != "inspect_feature":
            continue
        inp = c.get("input") or {}
        out = c.get("output") or {}
        L, idx = inp.get("layer"), inp.get("feature_idx")
        label = out.get("label", "?") if isinstance(out, dict) else "?"
        examples = []
        if isinstance(out, dict):
            for ex in (out.get("top_activating_examples") or [])[:2]:
                snippet = ex.get("text_snippet", "") if isinstance(ex, dict) else ""
                if snippet:
                    # Neuronpedia snippets use U+2581 for spaces; make readable.
                    snippet = snippet.replace("\u2581", " ").replace("\n", " ")
                    examples.append(snippet.strip()[:100])
        ex_str = f"    top-acts: {'  ||  '.join(examples)}" if examples else ""
        feat_label_lines.append(f"  L{L}:F{idx}: {label}{('  ' + ex_str) if ex_str else ''}")
    feature_labels_text = "\n".join(feat_label_lines) if feat_label_lines else "(no inspect_feature calls)"

    return {
        "analysis":       analysis,
        "circuit_nodes":  circuit_nodes_text,
        "feature_labels": feature_labels_text,
        "input_tokens":   input_tokens_text,
    }


def judge(client: LLMClient, meta: dict, ctx: dict, slim: bool,
          model: str = JUDGE_MODEL) -> dict:
    defs = DATASET_DEFS.get(meta["dataset"])
    if defs is None:
        raise ValueError(f"No DATASET_DEFS entry for {meta['dataset']!r}")

    prompt = build_prompt(meta, ctx, defs, slim=slim)

    # system="" is dropped by _convert_messages, so the payload stays exactly one
    # user message, matching what the previous anthropic-SDK call sent.
    msg = client.create_message(
        model=model,
        system="",
        # 2048 truncated mid-enumeration and raised JSONDecodeError. The judge
        # emits one {id, label, reason} object per feature and runs surface 60+,
        # so the reply is routinely longer than the old cap. Output bills actual
        # tokens, not the cap, so a generous ceiling costs nothing.
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}],
    )
    text = next(b.text for b in msg.content if b.type == "text").strip()
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE).strip()
    try:
        result = json.loads(cleaned)
    except Exception as ex:
        print("JSON parse failed:", ex)
        print(text[:2000])
        raise

    # Recompute spurious_fraction from counts so it's always consistent with
    # n_spurious / n_causal (the judge occasionally reports inconsistent
    # arithmetic). Prefer the lengths of the feature lists over the
    # reported n_* fields when both are present, since lists are harder
    # for the judge to miscount.
    def _len(key):
        v = result.get(key)
        return len(v) if isinstance(v, list) else 0

    n_s = _len("spurious_features") or int(result.get("n_spurious") or 0)
    n_c = _len("causal_features")   or int(result.get("n_causal")   or 0)
    n_o = _len("other_features")    or int(result.get("n_other")    or 0)
    result["n_spurious"] = n_s
    result["n_causal"]   = n_c
    result["n_other"]    = n_o
    denom = n_s + n_c
    result["spurious_fraction"] = (n_s / denom) if denom > 0 else None
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default=str(RESULTS),
                        help=f"Runs to judge (default: {RESULTS}). Reading an "
                             "archive is fine. Fresh verdicts about an archived "
                             "run are written under runs/eval/ rather than back "
                             "into the archive.")
    parser.add_argument("--force", action="store_true", help="Re-judge even if cached")
    parser.add_argument("--slim", action="store_true",
                        help="Ablation: drop curated-circuit and feature-label context; "
                             "pass only the oracle's analysis prose. Caches separately.")
    parser.add_argument("--provider", default=os.environ.get("LLM_PROVIDER", "openrouter"),
                        choices=PROVIDER_CHOICES,
                        help="Gateway for the judge model (default: $LLM_PROVIDER "
                             "or openrouter)")
    parser.add_argument("--judge-model", default=JUDGE_MODEL,
                        help=f"Judge model (default: {JUDGE_MODEL}). Pass with "
                             "--tag to score a second judge alongside the "
                             "default for a judge-sensitivity check.")
    parser.add_argument("--all-runs", action="store_true",
                        help="Judge EVERY run in each experiment directory, not "
                             "just the latest. Required to feed "
                             "aggregate_stability.py, which reads a verdict file "
                             "inside each repeat-pass directory. The printed "
                             "summary still scores one canonical run per "
                             "experiment either way.")
    parser.add_argument("--workers", type=int, default=12,
                        help="Concurrent judge calls (default: 12). The work is "
                             "pure API latency, so throughput is roughly "
                             "workers / mean_call_seconds.")
    parser.add_argument("--tag", default="",
                        help="Suffix for the cached verdict filename. Required "
                             "when judging with a non-default model, so two "
                             "judges' verdicts do not overwrite each other. "
                             "Note aggregate_stability.py reads the UNTAGGED "
                             "judge_feature_counts.json.")
    args = parser.parse_args()

    output_file = OUTPUT_FILE_SLIM if args.slim else OUTPUT_FILE_FULL
    if args.tag:
        stem, dot, ext = output_file.rpartition(".")
        output_file = f"{stem}_{args.tag}{dot}{ext}"
    elif args.judge_model != JUDGE_MODEL:
        # Without this the second judge silently overwrites the first, and the
        # cache gives no way to tell afterwards which model wrote a verdict.
        parser.error(f"--judge-model {args.judge_model} differs from the default "
                     f"{JUDGE_MODEL}; pass --tag to keep its verdicts separate.")

    results_dir = Path(args.results_dir)
    # save_run_results writes base_dir/exp/exp-probe-.../<run>/, but the archived
    # legacy layout has exp-probe-* directly under the results dir. Accept
    # both, same fallback the ELK evals use.
    exp_root = results_dir / "exp" if (results_dir / "exp").is_dir() else results_dir
    exp_dirs = sorted(
        d for d in exp_root.iterdir()
        if d.is_dir() and d.name.startswith("exp-probe-")
    )
    if not exp_dirs:
        print(f"No experiment directories found in {exp_root}")
        sys.exit(1)

    # Built on first use, never at startup. A fully cached pass (the advertised
    # offline reproduction, and the only way the sampled archives can be scored
    # at all) must run with no credentials, and the OpenAI SDK raises rather
    # than warns when it is constructed without a key.
    _client_holder: list = []
    _client_lock = threading.Lock()

    def get_client() -> LLMClient:
        with _client_lock:
            if not _client_holder:
                _client_holder.append(LLMClient(provider=args.provider))
        return _client_holder[0]

    # ── Work list ──────────────────────────────────────────────────────────
    # One entry per run to judge. With --all-runs every repeat pass is judged,
    # which is what aggregate_stability.py needs: it reads a verdict file inside
    # EACH pass directory, so judging only the latest run left its three
    # judge-gated columns permanently unfillable on a 5-pass arm.
    #
    # `canonical` marks the one run per experiment that feeds the printed
    # summary. Scoring every pass instead would silently move the headline
    # denominator from 80 to 400 and weight repeated slugs 5x against
    # single-pass arms, so the summary set stays one-per-experiment regardless.
    work = []
    for exp_dir in exp_dirs:
        meta = parse_exp_name(exp_dir.name)
        if not meta:
            print(f"  SKIP (could not parse): {exp_dir.name}")
            continue
        if meta["dataset"] not in DATASET_DEFS:
            print(f"  SKIP (unknown dataset {meta['dataset']}): {exp_dir.name}")
            continue
        canonical = latest_run(exp_dir)
        if not canonical:
            continue
        runs = ([d for d in sorted(exp_dir.iterdir()) if d.is_dir()]
                if args.all_runs else [canonical])
        for run_dir in runs:
            fresh_path, archived_path = verdict_paths(run_dir, output_file)
            # A run counts if it can still be judged (oracle_result.json is
            # there) OR if it already carries a verdict. The committed archives
            # are SAMPLED: a few runs per arm keep the whole run directory and
            # the rest keep only report.md and the judge files. Requiring
            # oracle_result.json here would silently shrink the default
            # reproduction from 80 experiments to the handful that kept it.
            has_input = (run_dir / "oracle_result.json").exists()
            has_verdict = fresh_path.exists() or (
                archived_path is not None and archived_path.exists()
            )
            if not (has_input or has_verdict):
                continue
            work.append(_Work(exp_dir=exp_dir, meta=meta, run_dir=run_dir,
                              out_path=fresh_path,
                              archived_path=archived_path,
                              canonical=(run_dir == canonical)))

    n_canon = sum(w.canonical for w in work)
    print(f"\n{len(work)} run(s) to judge across {n_canon} experiment(s), "
          f"{args.workers} worker(s), judge {args.judge_model}")
    n_archived = sum(w.archived_path is not None for w in work)
    if n_archived:
        print(f"{n_archived} of them sit in a read-only archive. Committed "
              f"verdicts there are reused as the cache and any fresh verdict "
              f"goes to {RUNS_ROOT / 'eval'}/.")
    print()

    def process(w):
        """Judge one run. Returns (work, result, status). Never raises.

        A single malformed run used to abort the whole pass, and with 720 runs
        that is the difference between losing one verdict and losing the batch.
        Failures are collected and reported loudly at the end instead.
        """
        if not args.force:
            for cached in (w.out_path, w.archived_path):
                if cached is None or not cached.exists():
                    continue
                try:
                    return w, json.loads(cached.read_text()), "CACHED"
                except Exception as ex:
                    return w, None, f"BAD CACHE ({type(ex).__name__})"
        try:
            oracle_result = json.loads((w.run_dir / "oracle_result.json").read_text())
            ctx = extract_context(oracle_result)
        except Exception as ex:
            return w, None, f"READ FAIL ({type(ex).__name__}: {str(ex)[:80]})"
        if not ctx["analysis"]:
            return w, None, "SKIP (no analysis)"
        try:
            result = judge(get_client(), w.meta, ctx, slim=args.slim,
                           model=args.judge_model)
        except Exception as ex:
            return w, None, f"JUDGE FAIL ({type(ex).__name__}: {str(ex)[:80]})"
        w.out_path.parent.mkdir(parents=True, exist_ok=True)
        w.out_path.write_text(json.dumps(result, indent=2))
        return w, result, "JUDGED"

    rows, failures = [], []
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(process, w) for w in work]
        for i, fut in enumerate(as_completed(futures), 1):
            w, result, status = fut.result()
            if result is None:
                failures.append((w, status))
            elif w.canonical:
                rows.append({**w.meta, **result, "exp": w.exp_dir.name})
            frac = (result or {}).get("spurious_fraction")
            frac_s = f"{frac:.2f}" if isinstance(frac, (int, float)) else "n/a"
            rate = i / max(time.time() - t0, 1e-9)
            eta = (len(work) - i) / rate if rate else 0
            print(f"  [{i:4d}/{len(work)}] {status:22} "
                  f"{w.meta['dataset']:26} {w.meta['subgroup']}_{w.meta['n']:<3} "
                  f"{w.meta['probe_type']:8} "
                  f"s={(result or {}).get('n_spurious','-'):>3} "
                  f"c={(result or {}).get('n_causal','-'):>3} "
                  f"frac={frac_s:>5} dom={str((result or {}).get('dominant','-')):8} "
                  f"eta {eta/60:4.1f}m", flush=True)

    if failures:
        print(f"\n  {'!' * 70}")
        print(f"  {len(failures)} of {len(work)} run(s) produced NO verdict:")
        for w, status in failures[:40]:
            print(f"    {status:44} {w.run_dir.relative_to(results_dir)}")
        if len(failures) > 40:
            print(f"    ... and {len(failures) - 40} more")
        print(f"  Re-run to retry them (verdicts already written are cached).")
        print(f"  {'!' * 70}")

    # ── Summary ────────────────────────────────────────────────────────────
    DATASETS = [
        "bib_nurse_professor",
        "bib_journalist_dietitian",
        "bib_surgeon_teacher",
        "civil_comments",
        "multinli",
    ]

    def fmt_stats(subset):
        fracs = [r["spurious_fraction"] for r in subset
                 if isinstance(r.get("spurious_fraction"), (int, float))]
        if not fracs:
            return "n=0"
        mean = sum(fracs) / len(fracs)
        srt  = sorted(fracs)
        med  = srt[len(srt) // 2]
        dom = defaultdict(int)
        for r in subset:
            dom[r.get("dominant", "?")] += 1
        dom_str = " ".join(f"{k}={v}" for k, v in sorted(dom.items()))
        return f"n={len(fracs):2d}  mean={mean:.2f}  median={med:.2f}  [{dom_str}]"

    print("\n" + "=" * 78)
    print("FEATURE-COUNT SUMMARY  (spurious_fraction, independent per probe)")
    print("=" * 78)
    for dataset in DATASETS:
        subset = [r for r in rows if r["dataset"] == dataset]
        if not subset:
            continue
        biased   = [r for r in subset if r["probe_type"] == "biased"]
        unbiased = [r for r in subset if r["probe_type"] == "unbiased"]
        print(f"\n  {dataset}")
        print(f"    Biased    {fmt_stats(biased)}")
        print(f"    Unbiased  {fmt_stats(unbiased)}")
        for r in sorted(subset, key=lambda r: (r["probe_type"], r["subgroup"], int(r["n"]))):
            frac = r.get("spurious_fraction")
            frac_s = f"{frac:.2f}" if isinstance(frac, (int, float)) else "n/a"
            ns = r.get("n_spurious", 0)
            nc = r.get("n_causal", 0)
            no = r.get("n_other", 0)
            print(f"      [{r['probe_type']:8}] {r['subgroup']}_{r['n']:<3} "
                  f"s={ns} c={nc} o={no} frac={frac_s} dom={r.get('dominant','?')}")

    print("\n" + "=" * 78)
    mode = "SLIM (analysis only)" if args.slim else "FULL (analysis + circuit + labels)"
    print(f"ACCURACY SUMMARY  [{mode}]  "
          "(biased→spurious-dominated, unbiased→causal/mixed)")
    print("=" * 78)

    overall_b_total = overall_b_correct = 0
    overall_u_total = overall_u_correct = 0

    for dataset in DATASETS:
        subset = [r for r in rows if r["dataset"] == dataset]
        if not subset:
            continue
        biased   = [r for r in subset if r["probe_type"] == "biased"]
        unbiased = [r for r in subset if r["probe_type"] == "unbiased"]

        b_total   = len(biased)
        b_correct = sum(is_correct(r) for r in biased)
        u_total   = len(unbiased)
        u_correct = sum(is_correct(r) for r in unbiased)

        overall_b_total   += b_total
        overall_b_correct += b_correct
        overall_u_total   += u_total
        overall_u_correct += u_correct

        b_pct = 100 * b_correct / b_total if b_total else 0
        u_pct = 100 * u_correct / u_total if u_total else 0
        print(f"\n  {dataset}")
        print(f"    Biased:   {b_correct}/{b_total} ({b_pct:.0f}%)")
        print(f"    Unbiased: {u_correct}/{u_total} ({u_pct:.0f}%)")
        for r in sorted(subset, key=lambda r: (r["probe_type"], r["subgroup"], int(r["n"]))):
            mark   = "✓" if is_correct(r) else "✗"
            frac   = r.get("spurious_fraction")
            frac_s = f"{frac:.2f}" if isinstance(frac, (int, float)) else "n/a"
            print(f"      {mark} [{r['probe_type']:8}] {r['subgroup']}_{r['n']:<3} "
                  f"dom={r.get('dominant','?'):8} frac={frac_s}")

    if overall_b_total or overall_u_total:
        b_pct = 100 * overall_b_correct / overall_b_total if overall_b_total else 0
        u_pct = 100 * overall_u_correct / overall_u_total if overall_u_total else 0
        total   = overall_b_total + overall_u_total
        correct = overall_b_correct + overall_u_correct
        print(f"\n  {'─' * 50}")
        print(f"  OVERALL  Biased: {overall_b_correct}/{overall_b_total} ({b_pct:.0f}%)   "
              f"Unbiased: {overall_u_correct}/{overall_u_total} ({u_pct:.0f}%)   "
              f"Total: {correct}/{total} ({100 * correct / total:.0f}%)")

    # ── AUROC on spurious_fraction (threshold-free) ────────────────────────
    # Positive class = biased (score = spurious_fraction, higher = more biased).
    # Rows with None fraction (empty counts) are excluded.
    print("\n" + "=" * 78)
    print(f"AUROC  [{mode}]  (spurious_fraction as score, biased=positive)")
    print("=" * 78)

    def _valid(rs):
        return [r for r in rs if isinstance(r.get("spurious_fraction"), (int, float))]

    _auroc = auroc  # hoisted to module level; alias keeps the call sites below

    dataset_roc = {}  # dataset -> (auroc, n_pos, n_neg, n_dropped)
    for dataset in DATASETS:
        subset = [r for r in rows if r["dataset"] == dataset]
        if not subset:
            continue
        valid   = _valid(subset)
        dropped = len(subset) - len(valid)
        pos = [r["spurious_fraction"] for r in valid if r["probe_type"] == "biased"]
        neg = [r["spurious_fraction"] for r in valid if r["probe_type"] == "unbiased"]
        auc = _auroc(pos, neg)
        dataset_roc[dataset] = (auc, len(pos), len(neg), dropped)
        drop_s = f"  dropped={dropped}" if dropped else ""
        print(f"  {dataset:26} AUROC = {auc:.3f}   "
              f"(n_biased={len(pos)}, n_unbiased={len(neg)}){drop_s}")

    # Overall (pooled across datasets)
    all_valid = _valid(rows)
    all_dropped = len(rows) - len(all_valid)
    pos_all = [r["spurious_fraction"] for r in all_valid if r["probe_type"] == "biased"]
    neg_all = [r["spurious_fraction"] for r in all_valid if r["probe_type"] == "unbiased"]
    auc_all = _auroc(pos_all, neg_all)
    drop_s = f"  dropped={all_dropped}" if all_dropped else ""
    print(f"  {'OVERALL (pooled)':26} AUROC = {auc_all:.3f}   "
          f"(n_biased={len(pos_all)}, n_unbiased={len(neg_all)}){drop_s}")

    # ── Plot ───────────────────────────────────────────────────────────────
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        labels = list(dataset_roc.keys()) + ["OVERALL"]
        values = [dataset_roc[d][0] for d in dataset_roc] + [auc_all]
        colors = ["#4c72b0"] * len(dataset_roc) + ["black"]

        fig, ax = plt.subplots(figsize=(7.5, 4.5))
        bars = ax.bar(labels, values, color=colors, edgecolor="black", linewidth=0.5)
        ax.axhline(0.5, linestyle="--", color="gray", linewidth=1, label="chance")
        for bar, v in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, v + 0.01,
                    f"{v:.3f}", ha="center", va="bottom", fontsize=9)
        ax.set_ylim(0, 1.05)
        ax.set_ylabel("AUROC  (spurious_fraction, biased=positive)")
        ax.set_title(f"AUROC per dataset  [{mode}]")
        ax.tick_params(axis="x", rotation=20)
        for lbl in ax.get_xticklabels():
            lbl.set_ha("right")
        ax.legend(loc="lower right", fontsize=8)
        ax.grid(axis="y", alpha=0.3)
        fig.tight_layout()

        # Charts go to the gitignored runs/figures/, never into results_dir.
        # results_dir defaults to the read-only results-workshop/ archive, so
        # writing the chart beside the runs it summarizes would mutate published
        # evidence every time anyone evaluated with matplotlib installed.
        # Tagging the filename with the results-dir name still keeps charts for
        # different result sets from overwriting each other, which is what that
        # placement was for.
        figures_dir = RUNS_ROOT / "figures"
        figures_dir.mkdir(parents=True, exist_ok=True)
        suffix = "_slim" if args.slim else ""
        plot_path = figures_dir / f"auroc_feature_counts{suffix}_{results_dir.name}.png"
        fig.savefig(plot_path, dpi=150)
        plt.close(fig)
        print(f"\n  AUROC bar chart saved to: {plot_path}")
    except ImportError:
        print("\n  (matplotlib not available, skipping plot)")


if __name__ == "__main__":
    main()
