# Circuit Oracle Report
**Date:** 2026-07-28 07:21:37 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by a chain of features that encode **feminine gender markers** (pronouns "She/her", the word "She" at prompt start, "empowering", and named-entity person features) rather than by any nutrition-, dietitian-, or profession-specific concept.

**Confidence:** 9

**Reasoning:** Tracing the circuit from the output (probe direction) backward reveals that the two largest direct-effect features driving the score are **L18:F14677** "instances of women or girls being mentioned" (frac_nonzero 0.012, promoted tokens: herself/she/her) at the final position with direct_effect ~0.23, and **L19:F9685** "references to women's names and their roles or accomplishments" (frac_nonzero 0.014) at direct_effect ~0.15. Both are purely gender-reference features — the L18 feature is among the largest individual contributors to the probe and feeds directly into the output. Tracing these upstream at the final position (pos 29, end-of-prompt "She") confirms the largest single input is the embedding **" She" (pos 29)** with direct_effect 14.4 into L18:F14677, followed by **"She" (pos 1)** at 7.2. There is no signal from nutrition/profession vocabulary (e.g., L6:F11327 "food" at pos 15) feeding the late gender features — the food feature appears as an isolated late-side contributor (direct_effect 0.10 to probe) but does not propagate through the gender chain.

The mid-layers are stacked almost exclusively with feminine-pronoun detectors: **L6:F11646** "references to women, triggered by pronouns/titles" (frac_nonzero 0.02, promoted: herself/hers/ihrem/she), **L7:F8644** "woman's name in context" (suppresses the male direction, promoted: himself/him), **L12:F12940** "female pronoun/possessive" (frac 0.007, promoted: herself/herself/bint), **L14:F12501** "feminine pronoun" (frac 0.014, promoted: Obrigada/feminist/herself), and **L15:F3330** "personal stories of women with 'she'." All these feed forward with positive direct_effects into L18:F14677 and L19:F9685.

Tracing further back, the **"She" (pos 1)** embedding is the dominant driver: it pushes L4:F7864 (4.4), L6:F11646 (4.4), L0:F15382 "mentions of a female person," L2:F7672 "women by name/relationship," and L4:F15317 "named entities/characters or people." None of these mid-layer features encode profession, food expertise, or health-domain semantics — they are personhood + female features. The suppressors (L6:F16329 female first names, L7:F8644, L18:F14743 "He") indicate the probe is sensitive to the male/female axis, not profession. The **" empowering" (pos 5)** embedding also contributes (1.87 direct_effect to L18:F14677), reinforcing the female-empowerment frame rather than any dietitian/health-coach concept.

**Implication for the user's concern:** The user is correct. The circuit shows the profession-classification probe is using **spurious gender features** (female-pronoun detectors running from L0 through L19, terminating in L18:F14677 / L19:F9685) as its primary signal. Genuine profession indicators such as food/nutrition vocabulary (L6:F11327) are present but contribute only weakly and are not part of the dominant path. The probe likely learned "female subject of a health/wellness biographical snippet" rather than "dietitian/nutritionist," which is a textbook spurious correlation — the model's notion of who is a dietitian is mediated by gendered pronoun statistics in the training data.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: She (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 29 | Emb: She (pos 29, end of prompt) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: empowering (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: food (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 1 | Early female-person detector (L0:F15382) | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 29 | Early female-person detector (L0:F15382) | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L2:F7672](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) | 1 | Women-by-name/relationship (L2:F7672) |  mentions of women by name and relationship | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) |
| [L2:F7672](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) | 2 | Women-by-name/relationship (L2:F7672) |  mentions of women by name and relationship | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Mixed pronoun/code feature (L4:F7864) | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Named-entity/people feature (L4:F15317) |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 3 | Named-entity/people feature (L4:F15317) |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Female pronoun/title feature (L6:F11646) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Female pronoun/title feature (L6:F11646) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 3 | Female pronoun/title feature (L6:F11646) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 29 | Female pronoun/title feature (L6:F11646) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 1 | Female first names (L6:F16329) — suppressor | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 29 | Female first names (L6:F16329) — suppressor | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 15 | Food/nutrition vocabulary (L6:F11327) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 19 | Woman's name in context (L7:F8644) — suppressor |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 29 | Woman's name in context (L7:F8644) — suppressor |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Female pronoun/possessive (L12:F12940) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L14:F12501](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) | 3 | Feminine pronoun (L14:F12501) |  uses of the feminine pronoun. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 29 | Personal story of woman with 'she' (L15:F3330) |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 29 | Person+pronoun reference (L17:F5889) |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Women/girls mentions (L18:F14677) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 29 | Women/girls mentions (L18:F14677) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 40 | Women/girls mentions (L18:F14677) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 66 | Women/girls mentions (L18:F14677) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 29 | He (L18:F14743) — suppressor | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 29 | Women's names and roles (L19:F9685) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe classification score (output direction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.340 |
| 3 | `inspect_feature` ×13 | L6:11646, L18:14677, L4:7864, L12:12940, L19:9685, L4:15317, L2:7672, L14:12501, L6:11327, L6:16329, L7:8644, L0:2349, L18:14743 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@29` | ❌ error | — | — | Trace L18:F14677 (women/girls references) upstream. Identify the input tokens th… |
| SA-2 | `L19:F9685@29` | ❌ error | — | — | Trace L19:F9685 (women's names and roles) upstream. What tokens drive this featu… |
| SA-3 | `L6:F11646@1` | ❌ error | — | — | Trace L6:F11646 (women pronouns/titles) upstream. Find what embedding tokens dri… |
| SA-4 | `L12:F12940@2` | ❌ error | — | — | Trace L12:F12940 (female pronouns/possessives) upstream. Find which input tokens… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14677@29, k=15 → Emb:" She"@29 (de=14.38) +14 more |
| 2 | `get_upstream_features` | L19:F9685@29, k=15 → Emb:" She"@29 (de=5.62) +14 more |
| 3 | `get_upstream_features` | L6:F11646@1, k=15 → Emb:"She"@1 (de=19.25) +14 more |
| 4 | `get_upstream_features` | L12:F12940@2, k=15 → Emb:"She"@1 (de=6.56) +14 more |
| 5 | `get_upstream_features` | L4:F7864@1, k=12 → Emb:"She"@1 (de=24.62) +11 more |
| 6 | `inspect_feature` ×2 | L17:5889, L14:12501 |
| 7 | `get_upstream_features` | L7:F8644@29, k=12 → Emb:"She"@1 (de=8.31) +11 more |
| 8 | `get_upstream_features` | L14:F12501@3, k=12 → L13:F11685 (de=-7.72) +11 more |
| 9 | `get_upstream_features` | L4:F15317@2, k=10 → Emb:"She"@1 (de=13.12) +9 more |
| 10 | `inspect_feature` ×3 | L15:3330, L0:15382, L6:11327 |
| 11 | `get_upstream_features` | L6:F11327@15, k=10 → Emb:" food"@15 (de=34.00) +9 more |

### Build

`build_circuit` → 20 nodes, 34 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 43,485 | 6,426 | 251,134 | 0 | $0.0358 | — | — |
| **Total** | | **43,485** | **6,426** | **251,134** | **0** | **$0.0358** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 27s