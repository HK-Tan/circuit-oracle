# Circuit Oracle Report
**Date:** 2026-07-28 07:25:16 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_7 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction-probe score is driven mostly by shallow lexical/template features and sentence-position signals, with a smaller but genuine semantic pathway for the *steepled abbey/church* description; the traced circuit does **not** show a dominant explicit negation-comparison mechanism.

**Confidence:** 7/10

**Reasoning:** The output is the synthetic probe target (rather than a vocabulary token), so its feature attributions directly describe the linear contradiction-probe direction.

The strongest positive direct effects include very early, non-semantic lexical features:

- **L0:2848 at pos 4** (“of”; direct effect **+0.1533**, activation 32.75; `frac_nonzero=0.01966`) is driven essentially directly by **Emb: “ of” (pos 4)** (+35.25). Its autointerp examples are ordinary uses of *of*, not contradictions.
- **L0:3820 at pos 5** (“the”; **+0.1426**, activation 26.875; `frac_nonzero=0.0299`) is likewise driven directly by **Emb: “ the” (pos 5)** (+34.25). This is a generic determiner detector.
- **L4:3833 at pos 4** (“plot-summary/courtroom-insight” framing; **+0.1416** at pos 4 and **+0.1270** at pos 3; `frac_nonzero=0.01052`) receives positive input from **Emb: “ glimpse” (pos 3)** (+7.03), **“ first” (pos 2)** (+4.28), and **“ of” (pos 4)** (+3.95). Its top examples suggest narrative/description framing, rather than a contradiction relation.
- **L6:5342 at pos 4** is an explicit *first* / sequence cue (**+0.1226**, `frac_nonzero=0.03652`; promoted tokens include “first,” “First,” “begin,” and “start”). It receives a large contribution from **Emb: “ first” (pos 2)** (+12.06), plus smaller inputs from *glimpse*, L4:3833, and the generic *of* detector.

Thus, the positive side of the probe contains a clear shallow route:
`Emb first/glimpse/of/the → function-word and narrative-frame features → “first” cue → probe`.
This is strong evidence of reliance on stylistic and positional regularities in the first sentence, not solely on a constructed semantic representation of contradiction.

There is, however, a content-sensitive semantic route. At position 9—the final subtoken of *“steepled”*—two L4 features are active:

- **L4:4605** is a church/chapel/building feature (`frac_nonzero=0.00521`; promoted tokens: “church,” “churches,” “chapel”). It has a **negative** probe effect (**−0.1162**).
- **L4:5749** detects ancient settlements/fortifications (`frac_nonzero=0.00542`) and also has a **negative** effect (**−0.1152**).

Both are positively supported by **Emb: “ steep” (pos 8)**, **Emb: “led” (pos 9)**, and **Emb: “ towering” (pos 6)**. This establishes that the model does represent relevant *abbey/steeple/building* content. But, crucially, these features push **against** the displayed probe direction, rather than supplying the main positive contradiction signal. They encode the first claim’s subject/property content, not the cross-sentence comparison to “lacks a steeple.”

The most prominent late-layer positive, **L17:451 at pos 1** (**+0.1177**, activation 55.25; `frac_nonzero=0.00671`), is labeled a **sentence-start detector**. Its upstream signal comes from several mid-layer positional features—notably L15:751 (+6.22), L10:14174 (+5.97), L15:851 (+4.19), and L9:8770 (+3.83)—rather than from the content words identifying the conflicting predicates. Separately, **L8:8406 at pos 1** is an *“I/Exactly” / document-boundary* style feature with the largest negative effect (**−0.1641**) and has a large direct upstream contribution from **Emb: `<bos>`** (+10.69). Together, these late signals reinforce that the probe direction is highly sensitive to sentence/document positioning.

The saved circuit therefore has two qualitatively different branches:

