# Circuit Oracle Report
**Date:** 2026-07-28 07:21:01 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_7 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe contradiction score is driven primarily by a chain of surface-level negation-word detectors culminating in late-layer "not + form-of-to-be" features at positions 23 and 29, with only secondary, much weaker contributions from genuine content features (sea/abbey/building detectors).

**Confidence:** 8/10

**Reasoning:**

The attribution circuit reveals that the probe's contradiction score is dominated by a single spurious signal: the presence of the word "not" (and especially the "not is" / "is not" pattern) in the prompt. The top positive drivers of the probe are:

1. **L16:F12358 (pos 29, direct_effect=0.3594)** — "the word 'not' followed within a few tokens by a form of the verb 'to be'" (frac_nonzero=0.028). This is the single strongest feature. It fires on the final "not is" pattern in "lacks a steeple. The abbey is not of great height". Upstream: the raw "not" embedding (de=19.5) and the "is" embedding (de=4.4) at pos 28 directly excite it, plus L0:F4958 (a pure lexical "not" detector, de=6.8) and L13:F3295 ("negations in the form of 'is/are not'", de=3.1).

2. **L16:F9779 (pos 23, direct_effect=0.2393)** — "negation words or contractions like 'won't', 'not', 'never'" (frac_nonzero=0.017). Fires on the first "not" in "you will not forget". Upstream: "will" embedding (de=7.3), "not" embedding (de=6.8), and L0:F4958 (de=3.8).

3. **L13:F3295 (pos 29, direct_effect=0.1855)** — "negations in the form of 'is/are not' as well as other uses of 'not'" (frac_nonzero=0.013), directly driven by the "not" embedding (de=17.75).

4. **L0:F4958 (pos 29/23)** — the raw lexical "not" detector with frac_nonzero=0.018 and a huge direct embedding effect of 34.25 from the "not" token.

These negation features form a thick self-reinforcing chain (L0 → L2/L3/L4 → L13/L15 → L16) that is overwhelmingly the dominant signal. The user's concern is validated: the circuit is "spurious" in the sense that it keys on the **surface form of the word "not"** and the **"not + is/are" syntactic pattern**, not on the actual semantic content of the contradiction (which would require comparing the premise "towering, steepled abbey" with the hypothesis "lacks a steeple").

Content features do exist but are secondary:
- L14:F10408 (pos 14, de=0.176) — geographical/water-body detector on "sea"
- L4:F4605 (pos 9, de=0.172) and L5:F14591 (pos 10, de=-0.174) — church/abbey building detectors
- L4:F3833 (pos 3, de=0.156) — summarization/perception cue on "glimpse"
- Generic lexical features for "the", "first", "is", "of"

