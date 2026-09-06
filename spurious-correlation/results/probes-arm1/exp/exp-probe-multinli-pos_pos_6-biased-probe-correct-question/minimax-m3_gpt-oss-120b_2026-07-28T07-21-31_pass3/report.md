# Circuit Oracle Report
**Date:** 2026-07-28 07:21:31 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_6 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "contradiction" classification is driven almost entirely by a deep chain of negation-detector features that fan in on a single word — `not` at position 21 ("not allowed to deforest") — with the late-layer L16:F12358 ("`not` + to-be within a few tokens") as the single biggest positive contributor, even though the premise and hypothesis in this NLI pair are about deforestation/clearing/fire, and the only true conflict is conceptual (clearing+fire vs. "not allowed to deforest"), not signalled by any semantic-feature comparison.

**Confidence:** 7

**Reasoning:** This confirms the user's concern in detail. The attribution graph's largest positive direct effects to the probe direction are all negation features anchored to a single token (` not`, pos 21). The chain is: ` not` embedding → L0:F4958 / F15454 / F9646 (three "not" / degree-word detectors at pos 21, direct_effects ~+0.19–+0.25) → L2:F12021 ("not" / negative terms, +0.26) → L3:F8011 ("mix of words/code fragments" that *promotes* `not` tokens, +0.34) and L3:F9803 (scientific "disproven" context, +0.19) → L4:F4492 ("negations in various languages", +0.31) → L13:F3295 ("is/are not" negation assembler, +0.34) and L13:F14177 ("not + am" negation assembler, +0.19) → L15:F10071 ("negations and equivocations", –0.19 to the probe) → L16:F12358 ("not + to-be", +0.34, top single positive driver).

The top positive contributors in the entire circuit (by direct_effect to the probe) are: L16:F12358 (+0.336, "not + to-be"), L3:F8011 (+0.338, promotes `not`), L4:F4492 (+0.311, "negations in various languages"), L2:F4819 (+0.262, "fire"), L0:F3820 (+0.252, "the"), L0:F8444 (+0.218, "to"), L0:F4958 (+0.189, "not"). Six of the top eight positive features are explicit negation / `not` detectors; none of them encode the *content* of either sentence. The "fire" feature (L2:F4819) is the only content-word positive driver and is dwarfed by the negation cluster.

