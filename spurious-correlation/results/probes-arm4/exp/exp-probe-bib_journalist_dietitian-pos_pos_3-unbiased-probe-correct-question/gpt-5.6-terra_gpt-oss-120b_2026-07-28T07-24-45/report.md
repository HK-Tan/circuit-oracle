# Circuit Oracle Report
**Date:** 2026-07-28 07:24:45 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe’s profession score is driven chiefly by genuine nutrition/wellness content—food, healthy eating, diet philosophy, and physical activity—plus a weaker generic “personal mission” writing-style cue, rather than by the female pronoun.

**Confidence:** 8/10

**Reasoning:** The built circuit shows several direct lexical-semantic routes from the input into the profession-probe direction:

- **Food/nutrition route:** `Emb: food (pos 15)` and `Emb: healthy (pos 14)` feed the **Healthy-food and diet detectors** supernode. The central feature is L6:F11327 at positions 15 and 41, a selective food/nutrition detector (`frac_nonzero=0.01166`) whose promoted tokens are *food, foods, eating, meals*. It has strong positive direct effect on the probe at pos 15 (+0.0933) and again later in the passage at pos 41 (+0.0532). Its immediate upstream attribution is dominated by the literal `food` embedding (+34), with `healthy` also positive (+4.34).

- **Diet-specific evidence:** L4:F13412 is a dietary-health detector (`frac_nonzero=0.01216`; promoted tokens include *diet, diets, dieting*). It receives positive input from `healthy` (+7.53) and `food` (+4.0), and contributes to the food pathway. This reflects the text’s explicit “healthy food,” “dieting,” “restricting food,” and food-philosophy discussion—strongly profession-relevant evidence for a nutrition/dietetic or wellness-oriented class.

- **Physical-activity route:** `Emb: physically (pos 21)` and `Emb: active (pos 22)` feed the **Explicit physical-activity detector** supernode. L4:F3047 is selective for exercise/physical activity (`frac_nonzero=0.00666`) and promotes *workout, exercise, gym, fitness*. It directly increases the probe score by +0.0825. Its largest upstream inputs are the embeddings `active` (+10.25) and `physically` (+8.44). This is direct semantic evidence from “be physically active,” not a demographic proxy. L0:F3597 additionally detects *active* specifically.

- **Late food integrator:** L14:F4197 (+0.0693) is labelled food insecurity but, based on both its promoted vocabulary (*food, foods*) and this input’s attribution, functions here as a broad late food-focused integrator rather than a literal deprivation detector. It is driven directly by `food` (+22.63), by the L6 food detector (+9.19), and positively by the diet-related pathway. Thus it carries the repeated food-domain signal forward into the probe.

- **Generic stylistic/career-language route:** L0:F4030 (+0.0776) is a mission-statement/personal-development feature (`frac_nonzero=0.02399`) driven principally by `passionate` (+6.31). It plausibly captures the bio-like framing—“passionate about empowering others,” “knowledge and confidence”—rather than a profession title. This is weaker evidence of a potentially spurious *genre/style* shortcut: such motivational professional bios may be correlated with the target profession but do not establish it alone.

On the user’s gender-marker concern: the embedding for **“She” (pos 1)** appears only as a small upstream contribution to the generic mission feature (+0.71), far below `passionate` (+6.31), `food` (+34 into L6:F11327), `active` (+10.25 into L4:F3047), and `physically` (+8.44). No high-effect inspected feature was a gender or female-pronoun detector. Therefore, this graph does **not** support gender as the principal causal mechanism for the probe’s score. The primary mechanism is an interpretable aggregation of nutrition, diet, and activity indicators, with a modest possible confound from motivational biography style.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F4030](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4030) | 3 | Career/personal-development mission-statement cue |  words related to mission statements and personal development used in career environments | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4030) |
| [L0:F3597](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3597) | 22 | Explicit physical-activity detector | the word "active" optionally preceded by an adverb of degree | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3597) |
| [L2:F13919](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13919) | 22 | Explicit physical-activity detector | words related to life goals and purpose | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13919) |
| [L4:F3047](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3047) | 22 | Explicit physical-activity detector |  words or phrases related to exercise and physical activity | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3047) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 15 | Healthy-food and diet detectors |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 15 | Healthy-food and diet detectors |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 41 | Healthy-food and diet detectors |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 15 | Late food-focused integrator |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2349 de=-0.123 |
| 3 | `inspect_feature` ×5 | L6:11327, L4:3047, L14:4197, L0:4030, L0:11814 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4197@15` | ❌ error | — | — | Trace this strong positive probe-driving feature upstream to embeddings. Determi… |
| SA-2 | `L6:F11327@15` | ❌ error | — | — | Trace the recurrent strong positive feature upstream to embeddings, identifying … |
| SA-3 | `L4:F3047@22` | ❌ error | — | — | Trace this positive probe feature upstream to embedding tokens; establish semant… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F4197@15, k=15 → Emb:" food"@15 (de=22.62) +14 more |
| 2 | `get_upstream_features` | L6:F11327@15, k=15 → Emb:" food"@15 (de=34.00) +14 more |
| 3 | `get_upstream_features` | L4:F3047@22, k=15 → Emb:" active"@22 (de=10.25) +14 more |
| 4 | `get_upstream_features` | L0:F4030@3, k=15 → Emb:" passionate"@3 (de=6.31) +14 more |
| 5 | `inspect_feature` ×3 | L4:13412, L2:13919, L0:3597 |
| 6 | `get_upstream_features` | L4:F13412@15, k=10 → Emb:" healthy"@14 (de=7.53) +9 more |
| 7 | `get_upstream_features` | L2:F13919@22, k=10 → Emb:" active"@22 (de=4.56) +9 more |

### Build

`build_circuit` → 10 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 17,282 | 2,109 | 61,694 | 0 | $0.0903 | — | — |
| **Total** | | **17,282** | **2,109** | **61,694** | **0** | **$0.0903** | | |

**Oracle wall-clock time:** 0m 31s