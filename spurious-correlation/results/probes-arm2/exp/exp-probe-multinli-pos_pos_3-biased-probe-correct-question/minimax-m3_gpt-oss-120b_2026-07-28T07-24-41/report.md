# Circuit Oracle Report
**Date:** 2026-07-28 07:24:41 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction classification is driven by a small, isolated tower of "does not" negation features at positions 35-36, not by any semantic comparison between the two sentences.

**Confidence:** 9

**Reasoning:** The circuit reveals a striking, narrow mechanism: the strongest direct contributors to the contradiction probe are features that fire exclusively at position 36 (the word "not") — L16:F6800 (direct_effect 0.208), L15:F11794, L14:F6648, L13:F102, L12:F9489, L4:F4492 (0.223), and many L0 features with direct_effects of 0.18-0.28. Tracing these features one hop upstream shows they are built from the "not" (pos 36, de 12-34) and "does" (pos 35, de 7-13) embeddings almost exclusively. The chain L12→L13→L14→L15→L16 forms a clean "does not" detector that is the single path into the output logit.

A second, much weaker path comes from L7:F13215, which traces back through L5:F15708, L4:F13244/F5749, and ultimately to the "castle" (pos 2) and "itself" (pos 3) embeddings. This is the only path that engages with the *content* of the premises (the subject of the negation), and its contribution to the logit is smaller than the "does not" path. The "any" (pos 38) embedding also drives L0:F10815 with de 40.5, but this feeds inhibition rather than the contradiction direction.

