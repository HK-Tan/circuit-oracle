# Circuit Oracle Report
**Date:** 2026-07-28 07:20:25 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's profession classification (journalist) is driven primarily by genuine profession-indicating features (sparse journalism/media detectors at L4–L14 firing on the token "journalistic" at pos 13) and by a separate, smaller narrative/verb-feature signal — not by the male pronoun "He" itself, which is present but functions as incidental lexical input rather than a gender-based shortcut.

**Confidence:** 7

**Reasoning:**

The probe's top direct-effect features decompose into two clearly separable families: a **profession-genuine pathway** and a **lexical-incidental pathway**. The profession-genuine pathway is the dominant signal and traces cleanly to the token "journalistic" at pos 13:

- **L14:F4420** (label: "words and phrases related to journalism and newspapers", frac_nonzero=0.0165, promoted tokens: `journalists`, `journalist`, `reporter`, `editorial`, `reporters`) is the strongest mid-layer profession feature in the graph. It receives direct_effect ≈ 24.4 from the raw `journalistic` token embedding and direct_effect ≈ 6.0 from L4:F13253.
- **L4:F13253** (label: "things related to journalism and the media", frac_nonzero=0.00648, promoted: `Journalism`, `journalists`, `media`, `reporters`) is the earliest profession-specific detector, receiving direct_effect ≈ 25.6 from the `journalistic` embedding and a secondary boost from `stories` at pos 3.
- **L7:F9092** (label: "words and phrases associated with broadcast journalism", frac_nonzero=0.00946) adds a parallel broadcast-journalism pathway, also driven by the `journalistic` embedding (direct_effect 14.9) and by L4:F13253 (4.75).
- **L1:F1136** ("image credits and descriptions") and **L1:F5357** ("words related to written works") are weak upstream contributors (≈0.9 each) to L4:F13253 — not profession features themselves, just incidental co-occurrences.

The **narrative/verb pathway** is smaller and somewhat tangential to the profession label:
- **L1:F14812** ("references to stories, chapters, and other narrative elements", frac_nonzero=0.00947) at pos 3 receives direct_effect ≈ 18.6 from the `stories` embedding.
- **L0:F5333** ("mentions of stories that are being told", frac_nonzero=0.0035, very sparse) at pos 3 also receives direct_effect ≈ 16.4 from the `stories` embedding — this is a highly specific, low-frequency feature tied to the journalism reporting context.
- **L0:F11261** ("the word 'migration'") and **L1:F16233** ("the word 'tips' and 'unit'") appear as direct top-feature entries but their *promoted tokens* and frac_nonzero indicate they are stray lexical co-activations rather than semantic profession signals.

The **gender concern** is the user's worry, and the data partially supports it but largely exonerates the profession pathway. **L0:F1069** ("references to a male person, particularly 'He' or 'His'", frac_nonzero=0.0078) does appear in the top-feature list with direct_effect −0.1621 at pos 1, and is *purely* the "He" token detector (its top activations are all on the literal "He" token in male-protagonist contexts). Crucially, however:
1. Its direct_effect on the probe is **negative** (−0.1621), meaning the male-pronoun feature actually *pushes against* the probe's classification score here.
2. It sits in layer 0 and is not a propagation node for any higher-layer profession feature in this graph — the `journalistic` profession pathway is entirely self-contained at pos 13.
3. The other top-feature entries that one might worry about as "spurious" (**L0:F11603** = the word "too", **L0:F8061** = the preposition "in", **L0:F6051** = periods/spaces, **L0:F1301** = "cancer", **L0:F14906** = "binding", **L0:F6962** = "env") are all generic low-level lexical features with no semantic relationship to gender or profession — they are background co-activations from the decoder's projection, not gendered shortcuts.

The single **L1:F9201** ("the word 'represent' and its variations in scientific contexts", frac_nonzero=0.00924) at pos 9 is a profession-adjacent lexical cue (the prompt says "represents the country in journalistic circles") and is the cleanest verb-level correlate of the agentive reporting role.

