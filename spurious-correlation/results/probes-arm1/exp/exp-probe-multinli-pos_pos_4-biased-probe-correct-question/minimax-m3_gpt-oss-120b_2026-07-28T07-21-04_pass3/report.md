# Circuit Oracle Report
**Date:** 2026-07-28 07:21:04 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "contradiction" classification is primarily driven by a chain of low-frac_nonzero negation features (L2:F8837 "No one/Nobody", L14:F336 "no/negative", L15:F13061 "no + one", L16:F11298 "No") that all fire on the "No one" tokens at positions 16–17, with weaker but real content-side contributions from tour/map/here features; the user's concern is **partially correct but overstated** — negation is the dominant signal, not the only one.

**Confidence:** 7

**Reasoning:** The top of the graph (features directly driving the probe direction) is dominated by **late-layer negation detectors** that all fire on the "No one" tokens at pos 16–17:
- **L16:F11298** (frac_nonzero 0.01043) — "No" / negation, direct_effect *not in top-20 here* (it is in the upstream chain). The strongest direct driver is the **L2:L1 negation feature chain**, not the late-layer one.
- **L14:F336** (frac_nonzero 0.0044) — "the word 'no' and related negative words," pos 16, direct_effect = +0.183.
- **L2:F8837** (frac_nonzero 0.01085) — "the word 'one' or 'body' when preceded by 'no' or 'every'," pos 17, direct_effect = −0.207 (negative; but it is in the upstream chain of L14:F336 via the L0/F1143 "No" and L1/F15800 "one" features). It also appears in the top-20 list with negative sign.

Tracing **upstream**, the negation chain is anchored almost entirely at the **embedding nodes** for the tokens " No" (pos 16) and " one" (pos 17):
- L14:F336 ← Emb:" No" (pos 16) with direct_effect = 33.0, plus Emb:" one" features at deeper layers
- L16:F11298 ← Emb:" No" (pos 16) direct_effect = 12.4, ← L14:F336 direct_effect = 6.94
- L2:F8837 ← Emb:" No" (pos 16) direct_effect = 18.6, ← Emb:" one" (pos 17) direct_effect = 9.25, ← L0:F4438 (pos 17) direct_effect = 9.13
- L1:F15800 (pos 17, "one") ← Emb:" one" direct_effect = 15.25

So the **negation word "No" alone (no context) is the single largest feed** to L14:F336 (33.0) and a top-3 feed into L16:F11298 (12.4) and L2:F8837 (18.6). This is exactly the kind of **spurious surface cue** the user worries about: a single negation word, decoupled from its semantic role (here "No one is usually at the tourist office" is a *setup* for a constructive suggestion, not a contradiction marker), supplies the bulk of the positive signal toward the probe.

However, the picture is **not purely spurious**. Several content-side features also contribute directly to the probe (with positive or negative direct_effect):
- L2:F3116 — "pick up" phrasal verb (pos 2), direct_effect = −0.609 (strong **negative** push — pushes *away* from the contradiction probe). This anchors at Emb:"Pick" (50.0) and Emb:" up" (20.75).
- L2:F14413 — "tour"/"tours" (pos 14), direct_effect = −0.281 (negative).
- L2:F1016 — "tour" verb/noun (pos 14), direct_effect = +0.217 (positive).
- L4:F11969 — "printed advertising materials" — but actually driven by Emb:" map" (5.94) and Emb:"Pick" (2.08) (and L2:F3116 feeds it), direct_effect = +0.180. This is the "map" → "brochure" misactivation.
- L8:F1872 — "diagrams/presentations" (pos 4, "map"), direct_effect = +0.178. Driven primarily by Emb:" map" (13.6).
- L4:F10722 — "here" with demonstratives (pos 9), direct_effect = −0.213 (negative).

