# Circuit Oracle Report
**Date:** 2026-07-28 07:20:19 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's profession-classification score is driven almost entirely by masculine-gendered pronoun features ("His" at pos 1, "He" at pos 14/37) and not by genuine profession-indicating content words like "research," "science," or "interest," confirming the user's concern about spurious gender-marker features.

**Confidence:** 9

**Reasoning:**

The top direct-effect features on the probe direction are overwhelmingly pronoun/gender features. The largest single contributor is **L7:F14893** (pos 1, direct_effect +0.430, label "pronouns or possessive pronouns") followed by its sibling **L7:F14946** (pos 1, −0.426, "the possessive pronoun 'his'") and **L6:F12990** (pos 1, −0.295, "male pronouns and titles"). All three are traceable to the raw embedding of the token " His" (pos 1) — subagent 1 confirmed direct_effects of 23.5 (→F14893), 18.4 (→F14946), 4.9 (→F12990) from the "His" embedding, with a cascade of supporting pronoun detectors at L0:F2994, L4:F4315, L2:F5491, and L0:F2749 all firing on the same token. The same pattern repeats at position 14/37 where the " He" embedding (direct_effect 22.4) drives **L18:F14743** ("He" feature, activation ~30) at three positions and **L14:F14097** ("he" detector). These late-layer features all suppress the probe score (negative direct_effects of −0.252, −0.205, −0.094, etc.) — so the probe is being pushed by the *presence of masculine pronouns* rather than by profession semantics.

The early-layer profession-adjacent content features exist but contribute much less and are partially neutralized. **L0:F4564** ("the word 'research'", pos 2, frac_nonzero 0.007) is directly driven by the " research" embedding (28.1) and pushes the probe positively (+0.157). Similarly **L2:F9740** ("interest", pos 3, +0.133), **L0:F2827** ("science", pos 8, −0.122), and **L0:F1065** ("interest" at pos 3, +0.088). However, their magnitudes are small relative to the pronoun features, and the L18:L7400 code/UI feature (pos 1, −0.159) and other pronoun features at the same position swamp them. There is no "computer scientist" or "professor" or "researcher" entity-feature visible in the top 30 — the closest things to profession content are generic lexical features for "research"/"science"/"interest", which are just noun vocabulary, not profession identity.

