# Circuit Oracle Report
**Date:** 2026-07-28 07:17:56 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_9 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction probe's classification score is driven by a combination of generic lexical-bag features (matching the words "recorded", "menu", "will", "provide", "how", "obtain", "list") and shallow structural cues (sentence-start at "A", low-frequency technical/scientific vocabulary), with no semantic understanding of the premise–hypothesis contradiction — the user's concern is confirmed.

**Confidence:** 8

**Reasoning:** The attribution graph is dominated by single-word lexical features at layers 0–4 (frac_nonzero mostly in the 0.001–0.03 range, very specific lexical detectors), not by any entity-recognition or semantic-relation circuit. Concretely:

- **Positive (pushing toward "contradiction")** contributions come from the "recorded" supernode (L1:F3691 "recording" in scientific docs +0.34; L2:F8776 finance/property +0.52; L2:F3059 verb "record" +0.20; L0:F7443 "record" +0.32), the " provide" supernode (L2:F7863 +0.16, L4:F7643 "helps/provide/results" +0.17), late-lexical triggers at "obtain"/"how"/"list" (L0:F5099 "obtain" +0.16, L0:F16046 question words +0.13, L0:F15480 +0.16, L4:F14235 "list" +0.17), and the sentence-start feature at "A" (L17:F451 +0.19, L8:F8406 "I"/"Exactly" +0.13 from <bos>). These features fire whenever the model sees the *word* "recorded", "provide", "obtain", "list", etc. — there is nothing in the circuit that ties the premise's "do not" negation to the hypothesis's "do" to recognize logical contradiction.

- **Negative (suppressing contradiction)** contributions come from " menu" (L0:F2108 –0.48, L1:F12253 –0.43, L2:F3648 –0.21, L3:F3573 –0.29, L4:F14061 –0.14), " will" (L0:F8046 –0.38, L2:F188 –0.21), and other single-word detectors — these are just lexical, not semantic.

