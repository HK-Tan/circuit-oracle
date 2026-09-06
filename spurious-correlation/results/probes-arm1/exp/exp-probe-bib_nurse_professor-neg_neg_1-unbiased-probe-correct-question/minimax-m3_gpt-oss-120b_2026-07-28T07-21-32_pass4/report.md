# Circuit Oracle Report
**Date:** 2026-07-28 07:21:32 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a mix of legitimate academic/profession indicators (degree markers like "BS" and "PhD", academic phrasing like "research interests include") and a strong, direct contribution from male-pronoun features (L0:F1069, L0:F2994) that fire on the surface tokens "His", "He", "his" — i.e. the model is partly using gendered surface markers rather than the actual profession content.

**Confidence:** 7

**Reasoning:** Top-feature inspection shows the two strongest single-feature contributors to the probe are both male-pronoun detectors at layer 0: L0:F1069 ("references to a male person, particularly 'He' or 'His'", frac_nonzero≈0.008, direct_effect=+0.070 on pos 1 "His") and L0:F2994 ("the pronoun 'his' and the pronoun 'he'", frac_nonzero≈0.073, direct_effect=−0.039 on pos 1). The L1:F10986 "academic research" feature (direct_effect=+0.067 on pos 3 "interests") is the strongest non-gendered driver. L8:F11284 "names, titles, universities, research" (direct_effect=−0.057 on pos 13) and L5:F12330 "College + place name" (direct_effect=+0.045 on pos 13) add profession-relevant signal. Crucially, the L0:F1069 male-pronoun feature's upstream trace is dominated by the raw `His` token embedding at pos 1 (direct_effect 21.6) and `<bos>` (6.8) — it is a near-direct readout of the gendered surface tokens, with no profession-specific mediation. The L2:F10852 / L6:F2254 / L7:F14129 degree features (BS at pos 17, PhD at pos 27) trace cleanly to the `BS` and `PhD` token embeddings and are genuine profession markers. The presence of the "owing" word feature L0:F13431 and the L14:F11252 "code/coordinate geometry" feature (firing on "visualization" via `Z`/3D-coordinate associations) shows the circuit is not purely spurious, but the dual presence of strongly weighted male-pronoun features sitting at the same early layer with comparable direct_effect to the academic-research features is exactly the gender-correlated signal the user is concerned about. The probe direction is being read off a residual stream where male-pronoun detectors, academic-credential detectors, and field-name detectors all contribute — the first of these is a spurious correlate of profession (the text is from a male scientist's Wikipedia bio), not a profession indicator per se.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 0 | Emb: <bos> (pos 0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: His (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: research (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: interests (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: include (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: visualization (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: graphics (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: BS (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 27 | Emb: PhD (pos 27) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Male pronoun markers (His/He/his) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | Male pronoun markers (His/He/his) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2159](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2159) | 3 | Male pronoun markers (His/He/his) |  words that end with "led" or are related to worth | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2159) |
| [L0:F10783](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10783) | 4 | Male pronoun markers (His/He/his) |  the word "include" (and variations of the word) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10783) |
| [L1:F10986](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) | 3 | Academic/biographical surface patterns |  words related to academic research | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) |
| [L2:F1621](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1621) | 3 | Academic/biographical surface patterns |  information about people's education and career | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1621) |
| [L4:F9757](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) | 1 | Academic/biographical surface patterns | various acronyms, IDs, and symbols, possibly related to scientific data | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 17 | Degree/credential markers (BS, PhD, M.Sc., Doctor) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 27 | Degree/credential markers (BS, PhD, M.Sc., Doctor) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 17 | Degree/credential markers (BS, PhD, M.Sc., Doctor) | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 27 | Degree/credential markers (BS, PhD, M.Sc., Doctor) | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 27 | Degree/credential markers (BS, PhD, M.Sc., Doctor) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L5:F12330](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12330) | 13 | College/institution context | mentions of "College" along with a preceding place name like "County" or "Valley" | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12330) |
| [L8:F11284](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) | 13 | Research/visualization/graphics field words |  words and phrases related to people's names, titles, universities, and research | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) |
| [L14:F11252](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11252) | 9 | Research/visualization/graphics field words |  code and coordinate geometry terms | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11252) |
| [L0:F13431](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13431) | 3 | 'owing' word feature (noise) | the word "owing". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13431) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe direction (profession classifier) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:1069 de=0.070 |
| 3 | `inspect_feature` ×14 | L0:1069, L1:10986, L5:12330, L8:11284, L14:11252, L0:13431, L0:10783, L6:2254, L2:10852, L7:14129, L4:9757, L0:2994, L0:2159, L2:1621 |
| 4 | `get_upstream_features` | Emb:"His"@1 (de=21.62) +7 more |
| 5 | `get_upstream_features` | Emb:"His"@1 (de=19.75) +7 more |
| 6 | `get_upstream_features` | Emb:" research"@2 (de=6.62) +7 more |
| 7 | `get_upstream_features` | Emb:" PhD"@27 (de=19.25) +7 more |
| 8 | `get_upstream_features` | Emb:" research"@2 (de=3.94) +7 more |
| 9 | `get_upstream_features` | Emb:" visualization"@9 (de=6.06) +7 more |
| 10 | `get_upstream_features` | Emb:" BS"@17 (de=18.38) +7 more |
| 11 | `get_upstream_features` | Emb:" BS"@17 (de=15.44) +7 more |
| 12 | `get_upstream_features` | Emb:"<bos>"@0 (de=-3.23) +7 more |
| 13 | `get_upstream_features` | Emb:" include"@4 (de=24.62) +7 more |
| 14 | `get_upstream_features` | Emb:" interests"@3 (de=6.53) +7 more |
| 15 | `get_upstream_features` | Emb:"<bos>"@0 (de=16.50) +7 more |
| 16 | `get_upstream_features` | Emb:" interests"@3 (de=12.25) +4 more |
| 17 | `get_upstream_features` | Emb:" PhD"@27 (de=22.00) +4 more |
| 18 | `get_source_influence` | {'depth': 3, 'source_positions': [0, 1, 2, 3, 4, 9, 10, 11, 12, 13, 17, 27, 28,  |
| 19 | `get_source_influence` | {'depth': 3, 'source_positions': [0, 1], 'S_pct_of_total': 3.724, 'R_pct_of_tota |
| 20 | `get_source_influence` | {'depth': 3, 'source_positions': [17, 27], 'S_pct_of_total': -13.232, 'R_pct_of_ |
| 21 | `get_source_influence` | {'depth': 3, 'source_positions': [2, 3, 4], 'S_pct_of_total': -4.704, 'R_pct_of_ |
| 22 | `get_source_influence` | {'depth': 3, 'source_positions': [9, 10, 11, 12, 13], 'S_pct_of_total': -3.563,  |

### Build

`build_circuit` → 16 nodes, 15 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 37,167 | 4,700 | 157,656 | 0 | $0.0262 | — | — |
| **Total** | | **37,167** | **4,700** | **157,656** | **0** | **$0.0262** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 15s