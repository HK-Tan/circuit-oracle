# Circuit Oracle Report
**Date:** 2026-07-28 07:25:06 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe’s toxicity score is driven primarily by explicit race/identity language and racism/bigot semantics in the prompt, with additional non-semantic lexical/style correlations; it is not exclusively an identity-group trigger.

**Confidence:** 8/10

**Reasoning:** The saved circuit has two important semantic routes plus a substantial set of direct lexical probe alignments.

1. **Race/identity lexical route — strongest evidence of the user’s concern.**  
   The embeddings for **“black” (pos 32)**, **“race” (pos 40)**, and, more weakly, **“white” (pos 15)** feed the `Race/ethnicity lexical detector`: L2:13158 at positions 32 and 40. This feature is highly selective (`frac_nonzero=0.00986`) and is genuinely a race/ethnicity detector: its activating examples include *“black”* and *“race”*, and its promoted tokens include *ethnic, Hispanic, Latino, Muslim,* and *Jewish*. Its direct positive effects on the probe score are large: **+0.3184** at “black” and **+0.2285** at “race.”

   The direct upstream attribution confirms this is mostly token-local identity/race recognition: “black” contributes **+10.5** into L2:13158 at pos 32, and “race” contributes **+13.625** into the same feature at pos 40. “White” also contributes positively to both copies (+1.1875 and +2.3125). An L1 social-context feature, L1:13646, also feeds this route. It is labeled social-justice text (`frac_nonzero=0.01158`), promotes *race* and *LGBTQ*, and its top examples discuss racial hysteria, race relations, privilege, and social identity categories.

   This is clear evidence that the probe relies partly on an **identity/race-topic correlate**, rather than requiring toxic intent. Neutral discussion of racial demographics or race relations could activate the same route.

2. **Racism/bigot-content route — evidence that the probe also responds to the actual harmful proposition.**  
   The prompt’s **“bigot”** token is split such that its `ot` token at pos 9 directly feeds L4:117 by **+3.5156**. L4:117 has a strong positive direct effect on the probe (**+0.2188**) and is a selective racism/racial-language detector (`frac_nonzero=0.01199`). Its promoted tokens are unusually coherent: *racially, racial, Racism, racist,* and *racism*. Its high-activation examples include “black racists,” “race relations,” and racial/social-justice language.

   That feature is also supported by L3:15009 at pos 9 (**+1.3125** upstream effect). Although its broad autointerp label is noisy, its promoted vocabulary—*prejudice, bias,* and *belief*—supports interpreting this particular contribution as a **prejudice/bias semantic context**. Therefore, the circuit does not merely detect that protected groups are named: it also responds to the explicit claim that people are “bigots” and to racialized prejudice language.

3. **Style and generic-token artifacts — evidence that the linear probe has spurious alignment beyond content.**  
   A separate path starts from **“clearly” (pos 2)**. It strongly excites L5:8030 (**+18.25** upstream), which contributes **+0.2109** to the probe. L5:8030 is a selective (`frac_nonzero=0.01007`) clarity/definition/difference feature, with examples around *clearly, defined, distinct,* and *clear-cut difference*. That is argumentative style, not toxicity.

   Several features affect the probe directly from layer 0:
   - L0:3255 at **“and” (pos 10)**: **+0.2314** to the score; it is simply an “and” detector (`frac_nonzero=0.02981`), directly sourced by the “and” embedding (**+36.75**).
   - L0:7969 at **“other” (pos 14)**: **+0.2090**; a selective “other” detector (`frac_nonzero=0.01373`), sourced by “other” (**+42.25**).
   - L0:6154 at “clearly”: **+0.2393**, an argument/writing-use-of-*clearly* feature (`frac_nonzero=0.02214`).
   - Conversely, L0:5707 and L1:2407, both *clearly*/perspective-related, are among the strongest **negative** score contributions (−0.3457 and −0.2412). This mixed-sign pattern illustrates that the probe direction is not a clean toxicity concept; it has idiosyncratic lexical/style weights.

Overall, the main positive semantic evidence is a combination of **race-topic detection** (`social_l1 → racial_l2 → probe`) and **explicit racism/prejudice language** (`emb_bigot → prejudice_l3/racism_l4 → probe`). The former supports the concern about spurious identity-group/topic dependence; the latter means the high score is also substantively supported by the prompt’s overtly racialized and derogatory claims. The direct “and,” “other,” and “clearly” effects show additional, clearly non-causal textual shortcuts in the probe.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L1:F13646](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) | 32 | Social-justice / identity-context detector |  text discussing social justice issues | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) |
| [L1:F13646](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) | 40 | Social-justice / identity-context detector |  text discussing social justice issues | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 32 | Race/ethnicity lexical detector |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 40 | Race/ethnicity lexical detector |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L3:F15009](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15009) | 9 | Bias/prejudice-context detector | words or phrases related to courts, legalese, and mental states | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15009) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 9 | Racism/racial-language detector |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L5:F8030](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/8030) | 3 | Argumentative clarity/style feature |  language discussing differences, clarity, and definition | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/8030) |
| [L0:F3255](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) | 10 | Direct generic lexical features |  the word "and" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) |
| [L0:F7969](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7969) | 14 | Direct generic lexical features |  the word "other" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7969) |
| [L0:F6154](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6154) | 2 | Direct generic lexical features |  uses of 'clearly' and nearby words that are related to arguments and writing | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6154) |
| [L0:F5707](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5707) | 2 | Direct generic lexical features |  words or phrases related to knowledge or perspective | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5707) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 12 features; top: L0:5707 de=-0.346 |
| 3 | `inspect_feature` ×6 | L2:13158, L4:117, L5:8030, L0:3255, L0:7969, L0:6154 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F13158@32` | ❌ error | — | — | Trace what drives this repeated positive probe feature at pos32, identify the ex… |
| SA-2 | `L4:F117@9` | ❌ error | — | — | Trace this positive probe-driving feature to embeddings; determine lexical/seman… |
| SA-3 | `L5:F8030@3` | ❌ error | — | — | Trace this positive probe-driving feature to embeddings; determine whether it ca… |
| SA-4 | `L0:F3255@10` | ❌ error | — | — | At this early direct-to-probe feature, inspect semantics and trace to exact toke… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L2:F13158@32, k=15 → Emb:" black"@32 (de=10.50) +14 more |
| 2 | `get_upstream_features` | L2:F13158@40, k=15 → Emb:" race"@40 (de=13.62) +14 more |
| 3 | `get_upstream_features` | L4:F117@9, k=15 → Emb:"ot"@9 (de=3.52) +14 more |
| 4 | `get_upstream_features` | L5:F8030@3, k=15 → Emb:" clearly"@2 (de=18.25) +14 more |
| 5 | `get_upstream_features` | L0:F3255@10, k=10 → Emb:" and"@10 (de=36.75) +9 more |
| 6 | `get_upstream_features` | L0:F7969@14, k=10 → Emb:" other"@14 (de=42.25) +9 more |
| 7 | `inspect_feature` ×8 | L0:5707, L1:2407, L3:15009, L3:12367, L1:13646, L1:3020, L0:16013, L0:14500 |

### Build

`build_circuit` → 14 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 26,687 | 3,067 | 78,317 | 0 | $0.1323 | — | — |
| **Total** | | **26,687** | **3,067** | **78,317** | **0** | **$0.1323** | | |

**Oracle wall-clock time:** 0m 40s