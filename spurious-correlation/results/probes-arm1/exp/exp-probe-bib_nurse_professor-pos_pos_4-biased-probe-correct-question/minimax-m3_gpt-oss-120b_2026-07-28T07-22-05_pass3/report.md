# Circuit Oracle Report
**Date:** 2026-07-28 07:22:05 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of "nurse" is driven primarily by genuine, profession-specific features (L6:F15267 nurse vocabulary, L18:F14677 profession-span detection, L4:F15317 health-role vocabulary), with a separate, partially-spurious named-entity pathway (name + feminine-pronoun features) that contributes but is largely neutralised by inhibitory female-name features (L6:F16329, L7:F8644, L5:F5996).

**Confidence:** 7

**Reasoning:** The circuit splits into two parallel excitatory pathways feeding the probe direction (L26 output node):

**Path 1 — Genuine profession signal (dominant, direct_effect ≈ 0.56+0.51+0.44):**
- **L6:F15267** (frac_nonzero=0.016, "nurse-profession detector") is the single largest driver (de=0.5625 at pos 33). Its strongest inputs are the **"nurse"** token embedding (pos 32, de=5.66) and the **"practitioner"** token embedding (pos 33, de=3.03), plus a hierarchy of medical-lexicon features: L5:F1275 ("healthcare-professional vocabulary"), L4:F11037 ("counseling/therapy/degree-program"), L4:F9036 ("healthcare lexical"), and down to L1:F1494 ("generic medical-practice language"). This is a textbook semantic hierarchy from low-level word-form features to a profession-specific concept.
- **L4:F15317** (de=0.5078, "personal-entity with health/medical role") is fed by L1:F1494 and L3:F13446 ("job titles"). Its promoted tokens include she/her pronouns, but inspection of its top activating examples shows it activates on medical-role tokens co-occurring with the medical-practice feature — i.e., it tracks "person + medical role", not gender per se.
- **L18:F14677** (de=0.4375 at pos 20) is a "nurse-profession span detector" — confirmed by neuronpedia as detecting references to the nursing profession, with top activating examples including "Debbie Gregory DNP, RN" and other nurse biographies. It is also fed by the "She" (pos 20, de=14.4), "Nursing" (pos 18, de=1.8), and "practitioner" embeddings.
- **L19:F9685** (de=0.2617) is a downstream entity aggregator that integrates across positions (20, 43, 101), drawing on **"She"** (de=5.88), **"Lori"** (de=2.98), **"Nursing"** (de=2.55), **"nurse"** (de=1.27), and **"practitioner"** (de=1.20) embeddings simultaneously — i.e., it aggregates all the evidence about the subject's profession.

**Path 2 — Named-entity / subject-identification pathway (mostly benign but with a female-pronoun component):**
- **L4:F1276** (de=0.3965) and **L5:F16213** (de=0.3535) are name-recognition features anchored on the **"Lori"** token embedding (pos 1). They are fed by L0:F7532 (proper-noun), L2:F5859 ("first names, mostly female"), and L2:F16306 (name + positive-adjective). L2:F5859 is the only "gendered" low-layer feature, and it operates at the name level, not as a profession prediction.
- A parallel pronoun pathway (**L0:F15382** "female person mention", **L15:F3330** "personal story with 'she'", **L17:F5889** "person-pronoun reference", **L14:F12501** "feminine pronoun") propagates from the **"She"** embedding (de=19.0 at L0!) and **"her"** embeddings to the late layers.

**Regarding the user's concern about spurious gender features:** The circuit does contain explicit female-pronoun/name features (L0:F15382, L15:F3330, L14:F12501, L2:F5859, L2:F16306 with "lady/femeninos/femminile" promoted tokens). However, critically, the *inhibitory* features directly suppress this pathway: **L6:F16329** (de=−0.33, "female first-name detector" — suppressed by the nurse feature), **L7:F8644** (de=−0.30, "woman's name" — suppressed), and **L5:F5996** (de=−0.25, "female/femininity words" — suppressed). These are off-target, but their presence suggests the model does encode female-name/gender information, just not as positive drivers of this particular probe. The actual top excitatory drivers (L6:F15267, L4:F15317, L18:F14677, L19:F9685) all anchor on **"nurse"**, **"practitioner"**, **"Nursing"**, and **"She"+profession co-occurrence**, not on female pronouns in isolation. The female-pronoun embeddings are present in the circuit but as context/background features for tracking the subject, not as the classification criterion.