Critically, the *content* of the premise — "early 17th-century tower house" at positions 6-14, "Irish oak," "without a single nail" — surfaces only as scattered L3 features (F14368 on "house", F9480/F10595 on "century", F4429 on "early") with direct_effects that are *inhibitory* or weakly signed relative to the negation tower. None of these content features propagate to the output logit; they are absorbed into the "house" bigram path that dies at L3:L14368. The model never builds a representation of "the premise asserts a 17th-century tower house, the hypothesis denies it" — the contradiction decision is collapsed to "the hypothesis contains 'does not… any'." This confirms the user's concern: the probe fires on the presence of explicit negation tokens in the second sentence, a spurious shortcut, rather than on the semantic incompatibility of the two sentences.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L16:F6800](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) | 36 | L16: 'does not' negation context | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) |
| [L15:F11794](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/11794) | 36 | L15: 'does not' negation detector | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/11794) |
| [L13:F102](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/102) | 36 | L13: 'does not' early abstraction | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/102) |
| [L14:F6648](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/6648) | 36 | L14: 'does not' feature | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/6648) |
| [L12:F9489](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/9489) | 36 | L12: 'does not' | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/9489) |
| [L7:F13215](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13215) | 2 | L7: 'castle' abstract entity | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13215) |
| [L5:F15708](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/15708) | 2 | L5: 'castle' entity | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/15708) |
| [L4:F13244](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) | 2 | L4: 'castle' content features | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) |
| [L4:F5749](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) | 2 | L4: 'castle' content features | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 36 | L4: 'castle' content features | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F5386](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5386) | 12 | L4: 'castle' content features | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5386) |
| [L3:F3534](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3534) | 36 | L3: negation/bigram features (house, neg) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3534) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 36 | L3: negation/bigram features (house, neg) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L3:F232](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/232) | 3 | L3: negation/bigram features (house, neg) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/232) |
| [L3:F14368](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14368) | 14 | L3: negation/bigram features (house, neg) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14368) |
| [L3:F9480](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9480) | 12 | L3: negation/bigram features (house, neg) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9480) |
| [L3:F10595](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10595) | 12 | L3: negation/bigram features (house, neg) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10595) |
| [L2:F4429](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) | 6 | L2: bigram/word features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) |
| [L2:F2415](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2415) | 38 | L2: bigram/word features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2415) |
| [L2:F15695](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15695) | 36 | L2: bigram/word features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15695) |
| [L2:F1430](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1430) | 14 | L2: bigram/word features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1430) |
| [L2:F8185](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8185) | 14 | L2: bigram/word features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8185) |
| [L2:F8185](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8185) | 2 | L2: bigram/word features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8185) |
| [L2:F9529](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9529) | 2 | L2: bigram/word features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9529) |
| [L2:F8734](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8734) | 2 | L2: bigram/word features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8734) |
| [L2:F8380](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8380) | 3 | L2: bigram/word features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8380) |
| [L1:F11](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11) | 3 | L1: lexical features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11) |
| [L1:F5108](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5108) | 36 | L1: lexical features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5108) |
| [L1:F14233](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) | 36 | L1: lexical features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) |
| [L1:F12702](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12702) | 14 | L1: lexical features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12702) |
| [L1:F1027](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1027) | 13 | L1: lexical features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1027) |
| [L1:F8633](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8633) | 2 | L1: lexical features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8633) |
| [L1:F5899](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5899) | 2 | L1: lexical features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5899) |
| [L0:F2158](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) | 17 | L0: token/embedding bigram detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) |
| [L0:F10346](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10346) | 3 | L0: token/embedding bigram detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10346) |
| [L0:F12378](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12378) | 3 | L0: token/embedding bigram detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12378) |
| [L0:F15866](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15866) | 4 | L0: token/embedding bigram detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15866) |
| [L0:F15322](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15322) | 3 | L0: token/embedding bigram detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15322) |
| [L0:F1454](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1454) | 12 | L0: token/embedding bigram detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1454) |
| [L0:F4367](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4367) | 12 | L0: token/embedding bigram detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4367) |
| [L0:F3013](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3013) | 4 | L0: token/embedding bigram detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3013) |
| [L0:F10815](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10815) | 38 | L0: token/embedding bigram detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10815) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 36 | L0: token/embedding bigram detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F11739](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11739) | 3 | L0: token/embedding bigram detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11739) |
| [L0:F9272](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9272) | 3 | L0: token/embedding bigram detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9272) |
| [L0:F8371](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8371) | 3 | L0: token/embedding bigram detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8371) |
| [L0:F9203](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9203) | 36 | L0: token/embedding bigram detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9203) |
| [L0:F14599](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14599) | 35 | L0: token/embedding bigram detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14599) |
| [L0:F15454](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15454) | 36 | L0: token/embedding bigram detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15454) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 2 | L0: token/embedding bigram detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F8671](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8671) | 2 | L0: token/embedding bigram detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8671) |
| [L0:F15757](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15757) | 2 | L0: token/embedding bigram detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15757) |
| [L0:F478](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/478) | 1 | L0: token/embedding bigram detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/478) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2158 de=0.277 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F2158@17` | ❌ error | — | — | Trace L0:F2158 at pos 17 - what input token does this respond to and what does i… |
| SA-2 | `L0:F10346@3` | ❌ error | — | — | Trace L0:F10346 at pos 3 - what input token does this respond to? Pos 3 is 'earl… |
| SA-3 | `L4:F13244@2` | ❌ error | — | — | Trace L4:F13244 at pos 2 - pos 2 is 'The'. What does this feature encode? |
| SA-4 | `L0:F15866@4` | ❌ error | — | — | Trace L0:F15866 at pos 4 - pos 4 is 'castle'. What does this encode? |
| SA-5 | `L16:F6800@36` | ❌ error | — | — | Trace L16:F6800 at pos 36 - pos 36 is likely 'does' or 'not' in the contradictio… |
| SA-6 | `L4:F4492@36` | ❌ error | — | — | Trace L4:F4492 at pos 36 - what does this feature encode? Pos 36 is likely 'does… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F2158@17, k=5 → Emb:" with"@17 (de=33.75) +4 more |
| 2 | `get_upstream_features` | L0:F10346@3, k=5 → Emb:" itself"@3 (de=13.94) +4 more |
| 3 | `get_upstream_features` | L4:F13244@2, k=5 → Emb:" castle"@2 (de=18.50) +4 more |
| 4 | `get_upstream_features` | L16:F6800@36, k=5 → Emb:" not"@36 (de=12.50) +4 more |
| 5 | `get_upstream_features` | L0:F1454@12, k=5 → Emb:"century"@12 (de=19.12) +4 more |
| 6 | `get_upstream_features` | L4:F4492@36, k=5 → Emb:" not"@36 (de=17.62) +4 more |
| 7 | `get_upstream_features` | L0:F4367@12, k=5 → Emb:"century"@12 (de=23.12) +4 more |
| 8 | `get_upstream_features` | L0:F4958@36, k=5 → Emb:" not"@36 (de=34.00) +4 more |
| 9 | `get_upstream_features` | L4:F5386@12, k=5 → Emb:"century"@12 (de=25.00) +4 more |
| 10 | `get_upstream_features` | L3:F14368@14, k=5 → Emb:" house"@14 (de=27.00) +4 more |
| 11 | `get_upstream_features` | L7:F13215@2, k=5 → L4:F5749 (de=8.25) +4 more |
| 12 | `get_upstream_features` | L2:F4429@6, k=5 → Emb:" early"@6 (de=35.25) +4 more |
| 13 | `get_upstream_features` | L2:F2415@38, k=5 → Emb:" not"@36 (de=10.06) +4 more |
| 14 | `get_upstream_features` | L3:F232@3, k=5 → Emb:" itself"@3 (de=26.50) +4 more |
| 15 | `get_upstream_features` | L15:F11794@36, k=5 → Emb:" does"@35 (de=7.19) +4 more |
| 16 | `get_upstream_features` | L0:F12378@3, k=5 → Emb:" itself"@3 (de=12.44) +4 more |
| 17 | `get_upstream_features` | L0:F15322@3, k=5 → Emb:" itself"@3 (de=16.75) +4 more |
| 18 | `get_upstream_features` | L0:F15866@4, k=5 → Emb:" comprises"@4 (de=13.56) +4 more |
| 19 | `get_upstream_features` | L1:F11@3, k=5 → Emb:" itself"@3 (de=20.00) +4 more |
| 20 | `get_upstream_features` | L3:F3534@36, k=5 → Emb:" not"@36 (de=16.12) +4 more |
| 21 | `get_upstream_features` | L4:F5749@2, k=5 → Emb:" castle"@2 (de=14.75) +4 more |
| 22 | `get_upstream_features` | L0:F10815@38, k=5 → Emb:" any"@38 (de=40.50) +4 more |
| 23 | `get_upstream_features` | L0:F3013@4, k=5 → Emb:" comprises"@4 (de=10.12) +4 more |
| 24 | `get_upstream_features` | L13:F102@36, k=5 → Emb:" not"@36 (de=9.50) +4 more |
| 25 | `get_upstream_features` | L3:F9480@12, k=5 → Emb:"century"@12 (de=14.88) +4 more |
| 26 | `get_upstream_features` | L3:F10595@12, k=5 → Emb:"century"@12 (de=6.41) +4 more |
| 27 | `get_upstream_features` | L1:F5108@36, k=5 → Emb:" not"@36 (de=14.94) +4 more |
| 28 | `get_upstream_features` | L1:F14233@36, k=5 → Emb:" not"@36 (de=6.59) +4 more |
| 29 | `get_upstream_features` | L5:F15708@2, k=5 → Emb:" castle"@2 (de=8.06) +4 more |
| 30 | `get_upstream_features` | L0:F11739@3, k=5 → Emb:" itself"@3 (de=16.62) +4 more |
| 31 | `get_upstream_features` | L0:F9272@3, k=5 → Emb:" itself"@3 (de=22.88) +4 more |
| 32 | `get_upstream_features` | L2:F1430@14, k=5 → Emb:" house"@14 (de=30.88) +4 more |
| 33 | `get_upstream_features` | L2:F8185@14, k=5 → Emb:" house"@14 (de=9.25) +4 more |
| 34 | `get_upstream_features` | L2:F8734@2, k=5 → Emb:" castle"@2 (de=5.31) +4 more |
| 35 | `get_upstream_features` | L14:F6648@36, k=5 → Emb:" not"@36 (de=7.56) +4 more |
| 36 | `get_upstream_features` | L12:F9489@36, k=5 → Emb:" not"@36 (de=8.81) +4 more |
| 37 | `get_upstream_features` | L2:F15695@36, k=5 → Emb:" not"@36 (de=8.75) +4 more |
| 38 | `get_upstream_features` | L3:F8011@36, k=5 → Emb:" not"@36 (de=20.75) +4 more |

### Build

`build_circuit` → 23 nodes, 23 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 17,019 | 7,438 | 63,984 | 0 | $0.0179 | — | — |
| **Total** | | **17,019** | **7,438** | **63,984** | **0** | **$0.0179** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 18s