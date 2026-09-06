# Circuit Oracle Report
**Date:** 2026-07-28 07:09:14 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_10 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a tightly clustered set of transcoder features that detect race- and identity-related vocabulary — the input tokens "race", "black", "white", "cops", "force", and "mentioning" — with zero circuit mass attributable to the actual semantic content of the sentence (the implicit-bias argument, the "not mentioning…assumed" structure, or the claim about bad cops being white).

**Confidence:** 6

**Reasoning:** The circuit terminates at the output probe node and is fed almost exclusively by a single conceptual supernode: **race/ethnicity terms (L6:F3902, +0.586 direct_effect, frac_nonzero=0.018)**, which itself traces directly to token embeddings for " race" (pos 5, +22.6), " black" (pos 16, +14.0), and modestly " cops" (pos 8) and " of" (pos 6). This is supplemented by **race/racism/Black-focused terms (L4:F117, +0.268 across positions 5/6/17)**, **race/gender/social issues (L3:F13061, +0.192 at pos 17)**, **discrimination language (L6:F9228, frac_nonzero=0.60 — extremely broad/generic)**, **race/origins/demographic (L7:F8030, frac_nonzero=0.11 — broad)**, and **race/ethnicity vocabulary (L2:F13158, +0.173)**. Upstream traces confirm these features are all driven by the *literal words* "race", "black", "white", "cops", "force", "mentioning" — not by sentence-level meaning.

This is a **strong, clean confirmation of the user's concern**. The user's hypothesis was that the probe relies on "an identity group" signal rather than actual prompt content. The circuit shows:

1. **Eight of the top 10 features driving the probe are race/ethnicity/demographic/identity detectors** (L6:F3902 race terms, L4:F117 race/racism/Black, L2:F13158 race-ethnicity vocabulary, L3:F13061 race/gender/social, L7:F8030 race/origins/demographic, L6:F9228 discrimination, L6:F343 patient demographics, L2:F10509 "race" word, L2:F13653 "force" word). All of these detect *which demographic terms appear*, not *what is being said about them*.

2. **The probe fires on the input text as a "race-mentioning text," not as a "biased-claim text."** A near-identical sentence that just discussed the weather but happened to contain the words "black cops" and "white people" would activate the same circuit. Conversely, a sentence with the same logical structure and toxic implication but using no demographic terms (e.g., "By not mentioning the names of the assailants, it is assumed the attackers are unknown") would produce a near-zero probe score despite equivalent or worse toxicity.

3. **One feature (L2:F10509, "the word 'race'", direct_effect = −0.49) is a notable anomaly** — it actively *suppresses* the probe when the word "race" appears. The subagent's interpretation is that this looks like a safety/sensitivity gate. But it is the *only* non-identity-related signal in the entire top 20, and it cuts *against* the probe rather than encoding the toxic-claim semantics.

4. **No features encode the actual argumentative content**: there is no detector for "omission implies", "not mentioning → assumed", "generalization", or any stance/tone/sarcasm/implicature machinery. The "mentioning" feature (L3:F6517) is a generic verb detector, not a negation/implicature detector. The "force" feature (L2:F13653) is a bare word detector.

5. **Two non-race features appear**: L4:F11200 (authorship "By" — a generic article-starter detector, +0.18) and L0:F1823 ("Bureau", −0.19 — fires on "the", irrelevant to the sentence meaning). Neither encodes content.

6. **One positive non-identity feature (L0:F1910, "not only", +0.166)** fires on "not" but is a generic negation/qualification detector, not a claim-content detector.

