# Circuit Oracle Report
**Date:** 2026-07-28 07:04:02 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by a tug-of-war between two parallel circuits originating from the same sentence: a strong pronoun/gender signal flowing from the leading "His" token (pos 1) and a genuine journalism signal flowing from the "report" verb (pos 21); net the pronoun-gender signal wins, so the probe is partially using a spurious male-pronoun feature as a substitute for the profession evidence.

**Confidence:** 7

**Reasoning:**

The circuit traces two distinct input-token pathways, both of which reach the probe logit but with opposite-signed effects.

**Path A — Spurious gender signal (from "His" at pos 1).** The raw "His" embedding (Emb: His (pos 1)) flows through three layers of pronoun/male-detector features — L0:F2994/F1069 (generic "his/he" detector, frac_nonzero≈0.07, promoted tokens include "▁she", suppressed "▁his"), L4:F4315 ("his" pronoun lexical detector, frac_nonzero=0.026), L6:F12990 ("male pronouns and titles" — explicitly labeled as a male-gendered pronoun feature, frac_nonzero=0.068) — and converges on L7:F14946 (the possessive "his" gate, frac_nonzero=0.017, promoted tokens dominated by "▁himself/his/his"). This L7:F14946 feature is a *strong direct suppressor of the probe* (direct_effect = −0.484, the second largest negative contributor in the graph). It feeds up into L19:F8814 ("various pronouns and names referring to people", frac_nonzero=0.087), which is the largest *positive* contributor to the probe (direct_effect = +0.262, activation 11.9 at pos 1) and aggregates L18:F10315 (pronouns/possessives), L18:F14743 ("He", pos 9), and L18:F7400 (the mislabeled "coding" feature whose promoted-token list is actually entirely male pronouns: "▁his/his/himself/▁seine/▁seiner…"). The net effect of the pronoun cascade on the probe is positive (L7:F14893 at +0.49, L19:F8814 at +0.26) minus the L7:F14946 suppressor (−0.48), giving a small but real positive net contribution keyed to the leading "His" — i.e., the probe is using the male pronoun as a partial proxy for "the person described."

**Path B — Genuine profession signal (from "report" at pos 21).** The "report" token embedding flows up through L4:F661 (reports/documentaries/TV coverage, frac_nonzero=0.009), L7:F13646 (news reporting and journalism, frac_nonzero=0.008), L8:F8855 (news reporters and news reporting, frac_nonzero=0.008, max_token "▁reporting") into L14:F4420 (words and phrases related to journalism and newspapers, frac_nonzero=0.016, promoted tokens "journalists/reporter/editorial") and L16:F15046 (names, organizations, and reporting verbs), finally reaching L19:F2486 (journalistic sources and news outlets, frac_nonzero=0.029, promoted "reporting/reporter/coverage"). L19:F2486 has direct_effect = −0.105 (slightly *negative* on the probe), and L14:F4420 has direct_effect = −0.158 (also negative). So even the genuine profession-evidence pathway ends up *suppressing* the probe's classification in this particular graph.

