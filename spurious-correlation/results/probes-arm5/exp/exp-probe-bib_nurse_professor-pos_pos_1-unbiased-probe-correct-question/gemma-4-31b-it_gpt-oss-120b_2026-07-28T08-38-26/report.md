# Circuit Oracle Report
**Date:** 2026-07-28 08:38:26 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of the profession as "nursing" is driven by a direct causal chain originating from the token " nurses" and passing through specific nursing and medical professional detectors.

**Confidence:** 10/10

**Reasoning:** 
The circuit analysis demonstrates that the probe's score is not driven by spurious markers (such as gender) but by genuine profession-specific indicators. The signal originates at the embedding for the token **" nurses" (pos 15)**, which provides a strong positive contribution to early-layer detectors. 

The signal flows through a series of increasingly abstract professional features:
1. **Nursing Profession Detectors:** The embedding excites **L6:F15267** (explicitly labeled as a detector for the nursing profession) and **L2:F15437** (a low-frequency nursing-token detector). 
2. **Medical & Healthcare Context:** These feed into a cluster of medical context features, including **L8:F16339** (hospital infections/bacteria), **L7:F210** (healthcare system terminology), and **L4:F11037** (broader professional/educational domain).
3. **Nursing Leadership/Management:** The signal culminates in late-layer features that encode nursing-specific leadership, specifically **L14:F3985** (management/medicine/research) and **L18:F13596** (role, skills, and leadership of nurse managers). 

