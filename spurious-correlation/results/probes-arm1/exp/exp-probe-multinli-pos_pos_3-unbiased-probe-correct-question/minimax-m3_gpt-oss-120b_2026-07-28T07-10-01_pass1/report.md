# Circuit Oracle Report
**Date:** 2026-07-28 07:10:01 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction score is driven primarily by content-words from the premise (not negation words) — the model recognizes that "castle / tower / house / early 17th-century" terms appear in the premise while the hypothesis re-asserts the same content, with the late layers encoding building/Scottish-location features rather than explicit negation.

**Confidence:** 6/10

**Reasoning:** The circuit reveals a layered chain rooted in **content tokens from the premise**, not negation cues. At the input embedding layer, the dominant drivers are `castle` (pos 2, direct_effect 18.5→L4:F13244), `house` (pos 14, 30.9→L2:F1430; 19.9→L0:F9604; 11.4→L4:F13244), and `tower` (pos 13, 23.1→L1:F1027; 18.5→L4:F5749; 10.1→L4:F5749). These excite layer-0 token detectors (F9604 "house", F1027 "tower", F4079 "tower/legal", F3089 "housing/condos") and layer-2 composition features (F1430 "house/White House", F4429 "early period", F15739 "tower/radio"). The signal converges at layer 4 on **F13244** ("land/estate") and **F5749** ("ancient settlements/fortifications"), which then feed the layer-6 feature **F486** ("Scottish locations/political terms") — labeled Scottish but in this context driven entirely by the `house`/`tower` token chain (top input direct_effect 19.9 from `house` embedding → F9604 → F486). F486 and F13244 directly feed the probe output.

