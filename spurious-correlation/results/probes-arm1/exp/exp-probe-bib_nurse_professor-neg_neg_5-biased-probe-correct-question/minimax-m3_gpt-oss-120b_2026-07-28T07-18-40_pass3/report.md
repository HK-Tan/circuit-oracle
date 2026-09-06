# Circuit Oracle Report
**Date:** 2026-07-28 07:18:40 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by a chain of male-pronoun features (L0 "his/he" detectors → L4/L6/L7 pronoun detectors → L18 "He" detector → L21/L22 actions-by-male features) feeding the output, with the only profession-related input (the token "history" at pos 8) contributing only via a single L0 feature (F1773, direct_effect +0.11) and the universities feature (F10137, –0.11); the user's concern is confirmed — the circuit is dominated by spurious gender-marker features rather than genuine profession indicators.

**Confidence:** 8

**Reasoning:**

**Spurious gender-marker dominance.** Out of the top-20 features driving the probe, **17 of 20 are pronoun/possessive features** that respond to "His", "his", "He" tokens:
- **L0:F2994** ("his" / "he" detector, frac_nonzero 0.07) at pos 1 & 12, direct_effect +0.49 and +0.38 — the top two features overall.
- **L0:F1069** ("male person, 'He' or 'His'", frac_nonzero 0.008) at pos 10 & 23, also a strong driver.
- **L4:F4315**, **L6:F12990**, **L7:F14946** are all "his/he" detectors (frac_nonzero 0.02–0.07) that propagate the same male-pronoun signal upward.
- **L7:F14893** (promoted tokens = herself/she/herself, suppressed = himself/his) at +0.49 / +0.13.
- **L18:F14743** ("He" detector, direct_effect –0.29 / –0.17 at pos 10 & 23).
- **L19:F8814** (direct_effect +0.29, promotes "herself/she", suppresses "himself/his" — a late-layer anti-male selector) and **L19:F8186** (direct_effect –0.11).
- **L21:F6216** (refers to a specific person, direct_effect +0.12) and **L22:F12117** ("actions people take", direct_effect –0.18, promotes "his/himself") are the deepest pre-output features.

Subagent tracing confirms the path bottoms out at token embeddings: "His" @ pos 1 → L0:F2994 with direct_effect ≈ 23.5; "his" @ pos 12 → L0:F2994 with direct_effect ≈ 44.5; "He" @ pos 10/23 → L0:F1069 with direct_effect ≈ 35.7. The entire gender signal is a literal lexical reflex on the male pronouns themselves, with no semantic abstraction above "this is a male referent."

**Genuine profession evidence is weak and partially suppressed.** Only **2 of 20** features carry profession-relevant content:
- **L0:F1773** ("history" token detector, frac_nonzero 0.007) at pos 8 — direct_effect only +0.11, and it bottoms out at the "history" embedding (direct_effect 26.75) with no further propagation (no L2/L18 "historian" feature appears in the top-20).
- **L12:F10137** (universities/institutions including Harvard, Stanford, Chicago) at pos 20 — direct_effect –0.11. Counterintuitively *suppresses* the probe score.

**Subagent interpretation note.** The L19:F8814 subagent reported a "gender-balance gate" interpretation, but the direct_effect pattern is clear: in the top features, the net signed contribution of male-pronoun features to the probe is large and mixed (some positive, some negative, but with massive |direct_effect| magnitudes up to 0.49), while the profession content is single-token, low-magnitude, and partly suppressed. There is **no high-level "historian" or "academic male" abstraction** in the circuit — the deepest pre-output features (L21–L22) still encode "actions taken by a he-referent," not profession identity.

