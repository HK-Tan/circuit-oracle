# Circuit Oracle Report
**Date:** 2026-07-28 07:18:42 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's positive classification is driven by a chain of identity-targeting lexical and hate-related features, not by the prompt's actual toxic content (no slur/insult words are present); the model picks up on co-occurring identity tokens ("Jew", "his", "self-hating", "liberal") via hate-shaped features that are largely triggered by the sub-token "hat" of "hating."

**Confidence:** 7

**Reasoning:**

The circuit begins at token embeddings. The single largest input contribution comes from the sub-token **"hat" at pos 3** (a sub-piece of "hating" / "hate"), with direct_effect ≈ 44 to L0:F2994 (pronoun "his"), ≈ 15 to L1:F2107 ("enter"/legal, frac_nonzero 0.009 — actually a statistical "hat"-notation feature, suppressed by the L0 hat-embedding), ≈ 12 to L3:F8492 ("the word 'hate'", frac_nonzero 0.0005, but here fired because of the "hat" subtoken), and ≈ 10 to L4:F8407 (antagonists/fighting, frac_nonzero 0.009). The **"Self"** token at pos 1 strongly drives L3:F735 (self-hyphenated words, frac 0.006) and L4:F10004 (hyphenated self- words, frac 0.004); these both project hate-themed vocab. The **"his"** token at pos 11 drives L0:F2994 (his/he pronoun detector). The **"-"** tokens at positions 2 and 7 separately drive L0:F8938 (hyphens near numbers) and L0:F3090 (JavaScript member access) — completely incidental features that happen to activate on the punctuation and then suppress the score slightly.

All of this means the "hate" identity-signal the probe is responding to originates almost entirely from the *sub-token "hat"* of the gerund "hating" and the *prefix "Self-"* of the compound word "Self-hating" — not from any actual slur, insult, or hateful content in the prompt. The "Jew" identity token (pos 6) only contributes a small direct effect (≈0.32 to L0:2994) and is not a primary driver; the insult words "stain" and "brethren" contribute negligibly to top features. Late-stage features confirm this is a **spurious identity-group pathway**:
- L3:F592 (love/hate polarity, frac 0.004) promotes `▁hate` and `▁love`,
- L3:F8492 (the word "hate", frac 0.0005) is a narrow lexical hate-detector that fires only because the subtoken "hat" looks like "hate" with `-ing` stripped,
- L4:F8407 (antagonists/fighting, frac 0.009) promotes `▁hated`, `▁Enemy`, `▁villains`, `▁hate`,
- L4:F5181 (political parties/ideologies, frac 0.010) promotes `▁anti`, `Semitism`, `▁hate`, `▁hatred`,
- L4:F10004 (self-hyphenated, frac 0.004) promotes `▁self`/`▁himself`/`▁themselves`,
- L6:F10545 (political rhetoric on race/historical states, frac 0.038) fires on tokens like `▁racist`, `▁slavery`, `▁Nazi`, `▁hysteria`.

