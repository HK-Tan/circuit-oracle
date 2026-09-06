# Circuit Oracle Report
**Date:** 2026-07-28 07:20:52 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_9 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity probe is driven primarily by *identity-group* features that fire on tokens like "white", "oriental", "guy", "married", "self hater", not by the model's reading of the slur-and-trope content of the sentence; signal flows from the bare embeddings of identity-related tokens through stacked race/ethnicity/gender-detector features (L0→L1→L2→L3→L4→L6) into the probe direction.

**Confidence:** 8

**Reasoning:** The top features driving the probe all encode identity categories rather than the prompt's actual harmful semantics ("hate", "lust", "self hater", the racial slur "oriental", or the implicit degradation). The largest positive contributions to the probe come from:

- **L6:F3902** ("terms referring to race and ethnicity", frac=0.018) firing at positions 9, 10, and 27 — driven directly by the embedding of " white" (pos 9) with direct_effect ≈ 13.6, plus parallel drive from " oriental" (pos 27, direct_effect 8.75). L4:F117 ("terms related to race, racism, social justice, with focus on Black people", frac=0.012) and L4:F14329 ("colors black/white", frac=0.007) upstream.
- **L3:F13061** ("words related to race, gender and social issues", frac=0.009) and **L3:F16373** ("demographic identity, especially race and gender", frac=0.006) at pos 10, both heavily excited by the " white" embedding (direct_effect 11 and 23.9 respectively).
- **L2:F13158** ("words about race and ethnicity", promoted tokens: ethnic, queer, LGBT, Hispanic, etc., frac=0.010), **L2:F15317** ("gendered words, especially female", frac=0.019), **L2:F9301** ("mentions of men and women in relationships/dating", frac=0.018), **L2:F10986** ("the word guys or guy", frac=0.010) — all generic identity/relationship detectors rather than toxicity detectors.
- **L6:F5671** ("references to people, with an emphasis on gender and family relations", frac=0.022) and **L6:F15948** ("words and entities referring to gender and pronouns", frac=0.206) at pos 10, driven by the "guy" embedding (direct_effect 9.6 / 5.0).
- **L4:F10004** at pos 22 ("self-hater" composition) does get a strong positive push from the "self" embedding (direct_effect 46.75) — this is the closest the circuit gets to encoding actual slur content, but its only downstream is the race/romance supernode, not a toxicity-specific feature.
- **L3:F8492** ("the word hate", frac=0.0005) at pos 22 contributes positively to the race/romance supernode but is gated by identity-context features.