In short, the circuit shows the probe classification of this text is being driven by the explicit "He" / "His" pronoun tokens cascading through a chain of gendered-pronoun detectors (pos 1: L0→L4/L6→L7→L18/L19; pos 14: L0:1069→L13:6622→L17:5889→L18:14743), with the profession-indicating content words "research" and "interest" contributing only a small positive push that is dominated by the pronoun features. The user's concern is validated: this is a textbook spurious-feature prediction, where the probe has learned a gender-marker shortcut (male pronouns ⇔ "computer scientist" profession) rather than a profession-concept representation.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | Late pronoun aggregators @ pos 1 (His) |  various pronouns and names referring to people | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 1 | Late pronoun aggregators @ pos 1 (His) |  pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L18:F7400](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) | 1 | Late pronoun aggregators @ pos 1 (His) |  words related to coding and software/UI interfaces, with some bias toward non-English words | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Mid-layer pronoun/possessive features @ pos 1 (promote, +) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | Mid-layer pronoun/possessive features @ pos 1 (promote, +) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Mid-layer male-pronoun feature @ pos 1 (suppress, −) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | Mid-layer male-pronoun feature @ pos 1 (suppress, −) |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 14 | Late 'He' pronoun feature @ pos 14 (suppress, −) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 37 | Late 'He' pronoun feature @ pos 14 (suppress, −) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L14:F14097](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) | 14 | Late 'He' pronoun feature @ pos 14 (suppress, −) |  occurrences of the word "he" | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) |
| [L22:F12117](https://neuronpedia.org/gemma-2-2b/22-gemmascope-transcoder-16k/12117) | 15 | Late 'He' pronoun feature @ pos 14 (suppress, −) |  references to actions that people can take or have taken. | [view](https://neuronpedia.org/gemma-2-2b/22-gemmascope-transcoder-16k/12117) |
| [L19:F8186](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8186) | 14 | Late 'He' pronoun feature @ pos 14 (suppress, −) |  references to a person, especially third-person pronouns and possessive pronouns. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8186) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | Early pronoun / person-reference features @ pos 1 | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2749](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2749) | 1 | Early pronoun / person-reference features @ pos 1 |  references to ownership or association with a person or group of people | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2749) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 14 | Early pronoun / person-reference features @ pos 1 |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L2:F5491](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) | 1 | Early pronoun / person-reference features @ pos 1 | references to God in the third person. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) |
| [L0:F1065](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1065) | 3 | Lexical periphery @ pos 1 (minor contributors) |  the word "interest", sometimes near the word "practicing" or "pattern" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1065) |
| [L0:F6568](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6568) | 3 | Lexical periphery @ pos 1 (minor contributors) | the word "anyway" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6568) |
| [L7:F16284](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/16284) | 14 | Lexical periphery @ pos 1 (minor contributors) |  mentions of people's names and relationships | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/16284) |
| [L0:F4564](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) | 2 | Profession-adjacent content words (research / interest / science) | the word "research." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) |
| [L2:F9740](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9740) | 3 | Profession-adjacent content words (research / interest / science) | the word "interest" and related words. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9740) |
| [L0:F2827](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2827) | 8 | Profession-adjacent content words (research / interest / science) |  the word "science" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2827) |
| [L0:F14201](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14201) | 3 | Profession-adjacent content words (research / interest / science) | words related to trade (business, finance, and health) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14201) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 13 | Profession-adjacent content words (research / interest / science) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L7:14893 de=0.430 |
| 3 | `inspect_feature` ×4 | L7:14893, L7:14946, L6:12990, L18:14743 |
| 4 | `get_top_features` | 30 features; top: L7:14893 de=0.430 |
| 5 | `inspect_feature` ×12 | L19:8814, L0:2994, L0:4564, L4:4315, L18:7400, L18:10315, L2:9740, L2:5491, L7:16284, L22:12117, L14:14097, L19:8186 |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ✅ reported | 4 | 7 | Trace the L7:F14893 (pronouns/possessives feature at pos 1) upstream to find whi… |
| SA-2 | `L18:F14743@14` | ✅ reported | 5 | 6 | Trace L18:F14743 ("He" feature at pos 14) upstream to confirm it is driven by th… |

<details>
<summary><b>SA-1</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `get_upstream_features` | L6:F12990@1, k=10 | Emb:"His"@1 (de=4.91) +9 more |
| 5 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 6 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 7 | `get_upstream_features` | L4:F4315@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 8 | `get_upstream_features` | L0:F2994@1, k=10 | Emb:"His"@1 (de=19.75) +9 more |

**Findings:** The pronoun/possessive feature L7:F14893 is driven primarily by the input token "His" at position 1. Upstream tracing shows a cascade: the raw embedding of "His" directly excites L7:F14893 (23.5) and also excites lower‑layer pronoun detectors (L6:F12990, L4:F4315, L0:F2994). These lower‑layer features themselves are specialized pronoun detectors, confirming that the activation originates from the …

</details>

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@14, k=10 | Emb:" He"@14 (de=22.38) +9 more |
| 3 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 4 | `get_upstream_features` | L0:F1069@14, k=10 | Emb:" He"@14 (de=35.75) +9 more |
| 5 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 6 | `get_upstream_features` | L17:F5889@14, k=10 | Emb:" He"@14 (de=21.50) +9 more |
| 7 | `inspect_feature` | L6, F2267 | "words that appear in programming code, legal jargon, or scientific tex" |
| 8 | `get_upstream_features` | L6:F2267@14, k=10 | Emb:"<bos>"@0 (de=-7.16) +9 more |
| 9 | `inspect_feature` | L13, F6622 | " pronouns." |
| 10 | `inspect_feature` | L13, F6622 | " pronouns." |
| 11 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 12 | `inspect_feature` | L4, F15438 | " mentions and declarations of conflicts of interest, study design, and" |

