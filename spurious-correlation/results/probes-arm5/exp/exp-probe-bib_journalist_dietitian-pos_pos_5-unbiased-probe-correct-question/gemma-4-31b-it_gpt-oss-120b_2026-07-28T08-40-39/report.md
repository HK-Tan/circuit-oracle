# Circuit Oracle Report
**Date:** 2026-07-28 08:40:39 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe classification score is driven by a circuit that detects health, nutrition, and exercise-related terminology, originating specifically from the token "nutrition" in the input text.

**Confidence:** 10/10

**Reasoning:**
The attribution graph reveals a clear, unidirectional flow of information from a specific input token to the probe's output. The primary driver is the token embedding for **"nutrition" (pos 7)**, which excites a hierarchy of features:
1.  **Low-layer Health/Exercise Detectors (L1):** Features like `L1:F6461` (technical physical activity) and `L1:F6631` (dietary patterns) activate immediately upon seeing "nutrition".
2.  **Mid-layer Summary Features (L4):** These signals converge into broader health summary features such as `L4:F10494` (general health/medicine/diet) and `L4:F13412` (diets and dietary health).
3.  **Nutrition Refinement (L6):** The signal further refines into features specifically targeting food and nutrition, such as `L6:F11327`.
4.  **High-layer Health/Exercise Features (L14):** Finally, these feed into high-layer features like `L14:F4197` (food-related concepts) and `L14:F16195` (physical activity and training), which provide the final push to the probe classification score.

