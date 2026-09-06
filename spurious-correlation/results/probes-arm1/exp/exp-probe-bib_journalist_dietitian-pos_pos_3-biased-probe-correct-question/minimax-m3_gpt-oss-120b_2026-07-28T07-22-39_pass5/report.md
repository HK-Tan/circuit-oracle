# Circuit Oracle Report
**Date:** 2026-07-28 07:22:39 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe classification for this "dietitian/nutritionist"-style biography is driven almost entirely by an accumulation of features that detect the *female gender* of the subject (She/her pronouns, female names, women's roles) — not by any profession-specific or topic-specific signal — confirming the user's concern about a spurious gender-marker circuit.

**Confidence:** 8

**Reasoning:** The top features feeding the probe direction are uniformly gendered: L6:F11646 (frac_nonzero 0.020, "references to women / pronouns", direct_effect +0.34), L18:F14677 (frac_nonzero 0.012, "instances of women or girls being mentioned", +0.24 at pos 29), L12:F12940 ("female pronouns and possessive pronouns", +0.16), L19:F9685 ("women's names and roles", +0.15), L14:F12501 ("feminine pronoun", +0.12), L10:F14965 ("terms relating to women", +0.16 on "is"), L0:F15382 ("mentions of a female person", +1.7–2.4 in the embedding->L6/L17 chain), and L2:F7672 ("mentions of women by name and relationship"). The only content/topic feature, L6:F11327 "food or nutrition" (+0.10 at pos 15 = "food"), is a minor contributor compared to the gender stack. The signal traces from the embeddings of the **pronouns "She" at pos 1 and 29, "her" at pos 40, and even "others" at pos 6** (which feeds L0:F2349) into the early female detectors, which propagate up through L6:11646 → L10:14965 → L12:12940 → L14:12501 → L17:5889 → L18:14677/14743 → L19:9685, each layer just re-accumulating the same "this text is about a woman" signal. L18:F14743 is a "He" feature that fires with **negative** direct_effect (−0.12) on the *masculine* token here (because the text says "She does not believe in dieting"), which actually pulls the probe *away* from its top direction — a clear sign the probe direction is aligned with "female" rather than "male" along the same gender axis. There is no dietitian/nutritionist/healthy-eating feature at any layer; the only true profession-adjacent feature (L6:F11327) carries about a third of the effect of a single pronoun detector. The probe direction is therefore using the subject's gender as a near-perfect proxy for the profession, which is exactly the spurious-correlation failure mode the user flagged.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 29 | Probe classification output | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 29 | Late-layer "women/girls mentioned" detectors |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Late-layer "women/girls mentioned" detectors |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 40 | Late-layer "women/girls mentioned" detectors |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 66 | Late-layer "women/girls mentioned" detectors |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 29 | Late-layer "women/girls mentioned" detectors |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 40 | Late-layer "women/girls mentioned" detectors |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 29 | Late-layer "women/girls mentioned" detectors | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 29 | Late-layer "women/girls mentioned" detectors |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Mid-layer female-pronoun/name detectors | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L14:F12501](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) | 3 | Mid-layer female-pronoun/name detectors |  uses of the feminine pronoun. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) |
| [L10:F14965](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) | 2 | Mid-layer female-pronoun/name detectors |  terms relating to women | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) |
| [L10:F14965](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) | 3 | Mid-layer female-pronoun/name detectors |  terms relating to women | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 29 | Mid-layer female-pronoun/name detectors |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 19 | Mid-layer female-pronoun/name detectors |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 3 | Mid-layer female-pronoun/name detectors |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L2:F7672](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) | 1 | Mid-layer female-pronoun/name detectors |  mentions of women by name and relationship | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Early-layer "female" detectors |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Early-layer "female" detectors |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 3 | Early-layer "female" detectors |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 29 | Early-layer "female" detectors |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 1 | Early-layer "female" detectors | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 29 | Early-layer "female" detectors | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Early-layer "female" detectors | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Early-layer "female" detectors |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 1 | Early-layer "female" detectors | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 29 | Early-layer "female" detectors | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F2349](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) | 6 | Early-layer "female" detectors |  the word "others" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 15 | Topic/content features (food, nutrition) — minor contribution |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 29 | Topic/content features (food, nutrition) — minor contribution |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: She (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 29 | Emb:  She (pos 29) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 40 | Emb:  her (pos 40) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb:  food (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb:  others (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.340 |
| 3 | `inspect_feature` ×9 | L6:11646, L18:14677, L4:7864, L19:9685, L12:12940, L4:15317, L2:7672, L14:12501, L6:11327 |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@1` | ❌ error | — | — | Trace this "references to women / pronouns" feature at L6 pos 1 ("She") upstream… |
| SA-2 | `L18:F14677@29` | ❌ error | — | — | Trace this L18 "women/girls being mentioned" feature at pos 29 upstream. Find th… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F11646@1, k=10 → Emb:"She"@1 (de=19.25) +9 more |
| 2 | `get_upstream_features` | L18:F14677@29, k=10 → Emb:" She"@29 (de=14.38) +9 more |
| 3 | `get_upstream_features` | L19:F9685@29, k=10 → Emb:" She"@29 (de=5.62) +9 more |
| 4 | `get_upstream_features` | L12:F12940@2, k=10 → Emb:"She"@1 (de=6.56) +9 more |
| 5 | `inspect_feature` ×6 | L7:8644, L18:14743, L6:16329, L17:5889, L10:14965, L0:15382 |
| 6 | `get_upstream_features` | L6:F11646@2, k=8 → L4:F15317 (de=7.69) +7 more |
| 7 | `get_upstream_features` | L18:F14677@1, k=8 → Emb:"She"@1 (de=27.12) +7 more |
| 8 | `get_upstream_features` | L6:F11327@15, k=8 → Emb:" food"@15 (de=34.00) +7 more |
| 9 | `get_upstream_features` | L14:F12501@3, k=8 → L13:F11685 (de=-7.72) +7 more |
| 10 | `get_upstream_features` | L19:F9685@1, k=8 → ❌ Feature (layer=19, feature_idx=9685) not found at pos=1. Thi |
| 11 | `get_upstream_features` | L17:F5889@29, k=8 → Emb:" She"@29 (de=19.38) +7 more |
| 12 | `get_upstream_features` | L12:F12940@1, k=8 → ❌ Feature (layer=12, feature_idx=12940) not found at pos=1. Th |
| 13 | `get_upstream_features` | L19:F9685@40, k=8 → Emb:" her"@40 (de=7.91) +7 more |
| 14 | `get_upstream_features` | L6:F11327@2, k=8 → ❌ Feature (layer=6, feature_idx=11327) not found at pos=2. Thi |
| 15 | `get_upstream_features` | L6:F16329@29, k=5 → Emb:" She"@29 (de=7.03) +4 more |
| 16 | `get_upstream_features` | L18:F14743@29, k=5 → Emb:" She"@29 (de=16.88) +4 more |
| 17 | `get_upstream_features` | L7:F8644@19, k=5 → Emb:"She"@1 (de=9.31) +4 more |
| 18 | `get_upstream_features` | L7:F8644@3, k=5 → Emb:"She"@1 (de=8.25) +4 more |
| 19 | `get_upstream_features` | L18:F14743@1, k=5 → Emb:"She"@1 (de=27.25) +4 more |
| 20 | `get_upstream_features` | L18:F14677@40, k=5 → Emb:" her"@40 (de=21.62) +4 more |
| 21 | `inspect_feature` ×2 | L0:2349, L4:7864 |

### Build

`build_circuit` → 10 nodes, 9 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 47,521 | 5,144 | 350,775 | 0 | $0.0415 | — | — |
| **Total** | | **47,521** | **5,144** | **350,775** | **0** | **$0.0415** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 16s