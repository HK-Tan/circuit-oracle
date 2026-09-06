# Circuit Oracle Report
**Date:** 2026-07-28 07:22:10 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_8 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** This is a contradiction-probe attribution graph where the classification score is driven almost entirely by a stack of low-level word-identity features (yield, who, Congress, lift, fund, control, levels, many, counsel, politicians) anchored on tokens from the *premise* (pos 2–8) and the *hypothesis* (pos 7), with **no negation or contradiction-detection features** anywhere in the top-20 list; the signal that pushes the probe toward "contradiction" is essentially topic overlap on legislative/Congress vocabulary plus a couple of mid-level features for "control" and "subjective language", which is a classic **spurious bag-of-keywords shortcut** rather than any genuine NLI reasoning.

**Confidence:** 7

**Reasoning:**

**What the probe is actually looking at (top features, ranked by |direct_effect|):**
- L0:6044 "yield" (pos 2, +0.79), L0:13437 "who" (pos 15, −0.58), L6:6096 "political parties/affiliations" (pos 2, +0.45), L2:6735 "political parties and politicians" (pos 2, −0.40), L1:6948 "lift" (pos 2, −0.39), L2:2701 "U.S. Congress" (pos 2, +0.38), L1:2116 "legal counsel/representation" (pos 7, +0.38), L0:9557 "clean" (pos 2, −0.37), L2:156 "amount/intensity words — levels" (pos 8, −0.37), L0:11606 "fund" (pos 7, −0.36), L3:13271 "control" (pos 5, +0.36), L3:123 "U.S. Congress" (pos 2, +0.36), L0:9529 "physical" (pos 5, +0.35), L3:8382 "many" (pos 13, +0.33), L1:3276 "U.S. Congress" (pos 2, +0.32), L6:13778 "subjective language, opinions and feelings" (pos 6, −0.31), L0:7021 "Congress" (pos 2, +0.31).

**The user's worry is largely confirmed, with one caveat.** There is no "negation word" or "no/not" feature in the top 20 — words like "no" and "not" do not appear. Instead, the *more spurious* mechanism is at work: the probe's contradiction score is driven by a noisy combination of single-word features that fire on premise tokens ("Congress", "fund", "levels", "many", "control") and an L6 feature (L6:13778, "subjective language") that fires on first-person pronouns like "we/our/think". In other words, the circuit reads *whether the text is about Congress and contains subjective/personal language*, not whether the hypothesis negates the premise. 

**Where the signal comes from (supernode trace):**
- **Emb → L0 (word identity)**: Six L0 features cluster on the *premise's* first content token region (pos 2, "Congress") — three different "Congress"-detectors (L0:7021, L1:3276, L2:2701, L3:123), plus three spurious misfires ("yield", "lift", "clean") that share no semantic content with the text — pure lexical collisions. Another cluster (L0:11606 "fund", L0:9529 "physical") sits on "funding levels" (pos 5–8). L0:13437 "who" fires on the relative-clause "who" at pos 15.
- **L1–L2 (lexical/conceptual)**: Features on "U.S. Congress" (L1:3276, L2:2701) and "political parties/politicians" (L2:6735) aggregate the premise's topic; L1:2116 fires on "counsel" (pos 7 of "legal services program"), and L2:156 on the quantity word "levels" (pos 8, "funding levels"). These features mix and partially cancel (L2:2701 +0.38 vs. L2:6735 −0.40, L1:3276 +0.32 vs. L1:6948 −0.39), so the signal-to-noise is poor.
- **L3–L6 (mid-level semantics)**: L3:123 "U.S. Congress mentions" (pos 2, +0.36) and L6:6096 "political parties/affiliations" (pos 2, +0.45) consolidate the congressional-topic signal. L3:13271 "control" (pos 5, +0.36) fires on "controls our funding" — *this is the only feature that picks up the entailment-bearing relation* (premise says Congress controls funding, hypothesis says Congress has no responsibility for funding). L6:13778 "subjective language" (pos 6, −0.31) is a generic subjective-pronoun detector that fires on "our" in the premise.

**Why the user's concern is well-founded:**
1. **No negation detection**: The contradiction relies on "no" + "responsibility" negating "controls", but neither "no" nor "responsibility" has any feature in the top 20. The model never "sees" the negation.
2. **Frac_nonzero on the topic features is very low (0.005–0.012)**: these are highly specific, entity-targeted detectors, not contradiction-reasoning features. The "subjective language" feature (L6:13778) is more generic (frac=0.05) but still tracks surface form, not entailment.
3. **The biggest single positive driver (L0:6044 "yield", +0.79) is a lexical collision** — a feature that learned "yield" patterns fires on a completely unrelated Congress sentence. This is direct evidence of feature noise.
4. **The control/responsibility axis is barely represented**: only L3:13271 "control" (+0.36) at pos 5 captures the entailment-relevant relation. There is no corresponding feature for "responsibility" or "no".

