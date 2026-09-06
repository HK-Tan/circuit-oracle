# Circuit Oracle Report
**Date:** 2026-07-28 07:24:04 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe is driven by genuine professional/affiliation signals — the word "Director" (pos 4), the Ph.D. degree tokens (pos 38/40), and the "Korea University" affiliation (pos 46) — not by spurious gender markers.

**Confidence:** 7

**Reasoning:**

Tracing the top direct-effect features reveals a clean profession-indicating circuit, not a gender-based shortcut:

1. **Strongest single direct driver (L14:F15086, pos 46, de=−0.061)**: traces upstream almost entirely to the "Korea" embedding (de=28.9), with "from" (pos 45, de=−3.7) also contributing. This is a Korea-affiliation feature at the position where the probe reads from.

2. **L6:F3774 (pos 46, de=−0.055)**: also driven by "Korea" (de=18.4) → a "Korea University" entity detector at the prediction position.

3. **L2:F10852 (pos 40, de=−0.052) and L7:F14129 (pos 40, de=+0.044)**: both fire on the "D" token in "Ph.D." (pos 40, embedding de=9.75 and 5.56) plus "Ph" (pos 38). These are Ph.D. credential detectors.

4. **L1:F14934 (pos 7, de=+0.048)**: the "Grid" token (pos 7, "Mobile Grid and Cloud Computing Laboratory") — a research-area indicator.

5. **L0 early features (pos 1–4)**: L0:F1069 ("He", de=+0.042) and L0:F8658 ("He"/"is", de=+0.047) carry the "He is also Director" subject introduction. L0:F4627 and L0:F4621 fire on "Director" (pos 4, emb de=27.5 and 14.6), with negative direct effects — they encode the academic title pattern.

6. **L7–L8 features (pos 11)**: L0:F1242, L0:F5743, L0:F10457, L4:F12934, L7:F5099, L8:F11284 all fire on "Laboratory" (pos 11, emb de up to 18) — research-affiliation evidence.

**Gender signal assessment**: The "He" pronoun (pos 1) is present in the circuit (L0:F1069, L0:F8658), but it is bundled with the much stronger title "Director" at pos 4. The L0 features fire on the whole subject-introduction span (pos 1–4), and the embedding traces show that the "Director" embedding dominates these early features (de=27.5, 18.9, 16.5, 14.6 across multiple L0 features at pos 4) over the "He" embedding (de=22.6 only for L0:F1069, de=8.0 for L0:F8658, and most "He" appearances are small or zero direct_effect).

**Source-influence check**: positions 38/40/46 (Ph.D./Korea) carry S_pct=−4.25% (S_over_R=−0.99, near-sign-magnitude match), while positions 1–4 (subject intro) carry S_pct=0.27%. The profession-specific tokens (Korea, Ph.D., Lab) dominate over the pronoun tokens.

