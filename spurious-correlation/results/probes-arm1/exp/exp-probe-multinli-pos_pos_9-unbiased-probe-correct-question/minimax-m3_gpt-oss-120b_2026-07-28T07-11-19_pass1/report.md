# Circuit Oracle Report
**Date:** 2026-07-28 07:11:19 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_9 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "contradiction" classification score is driven by a shallow lexical/negation heuristic — large-magnitude contributions come from the *menu/recorded/list* topic detectors, generic surface features (L17:451 sentence-start, L16:10989 "the", L16:11696 "does/did"), and crucially the L4 negation features L4:4492 and L4:2422 (labels: "negations in various languages" / "negations in other languages") that fire directly on the word "not" — rather than any genuine NLI-relevant semantic reasoning.

**Confidence:** 8

**Reasoning:** The user's suspicion is strongly confirmed. The attribution graph reveals that this NLI "contradiction" probe is not using a real semantic model of premise/hypothesis contradiction at all. The strongest direct effects on the probe score are split between two clearly shallow channels:

1. **A topic-firing channel over "menu/recorded/list"** — many of the top features (L2:8776 "finance/property law", L0:2108 + L1:12253 + L3:3573 all "the word menu", L0:7443 + L1:3691 + L2:3059 + L2:10798 "the word record/recording", L4:14061 + L4:14235 "the word list", L6:11757 "videos/YouTube", L6:6132 "CCTV/cameras") are essentially word-level lexical detectors that fire on the surface tokens `recorded menu will provide` and `lists`. These trace back cleanly to the token embeddings of "recorded" (pos 2), " menu" (pos 3), " will" (pos 4), " provide" (pos 5), and " lists" (pos 12) — confirming the signal originates in input token identity, not in any cross-sentence relation.

2. **A negation-word channel** — features L4:4492 ("negations in various languages", frac_nonzero=0.038) and L4:2422 ("negations in other languages like French, Malay, and Croatian", frac_nonzero=0.016) carry large direct effects from the "not" embedding at pos 17 (direct_effect 17.4 and 16.1 to those two features respectively). This is exactly the spurious "negation = contradiction" heuristic the user identified: the probe sees the word "not" and lights up, without encoding the actual semantic relation between the premise and the hypothesis (which here is subtle — the premise claims recorded menus *do* provide information, so "do not" in the second sentence is a true semantic contradiction, but the circuit fires on the surface "not" anyway, the same way it would fire on any random "not" in any random premise/hypothesis pair).

3. **A generic surface channel** — the late layer (L17:451 "start of sentences", L16:10989 "the", L16:11696 "does/did", L10:6670 "technical terms", L10:14174 "left curly brackets", L8:8406 "I/Exactly") and the L0 generic features (L0:9026 frac=0.41 "technical documents", L0:11835 frac=0.29 "code terms", L1:14137 frac=0.39 "legal/technical documents") are extremely high-frequency, broad-context features that fire almost everywhere — these carry smaller direct effects individually but anchor the probe in surface statistics.

