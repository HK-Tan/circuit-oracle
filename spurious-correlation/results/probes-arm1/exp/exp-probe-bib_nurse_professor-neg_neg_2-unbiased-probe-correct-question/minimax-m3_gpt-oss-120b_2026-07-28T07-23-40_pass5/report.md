# Circuit Oracle Report
**Date:** 2026-07-28 07:23:40 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of "profession" is driven by a mix of genuine profession indicators (the literal word "Engineering", academic degree markers, the named entity "Daniel", and biographical phrase patterns like "received") and several clearly spurious signals (the male pronoun "his", year-decade features for "1993/2002", the generic temporal word "later", and incidental features like "legal citation" at the "Beirut" token), with the positive profession signal partially canceled by inhibitory degree-reference and date features that are not specific to the profession.

**Confidence:** 7

**Reasoning:**

**Positive (toward profession classification) signal:**
- **Profession word indicator** (L1:F1372, direct_effect=+0.064, frac_nonzero=0.0077): fires on the literal token " Engineering" at pos 9 (direct embedding effect = 19.0). This is a genuine, surface-level profession token cue — the model has a dedicated "engineer"-word detector. This is the most legitimate feature in the circuit.
- **Canada/Canadian places** (L14:F5600 direct_effect=+0.064, L7:F8870 +0.0386, L4:F8439 +0.033, L0:F4687 +0.047): a four-layer stack all driven primarily by the " Waterloo" token embedding (direct_effect 12.6–17.25). Note F4687 is "place names" generic, F8439/L8870/F5600 are progressively more Canada-specific. This is essentially a "Waterloo is Canadian university" chain — it correlates with academic profession, but is location/ethnicity-correlated rather than profession-specific (a Canadian studies professor would also trigger this).
- **Academic degree references** (L7:F14129, direct_effect=+0.044 at pos 50 "D", +0.033 at pos 26): explicitly labels as "academic degrees, universities, and people associated with them" — a legitimate, profession-correlated signal (PhD holders tend to be academics/engineers). frac_nonzero=0.0042 confirms it's a degree-specific feature.
- **Person's name "Daniel"** (L2:F16309, direct_effect=+0.049): a name-recognition feature firing on pos 1. This is a generic name feature, not profession-specific — it fires on any proper name.
- **Biographical phrase starter** (L0:F15320 "received" +0.058, L0:F7905 "route" -0.047 at pos 2, L0:F13553 verbs +0.036, L0:F2085 "reception" -0.041): These are all firing on the "received" token at pos 2. The "received his degree" pattern is a biographical-genre cue rather than a profession cue. The mixed signs (F15320 "ice/word feature" actually fires on "received" → +0.058; F7905 "route" also at pos 2 → -0.047) suggest the layer-0 features here are mostly noise that happens to activate on this common bio-text token.

**Negative (against profession) signal — the spurious features:**
- **Male pronoun "his/he"** (L0:F2994, direct_effect=-0.036 at pos 3, frac_nonzero=0.073): This is the canonical "his" detector (max_act=76 on "his"). The pronoun "his" at pos 3 is a **gender marker**, not a profession indicator. The autointerp is literally "the pronoun 'his' and the pronoun 'he.'" With frac_nonzero=0.073 this is a high-frequency generic pronoun feature that the probe inherits as a "man in tech → engineer" prior. This is the precise concern the user raised. L0:F12235 (also at pos 6, -0.039) is a legal-document word feature that happens to activate near the pronoun region.
- **1990s decade + year digits** (L0:F11333/F11132/F618/F6515, all direct_effect ≈ -0.045 at pos 18/19; L2:F14934 +0.036 at pos 19): F11333 "the 1990's", F11132 "his + historical records + years", F618 "years", F6515 "the year 199X or 200X" — all firing on the year "1993" / "2002" tokens. These are date features, not profession features, and they push *against* the profession classification.
- **Generic temporal connector "later"** (L0:F2743, direct_effect=-0.069, max on token "later"): firing on "He later earned" at pos 23. This is a stopword/temporal-discourse marker, completely unrelated to profession.
- **Legal citation / academic publication** (L6:F3235 "academic publications, math, scientific institutions" -0.055, L6:F7546 "personal names, locations, Middle East" -0.044 at pos 38 "Beirut", L6:F7604 "legal citations ending in digit + d" -0.033 at pos 19): These fire on the location tokens "Beirut" and on year-digits. They are academic/genre features, not profession features. The "Beirut" embedding pulls in a Middle East location feature (F7546) — ethnicity/geography correlated.
- **Academic degree references (inhibitory)** (L6:F2254 "references to academic degrees" -0.044, L2:F13360 -0.038, L2:F10852 -0.033 at pos 50 "D"): These are degree-word features at "Ph.D" that paradoxically push *against* the profession probe. This is suspicious: if the probe is genuinely a profession classifier, degree words should be neutral or positive, not inhibitory. It suggests the probe may be detecting some narrower pattern (e.g., "researcher who does Robotics" specifically) where the PhD mention shifts things, or that the probe is partially anti-correlated with the most obvious degree-text features.

