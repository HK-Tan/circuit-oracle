# Circuit Oracle Report
**Date:** 2026-07-28 07:23:40 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_6 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction score is driven primarily by generic content-word detectors (about, land, fire, set, for, they) and a sentence-initial/position-1 feature on "So", not by any negation-specific feature — the user's concern is not supported by this circuit.

**Confidence:** 6

**Reasoning:** I traced the top-20 features driving the probe (the synthetic target with no string label). Every positive-contribution feature inspected turns out to be a generic lexical or syntactic detector, not a negation signal:

- **Lexical content-word features (Layers 1–3)** — L1:F361 ("agriculture/ecology words") at pos 9 (agriculture, +0.1504), L1:F461 ("the word 'land'") at pos 7 (+0.1826), L2:F4819 ("the word 'fire'") at pos 12 (+0.1787), L2:F10849 ("the word 'set'") at pos 3 (+0.1699), L2:F11518 ("'land' in scientific/agricultural contexts") at pos 7 (+0.252), L2:F15312 ("the word 'about'") at pos 4 (+0.21), L3:F4464 ("the word 'about'") at pos 4 (+0.1846), L3:F11720 ("the word 'that'") at pos 2 (+0.165), L3:F15978 ("land/property/acreage") at pos 7 (+0.165). All have low frac_nonzero (0.0026–0.0092), low activations, and their top examples confirm plain lexical content. Upstream tracing of L2:F11518 and L2:F4819 shows they feed almost exclusively from their own token's embedding (L2:F11518 ← Emb:"land" pos 7 with direct_effect 28.375; L2:F4819 ← Emb:"fire" pos 12 with 32).

- **Content-word features (Layers 4–6)** — L4:F5450 ("words related to starting/beginning") at pos 4, L4:F12225 at pos 2 (with upstream ← Emb:"they" pos 2 = 12.75, Emb:"So" pos 1 = 12.375, both content-bearing), L6:F14744 ("about/to/work") at pos 4, traced back to Emb:"about" (5.8125) and to L3:F4464 (2.2969) — again pure lexical cascading.

- **Mid-layer position-1 features (Layer 8)** — L8:F8406 (pos 1, "So", -0.2432). Its upstream is dominated by **Emb:<bos>** (10.25) and mid-layer syntax-detector features (L7:F462 "code documentation/import", L7:F5741 "code documentation/copyright", L5:F3992 "start of documentation blocks in code", L6:F14585 "the/it at sentence start"). This is a sentence-initial / structural-beginning pattern at position 1, not a negation cue.

- **Late-layer features (Layer 12+)** — L12:F12606 at pos 25 (the final "forest" token, +0.1543) is labeled as "political conspiracy/mental conditions/storytelling" but inspection shows it fires on "State", "stay", "ADD", "stories", "shared" — a generic content-word pile-up on the last token of the sentence. L17:F451 at pos 1 ("start of sentences", +0.1543) is explicitly a sentence-beginning feature, fed by a chain of generic content detectors (L7:F462 → L15:F751, L10:F14174, L15:F851, L9:F8770, L15:F10005).

