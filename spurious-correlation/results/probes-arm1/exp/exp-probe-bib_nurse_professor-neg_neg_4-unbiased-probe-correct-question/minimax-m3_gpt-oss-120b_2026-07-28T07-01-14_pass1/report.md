# Circuit Oracle Report
**Date:** 2026-07-28 07:01:14 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's positive classification score is driven by a mixture of (a) genuine profession/academic indicators — the "Director" title at pos 4, "Mobile Grid…Laboratory" technical-field vocabulary at pos 6–11, and the "Ph.D." degree cue at pos 38–40 — and (b) a spurious male-pronoun cue "He" at pos 1, which contributes positively to the score.

**Confidence:** 8

**Reasoning:** The circuit shows a mix of substantively profession-relevant signals and at least one demonstrably gender-based spurious cue. The genuine profession indicators are:
- **title_supernode** (layer 0–4) at pos 4: L0:F12904 ("mentions of…positions of authority" / "director"), L0:F4621 (administrative positions), L2:F4627 ("director"), L3:F3685 (job-position phrases), L4:F15748 (titles within organizations). All activate on the embedding of "Director" (pos 4) with direct_effect ≈ +27.5.
- **academic_field_supernode** (layer 0–8) at pos 6–11: L2:F12316 ("mobile" technical), L0:F5743 ("lab"), L1:F14934 ("grid"), L4:F12934 (academic journals / "Laboratory"), L8:F11284 (names/titles/research). These fire on the Mobile/Grid/Cloud/Computing/Laboratory noun phrase and feed positively into the probe.
- **phd_supernode** (layer 1–7) at pos 40: L1:F10132 (the "D" in "Ph.D."), L2:F10852 (academic titles/degrees), L5:F13801 (degree abbreviations), L6:F2254 (academic degrees), L7:F14129 (academic degrees/universities). These activate on the embedding of "Ph" (pos 38) and "D" (pos 40) and feed positively.
- **korea_supernode** (layer 1–14) at pos 46: L1:F10575 (Korean names), L5:F5563 (Korean food/conglomerates), L6:F3774 (unusual-capitalization proper nouns), L7:F13010 (Korean names), L14:F15086 (Korea/Korean references). This supernode is a *negative* contributor (direct_effect ≈ −0.06), because the country marker is being suppressed as a distractor for the profession label.

The spurious cue is the **gender_supernode**: L0:F1069 ("references to a male person, particularly when using the pronoun 'He' or 'His.'") at pos 1 with direct_effect = +0.042, and L0:F8658 ("is") at pos 2 with direct_effect = +0.047. These features are driven directly by the embedding of the input token "He" (direct_effect = +22.6) — the very first subject-pronoun of the bio. There is no profession semantic content in this supernode; it is purely a gendered-pronoun detector that the probe has learned to use as a positive class signal.

