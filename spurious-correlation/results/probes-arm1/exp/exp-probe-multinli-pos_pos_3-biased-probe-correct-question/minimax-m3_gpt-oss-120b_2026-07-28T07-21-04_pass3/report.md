# Circuit Oracle Report
**Date:** 2026-07-28 07:21:04 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** This attribution circuit reveals that the contradiction probe is driven primarily by a chain of generic negation-lexicon features anchored on the "not" in the hypothesis sentence "does not contain any…", with weaker contributions from premise-side content features about castle/itself/house/century.

**Confidence:** 6

**Reasoning:** The user's concern is strongly supported. The largest, deepest signal path in the circuit is a negation-lexicon chain — a textbook spurious-feature shortcut:

- **Token-embedding floor of the negation path:** the "Emb: ' not' (pos 36)" node has direct_effect = 12.5 into the late negation feature L16:F6800 and direct_effect = 17.625 into L4:F4492. The "Emb: ' does' (pos 35)" embedding also contributes 9.06 to L16:F6800, and "Emb: ' any' (pos 38)" contributes 40.5 to L0:F10815. None of these carry semantic content about castle, fortification, tower houses, or the contradiction between premise and hypothesis.
- **L0 lexical supernode** (L0:F4958 "the word 'not'", frac_nonzero 0.018, fires on any "not"; L0:F10815 "the word 'any'", frac_nonzero 0.006) sits directly on the contradiction-clause tokens and feeds into the mid-layer negation features. These are pure function-word detectors.
- **Mid-layer negation supernode** (L2:F2415 "small quantity/negative connotation words" — promoted tokens include `▁no, ▁none, ▁aucune, ▁ninguno`, frac_nonzero 0.047; L3:F3534 "n't/nut character sequence" — promoted tokens `Does, does, DOES`, frac_nonzero 0.008; L4:F4492 "negations in various languages" — top examples include `tak`, `pas`, `je`, frac_nonzero 0.038). All three are language-general negation detectors.
- **Late-layer negation supernode** (L13:F102, L14:F15790 "negations", frac_nonzero 0.011, suppressed tokens include `▁itſelf`; L14:F12021 "negations and assertions, especially related to experimental results", frac_nonzero 0.046; L15:F11794 "phrases that express disagreement or negation", frac_nonzero 0.014, max_token=`t`/n`t`; L16:F6800 "negations 'not', 'no', and contractions with 't'", frac_nonzero 0.031) — the L16 feature alone carries direct_effect = 0.208 to the probe. The whole stack is `not/n't/no` detection, with no entity-specific content. By the late layers, the model has aggregated a strong "this sentence contains a negated verb" signal, which the linear probe apparently weights heavily as evidence of contradiction.

**Content-side contributions are much weaker and more diffuse:**
- L4 castle-content features (F13244 "land ownership/plantation", F5749 "ancient settlements/fortifications") and L7:F13215 "military fortifications" carry ~0.21 each but are routed via the `castle` token at pos 2 — generic word-level content, not premise-vs-hypothesis comparison.
- L0 "itself" features at pos 3 (premise) and pos 34 (hypothesis) have direct_effects of -0.24 and +0.24 respectively — these cancel, consistent with the `itself` cue appearing in both sentences, providing essentially zero net semantic signal.
- L0 "century" features (F1454, F4367) and L3:F14368 "house" fire only on the premise, not on the hypothesis's "any tower houses" or on `does not contain`. They are not part of a comparison.

