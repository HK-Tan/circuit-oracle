# Circuit Oracle Report
**Date:** 2026-07-28 07:21:54 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "nurse" classification is driven almost entirely by genuine profession-defining tokens ("Perioperative", "nurses", "Perioperative Nursing"), channeled through a deep chain of nursing-specific and medical-context features; the "she/her" pronoun feature is a *suppressor* of the probe's positive direction, not a driver, so the user's concern about gender-based spurious correlation is not borne out by the circuit.

**Confidence:** 8

**Reasoning:**

**Main positive path (profession-grounded).** The strongest positive contributions come from features whose autointerp labels are explicitly about nursing and nursing-adjacent medical content. The chain runs from input-token embeddings all the way to the probe direction:
- The token embeddings `Emb: ' nurses' (pos 15)` (direct_effect = 42 to L18:F13596) and `Emb: 'perative' (pos 14)` (direct_effect = 6.25 to L18:F13596) supply the raw lexical signal.
- These immediately activate **early-layer nursing detectors**: L3:F15901 ("mentions of nurses, nursing, and nurse management", frac_nonzero = 0.0055, very specific), L6:F15267 ("words in the document referring to the profession of nursing", frac_nonzero = 0.016, fires on "RN", "nurse", "nursing"), L7:F3979 ("words related to nursing and healthcare", frac_nonzero = 0.008), and L2:F15437 ("words related to nurses", frac_nonzero = 0.007). These features are all low-density and entity-specific — they are NOT generic patterns. L4:F4665 (medical environments/treatments/personnel) and L7:F210 (healthcare-system names/hospitals) and L8:F16339 (hospital/clinical context) add medical-domain context.
- Mid-layer L14:F3985 ("terms related to management, leadership, medicine, studies, and research", promoted tokens include "patients", "Medical", "clinical", frac_nonzero = 0.066) integrates nursing + management vocabulary (which is the exact theme of the input — "Head Nurse", "Educational Coordinator", "Assistant Director").
- L18:F13596 ("text about the role, skills and leadership of nurse managers", promoted tokens = "Nurse"/"nursing", frac_nonzero = 0.005) and its sibling L18:F14457 ("healthcare implementation, patient care and technology", promoted = "hospital/patient/nurse") synthesize the profession + leadership context. L18:F1665 ("anesthesia", promoted = "anesthesia/incision") is a legitimate medical-specialty signal that responds to the "Perioperative" / surgical context (it appears with a *negative* direct_effect of -0.098 to the probe — i.e. it slightly *inhibits* the nurse probe, because anesthesia is more associated with physician/surgeon than with nursing; this is itself evidence the circuit is sensitive to the specific sub-specialty).
- L20:F4927 ("titles and acronyms following names, especially within the healthcare field", promoted = "nursing/Nursing/nurse", frac_nonzero = 0.017) is the late-layer driver that pushes directly into the probe direction (direct_effect ≈ +0.075, activation 56 at pos 14, 59.75 at pos 15).

**The "she" feature — inhibitory, not driving.** L18:F14677 (label: "instances of women or girls being mentioned"; promoted = "herself/she/her", suppressed = "himself/his/his") is exactly the kind of feature the user was worried about. However, its direct_effect on the probe is **−0.0645** (negative). Tracing it back, it is fed by the embedding `Emb: ' she' (pos 7)` (direct_effect 28.4 to the feature itself) and a chain L0:F12519 (the pronoun "she") → L4:F7864 → L6:F11646 → L12:F12940 → L17:F5889 (pronoun/possessive feature) → L18:F14677. Critically, this is an INHIBITORY feature for the nurse probe: it pushes the score *down*. The negative sign is not "she → nurse" but "she → ¬nurse". This makes sense given that the same generic "she/her" feature fires for women in *any* profession, so it is anticorrelated with the specific nursing signal once the nursing signal is already present. So the gender feature is actually acting as a slight *deboost* on the nurse score, not as the positive driver.

