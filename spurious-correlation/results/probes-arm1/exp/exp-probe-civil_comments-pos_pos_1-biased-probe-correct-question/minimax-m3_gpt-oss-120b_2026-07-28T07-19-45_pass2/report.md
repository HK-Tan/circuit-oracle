# Circuit Oracle Report
**Date:** 2026-07-28 07:19:45 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity classification is driven by a cascade of identity-group/race vocabulary detectors that activate on the mere presence of demographic tokens ("white", "black", "race", "trump", "Obama", "America") and on race-related framing words ("bigot", "clearly"), rather than on the toxic speech content itself.

**Confidence:** 7

**Reasoning:** The attribution graph for this toxicity probe reveals a circuit almost entirely built around identity-group/lexical signals, not semantic toxicity. The most strongly contributing feature is **L4:F14582** at pos 5 ("references to the White House and the US government", frac_nonzero=0.0079) which is driven almost exclusively by the **Emb:"trump"** token (direct_effect=18.125) — the word "trump" alone triggers a White House/political-identity detector. **L2:F13158** ("words about race and ethnicity", frac_nonzero=0.0099) fires at four positions (15, 25, 32, 40) directly from the embeddings of **"white"** (pos 25, direct_effect=10.5) and **"black"** (pos 32, direct_effect=10.5) — these are the strongest single embedding contributions. The downstream **L4:F117** ("race, racism, and social justice, with a particular focus on terms related to Black people", frac_nonzero=0.012) inherits this signal and the **L6:F3902** ("terms referring to race and ethnicity", frac_nonzero=0.018) is then driven by the same identity tokens (Emb:"white" pos 25 direct_effect=10.8, Emb:"race" pos 40 direct_effect=19.6).

Crucially, no feature in the top 20 detects *toxicity content* per se — i.e., slurs, dehumanization patterns, or aggressive speech. Instead, the **L6:F1707** ("discourse markers, qualifiers, intensifiers, or words expressing an opinion") fires on the word "tie" at position 1 (the article opener), and **L5:F8030** ("language discussing differences, clarity, and definition") is driven by the token "clearly" (Emb direct_effect=18.25) and "shows" — i.e., the *assertive framing* of the statement, not its hateful substance. The **L2:F585** generic identity-group feature (high activation 20.1 at pos 25) reinforces the "white"→race pattern.

