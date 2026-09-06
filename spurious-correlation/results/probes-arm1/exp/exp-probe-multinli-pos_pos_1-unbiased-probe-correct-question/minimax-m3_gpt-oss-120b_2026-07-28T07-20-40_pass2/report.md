# Circuit Oracle Report
**Date:** 2026-07-28 07:20:40 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** This is a probe attribution graph for a contradiction-classifier probe on a conspiracy-themed prompt; the circuit is overwhelmingly driven by surface-level lexical cues (the literal words "Conspiracy", "theorists", "MasterCard", "chip", "investing", and the function words "is" and "that") plus a few shallow concept features that aggregate those words, with no deeper semantic or reasoning path required.

**Confidence:** 6

**Reasoning:**

The circuit is dominated by **token-embedding → layer-0/1/2 lexical features → output** pathways. Almost every "semantic" supernode in the graph collapses to a single input word:

- **"Conspiracy/theorists" branch (the largest single source of positive drive):**
  - `Emb: Cons (pos 1)` feeds `cons_prefix` (L0:F16015, the "cons" prefix detector) and `Emb: piracy (pos 2)` feeds `conspiracy_mid` (L3:F9739, "words related to conspiracies", frac_nonzero 0.0076) with direct_effects of +8.75 and +7.625 from the raw token embeddings themselves. The "conspiracy" concept here is essentially the **dictionary entry of the word "Conspiracy"**, not a higher-order reasoning feature.
  - `conspiracy_late` (L8:F12761, "QAnon conspiracy theory", frac_nonzero 0.032) is anchored on the literal token `Emb: theorists` (pos 3) with direct_effect +4.56 from the embedding and +1.25 from L2:F16028. Its promoted-token list is generic ("preuve", "incest", "accuse") — it is essentially a **bag-of-conspiracy-keywords** feature, not a structured-argument feature.
  - "theory" (L1:F13684) and "enthusiast/hobbyist" (L4:F1602) fire on the *theorists* token — i.e. on the surface string "-ists" + "theor" — adding +0.144 and −0.135 to the probe.

- **"MasterCard/chip/investing" branch (entity recognition, content-relevant but shallow):**
  - `credit_card` (L7:F1062, "credit cards, loans, spending, gambling", frac_nonzero 0.003) is dominated by the embedding of `Card` (pos 6, +14) and `Master` (pos 5, −2.67), with L6:F10189 (+10) and L4:F4153 (+4.1) just refining the same token. It is **token-level entity recognition**, not a contradiction-reasoning feature.
  - `chip_concept` (L2:F16230, "semiconductor chips") is driven directly by `Emb: chip` (+27) and the L1 "chip" feature (F6066, +0.75) — i.e. the dictionary sense of the literal word "chip", not the contextual sense ("an identity/medical-record chip that the conspiracy theorists fear").
  - `invest_concept` (L1:F8696, "invest and its derivatives") is driven by `Emb: investing` (+21.9) — again a lexical match.

- **Function-word features (confirming the user concern):**
  - L0:F11375 ("is", frac_nonzero 0.01), L0:F3635 ("that", frac_nonzero 0.04), L0:F8444 ("to"), L0:F3937 ("scratch"), L0:F4287 ("marketing"), L0:F15958 ("tomorrow"), L0:F12377 (whitespace), L0:F4802 (whitespace/numbers) all appear with substantial direct_effects on the probe. These are **purely syntactic/format features** — most have frac_nonzero above the typical generic threshold and are exactly the kind of surface cue the user warned about. Several (notably "marketing", "tomorrow", "scratch", whitespace detectors) are completely content-irrelevant to contradiction detection yet still contribute.

**Direct answer to the user's concern:** The user's hypothesis is **partially confirmed**. The graph does rely heavily on:
1. The literal string "Conspiracy theorists" (treated as a dictionary entry plus a QAnon-keyword bag) rather than a parsed belief-claim that the model reasons about.
2. A heavy layer-0/1 lexical floor — generic function-word and format features ("is", "that", "to", whitespace, "marketing", "scratch", "tomorrow") are all directly driving the probe direction with non-trivial weights.

