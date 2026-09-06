# Circuit Oracle Report
**Date:** 2026-07-28 07:19:54 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_10 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity score is driven almost entirely by shallow, content-independent word-form detectors (literal "not", "race", "mention/mentioning", "By", "question", "the") anchored on the surface tokens "not", "race", "mentioning" and "By" — none of the features encode the actual toxic content (police brutality, racial stereotyping of cops); the classification rides on lexical triggers.

**Confidence:** 6

**Reasoning:** The output is a toxicity probe driven by a flat fan-in of low-level lexical features. There are no late-layer (L15+) semantic features in the top set; the deepest feature is **L4:F15173** (statements about *mentioning/discussing* something, frac_nonzero=0.043) with direct_effect +0.135, fed by the ` mentioning` token embedding (pos 3, de=17.5) and a lower-layer **L3:F6517** "mention" word stem detector (frac_nonzero=0.0056). All other top-20 features are layer-0 through layer-3 word-form detectors:

- **L2:F10509** ("the word race", de=-0.181) and **L0:F10682** ("race", de=+0.146) and **L3:F5475** ("race", de=-0.101) — all verified to be GENERIC lexical detectors: their top activating examples are cycling races, F1 Grand Prix, Irish stage races, race-car drivers (Helio Castroneves, IndyCar), not racial/ethnic identity. They are driven by the ` race` token embedding at pos 5.
- **L0:F4958** ("not", de=-0.227) and **L2:F2713** ("not", de=+0.084) — generic negation cue detectors (frac_nonzero 0.018 and 0.0033), top activations are arbitrary "not" usage in legal, scientific, product, news text.
- **L2:F11639** ("mention", de=+0.112) and **L2:F6539** ("mention / matter / mind", de=+0.100) and **L3:F11194** ("stating/communicating", de=+0.092) — all word-form detectors for the ` mentioning` token (pos 3) with no racial/social semantics; top examples are math papers saying "we mention that…", legal briefs, product reviews.
- **L3:F12410** ("By at start of sentence", de=+0.129) and **L0:F2455** ("the word case", de=-0.110) — purely positional/syntactic, top activations are auction catalogs, math corollaries, court orders, "By using the calculated phonon spectrum…"
- **L3:F672** ("question", de=+0.105) and **L0:F819** (negative), **L0:F2317** (negative) — word-form detectors on "question", "all", etc.
- **L4:F2668** ("realizations / acknowledgement of something", de=+0.099) — fires on "realize", "overlooked", "aware", "knowing" in completely generic contexts (UI screenshots, cataract surgery, book reviews, Indian stereotypes resource list).

