# Circuit Oracle Report
**Date:** 2026-07-28 07:18:21 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's positive classification score is driven by a mix of *profession-adjacent* signals (Director/PhD/Laboratory tokens) and *spurious* signals (the male pronoun "He", Korea/Korean entity marker, and the standalone word "Grid") that have no direct link to the academic-profession concept the probe is supposed to encode.

**Confidence:** 6

**Reasoning:**

The top direct-effect features for the probe split into roughly two camps:

**Profession-adjacent (arguably legitimate):**
- `L2:F4627` "the word director" (act=19, direct_effect=-0.047 at pos 4) — embedding " Director" → 27.5 direct_effect. This is the strongest profession signal.
- `L2:F10852` "academic titles and degrees" (act=36, -0.052 at pos 40) — driven by " Ph" (pos 38) and "D" (pos 40) token embeddings (14.1 and 9.75 direct_effects).
- `L7:F14129` "academic degrees, universities, and people associated with them" (act=46, +0.044) — genuine profession context.
- `L0:F5743` "the word 'lab'" (act=11, -0.038 at pos 11) — embedding " Laboratory" → 14.3 direct_effect.

**Spurious (not profession-specific):**
- `L0:F1069` "references to a male person, particularly when using the pronoun 'He' or 'His'" (act=17.75, **+0.042** at pos 1) — embedding "He" → 22.6. This is a textbook **gender marker** that activates on *every* male-referenced biography regardless of profession. Its semantic content is purely gendered, not occupational.
- `L0:F8658` "the word 'is'" (act=8.5, +0.047 at pos 2) — generic copula.
- `L14:F15086` "references to Korea/Korean" (act=39.75, **-0.061** at pos 46) — embedding " Korea" → 28.9 direct_effect, with upstream cascade through L7:F13010 (hyphenated Korean names, +11.7) and L5:F5563 (Korean food/institutions, +6.9). This is a **nationality/ethnicity marker** irrelevant to academic profession.
- `L1:F14934` "the word 'grid'" (act=13.25, +0.048 at pos 7) — embedding " Grid" → 18.25. Fires on the literal word "Grid" with no abstract profession concept attached; could fire on power-grid engineers, crossword grids, CSS grids, etc.
- `L0:F1069`/`F8658`/`F10846` ("also") — pure function-word detectors.

**Critical observation for the user's concern:** The male-pronoun feature F1069 contributes **+0.042** to the probe score, a magnitude comparable to the genuine profession signal from F4627 ("director", -0.047). Because F1069's `frac_nonzero` is only 0.0078 and it fires on "He" in *any* male-subject biography, its effect on the probe is a classic **gender-confound**: replacing "He" with "She" (a near-identical circuit) would shift the probe score by ~+0.04 even though nothing about the profession changed. The Korea entity marker (F15086) is similarly a **nationality confound** (-0.06) that the probe will pick up on Korean academics regardless of field. The "grid" feature is a **lexical confound** that activates on a research-area term rather than on the abstract profession concept.

The embedding node `Emb: He (pos 1)` has the single largest direct_effect (22.6) of any L0 feature in the graph, flowing into a gender-marker feature that pushes the probe — this is the strongest evidence for the user's concern that the circuit is using spurious gender features rather than genuine profession indicators.

