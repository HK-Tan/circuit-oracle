# Circuit Oracle

A Circuit Oracle is an LLM agent that reads a transcoder attribution graph of some
other model and answers a safety question about that model's internal computation.
The graph is the whole interface. The agent has no access to the subject model's
weights or its training data, only to tools that walk the graph (list the strongest
features at a position, follow an edge upstream, look up a feature's label and its
top activating contexts, group features into a supernode, and on one task clamp a
feature and regenerate). It then writes a report. This repository holds the agent,
the three tasks it was evaluated on, and the run artifacts behind the numbers.

| Task | Directory | Subject model | Transcoders | Question the oracle answers | Results |
|---|---|---|---|---|---|
| 1. Spurious probe features | `spurious-correlation/` | `google/gemma-2-2b` | Gemma Scope 16k transcoders | Is this linear probe reading a causal feature or a spurious one? | `spurious-correlation/results/` |
| 2. Secret elicitation (ELK) | `secret-elicitation/` | `Qwen/Qwen3-8B` plus a taboo LoRA | `mwhanna/qwen3-8b-transcoders` | Which word is the model hiding? | `secret-elicitation/results/` |
| 3. Suppression jailbreak | `refusal-jailbreaking/` | `Qwen/Qwen3-4B` | `mwhanna/qwen3-4b-transcoders` | Which features gate the suppressed answer, and does clamping them release it? | `refusal-jailbreaking/results/` |

All three run the same agent out of one shared package, `src/circuit_oracle/`.

Per-task detail lives in `spurious-correlation/README.md`,
`secret-elicitation/README.md` and `refusal-jailbreaking/README.md`.

## Status

This is the final code and result archive for the project. It is the code behind the
workshop paper plus a full re-run on rebuilt instruments and an ablation grid the
workshop paper did not have.

- The result tables are in [SUMMARY.md](SUMMARY.md), and the notes behind them, with the
  instrument next to every figure, are in [summary/details.md](summary/details.md).
- The earlier version of this work is the workshop paper at the ICML 2026 Mechanistic
  Interpretability Workshop, <https://openreview.net/forum?id=ANY6YrYUZE>.

## What is in this release

**Committed.** The shared package and the vendored attribution library, all three
tasks' entry scripts, the prompt and eval sets, both result archives per task, the
Arditi refusal-direction baseline and its two graded archives, and the ten task-1
probe checkpoints in `spurious-correlation/probe_extraction/probes/` (80 KB total).
The probe checkpoints are committed precisely because they are the one artifact that
is not exactly regenerable, so a re-trained probe would be a different probe and
every task-1 graph would move with it.

**Available upon request.** The full raw run dumps, plus the task-1 feature-ranking
dumps `probe_artifacts/plt_features/` and `probe_artifacts/sae_features/`. Open an
issue on this repository to ask for a copy. The judge verdicts scored from those dumps,
`probe_artifacts/sae_analysis/`, are committed, so the SAE comparison still re-derives
from the repository alone.

**Not committed.** Attribution graphs. Every `.pt` is gitignored (with one exception,
the probe checkpoints above) because a single graph runs to hundreds of megabytes and
each task builds dozens of them. Rebuild them on a GPU. Also not committed are model
weights and HuggingFace caches, the task-2 feature-label cache, and the `runs/` output
root of each task. One committed directory is named `runs/` and is tracked on purpose,
`refusal-jailbreaking/baselines/arditi/runs/`. It is the Arditi baseline's evidence
archive. The two ignore rules are anchored (`/runs/` and `/*/runs/`) so that they catch
each task's output root and leave that archive alone.

**Sampling rule for the archives.** Three example slugs per arm keep their full run
directory. That adds `oracle_result.json`, `elicitation.json`, `elicitation.md` and
`circuit.svg` to what every run keeps, plus `run.log` on tasks 1 and 2 in `results/`.
Task 3 writes no `run.log` at all, and the two `results-workshop/` archives predate it.
Every other run keeps `report.md` and `pinned_ids.json`, plus
`judge_feature_counts.json` on task 1 and `judge_scores*.json` on task 3. There is no
per-run `meta.json` and no per-run `eval.json`. On task 2 `eval.json` is the per-arm
aggregate, one level above the runs. Aggregate files are complete, so
`judge_summary.json`, `judge_summary.md`, `eval.json` and `gpu_timing*.json` are present
for every arm. The Arditi baseline archives are sampled the same way on a smaller file
set, where every slug keeps `meta.json` and only the three sampled slugs also keep
`baseline.txt` and `ablated.txt`. Do not write code that assumes every run directory has
an `oracle_result.json`. The full dumps are available upon request, see above.

