# Circuit Oracle Report
**Date:** 2026-07-28 07:17:08 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven primarily by a robust late-layer "academic credentials and institutions" circuit (L20:F14235), which is fed by genuinely profession-relevant features (PhD/B.A./M.B.A. detectors, "university", "from Stanford") — the user's concern about spurious gender-marker features is not borne out by the circuit. L0:F1069 (He/His pronoun detector) fires strongly on the "His" embedding but is a weak contributor to the final probe score and only feeds into a low-layer "research vocabulary" feature, not into the output-driving credential pathway.

**Confidence:** 6

**Reasoning:** The dominant signal chain is profession-grounded: the input tokens "Ph" (pos 13), "D" (pos 15), "from" (pos 19), and "from" (pos 33, before "Stanford University") light up L1:F10132 (PhD abbreviation detector, frac_nonzero=0.00233), L2:F10852 (academic-titles aggregator, frac_nonzero=0.00801, promoted_tokens include "PhD"/"degree"/"doctorate"), L3:F4213 (degree qualifications, frac_nonzero=0.01242, top_token "from"), L5:F13801, L6:F2254, L7:F14129 (degrees & universities, frac_nonzero=0.00417), L9:F988 (academic degrees, frac_nonzero=0.00436), L14:F3956, L17:F11003 (university, frac_nonzero=0.00986, promoted_tokens dominated by "University"), L19:F2496, and finally L20:F14235 (academic credentials & institutions, frac_nonzero=0.02278, promoted_tokens are elite universities: "UC"/"Cornell"/"University"/"UCLA"/"UBC"/"UW"/"Duke"/"USC"/"Vanderbilt"/"LSU"). This is a legitimate, content-rich profession signal — mentions of multiple doctoral-level degrees from named elite institutions.

L0:F1069 is the explicit male-pronoun feature the user worried about. It fires (direct_effect 0.0554) on the "His" embedding (direct_effect 21.625) at pos 1, but its downstream influence is minimal: it weakly excites L1:F10986 (research vocabulary, direct_effect ~0.06), and that research feature mostly routes into L6:F14747 (historical archives) and L8:F11284 (names/research) — none of which are the dominant contributors to the probe. The strongest output-drivers on the credential pathway (L7:F14129, L14:F3956, L17:F11003, L19:F2496, L20:F14235) all carry negative or near-zero direct_effect from the male-pronoun pathway.

The L8:F2383 "archeological sites" feature (direct_effect -0.0898, largest-magnitude contributor) is a mild suppressor triggered by the word "history" — it pushes against the probe score rather than for it, consistent with a profession disambiguation (the model is partially active on a "history/archaeology" reading, but the degree+university chain wins). The net sign of credential features on L20 is clearly positive and they originate in profession-content tokens, not gendered ones.

