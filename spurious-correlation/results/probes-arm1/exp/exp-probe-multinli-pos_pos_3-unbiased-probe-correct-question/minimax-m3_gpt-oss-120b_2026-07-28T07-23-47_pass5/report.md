# Circuit Oracle Report
**Date:** 2026-07-28 07:23:47 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** This probe is driven primarily by shallow lexical/syntactic cues (a mix of function-word features like "with", "from", "together", "itself", "any" and entity-name features like "castle", "tower", "house", "century") rather than deep semantic understanding of the premise-hypothesis contradiction — but the user's concern about "negation words" as a spurious shortcut is only partially borne out: the negation/hypothesis token "any" (pos 38) is a real but small contributor.

**Confidence:** 6

**Reasoning:** The top direct drivers of the probe are L4:F13244 ("terms related to land ownership and administration", +0.29 on the "castle" token at pos 2), L2:F1430 ("U.S. White House or generic house", −0.22 on "house" at pos 14), and L0:F2158 ("the word 'with'", +0.19 on "with" at pos 17). Crucially, all of these are *very* shallow: a top-feature direct_effect of ~0.29 from a layer-4 feature is tiny, and the bulk of the next 20 features are layer-0/1/2 single-word detectors. Tracing upstream confirms each late driver bottoms out at an *embedding node* for a single input token — there is essentially no multi-hop semantic composition. The circuit decomposes into three supernodes:

1. **Premise entity/structure supernode (L0–L4)**: L0:F5494 "early" (pos 6, +0.15), L0:F4367 "century" (pos 12, −0.12), L0:F1027 L1 "tower" (pos 13, +0.16), L0:F9604 "house" (pos 14), L0:F4079 "exposure/tower" (pos 13), L2:F4429 "beginning of a period" (pos 6, +0.14, fed by Emb:" early" with direct_effect 35.25), L1:F11220 "restore" (pos 16, −0.15), and L4:F5749 "ancient settlements/fortifications" (pos 2). These are pure lexical "castle-architecture" detectors.

2. **Function-word supernode (L0)**: F2158 "with" (pos 17, +0.19, fed by Emb:" with" de=33.75), F8974 "from" (pos 20, −0.12, fed by Emb:" from" de=39.75), F7360 "an" (pos 5, +0.16), F7513 "together" (pos 26, +0.13, fed by Emb:" together" de=43.0), F8082 "itself" (pos 3, −0.11), and F14108 "appropriate" (pos 2, −0.14). Each of these is a one-token, one-feature path. They carry genuinely "spurious" information — the probe is using generic function-word frequencies, not their role in the meaning.

3. **Negation-scope supernode (L0)**: F10815 "any" (pos 38, +0.12), with Emb:" any" de=40.5, and Emb:" not" de=3.2, Emb:" does" de=0.5. This *is* a small negation signal, but it is only one of ~20 roughly equal-magnitude features and its direct_effect (+0.12) is dwarfed by the lexical content features.

The top L8 feature F8406 ("the pronoun 'I'") is an *inhibitory* contributor (−0.11) and traces back to BOS, not a content word.

