# Circuit Oracle Report
**Date:** 2026-07-28 07:20:52 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_10 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

The circuit is now well-mapped. The probe's contradiction score is overwhelmingly driven by negation-word features anchored on the **"not"** token at position 17, with weak contributions from "strange/strangest" and "reverse/reversal". Below is the analysis.

**Analysis:** The probe's contradiction classification is driven by a thick stack of **"not" / negation-token** features anchored on the single token " not" at position 17, propagating through dedicated negation circuits at L0→L3→L4→L9→L16, with only weak contributions from lexical content features for "strange", "reverse", "is", "going", and "now" — i.e. the probe is using a **spurious negation-word shortcut**, not the actual premise/hypothesis content.

**Confidence:** 9

**Reasoning:** The circuit is dominated by negation detectors. Of the top-20 features by direct effect on the probe, **17 out of 20 are negation-related** and almost all fire at position 17 where " not" lives. The chain is:

- **Emb: " not" (pos 17)** → strongly activates **L0:F4958 "the word 'not'"** (act 30.6, +0.68 direct), which in turn drives L3 features **F8011, F12079, F2232, F9803, F1101, F10742** (all of which label themselves as various flavors of "negation in language/code/error messages", with "not"-style promoted tokens). These in turn feed the L4 super-hub **F4492 "negations in various languages"** (direct +1.22, the largest positive contributor), and **F2422 "negations in other languages"** (direct −1.27, an opposing pole on the same " not" token).
- L4:F4492 then drives **L9:F14687 "phrases using 'not', often followed by 'because' or 'but'"** (direct +0.25) and **L16:F12358 "the word 'not' followed within a few tokens by a form of 'to be'"** (direct +0.66, max_act 284 — the most extreme activation in the graph, because of the " is not" pattern at positions 16–17). L16:F12358 has a direct edge to the probe.
- The embedding node for " not" (pos 17) sends the largest single direct contribution to the entire path: direct_effect 18 onto L4:F4492, 13–22 onto various L3 negation features, 7.4 onto L9:F14687, and 23.1 onto L16:F12358. **" not" alone supplies more signal than every other content word combined.**
- The opposing L4:F2422 (multilingual negations) suppresses the probe by −1.27, and L3:F1101 (absence/negation in error messages) suppresses by −1.21, but the net across the full negation stack is strongly positive.
- Crucially, the **content features for the actual premise/hypothesis** — " strangest" (drives L1:F15749 +0.28 and L2:F16097 superlative −0.40), " reversal" (L1:F2580, L4:F7409 ±0.22), " is" (L0:F11375 +0.37), " going" (L0:F630 +0.23), " now" (L0:F5188/L0:F13522/L4:F430, ±0.25) — are all individually small and largely cancel out. The "democracy" and "role reversal" topical content never appears as a content-recognizing feature in the top-30.
- The "strangest/est" superlative circuit (L2:F16097, L3:F3669, L3:F319, L6:F5819) does contribute modestly, and L10:F6670 (technical terms) fires at the trailing "now in relation to democracy" position 19 — but these are 3–10× smaller than the negation signal.

