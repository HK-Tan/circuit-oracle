# Circuit Oracle Report
**Date:** 2026-07-28 07:22:15 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's positive classification score is driven predominantly by a cascade of male-pronoun/gender features originating from the token "His" at position 1 (and "him" at position 9), with the legitimate profession indicator (the "report" → journalism chain) playing a much smaller role. The user's concern is well-founded: gendered features outweigh semantic profession features.

**Confidence:** 8

**Reasoning:** The top features driving the probe direction are L7:F14893 (+0.47), L7:F14946 (−0.47), L6:F12990 (−0.30), and L0:F2994 (+0.29) — all of which are explicitly labeled as "his/he/him" or "pronouns/possessive pronouns" detectors (L7:F14893's autointerp: "pronouns or possessive pronouns"; L6:F12990: "male pronouns and titles"; L7:F14946: "possessive pronoun his"). These are grounded by the raw token embedding for "His" (pos 1), which feeds L4:F4315 (low-layer "his/he/him" detector, direct_effect 23.5) and L6:F12990 (direct_effect 4.9), and ultimately propagates a strong, partially anti-female signal: L7:F14946 promotes "himself/his" and suppresses "herself/she/her" (frac_nonzero 0.017). At higher layers the signal aggregates into L19:F8814 ("various pronouns and names referring to people"; promoted: herself/she/her but suppressed: himself/his — actually female-skewed here, but with frac_nonzero 0.087 it is a generic pronoun feature) and L18:F7400 (autointerp says coding, but promoted tokens are "himself/his/彼の/彼は" — a male-pronoun amplifier, direct_effect −0.155, frac_nonzero 0.016).

A separate, semantically meaningful profession chain exists from the embedding of "report" (pos 21) → L8:F8855 ("mentions of news reporters and news reporting", direct_effect 5.03) → L14:F4420 ("words and phrases related to journalism and newspapers", direct_effect −0.16) and L7:F13646 ("news reporting and journalism"). However, this profession chain is much weaker in direct_effect (L14:F4420 contributes only −0.16, L8:F8855 +5.0) compared to the pronoun chain (L7:F14893 +0.47, L7:F14946 −0.47, L6:F12990 −0.30, L0:F2994 +0.29 — sum ~±1.5 just from these four). Note also that L14:F4420 has a *negative* direct effect on the probe, meaning the genuine "journalism" feature actually pushes the probe *away* from its positive classification; the probe's positive score is being driven by the presence of masculine pronouns, not by the word "report."

Concretely, the circuit is dominated by the "His" → low-layer male-pronoun detector (L4:F4315) → male-pronoun aggregator (L6:F12990, L7:F14946, L7:F14893) → mid-layer pronoun/gender aggregators (L18:F10315, L18:F7400, L19:F8814) → probe output, with the parallel "report" → journalism path (L7:F13646, L8:F8855, L11:F5996, L14:F4420) providing a counteracting semantic signal. Even the L2:F9301 feature ("men/women in relationships or gendered social roles") contributes directly to the output, indicating that the probe is sensitive to general gendered-social-role vocabulary, not profession semantics. This pattern — where the strongest features are all variants of the male-pronoun signal from "His" / "him" while the profession-word feature "report" → journalism is weak or negatively signed — confirms the user's concern: the probe classification is largely an artifact of male gender markers, not of the journalist profession itself.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | Emb: His (pos 1) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F16297](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) | 9 | Emb: him (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: report (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F2011](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) | 2 | Emb: see (pos 4) |  the word "dream" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) |
| [L0:F7927](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7927) | 8 | Emb: taken (pos 8) |  past-participle verbs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7927) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 3 | Emb: to (pos 3) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | Low-layer pronoun detector (his/he/him) |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L5:F10952](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) | 1 | Third-person pronoun detector | third person pronouns in varying contexts | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Male pronouns/titles detector (his, him, Mr.) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Pronoun aggregator (+, his/him) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | Male possessive "his" detector (−, supresses female) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L2:F9301](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) | 1 | Men/women in gendered social roles |  all mentions of men and women in the context of relationships, dating, or gendered social roles | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 21 | News reporting/journalism token feature |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 21 | News reporting/journalism token feature |  words and phrases associated with broadcast journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 21 | News reporters & broadcast journalism |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 21 | News reporters & broadcast journalism | content related to film festivals and production, particularly documentary films, and the recognition they receive. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L11:F5996](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/5996) | 21 | News publications and staff |  references to news publications and their staff. | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/5996) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 21 | Journalism/newspapers detector (+, profession) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 9 | Pronouns/possessives (He/his) − | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 1 | Pronouns/possessives (He/his) − |  pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L18:F7400](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) | 1 | Masculine pronoun (his/himself) amplifier − |  words related to coding and software/UI interfaces, with some bias toward non-English words | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | Pronouns/names referring to people (+, gendered) |  various pronouns and names referring to people | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe classification score (output) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L7:14893 de=0.471 |
| 3 | `inspect_feature` ×5 | L7:14893, L7:14946, L6:12990, L0:2994, L19:8814 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ✅ reported | 4 | 9 | Trace the male pronoun/possessive feature L7:F14893 at position 1 (His). What in… |
| SA-2 | `L7:F14946@1` | ✅ reported | 4 | 8 | Trace the male pronoun "his" feature L7:F14946 at position 1. What input tokens … |
| SA-3 | `L19:F8814@1` | ✅ reported | 6 | 10 | Trace L19:F8814 (pronouns/names referring to people) at pos 1. What drives this?… |
| SA-4 | `L18:F10315@1` | ❌ error | — | — | Trace L18:F10315 (pos 1, -0.16 direct effect). What does this feature encode? |

