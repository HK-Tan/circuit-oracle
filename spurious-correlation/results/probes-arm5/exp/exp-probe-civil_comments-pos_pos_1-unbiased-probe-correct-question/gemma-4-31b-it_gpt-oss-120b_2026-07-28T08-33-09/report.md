# Circuit Oracle Report
**Date:** 2026-07-28 08:33:09 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity probe is driven by a "Government/Presidential Context" feature (L4:F14582) rather than the toxic lexical content of the prompt.

**Confidence:** 9

**Reasoning:** 
The attribution analysis reveals that the primary positive contributor to the probe's score is feature **L4:F14582** (direct effect: 0.1562). Inspection of this feature shows it is a highly specific detector for **references to the White House and the US government**, with promoted tokens including "Presidential", "Biden", "Trump", and "Obama". 

The signal flows from early-layer representations (Layer 0) into this government-context feature at Layer 4, which then directly drives the probe's classification score. Notably, the circuit does not highlight specific "toxicity" keywords (like "bigot" or "white bigots") as the primary drivers; instead, it relies on the presence of political figures and governmental context. This confirms the user's concern that the probe is using a **spurious correlation**—associating political/identity group mentions with toxicity—rather than identifying the actual hateful semantics of the text.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F7621](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7621) | 1 | Emb: clearly (pos 1) |  the word "clearly", and to a lesser extent words associated with amounts of things | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7621) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 5 | Emb: is (pos 5) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L4:F14582](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14582) | 5 | US Gov/Presidential Context (L4:F14582) |  references to the White House and the US government | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14582) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L0:12866 de=-0.206 |
| 3 | `inspect_feature` ×5 | L0:7621, L4:14582, L0:4422, L0:11375, L0:3916 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 15 features; top: L0:12866 de=-0.206 |
| 6 | `inspect_feature` ×5 | L4:14582, L0:11375, L0:7621, L0:4422, L0:12866 |
| 7 | `get_top_logits` | "" (100%) |
| 8 | `get_top_features` | 15 features; top: L0:12866 de=-0.206 |
| 9 | `inspect_feature` ×5 | L4:14582, L0:7621, L0:11375, L0:4422, L0:12866 |
| 10 | `get_top_logits` | "" (100%) |
| 11 | `get_top_features` | 10 features; top: L0:12866 de=-0.206 |
| 12 | `inspect_feature` | " references to the White House and the US government" |

### Build

`build_circuit` → 4 nodes, 3 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 502,357 | 1,310 | 0 | 0 | $0.0709 | — | — |
| **Total** | | **502,357** | **1,310** | **0** | **0** | **$0.0709** | | |

**Oracle wall-clock time:** 2m 31s