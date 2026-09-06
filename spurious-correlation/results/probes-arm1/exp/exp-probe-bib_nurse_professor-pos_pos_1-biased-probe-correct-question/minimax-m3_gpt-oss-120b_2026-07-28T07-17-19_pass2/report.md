# Circuit Oracle Report
**Date:** 2026-07-28 07:17:19 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven overwhelmingly by features that fire on the feminine pronoun "she" at position 7, with a smaller secondary contribution from genuine nursing-vocabulary features; gender markers are the primary signal, profession indicators secondary.

**Confidence:** 9

**Reasoning:** The dominant positive driver is the embedding of the single token "she" (position 7), which propagates upward through a chain of female-referent features: L6:F11646 "references to women, potentially triggered by pronouns and titles" (direct_effect +1.55, frac_nonzero 0.020), L12:F12940 "female pronouns and possessive pronouns" (+0.69, 0.0065), L18:F14677 "instances of women or girls being mentioned" (+0.91, 0.012) and L19:F9685 "women's names and their roles or accomplishments" (+0.56, 0.014). The subagent confirmed L6:F11646 receives a direct_effect of 31.6 from the raw " she" embedding alone — a massive, near-deterministic excitation. Supporting features L10:F14965 "terms relating to women", L7:F8952 "references to women by direct name or pronoun", and L7:F8644 "a woman's name in a variety of contexts" form a redundant mid-layer female-detection cluster, all promoting tokens like "▁herself"/"▁she"/"▁her" and suppressing "▁himself"/"▁his".

Genuine profession signal does exist but is small: L6:F15267 "words referring to the profession of nursing" (pos 15, +0.55) and L2:F15728 "mentions of nurses and nursing" (pos 15, +0.33) fire on the tokens "nurse"/"nursing"/"Perioperative" later in the passage, providing legitimate evidence the probe should use. However, the *top direct effects* on the output (1.55, 0.91, 0.69, 0.56) all come from gender features, while the nursing feature's combined contribution (~0.88 across two positions) is comparable in magnitude to a single gender feature.

Crucially, the inhibitory features (L6:F16329 "female first names and their possessive forms" -0.67, L0:F12519 "the pronoun she" -0.71, L1:F4232 "the possessive pronoun her" -0.43, L18:F14743 "He" -0.44, L2:F7672 "mentions of women by name and relationship" +0.25 but at pos 7) show the model is *also* activating male-coded features (suppressing the output) — meaning the output is being driven by a balance of male and female pronoun features, and the female side is winning because of the dense "she/her" pattern in the prompt.

**This confirms the user's concern is valid**: the circuit's primary signal path is Emb:"she" → L6:F11646 → L12:F12940 → L18:F14677/L19:F9685 → output. The model is using gendered pronouns as a proxy for profession, not actually identifying the nursing profession from the substantive content. The genuine nursing vocabulary features (L6:F15267, L2:F15728) exist in the circuit and contribute positively, but they are secondary to the gender pathway, and a counterfactual prompt that replaced "she" with "he" while keeping "nurses"/"Perioperative" intact would likely reduce the probe score substantially despite the profession content being unchanged.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 7 | Probe classification score (output) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 7 | Late-layer female-entity features (women / names / roles) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 7 | Late-layer female-entity features (women / names / roles) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 7 | Mid-layer female-pronoun detectors | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L10:F14965](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) | 7 | Mid-layer female-pronoun detectors |  terms relating to women | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) |
| [L14:F14097](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) | 7 | Mid-layer female-pronoun detectors |  occurrences of the word "he" | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 7 | Layer 6 female reference feature (dominant positive driver) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L7:F8952](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8952) | 7 | Layer 6 female reference feature (dominant positive driver) |  references to women, by direct name or pronoun | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8952) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 7 | Layer 6 female reference feature (dominant positive driver) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 7 | Gender-feature negative contributors (inhibitory) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L1:F4232](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4232) | 7 | Gender-feature negative contributors (inhibitory) |  the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4232) |
| [L0:F12519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) | 7 | Gender-feature negative contributors (inhibitory) |  the pronoun "she" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 7 | Gender-feature negative contributors (inhibitory) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L2:F7672](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) | 7 | Gender-feature negative contributors (inhibitory) |  mentions of women by name and relationship | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 15 | Profession-related nursing features (genuine profession signal) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 14 | Profession-related nursing features (genuine profession signal) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L2:F15728](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15728) | 15 | Profession-related nursing features (genuine profession signal) |  mentions of nurses and nursing | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15728) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 7 | Profession-related nursing features (genuine profession signal) | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=1.555 |
| 3 | `inspect_feature` ×8 | L6:11646, L18:14677, L12:12940, L19:9685, L4:7864, L0:12519, L6:16329, L18:14743 |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@7` | ✅ reported | 6 | 5 | Trace L6:F11646 (female pronouns/women). What tokens at pos 7 drive it? Is there… |
| SA-2 | `L19:F9685@7` | ✅ reported | 3 | 5 | Trace L19:F9685 (women's names and roles). What's the input source? |

<details>
<summary><b>SA-1</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@7, k=10 | Emb:" she"@7 (de=31.62) +9 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 5 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 6 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |

**Findings:** The L6:F11646 gender‑pronoun feature at position 7 is driven primarily by the raw embedding of the token " she" (direct effect 31.6). Smaller positive contributions come from higher‑layer features that detect generic pronouns, named entities, and code snippets, none of which encode profession information. No upstream node with a clear profession‑related signal (e.g., tokens like "doctor", "enginee…

</details>

<details>
<summary><b>SA-2</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F9685 | " references to women's names and their roles or accomplishments." |
| 2 | `get_upstream_features` | L19:F9685@7, k=10 | Emb:" she"@7 (de=12.25) +9 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 5 | `get_upstream_features` | L6:F11646@7, k=10 | Emb:" she"@7 (de=31.62) +9 more |

**Findings:** The target feature L19:F9685 (women's names & roles) receives its strongest positive influence directly from the input token embedding ' she' at position 7 (direct_effect ≈12‑31). That embedding also drives an intermediate lower‑layer detector L6:F11646, which is a pronoun‑based women reference detector, and further upstream from there we see a minor contribution from a generic code‑snippet featur…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×8 | L6:15267, L2:15728, L10:14965, L7:8644, L14:14097, L7:8952, L2:7672, L1:4232 |

### Build

`build_circuit` → 7 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 35,410 | 3,202 | 79,322 | 0 | $0.0192 | — | — |
| SA-1 | openai/gpt-oss-120b | 57,793 | 3,261 | 2,592 | 0 | $0.0107 | ✅ 6F/5E | Trace L6:F11646 (female pronouns/women). What tokens at pos … |
| SA-2 | openai/gpt-oss-120b | 33,283 | 3,074 | 10,112 | 0 | $0.0070 | ✅ 3F/5E | Trace L19:F9685 (women's names and roles). What's the input … |
| **Total** | | **126,486** | **9,537** | **92,026** | **0** | **$0.0369** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 10s