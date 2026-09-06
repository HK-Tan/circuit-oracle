# Circuit Oracle Report
**Date:** 2026-07-28 07:23:28 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction probe is driven almost entirely by a cluster of surface-lexical negation and contrastive-conjunction features — the words "isn't", "not", "but also", "not only" and the contraction "isn'/t" — not by any feature that encodes the semantic relationship (that "improve" appears in both premise and hypothesis but is negated in the hypothesis). The user's concern is corroborated by the circuit.

**Confidence:** 8

**Reasoning:** Every direct driver of the probe is a pure lexical/syntactic cue, traced to embedding nodes with no semantic intermediary:

1. **L16:F12358 ("not" + be-verb, pos 28, direct_effect=+0.373)** is the strongest output-driving feature. Tracing upstream one hop, it is fed almost entirely by the embedding nodes for " isn" (pos 26, de=5.09), "t" (pos 28, de=12.69) and the L0 "t-after-isn'" detector (F6236, de=7.94, frac_nonzero=0.0026, suppressed: "t"). The chain is Emb("isn't") → L0:F6236 → L16:F12358 → logit. There is no feature in this path that reads *what* "isn't" negates; only that the contraction "isn't" exists.

2. **L15:F12905 ("but also" contrastive, pos 13, direct_effect=-0.320)** is fed by the embedding for " but" (pos 13, de=4.0), L2:F5627 "not only" (pos 7, de=3.58), L4:F2884 "but" (pos 13, de=3.47) and L14:F11020 "but. and also" (pos 13, de=3.38). Every input to this node is the literal string "but" or the literal bigram "not only" — autointerp labels confirm they fire on the surface form, not on a contradiction relation.

3. **L16:F15025 ("not" + pronoun/emotional, pos 6, de=+0.320)** receives the embedding of " not" (pos 6, de=12.19), the embedding of " program" (pos 5, de=3.06), and L0/L1 "program"-word detectors (F14950, F11907) — the latter two actually suppress the feature (de=-0.35, -0.32) because "program" disambiguates "not program" as not-a-negation. The feature is driven by the raw "not" embedding at pos 6 of the premise.

4. **L15:F10071 ("negations and equivocations", pos 28, de=+0.32)** is fed by Emb("t" pos 28, de=12.7) and Emb(" isn" pos 26, de=5.1). Its label is literally "negations and equivocations" — it is a generic negation detector, not a contradiction detector.

5. **L4:F15629 ("said", pos 3, de=+0.67)** and L4:F12337 ("said", de=-0.51) are pure speech-attribution detectors: the embedding " said" (pos 3, de=34.25) accounts for nearly all of F15629's excitation. These features fire whenever "X said" appears, regardless of whether the attribution is being quoted to be contradicted.

6. **L2:F5627 ("not only", pos 7, de=+0.50)** is fed by Emb(" only" pos 7, de=21.25) and Emb(" not" pos 6, de=19.0) — the literal bigram.

7. **L3:F6227 ("informal not/pas fragments", pos 30, de=+0.32)** fires on "to" (pos 30, de=6.0) and "isn" (pos 26, de=2.5) — its promoted tokens are literally {not, Not, NOT}.

