#!/usr/bin/env python3
"""
Judge whether a set of SAE/transcoder features contains spurious ones.

Takes the top-N features ranked by EITHER biased or unbiased probe cosine similarity
(from rank_sae_features_by_probe.py), fetches their Neuronpedia descriptions, then
asks an LLM: "Does this feature set contain spurious features?"

The judge sees only the input prompt, the task description, and the features,
it does NOT know whether the features came from a biased or unbiased ranking.

Hypothesis: features ranked by the biased probe should contain spurious ones
(high cos_sim_biased → encodes spurious signal); features ranked by the unbiased
probe should not.

Usage (paths are relative to spurious-correlation/, and the script resolves
globs against it, so it runs the same from either directory):

    python scripts/judge_sae_features.py \\
        --input probe_artifacts/plt_features/bib_journalist_dietitian-pos_pos_1-transcoder.json \\
        --ranking biased

    # Both rankings in one go (saves two result files)
    python scripts/judge_sae_features.py \\
        --input probe_artifacts/plt_features/bib_journalist_dietitian-pos_pos_1-transcoder.json \\
        --ranking both

    # Every SAE ranking file, top 20 features each
    python scripts/judge_sae_features.py \\
        --input 'probe_artifacts/plt_features/bib_*-sae.json' --ranking both --top-n 20

    # Spend Kilo credits instead of OpenRouter ones
    python scripts/judge_sae_features.py --input ... --provider kilo
"""

import argparse
import json
import os
import sys
import threading
import time
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import dotenv
import requests

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# This file lives in spurious-correlation/scripts/, so the task root (which holds
# probe_artifacts/plt_features/, probe_artifacts/sae_features/, probe_artifacts/sae_analysis/) is one level up
# and the repo root is two.
_HERE      = Path(__file__).resolve().parent
_TASK_ROOT = _HERE.parent
_REPO_ROOT = _TASK_ROOT.parent

# Fresh verdicts go under the gitignored runs/, never into the committed
# probe_artifacts/sae_analysis/ archive that the published baseline was read
# from. Override with --out-dir.
DEFAULT_OUT_DIR = _TASK_ROOT / "runs" / "sae_analysis"

# Repo-root .env (API keys). Absent is fine when the keys are already exported.
# Loaded at import time, not inside main(), because argparse evaluates the
# --provider default from LLM_PROVIDER while building the parser: the old
# in-main load ran after parse_args and so could never be seen by that default.
dotenv.load_dotenv(_REPO_ROOT / ".env")

# The judge goes through the package's own client, which speaks the OpenAI
# /v1/chat/completions protocol and reaches every gateway. This file used to
# import the anthropic SDK and point it at OpenRouter's Anthropic-compat
# endpoint, the last place in the repo that did, but that SDK is not a declared
# dependency (see pyproject), so on a clean install the import crashed the
# script outright. The sys.path insert lets it run from a bare clone, without an
# editable install, matching eval_oracle_feature_counts.py.
sys.path.insert(0, str(_REPO_ROOT / "src"))
from circuit_oracle.llm_client import (  # noqa: E402
    LLMClient,
    PROVIDER_CHOICES,
    preflight_providers,
)

NP_MODEL_ID = "gemma-2-2b"
# Neuronpedia dictionary ids, templated on layer (fixed 2026-07-26). These were
# pinned to layer 22 while rank_sae_features_by_probe.py selected CivilComments
# features at layer 12 and MultiNLI at layer 17. Feature indices do NOT transfer
# across dictionaries, so a pinned reader hands the LLM the description of an
# unrelated feature. The layer now comes from the ranking file that produced the
# indices, and a file without one is rejected rather than assumed to be layer 22.
NP_TRANSCODER_SAE_ID_TEMPLATE = "{layer}-gemmascope-transcoder-16k"
NP_SAE_SAE_ID_TEMPLATE        = "{layer}-gemmascope-res-16k"

DEFAULT_TOP_N  = 20
# Corrected 2026-07-28, was "minimax/minimax-m2.7". The probes arms run
# minimax/minimax-m3, and this judge produces the SAE-cos / Trans-cos baseline
# the Oracle is compared against, so a stale default silently scored the two
# sides of the paper's central comparison on different models. Same staleness
# CLAUDE.md flags for the tasks 1 and 2 orchestrator defaults.
DEFAULT_MODEL  = "minimax/minimax-m3"
NP_TIMEOUT     = 15
NP_RETRY_DELAY = 1.0

