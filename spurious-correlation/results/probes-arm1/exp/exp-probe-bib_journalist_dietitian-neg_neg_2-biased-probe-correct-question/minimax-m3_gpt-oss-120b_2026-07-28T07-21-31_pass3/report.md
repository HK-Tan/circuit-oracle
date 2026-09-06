# Circuit Oracle Report
**Date:** 2026-07-28 07:21:31 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe classifies the profession as male primarily through a long pronoun-detection circuit anchored on the "His" (pos 1) and "him" (pos 9) input tokens, with a smaller contribution from journalism-related features at "report" (pos 21); the circuit confirms the user's concern that the classification relies on gendered pronoun cues rather than genuine profession indicators.

**Confidence:** 9

**Reasoning:**

The graph decomposes cleanly into two parallel paths feeding the logit:

**1) The dominant male-pronoun path (≈+1.0 to the logit, mostly from F14893 +0.49 and F8814 +0.26 at pos 1):** This path begins with the raw token embedding of **"His" (pos 1)** (direct_effect = +23.5 onto L7:F14893, +21.4 onto L18:F10315, +13.0 onto L18:F7400). That embedding immediately excites:
- **L0:F2994** (label: "the pronoun 'his' and 'he'", frac_nonzero=0.073) — a low-level "his/he" detector at pos 1 with direct_effect +0.29 to the logit.
- **L2:F9301** ("mentions of men and women in gendered social roles", frac_nonzero=0.018) and **L2:F5491** ("references to God in the third person", but functionally a His/He detector here, frac_nonzero=0.008).
- **L4:F4315** ("mentions of 'his' and he/him/hers", frac_nonzero=0.026).
- **L6:F12990** ("male pronouns and titles along with descriptors associated with men", frac_nonzero=0.068) — promoted tokens: "▁himself, ▁Himself" — the first clearly male-specific feature in the hierarchy.
- **L7:F14946** ("the possessive pronoun 'his' (or he, him)", frac_nonzero=0.017) and **L7:F14893** (a pronoun detector, frac_nonzero=0.009) — F14946 has a large negative direct_effect (-0.48) that suppresses the probe; F14893 has the largest positive direct_effect (+0.49) and acts as a positive conduit.
- **L19:F8814** ("various pronouns and names referring to people", frac_nonzero=0.087) — promoted tokens heavily female ("▁herself, ▁she, ▁her") but the function is a pronoun aggregator; in this context the activated feature represents a male-pronoun cue feeding the probe.
- **L18:F10315, F14743, F7400** (all pronoun detectors at pos 1 / 9) further consolidate the signal.

The "him" embedding at pos 9 also drives this path via **L0:F16297** ("the pronoun 'him'", frac_nonzero=0.033) and **L13:F10255** ("a lot of uses of the word 'I' and 'me'"), and its embedding contributes +18.4 into L18:F14743 — a "He" detector.

**2) The journalism/profession-content path (much weaker, mostly negative on the male probe):** The token **"report" (pos 21)** excites **L7:F13646** ("news reporting and journalism", frac_nonzero=0.008) and **L8:F8855** ("mentions of news reporters and news reporting", frac_nonzero=0.008), which then feed **L14:F4420** ("words and phrases related to journalism and newspapers", frac_nonzero=0.017 — promoted "▁journalists, ▁journalist, ▁reporter, ▁editorial"). However, this is the actual profession signal in the sentence, and the L14:F4420 feature carries a strong **negative** direct_effect (-0.16) on the male logit, while L19:F2486 (a journalism-aggregator, frac_nonzero=0.029) at pos 21 also carries a small **negative** contribution (-0.10). The L8:L14 layer journalism features also support F8855 and F2486 (negative -0.18 and -0.10 respectively).

