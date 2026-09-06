# Circuit Oracle Report
**Date:** 2026-07-28 07:22:58 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe is classified by gender markers — not by the Engineering / Robotics / Systems-Design profession content. The top 7 features by absolute direct effect all detect pronouns, possessives, or gendered referents; only two features (L5:F10392, L6:F170) detect academic/profession content, and they net out below the pronoun features.

**Confidence:** 9

**Reasoning:**

The circuit is overwhelmingly driven by gendered-pronoun features, confirming the user's concern. Tracing back to the embedding layer shows the signal originates from two input tokens: " his" (pos 3, direct_effect=43.25 into L0:F2994) and " He" (pos 22, direct_effect=21.88 into L18:F14743, 4.47 into L6:F12990). No embedding of profession terms ("Robotics", "Computer Vision", "Systems Design", "Ph.D") is present in the attribution graph.

The largest single driver is **L0:F2994** ("the pronoun 'his' and the pronoun 'he'", pos 3, direct_effect=+0.39, activation 39.5, frac_nonzero=0.073). It is fed almost entirely by the embedding of the token " his" itself. The same feature also fires at pos 25 ("his Ph.D") and pos 47 ("his research interests"), so each gendered possessive in the passage adds more positive signal to the probe.

The second-strongest positive driver is **L7:F14893** ("pronouns or possessive pronouns", direct_effect=+0.20, frac_nonzero=0.009 — a very selective feature). Its top input is again the " his" embedding (direct_effect=24.4). It is inhibited by L0:F2994 (direct_effect=-10.9) and excited by L6:F12990 (male-pronoun feature, direct_effect=+3.2), so it is part of a gendered-pronoun sub-circuit. Its promoted/suppressed tokens split sharply along gender lines (promotes "herself/she", suppresses "himself/his").

Layer 18 contains two more pronoun features: **L18:F14743** ("He", direct_effect=-0.14 at pos 22 and -0.11 at pos 81, frac_nonzero=0.018) and **L18:F10315** ("pronouns and possessive pronouns", direct_effect=-0.10). Both are anchored to the " He" / " his" embeddings.

**L6:F12990** ("male pronouns and titles along with descriptors associated with men", direct_effect=-0.17) and **L7:F14946** ("the possessive pronoun 'his'…", direct_effect=-0.18) are the largest negative contributors — they are gendered features whose decoder direction pushes against the probe. **L12:F2175** ("words referring to gender", direct_effect=-0.17, frac_nonzero=0.006) reinforces the picture at a higher layer.

The only profession-relevant features are **L5:F10392** ("fields of academic study", direct_effect=-0.11, pos 9 "Engineering") and **L6:F170** ("references to academic fields, especially those in the humanities", direct_effect=+0.14 at pos 9 and +0.10 at pos 8). The top activating examples for L5:F10392 are "Science", "Sports Administration", "Writing", "Literature" — humanities and soft fields, not engineering/robotics. L6:F170 is explicitly labeled "especially those in the humanities" with examples "literature", "English", "Writing". So even the "profession" features are mismatched: they fire on "Engineering" because the word pattern is academic, but the feature's identity is humanities-oriented, and the same paths then get overtaken by the pronoun signal.

The remaining L0 features (L0:F1326 "organizations", F7532 "proper nouns", F13553 "past-tense verbs", etc.) are tiny (direct_effect ~+0.10 each) and generic; they contribute to neither profession nor gender in a meaningful way.

**Mechanism summary:** The probe's classification score is built from a male-gender sub-circuit. The token " his" at position 3 (and " He" at position 22) activate a stack of pronoun/possessive features spanning L0, L6, L7, L12, and L18. These features (L0:F2994, L6:F170 at +0.14, L7:F14893 at +0.20) are the net positive drivers. Counter-features (L6:F12990, L7:F14946, L12:F2175) and the humanities-flavored academic-field features subtract from the score but do not flip it. Profession-true content (Robotics, Computer Vision, Systems Design, Ph.D) does not appear anywhere in the attribution graph.

