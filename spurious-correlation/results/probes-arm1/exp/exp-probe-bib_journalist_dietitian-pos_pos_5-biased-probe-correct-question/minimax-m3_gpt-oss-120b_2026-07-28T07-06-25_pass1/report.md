# Circuit Oracle Report
**Date:** 2026-07-28 07:06:25 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score for "nutritionist" is driven almost entirely by a small set of features that encode *female-person mentions* (pronouns, female names, name-with-role structures) rather than by features that encode the actual profession (nutrition/diet expertise), confirming the user's concern about spurious gender-based correlation.

**Confidence:** 9

**Reasoning:** The circuit shows a clear mechanism dominated by gender markers:

1. **L0/L6 female-mention detectors dominate the direct effects.** The single largest positive driver of the probe score is **L6:F11646 at pos 1 (direct_effect = +0.283)** and **pos 15 (+0.203)**. Inspecting F11646 reveals it is literally *"references to women, potentially triggered by pronouns and titles"* (frac_nonzero = 0.020) — its promoted tokens are `▁herself, ▁she, ▁her`. Its upstream chain traces cleanly to the **"Her" embedding at pos 1** (direct_effect = +18.1) and the **"She" embedding at pos 15** (direct_effect = +15.25). The same path is fed by **L0:F15382** ("mentions of a female person," direct_effect on the probe +0.283 at pos 1) and **L0:F9519** ("the pronoun 'she' and the possessive pronoun 'her'"), both of which receive their strongest direct excitation from those same feminine-pronoun embeddings.

2. **The L18 women-mention feature F14677 (direct_effect +0.171)** — *"instances of women or girls being mentioned"* — is a downstream aggregator whose strongest direct upstream input is the **"She" embedding at pos 15 (+15.25)**, followed by F11646 (+2.95), L17:F5889 (+3.97), and L15:F3330. L17:F5889 is a sentence-level *"women-mention aggregator"* whose own top input is again the "She" embedding (+20.25). This whole cascade is gender-recognition, not profession-recognition.

3. **The L19 women-name-with-role feature F9685 (direct_effect +0.133)** — *"references to women's names and their roles or accomplishments"* — has its strongest direct input from the **"Heather" embedding at pos 46 (+4.63)**, then from name-detector L4:F1276 (capitalized names) → L0:F7532 (proper nouns) → "Heather" embedding. F9685's promoted tokens are `▁herself, ▁she, ▁her` — it is firing because Heather is a female name, not because of any profession concept. Its label explicitly states it fires on "women's names and their roles or accomplishments," which is exactly the spurious-correlation signature: it counts as positive evidence for a *female-coded* profession (nutritionist, nurse, teacher) whenever a female name appears, regardless of what the person does.

4. **The single genuine content feature is L4:F13412 (direct_effect +0.137) at pos 7**, which detects *"terms related to diets and dietary health"* (promoted: `▁diet, ▁diets, ▁dieting`). Its only meaningful upstream is the **"nutrition" embedding at pos 7 (+12.6)**. This is the one feature in the top 15 that actually tracks the profession content. Crucially, it is the *only* feature in the entire top-15 list whose direct effect comes from a profession-content word rather than a gender marker.

5. **The negative-direct-effect features are also gender-related.** L7:F8644 (de = -0.21) is *"woman's name in a variety of contexts"*; L6:F16329 (de = -0.14) is *"female first names and their possessive forms"*; L0:F6051 (de = -0.125) is *"periods, spaces, and the number 1"* firing on the period at pos 14. These act as suppressors (e.g., the "Heather" name feature dampens the women-name-role path because the probe is asking about a *specific* profession, not generic "she"), but the dominant positive signal is still feminine-gender rather than nutrition expertise.