Overall the user's concern is correct in spirit but over-stated: the probe is *not* principally a "negation detector" — the contradiction score is built from a bag of shallow lexical features (mostly premise-side "castle-architecture" vocabulary plus bag of function words), and the hypothesis "does not… any" is just one of many small contributors. A probe that fires on the word "any" in the hypothesis is unreliable for the same reason a probe that fires on "with" in the premise is unreliable: neither reflects entailment reasoning, both reflect surface-form shortcuts.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F13244](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) | 2 | Late-layer contradiction drivers (entity/structural features) |  terms related to land ownership and administration, possibly including slavery or other forms of forced labor | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) |
| [L6:F486](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/486) | 14 | Late-layer contradiction drivers (entity/structural features) |  Scottish locations and political terms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/486) |
| [L2:F1430](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1430) | 14 | Late-layer contradiction drivers (entity/structural features) | mentions of the U.S. White House or a generic house | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1430) |
| [L2:F4429](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) | 6 | Premise entity/structure features (castle, tower, house, century) |  mentions of the beginning of a period | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) |
| [L1:F1027](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1027) | 13 | Premise entity/structure features (castle, tower, house, century) | the word "tower" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1027) |
| [L1:F11220](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11220) | 16 | Premise entity/structure features (castle, tower, house, century) | instances of the word "restore" and related words | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11220) |
| [L0:F5494](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5494) | 6 | Premise entity/structure features (castle, tower, house, century) | the word "early" often related to time | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5494) |
| [L0:F4367](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4367) | 12 | Premise entity/structure features (castle, tower, house, century) |  references to centuries | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4367) |
| [L0:F9604](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9604) | 14 | Premise entity/structure features (castle, tower, house, century) |  the word "house" along with words about social class/gatherings | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9604) |
| [L0:F4079](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4079) | 13 | Premise entity/structure features (castle, tower, house, century) |  the words "exposure," "tower" and words related to legal trials | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4079) |
| [L4:F5749](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) | 2 | Premise entity/structure features (castle, tower, house, century) |  terms that describe ancient settlements and fortifications | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) |
| [L0:F2158](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) | 17 | Function-word features (with, from, an, together, itself, appropriate) | the word "with" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) |
| [L0:F8974](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) | 20 | Function-word features (with, from, an, together, itself, appropriate) | the word "from" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) |
| [L0:F7360](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7360) | 5 | Function-word features (with, from, an, together, itself, appropriate) | the word "an" and sometimes also the acronym COX | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7360) |
| [L0:F7513](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7513) | 26 | Function-word features (with, from, an, together, itself, appropriate) | the word "together" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7513) |
| [L0:F8082](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8082) | 3 | Function-word features (with, from, an, together, itself, appropriate) | the word "itself" and sometimes words ending in "ing" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8082) |
| [L0:F14108](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14108) | 2 | Function-word features (with, from, an, together, itself, appropriate) | the word "appropriate" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14108) |
| [L0:F10815](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10815) | 38 | Hypothesis negation-scope features (does, not, any) |  the word "any". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10815) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:13244 de=0.287 |
| 3 | `inspect_feature` ×12 | L4:13244, L0:2158, L0:7360, L1:1027, L0:5494, L2:4429, L0:7513, L2:1430, L1:11220, L0:14108, L6:486, L0:8974 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F13244@2` | ❌ error | — | — | Trace the path from L4:F13244 (terms related to land ownership/property) - what … |
| SA-2 | `L0:F2158@17` | ❌ error | — | — | Trace the word "with" feature (L0:F2158) - what input token position 17 represen… |
| SA-3 | `L1:F1027@13` | ❌ error | — | — | Trace the word "tower" feature (L1:F1027) - what position 13 represents in the i… |
| SA-4 | `L2:F4429@6` | ❌ error | — | — | Trace "early period" feature L2:F4429 at position 6 - what tokens drive this and… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F13244@2, k=15 → Emb:" castle"@2 (de=18.50) +14 more |
| 2 | `get_upstream_features` | L2:F4429@6, k=15 → Emb:" early"@6 (de=35.25) +14 more |
| 3 | `get_upstream_features` | L1:F1027@13, k=15 → Emb:" tower"@13 (de=23.12) +14 more |
| 4 | `get_upstream_features` | L6:F486@14, k=15 → L5:F3316 (de=-2.38) +14 more |
| 5 | `inspect_feature` ×3 | L0:9604, L0:4079, L4:5749 |
| 6 | `get_upstream_features` | L0:F2158@17, k=10 → Emb:" with"@17 (de=33.75) +9 more |
| 7 | `get_upstream_features` | L0:F5494@6, k=10 → Emb:" early"@6 (de=21.12) +9 more |
| 8 | `get_upstream_features` | L0:F7513@26, k=10 → Emb:" together"@26 (de=43.00) +9 more |
| 9 | `get_upstream_features` | L2:F1430@14, k=10 → Emb:" house"@14 (de=30.88) +9 more |
| 10 | `get_upstream_features` | L3:F10598@3, k=10 → Emb:" itself"@3 (de=30.12) +9 more |
| 11 | `get_upstream_features` | L0:F7513@26, k=10 → Emb:" together"@26 (de=43.00) +9 more |
| 12 | `get_upstream_features` | L1:F11220@16, k=10 → Emb:" restored"@16 (de=20.00) +9 more |
| 13 | `get_upstream_features` | L0:F8974@20, k=10 → Emb:" from"@20 (de=39.75) +9 more |
| 14 | `get_upstream_features` | L0:F4367@12, k=10 → Emb:"century"@12 (de=23.12) +9 more |
| 15 | `get_upstream_features` | L0:F10815@38, k=10 → Emb:" any"@38 (de=40.50) +9 more |
| 16 | `get_upstream_features` | L0:F14108@2, k=10 → Emb:" castle"@2 (de=11.81) +9 more |
| 17 | `get_upstream_features` | L0:F8082@3, k=10 → Emb:" itself"@3 (de=19.88) +9 more |
| 18 | `get_upstream_features` | L8:F8406@1, k=10 → Emb:"<bos>"@0 (de=9.50) +9 more |
| 19 | `inspect_feature` ×5 | L8:8406, L0:10815, L0:4367, L0:8974, L3:10598 |
| 20 | `get_upstream_features` | L8:F8406@1, k=8 → Emb:"<bos>"@0 (de=9.50) +7 more |
| 21 | `get_top_features` | token="", k=10 → 10 features; top: L4:13244 de=0.287 |
| 22 | `inspect_feature` ×2 | L0:8082, L0:5494 |

### Build

`build_circuit` → 17 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 47,246 | 5,512 | 292,829 | 0 | $0.0384 | — | — |
| **Total** | | **47,246** | **5,512** | **292,829** | **0** | **$0.0384** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 38s