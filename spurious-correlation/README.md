# Task 1, spurious probe features

A linear probe reads one layer of Gemma-2-2B and scores a piece of text. Sometimes it has
learned the thing you asked for, and sometimes it has learned a shortcut that happened to
correlate with the thing in the training data. This task asks the Circuit Oracle to tell
the two apart from the probe's attribution graph alone.

The oracle never sees the training data, the probe weights, or a label. It sees an
attribution graph whose output node is the probe direction rather than a next-token logit,
and it answers one question. Which transcoder features actually drive this score.

Every prompt is run twice, once against a **biased** probe trained where the shortcut was
perfectly predictive, and once against an **unbiased** probe trained on balanced data where
the shortcut carries no signal. Neither run is told which probe it is looking at. A good
oracle calls the first one spurious and the second one causal.

The earlier version of this work is
[the workshop paper](https://openreview.net/forum?id=ANY6YrYUZE) (ICML 2026 Mechanistic
Interpretability Workshop). Numbers in `results/` are the final ones. Numbers in
`results-workshop/` are the runs behind the workshop paper, kept for provenance.

---

## The four datasets

`prompts.json` at the task root is the manifest. It holds 40 prompts, and each prompt
produces two graphs.

| Dataset slug | HuggingFace source | True label | Spurious shortcut | Probe layer | Prompts |
|---|---|---|---|---|---|
| `bib_nurse_professor` | `LabHC/bias_in_bios` | nurse vs professor | gender markers | 22 | 10 |
| `bib_journalist_dietitian` | `LabHC/bias_in_bios` | dietitian vs journalist | gender markers | 22 | 10 |
| `civil_comments` | `google/civil_comments` | toxic vs not | identity-attack annotation | 12 | 10 |
| `multinli` | `nyu-mll/multi_nli` | contradiction vs entailment | negation words in the hypothesis | 17 | 10 |
| `bib_surgeon_teacher` | `LabHC/bias_in_bios` | teacher vs surgeon | gender markers | 22 | 0 |

`bib_surgeon_teacher` is deliberately empty. Its probes failed quality screening, so it
contributes no prompts and no graphs. It stays in the valid-dataset list so a loop over all
five is legal, and its probe checkpoints stay committed for reference.

Each dataset splits its prompts across two subgroups.

- `neg_neg`, where the true label is 0 and the shortcut is absent.
- `pos_pos`, where the true label is 1 and the shortcut is present.

The two BiasInBios datasets carry 5 of each. CivilComments and MultiNLI carry 10 `pos_pos`
and no `neg_neg`.

### The 80-graph eval set

40 prompts, times the biased and the unbiased probe, gives **80 graphs**, 40 biased and 40
unbiased. Slugs are built from the manifest and look like this.

```
<dataset>-<subgroup>_<index>-<biased|unbiased>-probe-correct
```

For example `civil_comments-pos_pos_3-biased-probe-correct` and
`bib_nurse_professor-neg_neg_1-unbiased-probe-correct`. The trailing `correct` names the
attribution method, mean-pooled injection at the probe layer. Attribution starts at the
residual stream where the probe actually reads, so only features at or below the probe
layer are attributed. A `simple` method exists in the filter flags and injects at the final
layer instead. No reported run uses it.

`run_oracle_on_probes.py` derives these 80 slugs from `prompts.json` at startup and exits
with a list of what is missing rather than quietly running a subset.

---

## The probes

Ten checkpoints, committed under `probe_extraction/probes/`. They are roughly 7 KB each and
they are the one `.pt` exception in the repo-root `.gitignore`.

```
bib_journalist_dietitian_layer22_bfloat16.pt        bib_journalist_dietitian_layer22_bfloat16_unbiased.pt
bib_nurse_professor_layer22_bfloat16.pt             bib_nurse_professor_layer22_bfloat16_unbiased.pt
bib_surgeon_teacher_layer22_bfloat16.pt             bib_surgeon_teacher_layer22_bfloat16_unbiased.pt
civil_comments_layer12_bfloat16.pt                  civil_comments_layer12_bfloat16_unbiased.pt
multinli_layer17_bfloat16.pt                        multinli_layer17_bfloat16_unbiased.pt
```

Each file is a state dict with `state_dict`, `activation_dim` and `dtype` keys, not a
pickled module. `probe_extraction/README.md` documents the format and the loader.

