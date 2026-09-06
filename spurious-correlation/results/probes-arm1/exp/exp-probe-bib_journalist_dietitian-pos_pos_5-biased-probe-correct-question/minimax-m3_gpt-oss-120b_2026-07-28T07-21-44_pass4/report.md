# Circuit Oracle Report
**Date:** 2026-07-28 07:21:44 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

I have already built the circuit with embedding nodes (Emb: 'Her' pos 1, ' She' pos 15, ' Heather' pos 46, ' nutrition' pos 7, '<bos>' pos 0). Let me provide the final analysis.

**Analysis:** The probe's classification score is driven almost entirely by features that detect female gender markers — the possessive pronoun "Her" (pos 1), the pronoun "She" (pos 15), the female first name "Heather" (pos 46), and lower-layer capitalized-name/pronoun features — rather than by any feature that encodes the subject-matter profession (dietitian/nutritionist). The text's nutrition-domain vocabulary ("nutrition", "weight management", "Academy of Nutrition and Dietetics") has essentially no presence in the circuit.

**Confidence:** 9/10

**Reasoning:** The top features driving the probe are dominated by female-referent detectors:

- **L6:F11646 (pos 1) and pos 15** — direct_effect +0.49 — "references to women, triggered by pronouns and titles" (frac_nonzero 0.020, promoted tokens: herself, she, her)
- **L18:F14677 (pos 15)** — direct_effect +0.17 — "instances of women or girls being mentioned" (frac_nonzero 0.012, promoted tokens: herself, she, her)
- **L19:F9685 (pos 46)** — direct_effect +0.13 — "references to women's names and their roles" (frac_nonzero 0.014, promoted tokens: herself, she, her)
- **L12:F14970 (pos 46)** — direct_effect +0.16 — "names of people" (frac_nonzero 0.003, general name detector)
- **L7:F8644 (pos 46)** — direct_effect −0.21 — "woman's name in a variety of contexts" (actually suppresses)
- **L4:F1276 (pos 46)** — direct_effect +0.13 — "capitalized names and titles"
- **L4:F7864 (pos 1)** — direct_effect +0.11 — generic token feature firing on "Her"

Tracing these upstream through the circuit reveals that they all bottom out at female-gendered token embeddings: **"Her" (pos 1)**, **" She" (pos 15)**, and **" Heather" (pos 46)**. The single most important mid-layer node L17:F5889 ("references to people with pronouns", frac_nonzero 0.018) receives direct_effect 20.25 from the " She" embedding alone. The L15:F3330 "personal stories of individuals, especially women" receives direct_effect 15.6 from " She" and 2.0 from " Her" and 2.0 from " expertise".

The only feature that could plausibly be a profession indicator is **L4:F13412 (pos 7, on " nutrition")** — "terms related to diets and dietary health" (frac_nonzero 0.012, direct_effect +0.14). This is the lone profession-related feature, and its downstream effect is small compared to the cluster of female-gender features.