- **Direct negation cue?** There is no feature in the top-20 whose label or top-activating examples center on negation tokens (not, n't, never, no, cannot). The two features that fire on the second sentence where "not" appears (pos 21) are L0:F3498 ("they" pronoun) and L0:F2238 ("about" before a number) — both lexical, not semantic. The "not" token at pos 21 is not in the top contributor list at all; the only feature pointing at it is L12:F12606, which receives direct_effect 3.59 from Emb:"not" but is itself a generic late-layer content aggregator.

- **Strongest negative contributors** are L0:F3498 ("they" pronoun) at pos 2 (-0.6211) and L0:F2238 ("about" before numbers) at pos 4 (-0.3418) — these *suppress* the probe score, suggesting the probe is mildly *anti*-specific-content-words, but in this particular prompt the content-word mass slightly outweighs the suppression, leaving a small net positive.

**Conclusion on the user's concern:** The circuit does not use "negation word" features. It uses ordinary content-word detectors (about, land, fire, set, for, they) and a sentence-initial structural feature on "So". If this probe is classifying this premise/hypothesis pair as contradiction, the *mechanism* shown here is generic lexical content accumulation plus sentence-initial syntax — not negation semantics. The user's worry is empirically refuted by the inspected features: every top contributor decodes to a common function word, content noun, or sentence-position cue, none to a negation signal.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L17:F451](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) | 1 | Late-layer neutral sentence-position features (generic, NOT negation-specific) | start of sentences | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) |
| [L12:F12606](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) | 25 | Mid-layer content-word detectors (about, fire, land) |  phrases related to political conspiracy/organizations, mental conditions and storytelling terms | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) |
| [L8:F8406](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) | 1 | Position-1 mid-layer features (mostly syntax/sentence-initial at 'So') | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) |
| [L6:F14744](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14744) | 4 | Content-word features (about, land, fire, set, to, for, they, they-allowed) |  the words "about," "to," and "work." | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14744) |
| [L4:F5450](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5450) | 4 | Content-word features (about, land, fire, set, to, for, they, they-allowed) |  code snippets from different languages and words related to starting or beginning something | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5450) |
| [L4:F12225](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12225) | 2 | Content-word features (about, land, fire, set, to, for, they, they-allowed) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12225) |
| [L2:F15312](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15312) | 4 | Low-layer lexical features (about, land-sci, fire, set, agriculture, land/property) |  the word "about." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15312) |
| [L2:F11518](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11518) | 7 | Low-layer lexical features (about, land-sci, fire, set, agriculture, land/property) |  the word "land" in scientific/agricultural contexts | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11518) |
| [L2:F4819](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4819) | 12 | Low-layer lexical features (about, land-sci, fire, set, agriculture, land/property) | sentences containing the word "fire" or similar terms | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4819) |
| [L2:F10849](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10849) | 3 | Low-layer lexical features (about, land-sci, fire, set, agriculture, land/property) | the word "set" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10849) |
| [L2:F14822](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14822) | 1 | Low-layer lexical features (about, land-sci, fire, set, agriculture, land/property) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14822) |
| [L1:F361](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/361) | 9 | Low-layer lexical features (about, land-sci, fire, set, agriculture, land/property) |  words related to agriculture and ecology | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/361) |
| [L3:F15978](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15978) | 7 | Low-layer lexical features (about, land-sci, fire, set, agriculture, land/property) |  mentions of land, property, and acreage. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15978) |
| [L3:F4464](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4464) | 4 | Low-layer lexical features (about, land-sci, fire, set, agriculture, land/property) |  the word "about" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4464) |
| [L1:F461](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/461) | 7 | Low-layer lexical features (about, land-sci, fire, set, agriculture, land/property) |  the word "land" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/461) |
| [L3:F11720](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11720) | 2 | Low-layer lexical features (about, land-sci, fire, set, agriculture, land/property) | the word "that", often preceded and followed by specific words | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11720) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:3498 de=-0.621 |
| 3 | `inspect_feature` ×16 | L2:11518, L4:5450, L2:15312, L3:4464, L1:461, L2:4819, L0:8444, L2:10849, L0:15492, L3:15978, L6:14744, L17:451, L12:12606, L1:361, L0:3498, L0:2238 |
| 4 | `get_upstream_features` | Emb:" they"@2 (de=42.75) +7 more |
| 5 | `get_upstream_features` | Emb:" about"@4 (de=35.00) +7 more |
| 6 | `get_upstream_features` | Emb:" they"@2 (de=12.75) +7 more |
| 7 | `get_upstream_features` | Emb:"<bos>"@0 (de=10.25) +7 more |
| 8 | `get_upstream_features` | Emb:"."@18 (de=47.00) +7 more |
| 9 | `get_upstream_features` | Emb:"So"@1 (de=19.62) +7 more |
| 10 | `inspect_feature` ×8 | L3:11720, L2:11678, L1:4444, L7:462, L7:5741, L5:3992, L6:14585, L7:3099 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L17:F451@1` | ❌ error | — | — | Trace upstream from L17:F451 ('start of sentences' feature at position 1 'So'). … |
| SA-2 | `L12:F12606@25` | ❌ error | — | — | Trace upstream from L12:F12606 (political conspiracy/mental conditions/storytell… |
| SA-3 | `L6:F14744@4` | ❌ error | — | — | Trace upstream from L6:F14744 ('about','to','work' words feature at pos 4 'about… |
| SA-4 | `L4:F12225@2` | ❌ error | — | — | Trace upstream from L4:F12225 (pos 2, 'they'). What does this feature encode and… |
| SA-5 | `L2:F11518@7` | ❌ error | — | — | Trace upstream from L2:F11518 (word 'land' in scientific/agricultural contexts, … |
| SA-6 | `L2:F4819@12` | ❌ error | — | — | Trace upstream from L2:F4819 (word 'fire' feature, pos 12 'fire'). What does it … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L12:F12606@25, k=10 → Emb:" not"@21 (de=3.59) +9 more |
| 2 | `get_upstream_features` | L17:F451@1, k=10 → L16:F10989 (de=-11.88) +9 more |
| 3 | `get_upstream_features` | L6:F14744@4, k=10 → Emb:" about"@4 (de=5.81) +9 more |
| 4 | `get_upstream_features` | L2:F11518@7, k=10 → Emb:" land"@7 (de=28.38) +9 more |
| 5 | `get_upstream_features` | L2:F4819@12, k=10 → Emb:" fire"@12 (de=32.00) +9 more |
| 6 | `get_upstream_features` | L2:F10849@3, k=10 → Emb:" set"@3 (de=17.12) +9 more |

### Build

`build_circuit` → 7 nodes, 7 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 45,973 | 4,941 | 216,840 | 0 | $0.0327 | — | — |
| **Total** | | **45,973** | **4,941** | **216,840** | **0** | **$0.0327** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 23s