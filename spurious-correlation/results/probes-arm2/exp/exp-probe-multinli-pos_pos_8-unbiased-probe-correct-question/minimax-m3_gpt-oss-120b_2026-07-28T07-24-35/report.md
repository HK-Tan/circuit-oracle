# Circuit Oracle Report
**Date:** 2026-07-28 07:24:35 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_8 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction probe is driven by entity/syntactic features anchored to the premise's named entity ("Congress") and the hypothesis's opening verb phrase ("began to include"), not by any explicit negation or contradiction cue; the hypothesis's negation ("no responsibility") does not appear as a direct driver in the top of the circuit.

**Confidence:** 6

**Reasoning:** Tracing the top positive direct-effect features back to the embedding layer reveals a clean lexical/syntactic path, not a negation shortcut. Four parallel late-layer supernodes carry the positive score:

1. **L2:F2701 at pos 2** (direct_effect = 0.85) is the single strongest positive driver. Its upstream is dominated by the ` Congress` token embedding at pos 2 (de = 28.1), via L0 word-piece features F6044 (de = 0.49) and F15411 (de = 0.49). It encodes the premise's named entity — the structural anchor on which the contradiction turns.
2. **L3:F5753 at pos 12** (de = 0.53) is almost entirely fed by the ` include` token embedding (de = 41.0), i.e., a content verb from the hypothesis.
3. **L4:F59 at pos 11** (de = 0.41) traces back through L3:F12596 and L2:F11469, which in turn are driven by the ` began` and ` to` embeddings (de = 13.3 and 10.9 respectively). It detects the hypothesis's opening verb phrase "began to".
4. **L4:F7775 at pos 9** (de = 0.21) is fed by the comma embedding (de = 4.9) and the ` which` / `The` embeddings (via L3:F10633 and L0:F13564). It encodes a relative-clause syntactic boundary in the premise, not a polarity cue.

Crucially, the four "negation-flavored" tokens in the prompt — ` not` (pos 8), ` no` (pos 21), ` when` (pos 24), and the broader "does not support" / "no responsibility" phrases — do **not** appear as top positive direct-effect drivers, nor do they emerge as the top upstream feeders of any of the positive supernodes. The only negation-region feature that appears at all is L1:F5475 at pos 7 (de = −0.24, inhibitory), and L3:F8351 at pos 12 (de = −0.35, inhibitory, attached to the ` include` verb). These push *against* the contradiction score, not toward it. L0:F10198 at pos 2 (de = −0.37) and L2:F6735 at pos 2 (de = −0.35) are also inhibitory on the premise's "Congress" position.

So the circuit contradicts the user's "spurious negation" hypothesis: the positive signal comes from entity and syntactic-role features on the premise (Congress, comma/which) and the hypothesis's opening content (began to include), grounded all the way down to token embeddings at pos 1–4 (premise opening), 9 (comma), 10–12 (hypothesis opening), with ` Congress` at pos 2 as the dominant single source (de ≈ 28 into L2:F2701). The hypothesis's negation tokens are not the discriminative signal the probe is picking up.

