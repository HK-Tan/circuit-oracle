# Circuit Oracle Report
**Date:** 2026-07-28 07:02:53 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe is driven primarily by topic-relevant content (food, dieting, active, lifestyle, health) with a noticeable side-channel contribution from a female-pronoun feature (she/her), and a "mission/passion" content feature. The gender-marker node pushes the probe in the *opposite* direction of the main content path (negative direct_effect), so it is acting as a tone-down suppressor rather than as the primary classifier.

**Confidence:** 7

**Reasoning:** The strongest positive direct effects come from L6:F11327 (food/nutrition; direct_effect 0.093, promoted "foods/eating/FOOD"), L4:F3047 (exercise/physical activity; promoted "workout/exercise/gym"), and L4:F13412 (diet/health; promoted "diet/diets/dieting"). These are all genuine profession-relevant concepts. The downstream L14:F4197 (food-related) also feeds in positively, tracing back to the " food" token embedding at pos 15 (direct_effect 22.6). Low-layer content detectors L0:F10218 ("lifestyle", direct_effect 0.055), L0:F4030 ("mission statement / personal-development career language", 0.078), and L0:F2238 ("about", 0.053) also push positively — these are content signals, not gender markers.

The pronoun feature (L0:F9519, "she/her", frac_nonzero 0.011) has direct_effect −0.065 — it actively *suppresses* the probe score rather than promoting it. L0:F2349 ("others", −0.123) and L0:F11646 (pos 1, −0.065) are also negative. The user's hypothesis (that the circuit uses spurious gender markers) is **not** supported: the she-feature is an off-target, inhibitory side-channel, and the dominant positive path is anchored in topic words (food, dieting, active, lifestyle, healthy, passionate). The "lifestyle + food philosophy + physical activity" cluster is the genuine profession indicator; gender pronouns are slightly pulling against the classification.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: food (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 41 | Emb: food (pos 41) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: healthy (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 34 | Emb: dieting (pos 34) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 22 | Emb: active (pos 22) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: physically (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: lifestyle (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: passionate (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: others (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: She (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 1 | Gender pronoun feature (she/her) |  the pronoun "she" and the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L0:F11646](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11646) | 1 | Gender pronoun feature (she/her) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11646) |
| [L0:F2349](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) | 6 | Gender pronoun feature (she/her) |  the word "others" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) |
| [L0:F10218](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10218) | 17 | Content-word detectors (lifestyle, mission/passionate, pick) |  the word "lifestyle." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10218) |
| [L0:F4030](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4030) | 3 | Content-word detectors (lifestyle, mission/passionate, pick) |  words related to mission statements and personal development used in career environments | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4030) |
| [L0:F8566](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) | 9 | Content-word detectors (lifestyle, mission/passionate, pick) |  the word "pick" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 4 | Content-word detectors (lifestyle, mission/passionate, pick) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L0:F2845](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2845) | 9 | Content-word detectors (lifestyle, mission/passionate, pick) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2845) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 12 | Content-word detectors (lifestyle, mission/passionate, pick) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 34 | Health/diet/physical-activity concepts | terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F3047](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3047) | 22 | Health/diet/physical-activity concepts | words or phrases related to exercise and physical activity | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3047) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 15 | Food/nutrition concept (multi-pos) | words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 41 | Food/nutrition concept (multi-pos) | words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 15 | Food-related concept (late layer) |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Output logit (probe direction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2349 de=-0.123 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11327@15` | ✅ reported | 4 | 3 | Trace from L6:F11327. This feature is at pos 15 which is 'knowledge' or similar.… |
| SA-2 | `L4:F3047@22` | ✅ reported | 5 | 7 | Trace from L4:F3047. This feature is at pos 22 with high direct effect. Investig… |
| SA-3 | `L14:F4197@15` | ❌ error | — | — | Trace from L14:F4197 at pos 15. This is a later-layer feature. Determine its sem… |
| SA-4 | `L0:F4030@3` | ❌ error | — | — | Trace from L0:F4030 at pos 3. Pos 3 is 'is' or 'passionate' token in the prompt.… |
| SA-5 | `L0:F10218@17` | ❌ error | — | — | Trace from L0:F10218 at pos 17. Pos 17 is near 'make' or 'healthy' tokens. Inves… |

<details>
<summary><b>SA-1</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 2 | `get_upstream_features` | L6:F11327@15, k=10 | Emb:" food"@15 (de=34.00) +9 more |
| 3 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 4 | `get_upstream_features` | L4:F13412@15, k=10 | Emb:" healthy"@14 (de=7.53) +9 more |
| 5 | `inspect_feature` | L1, F11764 | " words and phrases related to health and fitness" |
| 6 | `get_upstream_features` | L1:F11764@15, k=10 | Emb:" healthy"@14 (de=5.97) +9 more |

**Findings:** The target feature L6:F11327 (food‑nutrition) receives its strongest excitatory input directly from the raw embedding of the token " food" (direct_effect 34.0) and also from the adjacent " healthy" token. Upstream, its activation is largely driven by a diet‑health feature in layer 4 (L4:F13412), which in turn is powered by a health‑fitness feature in layer 1 (L1:F11764). That health‑fitness featur…

</details>

<details>
<summary><b>SA-2</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F3047 | " words or phrases related to exercise and physical activity" |
| 2 | `get_upstream_features` | L4:F3047@22, k=10 | Emb:" active"@22 (de=10.25) +9 more |
| 3 | `inspect_feature` | L2, F13919 | "words related to life goals and purpose" |
| 4 | `inspect_feature` | L0, F3597 | "the word "active" optionally preceded by an adverb of degree" |
| 5 | `get_upstream_features` | L2:F13919@22, k=10 | Emb:" active"@22 (de=4.56) +9 more |
| 6 | `inspect_feature` | L1, F3066 | " discussion of physical exercise and sports" |
| 7 | `get_upstream_features` | L0:F3597@22, k=10 | Emb:" active"@22 (de=18.12) +9 more |
| 8 | `inspect_feature` | L1, F9918 | " words related to research studies of physical activity" |
| 9 | `get_upstream_features` | L1:F9918@22, k=10 | Emb:" active"@22 (de=5.28) +9 more |

**Findings:** The circuit originates at L4:F3047, a mid‑layer feature that detects exercise‑related language and strongly promotes workout‑type tokens. Its largest positive upstream drivers are direct token embeddings: the word 'active' (direct effect 10.25) and the adverb 'physically' (8.44). These embedding shortcuts already satisfy the lower‑third layer requirement (layer ≤ 8) and provide a concrete token‑le…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×3 | L0:2349, L0:9519, L0:8566 |
| 2 | `get_upstream_features` | L14:F4197@15, k=10 → Emb:" food"@15 (de=22.62) +9 more |
| 3 | `get_upstream_features` | L0:F4030@3, k=10 → Emb:" passionate"@3 (de=6.31) +9 more |
| 4 | `get_upstream_features` | L0:F10218@17, k=10 → Emb:" lifestyle"@17 (de=25.00) +9 more |
| 5 | `get_upstream_features` | L4:F13412@34, k=10 → Emb:" dieting"@34 (de=18.25) +9 more |
| 6 | `inspect_feature` ×4 | L14:4197, L0:4030, L0:10218, L0:11814 |
| 7 | `get_upstream_features` | L4:F3047@22, k=10 → Emb:" active"@22 (de=10.25) +9 more |
| 8 | `get_upstream_features` | L6:F11327@15, k=10 → Emb:" food"@15 (de=34.00) +9 more |
| 9 | `get_upstream_features` | L4:F3047@34, k=10 → ❌ Feature (layer=4, feature_idx=3047) not found at pos=34. Thi |
| 10 | `inspect_feature` ×3 | L0:9519, L0:4030, L0:10218 |
| 11 | `get_upstream_features` | L0:F9519@1, k=5 → Emb:"She"@1 (de=15.75) +4 more |
| 12 | `get_upstream_features` | L6:F11327@41, k=5 → Emb:" food"@41 (de=41.25) +4 more |

### Build

`build_circuit` → 16 nodes, 16 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 30,872 | 4,378 | 96,937 | 0 | $0.0203 | — | — |
| SA-1 | openai/gpt-oss-120b | 55,956 | 5,207 | 10,240 | 0 | $0.0117 | ✅ 4F/3E | Trace from L6:F11327. This feature is at pos 15 which is 'kn… |
| SA-2 | openai/gpt-oss-120b | 108,150 | 8,173 | 5,056 | 0 | $0.0212 | ✅ 5F/7E | Trace from L4:F3047. This feature is at pos 22 with high dir… |
| **Total** | | **194,978** | **17,758** | **112,233** | **0** | **$0.0532** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 1s