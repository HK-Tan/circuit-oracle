# Circuit Oracle Report
**Date:** 2026-07-28 07:19:29 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of this person as a computer science academic is driven by a mix of legitimate profession signals (Ph.D. degree, academic lab context) and clearly spurious features (Korea national origin, male pronoun "He"); notably, "He" is a positive driver while the actual job-title "Director" and the lab/grid tokens are negative drivers, indicating the probe weights nationality and gender markers more heavily than role-defining tokens.

**Confidence:** 7

**Reasoning:** The attribution graph reveals two distinct classes of features feeding the probe's classification score. 

**Profession-relevant (positive drivers):**
- **Academic degree cascade** (`sn_degree`): The token "Ph" at pos 38 and "D" at pos 40 (forming "Ph.D.") flow into L1:10132 (Ph.D. "D" detector, frac_nonzero=0.00233), then L2:10852 (academic titles and degrees, frac_nonzero=0.00801), L5:13801 (degree abbreviations), L6:2254 (academic degrees, frac_nonzero=0.00412), and converge at L7:14129 (academic degrees, universities, and people, frac_nonzero=0.00417). This is a genuine, well-formed profession signal.
- **Lab/academic context** (`sn_lab_neg`): Despite encoding genuinely academic content (laboratory, research facilities), L8:11284 actually drives the probe *negatively* (direct_effect = −0.0371), so this is academic vocabulary that works *against* the probe's target profession.

**Spurious/non-profession drivers:**
- **Korea national origin** (`sn_korea`): L14:15086 (references to Korea/Korean, direct_effect = −0.0613, the largest magnitude feature), fed by L1:10575 (Korean names, frac_nonzero=0.01043), L7:13010 (Korean hyphenated names), L5:5563 (Korean food/conglomerates), and L6:3774 (generic proper nouns firing on "Korea"). The signal originates almost entirely from the "Korea" token embedding at pos 46 (direct_effect = 28.875 to L14:15086). National origin is not a profession indicator.
- **Male gender pronoun** (`sn_gender_pronoun`): L0:1069 explicitly labeled "references to a male person, particularly when using the pronoun 'He' or 'His'" (frac_nonzero=0.0078) is a positive driver of the probe (direct_effect = +0.042), driven by the "He" embedding at pos 1. This is a textbook spurious gender marker.
- **"Director" title** (`sn_director_neg`): L2:4627 (the word "director", frac_nonzero=0.00347) is a *negative* driver (−0.0474), despite being the literal job title — the probe down-weights it.
- **"grid" keyword** (`sn_grid_neg`): L1:14934 (the word "grid") is a negative driver (frac_nonzero=0.00919).

