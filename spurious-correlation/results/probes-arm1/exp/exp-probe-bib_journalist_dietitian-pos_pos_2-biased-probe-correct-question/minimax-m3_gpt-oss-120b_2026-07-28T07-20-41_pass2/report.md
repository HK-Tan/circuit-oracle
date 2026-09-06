# Circuit Oracle Report
**Date:** 2026-07-28 07:20:41 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of "nutritionist/dietitian" is driven primarily by feminine-pronoun/name features that originate from the literal token "She" rather than by the genuine profession vocabulary; only one food/nutrition feature (L6:F11327) and one diet/health feature (L4:F13412) — both fed by the single token "nutrition" — represent any true profession signal, and they are dwarfed by the female-gender circuit.

**Confidence:** 8

**Reasoning:** The circuit is built around two parallel paths feeding the probe output. **Path A (female-gender / spurious, dominant):** The token embedding "She" at pos 1 (direct_effect = 27.1 → L18:F14677) and again at pos 23 (direct_effect = 5.7 → L19:F9685) lights up a stack of female-person detectors — L2:F7672 ("mentions of women by name and relationship", frac_nonzero 0.022), L4:F7864 (promoted tokens = herself, she's), L4:F15317 (named-entity feature with female-promoted tokens), L6:F11646 ("references to women, pronouns and titles"), L6:F16329 (female first names/possessives), L7:F8644 (woman's name), L10:F14965 (terms relating to women), L12:F12940 (female pronouns, frac_nonzero 0.0065), L14:F12501 (feminine pronoun), L18:F14677 (women/girls mentioned, frac_nonzero 0.012), L18:F14743 ("He" — pushed *negatively* at −0.11, suppressing male-pronoun signal), and L19:F9685 (women's names and roles). These features carry the largest direct_effects in the top-20 list (0.36, 0.29, 0.24, 0.20, 0.16, 0.15). **Path B (genuine profession, minor):** The token embedding "nutrition" at pos 13 (direct_effect = 27.1 at L0, 14.1 at L4) drives a tightly localised food/nutrition circuit — L0:F5201 ("the word nutrition"), L3:F6246 ("Nutrients/ure"), L4:F9554 (food/rations), L4:F13412 (diets/dietary health), L6:F11327 (food/nutrition). These contribute direct_effects of only 0.13–0.23. **Convergence:** Both paths feed the same probe direction. The female-gender path is the larger contributor (more features, larger direct_effects, and the "She" embedding has the strongest single direct_effect at 27.1). The profession path terminates at a single nutrition-token site. This pattern strongly supports the user's concern: the probe is leveraging the gendered referent "She" plus a few nutrition tokens as proxies, rather than a rich, multi-token semantic representation of the dietitian profession. If the same nutritional content were written with "He", the gender path would flip sign (L18:F14743, L6:F16329 promote male tokens) and the probe score would change substantially, indicating a genuine spurious-correlation failure mode.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: She (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 23 | Emb: She (pos 23) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: nutrition (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: has (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L2:F7672](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) | 1 | Early female-person / pronoun entity (L2:7672, L4:15317, L4:7864) |  mentions of women by name and relationship | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 1 | Early female-person / pronoun entity (L2:7672, L4:15317, L4:7864) |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Early female-person / pronoun entity (L2:7672, L4:15317, L4:7864) |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Early female-person / pronoun entity (L2:7672, L4:15317, L4:7864) | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L0:F5201](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5201) | 13 | Early nutrition/diet token detectors (L0:5201, L3:6246, L4:13412, L4:9554) | unspecified generic detector | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5201) |
| [L3:F6246](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6246) | 13 | Early nutrition/diet token detectors (L0:5201, L3:6246, L4:13412, L4:9554) | the word "Nutrients" and words containing "ure". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6246) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 13 | Early nutrition/diet token detectors (L0:5201, L3:6246, L4:13412, L4:9554) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 13 | Early nutrition/diet token detectors (L0:5201, L3:6246, L4:13412, L4:9554) | words related to food, rations and feeding | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Mid-layer female-pronoun/name detectors (L6:11646, L6:16329, L6:11327(food), L7:8644, L10:14965) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Mid-layer female-pronoun/name detectors (L6:11646, L6:16329, L6:11327(food), L7:8644, L10:14965) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 23 | Mid-layer female-pronoun/name detectors (L6:11646, L6:16329, L6:11327(food), L7:8644, L10:14965) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 1 | Mid-layer female-pronoun/name detectors (L6:11646, L6:16329, L6:11327(food), L7:8644, L10:14965) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 23 | Mid-layer female-pronoun/name detectors (L6:11646, L6:16329, L6:11327(food), L7:8644, L10:14965) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 13 | Mid-layer female-pronoun/name detectors (L6:11646, L6:16329, L6:11327(food), L7:8644, L10:14965) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 23 | Mid-layer female-pronoun/name detectors (L6:11646, L6:16329, L6:11327(food), L7:8644, L10:14965) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L10:F14965](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) | 2 | Mid-layer female-pronoun/name detectors (L6:11646, L6:16329, L6:11327(food), L7:8644, L10:14965) |  terms relating to women | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Late-layer female-person aggregators (L12:12940, L14:12501, L18:14677, L19:9685, L18:14743) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 3 | Late-layer female-person aggregators (L12:12940, L14:12501, L18:14677, L19:9685, L18:14743) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L14:F12501](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) | 2 | Late-layer female-person aggregators (L12:12940, L14:12501, L18:14677, L19:9685, L18:14743) |  uses of the feminine pronoun. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Late-layer female-person aggregators (L12:12940, L14:12501, L18:14677, L19:9685, L18:14743) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 2 | Late-layer female-person aggregators (L12:12940, L14:12501, L18:14677, L19:9685, L18:14743) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 23 | Late-layer female-person aggregators (L12:12940, L14:12501, L18:14677, L19:9685, L18:14743) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 23 | Late-layer female-person aggregators (L12:12940, L14:12501, L18:14677, L19:9685, L18:14743) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 23 | Late-layer female-person aggregators (L12:12940, L14:12501, L18:14677, L19:9685, L18:14743) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe output (profession classifier) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.357 |
| 3 | `inspect_feature` ×14 | L6:11646, L12:12940, L18:14677, L4:15317, L4:7864, L2:7672, L6:16329, L10:14965, L6:11327, L14:12501, L19:9685, L4:13412, L7:8644, L18:14743 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@23` | ❌ error | — | — | Trace upstream from L18:F14677 (instances of women or girls being mentioned). Wh… |
| SA-2 | `L6:F11327@13` | ✅ reported | 8 | 12 | Trace upstream from L6:F11327 (food/nutrition words). This is one of the few pro… |
| SA-3 | `L12:F12940@2` | ✅ reported | 8 | 10 | Trace upstream from L12:F12940 (female pronouns/possessives) at pos 2 (the "She"… |
| SA-4 | `L4:F13412@13` | ✅ reported | 3 | 4 | Trace upstream from L4:F13412 (diets/dietary health). Follow it to the embedding… |

<details>
<summary><b>SA-2</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 2 | `get_upstream_features` | L6:F11327@13, k=10 | Emb:" nutrition"@13 (de=21.00) +9 more |
| 3 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 4 | `inspect_feature` | L4, F9554 | " words related to food, rations and feeding" |
| 5 | `inspect_feature` | L1, F6895 | " the word "visit" and related forms" |
| 6 | `get_upstream_features` | L4:F13412@13, k=10 | Emb:" nutrition"@13 (de=14.06) +9 more |
| 7 | `inspect_feature` | L3, F6246 | " the word "Nutrients" and words containing "ure"." |
| 8 | `get_upstream_features` | L4:F9554@13, k=10 | Emb:" nutrition"@13 (de=15.88) +9 more |
| 9 | `get_upstream_features` | L3:F6246@13, k=10 | Emb:" nutrition"@13 (de=12.25) +9 more |

**Findings:** The food/nutrition feature (L6:11327) is principally driven by the raw token embedding for the word "nutrition" at the same position, delivering a large positive direct effect (21.0). Mid‑layer diet‑related features (L4:13412 and L4:9554) also receive strong excitatory input from the same token embedding, and they in turn feed forward to L6. The nutrient‑suffix detector (L3:6246) sits between the …

</details>

<details>
<summary><b>SA-3</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 2 | `get_upstream_features` | L12:F12940@2, k=10 | Emb:"She"@1 (de=6.03) +9 more |
| 3 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 4 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 5 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 6 | `inspect_feature` | L0, F14824 | "the word "has"" |
| 7 | `get_upstream_features` | L4:F15317@2, k=10 | Emb:"She"@1 (de=13.56) +9 more |
| 8 | `inspect_feature` | L2, F7672 | " mentions of women by name and relationship" |
| 9 | `inspect_feature` | L8, F7245 | " content in languages other than English, particularly French and poss" |
| 10 | `inspect_feature` | L7, F2765 | " mentions of people or characters, and their performance, roles, injur" |
| 11 | `get_upstream_features` | L6:F11646@2, k=10 | L4:F15317 (de=8.75) +9 more |

**Findings:** The target L12:F12940 is a female pronoun detector. Its strongest upstream driver is the raw token embedding for the word "She" (pos 1), providing a large positive direct effect, confirming that the feature is indeed responding to the pronoun itself rather than to any later profession token. Additional upstream contributors include a mid‑level entity feature (L4:F15317) that aggregates person‑enti…

</details>

<details>
<summary><b>SA-4</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 2 | `get_upstream_features` | L4:F13412@13, k=10 | Emb:" nutrition"@13 (de=14.06) +9 more |
| 3 | `inspect_feature` | L3, F6246 | " the word "Nutrients" and words containing "ure"." |
| 4 | `get_upstream_features` | L3:F6246@13, k=10 | Emb:" nutrition"@13 (de=12.25) +9 more |
| 5 | `inspect_feature` | L0, F5201 | " the word "nutrition"" |
| 6 | `get_upstream_features` | L0:F5201@13, k=10 | Emb:" nutrition"@13 (de=27.12) +9 more |

**Findings:** Tracing from the diet‑related feature L4:F13412 (position 13) quickly leads to the upstream token embedding " nutrition". The strongest positive upstream influence comes from the raw input embedding for the token "nutrition" (direct_effect ~14 at L4, ~12 at L3, ~27 at L0). Two intermediate features further specialize this signal: L3:F6246 captures nutritional morphemes ("Nutrients", "ure"), and L0…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L19:F9685@23, k=10 → Emb:" She"@23 (de=5.72) +9 more |
| 2 | `get_upstream_features` | L18:F14677@1, k=10 → Emb:"She"@1 (de=27.12) +9 more |
| 3 | `get_upstream_features` | L2:F7672@1, k=10 → Emb:"She"@1 (de=13.88) +9 more |
| 4 | `get_upstream_features` | L7:F8644@23, k=10 → Emb:"She"@1 (de=8.44) +9 more |
| 5 | `get_upstream_features` | L6:F11646@1, k=10 → Emb:"She"@1 (de=19.25) +9 more |
| 6 | `get_upstream_features` | L4:F15317@2, k=10 → Emb:"She"@1 (de=13.56) +9 more |
| 7 | `get_upstream_features` | L4:F7864@1, k=10 → Emb:"She"@1 (de=24.62) +9 more |
| 8 | `get_upstream_features` | L6:F11646@23, k=10 → Emb:" She"@23 (de=18.75) +9 more |

### Build

`build_circuit` → 9 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 73,722 | 4,456 | 122,563 | 0 | $0.0348 | — | — |
| SA-4 | openai/gpt-oss-120b | 50,344 | 3,603 | 2,544 | 0 | $0.0098 | ✅ 3F/4E | Trace upstream from L4:F13412 (diets/dietary health). Follow… |
| SA-2 | openai/gpt-oss-120b | 100,918 | 6,117 | 2,624 | 0 | $0.0188 | ✅ 8F/12E | Trace upstream from L6:F11327 (food/nutrition words). This i… |
| SA-3 | openai/gpt-oss-120b | 148,702 | 6,379 | 5,152 | 0 | $0.0262 | ✅ 8F/10E | Trace upstream from L12:F12940 (female pronouns/possessives)… |
| **Total** | | **373,686** | **20,555** | **132,883** | **0** | **$0.0896** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 29s