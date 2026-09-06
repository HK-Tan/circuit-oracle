# Circuit Oracle Report
**Date:** 2026-07-28 07:20:58 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by genuine nursing/profession-specific medical vocabulary (nurse, practitioner, labor, delivery) flowing through a hierarchy of healthcare-specific features, NOT by gender markers — the "She" pronoun and "also" tokens actually *suppress* the probe score rather than promote it.

**Confidence:** 8/10

**Reasoning:** The user's concern about spurious gender features is **not supported** by this circuit. The probe's positive drivers are all profession-grounded:

- **Direct embedding inputs** are the actual profession tokens: `Emb: nurse (pos 7)`, `Emb: practitioner (pos 8)`, `Emb: labor (pos 44)`, `Emb: delivery (pos 46)`. These are the genuine indicators.
- **L0:1832** ("the word labor", activation 21.1, direct_effect 0.044) is a token-level labor detector that directly drives the logit.
- **L6:15267** ("nursing profession", frac_nonzero 0.016, activations ~20-23) is a moderately specific nursing-term detector driven by embeddings of "nurse" and "practitioner" and forwarded from L4:9036 (healthcare abbreviations) and L5:1275 (healthcare professionals). It contributes via L14:3985.
- **L14:3985** ("management/leadership/medicine/research", frac_nonzero 0.066, direct_effect 0.089 at pos 8) is the strongest single contributor. Its top-activating examples are dominated by "nurse manager" contexts — it's a profession-context feature, not a generic one.
- **L4:4665** ("medical environments, treatments, personnel") is activated by the "labor" and "delivery" tokens through L3:9008 (childbirth) and L3:10198 (anesthetic procedures) — substantively medical.
- **L15:15159** ("medicine/healthcare", direct_effect 0.051) is fed by the "nurse" token embedding directly (effect 17.5).

**Gender/pronominal features are suppressors, not drivers:**
- **L0:15382** ("female person" — detects "She"/"Her") has direct_effect **-0.038** to the probe (suppresses).
- **L0:10846** ("also") has direct_effect **-0.042** (suppresses).
- **L7:3979** (nursing/healthcare) has direct_effect **-0.049** at pos 8 (suppresses, paradoxically — likely a sibling-inhibition effect).
- **L5:9749** (generic medical) at pos 46 has direct_effect **-0.047** (suppresses).

All four of these negative-contribution features point *away* from the nurse classification — exactly opposite to the spurious-gender hypothesis. If the probe were relying on "She" as a shortcut, L0:15382 would have a large *positive* direct_effect; instead it pushes the probe score down, meaning the model is using profession content to override the gender signal.

The only mildly suspicious feature is **L6:9980** (direct_effect 0.046, "pediatric gastroenterology abbreviations") — its top examples fire on "ology"/"enter" suffixes, suggesting it activates on the morphology of "gynecological" / "pediatrics" in the text rather than actual GI content. This is a content-feature (medical specialty morphology), not a gender feature, but it does fire on a non-target medical context.