# One (ranking file, ranking direction) pair. The unit of parallelism: 40
# prompts x 2 dictionary types x 2 rankings = 160 of these in a full re-judge.
_Unit = namedtuple("_Unit", ["path", "ranking"])

# Per-dataset task descriptions and spuriosity concerns (mirrors run_oracle_on_probes.py)
DATASET_CONCERNS = {
    "bib_journalist_dietitian": (
        "binary profession classification (dietitian vs journalist)",
        "The features encode spurious gender markers rather than genuine profession indicators to predict the profession.",
    ),
    "bib_nurse_professor": (
        "binary profession classification (nurse vs professor)",
        "The features encode spurious gender markers rather than genuine profession indicators to predict the profession.",
    ),
    "bib_surgeon_teacher": (
        "binary profession classification (surgeon vs teacher)",
        "The features encode spurious gender markers rather than genuine profession indicators to predict the profession.",
    ),
    "civil_comments": (
        "toxicity classification",
        "The features encode spurious identity-group signals rather than actual toxic content to predict toxicity.",
    ),
    "multinli": (
        "natural language inference (contradiction vs entailment)",
        "The features encode spurious negation-word signals rather than actual semantic contradiction to predict contradiction.",
    ),
}


# ---------------------------------------------------------------------------
# Neuronpedia
# ---------------------------------------------------------------------------

# Process-wide Neuronpedia cache, keyed on the pair that identifies a feature.
# The dictionary id has to be in the key: index 4711 at layer 12 is an unrelated
# feature to index 4711 at layer 22, which is the same confusion the layer fix
# above was about.
#
# This is a pure latency win, not a semantic change. The top-20 sets of the
# biased and the unbiased ranking overlap heavily, and so do different prompts
# from one dataset. Measured on the 160 existing verdict files: 2480 fetches
# collapse to 673 distinct (dict, feature) pairs, a 72.9 percent hit rate.
# Errors are cached too, deliberately, so a feature Neuronpedia does not have is
# not re-requested 3 times by every worker that wants it.
_NP_CACHE: dict[tuple[str, int], dict] = {}
_NP_LOCK = threading.Lock()


def fetch_neuronpedia(feature_idx: int, sae_id: str) -> dict:
    key = (sae_id, feature_idx)
    with _NP_LOCK:
        hit = _NP_CACHE.get(key)
    if hit is not None:
        return hit
    result = _fetch_neuronpedia_uncached(feature_idx, sae_id)
    with _NP_LOCK:
        _NP_CACHE[key] = result
    return result


def _fetch_neuronpedia_uncached(feature_idx: int, sae_id: str) -> dict:
    url = f"https://www.neuronpedia.org/api/feature/{NP_MODEL_ID}/{sae_id}/{feature_idx}"
    for attempt in range(3):
        try:
            resp = requests.get(url, timeout=NP_TIMEOUT)
            if resp.status_code == 429:
                time.sleep(NP_RETRY_DELAY * (attempt + 1))
                continue
            resp.raise_for_status()
            break
        except requests.RequestException as e:
            if attempt == 2:
                return {"error": str(e)}
            time.sleep(NP_RETRY_DELAY)
    else:
        return {"error": "Max retries exceeded"}

    data = resp.json()

    label = "No explanation available"
    if data.get("explanations"):
        label = data["explanations"][0].get("description", label)

    top_examples = []
    for act in (data.get("activations") or [])[:3]:
        tokens = act.get("tokens", [])
        values = act.get("values", [])
        text = "".join(tokens)[:200]
        max_val = max(values) if values else 0
        max_idx = values.index(max_val) if values else 0
        max_token = tokens[max_idx] if max_idx < len(tokens) else ""
        top_examples.append({
            "text_snippet": text,
            "max_activation": round(max_val, 3),
            "max_token": max_token,
        })

    return {
        "feature_idx":             feature_idx,
        "label":                   label,
        "top_activating_examples": top_examples,
        "promoted_tokens":         data.get("pos_str", [])[:10],
        "suppressed_tokens":       data.get("neg_str", [])[:10],
        "frac_nonzero":            data.get("frac_nonzero"),
    }


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------

def select_features(features: list[dict], ranking: str, top_n: int) -> list[dict]:
    """Return top-N features sorted by the chosen ranking key."""
    key = "rank_biased" if ranking == "biased" else "rank_unbiased"
    return sorted(features, key=lambda f: f[key])[:top_n]


