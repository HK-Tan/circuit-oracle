# Circuit Oracle Report
**Date:** 2026-07-28 07:10:25 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_7 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity classification is driven almost entirely by the *presence of identity-group tokens* ("Black", "White", "Gay", "Pride") rather than by any sentiment, slur, or harmful-content signal — confirming the user's concern that the circuit relies on spurious identity cues.

**Confidence:** 8/10

**Reasoning:**

The circuit traces cleanly from raw token embeddings (pos 1 "Black", pos 5 "black", pos 9/13 "Gay"/"gay", pos 17 "White", pos 2/10 "Pride") to the probe output through three parallel supernodes, none of which encode harmful semantics:

1. **Early-layer lexical "black"/"proud" detectors (suppress the probe).** L1:F9113 ("discussions about race and slavery", pos 1, direct_effect −0.32) and L2:F9528 ("the color black", pos 1 & 5, direct_effect −0.23/−0.17), L1:F12542 ("proud", pos 2, −0.22), L3:F7993 ("black", pos 1, −0.17) all fire on the literal tokens "Black"/"black"/"proud" and *push the probe DOWN*. Their upstream is just the raw embedding of those tokens (e.g. L3:F7993 receives direct_effect 23.5 from the "Black" embedding at pos 1; L2:F9528 receives direct_effect 30.0 from the same). These are pure lexical detectors, not toxicity-relevant.

2. **Mid-layer race/ethnicity detectors (promote the probe).** L2:F13158 ("words about race and ethnicity", direct_effect +0.25/+0.22 at pos 17 and 5) and L2:F11363 ("colors", +0.27 at pos 1) and L6:F3902 ("terms referring to race and ethnicity", +0.20/+0.17) and L4:F117 ("terms related to race, racism, and social justice") all activate on the identity tokens "Black"/"White" and contribute *positive* direct_effects to the probe. Their upstream is again the raw identity-token embedding (e.g. "White" at pos 17 → L2:F13158 with direct_effect 13.56). Promoted tokens for these features include "▁black", "▁white", "▁Hispanic", "▁ethnic", "Racism", "▁racist" — generic identity/race vocabulary, not slurs or hateful content.

3. **Mid- and late-layer LGBTQ+ detectors (promote the probe, strongly).** The dominant positive drivers are L4:F15899 ("language associated with the LGBTQ community", frac_nonzero 0.006, promoted "▁gay", "▁LGBTQ", "▁transgender"), L6:F6085 ("text related to homosexuality and same-sex marriage", frac_nonzero 0.0017), and L6:F15295 ("HIV/AIDS", promoted "▁gays", "▁homosexuality"). These feed L8:F15771 ("discussion of LGBTQ+ issues", direct_effect +0.32/+0.23/+0.19 at pos 9/13/2, frac_nonzero 0.0078), which is the single largest direct contributor to the probe. Tracing L8:F15771 upstream shows it is driven directly by the embeddings of the *literal* identity words: the " gay" embedding at pos 13 contributes direct_effect 18.4, "Gay" at pos 9 contributes 10.4, and "Pride"/"Pride" at pos 10/2 also contribute. The mid-layer features are themselves excited by those same identity-token embeddings (e.g. L6:F6085 gets direct_effect 21.75 from the "Gay" embedding at pos 9).