**Verdict on the user's concern:** The concern is well-supported. The circuit shows the probe uses **several spurious surface features rather than only genuine profession indicators**:

1. **Gender marker**: L0:F2994 ("his/he") is a high-frequency male-pronoun detector (frac_nonzero=0.073) that contributes negatively to the probe — the model is using masculine pronouns as a (mild) profession cue, consistent with gender bias in the training data.
2. **Date features**: Multiple year-decade features (F11333, F11132, F618, F6515) fire on "1993" and "2002" and push against the classification. These are date-noise, not profession-related.
3. **Temporal connector**: F2743 "later" is pure stopword noise.
4. **Location features masquerading as profession**: The Waterloo→Canada chain is the largest positive contribution, and it's ethnicity/location-correlated, not profession-specific.
5. **Inhibitory degree features**: F2254 firing on "Ph.D" with negative direct effect is counter-intuitive for a profession probe and suggests the probe has learned a non-obvious pattern that isn't simply "PhD = professional."

The strongest genuine profession signal is the single L1:F1372 "engineer/Engineering" token detector. Everything else is either correlational (Canada, names, biographical phrasing) or genuinely spurious (pronouns, dates, "later", legal-citation features). The probe is *partially* using real profession words but is significantly contaminated by gender markers, dates, and location features.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L1:F1372](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1372) | 9 | Profession word indicator (Engineering) | the word "engineer" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1372) |
| [L14:F5600](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5600) | 14 | Canada/Canadian places |  places and regions, particularly in Canada | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5600) |
| [L7:F8870](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8870) | 14 | Canada/Canadian places | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8870) |
| [L4:F8439](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8439) | 14 | Canada/Canadian places | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8439) |
| [L0:F4687](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4687) | 14 | Canada/Canadian places | place names | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4687) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 50 | Academic degree references (Ph.D) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 26 | Academic degree references (Ph.D) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L2:F16309](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16309) | 1 | Person's name (Daniel) |  people's names | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16309) |
| [L0:F15320](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) | 2 | Biographical phrase starter |  the word "ice" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) |
| [L0:F13553](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13553) | 2 | Biographical phrase starter |  verbs in the past tense or past participle | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13553) |
| [L0:F7905](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7905) | 2 | Biographical phrase starter |  the word "route," referencing paths, directions, or means of transportation | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7905) |
| [L0:F2085](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2085) | 2 | Biographical phrase starter |  the word "reception" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2085) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 3 | Male pronoun 'his/he' (gender marker) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F12235](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12235) | 6 | Male pronoun 'his/he' (gender marker) |  words related to legal documents and hunting | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12235) |
| [L0:F11333](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11333) | 19 | 1990s decade + year digits |  the 1990's | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11333) |
| [L0:F11132](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11132) | 19 | 1990s decade + year digits |  a mix of possessive pronouns like "his", names associated with historical records, and years. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11132) |
| [L0:F618](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/618) | 19 | 1990s decade + year digits |  years | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/618) |
| [L2:F14934](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14934) | 19 | 1990s decade + year digits |  years in the 1900s | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14934) |
| [L0:F6515](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) | 18 | 1990s decade + year digits |  the year 199X or 200X. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) |
| [L6:F3235](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) | 38 | Legal citation / academic publication |  academic publications, math, and scientific institutions | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) |
| [L6:F7546](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7546) | 38 | Legal citation / academic publication | a mix of personal names, locations, and food dishes, particularly those from the Middle East with "di" in the name | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7546) |
| [L6:F7604](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7604) | 19 | Legal citation / academic publication |  legal citations ending in a digit followed by "d" | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7604) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 50 | Academic degree references (inhibitory) | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L2:F13360](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13360) | 50 | Academic degree references (inhibitory) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13360) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 50 | Academic degree references (inhibitory) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L0:F2743](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2743) | 23 | Generic temporal connector 'later' | the word 'later' | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2743) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe output (profession classifier) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: Engineering (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: Waterloo (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Daniel (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: his (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 23 | Emb: later (pos 23) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 48 | Emb: Ph (pos 48) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 18 | Emb: 2002 (pos 18) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 19 | Emb: 1993 (pos 19) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 38 | Emb: Beirut (pos 38) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2743 de=-0.069 |
| 3 | `inspect_feature` ×6 | L1:1372, L14:5600, L0:15320, L2:16309, L0:4687, L7:14129 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L1:F1372@9` | ❌ error | — | — | Trace upstream from L1:F1372 ("the word engineer") at position 9. Find what inpu… |
| SA-2 | `L14:F5600@14` | ❌ error | — | — | Trace upstream from L14:F5600 ("places and regions, particularly in Canada") at … |
| SA-3 | `L7:F14129@50` | ❌ error | — | — | Trace upstream from L7:F14129 ("academic degrees, universities, and people assoc… |
| SA-4 | `L0:F2743@23` | ❌ error | — | — | Trace upstream from L0:F2743 (negative direct_effect) at position 23. Find what … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L1:F1372@9, k=10 → Emb:" Engineering"@9 (de=19.00) +9 more |
| 2 | `get_upstream_features` | L14:F5600@14, k=10 → L7:F8870 (de=15.94) +9 more |
| 3 | `get_upstream_features` | L7:F14129@50, k=10 → L6:F2254 (de=7.31) +9 more |
| 4 | `get_upstream_features` | L0:F15320@2, k=10 → Emb:" received"@2 (de=13.00) +9 more |
| 5 | `get_upstream_features` | L2:F16309@1, k=10 → Emb:"Daniel"@1 (de=12.94) +9 more |
| 6 | `get_upstream_features` | L0:F4687@14, k=10 → Emb:" Waterloo"@14 (de=16.25) +9 more |
| 7 | `get_top_features` | token="", k=30 → 30 features; top: L0:2743 de=-0.069 |
| 8 | `inspect_feature` ×15 | L0:11333, L0:11132, L0:6515, L0:7905, L0:2994, L0:618, L0:13553, L6:7604, L2:14934, L6:3235, L6:7546, L6:2254, L0:2085, L0:12235, L0:2743 |
| 9 | `get_upstream_features` | L7:F8870@14, k=10 → L4:F8439 (de=9.00) +9 more |
| 10 | `get_upstream_features` | L4:F8439@14, k=10 → Emb:" Waterloo"@14 (de=17.25) +9 more |
| 11 | `get_upstream_features` | L6:F2254@50, k=5 → L2:F10852 (de=12.31) +4 more |
| 12 | `get_upstream_features` | L6:F3235@38, k=5 → Emb:" Beirut"@38 (de=1.85) +4 more |
| 13 | `get_upstream_features` | L6:F7546@38, k=5 → Emb:" Beirut"@38 (de=15.06) +4 more |
| 14 | `get_upstream_features` | L0:F2743@23, k=5 → Emb:" later"@23 (de=42.25) +4 more |
| 15 | `get_upstream_features` | L0:F2994@3, k=5 → Emb:" his"@3 (de=43.25) +4 more |

### Build

`build_circuit` → 20 nodes, 20 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 55,830 | 7,301 | 196,474 | 0 | $0.0373 | — | — |
| **Total** | | **55,830** | **7,301** | **196,474** | **0** | **$0.0373** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 7s