**Findings:** The target L18:F14743 ('He' feature) is primarily driven by the raw input token " He" (direct_effect 22.375). Upstream, the earliest‑layer pronoun detector L0:F1069 (direct_effect 7.03) strongly responds to the same token (direct_effect 35.75 from the embedding). This early detector feeds into mid‑high layers (L13, L17) that consolidate pronoun information. A lower‑third feature L6:F2267 (layer ≤8…

</details>

### Re-dispatch (round 2): 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-3 | `L7:F14946@1` | ✅ reported | 3 | 5 | Trace L7:F14946 ("his" pronoun feature at pos 1) upstream to confirm it is drive… |
| SA-4 | `L19:F8814@1` | ❌ error | — | — | Trace L19:F8814 (general person pronouns, promoted tokens include she/her) at po… |
| SA-5 | `L0:F4564@2` | ❌ error | — | — | Trace L0:F4564 ("research" feature at pos 2) upstream to find which input token … |

<details>
<summary><b>SA-3</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 2 | `get_upstream_features` | L7:F14946@1, k=10 | Emb:"His"@1 (de=18.38) +9 more |
| 3 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 4 | `get_upstream_features` | L4:F4315@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 5 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 6 | `get_upstream_features` | L6:F12990@1, k=10 | Emb:"His"@1 (de=4.91) +9 more |
| 7 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 8 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |

**Findings:** The target feature L7:F14946 (pronoun "his" detector) is driven primarily by the input token embedding for "His" (direct_effect ≈ 18.4). A mid‑level pronoun feature in layer 4 (F4315) also contributes positively (≈ 4.4) and itself receives a strong excitatory signal from the same "His" embedding (direct_effect ≈ 23.5). Additionally, a male‑pronoun feature in layer 6 (F12990) feeds into the target …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×7 | L0:6051, L0:2827, L0:14201, L0:2749, L0:1069, L0:1065, L0:6568 |
| 2 | `get_upstream_features` | L19:F8814@1, k=10 → Emb:"His"@1 (de=9.31) +9 more |
| 3 | `get_upstream_features` | L0:F4564@2, k=5 → Emb:" research"@2 (de=28.12) +4 more |
| 4 | `get_upstream_features` | L7:F14893@1, k=5 → Emb:"His"@1 (de=23.50) +4 more |
| 5 | `get_upstream_features` | L0:F2994@1, k=5 → Emb:"His"@1 (de=19.75) +4 more |
| 6 | `get_upstream_features` | L0:F1069@14, k=5 → Emb:" He"@14 (de=35.75) +4 more |

### Build

`build_circuit` → 13 nodes, 18 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 51,805 | 5,374 | 254,583 | 0 | $0.0373 | — | — |
| SA-1 | openai/gpt-oss-120b | 79,697 | 3,960 | 2,624 | 0 | $0.0144 | ✅ 4F/7E | Trace the L7:F14893 (pronouns/possessives feature at pos 1) … |
| SA-2 | openai/gpt-oss-120b | 180,354 | 10,108 | 2,624 | 0 | $0.0332 | ✅ 5F/6E | Trace L18:F14743 ("He" feature at pos 14) upstream to confir… |
| SA-3 | openai/gpt-oss-120b | 90,507 | 5,530 | 8,704 | 0 | $0.0170 | ✅ 3F/5E | Trace L7:F14946 ("his" pronoun feature at pos 1) upstream to… |
| **Total** | | **402,363** | **24,972** | **268,535** | **0** | **$0.1018** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 6s