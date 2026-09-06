# Circuit Oracle Report
**Date:** 2026-07-28 07:23:00 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by male-gendered pronoun/male-biographical features, with weak positive contributions from the lexical "research" and "science" tokens; the user's concern is well-founded — gender markers dominate the circuit while genuine profession/field indicators are a minor side-channel.

**Confidence:** 8

**Reasoning:**

Looking at the top direct effects on the probe direction, the most influential features are all gendered language detectors:

- **L7:F14893** (label: "pronouns or possessive pronouns", frac_nonzero=0.009) has direct_effect = +0.430 — fires on "his/his/her" with promoted tokens = `▁herself, ▁elle, ▁she` (feminine-promoting). Upstream: the **Emb: "His" (pos 1)** is its biggest driver (direct_effect=23.5), confirming this is a male-possessive circuit originating from the very first content token.
- **L7:F14946** (label: "the possessive pronoun 'his'", frac_nonzero=0.017) direct_effect = −0.426 — anti-his detection, again tracing back to **Emb: "His"** (de=18.4) and Emb:"\<bos\>" (de=3.8).
- **L6:F12990** (label: "male pronouns and titles along with descriptors associated with men", frac_nonzero=0.068) direct_effect = −0.295 — fires on "his, man, husband, himself" with suppressed_tokens = `▁herself, ▁she, ▁ihrem`. Its biggest upstream is again **Emb: "His"** (de=4.9).
- **L18:F14743** (label: "He", frac_nonzero=0.018) fires at TWO positions (pos 14 and pos 37) with direct_effects of −0.252 and −0.205. Upstream it is fed by the **Emb: " He"** at pos 14 (de=22.4) and pos 37 (de=24.0), plus L17:F5889 ("references to people with pronouns and possessive pronouns") and L13:F6622 ("pronouns"). This is a textbook generic-pronoun stack, not a profession circuit.
- **L18:F7400** and **L18:F10315** (both labeled "pronouns and possessive pronouns", frac_nonzero ≈ 0.016/0.039) and **L19:F8814** ("various pronouns and names referring to people", frac_nonzero=0.087) and **L19:F8186** ("references to a person, especially third-person pronouns", frac_nonzero=0.026) and **L22:F12117** ("references to actions that people can take or have taken", frac_nonzero=0.034) all chain back to **Emb: "His"** (de=9.3 for F8814) and **Emb: "He"** at pos 14/37. Even the L17:F3683 "biographies" feature (which does fire on biographical text like "Jianlin Cheng…") sits in the pronoun-gendered circuit; its biggest upstream is also **Emb: " He"** (de=14.5) and L18:F14743.
- **L0:F1069** ("references to a male person, particularly when using the pronoun 'He' or 'His'", frac_nonzero=0.008) is the lowest-layer male-pronoun detector, feeding forward into all the above features.

The only features driving the probe that are NOT pure pronoun/male markers are the lexical topic words:

- **L0:F4564** ("the word 'research'", frac_nonzero=0.007) direct_effect = +0.157, driven by **Emb: " research"** (pos 2, de=28.1) — a genuine content signal.
- **L0:F2827** ("the word 'science'", frac_nonzero=0.010) direct_effect = −0.122, driven by **Emb: " scientific"** (pos 8, de=22.1).
- **L2:F9740** ("the word 'interest' and related words", frac_nonzero=0.006) direct_effect = +0.133, driven by **Emb: " interests"** (pos 3, de=27.0).
- **L0:F6051** ("periods, spaces, and the number 1", frac_nonzero=0.057) direct_effect = −0.125, driven by **Emb: "."** (pos 13, de=46.3) — a syntactic-formatting feature that is anti-correlated with biographies.

The sum of absolute direct effects on the probe direction is overwhelmingly carried by gendered features. The top-2 contributions alone (L7:F14893 +0.43 and L7:F14946 −0.43) are pure pronoun features; the top-10 contains only one topic-word feature (L0:F4564 "research"). Crucially, the "He" detector (L18:F14743) at both pos 14 and pos 37 pushes AGAINST the probe direction (negative direct_effect), meaning the pronoun circuit is partially cancelling itself rather than providing an unambiguous profession signal.

The two biography-related features that appear (L17:F3683 "biographies" and L18:F9023 "personal names and associated titles") are themselves downstream of male-pronoun features (L18:F14743, L0:F1069) and are tied to the "He" tokens, not to any profession-specific vocabulary. There is no feature in the top-25 whose label is "professor", "academic", "scientist", or any field/occupation indicator; the only "title/role" feature (L18:F9023) fires on bare personal names rather than on "Dr./PhD/Professor" tokens, and even so it sits downstream of the pronoun stack.

