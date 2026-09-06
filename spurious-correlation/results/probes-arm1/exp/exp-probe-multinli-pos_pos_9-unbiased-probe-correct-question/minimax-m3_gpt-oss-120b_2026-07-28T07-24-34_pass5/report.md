# Circuit Oracle Report
**Date:** 2026-07-28 07:24:34 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_9 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a bag of early-layer lexical word-detectors and a late-layer "start of sentence" code-context feature, not by anything that semantically encodes contradiction, negation, or the meaning of the prompt.

**Confidence:** 7

**Reasoning:**

The attribution graph traces a classification probe (not a next-token prediction) on the prompt "A recorded menu will provide information on how to obtain these lists. Recorded menus do not provide any information at this time." Three independent paths push the score:

1. **Content-word lexical supernode (drives the strongest negatives).** Direct effects on the probe come mostly from layers 0–2 word-identity features that fire on the specific tokens of the prompt: L0:F2108 (the word "menu", direct_effect −0.481), L1:F12253 (the word "menu", −0.428), L0:F8046 (the word "will", −0.381), L0:F7443 ("record" in various contexts, +0.320), L0:F6649 ("title", +0.254), and L2:F8776 ("words related to finance and property law", +0.523, suspiciously the *max-token* is "equity" — the feature is coactivating on "recorded"/"menu" purely because of surface-form co-occurrence in its training set). These features all trace straight to token embeddings (Emb: menu pos 3, Emb: will pos 4, Emb: recorded pos 2), confirming they are bag-of-content-word detectors, not semantic NLI features. None of them encode entailment, contradiction, or negation.

2. **Mid-layer "menu/recording" supernode.** L2:F3059 (verb "record"), L2:F4147 ("recorded" + reporting terms), L2:F188 ("will" in legal/consequence contexts), L3:F14624 (the word "recording" with related verbs), L3:F3573 ("menu" in interface contexts), L4:F7998 (telecommunications), and L2:F3648 (menu/restaurant code) aggregate these lexical signals and pass them upward. L2:F9012 ("failed" / not-successful) is also present, and combined with "recorded" + "menu" + "do not" these features give a strong "spurious contradiction" signal. The user's concern is validated: the circuit does **not** contain a clean "negation" or "antonym" feature — it simply co-occurs that the prompt contains a word-list with the *opposite* of what was promised (a common NLI surface pattern), and the model latches onto lexical/format cues.

3. **Late-layer "start of sentence" / code-context supernode (the +0.19 contribution).** L17:F451 ("start of sentences", +0.188) and its upstream chain at pos 1 ("A") — L6:F14585 ("the" / "it" at sentence start, +0.469), L7:F462 (code documentation blocks, +0.339), L9:F8770 ("It"/"In"/"There" sentence starters, +0.364), L10:F14174 (left curly brackets, +0.519), L9:F2762/L9:F15819/L9:F3056 (JavaScript/HTML/markup code), L15:F751/L15:F851 (JSDoc/code-snippets), L16:F10989 ("the", +0.808). This is a strong, high-confidence finding: the only mid/high-layer "abstract" feature feeding the probe is *triggering on the format cue "A" at sentence start* through a deep chain of code/syntax features, then acting as a generic sentence-starter detector. Its `get_source_influence` analysis confirms that positions 1–24 (the entire prompt) carry only ~18% of signed multi-hop influence — within the soft reference band — and the top contributing features are all code/JSDoc/curly-bracket features at pos 1.

