# Circuit Oracle Report
**Date:** 2026-07-28 07:21:27 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_6 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity probe fires almost entirely on the mere co-occurrence of racial identity tokens ("white", "black") and a few generic male-coded tokens ("dude", "man", "men"), with no circuit path that encodes the toxic content itself (the slur "stealing", the predicate "stealing thunder", or the negative-attitude predicate "expletives/strong opinions").

**Confidence:** 9

**Reasoning:**

Tracing the attribution graph top-down:

**Late-layer output drivers (L5–L9, "race_discourse" supernode):**
- **L9:F11035** ("mentions of different racial or ethnic groups", frac=0.018, activation=8.1) is the largest single driver (direct_effect=0.0942) — a generic detector that fires on any white/black/Whites/Blacks/Asian/Caucasian mention.
- **L8:F13464** ("discussions of racial issues, particularly white and black people", frac=0.026) and **L8:F15272** ("statistical language about human subjects", frac=0.038) both fire on the "dude" position purely because the surrounding tokens are racial terms.
- **L7:F9100** ("discussions of diversity, especially in media", frac=0.0078), **L7:F9113** ("words related to freedom/government/America", frac=0.010), **L7:F7215** ("racial discrimination in the American South", frac=0.0038), **L7:F114** ("fair treatment in employment…based on race, gender, or other protected characteristics", frac=0.0077) — all social-justice/race-discourse detectors with **frac_nonzero well under 0.01** (very specific category detectors, but specific to *race talk*, not to toxic content).
- **L6:F3902** ("terms referring to race and ethnicity"), **L6:F3077** ("places and categorizations of people by place", promoted_tokens include "white"/"Western"), **L6:F7829** ("expats, foreigners, British people"), **L6:F4008** ("expletives, strong opinions, negative words", frac=0.031), **L6:F627** ("words used when describing groups of people"), **L6:F1330** (Another-token detector) — all general-purpose detectors.
- **L5:F6786** ("terms associated with gender, race, sexual orientation, and disability"), **L5:F16048** (politics/government), **L5:F10172** ("ethnic slurs and terms related to the American South") — again, identity-category detectors.

**Mid-layer concept features (L2–L4, "mid_layer_race_concepts"):**
- **L4:F117** ("race, racism, social justice, focus on Black people", frac=0.012, activation=18.25) is a strong hub — fires on the "dude" position because the sentence contains both "white" and "black" racial labels.
- **L4:F15204** ("art galleries, museums, the White House") and **L4:F7136** ("the color white") fire from the raw "white" embedding (direct_effect from embedding = 43.5 onto F15204).
- **L3:F13061** ("words related to race, gender, social issues", frac=0.009) fires on BOTH the "dude" position (pos 3) and the "man's" position (pos 7), driven primarily by the "black" embedding (direct_effect=15.7) and "man" embedding.
- **L2:F13158** ("words about race and ethnicity", frac=0.010), **L2:F1708** ("mentions of colors"), **L2:F9837** ("references to men"), **L2:F10433** ("people, especially men"), **L2:F9909** ("groups of people/places"), **L2:F15317** (gendered words) — all fire on identity-mention positions.

**Early-layer lexical detectors (L0–L1, "lexical_detectors"):**
- **L0:F3436** ("mentions of 'white'") and **L0:F10910** ("'white', 'possession', 'immediate'…") — direct_effect ~0.29 and ~0.13 onto the probe, both from the "white" embedding (direct_effect from "white" embedding = 14.3 to each).
- **L0:F1015** ("the word 'black'") and **L1:F13069** ("the word 'black'") — fired by the "black" embedding (direct_effect from "black" embedding = 23.9 onto F1015).
- **L0:F15621** ("the word 'noise'") is actually firing on the token "stealing" — but this is a *wrong-fire* (its top activating examples are all "noise", but it happens to activate on "stealing" too). It contributes +0.10 to the probe, so a sliver of toxicity-relevant signal is present here.
- **L0:F4090** ("the word 'another'") — fires negatively (-0.27) because "Another" is associated with non-toxic contexts in the training distribution.