**The committed checkpoints are canonical.** They are not exactly regenerable, so every
number in this task is tied to these ten files. Retraining gives you probes that work but
not the same probes, and the graphs built from them are a different generation. Only
retrain if you are starting a new experiment, never to reproduce a published figure.

`probe_artifacts/spuriosity/accuracy_grids.md` holds the per-subgroup accuracy grid for
each probe pair, which is how you can see the shortcut at work. On `bib_nurse_professor`
the biased probe scores 98.9 percent on male professors and 17.6 percent on female
professors, while the unbiased probe stays near 97 percent on both.

---

## Directory map

```
prompts.json               the 40-prompt manifest that defines the 80-slug eval set
adapters/                  dataset adapters (bias_in_bios, civil_comments, multinli, generic_hf)
probe_extraction/          probe trainer, layer sweep, YAML configs, committed probes/
scripts/                   build, run, and eval entry points
probe_artifacts/           committed baseline artifacts (see Baselines below)
results/                   final runs, one directory per arm, read-only archive
results-workshop/          the runs behind the workshop paper, read-only archive
tests/                     64 tests, no GPU and no API needed
runs/                      default output root for everything you run, gitignored
```

Nothing writes into `results/` or `results-workshop/`. Every runner and evaluator defaults
its output to `runs/`, which the repo-root `.gitignore` covers.

---

## Setup

From the repository root.

```bash
uv venv --python 3.12 && source .venv/bin/activate
uv pip install -e '.[data,plots]'
cp .env.example .env       # then fill in OPENROUTER_API_KEY and HF_TOKEN
```

Python 3.12 or newer is required. Several modules use f-string syntax that is a 3.12
language feature, so on 3.11 the install succeeds and then dies with a syntax error at
import time.

Extras you need for parts of this task.

| Extra | Needed for |
|---|---|
| `data` | the dataset adapters, so graph building and probe training |
| `plots` | the AUROC bar chart from `eval_oracle_feature_counts.py` |
| `probes` | `nnsight`, only if you retrain probes or rerun the layer sweep |
| `baselines` | `sae-lens`, only for `rank_sae_features_by_probe.py`, the cosine baselines |

Add the extra you need to the install rather than installing SAELens by hand.

```bash
uv pip install -e '.[data,plots,baselines]'
```

### Environment variables

| Variable | Read by | Default |
|---|---|---|
| `OPENROUTER_API_KEY` | every LLM call | none, required |
| `HF_TOKEN` | model and dataset downloads | none, required for gated repos |
| `GRAPH_STORE` | graph build and read paths | the task root, so `spurious-correlation/probe_circuits/` |
| `PROBES_DIR` | `circuit_extraction.py` probe lookup | `spurious-correlation/probe_extraction/probes` |
| `LLM_PROVIDER` | default gateway | `openrouter` |

`GRAPH_STORE` is a root, and this task appends `probe_circuits` to it. Tasks 2 and 3 append
`graphs` instead, so one mounted volume serves all three. Every script here loads the
repo-root `.env` itself, so you can run them directly with no wrapper. It is loaded before
the argument parser is built, so a value set only in `.env` still reaches a flag default.
`LLM_PROVIDER=kilo` there changes what `--provider` defaults to.

---

## The pipeline, in order

### 1. Train the probes (skip this unless you are starting fresh)

One call per config. `--config` is required and there are five configs.

```bash
python spurious-correlation/probe_extraction/train_probes.py \
    --config spurious-correlation/probe_extraction/configs/bib_nurse_professor_gemma2_2b.yaml
python spurious-correlation/probe_extraction/train_probes.py \
    --config spurious-correlation/probe_extraction/configs/bib_journalist_dietitian_gemma2_2b.yaml
python spurious-correlation/probe_extraction/train_probes.py \
    --config spurious-correlation/probe_extraction/configs/bib_surgeon_teacher_gemma2_2b.yaml
python spurious-correlation/probe_extraction/train_probes.py \
    --config spurious-correlation/probe_extraction/configs/civil_comments_gemma2_2b.yaml --layer 12
python spurious-correlation/probe_extraction/train_probes.py \
    --config spurious-correlation/probe_extraction/configs/multinli_gemma2_2b.yaml --layer 17
```

