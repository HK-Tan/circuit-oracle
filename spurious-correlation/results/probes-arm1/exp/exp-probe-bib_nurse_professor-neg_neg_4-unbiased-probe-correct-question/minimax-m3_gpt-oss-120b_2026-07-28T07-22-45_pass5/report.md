# Circuit Oracle Report
**Date:** 2026-07-28 07:22:45 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe classifies this person as a professor by combining a strong positive signal from a male-pronoun feature at pos 1 ("He is also") with a positive computing-domain feature ("Grid"), a positive academic-degree feature at pos 40 ("Ph.D."), partially offset by a negative Korea/Korean-ethnicity feature at pos 46, confirming the user's concern that the probe relies on spurious gender markers rather than purely on profession indicators.

**Confidence:** 8

**Reasoning:** The top positive contributors to the probe score are dominated by the L0:F1069 "He/His male pronoun" feature (direct_effect +0.0479, activation 17.75 at pos 1, "He"), which traces directly to the `Emb: He (pos 1)` token embedding (direct_effect 22.625 to that feature) — the largest single edge in the entire circuit. The companion L0:F8658 ("is") and L0:F10846 ("also") features (direct_effects +0.0469 and +0.042) also live at positions 2-3 and trace to `Emb: is` and `Emb: also`, so the "He is also" subject-introduction fragment is the single most heavily weighted signal in the graph. L0:F1069's autointerp label is explicit: "references to a male person, particularly when using the pronoun 'He' or 'His'" — a textbook spurious correlate of professor biographies, not a profession indicator.

Alongside this gender signal, the circuit does include genuine profession-relevant features: L7:F14129 ("academic degrees, universities, and people associated with them", activation 46.25 at pos 40 "D", direct_effect +0.0435) and L2:F10852 ("academic titles and degrees", direct_effect +0.0518 at "D" in "Ph.D.") both fire on the "Ph.D." token and trace down to `Emb: Ph (pos 38)` and `Emb: D (pos 40)`, forming a degree-recognition supernode. L1:F14934 ("the word 'grid'", direct_effect +0.0479 at pos 7) provides a domain clue from "Mobile Grid and Cloud Computing Laboratory" and traces to `Emb: Grid (pos 7)`. A weaker academic-context supernode (L4:F12934 "names of academic journals", L8:F11284 "names, titles, universities, research", L0:F5743 "lab") fires around the "Computing Laboratory" token (pos 11) but with mixed signs.

Crucially, the L14:F15086 "references to Korea/Korean" feature (direct_effect -0.0613, the single most-negative contributor) and L6:F3774 (proper-noun detector, direct_effect -0.0549) both fire at pos 46 ("Korea University") and trace to `Emb: Korea (pos 46)` with direct_effects 28.875 and 18.375 respectively — these push the probe score down because Korean-academic-institution tokens are anti-correlated with the "professor" class in the probe's training data. L7:F13010 ("Korean names, especially with hyphens") and L5:F5563 ("Korean food/conglomerates") further confirm the Korea circuit is a nationality/ethnicity detector, not a profession one.

