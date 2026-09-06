# Circuit Oracle Report
**Date:** 2026-07-28 07:23:47 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** This probe classifies toxicity primarily through lexical identity-token detectors (particularly the word "white" at pos 4 and pronoun "he" at pos 2), not through semantic understanding of the conditional framing ("If...it would be a problem") that actually conveys the toxic sentiment.

**Confidence:** 7

**Reasoning:**

The attribution graph reveals a strikingly shallow circuit — the top features driving the probe score all live in layers 0-4, with no deep semantic composition. The single highest-contributing feature is **L0:F12768 at pos 2** (direct_effect=0.2051), whose upstream trace returns only the raw embedding of " he" (direct_effect=37). This is a pure lexical detector for the pronoun "he" — it fires whenever that token appears, regardless of context.

The second-strongest driver is **L0:F3436 at pos 4** (direct_effect=0.1719), which traces directly to the **" white"** token embedding (direct_effect=18). A cluster of additional "white"-position features follows: L0:F10910 (0.1035), L0:F13663 (-0.166, inhibitory), and L0:F6548. Together these form a "Lexical 'white' detectors" supernode. The **L4:F15204** feature (direct_effect=0.1177) is the highest-layer feature in the circuit, but its upstream trace shows it is **directly driven by the " white" embedding** (direct_effect=40.5) — it does not compose any higher-level meaning; it is just a deeper-layer re-encoding of the same lexical signal.

Critically, the word **"Hispanic" at pos 7** does NOT appear anywhere in the top upstream features. The probe ignores the actual identity being discussed (Hispanic) and the conditional structure ("If...would be"), firing instead on the **counterfactual identity word "white"** and the **pronoun "he"**. Features for "was" (L0:F2458) and "it" (L0:F880) contribute generically — the "it" feature traces to the generic pronoun embedding, not to any anaphoric resolution of the conditional clause.

The **mid_was_if** supernode (L2:F1139 at pos 3) does fire on the "If...was" construction (upstream: "If" emb 27.6, "was" emb 21.4), so there is *some* detection of the counterfactual framing, but it is a shallow structural pattern, not a semantic-toxicity detector.

**Confirmation of the user's concern:** The circuit demonstrates exactly the spurious pattern described. The probe's classification is driven by surface-level identity-token detectors (the lexical presence of "white" and the pronoun "he") rather than by features encoding the actual toxic content — which is the *counterfactual framing* (implying a problem would exist *but for* the person's identity). A model that truly understood the toxicity would route through features encoding negation+conditional+stereotyped-group, not through standalone identity-word detectors. The absence of any L10+ feature in the top drivers (the deepest is L4) confirms the probe is exploiting a bag-of-identity-words shortcut.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: he (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: white (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: was (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: it (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: If (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 2 | Lexical "he" detector (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L0:F310](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/310) | 2 | Lexical "he" detector (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/310) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 4 | Lexical "white" detectors (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F10910](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) | 4 | Lexical "white" detectors (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) |
| [L0:F13663](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13663) | 4 | Lexical "white" detectors (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13663) |
| [L0:F6548](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6548) | 4 | Lexical "white" detectors (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6548) |
| [L0:F2458](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2458) | 3 | Lexical "was" detector (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2458) |
| [L0:F880](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/880) | 8 | Lexical "it" detector (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/880) |
| [L2:F6983](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6983) | 4 | Mid-layer "white" features (L2-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6983) |
| [L2:F585](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) | 4 | Mid-layer "white" features (L2-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) |
| [L3:F11768](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11768) | 4 | Mid-layer "white" features (L2-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11768) |
| [L4:F15204](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) | 4 | Mid-layer "white" features (L2-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) |
| [L2:F1139](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1139) | 3 | Mid-layer "was/If" features (L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1139) |
| [L2:F11539](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11539) | 1 | Mid-layer "was/If" features (L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11539) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe logit | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token '1' is not one of the top-k next-token candidates capt |
| 3 | `get_top_features` | 10 features; top: L0:12768 de=0.205 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F12768@2` | ❌ error | — | — | Trace upstream from L0:F12768 at pos 2. Determine what token/pattern this featur… |
| SA-2 | `L0:F3436@4` | ❌ error | — | — | Trace upstream from L0:F3436 at pos 4. The input prompt is "<bos>If he was white… |
| SA-3 | `L0:F880@8` | ❌ error | — | — | Trace upstream from L0:F880 at pos 8. The input prompt is "<bos>If he was white … |
| SA-4 | `L4:F15204@4` | ❌ error | — | — | Trace upstream from L4:F15204 at pos 4. The input prompt is "<bos>If he was whit… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F12768@2, k=10 → Emb:" he"@2 (de=37.00) +9 more |
| 2 | `get_upstream_features` | L0:F3436@4, k=10 → Emb:" white"@4 (de=18.00) +9 more |
| 3 | `get_upstream_features` | L4:F15204@4, k=10 → Emb:" white"@4 (de=40.50) +9 more |
| 4 | `get_upstream_features` | L0:F880@8, k=10 → Emb:" it"@8 (de=42.50) +9 more |
| 5 | `get_upstream_features` | L2:F1139@3, k=5 → Emb:"If"@1 (de=27.62) +4 more |
| 6 | `get_upstream_features` | L0:F10910@4, k=5 → Emb:" white"@4 (de=14.56) +4 more |
| 7 | `get_upstream_features` | L0:F2458@3, k=5 → Emb:" was"@3 (de=36.75) +4 more |

### Build

`build_circuit` → 12 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 8,310 | 4,142 | 35,464 | 0 | $0.0096 | — | — |
| **Total** | | **8,310** | **4,142** | **35,464** | **0** | **$0.0096** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 49s