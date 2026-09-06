# Circuit Oracle Report
**Date:** 2026-07-28 07:20:03 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a mix of legitimate profession/medical-domain features (obstetrics terms like "Labor" and "Delivery", "nurse", "midwife") AND extensive gender/feminine-name features (feminine name spelling of "Melissa", "she/her" pronouns, "women being mentioned", "women's accomplishments") — confirming the user's concern that the circuit relies heavily on spurious gender markers.

**Confidence:** 8

**Reasoning:** The attribution graph reveals a dual-pathway circuit. The **legitimate profession pathway** runs from the tokens "Labor" (pos 9) and "Delivery" (pos 11) through the childbirth-word feature L3:9008 into L4:13803 ("terms related to obstetrics and gynecology," frac_nonzero 0.0138, promotes tokens like "pregnancy", "postpartum", "fertility") and onward to the nursing-profession feature L6:15267 ("words referring to nursing," promotes "RN", "nurse") and L12:14970 ("names of people"). The "midwife" token at pos 66 also strongly activates L4:13803 (direct_effect 22.375 from embedding), providing additional profession evidence. The **spurious gender pathway** is, however, equally prominent. The token " Melissa" at pos 5 directly excites L4:1276 (capitalized names, direct_effect 4.22), L6:8166 (proper names ending in 'a/i/e' — a feminine-name-spelling detector, direct_effect 0.37 to logit), and L6:11646 (references to women, direct_effect 0.37). The L18:14677 supernode ("instances of women or girls being mentioned," fires at pos 31, 54, 68 with direct_effects 0.45, 0.45, 0.41) is driven not just by name/pronoun but by the token "Melissa" itself (direct_effect 1.99) and "nurse" (direct_effect 1.94), and "her" (direct_effect 2.05). The L19:9685 supernode ("women's names and accomplishments") adds another 0.44+0.28+0.27 to the logit. Note the **inhibitory gender features** (negative direct_effect): L7:8644 ("woman's name in context," −0.44) and L13:11685 ("words related to women" at pos 66, −0.37) — but these are outweighed by the positive-promotion gender features. The output logit is thus pushed up by a combination of: (a) genuine profession terms (obstetrics, nursing, midwife) and (b) heavy gender/feminine-name signals that activate on Melissa's name and the surrounding she/her pronouns. The user is correct: the probe is not relying solely on spurious features, but gender markers constitute a substantial fraction of the positive signal driving the classification, making the circuit susceptible to the bias concern. A profession-neutral signal would need to come primarily from the L4:13803/L6:15267/L12:14970 cluster rather than the L18:14677/L19:9685/L6:8166/L6:11646 cluster that fires on feminine-name tokens.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: ' Melissa' (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: ' Labor' (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 11 | Emb: ' Delivery' (pos 11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: ' nurse' (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: ' her' (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 66 | Emb: ' midwife' (pos 66) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 68 | Emb: ' She' (pos 68) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 5 | Proper noun detector (L0:7532, pos 5) |  proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L2:F5859](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) | 5 | Female first name detector (L2:5859, pos 5) |  first names (mostly female) | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) |
| [L3:F9008](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) | 11 | Childbirth/birth words (L3:9008, pos 11) |  words related to childbirth or birth in general, including in animals. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 5 | Capitalized name/title detector (L4:1276, pos 5) | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 11 | Obstetrics/gynecology terms (L4:13803, pos 11 & 66) |  terms related to obstetrics and gynecology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 66 | Obstetrics/gynecology terms (L4:13803, pos 11 & 66) |  terms related to obstetrics and gynecology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 12 | Nursing profession words (L6:15267, pos 12) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F8166](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) | 5 | Proper names ending in a/i/e (L6:8166, pos 5) |  proper names longer than 4 characters and ending in 'a', 'i', or 'e' | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 5 | References to women (L6:11646, pos 5) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 12 | Woman's name in context (L7:8644, pos 12) - INHIBITORY |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 5 | Names of people (L12:14970, pos 5) |  names of people, both first and last names | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L13:F11685](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/11685) | 66 | Words related to women (L13:11685, pos 66) - INHIBITORY |  words related to women | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/11685) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 31 | Women/girls being mentioned (L18:14677, pos 31) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 54 | Women/girls being mentioned (L18:14677, pos 31) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 68 | Women/girls being mentioned (L18:14677, pos 31) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 31 | Women's names & accomplishments (L19:9685, pos 31/54/86) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 54 | Women's names & accomplishments (L19:9685, pos 31/54/86) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 86 | Women's names & accomplishments (L19:9685, pos 31/54/86) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:1276 de=0.559 |
| 3 | `inspect_feature` ×10 | L4:1276, L12:14970, L6:8166, L4:13803, L18:14677, L7:8644, L19:9685, L6:11646, L13:11685, L0:7532 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F9685@31` | ❌ error | — | — | Trace L19:F9685 upstream — this is a "women's names and accomplishments" feature… |
| SA-2 | `L18:F14677@31` | ❌ error | — | — | Trace L18:F14677 upstream — this is a "instances of women or girls being mention… |
| SA-3 | `L4:F13803@11` | ✅ reported | 4 | 5 | Trace L4:F13803 upstream — this is a "terms related to obstetrics and gynecology… |
| SA-4 | `L6:F8166@5` | ✅ reported | 4 | 3 | Trace L6:F8166 upstream — this is a "proper names longer than 4 characters and e… |

<details>
<summary><b>SA-3</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13803 | " terms related to obstetrics and gynecology" |
| 2 | `get_upstream_features` | L4:F13803@11, k=10 | Emb:" Delivery"@11 (de=12.19) +9 more |
| 3 | `inspect_feature` | L3, F9008 | " words related to childbirth or birth in general, including in animals" |
| 4 | `get_upstream_features` | L3:F9008@11, k=10 | Emb:" Delivery"@11 (de=11.19) +9 more |
| 5 | `inspect_feature` | L1, F12174 | " words relating to ways things are conventionally done, potential prob" |
| 6 | `inspect_feature` | L1, F7152 | "the word "delivery"" |
| 7 | `get_upstream_features` | L1:F12174@11, k=10 | Emb:" Labor"@9 (de=7.06) +9 more |

**Findings:** The target obstetrics feature (L4:F13803) is driven primarily by the input tokens "Delivery" (pos 11) and "Labor" (pos 9), both of which have large positive direct effects. These tokens feed into an intermediate childbirth‑related detector (L3:F9008), which in turn activates the target. Additional modest contributions come from a generic labor‑related detector (L1:F12174) and a delivery‑specific t…

</details>

<details>
<summary><b>SA-4</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F8166 | " proper names longer than 4 characters and ending in 'a', 'i', or 'e'" |
| 2 | `get_upstream_features` | L6:F8166@5, k=10 | L4:F1276 (de=5.19) +9 more |
| 3 | `inspect_feature` | L4, F1276 | "capitalized names and titles, and names with lowercase letters in the " |
| 4 | `get_upstream_features` | L4:F1276@5, k=10 | Emb:" Melissa"@5 (de=9.62) +9 more |
| 5 | `inspect_feature` | L0, F7532 | " proper nouns" |
| 6 | `get_upstream_features` | L0:F7532@5, k=10 | Emb:" Melissa"@5 (de=21.25) +9 more |
| 7 | `inspect_feature` | L2, F5859 | " first names (mostly female)" |
| 8 | `inspect_feature` | L4, F8939 | " proper names of people and organizations" |
| 9 | `get_upstream_features` | L2:F5859@5, k=10 | L0:F7532 (de=5.28) +9 more |

**Findings:** The circuit for L6:F8166 (detecting proper names >4 chars ending in a/i/e) is driven primarily by a capitalized‑name feature (L4:1276). That feature receives strong positive input from a generic proper‑noun detector (L0:7532) which is directly activated by the token "Melissa" (embedding). A female‑first‑name detector (L2:5859) also contributes positively. All upstream nodes lie in low layers (≤8) …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14677@31, k=10 → L14:F4385 (de=2.17) +9 more |
| 2 | `get_upstream_features` | L19:F9685@31, k=10 → Emb:" nurse"@12 (de=2.33) +9 more |
| 3 | `get_upstream_features` | L4:F13803@66, k=10 → Emb:" midwife"@66 (de=22.38) +9 more |
| 4 | `inspect_feature` ×6 | L2:5859, L18:3679, L18:9023, L14:4385, L14:12501, L13:4753 |
| 5 | `get_upstream_features` | L7:F8644@12, k=10 → Emb:" nurse"@12 (de=5.62) +9 more |
| 6 | `get_upstream_features` | L18:F14677@68, k=10 → Emb:" She"@68 (de=14.06) +9 more |
| 7 | `get_upstream_features` | L4:F13803@11, k=10 → Emb:" Delivery"@11 (de=12.19) +9 more |
| 8 | `inspect_feature` ×5 | L17:5889, L15:3330, L6:16329, L6:15267, L3:9008 |

### Build

`build_circuit` → 21 nodes, 35 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 44,450 | 5,879 | 209,182 | 0 | $0.0329 | — | — |
| SA-3 | openai/gpt-oss-120b | 64,814 | 3,608 | 0 | 0 | $0.0119 | ✅ 4F/5E | Trace L4:F13803 upstream — this is a "terms related to obste… |
| SA-4 | openai/gpt-oss-120b | 91,321 | 5,059 | 8,160 | 0 | $0.0169 | ✅ 4F/3E | Trace L6:F8166 upstream — this is a "proper names longer tha… |
| **Total** | | **200,585** | **14,546** | **217,342** | **0** | **$0.0617** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 48s