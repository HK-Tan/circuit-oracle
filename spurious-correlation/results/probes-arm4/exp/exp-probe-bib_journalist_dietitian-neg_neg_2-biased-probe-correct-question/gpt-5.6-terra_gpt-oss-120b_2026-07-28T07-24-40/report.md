# Circuit Oracle Report
**Date:** 2026-07-28 07:24:40 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The profession probe score is driven primarily by the opening masculine possessive **“His”**, through gendered pronoun/person-reference features, rather than by the text’s genuine reporting/news-organization evidence.

**Confidence:** 9/10

**Reasoning:** The saved circuit identifies a compact pronoun-driven mechanism:

- **Emb: His (pos 1)** directly excites the two dominant layer-7 probe drivers. Its upstream attribution to **L7:F14893** is strongly positive (+23.5), and to **L7:F14946** is also strongly positive (+18.38). Thus the principal input source is explicitly the token *“His,”* not the later occupational phrase *“report for … news organizations.”*
- The **Early masculine-pronoun detector** (**L0:F2994**, pos 1) is labeled *“the pronoun ‘his’ and the pronoun ‘he’”* and fires fairly broadly (`frac_nonzero=0.0733`). It feeds the layer-7 pronoun representation, though its listed edge to L7:F14893 is inhibitory (−4.69), so it is best interpreted as part of a competing/balancing encoding of the same pronoun rather than the main positive causal route.
- The core **Gendered pronoun / possessive representation** has two opposed components:
  - **L7:F14893** has the largest positive direct effect on the probe, **+0.4883**. It is a selective pronoun/possessive feature (`frac_nonzero=0.00885`) whose examples include *his*, while its promoted tokens are feminine forms such as *she*, *herself*, and *elle* and it suppresses *his/himself*. In this particular probe direction, this “female-associated” side pushes the score upward.
  - **L7:F14946** is the nearly equal but opposite driver, **−0.4844**. It is specifically labeled as a detector for *“his,” “he,” and “him”* (`frac_nonzero=0.01669`), promotes *his/himself*, and suppresses *she/her/herself*. It therefore pushes the probe score downward.
  
  The important finding is not merely the net cancellation: the two largest-magnitude contributions to the classification score are a **gender-pronoun contrast**, with a combined absolute effect of roughly 0.97—much larger than any inspected profession-semantic evidence.

- The **Late person-reference / pronoun representation** (**L19:F8814**, pos 1) is another positive probe driver (**+0.2617**) and is labeled *“various pronouns and names referring to people”* (`frac_nonzero=0.08655`). It promotes feminine pronouns (*she, her, herself*) while suppressing masculine ones (*his, himself*). It receives a direct positive contribution from **Emb: His (pos 1)** (+9.31), again showing that the probe direction is reading gender/person-reference structure from the initial pronoun.

There is also a negative **L18:F14743** feature at position 9 (the token *“him”*) with direct effect **−0.2070**. It is a highly selective *He* feature (`frac_nonzero=0.01809`) and is directly driven by **“ him”** (+18.38). This independently corroborates that masculine coreference is materially represented in the probe circuit. Although position 9 also receives small signals from *taken*, *world*, and *see*, these are much weaker than the pronoun embedding path and are not evidence of a reporter/journalist detector.

I found no leading feature labeled for **reporting, journalism, news organizations, travel, or a profession** among the highest-effect contributors. Given that the strongest positive and negative features are explicitly pronoun/gender detectors anchored at *His/him*, the user’s concern is supported: this probe appears substantially confounded by **gendered linguistic markers** (and generic person-reference cues), rather than cleanly classifying the profession described by the sentence.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | Early masculine-pronoun detector | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Gendered pronoun / possessive representation |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | Gendered pronoun / possessive representation |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | Late person-reference / pronoun representation |  various pronouns and names referring to people | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L7:14893 de=0.488 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ❌ error | — | — | Trace this strongest positive driver of the profession probe score upstream to e… |
| SA-2 | `L7:F14946@1` | ❌ error | — | — | Trace this strongest negative driver upstream to embeddings. Identify its semant… |
| SA-3 | `L19:F8814@1` | ❌ error | — | — | Trace this positive late/mid-layer probe driver upstream to embeddings, focusing… |
| SA-4 | `L18:F14743@9` | ❌ error | — | — | Trace this major negative driver at position 9 upstream. Determine what text sig… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×6 | L7:14893, L7:14946, L19:8814, L18:14743, L0:2994, L0:2011 |
| 2 | `get_upstream_features` | L7:F14893@1, k=15 → Emb:"His"@1 (de=23.50) +14 more |
| 3 | `get_upstream_features` | L7:F14946@1, k=15 → Emb:"His"@1 (de=18.38) +14 more |
| 4 | `get_upstream_features` | L19:F8814@1, k=15 → Emb:"His"@1 (de=9.31) +14 more |
| 5 | `get_upstream_features` | L18:F14743@9, k=15 → Emb:" him"@9 (de=18.38) +14 more |

### Build

`build_circuit` → 5 nodes, 5 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 13,279 | 1,990 | 36,125 | 0 | $0.0721 | — | — |
| **Total** | | **13,279** | **1,990** | **36,125** | **0** | **$0.0721** | | |

**Oracle wall-clock time:** 0m 29s