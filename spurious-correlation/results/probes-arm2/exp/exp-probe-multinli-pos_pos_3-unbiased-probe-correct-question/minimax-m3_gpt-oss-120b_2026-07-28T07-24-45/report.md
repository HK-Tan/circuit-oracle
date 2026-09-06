# Circuit Oracle Report
**Date:** 2026-07-28 07:24:45 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction probe is driven by an aggregate of premise-side entity/content features (castle, early 17th-century, tower house) together with a small but real negation-word feature in the hypothesis — a mixed lexical/negation pattern, not a pure spurious-negation shortcut.

**Confidence:** 7

**Reasoning:** The top-20 features by direct effect decompose cleanly into four premise-content supernodes and one negation supernode:

- **Entity recognizer: 'castle' (pos 2)** — L4:F13244 (+0.29, dee strongest driver), L4:F5749, L3:F10598, L0:F14108. These all anchor on the " castle" embedding at pos 2 (direct_effect 18.5 into L4:F13244), with secondary input from " itself" and abstract features on " house" (L6:F486 → L4:F13244). This is genuine content tracking of the subject entity.
- **'early 17th-century' tokens (pos 5–6, premise)** — L2:F4429 fires on both " early" (pos 6, de 35.25) and " early" (pos 39, de 36.5), with L0:F7360 (" an"), L0:F5494 (" early"), L0:F4367 ("century"), L0:F7513 (" together", de 43) also positive. The " together" feature at pos 26 is interesting: it's content/structural ("held together without a single nail"), not negation. The same L2:F4429 firing at pos 39 (" early" inside "does not contain any early 17th-century tower houses") shows a *shared lexical* feature, which is exactly what a surface-heuristic probe would learn.
- **'tower house' compound (pos 13–14, premise)** — L1:F1027 (" tower", de 23), L0:F4079 (" tower"), L0:F2158 (" with", de 33.75 — strong on "with Irish oak from the park"), L0:F11220 (" restored", de −20 → negative), L2:F1430 (" house", de −30.9, the *inhibitory* feature the user may be asking about), L0:F8974 (" from", de 39.75), L0:F10815 (" any", de 40.5). L2:F1430 at pos 14 is strongly negative (direct_effect −0.22 at pos 14), pulled down by an upstream " house" feature. This is a lexical/noun feature acting as a suppressor, not a negation detector.
- **Negation words in hypothesis (does/not/contain/any, pos 35–38)** — L0:F10815 (" any", de 40.5 into the feature) and L0:F8082 (" itself"). Only one of the top-20 features (L0:F10815 at pos 38) explicitly tracks a hypothesis-side negation word (" any"). "does" pos 35 and "not" pos 36 do not appear as top-20 positive drivers; "not" appears with a small +0.085 on L0:F7513 but that feature fires on " together" (pos 26) in the premise, not on "not".
- **BOS/'The' meta-state (pos 1, inhibitory)** — L8:F8406 (de −0.108), L7:F462 (de −4.78 into L8), L5:F3992, L6:F14585. These chain back to the BOS embedding and "The" — a generic position-1 representation, not content-specific.

The user's hypothesis that the probe uses "negation-word" signals rather than content is only *partially* supported. The single negation-lexical driver that does appear is the universal quantifier " any" (a standard NLI contradiction cue). The much larger contributions come from premise-side content features — " castle", " early", "century", " tower", " house", " from", " with", " together" — that fire on the assertion. The " tower house" / " house" features (L2:F1430, L1:F1027) actually carry **negative** direct effect on the probe, meaning the model is *suppressing* contradiction when it sees the tower-house noun phrase matching the hypothesis. So the contradiction signal is built mainly from the *absence* of overlap detectors: the model finds premise-entity and premise-content tokens but does not find a strong "the castle contains tower houses" match — exactly the lexical-overlap heuristic that NLI probes classically pick up.

