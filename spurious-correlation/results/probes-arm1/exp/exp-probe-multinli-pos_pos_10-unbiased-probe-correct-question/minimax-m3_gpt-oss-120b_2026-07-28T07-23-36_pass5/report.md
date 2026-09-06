# Circuit Oracle Report
**Date:** 2026-07-28 07:23:36 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_10 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

The circuit has been built. Let me finalize my analysis.

**Analysis:** The probe's contradiction classification score is driven almost entirely by shallow lexical features detecting the function words "not", "now", "on", "role", and the superlative suffix "-est" / "strange" — not by features encoding the actual semantic content of the premise or hypothesis.

**Confidence:** 8

**Reasoning:**

The circuit traces the probe's classification score (output node at L26) back to a small set of mid-layer features (L4–L12) that all share a striking common property: they are **shallow lexical/grammatical detectors** rather than semantic-concept features.

**Key late-layer features feeding the probe (L6–L12):**
- **L6:F12420 at pos 4** (direct_effect ≈ -0.34): "artistic elements that break established guidelines" — activated by the token "reversal" in the *premise* via L1:F2580 ("reverse" detector).
- **L4:F5709 at pos 9** (direct_effect ≈ -0.37): "astronomy terms" — activated by the token " now" via L0:F5232 ("now" word detector). This fires generically on "now" and is a misfire unrelated to "MASS/astronomy" content.
- **L10:F6670 at pos 19/21** (direct_effect ≈ +0.28): "technical/scientific terms" — fired on the second "reversal" and "on" in the hypothesis.
- **L12:F12606 at pos 19/21** (direct_effect ≈ +0.21): "political conspiracy / mental conditions" — fired on the *repetition* of "reversal"/"on" in the hypothesis.

**What drives these late features — the spurious path:**
- **Emb " not" (pos 17) → L0:F4958** ("not" detector, frac_nonzero=0.018) → **L3:F12079** ("negations and Chinese names") → **L3:F1101** ("error messages / negation terms") → **L4:F4492** ("negations in various languages") → **L4:F2422** (same theme) → late features.
- **Emb " now" (pos 9) → L0:F5232** ("now" detector) → L3:F7449 / L3:F1438 ("now" word detectors).
- **Emb " strangest" (pos 2) → L1:F15749** ("strange/strangest" detector) → L2:F10827 ("strikingness/emotional impact") and L2:F16097 ("superlative -est") → L4:F12799 ("-ly" / "oddities" detector) — note this feature's promoted tokens are exactly "weird/strange/strangely"!
- **Emb " role" (pos 3) → L4:F14368** ("role" detector, promoted token literally "role") → L4:F7409 ("reverse/inverse/around") → L5:F9068 ("populations/structures") → L6:F12420.

**Why this confirms the user's concern:**
1. **The probe is NOT using entailment-relevant features.** The single strongest positive feature (L10:F6670) and a major negative feature (L4:F5709) both fire on common function words like "now", "on", and "reversal" — they have high base rates (frac_nonzero 0.07+) and their top activating examples are about astronomy/technical jargon entirely unrelated to NLI.
2. **The negation signal is purely lexical.** Multiple "not" detectors (L0:F4958, L3:F12079, L4:F4492) form a feature chain that fires whenever the token "not" appears anywhere, regardless of scope. The token "not" here appears in the hypothesis ("There is **not** role reversal going on right now in relation to democracy"), and the chain amplifies this single token into a strong negative or positive contribution to the probe — even though the actual logical negation pattern is subtle (it negates an entire clause).
3. **"Strangest" and "role reversal" are handled as surface lexical patterns.** L4:F12799 detects "-ly" words and "oddities"; L1:F15749 detects "strange" generically. These are not encoding the meaning of "strangest" — they're matching token-shape patterns.
4. **The same lexical features that fire on the premise ("role reversal", "strangest") fire again on the hypothesis ("reversal", "on")**, giving the L10:L6670 and L12:L12606 features their dual positive effects. The probe is essentially reading off *token repetition between premise and hypothesis* and the *presence of "not"*, both of which are classic spurious NLI cues (annotation artifacts where annotators labeled any repeated-content-with-negation pair as contradiction).

