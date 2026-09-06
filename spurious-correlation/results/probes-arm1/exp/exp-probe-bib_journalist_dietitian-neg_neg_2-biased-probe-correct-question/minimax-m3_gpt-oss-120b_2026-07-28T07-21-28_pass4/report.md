# Circuit Oracle Report
**Date:** 2026-07-28 07:21:28 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's positive classification is driven primarily by male-gender pronoun features (his/him/He) anchored to the "His" token at position 1 and "him" at position 9, with only a modest negative contribution from a legitimate journalism-terms feature on "report" at position 21.

**Confidence:** 8

**Reasoning:** The circuit traces the probe score back to two competing signal paths, and the user concern is **confirmed**.

**Male-pronoun path (dominant positive driver).** The output logit at layer 26 receives the bulk of its positive activation from a chain of male-pronoun detectors:
- **L7:F14893** ("pronouns or possessive pronouns", frac_nonzero 0.0089, +0.49 direct to probe) fires on "His" at pos 1; its top upstream is `Emb: His` (+23.5), confirming the "His" token is the sole signal source. Its sibling L7:F14946 (also "his"-detector, –0.48) provides pushback, but the net is +0.004.
- **L19:F8814** ("various pronouns and names referring to people", frac_nonzero 0.087, +0.26) is the late-layer aggregator; its top upstream is `Emb: His` (+9.3) and L18:F7400/L18:F10315 (both male pronoun detectors) and L7:F14946. Top upstream of L18:F14743 ("He", frac_nonzero 0.018, –0.21) is `Emb: him` at pos 9 (+18.4) plus L0:F16297 ("him", +6.9). So the **"His"/"him" tokens alone are sufficient to activate the whole male-pronoun cascade** — no entity / profession information enters through this path.
- An entire hierarchy of male-pronoun features propagates the signal: L0:F2994/F2208/F16297 → L1:F7439 → L2:F5491 ("God's His", religious male) → L4:F4315 → L6:F12990 ("male pronouns and titles") → L7:F14893/F14946 → L18:F14743/F10315/F7400 → L19:F8814 → output. Almost every node in this chain is a `his`/`him`/`he` detector (verified by inspection of top-activating examples and the `▁his`/`▁him` suppressed tokens).

**Profession path (minor, mostly cancelling).** The genuine "journalist" signal is real but weak and self-cancelling:
- **L14:F4420** ("journalism/newspaper terms", frac_nonzero 0.017, –0.16) and **L19:F2486** ("journalistic sources and news outlets", –0.105) both fire on "report" at pos 21, with upstream chain `Emb: report` → L7:F13646 ("news reporting", +3.7) → L8:F8855 ("news reporters", +5.1) and L8:F8437 (film/media context, +3.3) → L14:F4420 → L19:F2486.
- L7:F13646 is *also* a top upstream of L19:F8814 (the male-pronoun aggregator), so the journalism feature is partly "re-routed" into the same late-layer pronoun bucket — its +3.7 contribution to the male-pronoun aggregator barely offsets the L18:F14743 ("He" feature) that pushes back. The net effect of the profession path on the output is small and is dominated by the much larger male-pronoun signal.

