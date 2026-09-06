# Circuit Oracle Report
**Date:** 2026-07-28 07:19:57 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by **two parallel, weakly-interacting pathways** — a genuine profession-content pathway anchored on the "journalistic" token, and a **substantial parallel male-pronoun pathway** that tracks the subject's gender through multiple pronoun tokens. The user's concern is partially validated: pronoun/gender features carry non-trivial direct effect, but journalism-content features also contribute meaningfully.

**Confidence:** 7

**Reasoning:**

**Pathway 1 — Content/profession (legitimate):** Token embedding of "journalistic" (pos 13, direct_effect 25.6) feeds L4 journalism/media supernode (F13253, F7446 → promoted tokens include "Journalism", "journalists", "journalism", "media"; frac_nonzero ≈ 0.006-0.07, content-specific). These feed L7 broadcast-journalism features (F9092, F13646 — promoted tokens "journalist", "reporter", "correspondent") which then excite L14 journalism vocabulary (F4420, frac_nonzero 0.016, fires on "reporter"/"newspaper"/"reporting"; promoted tokens "journalists", "journalist", "journalism"). F4420 has direct_effect −0.13 on the probe. The L1 lexical content features (F14812 "stories/narrative" at pos 3, F7449 "represents" at pos 9) and L0 word detectors ("researches", "stories", "represents") add small positive contributions at early layers (direct_effects ~0.1-0.2). This pathway is genuine profession evidence.

**Pathway 2 — Gender/pronoun (spurious):** Token embeddings of "He" (pos 1), "he" (pos 23), "him" (pos 46) feed a dedicated pronoun stack: L0 detectors (F16297 "him" frac_nonzero 0.033, F12768 "he", F2994 "his/he", F11400 "his/he") → L2 multilingual pronoun F2128, L2 gender-role F9301 → L4 "he/him" F14796 → L5 third-person F10952 → L6 male-pronoun+titles F12990 (suppresses "herself"/"she"/feminine) → L7 F14946 (his/he/him) and F14893 (pronouns, pos 1 AND pos 46) → L17 F5889 (pronoun references, very high activations ~330, frac_nonzero 0.018) and L18 F14743 ("He" - male pronoun, max_activation 421, frac_nonzero 0.018). F14893 and F14743 carry large direct_effects (+0.20 and −0.14 respectively). The L7 pronoun path has a LATER layer (L17-L18) than the content path's terminal L14, giving pronoun signals disproportionate late-layer weighting on the probe.

