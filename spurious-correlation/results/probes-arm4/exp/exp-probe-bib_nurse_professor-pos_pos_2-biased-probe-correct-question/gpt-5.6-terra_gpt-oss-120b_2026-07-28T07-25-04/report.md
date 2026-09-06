# Circuit Oracle Report
**Date:** 2026-07-28 07:25:04 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The profession probe score is driven by a mixture of real nursing evidence and a dominant, repeated female-subject signal, so the circuit supports the concern that the probe exploits gender-correlated shortcuts rather than profession alone.

**Confidence:** 9/10

**Reasoning:** The saved circuit has two distinct positive routes into the **Output: profession-classification probe score**:

1. **Genuine profession route:**  
   **Emb: Nursing (pos 10)** feeds directly into the **Nursing profession detector** at **L6:15267 (pos 10)**, which has a large direct effect on the probe score (**+0.473**, second-largest positive feature overall). Its examples are explicitly activated by *“RN,” “nurse,”* and *“nurses”*; its autointerp label is “words in the document referring to the profession of nursing” and it is selective (**frac_nonzero 0.01594**). The immediate upstream attribution is also overwhelmingly lexical: the ` Nursing` embedding contributes **+17.375** to this feature. This is legitimate, profession-specific evidence.

2. **Spurious gender / female-biography route:**  
   The strongest probe feature is **L6:11646 at pos 1**, direct effect **+0.498**; the same feature also contributes at positions 2 and 19 (**+0.348**, **+0.270**). It is a selective female-reference detector (**frac_nonzero 0.01976**) whose examples consistently trigger on *“her”*, and whose promoted tokens include *“she,” “her,”* and *“herself.”* Crucially, its main upstream source is the raw **`She` embedding at pos 1** (**+19.25**), not a nursing token. Thus the early **Emb: She (pos 1) → Female-pronoun detector** edge is a direct shortcut into the probe direction.

   This gender cue is reinforced in later layers by **L18:14677**, a women/girls mention detector (**frac_nonzero 0.01225; promoted: “she,” “her,” “herself”**). At pos 19—where the second sentence starts with *“She”*—it contributes **+0.377** to the score, third-largest positive contribution. Its principal upstream input is the local **` She` embedding at pos 19** (**+15.313**); it also receives positive support from the initial `She` at pos 1 (**+4.281**) and from the earlier female-pronoun detector **L6:11646 (pos 19; +2.219)**. This is the circuit’s strongest evidence that it constructs a persistent “female subject” representation and maps it to the profession probe.

   Additional score-positive features corroborate this:
   - **L12:12940 (pos 2)**, **+0.305**, is another female possessive-pronoun feature (**frac_nonzero 0.00652**), with *“her/herself”* examples.
   - **L4:15317 (pos 2)**, **+0.344**, is a named-person/female-associated feature (**frac_nonzero 0.0175**) with promoted tokens *“she/her/herself.”*
   - **L19:9685 (pos 140)**, **+0.260**, detects women’s names, roles, or accomplishments (**frac_nonzero 0.01351**; promoted tokens again include *“she,” “her,” “herself”*). Although it has some weak support from `Nursing` (**+1.258**) and `Practitioner` (**+0.961**), its semantics are still principally female-biographical rather than nursing-specific.

The direct-effect ranking therefore does **not** look like a clean “clinical terminology → nursing representation → probe” circuit. The top score contributors are: female pronoun **L6:11646 (+0.498)**, nursing **L6:15267 (+0.473)**, female subject **L18:14677 (+0.377)**, then further female/name features. The key gender features are both highly selective and directly grounded in the literal `She` tokens, whereas the valid nursing route is primarily grounded in the literal `Nursing` token.

The multi-hop source influence check is consistent with that conclusion. The opening gendered subject region (positions 1–4, including *She*) supplies **8.462%** of total signed influence after two hops—substantial, though just below the soft ~10% source-driven reference. In contrast, the education/nursing span (positions 8–20, including `Nursing`) has **−0.929% net signed influence** at that aggregation depth, because it contains opposing effects; this does not erase the strongly positive local `Nursing → L6:15267 → probe` route, but it shows the broader score is not being driven cleanly and uniformly by the profession span.

Overall: the probe has learned authentic nursing evidence, but it also puts substantial positive weight on **female pronouns, female-name/biography structure, and a repeated female-subject representation**. The observed score is therefore partly a profession prediction and partly a gender-correlated shortcut.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Female-pronoun detector |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Female-pronoun detector |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 19 | Female-pronoun detector |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Female-pronoun detector |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Female-pronoun detector | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 10 | Nursing profession detector |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 19 | Female-subject / biography representation |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Female-subject / biography representation |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 50 | Female-subject / biography representation |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 140 | Female-name/accomplishment representation |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11646 de=0.498 |
| 3 | `inspect_feature` ×8 | L6:11646, L6:15267, L18:14677, L4:15317, L4:7864, L12:12940, L19:9685, L6:8166 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@19` | ❌ error | — | — | Trace the strong positive feature at pos 19 upstream to embeddings; determine wh… |
| SA-2 | `L6:F11646@1` | ❌ error | — | — | Trace this repeatedly active strong probe-driving feature to embeddings. Identif… |
| SA-3 | `L19:F9685@140` | ❌ error | — | — | Trace the late feature at the biography continuation to embeddings, testing for … |
| SA-4 | `L6:F8166@81` | ❌ error | — | — | Trace this probe-driving feature at the clinical-experience portion to embedding… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F11646@1, k=15 → Emb:"She"@1 (de=19.25) +14 more |
| 2 | `get_upstream_features` | L6:F15267@10, k=15 → Emb:" Nursing"@10 (de=17.38) +14 more |
| 3 | `get_upstream_features` | L18:F14677@19, k=15 → Emb:" She"@19 (de=15.31) +14 more |
| 4 | `get_upstream_features` | L19:F9685@140, k=15 → L4:F1276 (de=1.45) +14 more |
| 5 | `get_upstream_features` | L6:F8166@81, k=15 → L5:F6637 (de=-6.31) +14 more |
| 6 | `get_source_influence` | {'source_positions': [1, 2, 3, 4], 'depth': 2} → {'depth': 2, 'source_positions': [1, 2, 3, 4], 'S_pct_of_total': 8.462, 'R_pct_o |
| 7 | `get_source_influence` | {'source_positions': [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'depth' → {'depth': 2, 'source_positions': [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,  |

### Build

`build_circuit` → 8 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 18,195 | 2,723 | 53,080 | 0 | $0.0996 | — | — |
| **Total** | | **18,195** | **2,723** | **53,080** | **0** | **$0.0996** | | |

**Oracle wall-clock time:** 0m 38s