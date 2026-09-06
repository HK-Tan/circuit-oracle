# Circuit Oracle Report
**Date:** 2026-07-28 07:02:29 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven almost entirely by female-pronoun/gender features (notably the repeated "She" at positions 1, 29, 40, 66) rather than by any genuine profession-specific content; the only topical feature (L6:11327 "food/nutrition") is a minor contributor.

**Confidence:** 9

**Reasoning:** The top of the circuit is dominated by a single semantic theme: female-gender references. The strongest direct driver of the probe is L18:F14677 ("instances of women or girls being mentioned," frac_nonzero=0.012) with direct_effect=0.235, firing at pos 29, 40, and 66 (each a sentence-initial "She"). L19:F9685 ("women's names and roles," frac_nonzero=0.014) adds 0.150 at pos 29. Both L18 and L19 features are driven almost entirely by the token embedding of "She" — emb_she_pos29 has direct_effect=5.6 into L19:F9685 and 16.9 into L18:F14743, while emb_she_pos1 (the opening "She") feeds L6:F11646 ("references to women, pronouns and titles," direct_effect=0.34) via a chain L2:F7672 (women-by-name) → L4:F15317 (named entities) → L6:F11646. Lower-layer detectors (L4:F7864, L5:F10952) also activate on "She." The only profession-relevant feature, L6:F11327 ("food/nutrition"), fires at pos 15 ("food") with a modest direct_effect=0.10 and is a generic content keyword rather than a profession indicator. There is a *suppressive* counter-signal: L18:F14743 ("He") at pos 29 pushes the probe *down* (direct_effect=-0.115), and L6:F16329 / L7:F8644 (female first names) also suppress the score, suggesting the probe direction is not the simple "female" axis but a more specific "profession performed by a generic-female-coded subject" axis. The overall mechanism is: the probe lights up because the text repeatedly uses female pronouns ("She…She…She…") while describing a single professional activity; the model has apparently learned to associate this pronoun pattern with a profession label rather than extracting semantic profession content (e.g., dietitian, nutritionist, wellness coach) from the actual vocabulary. This confirms the user's concern: the circuit is using **gender markers as a proxy for profession**, not genuine profession-indicative content.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Women/girls mentioned (L18:14677) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 29 | Women/girls mentioned (L18:14677) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 40 | Women/girls mentioned (L18:14677) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 66 | Women/girls mentioned (L18:14677) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 29 | Women's names + roles (L19:9685) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 29 | Male pronoun 'He' (L18:14743, suppressive) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Female pronouns (L12:12940) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L14:F12501](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) | 3 | Uses of feminine pronoun (L14:12501) |  uses of the feminine pronoun. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 29 | Woman's name in various contexts (L7:8644, suppressive) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 19 | Woman's name in various contexts (L7:8644, suppressive) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 1 | Female first names possessive (L6:16329, suppressive) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 29 | Female first names possessive (L6:16329, suppressive) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | References to women / pronouns (L6:11646) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | References to women / pronouns (L6:11646) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 29 | References to women / pronouns (L6:11646) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Code/pronoun detector (L4:7864) | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Named entities / people (L4:15317) |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 15 | Food/nutrition content (L6:11327) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L2:F7672](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) | 1 | Women by name & relationship (L2:7672) |  mentions of women by name and relationship | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) |
| [L0:F2349](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) | 6 | Word 'others' (L0:2349, suppressive) |  the word "others" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.340 |
| 3 | `inspect_feature` ×13 | L6:11646, L18:14677, L4:7864, L6:16329, L12:12940, L19:9685, L4:15317, L7:8644, L0:2349, L2:7672, L14:12501, L18:14743, L6:11327 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@29` | ❌ error | — | — | Trace L18:F14677 (women/girls feature) at pos 29. What input tokens drive it? Fi… |
| SA-2 | `L6:F11646@1` | ✅ reported | 4 | 6 | Trace L6:F11646 (female pronouns/titles) at pos 1. Find input token origins - li… |
| SA-3 | `L19:F9685@29` | ✅ reported | 4 | 6 | Trace L19:F9685 (women's names + roles) at pos 29. What input token triggers it? |
| SA-4 | `L12:F12940@2` | ❌ error | — | — | Trace L12:F12940 (female pronouns/possessives) at pos 2. Find input token. |

<details>
<summary><b>SA-2</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@1, k=10 | Emb:"She"@1 (de=19.25) +9 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 5 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 6 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 7 | `inspect_feature` | L4, F15688 | " sentences that contain the word "she" and words associated with confl" |
| 8 | `get_upstream_features` | L5:F10952@1, k=10 | Emb:"She"@1 (de=8.56) +9 more |
| 9 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |

**Findings:** The female‑pronoun feature L6:F11646 is primarily driven by the embedding of the token “She”. The signal propagates through a chain of pronoun‑detector features (L4:F7864 → L6:F11646, L5:F10952 → L6:F11646, L2:F2128 → L5:F10952). All paths reach layers ≤ 8 and contain a positive embedding contribution, satisfying the termination criteria.

</details>

<details>
<summary><b>SA-3</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F9685 | " references to women's names and their roles or accomplishments." |
| 2 | `get_upstream_features` | L19:F9685@29, k=15 | Emb:" She"@29 (de=5.62) +14 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 5 | `inspect_feature` | L14, F13478 | " occurrences of people's names, often with titles" |
| 6 | `get_upstream_features` | L6:F11646@29, k=10 | Emb:" She"@29 (de=17.62) +9 more |

**Findings:** The high‑level feature L19:F9685 that signals women's names and roles is primarily driven by low‑layer gender‑pronoun detection. The strongest upstream influence is the token embedding " She" at the same position (pos 29) with a large positive direct effect (5.6) and an even larger effect on the lower‑layer gate L6:F11646 (17.6). L6:F11646 acts as a gender‑pronoun detector, feeding into L19 and al…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F11327@15, k=8 → Emb:" food"@15 (de=34.00) +7 more |
| 2 | `get_upstream_features` | L14:F12501@3, k=8 → L13:F11685 (de=-7.72) +7 more |
| 3 | `get_upstream_features` | L18:F14743@29, k=5 → Emb:" She"@29 (de=16.88) +4 more |
| 4 | `get_upstream_features` | L12:F12940@2, k=5 → Emb:"She"@1 (de=6.56) +4 more |
| 5 | `get_upstream_features` | L2:F7672@1, k=5 → Emb:"She"@1 (de=13.88) +4 more |

### Build

`build_circuit` → 17 nodes, 22 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 35,316 | 4,321 | 124,583 | 0 | $0.0233 | — | — |
| SA-3 | openai/gpt-oss-120b | 55,931 | 4,084 | 2,592 | 0 | $0.0109 | ✅ 4F/6E | Trace L19:F9685 (women's names + roles) at pos 29. What inpu… |
| SA-2 | openai/gpt-oss-120b | 117,094 | 7,770 | 7,584 | 0 | $0.0223 | ✅ 4F/6E | Trace L6:F11646 (female pronouns/titles) at pos 1. Find inpu… |
| **Total** | | **208,341** | **16,175** | **134,759** | **0** | **$0.0565** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 37s