# Circuit Oracle Report
**Date:** 2026-07-28 08:38:02 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

{"analysis": "The contradiction probe is driven primarily by spurious syntactic markers of negation and contradiction, rather than a semantic understanding of the prompt's content. Specifically, the probe relies on the detection of 'not only' (L2:F5627) and the specific fragment 'isn't' (L0:F6236), combined with higher-layer negation context detectors (L16:F12358, L16:F15025). The presence of a speech attribution feature (L4:F15629 for 'said') also contributes positively, suggesting the model associates the structure 'Person said X... but Y is not X' with contradiction. The signal flows from raw token fragments to dedicated negation detectors, which then collectively drive the probe's score, confirming the user's concern that the circuit is relying on spurious lexical signals.", "confidence": 9, "reasoning": "The circuit analysis reveals three main paths driving the probe's classification score: \n1. **Negation Token to Detector**: The raw token fragment 't' following 'isn' (L0:F6236) feeds into a high-layer negation context detector (L16:F12358, L16:F15025) which specifically looks for 'not' followed by verbs or pronouns. \n2. **Phrase Matching**: The feature L2:F5627 explicitly detects the phrase 'not only', which is a strong syntactic marker often found in contrasting statements. \n3. **Speech Attribution**: The feature L4:F15629 detects the word 'said', providing a structural cue that a claim is being made, which is then contrasted by the negation signals. \nAll these features are generic syntactic or lexical markers (low frac_nonzero for specific phrases, but general purpose detectors) rather than features encoding the specific entities (e.g., ' Wagonheim' or 'lawyers') or the semantic meaning of the 'public image' claim. This confirms the probe is using 'shortcuts' (spurious features) to predict contradiction based on the presence of negation words and attribution patterns."}

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:15629 de=0.672 |
| 3 | `inspect_feature` ×6 | L4:15629, L2:5627, L0:6236, L16:12358, L16:15025, L3:6227 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 15 features; top: L4:15629 de=0.672 |
| 6 | `inspect_feature` ×5 | L4:15629, L2:5627, L0:6236, L16:12358, L16:15025 |
| 7 | `get_top_logits` | "" (100%) |
| 8 | `get_top_features` | 10 features; top: L4:15629 de=0.672 |
| 9 | `inspect_feature` ×5 | L4:15629, L0:6236, L16:12358, L16:15025, L2:5627 |
| 10 | `get_top_logits` | "" (100%) |
| 11 | `get_top_features` | 10 features; top: L4:15629 de=0.672 |
| 12 | `inspect_feature` ×8 | L4:15629, L4:12337, L2:5627, L0:6236, L16:12358, L16:15025, L15:12905, L3:6227 |
| 13 | `get_top_logits` | "" (100%) |
| 14 | `get_top_features` | 10 features; top: L4:15629 de=0.672 |
| 15 | `inspect_feature` ×5 | L4:15629, L2:5627, L0:6236, L16:12358, L16:15025 |
| 16 | `get_top_logits` | "" (100%) |
| 17 | `get_top_features` | 15 features; top: L4:15629 de=0.672 |
| 18 | `inspect_feature` ×6 | L4:15629, L4:12337, L2:5627, L0:6236, L16:12358, L16:15025 |
| 19 | `get_top_logits` | "" (100%) |
| 20 | `get_top_features` | 10 features; top: L4:15629 de=0.672 |
| 21 | `inspect_feature` ×5 | L4:15629, L4:12337, L2:5627, L16:12358, L16:15025 |
| 22 | `get_top_logits` | "" (100%) |
| 23 | `get_top_features` | 10 features; top: L4:15629 de=0.672 |

### Build

`build_circuit` → 0 nodes, 0 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 2,007,195 | 2,977 | 6 | 0 | $0.2822 | — | — |
| **Total** | | **2,007,195** | **2,977** | **6** | **0** | **$0.2822** | | |

**Oracle wall-clock time:** 7m 19s