Caveat lowering confidence: the positive drivers max out at L4 and the probe is on a mid-layer residual stream, so I could only trace 4–5 hops. The deeper circuit may still contain indirect negation-mediated paths that I could not reach, but no such path is visible in the top 20 features by direct effect.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L2:F2701](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) | 2 | L2:F2701 — 'Congress' entity feature at pos 2 (the premise) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) |
| [L3:F5753](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5753) | 12 | L3:F5753 — 'include' verb feature at pos 12 | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5753) |
| [L4:F59](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/59) | 11 | L4:F59 — 'began to' phrase feature at pos 11 (hyp start) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/59) |
| [L4:F7775](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7775) | 9 | L4:F7775 — 'comma/which' syntactic feature at pos 9 (premise clause) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7775) |
| [L0:F6044](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) | 2 | L0:F6044 — 'Congress' word-piece feature at pos 2 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) |
| [L0:F15411](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15411) | 2 | L0:F15411 — 'Congress' word-piece feature at pos 2 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15411) |
| [L3:F12596](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12596) | 11 | L3:F12596 — 'to' / 'began to' feature at pos 11 (hyp) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12596) |
| [L2:F11469](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11469) | 11 | L2:F11469 — 'began to' phrase feature at pos 11 (hyp) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11469) |
| [L2:F11734](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11734) | 9 | L2:F11734 — clause/relative-pronoun syntactic feature at pos 9 | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11734) |
| [L0:F4870](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4870) | 9 | L0:F4870 — comma token feature at pos 9 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4870) |
| [L3:F10633](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10633) | 3 | L3:F10633 — 'which ... The' opening tokens feature at pos 3/4 | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10633) |
| [L3:F10633](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10633) | 4 | L3:F10633 — 'which ... The' opening tokens feature at pos 3/4 | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10633) |
| [L0:F13564](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13564) | 4 | L0:F13564 — 'which' word feature at pos 4 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13564) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L2:2701 de=0.848 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F2701@2` | ❌ error | — | — | Trace the strongest positive driver L2:F2701 at pos 2 (the " Congress" position)… |
| SA-2 | `L3:F5753@12` | ❌ error | — | — | Trace the strong positive driver L3:F5753 at pos 12 (in the second sentence "the… |
| SA-3 | `L4:F59@11` | ❌ error | — | — | Trace the strong positive driver L4:F59 at pos 11 (" congress" start of second s… |
| SA-4 | `L0:F6044@2` | ❌ error | — | — | Trace the strong positive L0:F6044 at pos 2 (Congress, the premise entity). Dete… |
| SA-5 | `L0:F15411@2` | ❌ error | — | — | Trace the strong positive L0:F15411 at pos 2. Determine what this feature detect… |
| SA-6 | `L4:F7775@9` | ❌ error | — | — | Trace L4:F7775 at pos 9 (in "did not support the purpose" — a negation region). … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L2:F2701@2, k=15 → Emb:" Congress"@2 (de=28.12) +14 more |
| 2 | `get_upstream_features` | L3:F5753@12, k=15 → Emb:" include"@12 (de=41.00) +14 more |
| 3 | `get_upstream_features` | L4:F59@11, k=15 → Emb:" began"@10 (de=13.31) +14 more |
| 4 | `get_upstream_features` | L3:F12596@11, k=15 → Emb:" to"@11 (de=21.62) +14 more |
| 5 | `get_upstream_features` | L2:F11469@11, k=15 → Emb:" began"@10 (de=10.88) +14 more |
| 6 | `get_upstream_features` | L3:F4374@11, k=10 → Emb:" began"@10 (de=10.50) +9 more |
| 7 | `get_upstream_features` | L0:F6044@2, k=15 → Emb:" Congress"@2 (de=17.00) +14 more |
| 8 | `get_upstream_features` | L0:F15411@2, k=15 → Emb:" Congress"@2 (de=17.00) +14 more |
| 9 | `get_upstream_features` | L4:F7775@9, k=15 → Emb:","@9 (de=4.94) +14 more |
| 10 | `get_upstream_features` | L0:F8444@11, k=10 → Emb:" to"@11 (de=41.50) +9 more |
| 11 | `get_upstream_features` | L2:F11734@9, k=10 → Emb:","@9 (de=5.28) +9 more |
| 12 | `get_upstream_features` | L0:F4870@9, k=10 → Emb:","@9 (de=32.75) +9 more |
| 13 | `get_upstream_features` | L3:F10633@4, k=10 → Emb:" which"@4 (de=6.19) +9 more |
| 14 | `get_upstream_features` | L0:F13564@4, k=8 → Emb:" which"@4 (de=37.00) +7 more |
| 15 | `get_upstream_features` | L3:F10633@3, k=8 → Emb:","@3 (de=7.22) +7 more |
| 16 | `get_upstream_features` | L3:F123@2, k=10 → Emb:" Congress"@2 (de=20.62) +9 more |

### Build

`build_circuit` → 20 nodes, 25 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 15,912 | 5,221 | 73,620 | 0 | $0.0155 | — | — |
| **Total** | | **15,912** | **5,221** | **73,620** | **0** | **$0.0155** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 7s