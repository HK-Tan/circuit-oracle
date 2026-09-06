# Circuit Oracle Report
**Date:** 2026-07-28 07:24:13 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The probe's classification is driven by a mix of causal and spurious features. Causal features capture genuine task content: L2:F16028 (conspiracy theories), L3:F9739 (conspiracy-related words), L5:F559 (legal conspiracies/co-conspirators), L2:F16230 (semiconductor chips), L2:F7725 (card in technical context), L0:F8996 (invest/investment), L0:F44 (Conspiracy/Cons prefix), L0:F14625 (Cons abbreviation), L1:F13292 (personal), L0:F351 (expert), L4:F1248 (brand names), L0:F9026 (technical documents/data). However, several spurious features are prominent: L16:F11298, L15:F13061, L14:F336 all detect the word 'no' or negation — these are likely responding to 'No one thinks...' and represent a surface-level shortcut rather than contradiction reasoning. L2:F8142 combines places with negation, also spurious. L1:F13684 (the word 'theory') likely activates on 'theorists/conspiracy theorists' and is content-relevant but surface-level.

**Verdict:** mixed

**Spurious features:** L16:F11298, L15:F13061, L14:F336, L2:F8142
**Causal features:** L2:F16028, L3:F9739, L5:F559, L2:F16230, L2:F7725, L0:F8996, L0:F44, L0:F14625, L0:F351, L4:F1248, L0:F9026, L1:F13292


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L0:44 de=-0.527 |
| 3 | `inspect_feature` ×25 | L0:44, L0:11375, L0:3635, L0:14574, L4:15764, L0:14625, L5:559, L1:13292, L16:11298, L0:351, L15:13061, L10:16373, L2:16028, L2:16230, L3:9739, L0:2115, L2:8142, L14:336, L2:7725, L1:13684, L0:9026, L4:4515, L4:1248, L0:8996, L2:2415 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,210 | 371 | 370 | 0 | — | — | — |
| **Total** | | **1,210** | **371** | **370** | **0** | **—** | | |
