# Circuit Oracle Report
**Date:** 2026-07-28 07:22:17 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity classification is driven by a shallow, pattern-based circuit that latches onto the lexical form "Self-hating" (specifically the token "hat") plus a generic his/he pronoun detector, not on the identity-group content of the prompt.

**Confidence:** 4

**Reasoning:** The user's concern is well-supported. The circuit's strongest positive contributors are: **L4:F8407** ("antagonists and fighting," +0.17) and **L3:F735** ("self- followed by a hyphen," +0.14), both of which fire on the token "hat" in "Self-hating" — L3:F735's label explicitly mentions its top examples include "self-hating" contexts. Tracing upstream, F735's top input is the embedding of the "Self" token (direct_effect=29.6) followed by F8407's largest upstream is the "hat" embedding itself (direct_effect=10.75). The most identity-relevant feature, **L6:F10545** ("political rhetoric related to race, historical states, and government control," +0.09), does fire, but only at position 4 (i.e., it inherits the "hat" token's "hate" association via the antagonist detector rather than the "Jew" or "liberal" tokens). The **L0:F2994 "his/he" pronoun** detector (+0.15) is a strikingly generic feature (frac_nonzero=0.07, suppressed tokens literally include "his") — its largest upstream is just the "his" embedding (44.25). It is not entity-specific at all; it would fire on any sentence with a possessive masculine pronoun. Likewise, **L1:F2107** (legal/math "enter," +0.16) and **L0:F4336** (legal "favor," +0.10) appear to be triggered by the "hat" subword token resembling "hated" / legal boilerplate (their upstream is the "hat" embedding with direct_effects 15.3 and 12.4 respectively), not by anything in the actual identity-content. The token "Jew" at pos 6 contributes only marginally (direct_effect=0.18 to L0:F3090; 0.32 to L0:F2994) — the probe barely reads it. This is consistent with the user-described failure mode: the classifier's decision is dominated by **lexical co-occurrence patterns** (the bigram "self-hating" + a nearby masculine pronoun) rather than by the semantics of the targeted identity group or the actual slur structure of the sentence.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F8938](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8938) | 2 | Hyphen-adjacent-to-words (L0:F8938) | hyphens adjacent to numbers | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8938) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 11 | Generic his/he pronoun (L0:F2994) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F4336](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4336) | 3 | Legal/formal word 'favor' (L0:F4336) |  the word "favor" and words used in legal contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4336) |
| [L1:F2107](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2107) | 3 | Legal/math 'enter' (L1:F2107) |  the word "enter", and other words and symbols common to mathematical and legal documents | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2107) |
| [L3:F735](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) | 2 | self-hyphenated word phrases (L3:F735) |  words and phrases that include the word "self" followed by a hyphen | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) |
| [L3:F735](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) | 3 | self-hyphenated word phrases (L3:F735) |  words and phrases that include the word "self" followed by a hyphen | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) |
| [L3:F735](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) | 4 | self-hyphenated word phrases (L3:F735) |  words and phrases that include the word "self" followed by a hyphen | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) |
| [L3:F9615](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9615) | 3 | self- prefix words (L3:F9615) |  words containing the prefix "self-" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9615) |
| [L3:F9615](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9615) | 4 | self- prefix words (L3:F9615) |  words containing the prefix "self-" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9615) |
| [L3:F13717](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13717) | 3 | statistical 'hat' notation (L3:F13717) |  statistical estimation terms, especially those involving "hat" notation | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13717) |
| [L3:F592](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) | 3 | love/affection/hate vocabulary (L3:F592) | words related to love, affection, and hate, including foreign language | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) |
| [L3:F592](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) | 4 | love/affection/hate vocabulary (L3:F592) | words related to love, affection, and hate, including foreign language | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) |
| [L3:F8492](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8492) | 3 | formally-phrased text (L3:F8492) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8492) |
| [L3:F8492](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8492) | 4 | formally-phrased text (L3:F8492) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8492) |
| [L4:F8407](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) | 3 | Antagonists/fighting vocabulary (L4:F8407) |  words related to antagonists and fighting | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) |
| [L4:F8407](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) | 4 | Antagonists/fighting vocabulary (L4:F8407) |  words related to antagonists and fighting | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) |
| [L4:F5181](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5181) | 4 | Political-party/ideology terms (L4:F5181) |  terms relating to political parties or ideologies | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5181) |
| [L4:F10004](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10004) | 4 | Self- prefixed hyphenated words (L4:F10004) |  hyphenated words beginning with "self" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10004) |
| [L6:F10545](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10545) | 4 | Political rhetoric / race / government (L6:F10545) |  political rhetoric related to race, historical states, and government control | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10545) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:8407 de=0.172 |
| 3 | `inspect_feature` ×10 | L4:8407, L1:2107, L0:2994, L0:8938, L3:735, L3:9615, L3:13717, L0:3090, L0:4336, L6:10545 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F8407@4` | ❌ error | — | — | Trace the path from L4:F8407 ("words related to antagonists and fighting") at po… |
| SA-2 | `L0:F2994@11` | ❌ error | — | — | Trace the path from L0:F2994 (the pronoun "his"/"he") at pos 11. This is a very … |
| SA-3 | `L3:F735@4` | ❌ error | — | — | Trace the path from L3:F735 (self-hyphenated words) at pos 4. This fires on "Sel… |
| SA-4 | `L1:F2107@3` | ❌ error | — | — | Trace the path from L1:F2107 (legal/mathematical "enter" detector) at pos 3. Thi… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F8407@4, k=15 → Emb:"hat"@3 (de=10.75) +14 more |
| 2 | `get_upstream_features` | L3:F735@4, k=15 → Emb:"Self"@1 (de=29.62) +14 more |
| 3 | `get_upstream_features` | L0:F2994@11, k=10 → Emb:" his"@11 (de=44.25) +9 more |
| 4 | `get_upstream_features` | L1:F2107@3, k=10 → Emb:"hat"@3 (de=15.31) +9 more |
| 5 | `get_upstream_features` | L4:F8407@3, k=12 → Emb:"hat"@3 (de=7.41) +11 more |
| 6 | `get_upstream_features` | L6:F10545@4, k=10 → L4:F8407 (de=1.62) +9 more |
| 7 | `get_upstream_features` | L3:F735@3, k=10 → Emb:"Self"@1 (de=36.50) +9 more |
| 8 | `get_upstream_features` | L3:F735@2, k=10 → Emb:"Self"@1 (de=39.75) +9 more |
| 9 | `get_upstream_features` | L3:F592@3, k=8 → Emb:"hat"@3 (de=14.56) +7 more |
| 10 | `get_upstream_features` | L3:F8492@3, k=8 → Emb:"hat"@3 (de=19.38) +7 more |
| 11 | `get_upstream_features` | L0:F8938@2, k=5 → Emb:"-"@2 (de=34.50) +4 more |
| 12 | `inspect_feature` | L3, F592 → "words related to love, affection, and hate, including foreign language" |
| 13 | `get_upstream_features` | L0:F3090@7, k=5 → Emb:" -"@7 (de=13.69) +4 more |
| 14 | `get_upstream_features` | L0:F4336@3, k=5 → Emb:"hat"@3 (de=12.44) +4 more |
| 15 | `get_upstream_features` | L3:F10471@7, k=5 → Emb:" -"@7 (de=4.03) +4 more |
| 16 | `get_upstream_features` | L3:F9615@3, k=5 → Emb:"Self"@1 (de=36.00) +4 more |
| 17 | `get_upstream_features` | L3:F13717@3, k=5 → Emb:"hat"@3 (de=20.00) +4 more |
| 18 | `inspect_feature` ×2 | L4:5181, L4:10004 |

### Build

`build_circuit` → 22 nodes, 38 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 33,945 | 5,954 | 205,467 | 0 | $0.0297 | — | — |
| **Total** | | **33,945** | **5,954** | **205,467** | **0** | **$0.0297** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 27s