The circuit's terminal probe-driving features are race/ethnicity and gender/relationship detectors; the actual hate/trope lexicon ("hater", "self hater", the slur "oriental", "lust after white men") only enters the circuit *as raw token embeddings* (oriental → L6:F3902 with direct_effect 8.75; self → L4:F10004 with direct_effect 46.75) and is absorbed into a generic identity-group feature, not into a feature that distinguishes hateful from benign mention of those groups. **The probe therefore relies on the *presence* of identity tokens (an "identity group" signal) rather than on the toxic framing that combines them — confirming the user's concern about spurious identity-based rather than content-based detection.** No probe-driving feature encodes slur deployment, dehumanization, or the "self-hater" trope directly; everything routes through "race detected" / "gender detected" / "relationship detected" abstractions.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F753](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/753) | 2 | Layer 0: low-level lexical (author / appears / white-color) | the word "author" and words related to selling and prices | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/753) |
| [L0:F241](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/241) | 6 | Layer 0: low-level lexical (author / appears / white-color) | mentions of marriage | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/241) |
| [L0:F1998](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1998) | 3 | Layer 0: low-level lexical (author / appears / white-color) |  occurrences of the word "seem" or "is" or "are." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1998) |
| [L0:F16013](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16013) | 9 | Layer 0: low-level lexical (author / appears / white-color) | mentions of the color blue, and perhaps colors in general or the components of a graphic image | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16013) |
| [L0:F10910](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) | 9 | Layer 0: low-level lexical (author / appears / white-color) | the word "possession" and the words "white", "immediate" and "once" regardless of context | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) |
| [L0:F3024](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3024) | 10 | Layer 0: low-level lexical (author / appears / white-color) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3024) |
| [L1:F384](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/384) | 2 | Layer 1: lexical white / author detectors | the string "ash" or "pund" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/384) |
| [L1:F5220](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5220) | 2 | Layer 1: lexical white / author detectors |  references to authors and publications | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5220) |
| [L1:F6576](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6576) | 3 | Layer 1: lexical white / author detectors |  the word "appearance" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6576) |
| [L1:F7821](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7821) | 9 | Layer 1: lexical white / author detectors | mentions of computer fans. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7821) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 9 | Layer 2: race / ethnicity / gender-relationship detectors | words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F15317](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15317) | 10 | Layer 2: race / ethnicity / gender-relationship detectors |  gendered words, with a slight bias toward female-gendered words | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15317) |
| [L2:F15558](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15558) | 6 | Layer 2: race / ethnicity / gender-relationship detectors | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15558) |
| [L2:F10986](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10986) | 10 | Layer 2: race / ethnicity / gender-relationship detectors | the word "guys" or "guy" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10986) |
| [L2:F9301](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) | 10 | Layer 2: race / ethnicity / gender-relationship detectors |  all mentions of men and women in the context of relationships, dating, or gendered social roles | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 10 | Layer 3: demographic-identity & hate-word detectors | words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L3:F16373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) | 10 | Layer 3: demographic-identity & hate-word detectors |  mentions of demographic identity, especially race and gender | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) |
| [L3:F4512](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4512) | 15 | Layer 3: demographic-identity & hate-word detectors | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4512) |
| [L3:F8492](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8492) | 22 | Layer 3: demographic-identity & hate-word detectors | the word "hate" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8492) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 10 | Layer 4: race/social-justice + romance/relationship detectors | terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F14329](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14329) | 9 | Layer 4: race/social-justice + romance/relationship detectors |  mentions of the colors black, white, or another color with "or" in its name | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14329) |
| [L4:F12975](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12975) | 27 | Layer 4: race/social-justice + romance/relationship detectors | mentions of Asian countries, calendars, and paganism/eastern religions | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12975) |
| [L4:F6128](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6128) | 10 | Layer 4: race/social-justice + romance/relationship detectors |  references to romantic relationships, affairs, and family dynamics | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6128) |
| [L4:F10004](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10004) | 22 | Layer 4: race/social-justice + romance/relationship detectors | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10004) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 9 | Layer 6: late race/ethnicity + gender/people detectors (probe drivers) | terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 10 | Layer 6: late race/ethnicity + gender/people detectors (probe drivers) | terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 27 | Layer 6: late race/ethnicity + gender/people detectors (probe drivers) | terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F5671](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5671) | 10 | Layer 6: late race/ethnicity + gender/people detectors (probe drivers) |  references to people, with an emphasis on gender and family relations. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5671) |
| [L6:F15948](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15948) | 10 | Layer 6: late race/ethnicity + gender/people detectors (probe drivers) |  words and entities referring to gender and pronouns | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15948) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L1:5220 de=-0.453 |

