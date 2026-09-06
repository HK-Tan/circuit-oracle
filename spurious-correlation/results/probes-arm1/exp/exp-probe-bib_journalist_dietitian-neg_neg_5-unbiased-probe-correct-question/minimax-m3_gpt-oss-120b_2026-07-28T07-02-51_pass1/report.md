# Circuit Oracle Report
**Date:** 2026-07-28 07:02:51 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is strongly suppressed by a hierarchy of late-layer "reporter/journalism" features that originate from the single token "reporter" at the end of the passage, with smaller negative contributions from generic lexical detectors and one weak positive contribution from an "obtained" feature on the second token.

**Confidence:** 8

**Reasoning:** The dominant signal in the circuit is **not** a gender marker. The strongest suppressor is L14:F4420 (direct_effect = -0.1963) — labeled "words and phrases related to journalism and newspapers" (frac_nonzero=0.0165, specific) — which fires on pos 66 (the token "reporter") and promotes "journalist/journalistic/reporter" tokens. Its upstream L19:F2486 (direct_effect = -0.126, "journalistic sources and news outlets", frac_nonzero=0.0293) reinforces it. Both are excited from a journalism-detection cascade: L4:F13253 ("journalism and the media", frac_nonzero=0.0065) → L8:F8855 ("news reporters and news reporting", frac_nonzero=0.0085), all firing at pos 66. I traced L4:F13253 upstream and confirmed its primary driver is the **embedding node for the word "reporter" at pos 66** (direct_effect=+26.625) — so the signal truly originates from the explicit profession word "reporter", not from a spurious surface feature. L6:F12712 ("titles of editors and publishers in scientific publications", frac_nonzero=0.0175) also fires at pos 66 and pos 21 ("degree"), contributing -0.0815.

The user's hypothesis about gender-marker spuriousness is **not supported** by this graph. L0:F1069 — explicitly labeled "references to a male person, particularly when using the pronoun He or His" with max-activating examples dominated by "He" tokens — does fire at pos 1 (token "He"), but its direct_effect is only **-0.0889**, an order of magnitude smaller than the journalism features. It is a generic, broadly-firing L0 feature (frac_nonzero=0.0078, but its top-activating examples show it fires on essentially any "He" token regardless of profession). The remaining L0 features are even more generic: F8974 ("from"), F14824 ("has"), F8061 ("in"), F13864 ("ever"), F6051 ("punctuation/periods/1"), F4874 ("preparation"). These are pure lexical detectors for function words and punctuation, not profession or gender signals. F9397 ("technical jargon") and F8642 (promoted-token noise, weak +0.0938) are essentially background.

