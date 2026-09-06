# Circuit Oracle Report
**Date:** 2026-07-28 07:25:08 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity-probe score is driven primarily by the early phrase **“Indians are abusers”**, combining a genuine abuse/toxicity lexical signal with a substantial ethnic/national-group representation, rather than by identity alone.

**Confidence:** 8/10

**Reasoning:** The saved circuit has three direct positive routes into the **Output: toxicity-classification probe score**:

- **Abuse lexical detector — L2:F1003 at “abusers”** has a positive direct effect of **+0.3047** on the probe. Its label is *“the word ‘abuse’”* and it is selective (`frac_nonzero=0.00699`). Crucially, its largest upstream source is **Emb: “abusers” (pos 3)**, with a very large positive edge (**+14**), so this is clear lexical evidence from the explicitly derogatory accusation. The identity token also has only a small positive upstream effect (**Emb: Indians, pos 1 = +0.209**) on this feature.

- **Ethnic/national-group representation — L3:F13473 at “are”** has a positive probe effect of **+0.2891**. Its Neuronpedia interpretation is *mentions of racial and ethnic groups, especially in the United States*, and it is also selective (`frac_nonzero=0.00569`). It receives very strong positive attribution from **Emb: “Indians” (pos 1)** (**+10.25**) and from the relational/copular context **Emb: “are” (pos 2)** (**+5.2812**). This is direct evidence that the probe is sensitive to the protected-group mention in the construction “Indians are …,” not merely to later abusive content.

- **Abusive-claim/public-response context — L7:F15690 at “abusers”** provides another positive probe contribution (**+0.2051**). Although its label is broader—*public sentiment and action in response to a problem* (`frac_nonzero=0.07832`)—its upstream sources include **“abusers”** (**+1.680**), **“Indians”** (**+1.234**), and **“are”** (**+0.594**); it also receives a positive input from the ethnic-group feature (**L3:F13473 → L7:F15690, +0.340**). Thus it appears to integrate the group-targeted accusation into a broader hostile/social-conflict frame.

There is also a superficially strong but non-semantic direct route: **L0:F11154**, a detector for *“are”* (`frac_nonzero=0.02939`), contributes **+0.6523** directly to the probe. Its activation is overwhelmingly sourced from **Emb: “are” (pos 2)** (**+36**). This should not be interpreted as toxicity knowledge; it is likely a probe-aligned syntactic/corpus artifact of the early “X are Y” assertion form. In fact, this feature inhibits the ethnic-group feature in the local traced edge (**−1.656**), even though both independently have positive output effects.

The source-influence calculation supports a mixed conclusion. The identity position **“Indians” (pos 1)** carries **10.733% net signed influence**, a substantial share and stronger than the best non-source reference by the supplied metric (`S_over_R=1.77`). The predicate **“are” (pos 2)** contributes a nontrivial **4.225%**, while **“abusers” (pos 3)** has near-zero *net two-hop* influence (**−0.148%**) because of opposing downstream paths—despite its very clear strong local positive lexical edge into L2:F1003. Therefore, the low net figure for “abusers” is not evidence that toxic content is absent; it reflects cancellation in the full signed graph.

Overall, the circuit does **not** support the claim that classification is *solely* a spurious identity detector: the explicit repeated abuse language produces a concrete, selective lexical pathway. But the concern is materially justified: the group label has a large independent causal route through **L3:F13473**, and the probe additionally appears to reward the generic “group + are + negative predicate” construction. The score is best characterized as a blend of actual hostile-content detection and an undesirable identity-associated/group-targeted-claim signal.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F11154](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11154) | 2 | Copula lexical detector: L0:F11154 at 'are' |  the word "are" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11154) |
| [L2:F1003](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1003) | 3 | Abuse lexical detector: L2:F1003 at 'abusers' |  the word "abuse" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1003) |
| [L3:F13473](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13473) | 2 | Ethnic/national-group representation: L3:F13473 at 'are' |  mentions of racial and ethnic groups, especially in the United States | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13473) |
| [L7:F15690](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15690) | 3 | Abusive-claim/public-response context: L7:F15690 at 'abusers' |  text related to public sentiment and action in response to a problem | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15690) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 12 features; top: L0:11154 de=0.652 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F11154@2` | ❌ error | — | — | Trace the strongest positive driver of the synthetic toxicity-probe score to emb… |
| SA-2 | `L2:F1003@3` | ❌ error | — | — | Trace this positive probe-driving path upstream to embeddings. Determine whether… |
| SA-3 | `L3:F13473@2` | ❌ error | — | — | Trace this positive probe-driving path to embeddings and characterize its semant… |
| SA-4 | `L7:F15690@3` | ❌ error | — | — | Deep trace this later positive feature back to embeddings; explain its semantic … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×4 | L0:11154, L2:1003, L3:13473, L7:15690 |
| 2 | `get_upstream_features` | L2:F1003@3, k=20 → Emb:" abusers"@3 (de=14.00) +19 more |
| 3 | `get_upstream_features` | L3:F13473@2, k=20 → Emb:"Indians"@1 (de=10.25) +19 more |
| 4 | `get_upstream_features` | L7:F15690@3, k=20 → Emb:" abusers"@3 (de=1.68) +19 more |
| 5 | `get_upstream_features` | L0:F11154@2, k=20 → Emb:" are"@2 (de=36.00) +19 more |
| 6 | `inspect_feature` ×2 | L0:14740, L0:10155 |
| 7 | `get_source_influence` | {'source_positions': [1], 'depth': 2} → {'depth': 2, 'source_positions': [1], 'S_pct_of_total': 10.733, 'R_pct_of_total' |
| 8 | `get_source_influence` | {'source_positions': [3], 'depth': 2} → {'depth': 2, 'source_positions': [3], 'S_pct_of_total': -0.148, 'R_pct_of_total' |
| 9 | `get_source_influence` | {'source_positions': [2], 'depth': 2} → {'depth': 2, 'source_positions': [2], 'S_pct_of_total': 4.225, 'R_pct_of_total': |
| 10 | `inspect_feature` ×3 | L2:2123, L4:5206, L4:148 |

### Build

`build_circuit` → 8 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 19,541 | 2,460 | 64,466 | 0 | $0.1019 | — | — |
| **Total** | | **19,541** | **2,460** | **64,466** | **0** | **$0.1019** | | |

**Oracle wall-clock time:** 0m 37s