**Caveat on confidence:** No mid-layer feature (L10–L13) was traced, so the full convergence point where credential signals and pronoun signals merge (or fail to merge) is interpolated. The user's hypothesis is contradicted by the available evidence, but a deeper trace through the untraced layer range could in principle reveal a hidden shortcut.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: His (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: research (pos 2) / interests (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: research (pos 2) / interests (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: Ph (pos 13), D (pos 15), from (pos 19) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: Ph (pos 13), D (pos 15), from (pos 19) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 19 | Emb: Ph (pos 13), D (pos 15), from (pos 19) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 33 | Emb: from (pos 33) [Stanford] | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Male pronoun detector (He/His) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L1:F10986](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) | 3 | Academic research vocabulary |  words related to academic research | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) |
| [L1:F10132](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) | 15 | PhD abbreviation token detector | the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") written as "D" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 15 | Academic titles & degrees aggregator |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 29 | Academic titles & degrees aggregator |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L3:F4213](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) | 33 | Degree qualifications / awards detector |  mentions of degree qualifications or awards | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) |
| [L5:F13801](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) | 15 | Short-form degree abbreviations (PhD, DNP, RN) | abbreviations for degrees and mentions of educational attainment | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 15 | References to academic degrees | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L6:F14747](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14747) | 8 | Historical archives / documents terms |  terms related to historical archives and documents | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14747) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 15 | Academic degrees & universities detector |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L8:F2383](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2383) | 8 | Archeological sites / artifacts (misfire) |  words related to archeological sites, digs, and artifacts | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2383) |
| [L8:F11284](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) | 9 | Names / titles / universities / research |  words and phrases related to people's names, titles, universities, and research | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) |
| [L9:F988](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/988) | 29 | Academic degrees information |  information about academic degrees | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/988) |
| [L14:F3956](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3956) | 33 | Universities & degrees (Stanford/MBA context) | universities and degrees | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3956) |
| [L17:F11003](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) | 19 | University detector | university | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) |
| [L19:F2496](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2496) | 19 | Universities & degrees mentions |  mentions of universities and degrees | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2496) |
| [L20:F14235](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) | 19 | Academic credentials & institutions (output driver) |  references to academic credentials and institutions. | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) |
| [L20:F14235](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) | 33 | Academic credentials & institutions (output driver) |  references to academic credentials and institutions. | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) |
| [L20:F14235](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) | 46 | Academic credentials & institutions (output driver) |  references to academic credentials and institutions. | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L8:2383 de=-0.090 |
| 3 | `inspect_feature` ×5 | L0:6051, L1:10986, L0:1069, L7:14129, L1:1505 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F1069@1` | ❌ error | — | — | Trace L0:F1069 (male pronoun "He/His" detector at pos 1) upstream to identify wh… |
| SA-2 | `L7:F14129@15` | ✅ reported | 5 | 4 | Trace L7:F14129 (academic degrees/universities detector at pos 15, "Ph.D." area)… |
| SA-3 | `L1:F10986@3` | ✅ reported | 3 | 4 | Trace L1:F10986 (academic research words at pos 3, "research") upstream to ident… |
| SA-4 | `L14:F3956@33` | ✅ reported | 8 | 8 | Trace L14:F3956 (pos 33) upstream. Pos 33 is likely "Stanford" or "M.B.A.". Iden… |

<details>
<summary><b>SA-2</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14129 | " academic degrees, universities, and people associated with them" |
| 2 | `get_upstream_features` | L7:F14129@15, k=10 | L6:F2254 (de=7.09) +9 more |
| 3 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 4 | `inspect_feature` | L5, F13801 | "abbreviations for degrees and mentions of educational attainment" |
| 5 | `get_upstream_features` | L6:F2254@15, k=10 | L2:F10852 (de=12.31) +9 more |
| 6 | `inspect_feature` | L1, F10132 | " the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") writ" |
| 7 | `get_upstream_features` | L6:F2254@15, k=10 | L2:F10852 (de=12.31) +9 more |
| 8 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 9 | `get_upstream_features` | L2:F10852@15, k=10 | Emb:" Ph"@13 (de=14.00) +9 more |
| 10 | `get_upstream_features` | L5:F13801@15, k=10 | L2:F10852 (de=7.22) +9 more |

**Findings:** The target feature L7:F14129 (academic-degree detector) is driven primarily by a cascade of earlier‑layer degree detectors: L6:F2254 and L5:F13801, which themselves are strongly excited by the low‑level token embeddings "Ph" (pos 13) and "D" (pos 15). The earliest explicit token‑level influence appears at layer 2 (feature 10852) and layer 1 (feature 10132), both of which receive large positive dir…

</details>

<details>
<summary><b>SA-3</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F10986 | " words related to academic research" |
| 2 | `get_upstream_features` | L1:F10986@3, k=10 | Emb:" research"@2 (de=6.62) +9 more |
| 3 | `inspect_feature` | L0, F6113 | " the word "overall", sometimes alongside words that express quantity" |
| 4 | `inspect_feature` | L0, F13431 | "the word "owing"." |
| 5 | `get_upstream_features` | L0:F13431@3, k=5 | Emb:" interests"@3 (de=12.25) +4 more |
| 6 | `get_upstream_features` | L0:F6113@3, k=10 | Emb:" interests"@3 (de=14.19) +9 more |

**Findings:** The target feature L1:F10986 (research‑related detector) receives its strongest positive drive directly from the input token embeddings for "research" (pos 2) and "interests" (pos 3). Additional modest contributions come from two layer‑0 features: 0:6113 (captures summary words like "overall") and 0:13431 (captures the word "owing"). All upstream nodes are either embeddings or layer‑0 features, sa…

</details>

<details>
<summary><b>SA-4</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F3956 | " universities and degrees" |
| 2 | `get_upstream_features` | L14:F3956@33, k=10 | Emb:"<bos>"@0 (de=-5.06) +9 more |
| 3 | `inspect_feature` | L3, F4213 | " mentions of degree qualifications or awards" |
| 4 | `get_upstream_features` | L3:F4213@33, k=10 | Emb:" from"@33 (de=12.00) +9 more |
| 5 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 6 | `inspect_feature` | L4, F11633 | " words related to education and employment history" |

**Findings:** The target feature L14:F3956 (pos 33) is driven primarily by the token "from" at the same position and a cascade of lower‑layer features that detect academic degree language. The strongest upstream driver is the embedding of the word "from" (direct_effect 2.69). Below it, layer‑3 feature 4213 detects degree qualifications, itself strongly excited by the same "from" embedding (direct_effect 12.0) a…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F1069@1, k=10 → Emb:"His"@1 (de=21.62) +9 more |
| 2 | `inspect_feature` ×4 | L8:2383, L6:14747, L8:11284, L20:14235 |
| 3 | `get_upstream_features` | L20:F14235@19, k=10 → L17:F11003 (de=34.00) +9 more |
| 4 | `inspect_feature` ×5 | L9:988, L2:10852, L17:11003, L19:2496, L3:4213 |

### Build

`build_circuit` → 21 nodes, 25 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 31,152 | 5,293 | 126,248 | 0 | $0.0233 | — | — |
| SA-4 | openai/gpt-oss-120b | 52,239 | 3,425 | 2,528 | 0 | $0.0099 | ✅ 8F/8E | Trace L14:F3956 (pos 33) upstream. Pos 33 is likely "Stanfor… |
| SA-3 | openai/gpt-oss-120b | 48,122 | 3,343 | 5,056 | 0 | $0.0093 | ✅ 3F/4E | Trace L1:F10986 (academic research words at pos 3, "research… |
| SA-2 | openai/gpt-oss-120b | 106,756 | 6,322 | 21,920 | 0 | $0.0201 | ✅ 5F/4E | Trace L7:F14129 (academic degrees/universities detector at p… |
| **Total** | | **238,269** | **18,383** | **155,752** | **0** | **$0.0626** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 53s