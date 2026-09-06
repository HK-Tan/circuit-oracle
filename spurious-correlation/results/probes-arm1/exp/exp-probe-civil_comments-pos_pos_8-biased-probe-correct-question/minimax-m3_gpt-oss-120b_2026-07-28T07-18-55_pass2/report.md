# Circuit Oracle Report
**Date:** 2026-07-28 07:18:55 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_8 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity-classification score is driven almost entirely by entity/identity-recognition features that fire on the tokens "Islam" and "Allah" — not by features encoding the actual toxic content (e.g., "false", "Lucifer", the denigrating predicate). The circuit confirms the user's concern: it is a religion-mention detector, not a toxicity detector.

**Confidence:** 9/10

**Reasoning:** The attribution graph traces cleanly to two input tokens. The "Islam" embedding at pos 4 (direct_effect = 18.5 into L6:F7282, 21.5 into L4:F2405, 8.44 into L3:F12024, 12.25 into L0:F13885) and the "Allah" embedding at pos 13 (direct_effect = 15.81 into L6:F7282, 3.19 into L0:F13885) are the dominant positive drivers. From those embeddings, the signal flows through an almost entirely identity-recognition chain:

- **L0:F13885** ("names of people/places related to the Middle East", frac_nonzero = 0.054) is a generic region/entity detector — its top activating examples are "Yahya", "Wali", "Shah" — it does not encode toxicity.
- **L1:F4314** (frac_nonzero = 0.0047) is literally labeled "the word Muslim" and **suppresses** "Muslim/Islam" in its token logits (note `suppressed_tokens: ▁Muslim, ▁Muslims, ▁Islam, ▁islamic`), with a negative direct_effect of −0.244.
- **L3:F12024** (frac_nonzero = 0.010) similarly labeled "words referencing Islam… and Arabic names" and likewise suppresses the same tokens in its logit projections.
- **L4:F2405** (frac_nonzero = 0.007) — "religious identity/affiliation" — is again a category detector, with promoted tokens like "Catholic", "religions".
- **L4:F7545** — "religious extremism, violence, terrorism" — is a generic feature that fires on tokens like "fanatically", "fundamentalist", "ist", "ism" and is not specific to this prompt's actual toxic content.
- **L6:F7282** (frac_nonzero = 0.007, direct_effect = +0.41, the single largest contributor to the probe score) — "mentions of Islam or Middle Eastern places and people" — promoted tokens are "mosques, Muslim, Islamic, Islam, Muhammad". Its top activating examples include explicitly toxic passages about Muslims, but the feature itself is an entity-presence detector, not a toxicity detector.
- **L6:F3265** (frac_nonzero = 0.022) — "religion, religious figures, related concepts" — fires on tokens like "fearing", "church", "Rabbi". Generic religion-detector.
- **L6:F5764** — another Islam-specific detector.
- **L7:F14049** (frac_nonzero = 0.010) — "discussion of international political conflicts, especially those regarding Muslims, slavery, race, terrorism and cultural groups" — this is the closest the circuit comes to content-aware features, and it is downstream of the pure entity detectors.
- **L8:F13197** (frac_nonzero = 0.014, direct_effect = +0.26) — "words related to religion and faith" — generic.
- **L12:F7779** (frac_nonzero = 0.006, direct_effect = +0.14) — "negative language denigrating groups of people" — fires at pos 10 ("it's"), not at "false" or "Lucifer" where the actual toxic semantics live.