**What the circuit is NOT doing:**
- There is no feature that detects the predicate "stealing [someone's] thunder" as a unified structure.
- The "expletives / strong opinions" feature **F4008** (L6) fires on the "dude" position primarily because of the L3 race-issues feature F13061 and the "dude" embedding (direct_effect=10.6) — i.e., it tags "dude" as potentially expletive-laden because it sits next to racial labels, not because it detects actual expletives.
- The toxicity-relevant content tokens ("stealing", "thunder") are essentially absent from the high-direct-effect upstream chain. The probe gets almost all of its signal from race-IDENTITY features.

**Conclusion:** The probe's classification is driven by a circuit that runs *Emb:white, Emb:black, Emb:dude, Emb:man → L0–L2 lexical/concept detectors (white, black, race, men, color) → L3–L4 race-discourse hubs (F13061, F117, F15204) → L5–L9 race/ethnicity/diversity/justice detectors (F11035, F13464, F9100, F7215, F114, F6786, F10172) → output*. This is precisely the user's concern: the circuit uses **identity-group signals** (white+black co-occurrence, racial-issue vocabulary, social-justice vocabulary) rather than the actual toxicity-bearing predicates ("stealing thunder", attitude, contempt). The probe would likely score "Another white man talking about a black colleague's success" as similar to the actual toxic text, because the same identity-co-occurrence features fire. This is a textbook example of a probe relying on spurious demographic co-occurrence features.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L9:F11035](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/11035) | 3 | Late-layer race/ethnicity discourse features (L5–L9) |  mentions of different racial or ethnic groups, news, payments, political concepts and geographical locations. | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/11035) |
| [L8:F13464](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13464) | 3 | Late-layer race/ethnicity discourse features (L5–L9) |  discussions of racial issues, particularly those involving white and black people | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13464) |
| [L8:F15272](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15272) | 3 | Late-layer race/ethnicity discourse features (L5–L9) |  statistical language about human subjects in a research study | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15272) |
| [L7:F9100](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9100) | 3 | Late-layer race/ethnicity discourse features (L5–L9) |  discussions of diversity, especially in media | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9100) |
| [L7:F9113](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9113) | 3 | Late-layer race/ethnicity discourse features (L5–L9) | words related to freedom, government, or global entities | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9113) |
| [L7:F7215](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/7215) | 3 | Late-layer race/ethnicity discourse features (L5–L9) |  terms related to racial discrimination, predominantly in the context of the American South | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/7215) |
| [L7:F114](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/114) | 3 | Late-layer race/ethnicity discourse features (L5–L9) | discussions of fair treatment in employment and housing and especially disparities in pay or opportunity based on race, gender, or other protected characteristics. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/114) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 3 | Late-layer race/ethnicity discourse features (L5–L9) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3077](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3077) | 3 | Late-layer race/ethnicity discourse features (L5–L9) |  places and categorizations of people by place | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3077) |
| [L6:F7829](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7829) | 3 | Late-layer race/ethnicity discourse features (L5–L9) | mentions of expats, foreigners, or British people. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7829) |
| [L6:F627](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/627) | 3 | Late-layer race/ethnicity discourse features (L5–L9) |  words used when describing groups of people | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/627) |
| [L6:F1330](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1330) | 3 | Late-layer race/ethnicity discourse features (L5–L9) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1330) |
| [L6:F4008](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4008) | 3 | Late-layer race/ethnicity discourse features (L5–L9) |  expletives, strong opinions and negative words | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4008) |
| [L6:F14669](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14669) | 3 | Late-layer race/ethnicity discourse features (L5–L9) | a variety of seemingly unrelated words and symbols, possibly indicating multiple weak associations or noisy data. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14669) |
| [L5:F6786](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6786) | 3 | Late-layer race/ethnicity discourse features (L5–L9) | terms associated with gender, race, sexual orientation, and disability | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6786) |
| [L5:F16048](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16048) | 3 | Late-layer race/ethnicity discourse features (L5–L9) |  words relating to politics, government, and hierarchical organization | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16048) |
| [L5:F10172](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10172) | 3 | Late-layer race/ethnicity discourse features (L5–L9) |  ethnic slurs and terms related to the American South | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10172) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 3 | Mid-layer race/gender concepts (L2–L4) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F9880](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9880) | 1 | Mid-layer race/gender concepts (L2–L4) |  phrases indicating repetition or continuation which often use the word "another" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9880) |
| [L4:F15204](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) | 2 | Mid-layer race/gender concepts (L2–L4) |  art galleries, museums and the White House | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 3 | Mid-layer race/gender concepts (L2–L4) |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 7 | Mid-layer race/gender concepts (L2–L4) |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 2 | Mid-layer race/gender concepts (L2–L4) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 6 | Mid-layer race/gender concepts (L2–L4) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F1708](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1708) | 2 | Mid-layer race/gender concepts (L2–L4) |  mentions of colors | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1708) |
| [L2:F1708](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1708) | 6 | Mid-layer race/gender concepts (L2–L4) |  mentions of colors | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1708) |
| [L2:F9837](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9837) | 7 | Mid-layer race/gender concepts (L2–L4) |  references to men | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9837) |
| [L2:F9909](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9909) | 3 | Mid-layer race/gender concepts (L2–L4) |  terms used to describe groups of people or places | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9909) |
| [L2:F10433](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10433) | 7 | Mid-layer race/gender concepts (L2–L4) | mentions of people, especially men or groups of people | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10433) |
| [L2:F15317](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15317) | 3 | Mid-layer race/gender concepts (L2–L4) |  gendered words, with a slight bias toward female-gendered words | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15317) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 2 | Layer-0/L1 lexical token detectors (white, black, another, stealing) |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F10910](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) | 2 | Layer-0/L1 lexical token detectors (white, black, another, stealing) | the word "possession" and the words "white", "immediate" and "once" regardless of context | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) |
| [L0:F1015](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1015) | 6 | Layer-0/L1 lexical token detectors (white, black, another, stealing) |  the word "black" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1015) |
| [L0:F15621](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15621) | 4 | Layer-0/L1 lexical token detectors (white, black, another, stealing) | the word "noise," sometimes "noisy," and occasionally a related word like "improvement." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15621) |
| [L0:F4090](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4090) | 1 | Layer-0/L1 lexical token detectors (white, black, another, stealing) | the word "another" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4090) |
| [L0:F16013](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16013) | 6 | Layer-0/L1 lexical token detectors (white, black, another, stealing) |  mentions of the color blue, and perhaps colors in general or the components of a graphic image | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16013) |
| [L1:F13069](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13069) | 6 | Layer-0/L1 lexical token detectors (white, black, another, stealing) | the word 'black' | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13069) |
| [L1:F9113](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) | 6 | Layer-0/L1 lexical token detectors (white, black, another, stealing) |  discussions about race and slavery | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:3436 de=0.289 |
| 3 | `inspect_feature` ×10 | L0:3436, L0:4090, L4:15204, L4:7136, L6:4008, L0:10910, L3:13061, L0:1015, L0:15621, L9:11035 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L9:F11035@3` | ❌ error | — | — | Trace the path from L9:F11035 (racial/ethnic group mentions) upstream to the inp… |
| SA-2 | `L6:F4008@3` | ❌ error | — | — | Trace the path from L6:F4008 (expletives/strong opinions) upstream to input toke… |
| SA-3 | `L3:F13061@7` | ❌ error | — | — | Trace L3:F13061 (race/gender/social issues words) upstream to input tokens. Find… |
| SA-4 | `L4:F15204@2` | ✅ reported | 3 | 5 | Trace L4:F15204 (galleries, museums, White House) upstream. Why is this feature … |

<details>
<summary><b>SA-4</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F15204 | " art galleries, museums and the White House" |
| 2 | `get_upstream_features` | L4:F15204@2, k=10 | Emb:" white"@2 (de=43.50) +9 more |
| 3 | `inspect_feature` | L0, F10910 | "the word "possession" and the words "white", "immediate" and "once" re" |
| 4 | `get_upstream_features` | L0:F10910@2, k=10 | Emb:" white"@2 (de=14.31) +9 more |
| 5 | `inspect_feature` | L0, F3436 | " mentions of the word "white"" |
| 6 | `inspect_feature` | L0, F3241 | " contexts related to "agreement", especially in a collaborative or pol" |

**Findings:** The L4 feature F15204 (art galleries, museums, White House) fires because the prompt contains the token "white" (position 2). The raw embedding for "white" has a large positive direct effect (43.5) on F15204. Additionally, two layer‑0 lexical features (F10910 and F3436), both of which are specialized detectors for the word "white", also contribute positively (1.45 and 0.86 respectively). These low…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L9:F11035@3, k=12 → L8:F13464 (de=2.59) +11 more |
| 2 | `get_upstream_features` | L6:F4008@3, k=12 → Emb:" dude"@3 (de=10.56) +11 more |
| 3 | `get_upstream_features` | L3:F13061@7, k=12 → Emb:" black"@6 (de=15.69) +11 more |
| 4 | `get_upstream_features` | L6:F1330@3, k=10 → Emb:"Another"@1 (de=3.53) +9 more |
| 5 | `inspect_feature` ×17 | L8:13464, L6:3077, L8:15272, L6:7829, L6:627, L6:14669, L2:9909, L2:9837, L2:13158, L0:13442, L2:1708, L2:2850, L4:9757, L9:2762, L0:13663, L3:12848, L2:5925 |
| 6 | `get_upstream_features` | L2:F1708@6, k=8 → Emb:" black"@6 (de=20.00) +7 more |
| 7 | `get_upstream_features` | L2:F13158@6, k=8 → Emb:" black"@6 (de=10.81) +7 more |
| 8 | `get_upstream_features` | L0:F1015@6, k=6 → Emb:" black"@6 (de=23.88) +5 more |
| 9 | `inspect_feature` ×14 | L1:3020, L0:16013, L0:9076, L2:10433, L4:9880, L4:117, L4:9880, L4:117, L4:9880, L1:13069, L1:9113, L5:10172, L7:9113, L7:9100 |
| 10 | `get_upstream_features` | L9:F11035@3, k=8 → L8:F13464 (de=2.59) +7 more |
| 11 | `get_upstream_features` | L3:F13061@3, k=5 → Emb:" white"@2 (de=12.44) +4 more |
| 12 | `get_upstream_features` | L8:F13464@3, k=8 → Emb:" white"@2 (de=2.92) +7 more |
| 13 | `get_upstream_features` | L6:F627@3, k=5 → Emb:"<bos>"@0 (de=1.11) +4 more |
| 14 | `get_upstream_features` | L8:F15272@3, k=5 → Emb:" white"@2 (de=2.88) +4 more |
| 15 | `inspect_feature` ×6 | L6:3902, L7:114, L7:7215, L5:6786, L5:16048, L2:15317 |
| 16 | `get_upstream_features` | L0:F15621@4, k=6 → Emb:" stealing"@4 (de=20.75) +5 more |

### Build

`build_circuit` → 9 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 116,207 | 7,193 | 821,827 | 0 | $0.0928 | — | — |
| SA-4 | openai/gpt-oss-120b | 48,151 | 3,477 | 5,920 | 0 | $0.0094 | ✅ 3F/5E | Trace L4:F15204 (galleries, museums, White House) upstream. … |
| **Total** | | **164,358** | **10,670** | **827,747** | **0** | **$0.1022** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 35s