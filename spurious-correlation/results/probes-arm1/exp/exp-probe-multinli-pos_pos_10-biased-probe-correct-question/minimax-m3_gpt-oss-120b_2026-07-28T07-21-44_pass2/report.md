# Circuit Oracle Report
**Date:** 2026-07-28 07:21:44 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_10 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by a cascade of negation-detector features that originate at the single token " not" (pos 17) in the second sentence, with a small secondary contribution from the superlative "strangest" (pos 2).

**Confidence:** 9

**Reasoning:** The circuit reveals a striking pattern: the vast majority of the probe's signal — both positive and negative drivers — flows from a single input token, the word " not" at position 17. Every high-impact feature in the graph encodes some flavor of negation:

- **Embedding layer:** The " not" token at pos 17 directly excites L0:F4958 (a literal "not" detector, activation=30.6, direct_effect=0.68) and also reaches deeper features via long-range embedding connections.
- **Early layers (L1–L3):** A constellation of negation-related features — L3:F8011 (promotes "not"/NOT), L3:F1101 (error/absence contexts, -1.21), L3:F12079 (Chinese negations, +0.66), L3:F2232 (code patterns like NOC/NO that promote "no", -0.40), L3:F9803 (scientific studies where something is "not" the case, +0.41), L1:F14233 (multilingual negative markers) — all fire on or near pos 17 and feed into mid-layer features.
- **Mid layers (L4, L8, L9):** L4:F4492 ("negations in various languages", +1.22) and L4:F2422 (multilingual negation, -1.27) are the two largest single drivers and represent opposing directions on the same negation signal. L8:F9880 and L9:F14687 continue the negation/uncertainty pattern.
- **Late layers (L15, L16):** L16:F12358 ("not followed by a form of to be", activation=28.25, +0.66) and L15:F6160 / L15:F10071 aggregate these signals into a high-level "X is not Y" phrase detector, fed directly by the " not" and " is" embeddings.

The user's concern is **confirmed by the circuit topology**: the probe relies heavily on **spurious surface-level negation cues** — specifically, the mere presence of the word " not" in the hypothesis sentence — rather than on semantic features that compare premise and hypothesis content. Notably:
1. The two strongest features (L4:F4492 at +1.22 and L4:F2422 at -1.27, plus L3:F1101 at -1.21) are essentially identical negation detectors with opposite signs — the probe is reading "is this a negation?" rather than "is this a contradiction?".
2. Features like L3:F2232 (hex codes containing "NO"), L3:F9803 (scientific negation), and L3:F10742 (French fragments) are clearly off-topic code/foreign-language detectors that happen to fire at the " not" position.
3. Almost no feature in the circuit integrates information across positions 2 (premise: "strangest role reversal…democracy") and 17 (hypothesis: "not role reversal…democracy"). The only non-pos-17 contribution is L0:F11375 ("is" detector at pos 5, +0.37) and the L1–L3 "strangest"/superlative features (small magnitudes like -0.40, +0.28, +0.38) — these are dwarfed by the negation cascade.