Crucially, none of the high-contribution features encode the actually toxic linguistic content: "false", "Lucifer", the copula, or the structure "X is Y" defamation pattern. The strongest single contributor (L6:F7282 at +0.41) and L4:F2405 (+0.32) are pure identity-detectors; their only semantic commonality with this input is that it mentions a protected religious group, not that it denigrates one. The signal could be entirely produced by any neutral sentence mentioning "Islam" or "Allah" (e.g., "Islam is a monotheistic religion" or "Allah is the Arabic word for God"). The user's suspicion is confirmed by the data: the probe's classification is being driven by entity-presence features, not by lexical/semantic toxicity features. This is a textbook example of spurious-correlation in a linear probe — the residual stream direction the probe learned is aligned with religion-entity axes rather than toxicity axes.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F13885](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13885) | 4 | L0: Middle Eastern names/places (F13885) |  names of people and places, specifically those related to the middle east | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13885) |
| [L0:F13885](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13885) | 13 | L0: Middle Eastern names/places (F13885) |  names of people and places, specifically those related to the middle east | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13885) |
| [L1:F4314](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4314) | 4 | L1: 'Muslim' word detector (F4314) |  the word Muslim | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4314) |
| [L1:F2235](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2235) | 13 | L1: Quran passages (F2235) |  passages from the Quran | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2235) |
| [L3:F12024](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12024) | 4 | L3: Islam/Arabic terms (F12024) |  words referencing the religion of Islam, people who practice it, and Arabic names | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12024) |
| [L4:F2405](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) | 4 | L4: Religious identity/affiliation (F2405) |  words related to religious identity/affiliation or spirituality including related holidays | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) |
| [L4:F7545](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7545) | 4 | L4: Religious extremism/violence (F7545) |  words or phrases relating to religious extremism, violence, and terrorism. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7545) |
| [L6:F7282](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) | 4 | L6: Islam/Middle-Eastern mentions (F7282) |  mentions of Islam or Middle Eastern places and people, as well as mentions of a specific district. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) |
| [L6:F7282](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) | 13 | L6: Islam/Middle-Eastern mentions (F7282) |  mentions of Islam or Middle Eastern places and people, as well as mentions of a specific district. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) |
| [L6:F3265](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3265) | 4 | L6: Religion/religious figures (F3265) |  religion, religious figures, and related concepts and groups | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3265) |
| [L6:F5764](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5764) | 4 | L6: Islam-specific (F5764) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5764) |
| [L7:F14049](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14049) | 4 | L7: Political conflict / Muslim discourse (F14049) |  discussion of international political conflicts, especially those regarding Muslims, slavery, race, terrorism and cultural groups. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14049) |
| [L8:F13197](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13197) | 4 | L8: Religion/faith words (F13197) |  words related to religion and faith | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13197) |
| [L12:F7779](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/7779) | 10 | L12: Negative language about groups (F7779) |  negative language denigrating groups of people | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/7779) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:7282 de=0.410 |
| 3 | `inspect_feature` ×6 | L6:7282, L4:2405, L8:13197, L1:4314, L3:12024, L0:13885 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F7282@4` | ✅ reported | 3 | 5 | Trace this feature (L6:F7282 - mentions of Islam/Middle Eastern places/people) u… |
| SA-2 | `L8:F13197@4` | ✅ reported | 4 | 6 | Trace this feature (L8:F13197 - words related to religion and faith) upstream to… |
| SA-3 | `L4:F2405@4` | ✅ reported | 5 | 7 | Trace this feature (L4:F2405 - religious identity/affiliation words) upstream to… |
| SA-4 | `L0:F13885@4` | ❌ error | — | — | Trace this feature (L0:F13885 - Middle Eastern names/places) upstream to its sou… |

<details>
<summary><b>SA-1</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F7282 | " mentions of Islam or Middle Eastern places and people, as well as men" |
| 2 | `get_upstream_features` | L6:F7282@4, k=10 | Emb:" Islam"@4 (de=18.50) +9 more |
| 3 | `inspect_feature` | L0, F13885 | " names of people and places, specifically those related to the middle " |
| 4 | `get_upstream_features` | L0:F13885@4, k=10 | Emb:" Islam"@4 (de=12.25) +9 more |
| 5 | `inspect_feature` | L4, F2405 | " words related to religious identity/affiliation or spirituality inclu" |
| 6 | `get_upstream_features` | L4:F2405@4, k=10 | Emb:" Islam"@4 (de=21.50) +9 more |
| 7 | `inspect_feature` | L0, F2158 | "the word "with"" |

**Findings:** The target feature L6:F7282, which fires on the token "Islam", is driven primarily by the raw embedding of the token itself (direct_effect ~18.5). Upstream, it receives additional contribution from an early‑layer detector L0:13885 (direct_effect ~2.39) that focuses on Middle‑Eastern names, which in turn is strongly excited by the same "Islam" embedding (direct_effect ~12.25). Another path goes thr…

</details>

<details>
<summary><b>SA-2</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L8, F13197 | " words related to religion and faith" |
| 2 | `get_upstream_features` | L8:F13197@4, k=10 | Emb:" Islam"@4 (de=9.25) +9 more |
| 3 | `inspect_feature` | L4, F2405 | " words related to religious identity/affiliation or spirituality inclu" |
| 4 | `get_upstream_features` | L4:F2405@4, k=10 | Emb:" Islam"@4 (de=21.50) +9 more |
| 5 | `inspect_feature` | L6, F7282 | " mentions of Islam or Middle Eastern places and people, as well as men" |
| 6 | `get_upstream_features` | L6:F7282@4, k=10 | Emb:" Islam"@4 (de=18.50) +9 more |
| 7 | `inspect_feature` | L7, F14049 | " discussion of international political conflicts, especially those reg" |
| 8 | `inspect_feature` | L0, F13885 | " names of people and places, specifically those related to the middle " |

**Findings:** The target feature L8:F13197 (religion/faith detector) receives its strongest positive drive from the raw input token embedding ' Islam' (direct_effect 9.25). That same embedding also strongly excites an earlier layer‑4 feature (L4:F2405) that specializes in religious identity tokens, which in turn pushes L8:F13197 (direct_effect 4.78). Additional upstream contributors include a layer‑6 Middle‑Eas…

</details>

<details>
<summary><b>SA-3</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F2405 | " words related to religious identity/affiliation or spirituality inclu" |
| 2 | `get_upstream_features` | L4:F2405@4, k=10 | Emb:" Islam"@4 (de=21.50) +9 more |
| 3 | `inspect_feature` | L2, F7214 | " references to countries or regions associated with Islam" |
| 4 | `get_upstream_features` | L2:F7214@4, k=10 | Emb:" Islam"@4 (de=12.38) +9 more |
| 5 | `inspect_feature` | L2, F6894 | " mentions of religions" |
| 6 | `inspect_feature` | L0, F13885 | " names of people and places, specifically those related to the middle " |
| 7 | `get_upstream_features` | L2:F6894@4, k=10 | Emb:" Islam"@4 (de=8.88) +9 more |
| 8 | `inspect_feature` | L2, F15823 | " terms related to politics, economics, sports, and technology." |
| 9 | `inspect_feature` | L0, F3031 | "the word "bias"" |

**Findings:** The religious‑identity detector (L4:F2405) receives its strongest excitation from the raw input token " Islam" (direct_effect 21.5). Upstream, a mid‑layer geographic‑Islam feature (L2:F7214) and two broader religion‑mention features (L2:F6894, L2:F15823) add smaller positive contributions. A low‑layer generic "bias" feature also nudges it slightly. The path reaches layer 0 embeddings, satisfying b…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F13885@4, k=10 → Emb:" Islam"@4 (de=12.25) +9 more |
| 2 | `inspect_feature` ×7 | L7:14049, L0:880, L0:6051, L0:14656, L7:12448, L4:15997, L12:7779 |
| 3 | `get_upstream_features` | L6:F7282@13, k=5 → Emb:" Allah"@13 (de=15.81) +4 more |
| 4 | `get_upstream_features` | L3:F12024@4, k=10 → Emb:" Islam"@4 (de=8.44) +9 more |
| 5 | `get_upstream_features` | L6:F7282@4, k=10 → Emb:" Islam"@4 (de=18.50) +9 more |
| 6 | `inspect_feature` ×8 | L1:2235, L0:9026, L0:2158, L5:6490, L5:14348, L4:7545, L10:2716, L6:3265 |

### Build

`build_circuit` → 16 nodes, 25 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 43,472 | 5,002 | 152,198 | 0 | $0.0282 | — | — |
| SA-2 | openai/gpt-oss-120b | 79,871 | 4,414 | 2,560 | 0 | $0.0147 | ✅ 4F/6E | Trace this feature (L8:F13197 - words related to religion an… |
| SA-1 | openai/gpt-oss-120b | 61,248 | 3,485 | 5,056 | 0 | $0.0114 | ✅ 3F/5E | Trace this feature (L6:F7282 - mentions of Islam/Middle East… |
| SA-3 | openai/gpt-oss-120b | 96,229 | 5,987 | 5,152 | 0 | $0.0181 | ✅ 5F/7E | Trace this feature (L4:F2405 - religious identity/affiliatio… |
| **Total** | | **280,820** | **18,888** | **164,966** | **0** | **$0.0723** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 35s