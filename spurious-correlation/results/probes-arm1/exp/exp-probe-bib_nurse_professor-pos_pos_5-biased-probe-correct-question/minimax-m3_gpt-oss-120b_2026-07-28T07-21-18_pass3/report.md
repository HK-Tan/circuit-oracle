# Circuit Oracle Report
**Date:** 2026-07-28 07:21:18 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a mix of legitimate profession tokens (Labor, Delivery, midwife, nurse) and a dominant channel of female-gender/personhood features (She, her, Melissa as a woman's name), confirming the user's concern that gender markers are a major spurious driver.

**Confidence:** 8

**Reasoning:** The attribution graph shows the probe is driven by FOUR parallel upstream channels, only one of which is a genuine profession signal:

1. **Genuine profession channel (weak but real):** L4:F13803 (OB/GYN terms, frac_nonzero=0.014) is driven directly by the embeddings of "Labor" (pos 9, direct_effect 8.81), "Delivery" (pos 11, direct_effect 12.19), and "midwife" (pos 66, direct_effect 22.38) and fires at pos 11 (effect 0.45) and pos 66 (effect 0.32). L6:F15267 ("nursing profession") is driven almost entirely by the "nurse" embedding (pos 12, direct_effect 20.5) and contributes +0.28 to the score. These are legitimate, semantically meaningful features.

2. **Female-name-channel (strong spurious signal):** The "Melissa" embedding (pos 5) activates a cascade: L0:F7532 (proper nouns, 0.36) → L2:F5859 (first names, mostly female, 0.28) → L4:F1276 (capitalized names/titles, 0.56) → L6:F8166 (names ending in -a/-i/-e, 0.46) → L6:F11646 (women via pronouns/titles, 0.37) → L12:F14970 (names of people, 0.56). The direct_effect of 0.56 at L12 alone is the largest single contributor; this is detecting "Melissa" as a woman's name, not as a profession holder.

3. **Female-pronoun channel (strong spurious signal):** The "She" embeddings at pos 54 and 68 feed L14:F12501 (feminine pronoun, direct_effect 3.52/3.47), L15:F3330 (personal stories of women with "she", 3.52/3.47), and L17:F5889 (pronouns/possessives, 4.03/3.69) into L18:F14677 ("instances of women or girls being mentioned") at three positions (54: 0.45, 68: 0.41, 31: 0.43). The promoted tokens of F14677 are "herself, she, her" and suppressed are "himself, his" — this is purely a gender feature. L19:F9685 ("women's names + their roles/accomplishments," direct_effect 0.44) is also a combined gender+name+role feature whose top activating examples are female proper nouns, with promoted tokens "herself, she, her."

4. **Inhibitory counter-signals:** L7:F8644 (woman's name in misc contexts, −0.44) and L13:F11685 (words related to women, −0.37) actively push the probe score DOWN, but their magnitude is smaller than the excitatory women/pronoun features.

**Quantitatively, the direct_effects on the output show** that the top-15 features include 5 with substantial positive direct_effect (0.32–0.56) that are either gender/person markers (L12 names, L4 capitalized name, L6 female-name ending, L0 proper noun, L2 female first name, L6 women-via-pronouns) versus only 2 that are genuine profession markers (L4 OB/GYN, L6 nursing-profession). The L18 women/girls feature and L19 women's names+roles add another ~0.86 to the score. In total, gender/name features contribute roughly 2.5–3× the direct effect of profession features.

This confirms the user's hypothesis: the probe is partly relying on the subject's female gender (detected via the name "Melissa," the pronouns "she/her," and the pronoun-driven women-features) rather than purely on the obstetric/nursing/midwife profession vocabulary. The "midwife" profession token does activate L4:F13803 at pos 66 with strong direct_effect 0.32, but the cumulative gender signal is larger and operates on a separate pathway (L18:L19 stack) that would still fire on a Melissa-described man or on a female subject of any profession.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 5 | Proper-noun detector (L0:F7532) |  proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L2:F5859](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) | 5 | Female first-name detector (L2:F5859) |  first names (mostly female) | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) |
| [L2:F5859](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) | 31 | Female first-name detector (L2:F5859) |  first names (mostly female) | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 5 | Capitalized name/title detector (L4:F1276) | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 31 | Capitalized name/title detector (L4:F1276) | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 11 | OB/GYN terms detector (L4:F13803) |  terms related to obstetrics and gynecology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 66 | OB/GYN terms detector (L4:F13803) |  terms related to obstetrics and gynecology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L6:F8166](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) | 5 | Female-name ending detector (L6:F8166) |  proper names longer than 4 characters and ending in 'a', 'i', or 'e' | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) |
| [L6:F8166](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) | 31 | Female-name ending detector (L6:F8166) |  proper names longer than 4 characters and ending in 'a', 'i', or 'e' | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 12 | Nursing-profession term detector (L6:F15267) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 5 | Women via pronouns/titles (L6:F11646) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 54 | Women via pronouns/titles (L6:F11646) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 12 | Woman's name in misc contexts (L7:F8644) — INHIBITORY |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 54 | Woman's name in misc contexts (L7:F8644) — INHIBITORY |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 68 | Woman's name in misc contexts (L7:F8644) — INHIBITORY |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 5 | Names-of-people (L12:F14970) |  names of people, both first and last names | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L13:F11685](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/11685) | 66 | Words related to women (L13:F11685) — INHIBITORY |  words related to women | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/11685) |
| [L14:F12501](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) | 31 | Feminine pronoun use (L14:F12501) |  uses of the feminine pronoun. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) |
| [L14:F12501](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) | 54 | Feminine pronoun use (L14:F12501) |  uses of the feminine pronoun. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) |
| [L14:F12501](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) | 68 | Feminine pronoun use (L14:F12501) |  uses of the feminine pronoun. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 54 | Personal stories of women / 'she' (L15:F3330) |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 68 | Personal stories of women / 'she' (L15:F3330) |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 54 | People-via-pronouns/possessives (L17:F5889) |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 68 | People-via-pronouns/possessives (L17:F5889) |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 31 | Women/girls mentioned (L18:F14677) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 54 | Women/girls mentioned (L18:F14677) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 68 | Women/girls mentioned (L18:F14677) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 31 | Women's names + roles/accomplishments (L19:F9685) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 54 | Women's names + roles/accomplishments (L19:F9685) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token '1' is not one of the top-k next-token candidates capt |
| 3 | `get_top_features` | 15 features; top: L12:14970 de=0.559 |
| 4 | `inspect_feature` ×7 | L12:14970, L4:1276, L6:8166, L4:13803, L18:14677, L19:9685, L0:7532 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@31` | ❌ error | — | — | Trace L18:F14677 (women/girls mention feature) upstream. This feature fires on f… |
| SA-2 | `L19:F9685@31` | ❌ error | — | — | Trace L19:F9685 (women's names and their roles/accomplishments) upstream. Does i… |
| SA-3 | `L4:F13803@11` | ✅ reported | 5 | 13 | Trace L4:F13803 (obstetrics/gynecology terms) upstream. Determine which tokens d… |
| SA-4 | `L12:F14970@5` | ✅ reported | 6 | 7 | Trace L12:F14970 (names feature) upstream. Fires at pos 5. What input tokens dri… |

<details>
<summary><b>SA-3</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13803 | " terms related to obstetrics and gynecology" |
| 2 | `get_upstream_features` | L4:F13803@11, k=15 | Emb:" Delivery"@11 (de=12.19) +14 more |
| 3 | `inspect_feature` | L3, F9008 | " words related to childbirth or birth in general, including in animals" |
| 4 | `get_upstream_features` | L3:F9008@11, k=15 | Emb:" Delivery"@11 (de=11.19) +14 more |
| 5 | `inspect_feature` | L1, F12174 | " words relating to ways things are conventionally done, potential prob" |
| 6 | `get_upstream_features` | L1:F12174@11, k=15 | Emb:" Labor"@9 (de=7.06) +14 more |
| 7 | `inspect_feature` | L1, F7152 | "the word "delivery"" |
| 8 | `inspect_feature` | L1, F10791 | "the word "delivery"" |

**Findings:** Tracing from the obstetrics/gynecology feature (L4:F13803) shows that its strongest upstream drivers are the input token embeddings for "Delivery" (pos 11) and "Labor" (pos 9), providing the bulk of the positive direct effect. These feed into a mid‑layer birth‑related feature (L3:F9008), which in turn receives additional boost from a low‑layer generic aggregator (L1:F12174). Small contributions al…

</details>

<details>
<summary><b>SA-4</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F14970 | " names of people, both first and last names" |
| 2 | `get_upstream_features` | L12:F14970@5, k=10 | L4:F1276 (de=3.36) +9 more |
| 3 | `inspect_feature` | L4, F1276 | "capitalized names and titles, and names with lowercase letters in the " |
| 4 | `inspect_feature` | L0, F7532 | " proper nouns" |
| 5 | `inspect_feature` | L2, F5859 | " first names (mostly female)" |
| 6 | `get_upstream_features` | L4:F1276@5, k=10 | Emb:" Melissa"@5 (de=9.62) +9 more |

**Findings:** The L12:F14970 'names' feature is driven primarily by the raw token embedding for the word 'Melissa' (positive direct_effect 1.55) and by a cascade of lower‑layer detectors. The earliest strong upstream driver is L4:F1276, a capitalized‑name detector, which itself receives a large positive push directly from the 'Melissa' embedding (9.63). Further upstream, a generic proper‑noun detector (L0:F7532…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14677@31, k=10 → L14:F4385 (de=2.17) +9 more |
| 2 | `get_upstream_features` | L19:F9685@31, k=10 → Emb:" nurse"@12 (de=2.33) +9 more |
| 3 | `inspect_feature` ×5 | L2:5859, L7:8644, L13:11685, L6:11646, L6:15267 |
| 4 | `get_upstream_features` | L12:F14970@5, k=10 → L4:F1276 (de=3.36) +9 more |
| 5 | `get_upstream_features` | L18:F14677@54, k=10 → Emb:" She"@54 (de=14.56) +9 more |
| 6 | `get_upstream_features` | L18:F14677@68, k=10 → Emb:" She"@68 (de=14.06) +9 more |
| 7 | `get_upstream_features` | L4:F13803@66, k=10 → Emb:" midwife"@66 (de=22.38) +9 more |
| 8 | `get_upstream_features` | L6:F15267@12, k=10 → Emb:" nurse"@12 (de=20.50) +9 more |
| 9 | `get_upstream_features` | L19:F9685@54, k=8 → Emb:" She"@54 (de=5.56) +7 more |
| 10 | `inspect_feature` ×4 | L17:5889, L15:3330, L14:12501, L14:4385 |

### Build

`build_circuit` → 21 nodes, 31 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 48,330 | 6,455 | 133,291 | 0 | $0.0302 | — | — |
| SA-4 | openai/gpt-oss-120b | 58,313 | 3,328 | 2,592 | 0 | $0.0108 | ✅ 6F/7E | Trace L12:F14970 (names feature) upstream. Fires at pos 5. W… |
| SA-3 | openai/gpt-oss-120b | 80,456 | 5,775 | 2,528 | 0 | $0.0156 | ✅ 5F/13E | Trace L4:F13803 (obstetrics/gynecology terms) upstream. Dete… |
| **Total** | | **187,099** | **15,558** | **138,411** | **0** | **$0.0566** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 44s