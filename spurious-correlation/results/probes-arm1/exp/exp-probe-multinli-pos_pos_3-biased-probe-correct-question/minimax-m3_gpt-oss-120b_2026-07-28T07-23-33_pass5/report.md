# Circuit Oracle Report
**Date:** 2026-07-28 07:23:33 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

The user concern is validated. The circuit confirms the contradiction probe is being driven almost entirely by shallow lexical features anchored on the negation token "does not" in the second sentence, not by any genuine semantic comparison of the two premises.

**Analysis:** The probe's "contradiction" classification is driven by shallow lexical cues anchored on the negator "not" in the hypothesis, with secondary contributions from reflexive/century/castle-lexical features, rather than from any feature that compares the two premises' semantics.

**Confidence:** 8

**Reasoning:**

The circuit shows the probe (output logit) is fed by **five major supernodes**, four of which are pure surface-level lexical detectors:

1. **lex_not (largest contributor to the logit direction):** L0:F4958 ("the word 'not'", frac_nonzero=0.018, pos=36, direct_effect=+0.176), L3:F3534 ("n't/nut", frac_nonzero=0.008, pos=36), L0:F15322 (reflexives "itself/herself", pos=3), L0:F10815 ("any", pos=38, direct_effect=−0.183 — actually *inhibits* the probe), L0:F12378 ("latest", pos=3). The dominant signal in this group is L0:F4958, a pure word-identity detector for "not" — it fires on the literal token, not on any semantic notion of negation.

2. **neg_cross (L2/L4):** L2:F2415 ("small quantities or negative connotations", pos=38) and L4:F4492 ("negations in various languages", pos=36). Tracing L4:F4492 upstream shows its largest single direct_effect is the ` not` embedding at pos=36 (17.6) — a near-direct readout of the literal negator token.

3. **neg_disagree (L15-L16):** L15:F11794 ("phrases that express disagreement or negation") and L16:F6800 ("negations 'not', 'no', and contractions with 't'"). Tracing L16:F6800 reveals its top upstream contributors are *the literal embeddings* of ` not` (12.5) and ` does` (9.06), plus L4:F4492 — again pure surface form.

4. **lex_self, lex_century, lex_fort, lex_misc:** Additional single-word detectors ("itself", "century", "castle", "with", "latest", etc.) that contribute small signed effects but again encode token identity, not premise comparison.

What is *not* present anywhere in the top of the attribution graph: a feature representing the **semantic content** of premise A ("castle… early 17th-century tower house… held together without a single nail") being checked against hypothesis B ("does not contain any early 17th-century tower houses"). There is no entailment-comparison feature, no overlap/contradiction feature, and no entity-tracking circuit linking the two mentions of "tower house." The strongest positive contributions all share the same locus: the literal token ` not` at position 36, amplified through several layers of "not"/"n't"/disagreement detectors.

