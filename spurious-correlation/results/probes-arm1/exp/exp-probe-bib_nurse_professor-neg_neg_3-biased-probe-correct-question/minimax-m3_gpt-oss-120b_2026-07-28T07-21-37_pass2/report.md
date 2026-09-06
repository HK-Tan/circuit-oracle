# Circuit Oracle Report
**Date:** 2026-07-28 07:21:37 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's profession classification is driven primarily by a chain of male-pronoun/gender features — "He/his" tokens feed upward through L0 → L6 → L7 → L12 → L18 pronoun/gender detectors — which collectively form the bulk of the positive signal reaching the probe, with only a much smaller academic-context (University, degree, academic field) pathway.

**Confidence:** 9

**Reasoning:**

The attribution circuit is dominated by **gender/male-pronoun features** rather than profession-specific indicators. The signal flow is:

1. **Token embeddings** → **L0 low-level pronoun features**: The tokens "He" (pos 1, 21) and "his" (pos 3) are the strongest drivers. L0:F2994 (label: "the pronoun 'his' and the pronoun 'he'") fires with direct_effect=0.30 at pos 3 and 0.16 at pos 44, and L0:F1069 (label: "references to a male person, particularly when using the pronoun 'He' or 'His'") fires with direct_effect=0.10 at pos 21. Note the paradoxical promoted/suppressed token pattern: F2994 *suppresses* "his" while F1069 *suppresses* "He" — these are anti-pronoun features whose negative decoder aligns with the probe direction, meaning their **suppression** of the male pronoun tokens pushes toward the probe's class.

2. **L6 / L7 pronoun detectors** reinforce the signal: L6:F12990 (label: "male pronouns and titles along with descriptors associated with men", frac_nonzero=0.07) fires with direct_effect=−0.17 at pos 21, and L7:F14946 (label: "the possessive pronoun 'his'... and some non-ascii characters", frac_nonzero=0.017) fires with direct_effect=−0.17 at pos 2. Their upstream trace (L0:F1069, L1:F12922 "the pronoun 'he' or 'she' in a narrative context", L4:F14796 "the pronoun 'he' or 'him'") confirms they are stacked male-pronoun detectors.

3. **L12 gender-word detector**: L12:F2175 (label: "words referring to gender", fires on "male/female/men/masculine", frac_nonzero=0.006, suppresses "female/woman/herself") has direct_effect=−0.16 at pos 2. Its upstream L7:F14946 (his/he) and L6:F12990 (male pronouns) confirm it sits on top of the male-pronoun stack.

4. **L18 "He" detector**: L18:F14743 (label literally "He", max_activation≈421, fires on the token "He" in narrative, suppresses "she/her") has direct_effect=−0.15 at pos 21 and −0.13 at pos 42.

5. **Academic/legitimate profession pathway is much weaker**: L0:F6270 (label: "the word 'whom'", direct_effect=0.15 at pos 13 "University") and L0:F6127 (label: "degree and academia", direct_effect=−0.11 at pos 8 "degree") feed into L6:F170 (label: "references to academic fields, especially those in the humanities", direct_effect=+0.12 at pos 10 "Mathematics"). This branch represents the only content-relevant signal (academic field, degree), but its total magnitude is small compared to the pronoun chain.