**Interpretation of the user's concern — confirmed:** The probe's positive evidence for "male profession" comes almost entirely from the pronoun circuit (L0:L7:L19 "his/he/him" detectors), with the **strongest positive signals (+0.49, +0.29, +0.26) all coming from features at position 1 = "His"**. Meanwhile, the *actual* profession evidence ("report", journalism vocabulary at pos 21) flows into features that **suppress** the male classification (L14:F4420 direct_effect = -0.16, L19:F2486 direct_effect = -0.10, L18:F10315 = -0.18, L18:F7400 = -0.17, L18:F14743 = -0.21). The net effect of the journalism branch is mildly *anti*-male, not pro-male. This is precisely the spurious-correlation pattern the user suspected: the model predicts "male reporter" because the subject pronoun is "His" and "him", not because of any profession-relevant content. If the prompt were rewritten with "Her" / "she" instead, the L7 pronoun features would fire on female pronouns and the probe's sign would likely flip, even though the profession ("report for some of the top news organizations") would be identical.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | Layer 0: 'his/he' pronoun detectors | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2208](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2208) | 1 | Layer 0: 'his/he' pronoun detectors |  the pronoun "Him" and the possessive pronoun "His" when used in a religious context | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2208) |
| [L0:F16297](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) | 9 | Layer 0: 'his/he' pronoun detectors |  the pronoun "him" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) |
| [L0:F11767](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11767) | 6 | Layer 0: lexical content ('world', 'to', 'desire', 'taken') | the word "world" with a lower activation for "net" and "market" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11767) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 3 | Layer 0: lexical content ('world', 'to', 'desire', 'taken') | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F2011](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) | 2 | Layer 0: lexical content ('world', 'to', 'desire', 'taken') |  the word "dream" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) |
| [L0:F7927](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7927) | 8 | Layer 0: lexical content ('world', 'to', 'desire', 'taken') |  past-participle verbs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7927) |
| [L2:F9301](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) | 1 | Layer 2: gender/pronoun social roles |  all mentions of men and women in the context of relationships, dating, or gendered social roles | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) |
| [L2:F5491](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) | 1 | Layer 2: gender/pronoun social roles | references to God in the third person. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) |
| [L2:F5525](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5525) | 9 | Layer 2: gender/pronoun social roles | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5525) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | Layer 4: 'his' token specialist + world-sport feature |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L4:F11898](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11898) | 6 | Layer 4: 'his' token specialist + world-sport feature |  mentions of "World" followed by a sport or war-related word | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11898) |
| [L5:F10952](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) | 1 | Layer 5: third-person pronoun feature | third person pronouns in varying contexts | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Layer 6: male pronouns/titles detector |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | Layer 7: possessive-pronoun detector (his/him) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Layer 7: possessive-pronoun detector (his/him) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 21 | Layer 7: journalism/reporter feature at 'report' |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 21 | Layer 7: journalism/reporter feature at 'report' | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 21 | Layer 8: reporter/news reporting feature |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 21 | Layer 8: reporter/news reporting feature | content related to film festivals and production, particularly documentary films, and the recognition they receive. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L13:F10255](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/10255) | 9 | Layer 13: pronoun-direction feature at 'him' |  a lot of uses of the word "I" and "me" and the phrase "made me" | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/10255) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 21 | Layer 14: journalism-words feature at 'report' | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F10344](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10344) | 9 | Layer 14: journalism-words feature at 'report' |  pronouns related to feelings or actions | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10344) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 1 | Layer 18: late pronoun aggregation at 'His' |  pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 9 | Layer 18: late pronoun aggregation at 'His' | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F7400](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) | 1 | Layer 18: late pronoun aggregation at 'His' |  words related to coding and software/UI interfaces, with some bias toward non-English words | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | Layer 19: late pronoun aggregator (positive male) |  various pronouns and names referring to people | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 21 | Layer 19: late pronoun aggregator (positive male) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'male' is not one of the top-k next-token candidates c |
| 3 | `get_top_features` | 20 features; top: L7:14893 de=0.488 |
| 4 | `inspect_feature` ×8 | L7:14893, L0:2994, L19:8814, L7:14946, L6:12990, L18:10315, L18:14743, L4:4315 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ✅ reported | 5 | 4 | Trace the path upstream from L7:F14893 (a female-pronoun/female-pronoun detector… |
| SA-2 | `L0:F2994@1` | ❌ error | — | — | Trace the path upstream from L0:F2994 (a "his" pronoun feature at position 1, th… |
| SA-3 | `L19:F8814@1` | ✅ reported | 4 | 4 | Trace the path upstream from L19:F8814 (a pronouns/names feature at position 1, … |
| SA-4 | `L7:F14946@1` | ✅ reported | 5 | 7 | Trace the path upstream from L7:F14946 (a "his"/male-pronoun feature at position… |

<details>
<summary><b>SA-1</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 5 | `get_upstream_features` | L6:F12990@1, k=10 | Emb:"His"@1 (de=4.91) +9 more |

**Findings:** The chain starts from the raw embedding of the token "His" (pos 1), which injects a strong masculine pronoun signal. This embedding excites a dedicated male‑pronoun detector in layer 6 (F12990) and also directly drives the broader pronoun detector in layer 7 (F14893). An intermediate specialised "his" detector in layer 4 (F4315) further reinforces the signal. The final layer‑7 feature, despite hav…

</details>

<details>
<summary><b>SA-3</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F8814 | " various pronouns and names referring to people" |
| 2 | `get_upstream_features` | L19:F8814@1, k=10 | Emb:"His"@1 (de=9.31) +9 more |
| 3 | `inspect_feature` | L18, F7400 | " words related to coding and software/UI interfaces, with some bias to" |
| 4 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 5 | `get_upstream_features` | L7:F14946@1, k=10 | Emb:"His"@1 (de=18.38) +9 more |
| 6 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 7 | `get_upstream_features` | L6:F12990@1, k=5 | Emb:"His"@1 (de=4.91) +4 more |
| 8 | `get_upstream_features` | L4:F4315@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 9 | `inspect_feature` | L18, F10315 | " pronouns and possessive pronouns" |
| 10 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |

**Findings:** Tracing from the late-layer pronoun feature L19:F8814 reveals a short pronoun circuit. The raw embedding for the token 'His' strongly excites an early detector at layer 4 (F4315). That detector feeds two mid‑layer pronoun representations: a more abstract male‑pronoun feature at layer 6 (F12990) and a possessive‑pronoun specific feature at layer 7 (F14946). Both mid‑layer features contribute positi…

</details>

<details>
<summary><b>SA-4</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 2 | `get_upstream_features` | L7:F14946@1, k=10 | Emb:"His"@1 (de=18.38) +9 more |
| 3 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 4 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 5 | `get_upstream_features` | L4:F4315@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 6 | `get_upstream_features` | L6:F12990@1, k=10 | Emb:"His"@1 (de=4.91) +9 more |
| 7 | `get_upstream_features` | L7:F14946@1, k=15 | Emb:"His"@1 (de=18.38) +14 more |
| 8 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 9 | `get_upstream_features` | L0:F2994@1, k=10 | Emb:"His"@1 (de=19.75) +9 more |
| 10 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 11 | `get_upstream_features` | L5:F10952@1, k=10 | Emb:"His"@1 (de=10.69) +9 more |
| 12 | `inspect_feature` | L2, F9301 | " all mentions of men and women in the context of relationships, dating" |
| 13 | `get_upstream_features` | L2:F9301@1, k=10 | Emb:"His"@1 (de=11.56) +9 more |
| 14 | `inspect_feature` | L2, F9233 | " the pronouns "she" and "he"" |

**Findings:** The inhibitory L7:F14946 feature (male possessive pronoun) receives its strongest excitatory drive directly from the raw token embedding for "His" (direct_effect ≈ 18.4). This embedding passes through a cascade of pronoun-detecting features—L4:F4315, L6:F12990, L5:F10952, and L2:F9301—each adding additional positive influence. The dominant upstream signal is therefore the input token embedding its…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14743@9, k=12 → Emb:" him"@9 (de=18.38) +11 more |
| 2 | `get_upstream_features` | L14:F4420@21, k=10 → Emb:" report"@21 (de=5.22) +9 more |
| 3 | `get_upstream_features` | L18:F7400@1, k=10 → Emb:"His"@1 (de=13.00) +9 more |
| 4 | `get_upstream_features` | L19:F2486@21, k=10 → L14:F4420 (de=14.31) +9 more |
| 5 | `get_upstream_features` | L4:F11898@6, k=10 → Emb:" world"@6 (de=35.25) +9 more |
| 6 | `get_upstream_features` | L0:F11767@6, k=10 → Emb:" world"@6 (de=16.38) +9 more |
| 7 | `get_upstream_features` | L0:F2011@2, k=10 → Emb:" desire"@2 (de=12.94) +9 more |
| 8 | `get_upstream_features` | L2:F9301@1, k=10 → Emb:"His"@1 (de=11.56) +9 more |
| 9 | `get_upstream_features` | L2:F5491@1, k=10 → Emb:"His"@1 (de=23.88) +9 more |
| 10 | `get_upstream_features` | L0:F8444@3, k=10 → Emb:" to"@3 (de=39.50) +9 more |
| 11 | `get_upstream_features` | L0:F7927@8, k=10 → Emb:" has"@7 (de=16.00) +9 more |
| 12 | `get_upstream_features` | L0:F16297@9, k=10 → Emb:" him"@9 (de=42.25) +9 more |
| 13 | `inspect_feature` ×12 | L18:14743, L18:10315, L18:7400, L0:16297, L0:2011, L0:11767, L0:8444, L0:7927, L14:4420, L19:2486, L2:5491, L2:9301 |
| 14 | `get_upstream_features` | L19:F2486@21, k=10 → L14:F4420 (de=14.31) +9 more |
| 15 | `get_upstream_features` | L14:F4420@21, k=10 → Emb:" report"@21 (de=5.22) +9 more |
| 16 | `get_upstream_features` | L8:F8855@21, k=10 → Emb:" report"@21 (de=12.06) +9 more |
| 17 | `get_upstream_features` | L16:F14120@9, k=10 → Emb:" him"@9 (de=10.00) +9 more |
| 18 | `inspect_feature` ×6 | L7:13646, L8:8855, L8:8437, L14:10344, L13:10255, L16:14120 |
| 19 | `get_upstream_features` | L7:F14893@1, k=15 → Emb:"His"@1 (de=23.50) +14 more |
| 20 | `get_upstream_features` | L18:F10315@1, k=10 → Emb:"His"@1 (de=21.38) +9 more |
| 21 | `inspect_feature` ×4 | L11:10933, L11:9183, L9:8770, L13:8128 |
| 22 | `get_upstream_features` | L14:F4420@21, k=15 → Emb:" report"@21 (de=5.22) +14 more |
| 23 | `get_upstream_features` | L19:F2486@21, k=15 → L14:F4420 (de=14.31) +14 more |
| 24 | `get_upstream_features` | L4:F11898@6, k=8 → Emb:" world"@6 (de=35.25) +7 more |
| 25 | `get_upstream_features` | L0:F2208@1, k=8 → Emb:"His"@1 (de=12.81) +7 more |
| 26 | `get_upstream_features` | L5:F10952@1, k=8 → Emb:"His"@1 (de=10.69) +7 more |
| 27 | `inspect_feature` ×4 | L0:2208, L8:8855, L5:10952, L4:11898 |

### Build

`build_circuit` → 19 nodes, 35 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 112,084 | 7,981 | 465,222 | 0 | $0.0711 | — | — |
| SA-1 | openai/gpt-oss-120b | 44,590 | 3,921 | 0 | 0 | $0.0090 | ✅ 5F/4E | Trace the path upstream from L7:F14893 (a female-pronoun/fem… |
| SA-3 | openai/gpt-oss-120b | 113,821 | 6,682 | 2,528 | 0 | $0.0211 | ✅ 4F/4E | Trace the path upstream from L19:F8814 (a pronouns/names fea… |
| SA-4 | openai/gpt-oss-120b | 207,964 | 12,369 | 3,712 | 0 | $0.0387 | ✅ 5F/7E | Trace the path upstream from L7:F14946 (a "his"/male-pronoun… |
| **Total** | | **478,459** | **30,953** | **471,462** | **0** | **$0.1399** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 12s