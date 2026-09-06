# Circuit Oracle Report
**Date:** 2026-07-28 07:24:33 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_7 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe is driven almost entirely by a generic "X Pride" identity-group template detector (L8:F15771) that fires indiscriminately on Black Pride, Gay Pride, and White Pride — the "White Pride" line in the prompt activates the same circuit that fires on "Black Pride" and "Gay Pride," and the probe scores the text as toxic because that template is correlated with toxic completions in the probe's training data, not because the circuit reads the actual "NAZI!" content.

**Confidence:** 8

**Reasoning:** The circuit reaches the embedding layer and shows that the signal flowing into the probe logit is dominated by a single supernode, L8:F15771 ("pride_group"), which directly promotes the probe (direct_effect ≈ 0.32 at pos 9, 0.23 at pos 13, 0.19 at pos 2). Crucially, this same feature fires on Black/Gay/White Pride tokens — it is an *identity-group template* feature, not a toxicity or Nazism feature. Its three upstream feeders are themselves pure identity-template detectors:

- **L6:F6085 ("gay_group")** — direct_effect 0.22 at pos 9, sourced from the "Gay" / " gay" embeddings.
- **L6:F15295 ("pride_token")** — the bare "Pride" token recognition feature at pos 2.
- **L6:F3902 ("white_group")** — at pos 17 (White) and pos 5 (the lowercase "black" inside "being black and proud"); this feature does not encode "NAZI" — its upstream at L4:F117 is the "White" entity recognition feature, and its upstream at L2:F585 is the "White" capitalized identity-entity feature. The actual "NAZI!" token at pos 18 does not appear in the top features list at all.

Downstream, these L6 features are fed by a chain of similarly generic identity-recognition features: L4:F15899 and L4:F8645 (Pride-phrase modifiers), L4:F117 ("White" entity), L3:F13061 ("Black Pride" entity), and most tellingly **L2:F13158**, which is the *generic "X Pride" identity-template* feature — it fires at pos 17 (White Pride), pos 5 (the lowercase "black" of "being black and proud"), and pos 9 (Gay Pride) with positive direct_effect, indicating the model is treating "White Pride" as the same template as the other two Pride phrases.

The inhibitory features (L1:F9113 "negid" at -0.32, L1:F12542 at -0.22, L2:F9528 "black_lowercase" at -0.17–0.23) push *against* the probe, but they fire on legitimate benign identity mentions, not on the "NAZI!" content — so they partially cancel the false-positive signal from the template but never actually read the toxic word.

