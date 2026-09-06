# Circuit Oracle Report
**Date:** 2026-07-28 08:38:44 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by a combination of genuine profession-related indicators (nutrition/dietetics) and spurious gender markers (female pronouns), with the latter providing a significant contribution to the final score.

**Confidence:** 9

**Reasoning:** 
The circuit reveals two distinct parallel pathways driving the probe's score:
1. **Profession-Specific Pathway:** The token embedding for `" nutrition"` (pos 7) directly and indirectly (via L1:F6461, L1:F6631, L2:F2589) excites **L4:F13412** ("terms related to diets and dietary health"). This feature, which encodes professional domain knowledge, feeds into the probe logit.
2. **Spurious Gender Pathway:** A strong chain of gender markers originates from the token embeddings of `"She"` (pos 15) and `"Her"` (pos 1). These excite a cascade of features specializing in female mentions: **L6:F11646** $\rightarrow$ **L18:F14677** $\rightarrow$ **L19:F9685**. Specifically, L19:F9685 ("references to women's names and their roles or accomplishments") and L18:F14677 ("instances of women or girls being mentioned") have high direct effects on the probe.

The subagent tracing confirms that while professional terms like "nutrition" do contribute, the gender signal is amplified through multiple layers (0 $\rightarrow$ 6 $\rightarrow$ 15 $\rightarrow$ 17 $\rightarrow$ 18 $\rightarrow$ 19), indicating that the probe is heavily relying on the subject's gender (female) as a heuristic for the classification, corroborating the user's concern about spurious features.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 7 | Dietary Health & Nutrition Features |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 15 | Gender Marker (Female) Features |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 15 | Gender Marker (Female) Features |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 15 | Gender Marker (Female) Features |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11646 de=0.283 |
| 3 | `inspect_feature` ×5 | L6:11646, L18:14677, L12:14970, L19:9685, L4:13412 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F9685@15` | ✅ reported | 3 | 6 | Trace the path from L19:F9685 to see if it is driven by gender markers (she/her)… |
| SA-2 | `L18:F14677@15` | ✅ reported | 5 | 7 | Trace the path from L18:F14677 to see what triggers this gender-related feature. |
| SA-3 | `L4:F13412@7` | ✅ reported | 5 | 13 | Trace the path from L4:F13412 to identify which input tokens (e.g., 'nutrition',… |

<details>
<summary><b>SA-1</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F9685 | " references to women's names and their roles or accomplishments." |
| 2 | `get_upstream_features` | L19:F9685@15, k=10 | Emb:" She"@15 (de=6.12) +9 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `get_upstream_features` | L6:F11646@15, k=10 | Emb:" She"@15 (de=18.50) +9 more |
| 5 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 6 | `inspect_feature` | L18, F9023 | " personal names and associated titles" |
| 7 | `inspect_feature` | L14, F13478 | " occurrences of people's names, often with titles" |
| 8 | `get_upstream_features` | L17:F5889@15, k=10 | Emb:" She"@15 (de=20.25) +9 more |

**Findings:** Tracing from L19:F9685 (position 15) reveals that its strongest upstream drivers are gender markers. The token embedding "She" contributes a direct effect of 6.125, and "Her" adds 3.5312. A low‑layer (L6) feature (F11646) that specializes in feminine pronouns receives an even larger direct effect (18.5) from the same "She" token, confirming a gender‑driven pathway. A professional term, "nutrition"…

</details>

<details>
<summary><b>SA-2</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@15, k=10 | Emb:" She"@15 (de=15.25) +9 more |
| 3 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 4 | `get_upstream_features` | L6:F11646@15, k=10 | Emb:" She"@15 (de=18.50) +9 more |
| 5 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 6 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 7 | `get_upstream_features` | L6:F11646@15, k=10 | Emb:" She"@15 (de=18.50) +9 more |
| 8 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 9 | `get_upstream_features` | L17:F5889@15, k=10 | Emb:" She"@15 (de=20.25) +9 more |
| 10 | `get_upstream_features` | L0:F15382@15, k=10 | Emb:" She"@15 (de=23.62) +9 more |
| 11 | `inspect_feature` | L13, F6622 | " pronouns." |

**Findings:** The gender‑related feature L18:F14677 is primarily driven by direct token embeddings of the pronoun "She" (pos 15) and the name‑title token "Her" (pos 1). Upstream it receives strong excitatory contributions from a cascade of pronoun‑and‑female‑mention detectors spanning layers 0, 6, 15, 17, culminating in the target feature. The lowest‑layer contributor is L0:F15382 (layer 0), a very sparse detec…

</details>

<details>
<summary><b>SA-3</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 2 | `get_upstream_features` | L4:F13412@7, k=10 | Emb:" nutrition"@7 (de=12.62) +9 more |
| 3 | `inspect_feature` | L1, F6461 | " technical language around physical activity, muscle function, and rel" |
| 4 | `get_upstream_features` | L1:F6461@7, k=10 | Emb:" sports"@6 (de=9.19) +9 more |
| 5 | `inspect_feature` | L1, F6631 | " words related to dietary patterns and scientific studies" |
| 6 | `get_upstream_features` | L1:F6631@7, k=10 | Emb:" nutrition"@7 (de=5.12) +9 more |
| 7 | `inspect_feature` | L2, F2589 | " words related to medical professionals and medical specialties" |
| 8 | `inspect_feature` | L1, F15310 | " words related to physical exercise" |
| 9 | `inspect_feature` | L0, F9747 | " code snippets dealing with user interfaces and visualizers" |
| 10 | `get_upstream_features` | L2:F2589@7, k=10 | Emb:" nutrition"@7 (de=4.50) +9 more |
| 11 | `inspect_feature` | L1, F15310 | " words related to physical exercise" |
| 12 | `get_upstream_features` | L1:F15310@7, k=10 | Emb:" nutrition"@7 (de=8.56) +9 more |

**Findings:** The target dietary‑health feature L4:F13412 is primarily driven by the input token ' nutrition' (direct_effect ≈ 12.6). Additional upstream pathways pass through early‑layer (≤8) features that encode exercise, dietary‑pattern, medical‑professional, and general physical‑exercise language, each also receiving positive influence from the same token embeddings. This demonstrates that the model maps th…

</details>

### Build

`build_circuit` → 5 nodes, 4 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 88,420 | 1,110 | 0 | 0 | $0.0128 | — | — |
| SA-1 | openai/gpt-oss-120b | 81,604 | 5,921 | 17,696 | 0 | $0.0161 | ✅ 3F/6E | Trace the path from L19:F9685 to see if it is driven by gend… |
| SA-2 | openai/gpt-oss-120b | 110,084 | 7,629 | 22,752 | 0 | $0.0214 | ✅ 5F/7E | Trace the path from L18:F14677 to see what triggers this gen… |
| SA-3 | openai/gpt-oss-120b | 155,404 | 11,710 | 22,784 | 0 | $0.0307 | ✅ 5F/13E | Trace the path from L4:F13412 to identify which input tokens… |
| **Total** | | **435,512** | **26,370** | **63,232** | **0** | **$0.0810** | | |

**Oracle wall-clock time:** 8m 2s