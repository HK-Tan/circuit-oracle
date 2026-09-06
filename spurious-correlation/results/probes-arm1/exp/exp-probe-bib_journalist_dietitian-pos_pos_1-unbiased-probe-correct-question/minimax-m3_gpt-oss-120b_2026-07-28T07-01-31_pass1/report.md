# Circuit Oracle Report
**Date:** 2026-07-28 07:01:31 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** This probe's "dietitian" classification is driven overwhelmingly by genuine profession-domain lexical features (nutrition, dietary, health, eating, clients) anchored on the "Academy of Nutrition and Dietetics" token and nutrition verbs; the user's concern about gender-marker confounds is not supported — the circuit contains no features encoding "She/her" or gendered pronouns.

**Confidence:** 8

**Reasoning:**

The terminal node (L26, probe output) is fed by a circuit dominated by **profession-domain features**, not gender markers. The strongest single path runs through **L19:F1589** ("a context of scientific, specially nutritional studies", frac_nonzero=0.038, direct_effect up to 0.109 at multiple positions including pos 20 "Nutrition", pos 22 "Die[tetics]", and pos 23 "tetics"). Tracing this upstream confirms it is excited by **Emb:Nutrition (pos 20, direct_effect 34.25)** and **Emb:Die (pos 22, direct_effect 13.25)** — the actual words of "Academy of **Nutrition** and **Die**tetics" — via mid-layer **L4:F13412** (dietary-health terms, direct_effect 10.4). This is a clean lexical-onto-semantic pathway from the profession's own name.

Supporting profession-domain features all encode topic vocabulary, not demographics:
- **L6:F11327** (food/nutrition words, +0.119) — driven by Emb:eat (pos 9, direct_effect 22.1) and Emb:clients (pos 5)
- **L14:F4197** (food-related context, +0.122) — driven by Emb:eat (pos 9, direct_effect 17.9)
- **L4:F13412** (dietary terms, +0.124) — multi-position, "dietitian"/"diet"
- **L4:F12213** (health research, +0.094), **L6:F8984** (health words, +0.066), **L15:F8177** (eating words, +0.064)
- **L6:F6115** (commercial/clients, +0.128) — promoted tokens are "clients, customer, clientele"; this encodes a **client-facing professional relationship**, a structural property of dietitians (educating clients), not gender

Critically, I verified what activates at the gendered positions. **Emb:"She" (pos 1)** has only a small negative direct_effect (-0.86) on **L0:F6051** (a generic periods/spaces suppressor) and a +1.13 positive effect on L4:F13412. **Emb:"her" (pos 4)** contributes +0.93 to L6:F6115. There is **no "she/her pronoun" feature** anywhere in the top-20 direct-effect ranking; no feature has a label, top activating example, or promoted token indicating gender/feminine encoding. The two features that *might* look like confound candidates are L1:F15251 ("client" word detector, which is actually suppressing the output at the "clients" position) and L0:F6051 (periods/spaces — a generic punctuation suppressor) — both are lexical, not demographic.

