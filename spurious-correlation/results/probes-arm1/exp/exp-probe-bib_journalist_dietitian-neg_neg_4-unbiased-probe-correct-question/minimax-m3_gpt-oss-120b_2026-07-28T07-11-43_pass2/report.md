# Circuit Oracle Report
**Date:** 2026-07-28 07:11:43 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a *mix* of legitimate profession-indicating features (journalism/reporter/writer tokens, broadcasting, editorial roles, institutional/defense topic tokens) AND a clearly spurious pronoun-co-occurrence feature that tracks gendered "he/she" mentions — the user's concern is confirmed.

**Confidence:** 7

**Reasoning:**

The attribution graph reveals that the profession probe fires for a genuine cluster of journalism/defense‑writing signals, but ALSO for a single high‑impact gender signal. Specifically:

- **Profession-defining mid-layer supernode** (drives the output positively through `mid_journalism → output_logit`):
  - `L14:F4420` @ pos 28 — "words and phrases related to journalism and newspapers" (act 23.1, de = −0.07; *promoted tokens: journalists, journalism, reporter, editorial*).
  - `L8:F8855` @ pos 28 — "mentions of news reporters and news reporting" (promoted: reporter, journalistic, journalist, journalism).
  - `L4:F13253` @ pos 28 — "things related to journalism and the media" (promoted: Journalism, journalists, journalism, media, reporters).
  - `L6:F12712` @ pos 28 — "titles of editors and publishers in scientific publications" (Editor, Chief).
  - `L6:F10984` @ pos 71 — "mentions of TV and radio broadcasting".
  - `L6:F5849` @ pos 28 — "references to blogs and blog posts" (promoted: blogging, writer, blog, blogger, blogs).
  These are the "writer"/"freelance" / "Editor"/"broadcasting" / "blogging" tokens at pos 28 and pos 71. They flow from `Emb: writer` and `Emb: freelance` (de ≈ 5.75/2.69 into L14:F4420). This is the *legitimate* path — actual profession evidence.

- **Topical/institutional early-layer supernode** (`early_token_features → mid_journalism` and directly to output): `L3:F10489` ("Institute" at pos 7), `L1:F4459` ("research institutes" at pos 7, 0.003 frac_nonzero → very specific), `L0:F9297` ("government ministries" at pos 7), `L1:F1445` ("military vehicles/weapons" at pos 7), `L0:F15880` / `L2:F12901` ("Middle East" at pos 15), `L0:F3007` ("middle"), `L0:F10881` ("coverage"), `L0:F12713` ("New York City"), `L0:F9728` ("sponsor"). These pick up "Royal United Services Institute", "Defence", "Middle East", "Defense News" etc. — concrete domain vocabulary supporting the "defense journalist" reading.

- **Spurious gender signal** (`gender_pronoun → output_logit`):
  - `L0:F12768` @ pos 22 — labelled "mentions of 'he' and 'she' in close proximity" (frac_nonzero 0.011). It fires with **act 36, direct_effect +0.075** on the "he" token at pos 22 — *one of the strongest positive contributors* to the probe score. Its only major upstream is the "he" token embedding (de 40.25). Critically, its promoted tokens are generic pronouns ("them", "them", etc.) and it suppresses "he/he/그는/彼" — i.e., it does **not** specifically mean "male writer" but rather fires on the mere presence of gendered pronouns anywhere in the passage, then is *used* by the probe. The probe's profession weight projects onto this feature positively, so the probe effectively treats "has a 'he' or 'she' pronoun" as evidence for the profession. This is the textbook spurious correlate the user warned about.

- **Generic function-word features** (`L0:F7124` "at", `F15661` "spin", `F6051` "periods", `F4870` "commas", `F14824` "has", `F2127` "dream", `F4308` "partial", `F15323` "starting", `F12068` "starting points") — high-frequency, low-specificity words with small direct_effects, mostly noise/syntactic scaffolding. The probe also reads off these, which is mildly suspect but unsurprising for any linear probe.

- **Token-embedding roots** are reached for: `he` (pos 22) → `F12768` (the gender signal); `writer` (pos 28) and `freelance` (pos 27) → journalism mid-layer; `Institute` (pos 7), `Middle` (pos 14), `covering` (pos 12), `East` (pos 15) → early topical features.

