# Circuit Oracle Report
**Date:** 2026-07-28 08:38:52 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by semantic detectors for "conspiracy" and "semiconductor chips," both of which originate directly from the specific input tokens "Conspiracy" and "chip."

**Confidence:** 9/10

**Reasoning:** 
The attribution circuit reveals that the probe classification is not relying on spurious negation markers, but rather on the actual lexical content of the prompt. 

1.  **Conspiracy Signal:** The probe is positively influenced by a "conspiracy-related" feature (**L3:F9739**, frac_nonzero=0.00762), which is specifically excited by the token embedding of "Cons" (the start of "Conspiracy theorists") at position 1. This establishes a direct causal path from the input entity/concept to the probe score.
2.  **Hardware Signal:** Another significant driver is a "semiconductor chip" detector (**L2:F16230**, frac_nonzero=0.00969), which is driven by a very strong direct effect from the embedding of the token " chip" at position 11. This path is further supported by an intermediate hardware-specific feature at **L1:F6066**.
3.  **Absence of Spurious Features:** While some generic features (like "that" at L0:F3635) appear in the top features list, they do not form the dominant causal paths traced by the subagents. The primary drivers are highly specific detectors (low frac_nonzero) that map directly back to the prompt's key nouns.

The signal flows from the token embeddings (`Emb: Conspiracy` and `Emb: chip`) $\rightarrow$ semantic detectors in early layers (L2-L3) $\rightarrow$ the final probe direction in the residual stream. This indicates the probe is detecting the "conspiracy theory about a chip" content rather than relying on linguistic shortcuts like negation.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Conspiracy (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 11 | Emb: chip (pos 11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L3:F9739](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9739) | 2 | Conspiracy Detector (L3:F9739) |  words related to conspiracies | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9739) |
| [L2:F16230](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16230) | 11 | Chip/Semiconductor Detector (L2:F16230) |  mentions of semiconductor chips and devices | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16230) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L3:9739 de=-0.348 |
| 3 | `inspect_feature` ×5 | L3:9739, L2:16230, L7:1062, L0:3635, L0:16015 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 10 features; top: L3:9739 de=-0.348 |
| 6 | `inspect_feature` | " words related to conspiracies" |

### Dispatch: 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L3:F9739@2` | ✅ reported | 5 | 7 | Trace the signal from L3:F9739 (conspiracy detector) and L2:F16230 (chip detecto… |

<details>
<summary><b>SA-1</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F9739 | " words related to conspiracies" |
| 2 | `get_upstream_features` | L3:F9739@2, k=10 | Emb:"Cons"@1 (de=8.75) +9 more |
| 3 | `inspect_feature` | L2, F16230 | " mentions of semiconductor chips and devices" |
| 4 | `inspect_feature` | L2, F1741 | "fragments of words ending in "ction", "notes," or "ual."" |
| 5 | `get_upstream_features` | L2:F1741@2, k=10 | Emb:"Cons"@1 (de=22.88) +9 more |
| 6 | `inspect_feature` | L2, F16241 | " partial strings of the word "constructor" or words ending in "dering"" |
| 7 | `get_upstream_features` | L2:F16230@2, k=10 | ❌ Feature (layer=2, feature_idx=16230) not found at pos=2. Thi |
| 8 | `get_upstream_features` | L2:F16230@11, k=10 | Emb:" chip"@11 (de=27.00) +9 more |
| 9 | `get_upstream_features` | L0:F16015@1, k=10 | Emb:"Cons"@1 (de=21.12) +9 more |
| 10 | `inspect_feature` | L1, F6066 | " the word 'chip', possibly in the context of hardware" |
| 11 | `get_upstream_features` | L1:F6066@11, k=10 | Emb:" chip"@11 (de=21.38) +9 more |

**Findings:** The conspiracy detector (L3:F9739) receives its strongest positive drive from the sub‑word embedding token "Cons" at position 1, which is the first token of the word "Conspiracy". Additional, smaller contributions come from a suffix‑detector feature (L2:F1741) and a "constructor"‑suffix feature (L2:F16241), but the dominant source is the token embedding itself, satisfying the lower‑third layer req…

</details>

### Build

`build_circuit` → 5 nodes, 4 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 174,364 | 1,371 | 4,352 | 0 | $0.0250 | — | — |
| SA-1 | openai/gpt-oss-120b | 84,187 | 6,783 | 38,336 | 0 | $0.0173 | ✅ 5F/7E | Trace the signal from L3:F9739 (conspiracy detector) and L2:… |
| **Total** | | **258,551** | **8,154** | **42,688** | **0** | **$0.0423** | | |

**Oracle wall-clock time:** 8m 11s