In short, the probe is effectively acting as a **"does this text contain racial identity terms?" bag-of-words classifier** dressed up with shallow syntactic context. It identifies a *topic* (race/demographics) rather than a *toxic claim* (implicit bias, generalization, stereotyping). The user's worry is borne out by the circuit: the mechanism is identity-token presence, not semantic or lexical content beyond the identity words themselves.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2961](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2961) | 3 | Layer-0 lexical detectors (low-level) |  words that act as qualifications or negations, with a high preference for "necessarily" and "uncommon." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2961) |
| [L0:F1910](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1910) | 3 | Layer-0 lexical detectors (low-level) |  the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1910) |
| [L0:F1823](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1823) | 5 | Layer-0 lexical detectors (low-level) |  occurances of the word 'Bureau' | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1823) |
| [L0:F7820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7820) | 3 | Layer-0 lexical detectors (low-level) |  words indicating uncertainty or tentativeness | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7820) |
| [L2:F10509](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10509) | 5 | Word 'race' lexical detector (L2:F10509) — SUPPRESSES probe |  the word "race." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10509) |
| [L2:F13653](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13653) | 13 | Word 'force' detector (L2:F13653) | the word "force" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13653) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 5 | Race/ethnicity vocabulary (L2:F13158) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L3:F6517](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6517) | 3 | 'Mentioning' verb detector (L3:F6517) |  words related to mentioning something | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6517) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 17 | Race/gender/social issues (L3:F13061) |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 6 | Race/racism/Black-focused terms (L4:F117) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 5 | Race/racism/Black-focused terms (L4:F117) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 17 | Race/racism/Black-focused terms (L4:F117) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F11200](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11200) | 1 | Authorship 'By' (L4:F11200) |  a variety of words and phrases related to authorship and origination of something. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11200) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 6 | Race/ethnicity term cluster (L6:F3902) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 5 | Race/ethnicity term cluster (L6:F3902) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 16 | Race/ethnicity term cluster (L6:F3902) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F9228](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9228) | 6 | Discrimination language (L6:F9228, L6:F343) |  language regarding discrimination based on race, gender, religion, and disability | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9228) |
| [L6:F343](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/343) | 6 | Discrimination language (L6:F9228, L6:F343) |  references to patient demographics and characteristics | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/343) |
| [L7:F8030](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8030) | 6 | Race/origins/demographic (L7:F8030) |  words about people's races, origins, and demographic groups | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8030) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:3902 de=0.586 |
| 3 | `inspect_feature` ×6 | L6:3902, L2:10509, L4:117, L0:7820, L6:9228, L0:1823 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F3902@6` | ✅ reported | 4 | 12 | Trace this "terms referring to race and ethnicity" feature upstream through the … |
| SA-2 | `L4:F117@6` | ✅ reported | 4 | 18 | Trace this "terms related to race, racism, social justice, particularly Black pe… |
| SA-3 | `L2:F10509@5` | ✅ reported | 3 | 2 | Trace this L2 "the word race" feature upstream. It has a strong NEGATIVE direct_… |

<details>
<summary><b>SA-1</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F3902 | " terms referring to race and ethnicity" |
| 2 | `get_upstream_features` | L6:F3902@6, k=10 | Emb:" race"@5 (de=11.00) +9 more |
| 3 | `get_upstream_features` | L6:F3902@5, k=10 | Emb:" race"@5 (de=22.62) +9 more |
| 4 | `get_upstream_features` | L6:F3902@16, k=10 | Emb:" black"@16 (de=14.00) +9 more |
| 5 | `inspect_feature` | L4, F117 | " terms related to race, racism, and social justice, with a particular " |
| 6 | `get_upstream_features` | L4:F117@6, k=10 | Emb:" race"@5 (de=19.00) +9 more |
| 7 | `get_upstream_features` | L6:F3902@24, k=10 | ❌ Feature (layer=6, feature_idx=3902) not found at pos=24. Thi |
| 8 | `inspect_feature` | L4, F5584 | " words related to race, ethnicity, nationality or population groups" |
| 9 | `inspect_feature` | L4, F14329 | " mentions of the colors black, white, or another color with "or" in it" |
| 10 | `inspect_feature` | L5, F12135 | " terms related to discrimination based on identity" |
| 11 | `get_upstream_features` | L4:F5584@6, k=10 | Emb:" race"@5 (de=16.62) +9 more |
| 12 | `inspect_feature` | L5, F12135 | " terms related to discrimination based on identity" |
| 13 | `get_upstream_features` | L5:F12135@6, k=10 | Emb:" race"@5 (de=4.84) +9 more |
| 14 | `get_upstream_features` | L4:F14329@16, k=10 | Emb:" black"@16 (de=19.62) +9 more |

**Findings:** The race‑related activation at L6:F3902 is driven primarily by concrete token embeddings: the word 'race' (positions 5), the colour terms 'black' and 'white' (positions 16 and elsewhere), and the noun 'cops' (position 8). Upstream features in layers 4–5 act as increasingly abstract detectors for race/ethnicity terminology, but all of them receive their strongest positive influence from the same le…

</details>

<details>
<summary><b>SA-2</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F117 | " terms related to race, racism, and social justice, with a particular " |
| 2 | `get_upstream_features` | L4:F117@6, k=15 | Emb:" race"@5 (de=19.00) +14 more |
| 3 | `inspect_feature` | L3, F15128 | " proper nouns and frequently used short function words, especially "of" |
| 4 | `inspect_feature` | L2, F10295 | " the word "of" and words that end with "thereof."" |
| 5 | `get_upstream_features` | L4:F117@5, k=15 | Emb:" race"@5 (de=25.12) +14 more |
| 6 | `get_upstream_features` | L4:F117@8, k=15 | Emb:" cops"@8 (de=10.12) +14 more |
| 7 | `get_upstream_features` | L3:F15128@6, k=10 | Emb:" of"@6 (de=18.00) +9 more |
| 8 | `get_upstream_features` | L2:F10295@6, k=10 | Emb:" the"@4 (de=8.50) +9 more |
| 9 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |

**Findings:** The race‑related feature (L4:F117) is driven mainly by the raw token embedding for the word "race" (pos 5) and, to a lesser extent, by the embedding for "of" (pos 6). A shallow cascade of higher‑layer features (L3:F15128, L2:F10295, L1:F3431) propagates the "of" signal. A low‑frequency race‑specific feature (L2:F13158) adds a small boost when race terms appear. No positive influence comes from tok…

</details>

<details>
<summary><b>SA-3</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F10509 | " the word "race."" |
| 2 | `get_upstream_features` | L2:F10509@5, k=10 | Emb:" race"@5 (de=30.12) +9 more |
| 3 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 4 | `inspect_feature` | L0, F8747 | " the word "pair"" |

**Findings:** The L2 feature F10509 is a lexical detector for the word 'race'. Its strongest upstream driver is the raw token embedding for ' race' (direct_effect +30.1), confirming that the feature directly reads the input token. Additional low‑level upstream features (0:9026 and 0:8747) provide modest positive contributions, but the core signal originates from the embedding. Despite being a simple word detect…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×9 | L7:8030, L3:13061, L4:11200, L3:6517, L2:13653, L2:13158, L0:2961, L0:1910, L6:343 |

### Build

`build_circuit` → 20 nodes, 30 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 48,554 | 5,152 | 51,219 | 0 | $0.0238 | — | — |
| SA-3 | openai/gpt-oss-120b | 26,851 | 2,683 | 7,680 | 0 | $0.0058 | ✅ 3F/2E | Trace this L2 "the word race" feature upstream. It has a str… |
| SA-2 | openai/gpt-oss-120b | 107,535 | 8,323 | 2,752 | 0 | $0.0212 | ✅ 4F/18E | Trace this "terms related to race, racism, social justice, p… |
| SA-1 | openai/gpt-oss-120b | 150,523 | 8,523 | 17,632 | 0 | $0.0280 | ✅ 4F/12E | Trace this "terms referring to race and ethnicity" feature u… |
| **Total** | | **333,463** | **24,681** | **79,283** | **0** | **$0.0787** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 52s