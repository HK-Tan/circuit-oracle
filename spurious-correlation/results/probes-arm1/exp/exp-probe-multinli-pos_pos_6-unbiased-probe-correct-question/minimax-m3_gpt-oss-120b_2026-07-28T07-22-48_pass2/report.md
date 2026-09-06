# Circuit Oracle Report
**Date:** 2026-07-28 07:22:48 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_6 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

Based on the analysis, I have traced the circuit. The user's concern is partially validated by the findings, but with significant nuance. The probe uses BOTH content features and a negation/state feature - the user is right that the "not" + "allowed" tokens at the end of the sentence strongly drive a late-layer "state/negation" detector, BUT content lexical features (land, fire, agriculture) also contribute positively, and several unrelated generic features (pronoun, code markers) actually push AGAINST the contradiction classification.

**Analysis:** The probe's contradiction classification score is driven by a mix of generic lexical content features (land, fire, agriculture, function words) that fire on the prompt's content words, plus a late-layer L12 feature (F12606 at pos 25) that strongly activates on the negation/state-related tokens "not", "allowed", and "forest" — which IS the closest thing to a "negation-signal" shortcut the user worried about — while a separate set of unrelated pronoun/structural features actually suppress the contradiction signal.

**Confidence:** 5

**Reasoning:** The circuit shows several distinct pathways to the probe's output score at the final position (pos 25). 

**Path 1 — Lexical content (pushes TOWARD contradiction):** The tokens "land" (pos 7), "fire" (pos 12), and "agriculture" (pos 9) feed into dedicated word-detector features: L1:F461 ("the word land", 0.00685 frac_nonzero, +0.1826 direct_effect on probe), L2:F11518 ("land" in scientific/agricultural contexts, 0.00633, +0.252), L2:F4819 ("fire", 0.00667, +0.179), L1:F361 ("agriculture and ecology", 0.00704, +0.150), and L3:F15978 ("land, property, acreage", 0.00624, +0.165). These features each receive their dominant direct drive from the raw token embedding at the same position (e.g., L2:F11518 gets +28.375 from the "land" embedding). They are specific topic/keyword detectors (frac_nonzero < 1%), but they fire on the literal content words of the prompt rather than encoding any contradiction semantics — they're "this is about agriculture/land/fire" features, not "this is a contradiction" features.

**Path 2 — Function-word lexical (pushes TOWARD contradiction):** Generic function-word detectors L0:F8444 ("to", 0.01705, +0.178) and L0:F15492 ("for", 0.0569, +0.169), plus L2:F10849 ("set"), L2:F15312 ("about"), and L3:F4464 ("about"), L6:F14744 ("about/to/work", 0.01836, +0.159) also contribute. These are even more generic (frac_nonzero up to 5.7%) and fire on every "the/to/for/about" token in any text. They are essentially frequency-bias artifacts — common English words pushing the probe score in whatever direction the probe's training happened to weight them.

**Path 3 — Late-layer negation/state detector (pushes TOWARD contradiction — the "spurious negation" the user warned about):** L12:F12606 (0.01623, +0.154) at pos 25 is the most semantically relevant late-layer feature. Its upstream is dominated by the *token embeddings* of "not" (pos 21, +3.59), "allowed" (pos 22, +1.67), "forest" (pos 17, +1.5), "were" (pos 20, +1.16), and the token at the probe's own position "forest" (+0.996), plus L3:F6227 ("sentence fragments/informal language/abbreviations", 0.01667, +0.762) at pos 23 — notably, F6227's promoted tokens are "▁not, ▁NOT, ▁Not, Not, not" — it is fundamentally a NOT/NEGATION detector. So the user's concern is well-founded: the late-layer feature driving the contradiction signal at the final position is largely a "not + allowed + forest" pattern detector, which functions as a negation/state-keyword shortcut rather than reading the actual logical relationship between the two clauses.

**Path 4 — Sentence-start/structural (pushes TOWARD contradiction):** L17:F451 ("start of sentences", 0.00671, +0.154) at pos 1 is a high-activation (62.0) start-of-sentence detector feeding off the BOS and "So" embeddings via a chain of code/structure-related layers (L7:F462, L10:F14174, L15:F751, L15:F851 — all code-documentation detectors with frac_nonzero 0.0079-0.025). This is essentially a position-bias signal, not content.

