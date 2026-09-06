# Circuit Oracle Report
**Date:** 2026-07-28 07:20:29 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_10 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction classification is driven by a mix of (a) genuine content signals from the premise's "role reversal" / "strangest" lexical content and (b) the bare presence of the negation word "not" in the hypothesis, plus several high-level features that are not semantically contradiction-specific. The user's concern is partially validated: negation features and a low-content "not" detector are substantial contributors, but the "reversal" / "strangest" path is content-grounded (via the "reversal" / "strangest" / "role" tokens), and not pure negation heuristics.

**Confidence:** 5/10

**Reasoning:**

The circuit reaches token-embedding nodes for "reversal" (pos 4), "role" (pos 3), "strangest" (pos 2), "not" (pos 17), "now" (pos 9), "on" (pos 21), and "democracy" (pos 12).

**Content-grounded path (premise "strangest role reversal"):** The Emb tokens "reversal" and "role" excite L4:7409 ("vice versa / inverse / reverse" detector, frac_nonzero≈0.0096) at pos 4 (direct_effect=+3.70) and L0:6013 ("the word 'role'", frac_nonzero≈0.029) at pos 3 (direct_effect=+0.22). These feed L8:16033 ("figurative language about reversals of fortune", frac_nonzero≈0.02) at pos 4 (direct_effect=+0.22), which promotes the probe. L4:12799 (the "-ly/odd/strangest" feature, frac_nonzero≈0.0083) at pos 2 contributes +0.30 to the probe, with promoted tokens including "Weird/weird/strangely/oddly/strange" — this is genuinely picking up on "strangest" as a content word. This path is real lexical/semantic content, not spurious.