**Bottom line for the user.** The user's hypothesis is **not supported** by this circuit. The classification is anchored by token embeddings of "nurses" and "Perioperative" (pos 13–15) that flow through a coherent nursing-specific feature hierarchy — L3/L6/L7 nursing-token detectors → L14 medical-leadership integration → L18 nurse-manager synthesis → L20 healthcare-titles driver. The female-pronoun feature exists in the circuit but is *negatively* signed on the probe score, meaning the model is not using "she" as a positive proxy for "nurse" — if anything, the generic feminine-pronoun signal slightly dilutes the more specific nursing evidence. The circuit is dominated by genuine profession indicators, not gender markers.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L20:F4927](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) | 14 | Late-layer nurse/medical-management output drivers |  titles and acronyms following names, especially within the healthcare field | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) |
| [L20:F4927](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) | 15 | Late-layer nurse/medical-management output drivers |  titles and acronyms following names, especially within the healthcare field | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 14 | Mid-layer nurse-role and medical-context features |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 15 | Mid-layer nurse-role and medical-context features |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L18:F14457](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14457) | 14 | Mid-layer nurse-role and medical-context features |  words or phrases related to healthcare implementation, patient care and technology | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14457) |
| [L18:F1665](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/1665) | 14 | Mid-layer nurse-role and medical-context features | anesthesia | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/1665) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 14 | Leadership/medicine/management vocabulary features | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 15 | Leadership/medicine/management vocabulary features | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 15 | Early-layer nursing and healthcare-context detectors |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 15 | Early-layer nursing and healthcare-context detectors |  words and names associated with the Asante Healthcare system | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L8:F16339](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) | 15 | Early-layer nursing and healthcare-context detectors |  text discussing hospital infections and bacteria | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) |
| [L8:F16339](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) | 14 | Early-layer nursing and healthcare-context detectors |  text discussing hospital infections and bacteria | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 15 | Early-layer nursing and healthcare-context detectors |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 14 | Early-layer nursing and healthcare-context detectors |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L3:F15901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) | 15 | Early-layer nursing and healthcare-context detectors |  mentions of nurses, nursing, and nurse management | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) |
| [L2:F15437](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15437) | 15 | Early-layer nursing and healthcare-context detectors |  words related to nurses and sound | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15437) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 14 | Early-layer nursing and healthcare-context detectors |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 45 | Early-layer nursing and healthcare-context detectors |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 7 | Gender pronoun feature (women/girls) — INHIBITORY to probe |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 7 | Gender pronoun feature (women/girls) — INHIBITORY to probe |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 7 | Gender pronoun feature (women/girls) — INHIBITORY to probe | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 7 | Gender pronoun feature (women/girls) — INHIBITORY to probe | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 7 | Gender pronoun feature (women/girls) — INHIBITORY to probe | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L0:F12519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) | 7 | Gender pronoun feature (women/girls) — INHIBITORY to probe |  the pronoun "she" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:3985 de=0.163 |
| 3 | `inspect_feature` ×15 | L14:3985, L6:15267, L18:13596, L3:15901, L7:3979, L8:16339, L4:4665, L7:210, L20:4927, L18:14677, L2:15437, L9:16275, L18:14457, L4:8736, L4:9757 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L20:F4927@14` | ❌ error | — | — | Trace the path from L20:F4927 (titles/acronyms following names in healthcare — p… |
| SA-2 | `L18:F13596@15` | ❌ error | — | — | Trace the path from L18:F13596 (text about the role, skills and leadership of nu… |
| SA-3 | `L18:F14677@7` | ❌ error | — | — | Trace the path from L18:F14677 (instances of women or girls being mentioned — pr… |
| SA-4 | `L14:F3985@15` | ❌ error | — | — | Trace the path from L14:F3985 (terms related to management, leadership, medicine… |
| SA-5 | `L20:F4927@14` | ❌ error | — | — | Trace the path from L20:F4927 (titles/acronyms following names in healthcare — p… |
| SA-6 | `L18:F13596@15` | ❌ error | — | — | Trace the path from L18:F13596 (text about the role, skills and leadership of nu… |
| SA-7 | `L18:F14677@7` | ❌ error | — | — | Trace the path from L18:F14677 (instances of women or girls being mentioned — pr… |
| SA-8 | `L14:F3985@15` | ❌ error | — | — | Trace the path from L14:F3985 (terms related to management, leadership, medicine… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F13596@15, k=15 → Emb:" nurses"@15 (de=42.00) +14 more |
| 2 | `get_upstream_features` | L20:F4927@14, k=15 → L18:F13596 (de=14.31) +14 more |
| 3 | `get_upstream_features` | L18:F14677@7, k=15 → Emb:" she"@7 (de=28.38) +14 more |
| 4 | `get_upstream_features` | L14:F3985@15, k=15 → Emb:" nurses"@15 (de=10.62) +14 more |
| 5 | `get_upstream_features` | L6:F15267@15, k=15 → Emb:" nurses"@15 (de=16.12) +14 more |
| 6 | `get_upstream_features` | L3:F15901@15, k=15 → Emb:" nurses"@15 (de=14.88) +14 more |
| 7 | `get_upstream_features` | L4:F4665@14, k=15 → Emb:"perative"@14 (de=15.44) +14 more |
| 8 | `get_upstream_features` | L8:F16339@15, k=10 → Emb:" nurses"@15 (de=4.72) +9 more |
| 9 | `get_upstream_features` | L7:F210@15, k=10 → Emb:" nurses"@15 (de=11.38) +9 more |
| 10 | `get_upstream_features` | L14:F3985@14, k=15 → L4:F4665 (de=3.14) +14 more |
| 11 | `get_upstream_features` | L6:F11646@7, k=10 → Emb:" she"@7 (de=31.62) +9 more |
| 12 | `get_upstream_features` | L12:F12940@7, k=10 → Emb:" she"@7 (de=12.31) +9 more |
| 13 | `get_upstream_features` | L4:F7864@7, k=10 → Emb:" she"@7 (de=27.25) +9 more |
| 14 | `inspect_feature` ×2 | L17:5889, L0:12519 |
| 15 | `get_upstream_features` | L7:F3979@15, k=10 → L6:F15267 (de=7.97) +9 more |
| 16 | `inspect_feature` ×2 | L18:14457, L18:1665 |

### Build

`build_circuit` → 12 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 45,122 | 6,348 | 242,458 | 0 | $0.0357 | — | — |
| **Total** | | **45,122** | **6,348** | **242,458** | **0** | **$0.0357** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 27s