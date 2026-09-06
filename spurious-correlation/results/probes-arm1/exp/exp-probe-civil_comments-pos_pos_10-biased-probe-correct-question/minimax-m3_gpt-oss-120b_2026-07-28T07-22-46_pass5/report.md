# Circuit Oracle Report
**Date:** 2026-07-28 07:22:46 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_10 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by a chain of features that detect the mere presence of race-related vocabulary (the words "race", "black", "people", "mentioning") and the abstract concept of "mentioning race" — with no features encoding the toxic semantic content (e.g., the "bad cops are white" generalization, the assumption of whiteness, or the critique of media bias).

**Confidence:** 8

**Reasoning:** The attribution graph directly confirms the user's concern. The dominant late-layer features are all generic "race/ethnicity vocabulary" detectors that fire on the lexical surface:

- **L6:F3902** (pos 5,6, direct_effect +0.59/+0.27) — labeled "terms referring to race and ethnicity", max-activates on the token "▁race".
- **L6:F9228** (pos 6, -0.21) — "language regarding discrimination based on race, gender, religion, and disability", highly generic (frac_nonzero=0.60).
- **L4:F117** (pos 5,6,17, +0.27/+0.25/+0.24) — "terms related to race, racism, and social justice, with a particular focus on terms related to Black people" (the one feature that looks content-aware, yet its top activating examples are still about mentioning race, not the toxic claim itself).
- **L7:F8030** (pos 6, -0.19) — "words about people's races, origins, and demographic groups" (frac_nonzero=0.11, very generic).
- **L2:F10509** (pos 5, -0.49) — literally "the word 'race.'" Its strong negative direct_effect (suppresses "race" token) plus L0:F10682 (-0.84, L0 pos 5) and L0:F1823 ("Bureau", -0.19) round out a lexicon-only signal.

Tracing upstream from L6:F3902, the signal flows from `Emb: "race" (pos 5)` (direct_effect 11.0) and `Emb: "of" (pos 6)` (1.63) → early-layer race-token detectors (L0:F10682, L0:F2848, L2:F13158) → L2 race-word detector (F10509) → L3-L4 composition features (F6517 "mentioning", F13061 "race/gender/social issues", F117 "racism") → late-layer race concept (F3902, F9228, F8030) → output logit. The "black"/"people" tokens at pos 16-17 also feed in via L3:F13061 and L2:F13158 (both with the exact label "words about race and ethnicity"). Notably absent: any feature detecting "cops", "force", "helpless", "bad", "assumed", or "white" — the actual semantic content of the prompt. The `L0:F7820` "uncertainty" feature (-0.23) on "not" is the only non-race token-level signal, and it weakly suppresses rather than encodes the toxic content.

This is a textbook spurious-correlation circuit: the probe is essentially a "does this mention race?" classifier, not a toxicity classifier. Any sentence containing "race" + "black" + "people" — e.g., a neutral academic discussion, a news headline, or even an anti-racist statement — would receive a similar score. The circuit provides no evidence that the model (via the probe) is reading the *content* of the claim.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: ' race' (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 16 | Emb: ' black' (pos 16) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: ' people' (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: ' of' (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: ' mentioning' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F10682](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10682) | 5 | Early-layer race/ethnicity token detectors (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10682) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 5 | Early-layer race/ethnicity token detectors (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 6 | Early-layer race/ethnicity token detectors (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F11851](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11851) | 5 | Early-layer race/ethnicity token detectors (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11851) |
| [L0:F16013](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16013) | 16 | Early-layer race/ethnicity token detectors (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16013) |
| [L0:F9076](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9076) | 17 | Early-layer race/ethnicity token detectors (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9076) |
| [L0:F5970](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5970) | 17 | Early-layer race/ethnicity token detectors (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5970) |
| [L0:F6949](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6949) | 17 | Early-layer race/ethnicity token detectors (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6949) |
| [L1:F3020](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3020) | 16 | Early-layer race/ethnicity token detectors (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3020) |
| [L1:F12717](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12717) | 16 | Early-layer race/ethnicity token detectors (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12717) |
| [L1:F13646](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) | 16 | Early-layer race/ethnicity token detectors (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) |
| [L1:F4679](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4679) | 16 | Early-layer race/ethnicity token detectors (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4679) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 5 | Early-layer race/ethnicity token detectors (L0-L2) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 16 | Early-layer race/ethnicity token detectors (L0-L2) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F1708](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1708) | 16 | Early-layer race/ethnicity token detectors (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1708) |
| [L2:F10509](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10509) | 5 | L2: 'race' word detector (L2:F10509) |  the word "race." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10509) |
| [L3:F6517](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6517) | 3 | Mid-layer mention + race composition (L3-L4) |  words related to mentioning something | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6517) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 17 | Mid-layer mention + race composition (L3-L4) |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L3:F15128](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15128) | 6 | Mid-layer mention + race composition (L3-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15128) |
| [L3:F3678](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3678) | 6 | Mid-layer mention + race composition (L3-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3678) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 5 | Mid-layer mention + race composition (L3-L4) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 6 | Mid-layer mention + race composition (L3-L4) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 17 | Mid-layer mention + race composition (L3-L4) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F5584](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5584) | 6 | Mid-layer mention + race composition (L3-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5584) |
| [L4:F88](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/88) | 6 | Mid-layer mention + race composition (L3-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/88) |
| [L4:F11200](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11200) | 1 | Mid-layer mention + race composition (L3-L4) |  a variety of words and phrases related to authorship and origination of something. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11200) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 6 | Late-layer race/ethnicity concept features (L6-L7) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 5 | Late-layer race/ethnicity concept features (L6-L7) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F9228](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9228) | 6 | Late-layer race/ethnicity concept features (L6-L7) |  language regarding discrimination based on race, gender, religion, and disability | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9228) |
| [L7:F8030](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8030) | 6 | Late-layer race/ethnicity concept features (L6-L7) |  words about people's races, origins, and demographic groups | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8030) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Output logit (probe direction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:3902 de=0.586 |
| 3 | `inspect_feature` ×12 | L6:3902, L2:10509, L4:117, L0:7820, L6:9228, L3:13061, L0:1823, L7:8030, L4:11200, L3:6517, L0:2961, L2:13158 |
| 4 | `get_upstream_features` | Emb:" race"@5 (de=11.00) +9 more |
| 5 | `get_upstream_features` | Emb:" race"@5 (de=30.12) +9 more |
| 6 | `get_upstream_features` | Emb:" race"@5 (de=19.00) +9 more |
| 7 | `get_upstream_features` | Emb:" black"@16 (de=11.38) +9 more |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F5584@6` | ❌ error | — | — | Trace this feature back to its origin. What is L4:F5584 at pos 6 detecting? Trac… |
| SA-2 | `L0:F10682@5` | ❌ error | — | — | Trace L0:F10682 upstream. What is it detecting and how does it relate to the 'ra… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F5584@6, k=10 → Emb:" race"@5 (de=16.62) +9 more |
| 2 | `get_upstream_features` | L0:F10682@5, k=10 → Emb:" race"@5 (de=22.62) +9 more |
| 3 | `get_upstream_features` | L2:F13158@16, k=10 → Emb:" black"@16 (de=10.94) +9 more |

### Build

`build_circuit` → 11 nodes, 10 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 27,956 | 4,412 | 118,171 | 0 | $0.0208 | — | — |
| **Total** | | **27,956** | **4,412** | **118,171** | **0** | **$0.0208** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 0s