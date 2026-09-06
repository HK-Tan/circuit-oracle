# Circuit Oracle Report
**Date:** 2026-07-28 07:19:30 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

The investigation is complete. The circuit reaches token embeddings for the critical features, and the picture is clear.

**Analysis:** The probe's toxicity classification is driven primarily by a tight cluster of literal lexical signals — the subword token "hat" in "hating" (the largest single contributor at L4:F8407 with direct_effect=0.17, plus its upstream L3:F8492 "the word 'hate'" detector with frac_nonzero=0.00054, and L3:F592 love/hate sentiment), the "self-" prefix (L3:F735/F9615), the pronoun "his" (L0:F2994), and a late-layer "race/political-rhetoric" feature (L6:F10545) — not by a generic "identity group is present" heuristic.

**Confidence:** 8

**Reasoning:** The user's hypothesis (that the circuit relies on a spurious "an identity group is present" signal) is **not supported** by this attribution graph. Instead, the circuit shows three distinct lexical mechanisms that all converge on toxicity-relevant vocabulary:

1. **Literal hate vocabulary (dominant path).** The "hating" token in the prompt is decomposed into the subwords "hat" (pos 3) and "ing" (pos 4). The "hat" embedding feeds an explicit "the word 'hate'" feature L3:F8492 (frac_nonzero=0.00054 — extremely sparse and specific to the literal token "hate"; top activating examples show racist commentary and direct hate speech), a love/hate sentiment feature L3:F592 (promoted tokens: "love", "hate"), and ultimately L4:F8407 "antagonists and fighting" (promoted tokens: "attacking", "hated", "Enemy", "villains"). The word "hate" itself is the single largest direct contributor to the probe (0.17 direct_effect at L4:F8407 pos 4), and is upstream-driven by the "hat" token embedding at direct_effect=10.75.

2. **Morphological "self-" prefix.** Two redundant features (L3:F735 "self-hyphenated", L3:F9615 "self- prefix") are activated by the "Self-" in "Self-hating". These are tied to lexical form, not identity. They are driven by the "Self" embedding (direct_effect 36–39) and have low frac_nonzero (~0.005–0.006), indicating they fire only on actual "self-" constructions.

3. **Pronoun "his".** L0:F2994 (frac_nonzero 0.073) is a generic pronoun detector with no identity-group signal — its top activating examples are diverse (movie reviews, historical biographies, hurricane reporting). The "his" at pos 11 refers to "his brethren and his country" and is just standard pronoun processing.

4. **Late-layer political/racial rhetoric (L6:F10545, direct_effect=0.086, frac_nonzero=0.038).** This is the closest thing to an "identity group" feature, but its top activating examples are not generic "group nouns" — they are explicitly about racial political rhetoric: "racial hysteria", "far-right", "racist", "slavery", "Nazi". Its promoted token list reinforces this: "anti", "Semitism", "hate", "hatred". This feature is downstream of the "hating" lexical signal and the political-ideology feature L4:F5181 (promoted: "anti", "Semitism", "hate"), and is **driven by the actual hateful content** of the prompt, not by a generic identity-group detector.

The only "spurious-looking" features in the graph are minor distractors: the "hyphen" detector L0:F8938 firing on "-" at pos 2 (direct_effect 0.14) and the "code/member-access" L0:F3090 / "git-diff" L3:F15509 features firing on " -" at pos 7 (direct_effect 0.098 / -0.086). These are low-level surface-form artifacts (the model segments "Self-hating" with a hyphen, the " -" between "Jew" and "a" looks like a diff hunk) and they actually push the probe **toward** or **against** toxicity based on punctuation shape, not based on identity.