1. **Spurious/template branch:** `<bos>`, *first*, *glimpse*, *of*, and *the* feed sentence-start, narrative-frame, and lexical-order features, which directly influence the probe strongly.
2. **Relevant content branch:** *towering/steepled* feeds sparse church/fortification features, demonstrating semantic recognition of the described attribute, but these are negative contributors to this probe direction and do not visibly combine with an explicit detector for **“not/lacks/no steeple.”**

So the user’s concern is substantially supported: this particular attribution slice shows that the classifier is not principally implementing the desired semantic operation “earlier sentence asserts steeple; later sentence denies it.” It contains relevant lexical-semantic content, but much of the strongest positive evidence is generic framing, function-word, order, and boundary information. Notably, no top driver inspected here is a negation-word feature; the problem is broader than a simple *not* heuristic—it is substantial reliance on non-contradictory prompt-format/lexical correlates.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 4 | Lexical/function-word detectors: “of” and “the” | the word "of" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 5 | Lexical/function-word detectors: “of” and “the” | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L4:F3833](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) | 4 | Narrative/summary framing detector |  words used when summarizing plot points or providing courtroom insights | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) |
| [L6:F5342](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5342) | 4 | “first” lexical/order cue | the word "first" as well as words and prepositions that often follow it | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5342) |
| [L4:F4605](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) | 9 | Church/steepled-building semantic content |  words related to churches, chapels and other buildings, in addition to other information of Lincolnshire | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) |
| [L4:F5749](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) | 9 | Church/steepled-building semantic content |  terms that describe ancient settlements and fortifications | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) |
| [L8:F8406](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) | 1 | Sentence-initial / document-boundary signal | the first-person pronoun "I" and the word "Exactly" | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) |
| [L17:F451](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) | 1 | Late sentence-start detector | start of sentences | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 12 features; top: L8:8406 de=-0.164 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L17:F451@1` | ❌ error | — | — | Trace this positive driver of the contradiction-probe score fully upstream. Dete… |
| SA-2 | `L8:F8406@1` | ❌ error | — | — | Trace this strongest negative driver of the probe score upstream to embeddings; … |
| SA-3 | `L6:F5342@4` | ❌ error | — | — | Trace positive probe-driving feature upstream, identify lexical input origins an… |
| SA-4 | `L4:F3833@4` | ❌ error | — | — | Trace the positive early/mid-layer feature upstream to embeddings and characteri… |
| SA-5 | `L4:F4605@9` | ❌ error | — | — | Trace this negative contribution upstream, characterize the feature, and identif… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×10 | L8:8406, L0:2848, L0:3820, L4:3833, L0:9026, L6:5342, L17:451, L4:4605, L4:5749, L0:7710 |
| 2 | `get_upstream_features` | L4:F4605@9, k=12 → Emb:"led"@9 (de=6.44) +11 more |
| 3 | `get_upstream_features` | L4:F5749@9, k=12 → L2:F5878 (de=2.50) +11 more |
| 4 | `get_upstream_features` | L6:F5342@4, k=12 → Emb:" first"@2 (de=12.06) +11 more |
| 5 | `get_upstream_features` | L17:F451@1, k=12 → L16:F10989 (de=-12.31) +11 more |
| 6 | `get_upstream_features` | L8:F8406@1, k=12 → Emb:"<bos>"@0 (de=10.69) +11 more |
| 7 | `get_upstream_features` | L0:F2848@4, k=8 → Emb:" of"@4 (de=35.25) +7 more |
| 8 | `get_upstream_features` | L0:F3820@5, k=8 → Emb:" the"@5 (de=34.25) +7 more |
| 9 | `get_upstream_features` | L4:F3833@4, k=12 → Emb:" glimpse"@3 (de=7.03) +11 more |

### Build

`build_circuit` → 15 nodes, 20 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 25,659 | 3,234 | 60,930 | 0 | $0.1279 | — | — |
| **Total** | | **25,659** | **3,234** | **60,930** | **0** | **$0.1279** | | |

**Oracle wall-clock time:** 0m 43s