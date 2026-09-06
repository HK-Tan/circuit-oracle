# Circuit Oracle Report
**Date:** 2026-07-28 07:20:52 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's positive classification score is driven by **two parallel, largely independent pathways** — a dominant **gender-marker pathway** (anchored on the pronoun "His" at position 1 and "him" at position 9) and a weaker, genuine **journalism-vocabulary pathway** (anchored on "report" at position 21) — and the user's concern is well-founded: the gendered-pronoun pathway contributes substantially more signed effect than the profession pathway.

**Confidence:** 7/10

**Reasoning:**

Reading the `get_top_features` ranking for the probe direction, the top positive contributors are pronoun features:
- **L7:F14893** (pronouns/possessives, direct_effect +0.488, frac_nonzero 0.009) — promoted tokens include *herself, she*; suppressed *himself, his*. This is a feminine-leaning pronoun feature, but the embedding for "His" at pos 1 has direct_effect ≈ 23.5 into it (per the subagent trace), and it's amplified by L6:F12990 ("male pronouns and titles," direct_effect +5.59) and L4:F4315 ("mentions of 'his'," direct_effect +4.41). The chain L0:F2994 / F1069 ("his"/"He") → L4 → L6 → L7 is a cascade of male-pronoun detectors that fire on the "His" token.
- **L19:F8814** (mixed pronouns/names, direct_effect +0.262) — receives direct excitation from the "His" embedding (9.31), the L7 pronoun pair, and L18:F10315/F7400 (both pronoun detectors). It is genuinely a pronoun/name integrator, not a profession feature.
- **L18:F14743** ("He" emphatic at pos 9, direct_effect +0.207, but pos 9 is "him", so it fires via the "him" embedding direct_effect 18.4 plus L0:F16297 "him" detector direct_effect 6.9). Promoted tokens are *himself, Himself*; suppressed *she, her*. This is also pure gender.

The genuinely profession-related features are present but smaller and partially **inhibitory**:
- **L14:F4420** ("words related to journalism and newspapers," direct_effect −0.158 *on the probe*, despite firing strongly at pos 21 on "report"). It is driven by the "report" embedding (5.22) and by L8:F8855 ("news reporters and news reporting," promoted *reporter, journalist*) and L7:F13646 ("news reporting and journalism"). These *do* form a clean profession pathway — embedding(pos 21 = "report") → L7:F13646 → L8:F8855 → L11:F5996 → L14:F4420.
- **L19:F2486** ("journalistic sources and news outlets," direct_effect −0.105) — also a real journalism feature at pos 21, but pushing *against* the probe score.
- **L16:F8642** (legal/official reporting, direct_effect −4.84 on L14:F4420, also negative on the probe) — actively suppresses the journalism path.

So the "report" profession indicator exists and traces cleanly to embedding(pos 21), but it is net-negative on the probe, while the pronoun cascade from "His" (pos 1) and "him" (pos 9) is net-positive and stronger. The probe's "journalist" classification is being driven more by the male pronoun markers at the start of the sentence than by the profession vocabulary at the end. This is a clear case of a spurious feature (gender) outweighing the genuine profession indicator in the linear probe — consistent with the user's concern. The classification would be vulnerable to a counterfactual where "His" → "Her" (which would flip L7:F14893, L18:F10315, L19:F8814, etc.) while leaving "report for some of the top news organizations" untouched.

