# Circuit Oracle Report
**Date:** 2026-07-28 07:24:14 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction probe is driven primarily by a coincidence of three shallow signals — (1) a repeated "early" subword pattern, (2) reflexive/intensive pronoun "itself", and (3) lexical content-word features — all of which happen to fire in sentences of this Wikipedia sentence-pair NLI format. Crucially, the strongest circuit branch is the embedding of "early" (pos 6, direct_effect=35.25; pos 39, direct_effect=36.5) flowing into L2:F4429 ("beginning of a period", which fires strongly on `early`) and then directly into the probe logit. There is no "negation word" feature in this graph — neither "not" nor "does" appear in the top 20 features.

**Confidence:** 7

**Reasoning:**

**What actually drives the probe:** The "contradiction" probe is reading off surface artifacts of the NLI prompt format rather than semantic contradiction. The strongest direct effects on the probe come from L0 lexical features (`tower`, `house`, `an`, `with`, `itself`, `together`, `early`, `century`, `any`, `from`) — all fired by the premise about Ballymena's "early 17th-century tower house" — but these features are *content-independent*: each is a single-word lexical feature that would fire just as strongly on the premise alone. Their frac_nonzero values are low (0.003-0.024) but the features themselves encode single common words, not contradictions.

**No genuine negation detector exists in this circuit.** The user's hypothesis of a "negation words" shortcut is not what the graph shows. "not" (pos 36) and "does" (pos 35) do not appear in the top 20 features. The closest thing to a contradiction-related signal is L3:F10598 ("himself") at direct_effect=+0.122 firing on "itself" (pos 3) — but this is the *intensive reflexive* in the premise ("The castle itself comprises…"), not the negation in the hypothesis. Its label fires on `▁himself`/`▁itself` and is being used as a generic reflexive-pronoun detector, not as a contradiction marker.

**The most informative features are topic/entity features, not contradiction features:**
- L4:F13244 ("land ownership/administration/plantation") and L4:F5749 ("ancient settlements/fortifications") at pos 2 and pos 14 — these are generic entity/genre features about castles and houses that fire equally in any castle-architecture Wikipedia sentence.
- L5:L6 "Scottish/Irish place" features (F3316 "Irish/Scottish cultural references", F486 "Scottish locations") — these are bleeding from pos 14 (the "house" token where the L2:L3 "house" complex activates its L3 Irish/Scottish sub-feature) up to higher layers. The model has learned that "tower house" + "Irish oak" is a strong Irish/Scottish castle signature, and this Scottish/Irish signal propagates through L7 code-documentation features (F462, F5741) to L8 "I" pronoun (F8406, direct_effect=-0.108). This is a topic-routing path, not a contradiction path.
- L1:F11220 ("restore" — at pos 16 on `restored`) — fires on the word `restored`, also completely content-neutral.

**Spurious shortcut confirmed, but the mechanism is "format/topic signal stacking" not "negation":** The probe's contradiction score increases because the text *looks like* a contradiction-pair (premise repeated, "does not contain" structure, plus all the lexical/topic features that fire on the premise's castle vocabulary). The strongest individual direct effects are: F13244 (+0.287), F1430 (-0.221), F2158 (+0.191, "with"), F7360 (+0.158, "an"), F1027 (+0.155, "tower"), F5494 (+0.152, "early"), F11220 (-0.148, "restored"), F14108 (-0.142, "appropriate"-suppressor on "castle"), F4429 (+0.138, "beginning of period" on "early" pos 6), F7513 (+0.132, "together"), F486 (+0.125, Scottish), F8974 (-0.124, "from"), F5749 (-0.123, ancient settlements), F10598 (+0.122, "himself/itself"), F4429 pos 39 (+0.119, "early"), F4367 (-0.117, century), F10815 (+0.117, "any"), F8082 (-0.115, "itself"), F4079 (+0.111, "tower/exposure"), F8406 (-0.108, "I" pronoun).