So the user's concern is well-founded but nuanced: the probe's positive classification is driven by a mix of (a) the spurious male-pronoun feature cluster at "He is also" (largest positive L0 signal), (b) genuine academic-degree features at "Ph.D." (pos 40), and (c) a domain word "Grid" (pos 7), while being partially offset by Korea-ethnicity features at "Korea" (pos 46). Gender markers from the subject-introduction are doing substantial work; swapping "He" to "She" would noticeably reduce the probe's positive score even though the profession-relevant evidence (Ph.D., Grid, Laboratory, research interests) would remain intact.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L14:F15086](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/15086) | 46 | Korea/Korean Ethnicity (negative for professor) |  references to Korea/Korean | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/15086) |
| [L6:F3774](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) | 46 | Korea/Korean Ethnicity (negative for professor) |  proper nouns or names with unusual capitalization | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 40 | Academic Degrees & Universities (positive for professor) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 40 | Academic Degrees & Universities (positive for professor) | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 40 | Academic Degrees & Universities (positive for professor) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L1:F10132](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) | 40 | Academic Degrees & Universities (positive for professor) |  the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") written as "D" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) |
| [L5:F13801](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) | 40 | Academic Degrees & Universities (positive for professor) | abbreviations for degrees and mentions of educational attainment | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Male pronoun 'He/His' (positive for professor) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F8658](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8658) | 2 | Male pronoun 'He/His' (positive for professor) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8658) |
| [L0:F10846](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10846) | 3 | Male pronoun 'He/His' (positive for professor) | the word "also" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10846) |
| [L1:F14934](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14934) | 7 | 'Grid' / computing term (positive for professor) | the word "grid" and some related terms related to "grids" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14934) |
| [L4:F12934](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12934) | 11 | Academic context / lab / journal (mixed) |  names of academic journals | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12934) |
| [L0:F5743](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5743) | 11 | Academic context / lab / journal (mixed) | the word "lab" and words that might be associated with equipment or a positive experience | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5743) |
| [L8:F11284](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) | 11 | Academic context / lab / journal (mixed) |  words and phrases related to people's names, titles, universities, and research | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:15086 de=-0.061 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F15086@46` | ❌ error | — | — | Trace upstream from L14:F15086 at pos 46. This is the most negative contributor … |
| SA-2 | `L6:F3774@46` | ❌ error | — | — | Trace upstream from L6:F3774 at pos 46. This is strongly negative for the probe.… |
| SA-3 | `L7:F14129@40` | ❌ error | — | — | Trace upstream from L7:F14129 at pos 40. This is a strong positive contributor. … |
| SA-4 | `L2:F10852@40` | ❌ error | — | — | Trace upstream from L2:F10852 at pos 40. Strong negative feature. Determine what… |
| SA-5 | `L1:F14934@7` | ❌ error | — | — | Trace upstream from L1:F14934 at pos 7. Strong positive feature. Determine what … |
| SA-6 | `L0:F1069@1` | ❌ error | — | — | Trace upstream from L0:F1069 at pos 1. Strong positive feature at early layer, p… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×8 | L14:15086, L6:3774, L7:14129, L2:10852, L1:14934, L0:1069, L0:8658, L0:10846 |
| 2 | `get_upstream_features` | L0:F1069@1, k=10 → Emb:"He"@1 (de=22.62) +9 more |
| 3 | `get_upstream_features` | L1:F14934@7, k=10 → Emb:" Grid"@7 (de=18.25) +9 more |
| 4 | `get_upstream_features` | L7:F14129@40, k=10 → L6:F2254 (de=7.12) +9 more |
| 5 | `get_upstream_features` | L2:F10852@40, k=10 → Emb:" Ph"@38 (de=14.12) +9 more |
| 6 | `get_upstream_features` | L14:F15086@46, k=10 → Emb:" Korea"@46 (de=28.88) +9 more |
| 7 | `get_upstream_features` | L6:F3774@46, k=10 → Emb:" Korea"@46 (de=18.38) +9 more |
| 8 | `get_upstream_features` | L0:F8658@2, k=10 → Emb:"He"@1 (de=8.00) +9 more |
| 9 | `get_upstream_features` | L0:F10846@3, k=10 → Emb:" also"@3 (de=33.75) +9 more |
| 10 | `inspect_feature` ×5 | L2:4627, L0:12904, L0:1242, L0:15160, L0:3255 |
| 11 | `get_upstream_features` | L7:F14129@40, k=10 → L6:F2254 (de=7.12) +9 more |
| 12 | `inspect_feature` ×12 | L6:2254, L1:10132, L7:13010, L5:5563, L0:4621, L0:12208, L0:10457, L0:5743, L8:11284, L4:12934, L0:5718, L5:13801 |

### Build

`build_circuit` → 14 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 48,343 | 4,868 | 157,357 | 0 | $0.0298 | — | — |
| **Total** | | **48,343** | **4,868** | **157,357** | **0** | **$0.0298** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 9s