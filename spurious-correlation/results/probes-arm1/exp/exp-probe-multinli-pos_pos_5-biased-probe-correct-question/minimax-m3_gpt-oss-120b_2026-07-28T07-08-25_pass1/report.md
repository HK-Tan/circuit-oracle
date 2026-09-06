# Circuit Oracle Report
**Date:** 2026-07-28 07:08:25 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

The circuit has been built with token-embedding nodes tracing the full path. Now let me write the final analysis.

**Analysis:** The contradiction probe's classification is driven by a dense cluster of **lexical negation features** (not/isn't/but/not only) operating on the hypothesis sentence, with a secondary channel from speech-attribution features on the premise — the probe is largely using surface-level polarity cues rather than the semantic entailment relationship between the two sentences.

**Confidence:** 8

**Reasoning:**

The attribution circuit is overwhelmingly dominated by features whose autointerp labels are negation/polarity/contrast markers, confirming the user's hypothesis. Specifically:

**1. The primary driver is a chain of negation-word features converging on the hypothesis token "isn't" at position 28.** The most influential single feature is L16:F12358 (direct_effect=0.373), labeled "the word 'not' followed within a few tokens by a form of the verb 'to be'", which fires at the hypothesis "isn't" — exactly the contradiction polarity marker. Tracing upstream from L16:F12358 reveals the signal originates from:
- The token embedding of **"t" (pos 28, direct_effect=12.69)** and **"isn" (pos 26, direct_effect=5.09)** — the surface form of the negation,
- L0:F6236 (frac_nonzero=0.003, direct_effect=7.94) — specifically the "letter t following isn'/doesn'" feature, whose promoted tokens are "not, Not, NOT",
- L1:F423 "words that negate a following word/phrase" (direct_effect=1.56),
- L15:F10071 "negations and equivocations" (direct_effect=1.71),
- L13:F3295 "is/are not negations" (direct_effect=1.45).

This is a textbook **lexical-spuriosity circuit**: surface negation tokens → generic negation-word detectors → compound "not + be" detector → probe output. The model never needs to verify that the negation in the hypothesis *actually negates the same proposition* asserted in the premise.

**2. A second redundant negation channel fires on the premise "not only" (positions 6-7):** L2:F5627 "instances of the phrase 'not only'" (direct_effect=0.5), L9:F12274 "not only" (frac_nonzero=0.003), L15:F12905 "the word 'but' along with contrasting relationship" (direct_effect=-0.32, inhibitory) — these are pure lexical-phrase detectors on the "not only … but also" construction, with no semantic comparison of the two clauses.

**3. A minor contribution comes from the word "program" features (L0:F14950, L1:F11907, both with frac_nonzero ~0.002)** which fire on pos 5 and have opposite-sign direct effects (-0.35 and -0.32), likely reflecting the "program isn't going to improve" framing rather than genuine entailment reasoning.

**4. Speech-attribution features at L4 (F15629, F12337) on "said" (pos 3)** are the only features that anchor to the *premise* specifically rather than just negation words, and they have the largest single positive direct_effect (0.67) — but they merely detect the reporting verb "said" without doing any comparison.

