# Circuit Oracle Report
**Date:** 2026-07-28 07:25:09 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity-probe score is driven primarily by a combination of explicit abuse language and a group-targeted/racial-political framing, with a substantial direct contribution from the identity term *“Indians”*—so the circuit is not identity-only, but it does use identity-group signals as a meaningful predictive shortcut.

**Confidence:** 8/10

**Reasoning:** The synthetic probe target has a positive classification direction; its strongest positive drivers include L0:11375 (+0.221, merely the word “is”) and L0:11668 (+0.183, an apparently unrelated baseball feature), indicating some low-level probe-direction noise. The interpretable evidence is instead in the connected circuit saved above.

* **Identity-group path.** `Emb: Indians (pos 1)` strongly and directly excites:
  * L3:13473 at pos 2, a selective ethnic/racial-group feature (frac_nonzero **0.00569**), with a direct embedding contribution of **+10.25**. Its examples cover “Asian Americans,” “Blacks/African Americans,” and ethnicity/descent terminology. This feature itself contributes **+0.123** to the probe score.
  * L2:1680 at pos 1, a people/group-reference detector (frac_nonzero **0.01067**), directly fed by “Indians” at **+8.56** and contributing **+0.104** to the probe.
  * L2:2123, a nationality/demonym-form feature (frac_nonzero **0.00509**) whose promoted tokens include **Canadian**, **German**, **American**, and which is also driven by “Indians” on the path to the racial-group feature.
  * L0:10155, a broader group-membership feature (frac_nonzero **0.04598**).

  Thus the group-identity supernode is not recognizing a particular real-world entity or making a factual claim about Indians; it is recognizing the textual form of an identity/national group. Importantly, that signal has a **direct positive route to the probe**, via L3:13473 and L2:1680. This supports the concern that the learned linear probe treats group-reference structure as evidence correlated with toxicity.

* **Explicit harmful-content path.** `Emb: abusers (pos 3)` overwhelmingly drives L4:148: its direct embedding-to-feature effect is **+19.125**. L4:148 is a highly selective abuse/sexual-violence lexical detector (frac_nonzero **0.01077**) with promoted tokens **“violence,” “rape,” “abuse,”** and multilingual violence terms. This is strong evidence that the probe is responding to actual lexical content in the input, specifically repeated *“abusers/abusing.”* The same feature also receives a smaller positive contribution from the identity/group feature L0:10155 (+0.652), reflecting that the phrase is syntactically a group accusation.

* **Convergent contextual path.** Both strands converge on L6:10545, which contributes **+0.136** directly to the probe. This feature is labeled political rhetoric involving race, historical states, and government control (frac_nonzero **0.03818**); its activating examples include racialized political rhetoric, immigration-related discussion, “racist,” and “slavery.” It is directly excited by `abusers` (+1.898), `Indians` (+0.332), and the downstream abuse detector L4:148 (+1.391). Consequently, it appears to encode not just abuse as an isolated word, but a pattern of abusive accusation in a race/nationality/political context.

The resulting mechanism is therefore: **group-national identity mention (“Indians”) → identity/demonym detectors**, while **“abusers” → violence/abuse detector**; these signals combine into a racialized-political-rhetoric feature and then raise the toxicity-probe score. The classification is supported by genuine toxic semantics—repeated accusations of abuse and threats of backlash—but the direct group-identity pathway means the probe is partly entangled with a spurious correlate. In a benign statement mentioning Indians, Canadians, or another demonym without derogatory language, this circuit predicts that the identity supernode could still elevate the score.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F10155](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10155) | 1 | Group/national-identity detectors |  words related to membership in a group | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10155) |
| [L2:F2123](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2123) | 1 | Group/national-identity detectors |  words ending in "ian", "jani", "iti", "ino", or "olan" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2123) |
| [L2:F1680](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1680) | 1 | Group/national-identity detectors |  words that refer to people participating in some activity, such as consumers, patients in healthcare, or voters | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1680) |
| [L3:F13473](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13473) | 2 | Group/national-identity detectors |  mentions of racial and ethnic groups, especially in the United States | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13473) |
| [L4:F148](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/148) | 3 | Abuse/sexual-violence lexical detector |  words and phrases related to sexual assault and abuse | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/148) |
| [L6:F10545](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10545) | 3 | Race/political-rhetoric context detector |  political rhetoric related to race, historical states, and government control | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10545) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:11375 de=0.221 |
| 3 | `inspect_feature` ×5 | L0:11375, L0:11668, L6:10545, L3:13473, L2:1680 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F10545@3` | ❌ error | — | — | Trace this positive probe-driving feature to embeddings. Determine whether its s… |
| SA-2 | `L3:F13473@2` | ❌ error | — | — | Trace this positive probe-driving feature to embeddings. Determine whether it re… |
| SA-3 | `L2:F1680@1` | ❌ error | — | — | Trace this positive probe-driving feature through to embedding nodes and identif… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F10545@3, k=15 → Emb:" abusers"@3 (de=1.90) +14 more |
| 2 | `get_upstream_features` | L3:F13473@2, k=15 → Emb:"Indians"@1 (de=10.25) +14 more |
| 3 | `get_upstream_features` | L2:F1680@1, k=15 → Emb:"Indians"@1 (de=8.56) +14 more |
| 4 | `get_upstream_features` | L3:F9646@2, k=10 → Emb:"Indians"@1 (de=3.97) +9 more |
| 5 | `inspect_feature` ×4 | L3:9646, L4:148, L2:2123, L0:10155 |
| 6 | `get_upstream_features` | L4:F148@3, k=12 → Emb:" abusers"@3 (de=19.12) +11 more |

### Build

`build_circuit` → 6 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 17,586 | 2,027 | 64,018 | 0 | $0.0904 | — | — |
| **Total** | | **17,586** | **2,027** | **64,018** | **0** | **$0.0904** | | |

**Oracle wall-clock time:** 0m 38s