The user's specific concern — that "negation words" are the spurious feature — is *not* what this graph shows. There is no dedicated negation feature in the top 20. The actual spurious signals are: (a) the doubled "early" embedding pattern reinforcing the L2:F4429 "early" detector (which fires on the premise and doesn't distinguish entailment from contradiction), (b) the "itself" reflexive pronoun which fires on the premise's intensifier, and (c) a chain of castle/topic features (L4 → L5/L6 Scottish/Irish → L7 code-doc → L8 "I" pronoun) that has nothing to do with logical negation. The probe is essentially reading "this is the kind of sentence where contradiction pairs occur" via lexical/topic features, not via negation detection.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: castle (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: itself (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: an (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: early (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: century (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: tower (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: house (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 16 | Emb: restored (pos 16) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: with (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 20 | Emb: from (pos 20) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 26 | Emb: together (pos 26) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 39 | Emb: early (pos 39) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 38 | Emb: any (pos 38) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F2158](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) | 17 | Lexical content-word features (L0-L1) | the word "with" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) |
| [L0:F7360](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7360) | 5 | Lexical content-word features (L0-L1) | the word "an" and sometimes also the acronym COX | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7360) |
| [L0:F5494](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5494) | 6 | Lexical content-word features (L0-L1) | the word "early" often related to time | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5494) |
| [L0:F8974](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) | 20 | Lexical content-word features (L0-L1) | the word "from" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) |
| [L0:F7513](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7513) | 26 | Lexical content-word features (L0-L1) | the word "together" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7513) |
| [L0:F8082](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8082) | 3 | Lexical content-word features (L0-L1) | the word "itself" and sometimes words ending in "ing" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8082) |
| [L0:F1027](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1027) | 13 | Lexical content-word features (L0-L1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1027) |
| [L0:F4079](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4079) | 13 | Lexical content-word features (L0-L1) |  the words "exposure," "tower" and words related to legal trials | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4079) |
| [L0:F4367](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4367) | 12 | Lexical content-word features (L0-L1) |  references to centuries | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4367) |
| [L0:F10815](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10815) | 38 | Lexical content-word features (L0-L1) |  the word "any". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10815) |
| [L0:F14108](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14108) | 2 | Lexical content-word features (L0-L1) | the word "appropriate" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14108) |
| [L1:F11220](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11220) | 16 | Lexical content-word features (L0-L1) | instances of the word "restore" and related words | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11220) |
| [L2:F4429](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) | 6 | Beginning-of-period feature (L2:F4429) on 'early' (pos 6 & 39) |  mentions of the beginning of a period | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) |
| [L2:F4429](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) | 39 | Beginning-of-period feature (L2:F4429) on 'early' (pos 6 & 39) |  mentions of the beginning of a period | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) |
| [L2:F1430](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1430) | 14 | House/tower complex (L2-L3) | mentions of the U.S. White House or a generic house | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1430) |
| [L2:F8185](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8185) | 2 | House/tower complex (L2-L3) | places for shopping or military activities | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8185) |
| [L3:F14368](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14368) | 14 | House/tower complex (L2-L3) | the word "house" (or houses). | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14368) |
| [L1:F12702](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12702) | 14 | House/tower complex (L2-L3) | the word "house" or "homes" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12702) |
| [L0:F9604](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9604) | 14 | House/tower complex (L2-L3) |  the word "house" along with words about social class/gatherings | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9604) |
| [L4:F13244](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) | 2 | Castle/estate semantic (L4) |  terms related to land ownership and administration, possibly including slavery or other forms of forced labor | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) |
| [L4:F5749](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) | 2 | Castle/estate semantic (L4) |  terms that describe ancient settlements and fortifications | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) |
| [L4:F13244](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) | 14 | Castle/estate semantic (L4) |  terms related to land ownership and administration, possibly including slavery or other forms of forced labor | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) |
| [L4:F5749](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) | 14 | Castle/estate semantic (L4) |  terms that describe ancient settlements and fortifications | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) |
| [L4:F8583](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8583) | 14 | Castle/estate semantic (L4) |  historical references including people, titles, and dates | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8583) |
| [L1:F8633](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8633) | 2 | Castle/estate semantic (L4) |  words or phrases related to tourism and historical places | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8633) |
| [L5:F3316](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3316) | 14 | Scottish/Irish place + fortification (L5-L6) | Irish or Scottish geographical or cultural references, including names and places. | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3316) |
| [L6:F486](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/486) | 14 | Scottish/Irish place + fortification (L5-L6) |  Scottish locations and political terms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/486) |
| [L5:F3992](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3992) | 1 | Scottish/Irish place + fortification (L5-L6) | the start of documentation blocks in code | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3992) |
| [L6:F14585](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14585) | 1 | Scottish/Irish place + fortification (L5-L6) |  the words "the" and "it" at the beginning of sentences | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14585) |
| [L7:F462](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) | 1 | Scottish/Irish place + fortification (L5-L6) |  code documentation and import statements | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) |
| [L7:F5741](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5741) | 1 | Scottish/Irish place + fortification (L5-L6) |  code documentation or copyright information | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5741) |
| [L3:F10598](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10598) | 3 | Reflexive pronoun (L3:F10598 on 'itself') | the word "himself" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10598) |
| [L8:F8406](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) | 1 | First-person/I pronoun (L8:F8406) | the first-person pronoun "I" and the word "Exactly" | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe output (contradiction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:13244 de=0.287 |
| 3 | `inspect_feature` ×20 | L4:13244, L2:1430, L0:2158, L0:7360, L1:1027, L0:5494, L0:14108, L0:11220, L1:11220, L0:7513, L0:8974, L0:8082, L0:4079, L0:4367, L0:10815, L2:4429, L6:486, L3:10598, L4:5749, L8:8406 |
| 4 | `get_upstream_features` | Emb:" castle"@2 (de=18.50) +9 more |
| 5 | `get_upstream_features` | Emb:" early"@6 (de=35.25) +9 more |
| 6 | `get_upstream_features` | Emb:" early"@39 (de=36.50) +9 more |
| 7 | `get_upstream_features` | Emb:" house"@14 (de=30.88) +9 more |
| 8 | `get_upstream_features` | Emb:" restored"@16 (de=20.00) +9 more |
| 9 | `get_upstream_features` | Emb:" tower"@13 (de=23.12) +9 more |
| 10 | `get_upstream_features` | Emb:" with"@17 (de=33.75) +9 more |
| 11 | `get_upstream_features` | Emb:" an"@5 (de=27.38) +9 more |
| 12 | `get_upstream_features` | Emb:" early"@6 (de=21.12) +9 more |
| 13 | `get_upstream_features` | Emb:" from"@20 (de=39.75) +9 more |
| 14 | `get_upstream_features` | Emb:" together"@26 (de=43.00) +9 more |
| 15 | `get_upstream_features` | Emb:" any"@38 (de=40.50) +9 more |
| 16 | `get_upstream_features` | Emb:" castle"@2 (de=11.81) +9 more |
| 17 | `get_upstream_features` | Emb:" castle"@2 (de=14.75) +9 more |
| 18 | `get_upstream_features` | Emb:" itself"@3 (de=19.88) +9 more |
| 19 | `get_upstream_features` | Emb:" tower"@13 (de=19.12) +9 more |
| 20 | `get_upstream_features` | Emb:"century"@12 (de=23.12) +9 more |
| 21 | `get_upstream_features` | Emb:"<bos>"@0 (de=9.50) +9 more |
| 22 | `get_upstream_features` | Emb:" itself"@3 (de=30.12) +9 more |
| 23 | `get_upstream_features` | L5:F3316 (de=-2.38) +9 more |
| 24 | `get_upstream_features` | Emb:" itself"@3 (de=30.12) +9 more |
| 25 | `get_upstream_features` | Emb:" early"@39 (de=36.50) +9 more |
| 26 | `get_upstream_features` | Emb:" any"@38 (de=40.50) +9 more |
| 27 | `inspect_feature` ×2 | L1:1027, L1:11220 |
| 28 | `get_upstream_features` | L5:F3316 (de=-2.38) +9 more |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L8:F8406@1` | ❌ error | — | — | Trace the path from L8:F8406 — it's the "I" pronoun feature with direct_effect=-… |
| SA-2 | `L6:F486@14` | ❌ error | — | — | Trace the path from L6:F486 — Scottish locations feature, direct_effect=+0.125. … |
| SA-3 | `L3:F10598@3` | ❌ error | — | — | Trace the path from L3:F10598 — "himself" feature, direct_effect=+0.122. Where d… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` | L7, F8406 → " mathematical equations and symbols" |
| 2 | `get_upstream_features` | L7:F8406@1, k=5 → ❌ Feature (layer=7, pos=1, feature_idx=8406) not found in grap |
| 3 | `get_upstream_features` | L7:F462@1, k=10 → Emb:"<bos>"@0 (de=18.75) +9 more |
| 4 | `get_upstream_features` | L7:F5741@1, k=10 → L5:F3992 (de=11.50) +9 more |
| 5 | `get_upstream_features` | L3:F10598@3, k=5 → Emb:" itself"@3 (de=30.12) +4 more |
| 6 | `get_upstream_features` | L6:F486@14, k=5 → L5:F3316 (de=-2.38) +4 more |
| 7 | `inspect_feature` ×5 | L5:3992, L6:14585, L7:462, L7:5741, L1:1549 |
| 8 | `get_upstream_features` | L6:F486@14, k=5 → L5:F3316 (de=-2.38) +4 more |
| 9 | `get_upstream_features` | L1:F1549@3, k=5 → Emb:" itself"@3 (de=22.12) +4 more |
| 10 | `get_upstream_features` | L4:F13244@2, k=5 → Emb:" castle"@2 (de=18.50) +4 more |
| 11 | `get_upstream_features` | L0:F8082@3, k=5 → Emb:" itself"@3 (de=19.88) +4 more |
| 12 | `get_upstream_features` | L0:F14108@2, k=5 → Emb:" castle"@2 (de=11.81) +4 more |
| 13 | `get_upstream_features` | L4:F5749@2, k=5 → Emb:" castle"@2 (de=14.75) +4 more |
| 14 | `get_upstream_features` | L2:F4429@6, k=5 → Emb:" early"@6 (de=35.25) +4 more |
| 15 | `get_upstream_features` | L2:F4429@39, k=5 → Emb:" early"@39 (de=36.50) +4 more |
| 16 | `inspect_feature` ×8 | L0:9604, L1:7313, L1:2520, L1:12702, L2:8185, L1:8633, L1:14137, L0:1903 |
| 17 | `get_upstream_features` | L4:F13244@14, k=5 → Emb:" house"@14 (de=11.38) +4 more |
| 18 | `get_upstream_features` | L5:F3316@14, k=5 → Emb:" house"@14 (de=2.70) +4 more |
| 19 | `get_upstream_features` | L4:F8583@14, k=5 → Emb:" house"@14 (de=-5.06) +4 more |
| 20 | `get_upstream_features` | L0:F13200@13, k=5 → Emb:"century"@12 (de=3.38) +4 more |
| 21 | `get_upstream_features` | L0:F10633@13, k=5 → Emb:" tower"@13 (de=13.31) +4 more |
| 22 | `get_upstream_features` | L0:F14398@13, k=5 → Emb:" tower"@13 (de=15.25) +4 more |
| 23 | `inspect_feature` ×2 | L3:14368, L5:3316 |
| 24 | `get_upstream_features` | L4:F8583@14, k=5 → Emb:" house"@14 (de=-5.06) +4 more |
| 25 | `get_upstream_features` | L3:F14368@14, k=5 → Emb:" house"@14 (de=27.00) +4 more |
| 26 | `get_upstream_features` | L1:F5496@13, k=5 → Emb:" tower"@13 (de=5.69) +4 more |
| 27 | `inspect_feature` | L4, F8583 → " historical references including people, titles, and dates" |
| 28 | `get_upstream_features` | L2:F14368@14, k=5 → ❌ Feature (layer=2, pos=14, feature_idx=14368) not found in gr |
| 29 | `inspect_feature` | L1, F5496 → " mentions of kings, dukes, counts, and other European noble titles, an" |
| 30 | `get_upstream_features` | L1:F12702@14, k=5 → Emb:" house"@14 (de=23.88) +4 more |
| 31 | `get_upstream_features` | L2:F8185@2, k=5 → Emb:" castle"@2 (de=9.25) +4 more |
| 32 | `get_upstream_features` | L6:F486@14, k=5 → L5:F3316 (de=-2.38) +4 more |
| 33 | `get_upstream_features` | L5:F486@14, k=5 → ❌ Feature (layer=5, pos=14, feature_idx=486) not found in grap |
| 34 | `get_upstream_features` | L5:F3316@14, k=5 → Emb:" house"@14 (de=2.70) +4 more |
| 35 | `get_upstream_features` | L3:F14368@14, k=5 → Emb:" house"@14 (de=27.00) +4 more |
| 36 | `get_upstream_features` | L1:F11220@16, k=5 → Emb:" restored"@16 (de=20.00) +4 more |
| 37 | `inspect_feature` ×3 | L0:11516, L0:7732, L1:1430 |
| 38 | `get_upstream_features` | L1:F1430@14, k=5 → ❌ Feature (layer=1, pos=14, feature_idx=1430) not found in gra |
| 39 | `get_upstream_features` | L2:F1430@14, k=5 → Emb:" house"@14 (de=30.88) +4 more |
| 40 | `get_upstream_features` | L4:F13244@2, k=3 → Emb:" castle"@2 (de=18.50) +2 more |
| 41 | `get_upstream_features` | L4:F5749@2, k=3 → Emb:" castle"@2 (de=14.75) +2 more |
| 42 | `get_upstream_features` | L1:F1027@13, k=3 → Emb:" tower"@13 (de=23.12) +2 more |

### Build

`build_circuit` → 21 nodes, 30 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 109,086 | 10,371 | 1,731,885 | 0 | $0.1491 | — | — |
| **Total** | | **109,086** | **10,371** | **1,731,885** | **0** | **$0.1491** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 13s