**The user's concern is well-founded**: The probe reads "Computer Science professor" as a profession largely by stacking a tall tower of features that fire on **"He/his"** — the most male-coded tokens in the prompt. The token "He" at the very start of the prompt (pos 1) and the repeated "He received his..." constructions (pos 21, 42) drive a five-layer pronoun/gender circuit whose **suppression-of-female** direction is precisely what the profession probe has learned to look for. A bio about a woman ("She received her...") would activate the same circuit in the opposite direction and likely flip the classification, indicating the probe has partially latched onto gendered writing style as a profession cue. The genuine academic-context features (University, degree, academic fields) contribute only a minor share of the total signal, so the probe is substantially more sensitive to the subject's gender than to the profession-relevant content.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 3 | L0: his/he pronoun (low-level male pronoun detector) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 23 | L0: his/he pronoun (low-level male pronoun detector) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 44 | L0: his/he pronoun (low-level male pronoun detector) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 21 | L0: his/he pronoun (low-level male pronoun detector) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F6270](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) | 13 | L0: University / degree word detectors | the word "whom", sometimes also activating on nearby punctuation, sentence starts, discourse markers, and other function words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) |
| [L0:F6127](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6127) | 8 | L0: University / degree word detectors |  instances of the word "degree" and words associated with academia, especially higher education | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6127) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 21 | L6: male-pronoun & male-title detector | male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | L6: male-pronoun & male-title detector | male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 2 | L6: male-pronoun & male-title detector | male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 42 | L6: male-pronoun & male-title detector | male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 10 | L6: academic fields & humanities detector | references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 2 | L7: his/he pronoun detector (top token himself/his) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | L7: his/he pronoun detector (top token himself/his) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 3 | L7: his/he pronoun detector (top token himself/his) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | L7: his/he pronoun detector (top token himself/his) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 2 | L7: his/he pronoun detector (top token himself/his) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 3 | L7: his/he pronoun detector (top token himself/his) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L12:F2175](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) | 2 | L12: gender-word detector (male/female/men) |  words referring to gender | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 21 | L18: "He" pronoun (very strong, fires on "He" tokens) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 42 | L18: "He" pronoun (very strong, fires on "He" tokens) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2994 de=0.297 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F2994@3` | ❌ error | — | — | Trace this layer-0 feature upstream and inspect its semantics. What does it enco… |
| SA-2 | `L0:F6270@13` | ❌ error | — | — | Trace this layer-0 feature upstream and inspect its semantics. What does it enco… |
| SA-3 | `L6:F12990@21` | ✅ reported | 4 | 5 | Trace this L6 feature upstream. What does it encode? Does it detect gender prono… |
| SA-4 | `L6:F170@10` | ✅ reported | 7 | 7 | Trace this L6 feature upstream. What does it encode? Profession-related? |
| SA-5 | `L7:F14946@2` | ✅ reported | 3 | 6 | Trace this L7 feature upstream. What does it encode? |
| SA-6 | `L7:F14893@1` | ❌ error | — | — | Trace this L7 feature upstream. What does it encode? |
| SA-7 | `L12:F2175@2` | ❌ error | — | — | Trace this L12 feature upstream. What does it encode? |
| SA-8 | `L18:F14743@21` | ❌ error | — | — | Trace this L18 feature upstream. What does it encode? |

<details>
<summary><b>SA-3</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 2 | `get_upstream_features` | L6:F12990@21, k=10 | Emb:" He"@21 (de=4.59) +9 more |
| 3 | `inspect_feature` | L1, F12922 | " the pronoun "he" or "she" in a narrative context" |
| 4 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 5 | `inspect_feature` | L4, F14796 | "the pronoun "he" or "him"" |
| 6 | `get_upstream_features` | L1:F12922@21, k=10 | Emb:" He"@21 (de=23.12) +9 more |

**Findings:** The L6 feature 12990 is a gender‑pronoun detector focused on male references. Its upstream drivers include a direct embedding of the token " He" (the strongest positive influence) and several low‑layer pronoun detection features (layers 0,1,4) that also specialize on masculine pronouns. Consequently, this circuit encodes detection of male pronouns and associated descriptors, confirming it does det…

</details>

<details>
<summary><b>SA-4</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F170 | " references to academic fields, especially those in the humanities" |
| 2 | `get_upstream_features` | L6:F170@10, k=10 | L5:F10392 (de=11.38) +9 more |
| 3 | `inspect_feature` | L5, F10392 | " fields of academic study" |
| 4 | `inspect_feature` | L5, F15490 | " academic subjects and professions" |
| 5 | `get_upstream_features` | L5:F10392@10, k=10 | L3:F4113 (de=3.34) +9 more |
| 6 | `inspect_feature` | L3, F4113 | " mentions of academic degrees and areas of study" |
| 7 | `inspect_feature` | L4, F3727 | " mentions of academic degrees" |
| 8 | `get_upstream_features` | L3:F4113@9, k=10 | Emb:" in"@9 (de=11.94) +9 more |
| 9 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 10 | `get_upstream_features` | L5:F15490@10, k=10 | Emb:" Mathematics"@10 (de=1.83) +9 more |
| 11 | `get_upstream_features` | L2:F10852@6, k=10 | Emb:" B"@4 (de=12.12) +9 more |
| 12 | `inspect_feature` | L1, F10429 | " words related to academic programs" |
| 13 | `get_upstream_features` | L4:F3727@9, k=5 | Emb:" in"@9 (de=11.62) +4 more |

**Findings:** L6:F170 is a higher‑layer detector for references to academic fields, especially humanities. Its strongest upstream driver is L5:F10392 (fields of academic study) with a large positive effect, which itself is driven by L3:F4113 (degree/area mentions) and L4:F3727 (degree mentions). These lower‑layer features fire on tokens such as "degree", "in", and on concrete degree tokens (e.g., "Bachelor", "P…

</details>

<details>
<summary><b>SA-5</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 2 | `get_upstream_features` | L7:F14946@2, k=10 | Emb:"He"@1 (de=7.72) +9 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `get_upstream_features` | L6:F12990@2, k=10 | Emb:" received"@2 (de=3.23) +9 more |
| 5 | `inspect_feature` | L6, F10944 | " text in languages other than English" |

**Findings:** The L7 feature 14946 is a male‑pronoun detector, primarily driven by the earlier token "He" (embedding) and reinforced by a layer‑6 male‑pronoun feature (12990). Upstream traces quickly reach input embeddings (layer 0), satisfying the lower‑third layer requirement. The pathway shows a clear chain from raw token "He" through gender‑specific features to the final pronoun representation, indicating t…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×7 | L0:2994, L0:6270, L0:6127, L0:1069, L12:2175, L18:14743, L7:14893 |
| 2 | `get_upstream_features` | L7:F14893@1, k=10 → Emb:"He"@1 (de=14.75) +9 more |
| 3 | `get_upstream_features` | L18:F14743@21, k=10 → Emb:" He"@21 (de=23.38) +9 more |
| 4 | `get_upstream_features` | L0:F2994@3, k=10 → Emb:" his"@3 (de=42.50) +9 more |
| 5 | `get_upstream_features` | L0:F6270@13, k=10 → Emb:" University"@13 (de=22.88) +9 more |
| 6 | `get_upstream_features` | L12:F2175@2, k=10 → L7:F14946 (de=4.50) +9 more |
| 7 | `get_upstream_features` | L0:F1069@21, k=10 → Emb:" He"@21 (de=37.25) +9 more |

### Build

`build_circuit` → 14 nodes, 22 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 26,984 | 5,545 | 87,157 | 0 | $0.0200 | — | — |
| SA-5 | openai/gpt-oss-120b | 37,265 | 2,984 | 5,056 | 0 | $0.0075 | ✅ 3F/6E | Trace this L7 feature upstream. What does it encode? |
| SA-3 | openai/gpt-oss-120b | 53,044 | 3,783 | 5,088 | 0 | $0.0103 | ✅ 4F/5E | Trace this L6 feature upstream. What does it encode? Does it… |
| SA-4 | openai/gpt-oss-120b | 159,120 | 9,757 | 15,184 | 0 | $0.0299 | ✅ 7F/7E | Trace this L6 feature upstream. What does it encode? Profess… |
| **Total** | | **276,413** | **22,069** | **112,485** | **0** | **$0.0677** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 19s