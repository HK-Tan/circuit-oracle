# Circuit Oracle Report
**Date:** 2026-07-28 08:33:56 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by a combination of genuine academic indicators (degree mentions and research terminology) and a spurious gender marker (male pronouns).

**Confidence:** 9

**Reasoning:** 
The attribution circuit reveals that the probe's score is produced by three primary parallel pathways originating from the input embeddings:

1.  **Academic Degree Pathway:** A highly specific "Academic Degree Cascade" (L2:F10852 $\rightarrow$ L5:F13801 $\rightarrow$ L6:F2254 $\rightarrow$ L7:F14129) is triggered by the token embedding for **"PhD"** (pos 27). This pathway captures explicit evidence of professional qualification.
2.  **Academic Lexicon Pathway:** An "Academic Research Lexicon" feature (L1:F10986) is driven by token embeddings for **" research"** (pos 2) and **" interests"** (pos 3). This captures the general scholarly context of the research description.
3.  **Spurious Gender Pathway:** A "Male Pronoun Detector" (L0:F1069) is strongly activated by the token embedding for **"His"** (pos 1). This feature contributes positively to the probe score, confirming the user's concern that the probe relies on spurious gender markers (specifically male pronouns) as a heuristic for predicting the profession.

The signal flows from these early-layer lexical and gender detectors directly or indirectly toward the probe's output direction at layer 26. While the genuine indicators (PhD, research) are present and strong, the inclusion of the male pronoun feature (L0:F1069) in the causal circuit demonstrates that gender is being used as a predictive feature for this profession.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: His (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: research (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: interests (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 27 | Emb: PhD (pos 27) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Male Pronoun Detector |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L1:F10986](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) | 2 | Academic Research Lexicon |  words related to academic research | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 27 | Academic Degree Cascade | academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L5:F13801](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) | 27 | Academic Degree Cascade | abbreviations for degrees and mentions of educational attainment | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 27 | Academic Degree Cascade | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 27 | Academic Degree Cascade |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:1069 de=0.070 |
| 3 | `inspect_feature` ×5 | L0:1069, L1:10986, L5:12330, L7:14129, L4:9757 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F1069@1` | ✅ reported | 4 | 2 | Trace the path from L0:F1069 (Male pronoun feature) and L1:F10986 (Academic rese… |
| SA-2 | `L1:F10986@3` | ✅ reported | 6 | 11 | Trace the path from L1:F10986 (Academic research feature) to see where the signa… |
| SA-3 | `L7:F14129@27` | ✅ reported | 4 | 5 | Trace the path from L7:F14129 (Academic degrees/universities) to see where the s… |

<details>
<summary><b>SA-1</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 2 | `get_upstream_features` | L0:F1069@1, k=15 | Emb:"His"@1 (de=21.62) +14 more |
| 3 | `inspect_feature` | L1, F10986 | " words related to academic research" |
| 4 | `get_upstream_features` | L1:F10986@1, k=15 | ❌ Feature (layer=1, feature_idx=10986) not found at pos=1. Thi |
| 5 | `get_upstream_features` | L1:F10986@2, k=15 | Emb:" research"@2 (de=5.16) +14 more |
| 6 | `inspect_feature` | L0, F11532 | "titles and roles of people in organizations" |
| 7 | `inspect_feature` | L0, F8489 | " words related to reports, experiments, systems and research" |
| 8 | `get_upstream_features` | L0:F11532@2, k=10 | Emb:" research"@2 (de=3.33) +9 more |
| 9 | `inspect_feature` | L0, F10221 | " references to family and personal relationships" |
| 10 | `get_upstream_features` | L0:F8489@2, k=10 | Emb:"<bos>"@0 (de=6.88) +9 more |
| 11 | `get_upstream_features` | L0:F11532@2, k=10 | Emb:" research"@2 (de=3.33) +9 more |

**Findings:** The male‑pronoun feature (L0:F1069) is directly driven by the input token embedding "His" (positive direct effect 21.6) and the BOS embedding, both at layer 0, satisfying the lower‑third requirement. The academic‑research feature (L1:F10986) receives its strongest positive influence from the input token embedding " research" (direct effect 5.16) and from two low‑level lexical features: 11532 (titl…

</details>

<details>
<summary><b>SA-2</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F10986 | " words related to academic research" |
| 2 | `get_upstream_features` | L1:F10986@3, k=10 | Emb:" research"@2 (de=6.62) +9 more |
| 3 | `inspect_feature` | L0, F6113 | " the word "overall", sometimes alongside words that express quantity" |
| 4 | `inspect_feature` | L0, F13431 | "the word "owing"." |
| 5 | `get_upstream_features` | L0:F6113@3, k=10 | Emb:" interests"@3 (de=14.19) +9 more |
| 6 | `inspect_feature` | L0, F15256 | " the word "positive"" |

**Findings:** The academic‑research detector (L1:F10986) receives its strongest excitatory drive directly from the input token embeddings " research" (pos 2) and " interests" (pos 3). These embeddings encode the actual lexical items that define the scholarly context. A secondary pathway flows through a low‑layer (L0) word‑overall detector (F6113), which itself is strongly driven by the same " interests" embeddi…

</details>

<details>
<summary><b>SA-3</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14129 | " academic degrees, universities, and people associated with them" |
| 2 | `get_upstream_features` | L7:F14129@27, k=10 | Emb:" PhD"@27 (de=19.25) +9 more |
| 3 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 4 | `get_upstream_features` | L6:F2254@27, k=10 | Emb:" PhD"@27 (de=22.00) +9 more |
| 5 | `inspect_feature` | L5, F13801 | "abbreviations for degrees and mentions of educational attainment" |
| 6 | `inspect_feature` | L5, F11028 | " terms and phrases related to academic study and institutions" |
| 7 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |

**Findings:** The activation of L7:F14129 is ultimately driven by the raw input token embedding for the string 'PhD' at position 27. The embedding exerts a strong positive direct effect (≈19) on the target feature and also feeds lower‑layer degree detectors (L6:F2254, L5:F13801, L2:F10852). These intermediate features further amplify the signal, forming a concise upward‑flow circuit from the token embedding thr…

</details>

### Build

`build_circuit` → 8 nodes, 7 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 88,577 | 1,294 | 0 | 0 | $0.0129 | — | — |
| SA-3 | openai/gpt-oss-120b | 52,226 | 4,781 | 15,264 | 0 | $0.0109 | ✅ 4F/5E | Trace the path from L7:F14129 (Academic degrees/universities… |
| SA-1 | openai/gpt-oss-120b | 103,425 | 7,456 | 22,912 | 0 | $0.0203 | ✅ 4F/2E | Trace the path from L0:F1069 (Male pronoun feature) and L1:F… |
| SA-2 | openai/gpt-oss-120b | 38,741 | 4,078 | 15,200 | 0 | $0.0085 | ✅ 6F/11E | Trace the path from L1:F10986 (Academic research feature) to… |
| **Total** | | **282,969** | **17,609** | **53,376** | **0** | **$0.0527** | | |

**Oracle wall-clock time:** 3m 20s