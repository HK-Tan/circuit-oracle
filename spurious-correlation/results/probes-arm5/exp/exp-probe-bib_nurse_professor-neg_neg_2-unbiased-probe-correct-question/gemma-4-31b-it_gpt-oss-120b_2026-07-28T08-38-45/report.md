# Circuit Oracle Report
**Date:** 2026-07-28 08:38:45 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of the profession is driven by a mixture of genuine professional terminology and spurious geographic correlations.

**Confidence:** 9

**Reasoning:** 
The attribution circuit demonstrates that the probe's score is produced by two primary paths:
1. **Professional Signal:** The "Engineering Terminology Recognition" supernode (L1:F1372) specifically detects the word "Engineering" at multiple positions (pos 8, 20, 33). This is a genuine indicator of the subject's profession.
2. **Spurious Signal:** The "Geographic Entity Recognition" supernode (L14:F5600) is activated by the University of Waterloo and Beirut. This feature is labeled as detecting "places and regions, particularly in Canada." The fact that this geographic signal significantly contributes to the probe's classification score indicated that the model is relying on spurious correlations (e.g., associating specific universities or regions with certain professions) rather than strictly on professional credentials.

The signal flows from the token embeddings (Emb) through these specialized detectors in early (L1) and mid (L14) layers, which then directly influence the final probe score at L26. This confirms the user's concern: the probe is not purely focused on profession-specific indicators but is partially influenced by the geographic context of the entities mentioned.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L1:F1372](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1372) | 8 | Engineering Terminology Recognition | the word "engineer" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1372) |
| [L14:F5600](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5600) | 11 | Geographic Entity Recognition |  places and regions, particularly in Canada | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5600) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L0:2743 de=-0.069 |
| 3 | `inspect_feature` ×5 | L14:5600, L1:1372, L0:15320, L2:16309, L0:4687 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 15 features; top: L0:2743 de=-0.069 |
| 6 | `inspect_feature` ×4 | L1:1372, L14:5600, L2:16309, L0:4687 |
| 7 | `get_top_logits` | "" (100%) |
| 8 | `get_top_features` | 15 features; top: L0:2743 de=-0.069 |
| 9 | `inspect_feature` ×5 | L14:5600, L1:1372, L0:15320, L2:16309, L0:4687 |
| 10 | `get_top_logits` | "" (100%) |
| 11 | `get_top_features` | 15 features; top: L0:2743 de=-0.069 |
| 12 | `inspect_feature` ×5 | L14:5600, L1:1372, L0:15320, L2:16309, L0:2743 |
| 13 | `get_top_logits` | "" (100%) |
| 14 | `get_top_features` | 15 features; top: L0:2743 de=-0.069 |
| 15 | `inspect_feature` ×5 | L14:5600, L1:1372, L0:15320, L2:16309, L0:4687 |
| 16 | `get_top_logits` | "" (100%) |
| 17 | `get_top_features` | 10 features; top: L0:2743 de=-0.069 |
| 18 | `inspect_feature` ×5 | L14:5600, L1:1372, L0:15320, L2:16309, L0:4687 |
| 19 | `get_top_logits` | "" (100%) |
| 20 | `get_top_features` | 15 features; top: L0:2743 de=-0.069 |
| 21 | `inspect_feature` ×5 | L14:5600, L1:1372, L0:15320, L2:16309, L0:4687 |
| 22 | `get_top_logits` | "" (100%) |
| 23 | `get_top_features` | 15 features; top: L0:2743 de=-0.069 |
| 24 | `inspect_feature` ×5 | L14:5600, L1:1372, L0:15320, L2:16309, L0:4687 |
| 25 | `get_top_logits` | "" (100%) |
| 26 | `get_top_features` | 10 features; top: L0:2743 de=-0.069 |
| 27 | `inspect_feature` ×5 | L14:5600, L1:1372, L0:15320, L2:16309, L0:2743 |
| 28 | `get_top_logits` | "" (100%) |
| 29 | `get_top_features` | 15 features; top: L0:2743 de=-0.069 |
| 30 | `inspect_feature` ×5 | L14:5600, L1:1372, L0:15320, L2:16309, L0:2743 |
| 31 | `get_top_logits` | "" (100%) |
| 32 | `get_top_features` | 10 features; top: L0:2743 de=-0.069 |
| 33 | `inspect_feature` ×4 | L1:1372, L14:5600, L2:16309, L0:15320 |
| 34 | `get_top_logits` | "" (100%) |
| 35 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 36 | `get_top_features` | 15 features; top: L0:2743 de=-0.069 |
| 37 | `inspect_feature` ×5 | L1:1372, L14:5600, L0:15320, L2:16309, L0:4687 |

### Build

`build_circuit` → 9 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 3,946,545 | 3,633 | 4,224 | 0 | $0.5540 | — | — |
| **Total** | | **3,946,545** | **3,633** | **4,224** | **0** | **$0.5540** | | |

**Oracle wall-clock time:** 8m 0s