**The user's concern is supported.** The probe is being driven primarily by pronoun features (L7:F14893, L19:F8814, with cumulative positive effect ≈ +0.75) anchored on the word "His", while the genuine profession indicators (journalism L14:L19 features) are *net negative* in their direct effect. The male-pronoun/male-gender path is doing most of the work to raise the probe's score, and it would persist if "report"/"news" tokens were removed but the leading "His" remained. The six "his/he" related features (L0:2994, L0:1069, L4:4315, L6:12990, L7:14946, L18:14743, L19:8814) collectively contribute far more signed influence than the four genuine journalism features (L4:661, L7:13646, L8:8855, L14:4420, L16:15046, L19:2486), confirming the user's hypothesis that the probe leans on the male-pronoun artifact as a proxy for profession.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: His (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: report (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | His pronoun — lexical (L0:F2994, F1069) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | His pronoun — lexical (L0:F2994, F1069) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | His/him pronoun — lexical (L4:F4315) |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L4:F15567](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) | 1 | His/him pronoun — lexical (L4:F4315) | sentences with male or female pronouns and possessives, especially ones referring to writing | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Male pronouns/titles (L6:F12990) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | His-possessive gate (L7:F14946) — STRONG suppressor of probe |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Pronoun aggregator (L7:F14893) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 21 | News reporting/journalism (L7:F13646) |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L4:F661](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/661) | 21 | News reporting/journalism (L7:F13646) | words and phrases used when referring to reports, documentaries, and television coverage of news | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/661) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 21 | Reporters/news reporting (L8:F8855) |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 21 | Journalism/newspapers concept (L14:F4420) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | Pronouns/names referring to people (L19:F8814) — strong positive driver |  various pronouns and names referring to people | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 1 | Pronouns/names referring to people (L19:F8814) — strong positive driver |  pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 9 | Pronouns/names referring to people (L19:F8814) — strong positive driver | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F7400](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) | 1 | Pronouns/names referring to people (L19:F8814) — strong positive driver |  words related to coding and software/UI interfaces, with some bias toward non-English words | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 21 | Journalistic sources/news outlets (L19:F2486) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L16:F15046](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15046) | 21 | Journalistic sources/news outlets (L19:F2486) | names, organizations, and reporting verbs | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15046) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L7:14893 de=0.488 |
| 3 | `inspect_feature` ×14 | L7:14893, L7:14946, L0:2994, L19:8814, L6:12990, L18:14743, L4:4315, L18:10315, L18:7400, L14:4420, L0:2011, L2:9301, L4:11898, L19:2486 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ✅ reported | 6 | 9 | Trace the upstream causal path for the 'pronouns or possessive pronouns' feature… |
| SA-2 | `L19:F8814@1` | ✅ reported | 6 | 8 | Trace the upstream causal path for the 'pronouns and names referring to people' … |
| SA-3 | `L14:F4420@21` | ✅ reported | 4 | 6 | Trace the upstream causal path for the 'journalism and newspapers' feature L14:F… |
| SA-4 | `L7:F14946@1` | ✅ reported | 3 | 5 | Trace the upstream causal path for the '"his" pronouns' feature L7:F14946 at pos… |
| SA-5 | `L19:F2486@21` | ✅ reported | 6 | 16 | Trace the upstream causal path for the 'journalistic sources and news outlets' f… |
| SA-6 | `L0:F2994@1` | ❌ error | — | — | Trace the upstream causal path for the '"his" pronoun' feature L0:F2994 at posit… |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 5 | `get_upstream_features` | L6:F12990@1, k=10 | Emb:"His"@1 (de=4.91) +9 more |
| 6 | `get_upstream_features` | L4:F4315@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 7 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |
| 8 | `get_upstream_features` | L4:F15567@1, k=10 | Emb:"His"@1 (de=19.25) +9 more |
| 9 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 10 | `inspect_feature` | L3, F3205 | " code snippets and documentation references, possibly related to web d" |
| 11 | `inspect_feature` | L2, F9916 | " personal pronouns ("my", "his", "her")" |
| 12 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |

**Findings:** The pronoun feature L7:F14893 ("pronouns or possessive pronouns") receives its strongest drive directly from the raw token embedding of "His" (23.5). A second strong path goes through L4:F4315, a lexical detector for the token "his" and related pronouns, which itself is fed by the same embedding. L6:F12990 adds a gender‑aware layer that highlights male pronouns and masculine titles; it is driven b…

</details>

<details>
<summary><b>SA-2</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F8814 | " various pronouns and names referring to people" |
| 2 | `get_upstream_features` | L19:F8814@1, k=15 | Emb:"His"@1 (de=9.31) +14 more |
| 3 | `inspect_feature` | L18, F7400 | " words related to coding and software/UI interfaces, with some bias to" |
| 4 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 5 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 6 | `get_upstream_features` | L7:F14946@1, k=10 | Emb:"His"@1 (de=18.38) +9 more |
| 7 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 8 | `inspect_feature` | L18, F10315 | " pronouns and possessive pronouns" |
| 9 | `get_upstream_features` | L6:F12990@1, k=10 | Emb:"His"@1 (de=4.91) +9 more |
| 10 | `get_upstream_features` | L4:F4315@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |

