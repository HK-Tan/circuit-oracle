# Circuit Oracle Report
**Date:** 2026-07-28 07:23:06 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The NLI contradiction probe is driven almost entirely by shallow lexical/phrase features that detect "not only…but", "but", and "only" — the same set of contrastive-cue tokens the model uses to flag potential contradictions — rather than by features that encode the actual semantic content of the premise (Wagonheim, lawyers' public image, the program) or the hypothesis (the negated claim).

**Confidence:** 6

**Reasoning:** Tracing the top probe-driving features reveals that the entire attribution graph is dominated by **lexical phrase detectors** that fire on the input surface form. The two strongest drivers are:

- **L15:F12905** ("but" + contrastive/consequential relationship, direct_effect = **−0.36** at pos 13 and −0.15 at pos 12; frac_nonzero = 0.005). This is a "but" detector — its top activating examples are all sentences containing "but" in a contrasting relationship, and its promoted tokens are "also/Also" (the canonical "not only…but also" continuation). Critically, its direct_effect on the contradiction probe is **negative**, not positive — so the "but" cue by itself actually *suppresses* the contradiction score.
- **L17:F3763** ("only" word detector, direct_effect = **+0.17** at pos 7; frac_nonzero = 0.072). This fires on the word "only" — every top example is "not only…", "only the value for…", "only is it a collection…" — a pure single-word detector.

The **embedding nodes** the circuit reaches are pure surface tokens: "not" (pos 6, direct_effect +3.97 to F3763), "only" (pos 7), "but" (pos 13, direct_effect +4 to F12905), "program" (pos 5), "said" (pos 3), "will" (pos 8), "isn" (pos 26 in hypothesis), and "improve" (pos 31). The "not only" detector F5627 (L2) is a pure pattern matcher — its top activating examples are all "not only…but also" constructions with no semantic content about the entities involved.

The mid-layer supernode `mid_phrase_features` (L4–L11) contains the same family of contrastive markers: F2884 (L4) "but and other contrastive conjunctions", F3655 (L6) "just" with promoted tokens like "nejen" (Czech for "not only") — again a phrase-construction detector, F11267 (L11) "although/though/but…words implying absence of something". The early-layer `early_phrase_features` is full of "program/programmes/TV news program" detectors (F13565, F1560, F11907, F6000, F2782) — features that fire on the noun "program" regardless of who benefits or what it does.

**Crucially, the graph does not surface any feature that semantically encodes** the actual content of the contradiction: that the hypothesis ("The program isn't going to improve lawyers' public image") negates a specific claim from the premise ("…will help improve the public image of lawyers"). The "not" / "isn't" embeddings feed only into the same generic negation-word detectors (F6236 "the letter 't' when it follows 'isn''", F11267 "words implying absence") that fire on any negation anywhere. The entity tokens "Wagonheim", "heim", "lawyers" have negligible direct_effect on any of the top features (e.g., "Wagon" has +0.13, "heim" has −0.04 to F8046).

**Confirming the user's concern:** Yes — the circuit is largely spurious. It runs almost entirely on:
1. The **"not only…but also" surface pattern** (F5627, F12274, F3655, F6005, F10765, F1990, F3005) — a syntactic construction that's common in premise sentences and correlates with NLI contradictions in training data simply because contradictions are often set up with "X, not Y, but Z" framing.
2. The **single word "but"** (F12905, F2557, F11020, F10235, F11101) — a contrastive cue that fires on any contrast, regardless of whether the contrast is between premise and hypothesis or within a single sentence.
3. The **word "only"** (F3763) — a word-level detector with no semantic content.
4. The **word "program"** (F13565, F11907, F6000, F2782) — a generic noun detector.
5. The **word "will"** (F8046, direct_effect = −0.27) — a modal-verb detector that pushes against the contradiction score.
6. The **"said" reporting-verb pattern** (F12847, F16191) and the second-sentence "isn" negation (F6236) — pure surface patterns.

**Net mechanism:** the probe is picking up on the surface form *"not only X, but also Y"* in the premise, combined with the word *"isn't"* in the hypothesis, and — paradoxically — being *suppressed* by the actual "but" token. The most positive contributions come from "only" (L17) and the "not only" pattern detectors at the "only" position (L14, L15, L16), and the "improve" embedding in the hypothesis gets a small direct effect of −3.89 to L12:F12606. There is no feature in the top-15 list that recognizes that "lawyers' public image" or "the program" is the shared argument between premise and hypothesis.

The user's hypothesis is therefore **substantially correct for this particular attribution graph**: the contradiction probe is being driven by generic negation/contrastive lexical cues rather than by features that recognize the actual semantic relationship (or contradiction) between the premise's claim and the hypothesis's negation of it. This is a classic artifact: a probe trained on NLI supervision learns that *contradiction in NLI is correlated with the presence of words like "not", "but", "only", and "isn't"*, so it relies on those surface cues. On this SNLI-style sentence pair, the pattern "not only… but also…" in the premise combined with "isn't" in the hypothesis is exactly the kind of input where the probe would confidently fire contradiction even if the entities and propositions were swapped around — it is not reading the contradiction, it is pattern-matching the form.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L15:F1990](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/1990) | 7 | Late-layer "not only" / "but" phrase detectors (drive probe positively) | the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/1990) |
| [L14:F10765](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10765) | 7 | Late-layer "not only" / "but" phrase detectors (drive probe positively) | the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10765) |
| [L16:F6005](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6005) | 7 | Late-layer "not only" / "but" phrase detectors (drive probe positively) | Not only | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6005) |
| [L12:F3005](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/3005) | 7 | Late-layer "not only" / "but" phrase detectors (drive probe positively) |  the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/3005) |
| [L15:F12905](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) | 13 | "but" + contrastive phrase (L12-L15) — drives probe NEGATIVELY |  the word "but" along with surrounding words that indicate a contrasting or consequential relationship. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) |
| [L13:F2557](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/2557) | 13 | "but" + contrastive phrase (L12-L15) — drives probe NEGATIVELY |  occurrences of the word "but" and words that often appear near it | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/2557) |
| [L14:F11020](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11020) | 13 | "but" + contrastive phrase (L12-L15) — drives probe NEGATIVELY | the word "but". and "also" | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11020) |
| [L12:F10235](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/10235) | 13 | "but" + contrastive phrase (L12-L15) — drives probe NEGATIVELY |  the word "but", especially when preceded by a comma | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/10235) |
| [L17:F3763](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/3763) | 7 | "only" word detector (L17, drives probe +) | only | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/3763) |
| [L9:F12274](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12274) | 7 | Mid-layer phrase / contrast detectors |  the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12274) |
| [L7:F4284](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4284) | 13 | Mid-layer phrase / contrast detectors | instances of parenthetical commas and phrases | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4284) |
| [L6:F3655](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3655) | 7 | Mid-layer phrase / contrast detectors |  the word "just" and surrounding words | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3655) |
| [L4:F2884](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2884) | 13 | Mid-layer phrase / contrast detectors | the word "but" and other contrastive conjunctions and adverbs. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2884) |
| [L11:F11267](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/11267) | 31 | Mid-layer phrase / contrast detectors |  clauses beginning with "although", certain other conjunctions (though, but), and words implying an absence of something. | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/11267) |
| [L2:F5627](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5627) | 7 | Early-layer "not only" / "but" detectors + lexical features |  instances of the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5627) |
| [L2:F3379](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3379) | 13 | Early-layer "not only" / "but" detectors + lexical features |  the word "but" and similar terms | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3379) |
| [L2:F13565](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13565) | 5 | Early-layer "not only" / "but" detectors + lexical features |  the word "program(me)s" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13565) |
| [L2:F1560](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1560) | 5 | Early-layer "not only" / "but" detectors + lexical features |  the word "program" in the context of technical computer operation discussions | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1560) |
| [L1:F11907](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11907) | 5 | Early-layer "not only" / "but" detectors + lexical features |  the word "program" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11907) |
| [L4:F6000](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6000) | 5 | Early-layer "not only" / "but" detectors + lexical features |  the word "program" and its plural form | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6000) |
| [L3:F2782](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2782) | 5 | Early-layer "not only" / "but" detectors + lexical features |  references to television and news programming | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2782) |
| [L1:F1500](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1500) | 3 | Early-layer "not only" / "but" detectors + lexical features | the word "stress" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1500) |
| [L1:F1500](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1500) | 7 | Early-layer "not only" / "but" detectors + lexical features | the word "stress" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1500) |
| [L0:F11101](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11101) | 13 | Early-layer "not only" / "but" detectors + lexical features | sentences that contain the word "but" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11101) |
| [L0:F15525](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15525) | 3 | Early-layer "not only" / "but" detectors + lexical features |  places where something is being explained or reported | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15525) |
| [L4:F12847](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12847) | 3 | Early-layer "not only" / "but" detectors + lexical features | sentences with some reporting verb and the word 'that' | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12847) |
| [L3:F16191](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16191) | 3 | Early-layer "not only" / "but" detectors + lexical features |  verbs or legal names, pointing to its use in citing facts or sources | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16191) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 28 | Early-layer "not only" / "but" detectors + lexical features | the letter "t" when it follows the word "isn'" or "doesn'" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L5:F7144](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7144) | 3 | Positive lexical-context features (help contradiction) |  proper nouns followed by the word "said" | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7144) |
| [L0:F6131](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6131) | 3 | Positive lexical-context features (help contradiction) |  the word "trick", often within the context of telling or describing a trick | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6131) |
| [L0:F8046](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8046) | 8 | "will" word feature (L0) — pushes AGAINST probe |  the word "will." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8046) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: 'not' (pos 6) — negation word | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: 'only' (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: 'but' (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: 'program' (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: 'said' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: 'will' (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 31 | Emb: 'improve' (pos 31) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 26 | Emb: 'isn' (pos 26) — second-sentence negation | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 0 | Emb: BOS / start (pos 0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L15:12905 de=-0.355 |
| 3 | `inspect_feature` ×10 | L15:12905, L0:8046, L5:7144, L2:13565, L4:12847, L3:2782, L0:15525, L17:3763, L1:1500, L0:6131 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L15:F12905@13` | ❌ error | — | — | Trace the path upstream from L15:F12905 (the "but" feature) at position 13. This… |
| SA-2 | `L17:F3763@7` | ❌ error | — | — | Trace the path upstream from L17:F3763 (the "only" feature) at position 7. This … |
| SA-3 | `L3:F2782@5` | ❌ error | — | — | Trace the path upstream from L3:F2782 (TV/news program feature) at position 5. T… |
| SA-4 | `L0:F8046@8` | ❌ error | — | — | Trace the path upstream from L0:F8046 (the word "will" feature) at position 8. T… |
| SA-5 | `L5:F7144@3` | ❌ error | — | — | Trace the path upstream from L5:F7144 (proper noun + "said" feature) at position… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L15:F12905@13, k=10 → Emb:" only"@7 (de=5.97) +9 more |
| 2 | `get_upstream_features` | L17:F3763@7, k=10 → L15:F1990 (de=10.38) +9 more |
| 3 | `get_upstream_features` | L3:F2782@5, k=10 → Emb:" program"@5 (de=27.00) +9 more |
| 4 | `get_upstream_features` | L0:F8046@8, k=10 → Emb:" will"@8 (de=37.75) +9 more |
| 5 | `get_upstream_features` | L5:F7144@3, k=10 → L3:F16191 (de=2.97) +9 more |
| 6 | `get_upstream_features` | L2:F5627@7, k=8 → Emb:" only"@7 (de=21.25) +7 more |
| 7 | `get_upstream_features` | L9:F12274@7, k=8 → L6:F3655 (de=9.19) +7 more |
| 8 | `get_upstream_features` | L6:F3655@7, k=8 → Emb:" only"@7 (de=8.94) +7 more |
| 9 | `get_upstream_features` | L15:F1990@7, k=8 → Emb:" not"@6 (de=9.69) +7 more |
| 10 | `get_upstream_features` | L14:F10765@7, k=8 → L9:F12274 (de=8.06) +7 more |
| 11 | `get_upstream_features` | L4:F2884@13, k=6 → Emb:" but"@13 (de=17.75) +5 more |
| 12 | `get_upstream_features` | L14:F11020@13, k=6 → L13:F2557 (de=9.75) +5 more |
| 13 | `get_upstream_features` | L7:F4284@13, k=6 → Emb:" but"@13 (de=7.19) +5 more |
| 14 | `get_upstream_features` | L16:F6005@7, k=6 → L15:F1990 (de=12.25) +5 more |
| 15 | `get_upstream_features` | L12:F12606@31, k=6 → Emb:"<bos>"@0 (de=6.19) +5 more |
| 16 | `get_upstream_features` | L13:F2557@13, k=6 → L12:F10235 (de=6.09) +5 more |
| 17 | `get_upstream_features` | L4:F6000@5, k=6 → Emb:" program"@5 (de=21.62) +5 more |
| 18 | `get_upstream_features` | L12:F10235@13, k=6 → Emb:" but"@13 (de=4.69) +5 more |
| 19 | `get_upstream_features` | L12:F3005@7, k=6 → L9:F12274 (de=10.75) +5 more |
| 20 | `get_upstream_features` | L4:F6000@5, k=6 → Emb:" program"@5 (de=21.62) +5 more |
| 21 | `inspect_feature` ×31 | L2:5627, L9:12274, L6:3655, L15:1990, L14:10765, L4:2884, L14:11020, L7:4284, L16:6005, L4:6000, L12:3005, L12:10235, L13:2557, L1:11907, L3:16191, L1:1500, L0:15525, L4:12847, L3:2782, L2:1560, L2:3379, L0:11101, L2:13565, L17:3763, L15:12905, L5:7144, L12:12606, L0:8046, L0:6131, L0:6236, L11:11267 |

### Build

`build_circuit` → 17 nodes, 17 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 99,310 | 11,076 | 288,339 | 0 | $0.0604 | — | — |
| **Total** | | **99,310** | **11,076** | **288,339** | **0** | **$0.0604** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 2s