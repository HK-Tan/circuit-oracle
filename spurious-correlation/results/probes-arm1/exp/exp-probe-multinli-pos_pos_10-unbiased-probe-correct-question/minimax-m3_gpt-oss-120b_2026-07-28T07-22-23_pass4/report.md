# Circuit Oracle Report
**Date:** 2026-07-28 07:22:23 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_10 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "contradiction" score is driven by an over-representation of superficial, lexical-cue features — most prominently negation detectors (the "not" token at pos 17), the "now" token at pos 9, and "reversal"/"reversed" symmetry features at pos 4 — rather than any genuine semantic-comparison circuit that would actually compute entailment/contradiction between premise and hypothesis.

**Confidence:** 8

**Reasoning:** The user concern is essentially confirmed by the circuit topology. Of the 15 top features driving the probe, at least 7 are explicit negation/contradiction-words detectors and another 2–3 are reversal/symmetry vocabulary detectors, with no circuit component performing premise–hypothesis alignment on the underlying proposition:

1. **The "not" token is the single largest signal source.** The "Emb: not (pos 17)" embedding directly drives L0:F4958 (the "not" feature, frac_nonzero=0.018, direct_effect +3.52 to L3:F12079, which in turn pushes the probe +0.231), L3:F1101 (negation/absence, +1.5→L9:F14687, "not ... because/but" phrase feature, +1.33→L10:F6670, +0.275 to the probe), and L4:F4492 (negations in various languages, +2.97→L10:F6670, and +2.09→L12:F12606, +0.213 to the probe). The hypothesis sentence literally contains the word "not" (the *negation* of the premise), so these features fire trivially on that token without any reference to the *content* being negated.

2. **"Reversal/reversed" vocabulary is the second largest signal source.** Emb:"reversal (pos 4)" activates L4:F7409 ("vice versa, inverse, reverse, around", frac_nonzero=0.0096, +3.70 to L8:F16033, "figurative language related to reversals of fortune", +0.216 to probe), L6:F2743 (symmetry/equivalence, +1.58→L8:F16033), and L3:F12544 (legal/military terminology about reversal, +0.74 inhibiting L7:F4526, "comparisons, symmetry or reversals"). This is purely vocabulary matching on the word "reversal" in the premise.

3. **"Strangest" (pos 2) and superlative features.** L2:F16097 (superlative adjectives, direct_effect −0.279 to probe — *inhibits* contradiction!) feeds into L4:F12799 ("-ly words + odd/oddities", promoted tokens: weird/strangely/odd/strange, frac_nonzero=0.0083, +0.297 to probe). These are lexical cues that fire on the adjective form, not on any semantic property.

4. **"Now" (pos 9)** activates L4:F6072 ("the word 'now' followed by a verb", +0.248 to probe). This is a pure temporal-deixis word detector.

5. **"Role" (pos 3)** activates L0:F6013 ("the word 'role'", frac_nonzero=0.029, +0.220 to probe) and L4:F14368 ("words related to importance or roles", +0.223 away from probe). The two features push in opposite directions — a sign of generic vocabulary competition rather than concept binding.

6. **"Concerns" (pos 11)** and L12:F12606 ("political conspiracy, mental conditions, storytelling", +0.213 to probe) are also lexical-bag detectors; L12:F12606 is fed by Emb:"not (pos 17)" and the negation feature chain, not by any premise/hypothesis interaction.