The user concern is validated by the circuit: the probe's classification is heavily driven by **spurious gender markers** (pronouns "Her"/"She" and the female first name "Heather") rather than by genuine profession indicators. The circuit shows a clean chain `Emb(Her/She/Heather) → early female-pronoun detectors (L0) → female-entity features (L6-L7) → name/pronoun aggregators (L12-L15) → late "women's names and roles" features (L18-L19) → probe logit`, with the diet/nutrition profession signal present only as a minor side-branch via L4:F13412. The model has likely learned that this profession appears predominantly with female subjects in its training data, and the linear probe picks up the easier gender correlate instead of the more diagnostic professional vocabulary.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'Her' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: ' She' (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 46 | Emb: ' Heather' (pos 46) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: ' nutrition' (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 0 | Emb: '<bos>' (pos 0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 1 | Early-layer female pronoun detectors | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 15 | Early-layer female pronoun detectors |  the pronoun "she" and the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L0:F3232](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3232) | 15 | Early-layer female pronoun detectors |  mentions of the third person plural pronoun "They" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3232) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 46 | Early-layer female pronoun detectors |  proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 46 | Capitalized-name / pronoun features (L4) | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Capitalized-name / pronoun features (L4) | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 7 | Capitalized-name / pronoun features (L4) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Female-referent / women's name features (L6-L7) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 15 | Female-referent / women's name features (L6-L7) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 46 | Female-referent / women's name features (L6-L7) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 46 | Female-referent / women's name features (L6-L7) |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 46 | Name / pronoun features (L12) |  names of people, both first and last names | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L12:F15193](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/15193) | 46 | Name / pronoun features (L12) |  proper names | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/15193) |
| [L13:F6622](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) | 15 | Pronoun / personal-narrative features (L13-L15) |  pronouns. | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) |
| [L14:F5740](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5740) | 15 | Pronoun / personal-narrative features (L13-L15) |  sentences with multiple pronouns in them | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5740) |
| [L14:F8671](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/8671) | 46 | Pronoun / personal-narrative features (L13-L15) |  capitalized names of people | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/8671) |
| [L14:F13478](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/13478) | 46 | Pronoun / personal-narrative features (L13-L15) |  occurrences of people's names, often with titles | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/13478) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 15 | Pronoun / personal-narrative features (L13-L15) |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L15:F13002](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13002) | 46 | Pronoun / personal-narrative features (L13-L15) |  titles and names of people followed by their role or profession | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13002) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 15 | Pronoun reference feature (L17) |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 15 | Women/women's-name features driving probe (L18-L19) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F9023](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/9023) | 46 | Women/women's-name features driving probe (L18-L19) |  personal names and associated titles | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/9023) |
| [L18:F10572](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10572) | 46 | Women/women's-name features driving probe (L18-L19) |  proper nouns, especially names of people and characters | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10572) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 46 | Women/women's-name features driving probe (L18-L19) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L16:F6025](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6025) | 46 | Women/women's-name features driving probe (L18-L19) |  capitalized first names, sometimes followed by last names | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6025) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe score | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11646 de=0.283 |
| 3 | `inspect_feature` ×8 | L6:11646, L18:14677, L12:14970, L7:8644, L4:13412, L19:9685, L4:1276, L4:7864 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@15` | ❌ error | — | — | Trace L18:F14677 (women/girls mentioned, frac_nonzero=0.012, pos 15 - likely on … |
| SA-2 | `L19:F9685@46` | ❌ error | — | — | Trace L19:F9685 (women's names and roles, frac_nonzero=0.014, pos 46 - likely 'H… |
| SA-3 | `L6:F11646@1` | ❌ error | — | — | Trace L6:F11646 (references to women via pronouns/titles, pos 1 - likely 'Her') … |
| SA-4 | `L12:F14970@46` | ❌ error | — | — | Trace L12:F14970 (names of people, pos 46 - likely 'Heather' or similar) upstrea… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14677@15, k=10 → Emb:" She"@15 (de=15.25) +9 more |
| 2 | `get_upstream_features` | L19:F9685@46, k=10 → Emb:" Heather"@46 (de=4.62) +9 more |
| 3 | `get_upstream_features` | L6:F11646@1, k=10 → Emb:"Her"@1 (de=18.12) +9 more |
| 4 | `get_upstream_features` | L12:F14970@46, k=10 → Emb:"<bos>"@0 (de=-5.22) +9 more |
| 5 | `inspect_feature` ×9 | L17:5889, L15:3330, L0:15382, L6:16329, L16:6025, L18:9023, L18:10572, L7:2765, L0:7532 |
| 6 | `get_upstream_features` | L4:F1276@46, k=10 → Emb:" Heather"@46 (de=11.12) +9 more |
| 7 | `get_upstream_features` | L4:F7864@1, k=10 → Emb:"Her"@1 (de=14.75) +9 more |
| 8 | `get_upstream_features` | L4:F13412@7, k=10 → Emb:" nutrition"@7 (de=12.62) +9 more |
| 9 | `get_upstream_features` | L17:F5889@15, k=10 → Emb:" She"@15 (de=20.25) +9 more |
| 10 | `inspect_feature` ×8 | L0:9519, L4:13412, L7:8644, L6:16329, L0:10148, L0:5686, L0:6051, L13:6622 |
| 11 | `get_upstream_features` | L7:F2765@46, k=10 → Emb:" She"@15 (de=1.65) +9 more |
| 12 | `get_upstream_features` | L18:F9023@46, k=10 → Emb:"<bos>"@0 (de=-5.22) +9 more |
| 13 | `get_upstream_features` | L15:F3330@15, k=10 → Emb:" She"@15 (de=15.62) +9 more |
| 14 | `inspect_feature` ×8 | L14:5740, L14:13478, L0:14257, L0:3232, L15:13002, L12:15193, L14:8671, L2:6981 |
| 15 | `get_upstream_features` | L4:F13412@7, k=10 → Emb:" nutrition"@7 (de=12.62) +9 more |
| 16 | `get_upstream_features` | L4:F7864@1, k=10 → Emb:"Her"@1 (de=14.75) +9 more |
| 17 | `inspect_feature` ×3 | L3:6920, L2:2128, L4:7864 |

### Build

`build_circuit` → 13 nodes, 21 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 86,972 | 6,328 | 418,080 | 0 | $0.0588 | — | — |
| **Total** | | **86,972** | **6,328** | **418,080** | **0** | **$0.0588** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 31s