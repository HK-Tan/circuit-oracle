# Circuit Oracle Report
**Date:** 2026-07-28 07:20:10 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_8 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction classification score is driven by a small set of early-layer entity-recognition and lexical-pattern features anchored on a handful of premise tokens ("Congress", "include", "began to"), with the strongest positive signal coming from L0:L2 features that fire on the proper noun "Congress" — not from any feature that encodes negation, contradiction semantics, or the relational structure between premise and hypothesis.

**Confidence:** 8

**Reasoning:**

**What the output represents.** The terminal node is a linear-probe classification score (the "synthetic probe label" returned by get_top_logits), not a next-token logit. The probe reads out of the model's residual stream and is being driven almost entirely by early-layer (L0–L4) features, which is consistent with a shallow linear probe rather than a deep semantic comparison.

**The positive (contradiction-promoting) features** are nearly all *entity-anchor* detectors:
- **L2:F2701** ("words related to the U.S. Congress", frac_nonzero 0.011, pos=2) — direct_effect +0.85, the single largest positive contributor. Its top activating examples are dominated by the token "Congress".
- **L3:F5753** ("the word 'includes' or 'containing'", frac_nonzero 0.002, pos=12) — direct_effect +0.53, fires on the hypothesis token "include" via its raw embedding (direct_effect 41 from Emb:" include").
- **L0:F6044** ("the word 'yield'", frac_nonzero 0.029, pos=2, +0.49), **L0:F15411** ("political bodies, figures, processes", frac_nonzero 0.008, pos=2, +0.49), and **L4:F59** ("'to' preceded by verb/start/begin", frac_nonzero 0.020, pos=11, +0.41) — all entity/lexical detectors. F59 traces cleanly to Emb:" began" (pos=10) and Emb:" to" (pos=11).
- **L3:F123** ("United States Congress", pos=2, +0.25) is another Congress anchor.

**The negative (contradiction-inhibiting) features** are also lexical, not semantic:
- **L0:F10401** ("genes and proteins", pos=2, -0.37) and **L0:F9557** ("'clean'", pos=2, -0.31) are generic L0 features that *happen to fire on the "Congress" token embedding* (Emb:" Congress" gives them direct_effect 13.25 and 11.125 respectively) but whose semantic labels are unrelated to either premise or hypothesis. This is a textbook spurious correlation: the probe direction is partially aligned with L0 features that co-occur with "Congress" in training data but encode completely unrelated concepts (genes, cleanliness).
- **L3:F8351** ("including and code language", pos=12, -0.35) and **L2:F6735** ("political parties/politicians", pos=2, -0.35) similarly fire on the input tokens "include" and "Congress" respectively but are not detecting contradiction.
- **L1:F4224** ("'registration'", pos=2, -0.27) and **L1:F5475** (pos=7, -0.24) misfire on the input but carry no contradiction-relevant signal.

**Addressing the user's concern.** The user worried the circuit uses "negation words" as a spurious shortcut. Inspection of every feature with |direct_effect| ≥ 0.22 shows that *no feature encodes negation, polarity, or contradiction semantics*. There is no "not", "no", "never", or any other negation detector in the top 15 — in fact, **F4224 ("registration") at the position of "no responsibility"** is the closest lexical neighbor and it suppresses the probe rather than promoting it. The features that do drive the score are:

1. Entity-recognition features for "Congress" (L2:F2701, L3:F123, L0:F15411), and
2. Lexical/function-word features for the *hypothesis*-side token "include" (L3:F5753, L0:F10783) and the phrase "began to" (L4:F59, L2:F11469).

**What the circuit actually says about the mechanism.** The probe is firing on a *topic-overlap mismatch* between premise and hypothesis — specifically, the presence of the entity "Congress" in the premise and the verb "include" in the hypothesis. This is a well-known shallow heuristic for NLI contradiction: the model/probe is detecting that the hypothesis ("began to include…") asserts an action that the premise implies is the opposite of what Congress actually does. But the circuit shows it is doing so through *lexical co-occurrence on specific tokens*, not through any genuine entailment/contradiction reasoning — and several of the contributing features (L0:F10401 "genes", L0:F9557 "clean", L1:F4224 "registration") are entirely spurious activations on the "Congress" and "include" embeddings that happen to be aligned with the probe direction.

