# Circuit Oracle Report
**Date:** 2026-07-28 07:25:09 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe score is driven primarily by lexical/topic detectors for *conspiracy*, *MasterCard/payment cards*, and *chip*, rather than by a compositional representation of the final negated claim; the available attribution does **not** support “negation words” as the dominant mechanism.

**Confidence:** 7/10

**Reasoning:** The synthetic target returned by `get_top_logits` is the probe direction, and the strongest direct probe effects include both positive and negative signed contributions. The sign should be interpreted as direction along the probe weight, not automatically as “contradiction” versus “non-contradiction” without the probe’s label/sign convention.

The saved circuit has three content-bearing branches:

- **Conspiracy branch:** `Emb: Cons (pos 1) and piracy (pos 2)` → **Conspiracy-word detector** `L3:F9739@2` → probe.  
  `L3:F9739` is highly selective (`frac_nonzero=0.00762`) and its activating examples are repeatedly for *conspiracy/co-conspirator*. It receives its dominant positive input directly from the token embeddings **“Cons”** (+8.75) and **“piracy”** (+7.63), i.e. the beginning of *“Conspiracy theorists.”* Its probe direct effect is negative (−0.348), showing that this literal topic cue strongly moves the score in one probe direction.

- **Financial-card branch:** `Emb: Card (pos 6)` → **MasterCard/payment-card-and-money detector** `L7:F1062@6,11` → probe.  
  `L7:F1062` is selective (`frac_nonzero=0.00307`) and its examples concern debit/credit cards, spending, cash, and transactions. Its largest upstream input is directly from **“Card”** at position 6 (+14.0 for its occurrence at pos 6; +7.31 for its occurrence at pos 11), with additional positive support from the *chip* token at pos 11 (+2.69). It contributes negatively to the probe at both positions (−0.237 and −0.151). Thus the probe is responding to a payment-card/financial topic representation, not merely a surface negation cue.

- **Chip branch:** `Emb: chip (pos 11)` → **Chip / semiconductor lexical detector** `L2:F16230@11` → probe.  
  This detector is also selective (`frac_nonzero=0.00969`) and its examples are explicitly semiconductor-device/chip text. Its upstream attribution is overwhelmingly the raw embedding for **“ chip”** (+27.0); its direct effect on the probe is positive (+0.266). This is an especially clear lexical shortcut: one specific noun creates nearly the entire detector signal.

There is also a generic nuisance feature, **“that”** `L0:F3635@12`, with a positive direct effect (+0.225). Its label and examples identify it as simply the word *“that”* (`frac_nonzero=0.0428`). This demonstrates some lexical contamination, but it is not evidence that negation is the principal driver. Likewise, the surface-prefix feature `L0:F16015@1` detects **“cons”** and has a positive probe effect (+0.187), consistent with token-form/topic leakage around *Conspiracy*, not a semantic contradiction computation.

Most importantly, no inspected high-effect feature was a detector for **“No one,” “no,” “anything,” “nefarious,”** or a scoped-negation relation such as *“nobody thinks X is nefarious.”* The final sentence’s contradiction-relevant composition—an apparently suspicious scenario followed by explicit denial of nefarious intent—does not appear in the traced dominant paths. Instead, the probe linearly aggregates individually signed, shallow-to-mid-layer topical cues: conspiracy wording, Mastercard/card-money material, and chip terminology, plus generic token-form features.

The user’s broader concern about spurious features is therefore substantially justified, but with a qualification: this graph indicates **topic/lexical shortcutting more clearly than negation-word shortcutting**. The classification is not well supported as a genuine semantic contradiction judgment; it is better characterized as a mixture of content-keyword detectors whose directions happen to align with the probe.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F3635](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) | 12 | Generic lexical: “that” | the word "that" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) |
| [L3:F9739](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9739) | 2 | Conspiracy-word detector |  words related to conspiracies | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9739) |
| [L2:F16230](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16230) | 11 | Chip / semiconductor lexical detector |  mentions of semiconductor chips and devices | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16230) |
| [L7:F1062](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1062) | 6 | MasterCard / payment-card-and-money detector |  words and phrases related to credit cards, loans, spending, gambling, and money in general. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1062) |
| [L7:F1062](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1062) | 11 | MasterCard / payment-card-and-money detector |  words and phrases related to credit cards, loans, spending, gambling, and money in general. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1062) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L3:9739 de=-0.348 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F1062@6` | ❌ error | — | — | Trace this strong probe-driving feature upstream to embeddings. Determine whethe… |
| SA-2 | `L7:F1062@11` | ❌ error | — | — | Trace this second occurrence of the strong L7 feature upstream to embeddings, id… |
| SA-3 | `L3:F9739@2` | ❌ error | — | — | Trace this largest-magnitude early-mid feature to embedding sources; determine w… |
| SA-4 | `L2:F16230@11` | ❌ error | — | — | Trace this positive probe-driving feature upstream to embeddings, with focus on … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×5 | L7:1062, L3:9739, L2:16230, L0:3635, L0:16015 |
| 2 | `get_upstream_features` | L7:F1062@6, k=15 → Emb:"Card"@6 (de=14.00) +14 more |
| 3 | `get_upstream_features` | L7:F1062@11, k=15 → Emb:"Card"@6 (de=7.31) +14 more |
| 4 | `get_upstream_features` | L3:F9739@2, k=15 → Emb:"Cons"@1 (de=8.75) +14 more |
| 5 | `get_upstream_features` | L2:F16230@11, k=15 → Emb:" chip"@11 (de=27.00) +14 more |

### Build

`build_circuit` → 8 nodes, 7 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 11,671 | 2,734 | 49,426 | 0 | $0.0825 | — | — |
| **Total** | | **11,671** | **2,734** | **49,426** | **0** | **$0.0825** | | |

**Oracle wall-clock time:** 0m 38s