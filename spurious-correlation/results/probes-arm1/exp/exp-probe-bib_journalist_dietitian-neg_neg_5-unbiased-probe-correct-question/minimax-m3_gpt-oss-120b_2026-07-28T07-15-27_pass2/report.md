# Circuit Oracle Report
**Date:** 2026-07-28 07:15:27 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of "reporter" is driven almost entirely by a clean, semantically coherent journalism/media circuit anchored on the literal token " reporter" at position 66 — *not* by spurious gender markers or other superficial cues.

**Confidence:** 8

**Reasoning:** The circuit is a textbook profession-indicator pathway, not a gender-spurious one:

- **Source token (Emb: reporter, pos 66).** This is the dominant input. The " reporter" token embedding feeds every layer of the journalism supernode with the largest upstream direct effects (e.g., 28.25 → L19:F2486, 18.75 → L14:F4420, 26.625 → L4:F13253, 48.25 → L18:F14663). This is the unambiguous profession word.

- **Early/mid journalism features (L4–L9, pos 66)** are all genuine profession detectors with low frac_nonzero and clean semantic labels: L4:F13253 ("things related to journalism and the media", frac=0.0065), L4:F661 ("reports, documentaries, television coverage of news", frac=0.009), L6:F12712 ("titles of editors and publishers in scientific publications", frac=0.017), L7:F13646 ("news reporting and journalism", frac=0.0076), L7:F9092 ("broadcast journalism", frac=0.0095), L8:F8855 ("mentions of news reporters and news reporting", frac=0.0085). They fire specifically on the " reporter" token and project strongly upward.

- **Late-layer journalism features (L14–L19, pos 66)** are the probe's direct inputs: L14:F4420 ("journalism and newspapers", frac=0.0165, promotes "journalist/reporter/reporter"), L18:F14663 ("variations of 'report'", frac=0.0071, very high activation 56), and L19:F2486 ("journalistic sources and news outlets", frac=0.029, promotes "reporter/Reporter/Reporting"). All three are *negative* direct_effect on the probe here (the model is pushing the probe score *down* on the residual at pos 66 once profession is fully represented elsewhere — typical suppression), but they are still part of the profession circuit, not noise.

- **Where is the gender signal?** L0:F1069 ("references to a male person, particularly 'He'/'His'", frac=0.0078) does appear in the top-20 list, but at position 7 with direct_effect -0.089 and **it is not used by the upstream trace into the late-layer features** — none of the journalism supernodes at L7+ receive positive input from gender-pronoun features. The pronoun appears in the top features only because L0 features carry direct effects into the probe direction that aren't mediated through the journalism circuit. They are off-pathway noise on the residual stream, not drivers of the classification.

- **Auxiliary embeddings.** " freelancer" (pos 21), " obtained" (pos 2), and " ongoing" (pos 62) feed into the late-layer journalism features, consistent with the text describing the subject as a freelancer/reporter — these are additional profession-supporting context, not gender cues.

The user's concern that the circuit relies on spurious gender features rather than genuine profession indicators is **not supported** by this attribution graph. The dominant path is a tight, embedding-anchored journalism/reporter feature stack (L4 → L7 → L8 → L14 → L18 → L19) all firing on the token " reporter". Gender-pronoun features are present in the broad top-20 of direct probe effects at L0 but are not upstream drivers of the profession-indicating late-layer features.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 66 | Emb: reporter (pos 66) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: freelancer (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: obtained (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 62 | Emb: ongoing (pos 62) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 0 | Emb: <bos> (pos 0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 66 | Early journalism/media features (L4-L6) |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L4:F661](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/661) | 66 | Early journalism/media features (L4-L6) |  words and phrases used when referring to reports, documentaries, and television coverage of news | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/661) |
| [L6:F12712](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) | 66 | Early journalism/media features (L4-L6) |  titles of editors and publishers in scientific publications | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 66 | Mid journalism/news features (L7-L9) |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 66 | Mid journalism/news features (L7-L9) |  words and phrases associated with broadcast journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 66 | Mid journalism/news features (L7-L9) |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L9:F2845](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2845) | 66 | Mid journalism/news features (L7-L9) |  mentions of news organizations and journalists | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2845) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 66 | Late-layer journalism features (L14-L19) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L18:F14663](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14663) | 66 | Late-layer journalism features (L14-L19) | variations of the word "report." | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14663) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 66 | Late-layer journalism features (L14-L19) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe classification score (output logit) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:4420 de=-0.196 |
| 3 | `inspect_feature` ×18 | L14:4420, L19:2486, L4:13253, L0:4874, L0:6051, L0:8642, L0:14824, L0:8974, L0:8061, L0:13864, L6:12712, L0:9397, L0:926, L0:5099, L0:6786, L0:6127, L7:13646, L0:1069 |
| 4 | `get_upstream_features` | Emb:" reporter"@66 (de=18.75) +14 more |
| 5 | `get_upstream_features` | Emb:" reporter"@66 (de=28.25) +14 more |
| 6 | `get_upstream_features` | Emb:" reporter"@66 (de=15.12) +14 more |
| 7 | `get_upstream_features` | Emb:" reporter"@66 (de=26.62) +14 more |
| 8 | `inspect_feature` ×8 | L8:8855, L7:9092, L7:9521, L4:661, L9:7435, L9:2845, L18:14663, L17:5218 |
| 9 | `get_upstream_features` | Emb:" reporter"@66 (de=48.25) +9 more |
| 10 | `get_upstream_features` | Emb:" reporter"@66 (de=28.25) +9 more |

### Build

`build_circuit` → 9 nodes, 9 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 56,480 | 3,602 | 206,507 | 0 | $0.0337 | — | — |
| **Total** | | **56,480** | **3,602** | **206,507** | **0** | **$0.0337** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 8s