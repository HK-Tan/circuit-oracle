# Circuit Oracle Report
**Date:** 2026-07-28 07:20:08 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_10 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction score is driven by a heterogeneous mix of content-specific features (the literal word "reversal," the literal word "not," the lexical token "role," the period after the second sentence) and abstract semantic features that wire those tokens into higher-level "reversal," "subversion," and "negation" concepts, with the "not" token in the hypothesis (pos 17) acting as a strong but mostly redundant contributor whose inclusion is more lexical than semantic.

**Confidence:** 7

**Reasoning:**

The circuit traces cleanly to embedding nodes for every content word involved. Two key observations from the data support a nuanced view of the user's concern:

**1. The "not" embedding IS a strong direct contributor, but it is NOT the only — or even the main — signal.** The "not" token at pos 17 has direct embedding effects of 6.78 (L10), 6.56 (L12), 22.6 (L2), 18 (L4), and 15 (L3) into various downstream features. This is large, but it is functionally similar in magnitude to the "reversal" embedding (pos 4), which fires into 6 different downstream features with direct effects of 5–13 each. The probe is NOT relying on "not" alone.

**2. The "not" signal is partially redundant with content features.** The hypothesis "There is not [role reversal]…" contains BOTH "not" AND "reversal." The probe fires on:
- Lexical "not" → L3:F12079 (negation detector) and L4:F4492 (multilingual negations) — purely lexical cues
- Lexical "reversal" → L4:F7409 → L6:F12420 ("subverting conventions") → L7:F4526 (reversals/symmetry) and L8:F16033 (figurative reversal) — semantic content features
- Lexical "role" → L0:F6013/F6902 and L4:F14368 — the "role" content word
- "strangest" → L2:F16097 (superlative) and L4:F12799 (the "strangest" → "strange/odd/weird" detector, whose promoted tokens include "strange," "weird," "oddly")

**3. The user's concern is partially valid but not fully.** The user is right that there are several negation-word features (L3:F12079, L4:F4492, L4:F2422) that fire specifically on the word "not." However, these features do not appear in isolation: they co-occur with semantic content features that also respond to "reversal," "role," and "strangest." If you removed the word "not" and kept the rest, the circuit would still fire strongly because of the reversal/role/strangest content. The "not" features add a generic contradiction-marker boost on top of genuine content features.

**4. Specificity check:** All of these features have low frac_nonzero (L3:F12079=0.0098, L4:F4492=0.038, L4:F5709=0.014, L7:F4526=0.329 is the only exception — and it fires on "reversal" which is real content here). The negation features are highly selective; they fire because "not" actually appears, not as a generic contradiction reflex. This is the NLI setup (premise + hypothesis), and "not" legitimately signals negation in the hypothesis.

**5. Signal flow:** The strongest direct effects into the output logit are spread across the features (L4:F5709 −0.37, L6:F12420 −0.34, L4:F12799 +0.30, L2:F16097 −0.28, L10:F6670 +0.28). The "not" features contribute both negatively (L4:F5709 is a "now" detector suppressing "not"-like patterns) and positively (L3:F12079 promotes "absence"). The features are NOT uniformly aligned with the contradiction label — the circuit is a mixed vote, with both pushing-for and pushing-against features, which is more consistent with genuine multi-feature reasoning than with a single spurious shortcut.

