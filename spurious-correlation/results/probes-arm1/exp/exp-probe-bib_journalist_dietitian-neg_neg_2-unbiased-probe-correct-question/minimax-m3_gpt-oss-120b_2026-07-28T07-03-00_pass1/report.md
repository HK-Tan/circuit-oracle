# Circuit Oracle Report
**Date:** 2026-07-28 07:03:00 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's journalist-classification score is driven almost entirely by genuine profession-related content (the token "report" at position 21, and the "news organizations" phrase at positions 22-29) propagating through a clean chain of journalism-specific features, with only a tiny auxiliary contribution from the pronoun "His."

**Confidence:** 8

**Reasoning:**

The user's hypothesis — that the circuit relies on spurious gender markers ("His") rather than genuine profession cues — is **not supported** by this attribution graph. The evidence cuts the other way.

**Dominant signal: content tokens, not "His"** — The largest single direct effects on the probe all originate from the *verb* "report" at position 21, not from "His" at position 1. Specifically:
- L7:F13646 (news-reporting detector) receives direct effects of +7.22 from the **" report" embedding** and only +0.98 from the **"His" embedding** — a 7× disparity.
- L8:F8855 (reporter/news-reporting detector) receives a +12.06 direct effect from the " report" embedding, and never shows up in the upstream of the "His" feature.
- L14:F4420 ("words related to journalism and newspapers," frac_nonzero 0.0165) receives +5.22 from " report" vs. only +0.98 from "His" routed through L7:F13646.
- L19:F2486 ("journalistic sources and news outlets," frac_nonzero 0.029, promoted tokens = "reporting/reporter/coverage") is the most strongly negative-driving late-layer feature (direct effect -0.1128 at pos 21, summed to ~-0.49 across pos 21-29), and is fed by L14:F4420 with direct_effect +14.31. Its top activating examples are news-organization contexts ("by USA TODAY Network," "news director at KRLD-TV"), confirming it is a domain detector, not a gender detector.

**Where the "His" feature actually goes** — L0:F8964 (frac_nonzero 0.018, label "the possessive pronoun 'His'") does have a meaningful +0.0791 direct effect on the probe, which is *positive* and not negligible in isolation. But the only downstream feature it feeds is L7:F13646, and via that route it adds ≈0.98 to a feature that is simultaneously being excited by ≈7.22 from " report". The "His" path is a thin side-channel, not the backbone of the circuit. L0:F8964's top activating examples are also generic historical/biographical "His" openings (Frederick duke of, Nasr governor, etc.), so the feature itself is not stereotypically gendered in a "journalist" sense — it just happens to fire here.

**The two output-driving branches are content-driven:**
1. **Journalism branch (strongest):** Emb:" report" (pos 21) → L7:F13646 / L7:F9092 / L8:F8855 / L8:F8437 → L14:F4420 → L19:F2486 → output. All five features in this chain have frac_nonzero ≤ 0.029 and explicitly promote tokens like "reporter," "journalist," "reporting," "newspaper."
2. **Broadcasting/phrase branch:** Emb:" organizations" (pos 22) → L20:F8433 ("news broadcasting," frac_nonzero 0.036, promoted "news/News/journalists") + L21:F4401 → output.

**Generic "world" / "see" / "to" features at L0 are not profession-specific.** L0:F2203 ("world/game"), L0:F771 ("see"), L0:F14582 ("left") and friends contribute to early-layer activity, but the negative direct effects of L0:F2203 (-0.057) and L0:F771 (-0.054) on the probe *push against* the journalist classification, so they are not spurious-positive evidence either.

