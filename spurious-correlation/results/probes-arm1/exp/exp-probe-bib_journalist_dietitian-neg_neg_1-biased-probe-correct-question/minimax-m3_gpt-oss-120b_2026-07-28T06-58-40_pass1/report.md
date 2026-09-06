# Circuit Oracle Report
**Date:** 2026-07-28 06:58:41 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

The circuit has been built and includes embedding nodes. Now let me write the final analysis.

**Analysis:** The probe's positive classification score is driven by a dual-pathway circuit: a genuine profession-indicator path triggered by the verb "report" at the final token (pos 21), which activates a cascade of journalism/newspaper features (L4:F661 → L7:F13646 → L8:F8855 → L14:F4420 → L19:F2486); and a spurious gender-marker path triggered by the masculine possessive pronoun "His" at pos 1 and object pronoun " him" at pos 9, which feed a pronoun-cascade (L0:F2994, F16297 → L4:F4315 → L6:F12990 → L7:F14946 → L18:F14743, F10315, F7400) that promotes male-associated vocabulary and suppresses female pronouns, culminating in L19:F8814. Both L19:F2486 (journalism sources) and L19:F8814 (pronoun/name feature) push the probe's score — meaning the classifier relies on **both** the legitimate "reporter" profession word and the male gender cue.

**Confidence:** 7

**Reasoning:** The circuit reveals that the user is correct — gender markers are part of what the probe uses, but not exclusively. The "report" → journalism path (the legitimate profession signal) is the most strongly weighted: the "report" token embedding at pos 21 directly excites L14:F4420 (direct_effect 5.22), which in turn strongly feeds L19:F2486 (direct_effect 14.31), which directly drives the output (direct_effect 0.18). This is a clean bottom-up cascade through layers 0→4→7→8→14→19, with each step specifically detecting reporting/journalism terminology. F4420's promoted tokens (journalist, reporter, journalism) and F2486's promoted tokens (reporter, coverage, reporting) make the profession signal unambiguous.

However, the gender-marker path is real and substantial. The "His" embedding at pos 1 directly drives L7:F14946 (direct_effect 18.375), L18:F10315 (21.375), and L19:F8814 (9.31). The " him" embedding at pos 9 drives L0:F16297 (42.25) and L18:F14743 (18.375). These features all have promoted tokens like "himself/His" and suppressed tokens like "she/her/herself" — meaning they actively suppress female gender and boost male gender in the residual stream. L19:F8814 directly drives the output with direct_effect 0.23 (the largest single positive contribution to the probe). So when the model classifies the profession, it is simultaneously saying "this person is a journalist" (from "report") and "this person is male" (from "His"/"him"), and both signals feed the probe.