### Dispatch: 12 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L3:F13061@10` | ✅ reported | 6 | 6 | Trace this feature upstream to understand what it encodes. What tokens/concepts … |
| SA-2 | `L6:F3902@9` | ✅ reported | 6 | 11 | Trace this feature upstream. What does it encode and what input tokens drive it?… |
| SA-3 | `L4:F117@10` | ✅ reported | 5 | 5 | Trace this feature upstream. What does it encode and what input tokens drive it?… |
| SA-4 | `L3:F4512@15` | ❌ error | — | — | Trace this feature upstream. What does it encode and what input tokens drive it?… |
| SA-5 | `L1:F384@2` | ✅ reported | 4 | 4 | Trace this feature upstream. What does it encode? Reach embeddings. |
| SA-6 | `L1:F6576@3` | ✅ reported | 3 | 3 | Trace this feature upstream. What does it encode? Reach embeddings. |
| SA-7 | `L2:F13158@9` | ✅ reported | 5 | 6 | Trace this feature upstream. What does it encode? Reach embeddings. |
| SA-8 | `L4:F10004@22` | ❌ error | — | — | Trace this feature upstream. What does it encode? Reach embeddings. |
| SA-9 | `L2:F15558@6` | ❌ error | — | — | Trace this feature upstream. What does it encode? Reach embeddings. |
| SA-10 | `L3:F10286@4` | ❌ error | — | — | Trace this feature upstream. What does it encode? Reach embeddings. |
| SA-11 | `L0:F7773@3` | ❌ error | — | — | Trace this feature upstream. What does it encode? Reach embeddings. |
| SA-12 | `L6:F3902@27` | ❌ error | — | — | Trace this feature upstream. What does it encode? Reach embeddings. |

<details>
<summary><b>SA-1</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F13061 | " words related to race, gender and social issues" |
| 2 | `get_upstream_features` | L3:F13061@10, k=15 | Emb:" white"@9 (de=11.00) +14 more |
| 3 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 4 | `inspect_feature` | L2, F15317 | " gendered words, with a slight bias toward female-gendered words" |
| 5 | `inspect_feature` | L0, F9076 | " mentions of men, boys, areas, or general locations in a text" |
| 6 | `get_upstream_features` | L2:F13158@9, k=10 | Emb:" white"@9 (de=13.62) +9 more |
| 7 | `inspect_feature` | L1, F7821 | " mentions of computer fans." |
| 8 | `inspect_feature` | L2, F14965 | " words related to clothing and fabrics." |
| 9 | `inspect_feature` | L2, F1708 | " mentions of colors" |

**Findings:** The L3 feature 13061 (layer 3) aggregates signals about race, gender, and social‑issue terminology. Its strongest upstream driver is the input token embedding for the word "white", directly boosting the feature by 11.0. Below that, three mid‑level detectors contribute: a dedicated race/ethnicity detector (L2:F13158), a gendered‑word detector (L2:F15317), and an early‑layer masculine mention detect…

</details>

<details>
<summary><b>SA-2</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F3902 | " terms referring to race and ethnicity" |
| 2 | `get_upstream_features` | L6:F3902@9, k=10 | Emb:" white"@9 (de=13.56) +9 more |
| 3 | `inspect_feature` | L4, F117 | " terms related to race, racism, and social justice, with a particular " |
| 4 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 5 | `get_upstream_features` | L4:F117@9, k=10 | Emb:" white"@9 (de=15.06) +9 more |
| 6 | `get_upstream_features` | L2:F13158@9, k=10 | Emb:" white"@9 (de=13.62) +9 more |
| 7 | `inspect_feature` | L1, F7821 | " mentions of computer fans." |
| 8 | `inspect_feature` | L2, F585 | "the word "white", often in association with "dwarf"" |
| 9 | `inspect_feature` | L4, F14329 | " mentions of the colors black, white, or another color with "or" in it" |
| 10 | `get_upstream_features` | L4:F14329@9, k=10 | Emb:" white"@9 (de=12.69) +9 more |
| 11 | `inspect_feature` | L1, F13646 | " text discussing social justice issues" |
| 12 | `get_upstream_features` | L2:F13158@9, k=10 | Emb:" white"@9 (de=13.62) +9 more |
| 13 | `get_upstream_features` | L1:F7821@9, k=10 | Emb:" white"@9 (de=15.75) +9 more |
| 14 | `get_upstream_features` | L2:F585@9, k=10 | Emb:" white"@9 (de=30.75) +9 more |

