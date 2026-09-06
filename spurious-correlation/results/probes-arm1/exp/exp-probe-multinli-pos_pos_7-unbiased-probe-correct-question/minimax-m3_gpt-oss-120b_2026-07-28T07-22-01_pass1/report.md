# Circuit Oracle Report
**Date:** 2026-07-28 07:22:01 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_7 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction probe is driven by a circuit that mixes two signal types — a high-frequency generic "topic/structure" stream (sentence-initial "That", the architectural/ordinal content of sentence 1 about the abbey) and a low-frequency "contrast/negation" stream (features for "but", "not forget", disappointment, criticism, comparative statements) that fires almost entirely on sentence 2 — but the contrast stream's signal is not semantically grounded in actual contradiction; it latches onto the very common NLI-bias pattern of (1) starting with a generic descriptive sentence and (2) introducing a second sentence with the word "not"/"but" that often reverses a polarity.

**Confidence:** 7

**Reasoning:**

The circuit is built across 5 supernodes feeding the probe:

1. **Emb → lex_of (L0–L2):** All fifteen token-embedding nodes connect into a "L0 single-word features" supernode. Inspecting these L0 features (3848="of", 3820="the", 7710="you", 9854="will/may/future", 12456="collective/That", 8397="pronoun-start", 12189="moment", 11835="code", 9026="(< technical)", 2159="-led/worthy", 7056="first for the first time", 5053="first", 8046="that/thats", 3833="learn/peek context") reveals the user is partly right: the most positive contributors here are *not* negation signals but generic content-word detectors. In particular **L0:9854 "future/possibility"** fires on "first" (+0.094), **L0:2848 "of"** fires on "of" (+0.153 and +0.111), **L0:3820 "the"** fires on "the" (+0.143), **L0:9026 technical/numbers** fires on "abbey" (+0.124). The user's concern that the model uses "negation words" is *partially* wrong at this layer: the dominant L0/L1 signal is generic vocabulary presence, not negation.

