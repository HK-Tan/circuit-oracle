# Circuit Oracle Report
**Date:** 2026-07-28 07:20:27 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The profession-classification probe is driven almost entirely by female-gender/female-pronoun features rooted in the input token "She" and female-associated name/possessive features on "Sarah", with no genuine profession (nutrition, dietitian, RD) signal in the top contributors.

**Confidence:** 9

**Reasoning:** Every top positive driver in `get_top_features` is a gender-marking feature, not a profession indicator. The strongest contributors are:
- **L18:F14677** (frac_nonzero 0.012) — labeled "instances of women or girls being mentioned", promoted tokens `▁she`, `▁her`, `▁herself`. It fires at pos 1 ("She", activation 29.9), pos 12 ("Sarah", activation 18.3), and pos 34 ("Sarah", activation 23.8).
- **L6:F11646** (frac_nonzero 0.020) — "references to women, triggered by pronouns and titles", promotes `▁she`/`▁her`. Direct effect 0.375 at pos 1.
- **L12:F12940** (frac_nonzero 0.007) — "references to female pronouns and possessive pronouns", promotes `▁herself`, suppresses `▁himself`. Direct effect 0.252.
- **L4:F7864** (frac_nonzero 0.015) — although autointerp labels it "xml/source code", its actual promoted tokens are `▁herself`, `▁she`, `▁shes` — it acts as a female-pronoun amplifier.
- **L4:F15317** — "named entities like characters or people", promoted tokens `▁she`, `▁her`, `▁herself`.
- **L5:F16213** — "proper nouns consisting of a first and last name", promoted tokens `▁she`, `▁her`, `▁actress`.

The trace reaches the embedding layer cleanly: the **"She" embedding at pos 1** directly excites L6:F11646 (direct_effect 19.25), L4:F7864 (24.6), and L0:F15382 (a "mentions of a female person" feature, 16.9). The **"Sarah" embeddings at pos 12 and pos 34** feed L7:F2765 and L7:F8644 (a "woman's name" feature, though note F8644 actually *suppresses* the female-pronoun direction with promoted `▁himself` — net it slightly pulls the circuit toward male association, but the cumulative female signal dominates). The **"her" embedding at pos 4** also feeds L18:F14677 directly (direct_effect 3.08 at pos 12 upstream).

