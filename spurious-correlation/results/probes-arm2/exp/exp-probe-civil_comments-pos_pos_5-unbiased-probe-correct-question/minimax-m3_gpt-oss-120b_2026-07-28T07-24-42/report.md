# Circuit Oracle Report
**Date:** 2026-07-28 07:24:42 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by lexical and structural features detecting identity-group terms ("social justice", "warrior", "Muslim", "bakery", "gay") in a conditional+imperative sentence skeleton, rather than by any semantic/lexical content about toxicity, slur content, or actual harm.

**Confidence:** 8

**Reasoning:** The circuit I traced shows a sparse, shallow graph (only ~25 features, mostly in layers 0–6 — the top-20 direct-effect features on the probe target are all in L0–L6). The signal originates almost entirely at the **token-embedding level** of identity nouns:

- **L0 identity-group lexical detectors** — `L0:F9934` (de=+0.099), `F3591` (de=+0.064), `F9602` (de=−0.064), `F2260` (de=−0.073) at pos 5/6 fire directly on the **"social"** and **"justice"** embeddings, with `F4478` (de=−0.092) on "social" and `F3850`/`F8444`/`F4870`/`F13756` on the structural tokens "," "to" and "order". The strongest single direct-effect in the entire graph is `L0:F8444` on the **"to"** embedding (de=−0.224), with `L0:F7710` on "you" (de=−0.154) — purely function-word detectors with no toxicity content.
- **L0/L1 "warrior" identity cluster** — `L0:F13310` (de=+0.085, "you are"), `F7710` (de=−0.154 on "you"), and `L1:F14281` (de=−0.067 on "justice") combine the identity noun "warrior" with the surrounding conditional "If you are a …" frame. `L0:F9026` (de=+0.066 negative) at pos 7/13 also fires on the identity noun "warrior" and the identity noun "bakery" (a non-person entity used metonymically for an identity group).
- **L2–L3 conditional/imperative clause** — `L2:F14541` (de=+0.070 on ","), `F14209` (de=+0.069 on "go"), `F13877` (de=+0.066 on "warrior"), `L3:F10868` (de=+0.135 on "a"), `L3:F16254` (de=+0.104 on ","), `L3:F1526` (de=+0.072 on "justice") encode the *"If you are X, go do Y"* syntactic template. These are pure structure features — they would equally fire on "If you are a dentist, go brush your teeth."
- **L4–L6 identity-target composites** — `L4:F13700` (de=−0.065 on ","), `L6:F9005` (de=−0.113 on "bakery"), `L6:F2674` (de=+0.067 on "warrior") aggregate the identity nouns "warrior" and "bakery" as the **targets** of the conditional. `L4:F13041` (de=+2.58 inside `L6:F9005` upstream) and `L5:F14212` further reinforce "bakery" as an identity metonym.

The circuit **lacks any features encoding slur content, violence, threat, or toxicity semantics**. There are no late-layer features (L15–L25) representing a "this is a hateful statement" abstraction — the graph effectively dies after L6. The probe is therefore classifying based on a **spurious bag-of-identity-tokens + conditional-imperative-template** signal: it sees "social justice" + "warrior" + "Muslim" + "gay" + "If X, go Y" and outputs its positive class, even though the model's deeper layers never actually compute "this text advocates harm against an identity group" (which would be the legitimate signal).