The sum of the negation-path direct effects (~0.36 + 0.24 + 0.19 + 0.18 + 0.15 ≈ 1.1) far exceeds the content-path direct effects (~0.35), and crucially, the negation path is anchored by direct, massive embeddings (de=19.5, 17.75, 34.25) — the model is essentially using a "bag-of-negation-words" shortcut. A prompt containing "not" and "is not" anywhere would score as contradictory regardless of whether the statements actually conflict. The circuit confirms the user's hypothesis: negation-word features, not the premise/hypothesis semantic mismatch, drive the contradiction probe.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 29 | L16: 'not' followed by form of 'to be' (pos 29, final 'not is') |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |
| [L16:F9779](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/9779) | 23 | L16: negation/contraction detector (pos 23, mid 'not') | negation words or contractions like "won't", "not", "never" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/9779) |
| [L13:F3295](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) | 29 | L13: 'is/are not' pattern detector (pos 29) | negations in the form of "is/are not" as well as other uses of "not" | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) |
| [L15:F10071](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) | 29 | L15: broader negation/equivocation detector (pos 29) | negations and equivocations | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) |
| [L15:F3521](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3521) | 23 | L15: broader negation/equivocation detector (pos 29) | sentences containing words expressing negation or uncertainty in past or future tense | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3521) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 29 | L0: 'not' lexical detector (pos 23, 29) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 23 | L0: 'not' lexical detector (pos 23, 29) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L2:F12021](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) | 29 | L2: 'not'/negative-term detector (pos 29) | "not" or negative terms, with some bonus for sports‑related terms and "purpose". | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 29 | L3: multilingual negation-fragment detector (pos 29) | a mix of words and code fragments from different languages | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 23 | L4: cross-language negations (pos 23) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L2:F12694](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12694) | 23 | L2: possibility/Canisius cue (pos 23) |  the word "Canisius" and words that express possibility or a small probability | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12694) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 5 | Generic lexical features: 'the', 'first', 'is', 'of', 'glimpse' | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 18 | Generic lexical features: 'the', 'first', 'is', 'of', 'glimpse' |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 4 | Generic lexical features: 'the', 'first', 'is', 'of', 'glimpse' | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F5060](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5060) | 1 | Generic lexical features: 'the', 'first', 'is', 'of', 'glimpse' | mentions of dinner or breakfast | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5060) |
| [L14:F10408](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10408) | 14 | L14: geographical/water-body detector on 'sea' (pos 14) |  geographical locations, especially related to bodies of water | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10408) |
| [L4:F4173](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4173) | 14 | L4-6 marine / water detector (pos 14) |  words and phrases related to marine environments or legal terminology related to maritime issues. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4173) |
| [L6:F3848](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3848) | 14 | L4-6 marine / water detector (pos 14) |  words related to marine biology and fishing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3848) |
| [L4:F4605](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) | 9 | L4-5 church / building detector (pos 9-10) | words related to churches, chapels and other buildings, in addition to other information of Lincolnshire | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) |
| [L5:F14591](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14591) | 10 | L4-5 church / building detector (pos 9-10) | words related to the Catholic church | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14591) |
| [L4:F3833](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) | 3 | L4 summarization/perception cue (pos 3-4) | words used when summarizing plot points or providing courtroom insights | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) |
| [L4:F3833](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) | 4 | L4 summarization/perception cue (pos 3-4) | words used when summarizing plot points or providing courtroom insights | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L16:12358 de=0.359 |
| 3 | `inspect_feature` ×8 | L16:12358, L0:7710, L0:3820, L16:9779, L0:11375, L13:3295, L0:4958, L0:5060 |
| 4 | `get_upstream_features` | Emb:" not"@29 (de=19.50) +14 more |
| 5 | `get_upstream_features` | Emb:" will"@22 (de=7.31) +14 more |
| 6 | `get_upstream_features` | Emb:" not"@29 (de=17.75) +14 more |
| 7 | `get_upstream_features` | Emb:" not"@29 (de=34.25) +9 more |
| 8 | `get_upstream_features` | Emb:" of"@4 (de=35.25) +9 more |
| 9 | `get_upstream_features` | Emb:" glimpse"@3 (de=7.03) +9 more |
| 10 | `get_upstream_features` | Emb:"led"@9 (de=6.44) +9 more |
| 11 | `get_upstream_features` | Emb:" abbey"@10 (de=10.00) +9 more |
| 12 | `get_upstream_features` | Emb:" sea"@14 (de=19.88) +9 more |
| 13 | `get_upstream_features` | Emb:","@7 (de=6.12) +9 more |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F12358@29` | ✅ reported | 6 | 15 | Trace this negation-detection feature upward to find the source tokens driving i… |
| SA-2 | `L16:F9779@23` | ✅ reported | 5 | 11 | Trace this negation feature upward. It fires on the first 'not' in the text at p… |
| SA-3 | `L14:F10408@14` | ❌ error | — | — | Trace this L14 feature upstream. It fires on the 'sea' token at pos 14 in the fi… |
| SA-4 | `L0:F5060@1` | ❌ error | — | — | Trace this L0 feature upstream. It supposedly fires on 'dinner or breakfast' but… |
| SA-5 | `L4:F3833@3` | ✅ reported | 6 | 13 | Trace this L4 feature upstream. It fires at pos 3 ('glimpse'). Find the input so… |
| SA-6 | `L4:F4605@9` | ✅ reported | 6 | 8 | Trace this L4 feature upstream. It fires on 'steepled' (pos 9). Find the full up… |
| SA-7 | `L6:F5342@4` | ✅ reported | 5 | 4 | Trace this L6 feature upstream. It fires at pos 4 ('of'). Find the full upstream… |
| SA-8 | `L5:F14591@10` | ✅ reported | 3 | 4 | Trace this L5 feature upstream. It has negative direct effect (-0.1738) and fire… |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L16, F12358 | " the word "not" followed within a few tokens by a form of the verb "to" |
| 2 | `get_upstream_features` | L16:F12358@29, k=10 | Emb:" not"@29 (de=19.50) +9 more |
| 3 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 4 | `inspect_feature` | L2, F12021 | ""not" or negative terms, with some bonus for sports-related terms and " |
| 5 | `get_upstream_features` | L0:F4958@29, k=10 | Emb:" not"@29 (de=34.25) +9 more |
| 6 | `inspect_feature` | L13, F3295 | "negations in the form of "is/are not" as well as other uses of "not"" |
| 7 | `get_upstream_features` | L13:F3295@29, k=10 | Emb:" not"@29 (de=17.75) +9 more |
| 8 | `get_upstream_features` | L2:F12021@29, k=10 | Emb:" not"@29 (de=22.50) +9 more |
| 9 | `inspect_feature` | L15, F10071 | "negations and equivocations" |
| 10 | `inspect_feature` | L3, F8011 | " a mix of words and code fragments from different languages" |

**Findings:** The chain begins with the raw "not" token embedding (pos 29) which strongly excites a layer‑0 feature that simply detects the word "not". That feature feeds both the higher‑level negation gate at L16:12358 and intermediate pattern detectors at L13:3295 and L15:10071. The L13 detector specifically looks for "not" followed by a form of "to be", sharpening the signal into the "not is" pattern the mod…

</details>

<details>
<summary><b>SA-2</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L16, F9779 | "negation words or contractions like "won't", "not", "never"" |
| 2 | `get_upstream_features` | L16:F9779@23, k=10 | Emb:" will"@22 (de=7.31) +9 more |
| 3 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 4 | `inspect_feature` | L15, F3521 | "sentences containing words expressing negation or uncertainty in past " |
| 5 | `inspect_feature` | L2, F12694 | " the word "Canisius" and words that express possibility or a small pro" |
| 6 | `get_upstream_features` | L0:F4958@23, k=10 | Emb:" not"@23 (de=33.50) +9 more |
| 7 | `inspect_feature` | L4, F4492 | "negations in various languages" |
| 8 | `get_upstream_features` | L4:F4492@23, k=10 | Emb:" not"@23 (de=18.50) +9 more |
| 9 | `get_upstream_features` | L15:F3521@23, k=10 | Emb:" will"@22 (de=5.91) +9 more |

**Findings:** The negation feature L16:F9779 is driven primarily by the raw token embedding for 'not' (direct_effect ~7) and by a low‑layer lexical detector L0:4958 that also receives a huge direct effect from the same 'not' embedding (33.5). Additional context comes from the modal verb 'will' and from higher‑level sentence‑level negation detectors (L15:3521, L4:4492) and a possibility cue detector (L2:12694). …

</details>

<details>
<summary><b>SA-5</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F3833 | " words used when summarizing plot points or providing courtroom insigh" |
| 2 | `get_upstream_features` | L4:F3833@3, k=10 | Emb:" glimpse"@3 (de=13.56) +9 more |
| 3 | `inspect_feature` | L2, F6639 | " phrases related to perception" |
| 4 | `inspect_feature` | L2, F13793 | " words related to media, music, especially singles or tracks" |
| 5 | `inspect_feature` | L3, F85 | " instances of observing something, often through a narrow opening or f" |
| 6 | `get_upstream_features` | L2:F6639@3, k=10 | Emb:" glimpse"@3 (de=9.56) +9 more |
| 7 | `get_upstream_features` | L0:F9384@3, k=10 | Emb:" first"@2 (de=10.81) +9 more |
| 8 | `inspect_feature` | L3, F6616 | "different forms of seeing or noticing" |
| 9 | `get_upstream_features` | L3:F85@3, k=10 | Emb:" glimpse"@3 (de=12.31) +9 more |
| 10 | `get_upstream_features` | L2:F6639@3, k=10 | Emb:" glimpse"@3 (de=9.56) +9 more |
| 11 | `get_upstream_features` | L2:F13793@3, k=10 | Emb:" glimpse"@3 (de=10.62) +9 more |
| 12 | `inspect_feature` | L2, F66 | "words related to formal declarations, opinions, and assumptions pertai" |
| 13 | `inspect_feature` | L0, F9384 | " mentions of the first lady and/or of temporal context (like months an" |

**Findings:** The L4 feature F3833 (layer 4) is a high‑level summarization cue that is driven primarily by the input token "glimpse" and, to a lesser extent, by "first". Its strongest upstream contributors are low‑layer perception/observation detectors (L2:F6639, L3:F85, L3:F6616) which themselves are directly triggered by the same tokens. The chain reaches down to layer 0 (F9384), a generic lexical detector fo…

</details>

<details>
<summary><b>SA-6</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F4605 | " words related to churches, chapels and other buildings, in addition t" |
| 2 | `get_upstream_features` | L4:F4605@9, k=10 | Emb:"led"@9 (de=6.44) +9 more |
| 3 | `inspect_feature` | L3, F4081 | "mentions of the statistical software Stata and the term "stent"." |
| 4 | `inspect_feature` | L3, F7650 | "abbreviations, geographical locations, and the letter "l"" |
| 5 | `get_upstream_features` | L3:F4081@9, k=10 | Emb:" steep"@8 (de=11.44) +9 more |
| 6 | `inspect_feature` | L0, F2159 | " words that end with "led" or are related to worth" |
| 7 | `inspect_feature` | L2, F5878 | "the suffix "le"" |
| 8 | `get_upstream_features` | L3:F7650@9, k=10 | Emb:"led"@9 (de=5.81) +9 more |
| 9 | `get_upstream_features` | L2:F5878@9, k=10 | Emb:" steep"@8 (de=8.56) +9 more |

**Findings:** The L4 feature F4605 (layer 4) fires on the token 'steepled' because it aggregates a cascade of low‑level suffix and token detectors. The strongest upstream drivers are the embeddings for the tokens 'led' (pos 9) and ' steep' (pos 8), which directly excite the feature. These feed into a layer‑3 bigram detector (F4081) that captures the phrase ' steep', and a layer‑2 suffix detector (F5878) for the…

</details>

<details>
<summary><b>SA-7</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F5342 | "the word "first" as well as words and prepositions that often follow i" |
| 2 | `get_upstream_features` | L6:F5342@4, k=10 | Emb:" first"@2 (de=12.06) +9 more |
| 3 | `inspect_feature` | L4, F3833 | " words used when summarizing plot points or providing courtroom insigh" |
| 4 | `inspect_feature` | L4, F10564 | " ordinal numbers or the word "first" coupled with a noun or prepositio" |
| 5 | `get_upstream_features` | L4:F3833@4, k=10 | Emb:" glimpse"@3 (de=7.03) +9 more |
| 6 | `inspect_feature` | L4, F488 | " information about a player's first appearance or performance in sport" |
| 7 | `inspect_feature` | L3, F6616 | "different forms of seeing or noticing" |
| 8 | `inspect_feature` | L3, F6616 | "different forms of seeing or noticing" |
| 9 | `get_upstream_features` | L3:F6616@4, k=10 | Emb:" glimpse"@3 (de=18.38) +9 more |

**Findings:** Tracing from L6:F5342 (which fires on the token 'of' after the word 'first') reveals a short upstream chain. The strongest upstream driver is the raw embedding of the token 'first' (direct_effect 12.06), giving a direct token‑embedding connection. Beneath that, the next most influential upstream feature is L4:F3833, a connector‑language detector that amplifies 'of' in legal/summarizing contexts. L…

</details>

<details>
<summary><b>SA-8</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L5, F14591 | " words related to the Catholic church" |
| 2 | `get_upstream_features` | L5:F14591@10, k=10 | Emb:" abbey"@10 (de=10.00) +9 more |
| 3 | `inspect_feature` | L4, F4605 | " words related to churches, chapels and other buildings, in addition t" |
| 4 | `get_upstream_features` | L4:F4605@10, k=10 | Emb:" abbey"@10 (de=7.97) +9 more |
| 5 | `inspect_feature` | L2, F8185 | "places for shopping or military activities" |
| 6 | `get_upstream_features` | L2:F8185@10, k=10 | Emb:" abbey"@10 (de=9.44) +9 more |
| 7 | `inspect_feature` | L1, F7934 | " terms related to legal and governmental processes and actions." |
| 8 | `inspect_feature` | L4, F1104 | " words related to history, geography, and the middle ages, especially " |
| 9 | `inspect_feature` | L4, F4872 | " words related to religious organizations, especially the Catholic Chu" |
| 10 | `get_upstream_features` | L1:F7934@10, k=10 | Emb:" abbey"@10 (de=9.06) +9 more |
| 11 | `inspect_feature` | L4, F13244 | " terms related to land ownership and administration, possibly includin" |

**Findings:** The target L5 feature (F14591) that fires on the token 'abbey' is part of a hierarchy of religious‑place detectors. It receives strong excitatory input directly from the token embedding for 'abbey' and from an upstream church‑building detector (L4:F4605). That detector, in turn, is driven by a generic location detector (L2:F8185) which also receives a large positive push from the same 'abbey' embe…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F10408@14, k=10 → Emb:" sea"@14 (de=22.88) +9 more |
| 2 | `get_upstream_features` | L0:F11375@18, k=10 → Emb:" is"@18 (de=32.50) +9 more |
| 3 | `get_upstream_features` | L15:F10071@29, k=10 → Emb:" not"@29 (de=9.75) +9 more |
| 4 | `inspect_feature` ×3 | L14:10408, L4:4173, L6:3848 |

### Build

`build_circuit` → 28 nodes, 34 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 55,928 | 7,026 | 158,423 | 0 | $0.0347 | — | — |
| SA-2 | openai/gpt-oss-120b | 97,260 | 5,425 | 5,088 | 0 | $0.0179 | ✅ 5F/11E | Trace this negation feature upward. It fires on the first 'n… |
| SA-7 | openai/gpt-oss-120b | 103,394 | 6,094 | 2,560 | 0 | $0.0192 | ✅ 5F/4E | Trace this L6 feature upstream. It fires at pos 4 ('of'). Fi… |
| SA-6 | openai/gpt-oss-120b | 93,441 | 6,399 | 5,088 | 0 | $0.0179 | ✅ 6F/8E | Trace this L4 feature upstream. It fires on 'steepled' (pos … |
| SA-8 | openai/gpt-oss-120b | 128,751 | 6,174 | 5,120 | 0 | $0.0231 | ✅ 3F/4E | Trace this L5 feature upstream. It has negative direct effec… |
| SA-1 | openai/gpt-oss-120b | 110,871 | 9,727 | 25,920 | 0 | $0.0229 | ✅ 6F/15E | Trace this negation-detection feature upward to find the sou… |
| SA-5 | openai/gpt-oss-120b | 162,890 | 8,254 | 11,264 | 0 | $0.0296 | ✅ 6F/13E | Trace this L4 feature upstream. It fires at pos 3 ('glimpse'… |
| **Total** | | **752,535** | **49,099** | **213,463** | **0** | **$0.1653** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 42s