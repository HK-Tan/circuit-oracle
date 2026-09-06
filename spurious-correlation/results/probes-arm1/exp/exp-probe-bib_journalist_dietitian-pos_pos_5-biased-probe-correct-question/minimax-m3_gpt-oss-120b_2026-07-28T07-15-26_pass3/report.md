# Circuit Oracle Report
**Date:** 2026-07-28 07:15:26 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by a chain of features that detect **feminine pronouns and the female name "Heather"** — not by profession-related content like "nutrition," "dietetics," or "sports" — confirming the user's concern that the circuit uses spurious gender markers.

**Confidence:** 8

**Reasoning:** Every layer in the circuit encodes gender, not profession. The signal originates at embedding nodes for `Her` (pos 1, direct_effect up to +6.5), ` She` (pos 15, direct_effect up to +15.25), and ` Heather` (pos 46, direct_effect up to +6.5). These feed L0 detectors (F15382, F7532) → L4-L7 features like **L6:F11646 "references to women, potentially triggered by pronouns and titles"** (frac_nonzero 0.020, fired on `Her` at pos 1 and `She` at pos 15 with direct_effects 0.283 and 0.203), **L7:F8644 "woman's name in a variety of contexts"** (fired on `Heather` at pos 46, direct_effect −0.21 — note this is an *inhibitory* contribution), **L6:F16329 "female first names and their possessive forms"** (suppresses `himself`, `his`; fires on the feminine-pronoun positions), and **L5:F5996 "words associated with females, femininity or womanhood"**. These converge on **L14:F12501 "uses of the feminine pronoun"** and **L12:F14970 "names of people"** (fired on `Heather`), which in turn feed the late-layer drivers **L18:F14677 "instances of women or girls being mentioned"** (pos 15 and pos 46, combined direct_effect ~0.27, promoted `herself`/`she`/`her` and suppresses `himself`/`his`) and **L19:F9685 "references to women's names and their roles or accomplishments"** (pos 15 and 46, direct_effect ~0.13 each). Crucially, the top embedding contributors are pronouns and a name — never domain words. The content words ` sports` (pos 6) and ` areas` (pos 2) actually *inhibit* the L18 women-mentioned feature (direct_effects −1.88, −1.81), as does the ` Her` token via the L7:F8644 path in the opposite direction. The only profession-adjacent tokens (` nutrition`, ` disordered`) show up as minor positive or negative embedding contributions but do not feed any "dietitian/nutritionist" feature. The circuit thus encodes "this text is about a named woman" — a spurious correlate of the profession (the training set's dietitians happened to be women) — rather than any genuine nutritional/dietetic profession indicator. This is a textbook confound: the probe is essentially doing gender classification, not profession classification.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 15 | Early-layer token detectors (L0-L2) recognizing feminine pronouns & female name | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 46 | Early-layer token detectors (L0-L2) recognizing feminine pronouns & female name | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Mid-layer features: 'references to women / female names' (L4-L7) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 15 | Mid-layer features: 'references to women / female names' (L4-L7) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 46 | Mid-layer features: 'references to women / female names' (L4-L7) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 15 | Mid-layer features: 'references to women / female names' (L4-L7) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L5:F5996](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5996) | 46 | Mid-layer features: 'references to women / female names' (L4-L7) |  words associated with females, femininity or womanhood | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5996) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 46 | Mid-layer features: 'references to women / female names' (L4-L7) | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 46 | Name/identity features (L7-L12) |  names of people, both first and last names | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 46 | Name/identity features (L7-L12) |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L14:F12501](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) | 13 | L14: 'uses of the feminine pronoun' |  uses of the feminine pronoun. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 15 | L18-L19: 'instances of women / women's names and roles' |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 46 | L18-L19: 'instances of women / women's names and roles' |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 46 | L18-L19: 'instances of women / women's names and roles' |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 15 | L18-L19: 'instances of women / women's names and roles' |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L18:F9023](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/9023) | 46 | L18-L19: 'instances of women / women's names and roles' |  personal names and associated titles | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/9023) |
| [L18:F10572](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10572) | 46 | L18-L19: 'instances of women / women's names and roles' |  proper nouns, especially names of people and characters | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10572) |
| [L16:F6025](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6025) | 46 | L18-L19: 'instances of women / women's names and roles' |  capitalized first names, sometimes followed by last names | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6025) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.283 |
| 3 | `inspect_feature` ×4 | L6:11646, L7:8644, L18:14677, L12:14970 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@15` | ❌ error | — | — |  |
| SA-2 | `L12:F14970@46` | ❌ error | — | — |  |
| SA-3 | `L4:F13412@7` | ❌ error | — | — |  |
| SA-4 | `L0:F6051@14` | ❌ error | — | — |  |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14677@15, k=10 → Emb:" She"@15 (de=15.25) +9 more |
| 2 | `get_upstream_features` | L12:F14970@46, k=10 → Emb:"<bos>"@0 (de=-5.22) +9 more |
| 3 | `get_upstream_features` | L4:F13412@7, k=10 → Emb:" nutrition"@7 (de=12.62) +9 more |
| 4 | `inspect_feature` ×9 | L4:1276, L4:7864, L6:16329, L7:2765, L0:10148, L0:5686, L19:9685, L5:5996, L14:12501 |
| 5 | `get_upstream_features` | L19:F9685@46, k=10 → Emb:" Heather"@46 (de=4.62) +9 more |
| 6 | `get_upstream_features` | L18:F14677@46, k=10 → Emb:"Her"@1 (de=6.16) +9 more |
| 7 | `inspect_feature` ×3 | L16:6025, L18:9023, L18:10572 |
| 8 | `get_upstream_features` | L14:F12501@13, k=10 → Emb:" eating"@13 (de=-6.28) +9 more |

### Build

`build_circuit` → 11 nodes, 10 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 45,402 | 3,922 | 129,823 | 0 | $0.0261 | — | — |
| **Total** | | **45,402** | **3,922** | **129,823** | **0** | **$0.0261** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 7s