**Mechanism.** The probe classifies the subject as a journalist using (a) genuine profession cues — a tight cluster of journalism/reporter/editor/broadcast features at L4–L14, fed by the "writer" + "freelance" embeddings at pos 28 — AND (b) the bare presence of gendered pronouns (specifically the "he" embedding at pos 22 → L0:F12768 with +0.075 direct_effect). Because the biographical text repeatedly references "he" in describing a male defense writer, the pronoun-co-occurrence feature becomes confounded with the profession. The probe is partially legitimate but partially uses a spurious demographic correlate: the user's concern is validated.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 28 | Mid-layer: profession-defining (journalism/reporter/writer) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 28 | Mid-layer: profession-defining (journalism/reporter/writer) |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L6:F12712](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) | 28 | Mid-layer: profession-defining (journalism/reporter/writer) |  titles of editors and publishers in scientific publications | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 28 | Mid-layer: profession-defining (journalism/reporter/writer) |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L6:F10984](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10984) | 71 | Mid-layer: profession-defining (journalism/reporter/writer) |  mentions of TV and radio broadcasting | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10984) |
| [L6:F5849](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5849) | 28 | Mid-layer: profession-defining (journalism/reporter/writer) |  references to blogs and blog posts | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5849) |
| [L3:F10489](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10489) | 7 | Early-layer: topical/institutional token features |  the word "Institute" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10489) |
| [L1:F4459](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4459) | 7 | Early-layer: topical/institutional token features |  mentions of research institutes | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4459) |
| [L2:F12901](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12901) | 15 | Early-layer: topical/institutional token features |  the phrase "Middle East" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12901) |
| [L0:F15880](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15880) | 15 | Early-layer: topical/institutional token features | mentions of the Middle East | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15880) |
| [L1:F1445](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1445) | 7 | Early-layer: topical/institutional token features |  terms related to the military, especially vehicles and weapons | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1445) |
| [L0:F9297](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9297) | 7 | Early-layer: topical/institutional token features |  mentions of government ministries and ministers. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9297) |
| [L4:F5060](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5060) | 7 | Early-layer: topical/institutional token features | references to institutions and technology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5060) |
| [L0:F3007](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3007) | 14 | Early-layer: topical/institutional token features |  the word "middle", and sometimes the word "character", and "camp" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3007) |
| [L0:F10881](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10881) | 12 | Early-layer: topical/institutional token features |  the word "coverage" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10881) |
| [L0:F1229](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1229) | 14 | Early-layer: topical/institutional token features |  the word "shake," and words related to the middle of something | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1229) |
| [L0:F12713](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12713) | 15 | Early-layer: topical/institutional token features | mentions of "New York City." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12713) |
| [L0:F9728](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9728) | 12 | Early-layer: topical/institutional token features | the word "sponsor" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9728) |
| [L0:F6484](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6484) | 7 | Early-layer: topical/institutional token features |  the word "sky" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6484) |
| [L0:F2348](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2348) | 4 | Early-layer: topical/institutional token features |  the word "rapid" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2348) |
| [L0:F13096](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13096) | 3 | Early-layer: topical/institutional token features |  instances of the word "the", often followed by nouns or other determiners | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13096) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 22 | Gender-pronoun feature (he/she proximity) - spurious |  mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L0:F7124](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7124) | 2 | Generic function-word/structural features | the word "at" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7124) |
| [L0:F15661](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15661) | 7 | Generic function-word/structural features | the word "spin" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15661) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 38 | Generic function-word/structural features | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F4870](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4870) | 11 | Generic function-word/structural features |  commas and sometimes reach (context not clear) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4870) |
| [L0:F14824](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) | 40 | Generic function-word/structural features | the word "has" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) |
| [L0:F2127](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2127) | 7 | Generic function-word/structural features |  the word "dream" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2127) |
| [L0:F4308](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4308) | 1 | Generic function-word/structural features |  the word "partial" and related usages like "partially" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4308) |
| [L0:F15323](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15323) | 1 | Generic function-word/structural features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15323) |
| [L0:F12068](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12068) | 2 | Generic function-word/structural features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12068) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'PROBE_TARGET' is not one of the top-k next-token cand |
| 3 | `get_top_features` | 15 features; top: L0:7124 de=-0.157 |
| 4 | `inspect_feature` ×15 | L0:12768, L0:3007, L0:10881, L0:7124, L0:15661, L0:6484, L14:4420, L6:12712, L0:2348, L1:4459, L0:1229, L0:9297, L3:10489, L2:12901, L1:1445 |
| 5 | `get_upstream_features` | Emb:" writer"@28 (de=5.75) +11 more |
| 6 | `get_upstream_features` | Emb:" writer"@28 (de=6.22) +11 more |
| 7 | `get_upstream_features` | Emb:" he"@22 (de=40.25) +11 more |
| 8 | `get_upstream_features` | Emb:" Middle"@14 (de=20.75) +11 more |
| 9 | `get_upstream_features` | Emb:" covering"@12 (de=16.25) +11 more |
| 10 | `inspect_feature` ×2 | L4:13253, L8:8855 |
| 11 | `get_top_features` | 30 features; top: L0:7124 de=-0.157 |
| 12 | `inspect_feature` ×15 | L6:10984, L0:13096, L0:9728, L0:6051, L0:12713, L4:5060, L0:8690, L1:15323, L0:15880, L2:12068, L0:2127, L6:5849, L0:4870, L0:14824, L0:4308 |
| 13 | `get_upstream_features` | Emb:" Institute"@7 (de=16.12) +9 more |
| 14 | `get_upstream_features` | Emb:" broadcasting"@71 (de=13.06) +9 more |
| 15 | `get_upstream_features` | Emb:" Institute"@7 (de=11.81) +9 more |
| 16 | `get_upstream_features` | Emb:" Institute"@7 (de=15.12) +9 more |

### Build

`build_circuit` → 12 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 103,663 | 9,885 | 407,412 | 0 | $0.0674 | — | — |
| **Total** | | **103,663** | **9,885** | **407,412** | **0** | **$0.0674** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 55s