These late-layer features (especially L4:F5181 promoting "anti" + "Semitism", and L6:F10545 promoting racist/antisemitic vocabulary) are exactly the kinds of "identity-group + hate shape" detectors the user flagged as spurious: they fire because the prompt *names a religious group* alongside a *hate-flavored token* ("hating", parsed as the "hat" subtoken of "hate"), regardless of the actual semantic content (a condemnation of self-hatred). The model has effectively learned a heuristic: "identity-term + hate-shaped word → toxic," which is exactly the spurious feature the user warned about. Notably, no feature in the circuit detects the actual offensive content of the sentence (the concept of a person being a "stain" on their community), and most signal flows from token-shape features (subtoken "hat", the prefix "self-", punctuation) rather than from any semantic understanding of the insult.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 11 | Layer 0 lexical detectors | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F8938](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8938) | 2 | Layer 0 lexical detectors | hyphens adjacent to numbers | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8938) |
| [L0:F3090](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3090) | 7 | Layer 0 lexical detectors |  JavaScript or other C-style code with member access via "." and "->" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3090) |
| [L0:F4336](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4336) | 3 | Layer 0 lexical detectors |  the word "favor" and words used in legal contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4336) |
| [L1:F2107](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2107) | 3 | Layer 1 spurious/token-form features |  the word "enter", and other words and symbols common to mathematical and legal documents | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2107) |
| [L1:F5138](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5138) | 4 | Layer 1 spurious/token-form features | code referring to bounding boxes | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5138) |
| [L1:F11862](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11862) | 4 | Layer 1 spurious/token-form features | text from academic biological or legal documents that cites names | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11862) |
| [L3:F735](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) | 2 | Layer 3 lexical hate/self- detectors |  words and phrases that include the word "self" followed by a hyphen | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) |
| [L3:F735](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) | 3 | Layer 3 lexical hate/self- detectors |  words and phrases that include the word "self" followed by a hyphen | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) |
| [L3:F735](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) | 4 | Layer 3 lexical hate/self- detectors |  words and phrases that include the word "self" followed by a hyphen | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) |
| [L3:F592](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) | 4 | Layer 3 lexical hate/self- detectors | words related to love, affection, and hate, including foreign language | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) |
| [L3:F8492](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8492) | 4 | Layer 3 lexical hate/self- detectors | the word "hate" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8492) |
| [L3:F9615](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9615) | 3 | Layer 3 lexical hate/self- detectors |  words containing the prefix "self-" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9615) |
| [L3:F9615](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9615) | 4 | Layer 3 lexical hate/self- detectors |  words containing the prefix "self-" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9615) |
| [L3:F13717](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13717) | 3 | Layer 3 lexical hate/self- detectors |  statistical estimation terms, especially those involving "hat" notation | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13717) |
| [L3:F15509](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15509) | 7 | Layer 3 lexical hate/self- detectors |  code diffs like those produced by `git diff` | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15509) |
| [L4:F8407](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) | 3 | Layer 4 hostility / political-identity features |  words related to antagonists and fighting | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) |
| [L4:F8407](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) | 4 | Layer 4 hostility / political-identity features |  words related to antagonists and fighting | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) |
| [L4:F10004](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10004) | 4 | Layer 4 hostility / political-identity features |  hyphenated words beginning with "self" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10004) |
| [L4:F5181](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5181) | 4 | Layer 4 hostility / political-identity features |  terms relating to political parties or ideologies | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5181) |
| [L6:F10545](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10545) | 4 | Layer 6 political-rhetoric feature |  political rhetoric related to race, historical states, and government control | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10545) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:8407 de=0.172 |
| 3 | `inspect_feature` ×6 | L4:8407, L1:2107, L0:2994, L3:9615, L0:8938, L3:735 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F8407@4` | ✅ reported | 5 | 4 | Trace L4:F8407 (antagonists/fighting words) at pos 4 upstream to its source. Wha… |
| SA-2 | `L1:F2107@3` | ✅ reported | 3 | 5 | Trace L1:F2107 at pos 3 upstream. This is labeled "enter" / legal documents. Fin… |
| SA-3 | `L0:F2994@11` | ❌ error | — | — | Trace L0:F2994 (his/he pronoun) at pos 11 upstream to its source. This is a pron… |
| SA-4 | `L3:F735@3` | ❌ error | — | — | Trace L3:F735 (self- prefix) at pos 3 upstream. "Self-hating" is in the prompt a… |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F8407 | " words related to antagonists and fighting" |
| 2 | `get_upstream_features` | L4:F8407@4, k=10 | Emb:"hat"@3 (de=10.75) +9 more |
| 3 | `inspect_feature` | L3, F592 | "words related to love, affection, and hate, including foreign language" |
| 4 | `inspect_feature` | L3, F8492 | "the word "hate"" |
| 5 | `get_upstream_features` | L3:F592@4, k=10 | Emb:"hat"@3 (de=7.69) +9 more |
| 6 | `get_upstream_features` | L3:F8492@4, k=10 | Emb:"hat"@3 (de=12.75) +9 more |
| 7 | `inspect_feature` | L1, F5138 | " code referring to bounding boxes" |
| 8 | `inspect_feature` | L4, F8407 | " words related to antagonists and fighting" |
| 9 | `inspect_feature` | L1, F11862 | "text from academic biological or legal documents that cites names" |
| 10 | `inspect_feature` | L1, F11862 | "text from academic biological or legal documents that cites names" |

**Findings:** L4:F8407 is a high‑level antagonism detector whose strongest driver is the embedding of the token "hat" at the previous position (direct_effect ≈ 10.8). The token "hat" is a sub‑token of the word "hate", so the embedding injects a strong hate‑related signal. This signal is then amplified by two mid‑layer semantic features: L3:F592 (polarity feature that distinguishes love vs. hate) and L3:F8492 (s…

</details>

<details>
<summary><b>SA-2</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F2107 | " the word "enter", and other words and symbols common to mathematical " |
| 2 | `get_upstream_features` | L1:F2107@3, k=10 | Emb:"hat"@3 (de=15.31) +9 more |
| 3 | `inspect_feature` | L0, F1383 | "snippets of code with "%", System.out.println, and other code keywords" |
| 4 | `get_upstream_features` | L0:F1383@3, k=10 | Emb:"hat"@3 (de=9.75) +9 more |
| 5 | `get_upstream_features` | L1:F2107@3, k=20 | Emb:"hat"@3 (de=15.31) +19 more |
| 6 | `inspect_feature` | L0, F10395 | " the word "solar" and related concepts such as farmers" |
| 7 | `get_upstream_features` | L0:F10395@3, k=10 | Emb:"hat"@3 (de=9.19) +9 more |
| 8 | `inspect_feature` | L0, F11188 | "the word "is" or words relating to official authority" |

**Findings:** The L1:F2107 "enter" feature is primarily driven by the input subtoken "hat" at position 3 (direct effect 15.3). Minor positive contributions come from two lower‑layer features (L0:1383 and L0:10395), each of which also receives a strong excitation from the same "hat" embedding. Both lower‑layer features are unrelated to refusal or safety; they are incidental detectors for code snippets and the wo…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F2994@11, k=5 → Emb:" his"@11 (de=44.25) +4 more |
| 2 | `get_upstream_features` | L3:F735@3, k=5 → Emb:"Self"@1 (de=36.50) +4 more |
| 3 | `get_upstream_features` | L3:F735@2, k=5 → Emb:"Self"@1 (de=39.75) +4 more |
| 4 | `get_upstream_features` | L3:F9615@3, k=5 → Emb:"Self"@1 (de=36.00) +4 more |
| 5 | `get_upstream_features` | L4:F8407@4, k=5 → Emb:"hat"@3 (de=10.75) +4 more |
| 6 | `get_upstream_features` | L1:F2107@3, k=5 → Emb:"hat"@3 (de=15.31) +4 more |
| 7 | `get_upstream_features` | L0:F8938@2, k=5 → Emb:"-"@2 (de=34.50) +4 more |
| 8 | `get_upstream_features` | L0:F3090@7, k=5 → Emb:" -"@7 (de=13.69) +4 more |
| 9 | `get_upstream_features` | L0:F4336@3, k=5 → Emb:"hat"@3 (de=12.44) +4 more |
| 10 | `get_upstream_features` | L6:F10545@4, k=5 → L4:F8407 (de=1.62) +4 more |
| 11 | `inspect_feature` ×9 | L3:592, L3:8492, L4:5181, L4:10004, L0:3090, L0:4336, L6:10545, L3:13717, L3:15509 |
| 12 | `get_upstream_features` | L3:F8492@4, k=5 → Emb:"hat"@3 (de=12.75) +4 more |
| 13 | `get_upstream_features` | L4:F10004@4, k=5 → Emb:"Self"@1 (de=34.00) +4 more |

### Build

`build_circuit` → 12 nodes, 15 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 60,083 | 4,752 | 122,609 | 0 | $0.0311 | — | — |
| SA-2 | openai/gpt-oss-120b | 76,979 | 4,189 | 2,528 | 0 | $0.0141 | ✅ 3F/5E | Trace L1:F2107 at pos 3 upstream. This is labeled "enter" / … |
| SA-1 | openai/gpt-oss-120b | 141,957 | 7,347 | 0 | 0 | $0.0257 | ✅ 5F/4E | Trace L4:F8407 (antagonists/fighting words) at pos 4 upstrea… |
| **Total** | | **279,019** | **16,288** | **125,137** | **0** | **$0.0709** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 22s