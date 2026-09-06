# Circuit Oracle Report
**Date:** 2026-07-28 07:24:52 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of "journalist" is driven primarily by genuine profession-related lexical/contextual features centered on the verbs and nouns *report*, *news*, *top*, and *organizations*, aggregated by late-layer concept features — not by the masculine pronoun "His" as a gender spurious cue.

**Confidence:** 4

**Reasoning:** The user hypothesizes that the circuit uses spurious gender markers (e.g., "His") rather than genuine profession indicators. Inspecting the circuit, the dominant path is grounded in profession-specific vocabulary:

- **L14:F4420 (the strongest single feature, direct_effect ≈ -0.148)** is a "report/journal verb" concept feature that fires on the *report* token (pos 21) and propagates activations across positions 22, 25–29, feeding both L19:F2486 and L20:F8433. Its upstream chain leads back to the embeddings of *report*, *news*, *organizations*, and *countries* — i.e., real occupation context — and to early/mid features L4:F13253, L7:F13646, L7:F9092, L8:F8855, L8:F8437, L11:F5996, all of which are themselves anchored in those same profession tokens.
- **L19:F2486 (multi-position aggregator)** is fed by L14:F4420 *and* by a parallel "news" sub-circuit: L4:F13253 → L14:F8761 → L17:F4629 → L19:F2486, plus L15:F12238 → L17:F4629. All upstream edges into this branch come from the *news* embedding.
- **L20:F8433** ("top news orgs context", pos 26) is fed by the *top* token (via L14:F2781, L17:F11691, L19:F14973) and the report/news features, and is the most direct upstream of the output.
- A separate cluster: **L0:F8964** + **L0:F1069** at pos 1, the "His"-embedding features, are present and carry meaningful direct_effect (≈ +0.088, +0.050 at the L0 level). They contribute to L7:F13646 and L8:F8437 (the "His"→early report-context path contributes direct_effect of ~0.98–1.16 to those features). So the masculine pronoun *does* leak into the chain, but it enters via a feature (L7:F13646) that is more strongly driven by the *report* token (direct_effect 7.2 vs 0.98 for His), so its influence is washed out at L8 and beyond.

