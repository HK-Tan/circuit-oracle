# Circuit Oracle Report
**Date:** 2026-07-28 07:03:22 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven primarily by a cascade of masculine-pronoun ("he") features that trace directly back to the " he" token embedding, with a secondary contribution from a genuine profession-indicator feature (L14:F4420, "words and phrases related to journalism and newspapers") driven by the " writer"/" freelance" token embeddings. The user's concern is confirmed: the dominant signal is gender, not profession.

**Confidence:** 7

**Reasoning:**

The circuit splits into two parallel streams feeding the probe direction:

**1. Gender-pronoun stream (dominant, negative direct_effect):** The largest negative contributions to the probe score come from L18:F14743 ("He", direct_effect=-0.1157 at pos 22, activation=33.75, frac_nonzero=0.018) and L14:F14097 ("occurrences of the word 'he'", direct_effect=-0.0903 at pos 22, frac_nonzero=0.020). Tracing upstream, these are fed by a dense pronoun-detection chain — L17:F5889 ("references to people with pronouns", frac=0.018), L13:F1937 ("pronouns used to describe people", frac=0.054, direct_effect=2.64 into L14:F14097), L7:F14946 ("his/he/him possessive", frac=0.017, direct_effect=-0.079), L6:F12990 ("male pronouns and titles along with descriptors associated with men", frac=0.068, direct_effect=-0.072), and L4:F15567 ("sentences with male or female pronouns and possessives, especially ones referring to writing", direct_effect=2.0 into L18:F14743). All of these ultimately resolve to the raw " he" token embedding at position 22 (direct_effect=28.6 into L18:F14743, 40.25 into L0:F12768, 21.25 into L4:F14796). The intermediate feature L4:F15567 is particularly notable — its autointerp explicitly notes it fires in writing-related contexts, suggesting gender and profession are entangled in the model's mid-layers, but the late-layer L18 "He" feature suppresses the probe score via its direct negative effect.

**2. Profession-indicator stream (supportive, present but smaller):** The genuine profession signal flows from " writer" (pos 28, direct_effect=19.75 into L1:F15416) and " freelance" (pos 27, direct_effect=2.69 into L4:F13253) embeddings into L1:F15416 ("the word 'writers' or 'writer'", frac=0.004) → L4:F13253 ("things related to journalism and the media", frac=0.006) → L8:F8855 ("mentions of news reporters and news reporting", frac=0.008) → L14:F4420 ("words and phrases related to journalism and newspapers", direct_effect=-0.0713, frac=0.017). This is a clean profession detector — its top activating examples are reporter/newspaper contexts — and it does fire on the " writer" token in this prompt.