Read the two `--layer` overrides on the last two lines carefully. All five YAML configs
carry `layer: 22`, but the committed CivilComments probe sits at layer 12 and the MultiNLI
probe at layer 17. Without the override you get layer-22 probes, and
`circuit_extraction.py` will not find them, because it looks for a filename containing the
layer it expects for that dataset. The expected layers are hardcoded in its `_LAYER_MAP`,
22 for the three BiasInBios pairs, 12 for CivilComments and 17 for MultiNLI.

`--output-dir` defaults to `spurious-correlation/probe_extraction/probes`, the absolute
path where the committed checkpoints live, so training overwrites them unless you point it
somewhere else. The `output_dir: .` key inside every config is ignored.

Other flags are `--layer`, `--device`, `--output-dir` and `--overwrite`. Existing files are
skipped unless you pass `--overwrite`.

The two non-22 layers came out of a separate two-phase layer sweep, whose saved output
lives next to the configs. Phase 1 trains a biased probe at every layer and scores it on
the ambiguous split. Phase 2 filters on a threshold and re-scores the survivors on the
balanced split, then takes the layer that generalises worst, since that is the layer
leaning hardest on the shortcut.

Its record and the committed probes agree on MultiNLI and disagree on CivilComments.
`configs/layer_selection_multinli_gemma2_2b.json` records `selected_layer: 17`, which is
the committed probe. `configs/layer_selection_civil_comments_gemma2_2b.json` records
`selected_layer: 8`, while the committed probe is at layer 12 and every downstream script
expects 12. Treat the sweep as the diagnostic that motivated moving off layer 22 rather
than as the record of what shipped.

```bash
python spurious-correlation/probe_extraction/layer_sweep.py ambiguous \
    --config spurious-correlation/probe_extraction/configs/multinli_gemma2_2b.yaml
python spurious-correlation/probe_extraction/layer_sweep.py select \
    --config spurious-correlation/probe_extraction/configs/multinli_gemma2_2b.yaml \
    --phase1-json spurious-correlation/probe_extraction/configs/layer_sweep_multinli_gemma2_2b.json \
    --threshold 0.90
```

### 2. Build the 80 graphs (GPU)

The balanced multi-GPU launcher is the normal path. It cuts the 40 prompts into piles of
equal predicted work rather than one dataset per GPU, because prompt length varies about
fourfold across the manifest.

```bash
# See the plan and the predicted per-shard minutes without spending anything
python spurious-correlation/scripts/build_shards.py --shards 4 --dry-run

# Build
python spurious-correlation/scripts/build_shards.py --shards 4
```

On the committed manifest the planner reports a 108 minute serial estimate and about 27
minutes on 4 GPUs, a 3.99x speedup. Flags are `--shards`, `--gpu-ids`, `--dry-run`,
`--no-warm`, `--with-neuronpedia` and `--rebuild-existing`.

The first shard run does a single-prompt warm-up alone, before the fan-out, so the shards
do not race each other for the same cold HuggingFace downloads. That warm-up graph is one
of the 80 and is not wasted. Pass `--no-warm` only when the caches are already populated on
that machine. Read peak VRAM and the phase timings out of the warm-up log before trusting
any estimate. Per-shard logs land in `spurious-correlation/runs/build_logs/shard<N>.out`.

On one GPU, or to rebuild a single dataset, use the batch runner directly.

```bash
python spurious-correlation/scripts/run_extraction_batch.py --dataset bib_nurse_professor
python spurious-correlation/scripts/run_extraction_batch.py --dataset civil_comments --skip-existing
python spurious-correlation/scripts/run_extraction_batch.py --dataset multinli --tags neg_neg_1 pos_pos_2
```

Valid `--dataset` values are `bib_nurse_professor`, `bib_journalist_dietitian`,
`bib_surgeon_teacher`, `civil_comments` and `multinli`. One invocation per prompt, and each
invocation writes both the biased and the unbiased graph.

`circuit_extraction.py` is the single-prompt worker underneath. It is a top-to-bottom
script, not a library, so importing it runs the whole build. `--dataset` is required and it
exits with code 2 and the valid slug list if you omit it.

```bash
python spurious-correlation/scripts/circuit_extraction.py --dataset multinli
python spurious-correlation/scripts/circuit_extraction.py \
    --dataset civil_comments --prompt-tag pos_pos_1 --prompt "..."
```