**Findings:** The L6:3902 feature is a race/ethnicity detector that receives its strongest positive drive directly from the embedding of the input token ' white' at position 9 (direct_effect ~13.6).  One hop earlier, a similar strong signal comes from the same token to a layer‑4 race‑related feature (117) and a layer‑2 generic race feature (13158).  A parallel color‑mention feature (layer 4 idx 14329) also cont…

</details>

<details>
<summary><b>SA-3</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F117 | " terms related to race, racism, and social justice, with a particular " |
| 2 | `get_upstream_features` | L4:F117@10, k=10 | Emb:" white"@9 (de=12.12) +9 more |
| 3 | `inspect_feature` | L3, F13061 | " words related to race, gender and social issues" |
| 4 | `inspect_feature` | L3, F16373 | " mentions of demographic identity, especially race and gender" |
| 5 | `get_upstream_features` | L3:F13061@10, k=10 | Emb:" white"@9 (de=11.00) +9 more |
| 6 | `get_upstream_features` | L3:F16373@10, k=10 | Emb:" white"@9 (de=23.88) +9 more |
| 7 | `inspect_feature` | L2, F1708 | " mentions of colors" |

**Findings:** The target L4:F117 is a race‑focused feature that becomes active when the prompt mentions racial groups. Its strongest upstream driver is the embedding for the token ' white' (pos 9), which excites a mid‑layer demographic detector (L3:F16373). That detector aggregates race‑identity cues and passes a positive influence to the L4 feature. A parallel path via L3:F13061 also receives input from the sa…

</details>

<details>
<summary><b>SA-5</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F384 | " the string "ash" or "pund"" |
| 2 | `get_upstream_features` | L1:F384@2, k=10 | Emb:" author"@2 (de=13.94) +9 more |
| 3 | `inspect_feature` | L0, F753 | "the word "author" and words related to selling and prices" |
| 4 | `inspect_feature` | L0, F3612 | "the words "author", "authority", and "agency", often in a legal or aca" |
| 5 | `inspect_feature` | L0, F11009 | "the word "author" and related words like "book."" |

**Findings:** Tracing upstream from L1:F384 (pos 2) reveals that its activation is driven primarily by the input token embedding for "author" at the same position, with a large positive direct effect (13.94). Additional, much weaker, positive contributions come from three layer‑0 lexical detectors that fire on the token "author" in various contexts (generic, legal/academic, and book‑related). All upstream nodes…

</details>

<details>
<summary><b>SA-6</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F6576 | " the word "appearance"" |
| 2 | `get_upstream_features` | L1:F6576@3, k=10 | Emb:" appears"@3 (de=19.00) +9 more |
| 3 | `inspect_feature` | L0, F1998 | " occurrences of the word "seem" or "is" or "are."" |
| 4 | `inspect_feature` | L0, F7773 | " the word "lower" or "higher" in the context of comparisons" |
| 5 | `inspect_feature` | L0, F6705 | " adjectives expressing actions happening in time, often related to obs" |
| 6 | `get_upstream_features` | L0:F1998@3, k=10 | Emb:" appears"@3 (de=14.50) +9 more |

**Findings:** Tracing upstream from L1:F6576 (position 3) reveals that the feature primarily detects the lexical token "appearance". Its strongest upstream influence comes directly from the input embedding of the token " appears" (positive direct_effect 19.0), confirming a straightforward token‑level driving signal. Additional upstream contributors are low‑layer (layer 0) features: one that fires on copular ver…

</details>

<details>
<summary><b>SA-7</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 2 | `get_upstream_features` | L2:F13158@9, k=10 | Emb:" white"@9 (de=13.62) +9 more |
| 3 | `inspect_feature` | L1, F7821 | " mentions of computer fans." |
| 4 | `inspect_feature` | L0, F16013 | " mentions of the color blue, and perhaps colors in general or the comp" |
| 5 | `get_upstream_features` | L1:F7821@9, k=10 | Emb:" white"@9 (de=15.75) +9 more |
| 6 | `inspect_feature` | L0, F10910 | "the word "possession" and the words "white", "immediate" and "once" re" |
| 7 | `inspect_feature` | L1, F13646 | " text discussing social justice issues" |
| 8 | `get_upstream_features` | L0:F16013@9, k=10 | Emb:" white"@9 (de=15.56) +9 more |
| 9 | `inspect_feature` | L0, F12059 | " words related to purpose and intent" |