**Caveat reducing confidence:** The probe score is INHIBITED by L14:F4420 and L19:F2486 (negative direct_effects), and POSITIVELY pushed by the L0 "His" features. This sign pattern — the most profession-specific features *suppress* the probe, while the pronoun-related features *promote* it — is precisely the signature the user worried about: the gender marker may be acting as a *positive* signal, while the substantive profession evidence is being suppressed. The reported direct_effects are negative for L14:F4420, L19:F2486, L8:F8855, L7:F9092 (inhibitory on the probe), while L0:F8964, L0:F1069, L0:F15693, L0:F2011, L0:F13948, L0:F14287 (His/desire/see context features at layer 0) have positive direct_effects. This polarity mismatch is suspicious and suggests the probe direction may indeed be partially aligned with surface co-occurrence patterns (masculine-pronoun + travel/seeing language) rather than profession semantics. The mechanism is "profession-shaped" in topology but the sign structure partly supports the user's concern.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L20:F8433](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/8433) | 26 | L20:F8433 (top news orgs context) | — | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/8433) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 21 | L19:F2486 (late-context aggregator) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 22 | L19:F2486 (late-context aggregator) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 27 | L19:F2486 (late-context aggregator) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 28 | L19:F2486 (late-context aggregator) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 29 | L19:F2486 (late-context aggregator) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 30 | L19:F2486 (late-context aggregator) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 26 | L19:F2486 (late-context aggregator) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F14973](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/14973) | 26 | L19:F14973 (top-news-orgs concept) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/14973) |
| [L17:F4629](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/4629) | 27 | L17:F4629 (news token feature) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/4629) |
| [L17:F11691](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11691) | 26 | L17:F11691 (top qualifier) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11691) |
| [L15:F12238](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12238) | 27 | L15:F12238 (news word) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12238) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 21 | L14:F4420 (report/journal verb feature) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 22 | L14:F4420 (report/journal verb feature) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 25 | L14:F4420 (report/journal verb feature) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 26 | L14:F4420 (report/journal verb feature) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 27 | L14:F4420 (report/journal verb feature) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 28 | L14:F4420 (report/journal verb feature) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 29 | L14:F4420 (report/journal verb feature) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F2781](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/2781) | 26 | L14:F2781 (top descriptor) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/2781) |
| [L14:F8761](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/8761) | 27 | L14:F8761 (news word) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/8761) |
| [L11:F5996](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/5996) | 21 | L11:F5996 (mid-context) | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/5996) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 21 | L8:F8855 (report-context feature) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 22 | L8:F8855 (report-context feature) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 27 | L8:F8855 (report-context feature) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 21 | L8:F8437 (report-context feature) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 29 | L8:F8437 (report-context feature) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 21 | L7:F13646 (early report/journal concept) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 22 | L7:F13646 (early report/journal concept) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 27 | L7:F13646 (early report/journal concept) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 28 | L7:F13646 (early report/journal concept) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 29 | L7:F13646 (early report/journal concept) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 21 | L7:F9092 (verb-context feature) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 26 | L7:F9092 (verb-context feature) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 28 | L7:F9092 (verb-context feature) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 29 | L7:F9092 (verb-context feature) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 27 | L4:F13253 (news/orgs token feature) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 28 | L4:F13253 (news/orgs token feature) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 29 | L4:F13253 (news/orgs token feature) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L1:F14511](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14511) | 21 | L1:F14511 (early report word-feature) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14511) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 3 | L0:F8444 (preposition 'to' feature) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 20 | L0:F8444 (preposition 'to' feature) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F14287](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14287) | 4 | L0:F14287 (see-word feature) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14287) |
| [L0:F8964](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) | 1 | L0:F8964 (His-pronoun feature) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | L0:F1069 (His-pronoun feature) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F2011](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) | 2 | L0:F2011 (desire-token feature) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) |
| [L0:F13948](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13948) | 2 | L0:F13948 (desire-token feature) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13948) |
| [L0:F15693](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15693) | 2 | L0:F15693 (His/desire) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15693) |
| [L0:F2203](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2203) | 6 | L0:F2203 (world-token feature, INHIB) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2203) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `rank_segment_features` | ❌ This tool requires ctx.sibling_graphs to be set (at least on |
| 3 | `get_top_features` | 15 features; top: L14:4420 de=-0.147 |
| 4 | `get_top_features` | 20 features; top: L14:4420 de=-0.147 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@21` | ❌ error | — | — | Trace the upstream circuit for L14:F4420 at pos 21 ("report"). This is the stron… |
| SA-2 | `L19:F2486@21` | ❌ error | — | — | Trace the upstream circuit for L19:F2486 at pos 21. This feature fires at multip… |
| SA-3 | `L0:F8964@1` | ❌ error | — | — | Trace L0:F8964 at pos 1 ("His"). This is an early-layer feature activating on th… |
| SA-4 | `L0:F8444@3` | ❌ error | — | — | Trace L0:F8444 at pos 3 ("to") and pos 20 ("to"). This is an early-layer feature… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F4420@21, k=10 → Emb:" report"@21 (de=5.22) +9 more |
| 2 | `get_upstream_features` | L19:F2486@21, k=10 → L14:F4420 (de=14.31) +9 more |
| 3 | `get_upstream_features` | L0:F8964@1, k=10 → Emb:"His"@1 (de=13.69) +9 more |
| 4 | `get_upstream_features` | L0:F8444@3, k=10 → Emb:" to"@3 (de=39.50) +9 more |
| 5 | `get_upstream_features` | L8:F8855@21, k=10 → Emb:" report"@21 (de=12.06) +9 more |
| 6 | `get_upstream_features` | L7:F13646@21, k=10 → Emb:" report"@21 (de=7.22) +9 more |
| 7 | `get_upstream_features` | L8:F8437@21, k=10 → Emb:" report"@21 (de=5.75) +9 more |
| 8 | `get_upstream_features` | L0:F14287@4, k=10 → Emb:" see"@4 (de=25.12) +9 more |
| 9 | `get_upstream_features` | L7:F9092@21, k=10 → Emb:" report"@21 (de=-2.34) +9 more |
| 10 | `get_upstream_features` | L11:F5996@21, k=10 → Emb:"<bos>"@0 (de=-2.47) +9 more |
| 11 | `get_upstream_features` | L1:F14511@21, k=10 → Emb:" report"@21 (de=20.62) +9 more |
| 12 | `get_upstream_features` | L19:F2486@29, k=10 → Emb:" news"@27 (de=7.94) +9 more |
| 13 | `get_upstream_features` | L14:F4420@29, k=10 → Emb:" news"@27 (de=4.53) +9 more |
| 14 | `get_upstream_features` | L20:F8433@26, k=10 → Emb:" top"@26 (de=5.72) +9 more |
| 15 | `get_upstream_features` | L0:F2011@2, k=8 → Emb:" desire"@2 (de=12.94) +7 more |
| 16 | `get_upstream_features` | L0:F13948@2, k=8 → Emb:" desire"@2 (de=14.44) +7 more |
| 17 | `get_upstream_features` | L19:F14973@26, k=8 → Emb:" top"@26 (de=7.22) +7 more |
| 18 | `get_upstream_features` | L19:F2486@22, k=8 → L14:F4420 (de=8.44) +7 more |
| 19 | `get_upstream_features` | L0:F2203@6, k=8 → Emb:" world"@6 (de=18.25) +7 more |
| 20 | `get_upstream_features` | L0:F1069@1, k=8 → Emb:"His"@1 (de=21.62) +7 more |
| 21 | `get_upstream_features` | L5:F771@6, k=8 → Emb:" see"@4 (de=6.16) +7 more |
| 22 | `get_upstream_features` | L0:F15693@2, k=8 → Emb:"His"@1 (de=8.69) +7 more |
| 23 | `get_upstream_features` | L14:F2781@26, k=8 → Emb:" top"@26 (de=4.53) +7 more |
| 24 | `get_upstream_features` | L17:F11691@26, k=8 → Emb:" top"@26 (de=8.00) +7 more |
| 25 | `get_upstream_features` | L0:F8444@20, k=8 → Emb:" to"@20 (de=42.25) +7 more |
| 26 | `get_upstream_features` | L19:F2486@27, k=8 → Emb:" news"@27 (de=20.75) +7 more |
| 27 | `get_upstream_features` | L19:F2486@28, k=8 → L14:F4420 (de=8.56) +7 more |
| 28 | `get_upstream_features` | L17:F4629@27, k=8 → Emb:" news"@27 (de=42.50) +7 more |
| 29 | `get_upstream_features` | L4:F13253@28, k=8 → Emb:" news"@27 (de=18.25) +7 more |
| 30 | `get_upstream_features` | L7:F9092@28, k=8 → Emb:" news"@27 (de=10.38) +7 more |
| 31 | `get_upstream_features` | L7:F13646@27, k=8 → Emb:" news"@27 (de=6.31) +7 more |
| 32 | `get_upstream_features` | L15:F12238@27, k=8 → Emb:" news"@27 (de=33.25) +7 more |
| 33 | `get_upstream_features` | L14:F8761@27, k=8 → Emb:" news"@27 (de=13.50) +7 more |

### Build

`build_circuit` → 36 nodes, 53 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 52,795 | 14,935 | 145,605 | 0 | $0.0425 | — | — |
| **Total** | | **52,795** | **14,935** | **145,605** | **0** | **$0.0425** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 29s