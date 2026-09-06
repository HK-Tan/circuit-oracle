# Circuit Oracle Report
**Date:** 2026-07-28 07:22:34 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's positive score is driven by a mixture of (a) genuine profession/academic-degree indicators (BS, PhD, "from", "university", "research interests") and (b) the male-pronoun "He/His" used as a coreference anchor for the subject — but the male-pronoun signal is not acting as a spurious gender cue; it functions as a generic subject reference that the probe inherits from training-corpus statistics about Wikipedia biographies of male academics.

**Confidence:** 6

**Reasoning:** The attribution graph reveals two parallel pathways into the output logit:

**1. Genuine profession/degree pathway (dominant).** The "emb_bs" / "emb_phd" / "emb_from_bs" / "emb_from_phd" token embeddings flow into mid-layer degree-detector features. L2:F10852 ("academic titles and degrees", frac_nonzero 0.008) and L6:F2254 ("references to academic degrees", frac_nonzero 0.004) both fire on "BS" (pos 17) and "PhD" (pos 27), promoted-token set includes "▁degree", "▁PhD", "▁doctorate". These feed L7:F14129 ("degrees, universities, and people", frac_nonzero 0.004, activation 50, direct_effect +0.04) at "PhD", which then feeds L19:F2496 ("mentions of universities and degrees", frac_nonzero 0.038, direct_effect +0.037) and L17:F11003 ("university" token, direct_effect +0.057 feeding the L20:F14235). L3:F4213 ("mentions of degree qualifications or awards") also fires on "from" at pos 21 (direct_effect +0.035) and is driven directly by the "from" and "BS" embeddings. This is exactly the kind of evidence a profession classifier should use.

**2. "His/He" pronoun pathway.** "emb_his" at pos 1 has a very large direct_effect (+21.6) into L0:F1069 ("references to a male person, particularly when using the pronoun 'He' or 'His'", frac_nonzero 0.008, direct_effect +0.07) and into L2:F3877 ("references to 'His' and religious figures or concepts", frac_nonzero 0.007, direct_effect +0.035). Both connect to L1:F10986 ("words related to academic research") and L2:F1621 ("information about people's education and career"), which fire on "interests" (pos 3) and are also fed by "emb_research" and "emb_interests" embeddings.

**Assessment of the user's concern.** L0:F1069 is *labeled* as a male-pronoun feature, but it is also co-extensive with the "subject of a Wikipedia-style biography" pattern: its top-activating examples are all biographical prose about men ("He agrees…", "He was a …", "He later gains…"). The same token position feeds the degree-recognizing supernodes. So the circuit does contain a male-gender detector, but it is *entangled* with — not separable from — the profession signal. The "He/His" features are plausibly functioning as coreference anchors for the academic-career features downstream (L2:F1621 "education and career", L3:F4213 "degree qualifications"); a female-pronoun equivalent biography would activate a different L0 pronoun feature but could still drive L1:F10986 and L2:F1621 through the " research interests" tokens. The evidence is therefore *consistent with* the probe relying on genuine profession markers (degrees, university, research interests) with the pronoun acting as a co-occurring demographic side-channel that is hard for the probe to fully discount, but the dominant causal mass flows through degree/university features rather than gender features.