**Confirmation of user concern:** Yes, the circuit validates the concern. The probe relies significantly on (a) the "He" male pronoun (a gender marker, positive), (b) the "Korea" country token (a nationality marker), and (c) the "Ph.D." abbreviation. The actual job-title token "Director" pushes the probe *away* from the predicted profession, and the "grid" / "Laboratory" technical-context tokens also push negatively. The model's "evidence" is therefore substantially spurious: nationality and gender pronouns are weighted comparably to — or more than — the literal job title. A counterfactual bio about a female researcher from a different country with similar credentials would likely be classified differently not because of profession-relevant features but because of these demographic markers.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe Output (profession classification) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L14:F15086](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/15086) | 46 | Korea Entity Detectors (L1-L14) |  references to Korea/Korean | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/15086) |
| [L7:F13010](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13010) | 46 | Korea Entity Detectors (L1-L14) |  Korean names, especially those with multiple parts separated by hyphens, in credits or medical contexts. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13010) |
| [L5:F5563](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5563) | 46 | Korea Entity Detectors (L1-L14) |  words related to Korean food and Korean conglomerates | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5563) |
| [L6:F3774](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) | 46 | Korea Entity Detectors (L1-L14) |  proper nouns or names with unusual capitalization | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) |
| [L1:F10575](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10575) | 46 | Korea Entity Detectors (L1-L14) |  Korean names | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10575) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 40 | Academic Degree Detectors (L1-L7) — "Ph.D." |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 40 | Academic Degree Detectors (L1-L7) — "Ph.D." | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L5:F13801](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) | 40 | Academic Degree Detectors (L1-L7) — "Ph.D." | abbreviations for degrees and mentions of educational attainment | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 40 | Academic Degree Detectors (L1-L7) — "Ph.D." |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L1:F10132](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) | 40 | Academic Degree Detectors (L1-L7) — "Ph.D." |  the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") written as "D" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) |
| [L4:F13943](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13943) | 40 | Academic Degree Detectors (L1-L7) — "Ph.D." |  words and abbreviations related to academic research | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13943) |
| [L2:F4627](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4627) | 4 | "Director" Detector (L2) — negative driver | the word "director" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4627) |
| [L0:F4621](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4621) | 4 | "Director" Detector (L2) — negative driver | words related to administrative positions and bodies | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4621) |
| [L8:F11284](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) | 11 | Academic/Lab Context Detectors (L4-L8) — negative driver |  words and phrases related to people's names, titles, universities, and research | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) |
| [L7:F5099](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5099) | 11 | Academic/Lab Context Detectors (L4-L8) — negative driver | words or phrases related to scientific laboratories and research | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5099) |
| [L6:F2214](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2214) | 11 | Academic/Lab Context Detectors (L4-L8) — negative driver | words related to scientific research facilities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2214) |
| [L5:F4052](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/4052) | 11 | Academic/Lab Context Detectors (L4-L8) — negative driver | academic institutions and researchers | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/4052) |
| [L4:F12934](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12934) | 11 | Academic/Lab Context Detectors (L4-L8) — negative driver | names of academic journals | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12934) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Male Pronoun "He" Detector (L0) — gender marker |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L1:F14934](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14934) | 7 | Male Pronoun "He" Detector (L0) — gender marker | the word "grid" and some related terms related to "grids" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14934) |
| [L0:F15160](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15160) | 7 | "grid" Token Detector (L1) — negative driver | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15160) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:15086 de=-0.061 |
| 3 | `inspect_feature` ×8 | L14:15086, L6:3774, L0:10846, L2:10852, L1:14934, L2:4627, L0:8658, L7:14129 |
| 4 | `get_upstream_features` | Emb:" Korea"@46 (de=28.88) +9 more |
| 5 | `get_upstream_features` | Emb:" Korea"@46 (de=18.38) +9 more |
| 6 | `get_upstream_features` | Emb:" Director"@4 (de=27.50) +9 more |
| 7 | `get_upstream_features` | Emb:" Ph"@38 (de=14.12) +9 more |
| 8 | `get_upstream_features` | L6:F2254 (de=7.12) +9 more |
| 9 | `get_upstream_features` | Emb:" Korea"@46 (de=14.25) +9 more |
| 10 | `get_upstream_features` | Emb:" Korea"@46 (de=16.38) +9 more |
| 11 | `get_upstream_features` | L2:F10852 (de=11.31) +9 more |
| 12 | `get_upstream_features` | L2:F10852 (de=6.62) +9 more |
| 13 | `get_upstream_features` | Emb:" Ph"@38 (de=16.12) +9 more |
| 14 | `inspect_feature` ×9 | L0:1069, L0:1242, L1:10575, L0:10846, L0:12904, L0:3255, L0:5718, L0:5743, L8:11284 |
| 15 | `get_upstream_features` | Emb:"He"@1 (de=22.62) +9 more |
| 16 | `get_upstream_features` | Emb:" Laboratory"@11 (de=18.00) +9 more |
| 17 | `get_upstream_features` | Emb:" Director"@4 (de=18.88) +9 more |
| 18 | `get_upstream_features` | Emb:" Laboratory"@11 (de=15.75) +9 more |
| 19 | `get_upstream_features` | Emb:" Grid"@7 (de=14.06) +9 more |
| 20 | `get_upstream_features` | Emb:" Director"@4 (de=14.56) +9 more |
| 21 | `get_upstream_features` | Emb:" Laboratory"@11 (de=17.00) +9 more |
| 22 | `inspect_feature` ×3 | L6:2254, L4:13943, L1:10132 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F15086@46` | ✅ reported | 5 | 13 | Trace the L14:15086 (references to Korea) feature upstream to identify which inp… |
| SA-2 | `L7:F14129@40` | ✅ reported | 6 | 16 | Trace the L7:14129 (academic degrees, universities, people) feature upstream at … |
| SA-3 | `L2:F4627@4` | ✅ reported | 4 | 5 | Trace the L2:4627 (the word "director") feature at pos 4 (the "Director" token) … |
| SA-4 | `L8:F11284@11` | ✅ reported | 5 | 7 | Trace the L8:11284 (names, titles, universities, research) feature at pos 11 (La… |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F15086 | " references to Korea/Korean" |
| 2 | `get_upstream_features` | L14:F15086@46, k=15 | Emb:" Korea"@46 (de=28.88) +14 more |
| 3 | `inspect_feature` | L7, F13010 | " Korean names, especially those with multiple parts separated by hyphe" |
| 4 | `inspect_feature` | L5, F5563 | " words related to Korean food and Korean conglomerates" |
| 5 | `inspect_feature` | L6, F3774 | " proper nouns or names with unusual capitalization" |
| 6 | `get_upstream_features` | L7:F13010@46, k=10 | Emb:" Korea"@46 (de=14.25) +9 more |
| 7 | `inspect_feature` | L1, F10575 | " Korean names" |
| 8 | `get_upstream_features` | L6:F3774@46, k=10 | Emb:" Korea"@46 (de=18.38) +9 more |
| 9 | `get_upstream_features` | L5:F5563@46, k=10 | Emb:" Korea"@46 (de=16.38) +9 more |
| 10 | `get_upstream_features` | L1:F10575@46, k=10 | Emb:" Korea"@46 (de=18.00) +9 more |

**Findings:** The probe feature L14:15086 (references to Korea) is driven primarily by the direct embedding of the token "Korea" (direct_effect ~28.9). Additional positive pathways pass through mid‑layer features: a layer‑7 Korean‑name detector (13010), a layer‑5 Korean‑culture detector (5563), and a layer‑6 generic proper‑noun detector (3774). These in turn are fed by the same token embedding and an early‑laye…

</details>

<details>
<summary><b>SA-2</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14129 | " academic degrees, universities, and people associated with them" |
| 2 | `get_upstream_features` | L7:F14129@40, k=10 | L6:F2254 (de=7.12) +9 more |
| 3 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 4 | `inspect_feature` | L5, F13801 | "abbreviations for degrees and mentions of educational attainment" |
| 5 | `get_upstream_features` | L6:F2254@40, k=10 | L2:F10852 (de=11.31) +9 more |
| 6 | `get_upstream_features` | L5:F13801@40, k=10 | L2:F10852 (de=6.62) +9 more |
| 7 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 8 | `inspect_feature` | L1, F10132 | " the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") writ" |
| 9 | `get_upstream_features` | L2:F10852@40, k=10 | Emb:" Ph"@38 (de=14.12) +9 more |
| 10 | `inspect_feature` | L1, F14298 | "academic publications, papers, and citations" |

**Findings:** The tracing reveals a cascade that starts from raw token embeddings for "Ph" (pos 38) and "D" (pos 40) and quickly excites a series of low-layer degree-related features. The strongest upstream driver is L6:2254 (references to academic degrees), which itself is driven primarily by the embeddings of "Ph" and "D" and by L2:10852 (academic titles and degrees). All key nodes lie in layers ≤8, satisfyin…

</details>

<details>
<summary><b>SA-3</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F4627 | "the word "director"" |
| 2 | `get_upstream_features` | L2:F4627@4, k=15 | Emb:" Director"@4 (de=27.50) +14 more |
| 3 | `inspect_feature` | L0, F4621 | " words related to administrative positions and bodies" |
| 4 | `inspect_feature` | L0, F2115 | " data reported as a percentage inside brackets, especially in a labora" |
| 5 | `inspect_feature` | L1, F15565 | " people's job titles with "director" in them" |
| 6 | `get_upstream_features` | L0:F4621@4, k=10 | Emb:" Director"@4 (de=14.56) +9 more |
| 7 | `get_upstream_features` | L1:F15565@4, k=10 | Emb:" Director"@4 (de=20.75) +9 more |
| 8 | `inspect_feature` | L0, F10846 | "the word "also"" |
| 9 | `get_upstream_features` | L1:F15565@4, k=10 | Emb:" Director"@4 (de=20.75) +9 more |
| 10 | `get_upstream_features` | L0:F4621@4, k=15 | Emb:" Director"@4 (de=14.56) +14 more |
| 11 | `inspect_feature` | L0, F5705 | " words and phrases referencing recognition and achievement" |

**Findings:** The strong negative driver for the token 'Director' (L2:4627) is primarily fed by the embedding of the exact token 'Director' itself (positive direct effect 27.5). Upstream, a low‑frequency administrative‑role feature in layer 0 (L0:4621) provides a modest positive boost (0.73), suggesting the model uses role‑context cues to sharpen the director detection. Additional minor contributors include a p…

</details>

<details>
<summary><b>SA-4</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L8, F11284 | " words and phrases related to people's names, titles, universities, an" |
| 2 | `get_upstream_features` | L8:F11284@11, k=15 | Emb:" Laboratory"@11 (de=11.06) +14 more |
| 3 | `inspect_feature` | L4, F12934 | " names of academic journals" |
| 4 | `get_upstream_features` | L4:F12934@11, k=15 | Emb:" Laboratory"@11 (de=17.00) +14 more |
| 5 | `inspect_feature` | L7, F5099 | " words or phrases related to scientific laboratories and research" |
| 6 | `inspect_feature` | L6, F2214 | " words related to scientific research facilities" |
| 7 | `get_upstream_features` | L7:F5099@11, k=15 | Emb:" Laboratory"@11 (de=6.56) +14 more |
| 8 | `inspect_feature` | L5, F4052 | " academic institutions and researchers" |
| 9 | `inspect_feature` | L7, F10900 | " words related to cell biology and research proposals in that field" |
| 10 | `get_upstream_features` | L5:F4052@11, k=15 | Emb:" Laboratory"@11 (de=4.06) +14 more |

**Findings:** The target L8:11284 feature that drives the negative laboratory response receives its strongest positive influence from the embedding of the token 'Laboratory' itself, as well as from higher‑layer features that detect academic journals (L4:12934), scientific laboratory mentions (L7:5099), research facilities (L6:2214), and academic institutions (L5:4052). These upstream nodes collectively encode s…

</details>

### Build

`build_circuit` → 14 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 51,134 | 5,292 | 198,392 | 0 | $0.0336 | — | — |
| SA-4 | openai/gpt-oss-120b | 113,456 | 5,984 | 2,528 | 0 | $0.0206 | ✅ 5F/7E | Trace the L8:11284 (names, titles, universities, research) f… |
| SA-1 | openai/gpt-oss-120b | 133,844 | 8,612 | 8,160 | 0 | $0.0254 | ✅ 5F/13E | Trace the L14:15086 (references to Korea) feature upstream t… |
| SA-2 | openai/gpt-oss-120b | 131,160 | 9,317 | 64 | 0 | $0.0253 | ✅ 6F/16E | Trace the L7:14129 (academic degrees, universities, people) … |
| SA-3 | openai/gpt-oss-120b | 124,146 | 6,575 | 13,760 | 0 | $0.0228 | ✅ 4F/5E | Trace the L2:4627 (the word "director") feature at pos 4 (th… |
| **Total** | | **553,740** | **35,780** | **222,904** | **0** | **$0.1276** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 16s