The user's hypothesis is confirmed: the contradiction classifier relies on **superficial negation-word signals and lexical overlap** ("not", "now", "on", "strangest", "reversal" token repetition) rather than computing the actual semantic relationship between the premise and hypothesis.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: ' not' (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: ' strangest' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: ' role' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: ' now' (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: '.' (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: ' There' (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 17 | Negation word 'not' detector (L0) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F5232](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5232) | 9 | 'now' word detector (L0) |  the word "now" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5232) |
| [L0:F7696](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7696) | 21 | 'on' preposition detector (L0) | the word "on" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7696) |
| [L1:F15749](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15749) | 2 | 'strange/strangest' word detectors (L1-L2) |  the word "strange", or related words | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15749) |
| [L1:F2580](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2580) | 4 | 'strange/strangest' word detectors (L1-L2) | the word "reverse" in code snippets | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2580) |
| [L2:F16097](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) | 2 | Superlative '-est' suffix and 'strange/odd' detectors (L2-L3) | superlative adjectives and the words "test" or "point" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) |
| [L2:F10827](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10827) | 2 | Superlative '-est' suffix and 'strange/odd' detectors (L2-L3) |  words that reflect strikingness or emotional impact | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10827) |
| [L3:F319](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/319) | 2 | Superlative '-est' suffix and 'strange/odd' detectors (L2-L3) |  words ending in the suffix "-est" or "-ier" (the superlative and comparative suffixes). | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/319) |
| [L3:F8960](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8960) | 2 | Superlative '-est' suffix and 'strange/odd' detectors (L2-L3) |  words related to how other people are perceived | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8960) |
| [L3:F12079](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) | 17 | Multilingual negation/absence detectors (L3-L4) | negations and Chinese names | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 17 | Multilingual negation/absence detectors (L3-L4) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 17 | Multilingual negation/absence detectors (L3-L4) | negations in other languages like French, Malay, and Croatian | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L3:F1101](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) | 17 | Multilingual negation/absence detectors (L3-L4) |  error messages and terms indicating absence or negation in software contexts. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 17 | Multilingual negation/absence detectors (L3-L4) |  a mix of words and code fragments from different languages | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L3:F1438](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1438) | 9 | 'now' word detectors at L3 (L3) | the word "now" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1438) |
| [L3:F7449](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7449) | 9 | 'now' word detectors at L3 (L3) |  the word "now" often in the context of describing current situations | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7449) |
| [L4:F7409](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7409) | 4 | Role/reverse/structure detectors (L4-L5) |  words like "vice versa", "inverse", "reverse", "around", or directions | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7409) |
| [L4:F14368](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14368) | 4 | Role/reverse/structure detectors (L4-L5) |  words related to importance or roles in a system | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14368) |
| [L5:F9068](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9068) | 4 | Role/reverse/structure detectors (L4-L5) | words and phrases related to populations | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9068) |
| [L4:F12799](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12799) | 2 | Role/reverse/structure detectors (L4-L5) |  words ending in "-ly" along with phrases that contain the word 'odd' or 'oddities' | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12799) |
| [L6:F12420](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12420) | 4 | Role/reverse/structure detectors (L4-L5) |  artistic elements that break established guidelines | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12420) |
| [L4:F5709](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) | 9 | Late-layer negation/superlative features driving probe (L6-L10) | astronomy terms | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) |
| [L4:F6072](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6072) | 9 | Late-layer negation/superlative features driving probe (L6-L10) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6072) |
| [L10:F6670](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) | 19 | Late-layer negation/superlative features driving probe (L6-L10) | technical terms, especially within scientific or medical contexts | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) |
| [L10:F6670](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) | 21 | Late-layer negation/superlative features driving probe (L6-L10) | technical terms, especially within scientific or medical contexts | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) |
| [L12:F12606](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) | 21 | Late-layer negation/superlative features driving probe (L6-L10) |  phrases related to political conspiracy/organizations, mental conditions and storytelling terms | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) |
| [L12:F12606](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) | 19 | Late-layer negation/superlative features driving probe (L6-L10) |  phrases related to political conspiracy/organizations, mental conditions and storytelling terms | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Output: Probe classification score (contradiction class) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:5709 de=-0.371 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F5709@9` | ❌ error | — | — | Trace the path from L4:F5709 at pos 9. This is a late-layer feature with strong … |
| SA-2 | `L6:F12420@4` | ❌ error | — | — | Trace the path from L6:F12420 at pos 4. This is a late-layer feature with strong… |
| SA-3 | `L4:F12799@2` | ❌ error | — | — | Trace the path from L4:F12799 at pos 2. This is a late-layer feature with strong… |
| SA-4 | `L2:F16097@2` | ❌ error | — | — | Trace the path from L2:F16097 at pos 2. This is an early-layer feature with stro… |
| SA-5 | `L10:F6670@19` | ❌ error | — | — | Trace the path from L10:F6670 at pos 19. This is a mid-layer feature with strong… |
| SA-6 | `L3:F12079@17` | ❌ error | — | — | Trace the path from L3:F12079 at pos 17. This is an early-layer feature with str… |
| SA-7 | `L0:F6051@14` | ❌ error | — | — | Trace the path from L0:F6051 at pos 14. This is a very early-layer feature (laye… |
| SA-8 | `L12:F12606@21` | ❌ error | — | — | Trace the path from L12:F12606 at pos 21. This is a mid-layer feature with stron… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×8 | L4:5709, L6:12420, L4:12799, L2:16097, L10:6670, L3:12079, L0:6051, L12:12606 |
| 2 | `get_upstream_features` | L4:F5709@9, k=10 → Emb:" now"@9 (de=40.25) +9 more |
| 3 | `get_upstream_features` | L6:F12420@4, k=10 → Emb:" role"@3 (de=5.59) +9 more |
| 4 | `get_upstream_features` | L4:F12799@2, k=10 → Emb:" strangest"@2 (de=31.00) +9 more |
| 5 | `get_upstream_features` | L3:F12079@17, k=10 → Emb:" There"@15 (de=15.00) +9 more |
| 6 | `get_upstream_features` | L10:F6670@19, k=10 → Emb:" not"@17 (de=6.78) +9 more |
| 7 | `get_upstream_features` | L2:F16097@2, k=10 → Emb:" strangest"@2 (de=24.00) +9 more |
| 8 | `get_upstream_features` | L12:F12606@21, k=10 → Emb:" not"@17 (de=6.56) +9 more |
| 9 | `get_upstream_features` | L0:F6051@14, k=8 → Emb:"."@14 (de=46.25) +7 more |
| 10 | `inspect_feature` ×20 | L0:5232, L0:4958, L4:4492, L4:2422, L4:4492, L3:1101, L4:14368, L1:2580, L2:10827, L1:15749, L3:8960, L3:319, L2:5606, L0:7696, L4:7409, L5:9068, L2:3705, L3:7449, L3:1438, L3:8011 |

### Build

`build_circuit` → 16 nodes, 16 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 78,143 | 6,407 | 136,333 | 0 | $0.0393 | — | — |
| **Total** | | **78,143** | **6,407** | **136,333** | **0** | **$0.0393** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 34s