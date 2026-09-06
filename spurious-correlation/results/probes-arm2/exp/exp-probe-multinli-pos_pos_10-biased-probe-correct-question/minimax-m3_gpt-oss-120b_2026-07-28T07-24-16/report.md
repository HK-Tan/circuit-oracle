# Circuit Oracle Report
**Date:** 2026-07-28 07:24:16 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_10 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** This is a probe-attribution circuit for an NLI "contradiction" classifier on a classic entailment-contradiction pair where the second sentence ("There is **not** role reversal going on right now in relation to democracy") literally negates the first — and the probe is almost entirely driven by the surface-level negation token " not" at position 17, not by any genuine semantic comparison of the two sentences' content.

**Confidence:** 9

**Reasoning:**

The circuit is strikingly local to one token. Position 17 (" not") is the dominant signal source: the `get_source_influence` call returned `S_pct_of_total = 15.8%` and `S_over_R = 3.47`, meaning the single position 17 carries more signed multi-hop influence than the strongest non-source position by 3.5×. Position 17 is in the *hypothesis* (second sentence), not the premise.

Tracing downstream of the `Emb: " not" (pos 17)` node:
- **L0 "not" bigram detector** (F4958, activation 30.6) is the strongest single feature in the entire graph and receives direct_effect 32.75 from the " not" embedding. F15454 also fires on pos 17.
- **L2 negation-pattern features** (F12021 act 14.9, F6993, F7550) carry the " not" bigram up.
- **L3-L4 split**: the negation signal diverges into two opposing groups at the same layer/position:
  - *Promoters* (push toward contradiction): F4492 (L4, +1.22), F8011, F12079 (L3, +0.66 each), F2232, F9803.
  - *Inhibitors* (push against contradiction): F2422 (L4, −1.27), F1101 (L3, −1.21).
  - The L4 pair F2422/F4492 receive direct_effect 16.5 and 18.0 from the " not" embedding respectively — near-mirror images — indicating the model is internally disagreeing about how to interpret the same " not" token.
- **L8-L16 aggregators** (F14687, F9880, F6160 act 45.7, F10071, F12358) integrate these. Notably, F6160 is the highest-activation late feature (45.75), and its strongest upstream is the *premise* " There" (pos 15) with direct_effect 21.5, followed by F10742 (a "There is / There not" pattern detector) and the " not" embedding (6.3). F12358 similarly has " not" as its top driver (23.1).
- **Premise-side contributions are negligible.** The premise tokens (pos 1-14) only appear as minor features: F11375 (pos 5 " is", +0.37), F16097 (pos 2 " strangest", −0.40), F15749 (pos 2, +0.28). None of these are semantic-content features; they are positional/lexical features that connect only weakly to the output.

**What this means for the user's concern:** The user is correct. The contradiction probe is being driven by a **spurious lexical cue** — the single word " not" appearing in the hypothesis — rather than by any actual entailment-relation computation. Crucially, the prompt is constructed so that "not" should produce *entailment* (the second sentence negates the first, so the premise entails "there is NOT a role reversal going on"). A correct NLI classifier should suppress its contradiction response on " not" in this configuration. Instead, the model/probe's "contradiction" direction is *activated* by the bare presence of " not" (the "promoters" outweigh the "inhibitors": +3.2 vs −2.5 at L3-L4). The "There is / There not" pattern detector (F10742) feeds late aggregators that further amplify the contradiction signal.

