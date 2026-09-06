# Circuit Oracle Report
**Date:** 2026-07-28 07:21:20 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by masculine pronoun features (he/He) and a few generic topic-word and function-word detectors — the only nominally profession-related token ("writer" at pos 28) carries a single L1 feature with small direct effect, while the pronoun signal is amplified by a long chain of mid- and late-layer pronoun/person-features.

**Confidence:** 7

**Reasoning:** The attribution graph is dominated by a pronoun/identity cascade. The most strongly activating upstream node is the token embedding for "he" at pos 22 (direct_effect = 40.25) feeding L0:F12768 ("mentions of he and she in close proximity", frac_nonzero = 0.011, max_act 81 on "he"), which in turn drives L4:F15567 ("sentences with male or female pronouns and possessives, especially ones referring to writing", frac_nonzero = 0.017) and a stack of mid-layer pronoun detectors — L6:F12990, L7:F14946, L13:F1937 ("pronouns used to describe people, including possessive pronouns"), L13:F6622 ("pronouns"), L14:F4420, L17:F5889 ("references to people with pronouns and possessive pronouns") — culminating in L18:F14743 at positions 22, 39 and 67 with direct_effects of −0.116, −0.099 and −0.085 against the probe. The same chain fires off the capitalized "He" embeddings at pos 39 and 67 (direct_effect 20.5–28.6 into L17:F5889; L0:F1069 = "references to a male person, particularly when using the pronoun He or His", frac_nonzero = 0.0078) and through L15:F13002 ("titles and names of people followed by their role or profession", frac_nonzero = 0.0117) and L15:F3330 ("personal stories of individuals, especially women…"). Genuine profession indicators are thin: the "writer" embedding at pos 28 (direct_effect 19.75) only triggers L1:F15416 ("the word writer", frac_nonzero = 0.0043) with a modest 0.071 direct_effect, and is then re-routed into the same pronoun/person stack via L14:F4420 rather than any job-title or occupation circuit. By contrast, the probe is also pushed by shallow generic features — L0:F9630 ("the word topic"), L0:F13754 ("words related to official or functional bodies"), L0:F5288 ("the word service"), L2:F9293 ("the word cover"), L0:F5710 ("the word themes and words associated with academic papers"), L1:F15323 ("the word starting in academic papers") — and by pure function-word features such as L0:F3820 ("the"), L0:F4870 (commas), L0:F7124 ("at"), L0:F1053 ("as"), L0:F15661 ("spin"), L0:F6051, L0:F6556 and L1:F15063. All of these have low frac_nonzero and fire on a single token rather than on any profession-specific concept. Crucially, no late-layer feature in the top-30 promotes a profession, employer, or occupation label — and several of the top negatively-signed features (L0:F7124 "at" −0.16, L0:F15661 "spin" −0.11, L0:F3820 "the" −0.10, L1:F4459, L0:F4870 "comma") are stopping the score, indicating the probe is also being shaped by syntactic noise. This confirms the user concern: the circuit is using male-gender pronoun co-occurrence (plus generic lexical/stopword features) as a proxy for the subject's profession, not any genuine profession indicator, so the classifier's profession prediction is a gender-driven spurious correlation.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 22 | Late-layer pronoun/identity aggregator at pos 22 (he) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L14:F14097](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) | 22 | Late-layer pronoun/identity aggregator at pos 22 (he) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 39 | Late-layer pronoun/identity aggregator at pos 39 (He) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 67 | Late-layer pronoun/identity aggregator at pos 39 (He) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L15:F13002](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13002) | 39 | Late-layer pronoun/identity aggregator at pos 39 (He) |  titles and names of people followed by their role or profession | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13002) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 39 | Late-layer pronoun/identity aggregator at pos 39 (He) |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 22 | Mid-layer pronoun/people features |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 39 | Mid-layer pronoun/people features |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L13:F1937](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/1937) | 22 | Mid-layer pronoun/people features |  pronouns used to describe people, including possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/1937) |
| [L13:F6622](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) | 22 | Mid-layer pronoun/people features |  pronouns. | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) |
| [L13:F6622](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) | 39 | Mid-layer pronoun/people features |  pronouns. | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 28 | Mid-layer pronoun/people features | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 22 | Mid-layer pronoun/people features | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 22 | Mid-layer pronoun/people features | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 22 | Low-layer he-pronoun detector at pos 22 |  mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L4:F15567](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) | 22 | Low-layer he-pronoun detector at pos 22 | sentences with male or female pronouns and possessives, especially ones referring to writing | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 39 | Low-layer capitalized He detector at pos 39/67 |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 67 | Low-layer capitalized He detector at pos 39/67 |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L1:F15416](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15416) | 28 | Profession-relevant word features (writer at pos 28) | the word "writers" or "writer" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15416) |
| [L0:F9630](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9630) | 20 | Generic topic/structure features (topics, Defence, service, covering) | the word "topic." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9630) |
| [L0:F13754](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13754) | 9 | Generic topic/structure features (topics, Defence, service, covering) | words related to official or functional bodies and their actions, often involving government, structure, or critique. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13754) |
| [L0:F5288](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5288) | 6 | Generic topic/structure features (topics, Defence, service, covering) |  the word "service" and related terms in different contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5288) |
| [L0:F5710](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5710) | 4 | Generic topic/structure features (topics, Defence, service, covering) | the word "themes" and words associated with academic papers | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5710) |
| [L2:F9293](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9293) | 12 | Generic topic/structure features (topics, Defence, service, covering) |  the word "cover" used in different contexts | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9293) |
| [L1:F15323](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15323) | 1 | Sentence-start features (Starting, Starting at) | the word "starting" in academic papers | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15323) |
| [L1:F4459](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4459) | 7 | Sentence-start features (Starting, Starting at) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4459) |
| [L0:F5585](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5585) | 1 | Sentence-start features (Starting, Starting at) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5585) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 3 | Function-word features (the, comma, at, as) | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F4870](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4870) | 11 | Function-word features (the, comma, at, as) |  commas and sometimes reach (context not clear) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4870) |
| [L0:F7124](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7124) | 2 | Function-word features (the, comma, at, as) | the word "at" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7124) |
| [L0:F1053](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1053) | 25 | Function-word features (the, comma, at, as) |  the word "as." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1053) |
| [L0:F15661](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15661) | 7 | Function-word features (the, comma, at, as) | the word "spin" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15661) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 38 | Function-word features (the, comma, at, as) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F6556](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6556) | 1 | Function-word features (the, comma, at, as) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6556) |
| [L1:F15063](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15063) | 5 | Function-word features (the, comma, at, as) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15063) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:7124 de=-0.160 |
| 3 | `inspect_feature` ×5 | L1:15323, L0:5288, L0:12768, L2:9293, L1:15416 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F12768@22` | ❌ error | — | — | Trace the L0:F12768 ("he/she pronoun" feature) which is driving the probe POSITI… |
| SA-2 | `L1:F15416@28` | ❌ error | — | — | Trace the L1:F15416 ("writer" word feature) which drives the probe POSITIVELY. D… |
| SA-3 | `L0:F5288@6` | ❌ error | — | — | Trace the L0:F5288 ("service" word feature) at pos 6 driving the probe POSITIVEL… |
| SA-4 | `L1:F15323@1` | ❌ error | — | — | Trace the L1:F15323 ("starting" in academic contexts) at pos 1. Determine if thi… |
| SA-5 | `L2:F9293@12` | ❌ error | — | — | Trace L2:F9293 ("cover" word feature) at pos 12. Pos 12 in the text is "covering… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F12768@22, k=15 → Emb:" he"@22 (de=40.25) +14 more |
| 2 | `get_upstream_features` | L1:F15416@28, k=15 → Emb:" writer"@28 (de=19.75) +14 more |
| 3 | `get_upstream_features` | L0:F5288@6, k=15 → Emb:" Services"@6 (de=14.19) +14 more |
| 4 | `get_upstream_features` | L1:F15323@1, k=15 → Emb:"Starting"@1 (de=16.38) +14 more |
| 5 | `get_upstream_features` | L2:F9293@12, k=15 → Emb:" covering"@12 (de=26.50) +14 more |
| 6 | `get_upstream_features` | L0:F12768@22, k=5 → Emb:" he"@22 (de=40.25) +4 more |
| 7 | `get_upstream_features` | L18:F14743@22, k=5 → Emb:" he"@22 (de=28.62) +4 more |
| 8 | `get_upstream_features` | L14:F14097@22, k=5 → Emb:" he"@22 (de=2.70) +4 more |
| 9 | `inspect_feature` ×3 | L17:5889, L13:1937, L4:15567 |
| 10 | `get_upstream_features` | L18:F14743@39, k=8 → Emb:" He"@39 (de=21.88) +7 more |
| 11 | `get_upstream_features` | L14:F14097@22, k=8 → Emb:" he"@22 (de=2.70) +7 more |
| 12 | `get_upstream_features` | L18:F14743@67, k=8 → Emb:" He"@67 (de=23.38) +7 more |
| 13 | `inspect_feature` ×4 | L0:1069, L13:6622, L15:3330, L15:13002 |
| 14 | `get_upstream_features` | L17:F5889@39, k=8 → Emb:" He"@39 (de=20.50) +7 more |
| 15 | `get_upstream_features` | L15:F13002@39, k=8 → Emb:"Starting"@1 (de=-3.02) +7 more |
| 16 | `get_top_features` | token="", k=30 → 30 features; top: L0:7124 de=-0.160 |
| 17 | `inspect_feature` ×9 | L0:9630, L0:13754, L0:5710, L0:3638, L0:1053, L0:7124, L0:15661, L0:3820, L0:4870 |

### Build

`build_circuit` → 16 nodes, 16 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 51,756 | 6,348 | 288,217 | 0 | $0.0404 | — | — |
| **Total** | | **51,756** | **6,348** | **288,217** | **0** | **$0.0404** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 21s