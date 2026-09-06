# Circuit Oracle Report
**Date:** 2026-07-28 07:23:09 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_6 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction classification is driven almost entirely by a small set of *spurious* cues — the explicit negation tokens "not allowed" at the end of the sentence and low-level function-word/lexical features — rather than any actual comprehension of the contradiction between the premise ("clearing the land for agriculture") and the hypothesis ("not allowed to deforest for agricultural purposes"). The features firing on the content side (land, fire, about, for, set, agriculture) are *generic word-identity detectors* (frac_nonzero 0.006–0.06, no semantic composition), and the only late-layer "negation" feature (L12:F12606) literally activates on "conspiracy / State / ADD"-style token patterns triggered by the bare tokens "not" and "allowed."

**Confidence:** 7

**Reasoning:**

The circuit reveals four parallel paths into the probe output, none of which encodes the entailment/contradiction relationship in any meaningful way:

1. **Negation-token path (the user's hypothesis is confirmed here).** The strongest non-embedding path runs through **L3:F6227 at pos 23** (label: "sentence fragments…promoted tokens include `not`, `Not`, `NOT`"), which gets direct positive effect from the embedding nodes `Emb: not (pos 21, +5.16)`, `Emb: allowed (pos 22, +3.45)`, and `Emb: to (pos 23, +6.75)`. This is a surface-level "presence of a negation word near 'allowed to'" detector — not a model of the contradiction. The same pattern repeats through **L12:F12606 at pos 25** (label: "conspiracy / mental conditions / State / ADD"), whose top upstream contributors are the embeddings for `not (pos 21, +3.59)`, `allowed (pos 22, +1.67)`, `land (pos 7, +1.54)`, `forest (pos 17, +1.50)`, and `were (pos 20, +1.16)`. Despite its high-level label, this feature is just a bag-of-content-word detector that happens to fire when "not" + content words co-occur — it has no notion of contradiction semantics.

2. **Generic lexical path.** The L1–L3 content-word supernode (F11518 "land in agricultural context", F4819 "fire", F10849 "set", F461 "land", F361 "agricultural", F15312 "about", F4464 "about") is a cluster of *single-word detectors* with frac_nonzero between 0.006 and 0.009 — i.e., they fire on the word itself regardless of context. The trace shows each one is dominated by the *embedding* of its own word (e.g., F11518 pos 7 gets +28.4 from `Emb: land`; F461 pos 7 gets +24.9 from `Emb: land`; F10849 pos 3 gets +17.1 from `Emb: set`). These features do not compose meaning across the sentence.

3. **L0 function-word path.** F3498 (they), F2238 (about), F8444 (to), F15492 (for), F6051 (period) are pure function-word detectors at the embedding layer with very high frac_nonzero (F15492 = 0.057, F6051 = 0.057). They are essentially routing raw positional word identity into the probe.

4. **Sentence-start / code-syntax path (the most striking evidence of spuriousness).** **L17:F451 at pos 1** (label: "start of sentences") is the only "late-layer" feature with direct effect to the output, and it is fed by an entire chain of L5–L15 features at pos 1 whose top activating examples are *all code snippets*: **F14174 ("left curly brackets")**, **F10933 ("first word of a paragraph")**, **F3056 (programming keywords)**, **F15819 (code snippets)**, **F2762 (javascript code)**, **F13483 (whitespace)**, **F8770 (sentences beginning with It/In/There)**, **F462 (code documentation comments), F5741 (copyright headers)**, **F3992 (start of documentation blocks)**. The L15:F751 ("code snippets") and L15:F10005 ("Good/ The at block start") upstream links confirm this. The chain originates at `Emb: So (pos 1)` and `Emb: <bos> (pos 0)`. This path is detecting that the input *begins with a capitalized word*, not anything about the premise–hypothesis relationship. The activated code-syntax features all also have very low frac_nonzero (0.007–0.025) — they're highly specific surface detectors.

**What is missing from the circuit:** there is no feature that builds a representation of "the people set fire to forest" or "the people were not allowed to deforest" or compares them. There is no entity-tracking, no event-overlap computation, no discourse-relation feature. The only "semantic-ish" feature (F361 "words related to agriculture and ecology" at pos 9) is a single-word detector triggered by `Emb: agriculture (pos 9, +14.3)`. The mid-layer L4–L6 features (F12225 "transitional conclusion words", F5450 "starting something", F14744 "about/to/work", F9085 "starting or doing a task with effort") are also generic lexical patterns.

**Net assessment:** the user's concern is correct and well-supported by the graph. The contradiction signal is being constructed from (a) the *literal presence* of the negation word "not" combined with "allowed", plus (b) a grab-bag of low-level content-word and function-word features, plus (c) a code/syntax detection path triggered by the input starting with "So <bos>". There is no evidence the probe has identified that the premise and hypothesis make incompatible claims about the same event. The contradiction classification would likely fire on any sentence containing "not allowed to" + agriculture/land words, regardless of whether the surrounding context actually contradicts anything.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L3:F6227](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) | 23 | Negation/constraint phrase detectors (L2-L3) — fire on 'not allowed to' at end of sentence |  sentence fragments and informal or ungrammatical language, often including abbreviations. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) |
| [L2:F11518](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11518) | 7 | Content-word detectors (land, fire, about, for, to, set, agriculture) — very generic, low-level lexical features |  the word "land" in scientific/agricultural contexts | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11518) |
| [L2:F4819](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4819) | 12 | Content-word detectors (land, fire, about, for, to, set, agriculture) — very generic, low-level lexical features | sentences containing the word "fire" or similar terms | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4819) |
| [L2:F10849](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10849) | 3 | Content-word detectors (land, fire, about, for, to, set, agriculture) — very generic, low-level lexical features | the word "set" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10849) |
| [L1:F461](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/461) | 7 | Content-word detectors (land, fire, about, for, to, set, agriculture) — very generic, low-level lexical features |  the word "land" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/461) |
| [L1:F361](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/361) | 9 | Content-word detectors (land, fire, about, for, to, set, agriculture) — very generic, low-level lexical features |  words related to agriculture and ecology | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/361) |
| [L2:F15312](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15312) | 4 | Content-word detectors (land, fire, about, for, to, set, agriculture) — very generic, low-level lexical features |  the word "about." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15312) |
| [L3:F4464](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4464) | 4 | Content-word detectors (land, fire, about, for, to, set, agriculture) — very generic, low-level lexical features |  the word "about" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4464) |
| [L0:F3498](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) | 2 | Generic function-word embeddings (L0) — they, about, to, for, periods |  the pronoun "they" or its possessive form. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 4 | Generic function-word embeddings (L0) — they, about, to, for, periods |  the word "about" when followed by a numerical value | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 13 | Generic function-word embeddings (L0) — they, about, to, for, periods | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F15492](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15492) | 8 | Generic function-word embeddings (L0) — they, about, to, for, periods |  the word "for" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15492) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 18 | Generic function-word embeddings (L0) — they, about, to, for, periods | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L12:F12606](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) | 25 | Mid-layer L12 'conspiracy/State/ADD' feature — driven by 'not allowed' tokens, NOT by the contradiction semantics |  phrases related to political conspiracy/organizations, mental conditions and storytelling terms | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) |
| [L17:F451](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) | 1 | L17 'start of sentence' feature (pos 1, 'So') — path dominated by code/syntax-related features, not by meaning of premise | start of sentences | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) |
| [L10:F14174](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14174) | 1 | Mid-layer code/syntax features at pos 1 — curly brackets, code comments, scientific terms, imports, paragraph-start | left curly brackets | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14174) |
| [L10:F10933](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/10933) | 1 | Mid-layer code/syntax features at pos 1 — curly brackets, code comments, scientific terms, imports, paragraph-start |  the first word of a paragraph or title | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/10933) |
| [L9:F3056](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/3056) | 1 | Mid-layer code/syntax features at pos 1 — curly brackets, code comments, scientific terms, imports, paragraph-start |  various keywords in programming languages, markup languages, and mathematical notations | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/3056) |
| [L9:F15819](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15819) | 1 | Mid-layer code/syntax features at pos 1 — curly brackets, code comments, scientific terms, imports, paragraph-start | code snippets | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15819) |
| [L9:F2762](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2762) | 1 | Mid-layer code/syntax features at pos 1 — curly brackets, code comments, scientific terms, imports, paragraph-start |  various code snippets, especially javascript | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2762) |
| [L9:F13483](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/13483) | 1 | Mid-layer code/syntax features at pos 1 — curly brackets, code comments, scientific terms, imports, paragraph-start |  lines with a large amount of whitespace | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/13483) |
| [L9:F8770](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8770) | 1 | Mid-layer code/syntax features at pos 1 — curly brackets, code comments, scientific terms, imports, paragraph-start | sentences beginning with "It" or "In" and also the word "There". | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8770) |
| [L7:F462](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) | 1 | Mid-layer code/syntax features at pos 1 — curly brackets, code comments, scientific terms, imports, paragraph-start |  code documentation and import statements | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) |
| [L7:F5741](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5741) | 1 | Mid-layer code/syntax features at pos 1 — curly brackets, code comments, scientific terms, imports, paragraph-start |  code documentation or copyright information | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5741) |
| [L5:F3992](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3992) | 1 | Mid-layer code/syntax features at pos 1 — curly brackets, code comments, scientific terms, imports, paragraph-start | the start of documentation blocks in code | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3992) |
| [L4:F12225](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12225) | 2 | Mid-layer code/syntax features at pos 1 — curly brackets, code comments, scientific terms, imports, paragraph-start |  transitional conclusion words, often used in legal or academic writing | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12225) |
| [L4:F5450](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5450) | 4 | Mid-layer code/syntax features at pos 1 — curly brackets, code comments, scientific terms, imports, paragraph-start |  code snippets from different languages and words related to starting or beginning something | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5450) |
| [L6:F14744](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14744) | 4 | Mid-layer code/syntax features at pos 1 — curly brackets, code comments, scientific terms, imports, paragraph-start |  the words "about," "to," and "work." | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14744) |
| [L4:F9085](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9085) | 4 | Mid-layer code/syntax features at pos 1 — curly brackets, code comments, scientific terms, imports, paragraph-start |  phrases related to starting or doing a task with effort. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9085) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:3498 de=-0.621 |
| 3 | `inspect_feature` ×20 | L0:3498, L0:2238, L4:12225, L2:11518, L8:8406, L4:5450, L2:15312, L3:4464, L1:461, L2:4819, L0:8444, L2:10849, L0:15492, L3:15978, L6:14744, L17:451, L12:12606, L0:6051, L2:14822, L1:361 |
| 4 | `get_upstream_features` | L16:F10989 (de=-11.88) +9 more |
| 5 | `get_upstream_features` | Emb:" not"@21 (de=3.59) +9 more |
| 6 | `get_upstream_features` | Emb:"<bos>"@0 (de=10.25) +9 more |
| 7 | `get_upstream_features` | Emb:" about"@4 (de=5.81) +9 more |
| 8 | `inspect_feature` ×11 | L3:6227, L16:10989, L15:751, L10:14174, L13:8128, L9:8770, L7:462, L15:10005, L7:5741, L5:3992, L4:9085 |
| 9 | `get_upstream_features` | Emb:" to"@23 (de=6.75) +9 more |
| 10 | `get_upstream_features` | L9:F3056 (de=15.31) +9 more |
| 11 | `get_upstream_features` | L12:F12493 (de=9.12) +9 more |
| 12 | `get_upstream_features` | L10:F14174 (de=10.69) +7 more |
| 13 | `get_upstream_features` | L14:F15964 (de=18.88) +7 more |
| 14 | `inspect_feature` ×12 | L9:3056, L9:15819, L9:2762, L9:13483, L12:12493, L12:3684, L11:11186, L10:10933, L14:15964, L13:5948, L0:7820, L1:2493 |
| 15 | `get_upstream_features` | L10:F14174 (de=14.38) +4 more |
| 16 | `get_upstream_features` | L11:F11186 (de=-7.03) +4 more |
| 17 | `get_upstream_features` | L9:F2762 (de=14.94) +4 more |
| 18 | `get_upstream_features` | L9:F8770 (de=8.81) +4 more |
| 19 | `inspect_feature` ×2 | L10:12232, L10:6804 |
| 20 | `get_upstream_features` | L9:F3056 (de=15.31) +2 more |
| 21 | `get_upstream_features` | L9:F2762 (de=9.38) +2 more |
| 22 | `get_upstream_features` | Emb:"<bos>"@0 (de=14.50) +2 more |
| 23 | `get_upstream_features` | Emb:" set"@3 (de=17.12) +4 more |
| 24 | `get_upstream_features` | Emb:" to"@13 (de=41.00) +4 more |
| 25 | `get_upstream_features` | Emb:" for"@8 (de=39.00) +4 more |
| 26 | `get_upstream_features` | Emb:"."@18 (de=47.00) +4 more |
| 27 | `get_upstream_features` | Emb:"So"@1 (de=19.62) +4 more |
| 28 | `get_upstream_features` | Emb:" land"@7 (de=28.38) +4 more |
| 29 | `get_upstream_features` | Emb:" fire"@12 (de=32.00) +4 more |
| 30 | `get_upstream_features` | Emb:" about"@4 (de=13.69) +4 more |
| 31 | `get_upstream_features` | Emb:" set"@3 (de=10.19) +4 more |
| 32 | `get_upstream_features` | Emb:" agriculture"@9 (de=14.31) +4 more |
| 33 | `get_upstream_features` | Emb:" land"@7 (de=24.88) +4 more |

### Build

`build_circuit` → 20 nodes, 28 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 94,261 | 8,500 | 533,120 | 0 | $0.0705 | — | — |
| **Total** | | **94,261** | **8,500** | **533,120** | **0** | **$0.0705** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 2s