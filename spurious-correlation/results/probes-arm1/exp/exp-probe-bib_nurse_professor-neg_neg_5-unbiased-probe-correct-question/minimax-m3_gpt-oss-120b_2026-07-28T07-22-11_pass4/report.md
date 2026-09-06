# Circuit Oracle Report
**Date:** 2026-07-28 07:22:11 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by a deep stack of genuinely profession-relevant academic-credential features (Ph.D., B.A., M.B.A., university names, "research interests") — not gender markers — though one male-pronoun feature (L0:F1069) sits at the bottom of the circuit as a small secondary contributor.

**Confidence:** 7

**Reasoning:** The terminal supernode (`universities_degrees_l18_l20`, layer 19) contains L20:F14235 ("references to academic credentials and institutions", activated at pos 19/33/46, direct_effect=-0.056/-0.051/-0.044), L19:F2496 ("mentions of universities and degrees", activated at pos 19/33/46), and L18:F13805 ("Universities"). L19:F2496's promoted tokens are university names (UC, Cornell, UCLA, Duke, USC, etc.) and its top examples are nearly all degree-from-university sentences — exactly the profession-indicator pattern. Tracing upstream from L20:F14235@pos19 yields L17:F11003 ("university", promoted tokens = "University", "UNIVERSITY", "Univ", etc.) with direct_effect=34, then L17:F7973 ("phrases describing someone's education and the schools they attended", direct_effect=7.94) and L3:F4213 ("mentions of degree qualifications or awards"). Further upstream: L7:F14129 ("academic degrees, universities, and people associated with them", frac_nonzero=0.0042 — very specific, max activation on the "D" of "Ph.D."), L6:F2254 ("references to academic degrees", max on "Sc" of "M.Sc."), L5:F13801 ("abbreviations for degrees"), L2:F10852 ("academic titles and degrees", promoted tokens = "degree", "degrees", "PhD", "doctorate", frac_nonzero=0.008). The bottom of the chain reaches token-embedding nodes: "Ph" (pos 13, direct_effect=14), "D" (pos 15, direct_effect=9.6), "B" (pos 27, direct_effect=12.4), "A" (pos 29, direct_effect=9.2) — i.e., the literal "Ph.D." and "B.A." abbreviations — plus "from" (pos 19) and "research"/"interests" (pos 2-3). The gender feature L0:F1069 ("references to a male person... pronoun He/His", frac_nonzero=0.0078) does connect to L8:F11284 ("names, titles, universities, and research") and to the probe output, but its direct_effect is only +0.055 (and the top embedding contributor is "He" with direct_effect=35.75, a generic high-frequency word embedding rather than an encoded gender signal). The dominant signal in the circuit — by activation magnitude, depth, and direct_effect — is the academic-credential pathway: Ph.D. (pos 15), B.A. (pos 29-30), M.B.A. (pos 44-46), Harvard, Chicago, Stanford → L2 titles → L4-L6 degrees → L7 degrees+universities → L8 names+research → L9 Bachelor → L14/L17 university → L18-L20 universities/degrees → probe. The user's concern is partially supported (a male-pronoun feature is present and does feed the probe with positive sign) but is not the dominant mechanism: the credential features have higher activation, more nodes, deeper reach into the prompt, and chain through profession-specific early-layer features. The probe appears to learn the legitimate "academic biography" template rather than primarily relying on gender, though the male-pronoun feature's presence suggests some leakage of gender-statistical correlation.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: male pronouns (He/His) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: male pronouns (He/His) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 23 | Emb: male pronouns (He/His) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: 'Ph', 'D' (Ph.D. markers) and 'B' (B.A.) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: 'Ph', 'D' (Ph.D. markers) and 'B' (B.A.) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 27 | Emb: 'Ph', 'D' (Ph.D. markers) and 'B' (B.A.) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 29 | Emb: 'Ph', 'D' (Ph.D. markers) and 'B' (B.A.) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: 'research', 'interests', 'from' | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: 'research', 'interests', 'from' | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 19 | Emb: 'research', 'interests', 'from' | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Male pronoun / "He"/"His" detector |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 10 | Male pronoun / "He"/"His" detector |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 23 | Male pronoun / "He"/"His" detector |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 15 | Academic titles/degrees detector (L2) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 29 | Academic titles/degrees detector (L2) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 44 | Academic titles/degrees detector (L2) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L1:F10986](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) | 3 | Academic research words (L1) |  words related to academic research | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) |
| [L1:F10132](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) | 15 | Ph.D. abbreviation token (L1) |  the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") written as "D" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) |
| [L1:F14298](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14298) | 15 | Ph.D. abbreviation token (L1) | academic publications, papers, and citations | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14298) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 29 | Academic degrees detector (L4-L6) |  mentions of academic degrees | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L5:F13801](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) | 15 | Academic degrees detector (L4-L6) | abbreviations for degrees and mentions of educational attainment | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 15 | Academic degrees detector (L4-L6) | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 29 | Academic degrees detector (L4-L6) | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 44 | Academic degrees detector (L4-L6) | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 15 | Academic degrees & universities (L7) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 22 | Academic degrees & universities (L7) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 24 | Academic degrees & universities (L7) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 33 | Academic degrees & universities (L7) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 44 | Academic degrees & universities (L7) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 46 | Academic degrees & universities (L7) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L8:F11284](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) | 9 | Names / titles / universities / research (L8) |  words and phrases related to people's names, titles, universities, and research | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) |
| [L9:F988](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/988) | 29 | Bachelor / degree info (L9) |  information about academic degrees | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/988) |
| [L14:F3956](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3956) | 33 | University and education phrases (L14-L17) |  universities and degrees | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3956) |
| [L14:F3956](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3956) | 19 | University and education phrases (L14-L17) |  universities and degrees | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3956) |
| [L17:F11003](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) | 19 | University and education phrases (L14-L17) | university | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) |
| [L17:F11003](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) | 33 | University and education phrases (L14-L17) | university | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) |
| [L17:F11003](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) | 46 | University and education phrases (L14-L17) | university | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) |
| [L17:F7973](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7973) | 19 | University and education phrases (L14-L17) |  phrases describing someone's education and the schools they attended | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7973) |
| [L17:F7973](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7973) | 33 | University and education phrases (L14-L17) |  phrases describing someone's education and the schools they attended | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7973) |
| [L17:F7973](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7973) | 46 | University and education phrases (L14-L17) |  phrases describing someone's education and the schools they attended | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7973) |
| [L17:F11342](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11342) | 33 | University and education phrases (L14-L17) |  dates, especially years and sports-related terms | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11342) |
| [L18:F13805](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13805) | 19 | Universities and degrees (L18-L20) | Universities | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13805) |
| [L19:F2496](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2496) | 19 | Universities and degrees (L18-L20) |  mentions of universities and degrees | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2496) |
| [L19:F2496](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2496) | 33 | Universities and degrees (L18-L20) |  mentions of universities and degrees | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2496) |
| [L19:F2496](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2496) | 46 | Universities and degrees (L18-L20) |  mentions of universities and degrees | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2496) |
| [L20:F14235](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) | 19 | Universities and degrees (L18-L20) |  references to academic credentials and institutions. | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) |
| [L20:F14235](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) | 33 | Universities and degrees (L18-L20) |  references to academic credentials and institutions. | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) |
| [L20:F14235](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) | 46 | Universities and degrees (L18-L20) |  references to academic credentials and institutions. | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L8:2383 de=-0.090 |
| 3 | `inspect_feature` ×12 | L8:2383, L0:6051, L6:14747, L2:10852, L1:10986, L7:14129, L8:11284, L20:14235, L0:1069, L14:3956, L1:1505, L9:988 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L20:F14235@19` | ❌ error | — | — | Trace the L20:F14235 (academic credentials/institutions, fired at pos 19 "Ph.D. … |
| SA-2 | `L7:F14129@15` | ❌ error | — | — | Trace L7:F14129 (academic degrees/universities, fired at pos 15 "Ph.D.") upstrea… |
| SA-3 | `L0:F1069@1` | ❌ error | — | — | Trace L0:F1069 (male pronoun "He"/"His", fired at pos 1 "His") upstream to embed… |
| SA-4 | `L1:F10986@3` | ❌ error | — | — | Trace L1:F10986 (academic research words, fired at pos 3 "research") upstream to… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F1069@1, k=8 → Emb:"His"@1 (de=21.62) +7 more |
| 2 | `get_upstream_features` | L1:F10986@3, k=8 → Emb:" research"@2 (de=6.62) +7 more |
| 3 | `get_upstream_features` | L7:F14129@15, k=8 → L6:F2254 (de=7.09) +7 more |
| 4 | `get_upstream_features` | L20:F14235@19, k=8 → L17:F11003 (de=34.00) +7 more |
| 5 | `inspect_feature` ×2 | L17:11003, L19:2496 |
| 6 | `get_upstream_features` | L17:F11003@19, k=8 → Emb:"<bos>"@0 (de=-6.72) +7 more |
| 7 | `get_upstream_features` | L7:F14129@33, k=8 → L5:F5725 (de=-2.70) +7 more |
| 8 | `get_upstream_features` | L19:F2496@19, k=6 → L17:F11003 (de=15.69) +5 more |
| 9 | `get_upstream_features` | L7:F14129@46, k=6 → L6:F2254 (de=3.75) +5 more |
| 10 | `get_upstream_features` | L9:F988@29, k=6 → L6:F2254 (de=5.50) +5 more |
| 11 | `get_upstream_features` | L14:F3956@33, k=6 → Emb:"<bos>"@0 (de=-5.06) +5 more |
| 12 | `inspect_feature` ×5 | L6:2254, L5:13801, L1:10132, L18:13805, L4:3727 |
| 13 | `get_upstream_features` | L7:F14129@20, k=5 → ❌ Feature (layer=7, feature_idx=14129) not found at pos=20. Th |
| 14 | `get_upstream_features` | L20:F14235@33, k=5 → L17:F11003 (de=23.62) +4 more |
| 15 | `get_upstream_features` | L20:F14235@46, k=5 → L17:F11003 (de=19.12) +4 more |
| 16 | `get_upstream_features` | L17:F11003@19, k=5 → Emb:"<bos>"@0 (de=-6.72) +4 more |
| 17 | `get_upstream_features` | L7:F14129@19, k=5 → L5:F11028 (de=4.56) +4 more |
| 18 | `get_upstream_features` | L6:F2254@15, k=5 → L2:F10852 (de=12.31) +4 more |
| 19 | `get_upstream_features` | L6:F2254@29, k=5 → L5:F5725 (de=-18.88) +4 more |
| 20 | `get_upstream_features` | L6:F2254@44, k=5 → L2:F10852 (de=10.50) +4 more |
| 21 | `inspect_feature` ×3 | L3:4213, L17:7973, L17:11342 |
| 22 | `get_upstream_features` | L2:F10852@15, k=5 → Emb:" Ph"@13 (de=14.00) +4 more |
| 23 | `get_upstream_features` | L2:F10852@29, k=5 → Emb:" B"@27 (de=12.38) +4 more |
| 24 | `inspect_feature` ×2 | L1:14298, L8:11284 |
| 25 | `get_upstream_features` | L0:F1069@3, k=5 → ❌ Feature (layer=0, feature_idx=1069) not found at pos=3. This |
| 26 | `get_upstream_features` | L0:F1069@8, k=5 → ❌ Feature (layer=0, feature_idx=1069) not found at pos=8. This |
| 27 | `get_upstream_features` | L0:F1069@10, k=5 → Emb:" He"@10 (de=35.75) +4 more |
| 28 | `get_upstream_features` | L0:F1069@23, k=5 → Emb:" He"@23 (de=36.75) +4 more |
| 29 | `get_upstream_features` | L7:F14129@22, k=5 → Emb:"."@22 (de=-2.02) +4 more |
| 30 | `get_upstream_features` | L7:F14129@24, k=5 → L0:F10846 (de=2.61) +4 more |
| 31 | `get_upstream_features` | L8:F11284@9, k=5 → Emb:" research"@2 (de=3.89) +4 more |
| 32 | `inspect_feature` ×2 | L0:16067, L0:6051 |

### Build

`build_circuit` → 14 nodes, 20 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 65,812 | 7,332 | 591,841 | 0 | $0.0641 | — | — |
| **Total** | | **65,812** | **7,332** | **591,841** | **0** | **$0.0641** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 45s