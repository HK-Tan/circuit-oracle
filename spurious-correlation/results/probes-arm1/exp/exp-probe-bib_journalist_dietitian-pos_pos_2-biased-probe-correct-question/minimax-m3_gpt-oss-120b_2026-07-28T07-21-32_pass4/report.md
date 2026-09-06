# Circuit Oracle Report
**Date:** 2026-07-28 07:21:32 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven primarily by a deep, multi-layer "female pronoun" circuit originating from the tokens "She" at positions 1 and 23, with only a thin profession-keyword branch from "nutrition" at position 13 reaching the output.

**Confidence:** 8

**Reasoning:** The circuit is dominated by gender features, not profession features. At the top of the circuit, the single largest contributor to the probe score is **L18:F14677** (label: "instances of women or girls being mentioned", activation=34.5, direct_effect=0.24), with its upstream chain traced unambiguously to the **embedding of "She" at position 23** (direct_effect=14.3) and **"She" at position 1** (direct_effect=6.8) — the strongest direct embedding inputs in the entire graph. **L18:F14743** ("He" detector) provides a negative contribution (-0.11), confirming the gender axis is the discriminator, not the profession. The mid-layer supernode (L10–L14) reinforces this signal through **L12:F12940** ("female pronouns and possessive pronouns", direct_effect=0.29 at pos 2, fed by the "She" embedding at pos 1 with direct_effect=6.03), **L14:F12501** ("uses of the feminine pronoun", direct_effect=0.15), and **L10:F14965** ("terms relating to women", direct_effect=0.16). These mid-layer features themselves decompose back to the "She" embedding and to the early-layer L6:F11646 ("references to women, potentially triggered by pronouns and titles", the #1 overall feature, direct_effect=0.36 at pos 1, direct_effect=0.29 at pos 2), whose own strongest upstream input is the "She" token embedding (direct_effect=19.25) — overwhelmingly dominant over L4:F7864 (xml/code, 4.4) and the <bos> embedding (1.6). The early layer also includes L6:F16329 ("female first names and their possessive forms", but acting as a suppressor with negative direct_effect around -0.17) and L0:F12519 (which appears to inhibit the L6:11646 path with direct_effect=-2.25 from the "She" embedding — a sign of balancing male-gender pressure). 

By contrast, the **profession branch is tiny**: only three food/nutrition features contribute to the probe output. L6:F11327 ("words or phrases related to food or nutrition", direct_effect=0.15 at pos 13) traces cleanly to the **"nutrition" embedding at position 13** (direct_effect=21.0) and is supported by L4:F13412 ("diets and dietary health", 0.13) and L4:F9554 ("food, rations and feeding", ~0.06 in the upstream chain). These profession features are present in the circuit but their combined weight is much smaller than the gender chain. None of the late-layer (L18–L19) output-driving features are activated by nutrition/cooking tokens; the high-layer "is this a woman" detectors carry the score.

The user's concern is **well-supported by the circuit**: the probe leans heavily on the female-pronoun axis ("She" at positions 1 and 23) as a spurious proxy for the profession. The genuine profession indicators (nutrition, food, diet keywords) are present in the early/mid layers but do not propagate into the late-layer classification features the way the gender signal does. This is a textbook gender-confound pattern: a probe trained to detect "nutritionist" features will latch onto female-pronoun frequency as a shortcut because nutritionists in the training data are disproportionately female.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 23 | Probe output (classification score) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 23 | Late-layer women/gender detectors (L18-L19) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Late-layer women/gender detectors (L18-L19) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 23 | Late-layer women/gender detectors (L18-L19) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 23 | Late-layer women/gender detectors (L18-L19) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 23 | Late-layer women/gender detectors (L18-L19) |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 23 | Late-layer women/gender detectors (L18-L19) |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L14:F5740](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5740) | 23 | Late-layer women/gender detectors (L18-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5740) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 23 | Late-layer women/gender detectors (L18-L19) | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Mid-layer female pronoun/possessive features (L10-L14) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 3 | Mid-layer female pronoun/possessive features (L10-L14) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L14:F12501](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) | 2 | Mid-layer female pronoun/possessive features (L10-L14) |  uses of the feminine pronoun. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) |
| [L10:F14965](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) | 2 | Mid-layer female pronoun/possessive features (L10-L14) |  terms relating to women | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) |
| [L13:F11685](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/11685) | 23 | Mid-layer female pronoun/possessive features (L10-L14) | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/11685) |
| [L13:F6622](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) | 23 | Mid-layer female pronoun/possessive features (L10-L14) | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 23 | Mid-layer female pronoun/possessive features (L10-L14) |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 2 | Mid-layer female pronoun/possessive features (L10-L14) |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L8:F7245](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7245) | 2 | Mid-layer female pronoun/possessive features (L10-L14) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7245) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Early-layer women/pronoun features (L2-L6) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Early-layer women/pronoun features (L2-L6) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 23 | Early-layer women/pronoun features (L2-L6) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 1 | Early-layer women/pronoun features (L2-L6) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 2 | Early-layer women/pronoun features (L2-L6) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 23 | Early-layer women/pronoun features (L2-L6) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 23 | Early-layer women/pronoun features (L2-L6) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 2 | Early-layer women/pronoun features (L2-L6) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L2:F7672](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) | 1 | Early-layer women/pronoun features (L2-L6) |  mentions of women by name and relationship | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) |
| [L2:F2128](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2128) | 1 | Early-layer women/pronoun features (L2-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2128) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Early-layer women/pronoun features (L2-L6) |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Early-layer women/pronoun features (L2-L6) | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L0:F12519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) | 1 | Early-layer women/pronoun features (L2-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 13 | Profession/food keywords (L4-L6) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 13 | Profession/food keywords (L4-L6) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 13 | Profession/food keywords (L4-L6) |  words related to food, rations and feeding | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.357 |
| 3 | `inspect_feature` ×14 | L6:11646, L12:12940, L18:14677, L4:15317, L4:7864, L6:16329, L10:14965, L6:11327, L14:12501, L19:9685, L2:7672, L4:13412, L7:8644, L18:14743 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@23` | ❌ error | — | — | Trace from this "instances of women or girls being mentioned" feature (L18:F1467… |
| SA-2 | `L6:F11646@1` | ❌ error | — | — | Trace from this "references to women, potentially triggered by pronouns and titl… |
| SA-3 | `L6:F11327@13` | ❌ error | — | — | Trace from this "words or phrases related to food or nutrition" feature (L6:F113… |
| SA-4 | `L12:F12940@2` | ❌ error | — | — | Trace from this "female pronouns and possessive pronouns" feature (L12:F12940 at… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14677@23, k=20 → Emb:" She"@23 (de=14.31) +19 more |
| 2 | `get_upstream_features` | L6:F11646@1, k=20 → Emb:"She"@1 (de=19.25) +19 more |
| 3 | `get_upstream_features` | L6:F11327@13, k=20 → Emb:" nutrition"@13 (de=21.00) +19 more |
| 4 | `get_upstream_features` | L12:F12940@2, k=20 → Emb:"She"@1 (de=6.03) +19 more |
| 5 | `inspect_feature` ×8 | L4:15317, L4:13412, L10:14965, L17:5889, L15:3330, L0:15382, L7:2765, L4:9554 |
| 6 | `get_upstream_features` | L19:F9685@23, k=10 → Emb:" She"@23 (de=5.72) +9 more |
| 7 | `get_upstream_features` | L18:F14677@1, k=10 → Emb:"She"@1 (de=27.12) +9 more |
| 8 | `get_upstream_features` | L14:F12501@2, k=10 → L12:F12940 (de=13.56) +9 more |
| 9 | `get_upstream_features` | L10:F14965@2, k=10 → L4:F15317 (de=5.56) +9 more |
| 10 | `get_upstream_features` | L14:F12501@23, k=8 → ❌ Feature (layer=14, feature_idx=12501) not found at pos=23. T |
| 11 | `get_upstream_features` | L6:F16329@1, k=8 → Emb:"She"@1 (de=8.94) +7 more |
| 12 | `get_upstream_features` | L4:F7864@1, k=5 → Emb:"She"@1 (de=24.62) +4 more |
| 13 | `get_upstream_features` | L0:F12519@1, k=3 → Emb:"She"@1 (de=21.88) +2 more |

### Build

`build_circuit` → 9 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 56,582 | 5,290 | 290,630 | 0 | $0.0408 | — | — |
| **Total** | | **56,582** | **5,290** | **290,630** | **0** | **$0.0408** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 26s