- The "not" word (pos 17) and " information" (pos 20) only surface as sparse late technical-term embeddings (L10:F6670 +0.13) and never reach mid/late layers as proper negation detectors. The supposed "negation signal" the user suspected is *not* present as an organized circuit; instead, the model picks up on surface word co-occurrence statistics (a " menu will provide" or "how to obtain these lists" template). The probe direction appears to be reading the presence of specific content-bearing vocabulary, not computing the logical relation between premise and hypothesis — exactly the spurious-feature failure mode the user flagged.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L1:F3691](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3691) | 2 | Lexical features at position 2 (' recorded') — POSITIVE signal (pushing toward contradiction) |  the word "recording" in scientific or experimental documentation | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3691) |
| [L2:F8776](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8776) | 2 | Lexical features at position 2 (' recorded') — POSITIVE signal (pushing toward contradiction) |  words related to finance and property law | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8776) |
| [L2:F3059](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3059) | 2 | Lexical features at position 2 (' recorded') — POSITIVE signal (pushing toward contradiction) |  the verb "record" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3059) |
| [L0:F7443](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) | 2 | Lexical features at position 2 (' recorded') — POSITIVE signal (pushing toward contradiction) | the word "record" appearing in various contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) |
| [L0:F7404](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7404) | 2 | Lexical features at position 2 (' recorded') — POSITIVE signal (pushing toward contradiction) |  the word "faith", sometimes in association with related ideas like "links" or "opportunities" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7404) |
| [L0:F13280](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13280) | 2 | Lexical features at position 2 (' recorded') — POSITIVE signal (pushing toward contradiction) |  passages discussing real estate | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13280) |
| [L0:F9990](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9990) | 2 | Lexical features at position 2 (' recorded') — POSITIVE signal (pushing toward contradiction) |  the word "concert" and some words related to concerts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9990) |
| [L0:F12774](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12774) | 2 | Lexical features at position 2 (' recorded') — POSITIVE signal (pushing toward contradiction) | the word "correction" and words related to it. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12774) |
| [L1:F6817](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6817) | 2 | Lexical features at position 2 (' recorded') — POSITIVE signal (pushing toward contradiction) | the word "category" or "categories" regardless of the context they appear in | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6817) |
| [L1:F11317](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11317) | 2 | Lexical features at position 2 (' recorded') — POSITIVE signal (pushing toward contradiction) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11317) |
| [L0:F2108](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2108) | 3 | Lexical features at position 3 (' menu') — NEGATIVE signal (pushing away from contradiction) | the word "menu" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2108) |
| [L1:F12253](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12253) | 3 | Lexical features at position 3 (' menu') — NEGATIVE signal (pushing away from contradiction) |  the word 'menu' | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12253) |
| [L2:F3648](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3648) | 3 | Lexical features at position 3 (' menu') — NEGATIVE signal (pushing away from contradiction) | code snippets related to menus and restaurants | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3648) |
| [L3:F3573](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3573) | 3 | Lexical features at position 3 (' menu') — NEGATIVE signal (pushing away from contradiction) | the word "menu" often in conjunction with interface elements | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3573) |
| [L4:F7998](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7998) | 3 | Lexical features at position 3 (' menu') — NEGATIVE signal (pushing away from contradiction) |  words related to telecommunications and telephones | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7998) |
| [L4:F14061](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14061) | 3 | Lexical features at position 3 (' menu') — NEGATIVE signal (pushing away from contradiction) |  terms related to menus and data relations | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14061) |
| [L0:F5128](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5128) | 3 | Lexical features at position 3 (' menu') — NEGATIVE signal (pushing away from contradiction) |  the word "words" or words that are similar in meaning (word, Word, phrases, matrix) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5128) |
| [L0:F4523](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4523) | 3 | Lexical features at position 3 (' menu') — NEGATIVE signal (pushing away from contradiction) | the word "domestic" and words associated with globalism | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4523) |
| [L5:F14641](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14641) | 2 | Lexical features at position 3 (' menu') — NEGATIVE signal (pushing away from contradiction) |  words relating to recording audio and/or video | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14641) |
| [L6:F11757](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11757) | 2 | Lexical features at position 3 (' menu') — NEGATIVE signal (pushing away from contradiction) |  references to videos, particularly on YouTube | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11757) |
| [L6:F6132](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6132) | 2 | Lexical features at position 3 (' menu') — NEGATIVE signal (pushing away from contradiction) | mentions pertaining to surveillance and video technology | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6132) |
| [L0:F8046](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8046) | 4 | Lexical features at position 4 (' will') — NEGATIVE signal |  the word "will." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8046) |
| [L2:F188](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/188) | 4 | Lexical features at position 4 (' will') — NEGATIVE signal | the word "will" in various contexts, sometimes alongside words related to consequences or legal matters | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/188) |
| [L4:F7998](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7998) | 2 | Lexical features at position 4 (' will') — NEGATIVE signal |  words related to telecommunications and telephones | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7998) |
| [L2:F7863](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7863) | 5 | Lexical features at position 5 (' provide') — POSITIVE signal | the word "provide" in various forms. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7863) |
| [L4:F7643](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7643) | 5 | Lexical features at position 5 (' provide') — POSITIVE signal |  words related to providing assistance or describing results | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7643) |
| [L0:F16046](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16046) | 8 | Late-lexical features at positions 8-10 (how/obtain) — POSITIVE signal (late trigger) | question words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16046) |
| [L0:F15480](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15480) | 10 | Late-lexical features at positions 8-10 (how/obtain) — POSITIVE signal (late trigger) |  usages of the word "back" and similar words involved in processes | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15480) |
| [L0:F5099](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5099) | 10 | Late-lexical features at positions 8-10 (how/obtain) — POSITIVE signal (late trigger) | the word "obtain" and related words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5099) |
| [L4:F14235](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14235) | 12 | Late-lexical features at positions 8-10 (how/obtain) — POSITIVE signal (late trigger) |  the word "list" and words like "listed" and "alphabetically" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14235) |
| [L17:F451](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) | 1 | Sentence-start structural feature at position 1 ('A') — POSITIVE signal | start of sentences | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) |
| [L8:F8406](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) | 1 | Sentence-start structural feature at position 1 ('A') — POSITIVE signal | the first-person pronoun "I" and the word "Exactly" | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) |
| [L10:F6670](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) | 20 | Late-layer technical-term features — POSITIVE signal (sparse) | technical terms, especially within scientific or medical contexts | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token ' contradiction' is not one of the top-k next-token ca |
| 3 | `get_top_features` | 15 features; top: L2:8776 de=0.523 |
| 4 | `inspect_feature` ×15 | L2:8776, L0:2108, L1:12253, L0:8046, L1:3691, L0:7443, L3:3573, L0:6649, L0:7404, L4:7998, L2:3648, L2:188, L2:3059, L0:5128, L0:4523 |
| 5 | `get_top_features` | 40 features; top: L2:8776 de=0.523 |
| 6 | `inspect_feature` ×24 | L17:451, L2:11317, L4:7643, L0:13280, L0:9990, L0:15480, L5:14641, L2:7863, L6:11757, L1:6817, L1:5249, L0:9026, L1:10242, L0:3281, L0:3017, L4:14061, L0:12774, L6:6132, L0:5099, L8:8406, L0:16046, L10:6670, L4:14235, L0:14061 |
| 7 | `get_upstream_features` | L16:F10989 (de=-10.38) +9 more |
| 8 | `get_upstream_features` | Emb:" lists"@12 (de=16.62) +9 more |
| 9 | `get_upstream_features` | Emb:" recorded"@2 (de=19.50) +9 more |
| 10 | `get_upstream_features` | Emb:" recorded"@2 (de=24.75) +9 more |
| 11 | `get_upstream_features` | Emb:" recorded"@2 (de=22.50) +9 more |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L17:F451@1` | ✅ reported | 5 | 4 | Trace L17:F451 (start of sentences) upstream to identify what features drive the… |
| SA-2 | `L4:F14235@12` | ❌ error | — | — | Trace L4:F14235 (the word "list") upstream to see what drives it. |

<details>
<summary><b>SA-1</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L17, F451 | "start of sentences" |
| 2 | `get_upstream_features` | L17:F451@1, k=10 | L16:F10989 (de=-10.38) +9 more |
| 3 | `inspect_feature` | L15, F751 | "code snippets" |
| 4 | `inspect_feature` | L10, F14174 | "left curly brackets" |
| 5 | `inspect_feature` | L6, F14585 | " the words "the" and "it" at the beginning of sentences" |
| 6 | `get_upstream_features` | L6:F14585@1, k=10 | Emb:"A"@1 (de=9.88) +9 more |
| 7 | `get_upstream_features` | L15:F751@1, k=10 | L14:F15964 (de=22.62) +9 more |

**Findings:** Tracing from the start‑of‑sentence feature (L17:F451) reveals a cascade of positive excitatory drivers. The strongest upstream driver in the lower third of the model is a layer‑6 feature that responds to common sentence‑initial words ("the", "it"). This feature itself receives a large positive push from the raw embedding of the first input token "A". Mid‑level contributors include a code‑snippet d…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F14061@3, k=5 → Emb:" menu"@3 (de=16.25) +4 more |
| 2 | `get_upstream_features` | L5:F14641@2, k=5 → Emb:" recorded"@2 (de=13.75) +4 more |
| 3 | `get_upstream_features` | L6:F11757@2, k=5 → Emb:" recorded"@2 (de=18.00) +4 more |
| 4 | `get_upstream_features` | L6:F6132@2, k=5 → Emb:" recorded"@2 (de=9.06) +4 more |
| 5 | `get_upstream_features` | L4:F7998@3, k=5 → Emb:" menu"@3 (de=13.56) +4 more |
| 6 | `get_upstream_features` | L2:F7863@5, k=5 → Emb:" provide"@5 (de=24.38) +4 more |
| 7 | `get_upstream_features` | L4:F7643@5, k=5 → Emb:" provide"@5 (de=3.89) +4 more |
| 8 | `get_upstream_features` | L0:F15480@10, k=5 → Emb:" obtain"@10 (de=17.38) +4 more |
| 9 | `get_upstream_features` | L0:F16046@8, k=5 → Emb:" how"@8 (de=10.25) +4 more |
| 10 | `get_upstream_features` | L0:F5099@10, k=5 → Emb:" obtain"@10 (de=20.62) +4 more |
| 11 | `get_upstream_features` | L10:F6670@20, k=5 → Emb:" information"@20 (de=-4.62) +4 more |
| 12 | `get_upstream_features` | L8:F8406@1, k=5 → Emb:"<bos>"@0 (de=9.62) +4 more |
| 13 | `get_upstream_features` | L3:F3573@3, k=5 → Emb:" menu"@3 (de=21.38) +4 more |
| 14 | `get_upstream_features` | L2:F3648@3, k=5 → Emb:" menu"@3 (de=27.75) +4 more |
| 15 | `get_upstream_features` | L0:F14061@2, k=5 → Emb:" recorded"@2 (de=10.31) +4 more |
| 16 | `get_upstream_features` | L0:F13280@2, k=5 → Emb:" recorded"@2 (de=14.75) +4 more |
| 17 | `get_upstream_features` | L0:F7404@2, k=5 → Emb:" recorded"@2 (de=14.25) +4 more |
| 18 | `get_upstream_features` | L0:F12774@2, k=5 → Emb:" recorded"@2 (de=12.44) +4 more |
| 19 | `get_upstream_features` | L0:F9990@2, k=5 → Emb:" recorded"@2 (de=10.75) +4 more |
| 20 | `get_upstream_features` | L0:F2108@3, k=5 → Emb:" menu"@3 (de=25.75) +4 more |
| 21 | `get_upstream_features` | L0:F8046@4, k=5 → Emb:" will"@4 (de=36.00) +4 more |
| 22 | `get_upstream_features` | L1:F12253@3, k=5 → Emb:" menu"@3 (de=20.62) +4 more |
| 23 | `get_upstream_features` | L0:F4523@3, k=5 → Emb:" menu"@3 (de=11.69) +4 more |
| 24 | `get_upstream_features` | L0:F5128@3, k=5 → Emb:" menu"@3 (de=15.62) +4 more |
| 25 | `get_upstream_features` | L0:F7443@2, k=5 → Emb:" recorded"@2 (de=22.62) +4 more |
| 26 | `get_upstream_features` | L2:F7863@5, k=5 → Emb:" provide"@5 (de=24.38) +4 more |

### Build

`build_circuit` → 19 nodes, 18 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 112,581 | 7,275 | 333,639 | 0 | $0.0625 | — | — |
| SA-1 | openai/gpt-oss-120b | 69,973 | 4,569 | 0 | 0 | $0.0132 | ✅ 5F/4E | Trace L17:F451 (start of sentences) upstream to identify wha… |
| **Total** | | **182,554** | **11,844** | **333,639** | **0** | **$0.0758** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 36s