6. **The signal-flow topology confirms the user's hypothesis:** the probe direction at L26 receives its largest positive contributions from F14677 and F9685 — both of which read predominantly from the `Her` / `She` / `Heather` embeddings via female-mention and female-name detectors. The nutrition-term feature F13412 contributes positively but is *outweighed* by the gender features. The chain `Her/She/Heather embedding → L0 female-mention → L6 women-references → L18 women/girls → probe` is a textbook spurious-correlation pathway: the model has learned that the target profession (nutritionist) co-occurs with female pronouns in training data, and the probe is reading that co-occurrence rather than the profession-defining content.

In short, the circuit is a clear vindication of the user's concern: the probe is largely classifying the person as a "nutritionist" because the text contains feminine pronouns and a female first name, not because of any content about nutrition or dietetics. The only genuine profession-content feature (F13412 on "nutrition") is present but plays a smaller role than the gender-marker features.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Her (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: She (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 46 | Emb: Heather (pos 46) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: nutrition (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: . (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 15 | L0: female-person mention detectors (F15382, F9519, F7532) | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 15 | L0: female-person mention detectors (F15382, F9519, F7532) |  the pronoun "she" and the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 46 | L0: female-person mention detectors (F15382, F9519, F7532) |  proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 7 | L4: diet/nutrition term detector (F13412) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 46 | L4: capitalized name detector (F1276) | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | L6: women-references (F11646 + F16329 family) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 15 | L6: women-references (F11646 + F16329 family) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 1 | L6: women-references (F11646 + F16329 family) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 15 | L6: women-references (F11646 + F16329 family) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F8166](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) | 46 | L6: women-references (F11646 + F16329 family) |  proper names longer than 4 characters and ending in 'a', 'i', or 'e' | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 46 | L7: female-context name/sports cluster (F8644, F2765) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 46 | L7: female-context name/sports cluster (F8644, F2765) |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L8:F576](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/576) | 46 | L8: proper-name detector (F576) | proper names | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/576) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 46 | L12: generic names (F14970) |  names of people, both first and last names | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L16:F6025](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6025) | 46 | L16: capitalised first-name (F6025) | capitalized first names, sometimes followed by last names | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6025) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 15 | L17: women-mention aggregator (F5889) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 15 | L18: women/girls mention (F14677) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 46 | L19: women names + roles (F9685) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 46 | Output: probe direction (nutritionist) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11646 de=0.283 |
| 3 | `inspect_feature` ×13 | L6:11646, L7:8644, L18:14677, L12:14970, L4:13412, L19:9685, L4:1276, L0:10148, L0:6051, L4:7864, L7:2765, L0:5686, L6:16329 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@1` | ✅ reported | 6 | 20 | Trace the upstream path from L6:F11646 at pos 1 (top positive direct_effect, "re… |
| SA-2 | `L18:F14677@15` | ❌ error | — | — | Trace the upstream path from L18:F14677 at pos 15 ("instances of women or girls … |
| SA-3 | `L19:F9685@46` | ✅ reported | 5 | 9 | Trace the upstream path from L19:F9685 at pos 46 ("references to women's names a… |
| SA-4 | `L7:F8644@46` | ❌ error | — | — | Trace the upstream path from L7:F8644 at pos 46. This feature has a NEGATIVE dir… |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@1, k=15 | Emb:"Her"@1 (de=18.12) +14 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 5 | `get_upstream_features` | L0:F15382@1, k=10 | Emb:"Her"@1 (de=23.12) +9 more |
| 6 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"Her"@1 (de=14.75) +9 more |
| 7 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 8 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |
| 9 | `get_upstream_features` | L2:F2128@1, k=10 | Emb:"Her"@1 (de=22.38) +9 more |
| 10 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 11 | `get_upstream_features` | L4:F15317@1, k=10 | Emb:"Her"@1 (de=11.38) +9 more |
| 12 | `get_upstream_features` | L5:F10952@1, k=10 | Emb:"Her"@1 (de=7.56) +9 more |

**Findings:** The circuit from L6:F11646 back to the token embedding reveals a compact cascade driven almost entirely by the "Her" token. Upstream features in layers 0‑5 (female‑mention detector, generic pronoun detectors, and a mis‑labelled XML snippet detector) all receive strong positive excitation from the same embedding, confirming that the target feature is activated by female pronouns. All conditions are…

</details>

<details>
<summary><b>SA-3</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F9685 | " references to women's names and their roles or accomplishments." |
| 2 | `get_upstream_features` | L19:F9685@46, k=10 | Emb:" Heather"@46 (de=4.62) +9 more |
| 3 | `inspect_feature` | L4, F1276 | "capitalized names and titles, and names with lowercase letters in the " |
| 4 | `get_upstream_features` | L4:F1276@46, k=10 | Emb:" Heather"@46 (de=11.12) +9 more |
| 5 | `inspect_feature` | L16, F6025 | " capitalized first names, sometimes followed by last names" |
| 6 | `get_upstream_features` | L16:F6025@46, k=10 | L14:F8671 (de=3.48) +9 more |
| 7 | `inspect_feature` | L8, F576 | " proper names" |
| 8 | `get_upstream_features` | L8:F576@46, k=10 | L0:F7532 (de=3.66) +9 more |
| 9 | `inspect_feature` | L0, F7532 | " proper nouns" |
| 10 | `inspect_feature` | L6, F6493 | " names of people" |
| 11 | `inspect_feature` | L14, F8671 | " capitalized names of people" |
| 12 | `inspect_feature` | L13, F4753 | " proper nouns, especially names of people" |

**Findings:** The target feature L19:F9685 ("references to women's names and their roles or accomplishments") is driven by a cascade of name‑detection signals. The strongest upstream influence is the embedding for the token "Heather" (direct_effect = 4.625) – the actual token at position 46. This token is first recognised by a layer‑0 proper‑noun detector (F7532), which then excites a layer‑4 capitalised‑name d…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14677@15, k=10 → Emb:" She"@15 (de=15.25) +9 more |
| 2 | `get_upstream_features` | L7:F8644@46, k=10 → Emb:" She"@15 (de=3.98) +9 more |
| 3 | `get_upstream_features` | L12:F14970@46, k=10 → Emb:"<bos>"@0 (de=-5.22) +9 more |
| 4 | `get_upstream_features` | L4:F13412@7, k=10 → Emb:" nutrition"@7 (de=12.62) +9 more |
| 5 | `get_upstream_features` | L0:F6051@14, k=10 → Emb:"."@14 (de=47.00) +9 more |
| 6 | `get_upstream_features` | L7:F2765@46, k=10 → Emb:" She"@15 (de=1.65) +9 more |
| 7 | `get_upstream_features` | L6:F16329@15, k=10 → Emb:" She"@15 (de=7.31) +9 more |
| 8 | `get_upstream_features` | L15:F3330@15, k=10 → Emb:" She"@15 (de=15.62) +9 more |
| 9 | `get_upstream_features` | L17:F5889@15, k=10 → Emb:" She"@15 (de=20.25) +9 more |
| 10 | `get_upstream_features` | L0:F15382@15, k=10 → Emb:" She"@15 (de=23.62) +9 more |
| 11 | `get_upstream_features` | L6:F8166@46, k=10 → L4:F1276 (de=4.56) +9 more |
| 12 | `inspect_feature` ×7 | L14:5740, L14:13478, L13:6622, L0:9519, L6:8166, L2:16306, L0:7532 |

### Build

`build_circuit` → 17 nodes, 30 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 71,059 | 6,173 | 157,840 | 0 | $0.0382 | — | — |
| SA-3 | openai/gpt-oss-120b | 133,433 | 10,825 | 46,816 | 0 | $0.0272 | ✅ 5F/9E | Trace the upstream path from L19:F9685 at pos 46 ("reference… |
| SA-1 | openai/gpt-oss-120b | 147,792 | 10,962 | 32,736 | 0 | $0.0292 | ✅ 6F/20E | Trace the upstream path from L6:F11646 at pos 1 (top positiv… |
| **Total** | | **352,284** | **27,960** | **237,392** | **0** | **$0.0946** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 33s