**Assessment of the user's concern:** The concern is **partially correct but overstated**. Both pathways are present. The pronoun pathway is structurally elaborate (8 stacked features across L0-L18), includes gender-stereotyped features (F12990 "male pronouns and titles along with descriptors associated with men"; F9301 "men and women in the context of relationships, dating, or gendered social roles"), and reaches a later aggregation layer than the content pathway. The subject being a male journalist is confounded with the profession label, so a probe trained on a single example cannot fully disentangle them. The content pathway is real (journalism features fire on "journalistic" and propagate cleanly), so the probe is not *purely* using gender — but the parallel pronoun stack is a clear confound that should be flagged, and the probe would likely fire on pronoun-heavy non-journalist male subjects.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F16297](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) | 46 | L0 male-pronoun detectors: F16297 ("him"), F12768 ("he" in context), F2994 ("his/he"), F11400 (his/he) |  the pronoun "him" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 23 | L0 male-pronoun detectors: F16297 ("him"), F12768 ("he" in context), F2994 ("his/he"), F11400 (his/he) |  mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 52 | L0 male-pronoun detectors: F16297 ("him"), F12768 ("he" in context), F2994 ("his/he"), F11400 (his/he) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F11400](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11400) | 1 | L0 male-pronoun detectors: F16297 ("him"), F12768 ("he" in context), F2994 ("his/he"), F11400 (his/he) | the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11400) |
| [L0:F4564](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) | 2 | L0 content-word detectors: F4564 ("researches"), F10036 ("scientists"/research), F5333 ("stories"), F61 ("stories"), F5267 ("represents"), F14216 ("signs") | the word "research." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) |
| [L0:F10036](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10036) | 2 | L0 content-word detectors: F4564 ("researches"), F10036 ("scientists"/research), F5333 ("stories"), F61 ("stories"), F5267 ("represents"), F14216 ("signs") |  words about scientific research and scientists | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10036) |
| [L0:F5333](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5333) | 3 | L0 content-word detectors: F4564 ("researches"), F10036 ("scientists"/research), F5333 ("stories"), F61 ("stories"), F5267 ("represents"), F14216 ("signs") | mentions of stories that are being told | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5333) |
| [L0:F61](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/61) | 3 | L0 content-word detectors: F4564 ("researches"), F10036 ("scientists"/research), F5333 ("stories"), F61 ("stories"), F5267 ("represents"), F14216 ("signs") | the word "stories" sometimes along with apostrophes and common names. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/61) |
| [L0:F5267](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5267) | 9 | L0 content-word detectors: F4564 ("researches"), F10036 ("scientists"/research), F5333 ("stories"), F61 ("stories"), F5267 ("represents"), F14216 ("signs") | mentions of representation or things standing for other things. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5267) |
| [L0:F14216](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14216) | 7 | L0 content-word detectors: F4564 ("researches"), F10036 ("scientists"/research), F5333 ("stories"), F61 ("stories"), F5267 ("represents"), F14216 ("signs") |  the word "signs" and horizontal lines | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14216) |
| [L1:F14812](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) | 3 | L1 lexical content detectors: F14812 ("stories/narrative"), F7449 ("represents/representation") |  references to stories, chapters, and other narrative elements | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) |
| [L1:F7449](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7449) | 9 | L1 lexical content detectors: F14812 ("stories/narrative"), F7449 ("represents/representation") | instances of the word "representation" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7449) |
| [L2:F2128](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2128) | 1 | L2-L6 pronoun/gender stack: F2128 (he/him multilingual), F9301 (gender roles), F14796 (he/him core), F10952 (third-person pronoun), F12990 (male pronouns + male titles) | pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, *ele*, and *ela* across multiple languages. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2128) |
| [L2:F9301](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) | 1 | L2-L6 pronoun/gender stack: F2128 (he/him multilingual), F9301 (gender roles), F14796 (he/him core), F10952 (third-person pronoun), F12990 (male pronouns + male titles) | all mentions of men and women in the context of relationships, dating, or gendered social roles | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) |
| [L4:F14796](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14796) | 1 | L2-L6 pronoun/gender stack: F2128 (he/him multilingual), F9301 (gender roles), F14796 (he/him core), F10952 (third-person pronoun), F12990 (male pronouns + male titles) | the pronoun "he" or "him" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14796) |
| [L5:F10952](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) | 1 | L2-L6 pronoun/gender stack: F2128 (he/him multilingual), F9301 (gender roles), F14796 (he/him core), F10952 (third-person pronoun), F12990 (male pronouns + male titles) | third person pronouns in varying contexts | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | L2-L6 pronoun/gender stack: F2128 (he/him multilingual), F9301 (gender roles), F14796 (he/him core), F10952 (third-person pronoun), F12990 (male pronouns + male titles) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 13 | L4 journalism/media: F13253 (journalism and media), F7446 (media/information processes) |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L4:F7446](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7446) | 13 | L4 journalism/media: F13253 (journalism and media), F7446 (media/information processes) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7446) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 13 | L7 journalism broadcast: F9092 (broadcast journalism), F13646 (news reporting/journalism) |  words and phrases associated with broadcast journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 13 | L7 journalism broadcast: F9092 (broadcast journalism), F13646 (news reporting/journalism) |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | L7 pronoun output features: F14946 (his/he/him), F14893 (pronouns), F5889 (third-person pronoun aggregator) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 46 | L7 pronoun output features: F14946 (his/he/him), F14893 (pronouns), F5889 (third-person pronoun aggregator) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | L7 pronoun output features: F14946 (his/he/him), F14893 (pronouns), F5889 (third-person pronoun aggregator) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 13 | L14 journalism: F4420 (journalism/newspaper vocabulary) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 23 | L17-L18 pronoun aggregator: F5889 (pronoun references), F14743 ("He" - male pronoun) |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 23 | L17-L18 pronoun aggregator: F5889 (pronoun references), F14743 ("He" - male pronoun) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token ' journalist' is not one of the top-k next-token candi |
| 3 | `get_top_features` | 20 features; top: L0:6051 de=-0.256 |
| 4 | `inspect_feature` ×10 | L0:6051, L0:7696, L1:14812, L1:7449, L0:4564, L0:5333, L0:3255, L0:10187, L7:14893, L7:14946 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L1:F14812@3` | ❌ error | — | — | Trace the "stories" feature at L1:14812 pos 3 (fires on "stories" in "He researc… |
| SA-2 | `L7:F14893@46` | ✅ reported | 4 | 5 | Trace the "pronouns" feature at L7:14893 pos 46 upstream. The user is concerned … |
| SA-3 | `L1:F7449@9` | ✅ reported | 4 | 5 | Trace the "representation" feature at L1:7449 pos 9 (fires on "represents" in "r… |
| SA-4 | `L7:F14946@1` | ✅ reported | 7 | 9 | Trace the "his/he/him" pronoun feature at L7:14946 pos 1 upstream. The user is c… |
| SA-5 | `L1:F14812@3` | ❌ error | — | — | Trace L1:14812 "stories/narrative" feature at pos 3 upstream. Look for the actua… |

<details>
<summary><b>SA-2</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@46, k=10 | Emb:" him"@46 (de=12.56) +9 more |
| 3 | `inspect_feature` | L0, F16297 | " the pronoun "him"" |
| 4 | `inspect_feature` | L4, F11391 | " pronouns referring to people and words related to negative experience" |
| 5 | `inspect_feature` | L4, F4017 | " words and short phrases in French" |
| 6 | `get_upstream_features` | L0:F16297@46, k=10 | Emb:" him"@46 (de=43.25) +9 more |
| 7 | `get_upstream_features` | L4:F11391@46, k=10 | Emb:" him"@46 (de=21.12) +9 more |
| 8 | `get_upstream_features` | L4:F4017@46, k=10 | Emb:" him"@46 (de=16.38) +9 more |

**Findings:** The L7:14893 "pronouns or possessive pronouns" feature is driven primarily by the raw token embedding for the word "him" (pos 46). The signal flows upward through a very specific layer‑0 feature that also detects the token "him". Both of these upstream nodes are pure pronoun detectors; they do not encode any profession‑related semantics. Additional downstream aggregators at layer 4 (features 11391…

</details>

<details>
<summary><b>SA-3</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F7449 | "instances of the word "representation"" |
| 2 | `get_upstream_features` | L1:F7449@9, k=10 | Emb:" represents"@9 (de=20.50) +9 more |
| 3 | `inspect_feature` | L0, F5267 | "mentions of representation or things standing for other things." |
| 4 | `inspect_feature` | L0, F14520 | "verbs that describe actions affecting a noun, especially in the contex" |
| 5 | `get_upstream_features` | L0:F5267@9, k=10 | Emb:" represents"@9 (de=16.62) +9 more |
| 6 | `inspect_feature` | L0, F14143 | "the words "holiday" or "holidays" and "sanctity", and one time it find" |

**Findings:** The L1:7449 'representation' feature is driven almost entirely by the literal token 'represents' (embedding edge with large direct effect). Its upstream layer‑0 feature 5267 captures the broader concept of representation but still activates on the same token. Minor upstream influences from unrelated verb and holiday detectors are weak. Thus the feature encodes lexical detection of the word 'repres…

</details>

<details>
<summary><b>SA-4</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 2 | `get_upstream_features` | L7:F14946@1, k=10 | Emb:"He"@1 (de=11.50) +9 more |
| 3 | `inspect_feature` | L4, F14796 | "the pronoun "he" or "him"" |
| 4 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 5 | `get_upstream_features` | L4:F14796@1, k=10 | Emb:"He"@1 (de=17.12) +9 more |
| 6 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 7 | `inspect_feature` | L2, F9301 | " all mentions of men and women in the context of relationships, dating" |
| 8 | `get_upstream_features` | L2:F9301@1, k=10 | Emb:"He"@1 (de=14.94) +9 more |
| 9 | `get_upstream_features` | L6:F12990@1, k=10 | Emb:"He"@1 (de=3.41) +9 more |
| 10 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |

**Findings:** The L7:14946 feature is a male‑pronoun detector (he/him/his). Its activation at position 1 is driven primarily by the raw token embedding for "He" (positive direct effect 11.5) and reinforced by a cascade of upstream pronoun‑related features in lower layers: L4:14796 (core "he/him" detector), L6:12990 (male pronoun + gendered titles), L5:10952 (generic third‑person pronoun), L2:9301 (gender‑role m…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×9 | L0:61, L0:10036, L0:14216, L0:2994, L4:13253, L18:14743, L14:4420, L0:9121, L0:1301 |
| 2 | `get_upstream_features` | L4:F13253@13, k=10 → Emb:" journalistic"@13 (de=25.62) +9 more |
| 3 | `get_upstream_features` | L14:F4420@13, k=10 → Emb:" journalistic"@13 (de=24.38) +9 more |
| 4 | `get_upstream_features` | L18:F14743@23, k=10 → Emb:" he"@23 (de=25.50) +9 more |
| 5 | `get_upstream_features` | L1:F14812@3, k=10 → Emb:" stories"@3 (de=18.62) +9 more |
| 6 | `inspect_feature` ×8 | L3:7446, L7:9092, L7:13646, L0:12768, L17:5889, L0:16297, L4:14796, L6:12990 |
| 7 | `get_upstream_features` | L7:F9092@13, k=10 → Emb:" journalistic"@13 (de=14.88) +9 more |
| 8 | `get_upstream_features` | L17:F5889@23, k=10 → Emb:" he"@23 (de=33.75) +9 more |
| 9 | `get_upstream_features` | L4:F14796@1, k=10 → Emb:"He"@1 (de=17.12) +9 more |
| 10 | `get_upstream_features` | L0:F16297@46, k=10 → Emb:" him"@46 (de=43.25) +9 more |

### Build

`build_circuit` → 14 nodes, 16 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 75,943 | 6,172 | 225,631 | 0 | $0.0437 | — | — |
| SA-3 | openai/gpt-oss-120b | 48,961 | 3,260 | 5,056 | 0 | $0.0094 | ✅ 4F/5E | Trace the "representation" feature at L1:7449 pos 9 (fires o… |
| SA-2 | openai/gpt-oss-120b | 74,622 | 4,828 | 10,112 | 0 | $0.0142 | ✅ 4F/5E | Trace the "pronouns" feature at L7:14893 pos 46 upstream. Th… |
| SA-4 | openai/gpt-oss-120b | 134,359 | 8,789 | 7,680 | 0 | $0.0255 | ✅ 7F/9E | Trace the "his/he/him" pronoun feature at L7:14946 pos 1 ups… |
| **Total** | | **333,885** | **23,049** | **248,479** | **0** | **$0.0929** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 47s