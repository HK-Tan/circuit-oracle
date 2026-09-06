# Circuit Oracle Report
**Date:** 2026-07-28 07:23:37 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction classification is driven by a stack of "not only" / "but also" contrastive-construction features that fire on the surface-level phrasal pattern rather than on the actual semantic contradiction (premise claims X, hypothesis asserts not-X); the strongest positive contributors are all "not only" phrase detectors at layers 2–17, while the only top feature carrying the actual entailment-reversing negation (`isn't` at pos 28–31) has a near-zero or weakly negative direct effect on the probe.

**Confidence:** 4

**Reasoning:** The user is right that the circuit leans on spurious lexical/structural signals. Of the top-20 direct contributors, the bulk encode either the *phrase shape* "not only" / "but also" (L2:F5627 "not only", L2:F13565 "programs", L4:F6000 "program", L4:F12847 "reporting verb + that", L9:F12274 "not only", L12:F3005 "not only", L14:F10765 "not only", L15:F1990 "not only", L15:F12905 "but + contrasting relationship", L16:F6005 "Not only", L17:F3763 "only" — promoting "but", L14:F11020 "but/also", L10:F6078 "contrasting sections", L4:F5347 "but", L4:F2884 "but and contrastive conjunctions", L6:F3655 "just + surrounding words", L0:F2961 "qualifications or negations like necessarily/uncommon") or simply the token "will" (L0:F8046) / "program" (L1:F11907). The actual contradiction-bearing negation in the hypothesis — `isn't going to improve` (pos 26–31) — is barely represented. The features that *do* attend to pos 28–31 (L0:F6236 "t after isn'", L3:F6227 "informal / negation fragments", L7:F2088, L10:F6670, L11:F11267 "although/absent", L12:F12606) collectively push the probe with far smaller magnitude than the "not only"/"but also" tower, and L11:F11267 has *negative* direct_effect (-1.94) on L12:F12606, partly canceling the entailment signal.