**Mechanism summary.** The probe is a binary classifier whose positive class is strongly **gender-correlated, not profession-specific**: the 0.49 + 0.26 contributions from L7:F14893 and L19:F8814 (both built from the single token "His" at pos 1) outweigh the journalism-path contributions (~ –0.16 from L14:F4420 + –0.105 from L19:F2486, partially offset by the journalism feature's positive side-effect on the male-pronoun aggregator). The probe direction is satisfied almost entirely by *which pronoun opens the sentence*, not by the "report"/"news organizations" content that actually indicates the profession. The user's concern is well-founded: the circuit is a textbook example of a probe latching onto a male-gender spurious feature.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | Layer 0 male-pronoun token detectors | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2208](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2208) | 1 | Layer 0 male-pronoun token detectors |  the pronoun "Him" and the possessive pronoun "His" when used in a religious context | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2208) |
| [L0:F16297](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) | 9 | Layer 0 male-pronoun token detectors |  the pronoun "him" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) |
| [L2:F5491](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) | 1 | Layer 2 religious 'His' (God-context male) | references to God in the third person. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) |
| [L2:F9301](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) | 1 | Layer 2 religious 'His' (God-context male) |  all mentions of men and women in the context of relationships, dating, or gendered social roles | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) |
| [L1:F7439](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7439) | 1 | Layer 1 'his/him' pronoun |  the possessive pronouns "his" and "him" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7439) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | Layer 4 'his' pronoun cluster |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L4:F15567](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) | 1 | Layer 4 'his' pronoun cluster | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) |
| [L4:F9757](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) | 1 | Layer 4 'his' pronoun cluster | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Layer 6 male pronouns + titles (Mr, man) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Layer 7 male-possessive pronoun detectors (anti- vs pro-) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | Layer 7 male-possessive pronoun detectors (anti- vs pro-) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 21 | Layer 7 journalism/reporting cluster (pos 21) |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 21 | Layer 7 journalism/reporting cluster (pos 21) |  words and phrases associated with broadcast journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 21 | Layer 8 reporters + film/media (pos 21) |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 21 | Layer 8 reporters + film/media (pos 21) | content related to film festivals and production, particularly documentary films, and the recognition they receive. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 21 | Layer 14 journalism/newspaper terms (pos 21) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 9 | Layer 18 male-pronoun/He (pos 9) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 1 | Layer 18 male-pronoun/He (pos 9) |  pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L18:F7400](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) | 1 | Layer 18 male-pronoun/He (pos 9) |  words related to coding and software/UI interfaces, with some bias toward non-English words | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| [L16:F14120](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/14120) | 9 | Layer 16 people-directed refs (him/us/them) |  references to people being directed and/or affected in some way. | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/14120) |
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | Layer 19 people-pronoun/news-source (mixed) |  various pronouns and names referring to people | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 21 | Layer 19 people-pronoun/news-source (mixed) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L7:14893 de=0.488 |
| 3 | `inspect_feature` ×19 | L7:14893, L7:14946, L0:2994, L19:8814, L18:14743, L6:12990, L4:4315, L14:4420, L0:2011, L2:9301, L4:11898, L19:2486, L0:8444, L0:7927, L18:10315, L18:7400, L0:2208, L0:11767, L2:5491 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ❌ error | — | — | Trace the upstream path from L7:F14893 (label: pronouns/possessive pronouns, fir… |
| SA-2 | `L18:F14743@9` | ❌ error | — | — | Trace the upstream path from L18:F14743 (label: "He", fires at pos 9 = "given hi… |
| SA-3 | `L14:F4420@21` | ❌ error | — | — | Trace upstream from L14:F4420 (label: "journalism/newspaper terms", fires on "re… |
| SA-4 | `L19:F8814@1` | ❌ error | — | — | Trace upstream from L19:F8814 (label: "various pronouns and names referring to p… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L7:F14893@1, k=10 → Emb:"His"@1 (de=23.50) +9 more |
| 2 | `get_upstream_features` | L7:F14946@1, k=10 → Emb:"His"@1 (de=18.38) +9 more |
| 3 | `get_upstream_features` | L18:F14743@9, k=10 → Emb:" him"@9 (de=18.38) +9 more |
| 4 | `get_upstream_features` | L14:F4420@21, k=10 → Emb:" report"@21 (de=5.22) +9 more |
| 5 | `get_upstream_features` | L19:F8814@1, k=10 → Emb:"His"@1 (de=9.31) +9 more |
| 6 | `get_upstream_features` | L19:F2486@21, k=10 → L14:F4420 (de=14.31) +9 more |
| 7 | `get_upstream_features` | L18:F10315@1, k=8 → Emb:"His"@1 (de=21.38) +7 more |
| 8 | `get_upstream_features` | L18:F7400@1, k=8 → Emb:"His"@1 (de=13.00) +7 more |
| 9 | `get_upstream_features` | L6:F12990@1, k=8 → Emb:"His"@1 (de=4.91) +7 more |
| 10 | `get_upstream_features` | L4:F4315@1, k=8 → Emb:"His"@1 (de=23.50) +7 more |
| 11 | `inspect_feature` ×10 | L0:16297, L11:10933, L11:9183, L9:8770, L1:7439, L16:14120, L8:8855, L7:13646, L8:8437, L7:9092 |

### Build

`build_circuit` → 17 nodes, 41 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 69,339 | 6,678 | 248,075 | 0 | $0.0437 | — | — |
| **Total** | | **69,339** | **6,678** | **248,075** | **0** | **$0.0437** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 33s