Net: **the negation chain at positions 16–17 ("No one") is the single dominant feature family**, with Emb:" No" (pos 16) being by far the strongest single embedding node (direct_effects of 12–33 into the negation features). The L2 "tour" / L8 "map+chart" features provide weaker, mixed-sign content signal. The user's concern is **well-founded**: the probe is using "No" as a surface heuristic, but **the circuit is not exclusively negation-driven** — it also has content features ("map", "tour", "here", "pick up") that partially oppose or supplement the negation push. A purely contradiction-bearing example with content overlap to the hypothesis (e.g., "tourist office has maps AND walking tours") would likely be classified correctly; the spuriousness arises because "No one" *overrides* the otherwise partly cancelling content signal at positions 1–14.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 17 | Contradiction probe direction | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L16:F11298](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11298) | 16 | L16:F11298 — negation word "no"/"No" (pos 16) | no | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11298) |
| [L14:F336](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) | 16 | L14:F336 — negation word "no" / negative statements (pos 16) | the word "no" and related negative words | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) |
| [L15:F13061](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13061) | 16 | L15:F13061 — "no" + "one" / negative statements (pos 16) |  uses of the word "no" or similar negative statements and words associated with "one" | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13061) |
| [L2:F8837](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8837) | 17 | L2:F8837 — "No one" / "Nobody" (pos 17) |  the word "one" or "body" when preceded by the words "no" or "every." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8837) |
| [L1:F15800](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15800) | 17 | L1:F15800 — word "one" (pos 17) |  the word "one" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15800) |
| [L2:F3116](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) | 2 | L2:F3116 — "pick up" phrasal verb (pos 2) |  the phrasal verb "pick up" and variations | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) |
| [L2:F14413](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) | 14 | L2:F14413 — word "tour"/"tours" (pos 14) | the word "tour" or "tours" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) |
| [L2:F1016](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1016) | 14 | L2:F1016 — "tour" verb/noun (pos 14) |  forms of the verb "tour" and the noun "tour." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1016) |
| [L4:F11969](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11969) | 4 | L4:F11969 — "pick" (pos 1) feeding printed-materials circuit (pos 4) |  mentions of printed advertising materials | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11969) |
| [L8:F1872](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/1872) | 4 | L8:F1872 — diagrams/presentations/charts context (pos 4) |  words and phrases related to diagrams and presentations | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/1872) |
| [L4:F10722](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10722) | 9 | L4:F10722 — word "here" with demonstratives (pos 9) | uses of the word "here" alongside demonstrative pronouns and temporal words | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10722) |
| [L1:F6872](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6872) | 14 | L1:F6872 — word "interpretation" (pos 14) |  the word "interpretation" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6872) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 16 | Emb: " No" (pos 16) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: " one" (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: " tours" (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: "Pick" (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: " up" (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: " here" (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: " map" (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L2:3116 de=-0.609 |
| 3 | `inspect_feature` ×20 | L2:3116, L0:10562, L0:10904, L2:14413, L1:15800, L2:1016, L0:2238, L4:10722, L0:8566, L2:8837, L2:11769, L0:13092, L0:6051, L0:7727, L14:336, L1:6872, L4:11969, L8:1872, L16:11298, L0:13354 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F11298@16` | ❌ error | — | — | Trace the path from L16:F11298 ("No" / negation) — what features upstream drive … |
| SA-2 | `L14:F336@16` | ❌ error | — | — | Trace the path from L14:F336 ("no" / negation words) at pos 16 — what features u… |
| SA-3 | `L2:F8837@17` | ❌ error | — | — | Trace the path from L2:F8837 ("No one"/"Nobody" — negation+noun) at pos 17 — wha… |
| SA-4 | `L2:F14413@14` | ❌ error | — | — | Trace the path from L2:F14413 ("tour"/"tours") at pos 14 — does this feed a cont… |
| SA-5 | `L2:F1016@14` | ❌ error | — | — | Trace the path from L2:F1016 ("tour" verb/noun) at pos 14 — what input tokens dr… |
| SA-6 | `L2:F3116@2` | ❌ error | — | — | Trace the path from L2:F3116 ("pick up" phrasal verb) at pos 2 — what input toke… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L16:F11298@16, k=10 → Emb:" No"@16 (de=12.44) +9 more |
| 2 | `get_upstream_features` | L14:F336@16, k=10 → Emb:" No"@16 (de=33.00) +9 more |
| 3 | `get_upstream_features` | L2:F8837@17, k=10 → Emb:" No"@16 (de=18.62) +9 more |
| 4 | `get_upstream_features` | L2:F14413@14, k=10 → Emb:" tours"@14 (de=28.38) +9 more |
| 5 | `get_upstream_features` | L2:F1016@14, k=10 → Emb:" tours"@14 (de=27.75) +9 more |
| 6 | `get_upstream_features` | L2:F3116@2, k=10 → Emb:"Pick"@1 (de=50.00) +9 more |
| 7 | `get_upstream_features` | L4:F10722@9, k=10 → Emb:" here"@9 (de=24.12) +9 more |
| 8 | `get_upstream_features` | L4:F11969@4, k=10 → Emb:" map"@4 (de=5.94) +9 more |
| 9 | `get_upstream_features` | L8:F1872@4, k=8 → Emb:" map"@4 (de=13.62) +7 more |
| 10 | `get_upstream_features` | L15:F13061@16, k=8 → Emb:" No"@16 (de=12.50) +7 more |
| 11 | `get_upstream_features` | L0:F1143@16, k=8 → Emb:" No"@16 (de=26.88) +7 more |
| 12 | `get_upstream_features` | L13:F10768@16, k=8 → Emb:" No"@16 (de=11.88) +7 more |
| 13 | `get_upstream_features` | L12:F8719@16, k=8 → Emb:" No"@16 (de=15.38) +7 more |
| 14 | `get_upstream_features` | L0:F4438@17, k=8 → Emb:" No"@16 (de=29.38) +7 more |
| 15 | `get_upstream_features` | L15:F13061@16, k=5 → Emb:" No"@16 (de=12.50) +4 more |
| 16 | `get_upstream_features` | L15:F15582@16, k=5 → Emb:" No"@16 (de=6.97) +4 more |
| 17 | `inspect_feature` | L15, F13061 → " uses of the word "no" or similar negative statements and words associ" |
| 18 | `get_upstream_features` | L14:F336@16, k=5 → Emb:" No"@16 (de=33.00) +4 more |
| 19 | `get_upstream_features` | L1:F15800@17, k=5 → Emb:" one"@17 (de=15.25) +4 more |

### Build

`build_circuit` → 20 nodes, 22 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 72,946 | 6,627 | 223,090 | 0 | $0.0432 | — | — |
| **Total** | | **72,946** | **6,627** | **223,090** | **0** | **$0.0432** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 42s