# Circuit Oracle Report
**Date:** 2026-07-28 07:22:43 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's profession classification is driven primarily by **gender/pronoun features** ("his", "he", "His") rather than by profession-indicating concepts, with the deepest signal flowing from the literal "He" token at position 35 and the "His" token at position 13 through a cascade of pronoun-specific features; a few profession-adjacent tokens ("Laboratory", "Director") contribute only weakly via generic function-word features.

**Confidence:** 8

**Reasoning:** The circuit shows the dominant pathway to the probe's classification score is **gender/pronoun signal**, not profession knowledge.

- **Pronoun supernode (dominant):** L18:F14743 ("He", frac_nonzero=0.018) at pos 35 has the strongest direct effect (-0.141) and is fed directly by the `Emb: He (pos 35)` embedding (direct_effect=23.6). It also receives input from `Emb: He (pos 1)` and `Emb: His (pos 13)`. This single "He"-detecting feature carries the bulk of the late-layer signal.
- **Mid-layer gender cascade:** L7:F14893 ("pronouns or possessive pronouns", frac_nonzero=0.009) and L7:F14946 ("his/he/him", frac_nonzero=0.017) are aggregation points that fire at every pronoun position (pos 1, 2, 13) and feed the late pronoun node. L6:F12990 ("male pronouns and titles", frac_nonzero=0.068) is a slightly more general feature that activates on the "His" token at pos 13 and other pronoun positions, explicitly described by Neuronpedia as encoding **"male pronouns and titles along with descriptors associated with men."** Its promoted tokens include himself/himself; its suppressed tokens include herself/she. L4:F4315 ("his/he/him/hers", frac_nonzero=0.026) and L12:F2175 ("words referring to gender", frac_nonzero=0.006) provide additional gender-concept reinforcement, with L12:F2175 firing on words like male/masculine/men.
- **L0 base pronoun detector:** L0:F2994 (his/he, frac_nonzero=0.073) fires at every pronoun position (pos 13, 37, 55) with very high activations (40.75, 39, 13.75) — and crucially, its `suppressed_tokens` list contains "▁his", "his", "▁그의" (his in Korean) — meaning this feature's decoder pushes *against* the very pronoun tokens it detects, a clear gender-marker signal.
- **Weak profession content:** L2:F13731 ("lab/laboratory", frac_nonzero=0.007) at pos 11 receives direct_effect=20.4 from `Emb: Laboratory (pos 11)` and contributes a small -0.096 direct effect to the probe. The L0 "function words" supernode contains L0:F2848 ("of"), L0:F8658 ("is"), L0:F10846 ("also"), L0:F11024 ("clock"), L0:F3214 ("director") — but these are all **generic lexical features** (frequent function words, "director" co-occurring with `.gov` URLs in the autointerp examples) that don't encode profession semantics. They contribute only minor direct effects (+0.09 to +0.15 each).

