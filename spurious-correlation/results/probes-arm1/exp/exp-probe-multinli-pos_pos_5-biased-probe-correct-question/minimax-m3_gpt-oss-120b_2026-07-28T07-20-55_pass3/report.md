# Circuit Oracle Report
**Date:** 2026-07-28 07:20:55 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction probe is driven almost entirely by surface-level negation tokens ("not", "n't", "isn", "t") and the contrastive conjunctions built around them ("not only", "but"), not by any semantic comparison of premise vs. hypothesis content.

**Confidence:** 9

**Reasoning:** Tracing from the output probe backward, the strongest positive contributors are late-layer features that are pure negation detectors. L16:F15025 (direct_effect +0.32, pos 6) is labeled "the word 'not' combined with personal pronouns" and L16:F12358 (direct_effect +0.37, pos 28) is "the word 'not' followed within a few tokens by a form of the verb 'to be'" — these fire on the premise's "not only" and the hypothesis's "isn't" respectively. They are mid-layer aggregations (L13-L15) of yet earlier "not" tokens: L14:F2476 "negative polarity, sometimes in the context of politics or social issues", L13:F4368 the literal "not" feature, L15:F15779 "hedging language" — all firing on pos 6. Crucially, the probe's two largest positive contributions (L0:F6236 "t after isn'/doesn'" and L0:F6236 indirectly via L16:F12358 on the "t" of "isn't" at pos 28, plus L2:F5627 "instances of the phrase 'not only'" on pos 7) trace all the way down to raw token embeddings: `Emb: not (pos 6)`, `Emb: only (pos 7)`, and `Emb: t / isn / ' (pos 26-28)`. There is no evidence of any feature that compares premise meaning to hypothesis meaning. Instead, the L15 "but / contrasting" feature (L15:F12905, direct_effect −0.32 on pos 13) acts as a generic contrastive-conjunction detector, and the "said" speech-attribution features (L4:F15629) simply mark that the premise is a reported statement — neither of these encodes entailment relations. The user's concern is correct: the circuit's positive drive to the contradiction score comes from the *quantity and proximity* of negation tokens ("not", "n't", "isn't") and from the contrastive "not only … but" construction, not from any actual semantic contradiction detection. The "program" content words (L0:F14950, L1:F11907, L2:F8279, L2:F13565) actually contribute *negatively* to the probe (direct_effects −0.35, −0.32, −0.23), meaning shared vocabulary pushes the probe *away* from "contradiction" while bare negation pushes it *toward* "contradiction" — a classic spurious-correlation signature.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 6 | Early "not only / not / program" lexical detectors (L0) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 28 | Early "not only / not / program" lexical detectors (L0) | the letter "t" when it follows the word "isn'" or "doesn'" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L0:F1910](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1910) | 7 | Early "not only / not / program" lexical detectors (L0) |  the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1910) |
| [L0:F11907](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11907) | 5 | Early "not only / not / program" lexical detectors (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11907) |
| [L0:F14950](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14950) | 5 | Early "not only / not / program" lexical detectors (L0) |  instances of the word "program" and the word "step" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14950) |
| [L0:F15525](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15525) | 3 | Early "not only / not / program" lexical detectors (L0) |  places where something is being explained or reported | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15525) |
| [L0:F6131](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6131) | 3 | Early "not only / not / program" lexical detectors (L0) |  the word "trick", often within the context of telling or describing a trick | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6131) |
| [L2:F5627](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5627) | 7 | Mid-early "not only" / "program" bigram detectors (L1-L2) |  instances of the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5627) |
| [L2:F13565](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13565) | 5 | Mid-early "not only" / "program" bigram detectors (L1-L2) |  the word "program(me)s" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13565) |
| [L2:F8279](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8279) | 5 | Mid-early "not only" / "program" bigram detectors (L1-L2) |  the word "program" or the plural "programs", sometimes weakly activating on words related to changes of state | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8279) |
| [L1:F11907](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11907) | 5 | Mid-early "not only" / "program" bigram detectors (L1-L2) |  the word "program" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11907) |
| [L1:F805](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/805) | 7 | Mid-early "not only" / "program" bigram detectors (L1-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/805) |
| [L3:F6227](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) | 30 | Mid-early "not only" / "program" bigram detectors (L1-L2) |  sentence fragments and informal or ungrammatical language, often including abbreviations. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) |
| [L4:F15629](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15629) | 3 | "said" / speech-attribution / "explained" features (L4) |  speech attribution, such as the word "said" and phrases like "talking about" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15629) |
| [L4:F12337](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12337) | 3 | "said" / speech-attribution / "explained" features (L4) |  speech attribution, especially "said" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12337) |
| [L15:F12905](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) | 13 | Mid-layer "but" / contrastive-conjunction feature (L15) |  the word "but" along with surrounding words that indicate a contrasting or consequential relationship. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) |
| [L9:F12274](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12274) | 7 | Mid-layer "but" / contrastive-conjunction feature (L15) |  the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12274) |
| [L16:F15025](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15025) | 6 | Late "not + pronoun / be" features (L13-L16) |  usage of the word "not" combined with personal pronouns or related emotional or motivational language | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15025) |
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 28 | Late "not + pronoun / be" features (L13-L16) |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |
| [L13:F4368](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/4368) | 6 | Late "not + pronoun / be" features (L13-L16) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/4368) |
| [L14:F2476](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/2476) | 6 | Late "not + pronoun / be" features (L13-L16) | negative polarity, sometimes in the context of politics or social issues | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/2476) |
| [L15:F15779](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15779) | 6 | Late "not + pronoun / be" features (L13-L16) |  hedging language | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15779) |
| [L16:F9779](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/9779) | 30 | Late "not + pronoun / be" features (L13-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/9779) |
| [L15:F10071](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) | 28 | Late "not + pronoun / be" features (L13-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) |
| [L2:F7654](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7654) | 28 | Late "not + pronoun / be" features (L13-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7654) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:15629 de=0.672 |
| 3 | `inspect_feature` ×15 | L4:15629, L2:5627, L0:6236, L4:12337, L0:14950, L1:11907, L15:12905, L16:15025, L3:6227, L2:13565, L5:2329, L2:8279, L0:1910, L0:15525, L0:6131 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F5627@7` | ❌ error | — | — | Trace from L2:F5627 "not only" feature at pos 7. Find what tokens and early-laye… |
| SA-2 | `L0:F6236@28` | ❌ error | — | — | Trace from L0:F6236 "isn'+t" feature at pos 28 (the "t" in "isn't" in second sen… |
| SA-3 | `L16:F15025@6` | ❌ error | — | — | Trace from L16:F15025 "not + pronoun" feature at pos 6 (the "not" in "not only")… |
| SA-4 | `L4:F15629@3` | ❌ error | — | — | Trace from L4:F15629 "said" speech attribution feature at pos 3. Find what mid-l… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L2:F5627@7, k=15 → Emb:" only"@7 (de=21.25) +14 more |
| 2 | `get_upstream_features` | L0:F6236@28, k=15 → Emb:" isn"@26 (de=23.38) +14 more |
| 3 | `get_upstream_features` | L16:F15025@6, k=15 → Emb:" not"@6 (de=12.19) +14 more |
| 4 | `get_upstream_features` | L4:F15629@3, k=15 → Emb:" said"@3 (de=34.25) +14 more |
| 5 | `get_upstream_features` | L15:F12905@13, k=15 → Emb:" only"@7 (de=5.97) +14 more |
| 6 | `get_upstream_features` | L16:F12358@28, k=10 → Emb:"t"@28 (de=12.69) +9 more |
| 7 | `inspect_feature` ×4 | L13:4368, L14:2476, L15:15779, L16:12358 |
| 8 | `get_upstream_features` | L0:F4958@6, k=10 → Emb:" not"@6 (de=32.00) +9 more |
| 9 | `get_upstream_features` | L15:F12905@13, k=10 → Emb:" only"@7 (de=5.97) +9 more |
| 10 | `inspect_feature` ×2 | L0:4958, L9:12274 |

### Build

`build_circuit` → 8 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 53,264 | 4,492 | 203,806 | 0 | $0.0336 | — | — |
| **Total** | | **53,264** | **4,492** | **203,806** | **0** | **$0.0336** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 18s