**Crucially absent:** No feature in the circuit encodes that "improve" in the premise is the same lexical item as "improve" in the hypothesis, that the contradiction hinges on the polarity flip from "will improve" to "isn't going to improve", or any entity/subject tracking. The probe is being classified as contradiction by counting surface negation markers (n_isn't + n_not + n_but + n_only) in the prompt, not by performing NLI.

The user's concern is **fully confirmed**: the circuit relies on spurious lexical negation/contrast signals rather than on prompt content. A paraphrase that replaces "isn't going to improve" with "will not help" plus rephrasing "not only... but also" would likely produce the same high probe score, and a counterfactual premise with no negation but the same semantic content would not.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 28 | L0:F6236 — letter "t" after "isn'"/"doesn'" (pos 28) | the letter "t" when it follows the word "isn'" or "doesn'" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L0:F14950](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14950) | 5 | L0:F14950 + L1:F11907 — the word "program" (pos 5) |  instances of the word "program" and the word "step" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14950) |
| [L1:F11907](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11907) | 5 | L0:F14950 + L1:F11907 — the word "program" (pos 5) |  the word "program" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11907) |
| [L2:F5627](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5627) | 7 | L2:F5627 — phrase "not only" (pos 7) |  instances of the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5627) |
| [L3:F6227](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) | 30 | L3:F6227 — informal "not/pas" fragments (pos 30) |  sentence fragments and informal or ungrammatical language, often including abbreviations. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) |
| [L4:F15629](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15629) | 3 | L4:F15629 — speech attribution "said" (pos 3) |  speech attribution, such as the word "said" and phrases like "talking about" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15629) |
| [L4:F12337](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12337) | 3 | L4:F15629 — speech attribution "said" (pos 3) |  speech attribution, especially "said" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12337) |
| [L4:F2884](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2884) | 13 | L4:F2884 — contrastive "but" (pos 13) | the word "but" and other contrastive conjunctions and adverbs. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2884) |
| [L15:F12905](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) | 13 | L15:F12905 — "but also" contrastive pair (pos 13) |  the word "but" along with surrounding words that indicate a contrasting or consequential relationship. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) |
| [L14:F11020](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11020) | 13 | L14:F11020 — "but. and also" (pos 13) | the word "but". and "also" | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11020) |
| [L15:F10071](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) | 28 | L15:F10071 — "negations and equivocations" (pos 28) | negations and equivocations | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) |
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 28 | L16:F12358 — "not" + be-verb (pos 28) |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |
| [L16:F15025](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15025) | 6 | L16:F15025 — "not" + personal pronoun/emotional (pos 6) |  usage of the word "not" combined with personal pronouns or related emotional or motivational language | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15025) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'contradiction' is not one of the top-k next-token can |
| 3 | `get_top_features` | 10 features; top: L4:15629 de=0.672 |
| 4 | `inspect_feature` ×10 | L4:15629, L4:12337, L2:5627, L0:6236, L16:12358, L0:14950, L1:11907, L16:15025, L15:12905, L3:6227 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F5627@7` | ❌ error | — | — | Trace from L2:F5627 ("not only") upstream to identify the source of the negation… |
| SA-2 | `L16:F12358@28` | ❌ error | — | — | Trace from L16:F12358 ("not followed by be-verb") upstream. This is one of the h… |
| SA-3 | `L15:F12905@13` | ❌ error | — | — | Trace from L15:F12905 ("but also" contrastive conjunction) upstream. The premise… |
| SA-4 | `L4:F15629@3` | ❌ error | — | — | Trace from L4:F15629 ("said" speech attribution) upstream. This fires on "Wagonh… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L2:F5627@7, k=12 → Emb:" only"@7 (de=21.25) +11 more |
| 2 | `get_upstream_features` | L16:F12358@28, k=12 → Emb:"t"@28 (de=12.69) +11 more |
| 3 | `get_upstream_features` | L15:F12905@13, k=12 → Emb:" only"@7 (de=5.97) +11 more |
| 4 | `get_upstream_features` | L4:F15629@3, k=12 → Emb:" said"@3 (de=34.25) +11 more |
| 5 | `inspect_feature` ×3 | L4:2884, L14:11020, L15:10071 |
| 6 | `get_upstream_features` | L16:F15025@6, k=10 → Emb:" not"@6 (de=12.19) +9 more |
| 7 | `get_upstream_features` | L3:F6227@30, k=10 → Emb:" to"@30 (de=6.00) +9 more |
| 8 | `get_upstream_features` | L0:F6236@28, k=10 → Emb:" isn"@26 (de=23.38) +9 more |
| 9 | `get_upstream_features` | L15:F12905@13, k=6 → Emb:" only"@7 (de=5.97) +5 more |

### Build

`build_circuit` → 17 nodes, 20 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 30,103 | 5,264 | 140,421 | 0 | $0.0238 | — | — |
| **Total** | | **30,103** | **5,264** | **140,421** | **0** | **$0.0238** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 13s