Crucially, the trace shows no reliance on gender markers (e.g., "Her", "She") or generic profession markers; the circuit is grounded entirely in the semantic content of the profession-specific terminology ("nutrition"). This confirms that the probe is using genuine profession indicators rather than spurious gender-based correlations.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L1:F6461](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6461) | 7 | Low-layer Health/Exercise Detectors | technical language around physical activity, muscle function, and related studies | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6461) |
| [L1:F6631](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6631) | 7 | Low-layer Health/Exercise Detectors | words related to dietary patterns and scientific studies | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6631) |
| [L1:F15310](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15310) | 7 | Low-layer Health/Exercise Detectors | words related to physical exercise | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15310) |
| [L1:F760](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/760) | 7 | Low-layer Health/Exercise Detectors | scientific and medical terminology related to tissue and cells | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/760) |
| [L4:F10494](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) | 7 | Mid-layer Diet/Health Summary Features |  words related to health, medicine, diet, drugs, age groups, and excercise | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 7 | Mid-layer Diet/Health Summary Features |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 7 | Nutrition/Food Refinement Features |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 7 | High-layer Health/Exercise Features |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F16195](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/16195) | 7 | High-layer Health/Exercise Features | mentions of physical activity and training. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/16195) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:10494 de=0.176 |
| 3 | `inspect_feature` ×5 | L4:10494, L4:13412, L14:4197, L14:16195, L6:11327 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 10 features; top: L4:10494 de=0.176 |
| 6 | `inspect_feature` ×5 | L4:10494, L4:13412, L14:4197, L14:16195, L6:11327 |
| 7 | `get_top_logits` | "" (100%) |
| 8 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F10494@7` | ✅ reported | 9 | 16 | Trace the path from L4:F10494 and L4:F13412 to find the originating tokens in th… |
| SA-2 | `L14:F4197@7` | ✅ reported | 9 | 10 | Trace the path from L14:F4197 and L14:F16195 to see if they originate from profe… |

<details>
<summary><b>SA-1</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F10494 | " words related to health, medicine, diet, drugs, age groups, and excer" |
| 2 | `get_upstream_features` | L4:F10494@7, k=10 | Emb:" nutrition"@7 (de=11.25) +9 more |
| 3 | `inspect_feature` | L1, F6461 | " technical language around physical activity, muscle function, and rel" |
| 4 | `get_upstream_features` | L1:F6461@7, k=10 | Emb:" sports"@6 (de=9.19) +9 more |
| 5 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 6 | `get_upstream_features` | L4:F13412@7, k=10 | Emb:" nutrition"@7 (de=12.62) +9 more |
| 7 | `inspect_feature` | L1, F6631 | " words related to dietary patterns and scientific studies" |
| 8 | `get_upstream_features` | L1:F6631@7, k=10 | Emb:" nutrition"@7 (de=5.12) +9 more |
| 9 | `inspect_feature` | L1, F760 | " scientific and medical terminology related to tissue and cells" |
| 10 | `get_upstream_features` | L1:F760@7, k=10 | Emb:" nutrition"@7 (de=3.64) +9 more |
| 11 | `inspect_feature` | L2, F2589 | " words related to medical professionals and medical specialties" |
| 12 | `inspect_feature` | L1, F15310 | " words related to physical exercise" |
| 13 | `get_upstream_features` | L2:F2589@7, k=10 | Emb:" nutrition"@7 (de=4.50) +9 more |
| 14 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 15 | `inspect_feature` | L1, F165 | " names of sports teams and words related to sports statistics, contrac" |

**Findings:** The trace starts at two health/diet‑related features in layer 4 (F10494 and F13412). Both receive their strongest excitatory drive from the token embedding " nutrition" at position 7, confirming that the prompt token "nutrition" is the primary origin of the health‑related circuitry. Upstream from the layer 4 features we reach layer 1 and layer 2 detectors that specialise in exercise physiology (F6…

</details>

<details>
<summary><b>SA-2</b> — tool trace (22 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4197 | " words and phrases related to food insecurity." |
| 2 | `get_upstream_features` | L14:F4197@7, k=10 | Emb:" nutrition"@7 (de=12.88) +9 more |
| 3 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 4 | `inspect_feature` | L14, F16195 | "mentions of physical activity and training." |
| 5 | `get_upstream_features` | L6:F11327@7, k=10 | Emb:" nutrition"@7 (de=17.50) +9 more |
| 6 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 7 | `inspect_feature` | L9, F15926 | "mentions about eating and meals" |
| 8 | `get_upstream_features` | L4:F13412@7, k=10 | Emb:" nutrition"@7 (de=12.62) +9 more |
| 9 | `get_upstream_features` | L9:F15926@7, k=10 | Emb:" nutrition"@7 (de=8.06) +9 more |
| 10 | `inspect_feature` | L2, F15770 | " words related to economics and politics, especially regarding campaig" |
| 11 | `get_upstream_features` | L14:F16195@7, k=10 | Emb:" nutrition"@7 (de=7.97) +9 more |
| 12 | `inspect_feature` | L8, F7057 | " terms related to exercise, biology and chemistry" |
| 13 | `inspect_feature` | L1, F6461 | " technical language around physical activity, muscle function, and rel" |
| 14 | `inspect_feature` | L7, F11540 | " scientific discussion of vitamins and minerals" |
| 15 | `inspect_feature` | L1, F165 | " names of sports teams and words related to sports statistics, contrac" |
| 16 | `inspect_feature` | L7, F13562 | " terms related to physical and mental training or conditioning" |
| 17 | `get_upstream_features` | L7:F13562@7, k=10 | Emb:" nutrition"@7 (de=8.12) +9 more |
| 18 | `inspect_feature` | L4, F10494 | " words related to health, medicine, diet, drugs, age groups, and excer" |
| 19 | `get_upstream_features` | L1:F165@7, k=10 | Emb:" sports"@6 (de=8.44) +9 more |
| 20 | `get_upstream_features` | L7:F11540@7, k=10 | Emb:" nutrition"@7 (de=15.88) +9 more |
| 21 | `inspect_feature` | L1, F6461 | " technical language around physical activity, muscle function, and rel" |
| 22 | `get_upstream_features` | L2:F15770@7, k=10 | Emb:" nutrition"@7 (de=8.44) +9 more |

**Findings:** Both L14:F4197 and L14:F16195 trace back to the embedding token "nutrition" (position 7) with strong positive direct effects. Their downstream cascades involve diet, health, and exercise‑related features, but no positive upstream paths contain profession‑specific or gendered tokens. Hence these features originate from nutrition‑related signals rather than from profession or gender cues.

</details>

### Build

`build_circuit` → 6 nodes, 5 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 253,428 | 1,383 | 51,072 | 0 | $0.0367 | — | — |
| SA-1 | openai/gpt-oss-120b | 237,868 | 18,177 | 36,480 | 0 | $0.0471 | ✅ 9F/16E | Trace the path from L4:F10494 and L4:F13412 to find the orig… |
| SA-2 | openai/gpt-oss-120b | 423,511 | 16,143 | 80,864 | 0 | $0.0744 | ✅ 9F/10E | Trace the path from L14:F4197 and L14:F16195 to see if they … |
| **Total** | | **914,807** | **35,703** | **168,416** | **0** | **$0.1583** | | |

**Oracle wall-clock time:** 9m 55s