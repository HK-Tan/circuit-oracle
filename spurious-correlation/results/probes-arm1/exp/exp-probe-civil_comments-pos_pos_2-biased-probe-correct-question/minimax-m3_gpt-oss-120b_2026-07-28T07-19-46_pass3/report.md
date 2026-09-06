# Circuit Oracle Report
**Date:** 2026-07-28 07:19:46 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity score is driven almost entirely by a stack of race/ethnicity identity-token detectors that fire on the literal words "white" and "Hispanic", with the upstream circuit tracing cleanly from those token embeddings into a single L6 race-terms feature (L6:F3902) that pushes the probe positively, plus a weaker contribution from a controversial-race-issues feature at L11.

**Confidence:** 8

**Reasoning:** The signal flow begins at three input-token embeddings: "was" (pos 3, direct_effect 36.75 into L0:F2458), "white" (pos 4), and "Hispanic" (pos 7). The "Hispanic" embedding is the single largest direct driver of the L6 race-ethnicity feature (direct_effect 12.81 into L6:F3902@pos7), and "white" contributes 2.69 directly plus 14.75 into L4:F117 (race/racism/Black social-justice) at pos 4. These embeddings are read out by token-level detectors — L2:F585 ("white", frac_nonzero 0.0047), L2:F13158 (race/ethnicity words, frac_nonzero 0.0099), and L0:F2458 ("was", frac_nonzero 0.025) — which then feed a converging mid-layer circuit: L2:F13158 → L4:F117 → L6:F3902, the dominant positive path with cumulative direct_effect ~0.57 into the probe. L6:F3902 (frac_nonzero 0.018) is labeled "terms referring to race and ethnicity" and promotes tokens like "minorities", "ethnicity", "Hispanic" — i.e., it is a generic identity-group signal, not a toxicity-specific feature. The downstream L11:F1913 ("emotional, controversial, or political issues especially relating to race", frac_nonzero 0.0033) adds a smaller positive push (direct_effect 0.15). Two features actively push the probe DOWN: L7:F8030 (races/origins/demographic groups, direct_effect −0.24) and L3:F3248 (race/ethnic social-issues, direct_effect −0.18), but they are outweighed. Notably, L0:F2458 ("was", direct_effect −0.66) is the single largest MAGNITUDE feature in the graph but acts as a SUPPRESSOR, which is consistent with the probe being a generic mid-layer direction rather than a lexically meaningful detector. No features in the positive-driving path encode "slur", "insult", "harm", or any toxicity-specific concept — every positively-contributing feature is either a race/ethnicity identity-term detector, a "was"/"and" generic function-word detector, or an "emotional/controversial political race" feature. The circuit is consistent with the user's concern: the probe classifies this text using identity-group lexical signals and a generic controversy-around-race signal, not because the model's residual stream at this layer encodes a coherent notion of toxicity from the sentence's content. The factual claim "white and Hispanic" is a neutral descriptive conjunction ("If he was white and not Hispanic…"), yet the probe sees strong activation simply because race/ethnicity identity terms are present.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2458](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2458) | 3 | L0:F2458 'was' |  the word "was" and sometimes "were." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2458) |
| [L0:F3255](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) | 5 | L0:F3255 'and' |  the word "and" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) |
| [L2:F585](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) | 4 | L2:F585 'white' token detector | the word "white", often in association with "dwarf" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 7 | L2:F13158 race/ethnicity words |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 4 | L2:F13158 race/ethnicity words |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L3:F3248](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3248) | 7 | L3:F3248 race/ethnic social issues (suppressing) |  words and phrases related to race and ethnic groups, especially in the context of social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3248) |
| [L3:F3248](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3248) | 4 | L3:F3248 race/ethnic social issues (suppressing) |  words and phrases related to race and ethnic groups, especially in the context of social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3248) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 4 | L4:F117 race/racism/Black social justice |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 7 | L4:F117 race/racism/Black social justice |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 5 | L4:F117 race/racism/Black social justice |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F10174](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10174) | 7 | L4:F10174 racial/supernatural identity |  words referring to racial and/or supernatural identity | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10174) |
| [L5:F3924](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3924) | 7 | L5:F3924 race/ethnicity/religion (inhibitory) |  words relating to race, ethnicity, and/or religion | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3924) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 7 | L6:F3902 race & ethnicity terms |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 4 | L6:F3902 race & ethnicity terms |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L7:F8030](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8030) | 4 | L7:F8030 races/origins/demographic groups (inhibitory) |  words about people's races, origins, and demographic groups | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8030) |
| [L7:F8030](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8030) | 7 | L7:F8030 races/origins/demographic groups (inhibitory) |  words about people's races, origins, and demographic groups | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8030) |
| [L11:F1913](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/1913) | 5 | L11:F1913 emotional/controversial/political race issues |  emotional, controversial, or political issues especially relating to race | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/1913) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2458 de=-0.660 |
| 3 | `inspect_feature` ×4 | L6:3902, L2:13158, L4:117, L0:2458 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F3902@7` | ❌ error | — | — | Trace upstream from L6:F3902 at pos 7. This feature detects race/ethnicity terms… |
| SA-2 | `L2:F13158@7` | ✅ reported | 4 | 8 | Trace upstream from L2:F13158 at pos 7. This feature detects race/ethnicity word… |
| SA-3 | `L0:F2458@3` | ❌ error | — | — | Trace upstream from L0:F2458 at pos 3. This is "the word 'was'". What other feat… |

<details>
<summary><b>SA-2</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 2 | `get_upstream_features` | L2:F13158@7, k=10 | Emb:" Hispanic"@7 (de=11.12) +9 more |
| 3 | `inspect_feature` | L1, F12717 | " words or phrases related to education" |
| 4 | `get_upstream_features` | L1:F12717@7, k=10 | Emb:" Hispanic"@7 (de=9.06) +9 more |
| 5 | `inspect_feature` | L0, F1847 | "scientific terms and experimental details related to biological and ch" |
| 6 | `get_upstream_features` | L0:F1847@7, k=10 | Emb:" Hispanic"@7 (de=5.66) +9 more |
| 7 | `inspect_feature` | L0, F6548 | " the word "national"" |

**Findings:** The race/ethnicity detector (L2:F13158) receives its strongest excitatory drive directly from the input embedding of the token "Hispanic" at position 7 (direct_effect ≈ 11). Additional support comes from the token "white" and from upstream features in layers 1 and 0 that are themselves excited by the same "Hispanic" token. The traced path reaches an embedding node (satisfying condition b) and incl…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F3902@7, k=10 → Emb:" Hispanic"@7 (de=12.81) +9 more |
| 2 | `get_upstream_features` | L0:F2458@3, k=8 → Emb:" was"@3 (de=36.75) +7 more |
| 3 | `get_upstream_features` | L4:F117@4, k=8 → Emb:" white"@4 (de=14.75) +7 more |
| 4 | `inspect_feature` ×5 | L2:585, L5:3924, L4:10174, L7:8030, L3:3248 |
| 5 | `get_upstream_features` | L7:F8030@4, k=8 → L6:F3902 (de=5.62) +7 more |
| 6 | `inspect_feature` ×2 | L0:3255, L11:1913 |

### Build

`build_circuit` → 15 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 25,522 | 3,986 | 100,601 | 0 | $0.0185 | — | — |
| SA-2 | openai/gpt-oss-120b | 71,151 | 6,408 | 7,616 | 0 | $0.0146 | ✅ 4F/8E | Trace upstream from L2:F13158 at pos 7. This feature detects… |
| **Total** | | **96,673** | **10,394** | **108,217** | **0** | **$0.0331** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 16s