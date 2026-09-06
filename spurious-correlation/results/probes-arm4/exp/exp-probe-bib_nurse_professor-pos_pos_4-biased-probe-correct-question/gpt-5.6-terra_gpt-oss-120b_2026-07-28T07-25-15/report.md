# Circuit Oracle Report
**Date:** 2026-07-28 07:25:15 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The profession-probe score is driven by a mixed circuit: strong genuine nursing/medical phrase evidence is present, but a comparably prominent female-person/gender representation also directly raises the score.

**Confidence:** 8/10

**Reasoning:** The saved circuit shows two distinct evidence streams converging on the **Output: profession-classification probe score** rather than a language-model next-token logit.

1. **Direct profession evidence is substantial and specific.**  
   The embeddings for **“Nursing” (pos 18)**, **“nurse” (pos 32)**, and **“practitioner” (pos 33)** feed the *Medical/nursing phrase detectors* supernode:
   - **L5:F1275 at pos 33** is a healthcare-professional/medical-field feature (frac_nonzero **0.01326**); its strongest examples explicitly include *“nurse … practitioner”* and *DNP/RN*.
   - **L6:F15267 at pos 33 and pos 18** is the clearest nursing feature (frac_nonzero **0.01594**), with top activations on **“RN”** and **“nurse.”** It is also the strongest positive direct feature in the graph at pos 33 (**+0.5625**; additionally **+0.3574** at pos 18).
   - **L1:F1494 at pos 33** detects medical practices/studies (frac_nonzero **0.02375**) and activates on *“practitioner.”*

   The causal edges support a lexical/semantic mechanism, not merely demographic correlation: the raw embeddings for **“nurse”** and **“practitioner”** directly excite L6:F15267 (**+5.66** and **+3.03**, respectively), while L5:F1275 provides another strong upstream route (**+5.53** into L6:F15267). Thus, this is real occupation-relevant evidence.

2. **But the probe also uses a clear gender-coded shortcut.**  
   A separate *Name/feminine-person cues* stream starts from **“Lori” (pos 1)** and **“She” (pos 20)**:
   - **L4:F1276 at pos 1** receives a very large direct contribution from the embedding of **“Lori”** (**+16.5**) and functions as a capitalized-name/title detector (frac_nonzero **0.00341**).
   - **L4:F15317 at pos 33** is nominally an entity/person feature, but its promoted tokens are **“herself,” “she,” “her”** and it suppresses **“himself,” “his”** (frac_nonzero **0.0175**). It contributes strongly and positively to the probe (**+0.5078**).
   - **L6:F11646 at pos 20** detects references to women / feminine pronouns (frac_nonzero **0.01976**), and contributes **+0.2891** directly.

3. **The later representation is explicitly female-subject-oriented, and it directly pushes the probe.**  
   The gender stream propagates through *Female-subject / woman-with-accomplishment representation*:
   - **L18:F14677 at pos 20** is explicitly a women/girls-mentioned feature (frac_nonzero **0.01225**), with promoted tokens **“herself,” “she,” “her”** and suppression of masculine pronouns. It is a major positive probe driver (**+0.4375** at pos 20; also +0.2578 at positions 43 and 78).
   - This feature is overwhelmingly sourced by the **“She” embedding at pos 20** (**+14.44**), rather than needing nursing text to activate. It does receive smaller positive evidence from **“Nursing”** (**+1.80**) and “graduated,” but the pronoun route dominates.
   - **L19:F9685 at pos 20**, labeled references to women’s names and roles/accomplishments (frac_nonzero **0.01351**), also directly raises the probe (**+0.2617**) and is fed strongly by **“She”** (**+5.88**), with weaker support from **“Nursing”** (**+2.55**) and **“Lori”** (**+0.97**).
   - Intermediate L15:F3330 and L17:F5889 generalize this into a personal-story / pronominal-person representation, further feeding the female-coded late features.

The global multi-hop source calculation is consistent with these being causal input routes, not just feature-label coincidences: selected profession/name/pronoun source positions account for **16.729%** of total signed influence on the probe score, with **S/R = 14.704**. Most importantly, the local attribution reveals that **“She” alone has an exceptionally strong path to the late female features**, while **“nurse/practitioner/Nursing”** has a separate, highly specific path through medical/nursing detectors.

**Conclusion on the concern:** it is **not accurate** to say the circuit is *only* using spurious gender markers: the strongest individual feature, L6:F15267, is a selective nursing detector grounded in “nurse,” “practitioner,” and “Nursing.” However, the concern is materially justified: the classification probe has learned a **gender-associated component** that directly boosts its profession score through “Lori”/“She” and late female-subject features. This makes the score vulnerable to a counterfactual gender swap—e.g., replacing the name and pronouns with male-coded equivalents could lower the score even if the nursing credentials remained unchanged.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 1 | Name/feminine-person cues |  proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 1 | Name/feminine-person cues | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 33 | Name/feminine-person cues |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 20 | Name/feminine-person cues |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L1:F1494](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) | 33 | Medical/nursing phrase detectors |  words related to medical practices and studies. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 33 | Medical/nursing phrase detectors | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 33 | Medical/nursing phrase detectors |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 18 | Medical/nursing phrase detectors |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 20 | Female-subject / woman-with-accomplishment representation |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 20 | Female-subject / woman-with-accomplishment representation |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 20 | Female-subject / woman-with-accomplishment representation |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 43 | Female-subject / woman-with-accomplishment representation |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 78 | Female-subject / woman-with-accomplishment representation |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 20 | Female-subject / woman-with-accomplishment representation |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:15267 de=0.562 |
| 3 | `inspect_feature` ×5 | L6:15267, L4:15317, L18:14677, L4:1276, L19:9685 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@20` | ❌ error | — | — | Trace the strongest later-layer positive driver of the synthetic profession-prob… |
| SA-2 | `L6:F15267@33` | ❌ error | — | — | Trace this strongest direct positive low-layer driver at position 33. Identify i… |
| SA-3 | `L4:F15317@33` | ❌ error | — | — | Trace this strong positive driver at position 33 upstream, characterize whether … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14677@20, k=15 → Emb:" She"@20 (de=14.44) +14 more |
| 2 | `get_upstream_features` | L6:F15267@33, k=15 → Emb:" nurse"@32 (de=5.66) +14 more |
| 3 | `get_upstream_features` | L4:F15317@33, k=15 → Emb:" nurse"@32 (de=4.00) +14 more |
| 4 | `get_upstream_features` | L19:F9685@20, k=15 → Emb:" She"@20 (de=5.88) +14 more |
| 5 | `get_upstream_features` | L4:F1276@1, k=15 → Emb:"Lori"@1 (de=16.50) +14 more |
| 6 | `get_source_influence` | {'source_positions': [1, 2, 18, 20, 33, 43, 78], 'depth': 2} → {'depth': 2, 'source_positions': [1, 2, 18, 20, 33, 43, 78], 'S_pct_of_total': 1 |
| 7 | `inspect_feature` ×6 | L5:1275, L0:7532, L1:1494, L17:5889, L15:3330, L6:11646 |

### Build

`build_circuit` → 9 nodes, 15 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 26,675 | 2,889 | 63,416 | 0 | $0.1259 | — | — |
| **Total** | | **26,675** | **2,889** | **63,416** | **0** | **$0.1259** | | |

**Oracle wall-clock time:** 0m 51s