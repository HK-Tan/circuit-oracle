# Circuit Oracle Report
**Date:** 2026-07-28 07:21:12 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a circuit that is dominated by gendered pronoun/male-reference features (His, he, him, Male pronouns/titles) cascading from the "His" token at pos 1 and "him" at pos 9 through layers 0→4→6→7→18→19, with a smaller parallel profession-specific sub-circuit (report → journalism at pos 21). The user's concern is **confirmed**: the dominant signal is the male-gendered subject marker, not the genuine profession cue (journalism/reporter).

**Confidence:** 8

**Reasoning:** The late-layer features driving the probe are mostly **gender/pronoun detectors** rather than profession indicators:
- **L19:8814** (direct_effect +0.232) — "various pronouns and names referring to people"; promoted tokens are female (herself/she/her) but the input drives it via the "His" embedding (de=9.31 from Emb:His). This feature fires on the mere presence of a male-referring pronoun at pos 1.
- **L18:14743** (de −0.187, at pos 9) — fires on "him" (Emb:him, de=18.4); a high-frequency male-pronoun token detector.
- **L18:10315** (de −0.162) and **L7:14946** (de −0.467) — possessive "his" detectors, sourced directly from Emb:His (de=13–21).
- **L7:14893** (de +0.471) — labeled generic pronouns, but its promoted_tokens list (herself/she) and upstream path (Emb:His → L4:4315 → L6:12990 → L7:14893, plus the raw embedding de=23.5) show it is fundamentally a "this position has a masculine pronoun" detector being inverted.
- **L6:12990** (de −0.297), **L0:2994** (de +0.285), **L0:16297** (de +0.134 via "him"), **L4:4315** (de −0.182) — all variants of male-pronoun detectors, traced back to the "His"/"him" token embeddings.

The genuine profession signal exists but is **secondary and smaller in magnitude**:
- **L14:4420** (de −0.159, "journalism/newspapers", frac_nonzero=0.016) — receives Emb:report (de=5.22) and chains through **L8:8855** ("news reporters", frac=0.0085, de=5.03 into L14) and **L7:13646** ("news reporting", frac=0.0076, de=3.73). These are highly specific profession detectors that trace to the word "report" in "...opportunity to report for some of the top news organizations."

**Magnitude comparison:** the gender/pronoun supernode's aggregate direct effect on the probe (|−0.47| + |−0.30| + |+0.47| + |−0.18| + |−0.16| + |+0.29| + |+0.23| + |−0.19| ≈ 2.29) substantially exceeds the journalism sub-circuit's (|−0.16| + small upstream contributions ≈ <0.4). The probe is also inhibited by L18:7400 (coding/UI, de −0.155) and L18:14743 (He, de −0.187), but the dominant positive drive comes from male-pronoun features at pos 1 and pos 9, not from the "report"/"journalism" tokens at pos 21. **This is exactly the spurious-correlation pattern the user flagged**: a profession-classification probe (likely the "reporter/journalist" class) is leaning on the gendered subject marker of the sentence rather than on the lexical profession cues.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'His' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: ' him' (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: ' report' (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 0 | Emb: '<bos>' (pos 0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | Low-layer 'his'/'he' detector (L0:2994) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F16297](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) | 9 | Low-layer 'him' detector (L0:16297) |  the pronoun "him" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) |
| [L0:F7927](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7927) | 8 | Past-participle detector (L0:7927) |  past-participle verbs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7927) |
| [L0:F2011](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) | 2 | 'dream' token (L0:2011) |  the word "dream" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 3 | 'to' token (L0:8444) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L2:F9301](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) | 1 | Men/women in relationships (L2:9301) |  all mentions of men and women in the context of relationships, dating, or gendered social roles | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | 'His'/'his' token detector (L4:4315) |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Male pronouns/titles (L6:12990) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 21 | News reporting & journalism (L7:13646) |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Pronoun/possessive detector (female-promoted) (L7:14893) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | Possessive 'his'/'he'/'him' (L7:14946) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 21 | Reporter/news-reporting detector (L8:8855) |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 21 | Film festival/production (L8:8437) | content related to film festivals and production, particularly documentary films, and the recognition they receive. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 21 | Journalism & newspapers (L14:4420) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 9 | 'He' (L16:14120 -> L18:14743) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 1 | Male-bias pronouns/possessives (L18:10315) |  pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L18:F7400](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) | 1 | Coding/UI (suppresses) (L18:7400) |  words related to coding and software/UI interfaces, with some bias toward non-English words | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | Pronouns/names for people, male-promoted (L19:8814) |  various pronouns and names referring to people | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L7:14893 de=0.471 |
| 3 | `inspect_feature` ×12 | L7:14893, L7:14946, L0:2994, L19:8814, L18:14743, L18:10315, L14:4420, L18:7400, L6:12990, L4:4315, L2:9301, L0:8444 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ✅ reported | 4 | 7 | Trace this feature upstream to find the source. It fires on pronouns/possessives… |
| SA-2 | `L7:F14946@1` | ✅ reported | 3 | 5 | Trace this feature upstream. It fires on "his/he/him" tokens. Find the source em… |
| SA-3 | `L19:F8814@1` | ❌ error | — | — | Trace this feature upstream. It encodes "pronouns and names referring to people"… |
| SA-4 | `L14:F4420@21` | ✅ reported | 4 | 6 | Trace this feature upstream. It encodes "words and phrases related to journalism… |
| SA-5 | `L18:F14743@9` | ❌ error | — | — | Trace this feature upstream. It encodes "He" — fires on the token "he"/"He" at p… |

