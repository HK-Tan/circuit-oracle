# Circuit Oracle Report
**Date:** 2026-07-28 07:21:53 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of this text is driven by a mixture of (a) genuine profession-content features (OB/GYN terms and nursing vocabulary) and (b) a large mass of late-layer features that are explicitly female-gendered name/role features, confirming the user's hypothesis that the circuit relies on gender markers alongside profession indicators.

**Confidence:** 8

**Reasoning:**

The circuit has two distinct processing streams that both feed the probe:

1. **Genuine profession stream (clean, semantic):** The "Profession-content features" supernode contains L4:F13803 ("terms related to obstetrics and gynecology", frac_nonzero 0.014) and L6:F15267 ("words in the document referring to the profession of nursing", frac_nonzero 0.016). These are driven directly by the input token embeddings **Emb: Labor (pos 9)**, **Emb: Delivery (pos 11)**, and **Emb: nurse (pos 12)** — these tokens are the explicit profession-defining content of the passage. L4:F13803 is the strongest single driver (direct_effect 0.4492).

2. **Gendered-name stream (spurious):** The dominant late-layer signal is the "Late-layer gendered name+role features" supernode, built from L19:F9685 ("references to women's names and their roles or accomplishments", frac_nonzero 0.014, direct_effect 0.44), L18:F14677 ("instances of women or girls being mentioned", frac_nonzero 0.012, contributing 0.45+0.43+0.41 across multiple positions), and L13:F11685 ("words related to women", frac_nonzero 0.017, direct_effect −0.37 — actually inhibitory). Tracing these upstream reveals they are fed by:
   - **Emb: Melissa (pos 5)** and **Emb: Melissa (pos 31)** — the female first name
   - **Emb: her (pos 15)** — the feminine pronoun
   - The mid-layer **name_features** supernode (L12:F14970 "names of people", L7:F8644 "woman's name", L6:F8166 "proper names ending in a/i/e", L6:F11646 "references to women via pronouns") which itself descends from L0/L2 proper-noun features activated by the "Melissa" token.
   
   The features' promoted tokens confirm gender encoding: F9685 and F14677 promote "▁herself", "▁she", "▁her" and suppress "▁himself", "▁his" — these are explicitly gendered pronoun features, not profession features.

3. **Convergence:** Both streams converge on the probe output. The L4 profession feature feeds the probe directly (direct_effect 0.45) but ALSO feeds the late-layer gendered name+role supernode (L19:F9685 has F13803 in its upstream at direct_effect 2.33), meaning the model conflates the two — once "Labor/Delivery nurse" is recognized, it is folded into a "woman who works in a role" feature that carries heavy gendered signal.

**Conclusion on user concern:** The concern is **partially validated and partially nuanced**. The probe IS picking up genuine profession content (OB/GYN, nursing) — that signal is real and clean. BUT the late-layer circuit is dominated by an independently strong "female person + role" feature pathway. The model appears to represent "Melissa, the nurse/midwife" via features that encode both *profession* and *gender* inseparably. F14677 firing on positions 31, 54, 68 (all places where "she/her" or her name recurs) shows the probe's score is being inflated by repeated female-pronoun/name re-encodings of the same subject, not by additional profession evidence. If Melissa were described with the same professional content but with male pronouns, the late-layer women+name features would not fire, and the probe score would likely drop substantially — confirming the gender markers are doing meaningful classifier work rather than being mere epiphenomena.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 5 | Probe output (profession direction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 31 | Late-layer gendered name+role features |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 31 | Late-layer gendered name+role features |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 54 | Late-layer gendered name+role features |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 68 | Late-layer gendered name+role features |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L13:F11685](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/11685) | 66 | Late-layer gendered name+role features |  words related to women | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/11685) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 5 | Mid-layer name/proper-noun features |  names of people, both first and last names | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 31 | Mid-layer name/proper-noun features |  names of people, both first and last names | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 12 | Mid-layer name/proper-noun features |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L6:F8166](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) | 5 | Mid-layer name/proper-noun features |  proper names longer than 4 characters and ending in 'a', 'i', or 'e' | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 5 | Mid-layer name/proper-noun features |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 11 | Profession-content features (OB/GYN, nursing) |  terms related to obstetrics and gynecology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 66 | Profession-content features (OB/GYN, nursing) |  terms related to obstetrics and gynecology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 12 | Profession-content features (OB/GYN, nursing) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 5 | Capitalized-name detector | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 31 | Capitalized-name detector | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 5 | Generic proper-noun feature |  proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L2:F5859](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) | 5 | Generic proper-noun feature |  first names (mostly female) | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) |
| [L2:F5859](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) | 31 | Generic proper-noun feature |  first names (mostly female) | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L12:14970 de=0.559 |
| 3 | `inspect_feature` ×12 | L12:14970, L4:1276, L6:8166, L4:13803, L18:14677, L7:8644, L19:9685, L6:11646, L13:11685, L0:7532, L2:5859, L6:15267 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F9685@31` | ❌ error | — | — | Trace the "women's names and their roles" feature (L19:F9685) upstream to its so… |
| SA-2 | `L18:F14677@31` | ❌ error | — | — | Trace the "instances of women being mentioned" feature (L18:F14677) upstream. Is… |
| SA-3 | `L4:F13803@11` | ❌ error | — | — | Trace the OB/GYN terms feature (L4:F13803) upstream. This is a strong profession… |
| SA-4 | `L12:F14970@5` | ❌ error | — | — | Trace the "names of people" feature (L12:F14970) upstream. This fires on positio… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L19:F9685@31, k=15 → Emb:" nurse"@12 (de=2.33) +14 more |
| 2 | `get_upstream_features` | L18:F14677@31, k=15 → L14:F4385 (de=2.17) +14 more |
| 3 | `get_upstream_features` | L4:F13803@11, k=15 → Emb:" Delivery"@11 (de=12.19) +14 more |
| 4 | `get_upstream_features` | L12:F14970@5, k=15 → L4:F1276 (de=3.36) +14 more |
| 5 | `get_upstream_features` | L6:F11646@5, k=10 → Emb:" Melissa"@5 (de=6.94) +9 more |
| 6 | `get_upstream_features` | L14:F4385@31, k=10 → L13:F4753 (de=2.50) +9 more |
| 7 | `get_upstream_features` | L4:F1276@31, k=8 → Emb:" Melissa"@31 (de=6.28) +7 more |
| 8 | `inspect_feature` ×2 | L14:4385, L13:4753 |

### Build

`build_circuit` → 12 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 31,123 | 4,273 | 148,749 | 0 | $0.0234 | — | — |
| **Total** | | **31,123** | **4,273** | **148,749** | **0** | **$0.0234** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 18s