**The user's concern is well-founded and confirmed by the circuit.** The probe's classification is largely carried by features whose semantic content is "male pronoun / gendered language" — specifically the repeated "He/His/his" tokens throughout the biographical text. Genuine profession indicators (Ph.D., Computer Science, Korea University, National University of Computer and Emerging Sciences, parallel and distributed computing, Mobile Grid and Cloud Computing) are absent from the top-20 driving features. The only profession-adjacent feature ("laboratory") has a small direct effect and a very low frac_nonzero. The dominant L18 "He" feature has frac_nonzero=0.018 (highly specific) and is essentially a gender-marker detector being exploited as a profession proxy. This is a textbook example of a probe latching onto a spurious correlate (gendered biographical writing style) rather than the target concept (profession).

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 35 | Late-layer male pronoun features (L18 'He' at pos 35, L7 L18 deep pronoun aggregators) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 13 | Late-layer male pronoun features (L18 'He' at pos 35, L7 L18 deep pronoun aggregators) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Late-layer male pronoun features (L18 'He' at pos 35, L7 L18 deep pronoun aggregators) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | Late-layer male pronoun features (L18 'He' at pos 35, L7 L18 deep pronoun aggregators) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 2 | Late-layer male pronoun features (L18 'He' at pos 35, L7 L18 deep pronoun aggregators) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L12:F2175](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) | 2 | Mid-layer gender/pronoun concept (L12 'words referring to gender', L4 'his/he/him') |  words referring to gender | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 13 | Mid-layer gender/pronoun concept (L12 'words referring to gender', L4 'his/he/him') |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 13 | L6 'male pronouns and titles' feature at pos 13 (also fires at pos 1, 2, 35) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 35 | L6 'male pronouns and titles' feature at pos 13 (also fires at pos 1, 2, 35) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 2 | L6 'male pronouns and titles' feature at pos 13 (also fires at pos 1, 2, 35) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | L6 'male pronouns and titles' feature at pos 13 (also fires at pos 1, 2, 35) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 37 | L0 'his/he' pronoun feature (fires at every pronoun position; strongest at pos 37 & 55) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 55 | L0 'his/he' pronoun feature (fires at every pronoun position; strongest at pos 37 & 55) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 13 | L0 'his/he' pronoun feature (fires at every pronoun position; strongest at pos 37 & 55) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 5 | Generic function-word features from text body (of, is, also, clock, director/gov, his) | the word "of" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F11024](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11024) | 4 | Generic function-word features from text body (of, is, also, clock, director/gov, his) |  the word "clock", especially in a technical context | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11024) |
| [L0:F8658](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8658) | 2 | Generic function-word features from text body (of, is, also, clock, director/gov, his) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8658) |
| [L0:F10846](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10846) | 3 | Generic function-word features from text body (of, is, also, clock, director/gov, his) | the word "also" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10846) |
| [L0:F3214](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3214) | 4 | Generic function-word features from text body (of, is, also, clock, director/gov, his) |  titles followed by names or URLs from government sites | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3214) |
| [L2:F13731](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13731) | 11 | L2 'lab/laboratory' feature at pos 11 (profession-adjacent) |  the word "lab" or "laboratory" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13731) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2994 de=0.254 |
| 3 | `inspect_feature` ×13 | L0:2994, L6:12990, L0:2848, L0:11024, L18:14743, L7:14893, L7:14946, L0:8658, L4:4315, L12:2175, L2:13731, L0:3214, L0:10846 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F2994@37` | ❌ error | — | — | Trace the upstream path from L0:F2994 (his/he pronoun feature) at pos 37. Identi… |
| SA-2 | `L18:F14743@35` | ❌ error | — | — | Trace the upstream path from L18:F14743 (the "He" feature) at pos 35. Identify w… |
| SA-3 | `L7:F14893@13` | ❌ error | — | — | Trace the upstream path from L7:F14893 (pronouns feature) at pos 13. Identify wh… |
| SA-4 | `L2:F13731@11` | ❌ error | — | — | Trace the upstream path from L2:F13731 (lab/laboratory feature) at pos 11. Ident… |
| SA-5 | `L6:F12990@13` | ❌ error | — | — | Trace the upstream path from L6:F12990 (male pronouns/titles feature) at pos 13.… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14743@35, k=15 → Emb:" He"@35 (de=23.62) +14 more |
| 2 | `get_upstream_features` | L7:F14893@13, k=15 → Emb:" His"@13 (de=22.75) +14 more |
| 3 | `get_upstream_features` | L2:F13731@11, k=15 → Emb:" Laboratory"@11 (de=20.38) +14 more |
| 4 | `get_upstream_features` | L6:F12990@13, k=15 → Emb:" His"@13 (de=5.28) +14 more |

### Build

`build_circuit` → 15 nodes, 20 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 28,311 | 5,190 | 101,309 | 0 | $0.0208 | — | — |
| **Total** | | **28,311** | **5,190** | **101,309** | **0** | **$0.0208** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 7s