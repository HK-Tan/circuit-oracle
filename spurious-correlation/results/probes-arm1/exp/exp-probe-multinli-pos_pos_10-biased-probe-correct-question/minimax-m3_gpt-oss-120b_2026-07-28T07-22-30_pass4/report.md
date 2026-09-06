# Circuit Oracle Report
**Date:** 2026-07-28 07:22:30 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_10 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction score is driven almost entirely by a single negation token ("not" at position 17) and its downstream lexical/structural fallout — the L0–L16 features at position 17 are uniformly "not"/"negation" detectors across many languages, and the "There is" preamble (pos 15–16) feeds in only via the same negation-detector stack. No semantic content (entities, "role reversal", "democracy", "strangest") is read.

**Confidence:** 9

**Reasoning:** Every feature along the position-17 path encodes a negation cue. At the bottom of the circuit, the **Emb: " not" (pos 17)** node feeds **L0:F4958** (frac_nonzero 0.018; "the word 'not'") with direct_effect 8.13, which in turn drives **L1:F14233** ("negative sentiment markers: not/no/never in other languages"), **L2:F12021** ("not or negative terms"), and **L2:F6993** ("phrases describing uncertainty or difficulty"). These early detectors funnel into the mid-layer stack at pos 17 — **L3:F1101** ("absence/negation in software", suppresses the "not" token), **L3:F8011** (promoted tokens = "not, NOT, Not, ikke, nicht, geen" — a pure cross-lingual negation detector, frac_nonzero 0.003), **L3:F12079** ("negations and Chinese names"), **L3:F2232** ("NOC/NO/Not Found" — promoted "no/No/NO/nothing"), **L3:F9803** ("scientific studies disproven"), **L4:F2422** ("negations in other languages: French/Malay/Croatian"), **L4:F4492** ("negations in various languages"), and **L4:F7500** ("negation words") — all firing on the same single "not" position. At the late layers, **L8:F9880** ("doubt, negation, or uncertainty"), **L9:F14687** ("'not' often followed by 'because' or 'but'"), **L15:F6160** ("'is there'", promoted "no/kein/There"), **L15:F10071** ("negations and equivocations", fires on "not" with max_activation 190), and the dominant **L16:F12358** ("the word 'not' followed within a few tokens by a form of 'to be'", max_activation 284) integrate this stream and feed the probe output with the largest direct effects. The signal to the probe is overwhelmingly *because* of the literal word "not" in the hypothesis — the "is" token at pos 16 contributes only because the late L15–L16 features fire on the "not...is" pattern. The " There" embedding contributes through the same negation path, and the only non-position-17 features reaching the output — L2:F16097 ("superlative/test/point") and L3:F3669 ("ordinal rankings") on pos 2 ("strangest"), L1:F15749 ("strange") on pos 2, L0:F13522 ("speed") on pos 9, L0:F11375 ("is") on pos 5 — have small effects and are not part of the dominant negation cascade. **This confirms the user's concern: the probe classifies the premise/hypothesis pair as contradiction based on a shallow negation-lexicon feature at the "not" position, not on any comparison of semantic content (democracy, role reversal, strangeness).** The exact "not … is" pattern that triggers L16:F12358 is itself a classic contradiction cue, but it is encoded as a *lexical pattern*, not as the result of actually reading the two sentences' meanings.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: ' not' (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 16 | Emb: ' is' (pos 16) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: ' There' (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: ' reversal' (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 17 | Early-layer 'not' detectors (L0–L2) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L1:F14233](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) | 17 | Early-layer 'not' detectors (L0–L2) |  negative sentiment markers such as "not," "no," "never," and their equivalents in other languages | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) |
| [L2:F12021](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) | 17 | Early-layer 'not' detectors (L0–L2) | "not" or negative terms, with some bonus for sports-related terms and "purpose". | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) |
| [L2:F6993](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6993) | 17 | Early-layer 'not' detectors (L0–L2) | phrases describing uncertainty or difficulty | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6993) |
| [L2:F16097](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) | 2 | Early-layer 'not' detectors (L0–L2) | superlative adjectives and the words "test" or "point" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) |
| [L3:F3669](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3669) | 2 | Early-layer 'not' detectors (L0–L2) |  references to ordinal rankings of things | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3669) |
| [L1:F15749](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15749) | 2 | Early-layer 'not' detectors (L0–L2) |  the word "strange", or related words | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15749) |
| [L0:F13522](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13522) | 9 | Early-layer 'not' detectors (L0–L2) |  the word "speed" and related words about definition and measurement | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13522) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 5 | Early-layer 'not' detectors (L0–L2) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L3:F1101](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) | 17 | Mid-layer negation/uncertainty features (L3–L4, pos 17) |  error messages and terms indicating absence or negation in software contexts. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 17 | Mid-layer negation/uncertainty features (L3–L4, pos 17) |  a mix of words and code fragments from different languages | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L3:F12079](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) | 17 | Mid-layer negation/uncertainty features (L3–L4, pos 17) | negations and Chinese names | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) |
| [L3:F2232](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2232) | 17 | Mid-layer negation/uncertainty features (L3–L4, pos 17) |  character sequences like "NOC", "NO", "ORES", "NOS", "OF", "UNCH", and "oooooooo" within a series of hexadecimal codes, sometimes also picking up on related words such as "dangerously", "Bantus", "slave", and "plantation" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2232) |
| [L3:F9803](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9803) | 17 | Mid-layer negation/uncertainty features (L3–L4, pos 17) | sentences describing scientific studies or experiments, particularly where something is disproven | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9803) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 17 | Mid-layer negation/uncertainty features (L3–L4, pos 17) | negations in other languages like French, Malay, and Croatian | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 17 | Mid-layer negation/uncertainty features (L3–L4, pos 17) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F7500](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7500) | 17 | Mid-layer negation/uncertainty features (L3–L4, pos 17) | negation words | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7500) |
| [L8:F9880](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9880) | 17 | Late-layer negation + 'is there' integration (L8–L16) |  phrases expressing doubt, negation, or uncertainty | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9880) |
| [L9:F14687](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/14687) | 17 | Late-layer negation + 'is there' integration (L8–L16) | phrases using the word "not", often followed by "because" or "but." | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/14687) |
| [L15:F6160](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/6160) | 17 | Late-layer negation + 'is there' integration (L8–L16) |  occurrences of "is there" | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/6160) |
| [L15:F10071](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) | 17 | Late-layer negation + 'is there' integration (L8–L16) | negations and equivocations | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) |
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 17 | Late-layer negation + 'is there' integration (L8–L16) |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 17 | Probe (contradiction direction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:2422 de=-1.273 |
| 3 | `inspect_feature` ×20 | L4:2422, L4:4492, L3:1101, L0:4958, L3:12079, L3:8011, L16:12358, L3:2232, L3:9803, L2:16097, L0:11375, L0:13522, L3:3669, L1:14233, L1:15749, L9:14687, L2:6993, L4:5709, L4:430, L4:7500 |
| 4 | `get_upstream_features` | Emb:" not"@17 (de=23.12) +9 more |
| 5 | `get_upstream_features` | Emb:" not"@17 (de=13.19) +7 more |
| 6 | `inspect_feature` ×3 | L2:12021, L15:10071, L15:6160 |
| 7 | `get_upstream_features` | Emb:" not"@17 (de=18.00) +7 more |
| 8 | `get_upstream_features` | Emb:" not"@17 (de=16.50) +7 more |
| 9 | `get_upstream_features` | Emb:" not"@17 (de=32.75) +7 more |
| 10 | `get_upstream_features` | Emb:" There"@15 (de=15.00) +4 more |
| 11 | `get_upstream_features` | Emb:" There"@15 (de=21.50) +4 more |
| 12 | `inspect_feature` ×2 | L3:10742, L8:9880 |

### Dispatch: 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F12358@17` | ❌ error | — | — | Trace the path upstream from L16:F12358 (labeled 'not followed by is') to determ… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L3:F8011@17, k=5 → Emb:" not"@17 (de=21.00) +4 more |
| 2 | `get_upstream_features` | L3:F9803@17, k=5 → Emb:" not"@17 (de=13.62) +4 more |
| 3 | `get_upstream_features` | L15:F10071@17, k=5 → Emb:" not"@17 (de=11.62) +4 more |

### Build

`build_circuit` → 8 nodes, 7 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 49,973 | 4,529 | 407,773 | 0 | $0.0449 | — | — |
| **Total** | | **49,973** | **4,529** | **407,773** | **0** | **$0.0449** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 29s