Graphs are built at `max_feature_nodes=4096`, deliberately not the 8192 the other two tasks
use, because Gemma-2-2B is 26 layers at `d_model` 2304 and the archived graphs behind the
published numbers were built at 4096. Raising it makes a generation whose feature counts do
not compare with the published ones, and feature counts are the headline quantity here.

Expect graphs from roughly 80 MB on the shortest CivilComments prompt to roughly 400 MB on
the longest biography, and about 15 GB for the full store of 80. That range is an estimate
from the size model in `build_shards.py`, not a measurement.

### 3. Verify the store before you tear the GPU down

```bash
python spurious-correlation/scripts/run_extraction_batch.py --verify-store
```

No GPU and no model load. It walks the whole manifest across every dataset and fails unless
all 80 graphs are present and non-empty. On an empty store it prints
`STORE INCOMPLETE: 80 of 80 graph(s) missing or empty under <path>` and exits 1. On a good
store it prints `STORE OK`.

### 4. Run the oracle

One arm over all 80 graphs, sequentially.

```bash
python spurious-correlation/scripts/run_oracle_on_probes.py --arm probes-arm1
```

Output lands in `spurious-correlation/runs/probes-arm1/`. With no `--arm` it writes to
`spurious-correlation/runs/` and runs `minimax/minimax-m3` with an
`openai/gpt-oss-120b` subagent, which is the same pair `probes-arm1` uses. `--arm` still
matters, because arms 2 and 3 change the tool surface and the pipeline rather than the
models, and the arm name is recorded in the run's provenance.

Narrowing flags, all of which cut down the default 80.

```bash
# One graph
python spurious-correlation/scripts/run_oracle_on_probes.py \
    --slugs civil_comments-pos_pos_3-biased-probe-correct

# One dataset, or one probe type
python spurious-correlation/scripts/run_oracle_on_probes.py --dataset bib_journalist_dietitian
python spurious-correlation/scripts/run_oracle_on_probes.py --probe-type unbiased --method correct

# Override the per-dataset concern sentence
python spurious-correlation/scripts/run_oracle_on_probes.py \
    --concern "What features encode gender bias?"
```

The rest of the surface is `--all-in-store` (every graph in the store, a superset of the
reported 80), `--orchestrator-model` and `--subagent-model` (both refused alongside
`--arm`, which owns them), `--provider` (`openrouter` or `kilo`), `--max-hops` (default 12),
`--output-dir`, `--pass-index` and `--quiet`.

For the whole grid, use the parallel launcher. One subprocess per run, dispatched from a
dynamic queue, so the makespan is the slowest single run rather than the slowest shard.

```bash
# Print the plan, spend nothing
python spurious-correlation/scripts/run_arms.py --dry-run

# Price a small sample first, one run per arm before it deepens
python spurious-correlation/scripts/run_arms.py --pilot 10

# The full grid
python spurious-correlation/scripts/run_arms.py --jobs 32
```

`--dry-run` reports the grid as 720 runs. That is four single-pass arms at 80 slugs each,
which is 320, plus `probes-arm1` at 80 slugs times 5 passes, which is 400. Only arm 1
repeats, because within-configuration variance is a property of the pipeline rather than of
each arm. Flags are `--arms`, `--slugs`, `--repeats`
(default 5, applied to `probes-arm1` only), `--jobs` (default 32, the whole lever on wall
clock), `--provider`, `--output-dir` (default `runs`), `--log-dir` (default
`<output-dir>/logs`), `--pilot`, `--timeout` (default 3600 seconds per run),
`--no-skip-existing`, `--no-warmup` and `--dry-run`. Anything after those is forwarded
verbatim to the runner.

Resume is on by default. A run counts as complete only when its `oracle_result.json`
exists, so a crash halfway through leaves a directory that gets redone rather than skipped.

### 5. Evaluate

```bash
python spurious-correlation/scripts/eval_oracle_feature_counts.py \
    --results-dir spurious-correlation/runs/probes-arm1
```

The judge reads each run, enumerates every feature the oracle surfaced, and labels each one
spurious, causal or other. Biased and unbiased runs are judged independently, with no
pairing and no prior about which class should win.

