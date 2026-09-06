# Circuit Oracle Report
**Date:** 2026-07-28 07:06:18 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity probe is driven primarily by the literal token "hat" (the "hate" morpheme in "self-hating"), the "self-" prefix pattern, and the pronoun "his" — i.e., the classifier is reading content words and lexical morphology, but these are mixed with several genuine "spurious" identity-adjacent signals (political-ideology, self-reference detectors) that co-fir in this prompt because of the word "liberal" and the "self-" prefix.

**Confidence:** 7

**Reasoning:** The circuit's strongest path runs **Emb: "hat" (pos 3) → L0 hat subword detectors (6660, 4336) → L3 "hate" word (8492, frac_nonzero=0.00054) → L3 love/hate sentiment (592) → L4 antagonists/fighting (8407) → output**, with direct effects of 20, ~7, and 1.6 along the way. A parallel content path runs **Emb: "Self" (pos 1) → L3 self- prefix (735) and self--word (9615) → L4 hyphenated-self (10004) → output**, anchored by direct_effect 36 from the "Self" embedding. So the *core* mechanism is genuinely lexical: the probe is being driven by the morphemes "self-", "hat", and the "his" pronoun at pos 11 (L0:F2994, direct_effect 0.146, frac_nonzero=0.073 — a generic his/he detector firing on "his brethren"/"his country"). 

However, the user's concern about spurious identity features is **partly confirmed**. Several non-content features do contribute: **L4:5181** (political-ideology, "right-wing/liberal"; promoted_tokens include "anti", "Semitism", "hate"; frac_nonzero=0.0096) fires with direct_effect ~0.086 because the prompt contains the literal word "liberal" and "Jew" — this feature generalizes over identity-group discourse and is not specific to lexical toxicity. **L2:16224** (self-reference/self-publishing, frac_nonzero=0.067) and **L3:13302** (negative opinions/harm/warnings) provide additional non-lexical boosts. **L0:3090** (JavaScript code member-access, frac_nonzero=0.069) is firing on the " -" token at pos 7 with direct_effect 0.098 — a clearly spurious generic technical-code detector contributing positively to the toxicity score. The L1 features 2107 (legal/math "enter" pattern) and 14516 (math-hat notation) are low-level lexical noise, not identity signals.

