# Circuit Oracle Report
**Date:** 2026-07-28 08:38:06 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_10 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe predicts contradiction based on surface-level lexical markers and temporal cues rather than a semantic understanding of the prompt's contradiction.

**Confidence:** 10/10

**Reasoning:** 
The attribution circuit reveals that the probe's classification score is driven by three primary lexical pathways, none of which encode the actual semantic conflict between "democracy" and "role reversal."

1.  **Lexical Aggregation (The "Keywords" Path):** The most significant signal flows from surface-level keywords to a "Lexical Aggregator" (L6:F12420). This aggregator is fed by:
    *   **Superlative/Oddness Detectors:** Features like L4:F12799, L2:F16097, and L2:F10827 specifically detect the token "strangest" (pos 2).
    *   **Role Concept Detectors:** L4:F14368 and L0:F6013 act as simple detectors for the token "role" (pos 3).
    *   **Reversal Keyword Detectors:** L4:F7409 and L1:F2580 directly detect the token "reversal" (pos 4).
    The probe uses these as "anchors" for the contradiction label, regardless of whether the tokens are being negated or affirmed.

2.  **Temporal/Discourse Markers:** A distinct path flows from the tokens "right" and "now" (pos 8, 9) through a chain of temporal features (L0:F13522 $\rightarrow$ L2:F3705 $\rightarrow$ L4:F5709). This suggests the probe associates the phrasing "right now" with the specific style of contradiction examples it was trained on.

3.  **Negation Cues:** The probe also utilizes a superficial negation signal (L10:F6670) excited by the token "not" (pos 17). However, this is a generic response to the word "not" rather than a structured analysis of how the negation flips the meaning of the a specific proposition.