This is precisely the spurious-feature failure mode the user suspected: the model/probe is reading male pronouns, not engineering.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: his (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 22 | Emb: He (pos 22) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Daniel (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: received (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: Mechanical (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: achelors (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: Engineering (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 3 | L0: Pronoun 'his/he' detector | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 25 | L0: Pronoun 'his/he' detector | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 47 | L0: Pronoun 'his/he' detector | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 22 | L0: 'He'/capitalized token detector (pos 22) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 9 | L5: Fields of academic study detector |  fields of academic study | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 9 | L6: Academic fields (humanities-leaning) detector |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 8 | L6: Academic fields (humanities-leaning) detector |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 22 | L6: Male pronouns / male descriptors |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 3 | L6: Male pronouns / male descriptors |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 3 | L7: Female pronouns (suppresses 'himself/his') |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 3 | L7: 'his' possessive pronoun detector |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L12:F2175](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) | 2 | L12: Gender-referential words |  words referring to gender | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 22 | L18: 'He' (capitalized) pronoun detector | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 81 | L18: 'He' (capitalized) pronoun detector | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 3 | L18: Pronouns / possessives (his) |  pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L0:F1326](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1326) | 14 | L0: Other small positive contributors (org names, proper nouns, past-tense verbs) |  mentions of organizations and government agencies. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1326) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 1 | L0: Other small positive contributors (org names, proper nouns, past-tense verbs) |  proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L0:F15320](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) | 2 | L0: Other small positive contributors (org names, proper nouns, past-tense verbs) |  the word "ice" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) |
| [L0:F13553](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13553) | 2 | L0: Other small positive contributors (org names, proper nouns, past-tense verbs) |  verbs in the past tense or past participle | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13553) |
| [L0:F13526](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13526) | 21 | L0: Suppressing misc (months, 'received', gender) |  months of the year, sometimes in connection to a number | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13526) |
| [L0:F12351](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12351) | 2 | L0: Suppressing misc (months, 'received', gender) | words related to obtaining something, like receiving money or a receipt | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12351) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2994 de=0.395 |
| 3 | `inspect_feature` ×15 | L0:2994, L7:14893, L7:14946, L12:2175, L6:12990, L6:170, L0:1326, L0:7532, L0:12351, L0:15320, L0:13526, L0:13553, L5:10392, L18:14743, L18:10315 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F2994@3` | ❌ error | — | — | Trace upstream from L0:F2994 (the "his/he" pronoun feature at pos 3) to its deep… |
| SA-2 | `L7:F14893@3` | ❌ error | — | — | Trace upstream from L7:F14893 (pronouns/possessive pronouns feature) at pos 3. T… |
| SA-3 | `L6:F12990@22` | ❌ error | — | — | Trace upstream from L6:F12990 (male pronouns/titles feature) at pos 22. This is … |
| SA-4 | `L18:F14743@22` | ❌ error | — | — | Trace upstream from L18:F14743 (the "He" feature) at pos 22. This is a strong NE… |
| SA-5 | `L6:F170@9` | ❌ error | — | — | Trace upstream from L6:F170 (academic fields feature) at pos 9. This is a positi… |
| SA-6 | `L5:F10392@9` | ❌ error | — | — | Trace upstream from L5:F10392 (fields of academic study feature) at pos 9. This … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F2994@3, k=10 → Emb:" his"@3 (de=43.25) +9 more |
| 2 | `get_upstream_features` | L7:F14893@3, k=10 → Emb:" his"@3 (de=24.38) +9 more |
| 3 | `get_upstream_features` | L6:F12990@22, k=10 → Emb:" He"@22 (de=4.47) +9 more |
| 4 | `get_upstream_features` | L6:F170@9, k=10 → L5:F10392 (de=10.94) +9 more |
| 5 | `get_upstream_features` | L5:F10392@9, k=5 → Emb:" Mechanical"@8 (de=3.08) +4 more |
| 6 | `get_upstream_features` | L18:F14743@22, k=5 → Emb:" He"@22 (de=21.88) +4 more |

### Build

`build_circuit` → 20 nodes, 29 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 43,478 | 6,612 | 144,094 | 0 | $0.0296 | — | — |
| **Total** | | **43,478** | **6,612** | **144,094** | **0** | **$0.0296** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 25s