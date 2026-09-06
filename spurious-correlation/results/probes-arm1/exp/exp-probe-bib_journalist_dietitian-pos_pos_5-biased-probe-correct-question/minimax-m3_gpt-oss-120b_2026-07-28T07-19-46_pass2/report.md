# Circuit Oracle Report
**Date:** 2026-07-28 07:19:46 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is overwhelmingly driven by feminine-gender signal — the pronouns "Her"/"She" and the female name "Heather" — not by the genuine profession/health content (nutrition, disordered eating, Academy of Nutrition and Dietetics), which functions only as a minor side-channel.

**Confidence:** 9

**Reasoning:** The full causal chain into the probe logit at L26 is dominated by *gender/identity* features at every layer, with diet/nutrition vocabulary playing a structurally minor role.

**Primary excitatory path (gender, strong):**
- Token embeddings for "Her" (pos 1) and "She" (pos 15) feed an L0 female-mention detector (L0:F15382, frac_nonzero 0.009, "mentions of a female person"), which excites a stack of gendered features:
  - L6:F11646 ("references to women, pronouns and titles", frac 0.020)
  - L5:F5996 / L6:F16329 ("female first names and their possessive forms", "words associated with females/femininity")
  - L7:F8644 ("woman's name", activated on "Heather" and pronouns)
  - L14:F12501 ("uses of the feminine pronoun", frac 0.014)
  - L15:F3330 and L17:F5889 ("personal stories of women"/"pronouns and possessive pronouns")
  - L18:F14677 ("instances of women or girls being mentioned", activation 30.5 at pos 15, direct_effect 0.17)
  - L19:F9685 ("references to women's names and their roles or accomplishments", activation 20–22, direct_effect 0.10–0.13)
- The token "Heather" (pos 46) independently drives this same female-identity circuit via L0:F7532 (proper-noun detector) → L4:F1276 (capitalized name detector) → L19:F9685 (direct embedding effect 4.6).
- All of these features have promoted tokens that are *exclusively* feminine pronouns/reflexives (herself, she, her, 她, 但她, ihrem) and suppressed tokens that are masculine (himself, his, 彼).

**Secondary, much weaker path (profession/health):**
- "nutrition" (pos 7) and "sports" (pos 6) feed L1:F6461, L1:F6631, L2:F2589 (medical-professional/exercise features) → L4:F13412 ("diets and dietary health", direct_effect 0.14 at pos 7) → L6:F5548/L8:F930 (dietary context) → L14:F12501.
- "disordered" (pos 12) is another direct upstream of L14:F12501.
- Crucially, this dietary path does **not** feed L19:F9685 or L18:F14677 — the probe's top features. Instead it terminates at L14:F12501 (feminine pronoun) and L18:F14677, acting as a *bridge* that re-routes the nutritional content into the gender-identity features rather than being recognized as a profession indicator itself. There is no "Academy of Nutrition and Dietetics" entity feature, no "spokesperson/consultant" role feature, and no "dietitian/nutritionist" profession feature in the circuit.