**Path 5 — Suppressors (push AWAY from contradiction):** L0:F3498 ("the pronoun they", 0.02132, **-0.621**), L4:F12225 ("So/therefore transition words", 0.0129, **-0.275**), L8:F8406 ("I/Exactly", 0.00863, **-0.243**), and L0:F2238 ("about followed by a number", 0.00657, **-0.342**) all have strong negative direct_effects. These features — pronoun "they", conclusion-marker "So", pronoun "I", "about+numbers" — are highly generic and their strong negative sign is the dominant force in the circuit (sum ≈ -1.48, larger in magnitude than the +1.32 sum of the strongest positive features above). The user is right to be suspicious: most of the "movement" of the probe score comes from generic lexical features acting in BOTH directions, not from features that encode the actual entailment relationship.

**Verdict on user's concern:** Partially confirmed. The dominant positive driver at the late layer (L12:F12606) IS a negation/state-keyword detector firing on "not" + "allowed" + "forest" + "were" — exactly the kind of "negation-word shortcut" the user worried about. Combined with the strong negative generic-feature signals (pronoun, transition word, code-marker) that dominate the circuit's magnitude, the probe appears to rely heavily on surface lexical cues — function-word distributions, negation-keyword presence, and pronoun detectors — rather than on any feature that actually compares the two sentences' claims. The content-word features (land, fire, agriculture) contribute positively but only at moderate magnitudes and encode topic rather than entailment.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 25 | Probe (contradiction classifier) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L2:F11518](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11518) | 7 | Lexical content features (land/fire/agriculture) |  the word "land" in scientific/agricultural contexts | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11518) |
| [L2:F4819](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4819) | 12 | Lexical content features (land/fire/agriculture) | sentences containing the word "fire" or similar terms | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4819) |
| [L1:F361](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/361) | 9 | Lexical content features (land/fire/agriculture) |  words related to agriculture and ecology | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/361) |
| [L3:F15978](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15978) | 7 | Lexical content features (land/fire/agriculture) |  mentions of land, property, and acreage. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15978) |
| [L1:F461](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/461) | 7 | Lexical content features (land/fire/agriculture) |  the word "land" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/461) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 13 | Function-word lexical features (to/for/about/set) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F15492](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15492) | 8 | Function-word lexical features (to/for/about/set) |  the word "for" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15492) |
| [L2:F10849](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10849) | 3 | Function-word lexical features (to/for/about/set) | the word "set" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10849) |
| [L2:F15312](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15312) | 4 | Function-word lexical features (to/for/about/set) |  the word "about." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15312) |
| [L3:F4464](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4464) | 4 | Function-word lexical features (to/for/about/set) |  the word "about" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4464) |
| [L6:F14744](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14744) | 4 | Function-word lexical features (to/for/about/set) |  the words "about," "to," and "work." | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14744) |
| [L17:F451](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) | 1 | Sentence start / structural feature | start of sentences | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) |
| [L2:F14822](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14822) | 1 | Sentence start / structural feature |  the abbreviation "SO" followed by other characters | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14822) |
| [L12:F12606](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) | 25 | Late-layer 'negation/state' detector (contradiction signal) |  phrases related to political conspiracy/organizations, mental conditions and storytelling terms | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) |
| [L3:F6227](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) | 23 | Late-layer 'negation/state' detector (contradiction signal) |  sentence fragments and informal or ungrammatical language, often including abbreviations. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) |
| [L0:F3498](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) | 2 | Push AWAY from contradiction (pronoun, transition word, code-marker) |  the pronoun "they" or its possessive form. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) |
| [L4:F12225](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12225) | 2 | Push AWAY from contradiction (pronoun, transition word, code-marker) |  transitional conclusion words, often used in legal or academic writing | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12225) |
| [L8:F8406](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) | 1 | Push AWAY from contradiction (pronoun, transition word, code-marker) | the first-person pronoun "I" and the word "Exactly" | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 18 | Push AWAY from contradiction (pronoun, transition word, code-marker) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 4 | Push AWAY from contradiction (pronoun, transition word, code-marker) |  the word "about" when followed by a numerical value | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:3498 de=-0.621 |
| 3 | `inspect_feature` ×20 | L0:3498, L0:2238, L4:12225, L2:11518, L8:8406, L4:5450, L2:15312, L3:4464, L1:461, L2:4819, L0:8444, L2:10849, L0:15492, L3:15978, L6:14744, L17:451, L12:12606, L0:6051, L2:14822, L1:361 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F11518@7` | ✅ reported | 3 | 15 | Trace the path from L2:F11518 (the word "land") upstream to its origin. What tok… |
| SA-2 | `L2:F4819@12` | ❌ error | — | — | Trace the path from L2:F4819 (the word "fire") upstream. What tokens drive it? |
| SA-3 | `L8:F8406@1` | ✅ reported | 6 | 16 | Trace the path from L8:F8406 (the first-person pronoun "I" / "Exactly") upstream… |
| SA-4 | `L4:F12225@2` | ✅ reported | 3 | 4 | Trace the path from L4:F12225 (transitional conclusion words "So/therefore") ups… |
| SA-5 | `L12:F12606@25` | ❌ error | — | — | Trace the path from L12:F12606 upstream. This is a late-layer feature at positio… |
| SA-6 | `L17:F451@1` | ✅ reported | 6 | 11 | Trace the path from L17:F451 (start of sentences) upstream. Position 1 correspon… |
| SA-7 | `L2:F4819@12` | ❌ error | — | — | Trace the path from L2:F4819 (the word "fire") upstream at pos=12 to find out wh… |
| SA-8 | `L12:F12606@25` | ❌ error | — | — | Trace the path from L12:F12606 upstream at pos=25 (end of text). What drives thi… |

<details>
<summary><b>SA-1</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F11518 | " the word "land" in scientific/agricultural contexts" |
| 2 | `get_upstream_features` | L2:F11518@7, k=10 | Emb:" land"@7 (de=28.38) +9 more |
| 3 | `inspect_feature` | L0, F12492 | " the word "debt"" |
| 4 | `inspect_feature` | L0, F6693 | "the word "hell"" |
| 5 | `get_upstream_features` | L0:F12492@7, k=5 | Emb:" land"@7 (de=13.62) +4 more |
| 6 | `get_upstream_features` | L0:F12492@7, k=10 | Emb:" land"@7 (de=13.62) +9 more |
| 7 | `get_upstream_features` | L0:F6693@7, k=5 | Emb:" land"@7 (de=14.50) +4 more |
| 8 | `inspect_feature` | L1, F461 | " the word "land"" |

**Findings:** L2:F11518 (layer 2) representing the word "land" is primarily driven by the raw input embedding of the token " land" at position 7 (direct_effect 28.375). Smaller positive contributions come from neighboring tokens "they" and "clearing". Two low‑level token‑detector features in layer 0 (F12492 for "debt" and F6693 for "hell") also receive strong positive influence from the same "land" embedding, b…

</details>

<details>
<summary><b>SA-3</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L8, F8406 | "the first-person pronoun "I" and the word "Exactly"" |
| 2 | `get_upstream_features` | L8:F8406@1, k=10 | Emb:"<bos>"@0 (de=10.25) +9 more |
| 3 | `inspect_feature` | L7, F462 | " code documentation and import statements" |
| 4 | `inspect_feature` | L7, F5741 | " code documentation or copyright information" |
| 5 | `inspect_feature` | L5, F3992 | "the start of documentation blocks in code" |
| 6 | `get_upstream_features` | L7:F462@1, k=10 | Emb:"<bos>"@0 (de=20.12) +9 more |
| 7 | `get_upstream_features` | L5:F3992@1, k=10 | Emb:"<bos>"@0 (de=20.62) +9 more |
| 8 | `get_upstream_features` | L7:F5741@1, k=10 | Emb:"<bos>"@0 (de=11.88) +9 more |
| 9 | `inspect_feature` | L6, F14585 | " the words "the" and "it" at the beginning of sentences" |
| 10 | `inspect_feature` | L5, F7489 | " the last three letters of words." |

**Findings:** The L8:F8406 pronoun feature fires at position 1 because the token there is "I". Upstream, the strongest drivers are the BOS embedding (providing a large positive bias) and a small direct effect from the token "So" (the preceding token in the prompt). Intermediate features in layers 5‑7 that primarily detect code documentation patterns (462, 5741, 3992) also feed into the pronoun feature, likely d…

</details>

<details>
<summary><b>SA-4</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F12225 | " transitional conclusion words, often used in legal or academic writin" |
| 2 | `get_upstream_features` | L4:F12225@2, k=15 | Emb:" they"@2 (de=12.75) +14 more |
| 3 | `inspect_feature` | L2, F14822 | " the abbreviation "SO" followed by other characters" |
| 4 | `inspect_feature` | L3, F11720 | "the word "that", often preceded and followed by specific words" |

**Findings:** L4:F12225 is a conclusion‑word detector that spikes on tokens such as "So" and "therefore". Its strongest upstream drivers are the raw token embeddings for the preceding token "they" (pos2) and the explicit token "So" (pos1), giving it the bulk of its activation. A mid‑layer feature in layer 2 (F14822) further reinforces the presence of the word "So", while a layer 3 feature (F11720) contributes a…

</details>

<details>
<summary><b>SA-6</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L17, F451 | "start of sentences" |
| 2 | `get_upstream_features` | L17:F451@1, k=10 | L16:F10989 (de=-11.88) +9 more |
| 3 | `inspect_feature` | L7, F462 | " code documentation and import statements" |
| 4 | `inspect_feature` | L15, F751 | "code snippets" |
| 5 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 6 | `get_upstream_features` | L15:F751@1, k=10 | L14:F15964 (de=18.88) +9 more |
| 7 | `inspect_feature` | L14, F15964 | " newline characters." |
| 8 | `inspect_feature` | L10, F14174 | "left curly brackets" |
| 9 | `get_upstream_features` | L7:F462@1, k=10 | Emb:"<bos>"@0 (de=20.12) +9 more |

**Findings:** Tracing from the start‑of‑sentence detector (L17:F451) quickly reaches a low‑layer (L7) feature that already connects directly to input embeddings (<bos> and the token "So"). The path also passes through intermediate code‑related features (L15:F751, L15:F851, L14:F15964, L10:F14174) which are generic structural detectors and do not exhibit refusal‑related semantics (no promoted tokens like "cannot…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L2:F4819@12, k=10 → Emb:" fire"@12 (de=32.00) +9 more |
| 2 | `get_upstream_features` | L12:F12606@25, k=10 → Emb:" not"@21 (de=3.59) +9 more |
| 3 | `get_upstream_features` | L0:F3498@2, k=10 → Emb:" they"@2 (de=42.75) +9 more |
| 4 | `inspect_feature` ×6 | L1:5978, L0:11835, L3:6227, L0:2909, L1:1025, L1:6932 |
| 5 | `get_upstream_features` | L17:F451@1, k=10 → L16:F10989 (de=-11.88) +9 more |
| 6 | `get_upstream_features` | L8:F8406@1, k=10 → Emb:"<bos>"@0 (de=10.25) +9 more |
| 7 | `get_upstream_features` | L0:F2238@4, k=10 → Emb:" about"@4 (de=35.00) +9 more |
| 8 | `get_upstream_features` | L2:F10849@3, k=10 → Emb:" set"@3 (de=17.12) +9 more |
| 9 | `get_upstream_features` | L2:F15312@4, k=10 → Emb:" about"@4 (de=13.69) +9 more |
| 10 | `inspect_feature` ×7 | L16:10989, L13:8128, L14:2510, L9:8770, L15:10005, L1:3604, L0:13029 |
| 11 | `get_upstream_features` | L1:F361@9, k=10 → Emb:" agriculture"@9 (de=14.31) +9 more |
| 12 | `get_upstream_features` | L3:F15978@7, k=10 → Emb:" land"@7 (de=16.12) +9 more |
| 13 | `get_upstream_features` | L1:F461@7, k=10 → Emb:" land"@7 (de=24.88) +9 more |
| 14 | `get_upstream_features` | L2:F14822@1, k=10 → Emb:"So"@1 (de=19.62) +9 more |
| 15 | `inspect_feature` | L3, F6227 → " sentence fragments and informal or ungrammatical language, often incl" |
| 16 | `get_upstream_features` | L3:F6227@23, k=10 → Emb:" to"@23 (de=6.75) +9 more |
| 17 | `get_upstream_features` | L6:F14744@4, k=10 → Emb:" about"@4 (de=5.81) +9 more |
| 18 | `get_upstream_features` | L3:F15978@7, k=10 → Emb:" land"@7 (de=16.12) +9 more |
| 19 | `inspect_feature` | L0, F8444 → "the word "to"" |
| 20 | `get_upstream_features` | L3:F4464@4, k=10 → Emb:" set"@3 (de=10.19) +9 more |
| 21 | `get_upstream_features` | L2:F15312@4, k=10 → Emb:" about"@4 (de=13.69) +9 more |
| 22 | `inspect_feature` ×6 | L2:4531, L2:10631, L0:3498, L0:2238, L17:451, L0:8444 |
| 23 | `get_upstream_features` | L0:F8444@18, k=10 → ❌ Feature (layer=0, feature_idx=8444) not found at pos=18. Thi |
| 24 | `get_upstream_features` | L0:F8444@13, k=10 → Emb:" to"@13 (de=41.00) +9 more |
| 25 | `inspect_feature` ×2 | L6:14744, L12:12606 |
| 26 | `get_upstream_features` | L17:F451@1, k=10 → L16:F10989 (de=-11.88) +9 more |
| 27 | `get_upstream_features` | L12:F12606@25, k=10 → Emb:" not"@21 (de=3.59) +9 more |
| 28 | `get_upstream_features` | L16:F10989@1, k=10 → L15:F851 (de=28.00) +9 more |
| 29 | `get_upstream_features` | L15:F851@1, k=10 → L12:F12493 (de=19.38) +9 more |
| 30 | `get_upstream_features` | L15:F751@1, k=10 → L14:F15964 (de=18.88) +9 more |
| 31 | `get_upstream_features` | L12:F12493@1, k=10 → L10:F14174 (de=14.38) +9 more |
| 32 | `get_upstream_features` | L9:F2762@1, k=10 → Emb:"<bos>"@0 (de=14.50) +9 more |
| 33 | `get_upstream_features` | L10:F14174@1, k=10 → L9:F3056 (de=15.31) +9 more |
| 34 | `get_upstream_features` | L7:F462@1, k=10 → Emb:"<bos>"@0 (de=20.12) +9 more |
| 35 | `inspect_feature` ×6 | L12:12493, L9:2762, L10:14174, L7:462, L7:5741, L5:3992 |
| 36 | `get_upstream_features` | L12:F12606@25, k=10 → Emb:" not"@21 (de=3.59) +9 more |
| 37 | `inspect_feature` ×2 | L0:3498, L12:12606 |
| 38 | `get_upstream_features` | L12:F12606@25, k=10 → Emb:" not"@21 (de=3.59) +9 more |
| 39 | `inspect_feature` ×5 | L17:451, L1:361, L3:15978, L6:14744, L2:15312 |
| 40 | `get_upstream_features` | L12:F12606@25, k=10 → Emb:" not"@21 (de=3.59) +9 more |

### Build

`build_circuit` → 18 nodes, 18 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 121,282 | 9,291 | 1,634,286 | 0 | $0.1456 | — | — |
| SA-4 | openai/gpt-oss-120b | 36,329 | 2,182 | 2,544 | 0 | $0.0068 | ✅ 3F/4E | Trace the path from L4:F12225 (transitional conclusion words… |
| SA-1 | openai/gpt-oss-120b | 74,797 | 6,017 | 2,528 | 0 | $0.0149 | ✅ 3F/15E | Trace the path from L2:F11518 (the word "land") upstream to … |
| SA-6 | openai/gpt-oss-120b | 115,056 | 7,992 | 12,656 | 0 | $0.0222 | ✅ 6F/11E | Trace the path from L17:F451 (start of sentences) upstream. … |
| SA-3 | openai/gpt-oss-120b | 113,762 | 6,534 | 7,584 | 0 | $0.0211 | ✅ 6F/16E | Trace the path from L8:F8406 (the first-person pronoun "I" /… |
| **Total** | | **461,226** | **32,016** | **1,659,598** | **0** | **$0.2106** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 8m 28s