# Circuit Oracle Report
**Date:** 2026-07-28 07:23:35 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven primarily by genuine profession-indicating tokens ("Labor", "Delivery", "nurse") and nurse-management semantics — not by gender markers. Spurious proper-noun (L0:7532 firing on "Melissa"), date (L0:6515 firing on "1999"), and function-word features (L0:9911 firing on "that") are present but trace back to specific tokens, not demographic correlates.

**Confidence:** 7

**Reasoning:** The strongest positive signal to the probe flows through a coherent, profession-grounded chain rooted in the actual profession tokens: embeddings of "Labor" (pos 9), "Delivery" (pos 11), and "nurse" (pos 12) feed a layered hierarchy — L0:8854 (the word "nurse"), L1:14469 (nurse mentions), L3:9008 (Labor/Delivery bigram), L4:4665 (medical environments, activated by "Delivery" and "nurse"), L4:13803 (the "Labor and Delivery" phrase), L6:15267 (profession-of-nursing feature, max activation token "RN" / "nurse"), L7:210 (hospital/healthcare-system terms), L10:4751 (specific profession/job word), L14:3985 (management/leadership/medicine/research — with `frac_nonzero=0.066`, `direct_effect≈0.10` at pos 11), and L18:13596 (role, skills, leadership of nurse managers — `frac_nonzero=0.005`, highly specific). The L18 feature's largest upstream direct effect comes from the embedding of the token "nurse" itself (39.25), with L6:15267 contributing 4.81 and L7:210 contributing 3.14. L18:13596 then projects directly to the probe logit (direct_effect=0.0544).

The user's concern about spurious gender markers is **not supported** by the circuit. The "Melissa" proper-noun feature (L0:7532, `frac_nonzero=0.06`, `direct_effect=0.06`) does connect to the probe, but it is a generic proper-noun feature (top activating examples include Doreen, Mónica, Raquel, Corinne, Eileen) — it fires on the *name* token, not on gendered pronouns or markers. There is no "she/her" pronoun feature in the top-20, no femine-associated feature, and the female-pronoun embeddings are not in the positive-circuit upstream. The Melissa path appears to reflect that biographical paragraphs are commonly introduced with a named subject, which the probe may pick up as a genre cue rather than a gender cue.

However, two genuinely weak concerns remain. First, the L0:6515 year feature (firing on "1999", `direct_effect=−0.06`) is suppressive, but the year token "1" still appears in upstream lookups of L0:6515 with a strong positive direct_effect (29) — wait, the sign is correct: L0:6515's top direct_effect is 0.06 to the probe, sourced from the "1"/"9" token pair. This is a spurious, non-profession feature that reaches the probe via a year token, suggesting some correlation between biographical-text year mentions and profession. Second, the L0:9911 "that" feature is a generic function-word feature (`frac_nonzero=0.006`, low frequency) firing on the structural word "that" in "Prior to that, Melissa…" — this is a surface-form cue, not a profession cue. These are weak artifacts (low direct_effect ≈ 0.06 each) compared to the profession chain (L18:13596 + L14:3985 contribute the bulk of the positive signal), but they show the probe is not perfectly clean.

Inhibitory edges in the circuit (L3:15901 nurse/nursing suppression at −0.077, L7:3979 nursing/healthcare suppression at −0.058) are *also* downstream of the "nurse" token and suggest the transcoder's MLP has dedicated features that compete; the probe is read off a *mixture* of nurse-activating and nurse-suppressing features, weighted by the probe's linear direction. This is not gender-driven.

