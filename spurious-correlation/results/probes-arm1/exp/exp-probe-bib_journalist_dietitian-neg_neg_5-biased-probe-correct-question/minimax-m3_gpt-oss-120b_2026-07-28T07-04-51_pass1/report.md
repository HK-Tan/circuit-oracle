# Circuit Oracle Report
**Date:** 2026-07-28 07:04:51 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** This attribution graph shows the probe's "reporter" classification is driven by two partially converging pathways — a strong profession pathway from the literal "reporter" token, and a substantial, parallel gender-marker pathway from "He/his" pronouns that independently pushes the probe score, confirming the user's concern.

**Confidence:** 7

**Reasoning:**

The circuit splits into two distinct streams that both feed the probe direction (layer 26):

**Profession path (genuine, anchored to the word "reporter"):** The token embedding of "reporter" at pos 66 drives L4:F13253 ("things related to journalism and the media", frac_nonzero=0.0065, promoted tokens include ▁Journalism, ▁journalism, ▁media, ▁reporters), which feeds L14:F4420 ("words and phrases related to journalism and newspapers", frac_nonzero=0.0165, promoted ▁journalists, ▁reporter, ▁editorial, ▁reporters), which in turn drives L19:F2486 ("journalistic sources and news outlets", frac_nonzero=0.0293, promoted ▁reporting, ▁reporter, ▁coverage, ▁reporters). This is a clean lexical-to-semantic cascade: embedding → L4 media-detector → L14 journalism feature → L19 outlet feature → probe. Notably, L19:F2486 carries a *negative* direct effect (-0.1196), so the strongest top-feature here is actually *suppressing* the probe.

**Gender-marker path (spurious):** The pronoun "He" at pos 1 and "his" at pos 3 and pos 61 each feed L0:F2994 ("the pronoun 'his' and the pronoun 'he'", frac_nonzero=0.0733), which has a *positive* direct effect of +0.2324 on the probe — the single largest positive contribution in the entire top-20. L0:F1069 ("references to a male person, particularly when using the pronoun 'He' or 'His'", frac_nonzero=0.0078) is also active at pos 1 and pos 25. Upstream, these feed mid-layer pronoun features L6:F12990 ("male pronouns and titles…associated with men", frac_nonzero=0.068), L7:F14893/F14946 (pronouns/possessive pronouns, both frac_nonzero ≈ 0.009-0.017), and the late L18:F14743 ("He", frac_nonzero=0.018). Crucially, L18:F14743 appears at *three* positions (25, 69, 86) and consistently pushes the probe *negatively* (-0.106, -0.088, -0.093), while the earlier L0 pronoun features push it *positively*.

