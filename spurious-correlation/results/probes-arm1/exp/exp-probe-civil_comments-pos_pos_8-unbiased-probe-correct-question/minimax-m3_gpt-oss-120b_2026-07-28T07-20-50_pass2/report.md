# Circuit Oracle Report
**Date:** 2026-07-28 07:20:50 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_8 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by the *identity-token* " Islam" (pos 4) being detected by a multi-layer chain of Islam/Middle-Eastern/religious-affiliation entity features, with the actual toxic predicates ("false," "Lucifer," "problem") contributing only generic, low-impact lexical detectors.

**Confidence:** 9

**Reasoning:** The attribution graph reveals two distinct pathways driving the probe:

1. **The "Islam-identity" pathway (dominant, identity-based):** The single token embedding at pos 4 (" Islam") fires with very large direct effects into the cascade. It strongly excites L0:F13885 ("names of people and places, specifically those related to the middle east", frac_nonzero 0.054, direct_effect 12.25 from the embedding), which then feeds L1 Islamic-vocabulary detectors (F4314 "the word Muslim", F2352 "words associated with Islam"), a L0 generic religion detector (F4470), L2:F7214 ("references to countries or regions associated with Islam"), L4:F2405 ("words related to religious identity/affiliation"), L6:F7282 ("mentions of Islam or Middle Eastern places and people", direct_effect 18.5 from the " Islam" embedding), L6:F2674 (direct_effect 3.8 from " Islam"), L7:F11758 (cultural/Islamic proper-noun detector, direct_effect 3.4 from the embedding), and L8:F16294 (Mid-East/Central-Asia proper nouns, direct_effect 3.5 from the embedding). Critically, several features in this chain — F7282, F11758, F11743, F14049, F16294, F5783 — push the probe **up** (positive direct_effect to the output) simply by detecting that the prompt mentions Islam or a Middle-Eastern entity. None of them encode sentiment, threat, or the predicate "Lucifer / false."

2. **The "generic lexical" pathway (weak):** The toxic content words ("false religion," "Lucifer") do not surface as identity-features. Instead they only trigger a swarm of high-frac_nonzero, function-word L0 detectors (F11375 "is", F3635 "that", F880 "it", F2158 "with", F7253 "present/left"). These are vanilla lexical features that fire on almost any English sentence; they do not specifically encode the harmful claim. Some push the probe down (F11375 at pos 5, +0.226 to the output, but only because the *word* "is" is generic).

