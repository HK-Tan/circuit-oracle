# Circuit Oracle Report
**Date:** 2026-07-28 07:23:14 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "contradiction" classification is driven primarily by surface-level lexical/discourse signals — specifically discourse markers ("well", "yeah"), the contraction fragment "'t" (end of "haven't"), and the conjunction "because" — rather than by semantic content about the NCAA tournament, Louisville, or the Sweet 16.

**Confidence:** 7

**Reasoning:**

The attribution graph reveals that the probe's classification direction is dominated by shallow features:

1. **Strongest negative driver: L4:F12126 (pos 2, de=-0.65)** — labeled "expressions of agreement or acknowledgement, particularly 'well' and 'yeah'". This feature's top upstream inputs are the embeddings of " well" (de=14.6) and "yeah" (de=4.6), plus L0:F8352 ("the word 'well'") and L3:F4735 (multi-well plates — a false lexical match on the "well" token, not relevant). The circuit routes the *filler-word* "well" into the probe.

2. **Second strongest negative: L0:F6236 (pos 20, de=-0.46)** — labeled "the letter 't' when it follows the word 'isn'' or 'doesn''" (a contraction-ending detector). Its top inputs are embeddings for "t" (pos 20, de=17.9), " haven" (pos 18, de=16.6), and "'" (pos 19, de=12.1) — i.e., the "haven't" contraction, which the user explicitly flagged as a candidate spurious "negation word" signal. Promoted tokens confirm it pushes "not"/"Not"/"NOT".

3. **Strongest positive driver: L0:F16366 (pos 25, de=+0.29)** — labeled "the word 'because'", driven almost entirely by the "because" embedding (de=40.75). This is a conjunction/justification marker.

4. **L0:F8659 (pos 8, de=+0.29)** — labeled "the word 'foundation'" but firing on the "tournament" embedding (de=15.25); a generic word-identity feature.

5. **L4:F4847 (pos 2, de=+0.39)** — labeled "words/phrases often used in conversation, especially questions and answers" — another discourse-marker feature driven by " well" (de=8.06).

**Key finding confirming the user's concern:** The most negative-driving features (L4:F12126, L0:F6236) are **discourse/register markers** ("well", "yeah", "haven't") and a **contraction-ending 't'** that the LLM has learned to associate with negation. The "haven't" fragment is precisely the "negation word" signal the user flagged. The probe is not reading the semantic contradiction (Louisville being out, "I haven't missed a single game" — which is actually a *consistent* statement, not a contradiction). Instead, it keys on the **colloquial discourse register** (filler "well"/"yeah", contraction "haven't", casual "because") to fire its contradiction classification. The "tournament"/"double A" content words contribute only weakly (L0:F12862, F8083, F177 — "tournament"/"double" detectors) and are outvoted.

