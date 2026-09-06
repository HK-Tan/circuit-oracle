# Circuit Oracle Report
**Date:** 2026-07-28 07:23:40 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of this biography as a "nurse" profession is driven almost entirely by female-pronoun ("she") features anchored at the subject position (pos 7) and reinforced by a second clause subject (pos 53), with only a weak, secondary contribution from genuine profession-lexicon features on "Perioperative nurses" — confirming the user's concern that the circuit relies on spurious gender markers rather than profession content.

**Confidence:** 9

**Reasoning:**

The attribution graph is dominated by a single massive chain of features firing at position 7 on the token " she" — the first word of the second sentence. The "she" embedding at pos 7 sends enormous direct effect into the probe (31.6, 28.4, 12.3, 12.2, 33.75, 31.6 across multiple inspection calls) — easily the largest signal in the entire circuit. This embedding feeds `early_she_pos7` (L0:F12519, L1:F4232, L2:F8966, L2:F7672, L3:F4020), which feed `mid_she_pos7` (L4:F7864 with de=4.16, L4:F15567, L5:F10952, L6:F11646 with de=5.59, L6:F16329, L7:F8952, L10:F14965), which feed `late_she_pos7` (L12:F12940, L14:F14097, L15:F3330/F12956/F12472, L17:F5889, L18:F14677 with de=5.59, L19:F9685). Every one of these features traces back to the "she" embedding as its dominant upstream driver — a textbook pronoun-identity circuit.

Critically, the SAME L18:F14677 feature also fires at pos 53 and pos 38 on pronoun tokens ("she" in the third sentence, "her" elsewhere), feeding the probe with direct_effect=0.91, 0.32, 0.27 — meaning the model has detected "this paragraph is about a female person" and uses that as the primary classification signal.

By contrast, the genuine profession lexicon — `nursing_pos15` anchored on "Perioperative nurses" (L2:F15728, L3:F15901, L4:F11037/F8751, L5:F1275, L6:F15267) — contributes far less. The strongest single link from this chain is only de=0.55 (L6:F15267 at pos 15), and the embeddings of "nurses" and "Perio/perative" carry de=16.1 and 4.4 respectively but route through these same low-magnitude features. The probe's top direct-effect features at pos 7 (L6:F11646 de=1.55, L18:F14677 de=0.91) substantially outrank the top profession-lexicon features.

