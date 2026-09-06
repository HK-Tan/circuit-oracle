# Circuit Oracle Report
**Date:** 2026-07-28 08:32:23 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is primarily driven by a gender marker feature (L0:F12768) triggered by the token " he", indicating that the model is using gender as a spurious proxy for profession.

**Confidence:** 10/10

**Reasoning:**
The attribution analysis reveals a very simple and problematic circuit. The top feature contributing positively to the probe's classification score is **L0:F12768** (direct effect: 0.0747), which is explicitly labeled as detecting "mentions of 'he' and 'she' in close proximity." Further tracing of this feature upstream via `get_upstream_features` shows that it is driven almost entirely by the embedding of the token **" he"** at position 22 (direct effect: 40.25).

While some features related to the professional context (such as L0:F9297 for "Ministry" and L0:F10881 for "coverage") were active, the most consistent and strongest causal driver identified in the top-features analysis for the probe score was the gender marker. Other top features were either generic (e.g., L0:F7124 for the word "at") or had negative direct effects. This confirms the user's concern: the probe is not identifying "profession" based on occupational evidence, but is instead relying on a gendered pronoun as a shortcut for its classification.

**Circuit Summary:**
- **Emb: " he" (pos 22)** $\rightarrow$ **Gender Marker (L0:F12768)** $\rightarrow$ **Probe Score (L26)**

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 22 | Gender Marker (He/She) |  mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L0:7124 de=-0.157 |
| 3 | `inspect_feature` ×5 | L0:12768, L0:3007, L0:10881, L0:7124, L0:15661 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 15 features; top: L0:7124 de=-0.157 |
| 6 | `inspect_feature` ×6 | L0:12768, L0:3007, L0:10881, L0:9297, L0:7124, L0:15661 |
| 7 | `get_top_logits` | "" (100%) |
| 8 | `get_top_features` | 15 features; top: L0:7124 de=-0.157 |
| 9 | `inspect_feature` ×2 | L0:12768, L0:3007 |
| 10 | `get_upstream_features` | Emb:" he"@22 (de=40.25) +4 more |

### Build

`build_circuit` → 2 nodes, 1 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 445,259 | 1,095 | 0 | 0 | $0.0628 | — | — |
| **Total** | | **445,259** | **1,095** | **0** | **0** | **$0.0628** | | |

**Oracle wall-clock time:** 1m 40s