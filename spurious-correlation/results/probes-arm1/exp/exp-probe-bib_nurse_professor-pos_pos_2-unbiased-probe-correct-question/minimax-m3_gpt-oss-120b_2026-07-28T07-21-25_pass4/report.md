# Circuit Oracle Report
**Date:** 2026-07-28 07:21:25 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "nurse" classification is driven primarily by genuine profession-indicating features (the word "Nursing" at pos 10 and downstream nursing/medical vocabulary features), with a small contribution from the "graduated" / "University" tokens at the beginning of the bio — gender markers (e.g. L0:5038 firing on "graduated", L0:6270 on "University") are NOT gender features, and no pronoun/name feature appears in the top contributors.

**Confidence:** 7

**Reasoning:** The circuit converges on a single token position — **pos 10 (" Nursing")** — whose embedding (direct_effect ≈ 12–17 to multiple downstream features) is the dominant driver. The embedding activates L3:F15901 ("mentions of nurses/nursing/nurse management", frac_nonzero 0.005) and L6:F15267 ("words referring to the profession of nursing", frac_nonzero 0.016), which promote the strongly profession-specific tokens **"▁Nurse"**, **"▁nurse"**, **"Nursing"**. These feed L7:F3979 ("nursing/healthcare words") and L7:F210 (hospital/medical-center names, promoted tokens include **"▁medical"**, **"▁hospital"**, **"Hospital"**), then L8:F16339 (hospital-infection / medical text, promotes **"▁hospital"**, **"▁medical"**, **"▁physician"**), L14:F3985 (management/leadership/medicine/studies/research, promotes **"▁patients"**, **"Medical"**, **"▁clinical"**), L15:F15159 (medicine/healthcare words, promotes **"▁healthcare"**, **"▁patients"**, **"▁medical"**), and finally L18:F13596 (nurse-manager role/leadership, promoted tokens literally include **"Nurse"**, **"▁nurse"**, **"Nursing"**). Both L15 and L18 connect directly to the probe logit with positive direct effects.

The user's concern about spurious gender features is **not supported by this circuit**. The L0 features that fire on early tokens (L0:F5038 on "graduated" at pos 2 with direct_effect 0.088, L0:F6270 on "University" at pos 14 with direct_effect 0.072, L0:F16075 on "of" at pos 15) are generic word-level detectors — L0:F5038 fires on the word "graduated" generally, L0:F6270 fires on "University"/institution names. None of these encode gender; in fact the upstream-features call on L0:F5038 shows that its "She" embedding input at pos 1 carries only 0.373 direct effect (vs. 22.25 for "graduated" itself) — i.e. the pronoun barely influences this feature. The text's feminine markers ("She", "her", "Kayte") do not appear anywhere in the top-15 direct contributors to the probe, and no feature in the traced path has a label consistent with gender encoding.

The signal flow is: **` Nursing` token embedding → L3/L6 nursing-lexicon features → L7 healthcare-vocabulary → L8 hospital/medical → L14 management-medicine → L15/L18 nurse-manager medicine** → probe. This is a profession-indicator circuit, not a gender-marker circuit. The user's concern appears unfounded for this particular graph — the probe is doing what it should: classifying based on profession vocabulary, dominated by the highly specific token "Nursing" and a cascade of medical/nursing-domain features with low frac_nonzero (0.005–0.066, indicating selectivity).

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F5038](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5038) | 2 | L0: 'graduated' word feature | the word "graduated" or variations of it | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5038) |
| [L0:F11959](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11959) | 2 | L0: 'graduated' word feature |  the word "graduated" and the word "more." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11959) |
| [L0:F6270](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) | 14 | L0: 'University' / institution name | the word "whom", sometimes also activating on nearby punctuation, sentence starts, discourse markers, and other function words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) |
| [L3:F15901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) | 10 | L3: mentions of nurses / nursing |  mentions of nurses, nursing, and nurse management | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 10 | L6: 'nursing' as a profession label |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F4490](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) | 10 | L6: 'nursing' as a profession label |  proper nouns corresponding to locations, organizations, medical roles, and coding terms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 10 | L7: nursing/healthcare vocabulary + hospital names |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 10 | L7: nursing/healthcare vocabulary + hospital names |  words and names associated with the Asante Healthcare system | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L8:F16339](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) | 10 | L8: hospital/medical-infection text |  text discussing hospital infections and bacteria | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 10 | L14: management/leadership/medicine/studies | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L15:F15159](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) | 10 | L15: medicine/healthcare words |  words related to medicine and healthcare | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 10 | L18: nurse manager role/leadership text |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:3985 de=0.188 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@10` | ❌ error | — | — | Trace this feature upstream to identify what it encodes. This is a probe classif… |
| SA-2 | `L6:F15267@10` | ❌ error | — | — | Trace this feature upstream to identify what it encodes. Check if it relates to … |
| SA-3 | `L0:F5038@2` | ❌ error | — | — | Trace this feature upstream - it's at layer 0 pos 2 ("She"). Check if it encodes… |
| SA-4 | `L0:F6270@14` | ❌ error | — | — | Trace this feature upstream - it's at layer 0 pos 14. Check what token and what … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×4 | L14:3985, L6:15267, L0:5038, L0:6270 |
| 2 | `get_upstream_features` | L14:F3985@10, k=10 → Emb:" Nursing"@10 (de=12.12) +9 more |
| 3 | `get_upstream_features` | L6:F15267@10, k=10 → Emb:" Nursing"@10 (de=17.38) +9 more |
| 4 | `get_upstream_features` | L0:F5038@2, k=10 → Emb:" graduated"@2 (de=22.25) +9 more |
| 5 | `get_upstream_features` | L0:F6270@14, k=10 → Emb:" University"@14 (de=22.12) +9 more |
| 6 | `inspect_feature` ×9 | L8:16339, L7:210, L6:4490, L7:3979, L3:15901, L15:15159, L18:13596, L0:16075, L0:11959 |

### Build

`build_circuit` → 13 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 33,744 | 3,837 | 62,351 | 0 | $0.0185 | — | — |
| **Total** | | **33,744** | **3,837** | **62,351** | **0** | **$0.0185** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 55s