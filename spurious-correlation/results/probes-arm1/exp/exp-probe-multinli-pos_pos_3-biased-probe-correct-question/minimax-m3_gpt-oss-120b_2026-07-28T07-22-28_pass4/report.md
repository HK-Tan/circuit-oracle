# Circuit Oracle Report
**Date:** 2026-07-28 07:22:28 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction probe's score is driven primarily by negation-word features (not/no/does not/any) at the end of the second sentence, with a weaker contribution from generic content features about the castle/tower house topic — the circuit relies on a spurious lexical negation cue rather than on any representation of the actual semantic contradiction between the premises.

**Confidence:** 6

**Reasoning:** The strongest direct effects on the probe are concentrated at position 36 (" not") and position 38 (" any") in the second sentence. Top features by direct_effect: L0:F4958 ("not", pos 36, direct=0.176), L0:F10815 (very high activation=38 on "any", pos 38, direct=−0.183), L0:F2158 ("with", pos 17, direct=0.277), L4:F4492 (negations in various languages, pos 36, direct=0.223), L0:F15866 ("father/my family", pos 4, direct=0.222), L0:F12378 ("latest", pos 3, direct=0.235), L0:F1454 (centuries/decades, pos 12, direct=0.207), L3:F14368 (the word "house" at pos 14, direct=−0.185), L16:F6800 (negations "not/no/n't", pos 36, direct=0.208). The L16:F6800 "negation" feature traces cleanly back to the ` not` embedding (direct=12.5) and ` does` embedding (direct=9.06) at positions 36/35, then to L4:F4492 (pos 36, direct=1.09) and L3:F3534 (pos 36, direct=3.06), all the way down to the ` not` token embedding via L0:F4958 (the word "not", pos 36, direct=2.88). The auxiliary-verb chain ` does`+` not`+` contain`+` any` is itself a strong contradiction signal. Mid-layer F2415 (pos 38, "any", promoted tokens include "no/none/aucune") reinforces the negation word class.