This is a classic artifact of a linear probe: a single salient lexical cue ("not" appearing only in the hypothesis) is sufficient to separate contradiction from entailment in NLI training data, and the probe has latched onto it. The mechanism is "spot the negation word in the hypothesis" rather than "compare the meaning of the two sentences." A robust contradiction probe should require cross-sentence interaction features, which are conspicuously absent from this graph.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 2 | Emb: 'strangest' (pos 2) | the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 16 | Emb: ' is' (pos 16) | the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 15 | Emb: 'There' (pos 15) | the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 17 | Literal 'not' detector | the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 5 | Literal 'is' detector |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L1:F15749](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15749) | 2 | 'strange'-related word detector |  the word "strange", or related words | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15749) |
| [L1:F14233](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) | 17 | Multilingual negative marker detector | negative sentiment markers such as "not," "no," "never," and their equivalents in other languages | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) |
| [L2:F16097](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) | 2 | Superlative adjective detector (strangest/largest/highest) | superlative adjectives and the words "test" or "point" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 17 | Promotes 'not'/NOT negation token | a mix of words and code fragments from different languages | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L3:F1101](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) | 17 | Error/absence/negation in software contexts | error messages and terms indicating absence or negation in software contexts. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) |
| [L3:F12079](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) | 17 | Negation in Chinese/multilingual contexts | negations and Chinese names | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) |
| [L3:F2232](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2232) | 17 | NO/NOC/ORES pattern in code (promotes 'no') |  character sequences like "NOC", "NO", "ORES", "NOS", "OF", "UNCH", and "oooooooo" within a series of hexadecimal codes, sometimes also picking up on related words such as "dangerously", "Bantus", "slave", and "plantation" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2232) |
| [L3:F9803](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9803) | 17 | Scientific studies where something is disproven | sentences describing scientific studies or experiments, particularly where something is disproven | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9803) |
| [L3:F3669](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3669) | 2 | Ordinal rankings (largest/highest) |  references to ordinal rankings of things | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3669) |
| [L3:F10742](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10742) | 17 | French 'avoir' fragments |  fragments of French sentences, particularly those containing the verb "avoir" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10742) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 17 | Multilingual negation detector (positive driver) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 17 | Multilingual negation detector (negative driver) | negations in other languages like French, Malay, and Croatian | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L8:F9880](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9880) | 17 | Doubt/negation/uncertainty phrase detector |  phrases expressing doubt, negation, or uncertainty | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9880) |
| [L9:F14687](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/14687) | 17 | Phrases using 'not' (often + because/but) | phrases using the word "not", often followed by "because" or "but." | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/14687) |
| [L15:F10071](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) | 17 | Negations and equivocations | negations and equivocations | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) |
| [L15:F6160](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/6160) | 17 | 'not' followed by 'to be' within a few tokens | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/6160) |
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 17 | 'not' + 'to be' phrase detector (latest) |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:2422 de=-1.273 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F2422@17` | ✅ reported | 3 | 3 | Trace the upstream path from L4:F2422 (pos 17, direct_effect=-1.27). This is the… |
| SA-2 | `L4:F4492@17` | ✅ reported | 3 | 4 | Trace the upstream path from L4:F4492 (pos 17, direct_effect=+1.22). This is the… |
| SA-3 | `L3:F1101@17` | ✅ reported | 4 | 3 | Trace the upstream path from L3:F1101 (pos 17, direct_effect=-1.21). This is a s… |
| SA-4 | `L0:F4958@17` | ❌ error | — | — | Trace the upstream path from L0:F4958 (pos 17, direct_effect=+0.68, activation=3… |
| SA-5 | `L16:F12358@17` | ❌ error | — | — | Trace the upstream path from L16:F12358 (pos 17, direct_effect=+0.66, activation… |
| SA-6 | `L2:F16097@2` | ✅ reported | 3 | 8 | Trace the upstream path from L2:F16097 (pos 2, direct_effect=-0.40). This is at … |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F2422 | "negations in other languages like French, Malay, and Croatian" |
| 2 | `get_upstream_features` | L4:F2422@17, k=10 | Emb:" not"@17 (de=16.50) +9 more |
| 3 | `inspect_feature` | L3, F8011 | " a mix of words and code fragments from different languages" |
| 4 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 5 | `get_upstream_features` | L0:F4958@17, k=10 | Emb:" not"@17 (de=32.75) +9 more |
| 6 | `get_upstream_features` | L3:F8011@17, k=10 | Emb:" not"@17 (de=21.00) +9 more |
| 7 | `inspect_feature` | L3, F9803 | "sentences describing scientific studies or experiments, particularly w" |
| 8 | `inspect_feature` | L3, F12079 | "negations and Chinese names" |
| 9 | `get_upstream_features` | L4:F2422@17, k=15 | Emb:" not"@17 (de=16.50) +14 more |
| 10 | `get_upstream_features` | L3:F9803@17, k=10 | Emb:" not"@17 (de=13.62) +9 more |
| 11 | `get_upstream_features` | L3:F12079@17, k=10 | Emb:" There"@15 (de=15.00) +9 more |
| 12 | `inspect_feature` | L1, F14233 | " negative sentiment markers such as "not," "no," "never," and their eq" |

**Findings:** The strongest negative driver of the probe, L4:F2422, is a multilingual negation detector. Its activation is driven primarily by the raw token embedding for " not" (pos 17) which excites a low‑level "not" detector (L0:F4958). That detector feeds into an intermediate negation feature (L3:F8011) that further amplifies the signal. Both intermediate features positively influence L4:F2422, which in tur…

</details>

<details>
<summary><b>SA-2</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F4492 | "negations in various languages" |
| 2 | `get_upstream_features` | L4:F4492@17, k=10 | Emb:" not"@17 (de=18.00) +9 more |
| 3 | `inspect_feature` | L3, F8011 | " a mix of words and code fragments from different languages" |
| 4 | `inspect_feature` | L3, F12079 | "negations and Chinese names" |
| 5 | `get_upstream_features` | L3:F8011@17, k=10 | Emb:" not"@17 (de=21.00) +9 more |
| 6 | `get_upstream_features` | L3:F8011@17, k=10 | Emb:" not"@17 (de=21.00) +9 more |

**Findings:** The strongest positive influence on the probe originates from the input token embedding " not" at position 17 (direct_effect ≈ 18). This token feeds directly into a high‑level negation detector (L4:F4492) and also into two lower‑layer, more specialized negation features (L3:F8011 and L3:F12079). These lower‑layer features themselves are driven by the same " not" token (direct_effect ≈ 21 for L3:F8…

</details>

<details>
<summary><b>SA-3</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F1101 | " error messages and terms indicating absence or negation in software c" |
| 2 | `get_upstream_features` | L3:F1101@17, k=10 | Emb:" not"@17 (de=13.19) +9 more |
| 3 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 4 | `get_upstream_features` | L0:F4958@17, k=10 | Emb:" not"@17 (de=32.75) +9 more |
| 5 | `inspect_feature` | L2, F6993 | "phrases describing uncertainty or difficulty" |
| 6 | `inspect_feature` | L1, F14233 | " negative sentiment markers such as "not," "no," "never," and their eq" |
| 7 | `inspect_feature` | L2, F12021 | ""not" or negative terms, with some bonus for sports-related terms and " |

**Findings:** Tracing upstream from L3:F1101 (pos 17) reveals a cascade of negation-related detectors. The strongest upstream driver is the raw token embedding " not" (positive direct effect 13.19) feeding directly into the layer‑3 feature. The layer‑0 feature 4958 is a dedicated detector for the word "not" and passes a large positive influence to the target. Slightly higher layers (L2:F6993 and L1:F14233) capt…

</details>

<details>
<summary><b>SA-6</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F16097 | "superlative adjectives and the words "test" or "point"" |
| 2 | `get_upstream_features` | L2:F16097@2, k=10 | Emb:" strangest"@2 (de=24.00) +9 more |
| 3 | `inspect_feature` | L0, F12857 | "negative or peculiar adjectives describing something" |
| 4 | `get_upstream_features` | L0:F12857@2, k=5 | Emb:" strangest"@2 (de=11.06) +4 more |
| 5 | `inspect_feature` | L0, F11835 | "terms used in software code such as "assembly", "using", "namespace", " |
| 6 | `get_upstream_features` | L0:F11835@2, k=5 | Emb:"<bos>"@0 (de=-6.25) +4 more |

**Findings:** The target L2:F16097 is a superlative‑adjective detector that fires strongly on the word "strangest". Its strongest upstream driver is the raw embedding of the token "strangest" (direct_effect 24.0), satisfying the requirement to reach a lower‑layer embedding. A secondary upstream contributor is a low‑layer feature (L0:12857) that captures negative/peculiar adjectives like "weird", also driven by …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×7 | L16:12358, L3:12079, L0:11375, L3:2232, L3:9803, L3:3669, L1:15749 |
| 2 | `get_upstream_features` | L16:F12358@17, k=8 → Emb:" not"@17 (de=23.12) +7 more |
| 3 | `get_upstream_features` | L3:F2232@17, k=5 → Emb:" There"@15 (de=8.56) +4 more |
| 4 | `inspect_feature` ×2 | L15:10071, L9:14687 |
| 5 | `get_upstream_features` | L9:F14687@17, k=5 → Emb:" not"@17 (de=7.41) +4 more |
| 6 | `get_upstream_features` | L15:F6160@17, k=5 → Emb:" There"@15 (de=21.50) +4 more |
| 7 | `inspect_feature` ×2 | L8:9880, L3:10742 |

### Build

`build_circuit` → 24 nodes, 48 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 35,559 | 10,174 | 196,203 | 0 | $0.0346 | — | — |
| SA-6 | openai/gpt-oss-120b | 45,109 | 4,185 | 7,584 | 0 | $0.0094 | ✅ 3F/8E | Trace the upstream path from L2:F16097 (pos 2, direct_effect… |
| SA-2 | openai/gpt-oss-120b | 53,092 | 3,834 | 2,592 | 0 | $0.0103 | ✅ 3F/4E | Trace the upstream path from L4:F4492 (pos 17, direct_effect… |
| SA-3 | openai/gpt-oss-120b | 78,078 | 6,015 | 5,056 | 0 | $0.0154 | ✅ 4F/3E | Trace the upstream path from L3:F1101 (pos 17, direct_effect… |
| SA-1 | openai/gpt-oss-120b | 147,472 | 7,686 | 2,656 | 0 | $0.0268 | ✅ 3F/3E | Trace the upstream path from L4:F2422 (pos 17, direct_effect… |
| **Total** | | **359,310** | **31,894** | **214,091** | **0** | **$0.0965** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 31s