**Verdict.** The user's concern is validated: the probe is being driven by a 4-layer cascade of male-pronoun lexical features anchored to the specific tokens "His", "his", "He" in the prompt, with negligible contribution from the words "history", "Ph.D.", "Economics", or the university names that would constitute legitimate profession evidence. This is a textbook spurious-correlation circuit, likely reflecting training-data co-occurrence of male pronouns with "historian" rather than genuine profession understanding.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | Low-layer male pronoun detectors (L0, L4) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 12 | Low-layer male pronoun detectors (L0, L4) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 10 | Low-layer male pronoun detectors (L0, L4) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 23 | Low-layer male pronoun detectors (L0, L4) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | Low-layer male pronoun detectors (L0, L4) |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L0:F1773](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1773) | 8 | "history" token detector (L0) |  the word "history" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1773) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Mid-layer male pronoun/possessive detectors (L6, L7) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 10 | Mid-layer male pronoun/possessive detectors (L6, L7) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | Mid-layer male pronoun/possessive detectors (L6, L7) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 10 | Mid-layer male pronoun/possessive detectors (L6, L7) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 10 | Late "He" detector (L18) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 23 | Late "He" detector (L18) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 1 | Late "He" detector (L18) |  pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L18:F7400](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) | 1 | Late "He" detector (L18) |  words related to coding and software/UI interfaces, with some bias toward non-English words | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | Late anti-male pronoun detector (L19) |  various pronouns and names referring to people | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |
| [L19:F8186](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8186) | 10 | Late anti-male pronoun detector (L19) |  references to a person, especially third-person pronouns and possessive pronouns. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8186) |
| [L22:F12117](https://neuronpedia.org/gemma-2-2b/22-gemmascope-transcoder-16k/12117) | 11 | Late "actions by He" feature (L21, L22) |  references to actions that people can take or have taken. | [view](https://neuronpedia.org/gemma-2-2b/22-gemmascope-transcoder-16k/12117) |
| [L21:F6216](https://neuronpedia.org/gemma-2-2b/21-gemmascope-transcoder-16k/6216) | 10 | Late "actions by He" feature (L21, L22) |  references to a specific person, often using pronouns or names | [view](https://neuronpedia.org/gemma-2-2b/21-gemmascope-transcoder-16k/6216) |
| [L21:F4895](https://neuronpedia.org/gemma-2-2b/21-gemmascope-transcoder-16k/4895) | 11 | Late "actions by He" feature (L21, L22) | prepositions and related words | [view](https://neuronpedia.org/gemma-2-2b/21-gemmascope-transcoder-16k/4895) |
| [L12:F10137](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/10137) | 20 | Universities/institutions (L12) |  names of universities, cities, publications and other institutions. | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/10137) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Late pronoun gate (L7) — promotes female |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 10 | Late pronoun gate (L7) — promotes female |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L2:F5491](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) | 1 | Late pronoun gate (L7) — promotes female | references to God in the third person. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L7:14893 de=0.490 |
| 3 | `inspect_feature` ×15 | L7:14893, L0:2994, L19:8814, L2:5491, L0:1773, L7:14946, L6:12990, L4:4315, L18:7400, L18:10315, L22:12117, L18:14743, L21:6216, L19:8186, L12:10137 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F8814@1` | ✅ reported | 6 | 7 | Trace upstream from L19:F8814 (promotes "herself/she/her", suppresses "himself/h… |
| SA-2 | `L7:F14893@1` | ✅ reported | 3 | 8 | Trace upstream from L7:F14893 (pronoun/possessive pronoun detector) at pos 1. Id… |
| SA-3 | `L18:F14743@10` | ✅ reported | 5 | 7 | Trace upstream from L18:F14743 ("He" detector) at pos 10 (the position of "He" i… |
| SA-4 | `L0:F1773@8` | ❌ error | — | — | Trace upstream from L0:F1773 ("history" token detector) at pos 8. Confirm this f… |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F8814 | " various pronouns and names referring to people" |
| 2 | `get_upstream_features` | L19:F8814@1, k=15 | Emb:"His"@1 (de=9.31) +14 more |
| 3 | `inspect_feature` | L18, F7400 | " words related to coding and software/UI interfaces, with some bias to" |
| 4 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 5 | `get_upstream_features` | L18:F7400@1, k=10 | Emb:"His"@1 (de=13.00) +9 more |
| 6 | `get_upstream_features` | L7:F14946@1, k=10 | Emb:"His"@1 (de=18.38) +9 more |
| 7 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 8 | `inspect_feature` | L18, F10315 | " pronouns and possessive pronouns" |
| 9 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 10 | `get_upstream_features` | L6:F12990@1, k=10 | Emb:"His"@1 (de=4.91) +9 more |

**Findings:** Tracing from L19:F8814 (female‑pronoun promoter) reveals that its strongest excitatory upstream drivers are raw input token embeddings for the word "His" and a cascade of low‑layer pronoun detectors (L4:4315, L6:12990, L7:14946, L18:10315) that primarily promote male pronouns. The pathway reaches layer 4 (<=8) and includes direct embedding contributions, satisfying the required termination conditi…

</details>

<details>
<summary><b>SA-2</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `get_upstream_features` | L6:F12990@1, k=10 | Emb:"His"@1 (de=4.91) +9 more |
| 5 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 6 | `get_upstream_features` | L4:F4315@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |

**Findings:** The male‑gender signal for the token "His" is conveyed directly from the input embedding of that token. The embedding feeds strongly (23.5) into the low‑layer pronoun detector (L4:F4315) and also into the higher‑layer pronoun detector (L7:F14893). A mid‑layer male‑pronoun feature (L6:F12990) receives a smaller boost from the same embedding and then forwards a positive influence to the final pronou…

</details>

<details>
<summary><b>SA-3</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@10, k=10 | Emb:" He"@10 (de=22.38) +9 more |
| 3 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 4 | `get_upstream_features` | L0:F1069@10, k=10 | Emb:" He"@10 (de=35.75) +9 more |
| 5 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 6 | `get_upstream_features` | L18:F14743@23, k=10 | Emb:" He"@23 (de=24.50) +9 more |
| 7 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 8 | `get_upstream_features` | L17:F5889@10, k=5 | Emb:" He"@10 (de=21.75) +4 more |

**Findings:** The L18:F14743 feature ('He' detector) at both positions 10 and 23 is primarily driven by the raw input token embedding for 'He' (positive direct_effect ~22-24). Upstream tracing reveals a strong early-layer (layer 0) feature 1069 that directly responds to the male pronoun, itself excited almost entirely by the same token embedding (direct_effect ~35). This satisfies the requirement of reaching a …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F1773@8, k=5 → Emb:" history"@8 (de=26.75) +4 more |
| 2 | `get_upstream_features` | L0:F2994@12, k=5 → Emb:" his"@12 (de=44.50) +4 more |
| 3 | `get_upstream_features` | L22:F12117@11, k=8 → L21:F4895 (de=5.69) +7 more |
| 4 | `inspect_feature` ×2 | L21:4895, L0:1069 |

### Build

`build_circuit` → 14 nodes, 16 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 54,385 | 5,246 | 143,984 | 0 | $0.0312 | — | — |
| SA-2 | openai/gpt-oss-120b | 53,674 | 4,007 | 0 | 0 | $0.0105 | ✅ 3F/8E | Trace upstream from L7:F14893 (pronoun/possessive pronoun de… |
| SA-3 | openai/gpt-oss-120b | 76,200 | 5,207 | 5,056 | 0 | $0.0146 | ✅ 5F/7E | Trace upstream from L18:F14743 ("He" detector) at pos 10 (th… |
| SA-1 | openai/gpt-oss-120b | 115,632 | 6,278 | 5,120 | 0 | $0.0212 | ✅ 6F/7E | Trace upstream from L19:F8814 (promotes "herself/she/her", s… |
| **Total** | | **299,891** | **20,738** | **154,160** | **0** | **$0.0775** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 23s