Flags are `--results-dir`, `--force` (re-judge instead of using the cache), `--slim` (an
ablation that passes only the analysis prose and drops the circuit and label context),
`--provider`, `--judge-model` (default `openai/gpt-5.4-mini`), `--all-runs`, `--workers`
(default 12) and `--tag`. A non-default `--judge-model` requires `--tag`, so two judges
cannot overwrite each other's verdicts.

Pointing `--results-dir` at `results/` or `results-workshop/` is safe. Verdicts already
stored there are read as the cache, and any fresh verdict is written under
`spurious-correlation/runs/eval/<same relative path>/` instead. The AUROC chart goes to
`spurious-correlation/runs/figures/`.

`--all-runs` judges every repeat pass rather than one canonical run per experiment, which is
what `aggregate_stability.py` needs. The printed summary still scores one run per
experiment either way.

---

## The arms

Five arms, defined once in `src/circuit_oracle/arms.py` and resolved by `--arm`. An arm owns
the orchestrator, the subagent, the tool surface and the pipeline together, so a run's
identity is one registry key rather than a hand-assembled flag set. Passing `--arm`
alongside `--orchestrator-model` or `--subagent-model` is an error.

| Arm | Orchestrator | Subagent | What it varies |
|---|---|---|---|
| `probes-arm1` | `minimax/minimax-m3` | `openai/gpt-oss-120b` | nothing, the full pipeline with traversal and `inspect_feature` |
| `probes-arm2` | `minimax/minimax-m3` | `openai/gpt-oss-120b` | `inspect_feature` removed, so no Neuronpedia labels |
| `probes-arm3` | `minimax/minimax-m3` | `openai/gpt-oss-120b` | one-shot, top-k features by direct effect, no edge traversal |
| `probes-arm4` | `openai/gpt-5.6-terra` | `openai/gpt-oss-120b` | orchestrator only |
| `probes-arm5` | `google/gemma-4-31b-it` | `openai/gpt-oss-120b` | orchestrator only, open weights |

Arms 1, 2 and 3 share both models, so they are told apart only by the arm name in
`oracle_result.json` and by the output directory. That is why `--arm` routes to
`runs/<arm>/` rather than a shared root. Arm 3 records the subagent in its provenance but
never calls it, because the one-shot pipeline has no traversal to dispatch.

All five run in observational mode, which strips the intervention tools and the
end-of-turn chain guards from task 3. `CAUSAL_ONLY_TOOLS` in
`src/circuit_oracle/tool_schemas.py` names five, but two of those, `intervene_feature`
and `intervene_supernode`, are already retired from the agent-facing list, so three are
actually removed here: `pin_features`, `batched_anchor_sweep` and
`batched_supernode_sweep`. There is no live model in the loop on this task, only the
saved graph, which is why the intervention tools have nothing to run against.

---

## The scoring rule

The judge returns a categorical `dominant` field, one of `spurious`, `causal`, `mixed` or
`none`. The headline metric uses that field and nothing else.

```
biased   probe  ->  correct if dominant == "spurious"
unbiased probe  ->  correct if dominant in {"causal", "mixed"}
```

`spurious_fraction` is also recorded and it is descriptive output, not the rule. A threshold
of `f >= 0.5` on it gives a slightly different number, because one MultiNLI run sits at
exactly 0.50. The categorical rule is what the committed scorer and every figure use.

Alongside the accuracy the evaluator reports a threshold-free AUROC, using
`spurious_fraction` as the score with biased runs as the positive class, per dataset and
pooled.

---

## Where the numbers live

`results/` holds the final runs, one directory per arm. Each arm holds 80 experiment
directories under `<arm>/exp/`, and each experiment directory holds one run directory per
pass. `probes-arm1` has five passes per slug, the others have one.

```
results/probes-arm1/exp/exp-probe-<slug>-question/minimax-m3_gpt-oss-120b_<timestamp>_pass<N>/
    report.md                   the readable write-up, with Neuronpedia links per feature
    pinned_ids.json             the features the oracle committed to, as "layer_feature_position"
    judge_feature_counts.json   the judge verdict, including the dominant field
    oracle_result.json          full transcript and tool calls, sampled runs only
```

`results/stability_probes_arm1.json` is the committed traversal-stability summary over all
80 slugs and all 5 passes.

### Reported accuracy

`probes-arm1` repeats each slug five times, and the passes disagree. **Report the five-pass
mean, not the last pass.**