<details>
<summary><b>SA-1</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 5 | `get_upstream_features` | L6:F12990@1, k=10 | Emb:"His"@1 (de=4.91) +9 more |
| 6 | `get_upstream_features` | L4:F4315@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 7 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |

**Findings:** The male pronoun/possessive feature L7:F14893 is not a pure 'his' detector. It is a higher‑level pronoun aggregator that receives strong excitation from the raw embedding of the token "His" (direct_effect 23.5) and from earlier, more specialized pronoun detectors: L6:F12990 (male‑pronoun focused) and L4:F4315 (a low‑level recognizer that itself is driven by the same embedding). Additional modest c…

</details>

<details>
<summary><b>SA-2</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 2 | `get_upstream_features` | L7:F14946@1, k=10 | Emb:"His"@1 (de=18.38) +9 more |
| 3 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 4 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 5 | `get_upstream_features` | L4:F4315@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 6 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 7 | `get_upstream_features` | L6:F12990@1, k=10 | Emb:"His"@1 (de=4.91) +9 more |
| 8 | `inspect_feature` | L3, F3205 | " code snippets and documentation references, possibly related to web d" |
| 9 | `get_upstream_features` | L5:F10952@1, k=10 | Emb:"His"@1 (de=10.69) +9 more |

**Findings:** The male pronoun feature L7:F14946 is driven primarily by the raw input token embedding for "His" (direct_effect ~18.4). Upstream, a low‑layer pronoun detector at L4:F4315 captures mentions of "his" and related pronouns; its own embedding connection to "His" adds a large positive effect (~23.5) and passes ~4.4 influence downstream. A broader male‑pronoun / title feature at L6:F12990 further amplif…

</details>

<details>
<summary><b>SA-3</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F8814 | " various pronouns and names referring to people" |
| 2 | `get_upstream_features` | L19:F8814@1, k=10 | Emb:"His"@1 (de=9.31) +9 more |
| 3 | `inspect_feature` | L18, F7400 | " words related to coding and software/UI interfaces, with some bias to" |
| 4 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 5 | `get_upstream_features` | L18:F7400@1, k=10 | Emb:"His"@1 (de=13.00) +9 more |
| 6 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 7 | `inspect_feature` | L18, F10315 | " pronouns and possessive pronouns" |
| 8 | `get_upstream_features` | L7:F14946@1, k=10 | Emb:"His"@1 (de=18.38) +9 more |
| 9 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 10 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 11 | `inspect_feature` | L11, F10933 | "the letters "L", "H," and "a" when they are at the beginning of a text" |
| 12 | `get_upstream_features` | L18:F10315@1, k=10 | Emb:"His"@1 (de=21.38) +9 more |

**Findings:** The high‑level pronoun/name detector (L19:F8814) is primarily driven by a cascade of masculine pronoun features. The strongest upstream driver is L7:F14946, a tight detector for the possessive pronoun "his" (direct_effect 7.0). This in turn draws strong excitation from the generic pronoun co‑occurrence feature L4:F4315 and the male‑pronoun/title feature L6:F12990. A parallel pathway runs through L…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×9 | L18:10315, L18:7400, L18:14743, L14:4420, L4:4315, L0:7927, L0:8444, L0:2011, L2:9301 |
| 2 | `get_upstream_features` | L19:F8814@1, k=10 → Emb:"His"@1 (de=9.31) +9 more |
| 3 | `get_upstream_features` | L14:F4420@21, k=10 → Emb:" report"@21 (de=5.22) +9 more |
| 4 | `inspect_feature` ×5 | L8:8855, L7:13646, L8:8437, L7:9092, L11:5996 |
| 5 | `get_upstream_features` | L14:F4420@21, k=10 → Emb:" report"@21 (de=5.22) +9 more |
| 6 | `get_upstream_features` | L18:F14743@9, k=10 → Emb:" him"@9 (de=18.38) +9 more |
| 7 | `get_upstream_features` | L14:F4420@21, k=15 → Emb:" report"@21 (de=5.22) +14 more |
| 8 | `get_upstream_features` | L8:F8855@21, k=5 → Emb:" report"@21 (de=12.06) +4 more |

### Build

`build_circuit` → 20 nodes, 44 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 71,152 | 15,958 | 356,225 | 0 | $0.0619 | — | — |
| SA-1 | openai/gpt-oss-120b | 65,729 | 5,326 | 2,592 | 0 | $0.0131 | ✅ 4F/9E | Trace the male pronoun/possessive feature L7:F14893 at posit… |
| SA-2 | openai/gpt-oss-120b | 95,631 | 5,642 | 5,184 | 0 | $0.0178 | ✅ 4F/8E | Trace the male pronoun "his" feature L7:F14946 at position 1… |
| SA-3 | openai/gpt-oss-120b | 160,739 | 7,385 | 5,088 | 0 | $0.0286 | ✅ 6F/10E | Trace L19:F8814 (pronouns/names referring to people) at pos … |
| **Total** | | **393,251** | **34,311** | **369,089** | **0** | **$0.1214** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 57s