<details>
<summary><b>SA-1</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 5 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |
| 6 | `get_upstream_features` | L6:F12990@1, k=10 | Emb:"His"@1 (de=4.91) +9 more |
| 7 | `get_upstream_features` | L4:F4315@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |

**Findings:** The L7 feature (pronouns/possessive pronouns) fires on the token "His" because the raw token embedding sends a large positive direct effect (23.5) up to it. Upstream, a mid‑layer male‑pronoun detector (L6:12990) also contributes positively, but the L7 feature's own promoted token list is skewed toward female pronouns, causing a gender‑swap effect. The immediate source of the signal is the input em…

</details>

<details>
<summary><b>SA-2</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 2 | `get_upstream_features` | L7:F14946@1, k=15 | Emb:"His"@1 (de=18.38) +14 more |
| 3 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 4 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 5 | `get_upstream_features` | L4:F4315@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |

**Findings:** The target L7 feature that activates on masculine pronouns receives its strongest excitatory drive directly from the raw token embedding of "His" (pos 1). A prominent upstream driver is the lower‑layer L4 feature 4315, an early pronoun detector that also gets a large positive push from the same "His" embedding. This chain (Embedding → L4:F4315 → L7:F14946) satisfies the lower‑third layer condition…

</details>

<details>
<summary><b>SA-4</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@21, k=10 | Emb:" report"@21 (de=5.22) +9 more |
| 3 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 4 | `get_upstream_features` | L8:F8855@21, k=10 | Emb:" report"@21 (de=12.06) +9 more |
| 5 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 6 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |

**Findings:** The journalism signal at L14:F4420 originates from the raw token embedding of the word "report" (positive direct effect 5.22). This embedding strongly drives a layer‑8 feature (F8855) that detects mentions of news reporters and reporting (direct effect 12.06). The layer‑8 feature then excites the target feature. An even lower‑layer (layer‑7) feature (F13646) also detects news reporting language an…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L19:F8814@1, k=10 → Emb:"His"@1 (de=9.31) +9 more |
| 2 | `get_upstream_features` | L18:F7400@1, k=10 → Emb:"His"@1 (de=13.00) +9 more |
| 3 | `get_upstream_features` | L18:F10315@1, k=10 → Emb:"His"@1 (de=21.38) +9 more |
| 4 | `get_upstream_features` | L18:F14743@9, k=8 → Emb:" him"@9 (de=18.38) +7 more |
| 5 | `get_upstream_features` | L11:F10933@1, k=8 → L10:F14174 (de=11.56) +7 more |
| 6 | `get_upstream_features` | L11:F9183@1, k=8 → L10:F14174 (de=13.88) +7 more |
| 7 | `get_upstream_features` | L9:F8770@1, k=8 → L7:F462 (de=15.06) +7 more |
| 8 | `inspect_feature` ×13 | L10:14174, L0:16297, L7:462, L7:5741, L5:3992, L16:14120, L14:10344, L7:13646, L8:8855, L11:10933, L11:9183, L0:2011, L0:7927 |
| 9 | `get_upstream_features` | L8:F8437@21, k=8 → Emb:" report"@21 (de=5.75) +7 more |
| 10 | `get_upstream_features` | L7:F13646@21, k=8 → Emb:" report"@21 (de=7.22) +7 more |
| 11 | `inspect_feature` | L0, F2994 → "the pronoun "his" and the pronoun "he."" |
| 12 | `get_upstream_features` | L0:F2994@1, k=5 → Emb:"His"@1 (de=19.75) +4 more |
| 13 | `get_upstream_features` | L14:F4420@21, k=5 → Emb:" report"@21 (de=5.22) +4 more |

### Build

`build_circuit` → 23 nodes, 47 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 68,862 | 7,008 | 377,947 | 0 | $0.0517 | — | — |
| SA-2 | openai/gpt-oss-120b | 45,097 | 3,191 | 0 | 0 | $0.0087 | ✅ 3F/5E | Trace this feature upstream. It fires on "his/he/him" tokens… |
| SA-4 | openai/gpt-oss-120b | 54,390 | 3,932 | 0 | 0 | $0.0105 | ✅ 4F/6E | Trace this feature upstream. It encodes "words and phrases r… |
| SA-1 | openai/gpt-oss-120b | 69,393 | 3,662 | 2,528 | 0 | $0.0126 | ✅ 4F/7E | Trace this feature upstream to find the source. It fires on … |
| **Total** | | **237,742** | **17,793** | **380,475** | **0** | **$0.0836** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 4s