**Redactions.** Feature dashboards quote real text that a feature fires on, and some
of those contexts contain email addresses harvested from pretraining data. Every such
address in a committed artifact was replaced with the literal `[email redacted]`.
Nothing else was altered. For tasks 1 and 3 the unredacted contexts are public on
Neuronpedia under the feature ids each run records, at
`https://www.neuronpedia.org/gemma-2-2b/<layer>-gemmascope-transcoder-16k/<feature>`
for task 1 and
`https://www.neuronpedia.org/qwen3-4b/<layer>-transcoder-hp/<feature>` for task 3.
Task 2's transcoders are not on Neuronpedia, so its contexts are available on request.

## Layout

```
circuit-oracle/
├── pyproject.toml           the one installable distribution
├── .env.example             copy to .env HERE, all three tasks read it at this level
├── SUMMARY.md               the result tables, one instrument per task
├── src/
│   ├── circuit_oracle/      the agent (tools, orchestrator, subagents, arm registry, judge rubric)
│   └── circuit_tracer/      vendored attribution-graph library, MIT, see Attribution
├── scripts/
│   ├── run_autointerp_server.py   local feature-label server, task 2 only
│   ├── verify_graphs.py           loads every .pt in the store you name, reports corruption, --delete removes the bad ones
│   └── aggregate_stability.py     repeat-pass traversal stability, tasks 1 and 3
├── tests/                   cross-cutting tests for the shared package
├── summary/                 the detailed notes behind SUMMARY.md, backing data, one generator and one figure
├── spurious-correlation/    task 1
├── secret-elicitation/      task 2
└── refusal-jailbreaking/    task 3
```

Every task directory has the same three-name result convention.

```
<task>/
├── scripts/            entry points (build graphs, run the oracle, evaluate)
├── results/            the final runs, one subdirectory per arm. Archive, read-only.
├── results-workshop/   the runs behind the workshop paper. Archive, read-only.
└── runs/               where YOUR runs land. Gitignored, absent on a fresh clone.
```