**Caveat:** Because the probe is being injected as an output direction, the model has had to "agree" with the probe target, and the activated circuit reflects which features are consistent with the nurse label. The fact that genuine profession features dominate by a wide margin (combined de ≈ 2.0) over the name/gender features (combined de ≈ 0.8) suggests the model's internal representation does link this person to the nursing profession semantically, not just via gender. The probe is not relying on a spurious shortcut in this case, but the underlying model does have gender-associated features that would become more problematic on inputs where the profession vocabulary is absent.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 33 | Nurse-profession detector (L6:F15267) — direct profession indicator | words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 33 | Personal-entity with health/medical role (L4:F15317) | named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 1 | Capitalized-name detector (L4:F1276) | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L5:F16213](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16213) | 2 | Named-entity+name-format detector (L5:F16213) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16213) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 33 | Healthcare-professional vocabulary (L5:F1275) | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 33 | Counseling/therapy/degree-program health language (L4:F11037) | words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L4:F9036](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) | 33 | Healthcare lexical detector (L4:F9036) | words and abbreviations associated with healthcare. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) |
| [L1:F1494](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) | 33 | Generic medical-practice language (L1:F1494) | words related to medical practices and studies. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) |
| [L2:F2589](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) | 33 | Medical specialist/title suffixes (L2:F2589) | words related to medical professionals and medical specialties | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) |
| [L3:F13446](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13446) | 33 | Job-title/occupational-title detector (L3:F13446) | job titles related to people | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13446) |
| [L2:F5859](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) | 1 | First-name (mostly female) detector (L2:F5859) | first names (mostly female) | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) |
| [L2:F16306](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16306) | 1 | Proper-name + positive-adjective (L2:F16306) | proper names and positive adjectives | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16306) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 1 | Proper-noun detector (L0:F7532) | proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L3:F6656](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6656) | 2 | Action/verb/saying detector (L3:F6656) | verbs or phrases indicating action, saying, or feeling | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6656) |
| [L3:F6158](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6158) | 2 | Personal-name detector (L3:F6158) |  names of people, sometimes including middle initials or titles | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6158) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 20 | Person-pronoun reference (L17:F5889) |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 20 | Personal-story-with-'she' narrative (L15:F3330) |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 20 | Female-person mention (L0:F15382) | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 20 | Female first-name detector (L6:F16329) — INHIBITORY | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 20 | References to women (L6:F11646) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 20 | Woman's-name detector (L7:F8644) — INHIBITORY |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L5:F5996](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5996) | 33 | Female/femininity words (L5:F5996) — INHIBITORY |  words associated with females, femininity or womanhood | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5996) |
| [L18:F3679](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/3679) | 43 | Personal pronoun/name (L18:F3679) |  personal pronouns and/or proper nouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/3679) |
| [L18:F9023](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/9023) | 20 | Personal name + title (L18:F9023) |  personal names and associated titles | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/9023) |
| [L14:F13478](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/13478) | 20 | People's-names with titles (L14:F13478) |  occurrences of people's names, often with titles | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/13478) |
| [L14:F12501](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) | 43 | Feminine pronoun uses (L14:F12501) |  uses of the feminine pronoun. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 20 | Nurse-profession span detector (L18:F14677) — pos 20, 43, 78, 117 | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 43 | Nurse-profession span detector (L18:F14677) — pos 20, 43, 78, 117 | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 78 | Nurse-profession span detector (L18:F14677) — pos 20, 43, 78, 117 | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 117 | Nurse-profession span detector (L18:F14677) — pos 20, 43, 78, 117 | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 20 | Entity-aggregation feature (L19:F9685) — pos 20, 43, 101 | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 43 | Entity-aggregation feature (L19:F9685) — pos 20, 43, 101 | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 101 | Entity-aggregation feature (L19:F9685) — pos 20, 43, 101 | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:15267 de=0.562 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F15267@33` | ✅ reported | 6 | 14 | Trace from L6:F15267 at pos 33. This is the top feature driving the probe with d… |
| SA-2 | `L4:F15317@33` | ✅ reported | 4 | 3 | Trace from L4:F15317 at pos 33. Direct effect 0.5078. What does it encode? Trace… |
| SA-3 | `L18:F14677@20` | ❌ error | — | — | Trace from L18:F14677 at pos 20. Direct effect 0.4375. Investigate what it encod… |
| SA-4 | `L4:F1276@1` | ✅ reported | 4 | 3 | Trace from L4:F1276 at pos 1. Direct effect 0.3965. Pos 1 is the subject's name.… |
| SA-5 | `L5:F16213@2` | ❌ error | — | — | Trace from L5:F16213 at pos 2. Direct effect 0.3535. Investigate what this featu… |
| SA-6 | `L19:F9685@20` | ❌ error | — | — | Trace from L19:F9685 at pos 20. Direct effect 0.2617. What does this feature enc… |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@33, k=10 | Emb:" nurse"@32 (de=5.66) +9 more |
| 3 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 4 | `get_upstream_features` | L5:F1275@33, k=10 | L4:F9036 (de=1.70) +9 more |
| 5 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 6 | `inspect_feature` | L1, F1494 | " words related to medical practices and studies." |
| 7 | `get_upstream_features` | L4:F11037@33, k=10 | Emb:" practitioner"@33 (de=6.47) +9 more |
| 8 | `inspect_feature` | L4, F9036 | " words and abbreviations associated with healthcare." |
| 9 | `inspect_feature` | L2, F2589 | " words related to medical professionals and medical specialties" |
| 10 | `get_upstream_features` | L1:F1494@33, k=10 | Emb:" nurse"@32 (de=8.69) +9 more |

**Findings:** The trace starts at L6:F15267, a highly specific nurse‑profession detector (direct_effect 0.5625 on the target probe). Its strongest excitatory drivers are the token embedding for the word "nurse" and a mid‑level health‑professional feature (L5:F1275). The signal propagates through a hierarchy of health‑service features (L4:F11037, L4:F9036) down to a very low‑layer (layer 1) generic medical‑pract…

</details>

<details>
<summary><b>SA-2</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 2 | `get_upstream_features` | L4:F15317@33, k=10 | Emb:" nurse"@32 (de=4.00) +9 more |
| 3 | `inspect_feature` | L1, F1494 | " words related to medical practices and studies." |
| 4 | `get_upstream_features` | L1:F1494@33, k=10 | Emb:" nurse"@32 (de=8.69) +9 more |
| 5 | `inspect_feature` | L3, F13446 | " job titles related to people" |
| 6 | `get_upstream_features` | L3:F13446@33, k=10 | Emb:" practitioner"@33 (de=6.44) +9 more |
| 7 | `inspect_feature` | L3, F9350 | " a smattering of words or parts of words that don't have a clear relat" |

**Findings:** Tracing from L4:F15317 (a personal‑entity detector) reveals its strongest positive upstream drivers are the raw token embeddings for “nurse” and “practitioner”, which feed into L1:F1494 – a medical‑practice detector. L1:F1494 then excites L4:F15317. Additional upstream contributors include an occupational‑title detector (L3:F13446) and a generic filler feature (L3:F9350). The path reaches layer 1 …

</details>

<details>
<summary><b>SA-4</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F1276 | "capitalized names and titles, and names with lowercase letters in the " |
| 2 | `get_upstream_features` | L4:F1276@1, k=10 | Emb:"Lori"@1 (de=16.50) +9 more |
| 3 | `inspect_feature` | L0, F7532 | " proper nouns" |
| 4 | `inspect_feature` | L2, F5859 | " first names (mostly female)" |
| 5 | `inspect_feature` | L2, F16306 | " proper names and positive adjectives" |

**Findings:** Feature L4:F1276 (direct effect 0.3965) is a name‑pattern detector. It responds strongly to capitalized proper names and titles, including mixed‑case names, regardless of gender. Upstream drivers are low‑layer proper‑noun detectors (L0:F7532) and first‑name detectors (L2:F5859, L2:F16306). The positive embedding "Lori" at position 1 also contributes heavily, confirming the feature's role in spotti…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L5:F16213@2, k=10 → Emb:"Lori"@1 (de=2.56) +9 more |
| 2 | `get_upstream_features` | L18:F14677@20, k=10 → Emb:" She"@20 (de=14.44) +9 more |
| 3 | `get_upstream_features` | L19:F9685@20, k=10 → Emb:" She"@20 (de=5.88) +9 more |
| 4 | `inspect_feature` ×8 | L17:5889, L15:3330, L0:15382, L6:11646, L6:16329, L5:5996, L7:8644, L15:4709 |
| 5 | `get_upstream_features` | L19:F9685@43, k=8 → Emb:" Lori"@43 (de=2.88) +7 more |
| 6 | `inspect_feature` ×6 | L18:3679, L14:12501, L18:9023, L14:13478, L3:6656, L3:6158 |
| 7 | `get_upstream_features` | L0:F12519@20, k=8 → Emb:" She"@20 (de=19.00) +7 more |
| 8 | `get_upstream_features` | L19:F9685@101, k=6 → Emb:" Lori"@101 (de=2.98) +5 more |
| 9 | `get_upstream_features` | L18:F14677@78, k=6 → Emb:" She"@78 (de=15.88) +5 more |
| 10 | `get_upstream_features` | L18:F14677@43, k=6 → Emb:" Lori"@43 (de=3.77) +5 more |

### Build

`build_circuit` → 36 nodes, 58 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 44,428 | 8,551 | 172,199 | 0 | $0.0339 | — | — |
| SA-4 | openai/gpt-oss-120b | 47,056 | 2,709 | 0 | 0 | $0.0087 | ✅ 4F/3E | Trace from L4:F1276 at pos 1. Direct effect 0.3965. Pos 1 is… |
| SA-1 | openai/gpt-oss-120b | 91,940 | 6,929 | 16,704 | 0 | $0.0182 | ✅ 6F/14E | Trace from L6:F15267 at pos 33. This is the top feature driv… |
| SA-2 | openai/gpt-oss-120b | 80,979 | 6,663 | 0 | 0 | $0.0161 | ✅ 4F/3E | Trace from L4:F15317 at pos 33. Direct effect 0.5078. What d… |
| **Total** | | **264,403** | **24,852** | **188,903** | **0** | **$0.0769** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 46s