# Circuit Oracle Report
**Date:** 2026-07-28 07:21:49 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a mix of profession-relevant cues (academic-degree tokens like "Ph.D.", the word "Director", "Laboratory") and clearly spurious features: a male-pronoun feature ("He" at pos 1, direct_effect +0.042), several generic function-word features (the words "also", "is", "and", "still", "perspective"), and a "Korea/Korean" feature that fires on the institution name "Korea University" — a national-origin marker unrelated to the academic profession.

**Confidence:** 7

**Reasoning:** The circuit traced from embedding tokens up through mid- and late-layer features converges on the probe's output direction. The terminal supernode feeding the output is dominated by:

1. **Profession-genuine features** — `academic` (L7:F14129, "academic degrees, universities", pos 40 on "D" of "Ph.D."; L6:F2254, "references to academic degrees"; L5:F13801, "abbreviations for degrees") and `director_low` (L2:F4627 "the word director"; L2:F10852 "academic titles and degrees"; L1:F14934 "the word grid") — these are anchored to tokens like *Ph.D.* (pos 38–40), *Director* (pos 4), *Laboratory* (pos 11), and *Grid* (pos 7), i.e. the field- and role-defining vocabulary of an academic-engineer bio.

2. **Spurious gender/pronominal features** — `he_pronoun` (L0:F1069, frac_nonzero ≈ 0.008, label *"references to a male person, particularly when using the pronoun 'He' or 'His.'"*) sits at pos 1 on the token "He" and contributes direct_effect +0.042 to the output purely from the male pronoun. This is the canonical gender-marker confound: the feature is highly specific (low frac_nonzero) but specific to *gender*, not to the profession.

3. **Spurious national-origin features** — `korea_top` (L14:F15086, label *"references to Korea/Korean"*, pos 46 on the token " Korea"; L7:F13010 "Korean names…in credits or medical contexts") is driven by the embedding of "Korea" (direct_effect 28.9 into L14:F15086). The probe uses the subject's Korean institutional affiliation as a profession-classification signal.

4. **Generic function-word features** — `function_words` (L0:F10846 "also", F8658 "is", F3255 "and", F5718 "still", F15160 "concerns", F12208 "perspective"; all at positions 2–8) are sentence-grammar markers with no semantic relation to profession. Their activations are small (~0.03–0.04 each) but sum across many tokens, contributing cumulative signal that has no causal connection to the subject's occupation.

5. **Lab-vocabulary support** — `lab_low` (L0:F5743 "the word 'lab'", L4:F12934 "names of academic journals", L8:F11284 "names, titles, universities, and research", all at pos 11) is the cleanest profession-specific signal and tracks the token "Laboratory".

