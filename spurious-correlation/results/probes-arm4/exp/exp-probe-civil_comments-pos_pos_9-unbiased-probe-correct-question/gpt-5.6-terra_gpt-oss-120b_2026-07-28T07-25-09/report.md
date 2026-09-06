# Circuit Oracle Report
**Date:** 2026-07-28 07:25:09 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_9 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity-probe score is driven mostly by direct lexical/topic detectors for *married*, *white*, and *Maybe*, plus an unrelated author/book-context feature—not by a coherent high-level representation of the prompt’s full derogatory claim.

**Confidence:** 7/10

**Reasoning:** The saved circuit has four independently probe-aligned branches:

- **Emb: ` married` (pos 6) → Marriage lexical detector → probe.**  
  L2:F3399 at pos 6 is a very selective marriage feature (`frac_nonzero=0.00393`), with top examples dominated by “married.” Its strongest upstream input is exactly the ` married` embedding, with positive direct effect **29.0**. Despite its generic semantic content, it positively drives the probe (**+0.1748**). Supporting features also show a substantial marriage-family cluster: L3:F6262 (“mentions of marriage,” `frac_nonzero=0.00074`) and L3:F8254 (“marriage and family relationships,” `frac_nonzero=0.00509`). Thus the probe has learned to respond to marriage-related wording, which is not inherently toxic.

- **Emb: ` white` (pos 9) → Explicit “white” detector → probe.**  
  L0:F3436 is an explicit detector for “white” (`frac_nonzero=0.06114`), and it is driven overwhelmingly by the ` white` embedding (direct effect **18.0**). It has a positive direct effect on the toxicity direction (**+0.1719**). This is the clearest evidence supporting the user’s concern: the probe direction directly assigns toxicity-associated weight to a broad identity/race-word feature, rather than requiring that word to occur in a hostile proposition. The underlying prompt *is* racist and misogynistic, so `white` is genuinely relevant here; however, the observed circuit shows a shallow lexical trigger, not a mechanism that specifically represents racial denigration, stereotyping, or dehumanization.

- **Emb: ` Maybe` (pos 17) → Hedging/possibility detector → probe.**  
  L3:F10004 detects uncertainty/possibility language (`frac_nonzero=0.00398`), promotes tokens such as `perhaps`, `maybe`, and `possibly`, and receives a dominant direct upstream contribution of **43.25** from ` Maybe`. It then positively affects the probe (**+0.1387**). This is plainly a stylistic/grammatical feature: hedging itself is not toxicity. It may correlate with speculative attacks in the probe’s training data, but on its own is a spurious predictor.

- **Emb: ` author` (pos 2) → Author/book-context feature → probe.**  
  L6:F2851 is labelled “books and associated things such as authors and reading” (`frac_nonzero=0.01442`), promotes `books`, `book`, and `publishers`, and gets its largest positive upstream contribution from ` author` (**11.06**). Yet it is the largest positive listed feature-to-probe contribution (**+0.2061**). This is especially strong evidence of a non-semantic correlation in the probe: author/book context has no inherent relation to toxicity and does not represent the abusive content of this text.

There are also sizable **negative** direct contributions from generic/lexical features—for example L0:F753 (“author”/selling/prices, **−0.2754**) and a generic `to` feature L0:F8444 (negative at multiple positions). This reinforces that the linear probe direction is a mixture of many lexical axes with arbitrary signed weights, rather than a focused classifier based on a compositional toxicity representation.

Overall, the text is unequivocally toxic because it makes racist and misogynistic generalizations and uses the slur-like phrase “self hater”/“oriental women” in a demeaning frame. But this particular attribution graph does **not** demonstrate that the probe reaches that judgment by encoding the key hostile semantics—e.g., group-directed stereotyping, racialized relationship condemnation, or misogynistic generalization. The strongest positive evidence instead includes identity-adjacent (`white`), generic topical (`married`, `author`), and stylistic (`Maybe`) features. Therefore, the concern is substantially supported: the probe uses spurious lexical/topic signals alongside any unobserved genuine toxicity signal, and the author/book and hedge branches are particularly clear confounds.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L2:F3399](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3399) | 6 | Marriage lexical detector |  words related to marriage | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3399) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 9 | Explicit 'white' detector |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L3:F10004](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10004) | 17 | Hedging/possibility detector |  words which mean or indicate uncertainty or possibility | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10004) |
| [L6:F2851](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2851) | 2 | Author/book-context feature | books and associated things such as authors and reading | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2851) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:753 de=-0.275 |
| 3 | `inspect_feature` ×6 | L6:2851, L2:3399, L0:3436, L0:4408, L3:10004, L3:494 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F2851@2` | ❌ error | — | — | Trace the strongest positive driver of the synthetic toxicity-probe direction to… |
| SA-2 | `L2:F3399@6` | ❌ error | — | — | Trace this strong positive probe driver upstream to embeddings, identifying its … |
| SA-3 | `L3:F10004@17` | ❌ error | — | — | Trace this positive feature affecting the probe score to embeddings; assess its … |
| SA-4 | `L0:F3436@9` | ❌ error | — | — | At layer 0, identify which raw token this direct positive probe feature encodes … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F2851@2, k=20 → Emb:" author"@2 (de=11.06) +19 more |
| 2 | `get_upstream_features` | L2:F3399@6, k=20 → Emb:" married"@6 (de=29.00) +19 more |
| 3 | `get_upstream_features` | L3:F10004@17, k=20 → Emb:" Maybe"@17 (de=43.25) +19 more |
| 4 | `get_upstream_features` | L0:F3436@9, k=20 → Emb:" white"@9 (de=18.00) +19 more |
| 5 | `get_upstream_features` | L0:F753@2, k=20 → Emb:" author"@2 (de=18.38) +19 more |
| 6 | `inspect_feature` ×5 | L0:753, L0:8444, L3:6262, L3:8254, L3:11152 |

### Build

`build_circuit` → 9 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 22,264 | 2,527 | 54,162 | 0 | $0.1071 | — | — |
| **Total** | | **22,264** | **2,527** | **54,162** | **0** | **$0.1071** | | |

**Oracle wall-clock time:** 0m 37s