# Circuit Oracle Report
**Date:** 2026-07-28 07:21:02 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "nurse" classification is driven primarily by a cascade of **female-referential / female-gendered features** built from the pronouns "She" and the name "Linda" — not by genuine profession tokens — with only one weak profession-specific path (the obstetrics/birth feature fed by "labor" and "delivery") reaching the output.

**Confidence:** 8

**Reasoning:**

**The dominant path is gender-marked, not profession-marked.** The strongest single direct effect on the probe is L18:F14677 ("instances of women or girls being mentioned," activation 30, direct_effect 0.32). Its largest single input is the raw token "She" (Emb at pos 1, direct_effect 27.1), and it also receives strong excitation from L4:F7864 and L6:F11646 (both female-pronoun features that promote "herself"/"she"/"her"). This feature is purely about the *gender* of the subject, not about nursing.

The second-strongest contributor is L19:F9685 ("women's names and their roles or accomplishments," direct_effect 0.24). Its top embedding inputs are the token "Linda" (pos 24, direct_effect 3.45) and again "She" (pos 1, direct_effect 2.98), plus a smaller push from the "nurse" token (pos 7, direct_effect 1.80). The feature also receives the woman's-name feature L7:F8644 (pos 24 "Linda"), which itself is suppressed by the L4–L6 female-pronoun path (note the negative direct_effects of L4:F7864 = -2.0 onto L7:F8644 in some paths). Again, this is fundamentally a *named-female-referent* signal.

L12:F12940 ("references to female pronouns and possessive pronouns," direct_effect 0.32) and L12:F14970 ("names of people, both first and last names") are also deeply female-coded: their top input is the "She" embedding (direct_effect 6.03 onto F12940), and they promote "herself" / suppress "himself."

Even L6:F11646 ("references to women, potentially triggered by pronouns and titles") is a gender feature — it is built almost entirely from the "She" embedding (direct_effect 19.25) plus a downstream L4:F7864 (which autointerp says is "code snippets" but actually promotes "herself"/"she"). 

**The only profession-related features are surprisingly weak.** L6:F15267 ("words in the document referring to the profession of nursing," activation 23.4, direct_effect 0.39) is the cleanest profession indicator, and it is fed by the "nurse" embedding (pos 7, direct_effect 7.06) and "practitioner" (pos 8, direct_effect 3.48) — genuine profession evidence. However, it does **not** feed the probe logit directly in this graph; its downstream connection is into the L7 woman-name feature rather than into the output. L4:F13803 ("terms related to obstetrics and gynecology," direct_effect 0.29) is fed by the "labor" (direct_effect 10.2) and "delivery" (direct_effect 13.8) embeddings via a birth-feature (L3:F9008) — this *is* a legitimate domain signal, but it is the smallest of the major contributors and is essentially a medical-context signal rather than a profession label.

