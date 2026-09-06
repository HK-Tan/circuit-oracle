# Circuit Oracle Report
**Date:** 2026-07-28 07:25:04 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The profession probe score is driven primarily by a spurious male-gender/pronoun signal—especially **“his”** and **“He”**—with a smaller genuine academic-field/degree contribution from *Mathematics*.

**Confidence:** 9/10

**Reasoning:** The saved circuit shows two qualitatively different routes into the **Output: profession-classification probe score**.

1. **Dominant direct male-pronoun route.**  
   **Emb: “his” (pos 3)** directly activates the layer-0 **Male possessive-pronoun detector** (L0:F2994, pos 3). This feature has by far the largest positive direct effect on the probe direction (+0.2969; activation 38.75), and also recurs positively at later occurrences of *his* (e.g. pos 23 and 44). Its interpretation is unusually clear: it detects *“his”* / *“he”*, with `frac_nonzero=0.07326`. Its strongest upstream attribution is the literal *his* embedding at position 3 (+42.5). This is not profession semantics: the probe directly assigns positive weight to a lexical male marker.

2. **Pronoun/gender-context route, with mixed signed effects.**  
   **Emb: “He” (pos 1)** drives a cluster of gender and pronoun features:
   - L6:F12990: male pronouns, titles, and male-associated descriptors (`frac_nonzero=0.06766`; promoted tokens include *himself*; suppressed include *herself*).
   - L7:F14946: *his/he/him* detector (`frac_nonzero=0.01669`; promotes *himself*, *his* and suppresses *herself/she*).
   - L7:F14893: broader possessive-pronoun feature, but its token preferences are relatively female-associated (*herself*, *she*) and it suppresses *his/himself* (`frac_nonzero=0.00885`).

   The attribution signs show that the probe is not simply “detecting pronouns” neutrally: male-coded features L6:F12990 and L7:F14946 have substantial **negative** direct effects on the probe score (roughly −0.13 to −0.17), whereas the more female-associated L7:F14893 contributes **positively** (+0.123 to +0.167). The upstream evidence is direct: *He* at pos 1 contributes +14.75 into L7:F14893 and +7.72 into L7:F14946; *received* at pos 2 also helps establish the sentence-initial “He received…” pattern. Thus, gender is an explicit, high-weight decision axis, even though its net direction is mixed across male vs. female-coded subfeatures.

3. **A real but secondary academic-content route.**  
   The circuit also includes **Emb: “Mathematics” (pos 10)** feeding an **Academic-degree / field-of-study** cluster. L6:F170 is a detector for academic fields (`frac_nonzero=0.03882`) and provides a positive probe contribution (+0.1196). Its strongest upstream source is L5:F10392 at the *Mathematics* position (+11.375), a highly selective feature for fields of academic study (`frac_nonzero=0.00362`; top examples include *science*, *management*, *Administration*, and *literature*). This is a plausible profession-relevant cue: degree and disciplinary-field content can support an academic/computer-science-professor-like classification. However, its direct effect is appreciably smaller than the strongest direct *his* feature.

A later feature, L18:F14743, reinforces the diagnosis: it is an extremely strong *He* detector (`frac_nonzero=0.01809`) and is a major **negative** score driver (−0.1475 at pos 21, −0.1289 at pos 42). Its upstream attribution is dominated by the literal **“He” at position 21** (+23.375), alongside early male-reference feature L0:F1069. This independently confirms that later portions of the biography supply repeated gender signals to the probe.

Overall, the circuit supports the user’s concern. It is **not exclusively spurious**—the *Mathematics/degree/academic-field* pathway is genuine profession-related evidence—but the largest and cleanest positive driver is a direct *his* detector, while several other high-impact pathways encode male/female pronoun distinctions. The linear probe has therefore learned a substantial gender-correlated shortcut rather than relying mainly on occupation indicators such as *Assistant Professor*, *Computer Science*, degree structure, or institutional/employment relations.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 3 | Male possessive-pronoun detector | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Pronoun / gender-context features |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 2 | Pronoun / gender-context features |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Pronoun / gender-context features |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 2 | Pronoun / gender-context features |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 10 | Academic-degree / field-of-study features |  fields of academic study | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 10 | Academic-degree / field-of-study features |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2994 de=0.297 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14743@21` | ❌ error | — | — | Trace this strong negative driver of the synthetic profession-probe score to emb… |
| SA-2 | `L7:F14893@1` | ❌ error | — | — | Trace this strong positive probe-score driver upstream to embeddings; determine … |
| SA-3 | `L6:F12990@21` | ❌ error | — | — | Trace this strong negative score driver to embedding nodes. Identify its semanti… |
| SA-4 | `L0:F2994@3` | ❌ error | — | — | Inspect this dominant layer-0 positive feature and identify exact triggering tok… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×8 | L0:2994, L0:6270, L6:12990, L7:14893, L7:14946, L12:2175, L18:14743, L6:170 |
| 2 | `get_upstream_features` | L18:F14743@21, k=12 → Emb:" He"@21 (de=23.38) +11 more |
| 3 | `get_upstream_features` | L12:F2175@2, k=12 → L7:F14946 (de=4.50) +11 more |
| 4 | `get_upstream_features` | L7:F14946@2, k=12 → Emb:"He"@1 (de=7.72) +11 more |
| 5 | `get_upstream_features` | L7:F14893@1, k=12 → Emb:"He"@1 (de=14.75) +11 more |
| 6 | `get_upstream_features` | L6:F12990@21, k=12 → Emb:" He"@21 (de=4.59) +11 more |
| 7 | `get_upstream_features` | L6:F170@10, k=12 → L5:F10392 (de=11.38) +11 more |
| 8 | `get_upstream_features` | L0:F2994@3, k=12 → Emb:" his"@3 (de=42.50) +11 more |
| 9 | `inspect_feature` ×4 | L5:10392, L0:1069, L17:5889, L13:6622 |
| 10 | `get_upstream_features` | L5:F10392@10, k=12 → L3:F4113 (de=3.34) +11 more |

### Build

`build_circuit` → 7 nodes, 6 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 23,980 | 2,819 | 85,438 | 0 | $0.1236 | — | — |
| **Total** | | **23,980** | **2,819** | **85,438** | **0** | **$0.1236** | | |

**Oracle wall-clock time:** 0m 44s