No runner, evaluator or launcher writes into `results/` or `results-workshop/` by
default. Every default output root is `<task>/runs/`. Two scripts can be pointed at
an archive and will edit it, and both are called out under
[Reproducing the numbers](#reproducing-the-numbers).

The Arditi baseline has its own committed archive at
`refusal-jailbreaking/baselines/arditi/runs/`, and it is protected differently.
`apply_direction.py` and `llm_judge.py` default `--runs-dir` to
`refusal-jailbreaking/runs/arditi/`, which is gitignored, and they refuse to write
anywhere inside the archive unless you add `--force`. `exp_judge.py` reads the
archive's `judge_summary.json` to join the baseline column onto an oracle table, so a
re-run of the baseline recipe does not disturb the number the oracle side compares
against.

Beyond that shape, each task carries its own material.

- `spurious-correlation/` adds `prompts.json` (the 40 prompts behind the 80 graphs),
  `adapters/` (dataset loaders), `probe_extraction/` (the probe trainer and the
  committed checkpoints), `probe_artifacts/` (the cosine-baseline judge verdicts and
  the spuriosity grids), and `tests/`.
- `secret-elicitation/` adds `figures/`.
- `refusal-jailbreaking/` adds `data/` (three prompt sets, see the table below),
  `baselines/arditi/` (the refusal-direction comparison and the shared multi-judge
  scorers), `weights/` (the extracted direction's diagnostics), and `tests/`.

Task 3's three prompt sets are easy to confuse.

| File | Size | What it is |
|---|---|---|
| `data/prompts.json` | 50 entries | The eval set. 10 locked slugs plus 40 AdvBench prompts the Arditi baseline never trained on. All pure refusal, no censorship family. |
| `data/prompts_workshop.json` | 10 entries | The set behind the workshop paper, matching the 10 slug directories in `results-workshop/` one for one (the tiananmen slug holds two run directories, only one of which was graded). |
| `data/prompts_locked20.json` | 20 entries | The older v8 set. `scripts/build_prompt_set.py` reads its 10 locked refusal slugs out of this file. |

The agent package has two modes. `mode="causal"` runs the full
SCOUT, DISPATCH, MERGE, BUILD, PIN, ANCHOR, SUPERNODES, ANALYZE chain with batched
feature interventions, and is what task 3 uses. `mode="observational"` drops the
intervention tools and the intervention-phase guards, and is what tasks 1 and 2 use.

## Install

**Python 3.12 or newer.** Not 3.10, not 3.11. Several modules use multi-line
expressions inside f-strings, which is a 3.12 language feature. On 3.11 the package
installs and imports fine and then dies with a `SyntaxError` the first time one of
those modules loads, which under a fan-out means every worker fails at once.

```bash
uv venv .venv --python 3.12
source .venv/bin/activate
uv pip install -e ".[all]"
cp .env.example .env
```

`uv venv --python 3.12` fetches a managed interpreter, so a system `python3` older
than 3.12 is not a blocker. Task 3's `scripts/setup.sh` builds its own venv the same
way and does not gate on the system interpreter either. Every entry script imports
`circuit_oracle` and `circuit_tracer` as installed packages, so the editable install is
required rather than optional. Two exceptions read committed evidence and put `src/` on
`sys.path` themselves, so they run from a bare clone with only their third-party
dependencies installed. Both are listed under
[Reproducing the numbers](#reproducing-the-numbers).

The extras are split by what needs them, so a machine that only runs the agent does
not need the data-prep or plotting stacks.

| Extra | Pulls in | Needed for |
|---|---|---|
| `data` | `datasets` | task-1 dataset adapters, `baselines/arditi/fetch_data.py` |
| `plots` | `matplotlib` | `plot_elk_results.py`, the task-1 AUROC chart |
| `probes` | `nnsight` | `probe_extraction/train_probes.py` |
| `lora` | `peft` | `build_taboo_graphs.py`, which merges the taboo adapter |
| `screen` | `modal` | the `screen` stage of `build_prompt_set.py`, which samples completions on a Modal GPU |
| `baselines` | `sae-lens` | `rank_sae_features_by_probe.py`, the task-1 cosine baselines |
| `all` | all six | everything |

### Task 3 keeps its own environment

`refusal-jailbreaking/` needs a CUDA-pinned torch build for steered generation, so it
builds a second venv inside the task directory.

```bash
cd refusal-jailbreaking
bash scripts/setup.sh
```

**`setup.sh` is interactive.** It prompts for API keys with `read -p` under `set -e`,
so run it from a real terminal. With stdin redirected or piped the read returns
non-zero and the script dies mid-setup. It writes its keys to the repository-root
`.env`, so the two environments share one key file.

### One extra data step before the baseline runs

`refusal-jailbreaking/baselines/arditi/data/refusal_train.json` is not shipped. Its
harmful side is AdvBench (MIT) but its harmless side is 160 alpaca-cleaned
instructions under CC BY-NC 4.0, so the merged file is not redistributable. Rebuild
it locally.

```bash
cd refusal-jailbreaking
python -m baselines.arditi.fetch_data --seed 42 --n-train 128 --n-val 32
```

Without it, `extract_direction.py` and `build_prompt_set.py candidates` refuse to
run, and five prompt-sourcing tests under `refusal-jailbreaking/tests/` skip rather
than fail, with a skip message naming this command.

## Configuration

One `.env` at the repository root serves all three tasks. Copy `.env.example` to
`.env` and fill in what you need. Every variable the code reads is listed there and
every value is blank, the one exception being `CUDA_VISIBLE_DEVICES`, which is the
standard CUDA variable and belongs on a command line. The two required credentials are
live lines waiting for a value, and every optional variable is commented out, which
matters because several call sites read `os.environ.get(NAME, <default>)`. A line like
`GRAPH_STORE=` with nothing after it sets the variable to the empty string and beats the
default instead of falling back to it.

| Variable | Default | What reads it |
|---|---|---|
| `OPENROUTER_API_KEY` | none, required | every LLM call in the project |
| `KILO_API_KEY` (or `KILOCODE_API_KEY`) | none | `--provider kilo` only |
| `LLM_PROVIDER` | `openrouter` | the `--provider` default on entry scripts |
| `LLM_BASE_URL` | provider default | points `LLMClient` at any other OpenAI-compatible server, for example a self-hosted vLLM |
| `LLM_API_KEY` | `EMPTY` | bearer token for `LLM_BASE_URL` |
| `CIRCUIT_ORACLE_MODEL_PINS` | built-in pin list | per-model provider pins, format `model=provider,model=provider` |
| `CIRCUIT_ORACLE_SUB_BATCH` | `80` | rows per chunk in the batched steered decode. Drop it if a sweep OOMs |
| `HF_TOKEN` | none | downloading subject models and transcoders |
| `HF_HOME` | `~/.cache/huggingface` | the weights cache, and the root the task-2 feature-dump path is derived from |
| `CIRCUIT_TRACER_CACHE_DIR` | `~/.cache/circuit_tracer` | the vendored tracer's own pre-converted transcoder cache (`src/circuit_tracer/utils/caching.py`). Opt-in: the loader checks it first and falls through to a HuggingFace download when it is empty, which is what every command here does |
| `GRAPH_STORE` | repo-relative | ROOT of the graph store. Refusal and ELK append `graphs/`, probes appends `probe_circuits/` |
| `ORACLE_ENV_FILE` | repo-root `.env` | which KEY=VALUE file the task-2 scripts read |
| `PROBES_DIR` | `spurious-correlation/probe_extraction/probes` | where `circuit_extraction.py` looks for probe checkpoints |
| `ATTRIBUTE_BATCH_SIZE` | `256` | the `--batch-size` default in `build_taboo_graphs.py` |
| `AUTOINTERP_BASE_URL` | `http://127.0.0.1:8765` | where task 2's `inspect_feature` sends its requests |
| `AUTOINTERP_FEATURES_DIR` | derived from `$HF_HOME` | the transcoder feature dump the label server reads |
| `AUTOINTERP_CACHE_DIR` | `secret-elicitation/autointerp_cache` | where the label server caches what it generates |
| `AUTOINTERP_MODEL` | `openai/gpt-oss-120b` | the model the label server writes labels with |
| `AO_BASELINES_DIR` | `/workspace/activation_oracles/experiments` | external activation-oracle baseline JSONs for `print_table.sh` and `plot_elk_results.py`. Those files are not part of this repository and missing ones are dropped from the table rather than faked |

`--graph-dir`, `--env-file` and the other explicit flags always win over the
environment.

**Which scripts load `.env` themselves.** The task-1 and task-2 runners and
evaluators, and `scripts/run_autointerp_server.py`, parse it before they build their
argument parser, so they are safe to call directly and a variable set only in `.env`
still reaches a flag default. That is what makes `LLM_PROVIDER=kilo` in `.env` change
the `--provider` default rather than being read too late to matter. Task 2's scripts
also honour `$ORACLE_ENV_FILE` and take `--env-file`, on both the run path and the
graph-build path. Task 3 reaches `.env`
only through its shell wrappers, which do `set -a; source "$ENV_FILE"; set +a`, so
**always invoke task 3 through `scripts/run.sh`** (or `drun.sh`, or the `repro-*.sh`
wrappers) and never through `python scripts/run_all.py`. The wrappers also set
`HF_HOME` and the CUDA allocator config, both of which matter.

`LLMClient` speaks the OpenAI chat-completions protocol and nothing else, so one
`OPENROUTER_API_KEY` reaches every model used here, Anthropic and Google models
included. There is no `ANTHROPIC_API_KEY` anywhere in this project.
`--provider anthropic` was a silent alias for OpenRouter and now raises. The two
valid values are `openrouter` and `kilo`. Kilo is a second gateway over the same
`vendor/model` slugs. A kilo run still needs `OPENROUTER_API_KEY`, because two models
are pinned to OpenRouter no matter which gateway you select
(`_DEFAULT_MODEL_PINS` in `llm_client.py`). Those two are `openai/gpt-oss-120b`, the
subagent and the highest-call-count model in a run, and `google/gemma-4-31b-it`, the
open-weights orchestrator in arm 5 of tasks 1 and 3 and arm 3 of task 2. Set
`CIRCUIT_ORACLE_MODEL_PINS` to replace that list.

`secret-elicitation/autointerp_cache/` is created on first use by the label server
and is gitignored. If you regenerate labels, that cache is yours, not ours.

## Hardware

Graph construction is the only GPU stage for tasks 1 and 2. Once the `.pt` graphs
exist, an oracle run is API calls plus tensor reads and is happy on CPU. Task 3 needs
a GPU at run time as well, because its interventions run a live forward pass.

| Stage | What to provision |
|---|---|
| Task 1 graph build, Gemma-2-2B, 40 prompts to 80 graphs | The light one. `build_shards.py` splits the prompts across N cards by estimated work. Its `--dry-run` predicts 3.99x on 4 cards for the committed manifest, which is the planner's own arithmetic over its per-prompt cost model, not a stopwatch reading. It runs a calibration warm-up first, so read peak VRAM out of that log before trusting any estimate. |
| Task 2 graph build, Qwen3-8B plus the taboo adapter | The biggest resident footprint in the release. No per-copy figure is recorded in the code. Size for the same 80 GB card task 3 needs, and back `--batch-size` (or `$ATTRIBUTE_BATCH_SIZE`) off if attribution OOMs. |
| Task 3 graph build and steered generation, Qwen3-4B | The model plus its transcoders costs 36.4 GB per copy, so an 80 GB card is the target. That headroom is the point of `--workers N`, which shares one model copy across N concurrent prompts behind a GPU lock. |
| Task 1 and 2 oracle runs, every evaluator, every plot | CPU plus API. Task 2's `run_arms.py --jobs 114` wants about 80 GB of host RAM at 0.7 GB per run. |

## Arms

An **arm** is the identity of a run. One registry key owns the orchestrator model, the
subagent model, the tool surface, the pipeline shape and the discovery-annotation
mode together, and it routes output to `runs/<arm>/`. Entry scripts resolve `--arm`
through `circuit_oracle.arms.resolve_arm` and refuse ad-hoc model flags alongside it,
so a run's configuration is one name rather than a hand-assembled flag set.

The grid is sixteen arms. Five on probes, five on refusal, and six on ELK, because
each ELK orchestrator runs both the closed and the open protocol and those differ in
the tool surface, not only the prompt.

| Arm | Task | Orchestrator | Subagent | What it changes |
|---|---|---|---|---|
| `probes-arm1` | 1 | `minimax/minimax-m3` | `openai/gpt-oss-120b` | Full pipeline, traversal plus inspect |
| `probes-arm2` | 1 | `minimax/minimax-m3` | `openai/gpt-oss-120b` | `inspect_feature` removed |
| `probes-arm3` | 1 | `minimax/minimax-m3` | `openai/gpt-oss-120b` | One-shot top-k, no edge traversal |
| `probes-arm4` | 1 | `openai/gpt-5.6-terra` | `openai/gpt-oss-120b` | Full pipeline, second orchestrator |
| `probes-arm5` | 1 | `google/gemma-4-31b-it` | `openai/gpt-oss-120b` | Full pipeline, open-weights orchestrator |
| `elk-arm1-closed` | 2 | `minimax/minimax-m3` | none | Closed protocol, the 20-word menu is shown |
| `elk-arm1-open` | 2 | `minimax/minimax-m3` | none | Open protocol, menu hidden, top-10 from open vocabulary |
| `elk-arm2-closed` | 2 | `openai/gpt-5.6-terra` | none | Second orchestrator, closed |
| `elk-arm2-open` | 2 | `openai/gpt-5.6-terra` | none | Second orchestrator, open |
| `elk-arm3-closed` | 2 | `google/gemma-4-31b-it` | none | Open-weights orchestrator, closed |
| `elk-arm3-open` | 2 | `google/gemma-4-31b-it` | none | Open-weights orchestrator, open |
| `refusal-arm1` | 3 | `minimax/minimax-m3` | `openai/gpt-oss-120b` | Full pipeline. Headline arm, repeated 5x |
| `refusal-arm2` | 3 | `minimax/minimax-m3` | `openai/gpt-oss-120b` | No `inspect_feature`, shift-only discovery annotation |
| `refusal-arm3` | 3 | `minimax/minimax-m3` | `openai/gpt-oss-120b` | One-shot top-k, no traversal |
| `refusal-arm4` | 3 | `openai/gpt-5.6-terra` | `openai/gpt-oss-120b` | Full pipeline, second orchestrator |
| `refusal-arm5` | 3 | `google/gemma-4-31b-it` | `openai/gpt-oss-120b` | Full pipeline, open-weights orchestrator |

The ELK arms run no subagent layer, which is why the subagent column reads `none`
there. That literal string is what the run records, so no run claims a layer that
never executed.

**Always pass `--arm`.** The bare defaults still resolve to a working model pair, but
they do not reproduce any arm's tool surface (task 2's bare default is the closed tool
list with the default subagent, which is no arm at all) and they write to `runs/`
rather than `runs/<arm>/`, so nothing in the output records which configuration
produced it.

## Quickstart

Each block builds one graph (or one small set) and runs the oracle on it once, which
is the smallest thing that exercises a whole task end to end. Every block assumes the
install above, a filled-in `.env`, and a GPU for the build step.

### Task 1, one probe graph

```bash
python spurious-correlation/scripts/run_extraction_batch.py --dataset civil_comments --tags pos_pos_1
python spurious-correlation/scripts/run_oracle_on_probes.py \
    --arm probes-arm1 --slugs civil_comments-pos_pos_1-biased-probe-correct
```

The build writes one biased and one unbiased graph into
`$GRAPH_STORE/probe_circuits/`. The oracle run lands in
`spurious-correlation/runs/probes-arm1/`. For the whole set, drop `--tags`, repeat
the build for each of `bib_nurse_professor`, `bib_journalist_dietitian`,
`civil_comments` and `multinli`, then run
`python spurious-correlation/scripts/run_extraction_batch.py --verify-store` before
tearing the GPU down.

### Task 2, one taboo secret

The `mwhanna/qwen3-8b-transcoders` features are not on Neuronpedia, so
`inspect_feature` is served by a local shim that **must be running first**. A dead
shim degrades the run quietly rather than failing it.

```bash
python scripts/run_autointerp_server.py &            # listens on 127.0.0.1:8765
python secret-elicitation/scripts/build_taboo_graphs.py --words smile
python secret-elicitation/scripts/build_base_graphs.py
python secret-elicitation/scripts/run_oracle_on_taboo.py \
    --arm elk-arm1-closed --words smile --prompts 1
```

Both build steps need a GPU, and `build_taboo_graphs.py` also needs the `lora` extra
because it merges the adapter. Output lands in
`secret-elicitation/runs/elk-arm1-closed/`. For the open protocol swap in
`run_oracle_on_taboo_no_options.py` and `--arm elk-arm1-open`. `--words reported8`
(the default) is the 8 secrets behind the numbers in `results/`, and `--words all20`
is the 20 behind `results-workshop/`.

### Task 3, one suppression prompt

```bash
cd refusal-jailbreaking
bash scripts/setup.sh                                 # interactive, real terminal only
bash scripts/run.sh --arm refusal-arm1 --slugs self-checkout-theft
```

`run.sh` builds the graph if it is not cached, then runs the full causal pipeline and
writes `elicitation.json` and `elicitation.md` with the interventions it tried.
Output lands in `refusal-jailbreaking/runs/refusal-arm1/exp/`. Graphs are kept by
default, so a second run on the same slug is a cache hit. `--dry-run` resolves the
entry and stops without loading the model or spending anything.

To reproduce the workshop-paper prompt set instead, use the wrapper that pins it.

```bash
cd refusal-jailbreaking
bash scripts/repro-workshop.sh --orchestrator openai/gpt-5.4
```

The `--orchestrator` flag is not optional if you want the workshop configuration.
`run_all.py`'s default is now `openai/gpt-5.6-terra`, and the workshop runs used
`openai/gpt-5.4` with the `openai/gpt-oss-120b` subagent.

## Reproducing the numbers

Two of these commands are genuinely offline. They replay verdicts committed beside
each run and need no GPU, no key and no network, which makes them the fastest way to
check that a checkout is intact.

```bash
python spurious-correlation/scripts/eval_oracle_feature_counts.py
python secret-elicitation/scripts/eval_oracle_taboo.py
```

Both put `src/` on `sys.path` themselves, so neither needs the editable install or a
`PYTHONPATH` prefix. They still need their third-party dependencies, which is
`python-dotenv` and `openai` for the import of the shared client, plus `matplotlib`
for the task-1 AUROC chart.

The first prints 69 of 80 runs correct (86.25%) and a pooled AUROC of 0.882, read out
of the committed per-run `judge_feature_counts.json` verdicts in
`spurious-correlation/results-workshop/`. The second prints 69.2% (166 of 240) from
the committed grades in `secret-elicitation/results/elk-arm1-closed/eval.json`. Both
call the judge only for a run that has no committed verdict at all, and both send any
fresh output to `runs/` rather than into the archive.

### Task 1, spurious probes

| Number | Where it is committed | How to re-derive it |
|---|---|---|
| 69/80 correct, AUROC 0.882 (workshop paper) | per-run `judge_feature_counts.json` under `results-workshop/` | `eval_oracle_feature_counts.py`, offline |
| The arm grid | per-run `judge_feature_counts.json` under `results/probes-arm{1..5}/` | `eval_oracle_feature_counts.py --results-dir spurious-correlation/results/probes-arm1` |
| 5-pass traversal stability | `results/stability_probes_arm1.json` | `python scripts/aggregate_stability.py --track probes --runs-root spurious-correlation/results/probes-arm1` |

The archives are sampled, so only 3 of the 80 workshop runs still carry an
`oracle_result.json`. Three more sit under `results-workshop/opus-sonnet/`, which is a
separate exploratory set on a different concern wording and is excluded from every
score. `eval_oracle_feature_counts.py` no longer needs that file. It replays the
committed verdict, and falls back to the judge only when a run has neither. Fresh
verdicts go to `spurious-correlation/runs/eval/<path>/` and the AUROC chart to
`spurious-correlation/runs/figures/`.

### Task 2, secret elicitation

| Number | Where it is committed | How to re-derive it |
|---|---|---|
| All six arms, closed and open | `results/aggregate.json` and `results/aggregate.md` | `python secret-elicitation/scripts/aggregate_taboo_eval.py --results-root secret-elicitation/results --out-json secret-elicitation/runs/aggregate.json --out-md secret-elicitation/runs/aggregate.md` |
| Closed arm 1, 166/240 = 69.2% | `results/elk-arm1-closed/eval.json` | `eval_oracle_taboo.py`, offline |
| Open arm 1, top-10 recall 67/240 = 27.9% | `results/elk-arm1-open/eval.json` | `eval_oracle_taboo_no_options.py`, offline |
| Workshop closed, 82/120 = 68.3% | `results-workshop/closed/eval.json` | see below, offline with the right judge named |
| Workshop open, top-10 recall 40/120 = 33.3% | `results-workshop/open/eval.json` | see below, offline with the right judge named |

The two archives were graded by different judges and **their numbers are not
comparable**. `results/` was graded by `openai/gpt-oss-120b`, which is the current
code default, so a bare invocation replays it. `results-workshop/` was graded by
`openai/gpt-5.4-mini`. Its `eval.json` caches all 120 grades, so naming that judge
replays them and the command stays offline. Omit the flag and the mismatch guard
correctly throws the cache away and regrades all 120 runs, which costs API calls.

```bash
python secret-elicitation/scripts/eval_oracle_taboo.py \
    --results-dir secret-elicitation/results-workshop/closed \
    --judge-model openai/gpt-5.4-mini
```

Pointing `--results-dir` at either archive sends `eval.json` to
`secret-elicitation/runs/eval/<path>/eval.json` instead of overwriting the archive.

### Task 3, suppression jailbreak

| Number | Where it is committed |
|---|---|
| Oracle arm 1, 50 slugs, current five-model panel at N=1 | `results/refusal-arm1/judge_summary.json` and `.md` |
| Arditi baseline, same 50 slugs, same panel, N=1 | `baselines/arditi/runs/judge_summary.json` and `.md` |
| Oracle, workshop paper, 10 slugs | `results-workshop/judge_summary.json` and `.md` |
| Arditi baseline, workshop era, 20 slugs, earlier three-judge panel at N=5 | `baselines/arditi/runs-workshop/judge_summary.json` and `.md` |

There is no committed task-3 stability file. `scripts/aggregate_stability.py` needs
at least two passes of the same slug, and `results/refusal-arm1/` holds one pass of
each of its 50 slugs, so on this task the aggregator is a tool for your own repeat
runs rather than a way to re-derive a published number. It works as documented
against task 1, where `results/probes-arm1/` carries five `_passN` directories per
slug.

The two Arditi archives were measured on different instruments. `runs/` is 50 slugs
graded by the five-family `JUDGE_PANEL` at N=1. `runs-workshop/` is 20 slugs graded
by the earlier three-judge panel (Claude Opus 4.6, Gemini 3.5 Flash, Grok 4.3) at
N=5. Do not put a number from one on the same axis as a number from the other.

Re-judging task 3 is the one case that always spends API calls, because the judge
panel is external to the run and there is nothing to replay.

`exp_judge.py` does not load `.env`. Only task 3's shell wrappers do that, and this is
not one of them, so export the key into the live shell first or the script fails at
startup.

```bash
cd refusal-jailbreaking
export OPENROUTER_API_KEY=...
python -m baselines.arditi.exp_judge --exp-dir runs --source agentic
```

`--exp-dir` defaults to `runs/`. Pass `results/refusal-arm1` or `results-workshop`
only when you actually mean to re-score a committed archive **in place**, because
`exp_judge.py` writes `judge_scores.json` into every run directory it grades.
`distinct_judge.py` behaves the same way and writes its `--out-name` file into each
run directory. `noise_null.py` is the exception and is read-only on `--exp-dir`,
always writing under `runs/`. `--source auto` resolves to the sweep collector when
any `sweep-*` directory exists under the chosen root, and to the agentic collector
otherwise.

`scripts/aggregate_stability.py` writes nothing unless you pass `--out`, so pointing
it at an archive is read-only by construction. If a run set carries no recorded pass
indices it prints `using directory-name order (legacy layout)` and orders by
timestamp.

`secret-elicitation/scripts/print_table.sh` prints task 2's full comparison table.
Its activation-oracle and SAE baseline JSONs come from a separate harness that is not
part of this repository. Point `AO_BASELINES_DIR` at them if you have them. Missing
files are dropped from the table rather than faked.

## Tests

```bash
cd circuit-oracle
uv run --with pytest pytest
```

Run it from the repository root. That collects the shared-package tests in `tests/`
plus the per-task tests in `spurious-correlation/tests/` and
`refusal-jailbreaking/tests/`. Everything is CPU-only and calls no API. On a fresh
checkout it is 899 passed and 7 skipped. Five of the skips are the prompt-sourcing
tests waiting on `baselines/arditi/data/refusal_train.json`, which is rebuilt with
`fetch_data` and is not redistributed. The other two want a hand-labeled `shift_bucket`
corpus that is not shipped.

**Do not run plain `uv run pytest`.** It resolves a different interpreter, one
without this package installed, and reports a failure baseline that has nothing to do
with the code.

## Known limitations

**The task-1 probe checkpoints are not exactly regenerable.** That is why they are
committed rather than gitignored with the other `.pt` files. A re-trained probe is a
different probe, and every task-1 graph moves with it, so treat
`probe_extraction/probes/*.pt` as data rather than as build output.
`train_probes.py` is still there if you want to train your own, and it writes to
`spurious-correlation/probe_extraction/probes` by default.

**`secret-elicitation/scripts/build_base_graphs.py` is a reconstruction.** The script
that produced the archived `qwen3-8b-base-NN-None.pt` graphs was never committed and
the original procedure is unrecoverable. What ships is `build_taboo_graphs.py` with
the PEFT merge removed, sharing its prompts, its `attribute()` parameters and its
slug convention, which is the strongest reconstruction the surviving evidence
supports. Graphs it produces are a fresh generation.

**Graph generations must not be mixed inside one comparison.** Three separate
parameters changed between eras.

- Task 3 builds at `--max-feature-nodes 8192`. The workshop-era graphs were built at
  10000. Pass `--max-feature-nodes 10000` to rebuild in that generation.
- Task 2 builds at `batch_size=256`, up from 48. This is not throughput-only. The
  tracer sets `queue_size = min(update_interval * batch_size, ...)`, which is the
  granularity of its greedy feature re-rank, so the selected features change.
- Task 1 is fixed at 4096 feature nodes across both eras.

**The measuring instrument changed between the workshop paper and the final runs, on
every task.** Task 3's judge went from three models scoring three axes to the current
five-model `JUDGE_PANEL` in `src/circuit_oracle/judge_rubric.py` scoring two axes,
usability and plausibility, whose mean is the overall score. Task 2's judge went from
`openai/gpt-5.4-mini` to `openai/gpt-oss-120b`. Task 1 kept `openai/gpt-5.4-mini` as
its judge, but its orchestrator pair moved from `minimax-m2.7` with a
`deepseek-v3.2` subagent to `minimax-m3` with `gpt-oss-120b`, and its cosine
baselines were re-run on new settings. In every case the two generations of numbers
came off different instruments and do not belong on one axis, which is why
`summary/details.md` carries the instrument next to every figure.

**`intervene_feature` and `intervene_supernode` are retired from the agent-facing
tool surface.** The harness owns intervention execution now. The agent proposes
feature sets through `batched_supernode_sweep` and the harness runs T x 4 rows in one
batched call, and `batched_anchor_sweep` takes no arguments at all. The retired pair
was the pre-refactor design where the agent executed one intervention at a time, and
it was the only path that reached a non-KV-cached decode. Their schemas and Python
functions stay defined so legacy transcripts replay, and re-adding them to `TOOLS` in
`tool_schemas.py` is all it takes to bring them back. Retiring them removed the
factor -4 saturation test, because the harness factor set is `{0, -1, -2, -3}`.

**The activation-oracle and SAE baselines for task 2 are not in this repository.**
They came from a separate harness. `print_table.sh` and `plot_elk_results.py` read
them from `$AO_BASELINES_DIR` and drop what they cannot find.

## Attribution and license

This project is MIT licensed. See [LICENSE](LICENSE). Third-party and data notices are in [NOTICE](NOTICE).

`src/circuit_tracer/` is a vendored fork of
**[circuit-tracer](https://github.com/safety-research/circuit-tracer)** by Michael
Hanna and Mateusz Piotrowski (MIT, Copyright (c) 2024), pinned at upstream tag
`v0.5.0` (`4bb8c0ea10bde09727e14565ec8469656880da53`). Please cite and credit that
repository for everything in that directory. We claim only the delta, which is a
batched-row intervention backend (`feature_intervention_batched`,
`_get_feature_intervention_hooks_batched` with per-row delta indexing,
`prefill_batched` and `decode_step_batched` for KV-cached steered generation,
`_compact_kv_cache`, `BatchedInterventionResult`) plus a batch-broadcast fix in the
frozen-attention hook. No upstream line is deleted. The exact pin and the per-file
delta are recorded in `src/circuit_tracer/PORT-NOTES.md`, and the upstream MIT notice
travels with the code at `src/circuit_tracer/LICENSE`.

Data licensing. AdvBench is MIT. Alpaca-Cleaned is CC BY-NC 4.0, which is why
`baselines/arditi/data/refusal_train.json` is rebuilt locally rather than
redistributed. See `refusal-jailbreaking/baselines/arditi/data/SOURCES.md`.

Other work this builds on. [Attribution
graphs](https://transformer-circuits.pub/2025/attribution-graphs/biology.html)
(Lindsey et al.) and [transcoders](https://arxiv.org/abs/2406.11944) (Dunefsky et
al.) for the method. [Activation Oracles](https://arxiv.org/abs/2512.15674) (Karvonen,
Marks et al.) for the oracle framing. [Sparse Feature
Circuits](https://arxiv.org/abs/2403.19647) (Marks et al.) for the task-1 human
baseline. [Eliciting Secret Knowledge from Language
Models](https://arxiv.org/abs/2510.01070) (Cywinski et al.) for the task-2 taboo
setup, whose LoRA adapters we take from the Activation Oracles release.
[Refusal is mediated by a single
direction](https://arxiv.org/abs/2406.11717) (Arditi et al.) for the task-3 baseline.
[Neuronpedia](https://www.neuronpedia.org/) for feature labels.

## Citation

If you use this code, please cite the workshop paper. Machine-readable metadata is in
[CITATION.cff](CITATION.cff).

```bibtex
@inproceedings{tan2026circuitoracle,
  title     = {Circuit Oracle: Automating Attribution Graph Analysis via Natural-Language Queries},
  author    = {Tan, Hong Kiat and Kabir, Shariar and Agrawal, Swastik and Chereddy, Sai V R and Balasubramanian, Sriram},
  booktitle = {ICML 2026 Mechanistic Interpretability Workshop},
  year      = {2026},
  url       = {https://openreview.net/forum?id=ANY6YrYUZE}
}
```