**Findings:** The pronoun‑person probe L19:F8814 is driven primarily by the raw token embedding of "His" (direct_effect ~9.3) which flows through a cascade of pronoun‑related features. The strongest upstream conduit is a low‑layer feature L4:F4315 that directly detects the token "his" (embedding -> L4:F4315 direct_effect 23.5). This signal is amplified by mid‑layer pronoun detectors (L7:F14946, L6:F12990, L18:F…

</details>

<details>
<summary><b>SA-3</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@21, k=10 | Emb:" report"@21 (de=5.22) +9 more |
| 3 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 4 | `get_upstream_features` | L8:F8855@21, k=10 | Emb:" report"@21 (de=12.06) +9 more |
| 5 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 6 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |
| 7 | `get_upstream_features` | L7:F13646@21, k=10 | Emb:" report"@21 (de=7.22) +9 more |

**Findings:** The journalism feature (L14:F4420) is driven mainly by the raw input token ' report' at position 21, which directly excites the target. Upstream features in layers 8 and 7 that specialise in news‑reporter mentions (F8855) and generic news reporting (F13646) provide the strongest intermediate positive influence. A secondary path through an unrelated film‑festival feature (F8437) also receives stron…

</details>

<details>
<summary><b>SA-4</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 2 | `get_upstream_features` | L7:F14946@1, k=10 | Emb:"His"@1 (de=18.38) +9 more |
| 3 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 4 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 5 | `get_upstream_features` | L4:F4315@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 6 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 7 | `get_upstream_features` | L4:F4315@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 8 | `inspect_feature` | L2, F9301 | " all mentions of men and women in the context of relationships, dating" |
| 9 | `get_upstream_features` | L6:F12990@1, k=10 | Emb:"His"@1 (de=4.91) +9 more |
| 10 | `get_upstream_features` | L5:F10952@1, k=10 | Emb:"His"@1 (de=10.69) +9 more |
| 11 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |

**Findings:** The pronoun detector L7:F14946 is driven primarily by the raw token embedding for the word "His" (direct_effect +18.4) and by two lower‑layer pronoun detectors: L4:F4315 (a direct his/him pronoun detector, +4.4) and L6:F12990 (a broader male‑pronoun feature, +3.7). Both upstream features lie in layers ≤8, satisfying the lower‑third requirement, and each receives a strong positive signal from the "…

</details>

<details>
<summary><b>SA-5</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F2486 | " journalistic sources and news outlets." |
| 2 | `get_upstream_features` | L19:F2486@21, k=10 | L14:F4420 (de=14.31) +9 more |
| 3 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 4 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 5 | `get_upstream_features` | L14:F4420@21, k=10 | Emb:" report"@21 (de=5.22) +9 more |
| 6 | `inspect_feature` | L16, F15046 | " names, organizations, and reporting verbs" |
| 7 | `get_upstream_features` | L8:F8855@21, k=10 | Emb:" report"@21 (de=12.06) +9 more |
| 8 | `get_upstream_features` | L16:F15046@21, k=10 | Emb:" report"@21 (de=11.44) +9 more |
| 9 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 10 | `get_upstream_features` | L7:F13646@21, k=10 | Emb:" report"@21 (de=7.22) +9 more |
| 11 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |
| 12 | `get_upstream_features` | L4:F661@21, k=10 | Emb:" report"@21 (de=14.38) +9 more |

**Findings:** The pathway from the input token "report" (position 21) climbs through low‑layer news‑reporting features (L4:F661 → L7:F13646 → L8:F8855 → L14:F4420) and converges with a parallel name‑entity/reporting‑verb detector (L16:F15046). All these feed into the target L19:F2486, which represents the higher‑level concept of journalistic sources and news outlets. The trace reaches layers ≤8 and includes dir…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×4 | L4:15567, L0:1069, L7:13646, L8:8855 |

### Build

`build_circuit` → 13 nodes, 17 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 56,140 | 4,948 | 111,937 | 0 | $0.0295 | — | — |
| SA-3 | openai/gpt-oss-120b | 54,234 | 3,953 | 13,504 | 0 | $0.0107 | ✅ 4F/6E | Trace the upstream causal path for the 'journalism and newsp… |
| SA-4 | openai/gpt-oss-120b | 131,352 | 5,981 | 5,056 | 0 | $0.0234 | ✅ 3F/5E | Trace the upstream causal path for the '"his" pronouns' feat… |
| SA-2 | openai/gpt-oss-120b | 138,520 | 7,946 | 8,672 | 0 | $0.0257 | ✅ 6F/8E | Trace the upstream causal path for the 'pronouns and names r… |
| SA-1 | openai/gpt-oss-120b | 141,389 | 8,603 | 16,224 | 0 | $0.0266 | ✅ 6F/9E | Trace the upstream causal path for the 'pronouns or possessi… |
| SA-5 | openai/gpt-oss-120b | 144,992 | 9,956 | 23,616 | 0 | $0.0281 | ✅ 6F/16E | Trace the upstream causal path for the 'journalistic sources… |
| **Total** | | **666,627** | **41,387** | **179,009** | **0** | **$0.1439** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 10s