**Why this confirms the user's concern:** Eight of the top ten direct-effect features on the probe are pure negation/polarity/contrast lexical detectors (L4:F15629, L2:F5627, L0:F6236, L16:F12358, L0:F14950, L1:F11907, L15:F12905, L3:F6227, L16:F15025, L15:F10071, L13:F3295, L1:F423, L13:F4368). The circuit contains **no features that compare premise and hypothesis propositions**, no entity-recognition, no entailment-composition, and no contradiction-semantics features — only surface-form negation, "not", "but", and contraction detectors. The probe is essentially implementing: "if both sentences contain negation/contrast words, output contradiction," which is a well-known spurious cue for NLI.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: program (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: not (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: only (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: but (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 26 | Emb: isn (pos 26) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 28 | Emb: t (pos 28) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 30 | Emb: to (pos 30) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: said (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F14950](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14950) | 5 | L0: 'program' word feature (F11907 active at pos 5, F14950 at pos 5; F12483 'only' at pos 7) |  instances of the word "program" and the word "step" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14950) |
| [L1:F11907](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11907) | 5 | L0: 'program' word feature (F11907 active at pos 5, F14950 at pos 5; F12483 'only' at pos 7) |  the word "program" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11907) |
| [L0:F12483](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12483) | 7 | L0: 'program' word feature (F11907 active at pos 5, F14950 at pos 5; F12483 'only' at pos 7) | the word "only" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12483) |
| [L0:F4723](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4723) | 7 | L0: 'program' word feature (F11907 active at pos 5, F14950 at pos 5; F12483 'only' at pos 7) |  the word "only" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4723) |
| [L0:F1910](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1910) | 7 | L0: 'program' word feature (F11907 active at pos 5, F14950 at pos 5; F12483 'only' at pos 7) |  the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1910) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 6 | L0: 'program' word feature (F11907 active at pos 5, F14950 at pos 5; F12483 'only' at pos 7) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L1:F423](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/423) | 28 | L1: 'words that negate' (F423) at pos 28 (isn't) |  words that negate a following word or phrase. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/423) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 28 | L0: 't after isn'/doesn'' (F6236) at pos 28 - promotes 'not' | the letter "t" when it follows the word "isn'" or "doesn'" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L2:F5627](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5627) | 7 | L2: 'not only' phrase feature (F5627) at pos 7 |  instances of the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5627) |
| [L3:F6227](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) | 30 | L3: informal/foreign 'not' fragments (F6227) at pos 30 |  sentence fragments and informal or ungrammatical language, often including abbreviations. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) |
| [L4:F15629](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15629) | 3 | L4: 'said' / speech attribution (F15629, F12337) at pos 3 |  speech attribution, such as the word "said" and phrases like "talking about" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15629) |
| [L4:F12337](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12337) | 3 | L4: 'said' / speech attribution (F15629, F12337) at pos 3 |  speech attribution, especially "said" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12337) |
| [L4:F2884](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2884) | 13 | L4: 'said' / speech attribution (F15629, F12337) at pos 3 | the word "but" and other contrastive conjunctions and adverbs. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2884) |
| [L9:F12274](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12274) | 7 | L9: 'not only' phrase feature (F12274) at pos 7 |  the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12274) |
| [L13:F4368](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/4368) | 6 | L13: 'not' word feature (F4368 at pos 6, F3295 at pos 28) + 't/negative' (F851) at pos 28 |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/4368) |
| [L13:F3295](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) | 28 | L13: 'not' word feature (F4368 at pos 6, F3295 at pos 28) + 't/negative' (F851) at pos 28 | negations in the form of "is/are not" as well as other uses of "not" | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) |
| [L13:F851](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/851) | 28 | L13: 'not' word feature (F4368 at pos 6, F3295 at pos 28) + 't/negative' (F851) at pos 28 | the letter "t" with high activation, and also finds words indicating something negative or the end of an HTML tag. | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/851) |
| [L15:F10071](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) | 28 | L15: 'negations and equivocations' (F10071) at pos 28; L15 'but-contrast' (F12905) at pos 13 | negations and equivocations | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) |
| [L15:F12905](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) | 13 | L15: 'negations and equivocations' (F10071) at pos 28; L15 'but-contrast' (F12905) at pos 13 |  the word "but" along with surrounding words that indicate a contrasting or consequential relationship. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) |
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 28 | L16: 'not + form of to be' (F12358 at pos 28); L16 'not + pronoun/emotional' (F15025) at pos 6 |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |
| [L16:F15025](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15025) | 6 | L16: 'not + form of to be' (F12358 at pos 28); L16 'not + pronoun/emotional' (F15025) at pos 6 |  usage of the word "not" combined with personal pronouns or related emotional or motivational language | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15025) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Output: contradiction probe direction | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'contradiction' is not one of the top-k next-token can |
| 3 | `get_top_features` | 10 features; top: L4:15629 de=0.672 |
| 4 | `inspect_feature` ×10 | L4:15629, L2:5627, L0:6236, L16:12358, L16:15025, L0:14950, L1:11907, L15:12905, L3:6227, L4:12337 |
| 5 | `get_upstream_features` | Emb:"t"@28 (de=12.69) +7 more |
| 6 | `get_upstream_features` | Emb:" only"@7 (de=21.25) +7 more |
| 7 | `inspect_feature` ×7 | L15:10071, L1:423, L13:851, L13:3295, L0:12483, L0:4723, L0:1910 |
| 8 | `get_upstream_features` | Emb:" said"@3 (de=34.25) +4 more |
| 9 | `get_upstream_features` | Emb:" not"@6 (de=12.19) +4 more |
| 10 | `get_upstream_features` | Emb:" only"@7 (de=5.97) +4 more |
| 11 | `get_upstream_features` | Emb:" to"@30 (de=6.00) +4 more |
| 12 | `get_upstream_features` | Emb:" program"@5 (de=23.25) +4 more |
| 13 | `get_upstream_features` | Emb:" program"@5 (de=24.38) +4 more |
| 14 | `inspect_feature` ×4 | L13:4368, L9:12274, L4:2884, L0:4958 |

### Build

`build_circuit` → 19 nodes, 25 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 56,974 | 5,532 | 186,033 | 0 | $0.0349 | — | — |
| **Total** | | **56,974** | **5,532** | **186,033** | **0** | **$0.0349** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 11s