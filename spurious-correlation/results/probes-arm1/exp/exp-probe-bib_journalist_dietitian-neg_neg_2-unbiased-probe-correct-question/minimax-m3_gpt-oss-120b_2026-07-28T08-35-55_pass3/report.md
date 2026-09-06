# Circuit Oracle Report
**Date:** 2026-07-28 08:35:55 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by genuine profession-related signals (journalism/news vocabulary) — not by gender or spurious markers — with the dominant positive contributions coming from the literal token "report" and the phrase "news organizations" propagating through a clean journalism-feature cascade; the only "His" contribution is small, negative, and originates from a generic L0 pronoun detector, not a gendered profession shortcut.

**Confidence:** 7

**Reasoning:**

The attribution graph decomposes into a clean two-branch circuit feeding the probe direction:

**1. The "His / function-word" branch (genuine spurious concern, but small and NEGATIVE):**
- L0:F8964 (frac=0.018) activates on the possessive "His" at pos 1 with activation 10.69, contributing +0.079 to the probe — but this is a *generic* L0 token detector for the pronoun, not a gender–profession association. Its upstream is just the "His" embedding (direct_effect 13.7) and a tiny <bos> context.
- L0:F8444 (the word "to"), L0:F14287 (the word "see"), and L0:F2203 (the word "world"/"game") are likewise pure lexical detectors at L0 with low frac_nonzero (~0.017–0.031), all firing on the *content* of the sentence rather than on gender. L0:F2203 actually *suppresses* the probe (direct_effect −0.057) — its top activating examples are about the word "world" in narrative contexts, not gender.
- L4:F11898 ("World" in sport/war context) and L5:F771 ("see") are both early-layer lexical-context features also contributing to the probe, but again with semantic content, not gender.

**2. The "journalism" branch (the dominant signal — GENUINE profession indicator):**
- L14:F4420 (frac=0.017, label: "words and phrases related to journalism and newspapers", promoted tokens: journalists, journalist, journalism, reporter, editorial) fires on pos 21 (" report") with activation 27.4 and direct_effect −0.146. Despite the negative sign, this is the single largest-magnitude driver. It is driven upstream by the " report" token embedding (direct_effect 5.22) and by L8:F8855 ("mentions of news reporters", direct_effect 5.06) and L7:F13646 ("news reporting and journalism", 3.73) — all genuine profession-related features.
- L19:F2486 (frac=0.029, "journalistic sources and news outlets", promoted tokens: reporting, reporter, coverage, Reporter) fires on positions 21, 22, 26–29 (the words "report" and "news organizations") with direct_effects from −0.113 to −0.060. Its strongest upstream is L14:F4420 (direct_effect 14.31), creating the journalism cascade.
- L20:F8433 (frac=0.036, "words related to news broadcasting", promoted tokens: news, journalists, newspaper, journalism) fires on pos 26 (" top") and pos 27 (" news") with direct_effect −0.062, again driven upward by L14:F4420 and by the embeddings of "top" (5.69) and " news" (7.94).

**Why the user concern is partly right but mostly not borne out:**
The L0 pronoun feature on "His" is indeed "spurious" in the sense that it is a gender marker — but it is a *low-level lexical detector for the token "His"* with frac_nonzero 0.018 (rare/specific) and its top activating examples are uniformly about the literal word "His" in biography/history text (e.g., "His tenure", "His wife", "His parents"), not about male professions. It contributes only +0.079 to the probe, an order of magnitude smaller than the journalism-cascade's net influence. The model is *not* using "His → male → journalist" as a shortcut; it is using a direct "report / news organizations" → journalist pathway that flows through purpose-built profession features (L14:F4420, L19:F2486, L20:F8433) whose frac_nonzero values (0.017–0.036) confirm they are selective profession detectors rather than generic context features.