**Negation path (user's concern — partially confirmed):** Emb "not" at pos 17 strongly excites L3:12079 ("negations", frac_nonzero≈0.0098, direct_effect=+0.23), L4:4492 ("negations in various languages", frac_nonzero≈0.038, +0.30 net), and L2:12021 ("not or negative terms", frac_nonzero≈0.0057, +0.20 net). Together these contribute about +0.5 to the probe from a single "not" token. However, this is mitigated by *inhibitory* negation features at the same position: L4:2422 ("French/Malay/Croatian negations", frac_nonzero≈0.016, -0.22 net) and L3:1101 ("absence/negation in software contexts", frac_nonzero≈0.009, -0.23 net) push the other way. The net of the L4:4492 vs L4:2422 contrast (the "negations in various languages" detectors pair at the same layer) plus the L2:12021 exciter gives a non-trivial net positive from "not". Crucially, "not" is the only negation in the prompt and sits in the hypothesis, so this *is* a content feature (negation in the hypothesis) — but the fact that it's a bare token-embedding-driven negation detector firing on a single word, not on a contextual understanding of contradiction, is exactly the "spurious negation signal" the user worried about.

**Generic / off-target path (further spuriousness):** L12:12606 (political conspiracy / mental conditions / storytelling, frac_nonzero≈0.016, +0.21) fires at pos 21, fed by the bare "on" token and "not" + bos — the autointerp has nothing to do with contradiction. L10:6670 ("technical / scientific terms", frac_nonzero≈0.07 — the broadest feature in the top list, +0.28) fires at pos 19. These are generic decoders with no contradiction-specific semantics and they latch onto whichever content tokens happen to be nearby. L4:6072 ("now followed by a verb", +0.25 at pos 9) is similar — a generic grammatical pattern.

**Net assessment:** The user's hypothesis is **partially correct**. The circuit does rely on the bare "not" token via three separate negation-detector features (L3:12079, L4:4492, L2:12021) as a primary driver, which is the kind of spurious "negation word → contradiction" shortcut they suspected. However, it is *not* purely negation-based: there is a legitimate content path through "reversal" → L4:7409 → L8:16033 and "strangest" → L4:12799, plus several genuinely generic features (L12:12606, L10:6670) that fire on irrelevant tokens and would not survive a counterfactual ablation. The probe appears to be a weak classifier whose score is partially explained by content ("reversal", "strangest") and partially by a "hypothesis contains 'not'" shortcut.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L8:F16033](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16033) | 4 | Late-layer reversal/oddity detectors (L8, L7) |  figurative language related to reversals of fortune | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16033) |
| [L7:F905](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/905) | 4 | Late-layer reversal/oddity detectors (L8, L7) |  words indicating amounts, changes, or trends | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/905) |
| [L7:F11459](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/11459) | 4 | Late-layer reversal/oddity detectors (L8, L7) |  sentences where someone is metaphorically putting themselves in another person's position or when referencing roles | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/11459) |
| [L4:F7409](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7409) | 4 | Mid-layer 'reversal'/'vice versa' feature (L4) |  words like "vice versa", "inverse", "reverse", "around", or directions | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7409) |
| [L3:F12079](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) | 17 | Negation detectors at hypothesis 'not' (L3, L4, L2) | negations and Chinese names | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 17 | Negation detectors at hypothesis 'not' (L3, L4, L2) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L2:F12021](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) | 17 | Negation detectors at hypothesis 'not' (L3, L4, L2) | "not" or negative terms, with some bonus for sports-related terms and "purpose". | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 17 | Inhibitory negation features at 'not' (L4, L3) | negations in other languages like French, Malay, and Croatian | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L3:F1101](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) | 17 | Inhibitory negation features at 'not' (L4, L3) |  error messages and terms indicating absence or negation in software contexts. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) |
| [L4:F12799](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12799) | 2 | '-ly/odd' detector (positive) and superlative (inhibitory) at 'strangest' |  words ending in "-ly" along with phrases that contain the word 'odd' or 'oddities' | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12799) |
| [L2:F16097](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) | 2 | '-ly/odd' detector (positive) and superlative (inhibitory) at 'strangest' | superlative adjectives and the words "test" or "point" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) |
| [L12:F12606](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) | 21 | Late-layer generic detectors (L12 political/ADD; L10 technical) |  phrases related to political conspiracy/organizations, mental conditions and storytelling terms | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) |
| [L10:F6670](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) | 19 | Late-layer generic detectors (L12 political/ADD; L10 technical) | technical terms, especially within scientific or medical contexts | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) |
| [L0:F6013](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6013) | 3 | L0 'role' word detector (positive driver) | the word "role," sometimes in conjunction with words that make it abstract, like energy or medicine | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6013) |
| [L4:F6072](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6072) | 9 | L4 'now followed by verb' feature (positive) |  the word "now" followed by a verb | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6072) |
| [L4:F14368](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14368) | 4 | Inhibitory mid-layer features (L4 role-importance, L6 break-guidelines) |  words related to importance or roles in a system | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14368) |
| [L6:F12420](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12420) | 4 | Inhibitory mid-layer features (L4 role-importance, L6 break-guidelines) |  artistic elements that break established guidelines | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12420) |
| [L7:F4526](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4526) | 4 | Inhibitory mid-layer features (L4 role-importance, L6 break-guidelines) |  words related to comparisons, symmetry or reversals in data or situations | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4526) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:5709 de=-0.371 |
| 3 | `inspect_feature` ×15 | L4:5709, L6:12420, L4:12799, L2:16097, L10:6670, L4:6072, L3:12079, L7:905, L4:14368, L0:6013, L8:16033, L7:4526, L12:12606, L2:10705, L0:6051 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L8:F16033@4` | ❌ error | — | — | Trace the upstream path from L8:F16033 ("figurative language related to reversal… |
| SA-2 | `L10:F6670@19` | ❌ error | — | — | Trace the upstream path from L10:F6670 ("technical terms, especially within scie… |
| SA-3 | `L12:F12606@21` | ❌ error | — | — | Trace the upstream path from L12:F12606 (political conspiracy / mental condition… |
| SA-4 | `L3:F12079@17` | ❌ error | — | — | Trace the upstream path from L3:F12079 ("negations and Chinese names") firing at… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L8:F16033@4, k=15 → Emb:" reversal"@4 (de=13.00) +14 more |
| 2 | `get_upstream_features` | L10:F6670@19, k=15 → Emb:" not"@17 (de=6.78) +14 more |
| 3 | `get_upstream_features` | L3:F12079@17, k=15 → Emb:" There"@15 (de=15.00) +14 more |
| 4 | `get_upstream_features` | L12:F12606@21, k=15 → Emb:" not"@17 (de=6.56) +14 more |
| 5 | `inspect_feature` ×6 | L4:4492, L0:4958, L4:2422, L3:1101, L2:12021, L4:7409 |
| 6 | `get_upstream_features` | L4:F6072@9, k=10 → Emb:" now"@9 (de=49.75) +9 more |
| 7 | `get_upstream_features` | L7:F905@4, k=10 → Emb:" reversal"@4 (de=6.88) +9 more |
| 8 | `get_upstream_features` | L4:F14368@4, k=10 → Emb:" role"@3 (de=12.31) +9 more |
| 9 | `get_upstream_features` | L8:F16033@4, k=10 → Emb:" reversal"@4 (de=13.00) +9 more |
| 10 | `get_upstream_features` | L12:F12606@21, k=5 → Emb:" not"@17 (de=6.56) +4 more |
| 11 | `inspect_feature` ×3 | L7:11459, L6:2743, L0:5232 |

### Build

`build_circuit` → 14 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 52,640 | 6,300 | 267,096 | 0 | $0.0394 | — | — |
| **Total** | | **52,640** | **6,300** | **267,096** | **0** | **$0.0394** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 37s