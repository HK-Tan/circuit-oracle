# Circuit Oracle Report
**Date:** 2026-07-28 07:12:20 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a mix of spurious surface-level lexical/filler features (e.g., the suffix "t" of "haven't", the interjection "uh", the word "well", "yeah", and a "negation-in-various-languages" feature) rather than by features that encode the actual semantic content of the prompt (NCAA tournament, Louisville, Sweet 16, watching games).

**Confidence:** 8

**Reasoning:**

The attribution graph reveals that the probe's classification is heavily driven by **superficial lexical and pragmatic surface features**, exactly the concern the user raised. The top direct effects on the logit split across the prompt as follows:

- **L0:F6236 (pos 37) "the letter 't' when it follows 'isn'' or 'doesn''"** — direct_effect **+0.5352** at position 37, the "t" in "haven't". This feature's `promoted_tokens` are "not, Not, NOT, nicht, tidak" — it is explicitly a **negation suffix detector**. Its strongest upstream drive comes from the **raw token embedding of "t" at pos 37** (direct_effect 18.25 from the token itself, plus 16.75 from the adjacent "haven" embedding, 11.875 from the apostrophe). This is the single most positive feature in the top 15.

- **L4:F4492 (pos 37) "negations in various languages"** — direct_effect **+0.3105** at position 37. Tracing upstream (via the subagent) confirms this feature aggregates: L0:F6236 (negation "t"), L2:F1337 (negated verbs with pronouns, e.g., "isn't"), L1:F14233 (multilingual negative sentiment "not/no/never"), L2:F6993 (uncertainty phrases), and L3:F15210 ("yet to be" — pending/incomplete). All upstream signals are at pos 37, all converge on the same "haven't" suffix, and none reference any entity (Louisville, NCAA, Sweet 16) or the actual content of the claim.

- **L0:F8352 (pos 2) "the word 'well'"** — direct_effect **−0.5469**. A pure lexical detector of the discourse marker "well", with its dominant upstream being the "well" embedding (direct_effect 30.875).

- **L0:F4541 (pos 1) "adverbs of certainty 'obviously'"** — direct_effect **−0.3164**. Despite firing on "yeah" at pos 1 (embedding drive 12.375), its label is "obviously/certainty". This is a generic pragmatic-feature detector that has latched onto a discourse marker that happens to be at the start.

- **L0:F15972 (pos 1) "the word 'yeah'"** — direct_effect **+0.2891**. Pure lexical detection of "yeah" (embedding drive 26.625). The user concern is directly relevant here: this feature has nothing to do with the logical relationship between the claim and the premise — it just fires because the prompt starts with "yeah".

- **L0:F3820 (pos 3) "the word 'the'"** — direct_effect **+0.4590**. The function-word "the" (embedding drive 32.75). Completely content-free.

- **L0:F16366 (pos 25) "the word 'because'"** — direct_effect **+0.3730**. Lexical detector of "because" (embedding drive 40.75). While "because" is a discourse connective that might be considered semi-semantic, the feature itself is a pure lexical bigram detector, not a causal-reasoning detector.

- **L4:F9602 (pos 4) "interjections and filler words"** — direct_effect **−0.6289** (the **most negative** feature in the top 15). It fires on the "uh" at position 4. The subagent traced its upstream to the raw "uh" embedding (direct_effect 11.44), plus L2:F9629 ("interjections and sounds of hesitation") and L2:F752 ("personal opinion/viewpoint phrases"). The label may not be "negation words" per se, but it is a textbook **pragmatic/register feature** that the model uses to flag the casual conversational tone of the prompt.

- **L1:F177 (pos 6) "the word 'double'"** — direct_effect **−0.3867**. Lexical detector of "double" (in "NC double A" / NCAA, embedding drive 24.0). It is a literal-orthography feature that has nothing to do with the basketball-tournament meaning.

