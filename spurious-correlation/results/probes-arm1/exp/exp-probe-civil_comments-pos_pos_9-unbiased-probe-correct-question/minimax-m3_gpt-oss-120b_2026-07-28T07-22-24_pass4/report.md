# Circuit Oracle Report
**Date:** 2026-07-28 07:22:24 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_9 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a small set of lexical and surface-semantic features (the words "white," "appears," "married," "Maybe," and "author/authors/books") acting on the input tokens themselves, with no abstract "identity group" or demographic-category features present in the attribution graph.

**Confidence:** 7

**Reasoning:** The attribution graph traces the probe's classification score back through shallow transcoder features (layers 0–6) directly to token-embedding nodes for content words. **No features encoding identity-group abstractions appear anywhere in the circuit.** Instead, the top positive contributors are:

- **Lexical/surface features anchored at specific input tokens**:
  - `L0:F3436` (label "mentions of the word 'white'", frac_nonzero 0.061, direct_effect +0.17 at pos 9) — fires on the literal token "white" with no racial-group abstraction; it appears in snippets about "white men", "white slave traders", and even "white dwarf" (astronomy) and "white paper" (legal). It is a literal string detector.
  - `L0:F9881` ("appear", +0.11 at pos 3) and `L0:F8444` ("to", −0.18 / −0.15 at pos 4 and 7) — these are generic function-word/string detectors.
  - `L0:F753` / `L0:F4408` / `L1:F384` / `L2:F14801` / `L6:F2851` — a chain of "author" / "authors" / "books/reading" features rooted at pos 2. `L6:F2851` (label "books and associated things such as authors and reading", frac_nonzero 0.014) is the deepest feature in the circuit; its top activating examples include AmRen book recommendations and Barnes & Noble, not demographic content.

- **Semantic features on the word "married"**:
  - `L2:F3399` and `L3:F494` are both labeled "words related to marriage" and fire on the literal "married" token (pos 6) with high specificity (frac_nonzero ≈ 0.004–0.018). Their top-activating examples are about wedding ceremonies, personal biographies, and divorce — not racial content. `L1:F1431` is a "fair / ends of justice" legal-document feature also anchored at "married" (pos 6).

- **Uncertainty features on "Maybe"**:
  - `L3:F10004` and `L3:F11152` (labels "words which mean or indicate uncertainty or possibility", frac_nonzero ≈ 0.004) fire on the hedging word "Maybe" at pos 17 — the model's epistemic-modality detectors, not demographic categories.

Critically, the **only direct path from any "identity-related" content word to the probe logit goes through `L0:F3436` on the literal token "white"** — and the feature's own top-activating examples confirm it activates equally on non-racial uses of "white" (astronomy, paper, paint). There is no abstract "Asian women," "interracial," or "self-hate" feature in the graph. The negative-contributing "to" features (`L0:F8444` at pos 4 and 7) and the canceling marriage features (`L3:F6262`, `L3:F8254`) also operate on ordinary surface tokens.

