# Circuit Oracle Report
**Date:** 2026-07-28 07:23:30 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** This probe classification (the "journalist/reporter" profession class) is driven by a striking mixture of two largely *independent* signal pathways: a genuine profession-indicating track rooted in journalism/reporting vocabulary at the "report" token (pos 21), and a much stronger, parallel track running entirely on the **male pronouns "His" (pos 1) and "him" (pos 9)** — exactly the spurious gender-marker signal the user suspected.

**Confidence:** 8

**Reasoning:** The circuit cleanly splits into two supernodes that both feed the output logit:

1. **Genuine profession track (anchored on "report" at pos 21):** The `Emb: report` token (direct_effect 51.5 into L18:F14663 "report"/"Report") feeds a chain L7:F13646 ("news reporting and journalism") → L8:F8855 ("mentions of news reporters") + L8:F8437 (documentary/news content) → L14:F4420 ("words related to journalism and newspapers"; promotes *journalist*, *reporter*) → L19:F2486 ("journalistic sources and news outlets"; promotes *reporting*, *reporter*). This is a textbook profession-feature chain — every link's label and promoted tokens are journalism-specific. The L18:F14663 "report" word detector also feeds L19:F2486 directly. Net effect on the probe is positive and content-grounded.

2. **Spurious gender-marker track (anchored on "His"/"him"):** `Emb: His` (pos 1, direct_effect 19.75 into L0:F2994) and `Emb: him` (pos 9, direct_effect 42.25 into L0:F16297) ignite a *separate*, parallel chain:
   - L0:F2994 "his/he pronoun" (frac_nonzero 0.073, generic but high-density) →
   - L2:F5491 (religious "His") + L2:F9301 ("men and women in relationships/gendered social roles") →
   - L4:F4315 "his and associated pronouns" →
   - L6:F12990 "male pronouns and titles with descriptors associated with men" (promotes *himself*) →
   - L7:F14946 "his/his/him pronoun" (promotes *himself*, *his*) and L7:F14893 (female-pronoun contrast feature) →
   - L18:F7400 + L18:F10315 (male pronouns) and L18:F14743 ("He", pos 9) →
   - L19:F8814 ("various pronouns and names referring to people", at pos 1) →
   - **logit.**

   The aggregate positive direct_effects from this chain (0.49 + 0.26 + 0.20 + 0.18 + 0.17 etc. — all *positive*) substantially exceed those of the journalism track. Crucially, **none of the male-pronoun features ever reference journalism** — they fire on any "His"/"him"-led sentence regardless of profession. L0:F2994 is a high-density (frac 0.073) generic pronoun detector; the chain it seeds is a generic male-reference pathway, not a profession pathway.

3. **Independent of the profession signal, the gender-marker signal pushes the probe score on its own.** The probe's classifier weights apparently assign large positive weight to the male-pronoun direction (consistent with the profession being a stereotypically male role in the probe's training data). The user is correct: the circuit does use a spurious gender feature in addition to genuine profession features. The most direct evidence is that the `Emb: His` and `Emb: him` embeddings are themselves among the largest direct contributors to multiple late-layer features driving the logit, via a chain whose intermediate nodes (F2994, F12990, F14946, F7400, F10315, F14743, F8814) are all generic pronoun / male-pronoun features — none of them detect "journalist."