- **L2:F5201 (pos 8) "awards and accomplishments in sports"** — direct_effect **−0.3770**. Fires on "tournament" (embedding drive 16.375). This is the **only** feature that even gestures at prompt content, and its effect is **negative** on the probe (pushing away from the predicted class) — it does not support the classification.

- **L0:F10780 (pos 6) "LaTeX commands"** — direct_effect **+0.3184**. Activates incidentally on the same "double" position — a noise/incidental feature unrelated to any meaning in the prompt.

- **L4:F12126 (pos 2) "expressions of agreement 'well/yeah'"** — direct_effect **−0.4883**, and **L4:F4847 (pos 2) "words in questions/answers"** — direct_effect **+0.3379**. Both fire on "well" and encode conversational-pragmatic register, not semantic content.

- **L1:F13255 (pos 8) "the word 'season'"** — direct_effect **+0.2812** on "tournament". A seasonal-context lexical feature that has no causal relationship to the contradiction task.

**Summary of the mechanism:** The probe is a **surface-form detector** of conversational speech. It activates strongly on the register/style markers of the prompt — filler words ("uh", "well", "yeah"), function words ("the", "because"), and negation suffixes ("haven't" → "t"). The only content-related feature (sports/tournament) appears with a **negative** direct effect, meaning the actual semantic content is *not* what the probe uses to make its classification. The circuit is **not** tracing a "negation = contradiction" shortcut in the strong sense (it is not a single dedicated negation feature that fires the whole prediction), but the user's concern is substantively correct: the probe relies on **shallow, spurious surface features** — discourse markers, filler words, the literal orthography of negation contractions, and function-word detectors — rather than on any entity recognition or entailment-relevant semantic processing of the prompt (no feature for "Louisville", "Sweet 16", "watched", "missed", or "this year" appears in the top direct effects). The model is using "this looks like casual speech containing 'haven't' and 'uh' and 'well'" as its classification signal.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F8352](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) | 2 | Lexical: 'well' detector (L0:F8352) |  the word "well" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) |
| [L0:F15972](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15972) | 1 | Lexical: 'yeah' detector (L0:F15972) | the word "yeah" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15972) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 3 | Lexical: 'the' detector (L0:F3820) | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 37 | Negation suffix 't' detector (L0:F6236, pos 37 'haven\\'t') | the letter "t" when it follows the word "isn'" or "doesn'" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 20 | Negation suffix 't' detector (L0:F6236, pos 20 'haven\\'t') | the letter "t" when it follows the word "isn'" or "doesn'" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L0:F4541](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4541) | 1 | Adverbs of certainty 'obviously' (L0:F4541) |  adverbs of certainty such as "obviously" and related words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4541) |
| [L0:F16366](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) | 25 | Lexical: 'because' detector (L0:F16366) |  the word "because" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) |
| [L1:F177](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) | 6 | Lexical: 'double' detector (L1:F177) |  the word "double" and words that begin with "multi" or "doubly" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) |
| [L0:F7893](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7893) | 6 | Lexical: 'double' detector (L0:F7893) | the word "double" and words related to entrances and entering | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7893) |
| [L1:F13255](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13255) | 8 | Lexical: 'season' detector (L1:F13255) |  the word "season" and words associated with it | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13255) |
| [L0:F10780](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10780) | 6 | LaTeX commands (L0:F10780) - incidental activation at 'double' |  LaTeX commands for including packages and defining document class | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10780) |
| [L2:F5201](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5201) | 8 | Sports awards/championships (L2:F5201) on 'tournament' | awards and accomplishments in the context of sports | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5201) |
| [L2:F9629](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9629) | 4 | Hesitation/filler 'uh' (L2:F9629) |  interjections and sounds of hesitation or acknowledgment | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9629) |
| [L2:F752](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/752) | 4 | Personal opinion phrases (L2:F752) on 'uh' | phrases expressing personal opinions or viewpoints, often using words like "I," "think," "kind of," and related terms. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/752) |
| [L2:F1337](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1337) | 37 | Negated verb constructions (L2:F1337) on 't' pos 37 | negated verbs with personal pronouns, and foreign language pronouns | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1337) |
| [L1:F14233](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) | 37 | Multilingual negative sentiment 'not/no/never' (L1:F14233) | negative sentiment markers such as "not," "no," "never," and their equivalents in other languages | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) |
| [L2:F6993](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6993) | 37 | Uncertainty phrases (L2:F6993) on 't' pos 37 | phrases describing uncertainty or difficulty | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6993) |
| [L4:F9602](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9602) | 4 | Interjections/filler words (L4:F9602) on 'uh' |  interjections and filler words | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9602) |
| [L4:F12126](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) | 2 | Expressions of agreement 'well/yeah' (L4:F12126) on 'well' |  expressions of agreement or acknowledgement, particularly "well" and "yeah" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) |
| [L4:F4847](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) | 2 | Words in questions/answers (L4:F4847) on 'well' |  words or short phrases often used in conversation, and especially questions and answers | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 37 | Negations in various languages (L4:F4492) on 't' pos 37 | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:9602 de=-0.629 |
| 3 | `inspect_feature` ×13 | L4:9602, L0:8352, L0:6236, L0:3820, L0:16366, L0:10780, L4:4492, L0:4541, L4:12126, L4:4847, L1:177, L2:5201, L0:7893 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F4492@37` | ✅ reported | 7 | 21 | Trace upstream from L4:F4492 which is labeled "negations in various languages". … |
| SA-2 | `L0:F6236@37` | ❌ error | — | — | Trace upstream from L0:F6236 (label: "the letter 't' when it follows the word 'i… |
| SA-3 | `L4:F9602@4` | ✅ reported | 8 | 9 | Trace upstream from L4:F9602 (label: "interjections and filler words") at positi… |

<details>
<summary><b>SA-1</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F4492 | "negations in various languages" |
| 2 | `get_upstream_features` | L4:F4492@37, k=15 | Emb:"t"@37 (de=6.53) +14 more |
| 3 | `inspect_feature` | L0, F6236 | "the letter "t" when it follows the word "isn'" or "doesn'"" |
| 4 | `inspect_feature` | L2, F1337 | "negated verbs with personal pronouns, and foreign language pronouns" |
| 5 | `get_upstream_features` | L0:F6236@37, k=10 | Emb:"t"@37 (de=18.25) +9 more |
| 6 | `inspect_feature` | L2, F6993 | "phrases describing uncertainty or difficulty" |
| 7 | `get_upstream_features` | L2:F1337@37, k=10 | Emb:" haven"@35 (de=28.75) +9 more |
| 8 | `inspect_feature` | L3, F15210 | " the phrase "yet to be" (or variations with similar words) indicating " |
| 9 | `inspect_feature` | L3, F6227 | " sentence fragments and informal or ungrammatical language, often incl" |
| 10 | `inspect_feature` | L0, F1977 | " the letter "t", sometimes preceded by "m" or "usually"" |
| 11 | `inspect_feature` | L0, F1978 | " contractions ending in 't' or the word 'know'" |
| 12 | `get_upstream_features` | L2:F6993@37, k=10 | Emb:" I"@34 (de=3.02) +9 more |
| 13 | `inspect_feature` | L1, F14233 | " negative sentiment markers such as "not," "no," "never," and their eq" |

**Findings:** Feature L4:F4492 aggregates the trailing "t" of English negated contractions and, via upstream detectors (L0:F6236, L2:F1337, etc.), captures broader negation patterns across languages. The primary input token is the embedding for "t" at position 37 (direct_effect = 6.53), coming from the word "isn't"/"doesn't". Upstream features include a low‑frequency "t" detector (L0:F6236), a multi‑language ne…

</details>

<details>
<summary><b>SA-3</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F9602 | " interjections and filler words" |
| 2 | `get_upstream_features` | L4:F9602@4, k=15 | Emb:" uh"@4 (de=11.44) +14 more |
| 3 | `inspect_feature` | L2, F9629 | " interjections and sounds of hesitation or acknowledgment" |
| 4 | `get_upstream_features` | L2:F9629@4, k=15 | Emb:" uh"@4 (de=15.12) +14 more |
| 5 | `get_upstream_features` | L2:F9629@4, k=15 | Emb:" uh"@4 (de=15.12) +14 more |
| 6 | `inspect_feature` | L2, F752 | "phrases expressing personal opinions or viewpoints, often using words " |
| 7 | `inspect_feature` | L1, F2623 | " words in the context of someone talking or expressing opinions." |
| 8 | `inspect_feature` | L3, F7140 | "words or parts of words containing "man", "ent", "per", or "mate"" |
| 9 | `get_upstream_features` | L1:F2623@4, k=15 | Emb:" uh"@4 (de=12.31) +14 more |
| 10 | `inspect_feature` | L1, F11932 | " strings of repeated characters, which could be either excitement or c" |
| 11 | `inspect_feature` | L3, F16039 | " section delimiters and incomplete quotes" |
| 12 | `inspect_feature` | L2, F859 | " words that appear frequently in informal conversation" |
| 13 | `get_upstream_features` | L2:F752@4, k=15 | Emb:" uh"@4 (de=10.38) +14 more |
| 14 | `get_upstream_features` | L3:F7140@4, k=15 | Emb:" uh"@4 (de=10.69) +14 more |
| 15 | `get_upstream_features` | L3:F7140@4, k=15 | Emb:" uh"@4 (de=10.69) +14 more |

**Findings:** Tracing from the filler‑word feature L4:F9602 ("the") reveals a strong upstream drive from the raw token embedding "uh" (positive direct_effect >11). This embedding feeds into several low‑layer (≤3) features that specialize in hesitation sounds (L2:F9629), informal conversation cues (L2:F859), and generic spoken‑context markers (L1:F2623). All paths pass through layers ≤8 and include a positive em…

</details>

### Re-dispatch (round 2): 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-4 | `L0:F6236@20` | ❌ error | — | — | Trace upstream from L0:F6236 (label: "the letter 't' when it follows the word 'i… |
| SA-5 | `L0:F16366@25` | ❌ error | — | — | Trace upstream from L0:F16366 (label: "the word 'because'") at position 25, dire… |
| SA-6 | `L0:F4541@1` | ❌ error | — | — | Trace upstream from L0:F4541 (label: "adverbs of certainty such as 'obviously'")… |
| SA-7 | `L2:F5201@8` | ✅ reported | 6 | 11 | Trace upstream from L2:F5201 (label: "awards and accomplishments in the context … |
| SA-8 | `L0:F8352@2` | ❌ error | — | — | Trace upstream from L0:F8352 (label: "the word 'well'") at position 2, direct_ef… |

<details>
<summary><b>SA-7</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F5201 | "awards and accomplishments in the context of sports" |
| 2 | `get_upstream_features` | L2:F5201@8, k=10 | Emb:" tournament"@8 (de=16.38) +9 more |
| 3 | `inspect_feature` | L1, F11938 | "mentions of meals, restaurants, and food" |
| 4 | `get_upstream_features` | L1:F11938@8, k=10 | Emb:" tournament"@8 (de=13.00) +9 more |
| 5 | `inspect_feature` | L0, F15183 | " the word "fighting"" |
| 6 | `inspect_feature` | L0, F8659 | "the word "foundation" in different contexts, including religious, lega" |
| 7 | `get_upstream_features` | L0:F8659@8, k=10 | Emb:" tournament"@8 (de=15.25) +9 more |
| 8 | `inspect_feature` | L0, F12164 | " words related to the legal system" |
| 9 | `get_upstream_features` | L0:F15183@8, k=10 | Emb:" tournament"@8 (de=19.38) +9 more |
| 10 | `inspect_feature` | L0, F10442 | " words associated with medical emergencies or urgent situations" |

**Findings:** The target L2 feature (sports awards) receives its strongest excitatory drive from the raw token embedding of "tournament" (pos 8), which directly boosts the feature by a large margin. The signal propagates upward through a shallow hierarchy: the embedding feeds a layer‑1 food‑mention feature (F11938) that in turn modestly excites the sports‑award detector, and also reaches several layer‑0 lexical…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_features` | token="", k=20 → 20 features; top: L4:9602 de=-0.629 |
| 2 | `get_upstream_features` | L0:F8352@2, k=10 → Emb:" well"@2 (de=30.88) +9 more |
| 3 | `get_upstream_features` | L0:F16366@25, k=10 → Emb:" because"@25 (de=40.75) +9 more |
| 4 | `get_upstream_features` | L0:F4541@1, k=10 → Emb:"yeah"@1 (de=12.38) +9 more |
| 5 | `get_upstream_features` | L0:F6236@20, k=10 → Emb:"t"@20 (de=17.88) +9 more |
| 6 | `inspect_feature` ×6 | L0:15972, L1:13255, L5:2740, L2:752, L1:6846, L2:9629 |
| 7 | `get_upstream_features` | L4:F4492@37, k=10 → Emb:"t"@37 (de=6.53) +9 more |
| 8 | `get_upstream_features` | L0:F6236@37, k=10 → Emb:"t"@37 (de=18.25) +9 more |
| 9 | `get_upstream_features` | L4:F9602@4, k=10 → Emb:" uh"@4 (de=11.44) +9 more |
| 10 | `get_upstream_features` | L2:F5201@8, k=10 → Emb:" tournament"@8 (de=16.38) +9 more |
| 11 | `get_upstream_features` | L0:F3820@3, k=10 → Emb:" the"@3 (de=32.75) +9 more |
| 12 | `get_upstream_features` | L0:F15972@1, k=10 → Emb:"yeah"@1 (de=26.62) +9 more |
| 13 | `get_upstream_features` | L1:F177@6, k=10 → Emb:" double"@6 (de=24.00) +9 more |
| 14 | `get_upstream_features` | L0:F10780@6, k=10 → Emb:" double"@6 (de=15.62) +9 more |
| 15 | `get_upstream_features` | L4:F12126@2, k=10 → Emb:" well"@2 (de=14.62) +9 more |
| 16 | `get_upstream_features` | L4:F4847@2, k=10 → Emb:" well"@2 (de=8.06) +9 more |
| 17 | `get_upstream_features` | L1:F13255@8, k=10 → Emb:" tournament"@8 (de=18.50) +9 more |
| 18 | `get_upstream_features` | L0:F7893@6, k=10 → Emb:" double"@6 (de=18.62) +9 more |

### Build

`build_circuit` → 31 nodes, 47 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 65,697 | 8,589 | 309,446 | 0 | $0.0486 | — | — |
| SA-1 | openai/gpt-oss-120b | 226,760 | 17,276 | 19,296 | 0 | $0.0447 | ✅ 7F/21E | Trace upstream from L4:F4492 which is labeled "negations in … |
| SA-3 | openai/gpt-oss-120b | 177,822 | 13,201 | 66,720 | 0 | $0.0356 | ✅ 8F/9E | Trace upstream from L4:F9602 (label: "interjections and fill… |
| SA-7 | openai/gpt-oss-120b | 106,315 | 8,165 | 10,240 | 0 | $0.0210 | ✅ 6F/11E | Trace upstream from L2:F5201 (label: "awards and accomplishm… |
| **Total** | | **576,594** | **47,231** | **405,702** | **0** | **$0.1498** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 8m 11s