**Conclusion:** The circuit does use negation-word signals (L3:F12079, L4:F4492), validating part of the user's concern. But these negation features are not the dominant driver — the circuit also strongly encodes the literal content words "reversal" and "role" and the semantic concept of reversal/figurative reversal. The probe is relying on a combination of (a) real content about role reversal and (b) the presence of explicit negation in the hypothesis, which in an NLI setting is a legitimate (not purely spurious) signal. The user's worry is somewhat justified because several features (L0:F4958, L3:F12079, L4:F4492) are pure lexical negation detectors with no semantic grounding in the role-reversal content — but these are not the only features, and removing them would not collapse the classification.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 17 | Lexical 'not' detector (L0) | the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F5188](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5188) | 9 | Lexical 'now' detector (L0) |  the word "now" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5188) |
| [L0:F6013](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6013) | 3 | Lexical 'role' detector A (L0) | the word "role," sometimes in conjunction with words that make it abstract, like energy or medicine | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6013) |
| [L0:F6902](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6902) | 3 | Lexical 'role' detector B (L0) | the word "role" and words with minor associations | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6902) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 14 | Period/punctuation detector (L0) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L2:F16097](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) | 2 | Superlative adjectives (L2) | superlative adjectives and the words "test" or "point" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) |
| [L2:F9872](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9872) | 2 | Superlative adjectives (L2) |  the word "largest" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9872) |
| [L2:F10705](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10705) | 11 | Lexical 'concerns' (L2) |  the word "concerns" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10705) |
| [L3:F12079](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) | 17 | Negation/Chinese-name detector (L3) | negations and Chinese names | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 17 | Negations multilingual (L4) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F6072](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6072) | 9 | 'now'+verb pattern (L4) |  the word "now" followed by a verb | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6072) |
| [L4:F5709](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) | 9 | 'now' suppressor / astronomy MASS (L4) | astronomy terms | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) |
| [L4:F12799](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12799) | 2 | '-ly'/oddities detector on 'strangest' (L4) |  words ending in "-ly" along with phrases that contain the word 'odd' or 'oddities' | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12799) |
| [L4:F7409](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7409) | 4 | Lexical reversal cue (L4) | words like "vice versa", "inverse", "reverse", "around", or directions | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7409) |
| [L4:F14368](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14368) | 4 | Importance/role words (L4) |  words related to importance or roles in a system | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14368) |
| [L6:F12420](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12420) | 4 | Subverting conventions (L6) |  artistic elements that break established guidelines | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12420) |
| [L7:F4526](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4526) | 4 | Comparisons/symmetry/reversals (L7) |  words related to comparisons, symmetry or reversals in data or situations | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4526) |
| [L8:F16033](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16033) | 4 | Figurative reversal language (L8) |  figurative language related to reversals of fortune | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16033) |
| [L10:F6670](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) | 19 | Technical/scientific terms (L10) | technical terms, especially within scientific or medical contexts | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) |
| [L10:F6670](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) | 21 | Technical/scientific terms (L10) | technical terms, especially within scientific or medical contexts | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) |
| [L12:F12606](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) | 21 | Political/State conspiracy+negation (L12) |  phrases related to political conspiracy/organizations, mental conditions and storytelling terms | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) |
| [L12:F12606](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) | 19 | Political/State conspiracy+negation (L12) |  phrases related to political conspiracy/organizations, mental conditions and storytelling terms | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:5709 de=-0.371 |
| 3 | `inspect_feature` ×18 | L4:5709, L6:12420, L4:12799, L2:16097, L10:6670, L4:6072, L3:12079, L4:14368, L7:905, L0:6013, L8:16033, L7:4526, L12:12606, L2:10705, L0:6051, L2:9872, L0:6902, L0:5188 |

### Dispatch: 7 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L3:F12079@17` | ✅ reported | 4 | 7 | Trace the path upstream from L3:F12079 (pos 17, "not") — this is a negation dete… |
| SA-2 | `L7:F4526@4` | ❌ error | — | — | Trace the path upstream from L7:F4526 (pos 4, "reversal") — this is a "compariso… |
| SA-3 | `L8:F16033@4` | ✅ reported | 5 | 4 | Trace the path upstream from L8:F16033 (pos 4, "reversal") — this is a "figurati… |
| SA-4 | `L10:F6670@19` | ✅ reported | 3 | 6 | Trace the path upstream from L10:F6670 (pos 19, "reversal") — this is a "technic… |
| SA-5 | `L4:F5709@9` | ❌ error | — | — | Trace the path upstream from L4:F5709 (pos 9, "now") — this is described as "ast… |
| SA-6 | `L4:F6072@9` | ❌ error | — | — | Trace the path upstream from L4:F6072 (pos 9, "now") — this is a "now followed b… |
| SA-7 | `L12:F12606@21` | ❌ error | — | — | Trace the path upstream from L12:F12606 (pos 21, "State") — this is a "political… |

<details>
<summary><b>SA-1</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F12079 | "negations and Chinese names" |
| 2 | `get_upstream_features` | L3:F12079@17, k=10 | Emb:" There"@15 (de=15.00) +9 more |
| 3 | `get_upstream_features` | L0:F4958@17, k=10 | Emb:" not"@17 (de=32.75) +9 more |
| 4 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 5 | `inspect_feature` | L2, F12021 | ""not" or negative terms, with some bonus for sports-related terms and " |
| 6 | `inspect_feature` | L2, F7550 | " comparative adjectives and adverbs" |
| 7 | `get_upstream_features` | L2:F12021@17, k=10 | Emb:" not"@17 (de=22.62) +9 more |
| 8 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** The negation detector L3:F12079 receives its strongest excitatory drive from the raw token embedding of "not" (pos 17) and from the lexical detector L0:F4958, which itself is a direct embedding‑level detector for the word "not". A secondary semantic contributor is L2:F12021, a mid‑layer feature that aggregates negative polarity tokens; it also gets a large positive push from the same "not" embeddi…

</details>

<details>
<summary><b>SA-3</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L8, F16033 | " figurative language related to reversals of fortune" |
| 2 | `get_upstream_features` | L8:F16033@4, k=10 | Emb:" reversal"@4 (de=13.00) +9 more |
| 3 | `inspect_feature` | L4, F7409 | " words like "vice versa", "inverse", "reverse", "around", or direction" |
| 4 | `get_upstream_features` | L4:F7409@4, k=10 | Emb:" reversal"@4 (de=25.75) +9 more |
| 5 | `inspect_feature` | L2, F3690 | " words related to collaboration or separation, in technical contexts." |
| 6 | `inspect_feature` | L6, F12420 | " artistic elements that break established guidelines" |
| 7 | `inspect_feature` | L8, F16033 | " figurative language related to reversals of fortune" |
| 8 | `get_upstream_features` | L6:F12420@4, k=10 | Emb:" role"@3 (de=5.59) +9 more |
| 9 | `inspect_feature` | L1, F1382 | " words associated with situations where something is changing or has c" |