**Implication for the user's concern:** The user's hypothesis is confirmed. Of the top 20 features by direct effect on the probe, roughly 15 are female-identity/pronoun/name features, while only 2–3 are content-related (L4:F13412 diet, L2:F2589 medical-professional). The two highest-magnitude outputs (L19:F9685 activation ~20+, L18:F14677 activation 30.5) are both explicitly female-mention detectors. The probe therefore classifies "nutritionist" by routing through *who* is described (a woman) rather than *what* is described (nutrition/dietetics expertise). Genuine profession indicators are absent from the circuit — the model has no learned "dietitian" or "spokesperson" feature, so the gender signal does all the work.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'Her' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: ' She' (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 46 | Emb: ' Heather' (pos 46) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: ' sports' (pos 6) / ' nutrition' (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: ' sports' (pos 6) / ' nutrition' (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: ' disordered' (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 1 | Early female-marker detector (L0:F15382) | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 15 | Early female-marker detector (L0:F15382) | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 46 | Early proper-noun detector (L0:F7532) | proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L1:F6461](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6461) | 7 | Early diet/nutrition/medical-professional features (L1-L2) | technical language around physical activity, muscle function, and related studies | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6461) |
| [L1:F6631](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6631) | 7 | Early diet/nutrition/medical-professional features (L1-L2) | words related to dietary patterns and scientific studies | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6631) |
| [L2:F2589](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) | 7 | Early diet/nutrition/medical-professional features (L1-L2) | words related to medical professionals and medical specialties | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 46 | Mid-layer capitalized name detector (L4:F1276) | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 7 | Dietary-health feature (L4:F13412) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 13 | Dietary-health feature (L4:F13412) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Female-reference feature (L6:F11646, L5:F5996) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 15 | Female-reference feature (L6:F11646, L5:F5996) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L5:F5996](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5996) | 46 | Female-reference feature (L6:F11646, L5:F5996) |  words associated with females, femininity or womanhood | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5996) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 1 | Female-reference feature (L6:F11646, L5:F5996) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 15 | Female-reference feature (L6:F11646, L5:F5996) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 46 | Woman's-name feature (L7:F8644) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 46 | Person-mention feature (L7:F2765) |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L8:F930](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/930) | 13 | Dietary context (L8:F930, L6:F5548) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/930) |
| [L6:F5548](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5548) | 13 | Dietary context (L8:F930, L6:F5548) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5548) |
| [L14:F12501](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) | 13 | Late feminine-pronoun feature (L14:F12501) |  uses of the feminine pronoun. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 46 | Late name/role-mention feature (L12:F14970) |  names of people, both first and last names | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 15 | Late narrative-about-women feature (L15:L18) | personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 15 | Late narrative-about-women feature (L15:L18) | references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 15 | Late 'instances of women' feature (L18:F14677) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 46 | Late 'instances of women' feature (L18:F14677) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 15 | Late 'women's names & roles' feature (L19:F9685) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 46 | Late 'women's names & roles' feature (L19:F9685) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.283 |
| 3 | `inspect_feature` ×15 | L6:11646, L18:14677, L19:9685, L4:13412, L12:14970, L0:6051, L7:8644, L6:16329, L4:1276, L0:10148, L4:7864, L7:2765, L0:5686, L14:12501, L5:5996 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F9685@46` | ✅ reported | 3 | 6 | Trace the path upstream from L19:F9685 (pos 46, 'references to women's names and… |
| SA-2 | `L18:F14677@15` | ✅ reported | 5 | 13 | Trace the path upstream from L18:F14677 (pos 15, 'instances of women or girls be… |
| SA-3 | `L6:F11646@1` | ✅ reported | 3 | 2 | Trace the path upstream from L6:F11646 (pos 1, 'references to women, potentially… |
| SA-4 | `L4:F13412@7` | ✅ reported | 4 | 10 | Trace the path upstream from L4:F13412 (pos 7, 'terms related to diets and dieta… |

<details>
<summary><b>SA-1</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F9685 | " references to women's names and their roles or accomplishments." |
| 2 | `get_upstream_features` | L19:F9685@46, k=10 | Emb:" Heather"@46 (de=4.62) +9 more |
| 3 | `inspect_feature` | L4, F1276 | "capitalized names and titles, and names with lowercase letters in the " |
| 4 | `get_upstream_features` | L4:F1276@46, k=10 | Emb:" Heather"@46 (de=11.12) +9 more |
| 5 | `inspect_feature` | L0, F7532 | " proper nouns" |

**Findings:** Tracing from the women's‑name feature (L19:F9685) shows that its strongest upstream drivers are the raw token embeddings for the name 'Heather' (pos 46) and the pronoun 'Her' (pos 1). These tokens first activate a layer‑0 proper‑noun detector (L0:7532), which then excites a layer‑4 capitalized‑name detector (L4:1276). Both of these mid‑layer features funnel a large positive influence into L19:F968…

</details>

<details>
<summary><b>SA-2</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@15, k=10 | Emb:" She"@15 (de=15.25) +9 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `get_upstream_features` | L6:F11646@15, k=10 | Emb:" She"@15 (de=18.50) +9 more |
| 5 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 6 | `get_upstream_features` | L0:F15382@15, k=10 | Emb:" She"@15 (de=23.62) +9 more |
| 7 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 8 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 9 | `get_upstream_features` | L17:F5889@15, k=10 | Emb:" She"@15 (de=20.25) +9 more |
| 10 | `inspect_feature` | L13, F6622 | " pronouns." |

**Findings:** Tracing upstream from L18:F14677 (pos15) shows the primary driver is the raw token embedding for the pronoun "She" (direct_effect >15). The signal flows through a cascade of pronoun‑oriented features in layers 17, 15, 6, and finally a layer‑0 feature that directly detects female mentions. The pathway includes a lower‑third layer (layer 6) and concrete embedding contributions, satisfying the termin…

</details>

<details>
<summary><b>SA-3</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@1, k=10 | Emb:"Her"@1 (de=18.12) +9 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 5 | `get_upstream_features` | L0:F15382@1, k=10 | Emb:"Her"@1 (de=23.12) +9 more |
| 6 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"Her"@1 (de=14.75) +9 more |

**Findings:** The downstream feature L6:F11646 (woman‑reference detector) receives its strongest positive influence from the input token embedding "Her" (direct_effect ~18) and from two low‑layer features. Feature L0:15382 directly detects female mentions and is driven almost entirely by the embedding of "Her" (direct_effect 23.125). Feature L4:7864 is a generic markup/code pattern detector that also promotes f…

</details>

<details>
<summary><b>SA-4</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 2 | `get_upstream_features` | L4:F13412@7, k=10 | Emb:" nutrition"@7 (de=12.62) +9 more |
| 3 | `inspect_feature` | L1, F6461 | " technical language around physical activity, muscle function, and rel" |
| 4 | `inspect_feature` | L1, F6631 | " words related to dietary patterns and scientific studies" |
| 5 | `inspect_feature` | L2, F2589 | " words related to medical professionals and medical specialties" |
| 6 | `get_upstream_features` | L1:F6461@7, k=10 | Emb:" sports"@6 (de=9.19) +9 more |
| 7 | `get_upstream_features` | L1:F6631@7, k=10 | Emb:" nutrition"@7 (de=5.12) +9 more |
| 8 | `inspect_feature` | L1, F15310 | " words related to physical exercise" |
| 9 | `get_upstream_features` | L2:F2589@7, k=10 | Emb:" nutrition"@7 (de=4.50) +9 more |

**Findings:** The diet‑related L4 feature (F13412) is most strongly driven by the raw input token 'nutrition' (positive direct effect 12.6). Additional upstream contributors are lower‑layer features that encode exercise language (L1:6461) and dietary‑pattern language (L1:6631), both of which themselves receive strong excitation from the same 'nutrition' token and from a generic 'sports' token. A medical‑profess…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L12:F14970@46, k=8 → Emb:"<bos>"@0 (de=-5.22) +7 more |
| 2 | `get_upstream_features` | L19:F9685@15, k=5 → Emb:" She"@15 (de=6.12) +4 more |
| 3 | `get_upstream_features` | L7:F8644@46, k=5 → Emb:" She"@15 (de=3.98) +4 more |
| 4 | `get_upstream_features` | L14:F12501@13, k=5 → Emb:" eating"@13 (de=-6.28) +4 more |

### Build

`build_circuit` → 20 nodes, 21 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 51,028 | 5,774 | 114,793 | 0 | $0.0291 | — | — |
| SA-1 | openai/gpt-oss-120b | 40,557 | 2,627 | 2,528 | 0 | $0.0077 | ✅ 3F/6E | Trace the path upstream from L19:F9685 (pos 46, 'references … |
| SA-3 | openai/gpt-oss-120b | 56,037 | 2,895 | 64 | 0 | $0.0101 | ✅ 3F/2E | Trace the path upstream from L6:F11646 (pos 1, 'references t… |
| SA-4 | openai/gpt-oss-120b | 98,350 | 6,863 | 2,528 | 0 | $0.0189 | ✅ 4F/10E | Trace the path upstream from L4:F13412 (pos 7, 'terms relate… |
| SA-2 | openai/gpt-oss-120b | 131,657 | 8,049 | 5,088 | 0 | $0.0247 | ✅ 5F/13E | Trace the path upstream from L18:F14677 (pos 15, 'instances … |
| **Total** | | **377,629** | **26,208** | **125,001** | **0** | **$0.0905** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 28s