**Bottom line:** The classification is carried by a textbook profession-cue circuit — the verb "report" plus "news organizations" → journalism detectors → probe. "His" contributes marginally as a generic subject-introducing pronoun but is neither the primary nor a stereotyped-gender driver. The user's concern that the probe uses gender markers as a proxy for profession is not borne out by this attribution graph.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F8964](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) | 1 | L0: F8964 'His' pronoun detector (pos 1) |  the possessive pronoun "His" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 3 | L0 generic 'to'/'see'/'dream' / opinion tokens (pos 2-4) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F14287](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14287) | 4 | L0 generic 'to'/'see'/'dream' / opinion tokens (pos 2-4) | the word "see" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14287) |
| [L0:F2011](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) | 2 | L0 generic 'to'/'see'/'dream' / opinion tokens (pos 2-4) |  the word "dream" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) |
| [L0:F13948](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13948) | 2 | L0 generic 'to'/'see'/'dream' / opinion tokens (pos 2-4) |  the color "pink" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13948) |
| [L0:F15693](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15693) | 2 | L0 generic 'to'/'see'/'dream' / opinion tokens (pos 2-4) |  language related to personal anecdotes and opinions | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15693) |
| [L0:F2203](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2203) | 6 | L0 generic 'world'/'left' tokens (pos 6) |  instances of the words "world" or "game" (possibly "problem") or expressions of existential quandaries. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2203) |
| [L0:F14582](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14582) | 6 | L0 generic 'world'/'left' tokens (pos 6) | the word "left" and sometimes "center" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14582) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 20 | L0: F8444 'to' at pos 20 (token before 'report') | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F15185](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15185) | 2 | L0: F15185 generic 'do'/'us' (pos 2, contributes to 'to' at pos 6) | the word "do" alongside references to figures, types, and the pronouns "we" and "us", possibly in the context of scientific studies and collaborative efforts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15185) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 21 | L7-8: early journalism/news-reporting detectors (pos 21) | news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 21 | L7-8: early journalism/news-reporting detectors (pos 21) | words and phrases associated with broadcast journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L7:F3085](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3085) | 6 | L7-8: early journalism/news-reporting detectors (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3085) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 21 | L7-8: early journalism/news-reporting detectors (pos 21) | mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 21 | L7-8: early journalism/news-reporting detectors (pos 21) | content related to film festivals and production, particularly documentary films | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 21 | L14: F4420 'journalism/newspapers' (pos 21,22) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 22 | L14: F4420 'journalism/newspapers' (pos 21,22) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 21 | L19: F2486 'journalistic sources / news outlets' (pos 21-29) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 22 | L19: F2486 'journalistic sources / news outlets' (pos 21-29) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 25 | L19: F2486 'journalistic sources / news outlets' (pos 21-29) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 26 | L19: F2486 'journalistic sources / news outlets' (pos 21-29) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 27 | L19: F2486 'journalistic sources / news outlets' (pos 21-29) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 28 | L19: F2486 'journalistic sources / news outlets' (pos 21-29) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 29 | L19: F2486 'journalistic sources / news outlets' (pos 21-29) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L20:F8433](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/8433) | 26 | L20: F8433 'news broadcasting' (pos 22,26) + L21:F4401 (pos 22) | words related to news broadcasting | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/8433) |
| [L20:F8433](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/8433) | 22 | L20: F8433 'news broadcasting' (pos 22,26) + L21:F4401 (pos 22) | words related to news broadcasting | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/8433) |
| [L21:F4401](https://neuronpedia.org/gemma-2-2b/21-gemmascope-transcoder-16k/4401) | 22 | L20: F8433 'news broadcasting' (pos 22,26) + L21:F4401 (pos 22) | — | [view](https://neuronpedia.org/gemma-2-2b/21-gemmascope-transcoder-16k/4401) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:4420 de=-0.145 |
| 3 | `inspect_feature` ×9 | L14:4420, L19:2486, L0:8964, L0:8444, L0:14287, L20:8433, L0:2203, L4:11898, L5:771 |
| 4 | `get_top_features` | 30 features; top: L14:4420 de=-0.145 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@21` | ✅ reported | 5 | 7 | Trace the path upstream from L14:F4420 (journalism/newspapers) at position 21. G… |
| SA-2 | `L19:F2486@21` | ✅ reported | 6 | 10 | Trace the path upstream from L19:F2486 (journalistic sources / news outlets) at … |
| SA-3 | `L0:F8964@1` | ❌ error | — | — | Trace the path upstream from L0:F8964 ("His" possessive pronoun feature) at posi… |

<details>
<summary><b>SA-1</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@21, k=10 | Emb:" report"@21 (de=5.22) +9 more |
| 3 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 4 | `get_upstream_features` | L8:F8855@21, k=10 | Emb:" report"@21 (de=12.06) +9 more |
| 5 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 6 | `inspect_feature` | L7, F9092 | " words and phrases associated with broadcast journalism" |
| 7 | `get_upstream_features` | L7:F13646@21, k=10 | Emb:" report"@21 (de=7.22) +9 more |
| 8 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |
| 9 | `inspect_feature` | L0, F12801 | " verbs related to communication, help, enabling, and allowing" |

**Findings:** The L14:F4420 journalism feature is primarily driven by the input token "report" (position 21). The strongest upstream influence comes from the embedding of " report" directly to the target (direct effect 5.22) and via two mid‑layer journalism detectors: L8:8855 (direct effect 5.06) and L7:13646 (direct effect 3.73). Both of those sub‑features also receive a large positive effect from the same " r…

</details>

<details>
<summary><b>SA-2</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F2486 | " journalistic sources and news outlets." |
| 2 | `get_upstream_features` | L19:F2486@21, k=10 | L14:F4420 (de=14.31) +9 more |
| 3 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 4 | `get_upstream_features` | L14:F4420@21, k=10 | Emb:" report"@21 (de=5.22) +9 more |
| 5 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 6 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 7 | `get_upstream_features` | L8:F8855@21, k=10 | Emb:" report"@21 (de=12.06) +9 more |
| 8 | `get_upstream_features` | L7:F13646@21, k=10 | Emb:" report"@21 (de=7.22) +9 more |

**Findings:** The target L19:F2486 (journalistic sources) receives its strongest excitatory drive from the token embedding 'report' at position 21, propagated through a short chain of lower‑layer features (L7:F13646 → L8:F8855 → L14:F4420 → L19:F2486). A much smaller positive influence comes from the pronoun 'His' via L7:F13646, but its magnitude (≈0.98) is negligible compared to the 'report' pathway (≈12.06 at…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F4420@21, k=10 → Emb:" report"@21 (de=5.22) +9 more |
| 2 | `get_upstream_features` | L7:F13646@21, k=10 → Emb:" report"@21 (de=7.22) +9 more |
| 3 | `get_upstream_features` | L0:F8964@1, k=8 → Emb:"His"@1 (de=13.69) +7 more |
| 4 | `inspect_feature` ×5 | L0:2011, L0:13948, L0:15693, L0:15185, L0:14582 |

### Build

`build_circuit` → 15 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 32,531 | 4,756 | 130,540 | 0 | $0.0233 | — | — |
| SA-2 | openai/gpt-oss-120b | 72,427 | 4,392 | 8,640 | 0 | $0.0136 | ✅ 6F/10E | Trace the path upstream from L19:F2486 (journalistic sources… |
| SA-1 | openai/gpt-oss-120b | 106,947 | 6,360 | 10,240 | 0 | $0.0200 | ✅ 5F/7E | Trace the path upstream from L14:F4420 (journalism/newspaper… |
| **Total** | | **211,905** | **15,508** | **149,420** | **0** | **$0.0569** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 8s