**What this means for the user's concern.** The probe is indeed largely using spurious signals: (a) bag-of-content-word features keyed to "menu", "recorded", "will", "title" — which are surface tokens of the *premise*, not contradiction markers; (b) format/style features triggered by the bare "A" sentence starter through a code-sensor chain. Crucially, **no feature in the top-15 direct-effect list encodes negation, contradiction, antonymy, or NLI semantics**. L2:F9012 ("failed/not successful") is the closest thing, but it fires on "failed" tokens that don't appear in this prompt — its contribution is via the noisy "menu" / "recording" co-activation chain, not via real contradiction detection. The circuit is therefore a textbook example of a probe that latches onto lexical overlap and prompt-format cues rather than the actual semantic content needed to recognize contradiction.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 1 | Probe output (linear classification score) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L17:F451](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) | 1 | Late-layer 'start of sentence' feature | start of sentences | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) |
| [L0:F2108](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2108) | 3 | Early-layer 'recorded/record' word-level features | the word "menu" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2108) |
| [L0:F12253](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12253) | 3 | Early-layer 'recorded/record' word-level features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12253) |
| [L0:F8046](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8046) | 4 | Early-layer 'recorded/record' word-level features |  the word "will." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8046) |
| [L1:F3691](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3691) | 2 | Early-layer 'recorded/record' word-level features |  the word "recording" in scientific or experimental documentation | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3691) |
| [L0:F7443](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) | 2 | Early-layer 'recorded/record' word-level features | the word "record" appearing in various contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) |
| [L3:F3573](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3573) | 3 | Mid-layer 'menu/recording' related features | the word "menu" often in conjunction with interface elements | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3573) |
| [L4:F7998](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7998) | 3 | Mid-layer 'menu/recording' related features |  words related to telecommunications and telephones | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7998) |
| [L2:F3648](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3648) | 3 | Mid-layer 'menu/recording' related features | code snippets related to menus and restaurants | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3648) |
| [L2:F188](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/188) | 4 | Mid-layer 'menu/recording' related features | the word "will" in various contexts, sometimes alongside words related to consequences or legal matters | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/188) |
| [L2:F3059](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3059) | 2 | Mid-layer 'menu/recording' related features |  the verb "record" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3059) |
| [L2:F8776](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8776) | 2 | Mid-layer 'menu/recording' related features |  words related to finance and property law | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8776) |
| [L2:F4147](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4147) | 2 | Mid-layer 'menu/recording' related features |  the word "recorded" (and related reporting terms) | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4147) |
| [L3:F14624](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14624) | 2 | Mid-layer 'menu/recording' related features | the word "recording" along with related verbs and nouns | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14624) |
| [L0:F6649](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6649) | 3 | Other early-layer lexical features (title, faith, will, words, code) |  the word "Title" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6649) |
| [L0:F7404](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7404) | 2 | Other early-layer lexical features (title, faith, will, words, code) |  the word "faith", sometimes in association with related ideas like "links" or "opportunities" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7404) |
| [L0:F5128](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5128) | 3 | Other early-layer lexical features (title, faith, will, words, code) |  the word "words" or words that are similar in meaning (word, Word, phrases, matrix) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5128) |
| [L0:F13280](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13280) | 2 | Other early-layer lexical features (title, faith, will, words, code) |  passages discussing real estate | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13280) |
| [L0:F9990](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9990) | 2 | Other early-layer lexical features (title, faith, will, words, code) |  the word "concert" and some words related to concerts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9990) |
| [L0:F4523](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4523) | 3 | Other early-layer lexical features (title, faith, will, words, code) | the word "domestic" and words associated with globalism | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4523) |
| [L0:F11317](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11317) | 2 | Other early-layer lexical features (title, faith, will, words, code) |  the phrase "clinical practice" or "in practice", possibly medical or related | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11317) |
| [L10:F14174](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14174) | 1 | Mid-high code/syntax features (left braces, code blocks, JSDoc) feeding 'start of sentence' | left curly brackets | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14174) |
| [L9:F8770](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8770) | 1 | Mid-high code/syntax features (left braces, code blocks, JSDoc) feeding 'start of sentence' | sentences beginning with "It" or "In" and also the word "There". | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8770) |
| [L9:F2762](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2762) | 1 | Mid-high code/syntax features (left braces, code blocks, JSDoc) feeding 'start of sentence' |  various code snippets, especially javascript | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2762) |
| [L9:F3056](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/3056) | 1 | Mid-high code/syntax features (left braces, code blocks, JSDoc) feeding 'start of sentence' |  various keywords in programming languages, markup languages, and mathematical notations | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/3056) |
| [L9:F15819](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15819) | 1 | Mid-high code/syntax features (left braces, code blocks, JSDoc) feeding 'start of sentence' | code snippets | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15819) |
| [L9:F13483](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/13483) | 1 | Mid-high code/syntax features (left braces, code blocks, JSDoc) feeding 'start of sentence' |  lines with a large amount of whitespace | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/13483) |
| [L7:F462](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) | 1 | Mid-high code/syntax features (left braces, code blocks, JSDoc) feeding 'start of sentence' |  code documentation and import statements | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) |
| [L7:F5741](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5741) | 1 | Mid-high code/syntax features (left braces, code blocks, JSDoc) feeding 'start of sentence' |  code documentation or copyright information | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5741) |
| [L6:F14585](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14585) | 1 | Mid-high code/syntax features (left braces, code blocks, JSDoc) feeding 'start of sentence' |  the words "the" and "it" at the beginning of sentences | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14585) |
| [L5:F3992](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3992) | 1 | Mid-high code/syntax features (left braces, code blocks, JSDoc) feeding 'start of sentence' | the start of documentation blocks in code | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3992) |
| [L15:F751](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/751) | 1 | Mid-high code/syntax features (left braces, code blocks, JSDoc) feeding 'start of sentence' | code snippets | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/751) |
| [L15:F851](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/851) | 1 | Mid-high code/syntax features (left braces, code blocks, JSDoc) feeding 'start of sentence' |  code documentation blocks in various programming languages | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/851) |
| [L16:F10989](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/10989) | 1 | Mid-high code/syntax features (left braces, code blocks, JSDoc) feeding 'start of sentence' | the | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/10989) |
| [L13:F8128](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/8128) | 1 | Mid-high code/syntax features (left braces, code blocks, JSDoc) feeding 'start of sentence' |  sentences beginning with the word "In" | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/8128) |
| [L14:F2510](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/2510) | 1 | Mid-high code/syntax features (left braces, code blocks, JSDoc) feeding 'start of sentence' | the word "using" | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/2510) |
| [L11:F11186](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/11186) | 1 | Mid-high code/syntax features (left braces, code blocks, JSDoc) feeding 'start of sentence' | scientific and technical terms | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/11186) |
| [L11:F10933](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/10933) | 1 | Mid-high code/syntax features (left braces, code blocks, JSDoc) feeding 'start of sentence' | the letters "L", "H," and "a" when they are at the beginning of a text block | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/10933) |
| [L6:F14531](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14531) | 1 | Mid-high code/syntax features (left braces, code blocks, JSDoc) feeding 'start of sentence' | the number 1 | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14531) |
| [L15:F10005](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10005) | 1 | Mid-high code/syntax features (left braces, code blocks, JSDoc) feeding 'start of sentence' |  "Good" or instances of the word "The" at the beginning of a block of text | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10005) |
| [L14:F15964](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/15964) | 1 | Mid-high code/syntax features (left braces, code blocks, JSDoc) feeding 'start of sentence' |  newline characters. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/15964) |
| [L0:F1903](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1903) | 1 | Mid-high code/syntax features (left braces, code blocks, JSDoc) feeding 'start of sentence' | instances of sentences starting with "The" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1903) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: recorded (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: menu (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: will (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: A (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 0 | Emb: bos (pos 0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L2:8776 de=0.523 |
| 3 | `inspect_feature` ×15 | L2:8776, L0:2108, L1:12253, L0:8046, L1:3691, L0:7443, L3:3573, L0:6649, L0:7404, L4:7998, L2:3648, L2:188, L2:3059, L0:5128, L17:451 |
| 4 | `get_upstream_features` | Emb:" recorded"@2 (de=19.50) +9 more |
| 5 | `get_upstream_features` | Emb:" menu"@3 (de=25.75) +9 more |
| 6 | `get_upstream_features` | Emb:" menu"@3 (de=20.62) +9 more |
| 7 | `get_upstream_features` | Emb:" will"@4 (de=36.00) +9 more |
| 8 | `get_upstream_features` | Emb:" recorded"@2 (de=24.75) +9 more |
| 9 | `get_upstream_features` | Emb:" recorded"@2 (de=22.62) +9 more |
| 10 | `get_upstream_features` | Emb:" menu"@3 (de=21.38) +9 more |
| 11 | `get_upstream_features` | Emb:" menu"@3 (de=14.38) +9 more |
| 12 | `get_upstream_features` | Emb:" recorded"@2 (de=14.25) +9 more |
| 13 | `get_upstream_features` | Emb:" menu"@3 (de=13.56) +9 more |
| 14 | `get_upstream_features` | Emb:" menu"@3 (de=27.75) +9 more |
| 15 | `get_upstream_features` | Emb:" will"@4 (de=26.00) +9 more |
| 16 | `get_upstream_features` | Emb:" recorded"@2 (de=22.50) +9 more |
| 17 | `get_upstream_features` | Emb:" menu"@3 (de=15.62) +9 more |
| 18 | `get_upstream_features` | L16:F10989 (de=-10.38) +9 more |
| 19 | `inspect_feature` ×10 | L16:10989, L15:751, L6:14585, L9:8770, L7:462, L4:7643, L0:4523, L0:9990, L0:13280, L0:11317 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L17:F451@1` | ❌ error | — | — | Trace the path upstream from L17:F451 ('start of sentences' at pos 1) which cont… |
| SA-2 | `L2:F8776@2` | ❌ error | — | — | Trace upstream from L2:F8776 ('words related to finance and property law' at pos… |
| SA-3 | `L0:F2108@3` | ❌ error | — | — | Trace upstream from L0:F2108 ('the word menu' at pos 3, direct_effect=-0.481 to … |
| SA-4 | `L0:F8046@4` | ❌ error | — | — | Trace upstream from L0:F8046 ('the word will.' at pos 4, direct_effect=-0.381 to… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×3 | L16:10989, L10:14174, L15:851 |
| 2 | `get_upstream_features` | L16:F10989@1, k=5 → L15:F851 (de=26.50) +4 more |
| 3 | `get_upstream_features` | L10:F14174@1, k=5 → L9:F3056 (de=14.31) +4 more |
| 4 | `inspect_feature` ×6 | L13:8128, L14:2510, L9:3056, L9:15819, L9:2762, L9:13483 |
| 5 | `get_upstream_features` | L7:F462@1, k=5 → Emb:"<bos>"@0 (de=18.62) +4 more |
| 6 | `get_upstream_features` | L9:F8770@1, k=5 → L7:F462 (de=17.00) +4 more |
| 7 | `get_upstream_features` | L6:F14585@1, k=5 → Emb:"A"@1 (de=9.88) +4 more |
| 8 | `get_upstream_features` | L10:F14174@1, k=10 → L9:F3056 (de=14.31) +9 more |
| 9 | `inspect_feature` ×3 | L5:3992, L7:5741, L0:1903 |
| 10 | `get_upstream_features` | L5:F3992@1, k=5 → Emb:"<bos>"@0 (de=22.25) +4 more |
| 11 | `get_upstream_features` | L0:F1903@1, k=5 → Emb:"<bos>"@0 (de=16.88) +4 more |
| 12 | `get_upstream_features` | L1:F12253@3, k=15 → Emb:" menu"@3 (de=20.62) +14 more |
| 13 | `get_upstream_features` | L3:F3573@3, k=15 → Emb:" menu"@3 (de=21.38) +14 more |
| 14 | `get_upstream_features` | L4:F7998@3, k=15 → Emb:" menu"@3 (de=13.56) +14 more |
| 15 | `get_upstream_features` | L17:F451@1, k=20 → L16:F10989 (de=-10.38) +19 more |
| 16 | `inspect_feature` ×7 | L2:4147, L3:14624, L11:11186, L11:10933, L6:14531, L15:10005, L14:15964 |
| 17 | `get_source_influence` | {'depth': 3, 'source_positions': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, → {'depth': 3, 'source_positions': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, |
| 18 | `inspect_feature` ×4 | L0:2115, L0:13134, L0:10373, L0:11835 |
| 19 | `get_upstream_features` | L17:F451@1, k=10 → L16:F10989 (de=-10.38) +9 more |
| 20 | `get_upstream_features` | L3:F3573@3, k=10 → Emb:" menu"@3 (de=21.38) +9 more |
| 21 | `get_upstream_features` | L4:F7998@3, k=10 → Emb:" menu"@3 (de=13.56) +9 more |
| 22 | `get_upstream_features` | L2:F4147@2, k=10 → Emb:" recorded"@2 (de=27.50) +9 more |
| 23 | `get_upstream_features` | L2:F3059@2, k=10 → Emb:" recorded"@2 (de=22.50) +9 more |
| 24 | `inspect_feature` ×6 | L1:11170, L1:763, L1:581, L1:3751, L2:9012, L1:14313 |

### Build

`build_circuit` → 11 nodes, 10 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 103,965 | 8,554 | 871,093 | 0 | $0.0937 | — | — |
| **Total** | | **103,965** | **8,554** | **871,093** | **0** | **$0.0937** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 12s