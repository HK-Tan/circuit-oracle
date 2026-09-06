# Circuit Oracle Report
**Date:** 2026-07-28 07:25:08 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_10 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe score is driven primarily by superficial lexical/form cues—especially the phrase “not mentioning” and the token “question”—rather than by a coherent representation of the prompt’s racialized accusation or its actual toxicity.

**Confidence:** 8/10

**Reasoning:** The saved circuit shows a short, largely token-local mechanism feeding the linear probe direction.

* The strongest positive contribution is **L4:15173** at *“mentioning”* (direct effect **+0.1348**). Its label is “statements about mentioning or discussing something” (frequency **0.04342**). Crucially, its upstream attribution is dominated directly by **Emb: “ mentioning” (pos 3)**, with direct effect **+17.5**. It also receives a smaller positive path through the explicit mention-word detectors **L2:11639 → L3:6517 → L4:15173**. L2:11639 is a selective literal *mention* detector (frequency **0.00356**), while L3:6517 is likewise a *mention/mentioned* feature (frequency **0.00562**) and promotes “mention,” “mentioning,” “mentioned,” etc. This is direct lexical recognition, not a representation of abusive conduct, racial stereotyping, or a proposition about police behavior.

* A second positive late feature, **L4:2668** (**+0.0986**), was autointerpreted as realization/acknowledgement language (frequency **0.01065**). In this input it is principally sourced by **Emb: “ not” (pos 2)** (**+9.5**) and **Emb: “ mentioning” (pos 3)** (**+3.86**), with modest support from the “By” feature **L3:12410** (**+1.20**). Thus this branch appears to respond to the local construction *“By not mentioning …”*, not specifically to the racial groups or the hostile implication later in the sentence.

* The sentence-opening token is itself represented by **L3:12410**, a very sparse detector for sentence-initial **“By”** (frequency **0.0065**, direct probe effect **+0.1289**). It is almost entirely caused by **Emb: “By” (pos 1)** (**+48.75**). Its link into L4:2668 indicates that the probe is sensitive to this particular syntactic/discourse framing. That is another form/style cue, not semantic toxicity evidence.

* The other prominent positive direct driver is **L3:672** at *“question”* (**+0.1050**), a sparse literal **question** detector (frequency **0.0032**). It is overwhelmingly caused by **Emb: “ question” (pos 10)** (**+38.75**). “Question” here is merely part of *“cops in question”*; treating it as strong positive evidence is a clear lexical shortcut with no standalone toxic meaning.

* There **is** explicit racial-topic recognition, but it is not the positive basis of this score. **L0:10682** and **L2:10509** detect literal *race*; **L0:14813** is specifically labeled “mentions of race, racial issues, or racism” (frequency **0.01066**); and **L3:5475** also detects *race*. Yet their listed probe-direction effects are net **negative** for the leading race features—e.g. L2:10509 **−0.1807**, L0:14813 **−0.1064**, L3:5475 **−0.1011**—rather than positive. This is important: the circuit does not support the claim that an “identity group” feature alone is the principal *positive* driver on this example. It does show that the probe has an unstable or countervailing racial-topic component, but the observed positive score evidence is more strongly tied to wording such as “By,” “not,” “mentioning,” and “question.”

Overall, the circuit supports the concern that this classification is **not grounded chiefly in the prompt’s full semantic content**. The dominant positive circuit is a shallow bag of sparse lexical and constructional cues. It is not an entity-specific “black” or “white” detector in the traced positive paths, nor does it clearly compose *race + police violence + accusation/stereotype* into a toxicity representation. Instead, it appears that the probe direction has latched onto correlational surface patterns—especially the *“By not mentioning …”* frame and isolated lexical tokens—while racial-topic features contribute negatively or ambiguously.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L2:F11639](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11639) | 3 | Mentioning lexical detectors | the word "mention" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11639) |
| [L3:F6517](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6517) | 3 | Mentioning lexical detectors |  words related to mentioning something | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6517) |
| [L3:F12410](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12410) | 1 | Sentence-initial “By” form detector | the word "By" at the start of a phrase or sentence | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12410) |
| [L4:F15173](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15173) | 3 | Mentioning/discussion statement features |  statements about mentioning or discussing something | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15173) |
| [L4:F2668](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2668) | 3 | Mentioning/discussion statement features |  instances of realizations coupled with acknowledgement or acknowledgment of something. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2668) |
| [L3:F672](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/672) | 10 | Question lexical detector |  the word "question" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/672) |
| [L0:F10682](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10682) | 5 | Race/racial-topic lexical features (net suppressive) |  the word "race" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10682) |
| [L0:F14813](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14813) | 5 | Race/racial-topic lexical features (net suppressive) |  mentions of race, racial issues, or racism | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14813) |
| [L2:F10509](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10509) | 5 | Race/racial-topic lexical features (net suppressive) |  the word "race." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10509) |
| [L3:F5475](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5475) | 5 | Race/racial-topic lexical features (net suppressive) |  occurrences of the word "race" in different contexts | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5475) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:4958 de=-0.227 |
| 3 | `inspect_feature` ×5 | L4:15173, L4:573, L4:2668, L3:12410, L3:672 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F15173@3` | ❌ error | — | — | Trace the strongest positive late-layer contribution to the toxicity probe. Iden… |
| SA-2 | `L4:F2668@3` | ❌ error | — | — | Trace this positive late-layer contribution to the probe upstream to determine i… |
| SA-3 | `L4:F573@2` | ❌ error | — | — | Trace this strong negative late-layer contribution to the probe upstream; identi… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F15173@3, k=15 → Emb:" mentioning"@3 (de=17.50) +14 more |
| 2 | `get_upstream_features` | L4:F2668@3, k=15 → Emb:" not"@2 (de=9.50) +14 more |
| 3 | `get_upstream_features` | L3:F672@10, k=15 → Emb:" question"@10 (de=38.75) +14 more |
| 4 | `inspect_feature` ×11 | L2:11639, L2:6539, L0:10682, L0:4958, L2:10509, L3:6517, L2:14569, L3:11688, L0:1903, L0:14813, L3:5475 |
| 5 | `get_upstream_features` | L3:F12410@1, k=10 → Emb:"By"@1 (de=48.75) +9 more |

### Build

`build_circuit` → 10 nodes, 10 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 33,317 | 2,741 | 77,983 | 0 | $0.1439 | — | — |
| **Total** | | **33,317** | **2,741** | **77,983** | **0** | **$0.1439** | | |

**Oracle wall-clock time:** 0m 43s