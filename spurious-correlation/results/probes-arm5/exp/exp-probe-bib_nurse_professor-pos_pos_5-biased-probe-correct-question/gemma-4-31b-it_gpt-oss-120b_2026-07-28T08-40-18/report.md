# Circuit Oracle Report
**Date:** 2026-07-28 08:40:18 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe classification score is driven by a combination of genuine domain-specific professional indicators and spurious gender markers.

**Confidence:** 10/10

**Reasoning:**
The attribution circuit reveals two primary pathways contributing to the probe's classification score:

1.  **Genuine Profession Signal:** A strong signal originates from the input tokens "Labor" (pos 9) and "Delivery" (pos 11). These embeddings directly excite **OBGYN_Detection** (L4:F13803), a feature specifically tuned to obstetrics and gynecology terms (frac_nonzero: 0.0138). This feature is further supported by a birth-related detector (L3:F9008) and flows directly into the probe's output logit.

2.  **Spurious Gender Signal:** A significant portion of the classification is driven by the token "She" (pos 54). This token excites a chain of gender-detecting features, starting from early-layer markers (L6:F11646, L17:F5889) and culminating in high-layer **Female Entity Identification** nodes (L18:F14677 and L19:F9685). L18:F14677 specifically detects "instances of women or girls being mentioned," while L19:F9685 encodes "women's names and their roles." These features promote feminine pronouns (she, her, herself) and strongly excite the probe.

The presence of the gender-based path confirms the user's concern: the probe is not relying solely on the subject's role as a nurse/midwife but is also leveraging the subject's gender as a proxy for the profession, indicating a gender bias in the probe's classification mechanism.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 11 | OB/GYN Terms (Labor, Delivery) |  terms related to obstetrics and gynecology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 54 | Gender Marker Detection (She/Her) | references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 54 | Gender Marker Detection (She/Her) | references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 54 | Female Entity Identification |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 54 | Female Entity Identification |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L12:14970 de=0.559 |
| 3 | `inspect_feature` ×6 | L12:14970, L4:1276, L6:8166, L4:13803, L18:14677, L19:9685 |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@54` | ✅ reported | 8 | 12 | Trace the path from L18:F14677 and L19:F9685 to see if they are driven by gender… |
| SA-2 | `L4:F13803@11` | ✅ reported | 5 | 9 | Trace the path from L4:F13803 (obstetrics/gynecology) to see which tokens (e.g.,… |

<details>
<summary><b>SA-1</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@54, k=10 | Emb:" She"@54 (de=14.56) +9 more |
| 3 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 4 | `inspect_feature` | L19, F9685 | " references to women's names and their roles or accomplishments." |
| 5 | `get_upstream_features` | L19:F9685@54, k=10 | Emb:" She"@54 (de=5.56) +9 more |
| 6 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 7 | `get_upstream_features` | L6:F11646@54, k=10 | Emb:" She"@54 (de=19.25) +9 more |
| 8 | `get_upstream_features` | L17:F5889@54, k=10 | Emb:" She"@54 (de=19.88) +9 more |
| 9 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 10 | `inspect_feature` | L13, F6622 | " pronouns." |
| 11 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 12 | `get_upstream_features` | L13:F6622@54, k=10 | Emb:" She"@54 (de=13.38) +9 more |
| 13 | `inspect_feature` | L6, F2267 | "words that appear in programming code, legal jargon, or scientific tex" |

**Findings:** Both target features (L18:F14677 and L19:F9685) are primarily driven by the gender token "She" at position 54. The strongest upstream influence is the direct embedding of "She", a positive direct_effect that satisfies the embedding‑shortcut requirement. Additional upstream contributors include mid‑layer gender‑pronoun detectors (L17:F5889, L15:F3330, L6:F11646) and a very early layer female‑entity…

</details>

<details>
<summary><b>SA-2</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13803 | " terms related to obstetrics and gynecology" |
| 2 | `get_upstream_features` | L4:F13803@11, k=10 | Emb:" Delivery"@11 (de=12.19) +9 more |
| 3 | `inspect_feature` | L3, F9008 | " words related to childbirth or birth in general, including in animals" |
| 4 | `inspect_feature` | L1, F7152 | "the word "delivery"" |
| 5 | `inspect_feature` | L1, F10791 | "the word "delivery"" |
| 6 | `get_upstream_features` | L3:F9008@11, k=10 | Emb:" Delivery"@11 (de=11.19) +9 more |
| 7 | `inspect_feature` | L1, F12174 | " words relating to ways things are conventionally done, potential prob" |

**Findings:** The obstetrics/gynecology feature (L4:F13803) is strongly driven by the token embeddings for the words "Delivery" and "Labor", both of which have large positive direct effects. Upstream, a birth‑related feature (L3:F9008) also receives strong excitation from the same token embeddings and in turn excites the target feature. Additional shallow detectors for the word "delivery" (L1:F7152 and L1:F1079…

</details>

### Build

`build_circuit` → 6 nodes, 5 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 85,540 | 1,140 | 8,448 | 0 | $0.0125 | — | — |
| SA-2 | openai/gpt-oss-120b | 63,670 | 4,428 | 5,152 | 0 | $0.0123 | ✅ 5F/9E | Trace the path from L4:F13803 (obstetrics/gynecology) to see… |
| SA-1 | openai/gpt-oss-120b | 153,904 | 10,363 | 48,864 | 0 | $0.0300 | ✅ 8F/12E | Trace the path from L18:F14677 and L19:F9685 to see if they … |
| **Total** | | **303,114** | **15,931** | **62,464** | **0** | **$0.0549** | | |

**Oracle wall-clock time:** 9m 38s