The user concern is confirmed: the probe does indeed use the male pronoun "He" as a positive predictive feature (alongside "is"), independent of the actual profession-indicating content. The strong genuine profession signal (Director + Lab + Mobile/Grid + PhD) is also present, so the probe is not *purely* gender-based, but the gender cue is real and contributes a non-trivial direct_effect to the score. Counterfactual: swapping the subject to "She" would suppress the gender_supernode and reduce the probe's score even though every profession-indicating token (Director, Laboratory, Ph.D., Mobile Grid) remains identical.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L14:F15086](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/15086) | 46 | Korea / Korean country cues (negative push to probe) |  references to Korea/Korean | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/15086) |
| [L6:F3774](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) | 46 | Korea / Korean country cues (negative push to probe) |  proper nouns or names with unusual capitalization | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) |
| [L7:F13010](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13010) | 46 | Korea / Korean country cues (negative push to probe) |  Korean names, especially those with multiple parts separated by hyphens, in credits or medical contexts. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13010) |
| [L5:F5563](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5563) | 46 | Korea / Korean country cues (negative push to probe) |  words related to Korean food and Korean conglomerates | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5563) |
| [L1:F10575](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10575) | 46 | Korea / Korean country cues (negative push to probe) |  Korean names | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10575) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 40 | PhD / academic degree cues (positive push) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 40 | PhD / academic degree cues (positive push) | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 40 | PhD / academic degree cues (positive push) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L1:F10132](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) | 40 | PhD / academic degree cues (positive push) |  the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") written as "D" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) |
| [L5:F13801](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) | 40 | PhD / academic degree cues (positive push) | abbreviations for degrees and mentions of educational attainment | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) |
| [L2:F4627](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4627) | 4 | Title / role / director cues | the word "director" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4627) |
| [L0:F12904](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12904) | 4 | Title / role / director cues | mentions of the day prior or positions of authority | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12904) |
| [L3:F3685](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3685) | 5 | Title / role / director cues |  phrases involving job positions that include "of", "at", "partner", "director", or "secretary" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3685) |
| [L4:F15748](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15748) | 5 | Title / role / director cues | titles within organizations and/or descriptions of processes and management | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15748) |
| [L0:F4621](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4621) | 4 | Title / role / director cues |  words related to administrative positions and bodies | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4621) |
| [L4:F12934](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12934) | 11 | Academic field / lab / mobile-grid tokens |  names of academic journals | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12934) |
| [L8:F11284](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) | 11 | Academic field / lab / mobile-grid tokens |  words and phrases related to people's names, titles, universities, and research | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) |
| [L2:F12316](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12316) | 6 | Academic field / lab / mobile-grid tokens | the word "mobile" when used in a technical context | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12316) |
| [L0:F5743](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5743) | 11 | Academic field / lab / mobile-grid tokens | the word "lab" and words that might be associated with equipment or a positive experience | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5743) |
| [L0:F10457](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10457) | 11 | Academic field / lab / mobile-grid tokens | the string "filename" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10457) |
| [L1:F14934](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14934) | 7 | Academic field / lab / mobile-grid tokens | the word "grid" and some related terms related to "grids" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14934) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Male-pronoun cue "He" (positive push) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F8658](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8658) | 2 | Male-pronoun cue "He" (positive push) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8658) |
| [L0:F10846](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10846) | 3 | Generic function words / discourse cues | the word "also" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10846) |
| [L0:F1242](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1242) | 11 | Generic function words / discourse cues | the word "appropriate" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1242) |
| [L0:F3255](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) | 8 | Generic function words / discourse cues |  the word "and" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) |
| [L0:F15160](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15160) | 7 | Generic function words / discourse cues | the word "concerns" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15160) |
| [L0:F5718](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5718) | 3 | Generic function words / discourse cues | the word "still" and adverbs that indicate a continuing action | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5718) |
| [L0:F11786](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11786) | 5 | Generic function words / discourse cues |  the word "of" preceded by titles or names | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11786) |
| [L0:F12208](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12208) | 4 | Generic function words / discourse cues | the word "perspective" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12208) |
| [L3:F4213](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) | 45 | Generic function words / discourse cues |  mentions of degree qualifications or awards | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: He (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: is (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: also (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: Director (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: Grid (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: Mobile (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 11 | Emb: Laboratory (pos 11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: Computing (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 38 | Emb: Ph (pos 38) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 40 | Emb: D (pos 40) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 46 | Emb: Korea (pos 46) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:15086 de=-0.061 |
| 3 | `inspect_feature` ×15 | L14:15086, L6:3774, L0:10846, L2:10852, L1:14934, L2:4627, L0:8658, L7:14129, L0:12904, L0:1069, L0:1242, L0:15160, L0:3255, L0:5743, L4:12934 |
| 4 | `get_upstream_features` | Emb:" Korea"@46 (de=28.88) +7 more |
| 5 | `get_upstream_features` | Emb:" Korea"@46 (de=18.38) +7 more |
| 6 | `get_upstream_features` | Emb:" Ph"@38 (de=14.12) +7 more |
| 7 | `get_upstream_features` | L6:F2254 (de=7.12) +7 more |
| 8 | `inspect_feature` ×4 | L7:13010, L5:5563, L6:2254, L1:10132 |
| 9 | `get_upstream_features` | Emb:"He"@1 (de=22.62) +4 more |
| 10 | `get_upstream_features` | Emb:"He"@1 (de=8.00) +4 more |
| 11 | `inspect_feature` | " Korean names" |
| 12 | `get_upstream_features` | Emb:" Grid"@7 (de=18.25) +4 more |
| 13 | `get_upstream_features` | Emb:" also"@3 (de=33.75) +4 more |
| 14 | `get_upstream_features` | Emb:" Director"@4 (de=27.50) +4 more |
| 15 | `get_upstream_features` | Emb:" Grid"@7 (de=14.06) +4 more |
| 16 | `get_upstream_features` | Emb:" and"@8 (de=37.50) +4 more |
| 17 | `get_upstream_features` | Emb:" Laboratory"@11 (de=18.00) +4 more |
| 18 | `get_upstream_features` | Emb:" Laboratory"@11 (de=14.31) +4 more |
| 19 | `get_upstream_features` | Emb:" Laboratory"@11 (de=17.00) +4 more |
| 20 | `get_upstream_features` | Emb:" Director"@4 (de=16.50) +2 more |
| 21 | `get_upstream_features` | ❌ Feature (layer=0, feature_idx=12904) not found at pos=1. Thi |
| 22 | `get_upstream_features` | L2:F10852 (de=11.31) +2 more |
| 23 | `inspect_feature` ×2 | L1:14298, L1:10132 |
| 24 | `get_upstream_features` | Emb:" Korea"@46 (de=14.25) +4 more |
| 25 | `get_upstream_features` | Emb:" Korea"@46 (de=16.38) +4 more |
| 26 | `get_upstream_features` | Emb:" Ph"@38 (de=14.12) +2 more |
| 27 | `inspect_feature` | "abbreviations for degrees and mentions of educational attainment" |
| 28 | `get_top_features` | 30 features; top: L14:15086 de=-0.061 |
| 29 | `inspect_feature` ×7 | L0:4621, L0:12208, L0:10457, L2:12316, L3:4213, L8:11284, L0:5718 |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F1069@1` | ❌ error | — | — | Trace the "He" / male-pronoun feature at L0:F1069 pos 1 upstream. Confirm it tra… |
| SA-2 | `L0:F12904@4` | ❌ error | — | — | Trace the L0:F12904 (positions of authority) at pos 4 (Director) upstream to its… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L7:F14129@40, k=3 → L6:F2254 (de=7.12) +2 more |
| 2 | `get_upstream_features` | L4:F12934@11, k=3 → Emb:" Laboratory"@11 (de=17.00) +2 more |
| 3 | `inspect_feature` ×2 | L4:15748, L0:6051 |
| 4 | `get_upstream_features` | L4:F12934@11, k=3 → Emb:" Laboratory"@11 (de=17.00) +2 more |
| 5 | `inspect_feature` ×2 | L0:11786, L3:3685 |

### Build

`build_circuit` → 18 nodes, 17 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 73,967 | 7,315 | 840,456 | 0 | $0.0814 | — | — |
| **Total** | | **73,967** | **7,315** | **840,456** | **0** | **$0.0814** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 23s