However, the circuit is **not** the textbook "negation word" artifact (no "not", "no", "never" negation features appear in the top 20). The actual spurious mechanism is broader and more interesting: it is **lexical overspecification at the embedding and layer-0 level** — the probe is being driven by *which words are present* (especially "Conspiracy", "theorists", "MasterCard", "chip", "investing", "is", "that") rather than by a contradiction-reasoning computation that compares premise and hypothesis. The high-frac_nonzero "is" and "that" features (0.01 and 0.04) are the clearest examples of generic, non-content-specific cues the model is using. So the user's diagnostic — "spurious surface signals rather than actual prompt content" — is right in spirit, but the specific artifact is *entity-name/keyword matching + function-word frequency* rather than negation detection.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe: contradiction classifier | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L8:F12761](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/12761) | 3 | Late-layer conspiracy/QAnon concept |  words associated with the QAnon conspiracy theory | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/12761) |
| [L3:F9739](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9739) | 2 | Mid-layer conspiracy concept |  words related to conspiracies | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9739) |
| [L1:F13684](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13684) | 3 | "theory" lexical detector |  the word "theory" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13684) |
| [L4:F1602](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1602) | 3 | "enthusiast" suffix / hobbyist |  words or phrases that indicate intense interest or enthusiasm, often associated with hobbies or preferences | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1602) |
| [L7:F1062](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1062) | 6 | Credit card / money / gambling concept |  words and phrases related to credit cards, loans, spending, gambling, and money in general. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1062) |
| [L7:F1062](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1062) | 11 | Credit card / money / gambling concept |  words and phrases related to credit cards, loans, spending, gambling, and money in general. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1062) |
| [L2:F16230](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16230) | 11 | Semiconductor chip concept |  mentions of semiconductor chips and devices | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16230) |
| [L1:F8696](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8696) | 8 | "invest" lexical detector |  the word "invest" and its derivatives | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8696) |
| [L0:F3635](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) | 12 | "that" functional word | the word "that" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 7 | "is" functional word |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F16015](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16015) | 1 | "cons" prefix detector | the prefix "cons" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16015) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 24 | Misc function/format features (to, scratch, marketing, theory-token, etc.) — generic, low semantic content | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F3937](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3937) | 11 | Misc function/format features (to, scratch, marketing, theory-token, etc.) — generic, low semantic content |  the phrase "from scratch", sometimes activating on words nearby | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3937) |
| [L0:F4287](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4287) | 1 | Misc function/format features (to, scratch, marketing, theory-token, etc.) — generic, low semantic content |  words or phrases that relate to marketing or advertising | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4287) |
| [L0:F12377](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12377) | 4 | Misc function/format features (to, scratch, marketing, theory-token, etc.) — generic, low semantic content |  large gaps of whitespace | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12377) |
| [L0:F15958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15958) | 3 | Misc function/format features (to, scratch, marketing, theory-token, etc.) — generic, low semantic content |  the word "tomorrow" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15958) |
| [L0:F4802](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4802) | 4 | Misc function/format features (to, scratch, marketing, theory-token, etc.) — generic, low semantic content |  large blocks of whitespace and numbers | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4802) |
| [L1:F6066](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6066) | 11 | Layer-1 "chip" lexical feature | the word 'chip', possibly in the context of hardware | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6066) |
| [L0:F1506](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1506) | 11 | "circuit" / hardware co-occurrence word | the word "circuit" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1506) |
| [L0:F351](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/351) | 11 | "circuit" / hardware co-occurrence word | the word "expert" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/351) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L3:9739 de=-0.348 |
| 3 | `inspect_feature` ×16 | L3:9739, L2:16230, L7:1062, L0:3635, L1:13684, L0:16015, L4:1602, L8:12761, L0:15958, L0:11375, L1:8696, L0:4802, L0:8444, L0:3937, L0:12377, L0:4287 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L3:F9739@2` | ✅ reported | 5 | 8 | Trace L3:F9739 ("words related to conspiracies") upstream to find what input tok… |
| SA-2 | `L7:F1062@6` | ❌ error | — | — | Trace L7:F1062 ("credit cards, money, gambling") upstream. This fires at positio… |
| SA-3 | `L2:F16230@11` | ✅ reported | 5 | 4 | Trace L2:F16230 ("semiconductor chips") upstream. Fires at pos 11 (likely "chip"… |
| SA-4 | `L8:F12761@3` | ❌ error | — | — | Trace L8:F12761 ("QAnon conspiracy theory words") upstream. This fires at pos 3 … |

<details>
<summary><b>SA-1</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F9739 | " words related to conspiracies" |
| 2 | `get_upstream_features` | L3:F9739@2, k=10 | Emb:"Cons"@1 (de=8.75) +9 more |
| 3 | `inspect_feature` | L2, F1741 | "fragments of words ending in "ction", "notes," or "ual."" |
| 4 | `inspect_feature` | L2, F16241 | " partial strings of the word "constructor" or words ending in "dering"" |
| 5 | `inspect_feature` | L2, F11313 | "words containing the "cent" or "consu" substrings" |
| 6 | `get_upstream_features` | L2:F16241@2, k=10 | Emb:"Cons"@1 (de=17.25) +9 more |
| 7 | `get_upstream_features` | L0:F2115@2, k=10 | Emb:"piracy"@2 (de=12.88) +9 more |
| 8 | `inspect_feature` | L0, F2115 | " data reported as a percentage inside brackets, especially in a labora" |
| 9 | `get_upstream_features` | L2:F1741@2, k=10 | Emb:"Cons"@1 (de=22.88) +9 more |
| 10 | `get_upstream_features` | L2:F1741@2, k=10 | Emb:"Cons"@1 (de=22.88) +9 more |
| 11 | `inspect_feature` | L0, F16015 | "the prefix "cons"" |
| 12 | `inspect_feature` | L0, F800 | "code-related terms and names of programming languages, especially rela" |
| 13 | `get_upstream_features` | L0:F16015@1, k=10 | Emb:"Cons"@1 (de=21.12) +9 more |

**Findings:** The conspiracy feature (L3:F9739) receives strong lexical cues from the input embeddings of the tokens "Cons" (prefix) and "piracy" (suffix), which together form the word "Conspiracy". Upstream sub‑word detectors (L2:F1741, L2:F16241) and the prefix detector (L0:F16015) provide additional positive influence, indicating the signal is primarily surface/lexical rather than content‑driven. No deeper s…

</details>

<details>
<summary><b>SA-3</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F16230 | " mentions of semiconductor chips and devices" |
| 2 | `get_upstream_features` | L2:F16230@11, k=10 | Emb:" chip"@11 (de=27.00) +9 more |
| 3 | `inspect_feature` | L1, F6066 | " the word 'chip', possibly in the context of hardware" |
| 4 | `inspect_feature` | L0, F351 | " the word "expert"" |
| 5 | `get_upstream_features` | L1:F6066@11, k=10 | Emb:" chip"@11 (de=21.38) +9 more |
| 6 | `inspect_feature` | L0, F3937 | " the phrase "from scratch", sometimes activating on words nearby" |
| 7 | `get_upstream_features` | L0:F3937@11, k=10 | Emb:" chip"@11 (de=12.75) +9 more |
| 8 | `inspect_feature` | L0, F1506 | " the word "circuit"" |
| 9 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |

**Findings:** The L2 feature for semiconductor chips (F16230) is driven primarily by the raw input token embedding for " chip" (direct_effect 27.0, not shown as a feature edge). Upstream low-layer detectors contribute positively: a layer‑1 chip detector (F6066) and several layer‑0 technical-word detectors (expert, circuit, from‑scratch) each give modest excitatory influence, all residing in layers ≤8, satisfyin…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L8:F12761@3, k=10 → Emb:" theorists"@3 (de=4.56) +9 more |
| 2 | `get_upstream_features` | L4:F1602@3, k=10 → Emb:" theorists"@3 (de=3.23) +9 more |
| 3 | `get_upstream_features` | L1:F13684@3, k=10 → Emb:" theorists"@3 (de=10.12) +9 more |
| 4 | `get_upstream_features` | L0:F11375@7, k=10 → Emb:" is"@7 (de=31.38) +9 more |
| 5 | `get_upstream_features` | L7:F1062@6, k=10 → Emb:"Card"@6 (de=14.00) +9 more |
| 6 | `get_upstream_features` | L1:F8696@8, k=10 → Emb:" investing"@8 (de=21.88) +9 more |
| 7 | `get_upstream_features` | L0:F3635@12, k=10 → Emb:" that"@12 (de=41.00) +9 more |
| 8 | `get_upstream_features` | L2:F16230@11, k=10 → Emb:" chip"@11 (de=27.00) +9 more |

### Build

`build_circuit` → 22 nodes, 25 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 53,407 | 5,988 | 158,544 | 0 | $0.0327 | — | — |
| SA-1 | openai/gpt-oss-120b | 132,539 | 6,358 | 38,992 | 0 | $0.0243 | ✅ 5F/8E | Trace L3:F9739 ("words related to conspiracies") upstream to… |
| SA-3 | openai/gpt-oss-120b | 115,224 | 6,623 | 2,528 | 0 | $0.0213 | ✅ 5F/4E | Trace L2:F16230 ("semiconductor chips") upstream. Fires at p… |
| **Total** | | **301,170** | **18,969** | **200,064** | **0** | **$0.0783** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 19s