**Net assessment supporting the user's concern.** Of the top features by direct_effect on the probe, four out of five (L18:F14677 "women," L19:F9685 "women's names & roles," L12:F12940 "female pronouns," L6:F11646 "references to women") are *gender* features whose top activated tokens and promoted tokens are "she/her/herself." Only L6:F15267 ("nursing words") and L4:F13803 ("obstetrics/gynecology") are profession/domain features, and L6:F15267 is gated to the L7 woman-name supernode rather than going straight to the logit. The probe is therefore using "the subject is female" as a strong proxy for "the subject is a nurse" — the very spurious-correlation mechanism the user suspected. The signal flow is: input "She" / "Linda" → L4–L6 female-pronoun detectors → L12 female-name feature → L18 "instances of women" / L19 "women's names & roles" → probe logit, running in parallel with a weaker, but genuine, L3–L4 birth/obstetrics path from "labor" + "delivery."

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Early female-referential features (L4–L5) | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Early female-referential features (L4–L5) |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L5:F10952](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) | 1 | Early female-referential features (L4–L5) | third person pronouns in varying contexts | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Mid-layer female-referential features (L6) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Mid-layer female-referential features (L6) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 8 | Mid-layer female-referential features (L6) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F8166](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) | 24 | Mid-layer female-referential features (L6) |  proper names longer than 4 characters and ending in 'a', 'i', or 'e' | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 24 | Woman's-name feature L7:F8644 |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 8 | Woman's-name feature L7:F8644 |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Female pronoun/name features (L12) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 24 | Female pronoun/name features (L12) |  names of people, both first and last names | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | "Instances of women mentioned" L18:F14677 |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 55 | "Instances of women mentioned" L18:F14677 |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 24 | "Women's names and roles" L19:F9685 |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 46 | Obstetrics/gynecology feature L4:F13803 |  terms related to obstetrics and gynecology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L3:F9008](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) | 46 | Birth/childbirth feature L3:F9008 |  words related to childbirth or birth in general, including in animals. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11646 de=0.494 |
| 3 | `inspect_feature` ×10 | L6:11646, L4:7864, L4:15317, L6:15267, L12:14970, L12:12940, L18:14677, L7:8644, L4:13803, L19:9685 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F15267@8` | ❌ error | — | — | Trace L6:F15267 ('nursing profession words') upstream. This is the one professio… |
| SA-2 | `L6:F11646@1` | ✅ reported | 3 | 3 | Trace L6:F11646 ('references to women, pronouns and titles') upstream. This is a… |
| SA-3 | `L12:F12940@2` | ❌ error | — | — | Trace L12:F12940 ('female pronouns and possessive pronouns') upstream. This is a… |
| SA-4 | `L18:F14677@1` | ❌ error | — | — | Trace L18:F14677 ('instances of women or girls being mentioned') upstream. This … |
| SA-5 | `L4:F13803@46` | ✅ reported | 4 | 8 | Trace L4:F13803 ('terms related to obstetrics and gynecology') upstream. This is… |
| SA-6 | `L19:F9685@24` | ❌ error | — | — | Trace L19:F9685 ('women's names and their roles or accomplishments') upstream. D… |

<details>
<summary><b>SA-2</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@1, k=10 | Emb:"She"@1 (de=19.25) +9 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |

**Findings:** The target feature L6:F11646, which flags references to women via pronouns and titles, receives its strongest positive influence directly from the input embedding token 'She' (direct_effect 19.25). Additional upstream contributors are L4:F7864 and L5:F10952, both situated in layers 4 and 5 (within the lower‑third of the model). These upstream features also promote female‑related tokens and thus am…

</details>

<details>
<summary><b>SA-5</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13803 | " terms related to obstetrics and gynecology" |
| 2 | `get_upstream_features` | L4:F13803@46, k=10 | Emb:" delivery"@46 (de=13.81) +9 more |
| 3 | `inspect_feature` | L3, F9008 | " words related to childbirth or birth in general, including in animals" |
| 4 | `get_upstream_features` | L3:F9008@46, k=10 | Emb:" delivery"@46 (de=14.25) +9 more |
| 5 | `inspect_feature` | L0, F5398 | " the word "empty" in technical texts" |
| 6 | `inspect_feature` | L1, F12174 | " words relating to ways things are conventionally done, potential prob" |
| 7 | `inspect_feature` | L1, F4609 | " words related to childbirth and motherhood" |
| 8 | `get_upstream_features` | L1:F12174@46, k=10 | Emb:" labor"@44 (de=5.66) +9 more |

**Findings:** The obstetrics/gynecology feature (L4:F13803) is primarily driven by raw input tokens "delivery" and "labor", both with large positive direct effects. A higher‑level birth detector (L3:9008) also contributes, and it in turn receives excitation from the same tokens and a modest generic L1 feature. All required conditions are satisfied: we have reached a lower‑third layer (layer 4 ≤ 8) and identifie…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L12:F12940@2, k=10 → Emb:"She"@1 (de=6.03) +9 more |
| 2 | `get_upstream_features` | L18:F14677@1, k=10 → Emb:"She"@1 (de=27.12) +9 more |
| 3 | `get_upstream_features` | L19:F9685@24, k=10 → Emb:" Linda"@24 (de=3.45) +9 more |
| 4 | `get_upstream_features` | L7:F8644@24, k=10 → Emb:"She"@1 (de=7.34) +9 more |
| 5 | `get_upstream_features` | L6:F15267@8, k=10 → Emb:" nurse"@7 (de=7.06) +9 more |
| 6 | `get_upstream_features` | L12:F14970@24, k=10 → Emb:"<bos>"@0 (de=-3.17) +9 more |
| 7 | `inspect_feature` ×8 | L11:9183, L9:8770, L15:851, L10:12232, L7:2765, L6:8166, L5:10952, L3:9008 |
| 8 | `get_upstream_features` | L3:F9008@46, k=8 → Emb:" delivery"@46 (de=14.25) +7 more |

### Build

`build_circuit` → 15 nodes, 26 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 55,511 | 5,472 | 149,714 | 0 | $0.0322 | — | — |
| SA-2 | openai/gpt-oss-120b | 33,726 | 2,343 | 0 | 0 | $0.0065 | ✅ 3F/3E | Trace L6:F11646 ('references to women, pronouns and titles')… |
| SA-5 | openai/gpt-oss-120b | 97,084 | 7,865 | 0 | 0 | $0.0193 | ✅ 4F/8E | Trace L4:F13803 ('terms related to obstetrics and gynecology… |
| **Total** | | **186,321** | **15,680** | **149,714** | **0** | **$0.0579** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 42s