Crucially, *no feature in the circuit encodes the actual toxic semantic content* — there is no "police", "brutality", "cops", "Black people", "stereotype", or "white/black" identity feature. The four "race" detectors (L0:F10682, L2:F10509, L3:F5475) are confirmed to fire primarily on race-cars and competitive racing contexts; the same is true of "mention" features (scientific writing, product reviews, legal briefs). Token-level influence is dominated by **emb_not** (pos 2), **emb_mentioning** (pos 3), **emb_race** (pos 5), and **emb_by** (pos 1) — all shallow word-form signals. The signal flow is therefore: token embeddings → shallow word-form detectors → probe logit, with no semantic integration of who is doing what to whom. This matches the user's concern: the probe uses spurious surface cues (the words "not", "race", "mention", and sentence-initial "By") as a lexical shortcut, not the prompt's actual content about racial stereotyping of police violence.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: ' race' (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'By' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: ' not' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: ' mentioning' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 2 | L0: Generic negation cue ('not') |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F10682](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10682) | 5 | L0: Lexical 'race' detector (generic, also fires on race-cars) |  the word "race" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10682) |
| [L0:F2455](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2455) | 1 | L0: Sentence-start 'By/case' token detector | the word "case", sometimes in relation to a preposition | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2455) |
| [L2:F11639](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11639) | 3 | L2: Generic 'mention' word-form detector | the word "mention" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11639) |
| [L2:F2713](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2713) | 2 | L2: Secondary 'not' detector |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2713) |
| [L2:F10509](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10509) | 5 | L2: Generic 'race' word-form detector (also fires on race-cars / cycling) |  the word "race." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10509) |
| [L2:F6539](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6539) | 3 | L2: 'mention' / matter-related discussion detector | the word "mention" and words or phrases related to opinions or significance, as well as the word "matter." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6539) |
| [L3:F12410](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12410) | 1 | L3: 'By' at sentence start (syntactic position) | the word "By" at the start of a phrase or sentence | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12410) |
| [L3:F672](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/672) | 10 | L3: 'question' word-form detector |  the word "question" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/672) |
| [L3:F11194](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11194) | 3 | L3: Words related to stating/communicating information |  words related to stating or communicating information | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11194) |
| [L3:F5475](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5475) | 5 | L3: 'race' word-form detector (race-cars, race-relations) |  occurrences of the word "race" in different contexts | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5475) |
| [L4:F15173](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15173) | 3 | L4: Statements about mentioning/discussing something |  statements about mentioning or discussing something | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15173) |
| [L4:F2668](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2668) | 3 | L4: Realizations / acknowledgement of something |  instances of realizations coupled with acknowledgement or acknowledgment of something. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2668) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:4958 de=-0.227 |
| 3 | `inspect_feature` ×6 | L0:4958, L2:10509, L0:10682, L4:15173, L3:12410, L2:11639 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F15173@3` | ✅ reported | 3 | 7 | Trace L4:F15173 (statements about mentioning/discussing something) upstream. Wha… |
| SA-2 | `L2:F10509@5` | ❌ error | — | — | Trace L2:F10509 (the word "race") upstream. Is this a generic "race" detector or… |
| SA-3 | `L3:F12410@1` | ✅ reported | 3 | 6 | Trace L3:F12410 ("By" at start of sentence) upstream. This is a generic syntacti… |
| SA-4 | `L2:F11639@3` | ✅ reported | 3 | 4 | Trace L2:F11639 ("mention" word) upstream. Verify it's a generic "mention" detec… |
| SA-5 | `L2:F10509@5` | ❌ error | — | — | Trace L2:F10509 (the word "race") upstream to find its drivers and the embedding… |

<details>
<summary><b>SA-1</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F15173 | " statements about mentioning or discussing something" |
| 2 | `get_upstream_features` | L4:F15173@3, k=10 | Emb:" mentioning"@3 (de=17.50) +9 more |
| 3 | `inspect_feature` | L3, F6517 | " words related to mentioning something" |
| 4 | `get_upstream_features` | L3:F6517@3, k=10 | Emb:" mentioning"@3 (de=23.12) +9 more |
| 5 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |

**Findings:** The target feature L4:F15173 is primarily a generic mention detector. Its strongest upstream driver is the token embedding for the word "mentioning" (pos 3), providing a large positive direct effect (17.5). A lower‑layer lexical feature (L3:F6517) also detects the word stem "mention" and itself is driven by the same embedding. Minor positive contributions come from the surrounding tokens "not" and…

</details>

<details>
<summary><b>SA-3</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F12410 | "the word "By" at the start of a phrase or sentence" |
| 2 | `get_upstream_features` | L3:F12410@1, k=10 | Emb:"By"@1 (de=48.75) +9 more |
| 3 | `inspect_feature` | L2, F6621 | " the word "by"" |
| 4 | `inspect_feature` | L0, F12698 | "question-answer pairs (or just questions) and import statements" |
| 5 | `inspect_feature` | L0, F10278 | "code referring to "entry" in a hash table context" |
| 6 | `get_upstream_features` | L2:F6621@1, k=10 | Emb:"By"@1 (de=14.94) +9 more |
| 7 | `inspect_feature` | L0, F2455 | "the word "case", sometimes in relation to a preposition" |
| 8 | `get_upstream_features` | L0:F12698@1, k=10 | Emb:"<bos>"@0 (de=14.56) +9 more |
| 9 | `get_upstream_features` | L0:F2455@1, k=10 | Emb:"<bos>"@0 (de=13.31) +9 more |

**Findings:** The target feature L3:F12410 is a sentence-start detector for the token "By". Its strongest upstream driver is the raw embedding of the token "By" (pos 1) with a direct effect of 48.75, confirming that it directly reads the token at the start of the prompt. A secondary upstream path goes through a lower-layer lexical detector L2:F6621 which also receives strong excitation from the same "By" embedd…

</details>

<details>
<summary><b>SA-4</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F11639 | "the word "mention"" |
| 2 | `get_upstream_features` | L2:F11639@3, k=10 | Emb:" mentioning"@3 (de=27.25) +9 more |
| 3 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 4 | `inspect_feature` | L1, F3604 | " verbs in scientific or technical writing, especially those describing" |

**Findings:** L2:F11639 is a pure word‑form detector for "mention". Its dominant upstream driver is the raw token embedding of " mentioning", confirming it operates as a generic lexical detector. Additional minor positive influences come from a generic negation feature (L0:F4958) and a technical‑verb feature (L1:F3604), neither of which suggest any policy‑or refusal‑related behavior. The trace reaches layer 0 (…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×8 | L3:672, L2:6539, L4:2668, L3:11194, L0:3820, L2:2713, L3:5475, L0:1903 |
| 2 | `get_upstream_features` | L2:F10509@5, k=10 → Emb:" race"@5 (de=30.12) +9 more |
| 3 | `get_upstream_features` | L0:F10682@5, k=10 → Emb:" race"@5 (de=22.62) +9 more |

### Build

`build_circuit` → 18 nodes, 24 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 57,312 | 7,430 | 124,688 | 0 | $0.0336 | — | — |
| SA-1 | openai/gpt-oss-120b | 36,915 | 3,278 | 5,072 | 0 | $0.0076 | ✅ 3F/7E | Trace L4:F15173 (statements about mentioning/discussing some… |
| SA-4 | openai/gpt-oss-120b | 39,283 | 4,072 | 5,056 | 0 | $0.0084 | ✅ 3F/4E | Trace L2:F11639 ("mention" word) upstream. Verify it's a gen… |
| SA-3 | openai/gpt-oss-120b | 105,301 | 7,821 | 12,640 | 0 | $0.0207 | ✅ 3F/6E | Trace L3:F12410 ("By" at start of sentence) upstream. This i… |
| **Total** | | **238,811** | **22,601** | **147,456** | **0** | **$0.0703** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 39s