Critically, **no feature in the top 15 (and none revealed in upstream tracing) actually compares the proposition "role reversal is going on regarding democracy" against "no role reversal is going on regarding democracy."** There is no entity-recognition feature for "democracy" feeding the probe in a way that would track whether it is *the same entity* across sentences; L12:F12606 is just a "State/conspiracy" vocabulary detector. The hypothesis's negation of the premise is detected entirely by the bare "not" word, and the premise's claim is detected by the bare "reversal/strangest/role/now" words. This is the textbook definition of a spurious-cue NLI heuristic (the so-called "HANS" failure mode): the probe classifies the second sentence as a contradiction because (a) it contains the word "not" and (b) it shares many content words with the premise, exactly the surface-level cues a bag-of-words model would exploit, with no compositional entailment reasoning. The user's hypothesis — that the circuit uses spurious negation/vocabulary signals rather than prompt content for contradiction — is well supported.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 22 | Probe Output (Contradiction Score) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L4:F5709](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) | 9 | Negation Features (L0-L12) - "not" token detectors | astronomy terms | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) |
| [L6:F12420](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12420) | 4 | Negation Features (L0-L12) - "not" token detectors |  artistic elements that break established guidelines | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12420) |
| [L3:F12079](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) | 17 | Negation Features (L0-L12) - "not" token detectors | negations and Chinese names | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 17 | Negation Features (L0-L12) - "not" token detectors | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 17 | Negation Features (L0-L12) - "not" token detectors | negations in other languages like French, Malay, and Croatian | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L3:F1101](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) | 17 | Negation Features (L0-L12) - "not" token detectors |  error messages and terms indicating absence or negation in software contexts. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 17 | Negation Features (L0-L12) - "not" token detectors |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L9:F14687](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/14687) | 17 | Negation Features (L0-L12) - "not" token detectors | phrases using the word "not", often followed by "because" or "but." | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/14687) |
| [L10:F6670](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) | 19 | Negation Features (L0-L12) - "not" token detectors | technical terms, especially within scientific or medical contexts | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) |
| [L12:F12606](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) | 21 | Negation Features (L0-L12) - "not" token detectors |  phrases related to political conspiracy/organizations, mental conditions and storytelling terms | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) |
| [L4:F6072](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6072) | 9 | Reversal/Symmetry Features (L2-L8) - "reversal/reversed" |  the word "now" followed by a verb | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6072) |
| [L8:F16033](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16033) | 4 | Reversal/Symmetry Features (L2-L8) - "reversal/reversed" |  figurative language related to reversals of fortune | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16033) |
| [L7:F4526](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4526) | 4 | Reversal/Symmetry Features (L2-L8) - "reversal/reversed" |  words related to comparisons, symmetry or reversals in data or situations | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4526) |
| [L7:F905](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/905) | 4 | Reversal/Symmetry Features (L2-L8) - "reversal/reversed" |  words indicating amounts, changes, or trends | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/905) |
| [L4:F7409](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7409) | 4 | Reversal/Symmetry Features (L2-L8) - "reversal/reversed" |  words like "vice versa", "inverse", "reverse", "around", or directions | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7409) |
| [L6:F2743](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2743) | 4 | Reversal/Symmetry Features (L2-L8) - "reversal/reversed" |  scientific terms and phrases related to symmetry and equivalence | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2743) |
| [L3:F12544](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12544) | 4 | Reversal/Symmetry Features (L2-L8) - "reversal/reversed" |  legal and military terminology, and words indicating opposition or change | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12544) |
| [L5:F9068](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9068) | 4 | Reversal/Symmetry Features (L2-L8) - "reversal/reversed" | words and phrases related to populations | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9068) |
| [L2:F16097](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) | 2 | Superlative/Adjective Features (L2-L4) - "strangest" | superlative adjectives and the words "test" or "point" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) |
| [L4:F12799](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12799) | 2 | Superlative/Adjective Features (L2-L4) - "strangest" |  words ending in "-ly" along with phrases that contain the word 'odd' or 'oddities' | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12799) |
| [L3:F319](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/319) | 2 | Superlative/Adjective Features (L2-L4) - "strangest" | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/319) |
| [L2:F10827](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10827) | 2 | Superlative/Adjective Features (L2-L4) - "strangest" | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10827) |
| [L0:F6013](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6013) | 3 | "role" token Features (L0-L4) | the word "role," sometimes in conjunction with words that make it abstract, like energy or medicine | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6013) |
| [L4:F14368](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14368) | 4 | "role" token Features (L0-L4) |  words related to importance or roles in a system | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14368) |
| [L2:F10705](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10705) | 11 | "concerns" Feature (L2) |  the word "concerns" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10705) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: not (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: strangest (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: reversal (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: role (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: now (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: democracy (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:5709 de=-0.371 |
| 3 | `inspect_feature` ×15 | L4:5709, L6:12420, L4:12799, L2:16097, L10:6670, L4:6072, L3:12079, L7:905, L4:14368, L0:6013, L8:16033, L7:4526, L12:12606, L2:10705, L0:6051 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L3:F12079@17` | ❌ error | — | — | Trace the L3:F12079 (label: "negations and Chinese names") upstream to embedding… |
| SA-2 | `L4:F12799@2` | ❌ error | — | — | Trace L4:F12799 (label: "-ly words + odd/oddities", promoted: weird, strangely, … |
| SA-3 | `L8:F16033@4` | ❌ error | — | — | Trace L8:F16033 ("figurative language related to reversals of fortune") upstream… |
| SA-4 | `L2:F16097@2` | ❌ error | — | — | Trace L2:F16097 (label: "superlative adjectives and test/point") upstream. This … |
| SA-5 | `L0:F6013@3` | ❌ error | — | — | Trace L0:F6013 (label: "the word 'role'") upstream. This fires at pos 3 ("role")… |
| SA-6 | `L7:F905@4` | ❌ error | — | — | Trace L7:F905 ("words indicating amounts, changes, or trends") upstream. This is… |
| SA-7 | `L10:F6670@19` | ❌ error | — | — | Trace L10:F6670 (label: "technical/scientific terms") upstream. This fires at po… |
| SA-8 | `L12:F12606@21` | ❌ error | — | — | Trace L12:F12606 ("political conspiracy, mental conditions, storytelling") upstr… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L3:F12079@17, k=10 → Emb:" There"@15 (de=15.00) +9 more |
| 2 | `get_upstream_features` | L4:F12799@2, k=10 → Emb:" strangest"@2 (de=31.00) +9 more |
| 3 | `get_upstream_features` | L8:F16033@4, k=10 → Emb:" reversal"@4 (de=13.00) +9 more |
| 4 | `get_upstream_features` | L2:F16097@2, k=10 → Emb:" strangest"@2 (de=24.00) +9 more |
| 5 | `get_upstream_features` | L7:F905@4, k=10 → Emb:" reversal"@4 (de=6.88) +9 more |
| 6 | `get_upstream_features` | L10:F6670@19, k=10 → Emb:" not"@17 (de=6.78) +9 more |
| 7 | `get_upstream_features` | L12:F12606@21, k=10 → Emb:" not"@17 (de=6.56) +9 more |
| 8 | `get_upstream_features` | L0:F6013@3, k=10 → Emb:" role"@3 (de=15.56) +9 more |
| 9 | `get_upstream_features` | L6:F12420@4, k=10 → Emb:" role"@3 (de=5.59) +9 more |
| 10 | `get_upstream_features` | L7:F4526@4, k=10 → Emb:" reversal"@4 (de=5.16) +9 more |
| 11 | `get_upstream_features` | L4:F6072@9, k=10 → Emb:" now"@9 (de=49.75) +9 more |
| 12 | `inspect_feature` ×10 | L4:4492, L4:2422, L3:1101, L4:7409, L6:2743, L0:4958, L3:12544, L9:14687, L3:10225, L5:9068 |

### Build

`build_circuit` → 13 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 63,400 | 6,129 | 193,592 | 0 | $0.0380 | — | — |
| **Total** | | **63,400** | **6,129** | **193,592** | **0** | **$0.0380** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 22s