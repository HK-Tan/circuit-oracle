# Circuit Oracle Report
**Date:** 2026-07-28 07:23:17 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score for "nurse" is driven by a mix of two distinct signals: (1) a legitimate profession-signal pathway tracing from the "Nursing" token at pos 10 through nursing-specific features, and (2) a much stronger gender-marker pathway tracing from the "She" pronoun at pos 1 (and 19) through multiple "references to women" features that peak in the late layers and feed directly into the output.

**Confidence:** 8

**Reasoning:**

The circuit reveals two parallel pathways converging on the probe output:

**Genuine profession pathway (weaker):** Token "Nursing" at pos 10 → L4:11037 (counseling/therapy/social-work/degree program words, activation 14.4) → L5:10392 (fields of academic study, fires on "achelors"/"Nursing"/"Science" tokens) → L6:15267 (words referring to the profession of nursing, direct_effect 0.47 to output). L4:3727 (academic degree words) also contributes from "Science"/"Bachelors". This pathway is genuine but relatively modest in its direct contribution.

**Gender-marker pathway (dominant):** Token "She" at pos 1 (direct_effect 19.25 to L6:11646; 27.1 to L18:14677) drives a chain of gender-detection features. L4:7864 and L4:15317 activate on "She" and "graduated" (with promoted tokens "herself"/"she"/"her"), then L6:11646 (references to women via pronouns/titles, direct_effect 0.50 to output, fires at pos 1, 2, 19, 50) consolidates the signal. By L12:12940 (female pronouns), L18:14677 (instances of women or girls being mentioned, direct_effect 0.38 at pos 19, 0.29 at pos 1, fires with massive activation ~25-31), and L19:9685 (references to women's names and roles/accomplishments, direct_effect 0.26), the signal is purely about detecting a woman. L0:15382 (mentions of a female person) and L7:8644 (woman's name in a variety of contexts) reinforce this from multiple positions.