The user's hypothesis is *partially* right (the circuit does use shallow lexical shortcuts rather than semantic content) but *wrong about the specific shortcut* — it is not negation words but rather **entity/keyword co-occurrence features** plus **incidental L0/L1 features that fire on those keywords** that drive the contradiction score. No feature in the top contributors encodes negation or contradiction polarity.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: ' Congress' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'The' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: ' include' (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: ' began' (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 11 | Emb: ' to' (pos 11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F6044](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) | 2 | L0 features firing on 'Congress' token (entity-anchor features) | the word "yield" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) |
| [L0:F15411](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15411) | 2 | L0 features firing on 'Congress' token (entity-anchor features) |  terms relating to political bodies, figures, and processes | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15411) |
| [L0:F10401](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10401) | 2 | L0 features firing on 'Congress' token (entity-anchor features) |  mentions of genes and proteins | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10401) |
| [L0:F9557](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9557) | 2 | L0 features firing on 'Congress' token (entity-anchor features) | the word "clean" and words/phrases associated with people | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9557) |
| [L0:F3204](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3204) | 2 | L0 features firing on 'Congress' token (entity-anchor features) |  proper nouns, especially including titles of works and organizations | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3204) |
| [L2:F2701](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) | 2 | L2: U.S. Congress lexical feature |  words related to the U.S. Congress | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) |
| [L2:F6735](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6735) | 2 | L2: political parties/politicians (inhibitory on this input) |  political parties and politicians | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6735) |
| [L1:F4224](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4224) | 2 | L1: 'registration' word (misfire on 'to'/context) |  the word "registration" and its variations | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4224) |
| [L1:F5475](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5475) | 7 | L1: 'registration' word (misfire on 'to'/context) | words or phrases related to scientific studies, user interfaces, or labels | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5475) |
| [L3:F5753](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5753) | 12 | L3: 'includes' word feature (promotes probe) |  the word "includes" or "containing". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5753) |
| [L3:F123](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/123) | 2 | L3: 'includes' word feature (promotes probe) |  mentions of the United States Congress | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/123) |
| [L3:F8351](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8351) | 12 | L3: include/code language (inhibits probe) |  words related to including and code language symbols | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8351) |
| [L4:F59](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/59) | 11 | L4: 'to' after start-verb (began to include) |  phrases with the word 'to' preceded by a verb or the word 'start' or 'begin'. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/59) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe classification score (contradiction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L2:2701 de=0.848 |
| 3 | `inspect_feature` ×14 | L2:2701, L3:5753, L0:6044, L0:15411, L4:59, L0:10401, L3:8351, L2:6735, L0:9557, L1:4224, L3:123, L1:5475, L0:3204, L0:10783 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F2701@2` | ❌ error | — | — | Trace the path upstream from L2:F2701 (Congress-related feature) to identify whi… |
| SA-2 | `L3:F5753@12` | ✅ reported | 3 | 6 | Trace upstream from L3:F5753 (the "includes" word feature at position 12). This … |
| SA-3 | `L0:F6044@2` | ❌ error | — | — | Trace upstream from L0:F6044 (the "yield" word feature at position 2) - it posit… |
| SA-4 | `L4:F59@11` | ✅ reported | 3 | 8 | Trace upstream from L4:F59 (the 'to' preceded by verb/start/begin feature at pos… |
| SA-5 | `L2:F2701@2` | ❌ error | — | — | Trace upstream from L2:F2701 (Congress words feature) at pos 2. Find which token… |
| SA-6 | `L0:F6044@2` | ❌ error | — | — | Trace upstream from L0:F6044 (yield word feature) at pos 2. Find the embedding t… |
| SA-7 | `L0:F15411@2` | ❌ error | — | — | Trace upstream from L0:F15411 (political bodies feature) at pos 2. Find the embe… |
| SA-8 | `L3:F8351@12` | ❌ error | — | — | Trace upstream from L3:F8351 (include/code language feature) at pos 12. It has N… |

<details>
<summary><b>SA-2</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F5753 | " the word "includes" or "containing"." |
| 2 | `get_upstream_features` | L3:F5753@12, k=10 | Emb:" include"@12 (de=41.00) +9 more |
| 3 | `inspect_feature` | L2, F13152 | "scientific and legal jargon, as well as present tense verbs" |
| 4 | `get_upstream_features` | L2:F13152@12, k=10 | Emb:" include"@12 (de=10.12) +9 more |
| 5 | `inspect_feature` | L1, F13759 | "the word 'to'" |
| 6 | `get_upstream_features` | L1:F13759@11, k=10 | Emb:" to"@11 (de=15.94) +9 more |

**Findings:** Tracing upstream from the L3 "includes" detector (F5753) quickly reaches the raw token embedding for the word 'include' (pos 12) with a large positive direct_effect (41.0). The signal then passes through a mid‑level jargon feature (L2:F13152) that is modestly excited by the same token, before reaching a low‑level preposition detector (L1:F13759) which itself is driven by the embedding for 'to' (po…

</details>

<details>
<summary><b>SA-4</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F59 | " phrases with the word 'to' preceded by a verb or the word 'start' or " |
| 2 | `get_upstream_features` | L4:F59@11, k=10 | Emb:" began"@10 (de=13.31) +9 more |
| 3 | `inspect_feature` | L3, F12596 | " actions or methods, sometimes preceeded by the preposition 'a' or 'to" |
| 4 | `inspect_feature` | L2, F11469 | " the word "to"" |
| 5 | `get_upstream_features` | L3:F12596@11, k=10 | Emb:" to"@11 (de=21.62) +9 more |
| 6 | `get_upstream_features` | L2:F11469@11, k=10 | Emb:" began"@10 (de=10.88) +9 more |

**Findings:** Tracing upstream from L4:F59 (pos 11) reveals that the dominant drivers are the input token embeddings 'began' (pos 10) and 'to' (pos 11). These feed directly into the target feature and also through two intermediate detectors: a layer‑3 action/infinitive feature (12596) and a layer‑2 token‑specific 'to' detector (11469). All upstream nodes lie within the lower third of the model (layers ≤8) and c…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L2:F2701@2, k=10 → Emb:" Congress"@2 (de=28.12) +9 more |
| 2 | `get_upstream_features` | L0:F6044@2, k=10 → Emb:" Congress"@2 (de=17.00) +9 more |
| 3 | `get_upstream_features` | L0:F15411@2, k=10 → Emb:" Congress"@2 (de=17.00) +9 more |
| 4 | `get_upstream_features` | L3:F8351@12, k=10 → Emb:" include"@12 (de=28.38) +9 more |
| 5 | `get_upstream_features` | L0:F10401@2, k=5 → Emb:" Congress"@2 (de=13.25) +4 more |
| 6 | `get_upstream_features` | L0:F9557@2, k=5 → Emb:" Congress"@2 (de=11.12) +4 more |

### Build

`build_circuit` → 13 nodes, 15 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 70,553 | 5,888 | 139,962 | 0 | $0.0366 | — | — |
| SA-4 | openai/gpt-oss-120b | 68,667 | 5,228 | 0 | 0 | $0.0134 | ✅ 3F/8E | Trace upstream from L4:F59 (the 'to' preceded by verb/start/… |
| SA-2 | openai/gpt-oss-120b | 48,625 | 4,354 | 2,528 | 0 | $0.0099 | ✅ 3F/6E | Trace upstream from L3:F5753 (the "includes" word feature at… |
| **Total** | | **187,845** | **15,470** | **142,490** | **0** | **$0.0600** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 49s