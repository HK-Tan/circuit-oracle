# Circuit Oracle Report
**Date:** 2026-07-28 07:22:15 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity score is driven primarily by a small set of mid-layer features that fire specifically when an *identity-group noun* (especially "Indians", but also "Americans", "Asians", "Canadians", etc.) co-occurs with *abuse/violence vocabulary* ("abusers", "abusive", "abusing"), rather than by features that read the actual toxicity-laden lexical content of the prompt.

**Confidence:** 6

**Reasoning:**

The strongest positive driver, L0:F11375 (pos 8, de=+0.221, the literal word "is"), is a generic function-word detector with frac_nonzero ≈ 0.01; it carries no toxicity signal on its own — it just identifies that a copular clause exists. The second-strongest positive driver, L0:F11668 (pos 1, de=+0.183), is mislabeled "Baseball terminology" but functionally reads the "Indians" embedding (upstream direct_effect = 12.4 from the "Indians" token at pos 1) and is again a low-content word detector. L6:F10545 (pos 3, de=+0.136) is the closest thing to a "political rhetoric / race" feature, but its actual evidence is the lexical "abusers" embedding (de=1.9) plus L4:F148 ("sexual assault / abuse") and L0:F11154 ("are"). L3:F13473 (pos 2, de=+0.123) is the linchpin identity-detection feature: its label and examples are explicit — "mentions of racial and ethnic groups, especially in the United States" — and its upstream direct_effects (Emb "Indians" = 10.25, Emb "are" = 5.28, L2:F2123 = 2.45) show it fires on the surface form of a national/ethnic noun, not on any toxicity-bearing content. L2:F2123 reinforces this with an "-ian" suffix detector (promoted tokens include "Canadian", "American") that also activates on "Indians".

The strongest *negative* driver, L3:F14281 (pos 18, de=−0.157), is a *French/question-word* feature that happens to fire on "how" / "to" / "know" — its contribution is positional noise, not content. The other negative features are likewise generic: L0:F11154 ("are", de=−0.139), L0:F3498 ("they", de=−0.096), L6:F1600 ("problems", de=−0.098), L3:F5853 ("stated", de=−0.093). These cancel out the function-word positives but do not encode meaning.