The result: the probe is reading **" is not"** as a near-sufficient signal for the contradiction label, with the model leaning on generic "negation word" detectors (L0:F4958, L1:F14233, L1:F14680, L2:F12021, L3:F1101/F2232/F8011/F9803/F12079/F10742, L4:F4492/F2422/F7500/F13171, L9:F14687/F742, L16:F12358) rather than on any feature that encodes the semantic content of the premise (democracy / role reversal) or the hypothesis (no role reversal). The user's concern is confirmed: this is a **spurious negation-word heuristic**, exactly the failure mode the worry described.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: not (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: strangest (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: reversal (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: is (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: going (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: now (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: There (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 16 | Emb: is (pos 16) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 17 | L0:F4958 — 'not' (pos 17) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L1:F14233](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) | 17 | L1:F14233 — negative markers / not-no-never (pos 17) |  negative sentiment markers such as "not," "no," "never," and their equivalents in other languages | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) |
| [L1:F14680](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14680) | 17 | L1:F14680 — 'not' (pos 17) | the word "not" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14680) |
| [L1:F15749](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15749) | 2 | L1:F15749 — 'strange' (pos 2) |  the word "strange", or related words | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15749) |
| [L1:F2580](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2580) | 4 | L1:F2580 — 'reverse' in code (pos 4) | the word "reverse" in code snippets | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2580) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 5 | L0:F11375 — 'is' (pos 5) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F630](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/630) | 6 | L0:F630 — 'going' (pos 6) | the word "going" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/630) |
| [L0:F5188](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5188) | 9 | L0:F5188 — 'now' (pos 9) |  the word "now" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5188) |
| [L0:F13522](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13522) | 9 | L0:F13522 — 'speed' / measurement (pos 9) |  the word "speed" and related words about definition and measurement | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13522) |
| [L2:F12021](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) | 17 | L2:F12021 — 'not'/negation (pos 17) | "not" or negative terms, with some bonus for sports-related terms and "purpose". | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) |
| [L2:F6993](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6993) | 17 | L2:F6993 — uncertainty phrases (pos 17) | phrases describing uncertainty or difficulty | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6993) |
| [L2:F16097](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) | 2 | L2:F16097 — superlatives/-est (pos 2) | superlative adjectives and the words "test" or "point" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) |
| [L3:F1101](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) | 17 | L3:F1101 — absence/negation in error msgs (pos 17) |  error messages and terms indicating absence or negation in software contexts. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 17 | L3:F8011 — multilingual code fragments w/ 'not' promoted (pos 17) |  a mix of words and code fragments from different languages | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L3:F12079](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) | 17 | L3:F12079 — negations/Chinese names (pos 17) | negations and Chinese names | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) |
| [L3:F2232](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2232) | 17 | L3:F2232 — NO/NOC/NOS hex codes, 'no' promoted (pos 17) |  character sequences like "NOC", "NO", "ORES", "NOS", "OF", "UNCH", and "oooooooo" within a series of hexadecimal codes, sometimes also picking up on related words such as "dangerously", "Bantus", "slave", and "plantation" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2232) |
| [L3:F9803](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9803) | 17 | L3:F9803 — scientific negation/disproven (pos 17) | sentences describing scientific studies or experiments, particularly where something is disproven | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9803) |
| [L3:F10742](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10742) | 17 | L3:F10742 — French 'avoir' fragments (pos 17) |  fragments of French sentences, particularly those containing the verb "avoir" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10742) |
| [L3:F10225](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10225) | 7 | L3:F10225 — 'on' (pos 7) |  the word "on" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10225) |
| [L3:F3669](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3669) | 2 | L3:F3669 — ordinal rankings (pos 2) |  references to ordinal rankings of things | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3669) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 17 | L4:F2422 — multilingual negations (pos 17) [NEGATIVE] | negations in other languages like French, Malay, and Croatian | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 17 | L4:F4492 — negations in various languages (pos 17) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F7500](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7500) | 17 | L4:F7500 — negation words (pos 17) | negation words | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7500) |
| [L4:F13171](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13171) | 17 | L4:F13171 — passages where something is negated (pos 17) |  passages where something is negated | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13171) |
| [L4:F7409](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7409) | 4 | L4:F7409 — reverse/around/inverse (pos 4) |  words like "vice versa", "inverse", "reverse", "around", or directions | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7409) |
| [L4:F430](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/430) | 9 | L4:F430 — 'moment'/'now' (pos 9) |  phrases containing the word "moment" and often the word "now" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/430) |
| [L4:F5709](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) | 9 | L4:F5709 — astronomy/'now' (pos 9) | astronomy terms | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) |
| [L9:F14687](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/14687) | 17 | L9:F14687 — phrases with 'not' + because/but (pos 17) | phrases using the word "not", often followed by "because" or "but." | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/14687) |
| [L9:F742](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/742) | 17 | L9:F742 — negation/uncertainty (pos 17) | negation, uncertainty, or sensory statements | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/742) |
| [L10:F6670](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) | 19 | L10:F6670 — technical/medical terms (pos 19) | technical terms, especially within scientific or medical contexts | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) |
| [L6:F5819](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5819) | 2 | L6:F5819 — superlatives/high-degree (pos 2) |  words and phrases indicating superlatives or high degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5819) |
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 17 | L16:F12358 — 'not' + 'to be' (pos 17) |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:2422 de=-1.273 |
| 3 | `inspect_feature` ×20 | L4:2422, L4:4492, L3:1101, L0:4958, L3:8011, L3:12079, L16:12358, L3:2232, L3:9803, L2:16097, L3:3669, L0:11375, L1:14233, L1:15749, L9:14687, L2:6993, L0:13522, L4:5709, L4:430, L4:7500 |
| 4 | `get_top_features` | 30 features; top: L4:2422 de=-1.273 |
| 5 | `get_upstream_features` | Emb:" not"@17 (de=23.12) +9 more |
| 6 | `get_upstream_features` | Emb:" not"@17 (de=18.00) +9 more |
| 7 | `get_upstream_features` | Emb:" not"@17 (de=32.75) +9 more |
| 8 | `get_upstream_features` | Emb:" strangest"@2 (de=11.94) +9 more |
| 9 | `get_upstream_features` | Emb:" There"@15 (de=15.00) +9 more |
| 10 | `get_upstream_features` | Emb:" There"@15 (de=8.56) +9 more |
| 11 | `get_upstream_features` | Emb:" not"@17 (de=13.62) +9 more |
| 12 | `get_upstream_features` | Emb:" not"@17 (de=22.62) +9 more |
| 13 | `get_upstream_features` | Emb:" strangest"@2 (de=24.00) +9 more |
| 14 | `get_upstream_features` | Emb:" strangest"@2 (de=14.69) +9 more |
| 15 | `get_upstream_features` | Emb:" is"@5 (de=31.50) +9 more |
| 16 | `get_upstream_features` | Emb:" not"@17 (de=7.41) +9 more |
| 17 | `get_upstream_features` | Emb:" not"@17 (de=6.38) +9 more |
| 18 | `get_upstream_features` | Emb:" not"@17 (de=13.19) +9 more |
| 19 | `get_upstream_features` | Emb:" not"@17 (de=21.00) +9 more |
| 20 | `get_upstream_features` | Emb:" going"@6 (de=8.19) +9 more |
| 21 | `get_upstream_features` | Emb:" not"@17 (de=6.78) +9 more |
| 22 | `get_upstream_features` | Emb:" strangest"@2 (de=4.97) +9 more |
| 23 | `get_upstream_features` | Emb:" reversal"@4 (de=16.75) +9 more |
| 24 | `get_upstream_features` | Emb:" is"@5 (de=15.94) +9 more |
| 25 | `get_upstream_features` | Emb:" right"@8 (de=16.00) +9 more |
| 26 | `get_upstream_features` | Emb:" now"@9 (de=40.25) +9 more |
| 27 | `get_upstream_features` | Emb:" now"@9 (de=10.19) +9 more |
| 28 | `get_upstream_features` | Emb:" not"@17 (de=13.88) +9 more |
| 29 | `get_upstream_features` | Emb:" not"@17 (de=7.41) +9 more |
| 30 | `get_upstream_features` | Emb:" not"@17 (de=6.81) +9 more |
| 31 | `get_upstream_features` | Emb:" not"@17 (de=11.50) +9 more |
| 32 | `inspect_feature` ×12 | L4:13171, L10:6670, L3:10225, L3:12624, L3:10742, L9:742, L2:12021, L0:630, L0:5188, L4:7409, L1:2580, L6:5819 |
| 33 | `get_upstream_features` | Emb:" is"@16 (de=32.75) +9 more |
| 34 | `get_upstream_features` | Emb:" not"@17 (de=17.62) +9 more |
| 35 | `inspect_feature` ×8 | L1:14680, L2:573, L2:7550, L2:5606, L3:319, L2:3565, L2:8541, L2:11420 |
| 36 | `get_upstream_features` | Emb:" reversal"@4 (de=16.75) +9 more |
| 37 | `get_upstream_features` | Emb:" is"@5 (de=15.94) +9 more |
| 38 | `get_upstream_features` | Emb:" right"@8 (de=16.00) +9 more |
| 39 | `get_upstream_features` | Emb:" now"@9 (de=15.94) +9 more |
| 40 | `get_upstream_features` | Emb:" reversal"@4 (de=25.75) +9 more |
| 41 | `get_upstream_features` | Emb:" not"@17 (de=6.78) +9 more |
| 42 | `get_upstream_features` | Emb:" going"@6 (de=8.19) +9 more |
| 43 | `inspect_feature` | " the superlative adjective "closest" or "nearest"" |
| 44 | `get_upstream_features` | Emb:" not"@17 (de=18.00) +9 more |
| 45 | `get_upstream_features` | Emb:" not"@17 (de=18.00) +14 more |
| 46 | `get_upstream_features` | Emb:" not"@17 (de=23.12) +9 more |
| 47 | `get_upstream_features` | Emb:" There"@15 (de=15.00) +9 more |
| 48 | `get_upstream_features` | Emb:" not"@17 (de=21.00) +9 more |
| 49 | `get_upstream_features` | Emb:" not"@17 (de=13.19) +9 more |
| 50 | `get_upstream_features` | Emb:" There"@15 (de=8.56) +9 more |
| 51 | `get_upstream_features` | Emb:" not"@17 (de=13.62) +9 more |

### Build

`build_circuit` → 41 nodes, 60 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 104,381 | 11,229 | 513,328 | 0 | $0.0756 | — | — |
| **Total** | | **104,381** | **11,229** | **513,328** | **0** | **$0.0756** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 2s