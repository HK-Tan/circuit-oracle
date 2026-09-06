# Circuit Oracle Report
**Date:** 2026-07-28 07:20:52 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_7 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction score is driven almost entirely by a stack of "negation-word" detector features (the literal token "not" plus the pattern "not + form of to be"), triggered by the surface form of "is not" in the second sentence, rather than by any semantic comparison between premise and hypothesis.

**Confidence:** 9

**Reasoning:** The late-layer top features feeding the probe are all negation detectors: L16:F12358 ("not" followed within a few tokens by a form of "to be," direct_effect 0.36), L16:F9779 ("negation words or contractions like won't/not/never," 0.24), L15:F10071 ("negations and equivocations," 0.15), and L13:F3295 ("is/are not … other uses of not," 0.19). All four of these are explicitly auto-interpreted as negation-token detectors, with frac_nonzero in the 0.01–0.03 range and top activating tokens consisting of the word "not" and its morphological relatives (▁not, ▁won't, ▁never, etc.) — i.e., they are *category-specific to negation*, not to the entities "abbey" or "steeple."

Tracing upstream to the embedding layer confirms this is a *spurious surface feature*. The L0:F4958 feature that fires on the literal token "not" carries direct_effect 0.185 toward the probe, and its biggest upstream driver is the raw embedding of "▁not" at position 29 (direct_effect 34.25) — the word "not" in "is not of great height." Similarly, L16:F9779 at position 23 is driven directly by the embedding of the token "lacks" (pos 23) and the surrounding "will not" context, not by any "steeple/abbey" content. The L14:F10408 feature, despite its misleading "sea/ocean" autointerp label, fires at position 14 (the word "sea" in the first sentence) and receives direct contribution from the "sea" embedding (22.88) plus the L13:F3295 negation aggregator — it is part of the negation-cue pathway, not an entity-recognition pathway for the actual contradiction (steeple vs. lack of steeple).

What is striking is what is *missing*. There is no feature in the top 20 driving the probe that encodes "steeple/steepled" or "abbey" or "height" semantics, no feature that compares the premise claim ("towering, steepled abbey") to the hypothesis denial ("lacks a steeple"), and no late-layer "contradiction-detector" feature. Instead, the probe picks up a vertical stack of features whose semantics reduce to "this text contains the word 'not' near a form of 'to be.'" The remaining positive contributions (L0:F3820 "the," L0:F2848 "of," L0:F11375 "is," L0:F5060 "That," L0:F9026 punctuation/numbers) are generic function-word detectors with frac_nonzero and label profiles indicating they fire on common lexical patterns regardless of meaning, and they have no downstream semantic fan-in.

This validates the user's concern. The contradiction probe is relying on a **spurious shortcut**: the surface presence of a "not + copula" construction in the second sentence is sufficient to trigger a high contradiction score, even though a correct semantic classification would require comparing whether the premise's "steepled" claim is denied by the hypothesis's "lacks a steeple / not of great height." The hypothesis is in fact *consistent* with the premise (both agree the abbey is not particularly tall/spired), but the probe — and the features that feed it — have no such comparison pathway. Any text with "is not" or "lacks" would receive a similar score from this circuit.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 29 | Late-layer negation pattern detectors (L15-16) — drive probe via negation cues |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |
| [L16:F9779](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/9779) | 23 | Late-layer negation pattern detectors (L15-16) — drive probe via negation cues | negation words or contractions like "won't", "not", "never" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/9779) |
| [L15:F10071](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) | 29 | Late-layer negation pattern detectors (L15-16) — drive probe via negation cues | negations and equivocations | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) |
| [L13:F3295](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) | 29 | Mid-layer negation aggregators (L13-14) | negations in the form of "is/are not" as well as other uses of "not" | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) |
| [L14:F10408](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10408) | 14 | Mid-layer negation aggregators (L13-14) |  geographical locations, especially related to bodies of water | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10408) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 29 | Low-layer 'not' token detector (L0) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 5 | Generic function-word detectors (L0) | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 4 | Generic function-word detectors (L0) | the word "of" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F5060](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5060) | 1 | Generic function-word detectors (L0) | mentions of dinner or breakfast | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5060) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 18 | Generic function-word detectors (L0) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 10 | Generic function-word detectors (L0) | technical documents or data, including numbers, units, and references to figures or tables. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L16:12358 de=0.359 |
| 3 | `inspect_feature` ×4 | L16:12358, L16:9779, L13:3295, L15:10071 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F12358@29` | ✅ reported | 3 | 15 | Trace L16:F12358 ("not" followed by "to be") upstream. Find the input token sour… |
| SA-2 | `L16:F9779@23` | ✅ reported | 6 | 7 | Trace L16:F9779 (negation words "won't/not/never") upstream. Find its input toke… |
| SA-3 | `L15:F10071@29` | ✅ reported | 5 | 9 | Trace L15:F10071 (negations and equivocations) upstream. Find the input token so… |

<details>
<summary><b>SA-1</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L16, F12358 | " the word "not" followed within a few tokens by a form of the verb "to" |
| 2 | `get_upstream_features` | L16:F12358@29, k=10 | Emb:" not"@29 (de=19.50) +9 more |
| 3 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 4 | `get_upstream_features` | L0:F4958@29, k=5 | Emb:" not"@29 (de=34.25) +4 more |
| 5 | `inspect_feature` | L13, F3295 | "negations in the form of "is/are not" as well as other uses of "not"" |

**Findings:** The target feature L16:12358, which detects a "not" followed by a form of "to be", receives its strongest positive influence directly from the raw input embedding of the token "not" at position 29 (direct_effect ~19.5) and via a low‑level detector L0:4958 that also fires on the token "not" (direct_effect ~6.84). Both routes originate from the exact word "not" in the phrase "is not of great height"…

</details>

<details>
<summary><b>SA-2</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L16, F9779 | "negation words or contractions like "won't", "not", "never"" |
| 2 | `get_upstream_features` | L16:F9779@23, k=10 | Emb:" will"@22 (de=7.31) +9 more |
| 3 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 4 | `get_upstream_features` | L0:F4958@23, k=5 | Emb:" not"@23 (de=33.50) +4 more |
| 5 | `inspect_feature` | L15, F3521 | "sentences containing words expressing negation or uncertainty in past " |
| 6 | `get_upstream_features` | L16:F9779@23, k=30 | Emb:" will"@22 (de=7.31) +29 more |
| 7 | `inspect_feature` | L4, F4492 | "negations in various languages" |
| 8 | `inspect_feature` | L2, F12694 | " the word "Canisius" and words that express possibility or a small pro" |
| 9 | `inspect_feature` | L13, F102 | " phrases containing "not" or negative connotations" |
| 10 | `get_upstream_features` | L4:F4492@23, k=5 | Emb:" not"@23 (de=18.50) +4 more |

**Findings:** The target feature L16:F9779 (negation detection) receives its strongest excitatory drive from raw token embeddings "not" (pos23) and "will" (pos22). Upstream, a layer‑0 feature (F4958) that directly detects the word "not" feeds into it, providing a low‑layer (≤8) source. Additional contextual contributors include mid‑layer features that aggregate negation cues (L15:F3521, L4:F4492, L13:F102) and …

</details>

<details>
<summary><b>SA-3</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L15, F10071 | "negations and equivocations" |
| 2 | `get_upstream_features` | L15:F10071@29, k=10 | Emb:" not"@29 (de=9.75) +9 more |
| 3 | `inspect_feature` | L13, F3295 | "negations in the form of "is/are not" as well as other uses of "not"" |
| 4 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 5 | `inspect_feature` | L14, F13077 | "negations." |
| 6 | `get_upstream_features` | L2:F12021@29, k=10 | Emb:" not"@29 (de=22.50) +9 more |
| 7 | `get_upstream_features` | L13:F3295@29, k=5 | Emb:" not"@29 (de=17.75) +4 more |
| 8 | `get_upstream_features` | L0:F4958@29, k=5 | Emb:" not"@29 (de=34.25) +4 more |
| 9 | `inspect_feature` | L2, F12021 | ""not" or negative terms, with some bonus for sports-related terms and " |
| 10 | `inspect_feature` | L3, F8011 | " a mix of words and code fragments from different languages" |
| 11 | `inspect_feature` | L14, F12021 | "negations and assertions, especially those related to experimental res" |
| 12 | `inspect_feature` | L14, F15790 | "negations." |

**Findings:** The primary upstream driver of L15:F10071 is the embedding for the token " not" at position 29 (direct_effect = 9.75). This token feeds directly into the high‑layer negation/equivocation feature, establishing the input source of the refusal‑related signal. Additional positive contributions come from adjacent token " is" and lower‑layer features that detect the word "not" (layer 0) and broader nega…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×2 | L14:10408, L13:3295 |
| 2 | `get_top_features` | token="", k=30 → 30 features; top: L16:12358 de=0.359 |
| 3 | `get_upstream_features` | L14:F10408@14, k=8 → Emb:" sea"@14 (de=22.88) +7 more |
| 4 | `get_upstream_features` | L0:F5060@1, k=8 → Emb:"That"@1 (de=11.88) +7 more |
| 5 | `get_upstream_features` | L0:F3820@5, k=8 → Emb:" the"@5 (de=34.25) +7 more |
| 6 | `get_upstream_features` | L0:F2848@4, k=8 → Emb:" of"@4 (de=35.25) +7 more |
| 7 | `get_upstream_features` | L0:F4958@29, k=8 → Emb:" not"@29 (de=34.25) +7 more |
| 8 | `inspect_feature` ×8 | L0:7710, L0:11375, L4:3349, L4:4492, L0:9026, L0:3820, L0:2848, L0:5060 |
| 9 | `get_upstream_features` | L0:F3820@5, k=5 → Emb:" the"@5 (de=34.25) +4 more |
| 10 | `get_upstream_features` | L0:F2848@4, k=5 → Emb:" of"@4 (de=35.25) +4 more |
| 11 | `get_upstream_features` | L0:F5060@1, k=5 → Emb:"That"@1 (de=11.88) +4 more |
| 12 | `get_upstream_features` | L0:F11375@18, k=5 → Emb:" is"@18 (de=32.50) +4 more |
| 13 | `get_upstream_features` | L0:F9026@10, k=5 → Emb:" abbey"@10 (de=37.50) +4 more |

### Build

`build_circuit` → 8 nodes, 9 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 41,064 | 6,754 | 210,144 | 0 | $0.0330 | — | — |
| SA-1 | openai/gpt-oss-120b | 39,271 | 3,989 | 2,528 | 0 | $0.0083 | ✅ 3F/15E | Trace L16:F12358 ("not" followed by "to be") upstream. Find … |
| SA-2 | openai/gpt-oss-120b | 114,306 | 5,946 | 5,856 | 0 | $0.0208 | ✅ 6F/7E | Trace L16:F9779 (negation words "won't/not/never") upstream.… |
| SA-3 | openai/gpt-oss-120b | 173,626 | 9,542 | 5,056 | 0 | $0.0318 | ✅ 5F/9E | Trace L15:F10071 (negations and equivocations) upstream. Fin… |
| **Total** | | **368,267** | **26,231** | **223,584** | **0** | **$0.0940** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 34s