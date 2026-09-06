# Circuit Oracle Report
**Date:** 2026-07-28 07:22:38 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction probe is driven by a constellation of purely lexical/syntactic features — negation markers ("isn't", "not", "only"), contrastive conjunctions ("but"), and speech attribution ("said") — with the single highest-magnitude positive driver being the token embedding for "isn't" (L0:F6236, direct_effect +0.48; L16:F12358 direct_effect +0.37; L15:F10071, L13:F4368 all "not" detectors), rather than any feature that encodes the semantic relationship between the premise and the hypothesis.

**Confidence:** 8

**Reasoning:** The circuit shows a striking absence of features that compare premise to hypothesis or detect entailment/contradiction as a semantic relation. Instead, every late-layer feature that pushes the probe score positive is a negation/contrast/attribution surface marker:

- **"isn't" path (L0 → L16):** The largest-magnitude positive driver is L0:F6236 ("letter 't' following 'isn''/doesn''" at pos 28, frac_nonzero 0.003, very selective) with direct_effect +0.48. It feeds L16:F12358 ("not + form-of-be" at pos 28, direct_effect +0.37, frac_nonzero 0.028) and L15:F10071 ("negations and equivocations", direct_effect −0.32 at L15 but routed forward). These features fire on any negation regardless of what is being negated. The "isn't" in the second sentence ("The program isn't going to improve lawyers' public image") is being treated as a contradiction cue on its own.

- **"but also" / contrastive path (L4 → L15):** L4:F2884 ("'but' and other contrastive conjunctions"), L14:F11020 ("'but' and 'also'"), and L15:F12905 ("'but' + contrasting relationship") all fire on the word "but" at pos 13, with direct_effects of −0.32 to +0.37. L9:F12274 ("'not only'") at pos 7 (direct_effect +0.50) feeds forward. The model picks up the surface contrast structure "not only X but also Y" without comparing X and Y to the hypothesis's claim.

- **Speech attribution path (L4-L6):** L4:F15629 (frac_nonzero 0.014, "speech attribution / 'said'") fires on the word "said" at pos 3 with direct_effect +0.67 — the largest absolute direct_effect in the circuit. L4:F12337 is the matched inverse suppressor (−0.51), and L6:F4419 ("people providing information during official capacity") reinforces it. The probe is being pulled positive merely because a human is being quoted, not because the quoted content contradicts the hypothesis.

- **"not only" / "program" phrase (L0-L2):** L0:F1910 and L2:F5627 both detect "not only" (frac_nonzero 0.007-0.018), and L1:F11907 / L2:F13565 detect the word "program" (frac_nonzero 0.002-0.001 — extremely sparse, entity-specific). L0:F14950 ("instances of 'program' and 'step'", frac_nonzero 0.027) is a strong suppressor (−0.35). These are again surface-level lexical detectors.

- **"not" path (L13-L16, pos 6):** L13:F4368 ("the word 'not'", direct_effect +0.23 upstream of L16:F15025) and L16:F15025 ("'not' + pronouns/emotional language", direct_effect +0.32) feed the probe from the first sentence's "not only" — a negation in the premise, not in the hypothesis.