The two negative direct_effects at L0:F10783 (pos 4, "include") and L0:F2994 (pos 1, "His") and the negative L8:F11284 at pos 13 are countervailing signals that slightly suppress the probe's score — these come from generic token-shape features that are not profession-specific.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Early: Male pronoun 'He/His' (L0:F1069, L2:F3877) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L2:F3877](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3877) | 1 | Early: Male pronoun 'He/His' (L0:F1069, L2:F3877) |  references to "His" and religious figures or concepts | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3877) |
| [L1:F10986](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) | 3 | Early: Academic research/education words (L1:F10986, L2:F1621) |  words related to academic research | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) |
| [L2:F1621](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1621) | 3 | Early: Academic research/education words (L1:F10986, L2:F1621) |  information about people's education and career | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1621) |
| [L4:F9757](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) | 1 | Early: Generic token-shape/scientific-data feature (L4:F9757) | various acronyms, IDs, and symbols, possibly related to scientific data | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) |
| [L5:F12330](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12330) | 13 | Mid: 'College' with place name (L5:F12330) | mentions of "College" along with a preceding place name like "County" or "Valley" | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12330) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 17 | Mid: Academic degrees/titles (L2:F10852, L6:F2254) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 27 | Mid: Academic degrees/titles (L2:F10852, L6:F2254) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 17 | Mid: Academic degrees/titles (L2:F10852, L6:F2254) | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 27 | Mid: Academic degrees/titles (L2:F10852, L6:F2254) | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L3:F4213](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) | 21 | Mid: Degree qualifications/awards (L3:F4213) |  mentions of degree qualifications or awards | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 27 | Mid: Degrees, universities, and people (L7:F14129) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L19:F2496](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2496) | 31 | Late: Universities and degrees (L19:F2496) |  mentions of universities and degrees | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2496) |
| [L17:F11003](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) | 31 | Late: 'university' token (L17:F11003) | university | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:1069 de=0.070 |
| 3 | `inspect_feature` ×8 | L0:1069, L1:10986, L5:12330, L4:9757, L2:1621, L0:6446, L2:3877, L3:4213 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F1069@1` | ❌ error | — | — | Trace this L0:F1069 (male pronoun "He"/"His") feature upstream to its source. Wh… |
| SA-2 | `L2:F3877@1` | ❌ error | — | — | Trace this L2:F3877 (His + religious) upstream to its source. What does it encod… |
| SA-3 | `L1:F10986@3` | ❌ error | — | — | Trace L1:F10986 (academic research words) upstream. What is its source? It fires… |
| SA-4 | `L2:F1621@3` | ❌ error | — | — | Trace L2:F1621 (education/career) upstream. Position 3. Reach embeddings. |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F1069@1, k=10 → Emb:"His"@1 (de=21.62) +9 more |
| 2 | `get_upstream_features` | L1:F10986@3, k=10 → Emb:" research"@2 (de=6.62) +9 more |
| 3 | `get_upstream_features` | L2:F3877@1, k=10 → Emb:"His"@1 (de=20.88) +9 more |
| 4 | `get_upstream_features` | L2:F1621@3, k=10 → Emb:" interests"@3 (de=6.53) +9 more |
| 5 | `get_upstream_features` | L5:F12330@13, k=10 → Emb:"<bos>"@0 (de=-3.23) +9 more |
| 6 | `get_upstream_features` | L4:F9757@1, k=10 → Emb:"<bos>"@0 (de=16.50) +9 more |
| 7 | `get_upstream_features` | L3:F4213@21, k=10 → Emb:" from"@21 (de=11.19) +9 more |
| 8 | `get_upstream_features` | L0:F6446@3, k=10 → Emb:" interests"@3 (de=9.06) +9 more |
| 9 | `get_upstream_features` | L7:F14129@27, k=5 → Emb:" PhD"@27 (de=19.25) +4 more |
| 10 | `get_upstream_features` | L20:F14235@31, k=5 → L17:F11003 (de=30.38) +4 more |
| 11 | `get_upstream_features` | L7:F14129@17, k=5 → ❌ Feature (layer=7, feature_idx=14129) not found at pos=17. Th |
| 12 | `get_upstream_features` | L17:F11003@31, k=3 → Emb:" PhD"@27 (de=9.50) +2 more |
| 13 | `get_upstream_features` | L6:F2254@27, k=3 → Emb:" PhD"@27 (de=22.00) +2 more |
| 14 | `get_upstream_features` | L6:F2254@17, k=3 → Emb:" BS"@17 (de=18.38) +2 more |
| 15 | `inspect_feature` ×5 | L2:10852, L6:2254, L7:14129, L19:2496, L17:11003 |

### Build

`build_circuit` → 17 nodes, 22 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 32,723 | 5,160 | 167,420 | 0 | $0.0261 | — | — |
| **Total** | | **32,723** | **5,160** | **167,420** | **0** | **$0.0261** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 2s