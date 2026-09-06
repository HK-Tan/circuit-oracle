# Circuit Oracle Report
**Date:** 2026-07-28 07:20:30 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of "reporter" is driven primarily by a deep, on-target journalism semantic pathway rooted in the literal token " reporter" (pos 66), while the gender-marker features (male pronouns) that are present in the top-20 actually push *against* the probe — the user's concern about spurious gender features is not supported by this circuit.

**Confidence:** 7

**Reasoning:** The top positive contributors to the probe score split into two clearly distinct groups. **Group A — genuine profession signal (L0:F2994 "his/he" at pos 3 & 61, direct_effect +0.2324, +0.1270; L0:F7681 past-tense verb at pos 2, +0.0996; L0:F4677 "and" at pos 15, +0.0898; L7:F14893 pronouns at pos 1, +0.1377)**: these are *very early-layer* (L0–L7) features that fire on the surface tokens themselves. The "his/he" pronoun feature (F2994) has a strongly positive direct_effect, but it is not a profession signal — it is a low-level token detector at the literal "his" position (pos 3) and "his ongoing" (pos 61) whose upward influence stays local. Importantly, the **mid-to-late-layer profession features push the probe the wrong way**: L14:F4420 (journalism vocabulary, frac_nonzero 0.017, on token "reporter") has direct_effect **−0.2051**, L19:F2486 (journalistic sources, frac_nonzero 0.029) has direct_effect **−0.1196**, L18:F14743 ("He" pronoun, frac_nonzero 0.018) has direct_effects of **−0.1064, −0.0928, −0.0884** at three positions, L4:F13253 (media context) is **−0.1406**, and the L7 male-pronoun feature F12990 is **−0.1201 / −0.0928 / −0.0869**. The journalism semantic path (traced via subagent from L14:F4420) cleanly originates at the **" reporter" embedding (pos 66)** and propagates through L4 → L7 → L8 → L14 → L19, but *all of its late-layer features have negative direct_effect on the probe*. This means the **probe direction is anti-correlated with the model's own journalism/reporter representation** — the probe is essentially rewarding the *absence* of the model's strong "reporter" concept and rewarding instead shallow L0/L7 surface features (pronouns, function words, periods). So the user's worry is partially right but in an inverted way: the circuit *does* lean on a gender marker (L0:F2994 "his"), but that is the strongest single positive driver, while the genuine profession indicators (L4/L7/L8/L14/L19 journalism features) all *suppress* the probe score. The probe appears to be detecting a *male-coded textual surface* rather than the profession concept itself — a different kind of spurious correlation than the user suspected, but still a spurious one.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 66 | Emb: " reporter" (pos 66) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 25 | Emb: " He" (pos 25) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: " his" (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L1:F1024](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1024) | 66 | L1 writing/publishing detectors (F1024, F5357) | words and phrases frequently used when discussing writing, publishing, and editing books and other written works. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1024) |
| [L1:F5357](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5357) | 66 | L1 writing/publishing detectors (F1024, F5357) | words related to written works | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5357) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 66 | L4 media/journalism detector (F13253) |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 66 | L7 journalism reporters (F13646, F9092) | news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 66 | L7 journalism reporters (F13646, F9092) | words and phrases associated with broadcast journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L7:F12990](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/12990) | 25 | L7 male pronouns (F12990) — inhibitory | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/12990) |
| [L7:F12990](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/12990) | 1 | L7 male pronouns (F12990) — inhibitory | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/12990) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 66 | L8 news reporter mention (F8855) | mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 66 | L14 journalism vocabulary (F4420) — NEGATIVE direct effect | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F5740](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5740) | 25 | L14 multiple pronouns (F5740) — secondary, negative |  sentences with multiple pronouns in them | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5740) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 25 | L17 pronoun references (F5889) — POSITIVE toward L18:He |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 25 | L18 "He" pronoun (F14743) — pushes AGAINST probe | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 86 | L18 "He" pronoun (F14743) — pushes AGAINST probe | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 69 | L18 "He" pronoun (F14743) — pushes AGAINST probe | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 66 | L19 journalistic sources/outlets (F2486) — NEGATIVE direct effect |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L0:F8974](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) | 9 | L0 misc function-word features (F8974, F6051, F886, F8061, F14824, F7681, F4677) — generic textual features | the word "from" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 24 | L0 misc function-word features (F8974, F6051, F886, F8061, F14824, F7681, F4677) — generic textual features | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F886](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/886) | 2 | L0 misc function-word features (F8974, F6051, F886, F8061, F14824, F7681, F4677) — generic textual features |  text related to discounts, offers, or prices | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/886) |
| [L0:F8061](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) | 6 | L0 misc function-word features (F8974, F6051, F886, F8061, F14824, F7681, F4677) — generic textual features |  the preposition "in" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) |
| [L0:F14824](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) | 16 | L0 misc function-word features (F8974, F6051, F886, F8061, F14824, F7681, F4677) — generic textual features | the word "has" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) |
| [L0:F7681](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7681) | 2 | L0 misc function-word features (F8974, F6051, F886, F8061, F14824, F7681, F4677) — generic textual features | statements that describe something, often including a past tense verb | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7681) |
| [L0:F4677](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4677) | 15 | L0 misc function-word features (F8974, F6051, F886, F8061, F14824, F7681, F4677) — generic textual features |  the word "and", sometimes in conjunction with "the", "but", or "as". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4677) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 3 | L0 "his/he" pronoun detector (F2994) — POSITIVE direct effect | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 61 | L0 "his/he" pronoun detector (F2994) — POSITIVE direct effect | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2994 de=0.232 |
| 3 | `inspect_feature` ×15 | L0:2994, L14:4420, L0:8974, L0:6051, L0:886, L0:8061, L0:7681, L0:14824, L18:14743, L7:14893, L7:14946, L4:13253, L19:2486, L0:4677, L6:12990 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@66` | ✅ reported | 7 | 11 | Trace the journalism feature L14:F4420 (which fires on the token "reporter" and … |
| SA-2 | `L19:F2486@66` | ✅ reported | 8 | 10 | Trace the journalistic sources feature L19:F2486 upstream to see what drives the… |
| SA-3 | `L18:F14743@25` | ❌ error | — | — | Trace the "He" pronoun feature L18:F14743 (pos 25, where "His degrees" appears) … |
| SA-4 | `L0:F2994@3` | ❌ error | — | — | Trace the "his/he" pronoun feature L0:F2994 (pos 3 - "He obtained") upstream to … |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@66, k=10 | Emb:" reporter"@66 (de=18.75) +9 more |
| 3 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 4 | `get_upstream_features` | L4:F13253@66, k=10 | Emb:" reporter"@66 (de=26.62) +9 more |
| 5 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 6 | `get_upstream_features` | L8:F8855@66, k=10 | Emb:" reporter"@66 (de=16.88) +9 more |
| 7 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 8 | `inspect_feature` | L1, F1024 | " words and phrases frequently used when discussing writing, publishing" |
| 9 | `inspect_feature` | L1, F5357 | " words related to written works" |
| 10 | `get_upstream_features` | L1:F1024@66, k=10 | Emb:" reporter"@66 (de=8.06) +9 more |
| 11 | `get_upstream_features` | L7:F13646@66, k=10 | Emb:" reporter"@66 (de=15.12) +9 more |
| 12 | `inspect_feature` | L7, F9092 | " words and phrases associated with broadcast journalism" |

**Findings:** The profession token 'reporter' is driven primarily by a cascade of journalism‑related features. The strongest upstream driver is a low‑frequency media‑context feature in layer 4 (13253) that receives a large positive push directly from the 'reporter' embedding. This feeds into the target L14:F4420, which itself strongly promotes journalist tokens. Parallel pathways through layer‑8 (8855) and laye…

</details>

<details>
<summary><b>SA-2</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F2486 | " journalistic sources and news outlets." |
| 2 | `get_upstream_features` | L19:F2486@66, k=10 | Emb:" reporter"@66 (de=28.25) +9 more |
| 3 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 4 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 5 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 6 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 7 | `get_upstream_features` | L14:F4420@66, k=10 | Emb:" reporter"@66 (de=18.75) +9 more |
| 8 | `get_upstream_features` | L4:F13253@66, k=10 | Emb:" reporter"@66 (de=26.62) +9 more |

**Findings:** The journalistic‑sources feature (L19:F2486) is driven primarily by the raw token embedding of the word "reporter" and a cascade of intermediate journalism‑related features. The strongest upstream driver is the embedding of "reporter" (direct_effect 28.25). This feeds into a mid‑level journalism vocabulary feature (L14:F4420), which in turn is supported by earlier media detectors at layers 8, 7, a…

</details>

### Re-dispatch (round 2): 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-5 | `L4:F13253@66` | ✅ reported | 4 | 5 | Trace the L4:F13253 (media context) feature upstream to see what feeds it. This … |
| SA-6 | `L7:F12990@25` | ❌ error | — | — | Trace the L7:F12990 (male pronouns/titles, very suspicious as a potential spurio… |

<details>
<summary><b>SA-5</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 2 | `get_upstream_features` | L4:F13253@66, k=10 | Emb:" reporter"@66 (de=26.62) +9 more |
| 3 | `inspect_feature` | L1, F1024 | " words and phrases frequently used when discussing writing, publishing" |
| 4 | `inspect_feature` | L1, F5357 | " words related to written works" |
| 5 | `get_upstream_features` | L1:F1024@66, k=10 | Emb:" reporter"@66 (de=8.06) +9 more |
| 6 | `inspect_feature` | L1, F5357 | " words related to written works" |
| 7 | `get_upstream_features` | L1:F1024@66, k=10 | Emb:" reporter"@66 (de=8.06) +9 more |
| 8 | `get_upstream_features` | L1:F5357@66, k=10 | Emb:" reporter"@66 (de=12.00) +9 more |
| 9 | `inspect_feature` | L1, F10525 | " words followed by "er". " |
| 10 | `inspect_feature` | L0, F930 | " words related to legal proceedings, and/or annoying loud sounds" |
| 11 | `get_upstream_features` | L0:F930@66, k=10 | Emb:" reporter"@66 (de=9.38) +9 more |

**Findings:** The media/journalism feature L4:F13253 receives its strongest excitatory drive from the token embedding ' reporter' at the same position, delivering a large positive direct effect (26.6). Secondary upstream contributors are low‑layer (layer 1) writing‑related features (F1024 and F5357) which themselves are driven by the same ' reporter' embedding and a small positive influence from a generic layer…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14743@25, k=12 → Emb:" He"@25 (de=24.00) +11 more |
| 2 | `get_upstream_features` | L0:F2994@3, k=12 → Emb:" his"@3 (de=42.25) +11 more |
| 3 | `inspect_feature` ×3 | L0:1069, L17:5889, L14:5740 |

### Build

`build_circuit` → 16 nodes, 26 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 56,116 | 5,241 | 180,770 | 0 | $0.0340 | — | — |
| SA-2 | openai/gpt-oss-120b | 104,894 | 5,991 | 2,544 | 0 | $0.0194 | ✅ 8F/10E | Trace the journalistic sources feature L19:F2486 upstream to… |
| SA-1 | openai/gpt-oss-120b | 175,003 | 10,942 | 0 | 0 | $0.0328 | ✅ 7F/11E | Trace the journalism feature L14:F4420 (which fires on the t… |
| SA-5 | openai/gpt-oss-120b | 118,905 | 5,557 | 12,896 | 0 | $0.0214 | ✅ 4F/5E | Trace the L4:F13253 (media context) feature upstream to see … |
| **Total** | | **454,918** | **27,731** | **196,210** | **0** | **$0.1075** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 12s