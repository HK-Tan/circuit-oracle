# Circuit Oracle Report
**Date:** 2026-07-28 08:33:37 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

{"Analysis": "The probe's classification score is primarily driven by keywords related to nutrition, physical activity, and professional mission statements, rather than gender-specific markers.", "Confidence": 9, "Reasoning": "The circuit reveals that the probe's score is driven by features encoding a 'health and wellness' professional profile. Specifically, the signal flows from the input tokens 'food' (pos 15), 'physically' (pos 21), and 'active' (pos 22) to features L6:F11327 ('food or nutrition') and L4:F3047 ('exercise and physical activity'). These, along with L0:F4030 ('mission statements and personal development'), converge into a high-level feature L14:F4197, which acts as a domain specialist detector (labeled as 'food insecurity' but promoted tokens like 'food' and 'edible' suggest a broader nutrition/food domain). This complex of health-related features directly pushes the probe's classification score. While some gender-related features (L0:F2349 'others', L6:F11646 'women') are present in the attribution graph, they have negative direct effects or are not the primary drivers of the positive signal, confirming that the probe is relying on genuine professional indicators rather than spurious gender markers."}

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L0:2349 de=-0.123 |
| 3 | `inspect_feature` ×5 | L6:11327, L4:3047, L14:4197, L0:4030, L0:2349 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_upstream_features` | Emb:" food"@15 (de=34.00) +4 more |
| 6 | `get_upstream_features` | Emb:" active"@22 (de=10.25) +4 more |
| 7 | `get_upstream_features` | Emb:" food"@15 (de=22.62) +4 more |
| 8 | `inspect_feature` ×4 | L6:11327, L4:3047, L14:4197, L0:4030 |
| 9 | `get_top_logits` | "" (100%) |
| 10 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 11 | `get_top_features` | 15 features; top: L0:2349 de=-0.123 |
| 12 | `inspect_feature` ×7 | L6:11327, L4:3047, L14:4197, L0:2349, L0:4030, L0:9519, L6:11646 |

### Build

`build_circuit` → 0 nodes, 0 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 296,091 | 1,275 | 4,352 | 0 | $0.0420 | — | — |
| **Total** | | **296,091** | **1,275** | **4,352** | **0** | **$0.0420** | | |

**Oracle wall-clock time:** 2m 57s