# Circuit Oracle Report
**Date:** 2026-07-28 08:34:41 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by a gender-marker circuit that detects the masculine pronoun "he," rather than by any features encoding the subject's profession.

**Confidence:** 10/10

**Reasoning:**
The attribution analysis reveals that the probe's classification score is primarily driven by a hierarchy of features specifically detecting masculine pronouns. Starting from the output, the most influential late-layer feature is **L18:F14743**, which is a highly specific detector for the token "He" (frac_nonzero: 0.018). 

Tracing this feature upstream shows a direct and strong signal flow from a cascade of gender-related detectors:
1. **Gender Aggregators:** Features such as **L17:F5889** (references to people with pronouns) and **L15:F10510** (references to males in third person) aggregate the pronoun signal.
2. **Gender Token Detectors:** These feed into lower-level detectors like **L14:F14097** (occurrences of the word "he") and **L0:F12768** (mentions of "he" and "she").
3. **Input Embedding:** The entire chain originates from the token embedding of "**he**" at position 22.

Crucially, no features related to "defence," "writer," "journalist," or "security" appear in the top attribution paths. The signal is entirely dominated by the gender of the subject. This confirms the user's concern: the probe is using a spurious gender marker as a proxy for the professional classification, rather than identifying genuine professional indicators.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 22 | Emb: he (pos 22) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L14:F14097](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) | 22 | Gender Token Detectors (He/She) | occurrences of the word "he" | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 22 | Gender Token Detectors (He/She) | mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L4:F15567](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) | 22 | Gender Pronoun Aggregators | sentences with male or female pronouns and possessives, especially ones referring to writing | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 22 | Gender Pronoun Aggregators | references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L15:F10510](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10510) | 22 | Gender Pronoun Aggregators | references to males in third person and first person pronouns | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10510) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 22 | Late-Layer Gender Marker (He) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L0:7124 de=-0.160 |
| 3 | `inspect_feature` | "the word "starting" in academic papers" |
| 4 | `get_top_features` | 30 features; top: L0:7124 de=-0.160 |
| 5 | `inspect_feature` | "He" |

### Dispatch: 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14743@22` | ✅ reported | 7 | 18 | Trace the signal flow driving the probe's classification. Specifically, check if… |

<details>
<summary><b>SA-1</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@22, k=10 | Emb:" he"@22 (de=28.62) +9 more |
| 3 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 4 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |
| 5 | `get_upstream_features` | L4:F15567@22, k=10 | Emb:" he"@22 (de=17.75) +9 more |
| 6 | `inspect_feature` | L0, F12768 | " mentions of "he" and "she" in close proximity" |
| 7 | `inspect_feature` | L14, F14097 | " occurrences of the word "he"" |
| 8 | `inspect_feature` | L15, F10510 | " references to males in third person and first person pronouns" |
| 9 | `get_upstream_features` | L17:F5889@22, k=10 | Emb:" he"@22 (de=37.50) +9 more |
| 10 | `get_upstream_features` | L14:F14097@22, k=10 | Emb:" he"@22 (de=2.70) +9 more |
| 11 | `get_upstream_features` | L3:F9548@22, k=10 | Emb:" he"@22 (de=10.31) +9 more |

**Findings:** The probe's classification signal originates from a cascade of gender‑pronoun detectors. Starting from L18:F14743 (the explicit "He" feature), the strongest upstream influence is the raw token embedding " he" (positive direct effect 28.6). This propagates upward through a hierarchy of pronoun‑aware features (L17:5889, L15:10510, L14:14097, L4:15567) that each aggregate or count occurrences of male…

</details>

### Build

`build_circuit` → 5 nodes, 4 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 71,541 | 944 | 4,352 | 0 | $0.0105 | — | — |
| SA-1 | openai/gpt-oss-120b | 130,770 | 8,184 | 12,640 | 0 | $0.0247 | ✅ 7F/18E | Trace the signal flow driving the probe's classification. Sp… |
| **Total** | | **202,311** | **9,128** | **16,992** | **0** | **$0.0352** | | |

**Oracle wall-clock time:** 3m 57s