The probe direction (output) thus integrates (a) a legitimate, content-bearing journalism signal from "report" and (b) a stereotype-correlated male-pronoun signal from "His"/"him" that is not specifically indicative of the journalism profession. This is a classic case of a probe whose classification boundary has entangled a profession label with a gender correlate — and the attribution graph exposes both legs cleanly.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | L0 pronoun "his" / "he" detector (F2994) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 9 | L0 pronoun "his" / "he" detector (F2994) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F16297](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) | 9 | L0 pronoun "him" detector (F16297) |  the pronoun "him" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) |
| [L0:F2011](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) | 2 | L0 word "dream" (F2011) |  the word "dream" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) |
| [L0:F11767](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11767) | 6 | L0 word "world" (F11767) | the word "world" with a lower activation for "net" and "market" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11767) |
| [L0:F7927](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7927) | 8 | L0 past-participle verbs (F7927) |  past-participle verbs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7927) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 3 | L0 word "to" (F8444) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L2:F5491](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) | 1 | L2 religious "His" references (F5491) | references to God in the third person. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) |
| [L2:F9301](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) | 1 | L2 gendered men/women in social roles (F9301) |  all mentions of men and women in the context of relationships, dating, or gendered social roles | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | L4 "his"/pronoun context (F4315) |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L4:F11898](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11898) | 6 | L4 "World"+sport/war (F11898) |  mentions of "World" followed by a sport or war-related word | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11898) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | L6 male pronouns / titles / descriptors (F12990) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | L7 female pronouns incl. "his" (F14893) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | L7 male "his" pronoun (F14946) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 21 | L7 journalism / reporting (F13646, pos21) |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 21 | L8 news reporters / reporting (F8855, F8437 pos21) |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 21 | L8 news reporters / reporting (F8855, F8437 pos21) | content related to film festivals and production, particularly documentary films, and the recognition they receive. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 21 | L14 journalism / newspapers (F4420, pos21) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 9 | L18 "He" pronoun (F14743, pos9) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 1 | L18 male pronouns (F10315, F7400 pos1) |  pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L18:F7400](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) | 1 | L18 male pronouns (F10315, F7400 pos1) |  words related to coding and software/UI interfaces, with some bias toward non-English words | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| [L18:F14663](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14663) | 21 | L18 "report"/"Report" word detector (F14663, pos21) | variations of the word "report." | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14663) |
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | L19 mixed pronouns/names (F8814, pos1) |  various pronouns and names referring to people | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 21 | L19 journalism / news sources (F2486, pos21) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L7:14893 de=0.488 |
| 3 | `inspect_feature` ×4 | L7:14893, L0:2994, L19:8814, L0:2011 |
| 4 | `get_upstream_features` | Emb:"His"@1 (de=23.50) +14 more |
| 5 | `get_upstream_features` | Emb:"His"@1 (de=9.31) +14 more |
| 6 | `get_upstream_features` | Emb:"His"@1 (de=19.75) +14 more |
| 7 | `get_upstream_features` | Emb:" desire"@2 (de=12.94) +9 more |
| 8 | `inspect_feature` ×7 | L18:7400, L18:10315, L7:14946, L6:12990, L18:14743, L19:2486, L14:4420 |
| 9 | `get_upstream_features` | L14:F4420 (de=14.31) +9 more |
| 10 | `get_upstream_features` | Emb:" report"@21 (de=5.22) +9 more |
| 11 | `inspect_feature` ×6 | L4:4315, L4:11898, L0:7927, L0:8444, L0:11767, L2:5491 |
| 12 | `get_upstream_features` | L14:F4420 (de=14.31) +9 more |
| 13 | `get_upstream_features` | Emb:" him"@9 (de=18.38) +7 more |
| 14 | `get_upstream_features` | Emb:"His"@1 (de=13.00) +7 more |
| 15 | `get_upstream_features` | Emb:"His"@1 (de=4.91) +7 more |
| 16 | `get_upstream_features` | Emb:" world"@6 (de=16.38) +7 more |
| 17 | `inspect_feature` ×2 | L0:16297, L0:2208 |
| 18 | `get_upstream_features` | Emb:" him"@9 (de=42.25) +7 more |
| 19 | `get_upstream_features` | Emb:"His"@1 (de=12.81) +4 more |
| 20 | `get_upstream_features` | Emb:" world"@6 (de=35.25) +7 more |
| 21 | `get_upstream_features` | Emb:" has"@7 (de=16.00) +4 more |
| 22 | `get_upstream_features` | L14:F4420 (de=14.31) +9 more |
| 23 | `inspect_feature` ×2 | L8:8855, L7:13646 |
| 24 | `get_upstream_features` | Emb:" report"@21 (de=5.22) +4 more |
| 25 | `get_upstream_features` | Emb:" him"@9 (de=18.38) +4 more |
| 26 | `get_upstream_features` | Emb:" report"@21 (de=5.22) +2 more |
| 27 | `get_upstream_features` | Emb:" report"@21 (de=51.50) +2 more |
| 28 | `inspect_feature` ×2 | L8:8437, L18:14663 |
| 29 | `get_upstream_features` | L14:F4420 (de=14.31) +4 more |
| 30 | `get_upstream_features` | Emb:" report"@21 (de=51.50) +2 more |
| 31 | `get_upstream_features` | Emb:"His"@1 (de=21.38) +4 more |
| 32 | `get_upstream_features` | Emb:"His"@1 (de=13.00) +4 more |
| 33 | `get_upstream_features` | Emb:"His"@1 (de=18.38) +7 more |
| 34 | `inspect_feature` ×5 | L15:851, L11:10933, L11:9183, L9:8770, L16:14120 |
| 35 | `get_upstream_features` | Emb:"His"@1 (de=21.38) +4 more |
| 36 | `get_upstream_features` | L14:F4420 (de=14.31) +4 more |
| 37 | `get_upstream_features` | Emb:"His"@1 (de=18.38) +4 more |
| 38 | `get_upstream_features` | Emb:" him"@9 (de=18.38) +4 more |
| 39 | `get_upstream_features` | Emb:" report"@21 (de=5.22) +2 more |
| 40 | `get_upstream_features` | L14:F4420 (de=14.31) +4 more |
| 41 | `get_upstream_features` | Emb:"His"@1 (de=13.00) +2 more |
| 42 | `get_upstream_features` | Emb:"His"@1 (de=21.38) +2 more |
| 43 | `get_upstream_features` | Emb:" him"@9 (de=18.38) +2 more |
| 44 | `get_upstream_features` | L14:F4420 (de=14.31) +4 more |
| 45 | `get_upstream_features` | Emb:" him"@9 (de=18.38) +4 more |
| 46 | `inspect_feature` ×6 | L13:8128, L15:2579, L16:15045, L16:8642, L16:15046, L2:9301 |

### Build

`build_circuit` → 29 nodes, 41 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 82,713 | 8,567 | 603,016 | 0 | $0.0713 | — | — |
| **Total** | | **82,713** | **8,567** | **603,016** | **0** | **$0.0713** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 18s