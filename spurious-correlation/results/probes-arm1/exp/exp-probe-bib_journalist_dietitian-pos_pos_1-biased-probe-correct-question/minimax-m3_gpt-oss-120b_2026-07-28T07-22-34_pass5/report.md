# Circuit Oracle Report
**Date:** 2026-07-28 07:22:34 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's positive classification score is dominated by female-gender/feminine-pronoun features (L18 "women/girls mentioned," L12 "female pronouns," L6 "references to women," L14 "feminine pronoun") that fire on the input token "She" and "loves" — i.e., the model is using gender markers rather than nutrition/dietitian profession cues to score the profession.

**Confidence:** 8

**Reasoning:** Tracing the top positive drivers of the probe (returned by `get_top_features` for the synthetic target) reveals an almost entirely gender-based circuit. The **largest single positive contribution is L6:11646** ("references to women, potentially triggered by pronouns and titles," direct_effect +0.375, frac_nonzero 0.020) firing on positions 1 ("She") and 2 ("loves") — i.e., on the female pronoun itself. The **second-largest positive driver is L18:14677** ("instances of women or girls being mentioned," direct_effect +0.247, frac_nonzero 0.012) firing on positions 1, 12 ("Sarah"), and 34 ("Sarah's") — the "She", the name "Sarah", and the possessive "Sarah's". Tracing L18:14677 upstream one hop returns the **"She" token embedding as the dominant contributor (direct_effect +27.1)** plus L6:11646 (the same women-references feature). Other strong positive drivers — **L12:12940 "references to female pronouns and possessive pronouns" (+0.252)**, **L14:12501 "uses of the feminine pronoun" (+0.130)**, **L7:2765 "mentions of people/characters…personal details" (cumulative ~+0.58 across positions 2, 5, 11, 12)** — all directly promote feminine pronoun tokens in their decoder projections ("herself," "she," "her," "Autorin") and are sourced by the same "She" and "loves" embeddings. 

Crucially, the only direct **content/profession-related** signals are negative or absent: **L1:15251** (the word "client") has direct_effect **−0.170** (suppresses the probe score), and there is no positive feature in the top-20 for tokens like "nutrition," "dietitian," "diet," "recipes," or "eat healthier." The only profession-adjacent positive features are generic person/name detectors (L4:7864, L4:15317, L5:16213) which also fire primarily on "She"/"loves"/"Sarah" rather than on profession words. **L7:8644** ("woman's name in a variety of contexts"), which fires on "Sarah", is **negative (direct_effect −0.27)** — partially cancelling the positive gender signal. There is no feature in the top-20 whose semantic content is "registered dietitian," "nutrition professional," or even "healthcare provider."

