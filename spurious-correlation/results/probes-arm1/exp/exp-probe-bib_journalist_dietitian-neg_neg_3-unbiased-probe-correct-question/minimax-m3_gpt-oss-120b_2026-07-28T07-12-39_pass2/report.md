# Circuit Oracle Report
**Date:** 2026-07-28 07:12:39 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score (likely targeting the profession "journalist") is driven almost entirely by spurious lexical and surface cues — especially the token "stories" at position 3 and the word "journalistic" at position 13 — rather than by any higher-level profession concept; the strongest negative contributions even come from a "too" word detector and an unrelated "binding"/"migration" detector that all happen to fire on the same "stories" embedding.

**Confidence:** 6

**Reasoning:** Tracing the attribution graph from the probe output back to the embeddings reveals a striking absence of any profession-specific late-layer features. The deep feature on the journalism side is **L14:F4420** ("words and phrases related to journalism and newspapers," promoted tokens include *journalist*, *reporter*, *journalism*) at pos 13 with direct_effect −0.128, but it is clearly driven by the literal word "journalistic" (embedding direct_effect +24.4) and its downstream **L4:F13253** (journalism & media, +25.6 from the same embedding) and **L6:F12712** (editors/publishers) — these are vocabulary detectors, not profession-reasoning circuits. The L14 feature's top activating examples include the *reporter* / *newspaper* tokens, confirming it is a journalism-vocabulary feature, but the probe is reading off its activation as a profession signal.

On the positive side of the probe (features pushing *toward* the classification), almost everything is anchored at the token "stories" (pos 3): the "story/narrative" features **L0:F5333** (+0.11), **L1:F14812** (+0.19), and **L1:F16233** ("tips"/"unit" — weakly narrative-adjacent, +0.13) all receive their dominant drive from the raw ` stories` embedding with direct_effects of +16–18. The most strongly positive "story" feature (L1:F14812) has frac_nonzero only 0.0095 and is a generic narrative-references detector — it is not a profession signal. The negative contributions from **L0:F14906** ("binding" word, −0.22) and **L0:F11261** ("migration" word, −0.16) are also pure lexical detectors at the same "stories" position (embedding direct_effects +12.7 and +12.9 respectively) — these features happen to be activated by some lexical similarity to "stories" but have nothing to do with journalism. The remaining features are similarly low-level: **L0:F1069** ("He" pronoun detector, −0.16), **L0:F4564** ("research"), **L1:F9201** ("represent"), **L1:F2344** ("country"), **L0:F2711** ("foreign"), **L0:F11603** ("too"), and punctuation/function-word detectors like **L0:F8061** ("in"), **L0:F6051** (periods), and **L0:F6962** (an "env" code-token that misfires on the "same" subword).

