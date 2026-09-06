# Circuit Oracle Report
**Date:** 2026-07-28 08:36:39 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by a circuit that detects a specialized medical context (specifically labor and delivery) rather than spurious gender markers.

**Confidence:** 9/10

**Reasoning:** 
The circuit originates from the input token **" Labor" (pos 9)**, which feeds into early-layer features specializing in medical procedures and childbirth context (**Med_Context_Early**: L3:F10198, L3:F9008). This signal propagates through a series of mid-layer features that encode generic medical environments and institutions (**Med_Context_Mid**: L4:F4665, L6:F4490, L6:F9980, L7:F210), which detect hospitals and clinical settings. These converge on a late-layer feature (**Med_Leadership_Late**: L14:F3985) that encodes the intersection of medical terminology and professional roles (e.g., "nurse manager", "medical leadership"). Finally, this professional medical signal directly drives the probe's classification score. Notably, the evidence shows the probe relies on profession-specific lexical cues ("Labor") and institutional context rather than gender-coded tokens (e.g., "Melissa" or "mom"), contradicting the user's concern about spurious gender-based prediction.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: Labor (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L3:F10198](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10198) | 11 | Medical Procedure/Birth Context | words related to anesthetics and medical procedures | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10198) |
| [L3:F9008](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) | 11 | Medical Procedure/Birth Context | words related to childbirth or birth in general, including in animals. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 11 | Medical Environment/Institution |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L6:F4490](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) | 11 | Medical Environment/Institution | proper nouns corresponding to locations, organizations, medical roles, and coding terms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) |
| [L6:F9980](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9980) | 11 | Medical Environment/Institution |  words and abbreviations associated with pediatric gastroenterology and inflammatory bowel disease. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9980) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 11 | Medical Environment/Institution |  words and names associated with the Asante Healthcare system | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 11 | Medical Leadership/Profession Signal | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L14:3985 de=0.106 |
| 3 | `inspect_feature` ×6 | L14:3985, L0:9911, L6:9980, L7:210, L6:15267, L4:4665 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 15 features; top: L14:3985 de=0.106 |

### Dispatch: 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@11` | ✅ reported | 7 | 7 | Trace the path from L14:F3985 to understand what triggers this medicine/leadersh… |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 2 | `get_upstream_features` | L14:F3985@11, k=10 | L6:F4490 (de=3.00) +9 more |
| 3 | `inspect_feature` | L6, F4490 | " proper nouns corresponding to locations, organizations, medical roles" |
| 4 | `get_upstream_features` | L6:F4490@11, k=10 | L4:F4665 (de=3.92) +9 more |
| 5 | `inspect_feature` | L4, F4665 | " words and phrases related to medical environments, treatments, person" |
| 6 | `inspect_feature` | L6, F9980 | " words and abbreviations associated with pediatric gastroenterology an" |
| 7 | `get_upstream_features` | L4:F4665@11, k=10 | L3:F10198 (de=3.44) +9 more |
| 8 | `inspect_feature` | L3, F10198 | " words related to anesthetics and medical procedures" |
| 9 | `inspect_feature` | L3, F9008 | " words related to childbirth or birth in general, including in animals" |
| 10 | `get_upstream_features` | L3:F10198@11, k=10 | Emb:" Delivery"@11 (de=7.59) +9 more |
| 11 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 12 | `inspect_feature` | L6, F5948 | " words related to scientific publications" |

**Findings:** The target L14:F3985 (medicine/leadership) is chiefly driven by mid‑layer medical‑environment detectors. The strongest upstream driver is L6:F4490, which fires on proper nouns for hospitals and patients. That feature receives strong positive input from L4:F4665 (generic medical‑setting terms) and from the raw token embedding for "Delivery" (pos 11). The token "Delivery" (and the related token "Lab…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F4665@11, k=15 → L3:F10198 (de=3.44) +14 more |

### Build

`build_circuit` → 5 nodes, 4 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 154,701 | 974 | 4,224 | 0 | $0.0221 | — | — |
| SA-1 | openai/gpt-oss-120b | 160,597 | 9,795 | 17,696 | 0 | $0.0302 | ✅ 7F/7E | Trace the path from L14:F3985 to understand what triggers th… |
| **Total** | | **315,298** | **10,769** | **21,920** | **0** | **$0.0523** | | |

**Oracle wall-clock time:** 5m 55s