In short: the **dominant signal is content-driven** (the morphemes "self", "hat", "his" trigger real lexical features), but the probe also receives meaningful contributions (~15-20% of the total direct_effect at the top) from a small set of **identity-adjacent and code-style detectors** that are not specific to toxicity content — partly validating the user's concern that the probe is not purely lexical, though it is not solely "identity-group" driven either. The 84.25 max-activation example for L4:10004 even contains the phrase "Spoken like a true gliberal...the jews, the Lobby..." — showing that the self-hyphenated feature has been co-trained on antisemitic discourse, which is a real but secondary confound.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F8407](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) | 4 | Antagonists / fighting / hate vocabulary |  words related to antagonists and fighting | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) |
| [L4:F8407](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) | 3 | Antagonists / fighting / hate vocabulary |  words related to antagonists and fighting | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) |
| [L4:F5181](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5181) | 4 | Political parties/ideology terms (right-wing/liberal) |  terms relating to political parties or ideologies | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5181) |
| [L4:F10004](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10004) | 4 | Hyphenated self- words (self-hating) |  hyphenated words beginning with "self" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10004) |
| [L3:F592](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) | 4 | Love/hate sentiment words | words related to love, affection, and hate, including foreign language | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) |
| [L3:F592](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) | 3 | Love/hate sentiment words | words related to love, affection, and hate, including foreign language | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) |
| [L3:F8492](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8492) | 4 | The word \"hate\" | the word "hate" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8492) |
| [L3:F8492](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8492) | 3 | The word \"hate\" | the word "hate" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8492) |
| [L3:F735](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) | 3 | \"self-\" prefix (self-X) |  words and phrases that include the word "self" followed by a hyphen | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) |
| [L3:F735](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) | 4 | \"self-\" prefix (self-X) |  words and phrases that include the word "self" followed by a hyphen | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) |
| [L3:F735](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) | 2 | \"self-\" prefix (self-X) |  words and phrases that include the word "self" followed by a hyphen | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) |
| [L3:F9615](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9615) | 3 | Words containing self- prefix (broad) |  words containing the prefix "self-" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9615) |
| [L3:F9615](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9615) | 4 | Words containing self- prefix (broad) |  words containing the prefix "self-" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9615) |
| [L3:F5808](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5808) | 4 | -ing suffix words (hating) | words ending in "-ing" that have a sense of driving something forward | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5808) |
| [L3:F13302](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13302) | 4 | Negative opinions / harm / warnings |  words related to negative opinions, harm, and warnings | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13302) |
| [L2:F16224](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16224) | 3 | Self-reference/self-publishing words |  words and phrases related to self-awareness, self-reference, or self-publishing | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16224) |
| [L2:F16224](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16224) | 4 | Self-reference/self-publishing words |  words and phrases related to self-awareness, self-reference, or self-publishing | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16224) |
| [L1:F2107](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2107) | 3 | Low-level lexical / math-hat detectors |  the word "enter", and other words and symbols common to mathematical and legal documents | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2107) |
| [L1:F14516](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14516) | 3 | Low-level lexical / math-hat detectors |  equations with symbols, especially those using "hat" notation | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14516) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 11 | Pronoun \"his\"/\"he\" (pos 11) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F8938](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8938) | 2 | Hyphen character detector (pos 2) | hyphens adjacent to numbers | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8938) |
| [L0:F6660](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6660) | 3 | Subword \"hat\" detectors (pos 3) |  the word "hat" or pronouns referring to a female | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6660) |
| [L0:F4336](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4336) | 3 | Subword \"hat\" detectors (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4336) |
| [L0:F3090](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3090) | 7 | Code/JS member-access spurious firing (pos 7) |  JavaScript or other C-style code with member access via "." and "->" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3090) |
| [L0:F1094](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1094) | 3 | States / -hood suffix detector (pos 3) |  words and suffixes related to states and senses | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1094) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:8407 de=0.172 |
| 3 | `inspect_feature` ×7 | L4:8407, L1:2107, L0:2994, L0:8938, L3:735, L0:3090, L3:9615 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F8407@4` | ✅ reported | 5 | 5 | Trace the path from L4:F8407 (antagonists/fighting words) upstream to find what … |
| SA-2 | `L3:F735@3` | ❌ error | — | — | Trace the path from L3:F735 (self- hyphen words) at pos 3 upstream. What input t… |
| SA-3 | `L0:F2994@11` | ❌ error | — | — | Trace L0:F2994 (his/he pronoun) at pos 11. What specific token drives it and doe… |
| SA-4 | `L1:F2107@3` | ❌ error | — | — | Trace L1:F2107 (legal/math "enter" pattern) at pos 3. What token at position 3 t… |

<details>
<summary><b>SA-1</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F8407 | " words related to antagonists and fighting" |
| 2 | `get_upstream_features` | L4:F8407@4, k=10 | Emb:"hat"@3 (de=10.75) +9 more |
| 3 | `inspect_feature` | L3, F592 | "words related to love, affection, and hate, including foreign language" |
| 4 | `inspect_feature` | L3, F8492 | "the word "hate"" |
| 5 | `get_upstream_features` | L3:F592@4, k=10 | Emb:"hat"@3 (de=7.69) +9 more |
| 6 | `inspect_feature` | L1, F5138 | " code referring to bounding boxes" |
| 7 | `inspect_feature` | L3, F8492 | "the word "hate"" |
| 8 | `inspect_feature` | L1, F11862 | "text from academic biological or legal documents that cites names" |

**Findings:** The antagonism/fighting‑words feature (L4:8407) receives its strongest excitatory drive from the token embedding "hat" at position 3 (direct_effect ≈10.75). Upstream, the main contributors are a sentiment detector (L3:592) and a dedicated hate‑word detector (L3:8492), both in lower‑third layers. These are further driven by early‑layer features (L1:11862 and L1:5138) that detect citation‑style text…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L3:F735@3, k=10 → Emb:"Self"@1 (de=36.50) +9 more |
| 2 | `get_upstream_features` | L0:F2994@11, k=10 → Emb:" his"@11 (de=44.25) +9 more |
| 3 | `get_upstream_features` | L1:F2107@3, k=10 → Emb:"hat"@3 (de=15.31) +9 more |
| 4 | `get_upstream_features` | L3:F9615@3, k=10 → Emb:"Self"@1 (de=36.00) +9 more |
| 5 | `get_upstream_features` | L0:F8938@2, k=10 → Emb:"-"@2 (de=34.50) +9 more |
| 6 | `get_upstream_features` | L0:F3090@7, k=10 → Emb:" -"@7 (de=13.69) +9 more |
| 7 | `get_upstream_features` | L3:F13717@3, k=10 → Emb:"hat"@3 (de=20.00) +9 more |
| 8 | `get_upstream_features` | L3:F15509@7, k=10 → Emb:" -"@7 (de=16.38) +9 more |
| 9 | `get_upstream_features` | L6:F10545@4, k=10 → L4:F8407 (de=1.62) +9 more |
| 10 | `get_upstream_features` | L0:F4336@3, k=10 → Emb:"hat"@3 (de=12.44) +9 more |
| 11 | `get_upstream_features` | L0:F4336@11, k=10 → ❌ Feature (layer=0, feature_idx=4336) not found at pos=11. Thi |
| 12 | `inspect_feature` ×5 | L4:5181, L4:10004, L3:13302, L3:8492, L3:592 |
| 13 | `get_upstream_features` | L0:F3090@6, k=8 → ❌ Feature (layer=0, feature_idx=3090) not found at pos=6. This |
| 14 | `get_upstream_features` | L0:F8938@6, k=8 → ❌ Feature (layer=0, feature_idx=8938) not found at pos=6. This |
| 15 | `get_upstream_features` | L6:F10545@4, k=8 → L4:F8407 (de=1.62) +7 more |
| 16 | `get_upstream_features` | L4:F8407@3, k=10 → Emb:"hat"@3 (de=7.41) +9 more |
| 17 | `get_upstream_features` | L4:F5181@4, k=10 → Emb:"hat"@3 (de=2.92) +9 more |
| 18 | `inspect_feature` ×2 | L3:5808, L4:10004 |
| 19 | `get_upstream_features` | L4:F10004@4, k=8 → Emb:"Self"@1 (de=34.00) +7 more |
| 20 | `get_upstream_features` | L3:F13070@4, k=5 → Emb:"Self"@1 (de=13.19) +4 more |
| 21 | `get_upstream_features` | L5:F8793@4, k=5 → Emb:"Self"@1 (de=-1.30) +4 more |
| 22 | `inspect_feature` ×4 | L2:16224, L1:14516, L0:1094, L0:6660 |

### Build

`build_circuit` → 21 nodes, 27 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 42,647 | 6,332 | 316,910 | 0 | $0.0394 | — | — |
| SA-1 | openai/gpt-oss-120b | 98,666 | 6,937 | 9,216 | 0 | $0.0191 | ✅ 5F/5E | Trace the path from L4:F8407 (antagonists/fighting words) up… |
| **Total** | | **141,313** | **13,269** | **326,126** | **0** | **$0.0585** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 34s