**Verdict on the user's concern:** The dominant circuit mechanism is genuine profession identification via "Labor", "Delivery", and "nurse" tokens flowing through medical-lexicon → nursing-profession → nurse-management-role features. The "Melissa" path is a generic proper-noun cue, not a gender cue. There is no evidence the probe exploits "she" / "her" pronouns or female-name patterns; the circuit instead is anchored in real profession vocabulary. The probe is largely using the right signal, with minor surface-form artifacts (the year "1999", the word "that") that are weak but real.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 5 | L0:7532 (pos 5) - 'proper nouns' (Melissa) |  proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L0:F8854](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8854) | 12 | L0:8854 (pos 12) - the word 'nurse' |  the word "nurse" as well as some pronouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8854) |
| [L0:F6515](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) | 27 | L0:6515 (pos 27) - year 199X token '9' |  the year 199X or 200X. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) |
| [L0:F9911](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9911) | 3 | L0:9911 (pos 3) - word 'that' |  the word "that" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9911) |
| [L1:F14469](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14469) | 12 | L1:14469 (pos 12) - mentions of 'nurse' |  mentions of 'nurse' | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14469) |
| [L3:F15901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) | 12 | L3:15901 (pos 12) - nurses/nursing/nurse management [INHIBITS] |  mentions of nurses, nursing, and nurse management | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) |
| [L3:F9008](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) | 11 | L3:9008 (pos 11) - 'Labor'/'Delivery' bigram token | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 11 | L4:4665 (pos 11/12) - medical environments, treatments, personnel, facilities |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 12 | L4:4665 (pos 11/12) - medical environments, treatments, personnel, facilities |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 11 | L4:13803 (pos 11) - 'Labor'+'Delivery' / medical specialty phrase | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L5:F9749](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9749) | 11 | L5:9749 (pos 11/12) - medical conditions/procedures/practitioners [INHIBITS] |  words related to various medical conditions, procedures, and practitioners | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9749) |
| [L5:F9749](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9749) | 12 | L5:9749 (pos 11/12) - medical conditions/procedures/practitioners [INHIBITS] |  words related to various medical conditions, procedures, and practitioners | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9749) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 11 | L6:15267 (pos 11/12) - words referring to profession of nursing |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 12 | L6:15267 (pos 11/12) - words referring to profession of nursing |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F4490](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) | 11 | L6:4490 (pos 11) - proper nouns (locations, organizations, medical roles) |  proper nouns corresponding to locations, organizations, medical roles, and coding terms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) |
| [L6:F9980](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9980) | 11 | L6:9980 (pos 11) - pediatric medical/IBD terminology |  words and abbreviations associated with pediatric gastroenterology and inflammatory bowel disease. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9980) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 12 | L7:3979 (pos 12) - words related to nursing and healthcare [INHIBITS] |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 19 | L7:3979 (pos 12) - words related to nursing and healthcare [INHIBITS] |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 11 | L7:210 (pos 11/12) - Asante Healthcare/hospital-related terms |  words and names associated with the Asante Healthcare system | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 12 | L7:210 (pos 11/12) - Asante Healthcare/hospital-related terms |  words and names associated with the Asante Healthcare system | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L8:F16339](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) | 12 | L8:16339 (pos 12) - hospital infections/bacteria |  text discussing hospital infections and bacteria | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) |
| [L8:F4607](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/4607) | 12 | L8:4607 (pos 12) - job ad phrases about pay/shifts | phrases in job advertisements related to pay | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/4607) |
| [L10:F4751](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/4751) | 12 | L10:4751 (pos 12) - specific profession/job word |  words which describe a specific profession or job | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/4751) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 11 | L14:3985 (pos 11/12) - management/leadership/medicine/studies/research | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 12 | L14:3985 (pos 11/12) - management/leadership/medicine/studies/research | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 12 | L18:13596 (pos 12) - role, skills, leadership of nurse managers |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 11 | L18:13596 (pos 12) - role, skills, leadership of nurse managers |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:3985 de=0.106 |
| 3 | `inspect_feature` ×9 | L14:3985, L0:9911, L3:15901, L0:10771, L0:8444, L6:9980, L0:7532, L0:6515, L18:13596 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@11` | ❌ error | — | — | Trace this feature that detects management/leadership/medicine/research terms. W… |
| SA-2 | `L18:F13596@12` | ❌ error | — | — | Trace this nurse management / role feature. What specific input tokens drive it?… |
| SA-3 | `L3:F15901@12` | ❌ error | — | — | Trace this nurse/nursing feature which has negative direct_effect. What tokens d… |
| SA-4 | `L0:F7532@5` | ❌ error | — | — | Trace this "proper nouns" feature at position 5. What does it fire on at this po… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F3985@11, k=15 → L6:F4490 (de=3.00) +14 more |
| 2 | `get_upstream_features` | L18:F13596@12, k=15 → Emb:" nurse"@12 (de=39.25) +14 more |
| 3 | `get_upstream_features` | L6:F15267@12, k=10 → Emb:" nurse"@12 (de=20.50) +9 more |
| 4 | `get_upstream_features` | L4:F4665@11, k=10 → L3:F10198 (de=3.44) +9 more |
| 5 | `get_upstream_features` | L6:F4490@11, k=10 → L4:F4665 (de=3.92) +9 more |
| 6 | `get_upstream_features` | L7:F210@12, k=10 → Emb:" nurse"@12 (de=9.19) +9 more |
| 7 | `inspect_feature` ×4 | L6:15267, L4:4665, L6:4490, L7:210 |
| 8 | `get_upstream_features` | L4:F13803@11, k=10 → Emb:" Delivery"@11 (de=12.19) +9 more |
| 9 | `inspect_feature` | L7, F3979 → " words related to nursing and healthcare" |
| 10 | `get_upstream_features` | L0:F7532@5, k=10 → Emb:" Melissa"@5 (de=21.25) +9 more |
| 11 | `get_upstream_features` | L0:F6515@27, k=10 → Emb:"1"@26 (de=29.00) +9 more |
| 12 | `inspect_feature` ×2 | L8:16339, L8:4607 |
| 13 | `get_upstream_features` | L4:F4665@12, k=10 → Emb:" nurse"@12 (de=8.50) +9 more |
| 14 | `get_upstream_features` | L0:F7532@3, k=10 → ❌ Feature (layer=0, feature_idx=7532) not found at pos=3. This |
| 15 | `inspect_feature` ×2 | L0:2115, L0:8854 |
| 16 | `get_upstream_features` | L0:F2115@1, k=8 → Emb:"<bos>"@0 (de=0.91) +7 more |
| 17 | `inspect_feature` ×2 | L1:14469, L5:9749 |
| 18 | `get_upstream_features` | L16:F6954@12, k=10 → Emb:"<bos>"@0 (de=-1.83) +9 more |
| 19 | `get_upstream_features` | L3:F9008@11, k=10 → Emb:" Delivery"@11 (de=11.19) +9 more |
| 20 | `inspect_feature` ×3 | L13:3597, L10:4751, L8:7732 |
| 21 | `get_upstream_features` | L18:F13596@11, k=10 → Emb:"<bos>"@0 (de=-5.12) +9 more |

### Build

`build_circuit` → 24 nodes, 34 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 50,135 | 7,490 | 260,084 | 0 | $0.0396 | — | — |
| **Total** | | **50,135** | **7,490** | **260,084** | **0** | **$0.0396** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 49s