**Bottom line:** the circuit is overwhelmingly driven by genuine nursing profession vocabulary ("nurse", "practitioner", "labor and delivery") and is *dampened* by the female-pronoun signal — so the probe appears to be using profession content, not gender, for its classification.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F1832](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1832) | 44 | L0:1832 'the word labor' | the word "labor" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1832) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 1 | L0:15382 'female person' (suppresses probe) | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F10846](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10846) | 3 | L0:10846 'also' (suppresses probe) | the word "also" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10846) |
| [L1:F12174](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12174) | 46 | L1:12174 'labor/convention language' | words relating to ways things are conventionally done, potential problems, or political/economic issues | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12174) |
| [L1:F1494](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) | 8 | L1:1494 'medical practice/study' | words related to medical practices and studies. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) |
| [L3:F9008](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) | 46 | L3:9008 'childbirth/birth' | words related to childbirth or birth in general, including in animals. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) |
| [L3:F10198](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10198) | 46 | L3:10198 'anesthetics/medical procedures' | words related to anesthetics and medical procedures | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10198) |
| [L4:F9036](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) | 8 | L4:9036 'healthcare abbreviations (practitioner, RN, nurse)' | words and abbreviations associated with healthcare. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 46 | L4:4665 'medical environments, treatments, personnel' |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 8 | L4:11037 'counseling/social work/degree programs' | words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L5:F9749](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9749) | 8 | L5:9749 'generic medical/practitioner' (suppresses in this context) |  words related to various medical conditions, procedures, and practitioners | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9749) |
| [L5:F9749](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9749) | 46 | L5:9749 'generic medical/practitioner' (suppresses in this context) |  words related to various medical conditions, procedures, and practitioners | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9749) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 8 | L5:1275 'healthcare professionals' | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 7 | L6:15267 'nursing profession' |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 8 | L6:15267 'nursing profession' |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 47 | L6:15267 'nursing profession' |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F9980](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9980) | 46 | L6:9980 'pediatric GI abbreviations' (ology/enter suffix) |  words and abbreviations associated with pediatric gastroenterology and inflammatory bowel disease. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9980) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 7 | L7:3979 'nursing/healthcare' (suppresses in this context) |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 8 | L7:3979 'nursing/healthcare' (suppresses in this context) |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 7 | L14:3985 'management/leadership/medicine/research' | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 8 | L14:3985 'management/leadership/medicine/research' | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 11 | L14:3985 'management/leadership/medicine/research' | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 46 | L14:3985 'management/leadership/medicine/research' | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L15:F15159](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) | 7 | L15:15159 'medicine/healthcare' |  words related to medicine and healthcare | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:3985 de=0.089 |
| 3 | `inspect_feature` ×4 | L14:3985, L6:15267, L15:15159, L4:4665 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@8` | ❌ error | — | — | Trace what inputs drive the medical/management/nursing feature at L14:3985 pos 8… |
| SA-2 | `L6:F15267@8` | ✅ reported | 5 | 10 | Trace what inputs drive the nursing profession feature at L6:15267 pos 8. Find w… |
| SA-3 | `L4:F4665@46` | ✅ reported | 8 | 17 | Trace what inputs drive the medical environments feature at L4:4665 pos 46. Find… |
| SA-4 | `L0:F1832@44` | ❌ error | — | — | Trace what drives L0:1832 at pos 44. This early-layer feature may encode a gende… |

<details>
<summary><b>SA-2</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@8, k=10 | Emb:" nurse"@7 (de=7.06) +9 more |
| 3 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 4 | `get_upstream_features` | L5:F1275@8, k=10 | Emb:" nurse"@7 (de=2.30) +9 more |
| 5 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 6 | `inspect_feature` | L4, F9036 | " words and abbreviations associated with healthcare." |
| 7 | `get_upstream_features` | L4:F9036@8, k=10 | Emb:" practitioner"@8 (de=14.69) +9 more |
| 8 | `inspect_feature` | L1, F1494 | " words related to medical practices and studies." |

**Findings:** The nursing‑profession feature (L6:F15267) is driven primarily by the raw token embeddings for "nurse" (position 7) and "practitioner" (position 8). These embeddings feed directly into the target feature with strong positive direct effects. Upstream, a mid‑layer health‑professional detector (L5:F1275) amplifies the signal, itself receiving strong excitation from the same embeddings and from a more…

</details>

<details>
<summary><b>SA-3</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F4665 | " words and phrases related to medical environments, treatments, person" |
| 2 | `get_upstream_features` | L4:F4665@46, k=15 | Emb:" labor"@44 (de=3.45) +14 more |
| 3 | `inspect_feature` | L3, F9008 | " words related to childbirth or birth in general, including in animals" |
| 4 | `inspect_feature` | L3, F10198 | " words related to anesthetics and medical procedures" |
| 5 | `get_upstream_features` | L3:F9008@46, k=10 | Emb:" delivery"@46 (de=14.25) +9 more |
| 6 | `inspect_feature` | L1, F12174 | " words relating to ways things are conventionally done, potential prob" |
| 7 | `inspect_feature` | L1, F1013 | " words associated with distribution, sometimes in the context of biolo" |
| 8 | `get_upstream_features` | L3:F10198@46, k=10 | Emb:" delivery"@46 (de=12.62) +9 more |
| 9 | `get_upstream_features` | L1:F12174@46, k=10 | Emb:" labor"@44 (de=5.66) +9 more |
| 10 | `inspect_feature` | L0, F13670 | " words related to retail establishments and activities" |
| 11 | `inspect_feature` | L1, F3409 | " language concerning medical research studies" |
| 12 | `inspect_feature` | L0, F8978 | " the word "sole" or other words containing "long"" |
| 13 | `inspect_feature` | L0, F2318 | " the word "never"." |

**Findings:** The medical‑environment detector (L4:4665) is driven largely by the input tokens 'labor' and 'nurse'. These feed into two mid‑layer medical semantic detectors (L3:9008 for birth/delivery and L3:10198 for anesthetic procedures), each of which is strongly excited by the token 'delivery' and also by 'labor'. Both mid‑layer detectors forward activation to the target. A low‑layer generic convention fea…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×6 | L0:1832, L4:9757, L4:12178, L6:9980, L0:10846, L7:3979 |
| 2 | `get_upstream_features` | L14:F3985@8, k=8 → Emb:" practitioner"@8 (de=6.19) +7 more |
| 3 | `get_upstream_features` | L15:F15159@7, k=8 → Emb:" nurse"@7 (de=17.50) +7 more |
| 4 | `inspect_feature` ×2 | L0:3175, L0:15382 |
| 5 | `get_upstream_features` | L0:F15382@1, k=5 → Emb:"She"@1 (de=16.88) +4 more |
| 6 | `get_upstream_features` | L4:F4665@46, k=5 → Emb:" labor"@44 (de=3.45) +4 more |
| 7 | `inspect_feature` | L5, F9749 → " words related to various medical conditions, procedures, and practiti" |

### Build

`build_circuit` → 23 nodes, 33 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 41,213 | 5,712 | 112,597 | 0 | $0.0260 | — | — |
| SA-2 | openai/gpt-oss-120b | 91,143 | 6,654 | 64 | 0 | $0.0177 | ✅ 5F/10E | Trace what inputs drive the nursing profession feature at L6… |
| SA-3 | openai/gpt-oss-120b | 187,168 | 12,919 | 19,680 | 0 | $0.0361 | ✅ 8F/17E | Trace what inputs drive the medical environments feature at … |
| **Total** | | **319,524** | **25,285** | **132,341** | **0** | **$0.0798** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 38s