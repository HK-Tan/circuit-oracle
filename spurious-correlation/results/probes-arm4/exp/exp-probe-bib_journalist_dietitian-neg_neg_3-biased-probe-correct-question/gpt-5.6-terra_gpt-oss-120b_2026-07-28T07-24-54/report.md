# Circuit Oracle Report
**Date:** 2026-07-28 07:24:54 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The profession-probe score is driven mainly by genuine lexical/semantic occupation cues—*researches*, *represents*, and especially *journalistic*—but it also receives a clearly spurious positive contribution from masculine pronoun context.

**Confidence:** 8/10

**Reasoning:** The saved circuit separates several direct routes into the synthetic profession-probe direction:

- **Genuine profession-adjacent evidence.**  
  - The **Research lexical detector** contains L0:4564 at *researches* (pos 2), whose label is specifically “the word *research*” (frac_nonzero **0.00694**), and L0:10036, labelled scientific research/scientists (**0.01253**). L0:4564 is a positive direct driver of the score (+0.2119), so the probe treats research language as profession-relevant evidence.  
  - The **Representation lexical concept**, L1:7449 at *represents* (pos 9), is a selective detector for “representation” (**0.00628**) and positively drives the score (+0.2168). Its dominant upstream source is the embedding **Emb: represents (pos 9)**, with a very large positive edge (+20.5). This is not a broad entity-memory circuit; it is a lexical cue, only weakly linked to the potentially occupational meaning of political/country representation.  
  - Although it was a negative direct driver in this particular target direction (L4:13253, −0.1543), the graph also contains a highly profession-specific **journalism/media** feature, L4:13253 at *journalistic* (pos 13). Its promoted tokens are *Journalism*, *journalists*, *journalism*, *reporters*, and *media*, and its firing frequency is low (**0.00648**). Its upstream attribution is dominated by **Emb: journalistic (pos 13)** (+25.625). This is the cleanest semantic indicator that the text concerns journalism, but its negative sign means this probe direction is not simply “journalist-ness”; it may distinguish the probed profession from journalism or use journalism as counterevidence.

- **Narrative/story cues, which are weak and somewhat ambiguous occupation proxies.**  
  - **Emb: stories (pos 3)** strongly excites L1:14812 (+18.625), the **Narrative/story concept**. L1:14812 is labelled stories/chapters/narrative elements (**0.00947**) and has a positive score effect (+0.2168).  
  - At layer 0, L0:5333 (story mentions; **0.0035**) and L0:61 (stories; **0.04415**) also directly push the score up (+0.2051 and +0.2021). These features likely reflect a correlated textual domain—writing, reporting, literary narrative, or a biographical-description style—rather than a robust occupation representation. Thus they are more plausibly *dataset/style proxies* than decisive evidence for a profession.

- **Spurious gender/pronoun contribution.**  
  - The key concern is supported: L7:14893 at *him* (pos 46), labelled **pronouns or possessive pronouns** (**0.00885**), positively drives the probe (+0.1963). Its promoted tokens include *herself*, *she*, and gendered pronouns, confirming that it is a grammatical/gender-associated feature rather than profession semantics.  
  - It is fed overwhelmingly by **Emb: him (pos 46)** (+12.5625), with a smaller positive contribution from **He** (pos 1, +2.4531). A second direct score feature, L0:2994 at a later masculine-pronoun position, is explicitly labelled “the pronoun *his* and the pronoun *he*” (**0.07326**) and itself contributes positively (+0.1787).  
  - Therefore, masculine reference is not merely present in the sentence: it is causally aligned with the probe score. This is a real spurious route into the classifier, independent of the research/journalism content.

- **What does *not* explain the classification.** Several of the largest-magnitude features are plainly nonsemantic token/format detectors: L0:6051 for periods/spaces/numbers (−0.2559), L0:7696 for *on* (−0.2432), L0:3255 for *and* (−0.2031), and L0:10187 for *time* (−0.2021). These show that the linear probe direction also has substantial sensitivity to superficial lexical and formatting features. They should not be interpreted as profession knowledge.

Overall, the circuit is **mixed**. The central positive semantic evidence is word-level research, representation, and narrative language, while an explicit journalism/media feature exists but opposes this probe direction. The pronoun pathway is a substantial, direct, and semantically irrelevant contribution, so the concern is warranted: the classifier is not relying exclusively on genuine profession indicators and is partly using gendered grammatical context and stylistic/domain proxies.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F4564](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) | 2 | Research lexical detector | the word "research." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) |
| [L0:F10036](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10036) | 2 | Research lexical detector |  words about scientific research and scientists | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10036) |
| [L0:F5333](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5333) | 3 | Story/narrative lexical detectors | mentions of stories that are being told | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5333) |
| [L0:F61](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/61) | 3 | Story/narrative lexical detectors | the word "stories" sometimes along with apostrophes and common names. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/61) |
| [L1:F14812](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) | 3 | Narrative/story concept |  references to stories, chapters, and other narrative elements | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) |
| [L1:F7449](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7449) | 9 | Representation lexical concept | instances of the word "representation" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7449) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 46 | Male-pronoun / possessive-pronoun signal |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 52 | Male-pronoun / possessive-pronoun signal | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:6051 de=-0.256 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@46` | ❌ error | — | — | Trace this positive late-ish driver of the synthetic profession-probe score to e… |
| SA-2 | `L1:F7449@9` | ❌ error | — | — | Trace this major positive early driver to embedding tokens. Identify its semanti… |
| SA-3 | `L1:F14812@3` | ❌ error | — | — | Trace this major positive score-driving feature to embeddings and characterize p… |
| SA-4 | `L0:F4564@2` | ❌ error | — | — | Inspect and trace this direct positive layer-0 score driver; identify exact trig… |
| SA-5 | `L0:F5333@3` | ❌ error | — | — | Inspect this direct positive layer-0 score driver and identify exact trigger, es… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×12 | L0:6051, L0:7696, L1:7449, L1:14812, L0:4564, L0:5333, L0:3255, L0:10187, L0:61, L7:14893, L0:2994, L4:13253 |
| 2 | `get_upstream_features` | L7:F14893@46, k=20 → Emb:" him"@46 (de=12.56) +19 more |
| 3 | `get_upstream_features` | L4:F13253@13, k=20 → Emb:" journalistic"@13 (de=25.62) +19 more |
| 4 | `get_upstream_features` | L1:F7449@9, k=20 → Emb:" represents"@9 (de=20.50) +19 more |
| 5 | `get_upstream_features` | L1:F14812@3, k=20 → Emb:" stories"@3 (de=18.62) +19 more |
| 6 | `inspect_feature` ×3 | L0:10036, L0:9121, L7:14893 |

### Build

`build_circuit` → 9 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 27,765 | 3,130 | 74,085 | 0 | $0.1349 | — | — |
| **Total** | | **27,765** | **3,130** | **74,085** | **0** | **$0.1349** | | |

**Oracle wall-clock time:** 0m 44s