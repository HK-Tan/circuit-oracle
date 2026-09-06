# Circuit Oracle Report
**Date:** 2026-07-28 07:21:37 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

Now I have enough to confirm the circuit and finalize. The key findings: the strongest late-layer features feeding the probe are all female-pronoun / women-mention features (L18:F14677 "instances of women" and L19:F9685 "women's names with roles"), not the nursing profession feature. The genuine nursing feature (L6:F15267) exists but contributes less than the gender features.

**Analysis:** The probe's classification of "nurse" is driven primarily by a cascade of female-gender features — L6:F11646 ("references to women, pronouns/titles"), L12:F12940 ("female pronouns/possessives"), L18:F14677 ("instances of women/girls mentioned"), and L19:F9685 ("women's names with roles") — that are themselves activated by the female pronouns "She" (positions 1, 19, 50) and the female first name "Kayte" (position 140), not by profession tokens. The one genuine profession indicator, L6:F15267 ("nursing profession words" at "Nursing" pos 10, direct_effect=0.47) and L14:F3985 ("medicine/management terms"), is present but is outweighed by the gender features (e.g., L18:F14677 with direct_effect=0.377 at three positions, L19:F9685 with direct_effect=0.26 at two positions, L6:F11646 with direct_effect=0.50 at three positions).

**Confidence:** 8

**Reasoning:** The circuit is decisively female-pronoun-driven. Tracing each top-feature upstream to embedding nodes confirms the signal source:
- L6:F11646 (frac_nonzero=0.020) is directly fed by Emb:She (pos 1, direct_effect=19.25) — i.e., the very first token of the document.
- L18:F14677 (frac_nonzero=0.012) is directly fed by Emb:She at positions 1 (de=4.28), 19 (de=15.31), and 50 (de=15.69) — three different "She" tokens each independently promoting the feature.
- L19:F9685 ("women's names with roles", de=0.26) is directly fed by Emb:Kayte (pos 140) and Emb:She (pos 1) — the name "Kayte" itself is a female-coded proper name (L6:F8166, "names ending in -a/-i/-e") that also drives L6:F16329 ("female first names and possessive forms").

By contrast, the only direct, embedding-grounded profession feature is L6:F15267 from Emb:Nursing (pos 10, de=17.4 into the feature) and L14:F3985 from the same token — both legitimate profession indicators. But these have to compete with the much more numerous gender features that fire at every "She" position throughout the text. The L4:F15317 ("named entities") and L0:F15382 features in the L0 supernode also show promoted tokens like "▁herself", "▁she", "▁her" — meaning even the "entity" and "pronoun" early features are themselves female-pronoun features, not profession features.

The user's concern is correct: the classification circuit uses spurious gender markers (She/her pronouns and the female-coded name "Kayte") as the primary evidence for the "nurse" profession, rather than the profession tokens (Nursing, RN, OB/GYN, Postpartum). The genuine profession feature (L6:F15267) contributes meaningfully but is one of several signals, and the female-gender features collectively dominate the late-layer read-out feeding the probe.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: She (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 19 | Emb: She (pos 19) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: graduated (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: Nursing (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 140 | Emb: Kayte (pos 140) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: Of Science (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 19 | Early-layer female entity / She-pronoun features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 1 | Early-layer female entity / She-pronoun features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F12519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) | 19 | Early-layer female entity / She-pronoun features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) |
| [L0:F16075](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16075) | 15 | Early-layer female entity / She-pronoun features | the word "of" and court names | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16075) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | L4:F7864 — XML/code/multilingual tokens | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | L4:F15317 — named entities / people |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L5:F5996](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5996) | 81 | L5:F5996 — words associated with females/femininity |  words associated with females, femininity or womanhood | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5996) |
| [L5:F5996](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5996) | 2 | L5:F5996 — words associated with females/femininity |  words associated with females, femininity or womanhood | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5996) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | L6:F11646 — references to women (pronouns/titles) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | L6:F11646 — references to women (pronouns/titles) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 19 | L6:F11646 — references to women (pronouns/titles) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 10 | L6:F15267 — nursing profession words (GENUINE) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F8166](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) | 81 | L6:F8166 — proper names ending in -a/-i/-e |  proper names longer than 4 characters and ending in 'a', 'i', or 'e' | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 10 | L6:F170 — academic fields / humanities |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 1 | L6:F16329 — female first names / possessive forms | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 19 | L6:F16329 — female first names / possessive forms | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 10 | L7:F8644 — woman's name contexts |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 19 | L7:F8644 — woman's name contexts |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 2 | L7:F8644 — woman's name contexts |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | L12:F12940 — female pronouns/possessives | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 10 | L14:F3985 — medicine/management/leadership terms | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 19 | L18:F14677 — instances of women/girls mentioned |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | L18:F14677 — instances of women/girls mentioned |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 50 | L18:F14677 — instances of women/girls mentioned |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 140 | L19:F9685 — women's names with roles/accomplishments |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 19 | L19:F9685 — women's names with roles/accomplishments |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.498 |
| 3 | `inspect_feature` ×6 | L6:11646, L6:15267, L18:14677, L4:15317, L4:7864, L12:12940 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F15267@10` | ❌ error | — | — | Trace upstream from the "nursing profession words" feature at L6:F15267 pos 10. … |
| SA-2 | `L18:F14677@19` | ❌ error | — | — | Trace upstream from the "instances of women or girls being mentioned" feature at… |
| SA-3 | `L12:F12940@2` | ❌ error | — | — | Trace upstream from the "female pronouns/possessive pronouns" feature at L12:F12… |
| SA-4 | `L6:F11646@1` | ❌ error | — | — | Trace upstream from the "references to women, triggered by pronouns and titles" … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F15267@10, k=15 → Emb:" Nursing"@10 (de=17.38) +14 more |
| 2 | `get_upstream_features` | L18:F14677@19, k=15 → Emb:" She"@19 (de=15.31) +14 more |
| 3 | `get_upstream_features` | L12:F12940@2, k=15 → Emb:" graduated"@2 (de=4.81) +14 more |
| 4 | `get_upstream_features` | L6:F11646@1, k=15 → Emb:"She"@1 (de=19.25) +14 more |
| 5 | `inspect_feature` ×8 | L19:9685, L0:16075, L6:8166, L6:170, L14:3985, L7:8644, L6:16329, L5:5996 |
| 6 | `get_upstream_features` | L19:F9685@140, k=10 → L4:F1276 (de=1.45) +9 more |
| 7 | `get_upstream_features` | L18:F14677@50, k=10 → Emb:" She"@50 (de=15.69) +9 more |

### Build

`build_circuit` → 21 nodes, 33 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 47,002 | 6,004 | 118,265 | 0 | $0.0284 | — | — |
| **Total** | | **47,002** | **6,004** | **118,265** | **0** | **$0.0284** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 9s