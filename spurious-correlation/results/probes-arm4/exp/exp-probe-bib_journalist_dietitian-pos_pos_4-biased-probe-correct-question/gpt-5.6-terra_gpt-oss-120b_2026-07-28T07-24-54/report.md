# Circuit Oracle Report
**Date:** 2026-07-28 07:24:54 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The profession-probe score is driven substantially by female-gender / female-biography circuitry, alongside a smaller but genuine dietary-health signal—so the user’s concern is supported.

**Confidence:** 8/10

**Reasoning:** The circuit recorded in `Output: linear profession-classification probe score` is not a next-token circuit: all listed effects are projections onto the injected linear probe direction. Its largest positive drivers are overwhelmingly female-reference features rather than occupation-specific ones.

- **Direct gender route.** `Emb: She (pos 1)` strongly excites the early female-reference detector `L6:F11646` (at pos 1, direct upstream embedding effect **+19.25**). This feature is selective (`frac_nonzero=0.01976`) and its activating examples are dominated by *her*; its promoted tokens include *she*, *her*, and *herself*. `L6:F11646` directly raises the probe at both pos 1 (**+0.2090**) and pos 2 (**+0.1396**). Thus the initial “She has …” is itself a major positive classification cue.

- **Late consolidation of the female signal.** `Emb: she (pos 57)`—the pronoun near “Since becoming an RD, **she** has …”—is the strongest identified source for the major late feature `L18:F14677` (embedding-to-feature effect **+22.625**). `L18:F14677` is a selective women/girls-pronoun feature (`frac_nonzero=0.01225`), with promoted tokens *she*, *her*, and *herself*. It makes large direct positive contributions to the probe: **+0.1436** at pos 57, **+0.1245** at pos 94, and **+0.1240** at pos 1. Its upstream path also contains `L15:F3330` (personal stories, especially women; `frac_nonzero=0.01932`, **+3.4531** to `L18:F14677`) and `L17:F5889` (person/pronoun references; `frac_nonzero=0.01848`, **+3.5156**). This is a clear pronoun-to-female-biography representation-to-probe pathway, rather than an RD/dietetics pathway.

- **Biography/name-associated gender route.** At the “Heather” position (31), `L7:F8644` is specifically a *woman’s-name* feature (`frac_nonzero=0.00902`) and has the single largest-magnitude direct contribution, but **negative** (**−0.2119**). Its examples contain female names, daughters, and women’s contexts; its suppressed tokens include *herself*, *her*, and *she*, while promoted tokens are male-coded forms such as *himself*. Hence the probe is not simply adding every female marker: this particular female-name/gender direction counteracts the score. Nevertheless, its inputs are exactly the gender/name context: `She` at pos 1 contributes **+7.4688**, `L6:F11646` contributes **+3.1094** (pos 1) and **+2.9375** (pos 2), and the `Heather` embedding itself contributes **+1.1484**. A more generic personal-biography feature, `L7:F2765` (`frac_nonzero=0.04537`), positively contributes **+0.1338**, with the same female/name inputs.

- **Genuine profession-relevant evidence exists, but is less prominent.** `L4:F13412` is a fairly selective diet/dietary-health detector (`frac_nonzero=0.01216`), promoting *diet*, *diets*, and *dieting*. It contributes **+0.1631** at pos 21 and **+0.1226** at pos 55. Its upstream inputs include `Emb: Die (Dietetics; pos 20)` (**+4.0625**) and `Emb: Nutritional (pos 9)` (**+1.4531**). This is good evidence that the probe uses semantically appropriate “Nutritional Sciences”/“Dietetics” content.

Overall, the saved circuit has two separable positive mechanisms: (1) a valid diet-and-dietetics feature feeding the probe, and (2) multiple high-impact female pronoun / female personal-biography features, especially `L6:F11646` and `L18:F14677`. Since several of the largest positive direct probe effects are gender-related and are directly sourced from *She/she*, the classification is **not purely profession-based**. It appears to exploit a gender–profession correlation in its training signal in addition to recognizing genuine dietetics/nutrition evidence.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Early female-reference detectors |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Early female-reference detectors |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Early female-reference detectors |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 31 | Female personal-biography/name features | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 31 | Female personal-biography/name features |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 31 | Female personal-biography/name features |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 21 | Diet/dietary-health semantic feature |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L10:F14965](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) | 2 | Late female-pronoun / personal-story representation |  terms relating to women | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Late female-pronoun / personal-story representation | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 57 | Late female-pronoun / personal-story representation |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 57 | Late female-pronoun / personal-story representation |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 57 | Late female-pronoun / personal-story representation |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 94 | Late female-pronoun / personal-story representation |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Late female-pronoun / personal-story representation |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L7:8644 de=-0.212 |
| 3 | `inspect_feature` ×9 | L7:8644, L6:11646, L4:13412, L18:14677, L4:7864, L7:2765, L4:1276, L12:12940, L12:14970 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F8644@31` | ❌ error | — | — | Trace this strong NEGATIVE probe-driving feature to embeddings. Determine whethe… |
| SA-2 | `L6:F11646@1` | ❌ error | — | — | Trace this strongest positive early feature to embeddings. Determine whether it … |
| SA-3 | `L4:F13412@21` | ❌ error | — | — | Trace this positive feature at the education text position upstream to embedding… |
| SA-4 | `L18:F14677@57` | ❌ error | — | — | Trace this major late positive feature to embeddings. Test whether it carries ex… |
| SA-5 | `L7:F2765@31` | ❌ error | — | — | Trace this positive feature at position 31 upstream to embeddings. Clarify any i… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14677@57, k=15 → Emb:" she"@57 (de=22.62) +14 more |
| 2 | `get_upstream_features` | L6:F11646@1, k=15 → Emb:"She"@1 (de=19.25) +14 more |
| 3 | `get_upstream_features` | L4:F13412@21, k=15 → L3:F11774 (de=4.81) +14 more |
| 4 | `get_upstream_features` | L7:F8644@31, k=15 → Emb:"She"@1 (de=7.47) +14 more |
| 5 | `get_upstream_features` | L7:F2765@31, k=15 → Emb:"She"@1 (de=3.34) +14 more |
| 6 | `get_upstream_features` | L12:F12940@2, k=15 → Emb:"She"@1 (de=6.03) +14 more |
| 7 | `inspect_feature` ×6 | L3:11774, L3:10028, L17:5889, L15:3330, L4:15317, L10:14965 |

### Build

`build_circuit` → 9 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 29,704 | 2,895 | 89,079 | 0 | $0.1400 | — | — |
| **Total** | | **29,704** | **2,895** | **89,079** | **0** | **$0.1400** | | |

**Oracle wall-clock time:** 0m 40s