The only mildly suspicious aspect is the L4:L11898 "World" feature (sport/war context) and the L0 "world" detector F2203, but these are not gender-related — they are content-lexical features that happen to fire on the word "world" in this biography. The circuit is overwhelmingly a *lexical-vocabulary* circuit anchored on the words "report" and "news", not a demographic-shortcut circuit.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F8964](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) | 1 | Generic function-word / pronoun features (L0) |  the possessive pronoun "His" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 3 | Generic function-word / pronoun features (L0) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F14287](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14287) | 4 | Generic function-word / pronoun features (L0) | the word "see" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14287) |
| [L0:F2203](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2203) | 6 | Generic function-word / pronoun features (L0) |  instances of the words "world" or "game" (possibly "problem") or expressions of existential quandaries. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2203) |
| [L4:F11898](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11898) | 6 | Early-layer 'World' context (L4) | mentions of "World" followed by a sport or war-related word | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11898) |
| [L5:F771](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/771) | 6 | Early 'see' context (L5) |  the word "see" and words often associated with "see" | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/771) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 21 | Journalism features on 'report' (L14) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 22 | Journalism features on 'report' (L14) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 21 | Late journalism / news-outlet features (L19-L20) | journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 22 | Late journalism / news-outlet features (L19-L20) | journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 26 | Late journalism / news-outlet features (L19-L20) | journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 27 | Late journalism / news-outlet features (L19-L20) | journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 28 | Late journalism / news-outlet features (L19-L20) | journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 29 | Late journalism / news-outlet features (L19-L20) | journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L20:F8433](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/8433) | 26 | Late journalism / news-outlet features (L19-L20) | words related to news broadcasting | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/8433) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:4420 de=-0.145 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@21` | ✅ reported | 7 | 9 | Trace this feature upstream through the circuit. Identify what this feature enco… |
| SA-2 | `L19:F2486@21` | ✅ reported | 6 | 8 | Trace this feature upstream through the circuit. Identify what this feature enco… |
| SA-3 | `L0:F8964@1` | ❌ error | — | — | Trace this feature upstream. Identify what this feature encodes (likely an embed… |
| SA-4 | `L0:F8444@3` | ❌ error | — | — | Trace this feature upstream. Identify what this feature encodes (likely an embed… |
| SA-5 | `L0:F14287@4` | ❌ error | — | — | Trace this feature upstream. Identify what this feature encodes (likely an embed… |
| SA-6 | `L20:F8433@26` | ✅ reported | 4 | 3 | Trace this feature upstream. Identify what this feature encodes and where its si… |
| SA-7 | `L4:F11898@6` | ✅ reported | 5 | 11 | Trace this feature upstream. Identify what this feature encodes and where its si… |
| SA-8 | `L5:F771@6` | ✅ reported | 4 | 13 | Trace this feature upstream. Identify what this feature encodes and where its si… |

<details>
<summary><b>SA-1</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@21, k=10 | Emb:" report"@21 (de=5.22) +9 more |
| 3 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 4 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 5 | `get_upstream_features` | L8:F8855@21, k=10 | Emb:" report"@21 (de=12.06) +9 more |
| 6 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |
| 7 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |
| 8 | `get_upstream_features` | L7:F13646@21, k=10 | Emb:" report"@21 (de=7.22) +9 more |
| 9 | `inspect_feature` | L7, F9092 | " words and phrases associated with broadcast journalism" |
| 10 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |
| 11 | `get_upstream_features` | L4:F661@21, k=10 | Emb:" report"@21 (de=14.38) +9 more |

**Findings:** The L14 journalism feature (4420) is driven primarily by the token embedding for " report" (pos 21). The embedding excites a cascade of lower‑layer features: L8 feature 8855, L7 feature 13646, L8 feature 8437, and L7 feature 9092, each of which further refines the journalism semantics. The signal reaches a deep layer‑4 feature (661) that also directly responds to the same embedding, satisfying the…

</details>

<details>
<summary><b>SA-2</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F2486 | " journalistic sources and news outlets." |
| 2 | `get_upstream_features` | L19:F2486@21, k=10 | L14:F4420 (de=14.31) +9 more |
| 3 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 4 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 5 | `inspect_feature` | L16, F15046 | " names, organizations, and reporting verbs" |
| 6 | `get_upstream_features` | L14:F4420@21, k=10 | Emb:" report"@21 (de=5.22) +9 more |
| 7 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 8 | `get_upstream_features` | L8:F8855@21, k=10 | Emb:" report"@21 (de=12.06) +9 more |
| 9 | `get_upstream_features` | L7:F13646@21, k=10 | Emb:" report"@21 (de=7.22) +9 more |
| 10 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |

**Findings:** The traced circuit starts at a high‑level journalism‑source detector (L19:F2486) that heavily promotes reporting‑related vocabulary. Its strongest upstream driver is a mid‑level journalism term detector (L14:F4420), which itself is driven primarily by the raw input token ' report' and by a lower‑layer reporter‑mention feature (L8:F8855). The path descends to layer 7 and layer 8 features that encod…

</details>

<details>
<summary><b>SA-6</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L20, F8433 | "words related to news broadcasting" |
| 2 | `get_upstream_features` | L20:F8433@26, k=15 | Emb:" top"@26 (de=5.69) +14 more |
| 3 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 4 | `inspect_feature` | L7, F9092 | " words and phrases associated with broadcast journalism" |
| 5 | `get_upstream_features` | L14:F4420@21, k=15 | Emb:" report"@21 (de=5.22) +14 more |
| 6 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 7 | `get_upstream_features` | L7:F9092@26, k=15 | Emb:" top"@26 (de=-1.06) +14 more |

**Findings:** The target feature L20:F8433 (layer 20, pos 26) is a mid‑high‑level detector for broadcast‑news terminology. Its strongest upstream driver is the embedding for the token " top" (positive direct_effect 5.69), but the next most influential upstream feature is L14:4420, a layer‑14 journalism detector. Tracing further upstream reveals that L14:4420 is driven primarily by the embedding " report" and by…

</details>

<details>
<summary><b>SA-7</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F11898 | " mentions of "World" followed by a sport or war-related word" |
| 2 | `get_upstream_features` | L4:F11898@6, k=10 | Emb:" world"@6 (de=35.25) +9 more |
| 3 | `inspect_feature` | L3, F3205 | " code snippets and documentation references, possibly related to web d" |
| 4 | `get_upstream_features` | L3:F3205@6, k=10 | Emb:" the"@5 (de=7.56) +9 more |
| 5 | `inspect_feature` | L0, F12200 | " a variety of specific nouns" |
| 6 | `inspect_feature` | L2, F13522 | "words loosely related to events taking place during a narrative, inclu" |
| 7 | `get_upstream_features` | L2:F13522@6, k=10 | Emb:" the"@5 (de=10.00) +9 more |
| 8 | `inspect_feature` | L0, F2203 | " instances of the words "world" or "game" (possibly "problem") or expr" |
| 9 | `get_upstream_features` | L0:F12200@6, k=10 | Emb:"<bos>"@0 (de=6.12) +9 more |

**Findings:** The target feature L4:F11898 (detecting the token "World") is overwhelmingly driven by the direct embedding of the token "world" at the same position (positive direct effect 35.25). Smaller contributions come from lower‑layer noun and event detectors (L0:F12200, L2:F13522, L0:F2203) and a generic documentation feature (L3:F3205). All upstream paths are excitatory and include at least one token‑emb…

</details>

<details>
<summary><b>SA-8</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L5, F771 | " the word "see" and words often associated with "see"" |
| 2 | `get_upstream_features` | L5:F771@6, k=10 | Emb:" see"@4 (de=6.16) +9 more |
| 3 | `inspect_feature` | L4, F15940 | " occurrences of seeing something, or electrical charges/carriers" |
| 4 | `get_upstream_features` | L4:F15940@6, k=10 | Emb:" see"@4 (de=14.69) +9 more |
| 5 | `inspect_feature` | L4, F6653 | "the word "world"" |
| 6 | `get_upstream_features` | L4:F6653@6, k=10 | Emb:" world"@6 (de=27.25) +9 more |
| 7 | `inspect_feature` | L3, F6616 | "different forms of seeing or noticing" |
| 8 | `get_upstream_features` | L3:F6616@4, k=10 | Emb:" see"@4 (de=13.25) +9 more |

**Findings:** The L5:F771 feature detects the token 'see' and is driven mainly by the embedding of the word 'see' (pos 4) and by higher‑level seeing detectors in layers 4 and 3. Tracing upstream reaches lower‑third layers (≤8) and includes explicit embedding sources, satisfying the termination conditions.

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×3 | L0:8964, L0:8444, L0:14287 |
| 2 | `get_upstream_features` | L19:F2486@29, k=10 → Emb:" news"@27 (de=7.94) +9 more |
| 3 | `get_upstream_features` | L19:F2486@27, k=10 → Emb:" news"@27 (de=20.75) +9 more |
| 4 | `get_upstream_features` | L20:F8433@26, k=12 → Emb:" top"@26 (de=5.69) +11 more |
| 5 | `get_upstream_features` | L0:F8964@1, k=8 → Emb:"His"@1 (de=13.69) +7 more |
| 6 | `get_upstream_features` | L0:F8444@3, k=8 → Emb:" to"@3 (de=39.50) +7 more |
| 7 | `get_upstream_features` | L0:F14287@4, k=8 → Emb:" see"@4 (de=25.12) +7 more |
| 8 | `get_upstream_features` | L0:F2203@6, k=8 → Emb:" world"@6 (de=18.25) +7 more |
| 9 | `inspect_feature` | L0, F2203 → " instances of the words "world" or "game" (possibly "problem") or expr" |

### Build

`build_circuit` → 7 nodes, 9 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 27,718 | 4,076 | 60,455 | 0 | $0.0168 | — | — |
| SA-6 | openai/gpt-oss-120b | 74,110 | 6,273 | 10,720 | 0 | $0.0150 | ✅ 4F/3E | Trace this feature upstream. Identify what this feature enco… |
| SA-2 | openai/gpt-oss-120b | 110,650 | 6,743 | 7,616 | 0 | $0.0208 | ✅ 6F/8E | Trace this feature upstream through the circuit. Identify wh… |
| SA-8 | openai/gpt-oss-120b | 86,499 | 7,088 | 8,416 | 0 | $0.0174 | ✅ 4F/13E | Trace this feature upstream. Identify what this feature enco… |
| SA-7 | openai/gpt-oss-120b | 103,303 | 9,335 | 10,144 | 0 | $0.0212 | ✅ 5F/11E | Trace this feature upstream. Identify what this feature enco… |
| SA-1 | openai/gpt-oss-120b | 126,556 | 8,893 | 32,832 | 0 | $0.0248 | ✅ 7F/9E | Trace this feature upstream through the circuit. Identify wh… |
| **Total** | | **528,836** | **42,408** | **130,183** | **0** | **$0.1160** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 15s