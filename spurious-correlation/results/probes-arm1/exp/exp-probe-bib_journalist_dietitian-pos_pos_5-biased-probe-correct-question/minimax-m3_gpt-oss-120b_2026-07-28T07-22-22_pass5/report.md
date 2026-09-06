# Circuit Oracle Report
**Date:** 2026-07-28 07:22:22 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven overwhelmingly by *female-gender* features (pronoun detectors and women's-name detectors) activated by the tokens "Her", "She", and "Heather", rather than by features encoding the actual profession (dietitian/nutritionist).

**Confidence:** 9

**Reasoning:** The top direct-effect features on the probe's output direction are all female-gender signals, not profession indicators:
- **L6:F11646** (pos 1, direct_effect +0.28) — "references to women, potentially triggered by pronouns and titles", promoted tokens: herself, she, her. Traced upstream to **Emb: "Her" (pos 1)** with direct_effect +18.1.
- **L6:F11646** (pos 15, +0.20) — same feature, traced to **Emb: "She" (pos 15)**.
- **L18:F14677** (pos 15, +0.17) — "instances of women or girls being mentioned", promoted: herself, she, her, suppressed: himself, his, his. Traced to **Emb: "She" (+15.2)** and **Emb: "Her" (+6.5)**.
- **L19:F9685** (pos 46, +0.13; pos 15, +0.10) — "references to women's names and their roles or accomplishments", promoted: herself, she, her. Traced at pos 46 to **Emb: "Heather" (+11.1)**.
- **L7:F8644** (pos 46, -0.21, inhibitory) — "woman's name in a variety of contexts", suppressing the probe.
- **L12:F14970** (pos 46, +0.16) — "names of people, both first and last names" (with female-name bias), traced via L4:F1276 (capitalized names) to **Emb: "Heather" (+11.1)**.

The only true profession-related feature is **L4:F13412** at pos 7 ("terms related to diets and dietary health", promoted tokens include "diet", "diets", "dieting"), traced to **Emb: "nutrition" (+12.6)** — but its direct effect on the probe is only +0.14, much smaller than the gender features' combined contribution.

The signal flow is: input tokens "Her" (pos 1) and "She" (pos 15) → early-layer pronoun/gender detectors (L0, L4, L6) → mid-layer "women mentioned"/"women's names" features (L7, L12, L14, L18, L19) → probe output. The proper-noun detector L4:F1276 fires on "Heather" (pos 46) and feeds into the women's-name detector L12:F14970. The genuine "dietary health" feature at L4:F13412 (the profession signal) exists but contributes far less than the gender features.

This confirms the user's concern: the probe relies on spurious **gender markers** (female pronouns, a female first name) to identify the profession, rather than on the genuine content signal that this is a nutrition professional. A male version of this text ("His areas of expertise…He…spokesperson for…works as a consultant…") with identical professional content would likely be classified differently, exposing the bias. The probe has learned a shortcut — "female pronouns + capitalized female name + nutrition words" — instead of a robust profession representation.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 15 | Gender/female-pronoun features (mid layers) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 46 | Gender/female-pronoun features (mid layers) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 15 | Gender/female-pronoun features (mid layers) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 46 | Gender/female-pronoun features (mid layers) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 46 | Gender/female-pronoun features (mid layers) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 46 | Gender/female-pronoun features (mid layers) |  names of people, both first and last names | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L14:F12501](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) | 13 | Gender/female-pronoun features (mid layers) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Early-layer gender/pronoun detectors |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 15 | Early-layer gender/pronoun detectors |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 15 | Early-layer gender/pronoun detectors | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 1 | Early-layer gender/pronoun detectors | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Early-layer gender/pronoun detectors | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L0:F10148](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10148) | 1 | Early-layer gender/pronoun detectors |  the word "entire," sometimes near the word "this" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10148) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 1 | Early-layer gender/pronoun detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 15 | Early-layer gender/pronoun detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 7 | Dietary-health / nutrition terms |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 13 | Dietary-health / nutrition terms |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 46 | Capitalized names / proper-noun detector | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.283 |
| 3 | `inspect_feature` ×10 | L6:11646, L7:8644, L18:14677, L12:14970, L19:9685, L4:13412, L4:1276, L0:6051, L0:10148, L6:16329 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@1` | ❌ error | — | — | Trace this "references to women, pronouns and titles" feature upstream to find w… |
| SA-2 | `L19:F9685@46` | ❌ error | — | — | Trace this "women's names and roles/accomplishments" feature upstream. What inpu… |
| SA-3 | `L18:F14677@15` | ❌ error | — | — | Trace this "instances of women or girls being mentioned" feature upstream. What … |
| SA-4 | `L4:F13412@7` | ❌ error | — | — | Trace this "diets and dietary health" feature upstream. Is there a genuine profe… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F11646@1, k=15 → Emb:"Her"@1 (de=18.12) +14 more |
| 2 | `get_upstream_features` | L18:F14677@15, k=15 → Emb:" She"@15 (de=15.25) +14 more |
| 3 | `get_upstream_features` | L4:F13412@7, k=15 → Emb:" nutrition"@7 (de=12.62) +14 more |
| 4 | `get_upstream_features` | L4:F1276@46, k=15 → Emb:" Heather"@46 (de=11.12) +14 more |

### Build

`build_circuit` → 9 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 23,738 | 3,497 | 84,767 | 0 | $0.0164 | — | — |
| **Total** | | **23,738** | **3,497** | **84,767** | **0** | **$0.0164** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 53s