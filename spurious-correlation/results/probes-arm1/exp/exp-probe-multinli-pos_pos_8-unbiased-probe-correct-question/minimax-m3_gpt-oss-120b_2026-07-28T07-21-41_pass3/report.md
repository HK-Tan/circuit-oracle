# Circuit Oracle Report
**Date:** 2026-07-28 07:21:41 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_8 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction probe is driven primarily by surface-level lexical cues (the word "Congress," "include/including," commas/punctuation, "to," and the relativizer "who") rather than by deeper semantic features about premise/hypothesis content — so the user's concern about spurious negation-style signals is *partially* correct but more specifically the circuit shows a polysemy/surface-lexicon problem: a "Congress" + "include members who" template, which the probe apparently learned to associate with the contradiction class.

**Confidence:** 7

**Reasoning:** The top features driving the probe (by direct_effect) are:
- **L2:F2701** (+0.85, pos 2, label "words related to the U.S. Congress") — the highest positive driver.
- **L3:F5753** (+0.53, pos 12, label "the word 'includes' or 'containing'").
- **L0:F6044** (+0.49) and **L0:F15411** (+0.49, "terms relating to political bodies, figures, and processes") — both at pos 2.
- **L4:F59** (+0.41, pos 11, "phrases with the word 'to' preceded by a verb or 'start'/'begin'") — fires on the "began to" sequence in the premise.
- **L0:F195** (-0.21, pos 15, "the word 'who'") — small negative.

Tracing upstream from these top features reveals the circuit's true depth: nearly all of them root in token-embedding nodes for the same handful of surface tokens — ` Congress` (pos 2, +28 direct_effect to L2:F2701), ` include` (pos 12, +41 to L3:F5753, +25 to L0:F10783, +28 to L3:F8351), ` to` (pos 11, +21 to L3:F12596, +9 to L2:F11469, +41 to L0:F8444), ` began` (pos 10, +18/+13/+10 to L4:F59/L3:F12596/L2:F11469), `,` (pos 9, +33 to L0:F4870, +4.9 to L2:F11734), ` which` (pos 4), `The` (pos 1), and ` who`/` members` (pos 14-15).

The five supernodes feeding the probe output are:
1. **sn_congress_main** (L2:F2701, L1:F14850, L1:F2089, L1:F3276, L3:F123) — multiple "Congress"-entity features at pos 2.
2. **sn_congress_emb_l0** (L0:F10198 "Congress", F15411 "political bodies", F6044 "yield" (an off-target lexical neighbor), F10401 "genes" (off-topic), F3204 "proper nouns", F14565 "locations/government positions", F13168 "broad/wild/faced", F2335 "linear motion guides") — a mixed bag of L0 "Congress"-neighborhood features, several of which are NOT entity-specific.
3. **sn_incl_main** (L3:F5753 "includes", L0:F10783 "include", L0:F14517 "including", L1:F3271 "including", L2:F13152 "legal jargon/present tense verbs") — the "include/including" cluster at pos 12.
4. **sn_to_began_l4** (L4:F59 "to after start/begin", L3:F4374 "to", L2:F11469 "to", L3:F12596 "actions/methods a/to", L0:F8444 "to", L1:F13759, L1:F2493) — six separate "to" detectors all firing on pos 11.
5. **sn_punct_l4** (L4:F7775 "punctuation", L2:F11734 "quotes/dashes", L0:F4870 "commas") at pos 9.
6. **sn_who_members_l0** (L0:F195 "who") at pos 15.

**Crucially, the circuit does NOT contain a negation-word detector** (no feature for "no," "not," "without," "never," "nothing," "no" — the words that actually mark the contradiction in the hypothesis "the congress has no responsibility"). The user's hypothesis about "negation words" is therefore not quite right for THIS graph — the dominant signal is a different kind of spurious cue: the **premise-template fingerprint** of "The Congress, which controls X, began to include many members who…" — a long, politically-framed, multi-clause premise with embedded "which…began to include many members who" syntactic structure. The probe appears to have learned that long premise templates containing "Congress" + "include members who" predict the contradiction label, rather than learning the semantic content of premise vs. hypothesis. The `S_pct_of_total` is small and negative (-8.7%), suggesting the source-position (premise) influence on the probe is not strong as a single share, but the per-feature direct effects are concentrated exactly on these surface lexical detectors rather than on any compositional/semantic contradiction features — a classic surface-cue shortcut, but a different one from negation-word shortcuts (it's a "long-political-premise-template" shortcut, not a "negation" shortcut).