The user is correct: the circuit is dominated by spurious lexical cues (negation words, contrastive conjunctions, speech verbs) rather than features that encode the actual semantic relationship between premise and hypothesis. The probe has latched onto the heuristic "negation + contrast + attribution = contradiction," which will systematically misfire on any premise-hypothesis pair that lacks these surface markers even when they contradict, and will over-predict contradiction on any pair that contains them. Notably absent are any features for words like "improve"/"benefit" (the actual content words being contradicted), any "person-attribute conflict" detector, or any entailment-comparison feature. The single most predictive feature is the literal letter "t" completing "isn't," which is a textbook lexical shortcut.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 28 | Late-layer negation / 'not + be' features (L15-16) |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |
| [L16:F15025](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15025) | 6 | Late-layer negation / 'not + be' features (L15-16) |  usage of the word "not" combined with personal pronouns or related emotional or motivational language | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15025) |
| [L15:F10071](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) | 28 | Late-layer negation / 'not + be' features (L15-16) | negations and equivocations | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) |
| [L13:F4368](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/4368) | 6 | Late-layer negation / 'not + be' features (L15-16) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/4368) |
| [L15:F12905](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) | 13 | 'but' / contrastive conjunction (L14-15) |  the word "but" along with surrounding words that indicate a contrasting or consequential relationship. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) |
| [L14:F11020](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11020) | 13 | 'but' / contrastive conjunction (L14-15) | the word "but". and "also" | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11020) |
| [L9:F12274](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12274) | 7 | 'but' / contrastive conjunction (L14-15) |  the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12274) |
| [L4:F2884](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2884) | 13 | 'but' / contrastive conjunction (L14-15) | the word "but" and other contrastive conjunctions and adverbs. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2884) |
| [L4:F15629](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15629) | 3 | Speech attribution / 'said' (L4-6) |  speech attribution, such as the word "said" and phrases like "talking about" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15629) |
| [L4:F12337](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12337) | 3 | Speech attribution / 'said' (L4-6) |  speech attribution, especially "said" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12337) |
| [L6:F4419](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4419) | 3 | Speech attribution / 'said' (L4-6) |  instances of people providing information during an official capacity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4419) |
| [L2:F5627](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5627) | 7 | 'not only' / 'program' phrase features (L0-2) |  instances of the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5627) |
| [L0:F1910](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1910) | 7 | 'not only' / 'program' phrase features (L0-2) |  the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1910) |
| [L2:F13565](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13565) | 5 | 'not only' / 'program' phrase features (L0-2) |  the word "program(me)s" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13565) |
| [L2:F8279](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8279) | 5 | 'not only' / 'program' phrase features (L0-2) |  the word "program" or the plural "programs", sometimes weakly activating on words related to changes of state | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8279) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 28 | "isn't" letter-t / negation detector (L0-3) | the letter "t" when it follows the word "isn'" or "doesn'" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L3:F6227](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) | 30 | "isn't" letter-t / negation detector (L0-3) |  sentence fragments and informal or ungrammatical language, often including abbreviations. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 28 | "isn't" letter-t / negation detector (L0-3) | negations in other languages like French, Malay, and Croatian | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 28 | "isn't" letter-t / negation detector (L0-3) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:15629 de=0.672 |
| 3 | `inspect_feature` ×8 | L4:15629, L4:12337, L2:5627, L0:6236, L16:12358, L0:14950, L1:11907, L15:12905 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F15629@3` | ❌ error | — | — | Trace the full upstream path from L4:F15629 (speech attribution / "said" at pos … |
| SA-2 | `L2:F5627@7` | ❌ error | — | — | Trace the full upstream path from L2:F5627 (the "not only" phrase detector at po… |
| SA-3 | `L0:F6236@28` | ❌ error | — | — | Trace the full upstream path from L0:F6236 (the "isn'"/"doesn'" letter-t detecto… |
| SA-4 | `L15:F12905@13` | ❌ error | — | — | Trace the full upstream path from L15:F12905 (the "but" / contrasting conjunctio… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F15629@3, k=15 → Emb:" said"@3 (de=34.25) +14 more |
| 2 | `get_upstream_features` | L2:F5627@7, k=15 → Emb:" only"@7 (de=21.25) +14 more |
| 3 | `get_upstream_features` | L0:F6236@28, k=15 → Emb:" isn"@26 (de=23.38) +14 more |
| 4 | `get_upstream_features` | L15:F12905@13, k=15 → Emb:" only"@7 (de=5.97) +14 more |
| 5 | `inspect_feature` ×3 | L16:12358, L16:15025, L3:6227 |
| 6 | `get_upstream_features` | L16:F12358@28, k=15 → Emb:"t"@28 (de=12.69) +14 more |
| 7 | `get_upstream_features` | L15:F12905@13, k=15 → Emb:" only"@7 (de=5.97) +14 more |
| 8 | `inspect_feature` ×4 | L16:9779, L4:2422, L4:4492, L15:10071 |
| 9 | `get_upstream_features` | L16:F12358@28, k=20 → Emb:"t"@28 (de=12.69) +19 more |
| 10 | `get_upstream_features` | L16:F15025@6, k=15 → Emb:" not"@6 (de=12.19) +14 more |
| 11 | `inspect_feature` ×3 | L14:11020, L9:12274, L13:4368 |
| 12 | `get_upstream_features` | L16:F15025@6, k=20 → Emb:" not"@6 (de=12.19) +19 more |
| 13 | `get_upstream_features` | L15:F12905@13, k=20 → Emb:" only"@7 (de=5.97) +19 more |
| 14 | `inspect_feature` ×8 | L2:13565, L0:15525, L4:2884, L5:2329, L2:8279, L0:1910, L6:4419, L0:6131 |

### Build

`build_circuit` → 11 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 51,864 | 5,227 | 283,166 | 0 | $0.0388 | — | — |
| **Total** | | **51,864** | **5,227** | **283,166** | **0** | **$0.0388** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 34s