# Circuit Oracle Report
**Date:** 2026-07-28 07:24:46 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The profession-probe score is driven primarily by a female-gender circuit—beginning with “She” and reinforced by the female name/context—rather than by the text’s explicit nutrition/dietetics qualifications.

**Confidence:** 9/10

**Reasoning:** The saved circuit shows a direct path from **Emb: She (pos 1)**, and secondarily **Emb: loves (pos 2)**, into an increasingly abstract female-reference representation, which then drives the probe score.

* The strongest positive probe-driving feature is **L6:F11646** at positions 1 and 2 (direct effects **+0.375** and **+0.305**). It is a women-reference feature: its label is “references to women, potentially triggered by pronouns and titles” (`frac_nonzero=0.01976`) and its promoted tokens include *she*, *her*, and *herself*. Its main upstream source at pos 1 is the raw embedding **“She”** with direct effect **+19.25**. At pos 2, it receives positive input from **“ loves”** (+5.66), **“She”** (+4.19), and early named-entity/gender features.

* **L12:F12940** at pos 2 contributes **+0.252** to the probe. This is explicitly a female pronoun/possessive detector (`frac_nonzero=0.00652`), promoting *herself* and *womanhood*. It is fed by **“She”** (+5.31), **“ loves”** (+4.25), L6:F11646 (+2.63), and **L4:F15317** (+2.92).

* **L18:F14677** at pos 1 contributes **+0.247** and is the clearest late semantic feature: “instances of women or girls being mentioned” (`frac_nonzero=0.01225`), with promoted tokens *herself*, *she*, and *her*. Its dominant upstream input is again the raw **“She”** embedding (**+27.13**), with additional positive flow from L6:F11646 (+4.19) and L4:F7864 (+4.91). Thus this feature is a high-level gender detector, not a dietitian/nutrition detector.

* The early circuit corroborates that interpretation. **L4:F15317** at pos 2 is a named-person/entity feature (`frac_nonzero=0.0175`) whose promoted tokens are overwhelmingly female pronouns—*herself*, *she*, *her*. **L4:F7864** at pos 1 is nominally labeled code/XML-like (`frac_nonzero=0.01491`), but on this direction it promotes *herself*, *she*, and *shes*; its behavior here is consistent with supporting the female-reference pathway rather than representing nutrition. L0:F7509, although a **negative** probe contributor (−0.174), is also an explicit female-pronoun feature, further showing that gender is highly represented in the probe-relevant subspace.

* There is one genuine profession-adjacent signal: **L1:F15251** at pos 5 is a selective *client(s)* feature (`frac_nonzero=0.00325`). But it contributes **negatively** (−0.170) to this particular score and is not part of the dominant positive circuit. Likewise, the top positive features and their traced origins do not identify “nutrition,” “dietetics,” “Academy,” “healthy,” “recipes,” or the dietitian credential. The circuit is concentrated at the opening pronoun/name positions rather than the later domain-specific evidence.

* A notable countervailing feature is **L7:F8644** at the *Sarah* position (direct effect **−0.270**). Its label is “woman’s name in a variety of contexts” (`frac_nonzero=0.00902`), and it is fed by **“She”** (+8.25), **“Sarah”** (+2.30), and **“her”** (+1.98). Despite recognizing female-name context, its sign suppresses this probe direction. This does not rescue profession specificity: it indicates that several gender/name subfeatures have mixed directions, while the **net prominent positive evidence** is still explicitly female-reference based.

Therefore, the user’s concern is supported for this example: the circuit contains a substantial, direct, multi-layer **spurious gender-marker mechanism**. The text genuinely supplies strong dietitian evidence, but that evidence is absent from the top positive causal circuit inspected here; the probe’s score is chiefly explained by the model encoding that the subject is female.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Early female-reference detectors | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Early female-reference detectors |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Female pronoun/reference representation |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Female pronoun/reference representation |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Female possessive/pronoun detector | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Woman/girl mention detector |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 12 features; top: L6:11646 de=0.375 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@1` | ❌ error | — | — | Trace this strongest late positive contributor to the profession-probe score bac… |
| SA-2 | `L12:F12940@2` | ❌ error | — | — | Trace this positive contributor to the probe score back to embeddings. Determine… |
| SA-3 | `L6:F11646@1` | ❌ error | — | — | Trace the two highest direct-effect early-mid contributors at position 1, likely… |
| SA-4 | `L7:F8644@12` | ❌ error | — | — | Trace this major negative contributor at the Sarah/name position. Identify wheth… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×4 | L4:7864, L4:15317, L0:7509, L1:15251 |
| 2 | `get_upstream_features` | L18:F14677@1, k=12 → Emb:"She"@1 (de=27.12) +11 more |
| 3 | `get_upstream_features` | L12:F12940@2, k=12 → Emb:"She"@1 (de=5.31) +11 more |
| 4 | `get_upstream_features` | L6:F11646@1, k=12 → Emb:"She"@1 (de=19.25) +11 more |
| 5 | `get_upstream_features` | L6:F11646@2, k=12 → Emb:" loves"@2 (de=5.66) +11 more |
| 6 | `get_upstream_features` | L7:F8644@12, k=12 → Emb:"She"@1 (de=8.25) +11 more |
| 7 | `inspect_feature` ×4 | L18:14677, L12:12940, L6:11646, L7:8644 |

### Build

`build_circuit` → 7 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 27,989 | 2,369 | 34,408 | 0 | $0.1141 | — | — |
| **Total** | | **27,989** | **2,369** | **34,408** | **0** | **$0.1141** | | |

**Oracle wall-clock time:** 0m 31s