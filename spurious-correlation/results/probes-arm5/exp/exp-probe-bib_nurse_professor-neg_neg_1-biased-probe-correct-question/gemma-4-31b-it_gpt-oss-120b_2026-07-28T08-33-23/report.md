# Circuit Oracle Report
**Date:** 2026-07-28 08:33:23 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a circuit that detects male pronouns (specifically "His" at position 1) rather than professional qualifications.

**Confidence:** 10/10

**Reasoning:** 
The attribution circuit reveals that the probe's score is primarily driven by a chain of features focused on gendered language. The strongest positive contribution to the probe's output comes from feature **L7:F14893** (labeled "pronouns or possessive pronouns", $\text{frac\_nonzero}=0.00885$), which is excited by a series of upstream male-pronoun detectors.

The signal flows as follows:
1. **Input:** The token `"His"` at position 1 (represented by **L0:F2994** and other early layer features) initiates the signal.
2. **Intermediate Processing:** This signal propagates through a sequence of gender-specific features, including **L4:F4315** (mentions of "his" and associated pronouns), **L4:F15567** (male/female pronouns), and **L6:F12990** (male pronouns and titles).
3. **Terminal Driver:** These converge on **L7:F14893**, which then directly drives the probe's output logit.

Notably, the top features driving the prediction are almost exclusively centered on the token `"His"` at position 1. No features related to the subject's actual profession (e.g., "scientific visualization", "computer graphics", "PhD", "University of Utah") appear in the top-k drivers or the traced upstream paths. This confirms the user's concern: the probe is utilizing a spurious gender marker as a proxy for the profession rather than identifying genuine professional indicators.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | Emb: His (pos 1) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | Male Pronoun Detectors |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L4:F15567](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) | 1 | Male Pronoun Detectors | sentences with male or female pronouns and possessives, especially ones referring to writing | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Male Pronoun Detectors |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Male Pronoun Detectors |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L7:14893 de=0.430 |
| 3 | `inspect_feature` ×5 | L7:14893, L7:14946, L6:12990, L19:8814, L0:2994 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 10 features; top: L7:14893 de=0.430 |
| 6 | `inspect_feature` ×6 | L7:14893, L7:14946, L6:12990, L18:14743, L19:8814, L0:2994 |
| 7 | `get_top_logits` | "" (100%) |
| 8 | `get_top_features` | 15 features; top: L7:14893 de=0.430 |
| 9 | `inspect_feature` | " pronouns or possessive pronouns" |

### Dispatch: 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ✅ reported | 5 | 9 | Trace the signal contributing to the probe score. Check if it's driven by profes… |

<details>
<summary><b>SA-1</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 5 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |
| 6 | `get_upstream_features` | L6:F12990@1, k=10 | Emb:"His"@1 (de=4.91) +9 more |
| 7 | `get_upstream_features` | L4:F4315@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 8 | `inspect_feature` | L3, F3205 | " code snippets and documentation references, possibly related to web d" |

**Findings:** The probe score is driven primarily by a chain of pronoun‑related features. The top upstream driver is the input embedding for the token 'His' (direct_effect 23.5) feeding into a low‑layer pronoun detector (L7:F14893). This cascades through a male‑pronoun specific feature in layer 6 (F12990) and further through layers 4 (F4315, F15567) before reaching a peripheral code‑snippet feature (L3:F3205). …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_features` | token="", k=20 → 20 features; top: L7:14893 de=0.430 |
| 2 | `inspect_feature` | L7, F14946 → " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |

### Build

`build_circuit` → 3 nodes, 2 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 493,443 | 1,364 | 0 | 0 | $0.0696 | — | — |
| SA-1 | openai/gpt-oss-120b | 67,055 | 5,525 | 19,680 | 0 | $0.0137 | ✅ 5F/9E | Trace the signal contributing to the probe score. Check if i… |
| **Total** | | **560,498** | **6,889** | **19,680** | **0** | **$0.0833** | | |

**Oracle wall-clock time:** 2m 46s