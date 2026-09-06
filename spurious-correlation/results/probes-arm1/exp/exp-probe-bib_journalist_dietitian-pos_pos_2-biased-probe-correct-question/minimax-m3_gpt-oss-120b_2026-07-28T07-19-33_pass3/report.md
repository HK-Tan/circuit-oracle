# Circuit Oracle Report
**Date:** 2026-07-28 07:19:33 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by a cascade of female-pronoun/gender features anchored to the "She" token embedding, with minimal contribution from genuine profession or content indicators.

**Confidence:** 9

**Reasoning:**

The circuit is overwhelmingly a **gender-detection circuit**, not a profession-detection circuit. The signal flows from the token embedding of "She" (pos 1) through a tightly interlocking chain of female-pronoun features, reaching the probe output logit.

**Token-embedding sources (the root of the circuit):**
- **Emb: She (pos 1)** — the first word of the text — directly drives L4:F7864 (direct_effect ≈ 24.6) and L5:F10952 (8.56), the earliest features in the path.
- **Emb: has (pos 2)** — feeds L4:F15317 (direct_effect ≈ 3.9), reinforcing the subject-phrase parse.
- **Emb: She (pos 23)** — the second "She" later in the text — directly excites L18:F14677 (direct_effect ≈ 14.3), the most strongly-activating late-layer feature.