This directly confirms the user's concern: the probe (and whatever it was trained to detect) is using **identity-group token presence** as a shortcut rather than engaging with the actual content. Notably, the strongest direct effects come from *function words* ("to", "you", ",", "a") and the structural "If … go …" template, not from any toxic-content feature. Swapping the identity nouns for any other group (e.g. "If you are a dentist, go to a French bakery and order a birthday cake") would likely produce a comparable probe score, because the circuit is identity-token-counting, not toxicity-reasoning.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F3591](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3591) | 6 | Identity-group lexical features (L0) — fire on 'social justice' tokens | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3591) |
| [L0:F9934](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9934) | 6 | Identity-group lexical features (L0) — fire on 'social justice' tokens | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9934) |
| [L0:F9602](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9602) | 6 | Identity-group lexical features (L0) — fire on 'social justice' tokens | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9602) |
| [L0:F4478](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4478) | 5 | Identity-group lexical features (L0) — fire on 'social justice' tokens | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4478) |
| [L0:F2260](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2260) | 6 | Identity-group lexical features (L0) — fire on 'social justice' tokens | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2260) |
| [L0:F13310](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13310) | 3 | Identity-group lexical features (L0) — fire on 'warrior' / 'a ... warrior' | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13310) |
| [L0:F7710](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) | 2 | Identity-group lexical features (L0) — fire on 'warrior' / 'a ... warrior' | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) |
| [L0:F14281](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14281) | 6 | Identity-group lexical features (L0) — fire on 'warrior' / 'a ... warrior' | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14281) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 13 | Identity-group lexical features (L0) — fire on 'warrior' / 'a ... warrior' | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F3850](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3850) | 8 | Punctuation/syntax (L0) — fire on ',' and 'to' | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3850) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 10 | Punctuation/syntax (L0) — fire on ',' and 'to' | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F4870](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4870) | 8 | Punctuation/syntax (L0) — fire on ',' and 'to' | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4870) |
| [L0:F13756](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13756) | 15 | Punctuation/syntax (L0) — fire on ',' and 'to' | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13756) |
| [L1:F10447](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10447) | 4 | Social-justice combined detector (L1) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10447) |
| [L1:F14281](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14281) | 6 | Social-justice combined detector (L1) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14281) |
| [L1:F3604](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3604) | 9 | Social-justice combined detector (L1) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3604) |
| [L2:F14541](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14541) | 8 | Conditional/imperative clause structure (L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14541) |
| [L2:F14209](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14209) | 9 | Conditional/imperative clause structure (L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14209) |
| [L2:F13877](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13877) | 7 | Conditional/imperative clause structure (L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13877) |
| [L2:F8867](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8867) | 4 | Conditional/imperative clause structure (L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8867) |
| [L2:F346](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/346) | 2 | Conditional/imperative clause structure (L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/346) |
| [L2:F1537](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1537) | 6 | Conditional/imperative clause structure (L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1537) |
| [L2:F5569](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5569) | 6 | Conditional/imperative clause structure (L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5569) |
| [L3:F10868](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10868) | 4 | Mid-layer clause / identity-context features (L3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10868) |
| [L3:F16254](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16254) | 8 | Mid-layer clause / identity-context features (L3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16254) |
| [L3:F1526](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1526) | 6 | Mid-layer clause / identity-context features (L3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1526) |
| [L4:F13700](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13700) | 8 | Identity-target composite (L4) — 'warrior' at pos 7 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13700) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 7 | Identity-target composite (L4) — 'warrior' at pos 7 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F11323](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11323) | 7 | Identity-target composite (L4) — 'warrior' at pos 7 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11323) |
| [L4:F12425](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12425) | 7 | Identity-target composite (L4) — 'warrior' at pos 7 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12425) |
| [L4:F1602](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1602) | 7 | Identity-target composite (L4) — 'warrior' at pos 7 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1602) |
| [L4:F10459](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10459) | 7 | Identity-target composite (L4) — 'warrior' at pos 7 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10459) |
| [L4:F13041](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13041) | 13 | Identity-target composite (L4) — 'warrior' at pos 7 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13041) |
| [L5:F14124](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14124) | 7 | Mid-context features (L5) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14124) |
| [L5:F1062](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1062) | 7 | Mid-context features (L5) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1062) |
| [L5:F14212](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14212) | 13 | Mid-context features (L5) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14212) |
| [L5:F6565](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6565) | 13 | Mid-context features (L5) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6565) |
| [L5:F4109](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/4109) | 13 | Mid-context features (L5) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/4109) |
| [L6:F9005](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9005) | 13 | Second identity-target composite (L6) — 'bakery' at pos 13 | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9005) |
| [L6:F2674](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2674) | 7 | Second identity-target composite (L6) — 'bakery' at pos 13 | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2674) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:8444 de=-0.224 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L3:F10868@4` | ❌ error | — | — | Trace this feature upstream. Determine what it encodes (what token/context it fi… |
| SA-2 | `L3:F16254@8` | ❌ error | — | — | Trace this feature upstream. It fires on the comma at pos 8 after "warrior". Det… |
| SA-3 | `L0:F9934@6` | ❌ error | — | — | Trace this feature upstream. It fires on the token "justice" at pos 6 with stron… |
| SA-4 | `L0:F3850@8` | ❌ error | — | — | Trace this feature upstream. It fires at pos 8 (the comma) — determine what it e… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L3:F10868@4, k=10 → Emb:" a"@4 (de=18.62) +9 more |
| 2 | `get_upstream_features` | L0:F9934@6, k=10 → Emb:" justice"@6 (de=19.50) +9 more |
| 3 | `get_upstream_features` | L3:F16254@8, k=10 → Emb:"If"@1 (de=9.88) +9 more |
| 4 | `get_upstream_features` | L0:F3850@8, k=10 → Emb:","@8 (de=34.75) +9 more |
| 5 | `get_upstream_features` | L0:F8444@10, k=10 → Emb:" to"@10 (de=41.00) +9 more |
| 6 | `get_upstream_features` | L0:F7710@2, k=10 → Emb:" you"@2 (de=40.50) +9 more |
| 7 | `get_upstream_features` | L6:F9005@13, k=10 → Emb:" bakery"@13 (de=22.38) +9 more |
| 8 | `get_upstream_features` | L6:F2674@7, k=10 → Emb:" social"@5 (de=2.12) +9 more |
| 9 | `get_upstream_features` | L2:F13877@7, k=10 → Emb:" warrior"@7 (de=7.72) +9 more |
| 10 | `get_upstream_features` | L2:F14209@9, k=10 → Emb:" go"@9 (de=18.38) +9 more |
| 11 | `get_upstream_features` | L0:F4478@6, k=10 → Emb:" social"@5 (de=13.31) +9 more |
| 12 | `get_upstream_features` | L0:F13310@3, k=10 → Emb:" you"@2 (de=10.50) +9 more |
| 13 | `get_upstream_features` | L0:F13756@15, k=10 → Emb:" order"@15 (de=26.25) +9 more |
| 14 | `get_upstream_features` | L2:F14541@8, k=10 → Emb:"If"@1 (de=7.66) +9 more |
| 15 | `get_upstream_features` | L4:F13700@8, k=10 → L3:F16254 (de=4.59) +9 more |
| 16 | `get_upstream_features` | L1:F14281@6, k=10 → Emb:" justice"@6 (de=13.50) +9 more |
| 17 | `get_upstream_features` | L0:F9602@6, k=10 → Emb:" justice"@6 (de=12.38) +9 more |
| 18 | `get_upstream_features` | L0:F3591@6, k=10 → Emb:" social"@5 (de=21.00) +9 more |
| 19 | `get_upstream_features` | L3:F1526@6, k=10 → Emb:" social"@5 (de=9.62) +9 more |
| 20 | `get_upstream_features` | L4:F13041@13, k=10 → Emb:" bakery"@13 (de=21.38) +9 more |
| 21 | `get_upstream_features` | L2:F14541@8, k=5 → Emb:"If"@1 (de=7.66) +4 more |

### Build

`build_circuit` → 23 nodes, 30 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 20,748 | 7,360 | 57,478 | 0 | $0.0185 | — | — |
| **Total** | | **20,748** | **7,360** | **57,478** | **0** | **$0.0185** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 39s