The only positively-acting feature is L0:F8642 (direct_effect=+0.0938) on "obtained" at pos 2 — and its autointerp ("mathematical or logical proofs"), top activating examples (all on the word "actually" in math text), and promoted tokens are noise/garbage, suggesting it is not a meaningful profession signal either. The net direction of the probe is therefore negative (i.e., the passage is being classified as *not* the target profession), driven by the model's strong detection of the explicit word "reporter" building up a coherent "journalism" representation in layers 4→8→14→19 that the probe direction treats as evidence *against* the target profession. The circuit is **content-driven by the profession word itself**, not by gender or other spurious correlates.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: He (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: obtained (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: from (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: in (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 22 | Emb: ever (pos 22) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 16 | Emb: has (pos 16) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 66 | Emb: reporter (pos 66) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | L0: Male pronoun detector 'He/His' (F1069) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F8974](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) | 9 | L0: Generic lexical detectors (prepositions, function words) | the word "from" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) |
| [L0:F14824](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) | 16 | L0: Generic lexical detectors (prepositions, function words) | the word "has" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) |
| [L0:F8061](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) | 6 | L0: Generic lexical detectors (prepositions, function words) |  the preposition "in" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) |
| [L0:F13864](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13864) | 22 | L0: Generic lexical detectors (prepositions, function words) | the word "ever," sometimes in conjunction with comparatives or superlatives | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13864) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 24 | L0: Generic lexical detectors (prepositions, function words) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F9397](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9397) | 21 | L0: Generic lexical detectors (prepositions, function words) |  jargon and terminology from technical documents | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9397) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 66 | L4: Journalism/media feature (F13253) | things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L6:F12712](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) | 21 | L6: Editor/publisher title (F12712) |  titles of editors and publishers in scientific publications | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) |
| [L6:F12712](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) | 66 | L6: Editor/publisher title (F12712) |  titles of editors and publishers in scientific publications | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 66 | L8: News reporter/reporting detector (F8855) |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 66 | L14: Strong journalism vocabulary feature (F4420) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 66 | L19: Reporter/journalistic-sources gate (F2486) | journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L0:F8642](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8642) | 2 | L0: L0:F8642 (pos 2) - weak positive contributor | words and symbols appearing in mathematical or logical proofs and conclusions. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8642) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:4420 de=-0.196 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@66` | ❌ error | — | — | Trace L14:F4420 at pos 66. This feature has direct_effect=-0.1963 (strongly supp… |
| SA-2 | `L19:F2486@66` | ✅ reported | 5 | 16 | Trace L19:F2486 at pos 66. direct_effect=-0.126, suppresses probe. What does thi… |
| SA-3 | `L4:F13253@66` | ❌ error | — | — | Trace L4:F13253 at pos 66. direct_effect=-0.1162. What does this early-layer fea… |
| SA-4 | `L0:F8642@2` | ❌ error | — | — | Trace L0:F8642 at pos 2. This is the ONLY positively-acting feature (direct_effe… |
| SA-5 | `L0:F8642@2` | ✅ reported | 4 | 2 | Trace L0:F8642 at pos 2. This is a positively-acting feature (direct_effect=+0.0… |

<details>
<summary><b>SA-2</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F2486 | " journalistic sources and news outlets." |
| 2 | `get_upstream_features` | L19:F2486@66, k=10 | Emb:" reporter"@66 (de=28.25) +9 more |
| 3 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 4 | `get_upstream_features` | L14:F4420@66, k=10 | Emb:" reporter"@66 (de=18.75) +9 more |
| 5 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 6 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 7 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 8 | `get_upstream_features` | L4:F13253@66, k=10 | Emb:" reporter"@66 (de=26.62) +9 more |
| 9 | `get_upstream_features` | L8:F8855@66, k=10 | Emb:" reporter"@66 (de=16.88) +9 more |

**Findings:** L19:F2486 is a high‑level suppression gate that reacts to a strong journalism signal. Its upstream cascade originates from the raw token embedding "reporter" (pos 66) and passes through a hierarchy of journalism‑focused features (L14:F4420, L4:F13253, L8:F8855, L7:F13646). All these intermediate features detect various aspects of news reporting, editors, and media outlets. The pattern shows the fe…

</details>

<details>
<summary><b>SA-5</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F8642 | "words and symbols appearing in mathematical or logical proofs and conc" |
| 2 | `get_upstream_features` | L0:F8642@2, k=10 | Emb:" obtained"@2 (de=12.06) +9 more |
| 3 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 4 | `get_top_logits` | k=5 | "" (100%) |
| 5 | `get_top_features` | token="He", k=10 | ❌ Token 'He' is not one of the top-k next-token candidates cap |
| 6 | `inspect_feature` | L0, F4874 | " the word "preparation" and words connected to it" |
| 7 | `inspect_feature` | L0, F6051 | "periods, spaces, and the number 1" |

**Findings:** L0:F8642 at token position 2 is driven almost entirely by the embedding of the word "obtained" (direct_effect ≈ +12). The feature itself recognises language typical of formal statements about obtaining something, not a refusal or safety signal. Upstream we also see a male‑pronoun detector (F1069) on the preceding token "He", a preparation‑related detector (F4874) and a generic punctuation/number d…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×11 | L0:4874, L0:8642, L0:1069, L0:6051, L0:8974, L0:14824, L0:8061, L0:13864, L0:9397, L6:12712, L8:8855 |
| 2 | `get_upstream_features` | L4:F13253@66, k=10 → Emb:" reporter"@66 (de=26.62) +9 more |
| 3 | `get_upstream_features` | L0:F1069@1, k=5 → Emb:"He"@1 (de=22.62) +4 more |
| 4 | `get_upstream_features` | L0:F8642@2, k=3 → Emb:" obtained"@2 (de=12.06) +2 more |

### Build

`build_circuit` → 16 nodes, 18 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 48,285 | 4,823 | 94,210 | 0 | $0.0259 | — | — |
| SA-2 | openai/gpt-oss-120b | 105,657 | 8,797 | 10,944 | 0 | $0.0213 | ✅ 5F/16E | Trace L19:F2486 at pos 66. direct_effect=-0.126, suppresses … |
| SA-5 | openai/gpt-oss-120b | 43,677 | 4,808 | 19,456 | 0 | $0.0097 | ✅ 4F/2E | Trace L0:F8642 at pos 2. This is a positively-acting feature… |
| **Total** | | **197,619** | **18,428** | **124,610** | **0** | **$0.0569** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 59s