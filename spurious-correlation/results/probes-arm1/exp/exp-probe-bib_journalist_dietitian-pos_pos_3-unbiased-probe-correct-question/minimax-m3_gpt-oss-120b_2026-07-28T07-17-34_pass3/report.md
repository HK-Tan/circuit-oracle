# Circuit Oracle Report
**Date:** 2026-07-28 07:17:34 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's positive classification score is driven primarily by genuinely profession-relevant semantic features (food/nutrition, diet, exercise/physical activity, "healthy", "lifestyle", "passion", career-mission language), not by female-gender pronouns, but several *negative* contributions (she/her, "others", "easier", "studio", punctuation) partially offset that signal.

**Confidence:** 7

**Reasoning:** Inspecting the top features reveals that the probe's *positive* score is dominated by profession-content signals: the L6 food/nutrition feature F11327 (direct_effect 0.093, frac_nonzero 0.012, top-activating token "food"), traced upstream to the raw " food" token embedding at pos 15 (direct_effect 34) and " healthy" at pos 14; the L14 food-insecurity feature F4197 (0.069) at the same position; the L4 diet/dietary-health feature F13412 (0.057) which receives " healthy" (7.5) and " food" (4) embeddings; the L4 exercise/physical-activity feature F3047 (0.082, promoted tokens "workout/exercise/gym") which is grounded in the " active" and " physically" embeddings via L0:F3597 ("active") and L2:F13919 (life-goal/active semantics); and several content-word features — F10218 "lifestyle" (0.055), F8444 "to" (0.048, used in mission-statement constructions), F815 "passion" (0.045), F2845 "knowledge" (0.054), F2238 "about" (0.052, frqnz 0.0066, fires on "about empowering"), and F4030 "career mission-statement" (0.078) — all of which encode thematic language characteristic of a health-coach/nutritionist bio. The *negative* features do include a female-pronoun cluster (L0:F9519 "she/her" -0.065, L0:F15382 "female person/Her" -0.040, L1:F7244 "she" +0.056 but with female-suppression, L6:F11646 "references to women" -0.065, all firing on the opening "She is passionate"), plus L0:F2349 "others" (-0.123) at "empowering others". However, these gender-related features all have *negative* direct_effect on the probe score, meaning they push the classification *down*, not up — the model is not using gender as a positive cue. A balanced circuit diagram shows: embeddings → semantic concept features (food, diet, exercise, mission-statement, lifestyle) → output (positive); and pronoun features → output (negative). So the user's concern that the probe uses spurious gender markers is *partially* valid only in the sense that female-pronoun features are present and prominent in the attribution, but they contribute *against* the classification rather than for it; the classification is genuinely driven by profession-content vocabulary. The single strongest negative feature, F2349 "others", is lexical-content rather than gendered, and likely reflects the non-bio phrase "empowering others" suppressing the probe.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 15 | Food/nutrition concepts (L6, L14) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 41 | Food/nutrition concepts (L6, L14) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 50 | Food/nutrition concepts (L6, L14) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 15 | Food/nutrition concepts (L6, L14) |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 15 | Diet/dietary health (L4) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 34 | Diet/dietary health (L4) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F3047](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3047) | 22 | Exercise/physical activity (L4) |  words or phrases related to exercise and physical activity | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3047) |
| [L2:F6341](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6341) | 14 | The word 'healthy' (L2) |  the word "healthy" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6341) |
| [L0:F10218](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10218) | 17 | The word 'lifestyle' (L0) |  the word "lifestyle." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10218) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 12 | The word 'active' (L0) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L1:F815](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/815) | 3 | The word 'passion' (L1) |  the word "passion" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/815) |
| [L0:F2845](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2845) | 9 | The word 'knowledge' (L0) |  the word "knowledge" and words starting with the letter "A" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2845) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 4 | The word 'about' (L0) |  the word "about" when followed by a numerical value | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L0:F4030](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4030) | 3 | Career mission-statement language (L0) |  words related to mission statements and personal development used in career environments | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4030) |
| [L0:F2349](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) | 6 | The word 'others' (L0, NEGATIVE) |  the word "others" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 1 | Female pronouns 'she/her' (L0, L1, L6, NEGATIVE) |  the pronoun "she" and the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 1 | Female pronouns 'she/her' (L0, L1, L6, NEGATIVE) | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L1:F7244](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7244) | 1 | Female pronouns 'she/her' (L0, L1, L6, NEGATIVE) | the pronoun "she" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7244) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Female pronouns 'she/her' (L0, L1, L6, NEGATIVE) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L0:F5829](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5829) | 3 | The word 'easier' (L0, NEGATIVE) |  the word "easier" with some modifiers such as "max" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5829) |
| [L0:F9927](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9927) | 3 | The word 'studio' (L0, NEGATIVE) |  the word "studio," sometimes with a modifier like "usually" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9927) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 28 | Punctuation/periods (L0, NEGATIVE) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `rank_segment_features` | ❌ This tool requires ctx.sibling_graphs to be set (at least on |
| 3 | `get_top_features` | 20 features; top: L0:2349 de=-0.123 |
| 4 | `get_candidate_vote_tally` | ❌ This tool requires ctx.sibling_graphs to be set (at least on |
| 5 | `get_top_features` | 15 features; top: L0:2349 de=-0.123 |
| 6 | `inspect_feature` ×4 | L6:11327, L4:3047, L14:4197, L0:4030 |
| 7 | `get_top_features` | 30 features; top: L0:2349 de=-0.123 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11327@15` | ✅ reported | 4 | 8 | Trace this food/nutrition feature at L6 pos 15. Find what earlier features/embed… |
| SA-2 | `L4:F3047@22` | ✅ reported | 5 | 11 | Trace this exercise/physical activity feature at L4 pos 22. Find what earlier fe… |
| SA-3 | `L14:F4197@15` | ❌ error | — | — | Trace this food feature at L14 pos 15. Find what earlier features/embeddings it … |
| SA-4 | `L0:F2349@6` | ❌ error | — | — | Trace this top negative feature at L0 pos 6. What is it, and what does it depend… |

<details>
<summary><b>SA-1</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 2 | `get_upstream_features` | L6:F11327@15, k=10 | Emb:" food"@15 (de=34.00) +9 more |
| 3 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 4 | `get_upstream_features` | L4:F13412@15, k=10 | Emb:" healthy"@14 (de=7.53) +9 more |
| 5 | `inspect_feature` | L1, F11764 | " words and phrases related to health and fitness" |
| 6 | `inspect_feature` | L3, F10028 | "words or short phrases that include "made of/from", and words ending w" |

**Findings:** The target L6:F11327 (food/nutrition detector) is primarily driven by the raw token embedding "food" at the same position, delivering a very large positive direct effect (34.0). A secondary boost comes from the embedding "healthy" at the preceding token. The feature also receives upstream support from a mid‑level diet‑health detector (L4:13412), which itself is strongly excited by the embeddings "…

</details>

<details>
<summary><b>SA-2</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F3047 | " words or phrases related to exercise and physical activity" |
| 2 | `get_upstream_features` | L4:F3047@22, k=15 | Emb:" active"@22 (de=10.25) +14 more |
| 3 | `inspect_feature` | L2, F13919 | "words related to life goals and purpose" |
| 4 | `inspect_feature` | L0, F3597 | "the word "active" optionally preceded by an adverb of degree" |
| 5 | `get_upstream_features` | L2:F13919@22, k=15 | Emb:" active"@22 (de=4.56) +14 more |
| 6 | `inspect_feature` | L1, F9918 | " words related to research studies of physical activity" |
| 7 | `inspect_feature` | L1, F3066 | " discussion of physical exercise and sports" |
| 8 | `get_upstream_features` | L0:F3597@22, k=10 | Emb:" active"@22 (de=18.12) +9 more |
| 9 | `get_upstream_features` | L1:F9918@22, k=10 | Emb:" active"@22 (de=5.28) +9 more |
| 10 | `inspect_feature` | L1, F13882 | "words and short phrases related to physical activity and exercise" |
| 11 | `get_upstream_features` | L0:F3597@22, k=10 | Emb:" active"@22 (de=18.12) +9 more |

**Findings:** The L4 exercise feature (F3047) is driven primarily by the input token 'active' (pos 22) and the nearby token 'physically' (pos 21).  Its activation is further reinforced by a lower‑layer semantic node L2:F13919 that links the concept of being 'active' to life purpose, and by the raw detection node L0:F3597 that directly fires on the word 'active'.  Both the lower‑layer feature (layer 0) and the e…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F11327@15, k=10 → Emb:" food"@15 (de=34.00) +9 more |
| 2 | `inspect_feature` ×23 | L0:2349, L0:9519, L6:11646, L0:8566, L0:5829, L0:11814, L4:13412, L1:7244, L0:10218, L0:2845, L0:2238, L0:9927, L0:6051, L0:8444, L2:6341, L1:815, L0:8392, L0:5942, L4:7864, L0:15382, L0:1373, L9:15314, L0:12347 |

### Build

`build_circuit` → 25 nodes, 25 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 66,969 | 5,506 | 116,614 | 0 | $0.0337 | — | — |
| SA-2 | openai/gpt-oss-120b | 107,504 | 8,526 | 30,720 | 0 | $0.0217 | ✅ 5F/11E | Trace this exercise/physical activity feature at L4 pos 22. … |
| SA-1 | openai/gpt-oss-120b | 56,549 | 3,761 | 96 | 0 | $0.0107 | ✅ 4F/8E | Trace this food/nutrition feature at L6 pos 15. Find what ea… |
| **Total** | | **231,022** | **17,793** | **147,430** | **0** | **$0.0661** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 14s