**This directly confirms the user's concern.** The probe classifies the pair as contradiction because the hypothesis contains the word "not" (and to a lesser extent "any" and the reflexive-emphasis pattern "does not contain any"), not because the model has computed that hypothesis A and B are logically inconsistent. On any premise where the negator appears in the second sentence — even a semantically entailed one, or one that shares the same subject — these features would fire and the probe would score it as contradiction. The signal is a classic lexical spurious correlation, not a semantic inference.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 36 | Emb: ' not' (pos 36) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 35 | Emb: ' does' (pos 35) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: ' castle' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: ' tower' (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: ' itself' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 36 | Lexical negation features (L0): 'not', 'n't' |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L3:F3534](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3534) | 36 | Lexical negation features (L0): 'not', 'n't' | the character sequence "n't" or "nut" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3534) |
| [L0:F15322](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15322) | 3 | Lexical negation features (L0): 'not', 'n't' | reflexive pronouns, particularly "herself" and "itself." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15322) |
| [L0:F10815](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10815) | 38 | Lexical negation features (L0): 'not', 'n't' |  the word "any". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10815) |
| [L0:F12378](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12378) | 3 | Lexical negation features (L0): 'not', 'n't' |  the word "latest." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12378) |
| [L2:F2415](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2415) | 38 | Cross-lingual negation features (L2/L4) |  frequent words indicating small quantities or proximity, or words with negative connotations | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2415) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 36 | Cross-lingual negation features (L2/L4) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L15:F11794](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/11794) | 36 | Negation/disagreement phrase features (L15-L16) |  phrases that express disagreement or negation | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/11794) |
| [L16:F6800](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) | 36 | Negation/disagreement phrase features (L15-L16) |  negations "not", "no", and contractions with "t".  | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) |
| [L0:F10346](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10346) | 3 | Reflexive pronoun features (L0-L3): 'itself' |  the word "itself" and sometimes the word "node" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10346) |
| [L3:F232](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/232) | 3 | Reflexive pronoun features (L0-L3): 'itself' | the word "itself" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/232) |
| [L0:F1](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1) | 1 | Reflexive pronoun features (L0-L3): 'itself' | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1) |
| [L0:F1454](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1454) | 12 | Lexical century features (L0/L4) |  mentions of specific centuries or decades | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1454) |
| [L0:F4367](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4367) | 12 | Lexical century features (L0/L4) |  references to centuries | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4367) |
| [L4:F5386](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5386) | 12 | Lexical century features (L0/L4) |  mentions of centuries and decades | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5386) |
| [L4:F5749](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) | 2 | Fortification / castle / estate features (L4-L7) |  terms that describe ancient settlements and fortifications | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) |
| [L4:F13244](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) | 2 | Fortification / castle / estate features (L4-L7) |  terms related to land ownership and administration, possibly including slavery or other forms of forced labor | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) |
| [L5:F15708](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/15708) | 2 | Fortification / castle / estate features (L4-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/15708) |
| [L7:F13215](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13215) | 2 | Fortification / castle / estate features (L4-L7) |  terms used to describe military fortifications. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13215) |
| [L3:F14368](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14368) | 14 | Fortification / castle / estate features (L4-L7) | the word "house" (or houses). | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14368) |
| [L0:F2158](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) | 17 | Misc lexical features (L0-L2) | the word "with" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) |
| [L0:F15866](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15866) | 4 | Misc lexical features (L0-L2) |  references to one's paternal and maternal figures, as well as the pronouns 'we' and 'my' | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15866) |
| [L1:F11](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11) | 3 | Misc lexical features (L0-L2) |  the word "press", sometimes in conjunction with "button." | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11) |
| [L2:F4429](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) | 6 | Misc lexical features (L0-L2) |  mentions of the beginning of a period | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) |
| [L0:F3013](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3013) | 4 | Misc lexical features (L0-L2) | the word "manual" and words associated with documentation or printed materials | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3013) |
| [L0:F2364](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2364) | 1 | Misc lexical features (L0-L2) |  the word "The" and opening HTML heading tags | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2364) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2158 de=0.277 |
| 3 | `inspect_feature` ×10 | L0:2158, L0:10346, L4:13244, L0:12378, L3:232, L4:4492, L0:15866, L1:11, L7:13215, L16:6800 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F6800@36` | ❌ error | — | — | Trace L16:F6800 (negations feature) upstream to identify which input tokens driv… |
| SA-2 | `L4:F4492@36` | ❌ error | — | — | Trace L4:F4492 (negations in various languages) upstream to identify which input… |
| SA-3 | `L0:F10346@3` | ❌ error | — | — | Trace L0:F10346 (the word "itself") upstream. This fires at pos=3 (the first "it… |
| SA-4 | `L7:F13215@2` | ❌ error | — | — | Trace L7:F13215 (military fortification terms) upstream. This fires at pos=2 ("c… |
| SA-5 | `L4:F13244@2` | ❌ error | — | — | Trace L4:F13244 (land ownership / estates) upstream. This fires at pos=2 ("compr… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L16:F6800@36, k=15 → Emb:" not"@36 (de=12.50) +14 more |
| 2 | `get_upstream_features` | L4:F4492@36, k=15 → Emb:" not"@36 (de=17.62) +14 more |
| 3 | `get_upstream_features` | L7:F13215@2, k=15 → L4:F5749 (de=8.25) +14 more |
| 4 | `get_upstream_features` | L4:F13244@2, k=15 → Emb:" castle"@2 (de=18.50) +14 more |
| 5 | `get_upstream_features` | L0:F10346@3, k=15 → Emb:" itself"@3 (de=13.94) +14 more |
| 6 | `inspect_feature` ×14 | L0:4958, L3:3534, L4:5749, L15:11794, L0:2364, L2:2415, L2:4429, L0:1454, L4:5386, L0:4367, L0:15322, L0:3013, L3:14368, L0:10815 |
| 7 | `get_upstream_features` | L5:F15708@2, k=10 → Emb:" castle"@2 (de=8.06) +9 more |
| 8 | `get_upstream_features` | L4:F5749@2, k=10 → Emb:" castle"@2 (de=14.75) +9 more |

### Build

`build_circuit` → 13 nodes, 18 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 47,917 | 5,331 | 172,057 | 0 | $0.0311 | — | — |
| **Total** | | **47,917** | **5,331** | **172,057** | **0** | **$0.0311** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 24s