SYSTEM_PROMPT = f"""\
You are an interpretability researcher analyzing sparse autoencoder (SAE) features \
from a language model (Gemma-2-2B).

You will be given:
- An input text that was passed through the model
- The task the model is being probed for
- A set of SAE features that were active on this input, along with their \
  Neuronpedia labels and activating examples

Your job is to  determine whether the concern is true.

Respond with:
1. A verdict: YES (spurious features present) or NO (no spurious features)
2. A list of any spurious features identified, with reasoning
3. A brief overall summary
"""


def build_user_prompt(
    prompt: str,
    dataset: str,
    task_desc: str,
    concern: str,
    features_with_np: list[dict],
) -> str:
    lines = [
        f"Input text: {prompt[:400]}",
        f"Task: {task_desc}",
        f"Concern: {concern}",
        "",
        f"Active SAE features ({len(features_with_np)} shown):",
        "",
    ]

    for f in features_with_np:
        np = f.get("neuronpedia", {})
        lines += [
            f"Feature {f['feature_idx']}",
            f"  label:             {np.get('label', 'N/A')}",
            f"  promoted_tokens:   {np.get('promoted_tokens', [])}",
            f"  suppressed_tokens: {np.get('suppressed_tokens', [])}",
        ]
        for ex in np.get("top_activating_examples", []):
            lines.append(
                f"  example [{ex['max_token']!r} @{ex['max_activation']}]: "
                f"{ex['text_snippet'][:120]!r}"
            )
        lines.append("")

    lines.append(
        "Do these features contain spurious ones? "
        "Verdict (YES/NO), list of spurious features with reasoning, and summary."
    )
    return "\n".join(lines)


