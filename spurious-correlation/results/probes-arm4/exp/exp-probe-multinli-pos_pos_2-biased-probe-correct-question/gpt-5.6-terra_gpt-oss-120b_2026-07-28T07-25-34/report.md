# Circuit Oracle Report
**Date:** 2026-07-28 07:25:34 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction probe is driven predominantly by shallow lexical/style cues—especially the opening “yeah well uh” and the tokenized negation in “haven’t”—rather than by a circuit that compares the incompatible claims about not watching games versus not missing a Sweet-16 game.

**Confidence:** 8/10

**Reasoning:** The saved circuit identifies two main cue families feeding the synthetic probe-score output.

1. **Opening conversational-disfluency/style cues.**  
   - `Emb: well (pos 2)` strongly excites the layer-4 acknowledgment feature **L4:12126** (direct upstream embedding effect `+14.63`) and the conversational-phrase feature **L4:4847** (`+8.06`).  
   - L4:12126 is specifically labeled *agreement/acknowledgement, especially “well” and “yeah”* (`frac_nonzero=0.01233`); it contributes **−0.4883** directly to the probe.  
   - L4:4847 is a generic conversational/question-answer phrase feature (`frac_nonzero=0.01156`) and contributes **+0.3379**.  
   - `Emb: uh (pos 4)` strongly drives **L4:9602** (`+11.44`), whose activating examples are “mmm,” “Umm,” “ahem,” etc. This is plainly a filler/interjection feature (`frac_nonzero=0.00587`), not a contradiction or entailment feature. It is actually the largest reported direct probe driver, at **−0.6289**.

   Thus, the “yeah well the uh …” preamble makes a very large, mixed-sign contribution simply because it resembles a particular conversational register. These effects have no semantic reason to diagnose whether two propositions conflict.

2. **Lexical negation cue.**  
   - At the end of *“I haven’t missed”*, `Emb: t (pos 37; completes haven’t)` directly drives the late negation feature **L4:4492** by `+6.53`; the preceding `" haven"` token at position 35 also contributes `+1.30`.  
   - **L0:6236** at the same final `t` is an extremely specific contraction-ending feature: its label is *the letter “t” after “isn’/doesn’”* and it promotes tokens such as “not,” “nicht,” and “tidak” (`frac_nonzero=0.00258`). It contributes **+0.5352** directly to the probe and sends positive signal (`+4.41`) to L4:4492.  
   - **L4:4492** is labeled *negations in various languages* (`frac_nonzero=0.03828`) and contributes **+0.3105** to the probe.

   This is the one part of the circuit tied to a relevant linguistic ingredient: explicit negation. But it is still a **surface-form detector**, centered on the characters/subtokens of “haven’t,” not a representation of the logical relationship between the two clauses. In particular, it does not demonstrate that the model has constructed and compared: (a) “I haven’t watched [the tournament / any games]” with (b) “I haven’t missed a single Sweet-16 game,” where the latter entails watching at least those games.

The sports content provides little evidence of semantic comparison. The direct-feature list includes a negative **L2:5201** at `" tournament"` and a negative **L1:177** at `" double"`, but upstream tracing shows their dominant inputs are simply `Emb: tournament (pos 8)` (`+16.38`) and `Emb: double (pos 6)` (`+24.0`), respectively. They were not among the largest direct effects and were not shown to form a cross-clause incompatibility circuit.

Overall, the circuit supports the user concern: this probe score is substantially contaminated by **spurious register cues** (“yeah,” “well,” “uh”) and a **token-level negation/contraction cue** (“haven’t”). There is no identified late feature encoding proposition comparison, event overlap, or the crucial contradiction between “not watched it” and “not missed a single Sweet-16 game.”

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F12126](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) | 2 | Opening discourse/acknowledgment detectors |  expressions of agreement or acknowledgement, particularly "well" and "yeah" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) |
| [L4:F4847](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) | 2 | Opening discourse/acknowledgment detectors |  words or short phrases often used in conversation, and especially questions and answers | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) |
| [L4:F9602](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9602) | 4 | Filler/interjection detector |  interjections and filler words | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9602) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 37 | Lexical negation detector | the letter "t" when it follows the word "isn'" or "doesn'" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 37 | Late multilingual-negation feature | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:9602 de=-0.629 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F9602@4` | ❌ error | — | — | Trace this major negative driver of the synthetic contradiction-probe score to e… |
| SA-2 | `L4:F12126@2` | ❌ error | — | — | Trace this major negative driver of the probe score to embeddings; identify its … |
| SA-3 | `L4:F4847@2` | ❌ error | — | — | Trace this positive late feature upstream to embeddings. Explain what signal sup… |
| SA-4 | `L4:F4492@37` | ❌ error | — | — | Trace this positive feature at the final statement upstream to embeddings. Deter… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×8 | L4:9602, L4:12126, L4:4847, L4:4492, L0:6236, L0:8352, L0:3820, L0:16366 |
| 2 | `get_upstream_features` | L4:F9602@4, k=20 → Emb:" uh"@4 (de=11.44) +19 more |
| 3 | `get_upstream_features` | L4:F12126@2, k=20 → Emb:" well"@2 (de=14.62) +19 more |
| 4 | `get_upstream_features` | L4:F4847@2, k=20 → Emb:" well"@2 (de=8.06) +19 more |
| 5 | `get_upstream_features` | L4:F4492@37, k=20 → Emb:"t"@37 (de=6.53) +19 more |
| 6 | `get_upstream_features` | L2:F5201@8, k=15 → Emb:" tournament"@8 (de=16.38) +14 more |
| 7 | `get_upstream_features` | L1:F177@6, k=15 → Emb:" double"@6 (de=24.00) +14 more |

### Build

`build_circuit` → 9 nodes, 9 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 43,745 | 2,534 | 34,330 | 0 | $0.1560 | — | — |
| **Total** | | **43,745** | **2,534** | **34,330** | **0** | **$0.1560** | | |

**Oracle wall-clock time:** 0m 59s