**Crucially, the user's hypothesis is partially supported but with a more nuanced picture.** The circuit does NOT primarily use pure negation words (`not`, `does`, `contain`, `any`) as a shortcut. The `any` (pos 38, L0:F10815, direct_effect 0.117), `not` (pos 36), and `does not contain` cluster fire at L0, but their contribution flows mainly through L2:F4429 ("early") and L2:F1430 ("house"), not through dedicated negation features. Instead, the probe picks up: (1) the hypothesis repeating the premise's content tokens (`early`, `tower`, `house`), (2) the `not … any` syntactic negation pattern, and (3) a small spurious L8:F8406 path driven by code-documentation detectors reacting to the initial "The" (frac_nonzero 0.009, negligible). So the dominant signal is **content-overlap plus a mild negation pattern**, with token-level repetition of "early 17th-century tower houses" being the strongest signal — the model appears to classify contradiction partly because the same content-words appear, modulated by the `not/any` negation. This is more lexical/syntactic than purely semantic, but it is not the "negation-word spurious feature" the user feared.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F9604](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9604) | 14 | Layer 0: 'house' token detector (also social class) |  the word "house" along with words about social class/gatherings | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9604) |
| [L0:F3089](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3089) | 14 | Layer 0: 'house' token detector (also social class) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3089) |
| [L0:F9457](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9457) | 14 | Layer 0: 'house' token detector (also social class) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9457) |
| [L0:F1027](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1027) | 13 | Layer 0: 'tower' token detector | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1027) |
| [L0:F4079](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4079) | 13 | Layer 0: 'tower' token detector |  the words "exposure," "tower" and words related to legal trials | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4079) |
| [L0:F13200](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13200) | 13 | Layer 0: 'tower' token detector | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13200) |
| [L0:F10633](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10633) | 13 | Layer 0: 'tower' token detector | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10633) |
| [L0:F14398](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14398) | 13 | Layer 0: 'tower' token detector | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14398) |
| [L0:F5494](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5494) | 6 | Layer 0: content-word token detectors (early, with, itself, any, from, together) | the word "early" often related to time | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5494) |
| [L0:F5494](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5494) | 39 | Layer 0: content-word token detectors (early, with, itself, any, from, together) | the word "early" often related to time | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5494) |
| [L0:F2158](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) | 17 | Layer 0: content-word token detectors (early, with, itself, any, from, together) | the word "with" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) |
| [L0:F8082](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8082) | 3 | Layer 0: content-word token detectors (early, with, itself, any, from, together) | the word "itself" and sometimes words ending in "ing" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8082) |
| [L0:F10815](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10815) | 38 | Layer 0: content-word token detectors (early, with, itself, any, from, together) |  the word "any". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10815) |
| [L0:F8974](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) | 20 | Layer 0: content-word token detectors (early, with, itself, any, from, together) | the word "from" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) |
| [L0:F7513](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7513) | 26 | Layer 0: content-word token detectors (early, with, itself, any, from, together) | the word "together" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7513) |
| [L1:F1027](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1027) | 13 | Layer 1: 'tower' composition feature | the word "tower" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1027) |
| [L1:F11220](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11220) | 16 | Layer 1: 'tower' composition feature | instances of the word "restore" and related words | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11220) |
| [L1:F8633](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8633) | 2 | Layer 1: 'tower' composition feature |  words or phrases related to tourism and historical places | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8633) |
| [L1:F8633](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8633) | 13 | Layer 1: 'tower' composition feature |  words or phrases related to tourism and historical places | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8633) |
| [L1:F5496](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5496) | 13 | Layer 1: 'tower' composition feature | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5496) |
| [L2:F1430](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1430) | 14 | Layer 2: 'house'/'White House' composition feature | mentions of the U.S. White House or a generic house | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1430) |
| [L2:F15739](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15739) | 13 | Layer 2: 'house'/'White House' composition feature | the word "tower," possibly in contexts relating to radio or construction | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15739) |
| [L2:F4429](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) | 6 | Layer 2: 'house'/'White House' composition feature |  mentions of the beginning of a period | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) |
| [L2:F4429](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) | 39 | Layer 2: 'house'/'White House' composition feature |  mentions of the beginning of a period | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) |
| [L2:F8185](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8185) | 2 | Layer 2: 'house'/'White House' composition feature | places for shopping or military activities | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8185) |
| [L2:F8185](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8185) | 14 | Layer 2: 'house'/'White House' composition feature | places for shopping or military activities | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8185) |
| [L3:F10598](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10598) | 3 | Layer 3: 'itself' reflexive + 'early' period-start composition | the word "himself" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10598) |
| [L3:F14368](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14368) | 14 | Layer 3: 'itself' reflexive + 'early' period-start composition | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14368) |
| [L4:F13244](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) | 2 | Layer 4: building/estate & fortification entity features |  terms related to land ownership and administration, possibly including slavery or other forms of forced labor | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) |
| [L4:F13244](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) | 14 | Layer 4: building/estate & fortification entity features |  terms related to land ownership and administration, possibly including slavery or other forms of forced labor | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) |
| [L4:F5749](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) | 2 | Layer 4: building/estate & fortification entity features |  terms that describe ancient settlements and fortifications | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) |
| [L4:F5749](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) | 13 | Layer 4: building/estate & fortification entity features |  terms that describe ancient settlements and fortifications | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) |
| [L4:F5749](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) | 14 | Layer 4: building/estate & fortification entity features |  terms that describe ancient settlements and fortifications | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) |
| [L4:F8583](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8583) | 14 | Layer 4: building/estate & fortification entity features |  historical references including people, titles, and dates | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8583) |
| [L6:F486](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/486) | 14 | Layer 6: Scottish-locations-political-terms (driven by house/tower token paths) |  Scottish locations and political terms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/486) |
| [L6:F486](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/486) | 13 | Layer 6: Scottish-locations-political-terms (driven by house/tower token paths) |  Scottish locations and political terms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/486) |
| [L8:F8406](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) | 1 | Layer 8: spurious syntactic / code-documentation 'I/Exactly' feature (pos 1) | the first-person pronoun "I" and the word "Exactly" | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:13244 de=0.287 |
| 3 | `inspect_feature` ×19 | L4:13244, L2:1430, L0:2158, L0:7360, L1:1027, L0:5494, L0:14108, L1:11220, L0:7513, L0:8974, L2:4429, L6:486, L0:4367, L3:10598, L0:8082, L0:4079, L4:5749, L8:8406, L0:10815 |
| 4 | `get_upstream_features` | Emb:" castle"@2 (de=18.50) +14 more |
| 5 | `get_upstream_features` | L5:F3316 (de=-2.38) +14 more |
| 6 | `get_upstream_features` | Emb:"<bos>"@0 (de=9.50) +14 more |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F13244@2` | ❌ error | — | — | Trace upstream from L4:F13244 (pos 2, "castle" embedding context). The feature a… |
| SA-2 | `L6:F486@14` | ✅ reported | 4 | 3 | Trace upstream from L6:F486 (pos 14). The feature label is "Scottish locations a… |
| SA-3 | `L8:F8406@1` | ✅ reported | 5 | 8 | Trace upstream from L8:F8406 (pos 1). The feature label is "the first-person pro… |

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F486 | " Scottish locations and political terms" |
| 2 | `get_upstream_features` | L6:F486@14, k=10 | L5:F3316 (de=-2.38) +9 more |
| 3 | `inspect_feature` | L4, F13244 | " terms related to land ownership and administration, possibly includin" |
| 4 | `inspect_feature` | L0, F9604 | " the word "house" along with words about social class/gatherings" |
| 5 | `inspect_feature` | L4, F5749 | " terms that describe ancient settlements and fortifications" |
| 6 | `get_upstream_features` | L4:F13244@14, k=10 | Emb:" house"@14 (de=11.38) +9 more |
| 7 | `get_upstream_features` | L4:F5749@14, k=10 | Emb:" tower"@13 (de=10.12) +9 more |
| 8 | `get_upstream_features` | L0:F9604@14, k=10 | Emb:" house"@14 (de=19.88) +9 more |
| 9 | `get_upstream_features` | L0:F9604@14, k=10 | Emb:" house"@14 (de=19.88) +9 more |
| 10 | `inspect_feature` | L2, F8185 | "places for shopping or military activities" |
| 11 | `inspect_feature` | L2, F1430 | "mentions of the U.S. White House or a generic house" |
| 12 | `inspect_feature` | L4, F8583 | " historical references including people, titles, and dates" |

**Findings:** Tracing upstream from the late‑layer feature L6:F486 (Scottish locations) reveals that its strongest excitatory inputs are (1) a layer‑4 feature (13244) that fires on estate‑related language, itself driven by the raw embedding of the token "house" at position 14; (2) a layer‑0 feature (9604) that is a direct detector for the word "house" and receives a massive direct effect from the same embedding…

</details>

<details>
<summary><b>SA-3</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L8, F8406 | "the first-person pronoun "I" and the word "Exactly"" |
| 2 | `get_upstream_features` | L8:F8406@1, k=10 | Emb:"<bos>"@0 (de=9.50) +9 more |
| 3 | `inspect_feature` | L7, F462 | " code documentation and import statements" |
| 4 | `inspect_feature` | L7, F5741 | " code documentation or copyright information" |
| 5 | `get_upstream_features` | L7:F462@1, k=10 | Emb:"<bos>"@0 (de=18.75) +9 more |
| 6 | `get_upstream_features` | L7:F5741@1, k=10 | L5:F3992 (de=11.50) +9 more |
| 7 | `inspect_feature` | L5, F3992 | "the start of documentation blocks in code" |
| 8 | `inspect_feature` | L6, F14585 | " the words "the" and "it" at the beginning of sentences" |

**Findings:** The L8:F8406 feature (pos 1) is not primarily a semantic detector for the pronoun "I" or the word "Exactly". Its strongest upstream drivers are low‑level code‑documentation detectors (features 462, 5741, 3992) and a generic sentence‑initial word detector (feature 14585). The token "The" at position 1 contributes a small positive direct effect (~1.55) via the embedding pathway, but the bulk of the …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F13244@14, k=20 → Emb:" house"@14 (de=11.38) +19 more |
| 2 | `get_upstream_features` | L0:F9604@14, k=15 → Emb:" house"@14 (de=19.88) +14 more |
| 3 | `get_upstream_features` | L4:F5749@14, k=15 → Emb:" tower"@13 (de=10.12) +14 more |
| 4 | `get_upstream_features` | L4:F13244@2, k=15 → Emb:" castle"@2 (de=18.50) +14 more |
| 5 | `get_upstream_features` | L2:F1430@14, k=20 → Emb:" house"@14 (de=30.88) +19 more |
| 6 | `get_upstream_features` | L1:F11220@16, k=15 → Emb:" restored"@16 (de=20.00) +14 more |
| 7 | `get_upstream_features` | L2:F4429@39, k=15 → Emb:" early"@39 (de=36.50) +14 more |
| 8 | `get_upstream_features` | L2:F4429@6, k=15 → Emb:" early"@6 (de=35.25) +14 more |
| 9 | `get_upstream_features` | L0:F2158@17, k=10 → Emb:" with"@17 (de=33.75) +9 more |
| 10 | `get_upstream_features` | L3:F10598@3, k=15 → Emb:" itself"@3 (de=30.12) +14 more |
| 11 | `get_upstream_features` | L1:F1027@13, k=15 → Emb:" tower"@13 (de=23.12) +14 more |
| 12 | `get_upstream_features` | L6:F486@14, k=15 → L5:F3316 (de=-2.38) +14 more |
| 13 | `get_upstream_features` | L0:F10815@38, k=10 → Emb:" any"@38 (de=40.50) +9 more |
| 14 | `get_upstream_features` | L0:F7513@26, k=10 → Emb:" together"@26 (de=43.00) +9 more |
| 15 | `get_upstream_features` | L0:F5494@6, k=10 → Emb:" early"@6 (de=21.12) +9 more |
| 16 | `get_upstream_features` | L6:F486@13, k=5 → L4:F5749 (de=2.12) +4 more |
| 17 | `inspect_feature` ×5 | L0:9604, L2:8185, L2:9529, L1:12474, L1:8633 |
| 18 | `get_upstream_features` | L6:F486@13, k=5 → L4:F5749 (de=2.12) +4 more |
| 19 | `get_upstream_features` | L2:F15739@13, k=5 → Emb:" tower"@13 (de=24.50) +4 more |
| 20 | `inspect_feature` ×3 | L2:15739, L0:4079, L0:4079 |
| 21 | `get_upstream_features` | L0:F14108@2, k=10 → Emb:" castle"@2 (de=11.81) +9 more |
| 22 | `get_upstream_features` | L0:F8974@20, k=5 → Emb:" from"@20 (de=39.75) +4 more |
| 23 | `get_upstream_features` | L4:F5749@2, k=5 → Emb:" castle"@2 (de=14.75) +4 more |
| 24 | `get_upstream_features` | L0:F4079@13, k=5 → Emb:" tower"@13 (de=19.12) +4 more |
| 25 | `get_upstream_features` | L6:F486@14, k=20 → L5:F3316 (de=-2.38) +19 more |
| 26 | `inspect_feature` ×3 | L4:8583, L4:3089, L2:9989 |
| 27 | `get_upstream_features` | L2:F4429@39, k=5 → Emb:" early"@39 (de=36.50) +4 more |
| 28 | `get_upstream_features` | L0:F10815@38, k=5 → Emb:" any"@38 (de=40.50) +4 more |
| 29 | `get_upstream_features` | L4:F5749@13, k=5 → Emb:" tower"@13 (de=18.50) +4 more |
| 30 | `get_upstream_features` | L1:F1027@13, k=5 → Emb:" tower"@13 (de=23.12) +4 more |
| 31 | `get_upstream_features` | L0:F9604@14, k=5 → Emb:" house"@14 (de=19.88) +4 more |
| 32 | `get_upstream_features` | L2:F1430@14, k=5 → Emb:" house"@14 (de=30.88) +4 more |
| 33 | `inspect_feature` | L6, F486 → " Scottish locations and political terms" |
| 34 | `get_upstream_features` | L6:F486@14, k=20 → L5:F3316 (de=-2.38) +19 more |
| 35 | `inspect_feature` ×4 | L0:5494, L2:4429, L0:2158, L0:5494 |
| 36 | `get_upstream_features` | L4:F5749@2, k=10 → Emb:" castle"@2 (de=14.75) +9 more |
| 37 | `inspect_feature` | L6, F486 → " Scottish locations and political terms" |

### Build

`build_circuit` → 20 nodes, 34 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 92,808 | 9,421 | 950,009 | 0 | $0.0961 | — | — |
| SA-3 | openai/gpt-oss-120b | 93,031 | 7,258 | 10,496 | 0 | $0.0185 | ✅ 5F/8E | Trace upstream from L8:F8406 (pos 1). The feature label is "… |
| SA-2 | openai/gpt-oss-120b | 174,421 | 11,059 | 0 | 0 | $0.0328 | ✅ 4F/3E | Trace upstream from L6:F486 (pos 14). The feature label is "… |
| **Total** | | **360,260** | **27,738** | **960,505** | **0** | **$0.1474** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 48s