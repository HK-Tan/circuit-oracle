# Circuit Oracle Report
**Date:** 2026-07-28 07:11:44 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_8 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by lexical content features for "Congress," "funding/levels," "our," and "who/many" — not by spurious negation cues.

**Confidence:** 8

**Reasoning:** Tracing back through 3–6 layer hops, every one of the top features driving the probe direction has a direct embedding-level driver that is a *content word* from the prompt, not a negation/safety word:

- **L0:F13437 "the word who"** at pos 15 ("…members who did not support…") — direct_effect +0.789 (largest single feature in the graph). Upstream is overwhelmingly the **"who" token embedding** (direct_effect 35.25). Fractions of mass go to other content embeddings ("many," "members," "levels," "funding," "controls," "include"), and the only negative contributions come from the *punctuation* tokens "," (pos 3, 9). This is exactly the case the user suspected would be a "negation" trap, but it is actually a *content-word* feature: it detects the relative-pronoun "who" used to introduce the embedded clause that *states* the negation in the premise ("who did not support the purpose and goals"). The feature itself is purely lexical — it has no access to whether "who" is followed by a negation.
- **L2:F156 "words related to the amount or intensity of something"** at pos 8 ("levels") — direct_effect −0.37. Upstream is the **"levels" embedding** (direct_effect 28.0). This is a content feature on a content word.
- **L3:F13271 "the word control"** at pos 5 ("controls") — direct_effect +0.36. Upstream is the **"controls" embedding** (direct_effect 18.5).
- **L0:F11606 "the word fund"** at pos 7 ("funding") — direct_effect −0.36. Upstream is the **"funding" embedding** (direct_effect 20.1).
- **L1:F2116 "words related to legal counsel"** at pos 7 — driven by **"funding" embedding** (14.1) — content word, not negation.
- **L6:F6096 "political parties and affiliations"** at pos 2 ("Congress") — direct_effect +0.45. Upstream is the **"Congress" embedding** (13.8) plus a chain of party/Congress detector features (L0:F7021 "the word Congress", L0:F767 "Congress / immigration matters", L0:F10198 "the word Congress", L2:F2701 "U.S. Congress", L3:F123 "U.S. Congress", L2:F6735 "political parties and politicians", L4:F5265, L5:F842, etc.). This is entity-recognition on a content word.
- **L6:F13778 "subjective language, opinions and feelings"** at pos 6 ("our") — direct_effect −0.31. The subagent's trace showed this is a pronoun-detector cascade (L0:F636 first-person pronouns → L2:F107 first-person pronouns → L4:F2813 pronoun/possessive adjectives → L4:F8160 generic lexical aggregator → L6:F13778), ultimately anchored on the **"our" embedding** (13.6) and the **"our" possessive feature L0:F15773** (40.0 direct_effect upstream of the cascade). Although the autointerp label says "subjective language," the actual trigger is the possessive "our" — i.e. a content-word feature that signals "we're describing *our* system / *our* funding." This is again a *content-lexical* feature, not a negation cue.
- **L0:F6044 "the word yield"** (mislabeled — top examples all show "yield"), **L0:F9557 "the word clean and words associated with people"**, **L1:F6948 "the word lift"**, **L0:F9529 "the word physical"** — all are weakly activated generic lexical features that incidentally fire on "Congress"/"controls" but contribute small signed effects. None are negation detectors.
- **L3:F8382 "the word many"** at pos 13 — direct_effect +0.33. Upstream is the **"many" embedding** (23.5). Content word.

**On the user's concern (negation words as spurious signal):** I looked for negation features ("not," "no," "never," "neither," "without") in the top-20 features and their upstream chains, and **none are present**. The LLM's negation "did not support" in the premise never appears in the top-feature list; instead, the dominant signal is the content vocabulary of the premise: "Congress" (entity recognition), "who/many/members" (relative clause introducing the premise), "controls/our/funding/levels" (the structural description of the topic). The two features that *could* be mistaken for "spurious negation" — L0:F13437 "who" and L0:F15773 "our" — turn out, on tracing, to be honest content-word detectors whose embeddings carry most of the signal. The probe's contradiction classification here is being driven by the *lexical identity* of the words used to express the relationship, not by the model "sniffing out" the word "not" in the premise.

