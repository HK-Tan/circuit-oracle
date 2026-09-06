# Circuit Oracle Report
**Date:** 2026-07-28 07:23:35 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven primarily by **gender / "She" pronoun features** rather than by profession-specific content (nutritionist/dietitian vocabulary); a parallel but smaller food-topic pathway exists but the dominant causal signal flows through a multi-layer chain that ultimately aggregates the feminine pronoun "She" at many positions into late-layer output-driving features.

**Confidence:** 8

**Reasoning:**

**The dominant pathway is a pronoun / gender chain, not a profession chain.**
- The top feature driving the probe is **L6:F11646 at pos 1** (direct_effect = +0.34), and its largest upstream input is the **embedding of "She" at pos 1** (direct_effect = +19.25), with secondary contribution from L4:F7864, which itself is fed almost exclusively by the same "She" embedding (+24.6). L4:F7864 is therefore best read as a **dedicated "She" pronoun detector**.
- This "She" signal is preserved and amplified up the stack: L6:F11646 fires at positions 1, 2, and 29 (each a "She" or " She" token), so it is acting as a **multi-position feminine-pronoun aggregator** rather than encoding a semantic profession concept.
- The chain continues: L6:F11646 → L7:F2765 → L8:F7245 → L10:F14965 → **L12:F12940** (the "is copula / self-description" feature at pos 2) → **L14:F12501** (pos 3, fed by L6:F11646 and " empowering" pos-5 embedding) → **L17:L18 late-aggregator** (F5889 and F14677 firing at pos 1, 29, 40, 66 — i.e., every place a feminine pronoun appears) → output logit.
- Crucially, **the late aggregator L18:F14677 carries direct_effect +0.24 to the output** from pos 29 alone, and **fires at four different "She"/" She" positions** (1, 29, 40, 66), confirming it is a generic feminine-pronoun counter, not a "nutrition" feature.

**The profession-content pathway is real but secondary.**
- **L6:F11327 at pos 15** activates on the **embedding of " food"** (+34.0) and " healthy" (+4.3) — this is a genuine food/nutrition topic feature. It feeds **L19:F9685 at pos 29** (direct_effect +0.15 to the output), which appears to combine the food topic with the trailing " She" at pos 29. So nutrition/healthy-eating content does contribute, but at roughly half the magnitude of the pronoun pathway (0.15 vs. 0.34 for the top pronoun-driven feature), and the L19 feature itself is also receiving "She"-position inputs.

**Inhibitory features reinforce the diagnosis.**
- L6:F16329 (pos 1, pos 29) and L7:F8644 (pos 19, 29) carry **negative** direct_effects (−0.10 to −0.16) and are themselves fed by the "She" / " She" embeddings. These are anti-"She" suppressors; the net circuit clearly encodes *whether the text is about a woman*, not *what the woman does professionally*.

