# Circuit Oracle Report
**Date:** 2026-07-28 07:22:42 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe classifies this passage as the nursing profession, driven primarily by profession-specific vocabulary tokens ("Perioperative", "nurses") that activate nursing/medical-domain features, not by gender markers.

**Confidence:** 9

**Reasoning:**

The user worried the probe relies on spurious gender markers (e.g., "she"). The circuit shows the opposite. Signal flow: token embeddings for **"Perioperative"** (pos 13–14) and **"nurses"** (pos 15) flow into profession-specific features at L4–L8. L4:F4665 ("medical environments, treatments, personnel, facilities," frac=0.012) fires on "perative"/"Perio" and promotes "hospital". L6:F15267 ("profession of nursing," frac=0.016) and L7:F3979 ("nursing and healthcare," frac=0.008) both fire specifically on "nurses" with promoted tokens "Nurse/Nursing". L8:F16339 ("hospital infections and bacteria") and L7:F210 ("Asante Healthcare/hospital") provide general medical-setting context.

These mid-layer profession indicators feed L14:F3985 ("management, leadership, medicine, studies, research," frac=0.066) — whose top-activating examples are *nurse manager* text — at positions 14 and 15, which directly drives the probe (+0.1631, +0.1465). L14:F3985 in turn feeds L18:F13596 ("role, skills, leadership of nurse managers," frac=0.005) and L20:F4927 ("titles and acronyms in healthcare," frac=0.017), the strongest late-layer drivers. Notably, L18:F13596's *direct upstream* from token " nurses" is 42.0 — the largest single edge in the graph — confirming nursing vocabulary, not gender, is the dominant signal.

The "she" pronoun at pos 7 *does* appear in the circuit but only through the **suppressor** supernode (negative direct effects). L18:F14677 ("instances of women or girls being mentioned," frac=0.012) has direct_effect −0.065 on the probe, and L3:F15901 ("nurses, nursing, nurse management," frac=0.005) has −0.134. Both are *inhibitory* — the female-pronoun feature pushes the score *down*, not up. The L4:F8736 feature ("born and raised," pos 2) firing on "Formerly" is also mildly negative (−0.087), a generic biographical-introduction pattern, not a profession indicator.

Net assessment: the probe's positive signal is grounded in genuine profession vocabulary ("Perioperative", "nurses", "nurse management", healthcare-setting terms) flowing through a clean nursing-domain feature hierarchy. Gender markers enter the circuit only as **negative** contributors, meaning if anything the model is slightly discounting the profession signal when female pronouns are present. The user's concern about spurious gender reliance is not supported by this circuit.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 15 | Late output drivers — nursing profession signal |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 14 | Late output drivers — nursing profession signal |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L20:F4927](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) | 14 | Late output drivers — nursing profession signal |  titles and acronyms following names, especially within the healthcare field | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) |
| [L20:F4927](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) | 15 | Late output drivers — nursing profession signal |  titles and acronyms following names, especially within the healthcare field | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) |
| [L18:F14457](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14457) | 14 | Late output drivers — nursing profession signal | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14457) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 15 | Mid output driver — nurse management/leadership | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 14 | Mid output driver — nurse management/leadership | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 15 | Profession indicators — nursing/healthcare vocabulary |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 14 | Profession indicators — nursing/healthcare vocabulary |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 15 | Profession indicators — nursing/healthcare vocabulary |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L8:F16339](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) | 15 | Profession indicators — nursing/healthcare vocabulary |  text discussing hospital infections and bacteria | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 15 | Profession indicators — nursing/healthcare vocabulary |  words and names associated with the Asante Healthcare system | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 14 | Medical context — hospital/clinical terms |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 45 | Medical context — hospital/clinical terms |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L3:F15901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) | 15 | Suppressors — negative contributions to probe |  mentions of nurses, nursing, and nurse management | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) |
| [L4:F8736](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8736) | 2 | Suppressors — negative contributions to probe |  the phrase "born and raised" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8736) |
| [L2:F15437](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15437) | 15 | Suppressors — negative contributions to probe |  words related to nurses and sound | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15437) |
| [L9:F16275](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/16275) | 15 | Suppressors — negative contributions to probe |  terms related to the workplace environment, including job titles, business descriptions or complaints about work | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/16275) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 7 | Suppressors — negative contributions to probe |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:3985 de=0.163 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@15` | ❌ error | — | — | Trace L14:F3985 at position 15 upstream. This is the top direct contributor to t… |
| SA-2 | `L6:F15267@15` | ❌ error | — | — | Trace L6:F15267 at position 15 upstream. This is the second-highest direct contr… |
| SA-3 | `L18:F13596@15` | ❌ error | — | — | Trace L18:F13596 at position 15 upstream. Direct effect 0.0981 on the probe. Ins… |
| SA-4 | `L7:F3979@15` | ❌ error | — | — | Trace L7:F3979 at position 15 upstream. Direct effect -0.1182 (suppressing the p… |
| SA-5 | `L4:F4665@14` | ❌ error | — | — | Trace L4:F4665 at position 14 upstream. Direct effect 0.105 on the probe. This i… |
| SA-6 | `L8:F16339@15` | ❌ error | — | — | Trace L8:F16339 at position 15 upstream. Direct effect 0.1055. Inspect and trace… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×6 | L14:3985, L6:15267, L18:13596, L7:3979, L4:4665, L8:16339 |
| 2 | `get_upstream_features` | L14:F3985@15, k=10 → Emb:" nurses"@15 (de=10.62) +9 more |
| 3 | `get_upstream_features` | L6:F15267@15, k=10 → Emb:" nurses"@15 (de=16.12) +9 more |
| 4 | `get_upstream_features` | L18:F13596@15, k=10 → Emb:" nurses"@15 (de=42.00) +9 more |
| 5 | `get_upstream_features` | L7:F3979@15, k=10 → L6:F15267 (de=7.97) +9 more |
| 6 | `get_upstream_features` | L4:F4665@14, k=10 → Emb:"perative"@14 (de=15.44) +9 more |
| 7 | `get_upstream_features` | L8:F16339@15, k=10 → Emb:" nurses"@15 (de=4.72) +9 more |
| 8 | `inspect_feature` ×9 | L7:7, L7:210, L3:15901, L4:9757, L4:8736, L20:4927, L18:14677, L9:16275, L2:15437 |

### Build

`build_circuit` → 11 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 43,425 | 4,498 | 75,021 | 0 | $0.0229 | — | — |
| **Total** | | **43,425** | **4,498** | **75,021** | **0** | **$0.0229** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 2s