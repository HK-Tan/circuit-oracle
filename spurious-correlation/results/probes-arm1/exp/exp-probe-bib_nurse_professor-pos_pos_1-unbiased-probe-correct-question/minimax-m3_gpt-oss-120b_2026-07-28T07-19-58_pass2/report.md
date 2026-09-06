# Circuit Oracle Report
**Date:** 2026-07-28 07:19:58 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score for this profession is driven by genuine nursing/profession-indicating features (the literal tokens "nurses", "Perioperative") rather than by gender markers; "she" contributes a tiny signal (direct_effect ≈ 1.0) that is dwarfed by the profession token (direct_effect 10.6–42).

**Confidence:** 8

**Reasoning:**

The circuit flows from input token embeddings to the probe via profession-specific transcoder features at every layer:

1. **Token embedding inputs.** The dominant signal comes from the literal profession tokens at positions 13–15: " Perio" (pos 13), "perative" (pos 14) and " nurses" (pos 15). The single token " nurses" alone has a direct_effect of 10.6 on L14:F3985 and 42.0 on L18:F13596 — the largest excitatory signals in the entire graph. "perative" and " Perio" feed L4:F4665 (medical environment, de=15.4) and L18:F13596 (de=19.25). These are unambiguous profession words, not gender markers.

2. **Early layer profession detectors.** L0:F10920 ("the word nurse"), L2:F15437 (nurses/medical vocabulary), and L6:F15267 (frac_nonzero=0.016, label "nursing profession") are sparse, specific detectors that fire only on the literal "nurse/nurses" tokens. Their top activating examples are all "nurse," "nursing," "RN" contexts. The "she" embedding at pos 7 contributes only direct_effect 1.04 to L6:F15267 — minor compared to the 16.1 from " nurses" itself.

3. **Mid-layer profession/role features.** L7:F210 (healthcare institution names, de=3.6), L8:F16339 (hospital/medical context, de=4.9), L14:F3985 (management/leadership/medicine, frac_nonzero=0.066, de=10.6 from "nurses" embedding) all encode medical-institutional context, not gender.

4. **Late-layer nurse-manager features.** L18:F13596 (frac_nonzero=0.005, label "role, skills and leadership of nurse managers") and L18:F14457 (healthcare implementation, de=4.6) are the most discriminative features; their top activating examples are all about nurse managers specifically. L20:F4927 promotes "nurse/nursing" tokens directly (its promoted tokens are exactly the profession vocabulary).

5. **Inhibitory/suppressor features.** L3:F15901, L7:F3979, L9:F11754 (frac_nonzero=0.41, generic), L4:F8736 ("born and raised" — pushes AWAY from nurse class, de=-0.087), and L4:F9757 (acronyms, de=+0.075, weak) are generic healthcare/background features that suppress the probe, not gender features.

