# Circuit Oracle Report
**Date:** 2026-07-28 07:25:06 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction-probe score is driven primarily by the explicit surface negation **“No one”**, with weaker lexical contributions from prompt content such as *conspiracy* and *personal* information—not by a rich representation of the MasterCard claim’s semantic inconsistency.

**Confidence:** 8/10

**Reasoning:** The dominant positive circuit is an unusually direct negation pathway centered on the final sentence, “**No one** thinks Mastercard is up to anything nefarious.”

- The strongest late positive feature is **L16:F11298 at pos 30** (direct effect **+0.2402**). Its label is simply **“no”**, it fires selectively (`frac_nonzero=0.01043`), and its top activating cases are overwhelmingly literal *No/no*. It is driven most strongly by:
  - **Emb: “ No” (pos 30)**, direct effect **+12**;
  - **L15:F13061 at pos 30**, direct effect **+14**;
  - **L14:F336 at pos 30**, direct effect **+8.5**.
  Thus the high-level probe-driving feature is best understood as a persistent, position-local representation of the word **No**, rather than a detector of the proposition that Mastercard is or is not nefarious.

- **L15:F13061 at pos 30** is also a major direct driver of the probe (**+0.2100**). Its interpretation is “uses of the word *no* or similar negative statements and words associated with *one*,” with `frac_nonzero=0.01521`. Its immediate strongest causes are again **Emb: “ No” (+12.6875)** and **L14:F336 (+13)**. This confirms the circuit’s central chain:
  **Emb “No” → L14 negation representation → L15 negative-statement representation → L16 selective No representation → contradiction-probe score.**

- The word **“one”** supplies a separate phrase-level cue. **L4:F15764 at pos 31** directly raises the score by **+0.2910**, is selective (`frac_nonzero=0.00765`), and is labelled as a pronoun/verb/**one** sentence fragment detector. Its promoted tokens include *nobody*, *nothing*, *anyone*, and *anybody*, which is strong evidence for a “no one / nobody” construction rather than a MasterCard-specific semantic feature. It is principally sourced from **Emb: “ one” (pos 31)** with direct effect **+10.75**. This pathway feeds the probe directly alongside the deeper *No* pathway.

These connected supernodes were recorded in the circuit as:

1. **Emb: No (pos 30)**  
   → **Negation intermediate representation** (L14:F336)  
   → **Negative statement / No-one detector** (L15:F13061)  
   → **Highly selective No detector** (L16:F11298)  
   → **synthetic contradiction-probe score**.

2. **Emb: one (pos 31)**  
   → **No-one / pronoun-verb-one phrase detector** (L4:F15764)  
   → **synthetic contradiction-probe score**.

There is evidence for actual prompt-topic information, but it is secondary and not integrated into the dominant late semantic path:

- **L5:F559 at pos 2** has a conspiracy/co-conspirator interpretation (`frac_nonzero=0.00767`) and directly contributes **+0.2695**. This plausibly recognizes the prompt’s opening “Conspiracy theorists,” but it does not appear as the source of the late *No* features.
- **L1:F13292 at pos 11**, labelled **“personal”** (`frac_nonzero=0.00902`), contributes **+0.2422**, plausibly responding to “medical history” / personal information. Again, it is a shallow lexical cue rather than evidence that the model composed the full surveillance/financial claim with the denial.
- Several other major direct effects are even more generic: **L0:F11375** detects *is* (**+0.4766**), and **L0:F3635** detects *that* (**+0.3652**). These are grammatical/lexical features, not contradiction reasoning.

There are also negative direct effects from lexical features such as **L0:F44** at the initial *Conspiracy* token (**−0.5273**) and **L0:F14574** for *your* (**−0.3516**), showing that the probe direction is not simply “conspiracy language = contradiction.” The positive score arises largely from the classifier’s alignment with a **negated assertion / “No one” template**, with some shallower topic-word support.

Therefore, the user’s concern is substantially supported: this graph shows a **spurious or at least overly lexical negation-based mechanism**. The probe may be useful for detecting contradictions in-distribution if contradiction examples frequently use explicit denial wording, but on this input its main causal evidence is **No / no one**, not a robust comparison between the suspicious MasterCard proposition and the statement that nobody considers it nefarious.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 7 | Direct lexical: is |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F3635](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) | 12 | Direct lexical: that | the word "that" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) |
| [L5:F559](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/559) | 2 | Conspiracy lexical detector |  words frequently related to legal conspiracies and co-conspirators | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/559) |
| [L1:F13292](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13292) | 11 | Personal-information lexical detector |  the word "personal" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13292) |
| [L4:F15764](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15764) | 31 | No-one / pronoun-verb-one phrase detector |  fragments of sentences that contain a pronoun, a verb, and the word "one", or words with similar meanings | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15764) |
| [L14:F336](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) | 30 | Negation intermediate representation | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) |
| [L15:F13061](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13061) | 30 | Negative statement / No-one detector |  uses of the word "no" or similar negative statements and words associated with "one" | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13061) |
| [L16:F11298](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11298) | 30 | Highly selective No detector | no | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11298) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:44 de=-0.527 |
| 3 | `inspect_feature` ×5 | L16:11298, L15:13061, L4:15764, L0:11375, L0:3635 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F11298@30` | ❌ error | — | — | Trace why this late feature positively drives the synthetic contradiction probe.… |
| SA-2 | `L15:F13061@30` | ❌ error | — | — | Trace this late feature upstream to embeddings; establish whether it encodes the… |
| SA-3 | `L4:F15764@31` | ❌ error | — | — | Trace this feature upstream to identify token source and its contribution to the… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L16:F11298@30, k=20 → L15:F13061 (de=14.00) +19 more |
| 2 | `get_upstream_features` | L15:F13061@30, k=20 → L14:F336 (de=13.00) +19 more |
| 3 | `get_upstream_features` | L4:F15764@31, k=20 → Emb:" one"@31 (de=10.75) +19 more |
| 4 | `inspect_feature` ×4 | L0:44, L0:14574, L5:559, L1:13292 |

### Build

`build_circuit` → 11 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 18,318 | 2,612 | 48,462 | 0 | $0.0971 | — | — |
| **Total** | | **18,318** | **2,612** | **48,462** | **0** | **$0.0971** | | |

**Oracle wall-clock time:** 0m 34s