**Early-layer features (L0–L4):**
- L1:F2848 — fires on "she/her" pronouns (frac_nonzero 0.003)
- L2:F2128 — cross-lingual pronoun detector, promoted tokens include "she", "he", "her" (frac_nonzero 0.003)
- L2:F7672 — "mentions of women by name and relationship" (promoted tokens don't help but top examples are "wife", "She")
- L4:F7864 — female pronoun detector in practice despite an XML/code autointerp label
- L4:F15317 — "named entities like characters or people" (top examples are female pronouns)

**Mid-layer gender-gating (L5–L12):**
- L6:F11646 — "references to women, potentially triggered by pronouns and titles" (frac_nonzero 0.020). This is the *strongest single feature* driving the probe (direct_effect 0.357 at pos 1, 0.285 at pos 2). Promoted tokens are exclusively feminine pronouns: "herself", "she", "her", "ihrem", "Autorin".
- L6:F16329 — same family but **suppresses** the probe (negative direct_effect -0.173, -0.131), possibly an anti-male / male-context counter-feature.
- L10:F14965 — "terms relating to women" (frac_nonzero 0.019, "female", "woman", "Goddess")
- L12:F12940 — "references to female pronouns and possessive pronouns" (frac_nonzero 0.007, top-3 promoted tokens: "herself", "bint", "herself")

**Late-layer features (L13–L19):**
- L14:F12501 — "uses of the feminine pronoun" (direct_effect 0.148, "feminist", "herself" promoted)
- L15:F3330 — personal stories about women (the "She…action" narrative pattern)
- L17:F5889 — pronoun-based references to individuals with female bias
- **L18:F14677** — "instances of women or girls being mentioned" (activation 34.5, direct_effect 0.242 at pos 23). Top-3 promoted tokens: "herself", "she", "her"
- L19:F9685 — "references to women's names and their roles or accomplishments" (activation 21.75, direct_effect 0.146). Promoted tokens: "herself", "she", "her". Top examples are precisely about named women in roles: "Kathryn Vercil…", "Daphne", "Dr. Debbie Gregory", "Andrea runs the whole operation"
- L18:F14743 — **suppresses** the probe (-0.109), label "He" — a male-pronoun suppressor.

**The user's concern is confirmed.** Of the ~20 top features driving the probe, virtually every positively-contributing one is a **female-pronoun or female-entity detector**:
- Every positive feature (L6:F11646, L12:F12940, L18:F14677, L19:F9685, L14:F12501, L10:F14965, L4:F15317) has promoted tokens that are exclusively feminine ("herself", "she", "her", "ihrem") and top-activating examples dominated by female pronouns/names.
- Two of the top features are **negative** male-pronoun suppressors (L6:F16329, L18:F14743), pushing away the "he/him" direction.
- The actual **content/topic features** for nutrition and food exist (L6:F11327 "words or phrases related to food or nutrition", L4:F13412 "terms related to diets and dietary health") but they have relatively modest direct effects (0.152 and 0.127) and appear in the mid-layers without forming a strong chain to the output.

The probe is largely classifying the text as a particular profession by detecting "this text talks about a named woman" rather than "this text is about nutrition/cooking/health". If the same text began with "He has a passion for…", the probe's score would likely drop substantially, confirming the spurious-correlation diagnosis. The circuit shows **gender is the dominant signal; profession-relevant content is a minor secondary contributor.**

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe classification logit | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 23 | Late-layer female-detection features (L18–L19) | instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Late-layer female-detection features (L18–L19) | instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 23 | Late-layer female-detection features (L18–L19) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 23 | Late-layer female-detection features (L18–L19) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 23 | Late-layer female-detection features (L18–L19) | references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 23 | Late-layer female-detection features (L18–L19) | personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L14:F12501](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) | 2 | Late-layer female-detection features (L18–L19) |  uses of the feminine pronoun. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) |
| [L13:F6622](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) | 23 | Late-layer female-detection features (L18–L19) | pronouns. | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Mid-layer female pronoun/gender gating (L6–L12) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 3 | Mid-layer female pronoun/gender gating (L6–L12) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Mid-layer female pronoun/gender gating (L6–L12) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Mid-layer female pronoun/gender gating (L6–L12) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 23 | Mid-layer female pronoun/gender gating (L6–L12) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 1 | Mid-layer female pronoun/gender gating (L6–L12) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 23 | Mid-layer female pronoun/gender gating (L6–L12) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 23 | Mid-layer female pronoun/gender gating (L6–L12) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L10:F14965](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) | 2 | Mid-layer female pronoun/gender gating (L6–L12) |  terms relating to women | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) |
| [L8:F7245](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7245) | 2 | Mid-layer female pronoun/gender gating (L6–L12) | content in languages other than English, particularly French and possibly Sanskrit. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7245) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 2 | Mid-layer female pronoun/gender gating (L6–L12) | mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L5:F10952](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) | 1 | Mid-layer female pronoun/gender gating (L6–L12) | third person pronouns in varying contexts | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) |
| [L5:F645](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/645) | 2 | Mid-layer female pronoun/gender gating (L6–L12) | verbs in past tense | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/645) |
| [L2:F7672](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) | 1 | Mid-layer female pronoun/gender gating (L6–L12) |  mentions of women by name and relationship | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 13 | Content/topic features (nutrition, food, diet) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 13 | Content/topic features (nutrition, food, diet) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Early entity/pronoun features (L0–L4) | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Early entity/pronoun features (L0–L4) |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L2:F2128](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2128) | 1 | Early entity/pronoun features (L0–L4) |  pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, *ele*, and *ela* across multiple languages. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2128) |
| [L1:F2848](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2848) | 1 | Early entity/pronoun features (L0–L4) | the pronouns "she" and "her" (and sometimes "his") | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2848) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 23 | Early entity/pronoun features (L0–L4) | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: She (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: has (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 23 | Emb: She (pos 23) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: nutrition (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.357 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@1` | ✅ reported | 4 | 6 | Trace the path upstream from L6:F11646 at position 1. This is the strongest feat… |
| SA-2 | `L18:F14677@23` | ✅ reported | 6 | 8 | Trace the path upstream from L18:F14677 at position 23. This feature has very hi… |
| SA-3 | `L12:F12940@2` | ✅ reported | 7 | 11 | Trace the path upstream from L12:F12940 at position 2. Determine what this featu… |
| SA-4 | `L4:F7864@1` | ✅ reported | 5 | 5 | Trace the path upstream from L4:F7864 at position 1. Determine what this feature… |

<details>
<summary><b>SA-1</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@1, k=10 | Emb:"She"@1 (de=19.25) +9 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 5 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 6 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |
| 7 | `get_upstream_features` | L5:F10952@1, k=10 | Emb:"She"@1 (de=8.56) +9 more |

**Findings:** The target feature L6:F11646 is a female‑pronoun detector. Its strongest upstream driver is the raw input embedding for the token "She", which directly excites L6:F11646 (19.25). Additional upstream features in lower layers (L4:F7864, L5:F10952, L2:F2128) also detect pronouns and pass excitatory influence upward, ultimately converging on the same female‑pronoun signal. All upstream paths reach the…

</details>

<details>
<summary><b>SA-2</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@23, k=10 | Emb:" She"@23 (de=14.31) +9 more |
| 3 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 4 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 5 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 6 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 7 | `get_upstream_features` | L17:F5889@23, k=10 | Emb:" She"@23 (de=19.12) +9 more |
| 8 | `inspect_feature` | L13, F6622 | " pronouns." |
| 9 | `get_upstream_features` | L6:F11646@23, k=10 | Emb:" She"@23 (de=18.75) +9 more |

**Findings:** The traced circuit shows that L18:F14677 is a high‑level detector for mentions of women/girls, driven primarily by the raw token "She" and a cascade of pronoun‑related features across layers 0→6→13→15→17→18. The path reaches the lower‑third of the model (layer 0 and layer 6) and includes a direct embedding influence, satisfying the required termination conditions. The strongest upstream drivers ar…

</details>

<details>
<summary><b>SA-3</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 2 | `get_upstream_features` | L12:F12940@2, k=10 | Emb:"She"@1 (de=6.03) +9 more |
| 3 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 4 | `get_upstream_features` | L4:F15317@2, k=10 | Emb:"She"@1 (de=13.56) +9 more |
| 5 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 6 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 7 | `get_upstream_features` | L6:F11646@2, k=10 | L4:F15317 (de=8.75) +9 more |
| 8 | `inspect_feature` | L8, F7245 | " content in languages other than English, particularly French and poss" |
| 9 | `inspect_feature` | L7, F2765 | " mentions of people or characters, and their performance, roles, injur" |
| 10 | `get_upstream_features` | L10:F14965@2, k=10 | L4:F15317 (de=5.56) +9 more |
| 11 | `inspect_feature` | L5, F645 | " verbs in past tense" |

**Findings:** The target feature L12:F12940 is a gender‑pronoun detector (female pronouns and possessives). Its strongest upstream drivers are a low‑layer named‑entity detector (L4:F15317) that fires on the token "She", a mid‑layer women‑term detector (L10:F14965), and a layer‑6 pronoun‑title detector (L6:F11646). These cascade from the raw embedding of the token "She" (pos 1) and, to a lesser extent, the embed…

</details>

<details>
<summary><b>SA-4</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 2 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 3 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |
| 4 | `get_upstream_features` | L2:F2128@1, k=10 | Emb:"She"@1 (de=20.25) +9 more |
| 5 | `inspect_feature` | L1, F2848 | " the pronouns "she" and "her" (and sometimes "his")" |
| 6 | `get_upstream_features` | L1:F2848@1, k=10 | Emb:"She"@1 (de=6.78) +9 more |

**Findings:** Tracing upstream from L4:F7864 (a layer‑4 feature labelled as detecting XML/code snippets) reveals that its strongest driver is the input token embedding for "She" (direct_effect ≈ 24.6). The signal passes through a low‑frequency pronoun detector in layer 2 (F2128) and a more specific feminine‑pronoun detector in layer 1 (F2848) before reaching the target feature. No further upstream features with…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×9 | L19:9685, L18:14743, L10:14965, L4:15317, L6:11327, L14:12501, L2:7672, L4:13412, L6:11646 |

### Build

`build_circuit` → 9 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 25,284 | 6,374 | 122,075 | 0 | $0.0226 | — | — |
| SA-1 | openai/gpt-oss-120b | 64,716 | 4,088 | 5,056 | 0 | $0.0122 | ✅ 4F/6E | Trace the path upstream from L6:F11646 at position 1. This i… |
| SA-4 | openai/gpt-oss-120b | 65,116 | 5,593 | 2,688 | 0 | $0.0132 | ✅ 5F/5E | Trace the path upstream from L4:F7864 at position 1. Determi… |
| SA-2 | openai/gpt-oss-120b | 105,372 | 5,472 | 5,120 | 0 | $0.0192 | ✅ 6F/8E | Trace the path upstream from L18:F14677 at position 23. This… |
| SA-3 | openai/gpt-oss-120b | 110,093 | 7,452 | 29,344 | 0 | $0.0214 | ✅ 7F/11E | Trace the path upstream from L12:F12940 at position 2. Deter… |
| **Total** | | **370,581** | **28,979** | **164,283** | **0** | **$0.0885** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 25s