The two-sentence structure of the prompt (premise + negated-hypothesis) provides no corrective signal — premise features have at most ~0.4 direct_effect each, while the " not" token alone drives features with 10-30× that magnitude. The contradiction classification here is essentially "I see the word 'not' → contradiction," a classic shortcut that an NLI probe should not be taking.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 17 | Negation-context inhibitors (L3-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L3:F1101](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) | 17 | Negation-context inhibitors (L3-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 17 | Negation-context positives (L3-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 17 | Negation-context positives (L3-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L3:F12079](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) | 17 | Negation-context positives (L3-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) |
| [L3:F2232](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2232) | 17 | Negation-context positives (L3-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2232) |
| [L3:F9803](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9803) | 17 | Negation-context positives (L3-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9803) |
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 17 | Late-layer contradiction aggregators (L8-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |
| [L15:F6160](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/6160) | 17 | Late-layer contradiction aggregators (L8-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/6160) |
| [L15:F10071](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) | 17 | Late-layer contradiction aggregators (L8-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) |
| [L9:F14687](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/14687) | 17 | Late-layer contradiction aggregators (L8-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/14687) |
| [L8:F9880](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9880) | 17 | Late-layer contradiction aggregators (L8-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9880) |
| [L1:F14233](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) | 17 | Late-layer contradiction aggregators (L8-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 17 | "not" bigram detector at pos 17 (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F15454](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15454) | 17 | "not" bigram detector at pos 17 (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15454) |
| [L2:F12021](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) | 17 | Negation bigram pattern (L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) |
| [L2:F6993](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6993) | 17 | Negation bigram pattern (L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6993) |
| [L2:F7550](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7550) | 17 | Negation bigram pattern (L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7550) |
| [L3:F10742](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10742) | 17 | "There is/There not" pattern (L3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10742) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 5 | Premise-context features (L0-L2, minor) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L2:F16097](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) | 2 | Premise-context features (L0-L2, minor) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) |
| [L1:F15749](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15749) | 2 | Premise-context features (L0-L2, minor) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15749) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:2422 de=-1.273 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F2422@17` | ❌ error | — | — | Trace the top NEGATIVE-driving feature L4:F2422 at pos 17. What input token/conc… |
| SA-2 | `L4:F4492@17` | ❌ error | — | — | Trace the top POSITIVE-driving feature L4:F4492 at pos 17. What input token/conc… |
| SA-3 | `L3:F1101@17` | ❌ error | — | — | Trace the strong negative feature L3:F1101 at pos 17. What does it encode? Trace… |
| SA-4 | `L16:F12358@17` | ❌ error | — | — | Trace the late-layer feature L16:F12358 at pos 17 with high direct_effect 0.656.… |
| SA-5 | `L0:F4958@17` | ❌ error | — | — | Trace L0:F4958 at pos 17 - highest activation (30.6) of any feature. What token/… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F2422@17, k=10 → Emb:" not"@17 (de=16.50) +9 more |
| 2 | `get_upstream_features` | L4:F4492@17, k=10 → Emb:" not"@17 (de=18.00) +9 more |
| 3 | `get_upstream_features` | L3:F1101@17, k=10 → Emb:" not"@17 (de=13.19) +9 more |
| 4 | `get_upstream_features` | L16:F12358@17, k=10 → Emb:" not"@17 (de=23.12) +9 more |
| 5 | `get_upstream_features` | L0:F4958@17, k=10 → Emb:" not"@17 (de=32.75) +9 more |
| 6 | `get_upstream_features` | L3:F12079@17, k=8 → Emb:" There"@15 (de=15.00) +7 more |
| 7 | `get_upstream_features` | L3:F8011@17, k=8 → Emb:" not"@17 (de=21.00) +7 more |
| 8 | `get_upstream_features` | L3:F9803@17, k=8 → Emb:" not"@17 (de=13.62) +7 more |
| 9 | `get_upstream_features` | L3:F2232@17, k=8 → Emb:" There"@15 (de=8.56) +7 more |
| 10 | `get_upstream_features` | L15:F6160@17, k=6 → Emb:" There"@15 (de=21.50) +5 more |
| 11 | `get_source_influence` | {'source_positions': [17]} → {'depth': 2, 'source_positions': [17], 'S_pct_of_total': 15.807, 'R_pct_of_total |
| 12 | `get_upstream_features` | L3:F10742@17, k=6 → Emb:" There"@15 (de=29.50) +5 more |
| 13 | `get_upstream_features` | L8:F9880@17, k=6 → Emb:" There"@15 (de=10.12) +5 more |
| 14 | `get_upstream_features` | L15:F10071@17, k=6 → Emb:" not"@17 (de=11.62) +5 more |
| 15 | `get_upstream_features` | L2:F12021@17, k=6 → Emb:" not"@17 (de=22.62) +5 more |
| 16 | `get_upstream_features` | L2:F16097@2, k=6 → Emb:" strangest"@2 (de=24.00) +5 more |
| 17 | `get_upstream_features` | L0:F11375@5, k=6 → Emb:" is"@5 (de=31.50) +5 more |
| 18 | `get_upstream_features` | L1:F15749@2, k=6 → Emb:" strangest"@2 (de=11.94) +5 more |
| 19 | `get_upstream_features` | L9:F14687@17, k=6 → Emb:" not"@17 (de=7.41) +5 more |

### Build

`build_circuit` → 12 nodes, 16 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 23,443 | 5,169 | 68,634 | 0 | $0.0174 | — | — |
| **Total** | | **23,443** | **5,169** | **68,634** | **0** | **$0.0174** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 1s