Critically, the strongest single-edge input is the "She" token embedding → L18:F14677 (direct_effect 27.1), which alone exceeds the combined magnitude of any nutrition/profession-related features that may exist at higher layers. No feature in the top 20 with positive direct effect encodes "nutrition", "dietitian", "dietetics", "food", "health", "recipes", or any RD/professional identity concept. The user's concern is corroborated: the probe classification is carried by a chain **Emb:"She" → L0/L4/L5 female-entity features → L6 female-pronoun feature → L12 female-pronoun aggregator + L18 women/girls mention feature → probe logit**, with secondary "Sarah" name-based pathways converging on the same female-gender features. This is a textbook spurious-correlation circuit: the probe has learned to use the gendered surface form of the protagonist as its profession signal.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F-1](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/-1) | 1 | Emb: She (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/-1) |
| [L0:F-1](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/-1) | 2 | Emb: loves (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/-1) |
| [L0:F-1](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/-1) | 4 | Emb: her (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/-1) |
| [L0:F-1](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/-1) | 12 | Emb: Sarah (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/-1) |
| [L0:F-1](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/-1) | 34 | Emb: Sarah (pos 34) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/-1) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 1 | Low-layer female-entity detectors (L0-L5) | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Low-layer female-entity detectors (L0-L5) | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Low-layer female-entity detectors (L0-L5) |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L5:F16213](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16213) | 2 | Low-layer female-entity detectors (L0-L5) |  proper nouns consisting of a first and last name | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16213) |
| [L5:F10952](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) | 1 | Low-layer female-entity detectors (L0-L5) | third person pronouns in varying contexts | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Mid-layer female pronoun/possessive detector (L6) | references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Mid-layer female pronoun/possessive detector (L6) | references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 2 | Mid-layer female-associated name/possession features (L7) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 5 | Mid-layer female-associated name/possession features (L7) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 11 | Mid-layer female-associated name/possession features (L7) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 12 | Mid-layer female-associated name/possession features (L7) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 34 | Mid-layer female-associated name/possession features (L7) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 12 | Suppressing male-name feature (L7:F8644) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 34 | Suppressing male-name feature (L7:F8644) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Female pronoun/possessive aggregator (L12) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Late-layer women/girls mention feature (L18) | instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 12 | Late-layer women/girls mention feature (L18) | instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 34 | Late-layer women/girls mention feature (L18) | instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.375 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@1` | ✅ reported | 4 | 6 | Trace the strongest positive driver L18:F14677 at pos 1. What does it encode? Wh… |
| SA-2 | `L6:F11646@1` | ✅ reported | 5 | 7 | Trace L6:F11646 at pos 1 — this is a strong positive driver with high direct eff… |
| SA-3 | `L12:F12940@2` | ❌ error | — | — | Trace L12:F12940 at pos 2 — what does this feature detect? Does it encode nutrit… |
| SA-4 | `L4:F7864@1` | ❌ error | — | — | Trace L4:F7864 at pos 1. What does it encode? Is it a gender marker or professio… |

<details>
<summary><b>SA-1</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@1, k=10 | Emb:"She"@1 (de=27.12) +9 more |
| 3 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 4 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 5 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 6 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 7 | `inspect_feature` | L11, F9183 | " large empty spaces in the text" |
| 8 | `get_upstream_features` | L6:F11646@1, k=10 | Emb:"She"@1 (de=19.25) +9 more |
| 9 | `get_upstream_features` | L15:F851@1, k=10 | L12:F12493 (de=22.38) +9 more |

**Findings:** The target L18:F14677 encodes the presence of female references (pronouns like she/her). Its strongest positive driver is the raw token embedding for "She" (direct effect 27.1). The signal also propagates through lower‑layer features: L4:F7864 (code/snippet detector that still promotes female pronouns) and L6:F11646 (explicit female‑reference detector), both of which themselves receive strong exci…

</details>

<details>
<summary><b>SA-2</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@1, k=10 | Emb:"She"@1 (de=19.25) +9 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 5 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 6 | `get_upstream_features` | L5:F10952@1, k=10 | Emb:"She"@1 (de=8.56) +9 more |
| 7 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 8 | `get_upstream_features` | L0:F15382@1, k=10 | Emb:"She"@1 (de=16.88) +9 more |
| 9 | `inspect_feature` | L4, F15688 | " sentences that contain the word "she" and words associated with confl" |

**Findings:** Tracing from L6:F11646 reveals a cascade centered on female‑pronoun detection. The top driver is the raw embedding for the token "She" (pos 1), which directly excites L6:F11646 (direct_effect ≈ 19). Downstream, L6:F11646 encodes references to women (female pronouns/titles). Its strongest positive upstream contributors are: (1) a low‑layer, highly specific female‑person detector (L0:F15382) also dr…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×2 | L12:12940, L4:7864 |
| 2 | `get_upstream_features` | L12:F12940@2, k=10 → Emb:"She"@1 (de=5.31) +9 more |
| 3 | `get_upstream_features` | L7:F8644@12, k=8 → Emb:"She"@1 (de=8.25) +7 more |
| 4 | `inspect_feature` ×3 | L7:8644, L4:15317, L5:16213 |
| 5 | `get_upstream_features` | L18:F14677@34, k=8 → Emb:" Sarah"@34 (de=5.69) +7 more |
| 6 | `get_upstream_features` | L12:F12940@2, k=5 → Emb:"She"@1 (de=5.31) +4 more |
| 7 | `get_upstream_features` | L18:F14677@12, k=5 → Emb:" Sarah"@12 (de=7.00) +4 more |

### Build

`build_circuit` → 12 nodes, 16 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 16,646 | 4,087 | 89,522 | 0 | $0.0153 | — | — |
| SA-2 | openai/gpt-oss-120b | 91,262 | 5,669 | 5,696 | 0 | $0.0172 | ✅ 5F/7E | Trace L6:F11646 at pos 1 — this is a strong positive driver … |
| SA-1 | openai/gpt-oss-120b | 106,581 | 4,149 | 5,088 | 0 | $0.0186 | ✅ 4F/6E | Trace the strongest positive driver L18:F14677 at pos 1. Wha… |
| **Total** | | **214,489** | **13,905** | **100,306** | **0** | **$0.0510** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 8s