Critically, the user's concern is corroborated: **the circuit contains no feature that encodes the concept "journalist as a profession" or any role/agentive construct.** The strongest direct signal is the word "journalistic" itself (lexical), and the other strong signals come from surface tokens ("stories," "country," "He," "foreign," "research") whose relevance to the profession is purely co-occurrence-based. Features that *do* speak to profession semantics (L14:F4420 journalism-words) appear only at mid-to-late layers and are themselves triggered by the literal presence of the word "journalistic" rather than by contextual reasoning. The most negative feature (F14906 "binding", −0.22) and the "migration" feature (−0.16) are completely unrelated spurious lexical firings on the same "stories" embedding. The model is essentially using a bag-of-content-words heuristic at pos 3 ("stories") and pos 13 ("journalistic"), plus pronouns and function words, which is a textbook case of a probe picking up on lexical shortcuts rather than a genuine profession-indicating circuit. The graph is "flat" — all features are at layers 0–14, with no late-layer (>20) abstract profession features — which is itself evidence that the probe is reading off shallow lexical representations.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'He' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: ' researches' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: ' stories' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: ' same' (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: ' represents' (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 11 | Emb: ' the country' (pos 10-11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: ' in' (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: ' journalistic' (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: '.' (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 20 | Emb: ' foreign' (pos 20) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 27 | Emb: ' too' (pos 27) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | L0:F1069 — 'He' pronoun detector (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F4564](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) | 2 | L0:F4564 — 'research' word (pos 2) | the word "research." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) |
| [L0:F5333](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5333) | 3 | L0:F5333 — story / narrative (pos 3) | mentions of stories that are being told | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5333) |
| [L0:F14906](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14906) | 3 | L0:F14906 — 'binding' word (pos 3) |  the word "binding" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14906) |
| [L0:F11261](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11261) | 3 | L0:F11261 — 'migration' word (pos 3) |  the word "migration" and words related to it | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11261) |
| [L1:F9201](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9201) | 9 | L0:F9201 — 'represent' (pos 9) | the word "represent" and its variations in scientific contexts | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9201) |
| [L1:F2344](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2344) | 11 | L1:F2344 — 'country' word (pos 11) |  instances of the word "country" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2344) |
| [L0:F15423](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15423) | 11 | L0:F15423 — 'country' collector (pos 11) | The neuron seems to activate any time the word "country" is used, but also sometimes seems to activate for words related to groups of people such as "kids", "rest", or "total". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15423) |
| [L0:F8061](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) | 12 | L0:F8061 — preposition 'in' (pos 12) |  the preposition "in" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) |
| [L1:F14812](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) | 3 | L1:F14812 — story/narrative (pos 3) |  references to stories, chapters, and other narrative elements | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) |
| [L1:F16233](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/16233) | 3 | L1:F16233 — 'tips'/'unit' (pos 3) | the word "tips" and the word "unit" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/16233) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 13 | L4:F13253 — journalism & media (pos 13) |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L6:F12712](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) | 13 | L6:F12712 — editors/publishers (pos 13) |  titles of editors and publishers in scientific publications | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) |
| [L0:F2711](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2711) | 20 | L0:F2711 — 'foreign' word (pos 20) | the word "foreign." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2711) |
| [L0:F11603](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11603) | 27 | L0:F11603 — 'too' word (pos 27) |  the word "too" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11603) |
| [L0:F6962](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6962) | 7 | L0:F6962 — 'env' code-token (pos 7) | the token "env" possibly in code snippets | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6962) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 15 | L0:F6051 — periods/spaces/1 (pos 15) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 13 | L14:F4420 — journalism/newspaper words (pos 13) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:14906 de=-0.222 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L1:F14812@3` | ✅ reported | 4 | 4 | Trace the path from L1:F14812 (direct_effect +0.19) upstream through the circuit… |
| SA-2 | `L0:F11261@3` | ❌ error | — | — | Trace the path from L0:F11261 (direct_effect +0.16) upstream through the circuit… |
| SA-3 | `L1:F16233@3` | ✅ reported | 5 | 8 | Trace the path from L1:F16233 (direct_effect +0.13) upstream through the circuit… |
| SA-4 | `L0:F5333@3` | ❌ error | — | — | Trace the path from L0:F5333 (direct_effect +0.11) upstream through the circuit.… |
| SA-5 | `L0:F14906@3` | ❌ error | — | — | Trace the path from L0:F14906 (direct_effect -0.22, most negative) upstream thro… |
| SA-6 | `L0:F11603@27` | ❌ error | — | — | Trace the path from L0:F11603 (direct_effect -0.16) upstream through the circuit… |

<details>
<summary><b>SA-1</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F14812 | " references to stories, chapters, and other narrative elements" |
| 2 | `get_upstream_features` | L1:F14812@3, k=10 | Emb:" stories"@3 (de=18.62) +9 more |
| 3 | `inspect_feature` | L0, F479 | "the word "lift."" |
| 4 | `inspect_feature` | L0, F12991 | " references to figures and other documents" |
| 5 | `inspect_feature` | L0, F9438 | "Objective-C or C syntax related to pointers, object initialization and" |

**Findings:** L1:F14812 is a narrative‑reference detector (stories, chapters, etc.). Its dominant upstream influence is the raw token embedding for the word "stories" at position 3 (+18.6 direct effect). Additional, smaller positive contributions come from three layer‑0 features: a lexical "lift" detector, a figure‑citation detector, and a code‑syntax detector. All upstream nodes are either embeddings or layer‑…

</details>

<details>
<summary><b>SA-3</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F16233 | "the word "tips" and the word "unit"" |
| 2 | `get_upstream_features` | L1:F16233@3, k=10 | Emb:" stories"@3 (de=13.62) +9 more |
| 3 | `inspect_feature` | L0, F1301 | " mentions of cancer and related terms like tumors" |
| 4 | `inspect_feature` | L0, F8350 | "the word "ready"" |
| 5 | `inspect_feature` | L0, F11835 | "terms used in software code such as "assembly", "using", "namespace", " |
| 6 | `inspect_feature` | L0, F2189 | " technical writing related to scientific studies" |
| 7 | `get_upstream_features` | L0:F1301@3, k=10 | Emb:" stories"@3 (de=12.25) +9 more |
| 8 | `get_upstream_features` | L0:F1301@3, k=10 | Emb:" stories"@3 (de=12.25) +9 more |
| 9 | `get_upstream_features` | L0:F8350@3, k=10 | Emb:" stories"@3 (de=10.94) +9 more |

**Findings:** The L1:F16233 tip‑detecting feature receives its strongest excitatory drive from a low‑layer (layer 0) medical‑topic detector (F1301) that is itself strongly activated by the input token "stories" at position 3. This creates a concrete path: Embedding('stories', pos 3) → L0:F1301 → L1:F16233. Additional, weaker positive routes pass through other layer‑0 features that detect readiness, code termino…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F11261@3, k=10 → Emb:" stories"@3 (de=12.69) +9 more |
| 2 | `get_upstream_features` | L0:F5333@3, k=10 → Emb:" stories"@3 (de=16.38) +9 more |
| 3 | `inspect_feature` ×4 | L0:11261, L0:5333, L0:14906, L0:11603 |
| 4 | `get_upstream_features` | L0:F14906@3, k=10 → Emb:" stories"@3 (de=12.94) +9 more |
| 5 | `get_upstream_features` | L0:F11603@27, k=10 → Emb:" too"@27 (de=32.00) +9 more |
| 6 | `get_upstream_features` | L0:F1069@1, k=10 → Emb:"He"@1 (de=22.62) +9 more |
| 7 | `inspect_feature` ×15 | L0:8061, L14:4420, L0:2711, L0:6962, L0:6051, L0:15423, L4:13253, L1:9201, L0:1301, L0:4564, L1:2344, L6:12712, L1:1154, L1:14812, L1:16233 |
| 8 | `get_upstream_features` | L14:F4420@13, k=10 → Emb:" journalistic"@13 (de=24.38) +9 more |
| 9 | `get_upstream_features` | L0:F6962@7, k=5 → Emb:" same"@7 (de=14.81) +4 more |
| 10 | `get_upstream_features` | L0:F2711@20, k=5 → Emb:" foreign"@20 (de=25.62) +4 more |
| 11 | `get_upstream_features` | L0:F8061@12, k=5 → Emb:" in"@12 (de=39.75) +4 more |
| 12 | `get_upstream_features` | L1:F2344@11, k=10 → Emb:" country"@11 (de=22.75) +9 more |
| 13 | `get_upstream_features` | L0:F6051@15, k=5 → Emb:"."@15 (de=47.00) +4 more |
| 14 | `get_upstream_features` | L0:F15423@11, k=5 → Emb:" the"@10 (de=10.12) +4 more |
| 15 | `get_upstream_features` | L4:F13253@13, k=10 → Emb:" journalistic"@13 (de=25.62) +9 more |
| 16 | `get_upstream_features` | L6:F12712@13, k=10 → Emb:" journalistic"@13 (de=14.00) +9 more |
| 17 | `get_upstream_features` | L1:F9201@9, k=10 → Emb:" represents"@9 (de=23.50) +9 more |

### Build

`build_circuit` → 30 nodes, 36 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 61,900 | 7,201 | 102,908 | 0 | $0.0334 | — | — |
| SA-1 | openai/gpt-oss-120b | 50,818 | 4,550 | 7,680 | 0 | $0.0105 | ✅ 4F/4E | Trace the path from L1:F14812 (direct_effect +0.19) upstream… |
| SA-3 | openai/gpt-oss-120b | 84,247 | 5,873 | 17,696 | 0 | $0.0164 | ✅ 5F/8E | Trace the path from L1:F16233 (direct_effect +0.13) upstream… |
| **Total** | | **196,965** | **17,624** | **128,284** | **0** | **$0.0603** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 57s