**Conclusion**: The circuit is driven by entity-level professional evidence (title "Director", Ph.D. credential, Korea University affiliation, research laboratory), not by gender. The user's concern about gender-marker shortcuts is not supported by this graph — "He" appears, but it is part of the subject-introduction supernode whose dominant signal is "Director," and the strongest late-layer features fire on affiliation/credential tokens that have no gender content.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: He (pos 1) — masculine pronoun | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: is (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: also (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: Director (pos 4) — title | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: Grid (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: and (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 11 | Emb: Laboratory (pos 11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 38 | Emb: Ph (pos 38) / D (pos 40) — Ph.D. | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 40 | Emb: Ph (pos 38) / D (pos 40) — Ph.D. | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 46 | Emb: Korea (pos 46) — affiliation | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F10846](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10846) | 3 | L0 early lexical features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10846) |
| [L0:F8658](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8658) | 2 | L0 early lexical features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8658) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | L0 early lexical features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F1242](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1242) | 11 | L0 early lexical features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1242) |
| [L0:F15160](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15160) | 7 | L0 early lexical features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15160) |
| [L0:F3255](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) | 8 | L0 early lexical features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) |
| [L0:F5743](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5743) | 11 | L0 early lexical features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5743) |
| [L0:F12904](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12904) | 4 | L0 early lexical features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12904) |
| [L0:F5718](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5718) | 3 | L0 early lexical features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5718) |
| [L0:F4621](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4621) | 4 | L0 early lexical features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4621) |
| [L0:F12208](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12208) | 4 | L0 early lexical features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12208) |
| [L0:F10457](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10457) | 11 | L0 early lexical features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10457) |
| [L1:F14934](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14934) | 7 | L1–L2: subject + title pattern (He is also Director) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14934) |
| [L1:F10132](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) | 40 | L1–L2: subject + title pattern (He is also Director) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 40 | L1–L2: subject + title pattern (He is also Director) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F4627](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4627) | 4 | L1–L2: subject + title pattern (He is also Director) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4627) |
| [L5:F5563](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5563) | 46 | L5–L7: research-affiliation entities (Ph.D., Lab, Korea) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5563) |
| [L5:F13801](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) | 40 | L5–L7: research-affiliation entities (Ph.D., Lab, Korea) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) |
| [L6:F3774](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) | 46 | L5–L7: research-affiliation entities (Ph.D., Lab, Korea) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 40 | L5–L7: research-affiliation entities (Ph.D., Lab, Korea) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 40 | L5–L7: research-affiliation entities (Ph.D., Lab, Korea) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L7:F13010](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13010) | 46 | L5–L7: research-affiliation entities (Ph.D., Lab, Korea) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13010) |
| [L7:F5099](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5099) | 11 | L5–L7: research-affiliation entities (Ph.D., Lab, Korea) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5099) |
| [L8:F11284](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) | 11 | L5–L7: research-affiliation entities (Ph.D., Lab, Korea) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) |
| [L1:F10575](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10575) | 46 | L5–L7: research-affiliation entities (Ph.D., Lab, Korea) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10575) |
| [L4:F12934](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12934) | 11 | L5–L7: research-affiliation entities (Ph.D., Lab, Korea) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12934) |
| [L14:F15086](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/15086) | 46 | L14: late summary (Korea-affiliated Ph.D. Director) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/15086) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:15086 de=-0.061 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F15086@46` | ❌ error | — | — | Trace L14:F15086 at pos 46 upstream to identify what it encodes and which input … |
| SA-2 | `L6:F3774@46` | ❌ error | — | — | Trace L6:F3774 at pos 46 upstream. This is a strong negative direct effect featu… |
| SA-3 | `L0:F10846@3` | ❌ error | — | — | Trace L0:F10846 at pos 3 ("is") upstream. Pos 3 is the "is" token in "He is also… |
| SA-4 | `L0:F1069@1` | ❌ error | — | — | Trace L0:F1069 at pos 1 ("He") upstream. Pos 1 is the "He" pronoun — this is a p… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F15086@46, k=10 → Emb:" Korea"@46 (de=28.88) +9 more |
| 2 | `get_upstream_features` | L6:F3774@46, k=10 → Emb:" Korea"@46 (de=18.38) +9 more |
| 3 | `get_upstream_features` | L7:F14129@40, k=10 → L6:F2254 (de=7.12) +9 more |
| 4 | `get_upstream_features` | L2:F10852@40, k=10 → Emb:" Ph"@38 (de=14.12) +9 more |
| 5 | `get_upstream_features` | L7:F13010@46, k=10 → Emb:" Korea"@46 (de=14.25) +9 more |
| 6 | `get_upstream_features` | L5:F5563@46, k=10 → Emb:" Korea"@46 (de=16.38) +9 more |
| 7 | `get_upstream_features` | L0:F10846@3, k=10 → Emb:" also"@3 (de=33.75) +9 more |
| 8 | `get_upstream_features` | L0:F1069@1, k=10 → Emb:"He"@1 (de=22.62) +9 more |
| 9 | `get_upstream_features` | L1:F14934@7, k=10 → Emb:" Grid"@7 (de=18.25) +9 more |
| 10 | `get_upstream_features` | L2:F4627@4, k=10 → Emb:" Director"@4 (de=27.50) +9 more |
| 11 | `get_upstream_features` | L0:F8658@2, k=10 → Emb:"He"@1 (de=8.00) +9 more |
| 12 | `get_upstream_features` | L0:F12904@4, k=10 → Emb:" Director"@4 (de=16.50) +9 more |
| 13 | `get_upstream_features` | L8:F11284@11, k=10 → Emb:" Laboratory"@11 (de=11.06) +9 more |
| 14 | `get_upstream_features` | L0:F10457@11, k=10 → Emb:" Laboratory"@11 (de=15.75) +9 more |
| 15 | `get_upstream_features` | L0:F1242@11, k=10 → Emb:" Laboratory"@11 (de=18.00) +9 more |
| 16 | `get_upstream_features` | L4:F12934@11, k=10 → Emb:" Laboratory"@11 (de=17.00) +9 more |
| 17 | `get_upstream_features` | L1:F10132@40, k=10 → Emb:" Ph"@38 (de=16.12) +9 more |
| 18 | `get_upstream_features` | L0:F3255@8, k=10 → Emb:" and"@8 (de=37.50) +9 more |
| 19 | `get_upstream_features` | L0:F5743@11, k=10 → Emb:" Laboratory"@11 (de=14.31) +9 more |
| 20 | `get_upstream_features` | L0:F4621@4, k=10 → Emb:" Director"@4 (de=14.56) +9 more |
| 21 | `get_upstream_features` | L1:F10575@46, k=10 → Emb:" Korea"@46 (de=18.00) +9 more |
| 22 | `get_upstream_features` | L0:F15160@7, k=10 → Emb:" Grid"@7 (de=14.06) +9 more |
| 23 | `get_upstream_features` | L0:F5718@3, k=10 → Emb:" is"@2 (de=10.44) +9 more |
| 24 | `get_upstream_features` | L0:F12208@4, k=10 → Emb:" Director"@4 (de=18.88) +9 more |
| 25 | `get_upstream_features` | L6:F2254@40, k=10 → L2:F10852 (de=11.31) +9 more |
| 26 | `get_upstream_features` | L5:F13801@40, k=10 → L2:F10852 (de=6.62) +9 more |
| 27 | `get_source_influence` | {'depth': 2, 'source_positions': [1, 2, 3, 4]} → {'depth': 2, 'source_positions': [1, 2, 3, 4], 'S_pct_of_total': 0.271, 'R_pct_o |
| 28 | `get_source_influence` | {'depth': 2, 'source_positions': [38, 40, 46]} → {'depth': 2, 'source_positions': [38, 40, 46], 'S_pct_of_total': -4.254, 'R_pct_ |
| 29 | `rank_segment_features` | {'k': 15, 'seg_end': 47, 'seg_start': 0} → ❌ This tool requires ctx.sibling_graphs to be set (at least on |
| 30 | `get_candidate_vote_tally` | {} → ❌ This tool requires ctx.sibling_graphs to be set (at least on |

### Build

`build_circuit` → 14 nodes, 22 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 32,265 | 6,078 | 132,192 | 0 | $0.0249 | — | — |
| **Total** | | **32,265** | **6,078** | **132,192** | **0** | **$0.0249** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 19s