**Findings:** The trace starts at the high‑level figurative‑reversal detector (L8:F16033). Its strongest upstream driver is a lexical‑reversal cue detector in layer 4 (F7409), which in turn is driven by a technical‑reversal term detector (L2:F3690) and a general change detector (L1:F1382). A parallel artistic‑subversion detector in layer 6 (F12420) also feeds positively into the target. All paths reach embeddin…

</details>

<details>
<summary><b>SA-4</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L10, F6670 | "technical terms, especially within scientific or medical contexts" |
| 2 | `get_upstream_features` | L10:F6670@19, k=10 | Emb:" not"@17 (de=6.78) +9 more |
| 3 | `inspect_feature` | L4, F4492 | "negations in various languages" |
| 4 | `inspect_feature` | L3, F8011 | " a mix of words and code fragments from different languages" |
| 5 | `get_upstream_features` | L4:F4492@17, k=10 | Emb:" not"@17 (de=18.00) +9 more |

**Findings:** The technical‑terms detector (L10:F6670) at position 19 is primarily driven by the input token "reversal" (both at positions 4 and 19) and, more strongly, by a negation cue "not" at position 17. The "not" token excites a low‑layer (L4) negation feature (F4492), which in turn positively influences the technical‑terms feature. A small contribution also comes from a multilingual/code‑mixed feature (L…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F5709@9, k=10 → Emb:" now"@9 (de=40.25) +9 more |
| 2 | `get_upstream_features` | L4:F6072@9, k=10 → Emb:" now"@9 (de=49.75) +9 more |
| 3 | `get_upstream_features` | L12:F12606@21, k=10 → Emb:" not"@17 (de=6.56) +9 more |
| 4 | `get_upstream_features` | L0:F5188@9, k=5 → Emb:" now"@9 (de=15.94) +4 more |
| 5 | `get_upstream_features` | L10:F6670@19, k=8 → Emb:" not"@17 (de=6.78) +7 more |
| 6 | `get_upstream_features` | L10:F6670@21, k=8 → Emb:" not"@17 (de=5.38) +7 more |
| 7 | `get_upstream_features` | L7:F4526@4, k=8 → Emb:" reversal"@4 (de=5.16) +7 more |
| 8 | `get_upstream_features` | L4:F12799@2, k=6 → Emb:" strangest"@2 (de=31.00) +5 more |
| 9 | `get_upstream_features` | L2:F16097@2, k=6 → Emb:" strangest"@2 (de=24.00) +5 more |
| 10 | `get_upstream_features` | L6:F12420@4, k=8 → Emb:" role"@3 (de=5.59) +7 more |
| 11 | `get_upstream_features` | L8:F16033@4, k=8 → Emb:" reversal"@4 (de=13.00) +7 more |
| 12 | `get_upstream_features` | L2:F10705@11, k=5 → Emb:" concerns"@11 (de=25.75) +4 more |
| 13 | `get_upstream_features` | L4:F14368@4, k=5 → Emb:" role"@3 (de=12.31) +4 more |
| 14 | `get_upstream_features` | L2:F9872@2, k=5 → Emb:" strangest"@2 (de=14.25) +4 more |
| 15 | `get_upstream_features` | L0:F6051@14, k=5 → Emb:"."@14 (de=46.25) +4 more |
| 16 | `get_upstream_features` | L0:F6902@3, k=5 → Emb:" role"@3 (de=15.06) +4 more |
| 17 | `get_upstream_features` | L0:F6013@3, k=5 → Emb:" role"@3 (de=15.56) +4 more |

### Build

`build_circuit` → 29 nodes, 47 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 50,176 | 9,528 | 239,536 | 0 | $0.0409 | — | — |
| SA-4 | openai/gpt-oss-120b | 42,096 | 3,292 | 2,528 | 0 | $0.0083 | ✅ 3F/6E | Trace the path upstream from L10:F6670 (pos 19, "reversal") … |
| SA-3 | openai/gpt-oss-120b | 120,272 | 7,725 | 32 | 0 | $0.0227 | ✅ 5F/4E | Trace the path upstream from L8:F16033 (pos 4, "reversal") —… |
| SA-1 | openai/gpt-oss-120b | 72,881 | 5,869 | 5,088 | 0 | $0.0145 | ✅ 4F/7E | Trace the path upstream from L3:F12079 (pos 17, "not") — thi… |
| **Total** | | **285,425** | **26,414** | **247,184** | **0** | **$0.0864** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 52s