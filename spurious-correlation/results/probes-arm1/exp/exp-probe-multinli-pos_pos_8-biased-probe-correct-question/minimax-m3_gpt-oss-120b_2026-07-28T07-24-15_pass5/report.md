# Circuit Oracle Report
**Date:** 2026-07-28 07:24:15 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_8 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "contradiction" score is driven almost entirely by topic-entity features ("Congress", "controls", "funding", "political parties", "yield") anchored to the *premise* side of the premise/hypothesis pair — the *contradiction* label here is correlated with the model recognizing that the premise describes "Congress controls funding," not with any contradiction signal.

**Confidence:** 3

**Reasoning:** This attribution graph traces a *probe* (a linear classifier on residual-stream activations), not a next-token distribution, so the conventional "negation drives contradiction" hypothesis doesn't directly apply — there is no decision boundary on vocabulary logits. What I find instead is more troubling in a different way:

1. **All top-30 features are lexical/entity features on the premise.** F7021 ("the word 'Congress'", pos 2, direct_effect=+0.31), F3276 ("mentions of the U.S. Congress", L1 pos 2, +0.32), F2701 ("words related to the U.S. Congress", L2 pos 2, +0.38), F6096 ("political parties and affiliations", L6 pos 2, +0.45) are all *Congress/partisan entity* features on the very first content token of the premise. The opposite-polarity pair — F6735 ("political parties and politicians", L2 pos 2, -0.40) and F6948 (L1 pos 2, -0.39) — pushes the other way on the *same* position. The whole signal at pos 2 is a Congress-political tug-of-war; the winning direction is "Congress / political-party" topic presence.

2. **Premise-side syntax tokens ("funding", "levels", "controls", "our", "who", "many", "to") are doing real work.** F11606 ("fund", pos 7, -0.36), F15773 ("our", pos 6, but with strong inhibition downstream at F13778 L6, -0.31), F13437/F195 ("who", pos 15, -0.58 combined), F15792 ("many", pos 13, but pulled by F8382 L3 pos 13, +0.33), F13564 ("which", pos 4, +0.28) and F12596 (L3 pos 11, -0.30) all carry large direct effects. These are *not* negation cues ("no", "not", "never", "did not"), but they are equally content-free from the standpoint of NLI: the model is not reading that the *hypothesis* contradicts the premise; it is reacting to surface tokens like "funding", "our", "who", "many" appearing at particular positions.