The probe therefore appears to be reading off **a small set of literal lexical cues** — "white," "author," "married," "Maybe," "appears" — rather than any abstracted "spurious identity-group" signal. The user's concern about spurious identity-group features driving the probe is not supported by this attribution graph: the demographic relevance of the classification derives entirely from the surface word "white" in a feature that is clearly lexical (suppressed tokens include generic function words; promoted tokens are noisy), with no higher-layer abstraction aggregating identity. If the probe is firing on demographic content here, it is doing so through a string-matching pathway on the word "white" itself, not through a learned identity category — though one caveat is that Gemma-2-2B's L0 "word-detector" features still encode the distributional associations of those words, so "white" as a literal token is a poor man's identity signal.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: author (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: married (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: white (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: Maybe (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: to (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: appears (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F4408](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4408) | 2 | Lexical: 'author' / 'authors' (pos 2) — promotes probe |  the word "authors" in academic papers or similar documents | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4408) |
| [L0:F753](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/753) | 2 | Lexical: 'author' / 'authors' (pos 2) — promotes probe | the word "author" and words related to selling and prices | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/753) |
| [L1:F384](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/384) | 2 | Lexical: 'author' / 'authors' (pos 2) — promotes probe |  the string "ash" or "pund" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/384) |
| [L2:F14801](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14801) | 2 | Lexical: 'author' / 'authors' (pos 2) — promotes probe | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14801) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 9 | Lexical: 'white' (pos 9) — promotes probe |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F9881](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9881) | 3 | Lexical: 'appear(s)' (pos 3) — promotes probe | the word "appear" and its variants | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9881) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 4 | Lexical: 'to' (pos 4, 7) — suppresses probe | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 7 | Lexical: 'to' (pos 4, 7) — suppresses probe | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L2:F3399](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3399) | 6 | Semantic: marriage/wedding (pos 6) — promotes probe |  words related to marriage | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3399) |
| [L3:F494](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/494) | 6 | Semantic: marriage/wedding (pos 6) — promotes probe |  text relating to marriage, birth, death, family and religion | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/494) |
| [L1:F1431](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1431) | 6 | Semantic: marriage/wedding (pos 6) — promotes probe |  instances of the word "fair" and the phrase "ends of justice" in legal documents | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1431) |
| [L3:F6262](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6262) | 6 | Semantic: marriage/wedding (pos 6, 7) — suppresses probe | mentions of marriage | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6262) |
| [L3:F8254](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8254) | 7 | Semantic: marriage/wedding (pos 6, 7) — suppresses probe |  words and phrases related to marriage and family relationships | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8254) |
| [L3:F10004](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10004) | 17 | Semantic: uncertainty/possibility 'Maybe' (pos 17) — promotes probe |  words which mean or indicate uncertainty or possibility | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10004) |
| [L3:F11152](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11152) | 17 | Semantic: uncertainty/possibility 'Maybe' (pos 17) — suppresses probe | words that indicate uncertainty or possibility | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11152) |
| [L6:F2851](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2851) | 2 | Semantic: books/authors/reading (pos 2) — promotes probe | books and associated things such as authors and reading | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2851) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe classification logit | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:753 de=-0.275 |
| 3 | `inspect_feature` ×14 | L0:753, L6:2851, L0:8444, L2:3399, L0:3436, L3:6262, L0:4408, L3:8254, L3:10004, L1:384, L3:11152, L3:494, L0:9881, L1:1431 |
| 4 | `get_upstream_features` | Emb:" author"@2 (de=11.06) +9 more |
| 5 | `get_upstream_features` | Emb:" married"@6 (de=29.00) +9 more |
| 6 | `get_upstream_features` | Emb:" married"@6 (de=37.75) +9 more |
| 7 | `get_upstream_features` | Emb:" Maybe"@17 (de=43.25) +7 more |
| 8 | `get_upstream_features` | Emb:" married"@6 (de=26.62) +7 more |
| 9 | `get_upstream_features` | Emb:" married"@6 (de=17.75) +7 more |
| 10 | `get_upstream_features` | Emb:" white"@9 (de=18.00) +7 more |
| 11 | `get_upstream_features` | Emb:" author"@2 (de=13.94) +7 more |
| 12 | `get_upstream_features` | Emb:" author"@2 (de=15.94) +7 more |
| 13 | `get_upstream_features` | Emb:" appears"@3 (de=13.44) +7 more |
| 14 | `get_upstream_features` | Emb:" married"@6 (de=19.00) +7 more |
| 15 | `get_upstream_features` | Emb:" author"@2 (de=18.38) +4 more |
| 16 | `get_upstream_features` | Emb:" author"@2 (de=30.12) +4 more |
| 17 | `get_upstream_features` | Emb:" author"@2 (de=11.06) +4 more |
| 18 | `get_upstream_features` | Emb:" to"@7 (de=41.75) +4 more |
| 19 | `get_upstream_features` | Emb:" Maybe"@17 (de=41.25) +7 more |
| 20 | `get_upstream_features` | Emb:" to"@4 (de=40.25) +4 more |
| 21 | `get_upstream_features` | ❌ Feature (layer=0, feature_idx=8444) not found at pos=2. This |
| 22 | `get_upstream_features` | Emb:" to"@4 (de=40.25) +4 more |
| 23 | `get_upstream_features` | Emb:" Maybe"@17 (de=43.25) +4 more |
| 24 | `get_upstream_features` | Emb:" married"@6 (de=19.00) +4 more |
| 25 | `get_upstream_features` | Emb:" white"@9 (de=18.00) +4 more |
| 26 | `get_upstream_features` | Emb:" author"@2 (de=30.12) +4 more |
| 27 | `get_upstream_features` | Emb:" married"@6 (de=26.62) +4 more |
| 28 | `get_upstream_features` | Emb:" author"@2 (de=24.75) +4 more |

### Build

`build_circuit` → 16 nodes, 17 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 40,816 | 5,895 | 221,355 | 0 | $0.0326 | — | — |
| **Total** | | **40,816** | **5,895** | **221,355** | **0** | **$0.0326** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 23s