Net: the circuit's content-bearing backbone is **L2:F2123 (identity morpheme) → L3:F13473 (racial/ethnic group mention) → L6:F10545 (political-racial-rhetoric aggregator) → probe**, with **L4:F148 / L5:F3229 (abuse/violence vocabulary) → L6:F10545** adding a thin thread of real toxicity signal via the "abusers" token. In other words, the probe leans heavily on *who* is being talked about (an identity group) and only modestly on *what* is being said about them (the word "abusers"). If the noun "Indians" were replaced with a non-identity noun while keeping the identical hostile verb, the L2/L3 identity branch would go quiet and the probe score should drop substantially — confirming the user's concern that the circuit uses a **"subject-is-an-identity-group"** spurious feature rather than a faithful read of the prompt's toxicity-laden lexical semantics.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 8 | L0: function-word detectors (is/are/they/by/stated) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F11154](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11154) | 2 | L0: function-word detectors (is/are/they/by/stated) |  the word "are" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11154) |
| [L0:F3498](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) | 5 | L0: function-word detectors (is/are/they/by/stated) |  the pronoun "they" or its possessive form. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 7 | L0: function-word detectors (is/are/they/by/stated) |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F8381](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8381) | 23 | L0: function-word detectors (is/are/they/by/stated) |  the word 'by' | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8381) |
| [L0:F11668](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11668) | 1 | L0: function-word detectors (is/are/they/by/stated) |  Baseball terminology | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11668) |
| [L2:F2123](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2123) | 1 | L2: 'ian'/'jani' suffix feature + group-member nouns |  words ending in "ian", "jani", "iti", "ino", or "olan" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2123) |
| [L2:F1680](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1680) | 1 | L2: 'ian'/'jani' suffix feature + group-member nouns |  words that refer to people participating in some activity, such as consumers, patients in healthcare, or voters | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1680) |
| [L2:F9873](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9873) | 3 | L2: 'ian'/'jani' suffix feature + group-member nouns |  instances of abusive language or words that end in "ally" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9873) |
| [L2:F13183](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13183) | 7 | L2: 'ian'/'jani' suffix feature + group-member nouns |  the word "stated" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13183) |
| [L3:F13473](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13473) | 2 | L3: racial/ethnic group-mention feature (fires on 'Indians', 'Americans', 'Asians', etc.) |  mentions of racial and ethnic groups, especially in the United States | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13473) |
| [L3:F9646](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9646) | 2 | L3: racial/ethnic group-mention feature (fires on 'Indians', 'Americans', 'Asians', etc.) | verbs and associated nouns. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9646) |
| [L3:F4327](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4327) | 3 | L3: racial/ethnic group-mention feature (fires on 'Indians', 'Americans', 'Asians', etc.) | words and phrases that end with "ive", and also a few words that end in "ices" or "ishes", and also the phrase "advantage of the". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4327) |
| [L3:F5853](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5853) | 7 | L3: racial/ethnic group-mention feature (fires on 'Indians', 'Americans', 'Asians', etc.) |  instances of people speaking and making statements | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5853) |
| [L3:F14281](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14281) | 18 | L3: racial/ethnic group-mention feature (fires on 'Indians', 'Americans', 'Asians', etc.) |  questions about how to do things, and some French words | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14281) |
| [L4:F148](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/148) | 3 | L4: sexual-assault / abuse vocabulary feature |  words and phrases related to sexual assault and abuse | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/148) |
| [L5:F3229](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3229) | 3 | L5: violent-assault/murder vocabulary feature |  words related to violent assault and murder | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3229) |
| [L6:F10545](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10545) | 3 | L6: political-racial-rhetoric features (fired on 'abusers' / 'problems') |  political rhetoric related to race, historical states, and government control | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10545) |
| [L6:F1600](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1600) | 12 | L6: political-racial-rhetoric features (fired on 'abusers' / 'problems') |  negative words and phrases related to problems and imperfections | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1600) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:11375 de=0.221 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F11375@8` | ❌ error | — | — | Trace the path from L0:F11375 (pos 8, direct_effect=0.2207 — the single most imp… |
| SA-2 | `L0:F11668@1` | ❌ error | — | — | Trace the path from L0:F11668 (pos 1, direct_effect=0.1826). What does this feat… |
| SA-3 | `L3:F14281@18` | ❌ error | — | — | Trace the path from L3:F14281 (pos 18, direct_effect=-0.1572 — the strongest neg… |
| SA-4 | `L6:F10545@3` | ❌ error | — | — | Trace the path from L6:F10545 (pos 3, direct_effect=0.1357). What does this feat… |
| SA-5 | `L2:F1680@1` | ❌ error | — | — | Trace the path from L2:F1680 (pos 1, direct_effect=0.1045). What does this featu… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×15 | L0:11375, L0:11668, L3:14281, L0:11154, L6:10545, L3:13473, L5:3229, L2:1680, L0:8381, L6:1600, L3:9646, L3:4327, L0:3498, L0:3436, L3:5853 |
| 2 | `get_upstream_features` | L3:F13473@2, k=8 → Emb:"Indians"@1 (de=10.25) +7 more |
| 3 | `get_upstream_features` | L6:F10545@3, k=8 → Emb:" abusers"@3 (de=1.90) +7 more |
| 4 | `get_upstream_features` | L5:F3229@3, k=8 → Emb:" abusers"@3 (de=1.91) +7 more |
| 5 | `get_upstream_features` | L3:F14281@18, k=8 → Emb:" how"@17 (de=31.38) +7 more |
| 6 | `inspect_feature` ×4 | L2:2123, L4:148, L0:8444, L2:1680 |
| 7 | `get_upstream_features` | L0:F11375@8, k=6 → Emb:" is"@8 (de=32.50) +5 more |
| 8 | `get_upstream_features` | L0:F11668@1, k=6 → Emb:"Indians"@1 (de=12.38) +5 more |
| 9 | `get_upstream_features` | L3:F13473@3, k=6 → ❌ Feature (layer=3, feature_idx=13473) not found at pos=3. Thi |
| 10 | `get_upstream_features` | L0:F11154@2, k=5 → Emb:" are"@2 (de=36.00) +4 more |
| 11 | `get_upstream_features` | L0:F3436@7, k=5 → Emb:" stated"@7 (de=10.75) +4 more |
| 12 | `get_upstream_features` | L0:F3498@5, k=5 → Emb:" they"@5 (de=45.25) +4 more |
| 13 | `inspect_feature` | L0, F11668 → " Baseball terminology" |
| 14 | `get_upstream_features` | L3:F9646@2, k=5 → Emb:"Indians"@1 (de=3.97) +4 more |
| 15 | `get_upstream_features` | L3:F4327@3, k=5 → Emb:" abusers"@3 (de=12.75) +4 more |
| 16 | `get_upstream_features` | L3:F5853@7, k=5 → Emb:" stated"@7 (de=23.75) +4 more |
| 17 | `get_upstream_features` | L6:F1600@12, k=5 → Emb:" problems"@12 (de=21.25) +4 more |
| 18 | `get_upstream_features` | L0:F8381@23, k=5 → Emb:" by"@23 (de=36.25) +4 more |
| 19 | `get_upstream_features` | L2:F1680@1, k=5 → Emb:"Indians"@1 (de=8.56) +4 more |
| 20 | `inspect_feature` ×3 | L2:2123, L2:13183, L2:9873 |

### Build

`build_circuit` → 15 nodes, 23 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 57,690 | 5,934 | 320,962 | 0 | $0.0437 | — | — |
| **Total** | | **57,690** | **5,934** | **320,962** | **0** | **$0.0437** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 23s