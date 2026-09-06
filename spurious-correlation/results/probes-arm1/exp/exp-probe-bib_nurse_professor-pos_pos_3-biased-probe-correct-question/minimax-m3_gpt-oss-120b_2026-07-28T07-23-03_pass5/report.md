# Circuit Oracle Report
**Date:** 2026-07-28 07:23:03 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "nurse" classification is driven by a hybrid circuit in which female-gender/female-name features are the dominant late-layer pathway, while profession-specific vocabulary ("nurse practitioner", "labor", "delivery", OB/GYN terms) makes a smaller, more localized contribution.

**Confidence:** 8

**Reasoning:** The circuit has two parallel branches that converge on the probe:

**Gender/girl-name branch (dominant).** The Emb "She" token (pos 1) is the largest single source in the entire graph — it directly drives L4:F7864 ("named-entity recognition at She", direct_effect=24.6 from the embedding alone) and L4:F15317 (13.6), and from there L6:F11646 ("references to women… pronouns and titles", direct_effect=0.49) at pos 1 and 2. L6:F11646 feeds L12:F12940 ("female pronouns and possessive pronouns", direct_effect=0.32) and L12:F14970 ("names of people", at the " Linda" position, direct_effect=0.32). The late-layer features L18:F14677 ("instances of women or girls being mentioned", pos 1 and pos 55, total direct_effect≈0.64) and L19:F9685 ("women's names and their roles/accomplishments", pos 24 and 55, total direct_effect≈0.45) then fire on the "She", "she", and "Linda" tokens. These two L18/L19 features have direct_effects 0.32 and 0.24 on the probe and are fed by the Emb tokens "She" (27.1), "she" (23.9), and " Linda" (3.45) almost as strongly as by any profession features — i.e., the embedding of the pronoun "She" is by far the largest contributor to the L18 women-mention detector on pos 1.

**Profession branch (secondary).** L4:F13803 ("obstetrics and gynecology terms") at pos 46 is driven primarily by Emb " delivery" (13.8) and Emb " labor" (10.2), with L3:F9008 ("childbirth/birth vocabulary") mediating — these are genuine profession/specialty indicators. L6:F15267 ("words referring to the profession of nursing", direct_effect=0.39) is driven by Emb " nurse" (7.1) at pos 7, but it does not propagate strongly to the late layers; it has its own direct_effect=0.39 on the probe but is otherwise a leaf.

