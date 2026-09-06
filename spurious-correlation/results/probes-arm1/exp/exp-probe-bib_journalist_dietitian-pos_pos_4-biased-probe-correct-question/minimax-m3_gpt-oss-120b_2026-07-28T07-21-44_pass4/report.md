# Circuit Oracle Report
**Date:** 2026-07-28 07:21:44 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "dietitian" classification is driven overwhelmingly by female-gender/female-name features, not by dietetics-specific vocabulary. The strongest positive direct effects come from a stack of features (L18-F14677, L19-F9685, L12-F12940, L12-F14970, L6-F11646) that all fire on female pronouns ("She"/"she"), the female name "Heather", and possessives like "her". Genuine profession features (L4-F13412 "diets/dietary health", L3-F11774 firing on the "Die"/"te" subword of "Dietetics") do exist, but their direct effects are small and they trace only to local subword tokens, not to a clean profession concept.

**Confidence:** 9

**Reasoning:** The attribution graph is unambiguous about the user's concern. Of the top 20 direct-effect contributors to the probe, ~10 are pure gender/name features:

- **L6:F11646** "references to women, triggered by pronouns and titles" (frac_nonzero 0.02) — fires at pos 1 ("She") with direct_effect +0.209 and pos 2 with +0.14; its top upstream is the **Emb: She (pos 1)** with direct_effect +19.25. Promoted tokens are "herself/ihrem/she/her/ihren".
- **L18:F14677** "instances of women or girls being mentioned" (frac_nonzero 0.01) — fires at pos 57 ("she", +0.14), pos 94 ("She", +0.12), pos 1 (+0.12); its top upstream is **Emb: she (pos 57)** with direct_effect +22.6. Promoted: "herself/she/her/ihrem/She".
- **L19:F9685** "references to women's names and their roles" (frac_nonzero 0.01) — fires at pos 57, upstream is again **Emb: she (pos 57)** +9.94.
- **L12:F12940** "female pronouns and possessive pronouns" (pos 2, +0.12), upstream: **Emb: She (pos 1)** +6.03.
- **L12:F14970** "names of people, both first and last names" (pos 31, +0.11), upstream: **Emb: Heather (pos 31)** +2.98 and L4:F1276.
- **L7:F8644** "woman's name in a variety of contexts" (pos 31, -0.21, i.e. *suppresses* the probe).
- **L4:F1276** "capitalized names and titles" (pos 31, +0.12) — upstream is **Emb: Heather (pos 31)** +10.94.
- **L0:F7532** (pos 31, upstream **Emb: Heather (pos 31)** +18.5).
- **L0:F12519** also fires repeatedly on "She"/"she" but with *negative* sign — these are generic pronouns, not female-specific.

By contrast, the genuinely profession-related features have much smaller direct effects:
- **L4:F13412** "terms related to diets and dietary health" fires at pos 21 ("Dietetics"/"te") with direct_effect only +0.16, and at pos 55 ("RD") +0.12. Upstream: **Emb: Die (pos 20)** +4.06 and **Emb: RD (pos 55)** +11.3. Promoted tokens include "diet/diets/DIET/dieting".
- **L3:F11774** fires on the "Die" subword (+4.81) — purely a subword feature, not a profession concept.

Summing positive direct effects: gender-path features total roughly +0.86 (L6:11646 +0.35, L18:14677 +0.39, L19:9685 +0.09, L12:12940 +0.12, L12:14970 +0.11, L7:2765 +0.13, L4:1276 +0.12), versus the profession-path L4:13412 at +0.16 and its sub-word L3:11774 sub-component. The female-gender signal is roughly 3–4× the magnitude of the profession signal.

The signal flow shows: female-pronoun embeddings ("She" at pos 1, "she" at pos 57, "She" at pos 94) and the female proper name "Heather" (pos 31) flow through mid-layer female-gender detectors (L6:11646, L7:8644/2765, L6:16329) up to late-layer female-reference features (L18:14677, L19:9685, L12:12940/14970), which feed the probe. The profession path is a thin branch off subword tokens "Die"/"te" (Dietetics) and "RD" through L3:11774 and L4:13412, with L4:13412's L6::11774 subword root showing it is mostly detecting the literal letters "d-i-e-t" rather than the abstract profession.

**Conclusion for the user's concern:** The user is correct. The circuit is dominated by female-gender features. A dietitian-bio probe trained on this model is partially riding on a female-name/female-pronoun shortcut: L18-F14677 fires on "she" with direct_effect +22.6 directly into the probe's late layer, while the actual dietetics vocabulary (Dietetics, RD, Dietitian, nutrition) contributes only a fraction of the score. The profession signal is real but small, and the model's internal representation of "dietitian" is confounded with "female subject" — exactly the spurious-correlation mechanism the user suspected.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 57 | Probe output (profession classification) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 57 | Late-layer female-gender features (L18-F14677, L19-F9685, L12-F12940, L12-F14970) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 94 | Late-layer female-gender features (L18-F14677, L19-F9685, L12-F12940, L12-F14970) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Late-layer female-gender features (L18-F14677, L19-F9685, L12-F12940, L12-F14970) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 57 | Late-layer female-gender features (L18-F14677, L19-F9685, L12-F12940, L12-F14970) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Late-layer female-gender features (L18-F14677, L19-F9685, L12-F12940, L12-F14970) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 31 | Late-layer female-gender features (L18-F14677, L19-F9685, L12-F12940, L12-F14970) |  names of people, both first and last names | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 31 | Mid-layer female-gender features (L7-F8644, L7-F2765, L6-F11646, L6-F16329) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 31 | Mid-layer female-gender features (L7-F8644, L7-F2765, L6-F11646, L6-F16329) |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Mid-layer female-gender features (L7-F8644, L7-F2765, L6-F11646, L6-F16329) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Mid-layer female-gender features (L7-F8644, L7-F2765, L6-F11646, L6-F16329) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 1 | Mid-layer female-gender features (L7-F8644, L7-F2765, L6-F11646, L6-F16329) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 31 | Proper-noun / entity-name features (L4-F1276, L4-F15317, L0-F7532) | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Proper-noun / entity-name features (L4-F1276, L4-F15317, L0-F7532) |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 31 | Proper-noun / entity-name features (L4-F1276, L4-F15317, L0-F7532) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 21 | Profession-related features (L4-F13412 diets/dietary health, L3-F11774 "Die"/Dietetics) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 55 | Profession-related features (L4-F13412 diets/dietary health, L3-F11774 "Die"/Dietetics) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L3:F11774](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11774) | 21 | Profession-related features (L4-F13412 diets/dietary health, L3-F11774 "Die"/Dietetics) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11774) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L7:8644 de=-0.212 |
| 3 | `inspect_feature` ×14 | L7:8644, L6:11646, L4:13412, L18:14677, L4:7864, L7:2765, L4:1276, L0:8974, L12:12940, L12:14970, L0:6051, L19:9685, L6:16329, L4:15317 |