This validates the user's hypothesis: the probe relies on spurious lexical/discourse-marker features rather than understanding the actual semantic content of the prompt.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: ' well' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'yeah' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 20 | Emb: 't' (pos 20, end of 'haven't') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 18 | Emb: ' haven' (pos 18) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 19 | Emb: \"'\" (pos 19) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 25 | Emb: ' because' (pos 25) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: ' tournament' (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: ' double' (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 20 | Layer-0 lexical/word-identity features (discourse markers & content words) | the letter "t" when it follows the word "isn'" or "doesn'" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L0:F16366](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) | 25 | Layer-0 lexical/word-identity features (discourse markers & content words) |  the word "because" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) |
| [L0:F8659](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8659) | 8 | Layer-0 lexical/word-identity features (discourse markers & content words) | the word "foundation" in different contexts, including religious, legal, and abstract senses. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8659) |
| [L0:F8083](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8083) | 6 | Layer-0 lexical/word-identity features (discourse markers & content words) | the word "double" and surrounding words when numbers are also present | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8083) |
| [L0:F12862](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12862) | 8 | Layer-0 lexical/word-identity features (discourse markers & content words) |  the word "tournament" and related words such as "winning", but not always | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12862) |
| [L0:F177](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/177) | 6 | Layer-0 lexical/word-identity features (discourse markers & content words) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/177) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 3 | Layer-0 lexical/word-identity features (discourse markers & content words) | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F5112](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5112) | 1 | Layer-0 lexical/word-identity features (discourse markers & content words) |  the word "resolution", sometimes in the context of displaying images or patterns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5112) |
| [L0:F8352](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) | 2 | Layer-0 lexical/word-identity features (discourse markers & content words) |  the word "well" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) |
| [L1:F177](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) | 6 | Layer 1-3 mid-level features (discourse/composition) |  the word "double" and words that begin with "multi" or "doubly" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) |
| [L1:F6696](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6696) | 2 | Layer 1-3 mid-level features (discourse/composition) | the word "pool" in different contexts, but it also shows some activation for words associated with water-related activities and computing processes. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6696) |
| [L2:F1759](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1759) | 2 | Layer 1-3 mid-level features (discourse/composition) | occurrences of the word "know" with emphasis words or interjections nearby | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1759) |
| [L2:F7222](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7222) | 2 | Layer 1-3 mid-level features (discourse/composition) | the word "well" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7222) |
| [L3:F4735](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4735) | 2 | Layer 1-3 mid-level features (discourse/composition) |  references to multi-well plates and software used in scientific experiments | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4735) |
| [L3:F9770](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9770) | 7 | Layer 1-3 mid-level features (discourse/composition) |  technical and scientific writing about neuroscience and chemistry, possibly about calcium | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9770) |
| [L3:F12849](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12849) | 7 | Layer 1-3 mid-level features (discourse/composition) |  words or phrases that include the word "double", or contain a hyphen | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12849) |
| [L3:F13677](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13677) | 2 | Layer 1-3 mid-level features (discourse/composition) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13677) |
| [L3:F15027](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15027) | 2 | Layer 1-3 mid-level features (discourse/composition) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15027) |
| [L3:F2663](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2663) | 2 | Layer 1-3 mid-level features (discourse/composition) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2663) |
| [L3:F14561](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14561) | 2 | Layer 1-3 mid-level features (discourse/composition) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14561) |
| [L3:F14620](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14620) | 2 | Layer 1-3 mid-level features (discourse/composition) |  the word "well" and conjunctions like "and" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14620) |
| [L3:F9271](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9271) | 2 | Layer 1-3 mid-level features (discourse/composition) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9271) |
| [L3:F8423](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8423) | 2 | Layer 1-3 mid-level features (discourse/composition) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8423) |
| [L3:F5309](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5309) | 2 | Layer 1-3 mid-level features (discourse/composition) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5309) |
| [L4:F12126](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) | 2 | Layer 4 discourse/conversational features (key probe drivers) |  expressions of agreement or acknowledgement, particularly "well" and "yeah" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) |
| [L4:F4847](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) | 2 | Layer 4 discourse/conversational features (key probe drivers) |  words or short phrases often used in conversation, and especially questions and answers | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) |
| [L4:F5709](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) | 14 | Layer 4 discourse/conversational features (key probe drivers) | astronomy terms | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) |
| [L4:F3730](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3730) | 7 | Layer 4 discourse/conversational features (key probe drivers) |  text relating to lithium-ion batteries | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3730) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe classification direction (output) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'contradiction' is not one of the top-k next-token can |
| 3 | `get_top_features` | 15 features; top: L4:12126 de=-0.648 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F12126@2` | ❌ error | — | — | Trace the upstream path from L4:F12126 (pos 2, direct_effect=-0.65). Inspect eac… |
| SA-2 | `L0:F6236@20` | ❌ error | — | — | Trace the upstream path from L0:F6236 (pos 20, direct_effect=-0.457). This is a … |
| SA-3 | `L4:F4847@2` | ❌ error | — | — | Trace the upstream path from L4:F4847 (pos 2, direct_effect=+0.389). This has a … |
| SA-4 | `L0:F16366@25` | ❌ error | — | — | Trace the upstream path from L0:F16366 (pos 25, direct_effect=+0.293). This is a… |
| SA-5 | `L0:F8659@8` | ❌ error | — | — | Trace the upstream path from L0:F8659 (pos 8, direct_effect=+0.285). Layer-0 fea… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×9 | L0:8083, L3:9770, L4:5709, L1:177, L0:12862, L3:12849, L4:3730, L0:3820, L0:5112 |
| 2 | `get_upstream_features` | L4:F12126@2, k=10 → Emb:" well"@2 (de=14.62) +9 more |
| 3 | `get_upstream_features` | L0:F6236@20, k=10 → Emb:"t"@20 (de=17.88) +9 more |
| 4 | `get_upstream_features` | L4:F4847@2, k=10 → Emb:" well"@2 (de=8.06) +9 more |
| 5 | `get_upstream_features` | L0:F16366@25, k=10 → Emb:" because"@25 (de=40.75) +9 more |
| 6 | `get_upstream_features` | L0:F8659@8, k=10 → Emb:" tournament"@8 (de=15.25) +9 more |
| 7 | `inspect_feature` ×11 | L2:1759, L3:4735, L0:8352, L1:6696, L2:7222, L3:14620, L4:12126, L4:4847, L0:6236, L0:16366, L0:8659 |

### Build

`build_circuit` → 12 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 39,436 | 5,791 | 131,069 | 0 | $0.0266 | — | — |
| **Total** | | **39,436** | **5,791** | **131,069** | **0** | **$0.0266** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 9s