**Net interpretation.** The user's concern is well-founded but not the whole story. The probe DOES use genuine profession indicators (L4:F13803 OB/GYN, L6:F15267 nursing-vocabulary) — together they account for roughly +0.68 of direct_effect. But the late-layer pipeline that aggregates evidence for the probe is overwhelmingly female-gendered: L12:F12940 (female pronouns, +0.32), L18:F14677 (women mentioned, +0.64 across two positions), and L19:F9685 (women's names and roles, +0.45). These features are triggered almost entirely by the pronoun "She" (pos 1) and the name "Linda" (pos 24) — surface-level gender/person markers — rather than by tokens like "nurse" (pos 7) or "practitioner" (pos 8), which are the profession-defining tokens. Notably, the Emb " nurse" token feeds L6:F15267 strongly but does not reach L12 or beyond. So while the profession branch exists, the late-layer features the probe actually reads from are gender features, and the strong flow from Emb "She" → L4 → L6 → L12 → L18 → probe means the model could produce a high probe score on a male nurse with the same clinical vocabulary, just with "He" instead of "She", because the same late-layer pipeline would not activate. This is consistent with the user's worry that spurious gender markers are doing significant work, though genuine profession features are not entirely absent.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: She (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 24 | Emb: Linda (pos 24) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 55 | Emb: she (pos 55) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: nurse (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 44 | Emb: labor/delivery tokens (pos 44, 46) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 46 | Emb: labor/delivery tokens (pos 44, 46) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L2:F7672](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) | 1 | Early entity/pronoun recognition (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) |
| [L2:F5859](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) | 24 | Early entity/pronoun recognition (L0-L2) |  first names (mostly female) | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) |
| [L3:F9008](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) | 46 | Birth/childbirth vocabulary (L3) |  words related to childbirth or birth in general, including in animals. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 46 | Obstetrics/gynecology terms (L4) |  terms related to obstetrics and gynecology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Named-entity recognition at 'She' (L4) |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Named-entity recognition at 'She' (L4) | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | References to women / female pronouns at start (L6) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | References to women / female pronouns at start (L6) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 8 | Nursing profession vocabulary (L6) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Female pronouns and possessive pronouns (L12) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 24 | Names of people, first and last (L12) |  names of people, both first and last names | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Instances of women or girls being mentioned (L18) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 55 | Instances of women or girls being mentioned (L18) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 24 | Women's names and their roles/accomplishments (L19) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 55 | Women's names and their roles/accomplishments (L19) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.494 |
| 3 | `inspect_feature` ×9 | L6:11646, L6:15267, L4:7864, L4:15317, L12:14970, L12:12940, L18:14677, L4:13803, L19:9685 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@2` | ❌ error | — | — | Trace L6:F11646 ("references to women, triggered by pronouns/titles") upstream. … |
| SA-2 | `L12:F12940@2` | ❌ error | — | — | Trace L12:F12940 ("female pronouns and possessive pronouns") upstream. direct_ef… |
| SA-3 | `L19:F9685@24` | ❌ error | — | — | Trace L19:F9685 ("women's names and their roles/accomplishments") upstream. dire… |
| SA-4 | `L4:F13803@46` | ❌ error | — | — | Trace L4:F13803 ("obstetrics/gynecology terms") upstream. direct_effect=0.29. Th… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F11646@2, k=12 → L4:F15317 (de=8.75) +11 more |
| 2 | `get_upstream_features` | L12:F12940@2, k=12 → Emb:"She"@1 (de=6.03) +11 more |
| 3 | `get_upstream_features` | L19:F9685@24, k=12 → Emb:" Linda"@24 (de=3.45) +11 more |
| 4 | `get_upstream_features` | L4:F13803@46, k=12 → Emb:" delivery"@46 (de=13.81) +11 more |
| 5 | `get_upstream_features` | L6:F15267@8, k=12 → Emb:" nurse"@7 (de=7.06) +11 more |
| 6 | `get_upstream_features` | L12:F14970@24, k=12 → Emb:"<bos>"@0 (de=-3.17) +11 more |
| 7 | `inspect_feature` ×11 | L10:14965, L8:7245, L7:2765, L6:8166, L3:9008, L3:10398, L5:1275, L4:11037, L7:8644, L18:14677, L2:5859 |
| 8 | `get_upstream_features` | L18:F14677@1, k=8 → Emb:"She"@1 (de=27.12) +7 more |
| 9 | `get_upstream_features` | L18:F14677@55, k=8 → Emb:" she"@55 (de=23.88) +7 more |
| 10 | `get_upstream_features` | L19:F9685@55, k=8 → Emb:" she"@55 (de=10.12) +7 more |
| 11 | `inspect_feature` ×5 | L18:9023, L18:10572, L16:6025, L9:2984, L9:2587 |
| 12 | `get_upstream_features` | L7:F8644@24, k=8 → Emb:"She"@1 (de=7.34) +7 more |
| 13 | `get_upstream_features` | L6:F8166@24, k=8 → L5:F6637 (de=-3.17) +7 more |
| 14 | `get_upstream_features` | L12:F14970@24, k=8 → Emb:"<bos>"@0 (de=-3.17) +7 more |
| 15 | `get_upstream_features` | L4:F7864@1, k=8 → Emb:"She"@1 (de=24.62) +7 more |
| 16 | `get_upstream_features` | L4:F15317@2, k=8 → Emb:"She"@1 (de=13.56) +7 more |

### Build

`build_circuit` → 16 nodes, 18 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 68,937 | 5,824 | 243,951 | 0 | $0.0423 | — | — |
| **Total** | | **68,937** | **5,824** | **243,951** | **0** | **$0.0423** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 22s