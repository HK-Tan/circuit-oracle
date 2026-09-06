# Circuit Oracle Report
**Date:** 2026-07-28 07:25:09 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity probe is driven chiefly by the explicit hostile lexical construction “Self-hating,” which is amplified by a learned association between hyphenated self-descriptions, hate/antagonism, and political/identity-rhetoric—not by a clean, isolated detector of the identity term “Jew.”

**Confidence:** 7/10

**Reasoning:** The saved circuit shows a primarily lexical/form-based pathway:

- **Emb: Self (pos 1)** and **Emb: - (pos 2)** strongly form the **Hyphenated self- construction** node. The central feature is **L3:F735** at positions 3 and 4, a selective “self- followed by hyphen” feature (`frac_nonzero=0.00632`). Its largest positive upstream inputs are directly from `Self` (direct effects **36.5** at pos 3 and **29.63** at pos 4), with the hyphen contributing positively at pos 4 (**1.27**). This signal continues through **L4:F10004**, another highly selective “hyphenated words beginning with self” feature (`frac_nonzero=0.00397`; promoted tokens include `self`, `Self`, and `himself`).

- This is not merely a formatting feature in this prompt: it is joined to a genuine hostile-affect pathway. **L3:F8492** is an extremely selective literal **“hate”** detector (`frac_nonzero=0.00054`), and **L3:F592** represents love/hate vocabulary (`frac_nonzero=0.0044`; promoted tokens include `love`, `hate`, `HATE`). These feed **L4:F8407**, an antagonist/fighting feature (`frac_nonzero=0.00874`) whose promoted vocabulary includes `attacking`, `hated`, `Enemy`, `villains`, and `hate`. It is the largest positive high-layer feature directly driving the probe score: **+0.1719** at pos 4 and **+0.1030** at pos 3.

- There is also a secondary **political/identity-rhetoric association**: **L4:F5181** detects political parties/ideologies (`frac_nonzero=0.00962`) and promotes `anti`, `Semitism`, `hate`, and `hatred`; **L6:F10545** captures political rhetoric involving race/government (`frac_nonzero=0.03818`) and includes activating examples with “racial hysteria,” “racist,” and “slavery.” This node receives positive signal from the hostile/self-hyphen pathway—e.g. L4:F8407 → L6:F10545 has positive direct effect **+1.62**, and L3:F735 at pos 4 → L6:F10545 is **+0.68**—and then positively drives the probe (**L6:F10545: +0.0864**).

- Importantly, the traced embedding sources for the major circuit are **`Self`**, the **hyphen**, and the `hat` subtoken at position 3—the latter is a tokenizer fragment of “hating,” not a semantic mention of a hat. The direct upstream result for **L4:F8407** is especially clear: `hat` at pos 3 has direct effect **+10.75**, while L3:F735 at pos 4 connects positively (**+0.69**). Thus the attribution is localized around the word **“Self-hating”**, particularly its tokenization and lexical hate content.

- Some prominent direct probe drivers are plainly spurious or irrelevant. For example, **L0:F2994** is a generic `his/he` pronoun feature yet contributes **+0.1455** at pos 11; **L1:F2107** is a legal/math “enter” feature yet contributes **+0.1631**; and several low-layer features correspond to punctuation/code-style motifs. These are probe-direction correlations, not evidence that the model semantically judged pronouns, code, or legal language as toxic. Their presence supports the concern that this linear probe has entangled nuisance directions.

Overall, the positive score is substantively supported by the literal derogatory/hostile phrasing—especially **“hating”**—and its association with adversarial political rhetoric. However, the circuit also contains a nontrivial shortcut: the probe treats the **“self-” hyphenated construction** and politically/identity-associated language as toxic-adjacent signals. I did **not** find a clean causal path specifically originating in the token `Jew`; therefore this graph does not establish that “Jew” alone is the decisive driver. It does show that the probe is not purely semantic: it mixes real hate-language evidence with formatting, tokenization, political-rhetoric, and unrelated low-level correlates.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L3:F735](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) | 3 | Hyphenated self- construction |  words and phrases that include the word "self" followed by a hyphen | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) |
| [L3:F735](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) | 4 | Hyphenated self- construction |  words and phrases that include the word "self" followed by a hyphen | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) |
| [L4:F10004](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10004) | 4 | Hyphenated self- construction |  hyphenated words beginning with "self" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10004) |
| [L3:F592](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) | 4 | Hate / hostile-affect lexical detector | words related to love, affection, and hate, including foreign language | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) |
| [L3:F8492](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8492) | 4 | Hate / hostile-affect lexical detector | the word "hate" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8492) |
| [L4:F8407](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) | 4 | Hate / hostile-affect lexical detector |  words related to antagonists and fighting | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) |
| [L4:F5181](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5181) | 4 | Political-ideology / contentious-rhetoric association |  terms relating to political parties or ideologies | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5181) |
| [L6:F10545](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10545) | 4 | Political-ideology / contentious-rhetoric association |  political rhetoric related to race, historical states, and government control | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10545) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:8407 de=0.172 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F8407@4` | ❌ error | — | — | Trace this strongest late-ish positive driver of the toxicity probe upstream to … |
| SA-2 | `L1:F2107@3` | ❌ error | — | — | Trace this strong positive early probe driver upstream to token embeddings. Iden… |
| SA-3 | `L0:F2994@11` | ❌ error | — | — | Trace/inspect this direct positive layer-0 driver, particularly its input token … |
| SA-4 | `L3:F735@3` | ❌ error | — | — | Trace this recurrent strong positive feature upstream to embeddings. Determine s… |
| SA-5 | `L0:F8938@2` | ❌ error | — | — | Inspect this strong positive direct layer-0 feature; identify which exact token … |
| SA-6 | `L0:F3090@7` | ❌ error | — | — | Inspect this positive direct layer-0 feature and identify its exact lexical/sema… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×8 | L4:8407, L1:2107, L0:2994, L3:735, L0:8938, L0:3090, L0:4336, L6:10545 |
| 2 | `get_upstream_features` | L4:F8407@4, k=20 → Emb:"hat"@3 (de=10.75) +19 more |
| 3 | `get_upstream_features` | L3:F735@3, k=20 → Emb:"Self"@1 (de=36.50) +19 more |
| 4 | `get_upstream_features` | L3:F735@4, k=20 → Emb:"Self"@1 (de=29.62) +19 more |
| 5 | `get_upstream_features` | L6:F10545@4, k=20 → L4:F8407 (de=1.62) +19 more |
| 6 | `get_upstream_features` | L1:F2107@3, k=20 → Emb:"hat"@3 (de=15.31) +19 more |
| 7 | `inspect_feature` ×8 | L3:592, L3:8492, L1:5138, L0:1094, L0:6660, L0:10484, L4:5181, L4:10004 |

### Build

`build_circuit` → 7 nodes, 10 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 35,229 | 2,743 | 88,264 | 0 | $0.1513 | — | — |
| **Total** | | **35,229** | **2,743** | **88,264** | **0** | **$0.1513** | | |

**Oracle wall-clock time:** 0m 46s