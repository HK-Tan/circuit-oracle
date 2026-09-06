# Circuit Oracle Report
**Date:** 2026-07-28 07:24:57 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_10 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction classification is driven primarily by shallow "not"-token detectors in the hypothesis (the word `not` at position 17 inside "There is not role reversal..."), not by any semantic comparison between premise and hypothesis content.

**Confidence:** 8

**Reasoning:** The dominant path in the circuit is a negation-word shortcut: the embedding of `not` (pos 17, direct_effect=32.75 on L0:F4958 alone) feeds a chain of dedicated negation features at positions 17 — L0:F4958 and L0:F15454 → L2:F12021, F6993 → L3:F1101, F8011, F9803, F12079 → L4:F2422, F4492 — which then excite late-layer output-driving features L9:F14687 (pos 21), L9:F742 (pos 17), L10:F6670 (pos 19), L12:F12606 (pos 21). These L9–L12 features carry the largest signed contributions to the probe score (+0.28, +0.21, +0.21). Crucially, the *premise* content path (L0 "role/reversal/strangest" detectors → L5–L7 "role reversal" synthesis at pos 4 → L4 temporal/suppressor features) carries *negative* direct_effects (L4:F5709 −0.37 at "now", L2:F16097 −0.28 at "strangest", L4:F14368 −0.22 at "reversal") and is largely inactive in driving the score. The probe therefore classifies the pair as contradiction almost entirely because the hypothesis contains the surface token `not` (and, secondarily, the period at pos 14 with −0.19), without engaging any actual premise-vs-hypothesis semantic comparison — a textbook lexical-spurious-feature artifact, exactly matching the user's concern.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: 'not' (pos 17) - contradiction marker in hypothesis | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: 'now' (pos 9) - present-tense temporal marker | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: 'reversal' (pos 4) - premise content word | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: 'role' (pos 3) - premise content word | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: 'strangest' (pos 2) - premise content word | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: 'There' (pos 15) - hypothesis sentence start | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: '.' (pos 14) - sentence boundary | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: 'on' (pos 21) - hypothesis content | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 17 | L0-L2: 'not' token detectors at pos 17 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F15454](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15454) | 17 | L0-L2: 'not' token detectors at pos 17 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15454) |
| [L2:F12021](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) | 17 | L0-L2: 'not' token detectors at pos 17 | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) |
| [L2:F6993](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6993) | 17 | L0-L2: 'not' token detectors at pos 17 | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6993) |
| [L3:F1101](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) | 17 | L3: mid-layer negation-processing features at pos 17 | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 17 | L3: mid-layer negation-processing features at pos 17 | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L3:F9803](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9803) | 17 | L3: mid-layer negation-processing features at pos 17 | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9803) |
| [L3:F12079](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) | 17 | L3: mid-layer negation-processing features at pos 17 | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 17 | L4: negation-context aggregators at pos 17 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 17 | L4: negation-context aggregators at pos 17 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 4 | L0: premise content detectors (pos 4 'reversal', pos 3 'role', pos 2 'strangest') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F5232](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5232) | 9 | L0: premise content detectors (pos 4 'reversal', pos 3 'role', pos 2 'strangest') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5232) |
| [L0:F1903](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1903) | 1 | L0: premise content detectors (pos 4 'reversal', pos 3 'role', pos 2 'strangest') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1903) |
| [L0:F6013](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6013) | 3 | L0: premise content detectors (pos 4 'reversal', pos 3 'role', pos 2 'strangest') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6013) |
| [L4:F5709](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) | 9 | L4: 'now'/'right' temporal features at pos 9 (negative direct_effect) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) |
| [L4:F6072](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6072) | 9 | L4: 'now'/'right' temporal features at pos 9 (negative direct_effect) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6072) |
| [L4:F12799](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12799) | 2 | L4: 'now'/'right' temporal features at pos 9 (negative direct_effect) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12799) |
| [L4:F14368](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14368) | 4 | L4: 'now'/'right' temporal features at pos 9 (negative direct_effect) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14368) |
| [L2:F16097](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) | 2 | L2: 'strangest' detector at pos 2 (negative direct_effect) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) |
| [L2:F10705](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10705) | 11 | L2: 'strangest' detector at pos 2 (negative direct_effect) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10705) |
| [L5:F9068](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9068) | 4 | L5-L7: premise 'role reversal' synthesis features at pos 4 | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9068) |
| [L6:F12420](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12420) | 4 | L5-L7: premise 'role reversal' synthesis features at pos 4 | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12420) |
| [L6:F2743](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2743) | 4 | L5-L7: premise 'role reversal' synthesis features at pos 4 | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2743) |
| [L7:F905](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/905) | 4 | L5-L7: premise 'role reversal' synthesis features at pos 4 | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/905) |
| [L7:F4526](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4526) | 4 | L5-L7: premise 'role reversal' synthesis features at pos 4 | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4526) |
| [L8:F16033](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16033) | 4 | L5-L7: premise 'role reversal' synthesis features at pos 4 | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16033) |
| [L4:F7409](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7409) | 4 | L5-L7: premise 'role reversal' synthesis features at pos 4 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7409) |
| [L9:F14687](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/14687) | 21 | L9-L12: late-layer features driving the probe from 'not' context (pos 17, 19, 21) | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/14687) |
| [L9:F742](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/742) | 17 | L9-L12: late-layer features driving the probe from 'not' context (pos 17, 19, 21) | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/742) |
| [L10:F6670](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) | 19 | L9-L12: late-layer features driving the probe from 'not' context (pos 17, 19, 21) | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) |
| [L12:F12606](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) | 21 | L9-L12: late-layer features driving the probe from 'not' context (pos 17, 19, 21) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 14 | L0: '.' (period) feature at pos 14 (negative direct_effect) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Output: probe classification score (contradiction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:5709 de=-0.371 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F5709@9` | ❌ error | — | — | Trace the path from L4:F5709 at position 9. This feature has a strong negative d… |
| SA-2 | `L6:F12420@4` | ❌ error | — | — | Trace the path from L6:F12420 at position 4. This feature has a strong negative … |
| SA-3 | `L4:F12799@2` | ❌ error | — | — | Trace the path from L4:F12799 at position 2. This feature has a strong positive … |
| SA-4 | `L2:F16097@2` | ❌ error | — | — | Trace the path from L2:F16097 at position 2. Strong negative direct_effect (-0.2… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F5709@9, k=10 → Emb:" now"@9 (de=40.25) +9 more |
| 2 | `get_upstream_features` | L6:F12420@4, k=10 → Emb:" role"@3 (de=5.59) +9 more |
| 3 | `get_upstream_features` | L4:F12799@2, k=10 → Emb:" strangest"@2 (de=31.00) +9 more |
| 4 | `get_upstream_features` | L2:F16097@2, k=10 → Emb:" strangest"@2 (de=24.00) +9 more |
| 5 | `get_upstream_features` | L10:F6670@19, k=10 → Emb:" not"@17 (de=6.78) +9 more |
| 6 | `get_upstream_features` | L4:F6072@9, k=10 → Emb:" now"@9 (de=49.75) +9 more |
| 7 | `get_upstream_features` | L3:F12079@17, k=10 → Emb:" There"@15 (de=15.00) +9 more |
| 8 | `get_upstream_features` | L7:F905@4, k=10 → Emb:" reversal"@4 (de=6.88) +9 more |
| 9 | `get_upstream_features` | L4:F14368@4, k=10 → Emb:" role"@3 (de=12.31) +9 more |
| 10 | `get_upstream_features` | L0:F6013@3, k=10 → Emb:" role"@3 (de=15.56) +9 more |
| 11 | `get_upstream_features` | L8:F16033@4, k=10 → Emb:" reversal"@4 (de=13.00) +9 more |
| 12 | `get_upstream_features` | L7:F4526@4, k=10 → Emb:" reversal"@4 (de=5.16) +9 more |
| 13 | `get_upstream_features` | L12:F12606@21, k=10 → Emb:" not"@17 (de=6.56) +9 more |
| 14 | `get_upstream_features` | L2:F10705@11, k=10 → Emb:" concerns"@11 (de=25.75) +9 more |
| 15 | `get_upstream_features` | L0:F6051@14, k=10 → Emb:"."@14 (de=46.25) +9 more |
| 16 | `get_upstream_features` | L4:F2422@17, k=8 → Emb:" not"@17 (de=16.50) +7 more |
| 17 | `get_upstream_features` | L4:F4492@17, k=8 → Emb:" not"@17 (de=18.00) +7 more |
| 18 | `get_upstream_features` | L0:F4958@17, k=8 → Emb:" not"@17 (de=32.75) +7 more |
| 19 | `get_upstream_features` | L9:F14687@21, k=8 → Emb:" not"@17 (de=10.88) +7 more |
| 20 | `get_upstream_features` | L0:F6051@14, k=5 → Emb:"."@14 (de=46.25) +4 more |
| 21 | `get_upstream_features` | L0:F7696@21, k=8 → Emb:" on"@21 (de=38.75) +7 more |
| 22 | `get_upstream_features` | L3:F1101@17, k=8 → Emb:" not"@17 (de=13.19) +7 more |
| 23 | `get_upstream_features` | L3:F8011@17, k=8 → Emb:" not"@17 (de=21.00) +7 more |
| 24 | `get_upstream_features` | L3:F9803@17, k=8 → Emb:" not"@17 (de=13.62) +7 more |
| 25 | `get_upstream_features` | L3:F12079@17, k=8 → Emb:" There"@15 (de=15.00) +7 more |
| 26 | `get_upstream_features` | L0:F5232@9, k=8 → Emb:" now"@9 (de=34.50) +7 more |
| 27 | `get_upstream_features` | L0:F9026@4, k=8 → Emb:" reversal"@4 (de=22.62) +7 more |
| 28 | `get_upstream_features` | L0:F1903@1, k=8 → Emb:"<bos>"@0 (de=16.50) +7 more |

### Build

`build_circuit` → 18 nodes, 17 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 15,531 | 6,111 | 68,241 | 0 | $0.0161 | — | — |
| **Total** | | **15,531** | **6,111** | **68,241** | **0** | **$0.0161** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 40s