**Summary of the user's concern:** The "He" gender feature (L0:F1069) is present in the top-feature list but acts as incidental lexical input with a *negative* direct effect on the probe — it is not a driver of the journalist classification. The classification is instead dominated by a coherent journalism-lexicon pathway (L4:F13253 → L7:F9092 → L14:F4420) anchored on the word "journalistic", which is a genuine profession indicator. The user's concern that the circuit uses gender markers is **not well supported** by this attribution graph; the profession signal is lexically grounded, and the male-pronoun feature behaves as background noise rather than a causal spur. The most plausible "spurious" elements are not gendered but rather generic word-form features ("too", "in", ".") that appear in nearly every token and reflect the residual stream's general content rather than a profession shortcut.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 13 | Journalism profession features (L4-L14) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 13 | Journalism profession features (L4-L14) | words and phrases associated with broadcast journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 13 | Journalism profession features (L4-L14) | things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L1:F14812](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) | 3 | Storytelling / narrative detectors (L0-L1) |  references to stories, chapters, and other narrative elements | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) |
| [L0:F5333](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5333) | 3 | Storytelling / narrative detectors (L0-L1) | mentions of stories that are being told | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5333) |
| [L0:F11261](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11261) | 3 | Storytelling / narrative detectors (L0-L1) |  the word "migration" and words related to it | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11261) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Male pronoun detector (L0) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L1:F9201](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9201) | 9 | "Represents" feature (L1) | the word "represent" and its variations in scientific contexts | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9201) |
| [L0:F2711](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2711) | 20 | "Foreign" feature (L0) | the word "foreign." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2711) |
| [L0:F11603](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11603) | 27 | "Too" feature (L0) |  the word "too" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11603) |
| [L0:F8061](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) | 12 | "In" preposition feature (L0) |  the preposition "in" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:14906 de=-0.222 |
| 3 | `inspect_feature` ×6 | L0:14906, L1:14812, L0:11603, L0:1069, L0:11261, L0:8061 |
| 4 | `get_upstream_features` | Emb:" stories"@3 (de=18.62) +9 more |
| 5 | `get_upstream_features` | Emb:"He"@1 (de=22.62) +9 more |
| 6 | `get_upstream_features` | Emb:" stories"@3 (de=12.69) +9 more |
| 7 | `get_upstream_features` | Emb:" too"@27 (de=32.00) +9 more |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@13` | ✅ reported | 4 | 7 | Trace upstream from L14:F4420 at position 13 (the token "journalistic"). This is… |
| SA-2 | `L1:F14812@3` | ✅ reported | 8 | 12 | Trace upstream from L1:F14812 at pos 3 ("stories"). This is a late-layer feature… |
| SA-3 | `L0:F1069@1` | ❌ error | — | — | Trace upstream from L0:F1069 at pos 1 ("He"). This is the male pronoun feature -… |
| SA-4 | `L4:F13253@13` | ✅ reported | 4 | 10 | Trace upstream from L4:F13253 at pos 13 (the token "journalistic"). Report all f… |

<details>
<summary><b>SA-1</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@13, k=10 | Emb:" journalistic"@13 (de=24.38) +9 more |
| 3 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 4 | `get_upstream_features` | L4:F13253@13, k=10 | Emb:" journalistic"@13 (de=25.62) +9 more |
| 5 | `inspect_feature` | L7, F9092 | " words and phrases associated with broadcast journalism" |
| 6 | `inspect_feature` | L1, F1136 | " image credits and descriptions" |
| 7 | `get_upstream_features` | L7:F9092@13, k=10 | Emb:" journalistic"@13 (de=14.88) +9 more |
| 8 | `get_upstream_features` | L1:F1136@13, k=10 | Emb:" journalistic"@13 (de=5.28) +9 more |

**Findings:** Tracing from L14:F4420 (token "journalistic") reveals it is driven primarily by the raw embedding of the word and by a low‑layer journalism detector (L4:F13253). L4:F13253 is a sparse early‑layer feature that activates on journalism and media terms and receives strong positive influence from the same embedding and a modest contribution from a layer‑1 feature. A parallel pathway passes through a br…

</details>

<details>
<summary><b>SA-2</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F14812 | " references to stories, chapters, and other narrative elements" |
| 2 | `get_upstream_features` | L1:F14812@3, k=10 | Emb:" stories"@3 (de=18.62) +9 more |
| 3 | `inspect_feature` | L0, F479 | "the word "lift."" |
| 4 | `inspect_feature` | L0, F12991 | " references to figures and other documents" |
| 5 | `get_upstream_features` | L0:F479@3, k=10 | Emb:" stories"@3 (de=10.69) +9 more |
| 6 | `inspect_feature` | L0, F9438 | "Objective-C or C syntax related to pointers, object initialization and" |
| 7 | `get_upstream_features` | L0:F479@3, k=10 | Emb:" stories"@3 (de=10.69) +9 more |
| 8 | `get_upstream_features` | L0:F12991@3, k=10 | Emb:" stories"@3 (de=10.38) +9 more |

**Findings:** The primary upstream driver for L1:F14812 (the narrative‑story detector) is the raw token embedding for the word "stories" (direct_effect ~18.6). This embedding also strongly excites several lower‑layer features (L0:F479, L0:F12991, L0:F9438) with direct effects around 10.3–10.7, all of which in turn feed a modest positive contribution to the target L1 feature. All traced paths reach layer 0 (≤8),…

</details>

<details>
<summary><b>SA-4</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 2 | `get_upstream_features` | L4:F13253@13, k=10 | Emb:" journalistic"@13 (de=25.62) +9 more |
| 3 | `get_upstream_features` | L1:F1136@13, k=10 | Emb:" journalistic"@13 (de=5.28) +9 more |
| 4 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 5 | `inspect_feature` | L1, F5357 | " words related to written works" |
| 6 | `inspect_feature` | L1, F1136 | " image credits and descriptions" |
| 7 | `get_upstream_features` | L1:F5357@13, k=10 | Emb:" journalistic"@13 (de=9.00) +9 more |

**Findings:** L4:F13253 is a high‑level journalism detector that receives its strongest boost directly from the input token "journalistic" (embedding) and a secondary boost from the surrounding token "stories". Its main upstream drivers are L1 features 1136 and 5357, which themselves are modestly excited by the same "journalistic" token and by a technical‑document feature at layer 0. The trace reaches layer 0 (…

</details>

### Re-dispatch (round 2): 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-5 | `L0:F1069@1` | ❌ error | — | — | Trace upstream from L0:F1069 (pos 1, "He" - male pronoun feature) to see if it h… |
| SA-6 | `L0:F5333@3` | ❌ error | — | — | Trace upstream from L0:F5333 (pos 3, "stories being told" detector at frac_nonze… |
| SA-7 | `L7:F9092@13` | ❌ error | — | — | Trace upstream from L7:F9092 at position 13 (broadcast journalism feature). Repo… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×4 | L6:12712, L1:16233, L0:5333, L0:6962 |
| 2 | `get_upstream_features` | L0:F1069@1, k=5 → Emb:"He"@1 (de=22.62) +4 more |
| 3 | `inspect_feature` ×4 | L0:2711, L0:1301, L0:6051, L1:9201 |
| 4 | `get_upstream_features` | L0:F5333@3, k=8 → Emb:" stories"@3 (de=16.38) +7 more |
| 5 | `get_upstream_features` | L0:F2711@20, k=8 → Emb:" foreign"@20 (de=25.62) +7 more |
| 6 | `get_upstream_features` | L1:F9201@9, k=8 → Emb:" represents"@9 (de=23.50) +7 more |
| 7 | `get_upstream_features` | L0:F5333@3, k=10 → Emb:" stories"@3 (de=16.38) +9 more |
| 8 | `get_upstream_features` | L7:F9092@13, k=8 → Emb:" journalistic"@13 (de=14.88) +7 more |
| 9 | `get_upstream_features` | L0:F1069@1, k=5 → Emb:"He"@1 (de=22.62) +4 more |
| 10 | `inspect_feature` | L14, F4420 → "words and phrases related to journalism and newspapers" |

### Build

`build_circuit` → 14 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 36,738 | 5,363 | 263,551 | 0 | $0.0333 | — | — |
| SA-2 | openai/gpt-oss-120b | 97,366 | 7,263 | 32 | 0 | $0.0190 | ✅ 8F/12E | Trace upstream from L1:F14812 at pos 3 ("stories"). This is … |
| SA-1 | openai/gpt-oss-120b | 96,226 | 5,576 | 96 | 0 | $0.0178 | ✅ 4F/7E | Trace upstream from L14:F4420 at position 13 (the token "jou… |
| SA-4 | openai/gpt-oss-120b | 76,911 | 7,526 | 2,544 | 0 | $0.0161 | ✅ 4F/10E | Trace upstream from L4:F13253 at pos 13 (the token "journali… |
| **Total** | | **307,241** | **25,728** | **266,223** | **0** | **$0.0861** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 6s