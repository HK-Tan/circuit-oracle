# Circuit Oracle Report
**Date:** 2026-07-28 07:16:22 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction score is driven by a mix of premise content features ("early 17th-century tower house" at L4) and **hypothesis-side lexical/negation markers** — particularly the word "any" (L0:F10815, +0.117), the word "from" (L0:F8974, −0.124), the word "itself" (L0:F8082, −0.115), and L0:F14108 ("appropriate" at pos 2, −0.142) — combined with a deep sentence-start "The castle itself..." path (L5–L8) that the model appears to use to detect the **restated premise** before the contradiction.

**Confidence:** 6/10

**Reasoning:**

The circuit is dominated by two opposing streams feeding the probe:

1. **Premise content (pushes toward contradiction)** — L4:F13244 ("land/estate/slavery" at pos 2 castle, +0.287; frac_nonzero 0.0045) and L4:F5749 ("ancient settlements/fortifications" at pos 2 and pos 13, −0.123 / +0.094) directly read the premise entities "castle" / "tower" / "early 17th-century". These in turn are activated by the **Emb: castle (pos 2)** and **Emb: tower (pos 13)** token embeddings (direct_effect 18.5 and 23.1). The "early" temporal features L2:F4429 (pos 6 and 39, +0.138 / +0.119) and L0:F5494/L0:F4367/L0:F1454 fire on the repeated "early" / "century" tokens, which is genuine premise-vs-hypothesis overlap detection, **not** spurious.

2. **Lexical / negation-like markers (mixed) — partially validates the user's concern**: 
   - L0:F10815 = the word "any" at pos 38, **+0.117** toward contradiction. "any" is a quantifier in the negation "does not contain any early 17th-century tower houses" — this is genuinely hypothesis-side lexical content, but it is a **single word detector**, not a true negation/sentiment feature.
   - L0:F8974 = the word "from" at pos 20, **−0.124** (pushes *against* contradiction). Generic function word.
   - L0:F8082 = "itself" at pos 3, **−0.115**. Again, a function-word reflex pronoun.
   - L0:F2158 = "with" at pos 17, +0.191. Pure preposition.
   - L0:F7513 = "together" at pos 26, +0.132. Pure adverb.
   - L2:F1430 = "house/houses" at pos 14, **−0.221** (largest single suppressor). This is the **only** feature that fires specifically on the *content* noun of the hypothesis ("tower houses") and it pushes the probe *away* from contradiction.
   - L1:F11220 = "restored" at pos 16, −0.148.

3. **Sentence-start "The castle itself" deep path (L5–L8)** — L8:F8406, L7:F462, L7:F5741, L6:F14585, L5:F3992 all fire on pos 1 ("The") with very large activations (29–34). Upstream they trace to the bos and "The" embeddings. This path is **about detecting the sentence boundary of the restated premise**, not about contradiction per se — it likely supports the model's implicit alignment of the two "The castle itself…" sentences.

4. **get_source_influence corroborates** — the hypothesis segment (pos 33–39) carries only 5.6% signed share, and the broader premise (pos 2–32) carries 11.4% with S_over_R = 2.2, i.e. the **premise side drives the probe more than any single non-source driver**, but the influence is split across many small word-level features rather than concentrated on contradiction-semantic features.