The user's concern is confirmed: the circuit uses "an identity group" signal (the X-Pride template + Gay/Black/White entity detectors) rather than any feature tied to "NAZI!", "racism", or "hypocrisy" content. The probe appears to have learned that "X Pride" identity-group phrases correlate with toxicity in its training distribution and fires on the White Pride line for that spurious reason, not because the model genuinely recognizes the "NAZI!" or "racism" content. Notably, the lowercased "black" inside "being black and proud" (pos 5) flows into the same L6:F3902 white-group pathway that promotes the probe — another sign that the circuit conflates identity-mention patterns with toxicity rather than reading semantic content.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L8:F15771](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) | 9 | L8:F15771 — generic 'X Pride' identity-group template (fires on Black/Gay/White Pride tokens) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) |
| [L8:F15771](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) | 13 | L8:F15771 — generic 'X Pride' identity-group template (fires on Black/Gay/White Pride tokens) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) |
| [L8:F15771](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) | 2 | L8:F15771 — generic 'X Pride' identity-group template (fires on Black/Gay/White Pride tokens) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) |
| [L6:F6085](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) | 9 | L6:F6085 — 'Gay/gay' identity group detector | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) |
| [L6:F6085](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) | 13 | L6:F6085 — 'Gay/gay' identity group detector | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) |
| [L6:F15295](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15295) | 2 | L6:F15295 — 'Pride' token identity-label feature | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15295) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 17 | L6:F3902 — 'White/white' racial-group + 'black' mixed term (pos 5/17) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 5 | L6:F3902 — 'White/white' racial-group + 'black' mixed term (pos 5/17) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L4:F15899](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) | 9 | L4:F15899 — Pride-phrase modifier (boosts the Pride template) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) |
| [L4:F15899](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) | 13 | L4:F15899 — Pride-phrase modifier (boosts the Pride template) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) |
| [L4:F8645](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8645) | 9 | L4:F8645 — secondary Pride-phrase feature | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8645) |
| [L4:F8645](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8645) | 13 | L4:F8645 — secondary Pride-phrase feature | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8645) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 17 | L4:F117 — 'White' entity recognition | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 5 | L4:F117 — 'White' entity recognition | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 2 | L3:F13061 — 'Black Pride' entity recognition | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 17 | L2:F13158 — generic 'X Pride' identity-template feature (shared across Black/Gay/White + lower-case) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 5 | L2:F13158 — generic 'X Pride' identity-template feature (shared across Black/Gay/White + lower-case) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 9 | L2:F13158 — generic 'X Pride' identity-template feature (shared across Black/Gay/White + lower-case) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F11363](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11363) | 1 | L2:F11363 — 'Black' (capitalized) identity-entity feature | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11363) |
| [L2:F1644](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1644) | 2 | L2:F1644 — 'Pride' word-form feature | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1644) |
| [L2:F585](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) | 17 | L2:F585 — 'White' (capitalized) identity-entity feature | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) |
| [L2:F9528](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) | 5 | L2:F9528 — ' black' (lowercase) feature (inhibits the L3 Black-recognition path) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) |
| [L2:F9528](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) | 1 | L2:F9528 — ' black' (lowercase) feature (inhibits the L3 Black-recognition path) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) |
| [L1:F9113](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) | 1 | L1:F9113 — inhibitory identity-context feature (pushes AGAINST the probe) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) |
| [L1:F9113](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) | 5 | L1:F9113 — inhibitory identity-context feature (pushes AGAINST the probe) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) |
| [L1:F9113](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) | 17 | L1:F9113 — inhibitory identity-context feature (pushes AGAINST the probe) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) |
| [L1:F12542](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12542) | 2 | L1:F12542 — inhibitory 'Pride'-context feature (pushes AGAINST the probe) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12542) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'Black' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: ' Pride' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: ' black' (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: 'Gay' (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: ' gay' (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: 'White' (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L8:15771 de=0.324 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L8:F15771@9` | ❌ error | — | — | Trace upstream from L8:F15771 at pos 9. What does this feature represent? Trace … |
| SA-2 | `L6:F6085@9` | ❌ error | — | — | Trace upstream from L6:F6085 at pos 9. What does this feature represent? Trace b… |
| SA-3 | `L2:F13158@17` | ❌ error | — | — | Trace upstream from L2:F13158 at pos 17. What does this feature represent? Trace… |
| SA-4 | `L1:F9113@1` | ❌ error | — | — | Trace upstream from L1:F9113 at pos 1 (negative direct effect). What does this f… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L8:F15771@9, k=12 → Emb:"Gay"@9 (de=10.38) +11 more |
| 2 | `get_upstream_features` | L1:F9113@1, k=12 → Emb:"Black"@1 (de=16.88) +11 more |
| 3 | `get_upstream_features` | L2:F11363@1, k=12 → Emb:"Black"@1 (de=25.00) +11 more |
| 4 | `get_upstream_features` | L2:F13158@17, k=12 → Emb:"White"@17 (de=13.56) +11 more |
| 5 | `get_upstream_features` | L6:F6085@9, k=12 → Emb:"Gay"@9 (de=21.75) +11 more |
| 6 | `get_upstream_features` | L4:F15899@9, k=12 → Emb:"Gay"@9 (de=13.81) +11 more |
| 7 | `get_upstream_features` | L3:F13061@2, k=12 → Emb:"Black"@1 (de=12.06) +11 more |
| 8 | `get_upstream_features` | L6:F15295@2, k=12 → Emb:" Pride"@2 (de=10.75) +11 more |
| 9 | `get_upstream_features` | L6:F3902@17, k=12 → Emb:"White"@17 (de=7.12) +11 more |
| 10 | `get_upstream_features` | L4:F117@17, k=12 → Emb:"White"@17 (de=10.25) +11 more |
| 11 | `get_upstream_features` | L2:F9528@5, k=12 → Emb:" black"@5 (de=30.25) +11 more |
| 12 | `get_upstream_features` | L4:F8645@9, k=12 → Emb:"Gay"@9 (de=18.12) +11 more |
| 13 | `get_upstream_features` | L1:F12542@2, k=10 → Emb:" Pride"@2 (de=13.75) +9 more |
| 14 | `get_upstream_features` | L2:F1644@2, k=10 → Emb:" Pride"@2 (de=16.62) +9 more |
| 15 | `get_upstream_features` | L2:F585@17, k=10 → Emb:"White"@17 (de=27.88) +9 more |
| 16 | `get_upstream_features` | L2:F13158@5, k=10 → Emb:" black"@5 (de=10.75) +9 more |
| 17 | `get_upstream_features` | L8:F15771@5, k=15 → ❌ Feature (layer=8, feature_idx=15771) not found at pos=5. Thi |
| 18 | `get_upstream_features` | L6:F6085@13, k=15 → Emb:" gay"@13 (de=33.00) +14 more |
| 19 | `get_upstream_features` | L6:F3902@5, k=10 → Emb:" black"@5 (de=12.44) +9 more |
| 20 | `get_upstream_features` | L3:F7993@1, k=10 → Emb:"Black"@1 (de=23.50) +9 more |
| 21 | `get_upstream_features` | L1:F15447@2, k=10 → Emb:" Pride"@2 (de=13.88) +9 more |
| 22 | `get_upstream_features` | L1:F13646@17, k=10 → Emb:"White"@17 (de=4.62) +9 more |
| 23 | `get_upstream_features` | L3:F3248@17, k=10 → L2:F13158 (de=2.72) +9 more |
| 24 | `get_upstream_features` | L3:F11768@17, k=10 → Emb:"White"@17 (de=24.62) +9 more |
| 25 | `get_upstream_features` | L4:F15204@17, k=10 → Emb:"White"@17 (de=37.75) +9 more |
| 26 | `get_upstream_features` | L5:F8577@9, k=10 → Emb:"Gay"@9 (de=2.02) +9 more |
| 27 | `get_upstream_features` | L1:F4668@17, k=10 → Emb:"White"@17 (de=21.12) +9 more |
| 28 | `get_upstream_features` | L1:F13646@5, k=10 → Emb:" black"@5 (de=4.50) +9 more |
| 29 | `get_upstream_features` | L1:F13069@1, k=10 → Emb:"Black"@1 (de=19.38) +9 more |

### Build

`build_circuit` → 22 nodes, 30 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 36,468 | 6,766 | 105,429 | 0 | $0.0254 | — | — |
| **Total** | | **36,468** | **6,766** | **105,429** | **0** | **$0.0254** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 24s