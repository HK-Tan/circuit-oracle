# Circuit Oracle Report
**Date:** 2026-07-28 08:31:46 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity probe is primarily driven by a combination of structural markers (hyphenated "self-" prefixes) and semantic markers of conflict/antagonism, rather than complex toxicity reasoning.

**Confidence:** 8/10

**Reasoning:**
The circuit analysis reveals that the probe's classification score is driven by a relatively shallow path of features:
1. **Structural Detection:** The probe relies on **L3:F735**, which specifically detects words beginning with "self-". This feature fires on "Self-hating" (pos 0) and the hyphen (pos 1).
2. **Conflict/Antagonism Semantic:** This structural signal feeds into **L4:F8407**, a feature associated with "antagonists and fighting." The promoted tokens for this feature include "attacking," "hated," and "Enemy," and its top activating examples include terms like "villain" and "foe."
3. **Identity Interaction:** While the structural "self-hating" signal is strong, the feature **L4:F8407** also receives signal from the embedding of "Jew" (pos 3), suggesting the model associates the identity group in this specific antagonistic context.
4. **Probe Output:** This combination of "self-hyphenation" and "antagonism" (L4:F8407) directly increases the probe's score.

Regarding the user's concern about spurious features: the probe does indeed rely on a fairly generic "antagonist" feature (**L4:F8407**) and a structural pattern ("self-"). While "Jew" contributes, the probe is not performing a deep semantic analysis of "hate speech" but is instead reacting to the presence of conflict-related terminology and a specific prefix pattern often found in pejoratives (like "self-hating"). This suggests the probe may be partially relying on these as proxies for toxicity.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L3:F735](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) | 0 | Self-Hyphen Detector (L3:F735) |  words and phrases that include the word "self" followed by a hyphen | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) |
| [L4:F8407](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) | 0 | Antagonist/Conflict Detector (L4:F8407) |  words related to antagonists and fighting | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:8407 de=0.172 |
| 3 | `inspect_feature` ×7 | L4:8407, L1:2107, L0:2994, L0:8938, L3:735, L0:3090, L0:4336 |
| 4 | `get_top_logits` | "" (100%) |

### Build

`build_circuit` → 6 nodes, 5 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 95,637 | 981 | 0 | 0 | $0.0138 | — | — |
| **Total** | | **95,637** | **981** | **0** | **0** | **$0.0138** | | |

**Oracle wall-clock time:** 1m 5s