**Findings:** The target L2 feature (F13158) encodes race/ethnicity language. Its strongest upstream driver is the raw token embedding for " white" (direct_effect ~13.6), located at the input layer (≤8). A secondary pathway goes through a low‑level color detector (L0:F16013) also boosted by the same "white" token. Both routes converge on a layer‑1 feature (L1:F7821) that, despite a misleading label about comput…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×5 | L1:5220, L1:9113, L0:241, L6:15948, L6:5671 |
| 2 | `get_upstream_features` | L4:F10004@22, k=10 → Emb:" self"@21 (de=46.75) +9 more |
| 3 | `get_upstream_features` | L2:F15558@6, k=10 → Emb:" married"@6 (de=25.12) +9 more |
| 4 | `get_upstream_features` | L3:F10286@4, k=10 → Emb:" appears"@3 (de=20.62) +9 more |
| 5 | `get_upstream_features` | L0:F7773@3, k=10 → Emb:" appears"@3 (de=14.81) +9 more |
| 6 | `get_upstream_features` | L6:F3902@27, k=10 → Emb:" oriental"@27 (de=8.75) +9 more |
| 7 | `get_upstream_features` | L1:F5220@2, k=10 → Emb:" author"@2 (de=19.12) +9 more |
| 8 | `get_upstream_features` | L1:F9113@9, k=10 → Emb:" white"@9 (de=14.44) +9 more |
| 9 | `get_upstream_features` | L0:F241@6, k=10 → Emb:" married"@6 (de=12.81) +9 more |
| 10 | `get_upstream_features` | L6:F15948@10, k=10 → Emb:" guy"@10 (de=9.62) +9 more |
| 11 | `get_upstream_features` | L6:F5671@10, k=10 → Emb:" guy"@10 (de=5.03) +9 more |
| 12 | `inspect_feature` ×15 | L3:8890, L2:9320, L2:16224, L3:8492, L3:735, L4:12975, L5:13063, L3:15520, L4:6128, L2:15317, L2:9301, L2:10986, L4:14329, L3:16373, L3:16373 |

### Build

`build_circuit` → 15 nodes, 21 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 79,706 | 6,076 | 90,910 | 0 | $0.0367 | — | — |
| SA-5 | openai/gpt-oss-120b | 42,174 | 3,176 | 2,592 | 0 | $0.0083 | ✅ 4F/4E | Trace this feature upstream. What does it encode? Reach embe… |
| SA-3 | openai/gpt-oss-120b | 65,844 | 3,757 | 2,560 | 0 | $0.0122 | ✅ 5F/5E | Trace this feature upstream. What does it encode and what in… |
| SA-6 | openai/gpt-oss-120b | 49,892 | 3,481 | 5,856 | 0 | $0.0097 | ✅ 3F/3E | Trace this feature upstream. What does it encode? Reach embe… |
| SA-1 | openai/gpt-oss-120b | 106,822 | 6,856 | 5,056 | 0 | $0.0202 | ✅ 6F/6E | Trace this feature upstream to understand what it encodes. W… |
| SA-7 | openai/gpt-oss-120b | 111,479 | 8,458 | 7,680 | 0 | $0.0219 | ✅ 5F/6E | Trace this feature upstream. What does it encode? Reach embe… |
| SA-2 | openai/gpt-oss-120b | 187,487 | 9,519 | 7,680 | 0 | $0.0339 | ✅ 6F/11E | Trace this feature upstream. What does it encode and what in… |
| **Total** | | **643,404** | **41,323** | **122,334** | **0** | **$0.1428** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 45s