**Mechanism summary**: Signal flows Emb(premise "The Congress controls our funding levels many") → L0 word-identity detectors (noisy) → L1–L2 Congressional/legal/quantity concept detectors (partially cancelling) → L3–L6 Congress/parties/control/subjective aggregators (mostly topic, not entailment) → probe direction. The probe is essentially being driven by "this is text about Congress" + "this contains 'our'" rather than by any feature that detects the *negation of responsibility* — exactly the spurious shortcut the user suspected.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F6044](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) | 2 | L0 generic word-identity features on premise (pos 2) | the word "yield" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) |
| [L0:F13437](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13437) | 15 | L0 generic word-identity features on premise (pos 2) | the word "who" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13437) |
| [L0:F7021](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7021) | 2 | L0 generic word-identity features on premise (pos 2) |  the word "Congress" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7021) |
| [L0:F6948](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6948) | 2 | L0 generic word-identity features on premise (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6948) |
| [L0:F9557](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9557) | 2 | L0 generic word-identity features on premise (pos 2) | the word "clean" and words/phrases associated with people | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9557) |
| [L0:F9529](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9529) | 5 | L0 generic word-identity features on premise (pos 2) | the word "physical" and words related to programming | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9529) |
| [L0:F11606](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11606) | 7 | L0 fund + control + many word features |  the word "fund" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11606) |
| [L0:F12456](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12456) | 2 | L0 fund + control + many word features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12456) |
| [L1:F2116](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2116) | 7 | L1-L2 lexical/conceptual features (Congress, counsel, levels, politicians) |  words and phrases related to legal counsel or representation | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2116) |
| [L1:F3276](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3276) | 2 | L1-L2 lexical/conceptual features (Congress, counsel, levels, politicians) |  mentions of the United States Congress | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3276) |
| [L1:F8982](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8982) | 2 | L1-L2 lexical/conceptual features (Congress, counsel, levels, politicians) |  names of organizations, particularly related to India, and words associated with formal groups | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8982) |
| [L2:F2701](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) | 2 | L1-L2 lexical/conceptual features (Congress, counsel, levels, politicians) |  words related to the U.S. Congress | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) |
| [L2:F6735](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6735) | 2 | L1-L2 lexical/conceptual features (Congress, counsel, levels, politicians) |  political parties and politicians | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6735) |
| [L2:F156](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/156) | 8 | L1-L2 lexical/conceptual features (Congress, counsel, levels, politicians) |  words related to the amount or intensity of something | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/156) |
| [L3:F123](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/123) | 2 | L3-L6 mid-level semantic features (Congress mentions, control, many, subjective language) |  mentions of the United States Congress | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/123) |
| [L3:F13271](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13271) | 5 | L3-L6 mid-level semantic features (Congress mentions, control, many, subjective language) |  the word "control." | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13271) |
| [L3:F8382](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8382) | 13 | L3-L6 mid-level semantic features (Congress mentions, control, many, subjective language) |  the word "many", and sometimes "times" or "people" when near it | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8382) |
| [L6:F6096](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6096) | 2 | L3-L6 mid-level semantic features (Congress mentions, control, many, subjective language) |  political parties and affiliations | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6096) |
| [L6:F13778](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/13778) | 6 | L3-L6 mid-level semantic features (Congress mentions, control, many, subjective language) | subjective language, opinions and feelings. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/13778) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:6044 de=0.789 |
| 3 | `inspect_feature` ×19 | L0:6044, L0:13437, L6:6096, L2:6735, L2:156, L1:6948, L2:2701, L1:2116, L0:9557, L0:11606, L3:13271, L3:123, L0:9529, L3:8382, L1:3276, L6:13778, L0:7021, L1:8982, L1:12456 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F13778@6` | ❌ error | — | — | Trace the source of the "subjective language" feature at L6:13778, pos 6. What i… |
| SA-2 | `L2:F156@8` | ❌ error | — | — | Trace the source of the "amount/intensity words" feature at L2:156, pos 8. What … |
| SA-3 | `L0:F11606@7` | ❌ error | — | — | Trace the source of the "fund" feature at L0:11606, pos 7. What input tokens dri… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` | L0, F6044 → "the word "yield"" |

### Build

`build_circuit` → 7 nodes, 7 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 42,299 | 4,344 | 127,364 | 0 | $0.0255 | — | — |
| **Total** | | **42,299** | **4,344** | **127,364** | **0** | **$0.0255** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 1s