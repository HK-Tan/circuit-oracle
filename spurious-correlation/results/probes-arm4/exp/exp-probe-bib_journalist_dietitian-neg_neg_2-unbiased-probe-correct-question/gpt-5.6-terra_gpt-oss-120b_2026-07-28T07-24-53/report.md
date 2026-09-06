# Circuit Oracle Report
**Date:** 2026-07-28 07:24:53 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe score is driven primarily by a genuine journalism/reporter circuit centered on “report,” with smaller direct contributions from superficial lexical/gender-related cues such as “His” and “world.”

**Confidence:** 8/10

**Reasoning:** The synthetic probe target has no vocabulary semantics itself, so the relevant evidence is the signed attribution into its injected probe direction. The dominant direct drivers are actually *negative* contributions from journalism features: L14:4420 at position 21 (“report”; −0.1455) and L19:2486 at positions 21, 22, and 26 (up to −0.1128). Thus, the sign indicates the direction of this particular linear class/probe encoding, not absence of profession evidence: journalism evidence strongly moves the score in the probe’s negative direction.

The main circuit saved is:

`Emb: report (pos 21)` → **Reporter/news-reporting recognition** → **Journalism/profession evidence** → **Late news-outlet/broadcasting representation** → `Output: synthetic profession-probe score`.

* The source is explicitly the embedding for **“ report” at position 21**, which directly excites L14:4420 by +5.2188 and L19:2486 by +3.3594. Its net full-graph influence is substantial and negative: **−5.257%** of total signed influence, larger in magnitude than the strongest non-source comparison position (ratio −1.633). This is strong evidence that the probe is responding to the actual occupation-related word.
* Mid-level L8:8855 (position 21) is a highly selective reporter/news-reporting feature (frac_nonzero **0.00847**), with promoted tokens including **“reporter,” “journalistic,” “reporters,” “journalist,” “reporting,” “journalism.”** It feeds the L14 profession feature (+5.0625 upstream effect into L14:4420).
* L14:4420 is also selective (frac_nonzero **0.0165**) and unambiguously encodes journalism/newspapers. Its activating examples contain “managing editor,” “reporter,” “newspaper,” and “reporting”; promoted tokens are **“journalists,” “journalistic,” “journalist,” “journalism,” “reporter,” “editorial.”**
* This journalism representation excites L19:2486 (+14.3125): a news-outlets/journalistic-sources feature (frac_nonzero **0.02926**) promoting **“reporting,” “reporter,” “coverage,” “reporters.”** L14:4420 also feeds L20:8433 (+5.0625), a news-broadcasting feature (frac_nonzero **0.03572**) promoting **“news,” “journalists,” “newspaper,” “journalism,” “reporters.”**
* These later features have negative direct effects on the probe: L19:2486 is −0.1128 at the report position and repeatedly negative at surrounding positions, while L20:8433 is −0.0623. This makes the profession-specific pathway the major mechanism, regardless of the probe-direction sign convention.

There **is** a spurious-cue branch, but it appears secondary rather than decisive. `Emb: His (pos 1)` activates L0:8964, a literal **“His”** marker (frac_nonzero **0.01755**), which directly contributes **+0.0791** to the probe. The full source-position influence from “His” is **+3.219%**, appreciable but smaller than the semantic “report” path in magnitude. Since this feature is a pronoun detector rather than a profession feature, it is valid evidence that the linear probe has incorporated a gender-correlated shortcut.

There is also a weak lexical/pattern contribution from `Emb: world (pos 6)` through L4:11898 (+0.0542 direct probe effect). However, L4:11898 is a rare **“World” followed by sport/war word** pattern feature (frac_nonzero **0.00176**), not a journalism or gender concept. Its input source has net influence **−4.589%**, but the inspected feature does not support interpreting it as a meaningful profession signal in this sentence; it is best treated as incidental phrase-pattern leakage.

Overall, the attribution circuit does **not** support the conclusion that this prediction is mainly gender-driven. The explicit profession cue “report” activates a coherent, multi-layer, semantically specific **reporter → journalism → news outlet/broadcasting** circuit, which dominates the attribution. But the positive direct `His` branch shows the probe is not clean: it also uses a non-professional male-marker feature, so the user’s spurious-feature concern is partly justified as a secondary bias/shortcut.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 21 | Reporter/news-reporting recognition |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 21 | Reporter/news-reporting recognition | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 21 | Reporter/news-reporting recognition | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 21 | Journalism/profession evidence | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 22 | Journalism/profession evidence | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 21 | Late news-outlet / broadcasting representation |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 26 | Late news-outlet / broadcasting representation |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L20:F8433](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/8433) | 26 | Late news-outlet / broadcasting representation | words related to news broadcasting | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/8433) |
| [L0:F8964](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) | 1 | Male possessive marker |  the possessive pronoun "His" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) |
| [L4:F11898](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11898) | 6 | World phrase-pattern feature |  mentions of "World" followed by a sport or war-related word | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11898) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:4420 de=-0.145 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@21` | ❌ error | — | — | Trace this major negative driver of the synthetic profession-probe score upstrea… |
| SA-2 | `L19:F2486@21` | ❌ error | — | — | Trace this strongest recurring negative late driver of the synthetic profession-… |
| SA-3 | `L20:F8433@26` | ❌ error | — | — | Trace this negative driver of the synthetic profession-probe score upstream to e… |
| SA-4 | `L4:F11898@6` | ❌ error | — | — | Trace this positive feature driving the synthetic profession-probe score upstrea… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×6 | L14:4420, L19:2486, L20:8433, L4:11898, L0:8964, L0:8444 |
| 2 | `get_upstream_features` | L14:F4420@21, k=15 → Emb:" report"@21 (de=5.22) +14 more |
| 3 | `get_upstream_features` | L19:F2486@21, k=15 → L14:F4420 (de=14.31) +14 more |
| 4 | `get_upstream_features` | L4:F11898@6, k=15 → Emb:" world"@6 (de=35.25) +14 more |
| 5 | `get_upstream_features` | L20:F8433@26, k=12 → Emb:" top"@26 (de=5.69) +11 more |
| 6 | `inspect_feature` ×3 | L8:8855, L0:14287, L0:2203 |
| 7 | `get_source_influence` | {'source_positions': [1], 'depth': 2} → {'depth': 2, 'source_positions': [1], 'S_pct_of_total': 3.219, 'R_pct_of_total': |
| 8 | `get_source_influence` | {'source_positions': [21], 'depth': 2} → {'depth': 2, 'source_positions': [21], 'S_pct_of_total': -5.257, 'R_pct_of_total |
| 9 | `get_source_influence` | {'source_positions': [6], 'depth': 2} → {'depth': 2, 'source_positions': [6], 'S_pct_of_total': -4.589, 'R_pct_of_total' |

### Build

`build_circuit` → 9 nodes, 9 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 19,241 | 2,576 | 57,766 | 0 | $0.1012 | — | — |
| **Total** | | **19,241** | **2,576** | **57,766** | **0** | **$0.1012** | | |

**Oracle wall-clock time:** 0m 40s