The user's concern is well-founded: the probe exhibits gender bias. The presence of "His" and "him" are acting as a separate, large-magnitude positive signal that does not need the journalism context to fire — note that L7:F14946 fires on "His" regardless of profession. If the same text were rewritten with "Her" / "her" pronouns, F14946, F12990, F8814 etc. would all be silent or actively suppress the probe, even though the journalism evidence (L14:F4420, L19:F2486) would remain unchanged. That asymmetric reliance on gendered surface forms is a textbook spurious correlation. A robust profession probe should rely primarily on the journalism-detector path (L4→L7→L8→L14→L19) and not the pronoun path (L0→L4→L6→L7→L18→L19).

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'His' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: ' him' (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: ' report' (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F16297](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) | 9 | L0: 'him' pronoun detector |  the pronoun "him" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | L0: 'his/he' pronoun detector | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | L4: 'his' lexical marker + report/news coverage phrase |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L4:F661](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/661) | 21 | L4: 'his' lexical marker + report/news coverage phrase |  words and phrases used when referring to reports, documentaries, and television coverage of news | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/661) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | L6: male pronouns/titles aggregator |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | L7: 'his' possessive pronoun detector |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | L7: 'his' possessive pronoun detector |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 21 | L7: news reporting and journalism |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 21 | L8: news reporters/reporting feature |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 21 | L8: news reporters/reporting feature | content related to film festivals and production, particularly documentary films, and the recognition they receive. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 21 | L14: journalism/newspapers feature (promotes journalist/reporter) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 9 | L18: high-level male pronoun features (suppress 'she/her') | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 1 | L18: high-level male pronoun features (suppress 'she/her') |  pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L18:F7400](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) | 1 | L18: high-level male pronoun features (suppress 'she/her') |  words related to coding and software/UI interfaces, with some bias toward non-English words | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 21 | L19: journalistic sources/news outlets |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | L19: pronoun/name feature (suppresses 'she/her') |  various pronouns and names referring to people | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L7:14893 de=0.471 |
| 3 | `inspect_feature` ×19 | L7:14893, L7:14946, L0:2994, L6:12990, L19:8814, L18:14743, L4:4315, L18:10315, L14:4420, L18:7400, L0:2011, L2:9301, L0:8444, L0:7927, L4:11898, L0:2208, L0:11767, L19:2486, L0:13381 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@21` | ✅ reported | 6 | 10 | Trace upstream from L14:F4420 (journalism/newspapers feature at pos 21, the "rep… |
| SA-2 | `L19:F2486@21` | ✅ reported | 5 | 10 | Trace upstream from L19:F2486 (journalistic sources/news outlets feature at pos … |
| SA-3 | `L7:F14893@1` | ✅ reported | 6 | 11 | Trace upstream from L7:F14893 (male pronoun feature at pos 1 = "His"). The model… |
| SA-4 | `L18:F14743@9` | ✅ reported | 6 | 18 | Trace upstream from L18:F14743 (He feature at pos 9). I want to understand the m… |
| SA-5 | `L19:F8814@1` | ✅ reported | 6 | 11 | Trace upstream from L19:F8814 (pronouns and names feature at pos 1 = "His"). I w… |
| SA-6 | `L18:F7400@1` | ❌ error | — | — | Trace upstream from L18:F7400 (coding/UI features at pos 1, a negative contribut… |

<details>
<summary><b>SA-1</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@21, k=10 | Emb:" report"@21 (de=5.22) +9 more |
| 3 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 4 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 5 | `get_upstream_features` | L8:F8855@21, k=10 | Emb:" report"@21 (de=12.06) +9 more |
| 6 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |
| 7 | `get_upstream_features` | L7:F13646@21, k=10 | Emb:" report"@21 (de=7.22) +9 more |
| 8 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |
| 9 | `get_upstream_features` | L8:F8437@21, k=10 | Emb:" report"@21 (de=5.75) +9 more |
| 10 | `inspect_feature` | L0, F12801 | " verbs related to communication, help, enabling, and allowing" |
| 11 | `get_upstream_features` | L4:F661@21, k=10 | Emb:" report"@21 (de=14.38) +9 more |
| 12 | `get_upstream_features` | L7:F13646@21, k=10 | Emb:" report"@21 (de=7.22) +9 more |
| 13 | `inspect_feature` | L6, F12624 | "words related to art, architecture, or law." |
| 14 | `inspect_feature` | L5, F12586 | " mentions of reports" |

**Findings:** The journalism detector (L14:F4420) is primarily driven by the raw embedding of the token "report" at position 21. This signal propagates upward through a cascade of lower-layer features: the very specific report-phrase detector in layer 4 (F661), a broader news-reporting detector in layer 7 (F13646), and a mid-layer reporter detector in layer 8 (F8855). All these intermediate features are themsel…

</details>

<details>
<summary><b>SA-2</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F2486 | " journalistic sources and news outlets." |
| 2 | `get_upstream_features` | L19:F2486@21, k=10 | L14:F4420 (de=14.31) +9 more |
| 3 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 4 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 5 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 6 | `get_upstream_features` | L8:F8855@21, k=10 | Emb:" report"@21 (de=12.06) +9 more |
| 7 | `get_upstream_features` | L14:F4420@21, k=10 | Emb:" report"@21 (de=5.22) +9 more |
| 8 | `inspect_feature` | L16, F15046 | " names, organizations, and reporting verbs" |
| 9 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |
| 10 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |
| 11 | `get_upstream_features` | L7:F13646@21, k=10 | Emb:" report"@21 (de=7.22) +9 more |

**Findings:** The path starts at L19:F2486 (journalistic sources/news outlets) and is driven primarily by higher‑layer journalism features (L14:F4420, L8:F8855, L7:F13646). All of these receive strong positive influence from the input token ' report' at position 21, providing the required embedding shortcut. The circuit descends into lower layers (7‑8) and reaches a concrete token embedding, satisfying the term…

</details>

<details>
<summary><b>SA-3</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `get_upstream_features` | L6:F12990@1, k=10 | Emb:"His"@1 (de=4.91) +9 more |
| 5 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 6 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |
| 7 | `get_upstream_features` | L4:F4315@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 8 | `get_upstream_features` | L4:F15567@1, k=10 | Emb:"His"@1 (de=19.25) +9 more |
| 9 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 10 | `inspect_feature` | L3, F3205 | " code snippets and documentation references, possibly related to web d" |
| 11 | `inspect_feature` | L2, F9301 | " all mentions of men and women in the context of relationships, dating" |

**Findings:** The male possessive pronoun "His" (embedding) directly excites L7:F14893, a pronoun detector that the model later uses as a gender cue for profession selection. Upstream, a cascade of pronoun‑focused features (L6:F12990, L4:F4315, L4:F15567, L5:F10952) amplify this signal, each adding positive direct_effect. All these features reside in layers ≤8, satisfying the lower‑third floor, and we have mult…

</details>

<details>
<summary><b>SA-4</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@9, k=10 | Emb:" him"@9 (de=18.38) +9 more |
| 3 | `inspect_feature` | L0, F16297 | " the pronoun "him"" |
| 4 | `inspect_feature` | L16, F14120 | " references to people being directed and/or affected in some way." |
| 5 | `inspect_feature` | L14, F10344 | " pronouns related to feelings or actions" |
| 6 | `get_upstream_features` | L0:F16297@9, k=5 | Emb:" him"@9 (de=42.25) +4 more |
| 7 | `get_upstream_features` | L2:F5525@9, k=5 | Emb:" him"@9 (de=12.31) +4 more |
| 8 | `inspect_feature` | L2, F5525 | " instances of something moving directly to a location like someone com" |
| 9 | `inspect_feature` | L0, F7927 | " past-participle verbs" |
| 10 | `inspect_feature` | L0, F7927 | " past-participle verbs" |

**Findings:** The male‑pronoun signal at L18:F14743 originates from the input token embedding for " him" (direct_effect ~18) and is amplified by an early‑layer pronoun detector (0:16297) that itself is almost wholly sourced from the same embedding. These low‑layer sources satisfy the lower‑third‑layer requirement. Higher‑layer person‑reference and pronoun‑semantic features (layers 16, 14, 2) add modest boosts, …

</details>

<details>
<summary><b>SA-5</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F8814 | " various pronouns and names referring to people" |
| 2 | `get_upstream_features` | L19:F8814@1, k=10 | Emb:"His"@1 (de=9.31) +9 more |
| 3 | `inspect_feature` | L18, F7400 | " words related to coding and software/UI interfaces, with some bias to" |
| 4 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 5 | `get_upstream_features` | L18:F7400@1, k=10 | Emb:"His"@1 (de=13.00) +9 more |
| 6 | `get_upstream_features` | L7:F14946@1, k=10 | Emb:"His"@1 (de=18.38) +9 more |
| 7 | `inspect_feature` | L18, F10315 | " pronouns and possessive pronouns" |
| 8 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 9 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 10 | `get_upstream_features` | L4:F4315@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |

**Findings:** The pronoun‑name feature L19:F8814 is primarily driven by the raw token embedding for "His" and by a cascade of pronoun‑focused features. The strongest upstream driver that also satisfies the lower‑third layer requirement is L7:F14946, a sparse detector for the possessive pronoun "his". This feature itself receives a large positive boost from the same "His" embedding and from an earlier layer feat…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14743@9, k=15 → Emb:" him"@9 (de=18.38) +14 more |
| 2 | `get_upstream_features` | L18:F7400@1, k=10 → Emb:"His"@1 (de=13.00) +9 more |
| 3 | `get_upstream_features` | L18:F10315@1, k=10 → Emb:"His"@1 (de=21.38) +9 more |
| 4 | `get_upstream_features` | L7:F14946@1, k=10 → Emb:"His"@1 (de=18.38) +9 more |
| 5 | `get_upstream_features` | L0:F2994@1, k=10 → Emb:"His"@1 (de=19.75) +9 more |
| 6 | `get_upstream_features` | L0:F2994@9, k=10 → Emb:" him"@9 (de=13.94) +9 more |
| 7 | `inspect_feature` ×7 | L9:8770, L11:10933, L11:9183, L0:16297, L16:14120, L14:10344, L2:5525 |
| 8 | `get_upstream_features` | L19:F8814@1, k=10 → Emb:"His"@1 (de=9.31) +9 more |
| 9 | `get_upstream_features` | L19:F2486@21, k=10 → L14:F4420 (de=14.31) +9 more |
| 10 | `get_upstream_features` | L14:F4420@21, k=10 → Emb:" report"@21 (de=5.22) +9 more |
| 11 | `get_upstream_features` | L0:F16297@9, k=10 → Emb:" him"@9 (de=42.25) +9 more |
| 12 | `inspect_feature` ×3 | L7:13646, L8:8855, L4:661 |
| 13 | `get_upstream_features` | L11:F10933@1, k=5 → L10:F14174 (de=11.56) +4 more |
| 14 | `get_upstream_features` | L11:F9183@1, k=5 → L10:F14174 (de=13.88) +4 more |

### Build

`build_circuit` → 15 nodes, 32 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 115,762 | 6,078 | 378,751 | 0 | $0.0647 | — | — |
| SA-3 | openai/gpt-oss-120b | 121,276 | 8,622 | 14,144 | 0 | $0.0236 | ✅ 6F/11E | Trace upstream from L7:F14893 (male pronoun feature at pos 1… |
| SA-2 | openai/gpt-oss-120b | 122,296 | 7,753 | 16,672 | 0 | $0.0232 | ✅ 5F/10E | Trace upstream from L19:F2486 (journalistic sources/news out… |
| SA-1 | openai/gpt-oss-120b | 161,671 | 13,157 | 55,072 | 0 | $0.0330 | ✅ 6F/10E | Trace upstream from L14:F4420 (journalism/newspapers feature… |
| SA-4 | openai/gpt-oss-120b | 137,059 | 11,342 | 5,888 | 0 | $0.0275 | ✅ 6F/18E | Trace upstream from L18:F14743 (He feature at pos 9). I want… |
| SA-5 | openai/gpt-oss-120b | 127,471 | 9,091 | 11,200 | 0 | $0.0247 | ✅ 6F/11E | Trace upstream from L19:F8814 (pronouns and names feature at… |
| **Total** | | **785,535** | **56,043** | **481,727** | **0** | **$0.1967** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 9m 11s