**Bottom line on the user's concern:** The concern is strongly supported by the circuit. The dominant signal flow is Emb("His"/"He") → L0:L2 male-pronoun features → L4:L6 mid-pronoun/man features → L7 pronoun features (largest individual contributors, ±0.43) → L14:L22 biography/pronoun features. The genuine profession/field signal (L0:F4564 "research", L0:F2827 "science", L2:F9740 "interest") is present but constitutes a much smaller portion of the total direct effect and is partially cancelled by an anti-pronoun push in the same direction. The probe is largely classifying along a male-gendered biographical-text axis rather than along a computer-science/researcher axis.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: His (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: research (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: interests (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: scientific (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: He (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 37 | Emb: He (pos 37) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: . (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F4564](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) | 2 | Lexical: research (L0:F4564) | the word "research." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) |
| [L0:F2827](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2827) | 8 | Lexical: science (L0:F2827) |  the word "science" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2827) |
| [L2:F9740](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9740) | 3 | Lexical: interest/interest(s) (L2:F9740) | the word "interest" and related words. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9740) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 13 | Lexical: period/spacing (L0:F6051) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | Low-level male-pronoun features (L0:L2) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L2:F5491](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) | 1 | Low-level male-pronoun features (L0:L2) | references to God in the third person. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Low-level male-pronoun features (L0:L2) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 14 | Low-level male-pronoun features (L0:L2) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | Mid-layer pronoun/man features (L4:L6) |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Mid-layer pronoun/man features (L4:L6) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Late pronoun features pushing AGAINST probe (L7) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | Late pronoun features pushing AGAINST probe (L7) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L14:F14097](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) | 14 | Late biography/pronoun features (L14:L19) pushing AGAINST probe |  occurrences of the word "he" | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 14 | Late biography/pronoun features (L14:L19) pushing AGAINST probe | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 37 | Late biography/pronoun features (L14:L19) pushing AGAINST probe | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F7400](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) | 1 | Late biography/pronoun features (L14:L19) pushing AGAINST probe |  words related to coding and software/UI interfaces, with some bias toward non-English words | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 1 | Late biography/pronoun features (L14:L19) pushing AGAINST probe |  pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | Late biography/pronoun features (L14:L19) pushing AGAINST probe |  various pronouns and names referring to people | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |
| [L19:F8186](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8186) | 14 | Late biography/pronoun features (L14:L19) pushing AGAINST probe |  references to a person, especially third-person pronouns and possessive pronouns. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8186) |
| [L22:F12117](https://neuronpedia.org/gemma-2-2b/22-gemmascope-transcoder-16k/12117) | 15 | Late biography/pronoun features (L14:L19) pushing AGAINST probe |  references to actions that people can take or have taken. | [view](https://neuronpedia.org/gemma-2-2b/22-gemmascope-transcoder-16k/12117) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe direction (output) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L7:14893 de=0.430 |
| 3 | `inspect_feature` ×12 | L7:14893, L7:14946, L6:12990, L18:14743, L19:8814, L0:2994, L4:4315, L18:7400, L0:4564, L18:10315, L2:9740, L2:5491 |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ❌ error | — | — | Trace L7:F14893 — labeled "pronouns or possessive pronouns" — upstream to the in… |
| SA-2 | `L18:F14743@14` | ❌ error | — | — | Trace L18:F14743 — labeled "He" — upstream to the input embeddings. Determine wh… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_features` | token="", k=25 → 25 features; top: L7:14893 de=0.430 |
| 2 | `get_upstream_features` | L7:F14893@1, k=10 → Emb:"His"@1 (de=23.50) +9 more |
| 3 | `get_upstream_features` | L7:F14946@1, k=10 → Emb:"His"@1 (de=18.38) +9 more |
| 4 | `get_upstream_features` | L6:F12990@1, k=10 → Emb:"His"@1 (de=4.91) +9 more |
| 5 | `get_upstream_features` | L18:F14743@14, k=10 → Emb:" He"@14 (de=22.38) +9 more |
| 6 | `get_upstream_features` | L19:F8814@1, k=10 → Emb:"His"@1 (de=9.31) +9 more |
| 7 | `get_upstream_features` | L0:F2994@1, k=10 → Emb:"His"@1 (de=19.75) +9 more |
| 8 | `get_upstream_features` | L0:F4564@2, k=10 → Emb:" research"@2 (de=28.12) +9 more |
| 9 | `get_upstream_features` | L2:F9740@3, k=10 → Emb:" interests"@3 (de=27.00) +9 more |
| 10 | `get_upstream_features` | L2:F5491@1, k=10 → Emb:"His"@1 (de=23.88) +9 more |
| 11 | `get_upstream_features` | L4:F4315@1, k=10 → Emb:"His"@1 (de=23.50) +9 more |
| 12 | `inspect_feature` ×10 | L18:7400, L7:16284, L19:8186, L22:12117, L14:14097, L0:1069, L0:6051, L0:2827, L0:14201, L0:2749 |
| 13 | `get_upstream_features` | L18:F14743@37, k=8 → Emb:" He"@37 (de=24.00) +7 more |
| 14 | `get_upstream_features` | L19:F8814@1, k=8 → Emb:"His"@1 (de=9.31) +7 more |
| 15 | `get_upstream_features` | L18:F7400@1, k=8 → Emb:"His"@1 (de=13.00) +7 more |
| 16 | `get_upstream_features` | L18:F10315@1, k=8 → Emb:"His"@1 (de=21.38) +7 more |
| 17 | `get_upstream_features` | L0:F6051@13, k=5 → Emb:"."@13 (de=46.25) +4 more |
| 18 | `get_upstream_features` | L0:F2827@8, k=5 → Emb:" scientific"@8 (de=22.12) +4 more |
| 19 | `get_upstream_features` | L0:F14201@3, k=5 → Emb:" research"@2 (de=8.50) +4 more |
| 20 | `get_upstream_features` | L7:F16284@14, k=8 → L6:F12990 (de=2.41) +7 more |
| 21 | `get_upstream_features` | L19:F8186@14, k=8 → Emb:" He"@14 (de=14.50) +7 more |
| 22 | `get_upstream_features` | L22:F12117@15, k=8 → Emb:" He"@14 (de=4.94) +7 more |
| 23 | `get_upstream_features` | L14:F14097@14, k=8 → Emb:" He"@14 (de=2.47) +7 more |
| 24 | `inspect_feature` ×10 | L17:5889, L13:6622, L15:3330, L15:13002, L17:3683, L16:2918, L18:7217, L16:10989, L12:3684, L18:9023 |

### Build

`build_circuit` → 16 nodes, 16 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 61,399 | 6,759 | 263,810 | 0 | $0.0424 | — | — |
| **Total** | | **61,399** | **6,759** | **263,810** | **0** | **$0.0424** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 30s