The circuit reaches L0/L2/L4 features but the deepest dependencies land on layer-0 pronoun detectors (F2994, F1069, F16297) whose own upstream is the "His"/"him"/"desire" embeddings — i.e., the gender signal is grounded in the literal pronoun tokens, not in any profession context.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: His (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: him (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: report (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: desire (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: world (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | L0 pronouns: 'his'/'he' detectors | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | L0 pronouns: 'his'/'he' detectors |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F2011](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) | 2 | L0 pronouns: 'his'/'he' detectors |  the word "dream" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) |
| [L0:F16297](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) | 9 | L0 pronouns: 'his'/'he' detectors |  the pronoun "him" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | L4 pronoun detector (his/he/him) |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L4:F11898](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11898) | 6 | L4 pronoun detector (his/he/him) |  mentions of "World" followed by a sport or war-related word | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11898) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | L6 male pronouns/titles (descriptor) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | L7 'His' pronoun feature (pos 1) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | L7 'His' pronoun feature (pos 1) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 21 | L7–L8 journalism/reporter features (pos 21) |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 21 | L7–L8 journalism/reporter features (pos 21) |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 21 | L7–L8 journalism/reporter features (pos 21) | content related to film festivals and production, particularly documentary films, and the recognition they receive. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 1 | L18 pronoun/possessive 'his/his' (pos 1) |  pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L18:F7400](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) | 1 | L18 pronoun/possessive 'his/his' (pos 1) |  words related to coding and software/UI interfaces, with some bias toward non-English words | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 9 | L18 'He' emphatic (pos 9) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 21 | L14 journalism/newspapers (pos 21) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L16:F8642](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/8642) | 21 | L14 journalism/newspapers (pos 21) |  text related to official reporting and legal issues. | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/8642) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 21 | L14 journalism/newspapers (pos 21) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | L19 mixed pronouns+names (pos 1) |  various pronouns and names referring to people | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L7:14893 de=0.488 |
| 3 | `inspect_feature` ×6 | L7:14893, L7:14946, L6:12990, L0:2994, L19:8814, L18:14743 |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ✅ reported | 10 | 9 | Trace L7:F14893 (pronouns/possessives feature, fires at pos 1='His') upstream. F… |
| SA-2 | `L19:F8814@1` | ❌ error | — | — | Trace L19:F8814 (pronouns-and-names feature) upstream. We want to know if this l… |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `get_upstream_features` | L6:F12990@1, k=10 | Emb:"His"@1 (de=4.91) +9 more |
| 5 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 6 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |
| 7 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 8 | `get_upstream_features` | L4:F4315@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 9 | `inspect_feature` | L2, F9301 | " all mentions of men and women in the context of relationships, dating" |
| 10 | `get_upstream_features` | L4:F15567@1, k=15 | Emb:"His"@1 (de=19.25) +14 more |
| 11 | `inspect_feature` | L2, F9916 | " personal pronouns ("my", "his", "her")" |
| 12 | `inspect_feature` | L2, F9233 | " the pronouns "she" and "he"" |

**Findings:** The target feature L7:F14893 (pronoun/possessive detector) is overwhelmingly driven by the input token embedding for "His" at position 1 (direct_effect≈23.5). The strongest upstream transformer features are L6:F12990 and L4:F4315, both pronoun‑specific detectors that amplify the signal. The next‑level driver is L4:F15567, a feature that combines pronoun detection with a bias toward writing‑related…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×4 | L18:10315, L18:7400, L0:2011, L14:4420 |
| 2 | `get_upstream_features` | L14:F4420@21, k=8 → Emb:" report"@21 (de=5.22) +7 more |
| 3 | `get_upstream_features` | L18:F14743@9, k=8 → Emb:" him"@9 (de=18.38) +7 more |
| 4 | `get_upstream_features` | L18:F10315@1, k=8 → Emb:"His"@1 (de=21.38) +7 more |
| 5 | `get_upstream_features` | L19:F8814@1, k=8 → Emb:"His"@1 (de=9.31) +7 more |
| 6 | `get_upstream_features` | L0:F2011@2, k=8 → Emb:" desire"@2 (de=12.94) +7 more |
| 7 | `get_upstream_features` | L0:F2994@1, k=8 → Emb:"His"@1 (de=19.75) +7 more |
| 8 | `get_upstream_features` | L8:F8855@21, k=5 → Emb:" report"@21 (de=12.06) +4 more |
| 9 | `inspect_feature` ×3 | L8:8855, L7:13646, L0:16297 |
| 10 | `get_upstream_features` | L19:F2486@21, k=5 → L14:F4420 (de=14.31) +4 more |
| 11 | `inspect_feature` ×3 | L4:11898, L2:9301, L4:4315 |
| 12 | `get_upstream_features` | L7:F13646@21, k=5 → Emb:" report"@21 (de=7.22) +4 more |
| 13 | `get_upstream_features` | L11:F5996@21, k=5 → Emb:"<bos>"@0 (de=-2.47) +4 more |
| 14 | `get_upstream_features` | L0:F16297@9, k=5 → Emb:" him"@9 (de=42.25) +4 more |
| 15 | `get_upstream_features` | L11:F389@1, k=5 → L10:F12232 (de=-20.12) +4 more |
| 16 | `get_upstream_features` | L11:F9183@1, k=5 → L10:F14174 (de=13.88) +4 more |
| 17 | `get_upstream_features` | L9:F8770@1, k=5 → L7:F462 (de=15.00) +4 more |
| 18 | `inspect_feature` ×10 | L7:462, L7:5741, L10:7106, L10:14174, L11:10933, L10:12232, L0:1069, L19:2486, L16:8642, L8:8437 |

### Build

`build_circuit` → 15 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 66,071 | 5,665 | 182,632 | 0 | $0.0376 | — | — |
| SA-1 | openai/gpt-oss-120b | 202,333 | 7,848 | 0 | 0 | $0.0351 | ✅ 10F/9E | Trace L7:F14893 (pronouns/possessives feature, fires at pos … |
| **Total** | | **268,404** | **13,513** | **182,632** | **0** | **$0.0726** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 34s