| Pass | Correct | Accuracy |
|---|---|---|
| 1 | 62 / 80 | 77.50% |
| 2 | 62 / 80 | 77.50% |
| 3 | 62 / 80 | 77.50% |
| 4 | 61 / 80 | 76.25% |
| 5 | 66 / 80 | 82.50% |
| **mean** | | **78.25%**, standard deviation 2.44 points across passes |

The evaluator scores one canonical run per experiment, which is the newest one, so pointing
it at `results/probes-arm1` prints the single-pass figure of 66/80 and not the mean. There
is no shipped script that averages the passes, so compute it from the five
`judge_feature_counts.json` files under each experiment directory.

Single-pass arms, straight from the evaluator.

| Arm | Biased | Unbiased | Total | Pooled AUROC |
|---|---|---|---|---|
| `probes-arm2` | 36 / 40 | 29 / 40 | 65 / 80, 81% | 0.827 |
| `probes-arm3` | 27 / 40 | 35 / 40 | 62 / 80, 78% | 0.868 |
| `probes-arm4` | 26 / 40 | 30 / 40 | 56 / 80, 70% | 0.787 |
| `probes-arm5` | 28 / 40 | 30 / 40 | 58 / 80, 72% | 0.817 |

The AUROC column drops any run whose verdict carries no numeric `spurious_fraction`. That
is one run on arm 2 and two on arm 5. The accuracy column keeps them, since the categorical
rule does not need the fraction.

`results-workshop/` holds the runs behind the workshop paper. They are a different
instrument, `minimax/minimax-m2.7` orchestrating `deepseek/deepseek-v3.2`, one pass per
slug, and their number is 69/80 or 86 percent with a pooled AUROC of 0.882. Do not compare
that figure with the `results/` figures above as if they measured the same configuration.
The `results-workshop/opus-sonnet/` subdirectory is a separate 16-experiment (22-run) exploratory set on a
different concern wording, kept for provenance and excluded from every score.

---

## The cosine-similarity baselines

The oracle is compared against two much simpler detectors that skip the attribution graph.
Run the prompt through Gemma-2-2B, encode the residual stream at the probe's own layer with
a Gemma Scope dictionary, rank the active features by cosine similarity with the probe
weight vector, hand the top 20 to a judge, and ask whether the set contains spurious
features. **Trans-cos** uses the transcoder dictionary and **SAE-cos** uses the residual
SAE.

The judge is not told which probe produced the ranking. A biased ranking should get YES and
an unbiased ranking should get NO.

### Step 1, rank the features (GPU, needs the `baselines` extra)

```bash
# Both dictionaries, all datasets, in one process
python spurious-correlation/scripts/rank_sae_features_by_probe.py --all --type both

# One dataset, transcoder only
python spurious-correlation/scripts/rank_sae_features_by_probe.py \
    --dataset bib_journalist_dietitian --type transcoder
```

`--type` takes `sae`, `transcoder` or `both` and defaults to `transcoder`. `--type both`
exists because the two baselines differ only in which dictionary the residuals go through,
and running the script twice reloads Gemma-2-2B for the second type, which is most of the
wall clock.

Output goes to `probe_artifacts/plt_features/<dataset>-<subgroup>_<n>-transcoder.json` for
the transcoder and `probe_artifacts/sae_features/...-sae.json` for the SAE. Neither
directory is committed, because the two together are large. This step creates them, and
copies of both are available upon request (open an issue on this repository). Asking for
them is the offline alternative to re-running this GPU step, and step 3 scores off the committed
judge verdicts either way, so neither directory is needed to reproduce the baseline
numbers.

The dictionary is loaded at the probe's own layer, 22, 12 or 17, never a fixed layer, and
each output file records the layer and the exact dictionary id it used. Feature indices do
not transfer across dictionaries, so the downstream judge reads those fields rather than
assuming a layer.

Watch for the warning about a prompt with fewer than 20 active features. The top-20 cutoff
silently returns the whole active set in that case, which makes the biased and unbiased
lists identical and the baseline unmeasurable on that prompt. An early residual-SAE
ranking hit that case on 39 of 40 prompts, which is why the shipped SAE-cos numbers come
from the rankings above and not from that first attempt.

### Step 2, judge the ranked sets