In summary, the circuit reflects genuine toxicity detection: literal hate vocabulary + hate-speech rhetorical patterns, with the target identity ("Jew") being incidental scaffolding for the hateful predicate, not a feature being detected as a generic group cue. The user's concern is reasonable in general (toxicity probes can latch onto identity terms) but the attribution evidence here does not show that — it shows the probe latching onto the word "hate" and its morphological neighborhood.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 11 | Emb: ' his' (pos 11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'Self' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: '-' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: 'hat' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: ' -' (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 11 | Pronoun 'his'/'he' (L0:F2994) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F8938](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8938) | 2 | Hyphen-adjacent-to-text (L0:F8938) | hyphens adjacent to numbers | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8938) |
| [L0:F3090](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3090) | 7 | Code/member-access (L0:F3090) |  JavaScript or other C-style code with member access via "." and "->" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3090) |
| [L0:F4336](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4336) | 3 | 'favor'/legal terms (L0:F4336) |  the word "favor" and words used in legal contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4336) |
| [L1:F2107](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2107) | 3 | 'enter'/legal (L1:F2107) |  the word "enter", and other words and symbols common to mathematical and legal documents | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2107) |
| [L3:F735](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) | 2 | 'self-hyphenated' (L3:F735) |  words and phrases that include the word "self" followed by a hyphen | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) |
| [L3:F735](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) | 3 | 'self-hyphenated' (L3:F735) |  words and phrases that include the word "self" followed by a hyphen | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) |
| [L3:F735](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) | 4 | 'self-hyphenated' (L3:F735) |  words and phrases that include the word "self" followed by a hyphen | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) |
| [L3:F9615](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9615) | 3 | 'self-' prefix (L3:F9615) |  words containing the prefix "self-" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9615) |
| [L3:F9615](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9615) | 4 | 'self-' prefix (L3:F9615) |  words containing the prefix "self-" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9615) |
| [L3:F592](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) | 4 | Love/hate vocabulary (L3:F592) | words related to love, affection, and hate, including foreign language | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) |
| [L3:F15509](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15509) | 7 | Git-diff/code-diff format (L3:F15509) |  code diffs like those produced by `git diff` | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15509) |
| [L3:F13717](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13717) | 3 | 'hat' statistical notation (L3:F13717) |  statistical estimation terms, especially those involving "hat" notation | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13717) |
| [L4:F8407](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) | 3 | Antagonists/fighting (L4:F8407) |  words related to antagonists and fighting | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) |
| [L4:F8407](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) | 4 | Antagonists/fighting (L4:F8407) |  words related to antagonists and fighting | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) |
| [L4:F5181](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5181) | 4 | Political parties/ideologies (L4:F5181) |  terms relating to political parties or ideologies | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5181) |
| [L3:F5808](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5808) | 4 | '-ing' driving-forward (L3:F5808) | words ending in "-ing" that have a sense of driving something forward | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5808) |
| [L6:F10545](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10545) | 4 | Race/political-rhetoric (L6:F10545) |  political rhetoric related to race, historical states, and government control | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10545) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:8407 de=0.172 |
| 3 | `inspect_feature` ×11 | L4:8407, L1:2107, L0:2994, L3:9615, L0:8938, L3:735, L3:13717, L0:3090, L0:4336, L3:15509, L6:10545 |
| 4 | `get_upstream_features` | Emb:"hat"@3 (de=10.75) +9 more |
| 5 | `get_upstream_features` | L4:F8407 (de=1.62) +9 more |
| 6 | `get_upstream_features` | Emb:"Self"@1 (de=39.75) +9 more |
| 7 | `get_upstream_features` | Emb:"hat"@3 (de=7.69) +9 more |
| 8 | `get_upstream_features` | Emb:"Self"@1 (de=36.00) +9 more |
| 9 | `get_upstream_features` | Emb:"hat"@3 (de=2.92) +9 more |
| 10 | `get_upstream_features` | Emb:"hat"@3 (de=15.31) +9 more |
| 11 | `get_upstream_features` | Emb:" his"@11 (de=44.25) +9 more |
| 12 | `get_upstream_features` | Emb:"-"@2 (de=34.50) +9 more |
| 13 | `get_upstream_features` | Emb:" -"@7 (de=13.69) +9 more |
| 14 | `get_upstream_features` | Emb:"hat"@3 (de=12.44) +9 more |
| 15 | `inspect_feature` ×3 | L3:592, L4:5181, L3:5808 |
| 16 | `get_upstream_features` | Emb:"-"@2 (de=34.50) +9 more |
| 17 | `get_upstream_features` | Emb:" -"@7 (de=16.38) +9 more |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F10545@4` | ❌ error | — | — | Trace the upstream path for the 'race/political rhetoric' feature at L6:F10545 p… |
| SA-2 | `L4:F8407@4` | ✅ reported | 4 | 8 | Trace upstream from the 'antagonists and fighting' feature L4:F8407 pos 4. This … |
| SA-3 | `L0:F2994@11` | ❌ error | — | — | Trace upstream from the 'his' pronoun feature L0:F2994 pos 11. The 'his' at pos … |

<details>
<summary><b>SA-2</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F8407 | " words related to antagonists and fighting" |
| 2 | `get_upstream_features` | L4:F8407@4, k=10 | Emb:"hat"@3 (de=10.75) +9 more |
| 3 | `inspect_feature` | L3, F592 | "words related to love, affection, and hate, including foreign language" |
| 4 | `inspect_feature` | L3, F8492 | "the word "hate"" |
| 5 | `inspect_feature` | L1, F5138 | " code referring to bounding boxes" |
| 6 | `get_upstream_features` | L3:F592@4, k=10 | Emb:"hat"@3 (de=7.69) +9 more |
| 7 | `get_upstream_features` | L3:F8492@4, k=10 | Emb:"hat"@3 (de=12.75) +9 more |

**Findings:** The largest upstream driver of the 'antagonists and fighting' feature (L4:F8407) is the raw token embedding for the subword 'hat' (the tail of the word 'hating') at position 3, contributing a direct_effect of +10.75. This embedding feeds both the layer‑4 feature directly and also activates two lower‑layer sentiment detectors: L3:F592 (love/hate sentiment) and L3:F8492 (explicit 'hate' word detecto…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` | L3, F8492 → "the word "hate"" |
| 2 | `get_upstream_features` | L3:F592@4, k=5 → Emb:"hat"@3 (de=7.69) +4 more |
| 3 | `get_upstream_features` | L3:F13717@3, k=5 → Emb:"hat"@3 (de=20.00) +4 more |

### Build

`build_circuit` → 20 nodes, 28 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 38,446 | 6,111 | 213,558 | 0 | $0.0317 | — | — |
| SA-2 | openai/gpt-oss-120b | 70,857 | 4,201 | 2,528 | 0 | $0.0132 | ✅ 4F/8E | Trace upstream from the 'antagonists and fighting' feature L… |
| **Total** | | **109,303** | **10,312** | **216,086** | **0** | **$0.0449** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 56s