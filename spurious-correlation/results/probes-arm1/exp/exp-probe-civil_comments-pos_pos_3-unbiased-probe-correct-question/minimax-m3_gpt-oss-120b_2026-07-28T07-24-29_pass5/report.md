# Circuit Oracle Report
**Date:** 2026-07-28 07:24:29 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a chain of early-to-mid-layer lexical features that key on the words "self-", "hat-", "ing", "Jew" and the hyphenated "self-hating" compound, then activate mid-layer features for "hate", "self", and political identity-group rhetoric that push the probe output — meaning the classification is being driven substantially by content-word identity and slur-adjacent lexical features rather than truly abstract toxicity semantics.

**Confidence:** 7

**Reasoning:**

The top features driving the probe (highest direct_effect to the output) are predominantly **lexical and content-word detectors**, not abstract toxicity features. The top three are: L4:F8407 ("words related to antagonists and fighting", frac_nonzero=0.00874, direct_effect=0.1719), L1:F2107 ("enter / mathematical-legal documents", frac_nonzero=0.00897, direct_effect=0.1631), and L0:F2994 (pronoun "his", direct_effect=0.1455). Other large positive contributors are L0:F8938 (hyphens adjacent to numbers, direct_effect=0.1387), L3:F735 ("self- followed by hyphen" with toxic-context examples, direct_effect=0.1377), and L0:F3090 (C-style code with member access).

Tracing upstream from L4:F8407 ("antagonists and fighting") at the "hating" position (pos 4) reveals that the largest single direct_effect (10.75) comes from the **embedding of the "hat" subword token at pos 3** — i.e. the "hat-" part of "hating" literally acts as a strong feed-in. The next-biggest upstream contributor is L3:F592 ("words related to love, affection, and hate" — promotes "hate", frac_nonzero=0.0044, direct_effect=3.625), which itself reads from the "hat" subword embedding. L3:F8492 ("the word 'hate'", frac_nonzero=0.00054, direct_effect=1.61) is an even more specific "hate"-word detector that again keys off the "hat" subword.

The L0:L1 supernode (`early_lexical`) and L2–L3 supernode (`self_hyphen_compound`) show that the model is primarily reading off **subword string features**: "Self" embedding, hyphen, "hat" subword, "ing" subword, with a compound "self-hyphen" feature (L3:F735, frac_nonzero=0.00632) and "self-" prefix feature (L3:F9615, frac_nonzero=0.00549; L3:F10004 "hyphenated words beginning with self", frac_nonzero=0.00397) doing real work. These features are **content-agnostic, identity-agnostic lexical detectors** — they fire on "self-hating" regardless of who is being hated.

Critically, the **identity / "group" signal is mostly entering through the embedding of "Jew" at pos 6** and reaching a single L6:L7 supernode (`political_rhetoric`): L6:F10545 ("political rhetoric related to race, historical states, and government control", frac_nonzero=0.03818, direct_effect=0.0864, with top activations like "▁Nazi", "▁slavery", "▁racist", "▁hysteria") and L7:F11220 ("biblical names… Rabbis", frac_nonzero=0.00571, with the top activating example being Satmar Rabbi content) which **inhibits** the probe (direct_effect=-0.0796). So the "Jewish identity" content enters mostly as a single near-final feature that *reduces* the probe score (counter-direction), not as the dominant driver.

L4:F11580 ("negative language and swear words", frac_nonzero=0.00341, promotes "FUCK", "▁idiot", "▁moron") does contribute positively (direct_effect=0.0747), and L4:F5181 ("political parties or ideologies", frac_nonzero=0.00962, promotes "▁hate", "Semitism") contributes positively at pos 4 (direct_effect=0.139 if combined with its upstream contribution at pos 3). But the top-3 features by direct_effect to the probe are the "antagonists/fighting" word detector, the subword "hat" embedding path, and the pronoun "his" detector — not abstract-toxicity features.