The user is correct: the circuit is not a pure profession-detector. While genuine profession features (academic degrees, "Director", "Laboratory") are present, the model leans additionally on (a) the male pronoun at sentence-initial "He" (a clear gender confounder), (b) the Korea-related features (a national/ethnicity marker triggered by the institution name), and (c) several generic function-word features. These are the "spurious features" the concern flagged. The profession signal is real but not exclusive; the probe direction has learned to use male-pronominal and Korean-affiliation context as shortcuts in addition to the genuine field indicators.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L14:F15086](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/15086) | 46 | Korea/Korean references (L14, L7) |  references to Korea/Korean | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/15086) |
| [L7:F13010](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13010) | 46 | Korea/Korean references (L14, L7) |  Korean names, especially those with multiple parts separated by hyphens, in credits or medical contexts. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13010) |
| [L6:F3774](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) | 46 | Proper nouns / unusual capitalization (L6) |  proper nouns or names with unusual capitalization | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) |
| [L5:F5563](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5563) | 46 | Proper nouns / unusual capitalization (L6) |  words related to Korean food and Korean conglomerates | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5563) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 40 | Academic degrees / titles (L6-L7) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 40 | Academic degrees / titles (L6-L7) | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L5:F13801](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) | 40 | Academic degrees / titles (L6-L7) | abbreviations for degrees and mentions of educational attainment | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Male pronoun (L0) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 40 | Director/position keywords (L0-L2) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F4627](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4627) | 4 | Director/position keywords (L0-L2) | the word "director" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4627) |
| [L0:F12904](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12904) | 4 | Director/position keywords (L0-L2) | mentions of the day prior or positions of authority | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12904) |
| [L0:F4621](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4621) | 4 | Director/position keywords (L0-L2) |  words related to administrative positions and bodies | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4621) |
| [L1:F14934](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14934) | 7 | Director/position keywords (L0-L2) | the word "grid" and some related terms related to "grids" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14934) |
| [L0:F5743](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5743) | 11 | Lab/Laboratory keywords (L0) | the word "lab" and words that might be associated with equipment or a positive experience | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5743) |
| [L0:F1242](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1242) | 11 | Lab/Laboratory keywords (L0) | the word "appropriate" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1242) |
| [L0:F10457](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10457) | 11 | Lab/Laboratory keywords (L0) | the string "filename" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10457) |
| [L8:F11284](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) | 11 | Lab/Laboratory keywords (L0) |  words and phrases related to people's names, titles, universities, and research | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) |
| [L4:F12934](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12934) | 11 | Lab/Laboratory keywords (L0) |  names of academic journals | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12934) |
| [L0:F10846](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10846) | 3 | Function words (also, is, and, still, grid, perspective) (L0) | the word "also" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10846) |
| [L0:F8658](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8658) | 2 | Function words (also, is, and, still, grid, perspective) (L0) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8658) |
| [L0:F3255](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) | 8 | Function words (also, is, and, still, grid, perspective) (L0) |  the word "and" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) |
| [L0:F5718](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5718) | 3 | Function words (also, is, and, still, grid, perspective) (L0) | the word "still" and adverbs that indicate a continuing action | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5718) |
| [L0:F15160](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15160) | 7 | Function words (also, is, and, still, grid, perspective) (L0) | the word "concerns" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15160) |
| [L0:F12208](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12208) | 4 | Function words (also, is, and, still, grid, perspective) (L0) | the word "perspective" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12208) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:15086 de=-0.061 |
| 3 | `inspect_feature` ×20 | L14:15086, L6:3774, L0:10846, L2:10852, L1:14934, L2:4627, L0:8658, L7:14129, L0:1069, L0:1242, L0:12904, L0:15160, L0:3255, L0:5743, L4:12934, L0:5718, L8:11284, L0:4621, L0:12208, L0:10457 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F15086@46` | ❌ error | — | — | Trace the path from L14:F15086 ("references to Korea/Korean") upstream. What tok… |
| SA-2 | `L6:F3774@46` | ❌ error | — | — | Trace the path from L6:F3774 ("proper nouns or names with unusual capitalization… |
| SA-3 | `L7:F14129@40` | ❌ error | — | — | Trace the path from L7:F14129 ("academic degrees, universities") upstream at pos… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F15086@46, k=10 → Emb:" Korea"@46 (de=28.88) +9 more |
| 2 | `get_upstream_features` | L7:F14129@40, k=10 → L6:F2254 (de=7.12) +9 more |
| 3 | `get_upstream_features` | L6:F3774@46, k=10 → Emb:" Korea"@46 (de=18.38) +9 more |
| 4 | `inspect_feature` ×8 | L7:13010, L5:5563, L6:2254, L5:13801, L1:10132, L2:10852, L1:10575, L6:2254 |
| 5 | `get_upstream_features` | L1:F14934@7, k=10 → Emb:" Grid"@7 (de=18.25) +9 more |
| 6 | `get_upstream_features` | L0:F10846@3, k=10 → Emb:" also"@3 (de=33.75) +9 more |
| 7 | `get_upstream_features` | L2:F10852@40, k=10 → Emb:" Ph"@38 (de=14.12) +9 more |
| 8 | `get_upstream_features` | L8:F11284@11, k=10 → Emb:" Laboratory"@11 (de=11.06) +9 more |
| 9 | `get_upstream_features` | L0:F1069@1, k=10 → Emb:"He"@1 (de=22.62) +9 more |
| 10 | `get_upstream_features` | L0:F1242@11, k=10 → Emb:" Laboratory"@11 (de=18.00) +9 more |
| 11 | `get_upstream_features` | L0:F10457@11, k=10 → Emb:" Laboratory"@11 (de=15.75) +9 more |
| 12 | `get_upstream_features` | L2:F10852@4, k=10 → ❌ Feature (layer=2, feature_idx=10852) not found at pos=4. Thi |
| 13 | `get_upstream_features` | L2:F4627@4, k=10 → Emb:" Director"@4 (de=27.50) +9 more |
| 14 | `get_upstream_features` | L0:F12904@4, k=10 → Emb:" Director"@4 (de=16.50) +9 more |
| 15 | `get_upstream_features` | L0:F4621@4, k=10 → Emb:" Director"@4 (de=14.56) +9 more |
| 16 | `get_upstream_features` | L0:F12208@4, k=10 → Emb:" Director"@4 (de=18.88) +9 more |
| 17 | `get_upstream_features` | L0:F8658@2, k=10 → Emb:"He"@1 (de=8.00) +9 more |
| 18 | `get_upstream_features` | L0:F5743@11, k=10 → Emb:" Laboratory"@11 (de=14.31) +9 more |
| 19 | `get_upstream_features` | L6:F2254@40, k=10 → L2:F10852 (de=11.31) +9 more |
| 20 | `get_upstream_features` | L5:F13801@40, k=10 → L2:F10852 (de=6.62) +9 more |
| 21 | `get_upstream_features` | L1:F10132@40, k=10 → Emb:" Ph"@38 (de=16.12) +9 more |
| 22 | `get_upstream_features` | L4:F12934@11, k=10 → Emb:" Laboratory"@11 (de=17.00) +9 more |
| 23 | `get_upstream_features` | L7:F13010@46, k=10 → Emb:" Korea"@46 (de=14.25) +9 more |
| 24 | `get_upstream_features` | L5:F5563@46, k=10 → Emb:" Korea"@46 (de=16.38) +9 more |
| 25 | `get_upstream_features` | L0:F15160@7, k=10 → Emb:" Grid"@7 (de=14.06) +9 more |
| 26 | `get_upstream_features` | L0:F3255@8, k=10 → Emb:" and"@8 (de=37.50) +9 more |
| 27 | `get_upstream_features` | L0:F5718@3, k=10 → Emb:" is"@2 (de=10.44) +9 more |
| 28 | `get_upstream_features` | L4:F13943@40, k=5 → L2:F10852 (de=7.34) +4 more |

### Build

`build_circuit` → 17 nodes, 16 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 88,334 | 6,174 | 401,753 | 0 | $0.0580 | — | — |
| **Total** | | **88,334** | **6,174** | **401,753** | **0** | **$0.0580** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 26s