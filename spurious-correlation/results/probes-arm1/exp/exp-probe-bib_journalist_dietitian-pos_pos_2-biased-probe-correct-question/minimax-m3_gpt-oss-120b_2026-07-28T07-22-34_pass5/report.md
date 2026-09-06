# Circuit Oracle Report
**Date:** 2026-07-28 07:22:34 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe classifies this bio as a "nutritionist" profession using a circuit that is dominated by female-gender / pronoun features (She, her, herself, women, female names) rather than nutrition/cook/recipe semantic content, with only a single weak contribution from the embedding of "nutrition".

**Confidence:** 7

**Reasoning:** The attribution graph's top direct-effect features are almost exclusively gender markers, not profession indicators:
- **L4:15317** ("named entities like characters or people," promoted tokens include ▁she, ▁her — 0.018 frac_nonzero) and **L4:7864** (non-English/code/possessive-promoting feature, also promoting ▁herself — 0.015 frac_nonzero) fire at pos 1–2 from the "She" / " has" embeddings.
- **L6:11646** ("references to women…pronouns and titles", direct_effect +0.36/+0.29 at pos 1/2, promoted ▁herself/▁she/▁her, 0.020 frac_nonzero) and **L6:16329** ("female first names and possessive forms", direct_effect −0.17 at pos 1, suppresses ▁she/▁her, 0.122 frac_nonzero) form a yoked gender pair.
- **L2:7672** ("mentions of women by name and relationship", 0.022 frac_nonzero) and **L6:16329** further specialize on female-name/relationship signals.
- Mid-layer **L10:14965** ("terms relating to women", promoted ▁female/▁woman/▁she, 0.019) and **L12:12940** ("female pronouns and possessive pronouns", 0.007) propagate the gender signal upward.
- Late-layer **L14:12501** ("uses of the feminine pronoun", 0.014), **L18:14677** ("instances of women or girls being mentioned", 0.012) and **L19:9685** ("women's names and their roles or accomplishments", 0.014) — all with very low frac_nonzero (highly specific, selectivity ≈ 0.01) — are the dominant positive drivers of the probe, with direct_effects of +0.24, +0.20 and +0.15 respectively. **L18:14743** ("He") provides a negative pull (−0.11), confirming the direction is a *female* indicator.

Tracing upstream: L18:14677 at pos 1 receives direct_effect 27.1 from the **Emb:"She"** token and L18:14677 at pos 23 receives direct_effect 14.3 from **Emb:" She"** (a later feminine pronoun in the bio). The chain is Emb:She → L4:15317/7864 → L6:11646 → L10:14965/L12:12940 → L14:12501/L18:14677/L19:9685 → logit. The only profession-content feature in the top 20 is **L6:11327** ("words or phrases related to food or nutrition", pos 13 on "nutrition", direct_effect +0.15, 0.012 frac_nonzero), which traces directly to **Emb:" nutrition"** (direct_effect 21). It is an order of magnitude smaller than the cumulative female-gender signal.

The user's concern is confirmed: the circuit uses a spurious "is this bio about a woman?" feature (low-frac_nonzero, highly specific, female-name and pronoun detectors) as the primary evidence, and uses genuine profession markers ("nutrition", plus L4:13412 "diets and dietary health") only secondarily. The probe's classification of "nutritionist" is largely a confounded detection of *the gender of the subject* through features whose semantic content is she/her/women/female-names, with the actual content word "nutrition" providing a much smaller contribution. If the same prose were written about a man, the female-gender supernode would likely suppress the prediction rather than support it, which is the signature of a bias-correlated (not causally valid) probe.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: She (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 23 | Emb: She (pos 23) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: nutrition (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L2:F7672](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) | 1 | Early entity/female-name features (L2-L4) |  mentions of women by name and relationship | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Early entity/female-name features (L2-L4) |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Early entity/female-name features (L2-L4) | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 13 | Early entity/female-name features (L2-L4) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Female-gender pronoun/possessive features (L6) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Female-gender pronoun/possessive features (L6) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 23 | Female-gender pronoun/possessive features (L6) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 13 | Female-gender pronoun/possessive features (L6) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 1 | Female-gender pronoun/possessive features (L6) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 23 | Female-gender pronoun/possessive features (L6) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L10:F14965](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) | 2 | Mid-layer female/women terms (L10-L12) |  terms relating to women | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Mid-layer female/women terms (L10-L12) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 3 | Mid-layer female/women terms (L10-L12) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L14:F12501](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) | 2 | Late-layer pronoun/gender features (L14-L19) |  uses of the feminine pronoun. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Late-layer pronoun/gender features (L14-L19) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 2 | Late-layer pronoun/gender features (L14-L19) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 23 | Late-layer pronoun/gender features (L14-L19) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 23 | Late-layer pronoun/gender features (L14-L19) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 23 | Late-layer pronoun/gender features (L14-L19) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 23 | Late-layer pronoun/gender features (L14-L19) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.357 |
| 3 | `inspect_feature` ×14 | L6:11646, L12:12940, L18:14677, L4:15317, L4:7864, L6:16329, L6:11327, L10:14965, L14:12501, L19:9685, L4:13412, L7:8644, L18:14743, L2:7672 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@1` | ❌ error | — | — | Trace the upstream sources of the L18:14677 feature (instances of women/girls be… |
| SA-2 | `L18:F14677@23` | ❌ error | — | — | Trace upstream of L18:14677 (women/girls mentioned) at position 23. What input t… |
| SA-3 | `L6:F11327@13` | ❌ error | — | — | Trace upstream of L6:11327 (food/nutrition words) at pos 13. Is this a genuine p… |
| SA-4 | `L12:F12940@2` | ❌ error | — | — | Trace upstream of L12:12940 (female pronouns/possessives) at pos 2. Identify the… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14677@1, k=12 → Emb:"She"@1 (de=27.12) +11 more |
| 2 | `get_upstream_features` | L18:F14677@23, k=12 → Emb:" She"@23 (de=14.31) +11 more |
| 3 | `get_upstream_features` | L6:F11327@13, k=12 → Emb:" nutrition"@13 (de=21.00) +11 more |
| 4 | `get_upstream_features` | L12:F12940@2, k=12 → Emb:"She"@1 (de=6.03) +11 more |
| 5 | `get_upstream_features` | L6:F11646@2, k=8 → L4:F15317 (de=8.75) +7 more |
| 6 | `get_upstream_features` | L4:F15317@2, k=8 → Emb:"She"@1 (de=13.56) +7 more |
| 7 | `get_upstream_features` | L10:F14965@2, k=8 → L4:F15317 (de=5.56) +7 more |
| 8 | `get_upstream_features` | L4:F13412@13, k=8 → Emb:" nutrition"@13 (de=14.06) +7 more |
| 9 | `inspect_feature` ×3 | L8:7245, L7:2765, L6:16329 |
| 10 | `get_upstream_features` | L19:F9685@23, k=8 → Emb:" She"@23 (de=5.72) +7 more |
| 11 | `get_upstream_features` | L18:F14743@23, k=8 → Emb:" She"@23 (de=16.62) +7 more |

### Build

`build_circuit` → 8 nodes, 7 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 48,625 | 4,513 | 211,083 | 0 | $0.0327 | — | — |
| **Total** | | **48,625** | **4,513** | **211,083** | **0** | **$0.0327** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 14s