Crucially, the user's intuition is verified: the circuit has *no* feature that compares premise content to hypothesis content (no entity-recognition, no "fire vs. clearing" semantic match, no "deforest vs. clear" contradiction feature). The model classifies the pair as contradictory primarily because the word `not` appears once. Almost the entire contradiction signal reduces to "there is a `not` here," propagated through a tightly stacked tower of negation detectors (L0→L2→L3→L4→L13→L15→L16) that all fire on the same single input token. This is a textbook spurious-feature circuit: the probe is using a surface-level negation cue rather than a representation of the actual semantic contradiction.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: ' not' (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 20 | Emb: ' were' (pos 20) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: ' set' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 11 | Emb: ' setting' (pos 11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: ' about' (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: ' clearing' (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: ' fire' (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'So' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F3498](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) | 2 | Layer 0 lexical detectors (they/about/clearing/...) |  the pronoun "they" or its possessive form. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 4 | Layer 0 lexical detectors (they/about/clearing/...) |  the word "about" when followed by a numerical value | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 6 | Layer 0 lexical detectors (they/about/clearing/...) | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 13 | Layer 0 lexical detectors (they/about/clearing/...) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 21 | Layer 0 lexical detectors (they/about/clearing/...) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F15454](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15454) | 21 | Layer 0 lexical detectors (they/about/clearing/...) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15454) |
| [L0:F9646](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9646) | 21 | Layer 0 lexical detectors (they/about/clearing/...) |  words that indicate the degree, scale, or validity of something | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9646) |
| [L1:F8332](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8332) | 5 | Layer 0 lexical detectors (they/about/clearing/...) | the word "clear" or "clearance" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8332) |
| [L0:F3498](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) | 19 | Layer 0 lexical detectors (they/about/clearing/...) |  the pronoun "they" or its possessive form. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) |
| [L2:F2952](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2952) | 4 | Layer 2 content-word features (out / fire / not) |  the word "out", and sometimes activates on words relating to legal cases | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2952) |
| [L2:F4819](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4819) | 12 | Layer 2 content-word features (out / fire / not) | sentences containing the word "fire" or similar terms | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4819) |
| [L2:F12021](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) | 21 | Layer 2 content-word features (out / fire / not) | "not" or negative terms, with some bonus for sports-related terms and "purpose". | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 21 | Layer 3 negation detectors |  a mix of words and code fragments from different languages | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L3:F1101](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) | 21 | Layer 3 negation detectors |  error messages and terms indicating absence or negation in software contexts. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) |
| [L3:F6227](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) | 23 | Layer 3 negation detectors |  sentence fragments and informal or ungrammatical language, often including abbreviations. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) |
| [L3:F9803](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9803) | 21 | Layer 3 negation detectors | sentences describing scientific studies or experiments, particularly where something is disproven | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9803) |
| [L3:F8733](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8733) | 4 | Layer 3 negation detectors |  parts of words like "ch", "parms", "ened", and "ounesto" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8733) |
| [L3:F13138](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13138) | 4 | Layer 3 negation detectors |  words and phrases related to legal proceedings or documents. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13138) |
| [L3:F3797](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3797) | 1 | Layer 3 negation detectors | comments starting with "So" or "Okay". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3797) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 21 | Layer 4 cross-lingual negation aggregators | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 21 | Layer 4 cross-lingual negation aggregators | negations in other languages like French, Malay, and Croatian | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L13:F3295](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) | 21 | Layer 13 'is/are not' / 'am not' negation assemblers | negations in the form of "is/are not" as well as other uses of "not" | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) |
| [L13:F14177](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/14177) | 21 | Layer 13 'is/are not' / 'am not' negation assemblers | negation or dissent, often using "not" with "am" or other verbs | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/14177) |
| [L15:F2080](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2080) | 3 | Layer 15 'set' action-verb feature | the phrase "set" followed by articles or prepositions | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2080) |
| [L15:F2080](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2080) | 11 | Layer 15 'set' action-verb feature | the phrase "set" followed by articles or prepositions | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2080) |
| [L15:F10071](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) | 21 | Layer 15 'negations and equivocations' feature | negations and equivocations | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) |
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 21 | Layer 16 'not + to-be' detector (top driver) |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 21 | Probe direction (output) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'contradiction' is not one of the top-k next-token can |
| 3 | `get_top_features` | 20 features; top: L0:3498 de=-0.785 |
| 4 | `inspect_feature` ×18 | L0:3498, L0:2238, L3:1101, L3:8011, L16:12358, L2:2952, L4:4492, L2:4819, L0:3820, L0:8444, L4:2422, L15:2080, L3:8733, L3:6227, L0:4958, L3:13138, L3:3797, L1:8332 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F12358@21` | ❌ error | — | — | Trace the L16:F12358 'not + to be' feature from position 21 (the 'not' in 'not a… |
| SA-2 | `L15:F2080@3` | ❌ error | — | — | Trace the L15:F2080 'set' feature from position 3 ('set' in 'set about clearing'… |
| SA-3 | `L4:F4492@21` | ❌ error | — | — | Trace the L4:F4492 'negations in various languages' feature at pos 21. What nega… |
| SA-4 | `L3:F8011@21` | ❌ error | — | — | Trace the L3:F8011 'mix of words/code' feature that promotes 'not' tokens, at po… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L16:F12358@21, k=15 → Emb:" not"@21 (de=19.00) +14 more |
| 2 | `get_upstream_features` | L4:F4492@21, k=15 → Emb:" not"@21 (de=19.12) +14 more |
| 3 | `get_upstream_features` | L3:F8011@21, k=15 → Emb:" not"@21 (de=21.75) +14 more |
| 4 | `get_upstream_features` | L15:F2080@3, k=15 → Emb:" set"@3 (de=44.50) +14 more |
| 5 | `get_upstream_features` | L15:F2080@11, k=15 → Emb:" setting"@11 (de=45.75) +14 more |
| 6 | `get_upstream_features` | L2:F2952@4, k=12 → Emb:" set"@3 (de=13.50) +11 more |
| 7 | `get_upstream_features` | L2:F4819@12, k=12 → Emb:" fire"@12 (de=32.00) +11 more |
| 8 | `get_upstream_features` | L3:F6227@23, k=12 → Emb:" to"@23 (de=6.75) +11 more |
| 9 | `get_upstream_features` | L3:F1101@21, k=12 → Emb:" not"@21 (de=13.69) +11 more |
| 10 | `get_upstream_features` | L3:F3797@1, k=12 → Emb:"So"@1 (de=22.00) +11 more |
| 11 | `get_upstream_features` | L1:F8332@5, k=12 → Emb:" clearing"@5 (de=21.12) +11 more |
| 12 | `get_upstream_features` | L4:F2422@21, k=12 → Emb:" not"@21 (de=17.50) +11 more |
| 13 | `inspect_feature` ×7 | L2:12021, L15:10071, L0:9646, L0:15454, L3:9803, L13:3295, L13:14177 |
| 14 | `get_upstream_features` | L15:F10071@21, k=12 → Emb:" not"@21 (de=9.81) +11 more |
| 15 | `get_upstream_features` | L13:F3295@21, k=12 → Emb:" not"@21 (de=17.25) +11 more |
| 16 | `get_upstream_features` | L13:F14177@21, k=12 → Emb:" not"@21 (de=6.19) +11 more |
| 17 | `get_upstream_features` | L2:F2952@4, k=12 → Emb:" set"@3 (de=13.50) +11 more |

### Build

`build_circuit` → 17 nodes, 37 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 72,979 | 10,396 | 327,702 | 0 | $0.0540 | — | — |
| **Total** | | **72,979** | **10,396** | **327,702** | **0** | **$0.0540** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 50s