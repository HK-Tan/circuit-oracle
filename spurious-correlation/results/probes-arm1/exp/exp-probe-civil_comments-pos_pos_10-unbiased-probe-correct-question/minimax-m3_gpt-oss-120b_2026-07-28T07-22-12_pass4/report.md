# Circuit Oracle Report
**Date:** 2026-07-28 07:22:12 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_10 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a circuit that, in support of the user's concern, relies heavily on identity-group vocabulary tokens (primarily "race" at pos 5 and "not" at pos 2) and a generic "mentioning/discourse" feature, rather than on features that encode the actual semantic toxicity of the prompt.

**Confidence:** 7

**Reasoning:** Tracing from the top probe-driving features, the circuit is remarkably shallow and lexical. The strongest positive contributions come from L0:F10682 ("the word 'race'", direct_effect +0.146), L0:F14813 ("mentions of race, racial issues, or racism", direct_effect −0.106 — note negative), L4:F15173 ("statements about mentioning or discussing something", direct_effect +0.135), L3:F12410 ("the word 'By' at the start of a phrase", direct_effect +0.129), and L2:F11639 ("the word 'mention'", direct_effect +0.112). All of these are essentially token-identity detectors, not semantic-toxicity detectors: they activate on the surface strings "race", "mention"/"mentioning", "By", and the negation "not" (L0:F4958 with direct_effect −0.227, L0:F15267 "not" detector, L0:F2317 "uncertainty words" like "not"/"far"/"linear" at pos 3). When traced upstream, L4:F15173's dominant input is the embedding of the token "mentioning" itself (direct_effect 17.5), with secondary contributions from L3:F6517 ("words related to mentioning something", frac_nonzero 0.0056), L1:F5477 (another "mention" detector), and embedding nodes for "not" and "By". L0:F10682 ("race") receives direct_effect 22.6 from the "race" embedding at pos 5. The only feature that comes close to encoding identity-discrimination semantics is L6:F9228 ("language regarding discrimination based on race, gender, religion, and disability", direct_effect −0.093) — but it has frac_nonzero 0.597, meaning it fires on roughly 60% of all tokens, so it is a generic sentence-level feature rather than a specific toxicity detector, and its effect is inhibitory here. The L4 "mentioning-act" features (F15173, F2668 "realizations coupled with acknowledgement") are also generic discourse-marker features. Crucially, the circuit contains NO feature encoding the actual hateful framing (the "bad cops are white" generalization), NO toxic-slur or hostile-stereotype feature, and NO higher-layer (L10+) semantic-abstraction features — the deepest features are at L6. The user's concern is confirmed: the probe is essentially reading off the co-occurrence of identity-group vocabulary ("race") with discourse markers ("mentioning", "not", "By") rather than parsing the actual toxic content. The "not mentioning" phrase — which in context is a meta-discussion about race-mention omissions in media — triggers the same identity-token detectors as a genuinely hateful racial statement would, demonstrating the spurious-correlation problem.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: race (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: mentioning (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: not (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: By (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F10682](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10682) | 5 | L0 word 'race' detector |  the word "race" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10682) |
| [L0:F14813](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14813) | 5 | L0 race/racial issues context |  mentions of race, racial issues, or racism | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14813) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 2 | L0 word 'not' detector |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F15267](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15267) | 2 | L0 word 'not' detector |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15267) |
| [L0:F2317](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2317) | 3 | L0 word 'not' detector |  words or phrases expressing uncertainty or doubt | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2317) |
| [L3:F12410](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12410) | 1 | L0 'By' at sentence start | the word "By" at the start of a phrase or sentence | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12410) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 4 | L0 'the' function word | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F1903](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1903) | 1 | L0 'the' function word | instances of sentences starting with "The" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1903) |
| [L1:F5477](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5477) | 3 | L1-L2 'mention' word detectors |  instances of the word "mention" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5477) |
| [L2:F11639](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11639) | 3 | L1-L2 'mention' word detectors | the word "mention" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11639) |
| [L2:F6539](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6539) | 3 | L1-L2 'mention' word detectors | the word "mention" and words or phrases related to opinions or significance, as well as the word "matter." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6539) |
| [L2:F10509](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10509) | 5 | L1-L2 'mention' word detectors |  the word "race." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10509) |
| [L2:F2713](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2713) | 2 | L1-L2 'mention' word detectors |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2713) |
| [L3:F6517](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6517) | 3 | L3 'mentioning' discourse features |  words related to mentioning something | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6517) |
| [L3:F11194](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11194) | 3 | L3 'mentioning' discourse features |  words related to stating or communicating information | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11194) |
| [L3:F5475](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5475) | 5 | L3 'mentioning' discourse features |  occurrences of the word "race" in different contexts | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5475) |
| [L3:F672](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/672) | 10 | L3 'mentioning' discourse features |  the word "question" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/672) |
| [L4:F15173](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15173) | 3 | L4 'mentioning' statement act |  statements about mentioning or discussing something | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15173) |
| [L4:F2668](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2668) | 3 | L4 'mentioning' statement act |  instances of realizations coupled with acknowledgement or acknowledgment of something. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2668) |
| [L6:F9228](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9228) | 6 | L6 discrimination language feature |  language regarding discrimination based on race, gender, religion, and disability | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9228) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:4958 de=-0.227 |
| 3 | `inspect_feature` ×6 | L0:4958, L2:10509, L0:10682, L4:15173, L3:12410, L2:11639 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F15173@3` | ❌ error | — | — | Trace the path from L4:F15173 at pos 3 ("mention" / "mentioning" statements). Th… |
| SA-2 | `L0:F10682@5` | ❌ error | — | — | Trace the path from L0:F10682 at pos 5 ("race" word feature, positive direct eff… |
| SA-3 | `L0:F4958@2` | ❌ error | — | — | Trace the path from L0:F4958 at pos 2 ("not" word feature, negative direct effec… |
| SA-4 | `L2:F10509@5` | ❌ error | — | — | Trace the path from L2:F10509 at pos 5 ("race" word feature, negative direct eff… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F15173@3, k=10 → Emb:" mentioning"@3 (de=17.50) +9 more |
| 2 | `get_upstream_features` | L0:F10682@5, k=10 → Emb:" race"@5 (de=22.62) +9 more |
| 3 | `get_upstream_features` | L2:F10509@5, k=10 → Emb:" race"@5 (de=30.12) +9 more |
| 4 | `get_upstream_features` | L3:F12410@1, k=10 → Emb:"By"@1 (de=48.75) +9 more |
| 5 | `inspect_feature` ×16 | L3:6517, L1:5477, L3:11194, L3:672, L0:3820, L0:1903, L0:14813, L3:5475, L0:819, L6:9228, L2:2713, L4:573, L4:2668, L0:2317, L0:15267, L2:6539 |
| 6 | `get_upstream_features` | L2:F11639@3, k=8 → Emb:" mentioning"@3 (de=27.25) +7 more |
| 7 | `get_upstream_features` | L0:F14813@5, k=8 → Emb:" race"@5 (de=17.00) +7 more |

### Build

`build_circuit` → 14 nodes, 22 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 56,240 | 5,529 | 170,060 | 0 | $0.0337 | — | — |
| **Total** | | **56,240** | **5,529** | **170,060** | **0** | **$0.0337** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 29s