3. **The "yield" feature (L0:F6044, pos 2, +0.79) is a misnomer** — its top-activating examples are the noun "yield" in finance/manufacturing. At pos 2 ("Congress") it acts as a generic-formatting/sub-word feature (its embedding-edge direct_effect=17 from the Congress token suggests it's a tokenization sub-piece that happens to fire on capital-C words). It carries the single largest direct effect in the graph, which is suspicious — it's a spurious token-internal feature, not a semantic one.

4. **No hypothesis-side signal is visible.** I did not find any feature that reads the hypothesis "the congress has no responsibility when it comes to controlling funding levels" as a *negation* of the premise. The hypothesis-side token at pos 15 is "who" (in "...members who did not support..."); the token at the actual negation is not separately represented. The probe appears to score *high* (positive contribution from F6096, F2701, F3276) whenever the *premise* contains a political/government topic, independent of whether the hypothesis agrees or contradicts it.

5. **The user's concern is half-right but in a different way than they framed it.** The circuit is not driven by negation-word features; it is driven by **entity/topical features on the premise** (Congress, political parties, funding) that are mostly *content* but with a strong spurious component from single-word L0/L1 features like F6044 ("yield" - misfiring on "Congress"), F6948 ("lift" - misfiring on "Congress"), F8982/F12456 (Indian organization names - misfiring on "Congress"), F9135 (music/song - misfiring on "funding"). These features are pos 2 firing on "Congress" and pos 7 firing on "funding" — they look like token-overlap artifacts from the transcoder rather than negation artifacts. The probe is picking up on **"is this sentence about Congress / government / funding?"** as a high-level topic signature, which is a real semantic signal, not a negation-cue artifact. But because the *same* topic signature would fire on the premise in an *entailment* pair that says the same thing, the probe's contradiction score is also picking up a topical-bias signal that conflates "this is a government/funding topic" with "contradiction" — a topic-conditional shortcut.

The circuit reaches the output through three late-ish stages (l1_congress_entities → l2_congress_topics → l3_context_features → l6_political_features → output), all anchored to pos 2 ("Congress") in the premise, with a strong L0 spurious layer (l0_congress_words, l0_funding_features) feeding upward. Trace depth reaches the token-embedding nodes for ' Congress' (pos 2), ' funding' (pos 7), ' levels' (pos 8), ' controls' (pos 5), ' our' (pos 6), ' who' (pos 15), ' to' (pos 11), and ' many' (pos 13).

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F7021](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7021) | 2 | L0: word 'Congress' (F7021) + 'yield' (F6044) at pos 2 — entity/formatting features on the Congress token |  the word "Congress" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7021) |
| [L0:F6044](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) | 2 | L0: word 'Congress' (F7021) + 'yield' (F6044) at pos 2 — entity/formatting features on the Congress token | the word "yield" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) |
| [L0:F2470](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2470) | 2 | L0: word 'Congress' (F7021) + 'yield' (F6044) at pos 2 — entity/formatting features on the Congress token | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2470) |
| [L0:F13437](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13437) | 15 | L0: 'who' features (F13437, F195) at pos 15 — relative-pronoun features | the word "who" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13437) |
| [L0:F195](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/195) | 15 | L0: 'who' features (F13437, F195) at pos 15 — relative-pronoun features | the word "who" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/195) |
| [L0:F11606](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11606) | 7 | L0: 'fund' word feature (F11606) at pos 7, plus F13929/F9135 also on 'funding' |  the word "fund" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11606) |
| [L0:F13929](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13929) | 7 | L0: 'fund' word feature (F11606) at pos 7, plus F13929/F9135 also on 'funding' |  instances of the word "power" in a political or technical context | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13929) |
| [L0:F9135](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9135) | 7 | L0: 'fund' word feature (F11606) at pos 7, plus F13929/F9135 also on 'funding' |  mentions of music, specifically songs, and also the word "blank". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9135) |
| [L0:F15773](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15773) | 6 | L0: 'our' feature (F15773) at pos 6 — strong (act=40) |  the possessive pronoun "our" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15773) |
| [L0:F9557](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9557) | 2 | L0: 'our' feature (F15773) at pos 6 — strong (act=40) | the word "clean" and words/phrases associated with people | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9557) |
| [L0:F15792](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15792) | 13 | L0: 'many' feature (F15792) at pos 13 |  the word "many" (and to a lesser extent, similar words like "multiple" and "several"). | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15792) |
| [L0:F13564](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13564) | 4 | L0: 'which' feature (F13564) at pos 4 | the word "which" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13564) |
| [L1:F3276](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3276) | 2 | L1: U.S. Congress mentions (F3276) and other entity-style features at pos 2 |  mentions of the United States Congress | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3276) |
| [L1:F8982](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8982) | 2 | L1: U.S. Congress mentions (F3276) and other entity-style features at pos 2 |  names of organizations, particularly related to India, and words associated with formal groups | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8982) |
| [L1:F12456](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12456) | 2 | L1: U.S. Congress mentions (F3276) and other entity-style features at pos 2 |  names of organizations, particularly governmental or religious institutions, especially of Indian origin. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12456) |
| [L1:F2116](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2116) | 7 | L1: U.S. Congress mentions (F3276) and other entity-style features at pos 2 |  words and phrases related to legal counsel or representation | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2116) |
| [L1:F6853](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6853) | 2 | L1: U.S. Congress mentions (F3276) and other entity-style features at pos 2 | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6853) |
| [L1:F4224](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4224) | 2 | L1: U.S. Congress mentions (F3276) and other entity-style features at pos 2 | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4224) |
| [L1:F6948](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6948) | 2 | L1: F6948 ('lift', act=11) at pos 2 — generic single-word feature, low-specificity |  the word "lift" in the context of mechanical devices or ski infrastructure | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6948) |
| [L2:F2701](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) | 2 | L2: U.S. Congress topic features at pos 2 — F2701 (Congress topic, act=22), F6735 (political parties, act=18, NEGATIVE), and F156 at pos 8 (NEGATIVE on 'levels') |  words related to the U.S. Congress | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) |
| [L2:F6735](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6735) | 2 | L2: U.S. Congress topic features at pos 2 — F2701 (Congress topic, act=22), F6735 (political parties, act=18, NEGATIVE), and F156 at pos 8 (NEGATIVE on 'levels') |  political parties and politicians | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6735) |
| [L2:F156](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/156) | 8 | L2: U.S. Congress topic features at pos 2 — F2701 (Congress topic, act=22), F6735 (political parties, act=18, NEGATIVE), and F156 at pos 8 (NEGATIVE on 'levels') | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/156) |
| [L3:F123](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/123) | 2 | L3: context features — F123 (Congress pos 2, act=14), F13271 ('controls' pos 5, act=11), F8382 ('many' pos 13, act=14), F12596 (pos 11, act=15) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/123) |
| [L3:F13271](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13271) | 5 | L3: context features — F123 (Congress pos 2, act=14), F13271 ('controls' pos 5, act=11), F8382 ('many' pos 13, act=14), F12596 (pos 11, act=15) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13271) |
| [L3:F8382](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8382) | 13 | L3: context features — F123 (Congress pos 2, act=14), F13271 ('controls' pos 5, act=11), F8382 ('many' pos 13, act=14), F12596 (pos 11, act=15) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8382) |
| [L3:F12596](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12596) | 11 | L3: context features — F123 (Congress pos 2, act=14), F13271 ('controls' pos 5, act=11), F8382 ('many' pos 13, act=14), F12596 (pos 11, act=15) |  actions or methods, sometimes preceeded by the preposition 'a' or 'to'. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12596) |
| [L6:F6096](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6096) | 2 | L6: political-party/Congress features at pos 2 (F6096 act=21, POS on probe) and pos 6 (F13778 NEGATIVE on 'our') |  political parties and affiliations | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6096) |
| [L6:F13778](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/13778) | 6 | L6: political-party/Congress features at pos 2 (F6096 act=21, POS on probe) and pos 6 (F13778 NEGATIVE on 'our') | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/13778) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:6044 de=0.789 |
| 3 | `inspect_feature` ×4 | L0:6044, L6:6096, L2:2701, L1:2116 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F6044@2` | ❌ error | — | — | Trace this L0 "yield" feature upstream at position 2. What is its connection to … |
| SA-2 | `L1:F2116@7` | ❌ error | — | — | Trace L1:F2116 (legal counsel feature) at pos 7 upstream. What input is it about… |
| SA-3 | `L2:F156@8` | ❌ error | — | — | Trace L2:F156 at pos 8 upstream. Find what it represents and which input token. |
| SA-4 | `L3:F123@2` | ❌ error | — | — | Trace L3:F123 at pos 2 upstream. What is this feature and which input? |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F6044@2, k=15 → Emb:" Congress"@2 (de=17.00) +14 more |
| 2 | `get_upstream_features` | L1:F2116@7, k=15 → Emb:" funding"@7 (de=14.12) +14 more |
| 3 | `get_upstream_features` | L2:F156@8, k=15 → Emb:" levels"@8 (de=28.00) +14 more |
| 4 | `get_upstream_features` | L3:F123@2, k=15 → Emb:" Congress"@2 (de=20.62) +14 more |
| 5 | `get_upstream_features` | L3:F13271@5, k=15 → Emb:" controls"@5 (de=18.50) +14 more |
| 6 | `get_upstream_features` | L3:F8382@13, k=15 → Emb:" many"@13 (de=23.50) +14 more |
| 7 | `get_upstream_features` | L6:F13778@6, k=15 → Emb:" our"@6 (de=13.62) +14 more |
| 8 | `get_upstream_features` | L0:F9529@5, k=10 → Emb:" controls"@5 (de=14.00) +9 more |
| 9 | `inspect_feature` ×6 | L0:15792, L0:15773, L0:13437, L2:6735, L1:6948, L0:9557 |
| 10 | `get_upstream_features` | L6:F6096@2, k=10 → Emb:" Congress"@2 (de=13.81) +9 more |
| 11 | `inspect_feature` ×5 | L0:11606, L0:7021, L1:3276, L1:8982, L1:12456 |
| 12 | `get_top_features` | token="", k=30 → 30 features; top: L0:6044 de=0.789 |
| 13 | `inspect_feature` ×6 | L0:195, L0:10783, L0:13564, L3:12596, L0:9135, L0:13929 |
| 14 | `get_upstream_features` | L0:F9135@7, k=5 → Emb:" funding"@7 (de=16.88) +4 more |
| 15 | `get_upstream_features` | L0:F13929@7, k=5 → Emb:" funding"@7 (de=13.94) +4 more |
| 16 | `get_upstream_features` | L0:F13437@15, k=5 → Emb:" who"@15 (de=35.25) +4 more |
| 17 | `get_upstream_features` | L0:F2470@2, k=5 → Emb:" Congress"@2 (de=6.91) +4 more |
| 18 | `get_upstream_features` | L3:F12596@11, k=5 → Emb:" to"@11 (de=21.62) +4 more |
| 19 | `get_upstream_features` | L6:F13778@6, k=5 → Emb:" our"@6 (de=13.62) +4 more |

### Build

`build_circuit` → 20 nodes, 30 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 48,800 | 6,760 | 293,400 | 0 | $0.0404 | — | — |
| **Total** | | **48,800** | **6,760** | **293,400** | **0** | **$0.0404** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 56s