The picture is unambiguous: the probe's positive score is built from a stack of features whose top-activating examples and promoted tokens all concern female gender (She/her/herself, female first names, women's soccer, girls). The signal originates at the **"She" and "loves" token embeddings** and propagates through L4 → L6 → L12 → L18. Genuine profession indicators (the L1 "client" feature is even negative; the nutrition/dietitian vocabulary activates nothing in the top-20). This is exactly the spurious-correlation pattern the user suspected: the model has learned to classify the dietitian profession via feminine-gender markers rather than via nutrition-domain vocabulary, and the attribution graph confirms this circuit-by-circuit.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 1 | Probe output (RD/dietitian classification direction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Late-layer 'women/girls mentioned' features (PRIMARY DRIVERS) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 12 | Late-layer 'women/girls mentioned' features (PRIMARY DRIVERS) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 34 | Late-layer 'women/girls mentioned' features (PRIMARY DRIVERS) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | L12 'female pronouns and possessive pronouns' | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | L6 'references to women, pronouns and titles' (LARGEST single direct_effect +0.375) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | L6 'references to women, pronouns and titles' (LARGEST single direct_effect +0.375) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L14:F12501](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) | 2 | L14 'uses of the feminine pronoun' |  uses of the feminine pronoun. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 12 | L7 'woman's name in a variety of contexts' (NEGATIVE: -0.27) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 34 | L7 'woman's name in a variety of contexts' (NEGATIVE: -0.27) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 2 | L7 'mentions of people/characters, roles, family details' (POSITIVE) |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 5 | L7 'mentions of people/characters, roles, family details' (POSITIVE) |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 11 | L7 'mentions of people/characters, roles, family details' (POSITIVE) |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 12 | L7 'mentions of people/characters, roles, family details' (POSITIVE) |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L0:F7509](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7509) | 4 | L0 'female pronouns and words like daughter/husband' (NEGATIVE: -0.174) |  female pronouns and words like daughter and husband that refer to women | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7509) |
| [L1:F15251](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15251) | 5 | L1 'the word client' (NEGATIVE: -0.170) |  the word "client" and its plural form more often than not when capitalized as the first word of a sentence or preceded by a special character | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15251) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 1 | L6 'female first names and possessive forms' (NEGATIVE: -0.18) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 2 | L6 'female first names and possessive forms' (NEGATIVE: -0.18) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | L4 'xml/source code... but activates on She' (POSITIVE: +0.229) | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | L4 'named entities like characters or people' (POSITIVE: +0.189) |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L5:F16213](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16213) | 2 | L5 'proper nouns first+last name' (POSITIVE: +0.168) |  proper nouns consisting of a first and last name | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16213) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: She (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: loves (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: her (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: Sarah (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 34 | Emb: Sarah (pos 34) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: clients (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.375 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@1` | ❌ error | — | — | Trace this feature upstream. This appears to be a strong positive driver of the … |
| SA-2 | `L6:F11646@1` | ❌ error | — | — | Trace this feature upstream. It's a strong positive driver of the probe. Determi… |
| SA-3 | `L12:F12940@2` | ❌ error | — | — | Trace this feature upstream. It's a positive driver of the probe at pos 2 (likel… |
| SA-4 | `L4:F7864@1` | ❌ error | — | — | Trace this early-layer feature upstream. It's a positive driver of the probe at … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×4 | L18:14677, L6:11646, L12:12940, L4:7864 |
| 2 | `get_upstream_features` | L18:F14677@1, k=10 → Emb:"She"@1 (de=27.12) +9 more |
| 3 | `get_upstream_features` | L6:F11646@1, k=10 → Emb:"She"@1 (de=19.25) +9 more |
| 4 | `get_upstream_features` | L12:F12940@2, k=10 → Emb:"She"@1 (de=5.31) +9 more |
| 5 | `inspect_feature` ×5 | L7:2765, L4:15317, L5:16213, L14:12501, L12:14970 |
| 6 | `get_upstream_features` | L12:F12940@12, k=5 → ❌ Feature (layer=12, feature_idx=12940) not found at pos=12. T |
| 7 | `get_upstream_features` | L7:F2765@2, k=10 → Emb:"She"@1 (de=4.16) +9 more |
| 8 | `get_upstream_features` | L7:F2765@5, k=10 → Emb:"She"@1 (de=3.19) +9 more |
| 9 | `get_upstream_features` | L7:F2765@11, k=10 → Emb:"She"@1 (de=3.61) +9 more |
| 10 | `get_upstream_features` | L7:F2765@12, k=10 → Emb:"She"@1 (de=3.50) +9 more |
| 11 | `inspect_feature` ×8 | L0:7509, L1:15251, L6:16329, L7:8644, L11:9183, L15:851, L9:8770, L10:12232 |
| 12 | `get_upstream_features` | L18:F14677@34, k=5 → Emb:" Sarah"@34 (de=5.69) +4 more |
| 13 | `get_upstream_features` | L4:F7864@1, k=5 → Emb:"She"@1 (de=24.62) +4 more |
| 14 | `get_upstream_features` | L18:F14677@12, k=5 → Emb:" Sarah"@12 (de=7.00) +4 more |

### Build

`build_circuit` → 19 nodes, 26 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 47,000 | 6,191 | 153,042 | 0 | $0.0307 | — | — |
| **Total** | | **47,000** | **6,191** | **153,042** | **0** | **$0.0307** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 14s