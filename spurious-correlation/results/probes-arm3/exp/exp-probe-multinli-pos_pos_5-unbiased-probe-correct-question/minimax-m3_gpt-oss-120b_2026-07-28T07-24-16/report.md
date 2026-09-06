# Circuit Oracle Report
**Date:** 2026-07-28 07:24:16 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The circuit is driven by a mix of genuine task content and superficial lexical cues. Several features capture the core semantic content of the premise/hypothesis pair: L2:F13565 ('program(me)s'), L4:F12847 (reporting verbs with 'that'), L4:F6000 ('program' and plural), L0:F15461 (court proceedings), L4:F4080 (legal documents), and L4:F14393 (direct quotes/reports) reflect the actual NLI premise about a legal program. However, multiple high-impact features are clearly shortcut/negation cues that do not encode the contradiction itself: L0:F1910 ('not only'), L16:F7295 ('but also'), L17:F3763 ('only'), L15:F12905 and L4:F5347 ('but'), L0:F2961 (qualifications/negations like 'necessarily'), and L0:F8046 ('will'). The most negatively-weighted feature (L15:F12905, 'but') and the positive 'not only'/'but also' pair are classic NLI surface cues that a shallow model could exploit, while the actual contradiction ('isn't going to') receives no dedicated feature. This indicates the probe is leaning on correlational/lexical contrast markers rather than full contradiction reasoning, but the program/legal-topic features do contribute genuine content.

**Verdict:** mixed

**Spurious features:** L15:F12905, L0:F1910, L16:F7295, L17:F3763, L4:F5347, L0:F2961, L0:F8046
**Causal features:** L2:F13565, L4:F12847, L4:F6000, L0:F15461, L4:F4080, L4:F14393, L3:F2782, L5:F7144


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L15:12905 de=-0.355 |
| 3 | `inspect_feature` ×23 | L15:12905, L0:8046, L5:7144, L2:13565, L4:12847, L3:2782, L0:15525, L17:3763, L1:1500, L0:6131, L1:11907, L12:12606, L4:6000, L10:6670, L0:2961, L4:5347, L1:1090, L0:1910, L16:7295, L0:15461, L9:12274, L4:4080, L4:14393 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,171 | 403 | 370 | 0 | — | — | — |
| **Total** | | **1,171** | **403** | **370** | **0** | **—** | | |