The signal flow is: token embeddings of `not`, `only`, `but`, `program`, `will` → early lexicon features (L0:L1) → mid-layer "not only" phrase detectors (L2:L6, including L2:F5627 at activation 46 and L4:F12847 at activation 9) → late "not only / but also" concept features (L9:L17, including L15:F12905 at activation 49.5 and L17:F3763 at activation 46.5) → probe. The probe is essentially reading off the "biconditional-style 'not only X but also Y'" template — a common NLI surface cue that correlates with intra-sentence contrast and often with contradiction — rather than the actual semantic opposition between the two sentences. So the user's concern is well-founded: this is largely a spurious-template detector, not a genuine entailment-reversal detector.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F1910](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1910) | 7 | Early-layer negation/qualification lexicon (L0-L1) |  the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1910) |
| [L1:F1500](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1500) | 3 | Early-layer negation/qualification lexicon (L0-L1) | the word "stress" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1500) |
| [L1:F1500](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1500) | 7 | Early-layer negation/qualification lexicon (L0-L1) | the word "stress" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1500) |
| [L0:F2961](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2961) | 7 | Early-layer negation/qualification lexicon (L0-L1) |  words that act as qualifications or negations, with a high preference for "necessarily" and "uncommon." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2961) |
| [L0:F15525](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15525) | 3 | Early-layer negation/qualification lexicon (L0-L1) |  places where something is being explained or reported | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15525) |
| [L2:F5627](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5627) | 7 | Mid-layer 'not only' / contrastive phrase detectors (L2-L6) |  instances of the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5627) |
| [L2:F13565](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13565) | 5 | Mid-layer 'not only' / contrastive phrase detectors (L2-L6) |  the word "program(me)s" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13565) |
| [L6:F3655](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3655) | 7 | Mid-layer 'not only' / contrastive phrase detectors (L2-L6) |  the word "just" and surrounding words | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3655) |
| [L4:F12847](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12847) | 3 | Mid-layer 'not only' / contrastive phrase detectors (L2-L6) | sentences with some reporting verb and the word 'that' | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12847) |
| [L4:F5007](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5007) | 3 | Mid-layer 'not only' / contrastive phrase detectors (L2-L6) | words and phrases used in legal contexts, like testimony and arguments, and actions such as describing someone's mood or facial expression. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5007) |
| [L3:F16191](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16191) | 3 | Mid-layer 'not only' / contrastive phrase detectors (L2-L6) |  verbs or legal names, pointing to its use in citing facts or sources | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16191) |
| [L3:F2782](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2782) | 5 | Mid-layer 'not only' / contrastive phrase detectors (L2-L6) |  references to television and news programming | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2782) |
| [L4:F6000](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6000) | 5 | Mid-layer 'not only' / contrastive phrase detectors (L2-L6) |  the word "program" and its plural form | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6000) |
| [L3:F41](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/41) | 3 | Mid-layer 'not only' / contrastive phrase detectors (L2-L6) |  citations to other papers, specifically looking for "*et al.*" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/41) |
| [L8:F8775](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8775) | 7 | Late-layer 'not only' / 'but also' contrastive concept features (L8-L15) | the word "either" (and some related words) possibly in the context of alternatives or negation | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8775) |
| [L9:F12274](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12274) | 7 | Late-layer 'not only' / 'but also' contrastive concept features (L8-L15) |  the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12274) |
| [L10:F6078](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6078) | 13 | Late-layer 'not only' / 'but also' contrastive concept features (L8-L15) |  sections where multiple ideas are being contrasted | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6078) |
| [L12:F3005](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/3005) | 7 | Late-layer 'not only' / 'but also' contrastive concept features (L8-L15) |  the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/3005) |
| [L14:F10765](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10765) | 7 | Late-layer 'not only' / 'but also' contrastive concept features (L8-L15) | the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10765) |
| [L14:F11020](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11020) | 13 | Late-layer 'not only' / 'but also' contrastive concept features (L8-L15) | the word "but". and "also" | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11020) |
| [L4:F2884](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2884) | 13 | Late-layer 'not only' / 'but also' contrastive concept features (L8-L15) | the word "but" and other contrastive conjunctions and adverbs. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2884) |
| [L4:F5347](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5347) | 13 | Late-layer 'not only' / 'but also' contrastive concept features (L8-L15) |  the conjunction "but" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5347) |
| [L15:F1990](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/1990) | 7 | Output-gating late features (L15-L17) | the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/1990) |
| [L15:F12905](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) | 13 | Output-gating late features (L15-L17) |  the word "but" along with surrounding words that indicate a contrasting or consequential relationship. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) |
| [L15:F12905](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) | 12 | Output-gating late features (L15-L17) |  the word "but" along with surrounding words that indicate a contrasting or consequential relationship. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) |
| [L16:F6005](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6005) | 7 | Output-gating late features (L15-L17) | Not only | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6005) |
| [L17:F3763](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/3763) | 7 | Output-gating late features (L15-L17) | only | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/3763) |
| [L10:F6670](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) | 31 | Hypothesis-sentence 'isn't going to improve' features (L10-L12) | technical terms, especially within scientific or medical contexts | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) |
| [L12:F12606](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) | 31 | Hypothesis-sentence 'isn't going to improve' features (L10-L12) |  phrases related to political conspiracy/organizations, mental conditions and storytelling terms | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) |
| [L11:F11267](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/11267) | 31 | Hypothesis-sentence 'isn't going to improve' features (L10-L12) |  clauses beginning with "although", certain other conjunctions (though, but), and words implying an absence of something. | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/11267) |
| [L11:F14837](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/14837) | 31 | Hypothesis-sentence 'isn't going to improve' features (L10-L12) |  a hodge-podge of terms related to chemistry, sewing, misfortune and advice | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/14837) |
| [L3:F6227](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) | 30 | Hypothesis-sentence 'isn't going to improve' features (L10-L12) |  sentence fragments and informal or ungrammatical language, often including abbreviations. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 28 | Hypothesis-sentence 'isn't going to improve' features (L10-L12) | the letter "t" when it follows the word "isn'" or "doesn'" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L7:F2088](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2088) | 31 | Hypothesis-sentence 'isn't going to improve' features (L10-L12) |  words related to business, reviews, planning and organization. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2088) |
| [L0:F8046](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8046) | 8 | Early lexical: 'will' / 'program' / 'trick' (L0-L1) |  the word "will." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8046) |
| [L1:F11907](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11907) | 5 | Early lexical: 'will' / 'program' / 'trick' (L0-L1) |  the word "program" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11907) |
| [L0:F6131](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6131) | 3 | Early lexical: 'will' / 'program' / 'trick' (L0-L1) |  the word "trick", often within the context of telling or describing a trick | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6131) |
| [L1:F1090](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1090) | 5 | Early lexical: 'will' / 'program' / 'trick' (L0-L1) |  the word "approval" and its variants | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1090) |
| [L5:F7144](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7144) | 3 | 'proper noun + said' / reporting-verb context (L3-L5) |  proper nouns followed by the word "said" | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7144) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token '0' is not one of the top-k next-token candidates capt |
| 3 | `get_top_features` | 20 features; top: L15:12905 de=-0.355 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L15:F12905@13` | ❌ error | — | — | Trace upstream from L15:F12905 at pos 13. This is the strongest negative contrib… |
| SA-2 | `L2:F13565@5` | ❌ error | — | — | Trace upstream from L2:F13565 at pos 5. Pos 5 is the token "not" — a key negatio… |
| SA-3 | `L5:F7144@3` | ❌ error | — | — | Trace upstream from L5:F7144 at pos 3. Pos 3 is the token "the". This is one of … |
| SA-4 | `L0:F8046@8` | ❌ error | — | — | Trace upstream from L0:F8046 at pos 8. Pos 8 is the token "benefit". This is a s… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×4 | L15:12905, L2:13565, L5:7144, L0:8046 |
| 2 | `get_upstream_features` | L15:F12905@13, k=10 → Emb:" only"@7 (de=5.97) +9 more |
| 3 | `get_upstream_features` | L2:F13565@5, k=10 → Emb:" program"@5 (de=16.75) +9 more |
| 4 | `get_upstream_features` | L5:F7144@3, k=10 → L3:F16191 (de=2.97) +9 more |
| 5 | `get_upstream_features` | L0:F8046@8, k=10 → Emb:" will"@8 (de=37.75) +9 more |
| 6 | `inspect_feature` ×24 | L2:5627, L9:12274, L4:2884, L14:11020, L7:4284, L6:3655, L10:6078, L3:16191, L4:12847, L0:15525, L1:11907, L0:6131, L0:2961, L1:1500, L4:5007, L3:41, L3:2782, L4:6000, L4:5347, L0:1910, L1:1090, L17:3763, L12:12606, L10:6670 |
| 7 | `get_upstream_features` | L17:F3763@7, k=10 → L15:F1990 (de=10.38) +9 more |
| 8 | `get_upstream_features` | L12:F12606@31, k=10 → Emb:"<bos>"@0 (de=6.19) +9 more |
| 9 | `get_upstream_features` | L10:F6670@31, k=10 → Emb:" improve"@31 (de=-2.97) +9 more |
| 10 | `get_upstream_features` | L15:F12905@12, k=10 → Emb:" only"@7 (de=6.91) +9 more |
| 11 | `inspect_feature` ×10 | L15:1990, L14:10765, L16:6005, L12:3005, L8:8775, L7:2088, L0:6236, L3:6227, L11:11267, L11:14837 |

### Build

`build_circuit` → 14 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 77,633 | 6,388 | 243,174 | 0 | $0.0455 | — | — |
| **Total** | | **77,633** | **6,388** | **243,174** | **0** | **$0.0455** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 20s