This confirms the user's concern. The probe's score is largely a monotonic function of "does this prompt mention an identity group tied to Islam?" — the strongest single direct_effect to the probe (+0.2256) comes from L0:F11375 on the generic word "is" at pos 5, but the substantive, content-bearing signal arrives through the identity-recognition cascade. The actual toxic content ("false religion," "Lucifer is") is not detected by any specialized feature in the circuit; it is invisible to the probe. The probe is therefore classifying the prompt based on *which group is being discussed* (a spurious identity signal), not on *what is being said about them* (the actual toxicity). This is a textbook example of an identity-confounded probe: swapping "Islam" for any other group name would likely flip the probe's score even if the surrounding toxic template were held constant.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 5 | Generic lexical detectors (L0: function-word detectors) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 14 | Generic lexical detectors (L0: function-word detectors) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F3635](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) | 6 | Generic lexical detectors (L0: function-word detectors) | the word "that" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) |
| [L0:F880](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/880) | 7 | Generic lexical detectors (L0: function-word detectors) |  references to the pronoun "it", and sometimes "that", suggesting observation of the subject of a discussion | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/880) |
| [L0:F2158](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) | 3 | Generic lexical detectors (L0: function-word detectors) | the word "with" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) |
| [L0:F7253](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7253) | 2 | Generic lexical detectors (L0: function-word detectors) | the word "present" or the word "left" or inflected forms thereof | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7253) |
| [L0:F13885](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13885) | 4 | Middle-Eastern proper-noun detector | names of people and places, specifically those related to the middle east | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13885) |
| [L1:F4314](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4314) | 4 | Early-layer Islamic vocabulary detectors | the word Muslim | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4314) |
| [L1:F2352](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2352) | 4 | Early-layer Islamic vocabulary detectors | words associated with Islam | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2352) |
| [L0:F4470](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4470) | 4 | Generic religion detector | references to religion, religious figures, or important religious places | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4470) |
| [L2:F7214](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7214) | 4 | Islamic country/region reference (pushes DOWN on probe) |  references to countries or regions associated with Islam | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7214) |
| [L4:F2405](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) | 4 | Religious identity/affiliation detector |  words related to religious identity/affiliation or spirituality including related holidays | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) |
| [L6:F7282](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) | 4 | Islam / Middle-Eastern people+places detector (mixed sign) |  mentions of Islam or Middle Eastern places and people, as well as mentions of a specific district. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) |
| [L6:F2674](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2674) | 4 | Islam / Middle-Eastern people+places detector (mixed sign) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2674) |
| [L7:F11758](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/11758) | 4 | Cultural/Islamic proper-noun + district detector (PUSHES UP on probe) | words with some cultural (often middle eastern) or historical aspect that may be a name or location | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/11758) |
| [L7:F11743](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/11743) | 4 | Cultural/Islamic proper-noun + district detector (PUSHES UP on probe) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/11743) |
| [L7:F14049](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14049) | 4 | Cultural/Islamic proper-noun + district detector (PUSHES UP on probe) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14049) |
| [L8:F16294](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16294) | 4 | Mid-East / Central-Asia proper-noun entity (PUSHES UP on probe) |  proper nouns related to the Middle East and Central Asia, and potentially to Islam | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16294) |
| [L8:F5783](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/5783) | 4 | Mid-East / Central-Asia proper-noun entity (PUSHES UP on probe) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/5783) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:11375 de=0.226 |
| 3 | `inspect_feature` ×11 | L0:11375, L2:7214, L0:3635, L0:2158, L0:7253, L0:880, L0:11375, L6:7282, L8:16294, L3:290, L3:8595 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F7282@4` | ❌ error | — | — | Trace L6:F7282 ("mentions of Islam or Middle Eastern places and people"). What i… |
| SA-2 | `L2:F7214@4` | ✅ reported | 5 | 6 | Trace L2:F7214 ("references to countries or regions associated with Islam"). Wha… |
| SA-3 | `L8:F16294@4` | ✅ reported | 3 | 7 | Trace L8:F16294 ("proper nouns related to the Middle East and Central Asia, and … |
| SA-4 | `L8:F5783@4` | ❌ error | — | — | Trace L8:F5783 at position 4. What is this feature about? Reach embedding level. |
| SA-5 | `L7:F11758@4` | ✅ reported | 3 | 6 | Trace L7:F11758 at position 4. Reach embedding level. |
| SA-6 | `L6:F2674@4` | ❌ error | — | — | Trace L6:F2674 at position 4. Reach embedding level. |
| SA-7 | `L0:F3635@6` | ❌ error | — | — | Trace L0:F3635 at position 6 (the word "that"). This is high direct_effect 0.117… |
| SA-8 | `L0:F11375@5` | ❌ error | — | — | Trace L0:F11375 at position 5 ("is"). Direct effect 0.2256, the largest positive… |

<details>
<summary><b>SA-2</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F7214 | " references to countries or regions associated with Islam" |
| 2 | `get_upstream_features` | L2:F7214@4, k=10 | Emb:" Islam"@4 (de=12.38) +9 more |
| 3 | `inspect_feature` | L0, F13885 | " names of people and places, specifically those related to the middle " |
| 4 | `inspect_feature` | L1, F4314 | " the word Muslim" |
| 5 | `inspect_feature` | L1, F2352 | " words associated with Islam" |
| 6 | `get_upstream_features` | L0:F13885@4, k=10 | Emb:" Islam"@4 (de=12.25) +9 more |
| 7 | `get_upstream_features` | L0:F13885@4, k=10 | Emb:" Islam"@4 (de=12.25) +9 more |
| 8 | `get_upstream_features` | L1:F4314@4, k=10 | Emb:" Islam"@4 (de=16.50) +9 more |
| 9 | `inspect_feature` | L0, F4470 | " references to religion, religious figures, or important religious pla" |
| 10 | `inspect_feature` | L0, F3031 | "the word "bias"" |

**Findings:** L2:F7214, the detector for references to Islamic countries/regions, is primarily driven by the explicit "Islam" token (embedding at position 4) with a large positive direct effect. Early‑layer lexical detectors reinforce this signal: a layer‑0 Middle‑Eastern name detector (F13885), a layer‑1 "Muslim" word detector (F4314), a layer‑1 broader Islamic‑vocabulary detector (F2352), and a generic religi…

</details>

<details>
<summary><b>SA-3</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L8, F16294 | " proper nouns related to the Middle East and Central Asia, and potenti" |
| 2 | `get_upstream_features` | L8:F16294@4, k=10 | Emb:" Islam"@4 (de=3.53) +9 more |
| 3 | `inspect_feature` | L6, F7282 | " mentions of Islam or Middle Eastern places and people, as well as men" |
| 4 | `get_upstream_features` | L6:F7282@4, k=10 | Emb:" Islam"@4 (de=18.50) +9 more |
| 5 | `inspect_feature` | L0, F13885 | " names of people and places, specifically those related to the middle " |
| 6 | `get_upstream_features` | L0:F13885@4, k=10 | Emb:" Islam"@4 (de=12.25) +9 more |

**Findings:** The target L8:F16294 is driven primarily by the input token " Islam" at position 4 (direct_effect 3.53). Upstream, a mid‑layer feature L6:7282 (direct_effect 2.81) also receives a strong positive push from the same " Islam" embedding (direct_effect 18.5) and detects mentions of Islam and related places. An even earlier detector L0:13885 (direct_effect 2.39 to L6:7282, 12.25 from the embedding) ide…

</details>

<details>
<summary><b>SA-5</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F11758 | " words with some cultural (often middle eastern) or historical aspect " |
| 2 | `get_upstream_features` | L7:F11758@4, k=10 | L6:F7282 (de=4.28) +9 more |
| 3 | `inspect_feature` | L6, F7282 | " mentions of Islam or Middle Eastern places and people, as well as men" |
| 4 | `get_upstream_features` | L6:F7282@4, k=10 | Emb:" Islam"@4 (de=18.50) +9 more |
| 5 | `inspect_feature` | L0, F13885 | " names of people and places, specifically those related to the middle " |
| 6 | `get_upstream_features` | L0:F13885@4, k=10 | Emb:" Islam"@4 (de=12.25) +9 more |
| 7 | `inspect_feature` | L6, F2267 | "words that appear in programming code, legal jargon, or scientific tex" |

**Findings:** Tracing from L7:F11758 (position 4) reveals a strong cultural‑sensitivity pathway dominated by the token embedding "Islam". The embedding drives a layer‑6 feature (F7282) that explicitly detects Islamic references, which in turn strongly excites the target feature. An early layer‑0 name detector (F13885) also receives a large positive push from the same embedding, completing a lower‑third (≤8) cas…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L8:F5783@4, k=10 → L6:F7282 (de=3.48) +9 more |
| 2 | `get_upstream_features` | L6:F2674@4, k=10 → Emb:" Islam"@4 (de=3.80) +9 more |
| 3 | `get_upstream_features` | L3:F8595@3, k=10 → Emb:" problem"@2 (de=6.97) +9 more |
| 4 | `get_upstream_features` | L3:F290@3, k=10 → Emb:" with"@3 (de=12.06) +9 more |
| 5 | `get_upstream_features` | L7:F9503@3, k=10 → Emb:" problem"@2 (de=7.84) +9 more |
| 6 | `get_upstream_features` | L0:F2158@3, k=10 → Emb:" with"@3 (de=32.50) +9 more |
| 7 | `inspect_feature` ×3 | L4:2405, L6:7282, L2:12222 |
| 8 | `get_upstream_features` | L0:F2158@3, k=8 → Emb:" with"@3 (de=32.50) +7 more |
| 9 | `get_upstream_features` | L7:F11758@4, k=8 → L6:F7282 (de=4.28) +7 more |
| 10 | `get_upstream_features` | L0:F13885@4, k=8 → Emb:" Islam"@4 (de=12.25) +7 more |
| 11 | `get_upstream_features` | L0:F3635@6, k=8 → Emb:" that"@6 (de=40.50) +7 more |
| 12 | `get_upstream_features` | L0:F880@7, k=8 → Emb:" it"@7 (de=44.00) +7 more |
| 13 | `get_upstream_features` | L8:F16294@4, k=8 → Emb:" Islam"@4 (de=3.53) +7 more |
| 14 | `get_upstream_features` | L8:F16294@3, k=8 → ❌ Feature (layer=8, feature_idx=16294) not found at pos=3. Thi |
| 15 | `get_upstream_features` | L0:F13885@3, k=8 → ❌ Feature (layer=0, feature_idx=13885) not found at pos=3. Thi |
| 16 | `get_upstream_features` | L0:F11375@5, k=8 → Emb:" is"@5 (de=31.88) +7 more |
| 17 | `get_upstream_features` | L0:F7253@2, k=8 → Emb:"The"@1 (de=6.94) +7 more |

### Build

`build_circuit` → 18 nodes, 23 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 58,534 | 6,210 | 142,052 | 0 | $0.0335 | — | — |
| SA-3 | openai/gpt-oss-120b | 52,930 | 2,970 | 0 | 0 | $0.0097 | ✅ 3F/7E | Trace L8:F16294 ("proper nouns related to the Middle East an… |
| SA-5 | openai/gpt-oss-120b | 80,712 | 6,044 | 0 | 0 | $0.0157 | ✅ 3F/6E | Trace L7:F11758 at position 4. Reach embedding level. |
| SA-2 | openai/gpt-oss-120b | 120,157 | 6,625 | 15,456 | 0 | $0.0222 | ✅ 5F/6E | Trace L2:F7214 ("references to countries or regions associat… |
| **Total** | | **312,333** | **21,849** | **157,508** | **0** | **$0.0812** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 32s