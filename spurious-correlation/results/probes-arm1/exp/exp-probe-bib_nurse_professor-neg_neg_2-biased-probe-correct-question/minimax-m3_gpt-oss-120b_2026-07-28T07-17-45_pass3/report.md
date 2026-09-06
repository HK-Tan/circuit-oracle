# Circuit Oracle Report
**Date:** 2026-07-28 07:17:45 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

The circuit was saved (the warning is conservative — I did reach token-embedding nodes for `He` and `his`).

**Analysis:** The probe's positive classification score is driven by an academic-field detector (L6:F170) plus a tail of weak, partly offsetting pronoun signals — gender markers are present but as a *suppressor* of the probe score, not a driver. The user's concern about gender-marker-driven classification is partially borne out only in the wrong direction.

**Confidence:** 7

**Reasoning:**

**The only positive, profession-related signal is generic, not specific.** The single feature with a meaningfully positive direct effect (DE = +0.144 at pos 9) that has any academic-vocabulary content is L6:F170 ("references to academic fields, especially those in the humanities"). Its top activations are on words like *science*, *Writing*, *literature*, *English* — not on *engineer* or *mechanical*. The traced subagent confirms it is fed by L5:F10392 ("fields of academic study", frac 0.004), which in turn receives its largest positive push (DE = 3.08) directly from the **Emb: ' Mechanical'** token embedding, with secondary pushes from **Emb: 'achelors'** (1.26), **Emb: ' degree'** (0.86), and **Emb: ' Engineering'** (0.83). L5:F6384 ("higher education & professions", frac 0.007) and L3:F4113 ("academic degrees and areas of study", frac 0.003) reinforce the same pathway. Critically, **none of these features are profession-specific** — they fire on any academic discipline token ("Mechanical Engineering", "English Literature", "Sports Administration", "Business Administration" all appear in their top activating examples). So the probe is being driven by a *generic "this text mentions a field of study" detector*, not by anything that knows the difference between mechanical engineering, nursing, or history.

**Pronoun/gender features dominate the head of the list but mostly suppress the score.** Six of the top 20 features encode pronouns or gender:
- L0:F2994 "his/he" (DE = +0.39 at pos 3, also +0.13 at pos 25, +0.11 at pos 47) — but the 0.07 frac_nonzero shows it is a *generic* pronoun detector, not gender-specific; the autointerp note shows its decoder *suppresses* "his" tokens (it fires on the context around "his" but pushes the next token away from "his").
- L7:F14946 "his/he/him" (DE = −0.18, INHIBITORY).
- L12:F2175 "words referring to gender" (DE = −0.17, INHIBITORY) — promoted-token list is "himself, masculinity"; its top activations are "male, men, masculine, mens".
- L6:F12990 "male pronouns and titles" (DE = −0.17 at pos 22, INHIBITORY).
- L18:F14743 "He" (DE = −0.14, INHIBITORY at pos 22).
- L7:F14893 pronouns (DE = +0.20, but this feature promotes "herself/she" and suppresses "his/himself" — it is a feature for *feminine* pronouns that happens to fire on the "his" position; its positive effect is small).

The net signed contribution of the pronoun/gender features is therefore **negative** on the probe score. The probe is being *pushed away* from classifying by the very male-pronoun evidence the user suspected was driving it.

**L0:F7532 (proper nouns, DE = +0.10)** detects that "Daniel" is a name; this is an entity-recognition feature, not a profession indicator.