**Verdict on user concern (partially confirmed):** The probe is **not** using a clean "negation detector." However, a substantial fraction of the signal is carried by **single-word lexical detectors** ("any", "from", "with", "together", "itself") with no semantic content beyond the surface word. The only true semantic contradiction signal is implicit: L2:F4429 firing on **both** "early" occurrences (premise pos 6 and hypothesis pos 39) — the model uses word-repetition to align premise↔hypothesis, and the *absence* of an "early" or "tower" feature in the hypothesis is what flips the score toward contradiction. The "any" feature (+0.117) is a legitimate hypothesis-side cue, not a spurious negation reflex. The "house" feature at L2 (pos 14, −0.221) is the strongest suppressor, indicating the model also recognizes the *shared* noun and partially cancels the contradiction. Overall: the circuit mixes shallow word-level features with genuine temporal/architectural entity features, and the contradiction signal is diffuse rather than localized to a "negation" detector.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F13244](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) | 2 | Premise content features (castle/tower/century/early/restore) |  terms related to land ownership and administration, possibly including slavery or other forms of forced labor | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) |
| [L4:F13244](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) | 14 | Premise content features (castle/tower/century/early/restore) |  terms related to land ownership and administration, possibly including slavery or other forms of forced labor | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) |
| [L4:F5749](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) | 2 | Premise content features (castle/tower/century/early/restore) |  terms that describe ancient settlements and fortifications | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) |
| [L4:F5749](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) | 13 | Premise content features (castle/tower/century/early/restore) |  terms that describe ancient settlements and fortifications | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) |
| [L2:F1430](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1430) | 14 | Premise "house/houses" word feature (suppresses contradiction) | mentions of the U.S. White House or a generic house | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1430) |
| [L6:F486](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/486) | 14 | Mid-layer Scottish/architectural features (L6-L8) |  Scottish locations and political terms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/486) |
| [L8:F8406](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) | 1 | Mid-layer Scottish/architectural features (L6-L8) | the first-person pronoun "I" and the word "Exactly" | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) |
| [L2:F4429](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) | 6 | "early" temporal features (premise + hypothesis repetition) |  mentions of the beginning of a period | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) |
| [L2:F4429](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) | 39 | "early" temporal features (premise + hypothesis repetition) |  mentions of the beginning of a period | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) |
| [L0:F5494](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5494) | 6 | "early" temporal features (premise + hypothesis repetition) | the word "early" often related to time | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5494) |
| [L0:F1454](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1454) | 12 | "early" temporal features (premise + hypothesis repetition) |  mentions of specific centuries or decades | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1454) |
| [L0:F4367](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4367) | 12 | "early" temporal features (premise + hypothesis repetition) |  references to centuries | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4367) |
| [L0:F2158](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) | 17 | Lexical/grammatical word features (low-level) | the word "with" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) |
| [L0:F7360](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7360) | 5 | Lexical/grammatical word features (low-level) | the word "an" and sometimes also the acronym COX | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7360) |
| [L0:F7513](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7513) | 26 | Lexical/grammatical word features (low-level) | the word "together" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7513) |
| [L0:F8974](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) | 20 | Lexical/grammatical word features (low-level) | the word "from" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) |
| [L0:F10815](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10815) | 38 | Lexical/grammatical word features (low-level) |  the word "any". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10815) |
| [L0:F4079](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4079) | 13 | Lexical/grammatical word features (low-level) |  the words "exposure," "tower" and words related to legal trials | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4079) |
| [L0:F8082](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8082) | 3 | Lexical/grammatical word features (low-level) | the word "itself" and sometimes words ending in "ing" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8082) |
| [L1:F1027](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1027) | 13 | Lexical/grammatical word features (low-level) | the word "tower" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1027) |
| [L1:F11220](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11220) | 16 | Lexical/grammatical word features (low-level) | instances of the word "restore" and related words | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11220) |
| [L0:F14108](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14108) | 2 | Lexical/grammatical word features (low-level) | the word "appropriate" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14108) |
| [L3:F10598](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10598) | 3 | Lexical/grammatical word features (low-level) | the word "himself" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10598) |
| [L7:F462](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) | 1 | "The castle itself..." sentence-start deep path | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) |
| [L7:F5741](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5741) | 1 | "The castle itself..." sentence-start deep path | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5741) |
| [L6:F14585](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14585) | 1 | "The castle itself..." sentence-start deep path | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14585) |
| [L5:F3992](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3992) | 1 | "The castle itself..." sentence-start deep path | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3992) |
| [L2:F3491](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3491) | 37 | Hypothesis "does not contain any early 17th-century tower houses" |  the word "effect" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3491) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:13244 de=0.287 |
| 3 | `inspect_feature` ×19 | L4:13244, L2:1430, L0:2158, L0:7360, L1:1027, L0:5494, L1:11220, L0:14108, L2:4429, L0:7513, L6:486, L0:8974, L4:5749, L3:10598, L0:4367, L0:10815, L0:8082, L0:4079, L8:8406 |
| 4 | `get_upstream_features` | Emb:" castle"@2 (de=18.50) +9 more |
| 5 | `get_upstream_features` | Emb:" house"@14 (de=30.88) +9 more |
| 6 | `get_upstream_features` | Emb:" with"@17 (de=33.75) +9 more |
| 7 | `get_upstream_features` | Emb:" early"@6 (de=21.12) +9 more |
| 8 | `get_upstream_features` | Emb:" early"@6 (de=35.25) +9 more |
| 9 | `get_upstream_features` | Emb:" early"@39 (de=36.50) +9 more |
| 10 | `get_upstream_features` | Emb:" tower"@13 (de=23.12) +9 more |
| 11 | `get_upstream_features` | Emb:" restored"@16 (de=20.00) +9 more |
| 12 | `get_upstream_features` | Emb:" castle"@2 (de=11.81) +9 more |
| 13 | `get_upstream_features` | Emb:" together"@26 (de=43.00) +9 more |
| 14 | `get_upstream_features` | L5:F3316 (de=-2.38) +9 more |
| 15 | `get_upstream_features` | Emb:" from"@20 (de=39.75) +9 more |
| 16 | `get_upstream_features` | Emb:" itself"@3 (de=30.12) +9 more |
| 17 | `get_upstream_features` | Emb:" any"@38 (de=40.50) +9 more |
| 18 | `get_upstream_features` | Emb:" itself"@3 (de=19.88) +9 more |
| 19 | `get_upstream_features` | Emb:" tower"@13 (de=19.12) +9 more |
| 20 | `get_upstream_features` | Emb:" castle"@2 (de=14.75) +9 more |
| 21 | `get_upstream_features` | Emb:"century"@12 (de=23.12) +9 more |
| 22 | `get_upstream_features` | Emb:"<bos>"@0 (de=9.50) +9 more |
| 23 | `get_top_features` | 40 features; top: L4:13244 de=0.287 |
| 24 | `inspect_feature` ×13 | L451:17, L17:451, L0:1454, L0:5565, L2:6657, L1:6745, L3:11311, L6:5289, L0:5224, L2:3491, L1:8005, L1:593, L2:6867 |
| 25 | `get_upstream_features` | ❌ Feature (layer=17, pos=1, feature_idx=17) not found in graph |
| 26 | `get_upstream_features` | Emb:" contain"@37 (de=23.25) +9 more |
| 27 | `get_upstream_features` | Emb:" tower"@13 (de=15.31) +9 more |
| 28 | `get_upstream_features` | Emb:" restored"@16 (de=9.50) +9 more |
| 29 | `get_upstream_features` | Emb:"century"@12 (de=19.12) +9 more |
| 30 | `get_upstream_features` | Emb:" any"@38 (de=3.56) +9 more |
| 31 | `get_upstream_features` | L4:F13244 (de=6.09) +9 more |
| 32 | `get_upstream_features` | Emb:" castle"@2 (de=8.69) +9 more |
| 33 | `get_upstream_features` | Emb:" itself"@3 (de=15.25) +9 more |
| 34 | `get_upstream_features` | Emb:" itself"@3 (de=19.75) +9 more |
| 35 | `get_upstream_features` | Emb:" itself"@3 (de=13.50) +9 more |
| 36 | `get_upstream_features` | Emb:" comprises"@4 (de=18.50) +9 more |
| 37 | `get_upstream_features` | Emb:"7"@9 (de=9.94) +9 more |
| 38 | `get_upstream_features` | Emb:" comprises"@4 (de=13.12) +9 more |
| 39 | `get_upstream_features` | Emb:" comprises"@4 (de=13.75) +9 more |
| 40 | `get_upstream_features` | Emb:" castle"@2 (de=8.69) +9 more |
| 41 | `get_upstream_features` | Emb:" tower"@13 (de=18.50) +9 more |
| 42 | `get_upstream_features` | Emb:" itself"@3 (de=15.25) +9 more |
| 43 | `get_upstream_features` | Emb:" itself"@3 (de=19.75) +9 more |
| 44 | `get_source_influence` | {'depth': 2, 'source_positions': [33, 34, 35, 36, 37, 38, 39], 'S_pct_of_total': |
| 45 | `get_source_influence` | {'depth': 2, 'source_positions': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 |
| 46 | `get_top_features` | 15 features; top: L4:13244 de=0.287 |
| 47 | `get_upstream_features` | L5:F3316 (de=-2.38) +9 more |
| 48 | `get_upstream_features` | Emb:" itself"@3 (de=30.12) +9 more |
| 49 | `get_upstream_features` | L16:F10989 (de=-10.50) +9 more |
| 50 | `get_upstream_features` | Emb:"<bos>"@0 (de=18.75) +9 more |
| 51 | `get_upstream_features` | L5:F3992 (de=11.50) +9 more |
| 52 | `get_upstream_features` | Emb:"The"@1 (de=13.56) +9 more |
| 53 | `get_upstream_features` | Emb:"<bos>"@0 (de=22.62) +9 more |

### Build

`build_circuit` → 20 nodes, 23 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 85,239 | 9,252 | 769,091 | 0 | $0.0828 | — | — |
| **Total** | | **85,239** | **9,252** | **769,091** | **0** | **$0.0828** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 8s