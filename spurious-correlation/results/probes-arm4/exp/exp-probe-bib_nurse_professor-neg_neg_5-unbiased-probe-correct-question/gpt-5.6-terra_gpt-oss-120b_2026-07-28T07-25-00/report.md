# Circuit Oracle Report
**Date:** 2026-07-28 07:25:00 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe score is driven primarily by a genuine academic-profession/biography circuit—research, Ph.D., degrees, and universities—with a smaller direct male-pronoun contribution that is plausibly spurious but not the dominant mechanism.

**Confidence:** 8/10

**Reasoning:** The saved circuit shows two main evidence streams feeding the **Output: probe classification score**.

1. **Research-profession evidence.** The embedding for **“research”** (pos 2) drives the early **Academic-research cue** feature **L1:F10986** (pos 3). Its autointerp label is “words related to academic research” (frac_nonzero **0.03796**), with activating examples involving *research interests*, *investigator*, and *research agenda*. This feature directly contributes positively to the probe score (+0.0649). This is genuine profession-relevant evidence: the text explicitly says the subject’s research interests are in transnational business history.

2. **Credential/academic-biography evidence.** The embeddings for **“Ph”** (pos 13) and **“D”** (pos 15) strongly drive **L2:F10852** at pos 15: the direct upstream attribution from the two pieces is +14.0 and +9.625, respectively. F10852 is a selective academic-title/degree feature (frac_nonzero **0.00801**) whose promoted tokens include **“degree,” “degrees,” “PhD,”** and **“doctorate.”** It feeds **L7:F14129**, a highly selective academic-degree/university-person feature (frac_nonzero **0.00417**), which then helps form later university/education features.

   The late aggregation includes **L17:F11003** (frac_nonzero **0.00986**), a clean **university** feature whose promoted tokens are *University*, *university*, and *universities*, and **L17:F7973** (frac_nonzero **0.01542**), which detects descriptions of someone’s education and schools attended. The token **“from”** at pos 19 contributes directly to the university feature (+6.375): this should not be interpreted as meaningful in isolation, but as part of the recurring credential template “Ph.D. in History **from** Harvard University.” These paths then support the late academic-credential representation—e.g. **L20:F14235**, “references to academic credentials and institutions” (frac_nonzero **0.02278**, promoted tokens include *University*, *Cornell*, *UCLA*, *Duke*)—although this particular late feature has a *negative* direct effect on the probe score (−0.0564 at pos 19 and −0.0510 at pos 33). Thus the probe is sensitive to the credential profile, but its learned direction is not simply “more academic credentials = more positive score”; some credential signals oppose the selected class.

3. **Spurious gender evidence exists, but is not central.** **L0:F1069** at pos 1 is explicitly a male-pronoun feature, “references to a male person, particularly when using ‘He’ or ‘His’” (frac_nonzero **0.0078**). It has a positive direct effect on the probe (+0.0554). This is clear evidence that the linear probe uses gender-correlated information, so the concern is valid: replacing “His/He” with female or neutral pronouns could alter the score independently of the occupation. However, its effect is comparable to a single research/credential feature and is outweighed by the broad, repeated degree/university circuit. Also, some gender-linked routes are inhibitory: the credential feature L20:F14235 receives negative input from **“his”** (pos 12, −1.6484), so gender is not consistently aligned with the probe’s decision.

4. **A secondary subject-domain feature is negative rather than evidence for the class.** **L8:F2383** fires at the word **“history”** (pos 8), with a direct effect −0.0898—the largest individual signed effect among listed features. It is labeled archaeological-sites/digs/artifacts (frac_nonzero **0.02466**) and is directly driven by “history” (+5.5938), “transnational” (+3.2656), and “research” (+1.2188). This is not an entity-specific recognition of the subject; it appears to be a broad historical/archaeological semantic association. Its negative sign indicates that the probe distinguishes the target profession partly from adjacent humanities/history semantics, rather than relying on this as positive profession evidence.

Overall, the classification circuit is **mostly a generic academic-CV template detector**, not an entity-specific profession recognizer: academic-research language plus Ph.D./degree/university credentials form the strongest coherent pathways. The model does use a male marker directly, demonstrating some spurious dependence, but the traced evidence does **not** support the claim that gender is the principal driver on this input.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L1:F10986](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) | 3 | Academic-research cue |  words related to academic research | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 15 | Ph.D./academic-degree detector |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 15 | Academic biography / credentials |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L17:F11003](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) | 19 | University/education aggregation | university | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) |
| [L17:F7973](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7973) | 19 | University/education aggregation |  phrases describing someone's education and the schools they attended | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7973) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Male-pronoun feature |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L8:2383 de=-0.090 |
| 3 | `inspect_feature` ×5 | L20:14235, L14:3956, L8:2383, L7:14129, L1:10986 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L20:F14235@19` | ❌ error | — | — | Trace this high-activation late feature upstream to embeddings. Determine whethe… |
| SA-2 | `L20:F14235@33` | ❌ error | — | — | Trace this repeated late credential-related feature upstream to embeddings. Iden… |
| SA-3 | `L8:F2383@8` | ❌ error | — | — | Trace this strongest negative mid-layer feature to embeddings; identify whether … |
| SA-4 | `L7:F14129@15` | ❌ error | — | — | Trace this positive feature to embeddings and classify the signal: gender marker… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L20:F14235@19, k=20 → L17:F11003 (de=34.00) +19 more |
| 2 | `get_upstream_features` | L20:F14235@33, k=20 → L17:F11003 (de=23.62) +19 more |
| 3 | `get_upstream_features` | L8:F2383@8, k=20 → Emb:" history"@8 (de=5.59) +19 more |
| 4 | `get_upstream_features` | L7:F14129@15, k=20 → L6:F2254 (de=7.09) +19 more |
| 5 | `get_upstream_features` | L1:F10986@3, k=20 → Emb:" research"@2 (de=6.62) +19 more |
| 6 | `inspect_feature` ×6 | L0:6051, L0:1069, L2:10852, L17:11003, L19:2496, L17:7973 |
| 7 | `get_upstream_features` | L17:F11003@19, k=20 → Emb:"<bos>"@0 (de=-6.72) +19 more |
| 8 | `get_upstream_features` | L19:F2496@19, k=20 → L17:F11003 (de=15.69) +19 more |
| 9 | `get_upstream_features` | L17:F11003@33, k=20 → L15:F4934 (de=7.81) +19 more |
| 10 | `get_upstream_features` | L2:F10852@15, k=20 → Emb:" Ph"@13 (de=14.00) +19 more |

### Build

`build_circuit` → 10 nodes, 9 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 24,443 | 2,807 | 74,786 | 0 | $0.1219 | — | — |
| **Total** | | **24,443** | **2,807** | **74,786** | **0** | **$0.1219** | | |

**Oracle wall-clock time:** 0m 41s