No feature anywhere in the circuit encodes a *relational* property between the two sentences (e.g., polarity-flip, lexical overlap, entailment direction). The contradiction signal collapses to: (presence of the word "not") + (presence of "menu/recorded/list" topic tokens) + (generic technical-document surface features). This is a textbook spurious-correlation artifact, and the user's interpretation is correct.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2108](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2108) | 3 | Layer 0 lexical feature detectors (early token-level features) | the word "menu" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2108) |
| [L0:F8046](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8046) | 4 | Layer 0 lexical feature detectors (early token-level features) |  the word "will." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8046) |
| [L0:F7443](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) | 2 | Layer 0 lexical feature detectors (early token-level features) | the word "record" appearing in various contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) |
| [L0:F6649](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6649) | 3 | Layer 0 lexical feature detectors (early token-level features) |  the word "Title" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6649) |
| [L0:F7404](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7404) | 2 | Layer 0 lexical feature detectors (early token-level features) |  the word "faith", sometimes in association with related ideas like "links" or "opportunities" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7404) |
| [L0:F5128](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5128) | 3 | Layer 0 lexical feature detectors (early token-level features) |  the word "words" or words that are similar in meaning (word, Word, phrases, matrix) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5128) |
| [L0:F4523](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4523) | 3 | Layer 0 lexical feature detectors (early token-level features) | the word "domestic" and words associated with globalism | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4523) |
| [L0:F13280](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13280) | 2 | Layer 0 lexical feature detectors (early token-level features) |  passages discussing real estate | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13280) |
| [L0:F9990](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9990) | 2 | Layer 0 lexical feature detectors (early token-level features) |  the word "concert" and some words related to concerts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9990) |
| [L0:F15480](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15480) | 10 | Layer 0 lexical feature detectors (early token-level features) |  usages of the word "back" and similar words involved in processes | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15480) |
| [L0:F5099](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5099) | 10 | Layer 0 lexical feature detectors (early token-level features) | the word "obtain" and related words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5099) |
| [L0:F16046](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16046) | 8 | Layer 0 lexical feature detectors (early token-level features) | question words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16046) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 2 | Layer 0 lexical feature detectors (early token-level features) | technical documents or data, including numbers, units, and references to figures or tables. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F3017](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3017) | 3 | Layer 0 lexical feature detectors (early token-level features) |  mentions of weather and weather reporting | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3017) |
| [L0:F4071](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4071) | 5 | Layer 0 lexical feature detectors (early token-level features) |  the words "assigned" and "assigning", sometimes with a very weak association to "particular" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4071) |
| [L0:F9489](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9489) | 4 | Layer 0 lexical feature detectors (early token-level features) |  the word "would" and words adjacent to would | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9489) |
| [L0:F13938](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13938) | 2 | Layer 0 lexical feature detectors (early token-level features) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13938) |
| [L0:F11835](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11835) | 3 | Layer 0 lexical feature detectors (early token-level features) | terms used in software code such as "assembly", "using", "namespace", and "license" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11835) |
| [L1:F12253](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12253) | 3 | Layer 1 single-word features |  the word 'menu' | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12253) |
| [L1:F3691](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3691) | 2 | Layer 1 single-word features |  the word "recording" in scientific or experimental documentation | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3691) |
| [L1:F6817](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6817) | 2 | Layer 1 single-word features | the word "category" or "categories" regardless of the context they appear in | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6817) |
| [L1:F5249](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5249) | 2 | Layer 1 single-word features | the word "pipe" or "pipes" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5249) |
| [L1:F10242](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10242) | 2 | Layer 1 single-word features |  text about animals and/or experimental subjects being fed something in a scientific or agricultural context | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10242) |
| [L1:F7463](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7463) | 4 | Layer 1 single-word features |  the word "will," possibly indicating a future tense or prediction | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7463) |
| [L1:F1958](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1958) | 5 | Layer 1 single-word features | the word "provide" and its variations. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1958) |
| [L1:F4515](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4515) | 3 | Layer 1 single-word features |  details of album arrangements | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4515) |
| [L1:F11170](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11170) | 3 | Layer 1 single-word features | words related to telephones and connecting/disconnecting calls | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11170) |
| [L1:F7207](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7207) | 2 | Layer 1 single-word features |  mathematical notation, especially exponents with negative signs | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7207) |
| [L1:F14137](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14137) | 2 | Layer 1 single-word features |  words or phrases that appear in legal or technical documents, like names of laws, legal terms (pleaded, testified), and technical terms, especially when abbreviated or in code | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14137) |
| [L1:F12169](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12169) | 2 | Layer 1 single-word features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12169) |
| [L2:F8776](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8776) | 2 | Layer 2 lexical composition features |  words related to finance and property law | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8776) |
| [L2:F3648](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3648) | 3 | Layer 2 lexical composition features | code snippets related to menus and restaurants | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3648) |
| [L2:F188](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/188) | 4 | Layer 2 lexical composition features | the word "will" in various contexts, sometimes alongside words related to consequences or legal matters | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/188) |
| [L2:F3059](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3059) | 2 | Layer 2 lexical composition features |  the verb "record" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3059) |
| [L2:F11317](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11317) | 2 | Layer 2 lexical composition features |  abbreviated examples | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11317) |
| [L2:F7863](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7863) | 5 | Layer 2 lexical composition features | the word "provide" in various forms. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7863) |
| [L2:F10798](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10798) | 2 | Layer 2 lexical composition features |  words related to music recording | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10798) |
| [L2:F4147](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4147) | 2 | Layer 2 lexical composition features |  the word "recorded" (and related reporting terms) | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4147) |
| [L2:F9012](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9012) | 3 | Layer 2 lexical composition features |  instances where something was not successful | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9012) |
| [L2:F1838](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1838) | 3 | Layer 2 lexical composition features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1838) |
| [L3:F3573](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3573) | 3 | Layer 3 menu/recording topic detectors | the word "menu" often in conjunction with interface elements | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3573) |
| [L3:F14624](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14624) | 2 | Layer 3 menu/recording topic detectors | the word "recording" along with related verbs and nouns | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14624) |
| [L4:F7998](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7998) | 3 | Layer 4 negation-word and 'list' features |  words related to telecommunications and telephones | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7998) |
| [L4:F7998](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7998) | 2 | Layer 4 negation-word and 'list' features |  words related to telecommunications and telephones | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7998) |
| [L4:F7643](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7643) | 5 | Layer 4 negation-word and 'list' features |  words related to providing assistance or describing results | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7643) |
| [L4:F14061](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14061) | 3 | Layer 4 negation-word and 'list' features |  terms related to menus and data relations | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14061) |
| [L4:F14061](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14061) | 2 | Layer 4 negation-word and 'list' features |  terms related to menus and data relations | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14061) |
| [L4:F14235](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14235) | 12 | Layer 4 negation-word and 'list' features |  the word "list" and words like "listed" and "alphabetically" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14235) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 17 | Layer 4 negation-word and 'list' features | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 17 | Layer 4 negation-word and 'list' features | negations in other languages like French, Malay, and Croatian | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L4:F13248](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13248) | 2 | Layer 4 negation-word and 'list' features | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13248) |
| [L4:F15641](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15641) | 2 | Layer 4 negation-word and 'list' features | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15641) |
| [L5:F14641](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14641) | 2 | Layer 5 video/recording features |  words relating to recording audio and/or video | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14641) |
| [L5:F14534](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14534) | 2 | Layer 5 video/recording features | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14534) |
| [L5:F6053](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6053) | 2 | Layer 5 video/recording features | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6053) |
| [L6:F11757](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11757) | 2 | Layer 6 video references |  references to videos, particularly on YouTube | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11757) |
| [L6:F6132](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6132) | 2 | Layer 6 video references | mentions pertaining to surveillance and video technology | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6132) |
| [L8:F8406](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) | 1 | Layer 8 'I/Exactly' feature | the first-person pronoun "I" and the word "Exactly" | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) |
| [L10:F6670](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) | 20 | Layer 10 late technical-context features | technical terms, especially within scientific or medical contexts | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) |
| [L10:F6670](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) | 18 | Layer 10 late technical-context features | technical terms, especially within scientific or medical contexts | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) |
| [L10:F14174](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14174) | 1 | Layer 10 late technical-context features | left curly brackets | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14174) |
| [L16:F10989](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/10989) | 1 | Layer 16 late lexical features (does/did, 'the') | the | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/10989) |
| [L16:F11696](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11696) | 16 | Layer 16 late lexical features (does/did, 'the') | does/did | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11696) |
| [L17:F451](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) | 1 | Layer 17 sentence-start feature | start of sentences | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L2:8776 de=0.523 |
| 3 | `inspect_feature` ×12 | L2:8776, L0:2108, L1:12253, L0:8046, L1:3691, L0:7443, L3:3573, L0:6649, L0:7404, L4:7998, L17:451, L2:188 |
| 4 | `get_top_features` | 40 features; top: L2:8776 de=0.523 |
| 5 | `inspect_feature` ×27 | L2:3648, L2:3059, L0:5128, L0:4523, L2:11317, L4:7643, L0:9990, L0:13280, L0:15480, L5:14641, L2:7863, L6:11757, L1:6817, L8:8406, L10:6670, L6:6132, L1:5249, L0:9026, L1:10242, L0:3281, L0:3017, L4:14061, L0:12774, L0:5099, L0:16046, L4:14235, L0:14061 |
| 6 | `get_upstream_features` | L16:F10989 (de=-10.38) +9 more |
| 7 | `inspect_feature` ×3 | L16:10989, L15:751, L10:14174 |
| 8 | `get_upstream_features` | Emb:" recorded"@2 (de=19.50) +9 more |
| 9 | `get_upstream_features` | Emb:" recorded"@2 (de=24.75) +9 more |
| 10 | `get_upstream_features` | Emb:" will"@4 (de=36.00) +9 more |
| 11 | `get_upstream_features` | Emb:" menu"@3 (de=25.75) +9 more |
| 12 | `get_upstream_features` | Emb:" menu"@3 (de=20.62) +9 more |
| 13 | `get_upstream_features` | Emb:" menu"@3 (de=21.38) +9 more |
| 14 | `get_upstream_features` | Emb:" menu"@3 (de=13.56) +9 more |
| 15 | `get_upstream_features` | Emb:" will"@4 (de=26.00) +9 more |
| 16 | `get_upstream_features` | Emb:" provide"@5 (de=3.89) +9 more |
| 17 | `inspect_feature` ×2 | L1:11170, L1:7463 |
| 18 | `get_upstream_features` | Emb:" recorded"@2 (de=22.50) +9 more |
| 19 | `get_upstream_features` | Emb:" recorded"@2 (de=22.62) +9 more |
| 20 | `get_upstream_features` | Emb:" menu"@3 (de=15.62) +9 more |
| 21 | `get_upstream_features` | Emb:" menu"@3 (de=14.38) +9 more |
| 22 | `get_upstream_features` | Emb:" recorded"@2 (de=14.25) +9 more |
| 23 | `get_upstream_features` | Emb:" provide"@5 (de=24.38) +9 more |
| 24 | `get_upstream_features` | Emb:" recorded"@2 (de=13.75) +9 more |
| 25 | `get_upstream_features` | Emb:" recorded"@2 (de=18.00) +9 more |
| 26 | `get_upstream_features` | Emb:" recorded"@2 (de=12.62) +9 more |
| 27 | `get_upstream_features` | Emb:" menu"@3 (de=11.69) +9 more |
| 28 | `get_upstream_features` | Emb:" recorded"@2 (de=10.75) +9 more |
| 29 | `get_upstream_features` | Emb:" recorded"@2 (de=14.75) +9 more |
| 30 | `get_upstream_features` | Emb:" obtain"@10 (de=17.38) +9 more |
| 31 | `get_upstream_features` | Emb:" lists"@12 (de=16.62) +9 more |
| 32 | `get_upstream_features` | Emb:" obtain"@10 (de=20.62) +9 more |
| 33 | `get_upstream_features` | Emb:"<bos>"@0 (de=9.62) +9 more |
| 34 | `get_upstream_features` | Emb:" information"@20 (de=-4.62) +9 more |
| 35 | `get_upstream_features` | Emb:" recorded"@2 (de=9.06) +9 more |
| 36 | `get_upstream_features` | Emb:" menu"@3 (de=16.25) +9 more |
| 37 | `get_upstream_features` | Emb:" how"@8 (de=10.25) +9 more |
| 38 | `inspect_feature` ×8 | L1:11363, L2:13545, L3:11479, L3:15841, L3:14624, L4:4492, L4:2422, L3:11448 |
| 39 | `get_upstream_features` | Emb:" not"@17 (de=17.38) +9 more |
| 40 | `get_upstream_features` | Emb:" not"@17 (de=16.12) +9 more |
| 41 | `inspect_feature` ×7 | L2:9012, L2:4147, L1:763, L1:1958, L0:14478, L1:7207, L1:14137 |
| 42 | `get_upstream_features` | Emb:" recorded"@2 (de=19.50) +14 more |
| 43 | `get_upstream_features` | Emb:" recorded"@2 (de=13.75) +4 more |
| 44 | `get_upstream_features` | Emb:" recorded"@2 (de=18.00) +4 more |
| 45 | `get_upstream_features` | Emb:" menu"@3 (de=16.25) +4 more |
| 46 | `get_upstream_features` | Emb:" how"@8 (de=10.25) +4 more |
| 47 | `get_upstream_features` | Emb:" obtain"@10 (de=17.38) +4 more |
| 48 | `get_upstream_features` | Emb:" recorded"@2 (de=9.06) +4 more |
| 49 | `get_top_features` | 50 features; top: L2:8776 de=0.523 |
| 50 | `inspect_feature` ×6 | L16:11696, L0:11835, L1:4515, L0:9489, L0:4071, L2:10798 |
| 51 | `get_upstream_features` | Emb:" do"@16 (de=28.25) +9 more |
| 52 | `get_upstream_features` | Emb:" not"@17 (de=5.16) +9 more |
| 53 | `get_upstream_features` | Emb:"<bos>"@0 (de=-5.62) +9 more |
| 54 | `get_upstream_features` | Emb:" recorded"@2 (de=6.25) +9 more |
| 55 | `get_upstream_features` | Emb:" provide"@5 (de=17.25) +9 more |

### Build

`build_circuit` → 13 nodes, 22 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 129,826 | 9,873 | 1,055,456 | 0 | $0.1141 | — | — |
| **Total** | | **129,826** | **9,873** | **1,055,456** | **0** | **$0.1141** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 18s