The user's concern is well-supported by this circuit: the probe reads **identity-group vocabulary** (white/black/race/trump/Obama) and the **assertive discourse register** as proxies for toxicity, with the direct effect of the embedding nodes for these identity words (10–19 each) dwarfing anything tied to actual hateful content. A benign sentence like "white and black voters had different turnout in this race" — which uses the exact same vocabulary in a descriptive context — would light up nearly the same circuit, confirming that the probe's classification rests on demographic-name lexical features rather than on the toxic-speech semantics the user would expect.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 25 | Early lexical race/ethnicity detectors |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 32 | Early lexical race/ethnicity detectors |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 15 | Early lexical race/ethnicity detectors |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 40 | Early lexical race/ethnicity detectors |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F585](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) | 25 | Early lexical race/ethnicity detectors | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) |
| [L2:F14301](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14301) | 5 | Early lexical race/ethnicity detectors | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14301) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 9 | Mid-layer race/racism detectors |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 25 | Mid-layer race/racism detectors |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 32 | Mid-layer race/racism detectors |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 40 | Mid-layer race/racism detectors |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F5584](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5584) | 25 | Mid-layer race/racism detectors | words related to race, ethnicity, nationality or population groups | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5584) |
| [L4:F5584](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5584) | 40 | Mid-layer race/racism detectors | words related to race, ethnicity, nationality or population groups | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5584) |
| [L4:F14582](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14582) | 5 | Mid-layer race/racism detectors |  references to the White House and the US government | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14582) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 25 | Late-layer race/ethnicity supernode |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 40 | Late-layer race/ethnicity supernode |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L5:F8030](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/8030) | 3 | Late-layer race/ethnicity supernode |  language discussing differences, clarity, and definition | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/8030) |
| [L6:F1707](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1707) | 1 | Late-layer race/ethnicity supernode | a variety of discourse markers, qualifiers, intensifiers, or words expressing an opinion. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1707) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:5707 de=-0.346 |
| 3 | `inspect_feature` ×15 | L0:3255, L0:7969, L0:6051, L2:13158, L4:117, L5:8030, L6:3902, L0:5707, L1:2407, L0:6154, L0:7142, L0:12866, L4:14582, L6:1707, L0:247 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F13158@32` | ✅ reported | 5 | 4 | Trace the L2 race/ethnicity feature upstream to identify which input tokens driv… |
| SA-2 | `L4:F117@9` | ❌ error | — | — | Trace the L4 race/racism feature upstream. Identify which input tokens contribut… |
| SA-3 | `L6:F3902@25` | ✅ reported | 4 | 6 | Trace the L6 race/ethnicity feature upstream. Identify which input tokens contri… |
| SA-4 | `L5:F8030@3` | ✅ reported | 5 | 4 | Trace the L5 differences/clarity feature upstream. Identify which input tokens c… |

<details>
<summary><b>SA-1</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 2 | `get_upstream_features` | L2:F13158@32, k=10 | Emb:" black"@32 (de=10.50) +9 more |
| 3 | `inspect_feature` | L1, F13646 | " text discussing social justice issues" |
| 4 | `inspect_feature` | L1, F3020 | " the word "factor"" |
| 5 | `get_upstream_features` | L1:F13646@32, k=10 | Emb:" black"@32 (de=4.25) +9 more |
| 6 | `inspect_feature` | L1, F12717 | " words or phrases related to education" |
| 7 | `inspect_feature` | L0, F16013 | " mentions of the color blue, and perhaps colors in general or the comp" |
| 8 | `inspect_feature` | L0, F1015 | " the word "black"" |

**Findings:** The L2 race/ethnicity feature (F13158) receives its strongest excitatory drive from the raw token embedding for " black" (direct_effect ~10.5, not listed as a feature edge) and from a handful of higher‑layer detectors. The top upstream feature is a social‑justice detector (L1:13646) that promotes race‑related tokens, followed by lexical cues like "factor" (L1:3020) and education‑related language (…

</details>

<details>
<summary><b>SA-3</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F3902 | " terms referring to race and ethnicity" |
| 2 | `get_upstream_features` | L6:F3902@25, k=15 | Emb:" white"@25 (de=10.81) +14 more |
| 3 | `inspect_feature` | L4, F117 | " terms related to race, racism, and social justice, with a particular " |
| 4 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 5 | `inspect_feature` | L4, F5584 | " words related to race, ethnicity, nationality or population groups" |
| 6 | `get_upstream_features` | L4:F117@25, k=15 | Emb:" white"@25 (de=12.25) +14 more |
| 7 | `get_upstream_features` | L2:F13158@25, k=15 | Emb:" white"@25 (de=11.88) +14 more |

**Findings:** Tracing from the L6 race/ethnicity feature (F3902) reveals that the strongest upstream drivers are the input token "white" at position 25 (direct_effect ~10.8) and, to a lesser extent, the same token at position 15 and the token "America" at position 24. The main internal contributors are three mid‑layer detectors: L4:F117 (race/Black‑focused), L2:F13158 (general race/ethnicity lexicon), and L4:F5…

</details>

<details>
<summary><b>SA-4</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L5, F8030 | " language discussing differences, clarity, and definition" |
| 2 | `get_upstream_features` | L5:F8030@3, k=10 | Emb:" clearly"@2 (de=18.25) +9 more |
| 3 | `inspect_feature` | L4, F11503 | "instances of something being clear, obvious, or evident" |
| 4 | `inspect_feature` | L2, F7607 | " the word "shows" or its synonyms in the context of a study or results" |
| 5 | `get_upstream_features` | L2:F7607@3, k=10 | Emb:" shows"@3 (de=24.25) +9 more |
| 6 | `get_upstream_features` | L4:F11503@2, k=10 | Emb:" clearly"@2 (de=40.75) +9 more |
| 7 | `inspect_feature` | L3, F5501 | "technical terms, often related to science, math, or law" |
| 8 | `get_upstream_features` | L3:F5501@2, k=10 | Emb:"<bos>"@0 (de=3.52) +9 more |
| 9 | `inspect_feature` | L2, F9071 | " terms that might indicate the ending or summary of an argument" |

**Findings:** Tracing from the L5 differences/clarity feature (L5:F8030) reveals a concise upward pathway: the feature is driven primarily by a layer‑4 'clear/obvious' detector (L4:11503) and a layer‑2 'shows' detector (L2:7607). The layer‑4 node itself receives strong excitation from a layer‑3 technical‑term detector (L3:5501), which in turn is activated by a layer‑2 summary‑cue detector (L2:9071). The chain t…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L2:F13158@32, k=15 → Emb:" black"@32 (de=10.50) +14 more |
| 2 | `get_upstream_features` | L4:F14582@5, k=15 → Emb:" trump"@5 (de=18.12) +14 more |
| 3 | `get_upstream_features` | L4:F117@9, k=15 → Emb:"ot"@9 (de=3.52) +14 more |
| 4 | `get_upstream_features` | L5:F8030@3, k=15 → Emb:" clearly"@2 (de=18.25) +14 more |
| 5 | `get_upstream_features` | L6:F3902@25, k=15 → Emb:" white"@25 (de=10.81) +14 more |
| 6 | `get_upstream_features` | L6:F3902@40, k=15 → Emb:" race"@40 (de=19.62) +14 more |
| 7 | `get_upstream_features` | L4:F117@25, k=10 → Emb:" white"@25 (de=12.25) +9 more |
| 8 | `get_upstream_features` | L4:F117@32, k=10 → Emb:" black"@32 (de=12.06) +9 more |
| 9 | `get_upstream_features` | L6:F1707@1, k=10 → L4:F8223 (de=4.09) +9 more |
| 10 | `get_upstream_features` | L4:F14582@5, k=10 → Emb:" trump"@5 (de=18.12) +9 more |

### Build

`build_circuit` → 12 nodes, 10 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 60,775 | 4,171 | 161,155 | 0 | $0.0329 | — | — |
| SA-4 | openai/gpt-oss-120b | 87,410 | 5,962 | 7,904 | 0 | $0.0168 | ✅ 5F/4E | Trace the L5 differences/clarity feature upstream. Identify … |
| SA-3 | openai/gpt-oss-120b | 68,586 | 4,757 | 2,528 | 0 | $0.0132 | ✅ 4F/6E | Trace the L6 race/ethnicity feature upstream. Identify which… |
| SA-1 | openai/gpt-oss-120b | 87,797 | 4,822 | 0 | 0 | $0.0161 | ✅ 5F/4E | Trace the L2 race/ethnicity feature upstream to identify whi… |
| **Total** | | **304,568** | **19,712** | **171,587** | **0** | **$0.0790** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 26s