The presence of several off-topic L0 features in the Congress neighborhood (F6044 "yield," F10401 "genes," F2335 "linear motion guides") with non-zero direct_effect also suggests the circuit is not cleanly selective — it's a broad, low-frequency lexical bag rather than a precise semantic decomposition.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L2:F2701](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) | 2 | L2 'Congress' entity + L1 'US Congress' reference + L3 'Congress' entity |  words related to the U.S. Congress | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) |
| [L1:F14850](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14850) | 2 | L2 'Congress' entity + L1 'US Congress' reference + L3 'Congress' entity | references to the U.S. Congress. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14850) |
| [L1:F2089](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2089) | 2 | L2 'Congress' entity + L1 'US Congress' reference + L3 'Congress' entity |  mentions of `constructor` or `congress` | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2089) |
| [L1:F3276](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3276) | 2 | L2 'Congress' entity + L1 'US Congress' reference + L3 'Congress' entity |  mentions of the United States Congress | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3276) |
| [L3:F123](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/123) | 2 | L2 'Congress' entity + L1 'US Congress' reference + L3 'Congress' entity |  mentions of the United States Congress | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/123) |
| [L0:F10198](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10198) | 2 | L0 'Congress' word + L0 'political bodies' |  the word "Congress" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10198) |
| [L0:F15411](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15411) | 2 | L0 'Congress' word + L0 'political bodies' |  terms relating to political bodies, figures, and processes | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15411) |
| [L0:F6044](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) | 2 | L0 'Congress' word + L0 'political bodies' | the word "yield" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) |
| [L0:F10401](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10401) | 2 | L0 'Congress' word + L0 'political bodies' |  mentions of genes and proteins | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10401) |
| [L0:F3204](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3204) | 2 | L0 'Congress' word + L0 'political bodies' |  proper nouns, especially including titles of works and organizations | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3204) |
| [L0:F14565](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14565) | 2 | L0 'Congress' word + L0 'political bodies' | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14565) |
| [L0:F13168](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13168) | 2 | L0 'Congress' word + L0 'political bodies' |  the words "broad," "wild," and "faced" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13168) |
| [L1:F2335](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2335) | 2 | L0 'Congress' word + L0 'political bodies' |  technical descriptions of mechanical parts for guiding linear motion | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2335) |
| [L3:F5753](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5753) | 12 | L3 'includes/containing' + L0 'include' + L0 'including' + L1 'including' |  the word "includes" or "containing". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5753) |
| [L0:F10783](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10783) | 12 | L3 'includes/containing' + L0 'include' + L0 'including' + L1 'including' |  the word "include" (and variations of the word) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10783) |
| [L0:F14517](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14517) | 12 | L3 'includes/containing' + L0 'include' + L0 'including' + L1 'including' | the word "including" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14517) |
| [L1:F3271](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3271) | 12 | L3 'includes/containing' + L0 'include' + L0 'including' + L1 'including' | the word "including" or its variants | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3271) |
| [L2:F13152](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13152) | 12 | L3 'includes/containing' + L0 'include' + L0 'including' + L1 'including' | scientific and legal jargon, as well as present tense verbs | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13152) |
| [L4:F7775](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7775) | 9 | L4 punctuation, quotes/dashes; L2 punctuation-phrase feature; L0 comma feature |  various forms of punctuation | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7775) |
| [L2:F11734](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11734) | 9 | L4 punctuation, quotes/dashes; L2 punctuation-phrase feature; L0 comma feature |  phrases containing punctuation such as quotes and dashes | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11734) |
| [L0:F4870](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4870) | 9 | L4 punctuation, quotes/dashes; L2 punctuation-phrase feature; L0 comma feature |  commas and sometimes reach (context not clear) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4870) |
| [L2:F4680](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4680) | 9 | L4 punctuation, quotes/dashes; L2 punctuation-phrase feature; L0 comma feature | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4680) |
| [L2:F6493](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6493) | 9 | L4 punctuation, quotes/dashes; L2 punctuation-phrase feature; L0 comma feature | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6493) |
| [L4:F59](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/59) | 11 | L4 'to' after start/begin + L3 'to' feature + L2 'to' + L3 'actions/methods (a/to)' |  phrases with the word 'to' preceded by a verb or the word 'start' or 'begin'. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/59) |
| [L3:F4374](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4374) | 11 | L4 'to' after start/begin + L3 'to' feature + L2 'to' + L3 'actions/methods (a/to)' |  instances of the word "to" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4374) |
| [L2:F11469](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11469) | 11 | L4 'to' after start/begin + L3 'to' feature + L2 'to' + L3 'actions/methods (a/to)' |  the word "to" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11469) |
| [L3:F12596](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12596) | 11 | L4 'to' after start/begin + L3 'to' feature + L2 'to' + L3 'actions/methods (a/to)' |  actions or methods, sometimes preceeded by the preposition 'a' or 'to'. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12596) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 11 | L4 'to' after start/begin + L3 'to' feature + L2 'to' + L3 'actions/methods (a/to)' | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L1:F13759](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13759) | 11 | L4 'to' after start/begin + L3 'to' feature + L2 'to' + L3 'actions/methods (a/to)' | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13759) |
| [L1:F2493](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2493) | 11 | L4 'to' after start/begin + L3 'to' feature + L2 'to' + L3 'actions/methods (a/to)' | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2493) |
| [L0:F195](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/195) | 15 | L0 'who' (relativizer) at pos 15 | the word "who" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/195) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L2:2701 de=0.848 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F2701@2` | ❌ error | — | — | Trace the path from L2:F2701 (highest positive direct effect on probe) upstream.… |
| SA-2 | `L3:F5753@12` | ❌ error | — | — | Trace the path from L3:F5753 (high positive direct effect, pos=12) upstream. Det… |
| SA-3 | `L4:F59@11` | ❌ error | — | — | Trace the path from L4:F59 (high positive direct effect, pos=11) upstream. Deter… |
| SA-4 | `L0:F6044@2` | ❌ error | — | — | Trace the path from L0:F6044 upstream. Determine what this very-early feature en… |
| SA-5 | `L0:F15411@2` | ❌ error | — | — | Trace the path from L0:F15411 upstream. Determine what this very-early feature e… |
| SA-6 | `L4:F7775@9` | ❌ error | — | — | Trace the path from L4:F7775 (positive direct effect, pos=9) upstream. Determine… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×20 | L2:2701, L3:5753, L0:6044, L0:15411, L4:59, L0:10401, L2:6735, L3:8351, L0:9557, L1:4224, L3:123, L1:5475, L0:3204, L0:10783, L1:2089, L1:14565, L0:10198, L1:12456, L4:7775, L0:195 |
| 2 | `get_upstream_features` | L2:F2701@2, k=10 → Emb:" Congress"@2 (de=28.12) +9 more |
| 3 | `get_upstream_features` | L3:F5753@12, k=10 → Emb:" include"@12 (de=41.00) +9 more |
| 4 | `get_upstream_features` | L4:F59@11, k=10 → Emb:" began"@10 (de=13.31) +9 more |
| 5 | `get_upstream_features` | L0:F6044@2, k=10 → Emb:" Congress"@2 (de=17.00) +9 more |
| 6 | `get_upstream_features` | L2:F6735@2, k=10 → Emb:" Congress"@2 (de=9.12) +9 more |
| 7 | `get_upstream_features` | L3:F8351@12, k=10 → Emb:" include"@12 (de=28.38) +9 more |
| 8 | `get_upstream_features` | L0:F195@15, k=10 → Emb:" who"@15 (de=16.25) +9 more |
| 9 | `get_upstream_features` | L4:F7775@9, k=10 → Emb:","@9 (de=4.94) +9 more |
| 10 | `get_upstream_features` | L0:F10783@12, k=10 → Emb:" include"@12 (de=25.50) +9 more |
| 11 | `get_upstream_features` | L3:F123@2, k=10 → Emb:" Congress"@2 (de=20.62) +9 more |
| 12 | `inspect_feature` ×24 | L0:13168, L1:14850, L1:2335, L3:12596, L2:11469, L0:14517, L1:3271, L3:4374, L2:13152, L1:3276, L0:10198, L0:10401, L1:4224, L0:15411, L2:11469, L0:14517, L3:12596, L3:4374, L4:7775, L2:11734, L0:4870, L0:8444, L0:13168, L0:14517 |
| 13 | `get_upstream_features` | L3:F12596@11, k=8 → Emb:" to"@11 (de=21.62) +7 more |
| 14 | `get_upstream_features` | L2:F11469@11, k=8 → Emb:" began"@10 (de=10.88) +7 more |
| 15 | `get_upstream_features` | L1:F14850@2, k=8 → Emb:" Congress"@2 (de=17.62) +7 more |
| 16 | `get_upstream_features` | L0:F13168@2, k=8 → Emb:" Congress"@2 (de=12.88) +7 more |
| 17 | `get_upstream_features` | L3:F4374@11, k=8 → Emb:" began"@10 (de=10.50) +7 more |
| 18 | `get_upstream_features` | L0:F14517@12, k=8 → Emb:" include"@12 (de=12.88) +7 more |
| 19 | `get_upstream_features` | L2:F11734@9, k=8 → Emb:","@9 (de=5.28) +7 more |
| 20 | `get_upstream_features` | L0:F4870@9, k=8 → Emb:","@9 (de=32.75) +7 more |
| 21 | `get_upstream_features` | L0:F8444@11, k=8 → Emb:" to"@11 (de=41.50) +7 more |
| 22 | `get_upstream_features` | L2:F13152@12, k=8 → Emb:" include"@12 (de=10.12) +7 more |
| 23 | `get_upstream_features` | L1:F3271@12, k=8 → Emb:" include"@12 (de=16.00) +7 more |
| 24 | `get_source_influence` | {'depth': 3, 'source_positions': [2, 12, 11, 9, 15]} → {'depth': 3, 'source_positions': [2, 9, 11, 12, 15], 'S_pct_of_total': -8.676, ' |

### Build

`build_circuit` → 19 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 83,312 | 7,728 | 404,542 | 0 | $0.0585 | — | — |
| **Total** | | **83,312** | **7,728** | **404,542** | **0** | **$0.0585** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 46s