**Verdict on the user's concern:** The concern is well-founded but the picture is more nuanced than simple "the circuit uses gender." The late-layer L18 "He" feature actually pushes *against* the reporter classification, but the early-layer L0 pronoun detectors (F2994, F1069) push *toward* it. This means the probe's training data likely has a positive association between the male pronoun *density* in a passage and the "reporter" label — i.e., the probe has learned that biographies of male reporters contain many "he/his" tokens, and the early-layer pronoun features carry that statistical co-occurrence directly to the classification. A biography about a female reporter (e.g., substituting "she/her" while keeping "reporter" and the education details) would likely be classified less confidently as "reporter" by this probe, because the L0 pronoun pathway would no longer contribute. The genuine profession pathway exists but is partially cancelled by the negative L19 contribution, leaving the early pronoun detectors as a net positive driver.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'He' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: ' his' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 61 | Emb: ' his' (pos 61) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 25 | Emb: ' He' (pos 25) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 66 | Emb: 'reporter' (pos 66) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: 'He', 'and', 'in', 'from', '.' tokens (pos 1,2,6,9,15,24,50) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: 'He', 'and', 'in', 'from', '.' tokens (pos 1,2,6,9,15,24,50) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: 'He', 'and', 'in', 'from', '.' tokens (pos 1,2,6,9,15,24,50) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: 'He', 'and', 'in', 'from', '.' tokens (pos 1,2,6,9,15,24,50) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 24 | Emb: 'He', 'and', 'in', 'from', '.' tokens (pos 1,2,6,9,15,24,50) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 50 | Emb: 'He', 'and', 'in', 'from', '.' tokens (pos 1,2,6,9,15,24,50) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 3 | Pronoun 'his/he' detectors (L0: F2994) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 61 | Pronoun 'his/he' detectors (L0: F2994) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Male-person reference 'He/His' (L0: F1069) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 25 | Male-person reference 'He/His' (L0: F1069) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 24 | Generic punctuation/function-word features (L0: F6051, F7681, F8061, F886, F4677, F14824) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 50 | Generic punctuation/function-word features (L0: F6051, F7681, F8061, F886, F4677, F14824) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F7681](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7681) | 2 | Generic punctuation/function-word features (L0: F6051, F7681, F8061, F886, F4677, F14824) | statements that describe something, often including a past tense verb | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7681) |
| [L0:F8061](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) | 6 | Generic punctuation/function-word features (L0: F6051, F7681, F8061, F886, F4677, F14824) |  the preposition "in" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) |
| [L0:F886](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/886) | 2 | Generic punctuation/function-word features (L0: F6051, F7681, F8061, F886, F4677, F14824) |  text related to discounts, offers, or prices | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/886) |
| [L0:F4677](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4677) | 15 | Generic punctuation/function-word features (L0: F6051, F7681, F8061, F886, F4677, F14824) |  the word "and", sometimes in conjunction with "the", "but", or "as". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4677) |
| [L0:F14824](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) | 16 | Generic punctuation/function-word features (L0: F6051, F7681, F8061, F886, F4677, F14824) | the word "has" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) |
| [L0:F8974](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) | 9 | Generic punctuation/function-word features (L0: F6051, F7681, F8061, F886, F4677, F14824) | the word "from" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Male pronouns/titles (L6: F12990) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 25 | Male pronouns/titles (L6: F12990) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Possessive/pronoun features (L7: F14893, F14946) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | Possessive/pronoun features (L7: F14893, F14946) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 25 | 'He' pronoun (L18: F14743) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 69 | 'He' pronoun (L18: F14743) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 86 | 'He' pronoun (L18: F14743) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 66 | Journalism/reporter feature (L14: F4420) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 66 | Journalism/media (L4: F13253) |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 66 | Journalistic sources/news outlets (L19: F2486) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2994 de=0.232 |
| 3 | `inspect_feature` ×4 | L0:2994, L14:4420, L7:14893, L18:14743 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F2994@3` | ✅ reported | 3 | 4 | Trace upstream from L0:F2994 (the "his/he" pronoun feature) at position 3 ("He")… |
| SA-2 | `L14:F4420@66` | ✅ reported | 7 | 9 | Trace upstream from L14:F4420 (journalism/newspaper/reporter feature) at pos 66.… |
| SA-3 | `L18:F14743@25` | ✅ reported | 6 | 7 | Trace upstream from L18:F14743 (the "He" pronoun feature) at pos 25. What tokens… |

<details>
<summary><b>SA-1</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 2 | `get_upstream_features` | L0:F2994@3, k=10 | Emb:" his"@3 (de=42.25) +9 more |

**Findings:** The pronoun feature L0:F2994 at token position 3 receives its strongest upstream drive from the embedding of the input token " his" (direct_effect 42.25), with minor contributions from nearby tokens "He", "obtained", and the BOS token. This satisfies the required lower‑third layer (layer 0) and embedding connection conditions. No downstream profession‑related features were observed in this upstrea…

</details>

<details>
<summary><b>SA-2</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@66, k=10 | Emb:" reporter"@66 (de=18.75) +9 more |
| 3 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 4 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 5 | `get_upstream_features` | L4:F13253@66, k=10 | Emb:" reporter"@66 (de=26.62) +9 more |
| 6 | `get_upstream_features` | L8:F8855@66, k=10 | Emb:" reporter"@66 (de=16.88) +9 more |
| 7 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 8 | `inspect_feature` | L1, F1024 | " words and phrases frequently used when discussing writing, publishing" |
| 9 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |
| 10 | `get_upstream_features` | L7:F13646@66, k=10 | Emb:" reporter"@66 (de=15.12) +9 more |
| 11 | `inspect_feature` | L7, F9092 | " words and phrases associated with broadcast journalism" |

**Findings:** The profession feature L14:F4420 is driven almost entirely by the literal token "reporter" at position 66. The token embedding provides the strongest direct effect (18.75) and also excites several lower‑layer profession‑related detectors (L4:F13253, L8:F8855, L7:F13646, etc.) which in turn feed the target. No pronoun or other gendered token contributes positively; the pathway is a direct lexical l…

</details>

<details>
<summary><b>SA-3</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@25, k=10 | Emb:" He"@25 (de=24.00) +9 more |
| 3 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |

**Findings:** The pronoun feature L18:F14743 (detecting 'He') receives its strongest signal directly from the input token embedding of the word 'He' at position 25 (direct_effect 24.0). Additional upstream contributors include an early-layer gender reference detector (L0:F1069) and several mid‑to‑high layer features (L17:F5889, L13:F6622, L15:F3330, L14:F5740) that cumulatively refine the pronoun context. No do…

</details>

### Re-dispatch (round 2): 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-4 | `L7:F14893@1` | ❌ error | — | — | Trace upstream from L7:F14893 (pronouns/possessive pronouns feature) at pos 1 ("… |
| SA-5 | `L19:F2486@66` | ✅ reported | 6 | 8 | Trace upstream from L19:F2486 at pos 66. What does this feature detect, and what… |

<details>
<summary><b>SA-5</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F2486 | " journalistic sources and news outlets." |
| 2 | `get_upstream_features` | L19:F2486@66, k=10 | Emb:" reporter"@66 (de=28.25) +9 more |
| 3 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 4 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 5 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 6 | `get_upstream_features` | L14:F4420@66, k=10 | Emb:" reporter"@66 (de=18.75) +9 more |
| 7 | `get_upstream_features` | L4:F13253@66, k=10 | Emb:" reporter"@66 (de=26.62) +9 more |
| 8 | `inspect_feature` | L1, F1024 | " words and phrases frequently used when discussing writing, publishing" |
| 9 | `get_upstream_features` | L1:F1024@66, k=10 | Emb:" reporter"@66 (de=8.06) +9 more |
| 10 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |

**Findings:** The trace shows that L19:F2486 is a high‑level detector for journalistic sources and news outlets. Its strongest upstream driver is the raw token embedding "reporter" (pos 66). The signal then passes through a cascade of increasingly abstract journalism‑related features in layers 14 → 8 → 7 → 4 → 1, all of which fire on words like reporter, newspaper, editor, and general media terminology. We reac…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×5 | L0:8974, L0:6051, L7:14946, L19:2486, L4:13253 |
| 2 | `get_upstream_features` | L0:F2994@61, k=8 → Emb:" his"@61 (de=45.50) +7 more |
| 3 | `get_upstream_features` | L0:F2994@3, k=8 → Emb:" his"@3 (de=42.25) +7 more |
| 4 | `get_upstream_features` | L0:F2994@66, k=8 → ❌ Feature (layer=0, feature_idx=2994) not found at pos=66. Thi |
| 5 | `inspect_feature` ×5 | L0:14824, L0:7681, L0:8061, L0:886, L0:4677 |
| 6 | `get_upstream_features` | L19:F2486@25, k=10 → Emb:"<bos>"@0 (de=-6.50) +9 more |
| 7 | `get_upstream_features` | L18:F14743@66, k=10 → ❌ Feature (layer=18, feature_idx=14743) not found at pos=66. T |
| 8 | `inspect_feature` | L0, F1069 → " references to a male person, particularly when using the pronoun "He"" |
| 9 | `get_upstream_features` | L0:F1069@1, k=8 → Emb:"He"@1 (de=22.62) +7 more |
| 10 | `inspect_feature` ×2 | L6:12990, L1:1024 |

### Build

`build_circuit` → 16 nodes, 26 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 43,194 | 5,681 | 171,636 | 0 | $0.0301 | — | — |
| SA-1 | openai/gpt-oss-120b | 9,990 | 1,535 | 5,056 | 0 | $0.0025 | ✅ 3F/4E | Trace upstream from L0:F2994 (the "his/he" pronoun feature) … |
| SA-3 | openai/gpt-oss-120b | 23,674 | 3,228 | 0 | 0 | $0.0055 | ✅ 6F/7E | Trace upstream from L18:F14743 (the "He" pronoun feature) at… |
| SA-2 | openai/gpt-oss-120b | 131,192 | 5,597 | 5,056 | 0 | $0.0231 | ✅ 7F/9E | Trace upstream from L14:F4420 (journalism/newspaper/reporter… |
| SA-5 | openai/gpt-oss-120b | 107,931 | 7,530 | 9,984 | 0 | $0.0209 | ✅ 6F/8E | Trace upstream from L19:F2486 at pos 66. What does this feat… |
| **Total** | | **315,981** | **23,571** | **191,732** | **0** | **$0.0820** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 59s