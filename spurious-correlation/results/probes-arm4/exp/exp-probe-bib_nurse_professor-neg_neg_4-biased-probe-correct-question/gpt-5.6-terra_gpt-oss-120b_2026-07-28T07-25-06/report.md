# Circuit Oracle Report
**Date:** 2026-07-28 07:25:06 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe score is driven predominantly by lexical gender/person-reference features—especially *his/He*—rather than by a circuit representing the subject’s computing-research profession.

**Confidence:** 9/10

**Reasoning:** The strongest positive direct driver of the probe is the layer-0 feature **L0:2994**, firing at positions 37 and 55 (direct effects **+0.2539** and **+0.1543**). Its label is explicitly “the pronoun *his* and the pronoun *he*” (frequency **0.07326**). Crucially, tracing **L0:2994 at pos 37** reaches the raw embedding **Emb: “ his” (pos 37)** with a very large positive upstream effect (**+45.25**). Thus the local token *his* is directly read out by the profession probe direction.

The circuit also has a separate person/pronoun path from **Emb: “ His” (pos 13)**. The embedding excites **L7:14893 at pos 13** by **+22.75**. This feature is labelled “pronouns or possessive pronouns” (frequency **0.00885**) and contributes **+0.1299** directly to the probe. It is not a profession feature: its promoted tokens include feminine/reflexive pronoun continuations such as *herself* and *she*, while it suppresses masculine forms such as *his* and *himself*. The probe appears to exploit a person/gender-reference representation, not an academic or technical-role representation.

Several inspected features further support that interpretation:

- **L6:12990** is explicitly a **male-pronoun/title** feature (frequency **0.06766**), directly *negative* for the probe at several positions, including pos 13 (**−0.1660**) and pos 35 (**−0.1245**). Its upstream signal is strongly from **“His” (pos 13, +5.2812)**.  
- **L7:14946** is another *his/he/him* feature and is negative for the probe (**−0.1250** at pos 2; **−0.1147** at pos 1).  
- **L18:14743**, labelled simply **“He”** (frequency **0.01809**), is also negative (**−0.1406**). Its largest parent is **Emb: “ He” (pos 35)** with effect **+23.625**, with smaller support from **Emb: “His” (pos 13, +1.0781)** and an early male-reference detector **L0:1069**.  
- **L12:2175**, labelled “words referring to gender” (frequency **0.00622**), is likewise among the top negative direct contributors (**−0.1079**).

So the sign is mixed across different gender-coded directions: some male-pronoun signals increase the probe score, while others suppress it. But that does **not** mitigate the core finding: a large fraction of the accessible high-effect circuit is organized around pronouns, gender, and person reference. These are not indicators of being a computer scientist, researcher, director, or academic.

The remaining positive early features are also weak evidence for genuine profession classification. **L0:2848** is merely the word *of* (**+0.1484**, frequency **0.01966**); **L0:8658** is *is* (**+0.1104**, frequency **0.00671**); and **L0:11024** is a “clock/technical context” detector (**+0.1416**, frequency **0.00887**) but its active input position is the word **Director** rather than an explicit technical term, so it is not robust evidence that the probe uses the supplied “parallel and distributed computing,” “cloud,” or “Computer Science” content.

The saved circuit therefore has two principal positive branches:

1. **Emb: “his” (pos 37) → Male-pronoun lexical detector (L0:2994) → probe**  
2. **Emb: “His” (pos 13) → Pronoun/person-reference context (L7:14893) → probe**

with generic surface-form signals feeding the probe separately. There is no comparably supported traced path from tokens such as *Director*, *Laboratory*, *research*, *computing*, *cloud*, *Ph.D.*, or *Computer Science* into a profession-semantic detector that drives the score.

**Conclusion:** the user concern is well founded. On this example, the classification score is substantially driven by spurious gender/person-reference cues, particularly *his/He*, plus generic syntactic features. The graph does not provide evidence that the probe’s score is principally based on genuine profession indicators.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 37 | Male-pronoun lexical detector | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 55 | Male-pronoun lexical detector | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 13 | Pronoun/person-reference context |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 5 | Generic local surface cues | the word "of" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F11024](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11024) | 4 | Generic local surface cues |  the word "clock", especially in a technical context | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11024) |
| [L0:F8658](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8658) | 2 | Generic local surface cues |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8658) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2994 de=0.254 |
| 3 | `inspect_feature` ×7 | L0:2994, L0:2848, L0:11024, L7:14893, L6:12990, L7:14946, L18:14743 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@13` | ❌ error | — | — | Trace this positive driver of the synthetic profession-probe score to embeddings… |
| SA-2 | `L6:F12990@13` | ❌ error | — | — | Trace this major negative (suppressing) path to embedding inputs. Identify seman… |
| SA-3 | `L18:F14743@35` | ❌ error | — | — | Trace this major late negative path upstream to embeddings; identify what eviden… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14743@35, k=15 → Emb:" He"@35 (de=23.62) +14 more |
| 2 | `get_upstream_features` | L7:F14893@13, k=15 → Emb:" His"@13 (de=22.75) +14 more |
| 3 | `get_upstream_features` | L6:F12990@13, k=15 → Emb:" His"@13 (de=5.28) +14 more |
| 4 | `inspect_feature` ×5 | L0:8658, L4:4315, L12:2175, L0:1069, L17:5889 |
| 5 | `get_upstream_features` | L4:F4315@13, k=10 → Emb:" His"@13 (de=21.25) +9 more |
| 6 | `get_upstream_features` | L0:F2994@37, k=10 → Emb:" his"@37 (de=45.25) +9 more |

### Build

`build_circuit` → 6 nodes, 5 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 48,485 | 2,554 | 53,291 | 0 | $0.1728 | — | — |
| **Total** | | **48,485** | **2,554** | **53,291** | **0** | **$0.1728** | | |

**Oracle wall-clock time:** 0m 40s