# Circuit Oracle Report
**Date:** 2026-07-28 07:00:14 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of this person's profession is driven primarily by a confluence of (a) academic-credential pattern features (BS/PhD/University tokens) and (b) male-pronoun/male-biased features that fire on "His/He", with the male-pronoun features contributing positively to the probe score at multiple early layers.

**Confidence:** 7

**Reasoning:** The circuit shows the probe direction is fed by two major streams that converge at the output:

1. **Academic-credential stream (the legitimate profession signal):** `Emb: " BS" (17)` and `Emb: " PhD" (27)` activate L2 features L2:F10852 ("academic titles and degrees"), L3:F4213 ("degree qualifications or awards"), L6:F2254 ("references to academic degrees"), and L7:F14129 ("academic degrees, universities"). These flow into L17:F11003 ("university") and L20:F14235 ("academic credentials and institutions", promoting tokens like "University/UCLA/Cornell") at pos 31. This stream genuinely encodes the subject's profession (academic/researcher).

2. **Male-pronoun / spurious gender stream:** L0:F1069 (direct_effect +0.0698, "references to a male person, particularly when using the pronoun 'He' or 'His'"), L0:F2994 (direct_effect -0.0388 on "his"/"he"), and L2:F3877 ("references to 'His' and religious figures") all fire on `Emb: "His" (pos 1)`. Critically, L0:F1069 has direct_effect = **+0.0698**, the single largest positive contribution to the probe at the output level. The early male-pronoun node is the top positive direct contributor to the probe score.

The user's concern is **validated**: the probe relies substantially on a gender-marker feature (male pronoun detection) that is causally upstream of — and roughly equal in magnitude to — the legitimate academic-credential pathway. The circuit contains a direct edge from `early_male_pronoun` (L0-L2) to the `probe_output`. While the academic-credential pathway is also strong (L20:F14235 promoting "UC/Cornell/UCLA" tokens), the co-occurrence of a strongly positive male-pronoun contribution (L0:F1069) means the probe's classification score is being partially driven by "He/His" as a gender marker rather than purely by profession-indicating content like "visualization", "PhD", and university names. The academic-credential features at L6-L20 are real profession indicators, but they sit alongside — and are partially overshadowed at the early-layer entry point by — a spurious gender feature that fires on the very first token.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'His' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: ' research' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: ' interests' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: ' visualization' (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: ' graphics' (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: ' BS' (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 27 | Emb: ' PhD' (pos 27) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 31 | Emb: ' from' (pos 31) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Early male pronoun detectors (L0-L2) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | Early male pronoun detectors (L0-L2) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L2:F3877](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3877) | 1 | Early male pronoun detectors (L0-L2) |  references to "His" and religious figures or concepts | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3877) |
| [L1:F10986](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) | 3 | Research-interests/college phrase detectors (L0-L1) |  words related to academic research | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) |
| [L5:F12330](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12330) | 13 | Research-interests/college phrase detectors (L0-L1) | mentions of "College" along with a preceding place name like "County" or "Valley" | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12330) |
| [L2:F1621](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1621) | 3 | Career/education pattern features (L2-L3) |  information about people's education and career | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1621) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 17 | Career/education pattern features (L2-L3) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 27 | Career/education pattern features (L2-L3) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L3:F4213](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) | 21 | Career/education pattern features (L2-L3) |  mentions of degree qualifications or awards | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) |
| [L3:F4213](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) | 31 | Career/education pattern features (L2-L3) |  mentions of degree qualifications or awards | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 17 | Academic-degree detectors (L6-L7) | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 27 | Academic-degree detectors (L6-L7) | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 27 | Academic-degree detectors (L6-L7) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L7:F3549](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3549) | 9 | Visualization/graphics technical content (L7-L8) |  technical text containing numbers and letters, possibly related to medicine, mathematics or computer programming. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3549) |
| [L7:F16358](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/16358) | 9 | Visualization/graphics technical content (L7-L8) |  text referencing design and virtual reality. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/16358) |
| [L8:F11284](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) | 13 | Visualization/graphics technical content (L7-L8) |  words and phrases related to people's names, titles, universities, and research | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) |
| [L14:F11252](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11252) | 9 | Code/geometry technical feature (L14) |  code and coordinate geometry terms | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11252) |
| [L17:F11003](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) | 31 | Academic credential aggregators (L17-L20) | university | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) |
| [L19:F2496](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2496) | 31 | Academic credential aggregators (L17-L20) |  mentions of universities and degrees | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2496) |
| [L20:F14235](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) | 31 | Academic credential aggregators (L17-L20) |  references to academic credentials and institutions. | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe classification score | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:1069 de=0.070 |
| 3 | `inspect_feature` ×4 | L0:1069, L1:10986, L5:12330, L4:9757 |
| 4 | `get_upstream_features` | Emb:"His"@1 (de=21.62) +9 more |
| 5 | `get_upstream_features` | Emb:" research"@2 (de=6.62) +9 more |
| 6 | `get_upstream_features` | Emb:"<bos>"@0 (de=-3.23) +9 more |
| 7 | `inspect_feature` ×15 | L0:2994, L0:2159, L0:10783, L0:13431, L0:6446, L2:1621, L2:3877, L2:10852, L3:4213, L7:14129, L6:2254, L20:14235, L8:11284, L14:11252, L6:6331 |
| 8 | `get_upstream_features` | Emb:"His"@1 (de=19.75) +4 more |
| 9 | `get_upstream_features` | Emb:" interests"@3 (de=11.75) +4 more |
| 10 | `get_upstream_features` | Emb:" visualization"@9 (de=6.06) +9 more |
| 11 | `get_upstream_features` | Emb:" research"@2 (de=3.94) +4 more |
| 12 | `get_upstream_features` | L17:F11003 (de=30.38) +9 more |
| 13 | `get_upstream_features` | Emb:" PhD"@27 (de=19.25) +9 more |
| 14 | `get_upstream_features` | Emb:" BS"@17 (de=18.38) +9 more |
| 15 | `get_upstream_features` | Emb:" from"@21 (de=11.19) +9 more |
| 16 | `get_upstream_features` | Emb:" PhD"@27 (de=9.50) +4 more |
| 17 | `get_upstream_features` | L17:F11003 (de=14.12) +4 more |
| 18 | `inspect_feature` ×2 | L17:11003, L19:2496 |
| 19 | `get_upstream_features` | Emb:" visualization"@9 (de=6.06) +14 more |
| 20 | `get_upstream_features` | Emb:" research"@2 (de=3.94) +9 more |
| 21 | `get_upstream_features` | Emb:" BS"@17 (de=15.44) +7 more |
| 22 | `get_upstream_features` | Emb:" PhD"@27 (de=29.50) +7 more |
| 23 | `get_upstream_features` | Emb:" visualization"@9 (de=6.06) +4 more |
| 24 | `get_upstream_features` | Emb:"<bos>"@0 (de=-3.23) +4 more |
| 25 | `inspect_feature` ×2 | L7:3549, L7:16358 |
| 26 | `get_upstream_features` | Emb:" visualization"@9 (de=6.06) +19 more |
| 27 | `get_upstream_features` | Emb:" research"@2 (de=6.62) +4 more |

### Build

`build_circuit` → 16 nodes, 31 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 68,353 | 6,021 | 338,918 | 0 | $0.0481 | — | — |
| **Total** | | **68,353** | **6,021** | **338,918** | **0** | **$0.0481** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 23s