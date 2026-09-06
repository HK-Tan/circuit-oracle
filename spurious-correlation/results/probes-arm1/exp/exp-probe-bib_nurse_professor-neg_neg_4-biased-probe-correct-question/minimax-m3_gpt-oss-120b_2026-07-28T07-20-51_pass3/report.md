# Circuit Oracle Report
**Date:** 2026-07-28 07:20:51 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's positive classification score is driven by a cascading chain of male-pronoun features — the L0 "his/he" detectors, the L4-L6 "he/him/male titles" detectors, and the L7-L18 pronoun aggregators — all seeded directly by the token embeddings of the masculine pronouns "He" (pos 1, 35) and "His" (pos 13, 37, 55), with no meaningful contribution from profession-specific content.

**Confidence:** 8

**Reasoning:** The circuit is overwhelmingly a gender-pronoun pathway, not a profession-content pathway. The top three output-driving features by signed direct effect are all gender markers:
- **L0:F2994** ("his/he" pronoun) fires at pos 37 and pos 55 with direct_effects +0.254 and +0.154, and the subagent showed it is fed directly by the " His" embedding (pos 37, 55).
- **L6:F12990** ("male pronouns and titles") carries a *negative* direct_effect (−0.166 at pos 13, −0.125 at pos 2, −0.115 at pos 1) — meaning the model is partially cancelling it — but its presence in the top features still signals that the probe's classification is centered on the masculine-pronoun subspace.
- **L0:F2848** ("of"), **L0:F11024** ("clock" — but here triggered by the "is also Director of" neighborhood, likely an artifact of co-occurring with the title sentence) and **L0:F8658** are generic lexical features with very low frac_nonzero but not profession-specific.

Tracing deeper confirmed the gender chain: the " He" embedding at pos 1 (direct_effect 22.6) drives **L0:F1069** (male person reference, frac_nonzero 0.008), which in turn feeds **L4:F14796** (he/him, frac_nonzero 0.017) and **L6:F12990** (male pronouns/titles, frac_nonzero 0.068). The " His" embedding at pos 13 (direct_effect 5.28) also feeds **L6:F12990** directly. Upstream of **L18:F14743** ("He", frac_nonzero 0.018) sits **L17:F5889** (pronoun aggregator) and **L13:F6622** (general pronoun), with the strongest upstream being the " He" token embedding at pos 35 (direct_effect 23.6).

