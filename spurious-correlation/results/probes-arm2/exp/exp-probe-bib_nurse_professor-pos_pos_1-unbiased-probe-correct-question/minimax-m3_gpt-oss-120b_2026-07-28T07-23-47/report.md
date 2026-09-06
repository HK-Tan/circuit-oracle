# Circuit Oracle Report
**Date:** 2026-07-28 07:23:47 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven primarily by genuine profession/specialty token signals (the subword tokens of "Perioperative" and "nurses") flowing through a coherent mid-to-late-layer concept circuit, with only a negligible contribution from the gendered pronoun "she".

**Confidence:** 8

**Reasoning:** The circuit traces from token embeddings upward through three supernodes feeding the output logit node (layer 26, probe direction).

The dominant signal originates from the **token embeddings of " Perio" (pos 13), "perative" (pos 14), and " nurses" (pos 15)** — the actual profession name tokens. These embeddings feed into the early-layer lexical supernode (L0–L4: features F15437, F15901, F4665, F11037, F8751, F8736, F9757) which encode subword/lexical patterns. The " nurses" embedding has the largest direct effect on most downstream features (e.g., 19.25→F15437, 16.125→F15267, 14.875→F15901, 42→F13596, 15.4375→F4665).

The mid-layer supernode (L6–L8) acts as a "nurse concept" aggregator. Notably, **F15267 (L6)** is the strongest mid-layer driver (direct_effect 0.158 to the logit, 23.125 activation), with its primary upstream being the " nurses" embedding (16.125) and "perative" (4.375) — i.e., it detects the joint occurrence of the profession-name subwords. F210, F3979, F8194 (L7) and F16339 (L8) contribute additional positive signal (all anchored on " nurses" + "perative" embeddings).

The late-layer supernode (L14–L20) integrates these signals: **F3985 (L14)** receives direct effects of 10.625 from " nurses" and 1.914 from "perative" embeddings, and feeds the logit with direct_effect 0.163 (strongest single positive contributor). **F13596 (L18)** is driven overwhelmingly by the " nurses" embedding (direct_effect 42) and feeds the logit with 0.098. F14457 and F4927 (L20) further consolidate the "Perioperative" subword signal at pos 14.

**Regarding the gender-spurious-feature concern:** The " she" token (pos 7) appears in the circuit but with very small effects — direct_effects of only ~0.96–2.375 on downstream features, compared to the " nurses" embedding's 10–42. The pronoun is not amplified by any feature specifically firing on it; the model's representation of the profession is built almost entirely from the profession-name subword tokens. The probe is therefore using a **legitimate profession-indicator signal** (the literal "Perioperative" / "nurses" tokens), not a spurious gender feature. The user's hypothesis is not supported by this circuit.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: ' nurses' (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: 'perative' (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: ' Perio' (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: ' she' (pos 7) — minor gender signal | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L2:F15437](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15437) | 15 | Early-layer lexical features (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15437) |
| [L3:F15901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) | 15 | Early-layer lexical features (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 14 | Early-layer lexical features (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 15 | Early-layer lexical features (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L4:F9757](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) | 1 | Early-layer lexical features (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 15 | Early-layer lexical features (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L4:F8751](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8751) | 15 | Early-layer lexical features (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8751) |
| [L4:F8736](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8736) | 2 | Early-layer lexical features (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8736) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 14 | Mid-layer 'nurse' concept detectors (L6-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 15 | Mid-layer 'nurse' concept detectors (L6-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 15 | Mid-layer 'nurse' concept detectors (L6-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 15 | Mid-layer 'nurse' concept detectors (L6-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L7:F8194](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8194) | 15 | Mid-layer 'nurse' concept detectors (L6-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8194) |
| [L8:F16339](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) | 14 | Mid-layer 'nurse' concept detectors (L6-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) |
| [L8:F16339](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) | 15 | Mid-layer 'nurse' concept detectors (L6-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 14 | Late-layer profession/specialty features (L14-L20) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 15 | Late-layer profession/specialty features (L14-L20) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 14 | Late-layer profession/specialty features (L14-L20) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 15 | Late-layer profession/specialty features (L14-L20) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L18:F14457](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14457) | 14 | Late-layer profession/specialty features (L14-L20) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14457) |
| [L20:F4927](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) | 14 | Late-layer profession/specialty features (L14-L20) | — | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:3985 de=0.163 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@15` | ❌ error | — | — | Trace upstream from L14:F3985 at position 15. This is a top driver of the probe … |
| SA-2 | `L6:F15267@15` | ❌ error | — | — | Trace upstream from L6:F15267 at position 15. This is a strong positive driver o… |
| SA-3 | `L18:F13596@15` | ❌ error | — | — | Trace upstream from L18:F13596 at position 15. This is a strong positive driver … |
| SA-4 | `L8:F16339@15` | ❌ error | — | — | Trace upstream from L8:F16339 at position 15. This is a positive driver of the p… |
| SA-5 | `L4:F4665@14` | ❌ error | — | — | Trace upstream from L4:F4665 at position 14. This is a positive driver of the pr… |
| SA-6 | `L20:F4927@14` | ❌ error | — | — | Trace upstream from L20:F4927 at position 14. This is a positive driver of the p… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F3985@15, k=10 → Emb:" nurses"@15 (de=10.62) +9 more |
| 2 | `get_upstream_features` | L6:F15267@15, k=10 → Emb:" nurses"@15 (de=16.12) +9 more |
| 3 | `get_upstream_features` | L18:F13596@15, k=10 → Emb:" nurses"@15 (de=42.00) +9 more |
| 4 | `get_upstream_features` | L8:F16339@15, k=10 → Emb:" nurses"@15 (de=4.72) +9 more |
| 5 | `get_upstream_features` | L4:F4665@14, k=10 → Emb:"perative"@14 (de=15.44) +9 more |
| 6 | `get_upstream_features` | L20:F4927@14, k=10 → L18:F13596 (de=14.31) +9 more |
| 7 | `get_upstream_features` | L7:F210@15, k=10 → Emb:" nurses"@15 (de=11.38) +9 more |
| 8 | `get_upstream_features` | L7:F3979@15, k=10 → L6:F15267 (de=7.97) +9 more |
| 9 | `get_upstream_features` | L3:F15901@15, k=10 → Emb:" nurses"@15 (de=14.88) +9 more |
| 10 | `get_upstream_features` | L4:F9757@1, k=10 → Emb:"<bos>"@0 (de=14.00) +9 more |
| 11 | `get_upstream_features` | L2:F15437@15, k=8 → Emb:" nurses"@15 (de=19.25) +7 more |
| 12 | `get_upstream_features` | L18:F14457@14, k=8 → L14:F3985 (de=9.31) +7 more |
| 13 | `get_upstream_features` | L7:F8194@15, k=8 → Emb:"<bos>"@0 (de=-6.12) +7 more |

### Build

`build_circuit` → 8 nodes, 10 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 12,261 | 4,238 | 49,478 | 0 | $0.0117 | — | — |
| **Total** | | **12,261** | **4,238** | **49,478** | **0** | **$0.0117** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 0s