def run_one(
    input_path: Path,
    ranking: str,
    top_n: int,
    client: LLMClient,
    model: str,
    out_dir: Path | None = None,
    np_workers: int = 8,
    max_tokens: int = 4096,
) -> Path:
    # Every print in here goes through this buffer and is flushed as ONE write at
    # the end. With --workers the old streaming prints interleaved character by
    # character across threads, which made a 160 unit run unreadable and, worse,
    # made a real failure impossible to attribute to a unit.
    log: list[str] = []

    # Save. probe_artifacts/sae_analysis/ holds the committed verdicts behind
    # the published baseline, so a fresh judge run goes to the gitignored
    # runs/sae_analysis/ instead and leaves that archive untouched.
    OUT_DIR = out_dir or DEFAULT_OUT_DIR
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"{input_path.stem}-{ranking}.json"
    if os.path.exists(out_path):
        return out_path

    with open(input_path) as f:
        ranking_data = json.load(f)

    dataset   = ranking_data.get("dataset", "unknown")
    feat_type = ranking_data.get("type", "transcoder")
    prompt    = ranking_data.get("prompt", "")
    features  = ranking_data.get("features", [])

    task_desc, concern = DATASET_CONCERNS.get(dataset, ("unknown task", "unknown concern"))

    # The dictionary layer must be the one the feature indices were selected with.
    # Fail loud on old ranking files rather than silently defaulting to 22, which is
    # how the selector and the reader drifted apart in the first place.
    layer = ranking_data.get("layer")
    if layer is None:
        raise ValueError(
            f"{input_path} has no 'layer' key, so the dictionary its feature indices "
            "came from is unknown. It was produced before the 2026-07-26 layer fix. "
            "Re-run rank_sae_features_by_probe.py for this dataset."
        )
    template = (
        NP_TRANSCODER_SAE_ID_TEMPLATE if feat_type == "transcoder"
        else NP_SAE_SAE_ID_TEMPLATE
    )
    sae_id = template.format(layer=int(layer))
    log.append(f"  layer {layer}, Neuronpedia dictionary {sae_id}")

    selected = select_features(features, ranking, top_n)
    log.append(f"  Top-{top_n} by {ranking} ranking -> {len(selected)} features")

    # Fetch Neuronpedia. Threaded because these are 20 independent GETs against a
    # public API and the fetch, not the judging, is what made a serial run take
    # hours. Order is restored below, so the prompt the judge sees is identical
    # to the one the serial path built.
    features_with_np: list[dict] = [None] * len(selected)  # type: ignore[list-item]
    if selected:
        with ThreadPoolExecutor(max_workers=min(np_workers, len(selected))) as pool:
            futs = {
                pool.submit(fetch_neuronpedia, f["feature_idx"], sae_id): i
                for i, f in enumerate(selected)
            }
            for fut in as_completed(futs):
                i = futs[fut]
                features_with_np[i] = {**selected[i], "neuronpedia": fut.result()}

    # Summary table
    log.append("")
    for f in features_with_np:
        np = f.get("neuronpedia", {})
        log.append(
            f"    [{f['feature_idx']:5d}] "
            f"b={f['cos_sim_biased']:+.3f}(#{f['rank_biased']:3d}) "
            f"u={f['cos_sim_unbiased']:+.3f}(#{f['rank_unbiased']:3d})  "
            f"{np.get('error') or np.get('label', '')[:55]}"
        )

    # LLM call
    user_msg = build_user_prompt(prompt, dataset, task_desc, concern, features_with_np)
    log.append(f"\n  Querying {model}...")
    # The old call passed Anthropic's thinking={"type": "enabled",
    # "budget_tokens": 1024} inside max_tokens=2048, reserving roughly half the
    # budget for reasoning and leaving the rest for the visible answer. That
    # spelling is Anthropic-Messages-only and LLMClient.create_message exposes
    # no equivalent, so it is gone. This is a real behavior change, not a
    # rename: OpenRouter DOES accept a `reasoning` object on chat-completions,
    # but reaching it needs an extra_body passthrough the client does not have
    # today. Without a separate reservation, the default judge (minimax-m2.7,
    # which reasons by default) spends an unbounded share of max_tokens
    # thinking, so the budget is doubled to make an answer-starved completion
    # unlikely rather than merely less likely.
    # Measured 2026-07-28: at 4096, minimax/minimax-m3 starved 11 of 160 units on
    # the re-run, and the failures were NOT balanced across conditions (9 of 11
    # were unbiased), so silently scoring around them would have shrunk the U
    # denominator more than B and moved the headline. Hence --max-tokens rather
    # than a nudged constant: the value that avoids starvation is judge specific.
    response = client.create_message(
        model=model,
        max_tokens=max_tokens,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )
    # An empty completion IS the failure mode above: the client already retried
    # transient blanks and returns a truncated one verbatim, so bare next() would
    # surface it as a bewildering StopIteration. Name the cause instead.
    analysis = next(
        (b.text for b in response.content if b.type == "text" and b.text.strip()), None
    )
    if analysis is None:
        raise RuntimeError(
            f"{model} returned no text for {input_path.name} ({ranking}): "
            f"stop_reason={response.stop_reason!r}, blocks={response.content!r}. "
            "stop_reason 'max_tokens' means reasoning consumed the whole budget, "
            "so raise max_tokens here or pick a non-reasoning judge."
        )
    analysis = analysis.strip()

    log.append("\n  --- LLM verdict ---")
    log.append(analysis)

    # Write through a temp file and rename. The resume guard at the top keys on
    # mere existence, so a run killed partway through a json.dump would leave a
    # truncated file that every later run then SKIPS, silently dropping the unit
    # from the eval. rename is atomic within a filesystem.
    tmp_path = out_path.with_suffix(".json.tmp")
    with open(tmp_path, "w") as f:
        json.dump({
            # Provenance only. Nothing reads this field back, which is why the
            # committed verdicts in probe_artifacts/sae_analysis/ can carry a
            # scrubbed "<repo>/..." path here without breaking any scorer.
            "input_file":         str(input_path),
            "dataset":            dataset,
            "type":               feat_type,
            "prompt":             prompt,
            "ranking":            ranking,
            "top_n":              top_n,
            "model":              model,
            # Provenance of the feature indices, same argument as in the ranking
            # file: a verdict is only interpretable next to the dictionary its
            # feature descriptions were pulled from.
            "layer":              int(layer),
            "sae_id":             sae_id,
            "features_inspected": features_with_np,
            "analysis":           analysis,
        }, f, indent=2)
    tmp_path.rename(out_path)
    log.append(f"  Saved -> {out_path}")
    print("\n".join(log), flush=True)
    return out_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Judge spuriosity of SAE features ranked by probe cosine similarity"
    )
    parser.add_argument("--input", nargs="+", required=True,
                        help="Ranking JSON file(s) from rank_sae_features_by_probe.py")
    parser.add_argument("--ranking", default="both", choices=["biased", "unbiased", "both"],
                        help="Which probe ranking to use when selecting features (default: both)")
    parser.add_argument("--top-n", type=int, default=DEFAULT_TOP_N,
                        help=f"Number of top features to inspect (default: {DEFAULT_TOP_N})")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--max-tokens", type=int, default=4096,
                        help="Completion budget per unit (default: 4096). A reasoning "
                             "judge spends an unbounded share of this thinking, and a "
                             "starved completion raises rather than scoring blank. "
                             "Raise it if you see stop_reason='max_tokens'.")
    # Same gateway choice every other entry script offers. argparse rejects a
    # retired value passed on the command line, but NOT one arriving through
    # this default= (argparse does not validate defaults against choices), so
    # LLM_PROVIDER=anthropic in the environment gets past this line. It is
    # caught a few lines down: preflight_providers calls check_provider first.
    parser.add_argument("--provider", default=os.environ.get("LLM_PROVIDER", "openrouter"),
                        choices=PROVIDER_CHOICES,
                        help="Gateway for the judge model (default: $LLM_PROVIDER "
                             "or openrouter)")
    # A full re-judge is 160 units (40 prompts x 2 dictionary types x 2
    # rankings), each an LLM call behind up to 20 Neuronpedia GETs. Serial that
    # is hours and the whole of it is network wait, so it parallelises almost
    # perfectly. Mirrors --workers in eval_oracle_feature_counts.py.
    parser.add_argument("--workers", type=int, default=1,
                        help="Judge units to run concurrently (default: 1, serial). "
                             "20 is a good value for a full re-judge.")
    parser.add_argument("--np-workers", type=int, default=8,
                        help="Concurrent Neuronpedia fetches WITHIN one unit "
                             "(default: 8). Total in flight is roughly "
                             "--workers x --np-workers, so keep the product civil.")
    parser.add_argument("--out-dir", default=None,
                        help=f"Where verdicts land (default {DEFAULT_OUT_DIR}). "
                             "Existing files are SKIPPED, so point this somewhere new to "
                             "re-judge rather than resume. The committed verdicts in "
                             "probe_artifacts/sae_analysis/ are never written to. Score "
                             "a fresh set with "
                             "eval_sae_judge_spuriosity.py --analysis-dir.")
    args = parser.parse_args()

    model = args.model
    # Name the missing key before the Neuronpedia fetching, not on a 401 after it.
    preflight_providers([model], args.provider)
    client = LLMClient(provider=args.provider)

    # Resolve input files
    input_paths = []
    for pattern in args.input:
        p = Path(pattern)
        if p.exists():
            input_paths.append(p)
        else:
            matches = sorted(_TASK_ROOT.glob(pattern)) or sorted(Path(".").glob(pattern))
            if not matches:
                print(f"WARNING: no files matched: {pattern}")
            input_paths.extend(matches)

    if not input_paths:
        print("No input files found.")
        sys.exit(1)

    rankings = ["biased", "unbiased"] if args.ranking == "both" else [args.ranking]
    out_dir = Path(args.out_dir).resolve() if args.out_dir else None

    work = [_Unit(p, r) for p in input_paths for r in rankings]
    print(f"{len(work)} judge units ({len(input_paths)} files x {len(rankings)} rankings), "
          f"{args.workers} workers, model {model} via {args.provider}", flush=True)

    def process(u: _Unit) -> tuple[_Unit, Exception | None]:
        # Never raises. One unit dying must not take the other 159 with it, which
        # is what an unguarded executor does: as_completed re-raises on .result()
        # and the surviving work is thrown away.
        try:
            run_one(u.path, u.ranking, args.top_n, client, model,
                    out_dir=out_dir, np_workers=args.np_workers,
                    max_tokens=args.max_tokens)
            return u, None
        except Exception as e:  # noqa: BLE001
            return u, e

    failures: list[tuple[_Unit, Exception]] = []
    done = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futs = [pool.submit(process, u) for u in work]
        for fut in as_completed(futs):
            u, err = fut.result()
            done += 1
            if err is not None:
                failures.append((u, err))
                print(f"[{done}/{len(work)}] FAILED {u.path.name} ({u.ranking}): "
                      f"{type(err).__name__}: {err}", flush=True)
            else:
                print(f"[{done}/{len(work)}] ok {u.path.name} ({u.ranking})", flush=True)

    hits = len(_NP_CACHE)
    print(f"\nNeuronpedia: {hits} distinct features fetched.")
    if failures:
        # Loud, itemised and non-zero exit. A partial re-judge that reports
        # success is how a stale verdict set survives into a results table.
        print(f"\n{len(failures)} of {len(work)} units FAILED:")
        for u, e in failures:
            print(f"  {u.path.name} ({u.ranking}): {type(e).__name__}: {e}")
        print("\nRe-run the same command to retry only these "
              "(completed units are skipped).")
        sys.exit(1)

    print("\nAll done.")


if __name__ == "__main__":
    main()