The user's hypothesis of gender-marker spuriousness is **not supported**: the circuit's top features at the probe node are all topic-domain (nutrition, diet, health, eating, clients) and trace cleanly to the profession-defining words "Nutrition", "Dietetics", "eat healthier", "clients". Gender tokens "She" and "her" contribute only weakly and are not encoded by any dedicated feature.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 35 | Probe output (dietitian classification direction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 23 | Nutritional-studies context (L19:F1589) |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 22 | Nutritional-studies context (L19:F1589) |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 20 | Nutritional-studies context (L19:F1589) |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 35 | Nutritional-studies context (L19:F1589) |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 9 | Food/nutrition words (L14:F4197) |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 9 | Food/nutrition words (L6:F11327) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F6115](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6115) | 5 | Commercial activity / clients (L6:F6115) |  words related to commercial activity and customers | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6115) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 23 | Dietary-health terms (L4:F13412) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 9 | Dietary-health terms (L4:F13412) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 10 | Dietary-health terms (L4:F13412) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 22 | Dietary-health terms (L4:F13412) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F12213](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12213) | 10 | Health research (L4:F12213) | strings of letters followed by "ls" and "an", plus words associated with health research | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12213) |
| [L15:F8177](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/8177) | 9 | Eating-words (L15:F8177) | words associated with eating | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/8177) |
| [L6:F8984](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8984) | 10 | Health words (L6:F8984) |  words and phrases related to health | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8984) |
| [L0:F9888](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9888) | 3 | Formal-schooling words (L0:F9888) |  words related to formal schooling | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9888) |
| [L0:F5697](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5697) | 5 | Early-layer misc (L0:5697 'accompanied'; L0:8444 'to') | the word "accompanied" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5697) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 8 | Early-layer misc (L0:5697 'accompanied'; L0:8444 'to') | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 11 | Suppressor: periods/spaces (L0:F6051) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L1:F15251](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15251) | 5 | Suppressor: 'client' word (L1:F15251) |  the word "client" and its plural form more often than not when capitalized as the first word of a sentence or preceded by a special character | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15251) |
| [L5:F3400](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3400) | 3 | Suppressor: verbs of spending time (L5:F3400) |  verbs, adjectives, or nouns related to the act of spending time or enjoying experiences with others | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3400) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:6115 de=0.128 |
| 3 | `inspect_feature` ×14 | L6:6115, L4:13412, L14:4197, L6:11327, L19:1589, L0:6051, L4:12213, L1:15251, L0:9888, L0:5697, L0:8444, L5:3400, L6:8984, L15:8177 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F1589@23` | ✅ reported | 4 | 5 | Trace the upstream path from L19:F1589 (nutritional studies context feature, at … |
| SA-2 | `L6:F6115@5` | ❌ error | — | — | Trace L6:F6115 ("clients" feature) upstream. This fires on "clients" — does it c… |
| SA-3 | `L1:F15251@5` | ✅ reported | 5 | 1 | Trace L1:F15251 ("client" feature, suppressing) upstream. This is a NEGATIVE dir… |
| SA-4 | `L0:F6051@11` | ❌ error | — | — | Trace L0:F6051 (periods/spaces feature) upstream — this is the highest negative … |

<details>
<summary><b>SA-1</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F1589 | " a context of scientific, specially nutritional, studies" |
| 2 | `get_upstream_features` | L19:F1589@23, k=10 | L4:F13412 (de=10.38) +9 more |
| 3 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 4 | `inspect_feature` | L17, F7545 | "mentions of architecture, design, nurses and healthcare." |
| 5 | `get_upstream_features` | L4:F13412@23, k=10 | L3:F11774 (de=4.72) +9 more |
| 6 | `inspect_feature` | L3, F11774 | " what appears to be a smattering of strings related to scientific nota" |
| 7 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |

**Findings:** The profession‑core feature L19:F1589 (nutrition‑studies context) receives its strongest positive drive from a mid‑level diet‑terms feature at layer 4 (F13412). That feature itself is strongly excited by the raw input token embeddings for "Nutrition" (pos 20) and the fragment "Die" (pos 22) – both parts of the phrase "Academy of Nutrition and Dietetics" and the word "dietitian". Additional positiv…

</details>

<details>
<summary><b>SA-3</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F15251 | " the word "client" and its plural form more often than not when capita" |
| 2 | `get_upstream_features` | L1:F15251@5, k=10 | Emb:" clients"@5 (de=27.62) +9 more |
| 3 | `inspect_feature` | L0, F11663 | " the word "despite"" |
| 4 | `inspect_feature` | L0, F11835 | "terms used in software code such as "assembly", "using", "namespace", " |
| 5 | `inspect_feature` | L0, F2189 | " technical writing related to scientific studies" |
| 6 | `inspect_feature` | L0, F5165 | " words and phrases related to a person's thoughts, life experiences, o" |
| 7 | `get_upstream_features` | L0:F11663@5, k=10 | Emb:" clients"@5 (de=16.00) +9 more |

**Findings:** L1:F15251 is a suppressor for the token 'client'. Its strongest positive upstream driver is the raw input embedding for the token " clients" at position 5 (direct_effect 27.6), indicating the feature fires when the prompt contains the word 'clients'. Upstream transcoder features in layer 0 (F11663, F11835, F2189, F5165) have only weak or neutral influence and none show gender‑related tokens or pro…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F6115@5, k=10 → Emb:" clients"@5 (de=25.62) +9 more |
| 2 | `get_upstream_features` | L0:F6051@11, k=10 → Emb:"."@11 (de=46.50) +9 more |
| 3 | `get_upstream_features` | L4:F13412@9, k=8 → Emb:" eat"@9 (de=7.66) +7 more |
| 4 | `get_upstream_features` | L19:F1589@20, k=8 → Emb:" Nutrition"@20 (de=34.25) +7 more |
| 5 | `get_upstream_features` | L19:F1589@22, k=8 → Emb:" Nutrition"@20 (de=14.06) +7 more |
| 6 | `inspect_feature` | L3, F11774 → " what appears to be a smattering of strings related to scientific nota" |
| 7 | `get_upstream_features` | L6:F11327@9, k=6 → Emb:" eat"@9 (de=22.12) +5 more |
| 8 | `get_upstream_features` | L14:F4197@9, k=6 → Emb:" eat"@9 (de=17.88) +5 more |

### Build

`build_circuit` → 20 nodes, 24 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 38,785 | 5,343 | 163,161 | 0 | $0.0278 | — | — |
| SA-3 | openai/gpt-oss-120b | 62,890 | 4,375 | 9,472 | 0 | $0.0122 | ✅ 5F/1E | Trace L1:F15251 ("client" feature, suppressing) upstream. Th… |
| SA-1 | openai/gpt-oss-120b | 64,806 | 4,187 | 5,056 | 0 | $0.0123 | ✅ 4F/5E | Trace the upstream path from L19:F1589 (nutritional studies … |
| **Total** | | **166,481** | **13,905** | **177,689** | **0** | **$0.0523** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 40s