**The user's concern is validated.** The single largest direct contributor to the probe output is L6:11646 (0.50), which encodes "references to women, potentially triggered by pronouns and titles" — it has nothing to do with nursing specifically. The L18:14677 feature, contributing 0.38, is labeled "instances of women or girls being mentioned" — again, purely gender. The genuine profession feature L6:15267 (0.47) is comparable in direct effect, but the gender signal flows into MULTIPLE late-layer nodes (L6, L12, L18, L19) while the profession signal only feeds L6 and L19 weakly. The probe's classification is partially confounded: it classifies this text as nurse using both "the person is a nurse" and "the person is a woman," the latter being a spurious shortcut. If the subject pronoun were "He," the L6:11646, L18:14677, and L19:9685 chain would largely collapse (these features explicitly suppress "himself/his" tokens), even though the nursing content would remain unchanged.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 19 | L0: mentions of a female person (15382) | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 50 | L0: mentions of a female person (15382) | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F16075](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16075) | 15 | L0: word 'of' and court names (16075) | the word "of" and court names | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16075) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | L4: named entities / characters / people (15317) |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 1 | L4: named entities / characters / people (15317) |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | L4: female pronouns (7864, fires on 'She' pos 1) | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 19 | L4: female pronouns (7864, fires on 'She' pos 1) | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 6 | L4: academic degree words (3727) |  mentions of academic degrees | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 8 | L4: academic degree words (3727) |  mentions of academic degrees | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 9 | L4: academic degree words (3727) |  mentions of academic degrees | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 10 | L4: counseling/therapy/social-work/degree program words (11037) |  words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 22 | L4: counseling/therapy/social-work/degree program words (11037) |  words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 10 | L5: fields of academic study (10392) |  fields of academic study | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 132 | L5: fields of academic study (10392) |  fields of academic study | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | L6: references to women via pronouns/titles (11646) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | L6: references to women via pronouns/titles (11646) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 19 | L6: references to women via pronouns/titles (11646) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 50 | L6: references to women via pronouns/titles (11646) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 10 | L6: words referring to the profession of nursing (15267) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 22 | L6: words referring to the profession of nursing (15267) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 132 | L6: words referring to the profession of nursing (15267) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F8166](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) | 81 | L6: proper names ending in a/i/e (8166) |  proper names longer than 4 characters and ending in 'a', 'i', or 'e' | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 10 | L7: woman's name in a variety of contexts (8644) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 19 | L7: woman's name in a variety of contexts (8644) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 50 | L7: woman's name in a variety of contexts (8644) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 140 | L7: woman's name in a variety of contexts (8644) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | L12: female pronouns and possessive pronouns (12940) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | L18: instances of women or girls being mentioned (14677) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 19 | L18: instances of women or girls being mentioned (14677) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 21 | L18: instances of women or girls being mentioned (14677) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 50 | L18: instances of women or girls being mentioned (14677) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F3679](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/3679) | 140 | L18: personal pronouns and/or proper nouns (3679) |  personal pronouns and/or proper nouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/3679) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 19 | L19: references to women's names and roles/accomplishments (9685) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 140 | L19: references to women's names and roles/accomplishments (9685) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11646 de=0.498 |
| 3 | `inspect_feature` ×5 | L6:11646, L6:15267, L18:14677, L4:15317, L4:7864 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@1` | ❌ error | — | — | Trace the path from L6:F11646 (references to women, triggered by pronouns/titles… |
| SA-2 | `L6:F15267@10` | ❌ error | — | — | Trace the path from L6:F15267 (nursing profession terms). What input tokens driv… |
| SA-3 | `L18:F14677@1` | ❌ error | — | — | Trace the path from L18:F14677 (instances of women/girls being mentioned). What … |
| SA-4 | `L4:F15317@2` | ❌ error | — | — | Trace the path from L4:F15317 (named entities / characters / people). What token… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F11646@1, k=10 → Emb:"She"@1 (de=19.25) +9 more |
| 2 | `get_upstream_features` | L6:F15267@10, k=10 → Emb:" Nursing"@10 (de=17.38) +9 more |
| 3 | `get_upstream_features` | L18:F14677@1, k=10 → Emb:"She"@1 (de=27.12) +9 more |
| 4 | `get_upstream_features` | L4:F15317@2, k=10 → Emb:"She"@1 (de=10.94) +9 more |
| 5 | `get_upstream_features` | L19:F9685@140, k=10 → L4:F1276 (de=1.45) +9 more |
| 6 | `get_upstream_features` | L6:F8166@81, k=10 → L5:F6637 (de=-6.31) +9 more |
| 7 | `get_upstream_features` | L0:F16075@15, k=10 → Emb:" Of"@15 (de=26.50) +9 more |
| 8 | `get_upstream_features` | L12:F12940@2, k=10 → Emb:" graduated"@2 (de=4.81) +9 more |
| 9 | `inspect_feature` ×4 | L19:9685, L6:8166, L0:16075, L12:12940 |
| 10 | `get_upstream_features` | L18:F14677@19, k=10 → Emb:" She"@19 (de=15.31) +9 more |
| 11 | `get_upstream_features` | L19:F9685@140, k=10 → L4:F1276 (de=1.45) +9 more |
| 12 | `get_upstream_features` | L4:F7864@1, k=10 → Emb:"She"@1 (de=24.62) +9 more |
| 13 | `get_upstream_features` | L4:F11037@10, k=10 → Emb:" Nursing"@10 (de=10.62) +9 more |
| 14 | `get_upstream_features` | L5:F10392@10, k=10 → Emb:"achelors"@6 (de=3.56) +9 more |
| 15 | `get_upstream_features` | L15:F851@1, k=10 → L12:F12493 (de=22.38) +9 more |
| 16 | `inspect_feature` ×4 | L4:11037, L5:10392, L15:851, L4:3727 |
| 17 | `get_upstream_features` | L18:F3679@140, k=10 → Emb:"<bos>"@0 (de=-2.89) +9 more |
| 18 | `get_upstream_features` | L6:F11646@19, k=10 → Emb:" She"@19 (de=19.00) +9 more |
| 19 | `get_upstream_features` | L18:F14677@50, k=10 → Emb:" She"@50 (de=15.69) +9 more |
| 20 | `inspect_feature` ×4 | L18:3679, L15:4094, L7:8644, L0:15382 |
| 21 | `get_upstream_features` | L6:F11646@2, k=10 → L4:F15317 (de=5.94) +9 more |
| 22 | `get_upstream_features` | L19:F9685@1, k=10 → ❌ Feature (layer=19, feature_idx=9685) not found at pos=1. Thi |
| 23 | `get_upstream_features` | L19:F9685@19, k=10 → Emb:" She"@19 (de=6.19) +9 more |
| 24 | `get_upstream_features` | L18:F14677@21, k=10 → Emb:" her"@21 (de=22.12) +9 more |
| 25 | `inspect_feature` ×3 | L17:5889, L4:1276, L4:1302 |
| 26 | `get_upstream_features` | L6:F15267@19, k=10 → ❌ Feature (layer=6, feature_idx=15267) not found at pos=19. Th |
| 27 | `get_upstream_features` | L6:F15267@21, k=10 → ❌ Feature (layer=6, feature_idx=15267) not found at pos=21. Th |
| 28 | `get_upstream_features` | L6:F15267@22, k=10 → Emb:" nursing"@22 (de=21.00) +9 more |
| 29 | `get_upstream_features` | L6:F15267@132, k=10 → Emb:" Nursing"@132 (de=17.38) +9 more |

### Build

`build_circuit` → 20 nodes, 34 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 45,077 | 7,133 | 465,764 | 0 | $0.0500 | — | — |
| **Total** | | **45,077** | **7,133** | **465,764** | **0** | **$0.0500** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 36s