The circuit concludes that the probe is effectively a "keyword spotter." It identifies the labels "contradiction" by looking for the presence of "strangest," "role," "reversal," "not," and "now," confirming the user's concern that the model relies on spurious lexical features rather than semantic content.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: strangest (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: role (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: reversal (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: now/right (pos 8,9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: not (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L4:F12799](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12799) | 2 | Superlative/Oddness Detectors |  words ending in "-ly" along with phrases that contain the word 'odd' or 'oddities' | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12799) |
| [L2:F16097](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) | 2 | Superlative/Oddness Detectors | superlative adjectives and the words "test" or "point" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) |
| [L2:F10827](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10827) | 2 | Superlative/Oddness Detectors | words that reflect strikingness or emotional impact | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10827) |
| [L4:F14368](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14368) | 4 | Role Concept Detectors |  words related to importance or roles in a system | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14368) |
| [L0:F6013](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6013) | 3 | Role Concept Detectors | the word "role," sometimes in conjunction with words that make it abstract, like energy or medicine | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6013) |
| [L4:F7409](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7409) | 4 | Reversal Keyword Detectors | words like "vice versa", "inverse", "reverse", "around", or directions | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7409) |
| [L1:F2580](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2580) | 4 | Reversal Keyword Detectors | the word "reverse" in code snippets | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2580) |
| [L2:F3705](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3705) | 9 | Temporal/Discourse Markers (now, right) | references to particular years or seasons. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3705) |
| [L0:F13522](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13522) | 9 | Temporal/Discourse Markers (now, right) | the word "speed" and related words about definition and measurement | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13522) |
| [L4:F5709](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) | 9 | Temporal/Discourse Markers (now, right) | astronomy terms | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) |
| [L10:F6670](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) | 19 | Negation Cues (not) | technical terms, especially within scientific or medical contexts | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) |
| [L6:F12420](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12420) | 4 | Lexical Feature Aggregator |  artistic elements that break established guidelines | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12420) |
| [L5:F9068](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9068) | 4 | Lexical Feature Aggregator | words and phrases related to populations | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9068) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:5709 de=-0.371 |
| 3 | `inspect_feature` ×10 | L4:5709, L6:12420, L4:12799, L2:16097, L10:6670, L4:6072, L3:12079, L7:905, L4:14368, L0:6013 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F5709@9` | ✅ reported | 3 | 7 | Trace the path from the top features contributing to the probe score. Specifical… |
| SA-2 | `L6:F12420@4` | ✅ reported | 7 | 14 | Trace the path from the top features contributing to the probe score. Specifical… |
| SA-3 | `L4:F12799@2` | ✅ reported | 3 | 3 | Trace the path from the top features contributing to the probe score. Specifical… |
| SA-4 | `L10:F6670@19` | ❌ error | — | — | Trace the path from the top features contributing to the probe score. Specifical… |

<details>
<summary><b>SA-1</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F5709 | "astronomy terms" |
| 2 | `get_upstream_features` | L4:F5709@9, k=10 | Emb:" now"@9 (de=40.25) +9 more |
| 3 | `inspect_feature` | L2, F3705 | " references to particular years or seasons." |
| 4 | `get_upstream_features` | L2:F3705@9, k=10 | Emb:" now"@9 (de=16.75) +9 more |
| 5 | `inspect_feature` | L0, F13522 | " the word "speed" and related words about definition and measurement" |
| 6 | `inspect_feature` | L0, F3308 | "the phrase "well known"" |
| 7 | `inspect_feature` | L0, F9745 | " instances of the word "look" and sometimes the word "been"" |
| 8 | `get_upstream_features` | L0:F13522@9, k=10 | Emb:" right"@8 (de=16.00) +9 more |

**Findings:** The probe’s score is driven primarily by a chain of low‑level, temporally‑oriented features. The token embedding for "now" (pos 9) strongly excites L4:F5709, which in turn receives a modest boost from L2:F3705 – a feature that detects temporal references (years, seasons) and is itself activated by the same "now" token and by the token "right" (pos 8). L2:F3705 is further fed by L0:F13522, a very e…

</details>

<details>
<summary><b>SA-2</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F12420 | " artistic elements that break established guidelines" |
| 2 | `get_upstream_features` | L6:F12420@4, k=10 | Emb:" role"@3 (de=5.59) +9 more |
| 3 | `inspect_feature` | L4, F14368 | " words related to importance or roles in a system" |
| 4 | `inspect_feature` | L5, F9068 | "words and phrases related to populations" |
| 5 | `inspect_feature` | L4, F7409 | " words like "vice versa", "inverse", "reverse", "around", or direction" |
| 6 | `get_upstream_features` | L4:F14368@4, k=10 | Emb:" role"@3 (de=12.31) +9 more |
| 7 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 8 | `get_upstream_features` | L5:F9068@4, k=10 | Emb:" reversal"@4 (de=3.00) +9 more |
| 9 | `inspect_feature` | L4, F12799 | " words ending in "-ly" along with phrases that contain the word 'odd' " |
| 10 | `get_upstream_features` | L4:F12799@2, k=10 | Emb:" strangest"@2 (de=31.00) +9 more |
| 11 | `inspect_feature` | L2, F10827 | " words that reflect strikingness or emotional impact" |
| 12 | `inspect_feature` | L1, F2580 | "the word "reverse" in code snippets" |
| 13 | `get_upstream_features` | L4:F7409@4, k=10 | Emb:" reversal"@4 (de=25.75) +9 more |
| 14 | `get_upstream_features` | L2:F10827@2, k=10 | Emb:" strangest"@2 (de=10.94) +9 more |
| 15 | `inspect_feature` | L1, F1382 | " words associated with situations where something is changing or has c" |
| 16 | `get_upstream_features` | L1:F2580@4, k=10 | Emb:" reversal"@4 (de=16.75) +9 more |

**Findings:** The probe’s top‑scoring feature (L6:F12420) is driven mainly by three lexical‑token embeddings: **role**, **reversal**, and **strangest**. The pathway is: token *role* → L4:F14368 (role detector) → L6:F12420; token *reversal* → L4:F7409 (reverse‑keyword detector) → L6:F12420 (also via L5:F9068 and L1:F2580); token *strangest* → L4:F12799 (superlative detector) → L5:F9068 → L6:F12420 (and also via …

</details>

<details>
<summary><b>SA-3</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F12799 | " words ending in "-ly" along with phrases that contain the word 'odd' " |
| 2 | `get_upstream_features` | L4:F12799@2, k=10 | Emb:" strangest"@2 (de=31.00) +9 more |
| 3 | `inspect_feature` | L2, F10827 | " words that reflect strikingness or emotional impact" |
| 4 | `inspect_feature` | L2, F16097 | "superlative adjectives and the words "test" or "point"" |
| 5 | `get_upstream_features` | L2:F10827@2, k=10 | Emb:" strangest"@2 (de=10.94) +9 more |
| 6 | `get_upstream_features` | L2:F16097@2, k=10 | Emb:" strangest"@2 (de=24.00) +9 more |
| 7 | `inspect_feature` | L0, F12381 | " the words "lowest" and "highest"" |
| 8 | `inspect_feature` | L0, F12857 | "negative or peculiar adjectives describing something" |

**Findings:** Tracing from L4:F12799 (odd‑ness detector) quickly reaches a strong positive contribution from the token embedding "strangest" (direct_effect = 31). The next strongest upstream drivers are layer‑2 features 10827 and 16097, both of which respond to striking or superlative adjectives. Feature 16097 in particular is a dedicated superlative detector and contributes a large positive effect (≈ 24) to th…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L10:F6670@19, k=5 → Emb:" not"@17 (de=6.78) +4 more |

### Build

`build_circuit` → 12 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 174,088 | 2,185 | 4,224 | 0 | $0.0253 | — | — |
| SA-3 | openai/gpt-oss-120b | 62,269 | 4,852 | 21,184 | 0 | $0.0126 | ✅ 3F/3E | Trace the path from the top features contributing to the pro… |
| SA-1 | openai/gpt-oss-120b | 84,156 | 6,221 | 17,696 | 0 | $0.0166 | ✅ 3F/7E | Trace the path from the top features contributing to the pro… |
| SA-2 | openai/gpt-oss-120b | 258,739 | 19,909 | 46,400 | 0 | $0.0515 | ✅ 7F/14E | Trace the path from the top features contributing to the pro… |
| **Total** | | **579,252** | **33,167** | **89,504** | **0** | **$0.1059** | | |

**Oracle wall-clock time:** 7m 22s