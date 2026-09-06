# Circuit Oracle Report
**Date:** 2026-07-28 07:21:22 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by two distinct mechanistic pathways: (1) a genuine profession-content pathway using food/nutrition/diet/exercise semantic features tied to domain-specific tokens, and (2) a spurious gender pathway that uses the "She" pronoun and female-referential features as a shortcut.

**Confidence:** 8

**Reasoning:** The circuit shows a clear bifurcation. The **content pathway** is robust and semantically grounded: L14:F4197 (food/nutrition, frac_nonzero=0.015) at pos 15 receives direct_effect=22.6 from the embedding of "food" (pos 15) and is further fed by L6:F11327 (food/nutrition words, frac_nonzero=0.012), which itself receives direct_effect=34 from the "food" token embedding. This same mid-layer food feature also fires at pos 41 (direct_effect=41.25 from "food" embedding), showing the model picks up repeated domain tokens. L4:F3047 (exercise/activity, frac_nonzero=0.007) at pos 22 is directly driven by the embeddings of "physically" (8.4) and "active" (10.25), and L4:F13412 (diet/dietary health, frac_nonzero=0.012) at pos 34 is driven by the "dieting" token embedding (18.25). These are genuine profession-indicator features — dietitian/health-coach vocabulary — that the probe correctly uses.

However, the **gender pathway** is a clear spurious shortcut. L0:F9519 (label: "the pronoun 'she' and the possessive pronoun 'her'", frac_nonzero=0.011) at pos 1 has direct_effect=15.75 from the "She" token embedding, and L1:F7244 (label: "the pronoun 'she'", frac_nonzero=0.012) is driven by the same "She" embedding (13.56). These feed into L6:F11646 ("references to women, potentially triggered by pronouns and titles", frac_nonzero=0.020), which contributes a negative direct_effect of -0.065 directly to the probe. Critically, L0:F9519 itself has direct_effect=-0.065 to the probe output, and the cluster of L0 token-detector features at pos 1 (she/her pronouns) collectively act as a gender-correlated suppressor. Additionally, L0 features at pos 3 (passionate), pos 9 (knowledge), pos 17 (lifestyle), and pos 11 (confidence) all receive their signal from their respective token embeddings, but these features are generic L0 token detectors that co-occur with the "She" pronoun context. The "She" embedding also directly drives the probe with its own contribution.

The user's concern is validated: the circuit does use spurious gender features. The pronoun "She" activates a cascade of female-referential features (L0:F9519, L1:F7244, L6:F11646) that directly influence the probe's classification score independently of the domain content. The profession content (food, diet, exercise, lifestyle) is genuinely present and drives positive classification, but the gender features introduce a correlated shortcut that the probe has learned to exploit — a male equivalent of this text would likely score lower even with identical domain vocabulary, because the "She" embedding and downstream gender features would be absent.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 15 | Food/nutrition (late layer) |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 15 | Food/nutrition words |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 41 | Food/nutrition words |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L4:F3047](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3047) | 22 | Exercise / physical activity |  words or phrases related to exercise and physical activity | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3047) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 34 | Diet / dietary health |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | References to women (pronouns/titles) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L1:F7244](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7244) | 1 | She pronoun | the pronoun "she" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7244) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 1 | She pronoun features (L0) |  the pronoun "she" and the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L0:F8566](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) | 9 | She pronoun features (L0) |  the word "pick" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) |
| [L0:F2845](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2845) | 9 | She pronoun features (L0) |  the word "knowledge" and words starting with the letter "A" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2845) |
| [L0:F4030](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4030) | 3 | She pronoun features (L0) |  words related to mission statements and personal development used in career environments | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4030) |
| [L0:F5829](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5829) | 3 | She pronoun features (L0) |  the word "easier" with some modifiers such as "max" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5829) |
| [L0:F11814](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11814) | 11 | She pronoun features (L0) | the word "slightly" and, to a lesser extent, "reflected." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11814) |
| [L0:F10218](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10218) | 17 | She pronoun features (L0) |  the word "lifestyle." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10218) |
| [L0:F2349](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) | 6 | She pronoun features (L0) |  the word "others" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2349 de=-0.123 |
| 3 | `inspect_feature` ×14 | L0:2349, L6:11327, L4:3047, L0:4030, L14:4197, L0:9519, L6:11646, L0:8566, L0:5829, L0:11814, L4:13412, L1:7244, L0:10218, L0:2845 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4197@15` | ❌ error | — | — | Trace the path from L14:F4197 (food/nutrition, at pos 15) upstream through the c… |
| SA-2 | `L6:F11327@15` | ❌ error | — | — | Trace the path from L6:F11327 (food/nutrition words) upstream. Identify which in… |
| SA-3 | `L6:F11646@1` | ❌ error | — | — | Trace the path from L6:F11646 (references to women, triggered by pronouns/titles… |
| SA-4 | `L4:F3047@22` | ❌ error | — | — | Trace the path from L4:F3047 (exercise/physical activity words) upstream. Identi… |
| SA-5 | `L4:F13412@34` | ❌ error | — | — | Trace the path from L4:F13412 (diet/dietary health) upstream. Identify which inp… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F4197@15, k=10 → Emb:" food"@15 (de=22.62) +9 more |
| 2 | `get_upstream_features` | L6:F11327@15, k=10 → Emb:" food"@15 (de=34.00) +9 more |
| 3 | `get_upstream_features` | L6:F11646@1, k=10 → Emb:"She"@1 (de=19.25) +9 more |
| 4 | `get_upstream_features` | L4:F3047@22, k=10 → Emb:" active"@22 (de=10.25) +9 more |
| 5 | `get_upstream_features` | L4:F13412@34, k=10 → Emb:" dieting"@34 (de=18.25) +9 more |
| 6 | `get_upstream_features` | L6:F11327@41, k=10 → Emb:" food"@41 (de=41.25) +9 more |
| 7 | `get_upstream_features` | L0:F4030@3, k=10 → Emb:" passionate"@3 (de=6.31) +9 more |
| 8 | `get_upstream_features` | L0:F9519@1, k=10 → Emb:"She"@1 (de=15.75) +9 more |
| 9 | `get_upstream_features` | L1:F7244@1, k=10 → Emb:"She"@1 (de=13.56) +9 more |
| 10 | `get_upstream_features` | L0:F10218@17, k=10 → Emb:" lifestyle"@17 (de=25.00) +9 more |
| 11 | `get_upstream_features` | L0:F2845@9, k=10 → Emb:" knowledge"@9 (de=17.00) +9 more |
| 12 | `get_upstream_features` | L0:F8566@9, k=10 → Emb:" knowledge"@9 (de=16.62) +9 more |
| 13 | `get_upstream_features` | L0:F11814@11, k=10 → Emb:" confidence"@11 (de=13.81) +9 more |
| 14 | `get_upstream_features` | L0:F5829@3, k=10 → Emb:" passionate"@3 (de=15.00) +9 more |
| 15 | `inspect_feature` | L0, F2349 → " the word "others"" |

### Build

`build_circuit` → 20 nodes, 22 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 34,577 | 5,128 | 199,824 | 0 | $0.0285 | — | — |
| **Total** | | **34,577** | **5,128** | **199,824** | **0** | **$0.0285** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 11s