```bash
python spurious-correlation/scripts/judge_sae_features.py \
    --input 'probe_artifacts/plt_features/*-transcoder.json' \
    --ranking both --workers 20
```

`--input` is required and takes one or more paths or globs. A glob is resolved against the
task root first, so write it as `probe_artifacts/...` and the command works from any
directory. `--ranking` is `biased`, `unbiased` or `both` and defaults to `both`. Other
flags are `--top-n` (default 20), `--model` (default `minimax/minimax-m3`, matching the
probes arms), `--max-tokens` (default 4096), `--provider`, `--workers` (default 1, serial)
and `--np-workers` (default 8, concurrent Neuronpedia fetches inside one unit).

`--out-dir` defaults to `spurious-correlation/runs/sae_analysis`. Existing files are
skipped, so point it somewhere new to re-judge rather than resume. A full re-judge is 160
units, 40 prompts times 2 dictionary types times 2 rankings.

The committed verdicts behind the published baseline are in
`probe_artifacts/sae_analysis/`, 160 files named
`<dataset>-<subgroup>_<n>-<transcoder|sae>-<biased|unbiased>.json`. Nothing writes into
that directory.

### Step 3, score the verdicts

```bash
python spurious-correlation/scripts/eval_sae_judge_spuriosity.py
python spurious-correlation/scripts/eval_sae_judge_spuriosity.py --type plt
python spurious-correlation/scripts/eval_sae_judge_spuriosity.py --type sae
```

No GPU, no API, no key. It reads the committed verdicts and prints a per-dataset grid.
`--type` is `plt` (transcoder), `sae` or `all`, defaulting to `all`. `--dataset` filters to
one slug. `--analysis-dir` points it at a fresh judge run, and you must set it to match
`judge_sae_features.py --out-dir` or the scorer keeps reporting the committed numbers.
`--out-md` overrides the report file, which defaults to
`spurious-correlation/runs/spuriosity/judge_eval.md` and is appended to.

### Results

| Detector | Biased rankings | Unbiased rankings | Total |
|---|---|---|---|
| Trans-cos (`--type plt`) | 40 / 40 | 18 / 40 | 58 / 80, 72.5% |
| SAE-cos (`--type sae`) | 40 / 40 | 12 / 40 | 52 / 80, 65.0% |
| Oracle, workshop archive | 36 / 40 | 33 / 40 | 69 / 80, 86.25% |

Both baselines are perfect on biased rankings and weak on unbiased ones, which is the shape
of a detector that mostly answers YES. They discriminate only on the two BiasInBios
datasets. On CivilComments and MultiNLI each one says YES to all 10 unbiased rankings and
scores 0/10.

The oracle row above is the workshop archive, which is the comparison the workshop paper
made. The final `probes-arm1` five-pass mean of 78.25 percent also clears both baselines,
but it was scored on a different orchestrator, so read the two oracle figures separately.

`eval_probe_spuriosity.py` is a separate diagnostic that scores all four subgroups with both
probes and prints the most confident prompts. It needs a GPU because it loads the model.

```bash
python spurious-correlation/scripts/eval_probe_spuriosity.py --dataset civil_comments
```

`--dataset` takes any dataset slug or `all`, and defaults to `all`. The report is appended
to `spurious-correlation/runs/spuriosity/analysis.md`.

---

## Reproducing without a GPU or an API key

Two commands read committed evidence and print published numbers with no credentials and no
network.

```bash
python spurious-correlation/scripts/eval_oracle_feature_counts.py
python spurious-correlation/scripts/eval_sae_judge_spuriosity.py
```

The first defaults to `results-workshop/` and prints 69/80, 86 percent, with a pooled AUROC
of 0.882.

| Dataset | AUROC |
|---|---|
| `bib_nurse_professor` | 1.000 |
| `bib_journalist_dietitian` | 0.960 |
| `civil_comments` | 0.880 |
| `multinli` | 0.790 |

The second command prints the Trans-cos and SAE-cos grids above. Both read committed
verdicts. `eval_oracle_feature_counts.py` calls the judge only for a run that has
neither a verdict nor an `oracle_result.json` to judge from, which is none of them in
the committed archives. `eval_sae_judge_spuriosity.py` never calls a judge at all, it
only scores the verdicts in `probe_artifacts/sae_analysis/`.

