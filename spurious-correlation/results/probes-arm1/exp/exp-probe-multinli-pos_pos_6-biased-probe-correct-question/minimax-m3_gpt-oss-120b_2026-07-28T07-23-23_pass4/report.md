# Circuit Oracle Report
**Date:** 2026-07-28 07:23:23 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_6 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "contradiction" classification is driven almost entirely by a *negation* feature circuit converging on the single token **" not"** at position 21 (the prompt's last negation: "They were not allowed to deforest…"), with no meaningful use of the prompt's substantive content (fire/agriculture/deforestation) — confirming the user's concern about spurious negation-signal features.

**Confidence:** 9

**Reasoning:**

**Top driver (the smoking gun).** L16:F12358 at pos 21 has label *"the word 'not' followed within a few tokens by a form of the verb 'to be'"* (frac_nonzero=0.028) with direct_effect=+0.336 toward the probe direction. Its upstream root is the **Emb: " not" (pos 21)** with direct_effect=+19, then a chain of dedicated "not"-detector features: L0:F4958 *"the word 'not'"* (frac_nonzero=0.018) → L1:F5108 / L1:F14233 (both labeled "not") → L2:F12021 *"not or negative terms"* (frac_nonzero=0.006) → L3:F8011/F9803/F6227 (all promoting/noting "not", e.g. *"mix of words from different languages"* with promoted_tokens = `not, NOT, Not, ikke, nicht, geen`) → L4:F4492 *"negations in various languages"* + L4:F2422 *"negations in French, Malay, Croatian"* → L13:F3295/F14177 (L14:F13077, L15:F10071) all "negations/dissent" → L16:F12358.

**Counter-evidence direction.** L3:F1101 at pos 21 is the exact mirror — its autointerp is *"error messages and terms indicating absence or negation in software contexts"* and it has the LARGEST negative direct_effect (-0.338), i.e. it pushes the probe *away* from the contradiction class. The two features compete at the same token position on the same word "not"; the net signed signal is positive, but the entire content of the argument reduces to "presence of 'not' in the text" (with a positional bias toward sentence-final "were not allowed").

**What is NOT driving the probe.** The content-bearing features appear in the top-20 but with smaller direct_effects and they are dispersed:
- L2:F4819 (pos 12) *"sentences containing the word 'fire'"* — direct_effect +0.262
- L0:F3820 "the" (pos 6), L0:F8444 "to" (pos 13), L0:F3498 "they" (pos 2), L0:F2238 "about" (pos 4), L1:F8332 "clear/clearance" (pos 5) — all generic function-word detectors (frac_nonzero 0.007–0.030), with small positive contributions that look like generic text frequency artifacts rather than semantic content features.
- L15:F2080 *"set followed by articles/prepositions"* is a generic lexical pattern, not a content feature.

**Token-level diagnosis.** `get_upstream_features` of L16:F12358, L4:F4492, L3:F8011, L2:F12021, L0:F4958, L13:F3295, L15:F10071, L1:F14233, L1:F5108 all return **Emb: " not" (pos 21)** as the #1 upstream with direct_effect between +9.8 and +33.75. No other token embedding comes close. The "fire", "agriculture", "deforest", "forest", "setting", "clearing" tokens contribute via generic lexical detectors but not via a content-semantic circuit — they aren't the reason the probe fires.

**Circuit topology.** The signal flows: Emb(" not") → L0 "not"-detector (F4958) → L1 "not" (F5108, F14233) → L2 negation (F12021) → L3 mixed-language "not" features (F8011, F9803) → L4 multilingual negation (F4492, F2422) → L13/L15 negation+dissent (F3295, F14177, F10071) → L16 "not"+be (F12358) → probe direction. This is a feature *pyramid* all bottoming out on a single token, with a parallel "absence/error" branch (F1101) that *inhibits* the probe. No content feature about fire/agriculture/deforestation/permission enters this chain.

**Why this matters for the user's concern.** The user's worry is correct: the probe's "contradiction" classification is essentially a shallow bag-of-negation-features check keyed on the literal string " not" — exactly the kind of spurious shortcut a probe would latch onto if contradiction correlates with negation in training data. The probe is not "reading" the contradiction between the two sentences; it is reading the presence of the word *not* in the second sentence, and would presumably fire on any sentence ending in "not" (or "pas", "ikke", "nicht", etc., via L4:F2422 / L3:F8011). The content features (fire, clear, set about, agriculture) participate only as low-magnitude background noise, not as semantic evidence for or against contradiction.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: ' not' (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: ' the' (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: ' to' (pos 13) / ' fire' (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: ' to' (pos 13) / ' fire' (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: ' they' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: ' about' (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: ' set' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: ' clearing' (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'So' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 23 | Emb: ' to' (pos 23) / ' allowed' (pos 22) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 22 | Emb: ' to' (pos 23) / ' allowed' (pos 22) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 21 | L0 'not' word detector (pos 21) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F3498](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) | 2 | L0 'they' word detector (pos 2) |  the pronoun "they" or its possessive form. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 4 | L0 'about' word detector (pos 4) |  the word "about" when followed by a numerical value | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 6 | L0 'the' word detector (pos 6) | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 13 | L0 'to' word detector (pos 13) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L1:F5108](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5108) | 21 | L1 'not' word detector (pos 21) | the word "not" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5108) |
| [L1:F14233](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) | 21 | L1 'not' word detector (pos 21) |  negative sentiment markers such as "not," "no," "never," and their equivalents in other languages | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) |
| [L1:F8332](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8332) | 5 | L1 'clear/clearance' (pos 5) | the word "clear" or "clearance" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8332) |
| [L2:F12021](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) | 21 | L2 'not' / negation (pos 21) | "not" or negative terms, with some bonus for sports-related terms and "purpose". | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) |
| [L2:F4819](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4819) | 12 | L2 'fire' (pos 12) | sentences containing the word "fire" or similar terms | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4819) |
| [L2:F2952](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2952) | 4 | L2 'out' (pos 4) |  the word "out", and sometimes activates on words relating to legal cases | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2952) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 21 | L3 'not' positive (pos 21) — promotes 'not' |  a mix of words and code fragments from different languages | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L3:F9803](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9803) | 21 | L3 'not' positive (pos 21) — promotes 'not' | sentences describing scientific studies or experiments, particularly where something is disproven | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9803) |
| [L3:F6227](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) | 23 | L3 'not' positive (pos 21) — promotes 'not' |  sentence fragments and informal or ungrammatical language, often including abbreviations. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) |
| [L3:F1101](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) | 21 | L3 'not' negative/abs-error (pos 21) — pushes toward 'not' as absence |  error messages and terms indicating absence or negation in software contexts. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) |
| [L3:F13138](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13138) | 4 | L3 'not' negative/abs-error (pos 21) — pushes toward 'not' as absence |  words and phrases related to legal proceedings or documents. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13138) |
| [L3:F8733](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8733) | 4 | L3 'not' negative/abs-error (pos 21) — pushes toward 'not' as absence |  parts of words like "ch", "parms", "ened", and "ounesto" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8733) |
| [L3:F3797](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3797) | 1 | L3 'not' negative/abs-error (pos 21) — pushes toward 'not' as absence | comments starting with "So" or "Okay". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3797) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 21 | L4 'not' across languages (pos 21/4) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 21 | L4 'not' across languages (pos 21/4) | negations in other languages like French, Malay, and Croatian | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L6:F1468](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1468) | 3 | L6 'set' + article (pos 3) | variations of the word "set" followed by an article | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1468) |
| [L14:F8363](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/8363) | 3 | L14 'set' + prep (pos 3) |  the word "set" followed by prepositions | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/8363) |
| [L14:F13077](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/13077) | 21 | L14 'set' + prep (pos 3) | negations. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/13077) |
| [L15:F2080](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2080) | 3 | L15 'set' + article/prep (pos 3,11) | the phrase "set" followed by articles or prepositions | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2080) |
| [L15:F10071](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) | 21 | L15 'set' + article/prep (pos 3,11) | negations and equivocations | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) |
| [L13:F14177](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/14177) | 21 | L15 'set' + article/prep (pos 3,11) | negation or dissent, often using "not" with "am" or other verbs | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/14177) |
| [L13:F3295](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) | 21 | L15 'set' + article/prep (pos 3,11) | negations in the form of "is/are not" as well as other uses of "not" | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) |
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 21 | L16 'not' + be-verb (pos 21) |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:3498 de=-0.785 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F3498@2` | ❌ error | — | — | Trace L0:F3498 at pos 2. What does this feature detect and what feeds into it? |
| SA-2 | `L16:F12358@21` | ❌ error | — | — | Trace L16:F12358 at pos 21 - top positive driver. What does it encode and what u… |
| SA-3 | `L3:F8011@21` | ❌ error | — | — | Trace L3:F8011 at pos 21 - a positive contributor at the last position. What doe… |
| SA-4 | `L0:F2238@4` | ❌ error | — | — | Trace L0:F2238 at pos 4. What does it encode? |
| SA-5 | `L3:F1101@21` | ❌ error | — | — | Trace L3:F1101 at pos 21 - a strong negative feature. What does it detect? |
| SA-6 | `L15:F2080@3` | ❌ error | — | — | Trace L15:F2080 at pos 3 - a late-layer feature. What does it detect and where d… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×18 | L0:3498, L0:2238, L3:1101, L3:8011, L16:12358, L2:2952, L4:4492, L2:4819, L0:3820, L0:8444, L4:2422, L15:2080, L1:8332, L3:8733, L3:6227, L0:4958, L3:13138, L3:3797 |
| 2 | `get_upstream_features` | L16:F12358@21, k=10 → Emb:" not"@21 (de=19.00) +9 more |
| 3 | `get_upstream_features` | L4:F4492@21, k=10 → Emb:" not"@21 (de=19.12) +9 more |
| 4 | `get_upstream_features` | L3:F8011@21, k=10 → Emb:" not"@21 (de=21.75) +9 more |
| 5 | `get_upstream_features` | L3:F1101@21, k=10 → Emb:" not"@21 (de=13.69) +9 more |
| 6 | `get_upstream_features` | L15:F2080@3, k=10 → Emb:" set"@3 (de=44.50) +9 more |
| 7 | `get_upstream_features` | L4:F2422@21, k=10 → Emb:" not"@21 (de=17.50) +9 more |
| 8 | `get_upstream_features` | L2:F2952@4, k=8 → Emb:" set"@3 (de=13.50) +7 more |
| 9 | `get_upstream_features` | L2:F4819@12, k=8 → Emb:" fire"@12 (de=32.00) +7 more |
| 10 | `get_upstream_features` | L0:F3498@2, k=8 → Emb:" they"@2 (de=42.75) +7 more |
| 11 | `get_upstream_features` | L0:F2238@4, k=8 → Emb:" about"@4 (de=35.00) +7 more |
| 12 | `get_upstream_features` | L15:F10071@21, k=8 → Emb:" not"@21 (de=9.81) +7 more |
| 13 | `get_upstream_features` | L13:F3295@21, k=8 → Emb:" not"@21 (de=17.25) +7 more |
| 14 | `get_upstream_features` | L3:F9803@21, k=8 → Emb:" not"@21 (de=13.94) +7 more |
| 15 | `get_upstream_features` | L2:F12021@21, k=8 → Emb:" not"@21 (de=23.12) +7 more |
| 16 | `get_upstream_features` | L1:F8332@5, k=8 → Emb:" clearing"@5 (de=21.12) +7 more |
| 17 | `get_upstream_features` | L3:F6227@23, k=8 → Emb:" to"@23 (de=6.75) +7 more |
| 18 | `get_upstream_features` | L3:F3797@1, k=8 → Emb:"So"@1 (de=22.00) +7 more |
| 19 | `inspect_feature` ×3 | L15:10071, L2:12021, L3:9803 |
| 20 | `get_upstream_features` | L13:F3295@21, k=8 → Emb:" not"@21 (de=17.25) +7 more |
| 21 | `get_upstream_features` | L0:F8444@13, k=8 → Emb:" to"@13 (de=41.00) +7 more |
| 22 | `get_upstream_features` | L0:F3820@6, k=8 → Emb:" the"@6 (de=34.25) +7 more |
| 23 | `get_upstream_features` | L0:F4958@21, k=8 → Emb:" not"@21 (de=33.75) +7 more |
| 24 | `get_upstream_features` | L3:F6227@23, k=8 → Emb:" to"@23 (de=6.75) +7 more |
| 25 | `get_upstream_features` | L3:F8733@4, k=8 → Emb:" set"@3 (de=7.12) +7 more |
| 26 | `get_upstream_features` | L3:F13138@4, k=8 → Emb:" set"@3 (de=10.12) +7 more |
| 27 | `inspect_feature` ×6 | L13:3295, L0:9646, L1:5108, L1:14233, L14:13077, L13:14177 |
| 28 | `get_upstream_features` | L6:F1468@3, k=6 → Emb:" set"@3 (de=24.50) +5 more |
| 29 | `get_upstream_features` | L14:F8363@3, k=6 → Emb:" set"@3 (de=15.44) +5 more |
| 30 | `inspect_feature` ×2 | L6:1468, L14:8363 |

### Build

`build_circuit` → 27 nodes, 31 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 63,996 | 8,451 | 304,472 | 0 | $0.0476 | — | — |
| **Total** | | **63,996** | **8,451** | **304,472** | **0** | **$0.0476** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 18s