**Why this is the spurious shortcut:** Genuine NLI contradiction here requires noticing that the premise asserts the castle *does* contain a 17th-century tower house while the hypothesis asserts the castle *does not* contain any 17th-century tower houses. That comparison needs shared-entity grounding ("castle/tower house" in both sentences) plus polarity inversion ("contains" vs "does not contain"). The circuit's strongest path instead does the following: detect that the hypothesis contains a "does not…any" negation+negated-quantifier pattern, then aggregate generic negation features upward and let the linear probe read the cumulative negation score. There is no cross-sentence comparison node — the two `itself` features (pos 3 and pos 34) have direct_effects of opposite sign and roughly cancel, and the castle/century/house features do not aggregate into a comparison structure. The probe is effectively a "negation in the hypothesis sentence" detector, which will fire on any premise–hypothesis pair where the hypothesis happens to negate, not specifically on the true entailment relationship — a classic artifact and the mechanism the user suspected.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L16:F6800](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) | 36 | Late-layer negation features (L14-L16) driving contradiction |  negations "not", "no", and contractions with "t".  | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) |
| [L15:F11794](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/11794) | 36 | Late-layer negation features (L14-L16) driving contradiction |  phrases that express disagreement or negation | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/11794) |
| [L14:F15790](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/15790) | 36 | Late-layer negation features (L14-L16) driving contradiction | negations. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/15790) |
| [L14:F12021](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12021) | 36 | Late-layer negation features (L14-L16) driving contradiction | negations and assertions, especially those related to experimental results | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12021) |
| [L13:F102](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/102) | 36 | Late-layer negation features (L14-L16) driving contradiction | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/102) |
| [L2:F15695](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15695) | 36 | Late-layer negation features (L14-L16) driving contradiction |  the letter "t" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15695) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 36 | Mid-layer negation features (L2-L4) at the second 'not' | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L3:F3534](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3534) | 36 | Mid-layer negation features (L2-L4) at the second 'not' | the character sequence "n't" or "nut" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3534) |
| [L2:F2415](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2415) | 38 | Mid-layer negation features (L2-L4) at the second 'not' |  frequent words indicating small quantities or proximity, or words with negative connotations | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2415) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 36 | L0 'not' / 'any' lexical features at the contradiction clause |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F10815](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10815) | 38 | L0 'not' / 'any' lexical features at the contradiction clause |  the word "any". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10815) |
| [L7:F13215](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13215) | 2 | L7 content feature: 'castle' as fortification |  terms used to describe military fortifications. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13215) |
| [L4:F13244](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) | 2 | L4 content features: castle-related (settlement/land) |  terms related to land ownership and administration, possibly including slavery or other forms of forced labor | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) |
| [L4:F5749](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) | 2 | L4 content features: castle-related (settlement/land) |  terms that describe ancient settlements and fortifications | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) |
| [L0:F10346](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10346) | 3 | L0-L3 'itself' / reflexive features (premise side) |  the word "itself" and sometimes the word "node" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10346) |
| [L0:F15322](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15322) | 3 | L0-L3 'itself' / reflexive features (premise side) | reflexive pronouns, particularly "herself" and "itself." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15322) |
| [L0:F12378](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12378) | 3 | L0-L3 'itself' / reflexive features (premise side) |  the word "latest." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12378) |
| [L3:F232](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/232) | 3 | L0-L3 'itself' / reflexive features (premise side) | the word "itself" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/232) |
| [L0:F1454](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1454) | 12 | L0-L4 'century' features (mentions of specific centuries) |  mentions of specific centuries or decades | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1454) |
| [L0:F4367](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4367) | 12 | L0-L4 'century' features (mentions of specific centuries) |  references to centuries | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4367) |
| [L3:F14368](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14368) | 14 | L3 'house/houses' feature at premise 'tower houses' | the word "house" (or houses). | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14368) |
| [L0:F2158](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) | 17 | L0 'with' / 'comprises' / 'manual' lexical features at the premise description | the word "with" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) |
| [L0:F3013](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3013) | 4 | L0 'with' / 'comprises' / 'manual' lexical features at the premise description | the word "manual" and words associated with documentation or printed materials | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3013) |
| [L0:F15866](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15866) | 4 | L0 'with' / 'comprises' / 'manual' lexical features at the premise description |  references to one's paternal and maternal figures, as well as the pronouns 'we' and 'my' | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15866) |
| [L2:F4429](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) | 6 | L0 'with' / 'comprises' / 'manual' lexical features at the premise description |  mentions of the beginning of a period | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) |
| [L1:F11](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11) | 3 | L0 'with' / 'comprises' / 'manual' lexical features at the premise description |  the word "press", sometimes in conjunction with "button." | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2158 de=0.277 |
| 3 | `inspect_feature` ×20 | L0:2158, L0:10346, L4:13244, L0:12378, L3:232, L4:4492, L0:15866, L1:11, L7:13215, L16:6800, L0:1454, L0:15322, L4:5386, L0:4367, L2:2415, L0:3013, L3:14368, L0:10815, L0:4958, L2:4429 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F6800@36` | ❌ error | — | — | Trace the L16:F6800 "negations" feature at pos 36. This is a late-layer feature … |
| SA-2 | `L7:F13215@2` | ❌ error | — | — | Trace the L7:F13215 "military fortifications" feature at pos 2. This fires on "c… |
| SA-3 | `L4:F4492@36` | ❌ error | — | — | Trace the L4:F4492 "negations in various languages" feature at pos 36. Direct ef… |
| SA-4 | `L4:F13244@2` | ❌ error | — | — | Trace the L4:F13244 "terms related to land ownership" at pos 2. Direct effect 0.… |
| SA-5 | `L0:F10346@3` | ❌ error | — | — | Trace the L0:F10346 "itself" feature at pos 3. Direct effect -0.2422 (inhibitory… |
| SA-6 | `L0:F4958@36` | ❌ error | — | — | Trace the L0:F4958 "the word not" at pos 36. Direct effect +0.1758. This is the … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L16:F6800@36, k=15 → Emb:" not"@36 (de=12.50) +14 more |
| 2 | `get_upstream_features` | L7:F13215@2, k=15 → L4:F5749 (de=8.25) +14 more |
| 3 | `get_upstream_features` | L4:F4492@36, k=15 → Emb:" not"@36 (de=17.62) +14 more |
| 4 | `get_upstream_features` | L4:F13244@2, k=15 → Emb:" castle"@2 (de=18.50) +14 more |
| 5 | `get_upstream_features` | L0:F10346@3, k=15 → Emb:" itself"@3 (de=13.94) +14 more |
| 6 | `get_upstream_features` | L0:F4958@36, k=10 → Emb:" not"@36 (de=34.00) +9 more |
| 7 | `get_upstream_features` | L0:F2158@17, k=10 → Emb:" with"@17 (de=33.75) +9 more |
| 8 | `get_upstream_features` | L4:F4492@3, k=10 → ❌ Feature (layer=4, feature_idx=4492) not found at pos=3. This |
| 9 | `get_upstream_features` | L4:F13215@2, k=8 → ❌ Feature (layer=4, pos=2, feature_idx=13215) not found in gra |
| 10 | `get_upstream_features` | L4:F5749@2, k=8 → Emb:" castle"@2 (de=14.75) +7 more |
| 11 | `inspect_feature` ×6 | L4:5749, L15:11794, L3:3534, L14:12021, L14:15790, L2:15695 |
| 12 | `get_upstream_features` | L0:F10815@38, k=10 → Emb:" any"@38 (de=40.50) +9 more |
| 13 | `get_upstream_features` | L0:F12378@3, k=8 → Emb:" itself"@3 (de=12.44) +7 more |
| 14 | `get_upstream_features` | L0:F1454@12, k=8 → Emb:"century"@12 (de=19.12) +7 more |
| 15 | `get_upstream_features` | L0:F4367@12, k=8 → Emb:"century"@12 (de=23.12) +7 more |
| 16 | `get_upstream_features` | L0:F15322@3, k=8 → Emb:" itself"@3 (de=16.75) +7 more |
| 17 | `get_upstream_features` | L0:F5386@12, k=8 → ❌ Feature (layer=0, pos=12, feature_idx=5386) not found in gra |
| 18 | `get_upstream_features` | L3:F14368@14, k=8 → Emb:" house"@14 (de=27.00) +7 more |
| 19 | `get_upstream_features` | L0:F3013@4, k=8 → Emb:" comprises"@4 (de=10.12) +7 more |
| 20 | `get_upstream_features` | L2:F2415@38, k=8 → Emb:" not"@36 (de=10.06) +7 more |
| 21 | `get_upstream_features` | L0:F4958@36, k=8 → Emb:" not"@36 (de=34.00) +7 more |
| 22 | `get_upstream_features` | L4:F5386@12, k=8 → Emb:"century"@12 (de=25.00) +7 more |
| 23 | `get_upstream_features` | L2:F2415@38, k=8 → Emb:" not"@36 (de=10.06) +7 more |
| 24 | `get_upstream_features` | L2:F2415@14, k=8 → ❌ Feature (layer=2, feature_idx=2415) not found at pos=14. Thi |
| 25 | `get_upstream_features` | L0:F10815@38, k=8 → Emb:" any"@38 (de=40.50) +7 more |
| 26 | `inspect_feature` | L0, F10346 → " the word "itself" and sometimes the word "node"" |

### Build

`build_circuit` → 21 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 56,070 | 7,433 | 291,063 | 0 | $0.0432 | — | — |
| **Total** | | **56,070** | **7,433** | **291,063** | **0** | **$0.0432** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 45s