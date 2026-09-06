# Circuit Oracle Report
**Date:** 2026-07-28 07:25:40 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The profession probe’s positive score is driven predominantly by a propagated *female-reference / female-biography* signal from repeated “She” markers, rather than by an identifiable nutrition, health, or lifestyle-profession concept.

**Confidence:** 9/10

**Reasoning:** The saved circuit begins at the embeddings for **“She” at positions 1 and 29** (`Emb: She (pos 1)`, `Emb:  She (pos 29)`), not at content-bearing words such as “healthy,” “food,” “physically active,” or “wholefoods.”

The strongest direct positive driver of the probe score is **L6:F11646 at pos 1** (direct effect **+0.3398**, activation 12.5). Its autointerp label is “references to women, potentially triggered by pronouns and titles”; its activating examples are overwhelmingly instances of *her*, and it promotes **“she,” “her,” and “herself.”** It is selective (`frac_nonzero=0.01976`) but selective for a gendered-reference category, not an individual or profession. Crucially, its largest upstream contribution is directly from the **`She` embedding at position 1** (**+19.25**), establishing a short, direct gender-marker-to-probe path.

That same source signal is consolidated downstream:
- **L12:F12940 at pos 2** is a female possessive/pronoun feature (`frac_nonzero=0.00652`), with positive direct effect **+0.1572** on the probe. It receives positive input from `She` at pos 1 (**+6.56**) and from L6:F11646 (**+3.69**).
- **L18:F14677**, active at several positions and especially position 29 (direct effect **+0.2354**), is explicitly a detector for mentions of **women or girls** (`frac_nonzero=0.01225`) and promotes *she/her/herself*. Its leading upstream source is the local **“ She” at pos 29** embedding (**+14.38**), followed by the initial `She` embedding (**+7.22**). It also receives positive support from L6:F11646 and L12:F12940.
- **L19:F9685 at pos 29** independently contributes **+0.1504**. Its label, “women’s names and their roles or accomplishments,” may superficially resemble occupational evidence, but its promoted tokens are again overwhelmingly female pronouns and its examples are female-person descriptions. Thus it appears to turn *female subject in a biographical/profile-like description* into probe-aligned evidence—not to recognize the health/nutrition profession itself.

The early intermediary **L4:F7864 at pos 1** also supports this path (direct effect **+0.2080**). Its generic autointerp label is noisy (“XML/source code”), but its strongest upstream attribution is nevertheless the literal `She` token (**+24.63**) and it promotes *herself/she*. In this input and circuit, its functional role is pronoun-sensitive rather than evidence of technical or profession semantics.

Therefore, the circuit supports the user’s concern: the probe direction is substantially aligned with a **spurious gender signal**—“female subject / she-her biography”—and that signal is repeatedly amplified through layers 6, 12, 18, and 19 before entering the probe-score output. The visible substantive text is compatible with a nutrition/wellness profession, but no high-impact inspected feature in the circuit encodes those substantive profession indicators. The main positive evidence recovered is instead gendered pronouns and a generic female-profile framing.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Early pronoun-triggered feature | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Female-reference detector |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Female-reference detector |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Female possessive/pronoun detector | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 29 | Woman/girl mention detector |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Woman/girl mention detector |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 40 | Woman/girl mention detector |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 66 | Woman/girl mention detector |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 29 | Women, roles, or accomplishments detector |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11646 de=0.340 |
| 3 | `inspect_feature` ×4 | L6:11646, L18:14677, L4:7864, L12:12940 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@1` | ❌ error | — | — | Trace this strong positive probe-driving feature to embeddings. Determine whethe… |
| SA-2 | `L18:F14677@29` | ❌ error | — | — | Trace this strong positive probe-driving feature to embeddings. Determine semant… |
| SA-3 | `L4:F7864@1` | ❌ error | — | — | Trace this strong positive probe-driving feature to embeddings, focusing on whet… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F11646@1, k=15 → Emb:"She"@1 (de=19.25) +14 more |
| 2 | `get_upstream_features` | L18:F14677@29, k=15 → Emb:" She"@29 (de=14.38) +14 more |
| 3 | `get_upstream_features` | L12:F12940@2, k=15 → Emb:"She"@1 (de=6.56) +14 more |
| 4 | `get_upstream_features` | L4:F7864@1, k=15 → Emb:"She"@1 (de=24.62) +14 more |
| 5 | `inspect_feature` | L19, F9685 → " references to women's names and their roles or accomplishments." |

### Build

`build_circuit` → 8 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 11,881 | 2,011 | 41,218 | 0 | $0.0702 | — | — |
| **Total** | | **11,881** | **2,011** | **41,218** | **0** | **$0.0702** | | |

**Oracle wall-clock time:** 1m 25s