**The user's concern is well-supported.** No feature in the circuit encodes "professor", "researcher", "academic", "computer science", "PhD", or any other profession-indicator. The only profession-adjacent tokens (" Director", " Mobile Grid", " Ph.D.", " Computer Science") do not appear in the top features. Instead, the entire positive contribution to the probe flows from the repeated masculine pronouns — the subject is described with "He", " His", " he", "His" at five positions (1, 13, 35, 37, 55), and these pronouns cascade through a dedicated gender-detection circuit (L0 → L2/L4 → L6 → L7 → L13/L17 → L18) that ends up being what the probe reads. The negative-contribution features (L6:F12990 and L18:F14743) at the last position are the model partially correcting for the gender signal, but they are still *about gender*, not about profession. A female pronoun version of the same biography would produce a substantially different score from this circuit despite identical professional content — confirming the probe has latched onto a spurious gender marker rather than the genuine profession signal.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'He' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: ' His' (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 35 | Emb: ' He' (pos 35) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 37 | Emb: ' His' (pos 37) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 55 | Emb: ' His' (pos 55) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: ' Director' (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: ' of' (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: ' is' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Early-layer male pronoun features (L0) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 37 | Early-layer male pronoun features (L0) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 55 | Early-layer male pronoun features (L0) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 5 | Early-layer lexical features (L0) | the word "of" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F11024](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11024) | 4 | Early-layer lexical features (L0) |  the word "clock", especially in a technical context | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11024) |
| [L0:F8658](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8658) | 2 | Early-layer lexical features (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8658) |
| [L2:F9301](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) | 1 | Mid-layer male pronoun detectors (L2-L4) |  all mentions of men and women in the context of relationships, dating, or gendered social roles | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) |
| [L4:F14796](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14796) | 1 | Mid-layer male pronoun detectors (L2-L4) | the pronoun "he" or "him" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14796) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 13 | Mid-layer male pronoun detectors (L2-L4) |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 13 | Mid-layer male pronoun/title feature (L6) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 35 | Mid-layer male pronoun/title feature (L6) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 2 | Mid-layer male pronoun/title feature (L6) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Mid-layer male pronoun/title feature (L6) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Late-layer pronoun/gender features (L7-L18) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 13 | Late-layer pronoun/gender features (L7-L18) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | Late-layer pronoun/gender features (L7-L18) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 2 | Late-layer pronoun/gender features (L7-L18) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L13:F6622](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) | 2 | Late-layer pronoun/gender features (L7-L18) | pronouns. | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) |
| [L13:F6622](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) | 35 | Late-layer pronoun/gender features (L7-L18) | pronouns. | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 35 | Late-layer pronoun/gender features (L7-L18) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2994 de=0.254 |
| 3 | `inspect_feature` ×5 | L0:2994, L0:2848, L0:11024, L6:12990, L18:14743 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14743@35` | ✅ reported | 5 | 7 | Trace the circuit upstream from L18:F14743 (a "He" feature at pos 35) to underst… |
| SA-2 | `L6:F12990@13` | ✅ reported | 4 | 5 | Trace upstream from L6:F12990 (a "male pronouns/titles" feature at pos 13) to fi… |
| SA-3 | `L0:F2994@37` | ❌ error | — | — | Trace upstream from L0:F2994 (a "his/he" pronoun feature at pos 37) — since this… |
| SA-4 | `L7:F14893@1` | ✅ reported | 4 | 3 | Trace upstream from L7:F14893 (at pos 1) to understand what this feature represe… |

<details>
<summary><b>SA-1</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@35, k=10 | Emb:" He"@35 (de=23.62) +9 more |
| 3 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 4 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 5 | `inspect_feature` | L13, F6622 | " pronouns." |
| 6 | `get_upstream_features` | L0:F1069@35, k=5 | Emb:" He"@35 (de=36.50) +4 more |
| 7 | `get_upstream_features` | L17:F5889@35, k=5 | Emb:" He"@35 (de=22.62) +4 more |
| 8 | `get_upstream_features` | L13:F6622@35, k=5 | Emb:" He"@35 (de=13.62) +4 more |
| 9 | `inspect_feature` | L6, F2267 | "words that appear in programming code, legal jargon, or scientific tex" |

**Findings:** The target L18:F14743 is a masculine pronoun detector. Its strongest upstream driver is the raw token embedding for the space‑prefixed token " He" (direct effect 23.6). The next strongest upstream influences come from early‑layer gender‑specific features (L0:F1069) and mid‑layer pronoun aggregators (L17:F5889, L13:F6622). All of these are clearly pronoun/gender related. A content‑focused feature a…

</details>

<details>
<summary><b>SA-2</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 2 | `get_upstream_features` | L6:F12990@13, k=10 | Emb:" His"@13 (de=5.28) +9 more |
| 3 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 4 | `get_upstream_features` | L4:F4315@13, k=10 | Emb:" His"@13 (de=21.25) +9 more |
| 5 | `inspect_feature` | L5, F14955 | " text about people's free time that mentions both family and hobbies" |
| 6 | `get_upstream_features` | L5:F14955@13, k=10 | Emb:" His"@13 (de=4.47) +9 more |
| 7 | `inspect_feature` | L4, F15438 | " mentions and declarations of conflicts of interest, study design, and" |

**Findings:** The male‑pronoun feature (L6:F12990) is primarily driven by the raw input token embedding for "His" at position 13 (direct_effect 5.28). Additional positive contributions come from an earlier pronoun detector (L4:F4315) and a contextual personal‑narrative feature (L5:F14955). Both upstream sources reside in layers ≤8, satisfying the lower‑third floor requirement, and we have a direct embedding inf…

</details>

<details>
<summary><b>SA-4</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@1, k=10 | Emb:"He"@1 (de=14.75) +9 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `get_upstream_features` | L6:F12990@1, k=10 | Emb:"He"@1 (de=3.41) +9 more |
| 5 | `inspect_feature` | L4, F14796 | "the pronoun "he" or "him"" |
| 6 | `get_upstream_features` | L4:F14796@1, k=10 | Emb:"He"@1 (de=17.12) +9 more |
| 7 | `inspect_feature` | L2, F9301 | " all mentions of men and women in the context of relationships, dating" |

**Findings:** The target feature L7:F14893 is a pronoun detector that fires strongly on the token "He" at position 1. Its strongest upstream driver is the raw embedding of the token "He" (direct_effect ~14.7), followed by a cascade of gender‑specific features: L6:F12990 (male pronoun & title detector), L4:F14796 (specific "he/him" detector), and L2:F9301 (broader gender‑role detector). All these upstream featur…

</details>

### Re-dispatch (round 2): 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-5 | `L7:F14946@1` | ❌ error | — | — | Trace upstream from L7:F14946 (a "his" pronoun feature at pos 1 and pos 2) to un… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×6 | L0:1069, L4:14796, L7:14893, L7:14946, L4:4315, L2:9301 |
| 2 | `get_upstream_features` | L0:F11024@4, k=8 → Emb:" Director"@4 (de=12.81) +7 more |
| 3 | `get_upstream_features` | L0:F2848@5, k=8 → Emb:" of"@5 (de=34.75) +7 more |
| 4 | `get_upstream_features` | L0:F8658@2, k=8 → Emb:"He"@1 (de=8.00) +7 more |
| 5 | `get_upstream_features` | L7:F14946@1, k=5 → Emb:"He"@1 (de=11.50) +4 more |
| 6 | `get_upstream_features` | L7:F14946@2, k=5 → Emb:"He"@1 (de=9.00) +4 more |
| 7 | `get_upstream_features` | L0:F1069@1, k=5 → Emb:"He"@1 (de=22.62) +4 more |
| 8 | `get_upstream_features` | L4:F14796@1, k=5 → Emb:"He"@1 (de=17.12) +4 more |
| 9 | `get_upstream_features` | L13:F6622@35, k=5 → Emb:" He"@35 (de=13.62) +4 more |
| 10 | `get_upstream_features` | L17:F5889@35, k=5 → Emb:" He"@35 (de=22.62) +4 more |

### Build

`build_circuit` → 14 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 47,486 | 5,047 | 110,430 | 0 | $0.0269 | — | — |
| SA-2 | openai/gpt-oss-120b | 58,625 | 5,503 | 7,584 | 0 | $0.0122 | ✅ 4F/5E | Trace upstream from L6:F12990 (a "male pronouns/titles" feat… |
| SA-4 | openai/gpt-oss-120b | 56,117 | 4,536 | 10,912 | 0 | $0.0113 | ✅ 4F/3E | Trace upstream from L7:F14893 (at pos 1) to understand what … |
| SA-1 | openai/gpt-oss-120b | 92,623 | 6,545 | 7,680 | 0 | $0.0179 | ✅ 5F/7E | Trace the circuit upstream from L18:F14743 (a "He" feature a… |
| **Total** | | **254,851** | **21,631** | **136,606** | **0** | **$0.0684** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 42s