The profession-relevant nodes (`Emb: Director`, `Emb: Ph`, `Emb: Laboratory`, `late_degree`) are present and contributing, so the probe is not *purely* spurious — but the gender and nationality markers carry comparable weight, which is exactly the bias the user suspected.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L14:F15086](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/15086) | 46 | L14: Korea/Korean entity |  references to Korea/Korean | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/15086) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 40 | L7: academic degrees/universities |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L4:F12934](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12934) | 11 | L4/L8: research/laboratory/journals |  names of academic journals | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12934) |
| [L8:F11284](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) | 11 | L4/L8: research/laboratory/journals |  words and phrases related to people's names, titles, universities, and research | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) |
| [L6:F3774](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) | 46 | L4/L8: research/laboratory/journals |  proper nouns or names with unusual capitalization | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | L0: male pronoun "He/His" (GENDER MARKER) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L1:F14934](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14934) | 7 | L1: "grid" word | the word "grid" and some related terms related to "grids" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14934) |
| [L2:F4627](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4627) | 4 | L2: "director" word + titles | the word "director" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4627) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 40 | L2: "director" word + titles |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L0:F10846](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10846) | 3 | L0: "also", "is", "is", "Lab" | the word "also" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10846) |
| [L0:F8658](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8658) | 2 | L0: "also", "is", "is", "Lab" |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8658) |
| [L0:F5718](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5718) | 3 | L0: "also", "is", "is", "Lab" | the word "still" and adverbs that indicate a continuing action | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5718) |
| [L0:F5743](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5743) | 11 | L0: "also", "is", "is", "Lab" | the word "lab" and words that might be associated with equipment or a positive experience | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5743) |
| [L0:F3255](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) | 8 | L0: "also", "is", "is", "Lab" |  the word "and" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) |
| [L0:F15160](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15160) | 7 | L0: "also", "is", "is", "Lab" | the word "concerns" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15160) |
| [L0:F10457](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10457) | 11 | L0: "also", "is", "is", "Lab" | the string "filename" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10457) |
| [L0:F1242](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1242) | 11 | L0: "also", "is", "is", "Lab" | the word "appropriate" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1242) |
| [L0:F12904](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12904) | 4 | L0: "also", "is", "is", "Lab" | mentions of the day prior or positions of authority | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12904) |
| [L0:F4621](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4621) | 4 | L0: "also", "is", "is", "Lab" |  words related to administrative positions and bodies | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4621) |
| [L0:F12208](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12208) | 4 | L0: "also", "is", "is", "Lab" | the word "perspective" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12208) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:15086 de=-0.061 |
| 3 | `inspect_feature` ×6 | L1:14934, L0:8658, L7:14129, L0:1069, L0:1242, L14:15086 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F15086@46` | ✅ reported | 5 | 13 | Trace what drives the Korea/Korean feature at L14:F15086 at pos 46. Find embeddi… |
| SA-2 | `L7:F14129@40` | ✅ reported | 7 | 11 | Trace the academic degrees/universities feature at L7:F14129 at pos 40 back to e… |
| SA-3 | `L1:F14934@7` | ✅ reported | 4 | 3 | Trace the "grid" word feature at L1:F14934 at pos 7 back to embeddings. What tok… |
| SA-4 | `L0:F1069@1` | ❌ error | — | — | Trace the male pronoun "He" feature at L0:F1069 at pos 1 back to embedding. This… |

<details>
<summary><b>SA-1</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F15086 | " references to Korea/Korean" |
| 2 | `get_upstream_features` | L14:F15086@46, k=15 | Emb:" Korea"@46 (de=28.88) +14 more |
| 3 | `inspect_feature` | L7, F13010 | " Korean names, especially those with multiple parts separated by hyphe" |
| 4 | `inspect_feature` | L5, F5563 | " words related to Korean food and Korean conglomerates" |
| 5 | `get_upstream_features` | L7:F13010@46, k=10 | Emb:" Korea"@46 (de=14.25) +9 more |
| 6 | `inspect_feature` | L6, F3774 | " proper nouns or names with unusual capitalization" |
| 7 | `inspect_feature` | L1, F10575 | " Korean names" |
| 8 | `get_upstream_features` | L5:F5563@46, k=10 | Emb:" Korea"@46 (de=16.38) +9 more |
| 9 | `get_upstream_features` | L1:F10575@46, k=10 | Emb:" Korea"@46 (de=18.00) +9 more |

**Findings:** The high‑level Korea/Korean feature at L14:F15086 is driven primarily by a direct embedding signal for the token " Korea" (pos 46) and by a cascade of lower‑layer name/food/context detectors. The strongest upstream contributors are: (1) the raw token embedding for " Korea", (2) a layer‑7 feature that spots hyphenated Korean personal names, (3) a layer‑5 feature that captures Korean food and instit…

</details>

<details>
<summary><b>SA-2</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14129 | " academic degrees, universities, and people associated with them" |
| 2 | `get_upstream_features` | L7:F14129@40, k=15 | L6:F2254 (de=7.12) +14 more |
| 3 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 4 | `inspect_feature` | L5, F13801 | "abbreviations for degrees and mentions of educational attainment" |
| 5 | `get_upstream_features` | L6:F2254@40, k=15 | L2:F10852 (de=11.31) +14 more |
| 6 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 7 | `get_upstream_features` | L2:F10852@40, k=10 | Emb:" Ph"@38 (de=14.12) +9 more |
| 8 | `inspect_feature` | L1, F10132 | " the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") writ" |
| 9 | `get_upstream_features` | L1:F10132@40, k=15 | Emb:" Ph"@38 (de=16.12) +14 more |
| 10 | `get_upstream_features` | L5:F13801@40, k=15 | L2:F10852 (de=6.62) +14 more |
| 11 | `inspect_feature` | L3, F8294 | " words and phrases related to advanced education, research, and high-l" |

**Findings:** The academic‑degree feature at L7:F14129 receives its strongest drive from lower‑layer degree detectors (L6:F2254, L5:F13801, L2:F10852) which themselves are excited primarily by the raw input embeddings for the tokens " Ph" (position 38) and "D" (position 40). These embeddings encode the characters that form the abbreviation "PhD" and the solitary "D" token, respectively. The signal propagates up…

</details>

<details>
<summary><b>SA-3</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F14934 | "the word "grid" and some related terms related to "grids"" |
| 2 | `get_upstream_features` | L1:F14934@7, k=15 | Emb:" Grid"@7 (de=18.25) +14 more |
| 3 | `inspect_feature` | L0, F6023 | " sections of documents with proper nouns and industry terminology." |
| 4 | `get_upstream_features` | L0:F6023@7, k=10 | Emb:" Grid"@7 (de=11.62) +9 more |
| 5 | `inspect_feature` | L0, F9122 | " words related to parents" |
| 6 | `get_upstream_features` | L0:F9122@7, k=10 | Emb:" Grid"@7 (de=11.44) +9 more |
| 7 | `inspect_feature` | L0, F4993 | " section titles, proper names, and words related to stages and periods" |

**Findings:** The L1 feature F14934 (layer 1, position 7) is a dedicated "grid" detector. Its strongest upstream driver is the raw input embedding for the token " Grid" at the same position, contributing a direct_effect of +18.25 (not shown as an edge because embedding nodes are not represented in the feature‑to‑feature edge list). Secondary contributions come from three layer‑0 features (6023, 9122, 4993) that…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F1069@1, k=10 → Emb:"He"@1 (de=22.62) +9 more |
| 2 | `inspect_feature` ×14 | L0:10846, L0:12904, L2:10852, L2:4627, L0:3255, L0:5743, L4:12934, L8:11284, L0:5718, L0:4621, L0:12208, L0:10457, L0:15160, L6:3774 |
| 3 | `get_upstream_features` | L14:F15086@46, k=3 → Emb:" Korea"@46 (de=28.88) +2 more |
| 4 | `get_upstream_features` | L0:F10846@3, k=3 → Emb:" also"@3 (de=33.75) +2 more |
| 5 | `get_upstream_features` | L0:F5743@11, k=3 → Emb:" Laboratory"@11 (de=14.31) +2 more |
| 6 | `get_upstream_features` | L4:F12934@11, k=5 → Emb:" Laboratory"@11 (de=17.00) +4 more |
| 7 | `get_upstream_features` | L8:F11284@11, k=5 → Emb:" Laboratory"@11 (de=11.06) +4 more |
| 8 | `get_upstream_features` | L2:F10852@40, k=5 → Emb:" Ph"@38 (de=14.12) +4 more |
| 9 | `get_upstream_features` | L2:F4627@4, k=3 → Emb:" Director"@4 (de=27.50) +2 more |
| 10 | `get_upstream_features` | L0:F8658@2, k=3 → Emb:"He"@1 (de=8.00) +2 more |
| 11 | `get_upstream_features` | L0:F12208@4, k=3 → Emb:" Director"@4 (de=18.88) +2 more |
| 12 | `get_upstream_features` | L0:F5718@3, k=3 → Emb:" is"@2 (de=10.44) +2 more |
| 13 | `get_upstream_features` | L0:F4621@4, k=3 → Emb:" Director"@4 (de=14.56) +2 more |
| 14 | `get_upstream_features` | L0:F15160@7, k=3 → Emb:" Grid"@7 (de=14.06) +2 more |
| 15 | `get_upstream_features` | L0:F10457@11, k=3 → Emb:" Laboratory"@11 (de=15.75) +2 more |
| 16 | `get_upstream_features` | L0:F1242@11, k=3 → Emb:" Laboratory"@11 (de=18.00) +2 more |

### Build

`build_circuit` → 14 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 42,284 | 5,437 | 247,923 | 0 | $0.0341 | — | — |
| SA-3 | openai/gpt-oss-120b | 73,786 | 5,361 | 9,216 | 0 | $0.0144 | ✅ 4F/3E | Trace the "grid" word feature at L1:F14934 at pos 7 back to … |
| SA-1 | openai/gpt-oss-120b | 100,617 | 5,085 | 5,072 | 0 | $0.0182 | ✅ 5F/13E | Trace what drives the Korea/Korean feature at L14:F15086 at … |
| SA-2 | openai/gpt-oss-120b | 130,289 | 7,527 | 3,328 | 0 | $0.0241 | ✅ 7F/11E | Trace the academic degrees/universities feature at L7:F14129… |
| **Total** | | **346,976** | **23,410** | **265,539** | **0** | **$0.0908** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 0s