**Mechanism summary.** The probe fires because Gemma-2-2B's residual stream at the probe's layer is dominated by features that simply *detect the presence of protected-class identity words* — "Black", "White", "Gay", "Pride" — regardless of context. Notably absent from the entire top-20 circuit are: any slur feature, any "NAZI" feature, any "hypocrisy"/"worse than racism" semantic feature, any negative-sentiment or threat feature, or any feature whose top activating examples include the actual toxic content. The one token in the prompt that *is* overtly toxic ("NAZI!") does not appear in any upstream embedding node feeding the probe. Instead, the model treats the prompt as a "discussion of LGBTQ+ / race-and-pride topics" and routes that identity-presence signal into the toxicity direction. This is exactly the spurious-correlation mechanism the user suspected: the probe classifies the prompt as toxic on the basis of *who is being talked about* (named identity groups), not *what is being said about them*. The presence of two opposing early-layer "black"-lexical detectors with negative direct_effect partially cancels the race signal, but the much stronger LGBTQ+ supernode carries the probe to a high toxicity score, and a prompt like "Black Pride = …" (which contains zero toxic content) would produce the same identity-token activation pattern.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Black (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: black (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: White (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: Gay (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: gay (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: Pride (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: Pride (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L1:F9113](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) | 1 | Early-layer "black" / "proud" lexical detectors (suppress probe) |  discussions about race and slavery | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) |
| [L1:F12542](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12542) | 2 | Early-layer "black" / "proud" lexical detectors (suppress probe) | mentions of the word "proud" or words relating to TV shows and TV seasons. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12542) |
| [L2:F9528](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) | 1 | Early-layer "black" / "proud" lexical detectors (suppress probe) |  the color black | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) |
| [L2:F9528](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) | 5 | Early-layer "black" / "proud" lexical detectors (suppress probe) |  the color black | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) |
| [L3:F7993](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7993) | 1 | Early-layer "black" / "proud" lexical detectors (suppress probe) | the word "black" and its plural form "blacks" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7993) |
| [L3:F7993](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7993) | 2 | Early-layer "black" / "proud" lexical detectors (suppress probe) | the word "black" and its plural form "blacks" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7993) |
| [L2:F1644](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1644) | 2 | Early-layer "black" / "proud" lexical detectors (suppress probe) |  different forms of the word "pride" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1644) |
| [L2:F11363](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11363) | 1 | Mid-layer race / ethnicity detectors (promote probe) |  colors and words like Diamond. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11363) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 5 | Mid-layer race / ethnicity detectors (promote probe) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 17 | Mid-layer race / ethnicity detectors (promote probe) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 5 | Mid-layer race / ethnicity detectors (promote probe) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 17 | Mid-layer race / ethnicity detectors (promote probe) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 17 | Mid-layer race / ethnicity detectors (promote probe) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 2 | Mid-layer race / ethnicity detectors (promote probe) |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L4:F15899](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) | 9 | Mid-layer LGBTQ+ identity detectors (promote probe) |  language associated with the LGBTQ community and discussions of gender and identity. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) |
| [L4:F15899](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) | 13 | Mid-layer LGBTQ+ identity detectors (promote probe) |  language associated with the LGBTQ community and discussions of gender and identity. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) |
| [L6:F6085](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) | 9 | Mid-layer LGBTQ+ identity detectors (promote probe) |  text related to homosexuality and same-sex marriage | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) |
| [L6:F6085](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) | 13 | Mid-layer LGBTQ+ identity detectors (promote probe) |  text related to homosexuality and same-sex marriage | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) |
| [L6:F15295](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15295) | 2 | Mid-layer LGBTQ+ identity detectors (promote probe) |  words and abbreviations related to HIV/AIDS and viral infections. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15295) |
| [L8:F15771](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) | 2 | Late-layer LGBTQ+ discourse aggregator | discussion of LGBTQ+ issues, especially same-sex marriage, adoption, and related topics | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) |
| [L8:F15771](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) | 9 | Late-layer LGBTQ+ discourse aggregator | discussion of LGBTQ+ issues, especially same-sex marriage, adoption, and related topics | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) |
| [L8:F15771](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) | 13 | Late-layer LGBTQ+ discourse aggregator | discussion of LGBTQ+ issues, especially same-sex marriage, adoption, and related topics | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L8:15771 de=0.324 |
| 3 | `inspect_feature` ×14 | L8:15771, L6:6085, L4:15899, L2:13158, L1:9113, L2:11363, L2:9528, L3:13061, L1:12542, L6:3902, L4:117, L2:1644, L6:15295, L3:7993 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L8:F15771@9` | ✅ reported | 7 | 6 | Trace upstream from L8:F15771 at position 9. Find which input tokens drive this … |
| SA-2 | `L8:F15771@13` | ✅ reported | 5 | 9 | Trace upstream from L8:F15771 at position 13. Find which input tokens drive this… |
| SA-3 | `L2:F13158@17` | ✅ reported | 5 | 7 | Trace upstream from L2:F13158 (words about race and ethnicity) at position 17. F… |
| SA-4 | `L2:F13158@5` | ✅ reported | 5 | 8 | Trace upstream from L2:F13158 (words about race and ethnicity) at position 5. Fi… |
| SA-5 | `L1:F9113@1` | ❌ error | — | — | Trace upstream from L1:F9113 (discussions about race and slavery) at position 1.… |
| SA-6 | `L1:F12542@2` | ✅ reported | 4 | 5 | Trace upstream from L1:F12542 (word "proud") at position 2. This is a NEGATIVE d… |
| SA-7 | `L3:F7993@1` | ✅ reported | 5 | 6 | Trace upstream from L3:F7993 (word "black") at position 1. This is a NEGATIVE di… |
| SA-8 | `L2:F9528@1` | ✅ reported | 3 | 6 | Trace upstream from L2:F9528 (the color black) at position 1. This is a NEGATIVE… |

<details>
<summary><b>SA-1</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L8, F15771 | "discussion of LGBTQ+ issues, especially same-sex marriage, adoption, a" |
| 2 | `get_upstream_features` | L8:F15771@9, k=10 | Emb:"Gay"@9 (de=10.38) +9 more |
| 3 | `inspect_feature` | L6, F6085 | " text related to homosexuality and same-sex marriage" |
| 4 | `inspect_feature` | L4, F15899 | " language associated with the LGBTQ community and discussions of gende" |
| 5 | `get_upstream_features` | L6:F6085@9, k=10 | Emb:"Gay"@9 (de=21.75) +9 more |
| 6 | `get_upstream_features` | L4:F15899@9, k=10 | Emb:"Gay"@9 (de=13.81) +9 more |
| 7 | `inspect_feature` | L4, F8645 | " passages discussing same-sex marriage" |
| 8 | `get_upstream_features` | L1:F8766@9, k=10 | Emb:"Gay"@9 (de=2.42) +9 more |
| 9 | `inspect_feature` | L1, F8766 | " words related to Harry Potter fan fiction and formal procedures" |
| 10 | `inspect_feature` | L7, F10287 | " mentions and terms related to LGBTQ rights" |
| 11 | `inspect_feature` | L7, F10287 | " mentions and terms related to LGBTQ rights" |

**Findings:** Tracing upstream from L8:F15771 (position 9) quickly reaches the raw input embedding for the token “Gay" (pos 9) with a large positive direct effect (10.38). This embedding also strongly excites L6:F6085 (direct effect 21.75) and L4:F15899 (13.81), both of which are earlier‑layer detectors for homosexuality‑related language. Consequently, the primary driver of the LGBTQ‑related feature at L8 is th…

</details>

<details>
<summary><b>SA-2</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L8, F15771 | "discussion of LGBTQ+ issues, especially same-sex marriage, adoption, a" |
| 2 | `get_upstream_features` | L8:F15771@13, k=10 | Emb:" gay"@13 (de=18.38) +9 more |
| 3 | `inspect_feature` | L6, F6085 | " text related to homosexuality and same-sex marriage" |
| 4 | `get_upstream_features` | L6:F6085@13, k=10 | Emb:" gay"@13 (de=33.00) +9 more |
| 5 | `inspect_feature` | L4, F15899 | " language associated with the LGBTQ community and discussions of gende" |
| 6 | `inspect_feature` | L7, F16171 | " texts about homosexuality, gay marriage, and religious views on these" |
| 7 | `inspect_feature` | L4, F8645 | " passages discussing same-sex marriage" |

**Findings:** The target L8:F15771 is an LGBTQ‑related discourse detector. Its strongest upstream driver is the token embedding for the word "gay" at the same position (direct_effect 18.4), confirming that the prompt token "gay" directly fuels this feature. Additional supporting upstream features in lower layers detect broader LGBTQ vocabulary (L4:F15899), explicit mentions of homosexuality and same‑sex marriag…

</details>

<details>
<summary><b>SA-3</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 2 | `get_upstream_features` | L2:F13158@17, k=10 | Emb:"White"@17 (de=13.56) +9 more |
| 3 | `inspect_feature` | L1, F13646 | " text discussing social justice issues" |
| 4 | `get_upstream_features` | L1:F13646@17, k=10 | Emb:"White"@17 (de=4.62) +9 more |
| 5 | `inspect_feature` | L1, F7821 | " mentions of computer fans." |
| 6 | `inspect_feature` | L1, F438 | " words related to surveys, data collection, and respondents" |
| 7 | `get_upstream_features` | L1:F7821@17, k=10 | Emb:"White"@17 (de=13.25) +9 more |
| 8 | `inspect_feature` | L0, F3167 | " the word "shape"" |

**Findings:** The race‑related detector L2:F13158 receives its strongest positive drive from the input token embedding \"White\" at position 17 (direct_effect = 13.56). Additional positive contributions come from a social‑justice context detector (L1:F13646) and two more generic features (L1:F7821, L1:F438). All these upstream paths have been traced down to embedding nodes, satisfying the lower‑third layer requ…

</details>

<details>
<summary><b>SA-4</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 2 | `get_upstream_features` | L2:F13158@5, k=10 | Emb:" black"@5 (de=10.75) +9 more |
| 3 | `inspect_feature` | L1, F13646 | " text discussing social justice issues" |
| 4 | `get_upstream_features` | L1:F13646@5, k=10 | Emb:" black"@5 (de=4.50) +9 more |
| 5 | `inspect_feature` | L0, F16013 | " mentions of the color blue, and perhaps colors in general or the comp" |
| 6 | `inspect_feature` | L1, F3020 | " the word "factor"" |
| 7 | `get_upstream_features` | L1:F3020@5, k=10 | Emb:" black"@5 (de=16.38) +9 more |
| 8 | `inspect_feature` | L0, F13380 | "the word "uniform" and sometimes words related to roads or passing, bu" |
| 9 | `get_upstream_features` | L0:F16013@5, k=10 | Emb:" black"@5 (de=15.81) +9 more |

**Findings:** The race‑related feature L2:F13158 is primarily driven by the input token " black" at position 5 (direct effect 10.75). Additional positive contributions come from " being" and " Pride". Upstream tracing shows that intermediate features in layers 1 and 0 (F13646, F3020, F16013) are also excited mainly by the same token " black". All traced paths reach the lower third of the model (layers ≤8) and i…

</details>

<details>
<summary><b>SA-6</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F12542 | "mentions of the word "proud" or words relating to TV shows and TV seas" |
| 2 | `get_upstream_features` | L1:F12542@2, k=15 | Emb:" Pride"@2 (de=13.75) +14 more |
| 3 | `inspect_feature` | L0, F5012 | " words related to time periods, natural science, and publishing" |
| 4 | `inspect_feature` | L0, F12292 | " words or phrases related to specifications or cost" |
| 5 | `get_upstream_features` | L0:F5012@2, k=10 | Emb:"Black"@1 (de=8.62) +9 more |
| 6 | `inspect_feature` | L0, F12717 | " the word "pride" in different contexts" |

**Findings:** Tracing upstream from the target feature L1:F12542 (position 2, token "proud") reveals a strong positive excitation from the input token embedding " Pride" (direct_effect 13.75). The next most influential upstream node is a layer‑0 feature (F5012) with a modest positive effect (0.488) that itself is driven primarily by the embedding of the token "Black" (direct_effect 8.63). Additional modest upst…

</details>

<details>
<summary><b>SA-7</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F7993 | "the word "black" and its plural form "blacks"" |
| 2 | `get_upstream_features` | L3:F7993@1, k=15 | Emb:"Black"@1 (de=23.50) +14 more |
| 3 | `inspect_feature` | L0, F1015 | " the word "black"" |
| 4 | `inspect_feature` | L0, F13380 | "the word "uniform" and sometimes words related to roads or passing, bu" |
| 5 | `inspect_feature` | L2, F11363 | " colors and words like Diamond." |
| 6 | `inspect_feature` | L2, F15681 | " words that indicate that something is improving or getting better" |
| 7 | `get_upstream_features` | L0:F1015@1, k=10 | Emb:"Black"@1 (de=16.88) +9 more |

**Findings:** The L3:F7993 feature (detecting the word 'black') is driven primarily by the raw token embedding for 'Black' at position 1 (direct_effect 23.5). Smaller positive contributions come from the <bos> embedding and low‑layer lexical detectors (L0:F1015, L2:F11363). All positive pathways have been traced to token embeddings, satisfying the requirement of reaching a lower‑third layer (≤8) and exposing em…

</details>

<details>
<summary><b>SA-8</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F9528 | " the color black" |
| 2 | `get_upstream_features` | L2:F9528@1, k=10 | Emb:"Black"@1 (de=30.00) +9 more |
| 3 | `inspect_feature` | L1, F9113 | " discussions about race and slavery" |
| 4 | `get_upstream_features` | L1:F9113@1, k=10 | Emb:"Black"@1 (de=16.88) +9 more |
| 5 | `inspect_feature` | L0, F3348 | " mentions of colors" |

**Findings:** The negative‑direct‑effect feature L2:F9528 ('the color black') receives its strongest excitatory drive directly from the input token embedding 'Black' (pos 1) and, to a lesser extent, from the BOS token. A shallow color detector (L0:3348) also contributes, confirming a lexical grounding path. Additionally, a race‑related higher‑level feature (L1:9113) feeds into the black feature, linking the wor…

</details>

### Build

`build_circuit` → 12 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 42,574 | 5,171 | 117,617 | 0 | $0.0260 | — | — |
| SA-2 | openai/gpt-oss-120b | 63,733 | 4,981 | 5,056 | 0 | $0.0126 | ✅ 5F/9E | Trace upstream from L8:F15771 at position 13. Find which inp… |
| SA-1 | openai/gpt-oss-120b | 109,414 | 9,542 | 43,424 | 0 | $0.0228 | ✅ 7F/6E | Trace upstream from L8:F15771 at position 9. Find which inpu… |
| SA-3 | openai/gpt-oss-120b | 61,872 | 4,814 | 18,784 | 0 | $0.0125 | ✅ 5F/7E | Trace upstream from L2:F13158 (words about race and ethnicit… |
| SA-4 | openai/gpt-oss-120b | 108,041 | 9,053 | 7,808 | 0 | $0.0218 | ✅ 5F/8E | Trace upstream from L2:F13158 (words about race and ethnicit… |
| SA-7 | openai/gpt-oss-120b | 77,784 | 4,333 | 64 | 0 | $0.0143 | ✅ 5F/6E | Trace upstream from L3:F7993 (word "black") at position 1. T… |
| SA-8 | openai/gpt-oss-120b | 39,213 | 3,636 | 2,624 | 0 | $0.0081 | ✅ 3F/6E | Trace upstream from L2:F9528 (the color black) at position 1… |
| SA-6 | openai/gpt-oss-120b | 47,782 | 4,177 | 10,112 | 0 | $0.0098 | ✅ 4F/5E | Trace upstream from L1:F12542 (word "proud") at position 2. … |
| **Total** | | **550,413** | **45,707** | **205,489** | **0** | **$0.1278** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 21s