### Dispatch: 7 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F9685@57` | ❌ error | — | — | Trace the path from L19:F9685 ("references to women's names and roles"). I want … |
| SA-2 | `L18:F14677@57` | ❌ error | — | — | Trace the path from L18:F14677 ("instances of women or girls being mentioned") a… |
| SA-3 | `L12:F12940@2` | ❌ error | — | — | Trace the path from L12:F12940 ("references to female pronouns and possessive pr… |
| SA-4 | `L4:F13412@21` | ❌ error | — | — | Trace the path from L4:F13412 ("terms related to diets and dietary health") at p… |
| SA-5 | `L7:F8644@31` | ❌ error | — | — | Trace the path from L7:F8644 ("woman's name in a variety of contexts") at pos 31… |
| SA-6 | `L7:F2765@31` | ❌ error | — | — | Trace the path from L7:F2765 ("mentions of people, roles, personal details") at … |
| SA-7 | `L4:F1276@31` | ❌ error | — | — | Trace the path from L4:F1276 ("capitalized names and titles") at pos 31. Direct … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L7:F8644@31, k=10 → Emb:"She"@1 (de=7.47) +9 more |
| 2 | `get_upstream_features` | L6:F11646@1, k=10 → Emb:"She"@1 (de=19.25) +9 more |
| 3 | `get_upstream_features` | L4:F13412@21, k=10 → L3:F11774 (de=4.81) +9 more |
| 4 | `get_upstream_features` | L18:F14677@57, k=10 → Emb:" she"@57 (de=22.62) +9 more |
| 5 | `get_upstream_features` | L7:F2765@31, k=10 → Emb:"She"@1 (de=3.34) +9 more |
| 6 | `get_upstream_features` | L12:F12940@2, k=10 → Emb:"She"@1 (de=6.03) +9 more |
| 7 | `get_upstream_features` | L19:F9685@57, k=10 → Emb:" she"@57 (de=9.94) +9 more |
| 8 | `get_upstream_features` | L4:F7864@1, k=10 → Emb:"She"@1 (de=24.62) +9 more |
| 9 | `get_upstream_features` | L6:F11646@2, k=10 → L4:F15317 (de=8.75) +9 more |
| 10 | `get_upstream_features` | L18:F14677@94, k=10 → Emb:" She"@94 (de=15.62) +9 more |
| 11 | `get_upstream_features` | L4:F1276@31, k=10 → Emb:" Heather"@31 (de=10.94) +9 more |
| 12 | `get_upstream_features` | L12:F14970@31, k=10 → Emb:"<bos>"@0 (de=-3.48) +9 more |
| 13 | `get_upstream_features` | L4:F15317@2, k=10 → Emb:"She"@1 (de=13.56) +9 more |
| 14 | `get_upstream_features` | L6:F16329@1, k=10 → Emb:"She"@1 (de=8.94) +9 more |
| 15 | `get_upstream_features` | L3:F11774@21, k=10 → Emb:" Die"@20 (de=5.88) +9 more |
| 16 | `get_upstream_features` | L17:F5889@57, k=8 → Emb:" she"@57 (de=30.62) +7 more |
| 17 | `get_upstream_features` | L15:F3330@57, k=8 → Emb:" she"@57 (de=24.00) +7 more |
| 18 | `get_upstream_features` | L16:F2918@57, k=8 → Emb:" she"@57 (de=26.88) +7 more |
| 19 | `get_upstream_features` | L3:F10028@21, k=8 → Emb:" Die"@20 (de=6.94) +7 more |
| 20 | `get_upstream_features` | L0:F7532@31, k=8 → Emb:" Heather"@31 (de=18.50) +7 more |
| 21 | `get_upstream_features` | L0:F14824@2, k=8 → Emb:" has"@2 (de=32.75) +7 more |
| 22 | `get_upstream_features` | L4:F13412@55, k=5 → Emb:" RD"@55 (de=11.31) +4 more |
| 23 | `get_upstream_features` | L3:F11774@21, k=5 → Emb:" Die"@20 (de=5.88) +4 more |

### Build

`build_circuit` → 12 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 36,479 | 6,234 | 212,282 | 0 | $0.0312 | — | — |
| **Total** | | **36,479** | **6,234** | **212,282** | **0** | **$0.0312** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 33s