2. **phrase_first (L3–L4):** L4:10564 "ordinal/first + noun/prep" (+0.107 at pos 10's path) and L4:3833 "learn/peek courtroom" (+0.142, +0.127) again are NOT negation features — they are highly polysemous mid-layer features that happen to also fire on "glimpse"/"first" prepositional sequences. The user's intuition that these are spurious is half-correct: they ARE generic-context features, not contradiction-specific.

3. **phrase_steeple (L2–L4):** L4:4605 "churches/églises" (-0.116, -0.103) and L4:5749 "ancient settlements/fortifications" (-0.115, -0.093) — these actually encode the abbey/religious-building concept but push *against* the probe. So content-word features are slightly anti-contradiction, which is consistent with sentence 1 not being a contradiction. **L4:2274 "bad/disappoint opinion"** at pos 24 ("forget") fires on the "you will not forget" segment — a negative-opinion detector that registers on the "wonder" language, contributing to the latent contradiction signal.

4. **phrase_firstof (L5–L6) — the keystone layer:** L6:5342 "first + following prep" (+0.123) is a legitimate phrase detector for "first of", but L6:1912 "criticism/negativity" (+0.14 contribution) and L6:2215 "comparative statements" are the features the user is right to flag. L6:1912 is a famous contrast-bias feature that fires on any "not + memorable verb" / "is not of great X" pattern. Its top activating examples are things like "pulls no punches", "disappoint", "beat" — exactly the lexical environment NLI models learn to associate with contradictions.

5. **late_mid (L8–L11) and late_contrast (L13–L17):** Here the user's concern is fully vindicated. The biggest negative contributor to the probe is **L8:8406** (label: "first-person I / Exactly") at -0.164 — and the inspection of its upstreams shows it fires on sentence-initial "That" (pos 1) because L8:8406 misfires on demonstratives/sentence-initial tokens. Meanwhile the *positive* late-layer contributors are **L13:8128 "sentences beginning with In"** (+0.118), **L14:2510 "using"**, **L16:10989 "the"** (huge activation 125, positive to L17:451), **L17:451 "start of sentences"** (+0.118), and critically **L13:7001 "disappoint/surprise/failure"** (fires on "forget" pos 24, direct_effect on it) and **L16:16037 "but"** (label: "but", activated 13, fires on "and" pos 33 — confusion pattern), **L14:12859 "but/threats/uncertainty"** (fires on "and" pos 33), **L17:14979 "but"** (fires on "and" pos 33). The L13–L17 features are almost all **discourse-marker detectors** ("but", sentence-start, surprise/disappoint) that generic sentence 1 → 2 patterns trigger.

**Verdict on the user's concern:** The user is *partially* correct. At the very lowest layer (L0–L2) the circuit is dominated by genuine content-word features ("of", "the", "you", "moment", "will", "first") with no negation signal. But from L3 upward, especially **L6:1912 "criticism/negativity"**, **L13:7001 "surprise/disappoint/failure"**, **L14:12859 "but/threats"**, **L16:16037 "but"**, and **L17:14979 "but"** form a contrast-bias stream that the contradiction probe latches onto. These features have extremely low frac_nonzero (0.005–0.046) and high specificity for "but" / "disappoint" / "not forget" — they are NOT a faithful semantic encoding of contradiction; they are the NLI-bias shortcut the user suspected. The probe is being driven by (a) genuine lexical-content signal at L0 (mitigating), and (b) a contrast/discourse-marker shortcut at L6–L17 (confirming the user's worry). The circuit is best described as a hybrid where the spurious features dominate the late-layer decision.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: first (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: That (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: of (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: the (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: glimpse (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: towering (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: steep (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: led (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: abbey (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 20 | Emb: moment (pos 20) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: you (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 23 | Emb: not (pos 23) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 24 | Emb: forget (pos 24) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 33 | Emb: and (pos 33) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 30 | Emb: of (pos 10/30) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 4 | L0 single-word features | the word "of" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 30 | L0 single-word features | the word "of" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 5 | L0 single-word features | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F7710](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) | 21 | L0 single-word features | the pronoun "you" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) |
| [L0:F9854](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9854) | 2 | L0 single-word features |  words indicating possibility or future tense verbs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9854) |
| [L0:F12456](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12456) | 1 | L0 single-word features |  the word "collective" and other words with shared meaning, but also finds some words such as "rose" and "that" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12456) |
| [L0:F8397](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8397) | 1 | L0 single-word features |  pronouns at the beginning of sentences or paragraphs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8397) |
| [L0:F12189](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12189) | 20 | L0 single-word features | the word "moment" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12189) |
| [L0:F11835](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11835) | 10 | L0 single-word features | terms used in software code such as "assembly", "using", "namespace", and "license" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11835) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 10 | L0 single-word features | technical documents or data, including numbers, units, and references to figures or tables. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F2159](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2159) | 9 | L0 single-word features |  words that end with "led" or are related to worth | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2159) |
| [L0:F7056](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7056) | 2 | L0 single-word features |  mentions of something happening for the first time | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7056) |
| [L1:F5053](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5053) | 2 | L0 single-word features |  the word "first" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5053) |
| [L2:F8046](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8046) | 1 | L0 single-word features |  common words and phrases that include the letter 't' and are commonly used to start clauses | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8046) |
| [L4:F3833](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) | 3 | L3-L4 ordinal/first + glimpse |  words used when summarizing plot points or providing courtroom insights | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) |
| [L4:F3833](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) | 4 | L3-L4 ordinal/first + glimpse |  words used when summarizing plot points or providing courtroom insights | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) |
| [L4:F10564](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10564) | 4 | L3-L4 ordinal/first + glimpse |  ordinal numbers or the word "first" coupled with a noun or preposition | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10564) |
| [L3:F9772](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9772) | 4 | L3-L4 ordinal/first + glimpse | a phrase combined with a small amount of something and other random words. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9772) |
| [L4:F2581](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2581) | 2 | L3-L4 ordinal/first + glimpse |  mentions of things being "first" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2581) |
| [L3:F11165](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11165) | 2 | L3-L4 ordinal/first + glimpse | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11165) |
| [L4:F4605](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) | 9 | L2-L4 steepled/towering/abbey + criticize |  words related to churches, chapels and other buildings, in addition to other information of Lincolnshire | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) |
| [L4:F4605](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) | 10 | L2-L4 steepled/towering/abbey + criticize |  words related to churches, chapels and other buildings, in addition to other information of Lincolnshire | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) |
| [L4:F5749](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) | 9 | L2-L4 steepled/towering/abbey + criticize |  terms that describe ancient settlements and fortifications | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) |
| [L4:F5749](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) | 10 | L2-L4 steepled/towering/abbey + criticize |  terms that describe ancient settlements and fortifications | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) |
| [L4:F13244](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) | 10 | L2-L4 steepled/towering/abbey + criticize |  terms related to land ownership and administration, possibly including slavery or other forms of forced labor | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) |
| [L3:F4081](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4081) | 9 | L2-L4 steepled/towering/abbey + criticize | mentions of the statistical software Stata and the term "stent". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4081) |
| [L2:F5878](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5878) | 9 | L2-L4 steepled/towering/abbey + criticize | the suffix "le" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5878) |
| [L2:F8185](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8185) | 10 | L2-L4 steepled/towering/abbey + criticize | places for shopping or military activities | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8185) |
| [L2:F12263](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12263) | 10 | L2-L4 steepled/towering/abbey + criticize | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12263) |
| [L4:F9757](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) | 1 | L2-L4 steepled/towering/abbey + criticize | various acronyms, IDs, and symbols, possibly related to scientific data | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) |
| [L4:F2274](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2274) | 24 | L2-L4 steepled/towering/abbey + criticize |  words indicating opinions, particularly negative ones, and also words related to events and technology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2274) |
| [L6:F5342](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5342) | 4 | L5-L6 'first of' / sentence-initial that / contrast | the word "first" as well as words and prepositions that often follow it | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5342) |
| [L6:F5342](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5342) | 3 | L5-L6 'first of' / sentence-initial that / contrast | the word "first" as well as words and prepositions that often follow it | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5342) |
| [L6:F14585](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14585) | 1 | L5-L6 'first of' / sentence-initial that / contrast |  the words "the" and "it" at the beginning of sentences | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14585) |
| [L6:F1610](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1610) | 4 | L5-L6 'first of' / sentence-initial that / contrast |  language related to scientific discovery or invention | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1610) |
| [L6:F1912](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1912) | 24 | L5-L6 'first of' / sentence-initial that / contrast | words related to criticism, negativity and the expression of opinions. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1912) |
| [L6:F2215](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2215) | 24 | L5-L6 'first of' / sentence-initial that / contrast | comparative statements involving amounts or quantities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2215) |
| [L5:F7444](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7444) | 2 | L5-L6 'first of' / sentence-initial that / contrast |  words or phrases that an individual would express or think | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7444) |
| [L8:F8406](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) | 1 | L8-L11 mid-context / sentence-initial that | the first-person pronoun "I" and the word "Exactly" | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) |
| [L9:F8770](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8770) | 1 | L8-L11 mid-context / sentence-initial that | sentences beginning with "It" or "In" and also the word "There". | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8770) |
| [L9:F15819](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15819) | 1 | L8-L11 mid-context / sentence-initial that | code snippets | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15819) |
| [L10:F14174](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14174) | 1 | L8-L11 mid-context / sentence-initial that | left curly brackets | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14174) |
| [L11:F11186](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/11186) | 1 | L8-L11 mid-context / sentence-initial that | scientific and technical terms | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/11186) |
| [L11:F10933](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/10933) | 1 | L8-L11 mid-context / sentence-initial that | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/10933) |
| [L13:F7001](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/7001) | 24 | L13-L17 contrast/but + surprise + sentence-start | words and phrases expressing surprise, knowledge, potential, or failure | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/7001) |
| [L13:F8128](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/8128) | 1 | L13-L17 contrast/but + surprise + sentence-start |  sentences beginning with the word "In" | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/8128) |
| [L14:F12859](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12859) | 33 | L13-L17 contrast/but + surprise + sentence-start |  terms of uncertainty, threats, and medical situations. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12859) |
| [L14:F2510](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/2510) | 1 | L13-L17 contrast/but + surprise + sentence-start | the word "using" | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/2510) |
| [L15:F751](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/751) | 1 | L13-L17 contrast/but + surprise + sentence-start | code snippets | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/751) |
| [L15:F851](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/851) | 1 | L13-L17 contrast/but + surprise + sentence-start | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/851) |
| [L15:F10005](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10005) | 1 | L13-L17 contrast/but + surprise + sentence-start | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10005) |
| [L16:F10989](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/10989) | 1 | L13-L17 contrast/but + surprise + sentence-start | the | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/10989) |
| [L16:F16037](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/16037) | 33 | L13-L17 contrast/but + surprise + sentence-start | but | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/16037) |
| [L17:F451](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) | 1 | L13-L17 contrast/but + surprise + sentence-start | start of sentences | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) |
| [L17:F14979](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/14979) | 33 | L13-L17 contrast/but + surprise + sentence-start | variations of "but" | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/14979) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe (contradiction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L8:8406 de=-0.164 |
| 3 | `inspect_feature` ×17 | L8:8406, L0:2848, L0:3820, L4:3833, L0:9026, L6:5342, L17:451, L0:7710, L0:9854, L0:11835, L4:4605, L4:5749, L4:13244, L4:2581, L4:9757, L2:8046, L5:7444 |
| 4 | `get_upstream_features` | Emb:"<bos>"@0 (de=10.69) +14 more |
| 5 | `get_upstream_features` | Emb:" glimpse"@3 (de=7.03) +14 more |
| 6 | `get_upstream_features` | Emb:" glimpse"@3 (de=13.56) +14 more |
| 7 | `get_upstream_features` | Emb:" first"@2 (de=12.06) +14 more |
| 8 | `get_upstream_features` | L16:F10989 (de=-12.31) +14 more |
| 9 | `get_upstream_features` | Emb:" of"@4 (de=35.25) +14 more |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L17:F451@1` | ❌ error | — | — | Trace the path upstream from L17:F451 at position 1 (start of sentences / senten… |
| SA-2 | `L8:F8406@1` | ❌ error | — | — | Trace the path upstream from L8:F8406 at position 1. The autointerp label says "… |
| SA-3 | `L4:F3833@3` | ❌ error | — | — | Trace L4:F3833 at pos 3 (the word "glimpse"). The autointerp says "words used wh… |
| SA-4 | `L6:F5342@4` | ✅ reported | 4 | 6 | Trace L6:F5342 at pos 4. Autointerp says "the word 'first' as well as words and … |
| SA-5 | `L0:F9854@2` | ❌ error | — | — | Trace L0:F9854 at pos 2. Autointerp says "words indicating possibility or future… |

<details>
<summary><b>SA-4</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F5342 | "the word "first" as well as words and prepositions that often follow i" |
| 2 | `get_upstream_features` | L6:F5342@4, k=10 | Emb:" first"@2 (de=12.06) +9 more |
| 3 | `inspect_feature` | L4, F3833 | " words used when summarizing plot points or providing courtroom insigh" |
| 4 | `inspect_feature` | L4, F10564 | " ordinal numbers or the word "first" coupled with a noun or prepositio" |
| 5 | `inspect_feature` | L4, F2848 | " words related to installation of software, bee keeping, crafting and " |
| 6 | `inspect_feature` | L4, F488 | " information about a player's first appearance or performance in sport" |
| 7 | `get_upstream_features` | L4:F10564@4, k=10 | Emb:" first"@2 (de=11.88) +9 more |
| 8 | `inspect_feature` | L3, F9772 | "a phrase combined with a small amount of something and other random wo" |
| 9 | `get_upstream_features` | L4:F10564@4, k=10 | Emb:" first"@2 (de=11.88) +9 more |

**Findings:** The target feature L6:F5342 is driven primarily by the embedding for the token 'first' (pos2) and reinforced by a chain of upstream features, notably L4:10564 which directly detects ordinal constructions like 'first of', and auxiliary context features L4:3833 and L3:9772. Positive direct_effect edges from these upstream nodes culminate in a strong activation for the phrase 'first of' in the curren…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×10 | L4:10564, L3:9772, L16:10989, L14:2510, L15:751, L10:14174, L13:8128, L9:8770, L6:14585, L11:11186 |
| 2 | `get_top_features` | token="", k=30 → 30 features; top: L8:8406 de=-0.164 |
| 3 | `get_upstream_features` | L0:F7710@21, k=10 → Emb:" you"@21 (de=42.25) +9 more |
| 4 | `get_upstream_features` | L4:F4605@9, k=10 → Emb:"led"@9 (de=6.44) +9 more |
| 5 | `get_upstream_features` | L4:F5749@9, k=10 → L2:F5878 (de=2.50) +9 more |
| 6 | `get_upstream_features` | L4:F2581@2, k=10 → Emb:" first"@2 (de=26.25) +9 more |
| 7 | `get_upstream_features` | L4:F9757@1, k=10 → Emb:"<bos>"@0 (de=15.31) +9 more |
| 8 | `get_upstream_features` | L5:F7444@2, k=10 → Emb:"That"@1 (de=7.34) +9 more |
| 9 | `inspect_feature` ×10 | L3:4081, L2:5878, L2:8185, L6:1610, L0:12456, L0:8397, L9:15819, L13:7001, L17:14979, L0:12189 |
| 10 | `get_upstream_features` | L0:F12456@1, k=8 → Emb:"That"@1 (de=14.06) +7 more |
| 11 | `get_upstream_features` | L2:F8046@1, k=8 → Emb:"That"@1 (de=12.19) +7 more |
| 12 | `get_upstream_features` | L17:F14979@33, k=10 → Emb:"<bos>"@0 (de=-4.94) +9 more |
| 13 | `get_upstream_features` | L0:F3820@5, k=8 → Emb:" the"@5 (de=34.25) +7 more |
| 14 | `get_upstream_features` | L0:F2848@30, k=8 → Emb:" of"@30 (de=37.25) +7 more |
| 15 | `get_upstream_features` | L0:F9026@10, k=8 → Emb:" abbey"@10 (de=37.50) +7 more |
| 16 | `get_upstream_features` | L0:F11835@10, k=8 → Emb:" abbey"@10 (de=7.19) +7 more |
| 17 | `get_upstream_features` | L4:F13244@10, k=8 → Emb:" abbey"@10 (de=9.06) +7 more |
| 18 | `get_upstream_features` | L13:F7001@24, k=8 → Emb:" not"@23 (de=10.44) +7 more |
| 19 | `inspect_feature` ×9 | L6:1912, L3:14777, L4:2274, L6:2215, L16:16037, L14:12859, L1:5053, L0:7056, L0:2159 |

### Build

`build_circuit` → 22 nodes, 26 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 137,809 | 14,663 | 590,795 | 0 | $0.0944 | — | — |
| SA-4 | openai/gpt-oss-120b | 103,269 | 4,278 | 5,152 | 0 | $0.0181 | ✅ 4F/6E | Trace L6:F5342 at pos 4. Autointerp says "the word 'first' a… |
| **Total** | | **241,078** | **18,941** | **595,947** | **0** | **$0.1125** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 41s