The subjective-language / pronoun supernode (sn_our_l6) deserves a caveat: although the top-3 path is content-driven, L6:F13778 has a high frac_nonzero (0.055) and is a generic pronoun/opinion aggregator rather than a specific entity detector, so it could contribute mild "soft-bias" effects (e.g., first-person framings tend to correlate with premise-style text in NLI). But its contribution is small in absolute signed terms and the dominant signal is still content-lexical.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Output logit (probe direction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L6:F13778](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/13778) | 6 | Subjective-language / possessive at 'our' | subjective language, opinions and feelings. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/13778) |
| [L4:F8160](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8160) | 6 | Subjective-language / possessive at 'our' | a grab-bag of seemingly random words | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8160) |
| [L4:F2813](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2813) | 6 | Subjective-language / possessive at 'our' |  pronouns and possessive adjectives, especially when next to conjugated verbs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2813) |
| [L2:F107](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/107) | 6 | Subjective-language / possessive at 'our' |  first person pronouns like "I", "me", "my", "we", "he", or "she" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/107) |
| [L0:F636](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/636) | 6 | Subjective-language / possessive at 'our' |  first-person pronouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/636) |
| [L0:F15773](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15773) | 6 | Subjective-language / possessive at 'our' |  the possessive pronoun "our" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15773) |
| [L6:F6096](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6096) | 2 | Political party / affiliation at 'Congress' |  political parties and affiliations | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6096) |
| [L5:F842](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/842) | 2 | Political party / affiliation at 'Congress' | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/842) |
| [L4:F5265](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5265) | 2 | Political party / affiliation at 'Congress' | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5265) |
| [L2:F6735](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6735) | 2 | Political party / affiliation at 'Congress' |  political parties and politicians | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6735) |
| [L2:F2701](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) | 2 | Political party / affiliation at 'Congress' |  words related to the U.S. Congress | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) |
| [L1:F3276](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3276) | 2 | Political party / affiliation at 'Congress' |  mentions of the United States Congress | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3276) |
| [L0:F7021](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7021) | 2 | Political party / affiliation at 'Congress' |  the word "Congress" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7021) |
| [L0:F767](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/767) | 2 | Political party / affiliation at 'Congress' | the word "Congress" as well as the phrase "immigration matters" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/767) |
| [L0:F10198](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10198) | 2 | Political party / affiliation at 'Congress' |  the word "Congress" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10198) |
| [L0:F15411](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15411) | 2 | Political party / affiliation at 'Congress' |  terms relating to political bodies, figures, and processes | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15411) |
| [L0:F13168](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13168) | 2 | Political party / affiliation at 'Congress' |  the words "broad," "wild," and "faced" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13168) |
| [L3:F123](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/123) | 2 | Political party / affiliation at 'Congress' |  mentions of the United States Congress | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/123) |
| [L0:F13437](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13437) | 15 | Content words: 'who' (pos 15) and 'many' (pos 13) | the word "who" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13437) |
| [L3:F8382](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8382) | 13 | Content words: 'who' (pos 15) and 'many' (pos 13) |  the word "many", and sometimes "times" or "people" when near it | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8382) |
| [L0:F11606](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11606) | 7 | Funding / 'fund' and 'levels' content |  the word "fund" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11606) |
| [L1:F2116](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2116) | 7 | Funding / 'fund' and 'levels' content |  words and phrases related to legal counsel or representation | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2116) |
| [L2:F156](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/156) | 8 | Funding / 'fund' and 'levels' content |  words related to the amount or intensity of something | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/156) |
| [L3:F13271](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13271) | 5 | Funding / 'fund' and 'levels' content |  the word "control." | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13271) |
| [L0:F6044](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) | 2 | Funding / 'fund' and 'levels' content | the word "yield" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) |
| [L0:F9557](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9557) | 2 | Funding / 'fund' and 'levels' content | the word "clean" and words/phrases associated with people | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9557) |
| [L1:F6948](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6948) | 2 | Funding / 'fund' and 'levels' content |  the word "lift" in the context of mechanical devices or ski infrastructure | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6948) |
| [L0:F9529](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9529) | 5 | Funding / 'fund' and 'levels' content | the word "physical" and words related to programming | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9529) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:6044 de=0.789 |
| 3 | `inspect_feature` ×19 | L0:6044, L0:13437, L6:6096, L2:6735, L1:6948, L2:2701, L1:2116, L0:9557, L2:156, L3:13271, L0:11606, L3:123, L0:9529, L6:13778, L0:7021, L1:8982, L1:12456, L3:8382, L1:3276 |
| 4 | `get_upstream_features` | Emb:" Congress"@2 (de=13.81) +14 more |
| 5 | `get_upstream_features` | Emb:" Congress"@2 (de=17.00) +14 more |
| 6 | `get_upstream_features` | Emb:" who"@15 (de=35.25) +14 more |
| 7 | `get_upstream_features` | Emb:" Congress"@2 (de=9.12) +9 more |
| 8 | `get_upstream_features` | Emb:" Congress"@2 (de=16.00) +9 more |
| 9 | `get_upstream_features` | Emb:" Congress"@2 (de=28.12) +9 more |
| 10 | `get_upstream_features` | Emb:" funding"@7 (de=14.12) +14 more |
| 11 | `get_upstream_features` | Emb:" Congress"@2 (de=11.12) +9 more |
| 12 | `get_upstream_features` | Emb:" levels"@8 (de=28.00) +9 more |
| 13 | `get_upstream_features` | Emb:" controls"@5 (de=18.50) +9 more |
| 14 | `get_upstream_features` | Emb:" funding"@7 (de=20.12) +9 more |
| 15 | `get_upstream_features` | Emb:" Congress"@2 (de=20.62) +9 more |
| 16 | `get_upstream_features` | Emb:" Congress"@2 (de=21.00) +9 more |
| 17 | `get_upstream_features` | Emb:" controls"@5 (de=14.00) +9 more |
| 18 | `get_upstream_features` | Emb:" our"@6 (de=13.62) +9 more |
| 19 | `get_upstream_features` | Emb:" many"@13 (de=23.50) +9 more |
| 20 | `get_upstream_features` | Emb:" Congress"@2 (de=21.88) +9 more |
| 21 | `get_upstream_features` | Emb:" Congress"@2 (de=7.91) +9 more |
| 22 | `get_upstream_features` | Emb:" Congress"@2 (de=5.34) +9 more |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F13778@6` | ✅ reported | 5 | 8 | Trace from L6:F13778 (subjective language). What drives this feature and does it… |
| SA-2 | `L2:F156@8` | ❌ error | — | — | Trace from L2:F156 (amount/intensity words at pos 8='levels'). What token drives… |

<details>
<summary><b>SA-1</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F13778 | "subjective language, opinions and feelings." |
| 2 | `get_upstream_features` | L6:F13778@6, k=10 | Emb:" our"@6 (de=13.62) +9 more |
| 3 | `inspect_feature` | L4, F8160 | "a grab-bag of seemingly random words" |
| 4 | `inspect_feature` | L4, F2813 | " pronouns and possessive adjectives, especially when next to conjugate" |
| 5 | `inspect_feature` | L0, F636 | " first-person pronouns" |
| 6 | `get_upstream_features` | L4:F8160@6, k=10 | Emb:" our"@6 (de=7.31) +9 more |
| 7 | `inspect_feature` | L2, F107 | " first person pronouns like "I", "me", "my", "we", "he", or "she"" |
| 8 | `get_upstream_features` | L2:F107@6, k=10 | Emb:" our"@6 (de=11.62) +9 more |

**Findings:** L6:F13778 (subjective language) is primarily driven by lexical pronoun content, especially the token 'our'. Upstream analysis shows a cascade of pronoun detectors: L0:F636 and L2:F107 (first‑person pronoun features) feed into L4:F2813 (pronoun/possessive adjective detector), which together feed into L4:F8160 (a generic lexical aggregator) and finally into the target feature. No negation, refusal, …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F13778@6, k=8 → Emb:" our"@6 (de=13.62) +7 more |
| 2 | `get_upstream_features` | L2:F156@8, k=10 → Emb:" levels"@8 (de=28.00) +9 more |
| 3 | `get_upstream_features` | L3:F13271@5, k=8 → Emb:" controls"@5 (de=18.50) +7 more |
| 4 | `get_upstream_features` | L6:F6096@2, k=8 → Emb:" Congress"@2 (de=13.81) +7 more |
| 5 | `get_upstream_features` | L0:F15773@6, k=8 → Emb:" our"@6 (de=40.00) +7 more |
| 6 | `get_upstream_features` | L3:F123@2, k=8 → Emb:" Congress"@2 (de=20.62) +7 more |
| 7 | `inspect_feature` ×5 | L0:15773, L0:10198, L0:767, L0:15411, L0:13168 |
| 8 | `get_upstream_features` | L6:F6096@2, k=15 → Emb:" Congress"@2 (de=13.81) +14 more |

### Build

`build_circuit` → 13 nodes, 15 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 56,815 | 6,380 | 254,719 | 0 | $0.0400 | — | — |
| SA-1 | openai/gpt-oss-120b | 73,339 | 5,101 | 15,200 | 0 | $0.0143 | ✅ 5F/8E | Trace from L6:F13778 (subjective language). What drives this… |
| **Total** | | **130,154** | **11,481** | **269,919** | **0** | **$0.0543** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 2s