**So the user is essentially correct**, but with a refinement: the circuit is not exclusively using "identity group" signals. It is using a **mix of (a) the literal "hate" / "hat" subword and the "self-hating" compound as lexical triggers**, plus (b) a single identity-related feature (L6:F10545 "race/holocaust/political rhetoric") and (c) a swear-word feature (L4:F11580). The "identity group" signal is a real contributor via L6:F10545 and L7:F11220, but it is **one of several lexical triggers** rather than the sole driver. The dominant drivers are content-word lexical features (the words "hat", "self-", "hate", and pronoun "his") rather than a learned abstract "this is toxic" representation. The probe is therefore partially a **spurious lexical-feature detector** that reads "self-hating" + identity content + hate-vocabulary as a toxicity signal — i.e. exactly the kind of shortcut the user suspected, with the "identity group" signal coming in late (L6:L7) but the **lexical-confound** signal ("hate"/"hat"/"self-") dominating throughout L0–L4.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Self (pos 1) — capitalized "Self" token | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: - (pos 2) — hyphen token | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: hat (pos 3) — "hat" subword of "hating" | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: ing (pos 4) — "ing" subword of "hating" | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: liberal (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: Jew (pos 6) — identity/religious group token | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 11 | Emb: his (pos 11) — pronoun | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 11 | Early lexical detectors (L0–L1) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F8938](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8938) | 2 | Early lexical detectors (L0–L1) | hyphens adjacent to numbers | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8938) |
| [L0:F15366](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15366) | 3 | Early lexical detectors (L0–L1) |  references to females and past tense verbs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15366) |
| [L0:F1094](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1094) | 3 | Early lexical detectors (L0–L1) |  words and suffixes related to states and senses | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1094) |
| [L0:F4336](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4336) | 3 | Early lexical detectors (L0–L1) |  the word "favor" and words used in legal contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4336) |
| [L1:F2107](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2107) | 3 | Early lexical detectors (L0–L1) |  the word "enter", and other words and symbols common to mathematical and legal documents | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2107) |
| [L1:F5138](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5138) | 4 | Early lexical detectors (L0–L1) |  code referring to bounding boxes | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5138) |
| [L2:F3983](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3983) | 3 | Self-hyphen compound detectors (L2–L3) | the word "hat" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3983) |
| [L2:F16224](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16224) | 3 | Self-hyphen compound detectors (L2–L3) |  words and phrases related to self-awareness, self-reference, or self-publishing | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16224) |
| [L2:F16224](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16224) | 4 | Self-hyphen compound detectors (L2–L3) |  words and phrases related to self-awareness, self-reference, or self-publishing | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16224) |
| [L3:F735](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) | 3 | Self-hyphen compound detectors (L2–L3) |  words and phrases that include the word "self" followed by a hyphen | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) |
| [L3:F735](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) | 2 | Self-hyphen compound detectors (L2–L3) |  words and phrases that include the word "self" followed by a hyphen | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) |
| [L3:F735](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) | 4 | Self-hyphen compound detectors (L2–L3) |  words and phrases that include the word "self" followed by a hyphen | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) |
| [L3:F9615](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9615) | 3 | Self-hyphen compound detectors (L2–L3) |  words containing the prefix "self-" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9615) |
| [L3:F9615](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9615) | 4 | Self-hyphen compound detectors (L2–L3) |  words containing the prefix "self-" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9615) |
| [L3:F10004](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10004) | 4 | Self-hyphen compound detectors (L2–L3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10004) |
| [L3:F13717](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13717) | 3 | Self-hyphen compound detectors (L2–L3) |  statistical estimation terms, especially those involving "hat" notation | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13717) |
| [L3:F13717](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13717) | 4 | Self-hyphen compound detectors (L2–L3) |  statistical estimation terms, especially those involving "hat" notation | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13717) |
| [L3:F8675](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8675) | 3 | Self-hyphen compound detectors (L2–L3) | mostly finds articles like a, an, the etc., as well as words like "own" and "abuse". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8675) |
| [L3:F696](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/696) | 4 | Self-hyphen compound detectors (L2–L3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/696) |
| [L3:F592](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) | 3 | Hate / love / antagonism complex (L3) | words related to love, affection, and hate, including foreign language | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) |
| [L3:F592](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) | 4 | Hate / love / antagonism complex (L3) | words related to love, affection, and hate, including foreign language | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) |
| [L3:F8492](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8492) | 3 | Hate / love / antagonism complex (L3) | the word "hate" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8492) |
| [L3:F8492](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8492) | 4 | Hate / love / antagonism complex (L3) | the word "hate" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8492) |
| [L3:F13302](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13302) | 3 | Hate / love / antagonism complex (L3) |  words related to negative opinions, harm, and warnings | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13302) |
| [L3:F13302](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13302) | 4 | Hate / love / antagonism complex (L3) |  words related to negative opinions, harm, and warnings | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13302) |
| [L3:F15509](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15509) | 7 | Hate / love / antagonism complex (L3) |  code diffs like those produced by `git diff` | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15509) |
| [L3:F5808](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5808) | 4 | Hate / love / antagonism complex (L3) | words ending in "-ing" that have a sense of driving something forward | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5808) |
| [L3:F14455](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14455) | 4 | Hate / love / antagonism complex (L3) |  words related to government, law, business, and public policy | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14455) |
| [L3:F12592](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12592) | 4 | Hate / love / antagonism complex (L3) |  language used to criticize or belittle someone | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12592) |
| [L3:F13070](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13070) | 4 | Hate / love / antagonism complex (L3) |  words related to automation | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13070) |
| [L3:F15447](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15447) | 3 | Hate / love / antagonism complex (L3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15447) |
| [L4:F8407](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) | 3 | Late lexical/compound features (L4) |  words related to antagonists and fighting | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) |
| [L4:F8407](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) | 4 | Late lexical/compound features (L4) |  words related to antagonists and fighting | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) |
| [L4:F11580](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11580) | 3 | Late lexical/compound features (L4) | negative language and swear words | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11580) |
| [L4:F5181](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5181) | 4 | Late lexical/compound features (L4) |  terms relating to political parties or ideologies | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5181) |
| [L4:F14198](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14198) | 4 | Late lexical/compound features (L4) |  terms found in legal or political discourse, especially where rights are being violated or impinged. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14198) |
| [L2:F1319](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1319) | 4 | Late lexical/compound features (L4) | words ending in "ing," regardless of their part of speech, but with a preference for present participles | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1319) |
| [L2:F7846](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7846) | 4 | Late lexical/compound features (L4) |  adjectives and adverbs ending in "ed", "ing", "al", "ent", "ive", "able", "ile", "dependent" or "specific" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7846) |
| [L2:F9871](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9871) | 7 | Late lexical/compound features (L4) | latex and code snippets and mathematical symbols | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9871) |
| [L2:F10471](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10471) | 7 | Late lexical/compound features (L4) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10471) |
| [L6:F10545](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10545) | 4 | Political-rhetoric / identity content (L6–L7) |  political rhetoric related to race, historical states, and government control | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10545) |
| [L7:F11220](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/11220) | 6 | Political-rhetoric / identity content (L6–L7) | biblical names and related words, especially Rabbis with specific suffixes like "baum" and "as". | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/11220) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe direction (output) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'probe' is not one of the top-k next-token candidates  |
| 3 | `get_top_features` | 20 features; top: L4:8407 de=0.172 |
| 4 | `inspect_feature` ×5 | L4:8407, L1:2107, L0:2994, L0:8938, L3:735 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F8407@4` | ❌ error | — | — | Trace the path upstream from L4:F8407 at pos 4 ("stain"). This feature is labele… |
| SA-2 | `L0:F2994@11` | ❌ error | — | — | Trace the path upstream from L0:F2994 at pos 11 (likely "his"). This feature det… |
| SA-3 | `L3:F735@3` | ❌ error | — | — | Trace the path upstream from L3:F735 at pos 3 — this is the "self-hyphen" featur… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×2 | L0:3090, L0:4336 |
| 2 | `get_upstream_features` | L4:F8407@4, k=10 → Emb:"hat"@3 (de=10.75) +9 more |
| 3 | `get_upstream_features` | L3:F735@3, k=10 → Emb:"Self"@1 (de=36.50) +9 more |
| 4 | `get_upstream_features` | L0:F2994@11, k=8 → Emb:" his"@11 (de=44.25) +7 more |
| 5 | `get_upstream_features` | L1:F2107@3, k=8 → Emb:"hat"@3 (de=15.31) +7 more |
| 6 | `inspect_feature` ×6 | L3:592, L3:8492, L1:5138, L0:1094, L3:9615, L0:8938 |
| 7 | `get_upstream_features` | L4:F8407@3, k=12 → Emb:"hat"@3 (de=7.41) +11 more |
| 8 | `inspect_feature` ×3 | L3:13302, L2:1319, L2:7846 |
| 9 | `get_upstream_features` | L6:F10545@4, k=8 → L4:F8407 (de=1.62) +7 more |
| 10 | `inspect_feature` ×5 | L6:10545, L4:11580, L4:5181, L4:10004, L3:13717 |
| 11 | `get_upstream_features` | L6:F10545@4, k=12 → L4:F8407 (de=1.62) +11 more |
| 12 | `get_upstream_features` | L6:F10545@4, k=15 → L4:F8407 (de=1.62) +14 more |
| 13 | `inspect_feature` ×3 | L4:14198, L3:8675, L0:15366 |
| 14 | `get_upstream_features` | L4:F5181@4, k=10 → Emb:"hat"@3 (de=2.92) +9 more |
| 15 | `get_upstream_features` | L4:F10004@4, k=10 → Emb:"Self"@1 (de=34.00) +9 more |
| 16 | `inspect_feature` ×6 | L3:5808, L3:14455, L3:13070, L3:12592, L2:16224, L2:3983 |
| 17 | `get_upstream_features` | L4:F8407@6, k=10 → ❌ Feature (layer=4, feature_idx=8407) not found at pos=6. This |
| 18 | `get_upstream_features` | L4:F8407@11, k=8 → ❌ Feature (layer=4, feature_idx=8407) not found at pos=11. Thi |
| 19 | `inspect_feature` ×4 | L7:11220, L3:15509, L3:10471, L2:9871 |

### Build

`build_circuit` → 13 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 51,410 | 7,092 | 488,444 | 0 | $0.0532 | — | — |
| **Total** | | **51,410** | **7,092** | **488,444** | **0** | **$0.0532** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 38s