Neither command needs the editable install or a `PYTHONPATH` prefix.
`eval_oracle_feature_counts.py` puts `src/` on `sys.path` itself before importing the
shared LLM client, so it runs from a bare clone. What it does need is its third-party
dependencies, which is `python-dotenv` and `openai` for that import, plus `matplotlib`
if you want the AUROC chart. `eval_sae_judge_spuriosity.py` imports neither and needs
only the standard library.

---

## Traversal stability

The five repeat passes of `probes-arm1` measure how much of the oracle's answer is stable
across identical runs.

```bash
python scripts/aggregate_stability.py --track probes \
    --runs-root spurious-correlation/results/probes-arm1
```

Run from the repository root. `--track` and `--runs-root` are required, `--n-layers`
defaults to 26 for this task, and `--out` writes the full result as JSON. Without `--out`
the script writes nothing, so pointing it at an archive is read-only by construction. Point
`--runs-root` at exactly one arm. Mixing arms in one root averages across configurations
and means nothing.

It reports Jaccard overlap on the pinned feature set at three levels of identity (exact
feature, layer, and early or mid or late band), Jaccard on the flagged spurious and causal
sets, the spread in tool-call counts, and the rate at which the `dominant` verdict flips
between passes.

The committed `results/stability_probes_arm1.json` covers all 80 slugs. Rerunning the
aggregator against the archive finds only the sampled slugs that kept their
`oracle_result.json`, so its numbers differ. Use the committed file for the reported values.

A run set with no recorded pass index prints
`using directory-name order (legacy layout)` and falls back to timestamp order.

---

## Hardware

| Stage | Needs |
|---|---|
| Train probes, layer sweep | one GPU, `nnsight` |
| Build the 80 attribution graphs | one GPU, roughly 27 minutes on 4 cards or 108 minutes on 1 |
| Rank SAE and transcoder features | one GPU, the `baselines` extra (`sae-lens`) |
| `eval_probe_spuriosity.py` | one GPU |
| Oracle runs, all judges, all other evals | CPU, API calls only |

The two build timings are the shard planner's own estimate, printed by
`build_shards.py --dry-run` on the committed manifest, not a stopwatch reading.

Graph building loads Gemma-2-2B plus its Gemma Scope transcoders and offloads the
transcoders to CPU during attribution. This repository provisions one 80 GB card because
task 3 needs one, and task 1 sits well inside that. There is no measured peak-VRAM figure
for this task, so read one off the warm-up run's log before sizing a machine. Getting that
reading is exactly what the warm-up is for.

Once the graphs exist, everything else here runs on a laptop.

---

## Tests

From the repository root.

```bash
PYTHONPATH=src python -m pytest -q spurious-correlation/tests
```

64 tests, no GPU, no API key, about two seconds. They cover the shard planner, the
dictionary-id mapping across layers, manifest coverage, the extraction config, the arm
launcher, and the store verifier.

---

## Archives, sampling and redactions

`results/` and `results-workshop/` are archives. No command writes into them. Every default
output root is `<task>/runs/`, which the repo-root `.gitignore` covers.

**Sampling.** Three example slugs per arm keep the full run directory. In `results/` that
adds `oracle_result.json`, `circuit.svg`, `run.log` and the two elicitation dumps. The
workshop archive predates the run log and the elicitation dumps, so its three sampled runs
carry `oracle_result.json` and `circuit.svg` plus two older judge files, `judge_eval.json`
and `judge_feature_counts_slim.json`. Every other run
keeps its `report.md`, `pinned_ids.json` and `judge_feature_counts.json`. That is enough to
reproduce every published number, since the scorers replay committed verdicts. The full raw
dumps, along with `probe_artifacts/plt_features/` and `probe_artifacts/sae_features/`, are
available upon request. Do not write code that assumes every run directory has
an `oracle_result.json`. In `results-workshop/` only 3 of the 80 scored runs still carry
one, with three more under the excluded `opus-sonnet/` set.

**Redactions.** Email addresses inside activation-context strings were redacted from
committed artifacts and replaced with `[email redacted]`. The unredacted contexts are on
Neuronpedia under the feature ids each run records. `pinned_ids.json` stores them as
`layer_feature_position`, and `report.md` links each feature directly, in the form
`https://neuronpedia.org/gemma-2-2b/<layer>-gemmascope-transcoder-16k/<feature>`.