A genuine cross-sentence semantic comparison (e.g., noticing that the hypothesis's "does not contain any" negates the premise's "comprises") is **not** present in the top-20 graph. The only negation-side evidence is the surface word " any" (and the generic-position BOS feature). So the user's concern is partly right: the circuit leans on lexical/positional cues (entity tokens, " any", a position-1 BOS meta-state) more than on a real semantic-negation composition. But it is **not** purely a "negation-word" detector — premise content features contribute the majority of the positive direct effect.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F13244](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) | 2 | Entity recognizer: 'castle' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) |
| [L4:F5749](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) | 2 | Entity recognizer: 'castle' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) |
| [L3:F10598](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10598) | 3 | Entity recognizer: 'castle' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10598) |
| [L0:F14108](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14108) | 2 | Entity recognizer: 'castle' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14108) |
| [L2:F4429](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) | 6 | 'early 17th-century' tokens (pos 5–6, premise) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) |
| [L2:F4429](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) | 39 | 'early 17th-century' tokens (pos 5–6, premise) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) |
| [L0:F7360](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7360) | 5 | 'early 17th-century' tokens (pos 5–6, premise) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7360) |
| [L0:F5494](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5494) | 6 | 'early 17th-century' tokens (pos 5–6, premise) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5494) |
| [L0:F4367](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4367) | 12 | 'early 17th-century' tokens (pos 5–6, premise) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4367) |
| [L0:F7513](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7513) | 26 | 'early 17th-century' tokens (pos 5–6, premise) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7513) |
| [L1:F1027](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1027) | 13 | 'tower house' compound (pos 13–14, premise) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1027) |
| [L0:F4079](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4079) | 13 | 'tower house' compound (pos 13–14, premise) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4079) |
| [L0:F10815](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10815) | 38 | 'tower house' compound (pos 13–14, premise) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10815) |
| [L0:F8974](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) | 20 | 'tower house' compound (pos 13–14, premise) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) |
| [L1:F11220](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11220) | 16 | 'tower house' compound (pos 13–14, premise) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11220) |
| [L2:F1430](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1430) | 14 | 'tower house' compound (pos 13–14, premise) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1430) |
| [L0:F2158](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) | 17 | 'tower house' compound (pos 13–14, premise) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) |
| [L0:F8082](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8082) | 3 | Negation words in hypothesis (does/not/contain/any, pos 35–38) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8082) |
| [L6:F486](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/486) | 14 | Mid-layer abstract features on 'house' (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/486) |
| [L4:F13244](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) | 14 | Mid-layer abstract features on 'house' (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) |
| [L3:F14368](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14368) | 14 | Mid-layer abstract features on 'house' (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14368) |
| [L2:F8185](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8185) | 14 | Mid-layer abstract features on 'house' (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8185) |
| [L0:F9604](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9604) | 14 | Mid-layer abstract features on 'house' (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9604) |
| [L8:F8406](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) | 1 | BOS/'The' meta-state on pos 1 (inhibitory) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) |
| [L7:F462](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) | 1 | BOS/'The' meta-state on pos 1 (inhibitory) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) |
| [L7:F5741](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5741) | 1 | BOS/'The' meta-state on pos 1 (inhibitory) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5741) |
| [L5:F3992](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3992) | 1 | BOS/'The' meta-state on pos 1 (inhibitory) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3992) |
| [L6:F14585](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14585) | 1 | BOS/'The' meta-state on pos 1 (inhibitory) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14585) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:13244 de=0.287 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F13244@2` | ❌ error | — | — | Trace this feature at L4:13244 pos 2. What input does it fire on? What upstream … |
| SA-2 | `L2:F1430@14` | ❌ error | — | — | Trace this INHIBITORY feature at L2:1430 pos 14. What input token is at position… |
| SA-3 | `L0:F2158@17` | ❌ error | — | — | Trace this feature at L0:2158 pos 17. Position 17 is likely "does" or "not" in t… |
| SA-4 | `L1:F1027@13` | ❌ error | — | — | Trace this feature at L1:1027 pos 13. Position 13 likely corresponds to "does" o… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F13244@2, k=10 → Emb:" castle"@2 (de=18.50) +9 more |
| 2 | `get_upstream_features` | L0:F2158@17, k=10 → Emb:" with"@17 (de=33.75) +9 more |
| 3 | `get_upstream_features` | L0:F7360@5, k=10 → Emb:" an"@5 (de=27.38) +9 more |
| 4 | `get_upstream_features` | L1:F1027@13, k=10 → Emb:" tower"@13 (de=23.12) +9 more |
| 5 | `get_upstream_features` | L0:F5494@6, k=10 → Emb:" early"@6 (de=21.12) +9 more |
| 6 | `get_upstream_features` | L2:F4429@6, k=10 → Emb:" early"@6 (de=35.25) +9 more |
| 7 | `get_upstream_features` | L2:F4429@39, k=10 → Emb:" early"@39 (de=36.50) +9 more |
| 8 | `get_upstream_features` | L1:F11220@16, k=10 → Emb:" restored"@16 (de=20.00) +9 more |
| 9 | `get_upstream_features` | L0:F14108@2, k=10 → Emb:" castle"@2 (de=11.81) +9 more |
| 10 | `get_upstream_features` | L4:F5749@2, k=10 → Emb:" castle"@2 (de=14.75) +9 more |
| 11 | `get_upstream_features` | L3:F10598@3, k=10 → Emb:" itself"@3 (de=30.12) +9 more |
| 12 | `get_upstream_features` | L0:F7513@26, k=10 → Emb:" together"@26 (de=43.00) +9 more |
| 13 | `get_upstream_features` | L6:F486@14, k=10 → L5:F3316 (de=-2.38) +9 more |
| 14 | `get_upstream_features` | L0:F8974@20, k=10 → Emb:" from"@20 (de=39.75) +9 more |
| 15 | `get_upstream_features` | L0:F4367@12, k=10 → Emb:"century"@12 (de=23.12) +9 more |
| 16 | `get_upstream_features` | L0:F10815@38, k=10 → Emb:" any"@38 (de=40.50) +9 more |
| 17 | `get_upstream_features` | L2:F1430@14, k=10 → Emb:" house"@14 (de=30.88) +9 more |
| 18 | `get_upstream_features` | L0:F4079@13, k=10 → Emb:" tower"@13 (de=19.12) +9 more |
| 19 | `get_upstream_features` | L0:F8082@3, k=10 → Emb:" itself"@3 (de=19.88) +9 more |
| 20 | `get_upstream_features` | L8:F8406@1, k=10 → Emb:"<bos>"@0 (de=9.50) +9 more |
| 21 | `get_upstream_features` | L7:F462@1, k=10 → Emb:"<bos>"@0 (de=18.75) +9 more |
| 22 | `get_upstream_features` | L5:F3992@1, k=10 → Emb:"<bos>"@0 (de=22.62) +9 more |
| 23 | `get_upstream_features` | L4:F13244@14, k=10 → Emb:" house"@14 (de=11.38) +9 more |
| 24 | `get_upstream_features` | L0:F9604@14, k=8 → Emb:" house"@14 (de=19.88) +7 more |
| 25 | `get_upstream_features` | L2:F8185@14, k=5 → Emb:" house"@14 (de=9.25) +4 more |
| 26 | `get_upstream_features` | L3:F14368@14, k=5 → Emb:" house"@14 (de=27.00) +4 more |

### Build

`build_circuit` → 20 nodes, 20 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 33,795 | 6,605 | 94,615 | 0 | $0.0237 | — | — |
| **Total** | | **33,795** | **6,605** | **94,615** | **0** | **$0.0237** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 23s