This hierarchical progression—from a literal profession token to a domain-specific detector, then to a broader medical context, and finally to a professional leadership role—confirms that the model is utilizing legitimate semantic evidence of the subject's profession to drive the probe's classification. No features related to gender or other irrelevant demographic markers were found to contribute significantly to the output.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: nurses (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 15 | Nursing Profession Detectors |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L2:F15437](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15437) | 15 | Nursing Profession Detectors | words related to nurses and sound | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15437) |
| [L8:F16339](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) | 15 | Medical & Healthcare Context |  text discussing hospital infections and bacteria | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 15 | Medical & Healthcare Context | words and names associated with the Asante Healthcare system | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 15 | Medical & Healthcare Context | words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 15 | Nursing Leadership/Management | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 15 | Nursing Leadership/Management |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L14:3985 de=0.163 |
| 3 | `inspect_feature` ×5 | L14:3985, L6:15267, L8:16339, L4:4665, L18:13596 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 6 | `get_top_features` | 10 features; top: L14:3985 de=0.163 |
| 7 | `inspect_feature` ×5 | L14:3985, L6:15267, L8:16339, L4:4665, L18:13596 |
| 8 | `get_top_logits` | "" (100%) |
| 9 | `get_top_features` | 15 features; top: L14:3985 de=0.163 |
| 10 | `inspect_feature` ×5 | L14:3985, L6:15267, L18:13596, L20:4927, L8:16339 |
| 11 | `get_top_logits` | "" (100%) |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@15` | ✅ reported | 4 | 8 | Trace the signal driving the probe score. Identify if it originates from nursing… |
| SA-2 | `L6:F15267@15` | ✅ reported | 6 | 14 | Trace the signal driving the probe score. Identify if it originates from nursing… |
| SA-3 | `L18:F13596@15` | ✅ reported | 5 | 10 | Trace the signal driving the probe score. Identify if it originates from nursing… |

<details>
<summary><b>SA-1</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 2 | `get_upstream_features` | L14:F3985@15, k=10 | Emb:" nurses"@15 (de=10.62) +9 more |
| 3 | `inspect_feature` | L8, F16339 | " text discussing hospital infections and bacteria" |
| 4 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 5 | `get_upstream_features` | L8:F16339@15, k=10 | Emb:" nurses"@15 (de=4.72) +9 more |
| 6 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 7 | `inspect_feature` | L7, F8194 | "mentions of the word "nurse" or the initials or last names of people" |
| 8 | `get_upstream_features` | L6:F15267@15, k=10 | Emb:" nurses"@15 (de=16.12) +9 more |

**Findings:** The probe score is driven primarily by the literal token " nurses" (embedding at position 15). This token strongly excites a low‑layer feature (L6:F15267) that detects nursing‑profession language, which in turn feeds upward through a cascade of medical‑environment features (L7:F210, L8:F16339) and finally to the higher‑level leadership/management feature (L14:F3985). All positive‑effect paths term…

</details>

<details>
<summary><b>SA-2</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@15, k=10 | Emb:" nurses"@15 (de=16.12) +9 more |
| 3 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 4 | `inspect_feature` | L4, F8751 | " cell types in the brain, especially glial cells and neurons, and rela" |
| 5 | `get_upstream_features` | L4:F11037@15, k=10 | Emb:" nurses"@15 (de=5.16) +9 more |
| 6 | `inspect_feature` | L2, F15437 | " words related to nurses and sound" |
| 7 | `get_upstream_features` | L4:F8751@15, k=10 | Emb:" nurses"@15 (de=9.81) +9 more |
| 8 | `inspect_feature` | L2, F5224 | " words related to retail and customer service jobs" |
| 9 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |

**Findings:** The probe signal originates from a cascade of nursing‑specific detectors. The primary driver is L6:F15267, which directly activates on the token "nurses" (positive embedding influence 16.1) and is itself a nursing‑profession detector. Upstream, L4:F11037 feeds it with social‑work / counseling context, and in turn L2:F15437 (a low‑frequency nursing‑token detector) feeds L4:F11037. All positive path…

</details>

<details>
<summary><b>SA-3</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F13596 | " text about the role, skills and leadership of nurse managers" |
| 2 | `get_upstream_features` | L18:F13596@15, k=10 | Emb:" nurses"@15 (de=42.00) +9 more |
| 3 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 4 | `get_upstream_features` | L6:F15267@15, k=10 | Emb:" nurses"@15 (de=16.12) +9 more |
| 5 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 6 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 7 | `inspect_feature` | L8, F16339 | " text discussing hospital infections and bacteria" |
| 8 | `get_upstream_features` | L8:F16339@15, k=10 | Emb:" nurses"@15 (de=4.72) +9 more |
| 9 | `get_upstream_features` | L4:F11037@15, k=10 | Emb:" nurses"@15 (de=5.16) +9 more |
| 10 | `inspect_feature` | L2, F15437 | " words related to nurses and sound" |
| 11 | `get_upstream_features` | L2:F15437@15, k=10 | Emb:" nurses"@15 (de=19.25) +9 more |

**Findings:** The probe score is driven primarily by the token embedding for " nurses" at position 15. This token strongly excites a low‑layer (layer 6) feature that is explicitly tuned to nursing‑profession words (F15267). That feature in turn feeds the higher‑layer target (F13596) and also activates several intermediate features (layers 4, 8, 14) that encode related professional and medical contexts. Because …

</details>

### Build

`build_circuit` → 5 nodes, 4 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 395,463 | 1,475 | 0 | 0 | $0.0560 | — | — |
| SA-1 | openai/gpt-oss-120b | 75,522 | 4,533 | 5,056 | 0 | $0.0141 | ✅ 4F/8E | Trace the signal driving the probe score. Identify if it ori… |
| SA-3 | openai/gpt-oss-120b | 128,224 | 9,403 | 15,040 | 0 | $0.0251 | ✅ 5F/10E | Trace the signal driving the probe score. Identify if it ori… |
| SA-2 | openai/gpt-oss-120b | 99,230 | 8,229 | 12,768 | 0 | $0.0200 | ✅ 6F/14E | Trace the signal driving the probe score. Identify if it ori… |
| **Total** | | **698,439** | **23,640** | **32,864** | **0** | **$0.1152** | | |

**Oracle wall-clock time:** 7m 45s