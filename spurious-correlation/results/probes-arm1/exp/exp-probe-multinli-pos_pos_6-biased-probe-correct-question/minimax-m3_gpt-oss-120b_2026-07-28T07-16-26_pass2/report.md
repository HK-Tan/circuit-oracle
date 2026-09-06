# Circuit Oracle Report
**Date:** 2026-07-28 07:16:26 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_6 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction classification is driven almost entirely by superficial "not / negation word" features at every layer, with a small contribution from the "set about" phrase detectors — the model has not extracted any contradiction-specific semantic content from the prompt.

**Confidence:** 8/10

**Reasoning:** The circuit strongly confirms the user's concern. The single most influential path is a tower of negation detectors stacked on top of the **emb " not" (pos 21)** token:

- **L0 not-token supernode (L0:F4958, L0:F15454, L0:F9646, all at pos 21, direct_effect ≈ +0.78 on the top of the graph)** fires directly on the literal " not" embedding (direct_effect from the token itself ≈ +33 to +42 across multiple downstream features). These are generic "not"-as-token detectors (frac_nonzero 0.0034–0.022), not contradiction detectors.
- **L2 negation supernode (L2:F12021 "not/negative terms", L2:F6993 "uncertainty", L2:F4544 "not/contractions")** at pos 21 builds on the L0 features and the " not" embedding. L2:F12021 alone gets direct_effect +0.26.
- **L3 negation supernode (L3:F8011 code-mix-negation, L3:F1101 "absence/negation in software", L3:F8733 word fragments, L3:F6227 sentence fragments, L3:F13138 legal-document words, L3:F3797 "So/Okay")** — note F1101 (which sounds negation-related) actually pushes *against* the target (direct_effect −0.34), and F8011 pushes *for* it (+0.34). L3 is the noisiest layer; features with a generic "negation-adjacent" or "error/discourse marker" character all get non-trivial direct_effect, but none of them carry NLI-specific meaning.
- **L4 cross-lingual negation (L4:F4492 "negations in various languages", L4:F2422 "negations in French/Malay/Croatian")** at pos 21 — direct_effect +0.31 / −0.21. These are language-detector features for the word "not" in non-English languages, with frac_nonzero 0.04. The French/Malay detectors contribute negative direct_effect, partially cancelling the English "not" signal, but the L4 supernode's net effect on the probe is still significant.
- **L13 negation-advanced (L13:F3295 "is/are not", L13:F14177 "not + am/other verbs")** at pos 21, direct_effect ≈ +0.34. Both are generic negation patterns in legal/scientific text, not contradiction.
- **L15 phrase detector (L15:F2080 "set followed by articles/prepositions", L15:F10071 "negations and equivocations")** at pos 3/11/21. F2080 fires on "set about" and "setting" — it contributes +0.20 because "set about" appears in the premise, but the label is the phrase "set …", not contradiction content. F10071 is again a generic negation feature (frac_nonzero 0.013).
- **L16 terminal feature (L16:F12358, "not followed within a few tokens by a form of 'to be'", direct_effect +0.34)** is the highest-magnitude non-embedding contributor, but it is a local "not + be" pattern detector — it fires whenever the model sees the sequence "not … is/was/were", which trivially happens in this NLI premise. frac_nonzero is 0.028.

Embedding-level inspection confirms that almost every important downstream feature is fed primarily by the **emb " not" (pos 21)** token (direct_effect 13.7 → 23 → 33 across layers) and the **emb " were" (pos 20)** token (direct_effect 3.7 → 14). The premise's " not" is the single dominant cause; downstream features progressively refine this into "not + be-form" patterns but never reach NLI-semantic content.

What is **missing** from the circuit is more striking than what is present: there is no feature for "permission denied" semantics, no "rule" vs. "action" comparison feature, no world-knowledge or entity-relation feature tying "they cleared land" to "they were not allowed to deforest." The premise's content-bearing words ("clearing", "agriculture", "setting fire", "massive tracts of forest", "deforest") contribute only generic L1-L2 lexical features (L1:F8332 "clear", L1:F361 "agriculture/ecology", L2:F2952 "out", L2:F4819 "fire") and these are mostly washed out by 5+ downstream negation features that the probe picks up. The probe is essentially counting negation cues, exactly as the user suspected.