**Verdict on user concern:** The user's hypothesis that the circuit uses spurious gender markers is **not supported**. The dominant path is "nurses/Perioperative" → nursing-profession detectors → nurse-manager role features → probe. The pronoun "she" enters only once, with direct_effect ≈ 1.0 at L6, which is an order of magnitude smaller than the profession-token signal at the same feature. The probe appears to use a legitimate, profession-grounded representation. The user's concern likely arose from a superficial reading of the input sentence, but the mechanistic evidence shows the model is using "nurse/nursing" tokens as the primary classification evidence.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: ' nurses' (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: 'perative' (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: ' Perio' (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: ' she' (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F10920](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10920) | 15 | L0: F10920 — 'the word nurse' detector (pos 15) |  the word "nurse" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10920) |
| [L2:F15437](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15437) | 15 | L2: F15437 — nurses/medical vocabulary (pos 15) |  words related to nurses and sound | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15437) |
| [L3:F15901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) | 15 | L3: F15901 — mentions of nurses/nursing/nurse management (pos 15) [inhibitory] |  mentions of nurses, nursing, and nurse management | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 14 | L4: F4665 — medical environments/personnel/facilities (pos 14) |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L4:F8736](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8736) | 2 | L4: F8736 — 'born and raised' / hometown phrasing (pos 2) [inhibitory] |  the phrase "born and raised" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8736) |
| [L4:F9757](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) | 1 | L4: F9757 — acronyms / IDs (pos 1) [inhibitory] | various acronyms, IDs, and symbols, possibly related to scientific data | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 15 | L6: F15267 — 'nursing profession' word detector (frac_nonzero=0.016, pos 15) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 14 | L6: F15267 — 'nursing profession' word detector (frac_nonzero=0.016, pos 15) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 15 | L7: F210 — healthcare institution / hospital name detector (pos 15) |  words and names associated with the Asante Healthcare system | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 15 | L7: F3979 — nursing/healthcare words (pos 15) [inhibitory] |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L8:F16339](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) | 15 | L8: F16339 — hospital/medical-infection context (pos 15) |  text discussing hospital infections and bacteria | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) |
| [L9:F11754](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/11754) | 15 | L9: F11754 — nurses/managers/employees (frac_nonzero=0.41, generic) (pos 15) [inhibitory] |  words related to nurses, managers, and/or employees | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/11754) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 15 | L14: F3985 — management/leadership/medicine (frac_nonzero=0.066) (pos 14,15) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 14 | L14: F3985 — management/leadership/medicine (frac_nonzero=0.066) (pos 14,15) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 15 | L18: F13596 — text about role/skills/leadership of nurse managers (frac_nonzero=0.005) (pos 14,15) |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 14 | L18: F13596 — text about role/skills/leadership of nurse managers (frac_nonzero=0.005) (pos 14,15) |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L18:F14457](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14457) | 14 | L18: F14457 — healthcare implementation/patient care (pos 14) |  words or phrases related to healthcare implementation, patient care and technology | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14457) |
| [L19:F5028](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/5028) | 14 | L19: F5028 — generic healthcare industry words (frac_nonzero=0.21) (pos 14) |  words related to the healthcare industry | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/5028) |
| [L20:F4927](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) | 14 | L20: F4927 — titles/acronyms in healthcare (promotes 'nurse/nursing') (pos 14) |  titles and acronyms following names, especially within the healthcare field | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe output (profession classifier) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:3985 de=0.163 |
| 3 | `inspect_feature` ×12 | L14:3985, L6:15267, L18:13596, L3:15901, L7:3979, L8:16339, L4:4665, L7:210, L4:8736, L20:4927, L4:9757, L2:15437 |
| 4 | `get_upstream_features` | Emb:" nurses"@15 (de=10.62) +7 more |
| 5 | `get_upstream_features` | Emb:" nurses"@15 (de=42.00) +7 more |
| 6 | `get_upstream_features` | L18:F13596 (de=14.31) +7 more |
| 7 | `get_upstream_features` | Emb:" nurses"@15 (de=4.72) +7 more |
| 8 | `get_upstream_features` | Emb:" nurses"@15 (de=16.12) +9 more |
| 9 | `get_upstream_features` | Emb:"perative"@14 (de=7.72) +9 more |
| 10 | `get_upstream_features` | Emb:"perative"@14 (de=15.44) +9 more |
| 11 | `get_upstream_features` | Emb:"<bos>"@0 (de=14.00) +7 more |
| 12 | `get_upstream_features` | Emb:" from"@2 (de=6.09) +7 more |
| 13 | `get_upstream_features` | Emb:" nurses"@15 (de=19.25) +7 more |
| 14 | `get_upstream_features` | L18:F14457 (de=3.47) +7 more |
| 15 | `inspect_feature` ×4 | L18:14457, L18:14457, L9:11754, L19:5028 |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L20:F4927@14` | ❌ error | — | — | Trace from L20:F4927 (nursing/healthcare titles feature at pos 14 "perative") up… |
| SA-2 | `L14:F3985@15` | ✅ reported | 4 | 6 | Trace from L14:F3985 (management/leadership/medicine feature at pos 15 "nurses")… |

<details>
<summary><b>SA-2</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 2 | `get_upstream_features` | L14:F3985@15, k=10 | Emb:" nurses"@15 (de=10.62) +9 more |
| 3 | `inspect_feature` | L8, F16339 | " text discussing hospital infections and bacteria" |
| 4 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 5 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 6 | `get_upstream_features` | L6:F15267@15, k=10 | Emb:" nurses"@15 (de=16.12) +9 more |

**Findings:** The downstream L14 nurse‑management feature is driven primarily by the raw input token "nurses" (direct_effect 10.6) and also receives a smaller excitatory signal from the gender pronoun "she" (direct_effect 1.0) via the L6 nursing‑profession feature. Upstream medical‑context features (hospital infection, Asante healthcare) further modulate the signal. No male pronoun or explicitly gendered name a…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×2 | L0:10920, L0:9026 |
| 2 | `get_upstream_features` | L14:F3985@14, k=5 → L4:F4665 (de=3.14) +4 more |
| 3 | `get_upstream_features` | L18:F13596@14, k=5 → Emb:"perative"@14 (de=19.25) +4 more |
| 4 | `get_upstream_features` | L13:F3597@14, k=5 → Emb:"<bos>"@0 (de=-29.12) +4 more |
| 5 | `get_upstream_features` | L13:F3597@14, k=5 → Emb:"<bos>"@0 (de=-29.12) +4 more |
| 6 | `inspect_feature` | L13, F3597 → " technical writing related to legal, medical, or engineering contexts" |
| 7 | `get_upstream_features` | L19:F5028@14, k=5 → L18:F14457 (de=3.47) +4 more |

### Build

`build_circuit` → 21 nodes, 36 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 47,909 | 6,315 | 234,222 | 0 | $0.0360 | — | — |
| SA-2 | openai/gpt-oss-120b | 49,744 | 3,044 | 5,056 | 0 | $0.0094 | ✅ 4F/6E | Trace from L14:F3985 (management/leadership/medicine feature… |
| **Total** | | **97,653** | **9,359** | **239,278** | **0** | **$0.0454** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 42s