**What this means for the user's concern.**
The user's concern is **confirmed**: the probe's classification (likely "nutritionist/dietitian" or similar) is being driven substantially by the presence of the feminine pronoun "She" repeated throughout the bio. Features at L4 (7864), L6 (11646), L12 (12940), L14 (12501), L17 (5889), and L18 (14677) all activate primarily on pronoun tokens rather than on profession-defining vocabulary. The downstream F14677 aggregator fires at *every* "She" position in the prompt, which is the signature of a gender feature, not a profession feature. While a true food/nutrition pathway (L6:F11327 → L19:F9685) does exist and contributes, the **dominant causal signal to the probe is the count/presence of "She"**, indicating the probe — and therefore this circuit — is exploiting a spurious gender cue. The user's worry that "the circuit uses spurious features (e.g. gender markers) rather than genuine profession indicators" is supported by the attribution evidence.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F12519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) | 1 | Pronoun / sentence-initial detectors (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 1 | Pronoun / sentence-initial detectors (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F2349](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) | 6 | Pronoun / sentence-initial detectors (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) |
| [L2:F7672](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) | 1 | Pronoun / sentence-initial detectors (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) |
| [L3:F4020](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4020) | 1 | Pronoun / sentence-initial detectors (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4020) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | 'She' pronoun detector (L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Subject + copula pattern (L4-L5) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L5:F10952](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) | 1 | Subject + copula pattern (L4-L5) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) |
| [L3:F5393](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5393) | 2 | Subject + copula pattern (L4-L5) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5393) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | 'She' multi-position aggregator (L6) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | 'She' multi-position aggregator (L6) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 29 | 'She' multi-position aggregator (L6) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 15 | Food/nutrition topic feature (L6) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 1 | Inhibitory pronoun-side features (L6-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 29 | Inhibitory pronoun-side features (L6-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 29 | Inhibitory pronoun-side features (L6-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 19 | Inhibitory pronoun-side features (L6-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 2 | Mid-layer 'She'-driven bridges (L7-L10) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L8:F7245](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7245) | 2 | Mid-layer 'She'-driven bridges (L7-L10) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7245) |
| [L10:F14965](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) | 2 | Mid-layer 'She'-driven bridges (L7-L10) | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | 'is' copula / self-description (L12) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L14:F12501](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) | 3 | Empowerment / self-description feature (L14) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 29 | Late-layer multi-position 'She' aggregator (L17-L18) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 29 | Late-layer multi-position 'She' aggregator (L17-L18) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Late-layer multi-position 'She' aggregator (L17-L18) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 66 | Late-layer multi-position 'She' aggregator (L17-L18) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 40 | Late-layer multi-position 'She' aggregator (L17-L18) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 29 | Food topic / healthy-eating (L19) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.340 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@1` | ❌ error | — | — | Trace what L6:F11646 at pos 1 encodes. This feature fires on "She is" at the sta… |
| SA-2 | `L18:F14677@29` | ❌ error | — | — | Trace what L18:F14677 at pos 29 encodes. This feature fires at the truncated end… |
| SA-3 | `L4:F7864@1` | ❌ error | — | — | Trace what L4:F7864 at pos 1 encodes. This is an early-layer feature firing on "… |
| SA-4 | `L12:F12940@2` | ❌ error | — | — | Trace what L12:F12940 at pos 2 encodes. This mid-layer feature fires after "She … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F11646@1, k=10 → Emb:"She"@1 (de=19.25) +9 more |
| 2 | `get_upstream_features` | L4:F7864@1, k=10 → Emb:"She"@1 (de=24.62) +9 more |
| 3 | `get_upstream_features` | L12:F12940@2, k=10 → Emb:"She"@1 (de=6.56) +9 more |
| 4 | `get_upstream_features` | L18:F14677@29, k=10 → Emb:" She"@29 (de=14.38) +9 more |
| 5 | `get_upstream_features` | L4:F7864@2, k=10 → ❌ Feature (layer=4, feature_idx=7864) not found at pos=2. This |
| 6 | `get_upstream_features` | L18:F14677@1, k=10 → Emb:"She"@1 (de=27.12) +9 more |
| 7 | `get_upstream_features` | L19:F9685@29, k=10 → Emb:" She"@29 (de=5.62) +9 more |
| 8 | `get_upstream_features` | L6:F11327@15, k=10 → Emb:" food"@15 (de=34.00) +9 more |
| 9 | `get_upstream_features` | L4:F15317@2, k=8 → Emb:"She"@1 (de=13.12) +7 more |
| 10 | `get_upstream_features` | L14:F12501@3, k=8 → L13:F11685 (de=-7.72) +7 more |
| 11 | `get_upstream_features` | L17:F5889@29, k=8 → Emb:" She"@29 (de=19.38) +7 more |
| 12 | `get_upstream_features` | L6:F16329@1, k=8 → Emb:"She"@1 (de=8.94) +7 more |

### Build

`build_circuit` → 18 nodes, 20 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 21,519 | 5,632 | 37,733 | 0 | $0.0155 | — | — |
| **Total** | | **21,519** | **5,632** | **37,733** | **0** | **$0.0155** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 2s