The user's hypothesis is **partially confirmed but overstated**. The circuit does contain a heavy negation-word sub-circuit that fires on ` not`, ` does`, ` any`, ` contain` — pure function-word negation cues that exist in the contradiction sentence but say nothing about what is contradicted. L16:F6800 (frac_nonzero=0.031) and L4:F4492 (frac_nonzero=0.038) are exactly the kind of "negation detectors" the user flags. However, the circuit is **not exclusively** negation-driven. There is a parallel content path: L4:F13244 (land/estate terms, pos 2, direct=0.239), L4:F5386 (pos 12, direct=−0.199), L7:F13215 (military fortifications, pos 2, direct=0.209), L0:F4367 and L0:F1454 (centuries at pos 12, direct=0.207 / −0.198) — these track ` castle`, ` tower`, ` house`, ` early`, ` 17th-century` (premise content). L0:F15322 (pos 3, " itself" direct=0.207) and L1:F11 (pos 3, direct=−0.221) signal the ` itself` repeat that links premise to hypothesis. So the model **does** pick up that the same entity ("castle itself") is in both sentences, plus its time-period attribute. But the dominant positive signal is the ` does not contain any` negation chain in sentence two, and the entity-recognition features (L4:F13244 "estate/land", L7:F13215 "fortification") are arguably also shallow lexical triggers rather than deep semantic representations. The result is a partly-spurious, partly-content cue mix: a probe relying on "negation present" plus a few entity words, with no clear component that compares premise to hypothesis to detect actual semantic conflict.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L16:F6800](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) | 36 | Late-layer negation detectors (L13-L16) |  negations "not", "no", and contractions with "t".  | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) |
| [L15:F11794](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/11794) | 36 | Late-layer negation detectors (L13-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/11794) |
| [L14:F6648](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/6648) | 36 | Late-layer negation detectors (L13-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/6648) |
| [L13:F102](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/102) | 36 | Late-layer negation detectors (L13-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/102) |
| [L13:F3295](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) | 36 | Late-layer negation detectors (L13-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 36 | Mid-layer negation / auxiliary verbs (L2-L4) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L3:F3534](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3534) | 36 | Mid-layer negation / auxiliary verbs (L2-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3534) |
| [L2:F2415](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2415) | 38 | Mid-layer negation / auxiliary verbs (L2-L4) |  frequent words indicating small quantities or proximity, or words with negative connotations | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2415) |
| [L2:F4429](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) | 6 | Mid-layer negation / auxiliary verbs (L2-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 36 | Early-layer lexical features (L0-L1) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F10815](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10815) | 38 | Early-layer lexical features (L0-L1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10815) |
| [L0:F2158](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) | 17 | Early-layer lexical features (L0-L1) | the word "with" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) |
| [L0:F4367](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4367) | 12 | Early-layer lexical features (L0-L1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4367) |
| [L0:F15322](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15322) | 3 | Early-layer lexical features (L0-L1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15322) |
| [L0:F12378](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12378) | 3 | Early-layer lexical features (L0-L1) |  the word "latest." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12378) |
| [L0:F1454](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1454) | 12 | Early-layer lexical features (L0-L1) |  mentions of specific centuries or decades | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1454) |
| [L1:F11](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11) | 3 | Early-layer lexical features (L0-L1) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11) |
| [L0:F10346](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10346) | 3 | Early-layer lexical features (L0-L1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10346) |
| [L4:F13244](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) | 2 | Content / entity features (L4-L7) |  terms related to land ownership and administration, possibly including slavery or other forms of forced labor | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) |
| [L4:F5386](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5386) | 12 | Content / entity features (L4-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5386) |
| [L7:F13215](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13215) | 2 | Content / entity features (L4-L7) |  terms used to describe military fortifications. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13215) |
| [L3:F14368](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14368) | 14 | Content / entity features (L4-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14368) |
| [L3:F232](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/232) | 3 | Content / entity features (L4-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/232) |
| [L4:F5749](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) | 2 | Content / entity features (L4-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2158 de=0.277 |
| 3 | `inspect_feature` ×10 | L0:2158, L4:13244, L0:12378, L4:4492, L0:15866, L7:13215, L16:6800, L0:1454, L0:4958, L2:2415 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F6800@36` | ❌ error | — | — | Trace the L16:F6800 negation feature upstream. This is a "not/no" negation featu… |
| SA-2 | `L4:F4492@36` | ❌ error | — | — | Trace L4:F4492 (negations in various languages) at pos 36. This is a negation de… |
| SA-3 | `L7:F13215@2` | ❌ error | — | — | Trace L7:F13215 (military fortifications) at pos 2. This is a content feature th… |
| SA-4 | `L0:F2158@17` | ❌ error | — | — | Trace L0:F2158 ("the word with") at pos 17. Determine what earlier embedding/fea… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L16:F6800@36, k=12 → Emb:" not"@36 (de=12.50) +11 more |
| 2 | `get_upstream_features` | L4:F4492@36, k=12 → Emb:" not"@36 (de=17.62) +11 more |
| 3 | `get_upstream_features` | L7:F13215@2, k=12 → L4:F5749 (de=8.25) +11 more |
| 4 | `get_upstream_features` | L4:F13244@2, k=12 → Emb:" castle"@2 (de=18.50) +11 more |
| 5 | `get_upstream_features` | L15:F11794@36, k=10 → Emb:" does"@35 (de=7.19) +9 more |
| 6 | `get_upstream_features` | L3:F3534@36, k=10 → Emb:" not"@36 (de=16.12) +9 more |
| 7 | `get_upstream_features` | L4:F5749@2, k=10 → Emb:" castle"@2 (de=14.75) +9 more |
| 8 | `get_upstream_features` | L0:F10346@3, k=10 → Emb:" itself"@3 (de=13.94) +9 more |
| 9 | `get_upstream_features` | L0:F15322@3, k=10 → Emb:" itself"@3 (de=16.75) +9 more |
| 10 | `get_upstream_features` | L0:F4367@12, k=10 → Emb:"century"@12 (de=23.12) +9 more |
| 11 | `get_upstream_features` | L0:F10815@38, k=10 → Emb:" any"@38 (de=40.50) +9 more |
| 12 | `get_upstream_features` | L3:F14368@14, k=10 → Emb:" house"@14 (de=27.00) +9 more |
| 13 | `get_upstream_features` | L3:F232@3, k=10 → Emb:" itself"@3 (de=26.50) +9 more |
| 14 | `get_upstream_features` | L4:F5386@12, k=10 → Emb:"century"@12 (de=25.00) +9 more |
| 15 | `inspect_feature` ×2 | L0:4958, L2:2415 |
| 16 | `get_upstream_features` | L2:F2415@38, k=10 → Emb:" not"@36 (de=10.06) +9 more |
| 17 | `get_upstream_features` | L0:F3013@4, k=10 → Emb:" comprises"@4 (de=10.12) +9 more |
| 18 | `get_upstream_features` | L2:F4429@6, k=10 → Emb:" early"@6 (de=35.25) +9 more |
| 19 | `get_upstream_features` | L1:F11@3, k=10 → Emb:" itself"@3 (de=20.00) +9 more |
| 20 | `get_upstream_features` | L4:F5749@2, k=10 → Emb:" castle"@2 (de=14.75) +9 more |
| 21 | `get_upstream_features` | L5:F15708@2, k=10 → Emb:" castle"@2 (de=8.06) +9 more |
| 22 | `get_upstream_features` | L6:F13795@2, k=10 → L4:F13244 (de=5.09) +9 more |
| 23 | `get_upstream_features` | L13:F102@36, k=10 → Emb:" not"@36 (de=9.50) +9 more |
| 24 | `get_upstream_features` | L14:F6648@36, k=10 → Emb:" not"@36 (de=7.56) +9 more |
| 25 | `get_upstream_features` | L13:F3295@36, k=10 → Emb:" not"@36 (de=18.00) +9 more |

### Build

`build_circuit` → 15 nodes, 15 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 33,378 | 7,539 | 214,791 | 0 | $0.0319 | — | — |
| **Total** | | **33,378** | **7,539** | **214,791** | **0** | **$0.0319** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 26s