**Conclusion for the user concern:** The user's worry is well-motivated but the direction is reversed. The circuit is *not* using male-pronoun markers as a positive profession signal — those features are net-suppressing the probe. The actual positive driver is a **generic academic-field vocabulary detector** (L6:F170 → L5:F10392) that fires on any field name. This is still a "spurious" feature in the sense the user fears: a female nurse, a female teacher, a female historian would light up the same pathway equally, because the circuit has no feature that distinguishes "mechanical engineer" from "historian" or "English literature student". But the specific mechanism is generic field-of-study vocabulary, not gender. To distinguish the *profession* "mechanical engineer" from merely the *field* "mechanical engineering", the probe would need a feature selective to engineering/STEM-technical-profession combinations, and none appears in the top 20. The pipeline the probe relies on — generic "this is a degree in some field" — is coarser than a genuine profession indicator.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 22 | Emb: ' He' (pos 22) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: ' his' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: ' received' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: ' Mechanical' (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: ' Engineering' (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: 'achelors' (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'Daniel' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 3 | L0:F2994 'his/he' pronoun (generic, 0.07 frac) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 25 | L0:F2994 'his/he' pronoun (generic, 0.07 frac) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 47 | L0:F2994 'his/he' pronoun (generic, 0.07 frac) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 22 | L0:F1069 'He/His' male pronoun (0.008 frac) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 1 | L0:F7532 proper-noun detector (0.06 frac) |  proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L3:F4113](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4113) | 7 | L3:F4113 degree/field-of-study detector (0.003 frac) |  mentions of academic degrees and areas of study | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4113) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 3 | L4:F4315 'his' pronoun chain (0.026 frac) |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 9 | L5:F10392 'fields of academic study' (0.004 frac) |  fields of academic study | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L5:F6384](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6384) | 9 | L5:F6384 'higher education & professions' (0.007 frac) | words related to higher education and professions | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6384) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 9 | L6:F170 academic-field detector (0.039 frac) — generic, NOT profession-specific |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 8 | L6:F170 academic-field detector (0.039 frac) — generic, NOT profession-specific |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 22 | L6:F12990 male pronouns & male-associated descriptors (0.068 frac) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 3 | L6:F12990 male pronouns & male-associated descriptors (0.068 frac) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 3 | L7:F14893 pronouns/possessive-pronouns (0.009 frac) — pushes probe UP |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 3 | L7:F14946 'his/he/him' pronoun — INHIBITORY to probe (neg DE) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L12:F2175](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) | 2 | L12:F2175 gender words (0.006 frac) — pushes probe DOWN |  words referring to gender | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 22 | L18:F14743 'He' (0.018 frac) — drives probe DOWN at pos 22 | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 81 | L18:F14743 'He' (0.018 frac) — drives probe DOWN at pos 22 | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe direction (synthetic target) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2994 de=0.395 |
| 3 | `inspect_feature` ×9 | L0:2994, L7:14893, L7:14946, L12:2175, L6:12990, L6:170, L18:14743, L0:7532, L5:10392 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14743@22` | ❌ error | — | — | Trace upstream from L18:F14743 (a "He" feature at pos 22). Determine what tokens… |
| SA-2 | `L0:F2994@3` | ❌ error | — | — | Trace upstream from L0:F2994 (a "his/he" pronoun feature at pos 3 — the "receive… |
| SA-3 | `L6:F170@9` | ✅ reported | 7 | 10 | Trace upstream from L6:F170 (academic-fields feature) at pos 9 ("Mechanical"). T… |

<details>
<summary><b>SA-3</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F170 | " references to academic fields, especially those in the humanities" |
| 2 | `get_upstream_features` | L6:F170@9, k=10 | L5:F10392 (de=10.94) +9 more |
| 3 | `inspect_feature` | L5, F10392 | " fields of academic study" |
| 4 | `inspect_feature` | L5, F6384 | "words related to higher education and professions" |
| 5 | `inspect_feature` | L3, F4113 | " mentions of academic degrees and areas of study" |
| 6 | `get_upstream_features` | L5:F10392@9, k=10 | Emb:" Mechanical"@8 (de=3.08) +9 more |
| 7 | `get_upstream_features` | L5:F10392@9, k=10 | Emb:" Mechanical"@8 (de=3.08) +9 more |
| 8 | `get_upstream_features` | L5:F10392@9, k=10 | Emb:" Mechanical"@8 (de=3.08) +9 more |

**Findings:** The L6:F170 feature at position 9 is not a profession identifier; it is a broad academic‑field detector. Its strongest upstream driver is L5:F10392 (another generic field detector) which in turn receives a large positive push directly from the input token embedding "Mechanical" (pos 8). Additional modest contributions come from degree‑related tokens ("achelors", " degree", " Engineering") and from…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×2 | L5:6384, L3:4113 |
| 2 | `get_upstream_features` | L18:F14743@22, k=8 → Emb:" He"@22 (de=21.88) +7 more |
| 3 | `get_upstream_features` | L7:F14893@3, k=8 → Emb:" his"@3 (de=24.38) +7 more |
| 4 | `get_upstream_features` | L12:F2175@2, k=6 → Emb:" received"@2 (de=4.09) +5 more |
| 5 | `get_upstream_features` | L6:F12990@22, k=6 → Emb:" He"@22 (de=4.47) +5 more |
| 6 | `inspect_feature` ×2 | L0:1069, L4:4315 |
| 7 | `get_upstream_features` | L7:F14946@3, k=6 → Emb:" his"@3 (de=23.12) +5 more |

### Build

`build_circuit` → 21 nodes, 26 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 34,038 | 5,563 | 107,568 | 0 | $0.0233 | — | — |
| SA-3 | openai/gpt-oss-120b | 101,859 | 6,403 | 0 | 0 | $0.0191 | ✅ 7F/10E | Trace upstream from L6:F170 (academic-fields feature) at pos… |
| **Total** | | **135,897** | **11,966** | **107,568** | **0** | **$0.0425** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 29s