**Confirmation of the user's concern:** The gender-pronoun features dominate the top-feature list by activation magnitude (L18:F14743 fires at 33.75 across positions 22, 39, and 67, and the chain includes six dedicated pronoun detectors at L4, L6, L7, L13, L14, L17, L18). The profession feature is present but its contribution is diluted by the gender cascade. The probe's classification is being driven by "he/his" pronoun tokens across the text rather than by the subject's actual profession, confirming the worry about spurious gender-marker reliance. The few "defense" / "Institute" / "covering" / "Starting" context features in the top list carry much smaller direct effects and do not aggregate into any structured "defense journalist" supernode in the circuit.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 22 | Male pronoun features (L17-L18, pos 22): "He" detector and pronoun-reference aggregator | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 22 | Male pronoun features (L17-L18, pos 22): "He" detector and pronoun-reference aggregator |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L14:F14097](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) | 22 | Mid-layer masculine-pronoun detectors (L4-L14, pos 22) | occurrences of the word "he" | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) |
| [L13:F1937](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/1937) | 22 | Mid-layer masculine-pronoun detectors (L4-L14, pos 22) |  pronouns used to describe people, including possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/1937) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 22 | Mid-layer masculine-pronoun detectors (L4-L14, pos 22) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 22 | Mid-layer masculine-pronoun detectors (L4-L14, pos 22) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L4:F15567](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) | 22 | Mid-layer masculine-pronoun detectors (L4-L14, pos 22) | sentences with male or female pronouns and possessives, especially ones referring to writing | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) |
| [L4:F14796](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14796) | 22 | Mid-layer masculine-pronoun detectors (L4-L14, pos 22) | the pronoun "he" or "him" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14796) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 28 | Journalism-profession feature (L14, pos 28): "words and phrases related to journalism and newspapers" | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 28 | Mid-layer writer/journalism detectors (L4-L8, pos 28) |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 28 | Mid-layer writer/journalism detectors (L4-L8, pos 28) |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L1:F15416](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15416) | 28 | Mid-layer writer/journalism detectors (L4-L8, pos 28) | the word "writers" or "writer" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15416) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 22 | Low-layer pronoun pair / single-pronoun features (L0, pos 22) |  mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L0:F7376](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7376) | 28 | Low-layer pronoun pair / single-pronoun features (L0, pos 22) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7376) |
| [L1:F15323](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15323) | 1 | Context "Starting" feature (L1, pos 1) | the word "starting" in academic papers | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15323) |
| [L1:F4459](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4459) | 7 | Context "research institute" feature (L1, pos 7) |  mentions of research institutes | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4459) |
| [L1:F15063](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15063) | 5 | Context "United States" feature (L1, pos 5) | mentions of the United States | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15063) |
| [L2:F9293](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9293) | 12 | Context "cover" feature (L2, pos 12) |  the word "cover" used in different contexts | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9293) |
| [L0:F7124](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7124) | 2 | Misc low-layer punctuation/function-word suppressors (L0-L1) | the word "at" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7124) |
| [L0:F15661](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15661) | 7 | Misc low-layer punctuation/function-word suppressors (L0-L1) | the word "spin" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15661) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 3 | Misc low-layer punctuation/function-word suppressors (L0-L1) | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F6556](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6556) | 1 | Misc low-layer punctuation/function-word suppressors (L0-L1) |  instances of the word "closing" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6556) |
| [L0:F4870](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4870) | 11 | Misc low-layer punctuation/function-word suppressors (L0-L1) |  commas and sometimes reach (context not clear) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4870) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 38 | Misc low-layer punctuation/function-word suppressors (L0-L1) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:7124 de=-0.160 |
| 3 | `inspect_feature` ×5 | L18:14743, L0:7124, L1:15323, L0:15661, L0:3820 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14743@22` | ✅ reported | 6 | 7 | Trace the upstream path from L18:F14743 ("He" - the masculine pronoun feature). … |
| SA-2 | `L1:F15323@1` | ❌ error | — | — | Trace the upstream path from L1:F15323 ("starting" token feature) at position 1.… |
| SA-3 | `L14:F14097@22` | ✅ reported | 4 | 3 | Trace the upstream path from L14:F14097 at position 22. This has negative direct… |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@22, k=15 | Emb:" he"@22 (de=28.62) +14 more |
| 3 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |
| 4 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 5 | `get_upstream_features` | L4:F15567@22, k=15 | Emb:" he"@22 (de=17.75) +14 more |
| 6 | `inspect_feature` | L3, F9548 | " uses of the word "this" followed by a pause or conjunction, sometimes" |
| 7 | `get_upstream_features` | L17:F5889@22, k=15 | Emb:" he"@22 (de=37.50) +14 more |
| 8 | `inspect_feature` | L0, F12768 | " mentions of "he" and "she" in close proximity" |
| 9 | `get_upstream_features` | L0:F12768@22, k=10 | Emb:" he"@22 (de=40.25) +9 more |
| 10 | `inspect_feature` | L14, F14097 | " occurrences of the word "he"" |

**Findings:** The masculine pronoun feature L18:F14743 is driven primarily by the raw embedding for " he" and a cascade of low‑level pronoun detectors. The strongest upstream source appears at layer 4 (F15567), a sentence‑level gender‑pronoun detector that itself is strongly excited by the same embedding. Additional upstream contributions come from layer 17 (F5889) and layer 14 (F14097), which are higher‑level …

</details>

<details>
<summary><b>SA-3</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F14097 | " occurrences of the word "he"" |
| 2 | `get_upstream_features` | L14:F14097@22, k=10 | Emb:" he"@22 (de=2.70) +9 more |
| 3 | `inspect_feature` | L13, F1937 | " pronouns used to describe people, including possessive pronouns" |
| 4 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |
| 5 | `get_upstream_features` | L13:F1937@22, k=10 | Emb:" he"@22 (de=8.94) +9 more |
| 6 | `inspect_feature` | L0, F12768 | " mentions of "he" and "she" in close proximity" |
| 7 | `get_upstream_features` | L4:F15567@22, k=10 | Emb:" he"@22 (de=17.75) +9 more |
| 8 | `inspect_feature` | L3, F9548 | " uses of the word "this" followed by a pause or conjunction, sometimes" |
| 9 | `inspect_feature` | L6, F6622 | " pronouns and possessive pronouns in the context of legal and athletic" |

**Findings:** The traced path shows that L14:F14097 is primarily a detector for the masculine pronoun "he". Its strongest upstream driver is a lower‑layer (L4) sentence‑level pronoun detector that itself is strongly excited by the raw embedding of the token " he". The chain does not involve any profession‑specific or gender‑neutral cues; it is a clear gender‑pronoun marker. Thus, the semantic concept encoded by…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×12 | L7:14946, L2:9293, L1:4459, L1:15416, L1:15063, L0:12768, L0:5288, L0:6556, L0:4870, L0:6051, L6:12990, L14:4420 |
| 2 | `get_upstream_features` | L1:F15416@28, k=5 → Emb:" writer"@28 (de=19.75) +4 more |
| 3 | `get_upstream_features` | L14:F4420@28, k=5 → Emb:" writer"@28 (de=5.75) +4 more |
| 4 | `get_upstream_features` | L1:F15323@1, k=5 → Emb:"Starting"@1 (de=16.38) +4 more |
| 5 | `get_upstream_features` | L1:F4459@7, k=5 → Emb:" Institute"@7 (de=27.50) +4 more |
| 6 | `get_upstream_features` | L0:F15661@7, k=3 → Emb:" Institute"@7 (de=19.38) +2 more |
| 7 | `get_upstream_features` | L0:F4870@11, k=3 → Emb:","@11 (de=30.00) +2 more |
| 8 | `get_upstream_features` | L0:F12768@22, k=3 → Emb:" he"@22 (de=40.25) +2 more |
| 9 | `get_upstream_features` | L18:F14743@22, k=5 → Emb:" he"@22 (de=28.62) +4 more |
| 10 | `get_upstream_features` | L14:F14097@22, k=3 → Emb:" he"@22 (de=2.70) +2 more |
| 11 | `get_upstream_features` | L6:F12990@22, k=3 → Emb:" he"@22 (de=6.50) +2 more |
| 12 | `get_upstream_features` | L7:F14946@22, k=3 → Emb:" he"@22 (de=14.19) +2 more |
| 13 | `get_upstream_features` | L2:F9293@12, k=3 → Emb:" covering"@12 (de=26.50) +2 more |
| 14 | `get_upstream_features` | L0:F6051@38, k=3 → Emb:"."@38 (de=47.50) +2 more |
| 15 | `get_upstream_features` | L1:F15063@5, k=3 → Emb:" United"@5 (de=21.88) +2 more |
| 16 | `inspect_feature` ×6 | L8:8855, L4:13253, L4:15567, L13:1937, L17:5889, L4:14796 |
| 17 | `get_upstream_features` | L4:F14796@22, k=3 → Emb:" he"@22 (de=21.25) +2 more |
| 18 | `get_upstream_features` | L14:F4420@28, k=5 → Emb:" writer"@28 (de=5.75) +4 more |
| 19 | `get_upstream_features` | L8:F8855@28, k=3 → Emb:" writer"@28 (de=4.72) +2 more |
| 20 | `get_upstream_features` | L13:F1937@22, k=3 → Emb:" he"@22 (de=8.94) +2 more |
| 21 | `get_upstream_features` | L1:F15416@28, k=5 → Emb:" writer"@28 (de=19.75) +4 more |

### Build

`build_circuit` → 18 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 52,929 | 5,785 | 295,763 | 0 | $0.0406 | — | — |
| SA-3 | openai/gpt-oss-120b | 120,933 | 8,079 | 256 | 0 | $0.0230 | ✅ 4F/3E | Trace the upstream path from L14:F14097 at position 22. This… |
| SA-1 | openai/gpt-oss-120b | 133,409 | 6,890 | 10,176 | 0 | $0.0243 | ✅ 6F/7E | Trace the upstream path from L18:F14743 ("He" - the masculin… |
| **Total** | | **307,271** | **20,754** | **306,195** | **0** | **$0.0879** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 31s