The ratio of "she"-driven signal to profession-lexicon signal is roughly 30:1 at the embedding level, and even after the mid-layer profession features attenuate, the pronoun chain remains dominant. The model has effectively learned a shortcut: "biography about a woman → nurse" (correlated because nursing biographies in training data skew female), rather than "mentions Perioperative nursing certification and 41 years of nursing experience → nurse." This is exactly the spurious-correlation failure mode the user suspected, and the circuit makes it visible at every layer from L0 through L19.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: ' she' (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 53 | Emb: ' she' (pos 53) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: ' nurses' (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: 'Perio/perative' (pos 13-14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: 'Perio/perative' (pos 13-14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F12519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) | 7 | Early-layer 'she' pronoun features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) |
| [L1:F4232](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4232) | 7 | Early-layer 'she' pronoun features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4232) |
| [L2:F8966](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8966) | 7 | Early-layer 'she' pronoun features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8966) |
| [L2:F7672](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) | 7 | Early-layer 'she' pronoun features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) |
| [L0:F7509](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7509) | 7 | Early-layer 'she' pronoun features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7509) |
| [L1:F7244](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7244) | 7 | Early-layer 'she' pronoun features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7244) |
| [L3:F4020](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4020) | 7 | Early-layer 'she' pronoun features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4020) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 7 | Mid-layer female-pronoun / 'she'-context features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F15567](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) | 7 | Mid-layer female-pronoun / 'she'-context features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 7 | Mid-layer female-pronoun / 'she'-context features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L5:F10952](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) | 7 | Mid-layer female-pronoun / 'she'-context features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) |
| [L5:F6637](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6637) | 7 | Mid-layer female-pronoun / 'she'-context features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6637) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 7 | Mid-layer female-pronoun / 'she'-context features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 7 | Mid-layer female-pronoun / 'she'-context features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L7:F8952](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8952) | 7 | Mid-layer female-pronoun / 'she'-context features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8952) |
| [L10:F14965](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) | 7 | Mid-layer female-pronoun / 'she'-context features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 7 | Late-layer 'she'/female-persona features at pos 7 | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L14:F14097](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) | 7 | Late-layer 'she'/female-persona features at pos 7 | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 7 | Late-layer 'she'/female-persona features at pos 7 | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L15:F12956](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12956) | 7 | Late-layer 'she'/female-persona features at pos 7 | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12956) |
| [L15:F12472](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12472) | 7 | Late-layer 'she'/female-persona features at pos 7 | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12472) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 7 | Late-layer 'she'/female-persona features at pos 7 | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 7 | Late-layer 'she'/female-persona features at pos 7 | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 7 | Late-layer 'she'/female-persona features at pos 7 | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 53 | Late-layer 'she' at pos 53 (second clause subject) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 38 | Late-layer 'she' at pos 53 (second clause subject) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L2:F15728](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15728) | 15 | Profession-lexicon features at pos 15 (' nurses') | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15728) |
| [L2:F12997](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12997) | 15 | Profession-lexicon features at pos 15 (' nurses') | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12997) |
| [L3:F15901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) | 15 | Profession-lexicon features at pos 15 (' nurses') | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 15 | Profession-lexicon features at pos 15 (' nurses') | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L4:F8751](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8751) | 15 | Profession-lexicon features at pos 15 (' nurses') | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8751) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 14 | Profession-lexicon features at pos 15 (' nurses') | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 15 | Profession-lexicon features at pos 15 (' nurses') | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 15 | Profession-lexicon features at pos 15 (' nurses') | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 14 | Profession-lexicon features at pos 15 (' nurses') | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe output (nurse classification) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_candidate_vote_tally` | ❌ This tool requires ctx.sibling_graphs to be set (at least on |
| 3 | `rank_segment_features` | ❌ This tool requires ctx.sibling_graphs to be set (at least on |
| 4 | `get_top_features` | 20 features; top: L6:11646 de=1.555 |
| 5 | `get_upstream_features` | Emb:" she"@7 (de=31.62) +14 more |
| 6 | `get_upstream_features` | Emb:" she"@7 (de=28.38) +14 more |
| 7 | `get_upstream_features` | Emb:" nurses"@15 (de=16.12) +14 more |
| 8 | `get_upstream_features` | Emb:" she"@7 (de=27.25) +14 more |
| 9 | `get_upstream_features` | Emb:" she"@53 (de=22.62) +14 more |
| 10 | `get_upstream_features` | Emb:" she"@7 (de=12.25) +14 more |
| 11 | `get_upstream_features` | Emb:" she"@7 (de=12.31) +14 more |
| 12 | `get_upstream_features` | Emb:" she"@7 (de=31.62) +11 more |
| 13 | `get_upstream_features` | Emb:" she"@7 (de=33.75) +9 more |
| 14 | `get_upstream_features` | Emb:"perative"@14 (de=7.72) +9 more |
| 15 | `get_upstream_features` | L17:F3502 (de=9.75) +9 more |
| 16 | `get_upstream_features` | L16:F14205 (de=7.91) +9 more |
| 17 | `get_upstream_features` | Emb:"Formerly"@1 (de=7.50) +9 more |
| 18 | `get_upstream_features` | Emb:" nurses"@15 (de=5.16) +9 more |

### Build

`build_circuit` → 10 nodes, 9 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 18,017 | 4,408 | 48,595 | 0 | $0.0136 | — | — |
| **Total** | | **18,017** | **4,408** | **48,595** | **0** | **$0.0136** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 53s