The user's worry is well-founded: this probe is exploiting the spurious surface correlation between "not …" patterns and contradiction labels rather than any genuine NLI inference. A robust probe would need to track entailment relation structure, which is absent here.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 21 | Word 'not' detectors |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F15454](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15454) | 21 | Word 'not' detectors |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15454) |
| [L0:F9646](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9646) | 21 | Word 'not' detectors |  words that indicate the degree, scale, or validity of something | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9646) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 6 | Function-word detectors (the/to/they/about/clearing) | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 13 | Function-word detectors (the/to/they/about/clearing) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F3498](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) | 2 | Function-word detectors (the/to/they/about/clearing) |  the pronoun "they" or its possessive form. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 4 | Function-word detectors (the/to/they/about/clearing) |  the word "about" when followed by a numerical value | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L0:F12492](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12492) | 7 | Word 'debt' detector (off-topic) |  the word "debt" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12492) |
| [L0:F2506](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2506) | 12 | Word 'debt' detector (off-topic) |  the word "free" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2506) |
| [L0:F9161](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9161) | 1 | Word 'debt' detector (off-topic) |  the word "nice" and potentially related phrases like "food courts" and "single domain" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9161) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 18 | Word 'debt' detector (off-topic) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L1:F8332](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8332) | 5 | Word 'clear' detector | the word "clear" or "clearance" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8332) |
| [L1:F361](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/361) | 9 | Word 'clear' detector |  words related to agriculture and ecology | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/361) |
| [L1:F12068](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12068) | 1 | Word 'clear' detector |  words and phrases related to space, astronomy, and science in general. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12068) |
| [L2:F2952](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2952) | 4 | Words 'set/out/fire' detectors |  the word "out", and sometimes activates on words relating to legal cases | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2952) |
| [L2:F4819](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4819) | 12 | Words 'set/out/fire' detectors | sentences containing the word "fire" or similar terms | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4819) |
| [L2:F12021](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) | 21 | Negation-word detectors (early-mid layer) | "not" or negative terms, with some bonus for sports-related terms and "purpose". | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) |
| [L2:F6993](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6993) | 21 | Negation-word detectors (early-mid layer) | phrases describing uncertainty or difficulty | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6993) |
| [L2:F4544](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4544) | 21 | Negation-word detectors (early-mid layer) | the word "not" or contractions including "not" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4544) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 21 | Mid-layer negation/error/word-fragment detectors |  a mix of words and code fragments from different languages | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L3:F1101](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) | 21 | Mid-layer negation/error/word-fragment detectors |  error messages and terms indicating absence or negation in software contexts. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) |
| [L3:F8733](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8733) | 4 | Mid-layer negation/error/word-fragment detectors |  parts of words like "ch", "parms", "ened", and "ounesto" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8733) |
| [L3:F6227](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) | 23 | Mid-layer negation/error/word-fragment detectors |  sentence fragments and informal or ungrammatical language, often including abbreviations. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) |
| [L3:F13138](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13138) | 4 | Mid-layer negation/error/word-fragment detectors |  words and phrases related to legal proceedings or documents. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13138) |
| [L3:F3797](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3797) | 1 | Mid-layer negation/error/word-fragment detectors | comments starting with "So" or "Okay". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3797) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 21 | Cross-lingual negation / not-be detectors | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 21 | Cross-lingual negation / not-be detectors | negations in other languages like French, Malay, and Croatian | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L4:F7140](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7140) | 1 | Cross-lingual negation / not-be detectors | the word "so" at the beginning of a sentence or phrase | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7140) |
| [L4:F12225](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12225) | 2 | Cross-lingual negation / not-be detectors |  transitional conclusion words, often used in legal or academic writing | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12225) |
| [L4:F15596](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15596) | 1 | Cross-lingual negation / not-be detectors |  the word "So" possibly acting as a discourse marker, along with other words that frequently occur near it. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15596) |
| [L8:F8406](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) | 1 | First-person 'I' / 'Exactly' detector | the first-person pronoun "I" and the word "Exactly" | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) |
| [L13:F3295](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) | 21 | Negation 'is/are not' / dissent | negations in the form of "is/are not" as well as other uses of "not" | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) |
| [L13:F14177](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/14177) | 21 | Negation 'is/are not' / dissent | negation or dissent, often using "not" with "am" or other verbs | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/14177) |
| [L15:F2080](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2080) | 3 | Phrase 'set about/setting' detectors | the phrase "set" followed by articles or prepositions | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2080) |
| [L15:F2080](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2080) | 11 | Phrase 'set about/setting' detectors | the phrase "set" followed by articles or prepositions | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2080) |
| [L15:F10071](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) | 21 | Phrase 'set about/setting' detectors | negations and equivocations | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) |
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 21 | "not" + be-form detector |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:3498 de=-0.785 |
| 3 | `get_top_features` | 30 features; top: L0:3498 de=-0.785 |
| 4 | `inspect_feature` ×28 | L0:3498, L16:12358, L3:1101, L3:8011, L4:4492, L0:2238, L2:2952, L2:4819, L0:3820, L0:8444, L4:2422, L15:2080, L1:8332, L3:8733, L3:6227, L0:4958, L3:13138, L3:3797, L1:361, L0:12492, L8:8406, L4:7140, L4:12225, L0:2506, L0:9161, L4:15596, L0:6051, L1:12068 |
| 5 | `get_upstream_features` | Emb:" not"@21 (de=19.00) +14 more |
| 6 | `get_upstream_features` | Emb:" not"@21 (de=21.75) +14 more |
| 7 | `get_upstream_features` | Emb:" not"@21 (de=19.12) +14 more |
| 8 | `get_upstream_features` | Emb:" fire"@12 (de=32.00) +14 more |
| 9 | `get_upstream_features` | Emb:" set"@3 (de=13.50) +14 more |
| 10 | `get_upstream_features` | Emb:" set"@3 (de=44.50) +14 more |
| 11 | `inspect_feature` ×14 | L15:10071, L13:3295, L13:14177, L2:12021, L0:9646, L0:15454, L3:1101, L2:6993, L0:12414, L3:9803, L3:6374, L2:4544, L14:8363, L6:1468 |
| 12 | `get_upstream_features` | Emb:" not"@21 (de=23.12) +14 more |
| 13 | `get_upstream_features` | Emb:" not"@21 (de=13.69) +14 more |
| 14 | `get_upstream_features` | Emb:" were"@20 (de=14.00) +9 more |
| 15 | `get_upstream_features` | Emb:" not"@21 (de=7.72) +9 more |
| 16 | `get_upstream_features` | Emb:" they"@2 (de=42.75) +9 more |
| 17 | `get_upstream_features` | Emb:" about"@4 (de=35.00) +9 more |
| 18 | `get_upstream_features` | Emb:" agriculture"@9 (de=14.31) +9 more |
| 19 | `get_upstream_features` | Emb:" the"@6 (de=34.25) +9 more |
| 20 | `get_upstream_features` | Emb:" to"@13 (de=41.00) +9 more |
| 21 | `get_upstream_features` | Emb:" not"@21 (de=13.69) +9 more |
| 22 | `get_upstream_features` | Emb:" they"@2 (de=12.75) +9 more |
| 23 | `get_upstream_features` | Emb:" clearing"@5 (de=21.12) +9 more |
| 24 | `get_upstream_features` | Emb:" not"@21 (de=33.75) +9 more |
| 25 | `get_upstream_features` | Emb:" not"@21 (de=13.69) +9 more |
| 26 | `get_upstream_features` | Emb:" not"@21 (de=13.69) +9 more |
| 27 | `get_upstream_features` | ❌ Feature (layer=0, feature_idx=4958) not found at pos=19. Thi |
| 28 | `get_upstream_features` | Emb:" set"@3 (de=13.50) +9 more |
| 29 | `get_upstream_features` | Emb:" set"@3 (de=13.50) +9 more |
| 30 | `get_upstream_features` | Emb:" not"@21 (de=17.50) +9 more |
| 31 | `get_upstream_features` | Emb:" set"@3 (de=7.12) +9 more |
| 32 | `get_upstream_features` | Emb:" to"@23 (de=6.75) +9 more |
| 33 | `get_upstream_features` | Emb:" not"@21 (de=19.12) +9 more |
| 34 | `get_upstream_features` | Emb:" setting"@11 (de=45.75) +9 more |

### Build

`build_circuit` → 24 nodes, 47 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 98,874 | 8,757 | 364,088 | 0 | $0.0620 | — | — |
| **Total** | | **98,874** | **8,757** | **364,088** | **0** | **$0.0620** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 8s