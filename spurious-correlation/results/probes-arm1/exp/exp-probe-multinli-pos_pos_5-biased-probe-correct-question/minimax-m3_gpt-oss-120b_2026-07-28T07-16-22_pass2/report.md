# Circuit Oracle Report
**Date:** 2026-07-28 07:16:22 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The NLI contradiction probe is driven almost entirely by surface-level negation/contrast lexical signals (not, only, isn't, but) at the input token positions, with no engagement of entity-level or propositional content features about the "program", "lawyers", or "image" concepts that would be needed to actually resolve the entailment between premise and hypothesis.

**Confidence:** 8

**Reasoning:**

The circuit traces cleanly from the probe's output logit backward through late-layer negation features down to the input tokens "not" (pos 6), "only" (pos 7), "but" (pos 13), and "isn"+"t" (pos 26-28), with virtually no contribution from the rest of the prompt. This confirms the user's concern: the probe is relying on spurious, generic lexical patterns rather than on any semantic understanding of the proposition.

**Token-embedding root nodes (all early-layer):**
- Emb: "not" (pos 6), Emb: "only" (pos 7) — premise "not only… benefit the needy"
- Emb: "but" (pos 13) — contrast "but also…"
- Emb: "isn" (pos 26), Emb: "t" (pos 28) — hypothesis "isn't going to improve"
- Emb: "program" (pos 5), Emb: "said" (pos 3) — minor upstream contributions

**Low/mid-layer supernodes encoding the lexical patterns:**
- *not_letter_only_low* (L0-L1, pos 5-7): L0:F4958 "not", L0:F1910 "not only", L0:F12483 "only", L0:F4723 "only", L1:F11907 "program", L0:F14950 "program". frac_nonzero 0.001-0.027. These are all surface-string detectors for the words "not" and "only".
- *but_mid_low* (L0-L4, pos 13): L0:F11101 "but", L2:F3379 "but", L4:F2884 "but", L10:F6078 "contrastive sections". All fire on the literal conjunction "but".
- *isnt_letter_t_low* (L0-L4, pos 26-28): L0:F6236 "the letter t after isn'", L1:F423 "words that negate a following word", L2:F7654 "the letter t with preference for negative emotions", L4:F4492/L4:F2422 "negations in other languages" (these are actually weirdly multilingual, but they fire on the "isn't" token here). Activated by Emb "isn" + Emb "t".

**Mid-layer phrase-level features:**
- *not_only_mid* (L2-L9, pos 7): L2:F5627 "not only", L4:F11560 "not only", L6:F3655 "just and surrounding words", L9:F12274 "not only". Each frac_nonzero 0.003-0.013 — these are very specific phrase detectors that simply recognize the string "not only" without semantic role.
- *speech_attr_l4* (L4, pos 3): L4:F15629 "speech attribution (said)" — the only feature encoding something about the content of the sentence (a person reporting speech). Direct effect +0.67, but it is isolated and not integrated with the rest of the circuit.

**Late-layer features driving the probe directly (L13-L16):**
- *late_neg_chain_pos6* (L13-L16, pos 6): L13:F4368 "not", L14:F2476 "negative polarity", L15:F15779 "hedging language", L16:F15025 "not combined with pronouns / emotional language". Direct effect +0.32. These are general-purpose negation/polarity detectors that have no idea what the negation applies to.
- *contrast_but_features* (L12-L15, pos 13): L12:F10235 "but (preceded by comma)", L13:F2557 "but and surrounding words", L14:F11020 "but/also", L15:F12905 "but with contrasting relationship". Direct effect -0.32 (inhibits the probe; "but" actually pushes against contradiction here, perhaps because it normally signals elaboration rather than opposition). The promoted token for F12905 is "also", confirming it's a "not only… but also" detector.
- *late_neg_chain_pos28* (L13-L16, pos 28): L13:F3295 "is/are not", L13:F851 "letter t / negative HTML tags", L14:F13077 "negations", L15:F10071 "negations and equivocations", L16:F12358 "not followed by a form of to be". Direct effect +0.37. This is the "isn't" chain in the hypothesis.

**Quantitative attribution analysis (get_source_influence):**
- Positions 6,7,13 ("not", "only", "but") → S_pct_of_total = 16.6%, S_over_R = 1.65. These positions carry a substantial, signed, multi-hop share — the probe is being driven by them.
- Positions 26,28 ("isn", "t" of "isn't") → S_pct_of_total = 19.3%, S_over_R = 1.74. Same story on the hypothesis side.
- All other positions (1-5, 8-25, 27 — including "lawyers", "image", "public", "needy", "program", "going to improve") → S_pct_of_total = 2.7%, S_over_R = 0.24. These are negligible. The content-bearing words of the sentence contribute essentially nothing to the probe's contradiction score.

**Interpretation:** The probe fires "contradiction" because Gemma-2-2B's late layers (L13-L16) contain features that detect generic patterns of negation ("not", "isn't", "hedging", "negative polarity") and contrast ("but also"). Both premise ("not only… but also") and hypothesis ("isn't going to improve") trigger these features, and their activation in *parallel* rather than their propositional relationship is what the linear probe latches onto. Critically, there is no feature in the circuit that encodes (a) what the program does (benefit the needy / improve image), (b) that the two sentences share the same subject ("program"/"lawyers' image"), or (c) the actual semantic opposition between the premise's positive claim and the hypothesis's negated claim. A swap of "lawyers" for "doctors" or "isn't going to" for "is going to" would likely flip the probe's score even though the entailment relationship has not been assessed. This confirms the user's hypothesis: the circuit uses spurious negation/contrast lexical signals rather than prompt content to predict contradiction.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 31 | NLI probe (contradiction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L13:F3295](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) | 28 | Late negation features at "isn't" (pos 28, L13-L16) | negations in the form of "is/are not" as well as other uses of "not" | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) |
| [L13:F851](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/851) | 28 | Late negation features at "isn't" (pos 28, L13-L16) | the letter "t" with high activation, and also finds words indicating something negative or the end of an HTML tag. | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/851) |
| [L14:F13077](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/13077) | 28 | Late negation features at "isn't" (pos 28, L13-L16) | negations. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/13077) |
| [L15:F10071](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) | 28 | Late negation features at "isn't" (pos 28, L13-L16) | negations and equivocations | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) |
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 28 | Late negation features at "isn't" (pos 28, L13-L16) |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |
| [L13:F4368](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/4368) | 6 | Late negation features at "not" (pos 6, L13-L16) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/4368) |
| [L14:F2476](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/2476) | 6 | Late negation features at "not" (pos 6, L13-L16) | negative polarity, sometimes in the context of politics or social issues | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/2476) |
| [L15:F15779](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15779) | 6 | Late negation features at "not" (pos 6, L13-L16) |  hedging language | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15779) |
| [L16:F15025](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15025) | 6 | Late negation features at "not" (pos 6, L13-L16) |  usage of the word "not" combined with personal pronouns or related emotional or motivational language | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15025) |
| [L12:F10235](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/10235) | 13 | Contrast/but features at "but" (pos 13, L12-L15) |  the word "but", especially when preceded by a comma | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/10235) |
| [L13:F2557](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/2557) | 13 | Contrast/but features at "but" (pos 13, L12-L15) |  occurrences of the word "but" and words that often appear near it | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/2557) |
| [L14:F11020](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11020) | 13 | Contrast/but features at "but" (pos 13, L12-L15) | the word "but". and "also" | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11020) |
| [L15:F12905](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) | 13 | Contrast/but features at "but" (pos 13, L12-L15) |  the word "but" along with surrounding words that indicate a contrasting or consequential relationship. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) |
| [L2:F5627](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5627) | 7 | Mid-layer "not only" features at pos 7 (L2, L4, L6, L9) |  instances of the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5627) |
| [L4:F11560](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11560) | 7 | Mid-layer "not only" features at pos 7 (L2, L4, L6, L9) | the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11560) |
| [L6:F3655](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3655) | 7 | Mid-layer "not only" features at pos 7 (L2, L4, L6, L9) |  the word "just" and surrounding words | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3655) |
| [L9:F12274](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12274) | 7 | Mid-layer "not only" features at pos 7 (L2, L4, L6, L9) |  the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12274) |
| [L0:F11101](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11101) | 13 | Mid/low-layer contrast features at "but" (pos 13, L0-L4) | sentences that contain the word "but" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11101) |
| [L2:F3379](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3379) | 13 | Mid/low-layer contrast features at "but" (pos 13, L0-L4) |  the word "but" and similar terms | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3379) |
| [L4:F2884](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2884) | 13 | Mid/low-layer contrast features at "but" (pos 13, L0-L4) | the word "but" and other contrastive conjunctions and adverbs. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2884) |
| [L10:F6078](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6078) | 13 | Mid/low-layer contrast features at "but" (pos 13, L0-L4) |  sections where multiple ideas are being contrasted | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6078) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 28 | Low-layer "isn't" / negation letter features at pos 26-28 (L0-L3) | the letter "t" when it follows the word "isn'" or "doesn'" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L1:F423](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/423) | 28 | Low-layer "isn't" / negation letter features at pos 26-28 (L0-L3) |  words that negate a following word or phrase. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/423) |
| [L2:F7654](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7654) | 28 | Low-layer "isn't" / negation letter features at pos 26-28 (L0-L3) |  the letter 't', but with some preference for words related to negative emotions or needs | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7654) |
| [L3:F6227](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) | 30 | Low-layer "isn't" / negation letter features at pos 26-28 (L0-L3) |  sentence fragments and informal or ungrammatical language, often including abbreviations. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 28 | Low-layer "isn't" / negation letter features at pos 26-28 (L0-L3) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 28 | Low-layer "isn't" / negation letter features at pos 26-28 (L0-L3) | negations in other languages like French, Malay, and Croatian | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 6 | Low-layer "not" / "only" features at pos 5-7 (L0-L1) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F1910](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1910) | 7 | Low-layer "not" / "only" features at pos 5-7 (L0-L1) |  the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1910) |
| [L0:F12483](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12483) | 7 | Low-layer "not" / "only" features at pos 5-7 (L0-L1) | the word "only" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12483) |
| [L0:F4723](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4723) | 7 | Low-layer "not" / "only" features at pos 5-7 (L0-L1) |  the word "only" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4723) |
| [L1:F11907](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11907) | 5 | Low-layer "not" / "only" features at pos 5-7 (L0-L1) |  the word "program" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11907) |
| [L0:F14950](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14950) | 5 | Low-layer "not" / "only" features at pos 5-7 (L0-L1) |  instances of the word "program" and the word "step" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14950) |
| [L4:F15629](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15629) | 3 | Speech attribution feature at "said" (pos 3, L4) |  speech attribution, such as the word "said" and phrases like "talking about" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15629) |
| [L4:F12337](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12337) | 3 | Speech attribution feature at "said" (pos 3, L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12337) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: "not" (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: "only" (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: "but" (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 26 | Emb: "isn" (pos 26) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 28 | Emb: "t" (pos 28) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: "said" (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: "program" (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:15629 de=0.672 |
| 3 | `inspect_feature` ×8 | L4:15629, L2:5627, L0:6236, L16:12358, L0:14950, L1:11907, L16:15025, L15:12905 |
| 4 | `get_upstream_features` | Emb:" said"@3 (de=34.25) +9 more |
| 5 | `get_upstream_features` | Emb:" only"@7 (de=21.25) +9 more |
| 6 | `get_upstream_features` | Emb:" isn"@26 (de=23.38) +9 more |
| 7 | `get_upstream_features` | Emb:"t"@28 (de=12.69) +9 more |
| 8 | `get_upstream_features` | Emb:" only"@7 (de=5.97) +9 more |
| 9 | `get_upstream_features` | Emb:" not"@6 (de=12.19) +9 more |
| 10 | `get_upstream_features` | Emb:" said"@3 (de=28.00) +9 more |
| 11 | `get_upstream_features` | Emb:" program"@5 (de=24.38) +9 more |
| 12 | `get_upstream_features` | Emb:" program"@5 (de=23.25) +9 more |
| 13 | `get_upstream_features` | Emb:" to"@30 (de=6.00) +9 more |
| 14 | `get_upstream_features` | Emb:"t"@28 (de=12.69) +14 more |
| 15 | `get_upstream_features` | Emb:" not"@6 (de=12.19) +9 more |
| 16 | `get_upstream_features` | Emb:" only"@7 (de=5.97) +9 more |
| 17 | `inspect_feature` ×2 | L3:6227, L0:15525 |
| 18 | `get_upstream_features` | L0:F6236 (de=5.16) +7 more |
| 19 | `get_upstream_features` | Emb:" not"@6 (de=15.25) +7 more |
| 20 | `get_upstream_features` | Emb:" not"@6 (de=32.00) +7 more |
| 21 | `get_upstream_features` | L6:F3655 (de=9.19) +7 more |
| 22 | `get_upstream_features` | Emb:" but"@13 (de=17.75) +7 more |
| 23 | `get_upstream_features` | L13:F2557 (de=9.75) +7 more |
| 24 | `get_upstream_features` | Emb:" not"@6 (de=14.25) +7 more |
| 25 | `get_upstream_features` | L14:F2476 (de=10.31) +7 more |
| 26 | `get_upstream_features` | Emb:" isn"@26 (de=14.00) +7 more |
| 27 | `get_upstream_features` | L0:F6236 (de=7.81) +7 more |
| 28 | `get_upstream_features` | L0:F6236 (de=6.69) +7 more |
| 29 | `get_upstream_features` | Emb:" isn"@26 (de=10.31) +7 more |
| 30 | `inspect_feature` ×12 | L15:10071, L13:4368, L0:4958, L9:12274, L4:2884, L14:11020, L14:2476, L15:15779, L1:423, L13:851, L13:3295, L2:7654 |
| 31 | `get_upstream_features` | L12:F10235 (de=6.09) +7 more |
| 32 | `get_upstream_features` | Emb:" only"@7 (de=8.94) +7 more |
| 33 | `get_upstream_features` | L0:F6236 (de=7.28) +7 more |
| 34 | `get_upstream_features` | Emb:" but"@13 (de=4.69) +7 more |
| 35 | `get_upstream_features` | Emb:" but"@13 (de=42.50) +7 more |
| 36 | `get_upstream_features` | Emb:" but"@13 (de=20.75) +7 more |
| 37 | `inspect_feature` ×10 | L13:2557, L6:3655, L14:13077, L12:10235, L0:11101, L2:3379, L2:13565, L5:2329, L2:8279, L0:1910 |
| 38 | `get_upstream_features` | L2:F5627 (de=9.88) +4 more |
| 39 | `get_upstream_features` | Emb:" but"@13 (de=5.69) +4 more |
| 40 | `inspect_feature` ×9 | L4:11560, L10:12520, L4:2422, L1:2493, L4:4492, L0:12318, L0:12483, L0:4723, L10:6078 |
| 41 | `rank_segment_features` | ❌ This tool requires ctx.sibling_graphs to be set (at least on |
| 42 | `get_source_influence` | {'depth': 3, 'source_positions': [6, 7, 13], 'S_pct_of_total': 16.551, 'R_pct_of |
| 43 | `get_source_influence` | {'depth': 3, 'source_positions': [26, 28], 'S_pct_of_total': 19.261, 'R_pct_of_t |
| 44 | `get_source_influence` | {'depth': 3, 'source_positions': [1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 14, 15, 16, 1 |

### Build

`build_circuit` → 16 nodes, 17 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 101,986 | 8,822 | 475,159 | 0 | $0.0697 | — | — |
| **Total** | | **101,986** | **8,822** | **475,159** | **0** | **$0.0697** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 5s