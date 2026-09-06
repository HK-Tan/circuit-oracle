# Circuit Oracle Report
**Date:** 2026-07-28 07:25:00 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe’s score is driven primarily by a highly direct **female-pronoun / female-person circuit** centered on “she,” with real but smaller explicit nursing evidence from “Perioperative nurses”; therefore the concern about spurious gender reliance is substantiated.

**Confidence:** 9/10

**Reasoning:**  
The probe target is synthetic (the sole returned label was `""`), so all direct effects below refer to its injected classification direction rather than a next-token logit.

The strongest positive driver is **L6:F11646 at position 7**, with direct effect **+1.5547**. It is an unusually selective female-reference feature (`frac_nonzero=0.01976`): its activating examples overwhelmingly fire on **“her”**, it promotes *she/her/herself*, and its autointerp label is “references to women, potentially triggered by pronouns and titles.” Direct upstream attribution shows that its dominant input is **Emb: “ she” (pos 7)**, with a very large positive effect (**+31.625**) into the feature. This is direct evidence that the model identifies the subject as female and that this representation aligns positively with the probe direction.

That signal is preserved and amplified in the female-reference branch:

- **L12:F12940 (pos 7)**, direct effect **+0.6875**, is a specific female-pronoun/possessive detector (`frac_nonzero=0.00652`) with examples triggered by *her* and *herself*. It receives positive input from `she` (**+12.3125**) and from L6:F11646 (**+4.9688**).
- **L15:F12956 (pos 7)** is a “female names and female-related words” feature (`frac_nonzero=0.0188`), positively feeding the late female detector.
- **L18:F14677 (pos 7)** is the second-largest positive output feature, direct effect **+0.9062**. It detects mentions of women/girls (`frac_nonzero=0.01225`), promotes *she/her/herself*, and receives **+28.375** directly from Emb: ` she`, plus positive signals from L6:F11646 (**+5.5938**) and L12:F12940 (**+4.3125**).
- **L19:F9685 (pos 7)**, direct effect **+0.5625**, represents women’s names/roles/accomplishments (`frac_nonzero=0.01351`) and is likewise directly excited by ` she` (**+12.25**) and the preceding female features.

Thus, the saved circuit’s `Emb: she → Female-pronoun detectors → Composed female-reference detectors → Late female-person evidence → Probe classification score` path is not merely correlational at the text level: its links are positive attribution edges and its major nodes are among the probe’s largest direct contributors. The late female features feed the score directly, rather than serving only as incidental intermediates.

There **is** a genuine profession mechanism. The text’s **“Perioperative nurses”** tokens activate **L6:F15267** at positions 14 and 15. This feature is explicitly a nursing-profession detector (`frac_nonzero=0.01594`), with top activating examples on *RN*, *nurse*, and *nurses*. At pos 15 it contributes **+0.5547** directly to the probe; at pos 14 it contributes an additional **+0.3203**. Its upstream inputs are the profession tokens themselves: **Emb: ` nurses` (pos 15), +16.125**; **Emb: `perative` (pos 14), +4.375**; and **Emb: ` Perio` (pos 13), +1.25**.

The full multi-hop source-influence measurement confirms that the profession phrase is meaningfully causal: positions 13–15 account for **+10.469%** of total signed influence, with `S_over_R=7.09`, a strong source-driven result. So this is not a classifier based *only* on gender; it does use explicit nursing language.

However, the local output-feature ranking makes the spurious issue clear. The single strongest score contribution is the female detector L6:F11646 (**+1.5547**), and the next is L18:F14677 (**+0.9062**), both driven by `she`; these individually exceed the principal nursing feature’s **+0.5547**. Multiple additional gender/female-person features contribute positively as well (L12:F12940, L19:F9685). The direct two-hop aggregate for just position 7 is net negative (**−1.505%**) because there are countervailing suppressive pathways, so it should not be read as a clean total gender effect. But this does **not** negate the positive, dominant direct feature contributions from the female circuit; it means the residual circuit also contains inhibition that partially offsets them.

In short: the probe is using valid occupational evidence—especially the explicit *Perioperative nurses* phrase—but it is also substantially aligned with a chain of highly specific **female-marker features**, headed by the pronoun *she*. This is a mixed mechanism with a prominent gender-associated shortcut, not a profession-pure classifier.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 7 | Female-pronoun detectors |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 7 | Composed female-reference detectors | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L15:F12956](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12956) | 7 | Composed female-reference detectors | female names and female-related words in the document. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12956) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 7 | Composed female-reference detectors |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 7 | Late female-person / women-reference evidence |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 7 | Late female-person / women-reference evidence |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 15 | Nursing profession detector |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 14 | Nursing profession detector |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11646 de=1.555 |
| 3 | `inspect_feature` ×5 | L6:11646, L18:14677, L12:12940, L19:9685, L4:7864 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@7` | ❌ error | — | — | Trace the positive path driving the probe score. Determine whether it originates… |
| SA-2 | `L6:F11646@7` | ❌ error | — | — | Trace the strongest positive probe-driving feature upstream to token embeddings.… |
| SA-3 | `L19:F9685@7` | ❌ error | — | — | Trace this late positive probe feature upstream, identify its semantics and sour… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F11646@7, k=20 → Emb:" she"@7 (de=31.62) +19 more |
| 2 | `get_upstream_features` | L18:F14677@7, k=20 → Emb:" she"@7 (de=28.38) +19 more |
| 3 | `get_upstream_features` | L12:F12940@7, k=20 → Emb:" she"@7 (de=12.31) +19 more |
| 4 | `get_upstream_features` | L19:F9685@7, k=20 → Emb:" she"@7 (de=12.25) +19 more |
| 5 | `get_upstream_features` | L6:F15267@15, k=15 → Emb:" nurses"@15 (de=16.12) +14 more |
| 6 | `inspect_feature` ×3 | L6:15267, L17:5889, L15:12956 |
| 7 | `get_source_influence` | {'source_positions': [7], 'depth': 2} → {'depth': 2, 'source_positions': [7], 'S_pct_of_total': -1.505, 'R_pct_of_total' |
| 8 | `get_source_influence` | {'source_positions': [13, 14, 15], 'depth': 2} → {'depth': 2, 'source_positions': [13, 14, 15], 'S_pct_of_total': 10.469, 'R_pct_ |

### Build

`build_circuit` → 9 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 18,626 | 2,546 | 64,616 | 0 | $0.1009 | — | — |
| **Total** | | **18,626** | **2,546** | **64,616** | **0** | **$0.1009** | | |

**Oracle wall-clock time:** 0m 39s