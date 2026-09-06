# Circuit Oracle Report
**Date:** 2026-07-28 07:11:55 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction score is driven by a stack of "not only … but" contrast/conjunction features (and the standalone "only" token) that fire on lexical contrast markers in the premise rather than encoding any entity-level, world-knowledge, or entailment signal. A separate, smaller contribution comes from a "Wagonheim said" / "program will" attribution cluster that picks up the proper-noun-plus-said reporting pattern.

**Confidence:** 8

**Reasoning:** 

The terminal of the circuit is the L17 feature 3763 ("only" with promoted tokens "▁but"/"but" — it explicitly *wants* to say "but" next) at position 7, which directly drives the probe with frac_nonzero 0.072 and is the strongest positive late-layer signal. It is fed by a whole tower of phrase detectors — L16:F6005 ("Not only"), L15:F1990 ("not only") and L15:F12905 ("the word 'but' along with surrounding words that indicate a contrasting or consequential relationship" — promoted tokens: also/Also/également), L14:F10765 ("not only") and L14:F11020 ("but"/"also"), L12:F3005 ("not only"), L9:F12274 ("not only") — all of which are themselves driven by L2:F5627 ("instances of the phrase 'not only'", frac_nonzero 0.0069, very specific), and ultimately by the raw " not" (pos 6) and " only" (pos 7) token embeddings (direct_effect ≈ 19–21 each at L2). A parallel arm goes L2:F4481 ("but") → L4:F5347 ("but")/F2884 ("but and other contrastive conjunctions") → L4 also gets direct excitation from the " but" embedding at pos 13. Other low-layer phrase detectors (L0:F1910 "not only" with frac_nonzero 0.018, L0:F2961 "qualifications or negations… 'necessarily'/'uncommon'") and the suppression-side L1:F1500 ("stress") further reinforce the "only"-position.

The corroborating evidence is decisive: virtually every feature in the high-positive direct_effect column encodes (a) the literal token "only", (b) the literal token "not", (c) the literal token "but", or (d) the multi-word phrase "not only" or "not only … but also". Frac_nonzero values for the phrase detectors are all very low (0.003–0.018), meaning these are highly specific lexical matchers, not semantic entailment computations. There is no feature in the top-20 by direct_effect that encodes semantic content about lawyers, image, programs, beneficiaries, or any entity — the only entity-touching feature (L5:F7144, "proper nouns followed by 'said'") is a generic attribution pattern that fires on *any* person-plus-said construction, not on the substantive content of the premise or hypothesis. The two purely-lexical "improvement" features (L10:F6670 technical terms; L12:F12606 political/mental/storytelling) at position 31 are the only items reading the final sentence's "improve" — and even they are fired by the token itself with misc suppressed tokens, not by entailment reasoning.

**This validates the user's concern.** The contradiction probe is largely a shallow lexical detector: when the premise contains the contrastive construction "not only … but also" plus the negation pattern "isn't going to", the residual stream activations for the "only"/"but"/"not"/"said"/"will" tokens create a strong signal in the contrast-phrase features, and the linear probe reads that contrast signal as "contradiction." The probe is not picking up genuine semantic incompatibility between the two sentences (which would require features for "public image of lawyers" or entailment-over-improve); it is picking up that the input *looks like* the kind of text where one claim is being contrasted with another. The same features would fire with similar magnitude on any "X said the program not only will benefit A, but also B" sentence regardless of whether the second sentence actually contradicts the first. The user's worry that the circuit uses spurious negation/contrast-lexical signals rather than prompt content is correct.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F1910](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1910) | 7 | Layer 0: \"not only\" phrase detector (F1910 @7) and negation/qualifier (F2961 @7) |  the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1910) |
| [L0:F2961](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2961) | 7 | Layer 0: \"not only\" phrase detector (F1910 @7) and negation/qualifier (F2961 @7) |  words that act as qualifications or negations, with a high preference for "necessarily" and "uncommon." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2961) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 6 | Layer 0: \"not only\" phrase detector (F1910 @7) and negation/qualifier (F2961 @7) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F4723](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4723) | 7 | Layer 0: \"only\" token detector (F4723 @7, F12483 @7) |  the word "only" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4723) |
| [L0:F12483](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12483) | 7 | Layer 0: \"only\" token detector (F4723 @7, F12483 @7) | the word "only" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12483) |
| [L0:F8046](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8046) | 8 | Layer 0: \"will\" token detector (F8046 @8) |  the word "will." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8046) |
| [L1:F1090](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1090) | 5 | Layer 0: \"program\" / plan token (F1090 @5) |  the word "approval" and its variants | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1090) |
| [L0:F7448](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7448) | 5 | Layer 0: \"program\" / plan token (F1090 @5) |  the word "program" related to sports, school, health, or television | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7448) |
| [L0:F1982](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1982) | 5 | Layer 0: \"program\" / plan token (F1090 @5) | the word "program" or similar words like "card" or "project". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1982) |
| [L0:F15525](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15525) | 3 | Layer 0: \"said\" reporting-verb detector (F15525 @3, F6131 @3, F10875 @3) |  places where something is being explained or reported | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15525) |
| [L0:F10875](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10875) | 3 | Layer 0: \"said\" reporting-verb detector (F15525 @3, F6131 @3, F10875 @3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10875) |
| [L0:F6131](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6131) | 3 | Layer 0: \"said\" reporting-verb detector (F15525 @3, F6131 @3, F10875 @3) |  the word "trick", often within the context of telling or describing a trick | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6131) |
| [L0:F437](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/437) | 1 | Layer 0: Proper-name / surname detector (F437 @1) |  words that are names or titles of things, or otherwise capitalized non-nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/437) |
| [L0:F4789](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4789) | 2 | Layer 0: Proper-name / surname detector (F437 @1) |  names, especially last names, which often contain "thaler" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4789) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 28 | Layer 0: \"isn'\" + \"t\" contraction marker (F6236 @28) | the letter "t" when it follows the word "isn'" or "doesn'" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L1:F1500](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1500) | 7 | Layer 1: high-activation \"stress\"/qualifier (F1500 @7) | the word "stress" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1500) |
| [L1:F1500](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1500) | 3 | Layer 1: high-activation \"stress\"/qualifier (F1500 @7) | the word "stress" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1500) |
| [L1:F11907](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11907) | 5 | Layer 1: \"program\" token detector (F11907 @5) |  the word "program" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11907) |
| [L2:F5627](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5627) | 7 | Layer 2: \"not only\" phrase detector (F5627 @7); \"but\" (F4481, F5434 @13) |  instances of the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5627) |
| [L2:F13565](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13565) | 5 | Layer 2: \"not only\" phrase detector (F5627 @7); \"but\" (F4481, F5434 @13) |  the word "program(me)s" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13565) |
| [L2:F4481](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4481) | 13 | Layer 2: \"not only\" phrase detector (F5627 @7); \"but\" (F4481, F5434 @13) | the word "but" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4481) |
| [L2:F5434](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5434) | 13 | Layer 2: \"not only\" phrase detector (F5627 @7); \"but\" (F4481, F5434 @13) | sentences that use the phrase "but rather" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5434) |
| [L3:F2782](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2782) | 5 | Layer 3: TV/news program references (F2782 @5); citations (F16191 @3); et al (F41 @3) |  references to television and news programming | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2782) |
| [L3:F16191](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16191) | 3 | Layer 3: TV/news program references (F2782 @5); citations (F16191 @3); et al (F41 @3) |  verbs or legal names, pointing to its use in citing facts or sources | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16191) |
| [L3:F41](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/41) | 3 | Layer 3: TV/news program references (F2782 @5); citations (F16191 @3); et al (F41 @3) |  citations to other papers, specifically looking for "*et al.*" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/41) |
| [L3:F6227](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) | 30 | Layer 3: TV/news program references (F2782 @5); citations (F16191 @3); et al (F41 @3) |  sentence fragments and informal or ungrammatical language, often including abbreviations. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) |
| [L3:F3755](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3755) | 13 | Layer 3: TV/news program references (F2782 @5); citations (F16191 @3); et al (F41 @3) |  the word "claim" or the french word "que" in addition to other seemingly random words | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3755) |
| [L4:F5347](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5347) | 13 | Layer 4: \"but\" conjunction (F5347 @13); contrast (F2884 @13); reporting + that (F12847 @3, F14393 @3); legal (F5007 @3); program (F6000 @5); non-en neg (F2422 @28) |  the conjunction "but" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5347) |
| [L4:F2884](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2884) | 13 | Layer 4: \"but\" conjunction (F5347 @13); contrast (F2884 @13); reporting + that (F12847 @3, F14393 @3); legal (F5007 @3); program (F6000 @5); non-en neg (F2422 @28) | the word "but" and other contrastive conjunctions and adverbs. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2884) |
| [L4:F12847](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12847) | 3 | Layer 4: \"but\" conjunction (F5347 @13); contrast (F2884 @13); reporting + that (F12847 @3, F14393 @3); legal (F5007 @3); program (F6000 @5); non-en neg (F2422 @28) | sentences with some reporting verb and the word 'that' | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12847) |
| [L4:F14393](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14393) | 3 | Layer 4: \"but\" conjunction (F5347 @13); contrast (F2884 @13); reporting + that (F12847 @3, F14393 @3); legal (F5007 @3); program (F6000 @5); non-en neg (F2422 @28) |  direct quotes or reports of people speaking | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14393) |
| [L4:F5007](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5007) | 3 | Layer 4: \"but\" conjunction (F5347 @13); contrast (F2884 @13); reporting + that (F12847 @3, F14393 @3); legal (F5007 @3); program (F6000 @5); non-en neg (F2422 @28) | words and phrases used in legal contexts, like testimony and arguments, and actions such as describing someone's mood or facial expression. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5007) |
| [L4:F6000](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6000) | 5 | Layer 4: \"but\" conjunction (F5347 @13); contrast (F2884 @13); reporting + that (F12847 @3, F14393 @3); legal (F5007 @3); program (F6000 @5); non-en neg (F2422 @28) |  the word "program" and its plural form | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6000) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 28 | Layer 4: \"but\" conjunction (F5347 @13); contrast (F2884 @13); reporting + that (F12847 @3, F14393 @3); legal (F5007 @3); program (F6000 @5); non-en neg (F2422 @28) | negations in other languages like French, Malay, and Croatian | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L5:F7144](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7144) | 3 | Layer 5: proper-noun + \"said\" attribution (F7144 @3) |  proper nouns followed by the word "said" | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7144) |
| [L6:F3655](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3655) | 7 | Layer 6: \"just\" and neighbouring words (F3655 @7) |  the word "just" and surrounding words | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3655) |
| [L7:F4284](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4284) | 13 | Layer 7: parenthetical/contrast cues (F4284 @13); business/review (F2088 @31) | instances of parenthetical commas and phrases | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4284) |
| [L7:F2088](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2088) | 31 | Layer 7: parenthetical/contrast cues (F4284 @13); business/review (F2088 @31) |  words related to business, reviews, planning and organization. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2088) |
| [L9:F12274](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12274) | 7 | Layer 9: \"not only\" phrase detector (F12274 @7) |  the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12274) |
| [L9:F12274](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12274) | 8 | Layer 9: \"not only\" phrase detector (F12274 @7) |  the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12274) |
| [L9:F12274](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12274) | 9 | Layer 9: \"not only\" phrase detector (F12274 @7) |  the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12274) |
| [L10:F6078](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6078) | 12 | Layer 10: contrasting sections (F6078 @13); technical (F6670 @31) |  sections where multiple ideas are being contrasted | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6078) |
| [L10:F6078](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6078) | 13 | Layer 10: contrasting sections (F6078 @13); technical (F6670 @31) |  sections where multiple ideas are being contrasted | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6078) |
| [L10:F6670](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) | 31 | Layer 10: contrasting sections (F6078 @13); technical (F6670 @31) | technical terms, especially within scientific or medical contexts | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) |
| [L11:F11267](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/11267) | 31 | Layer 11: \"although\"/concession (F11267 @31); misc (F14837 @31) |  clauses beginning with "although", certain other conjunctions (though, but), and words implying an absence of something. | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/11267) |
| [L11:F14837](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/14837) | 31 | Layer 11: \"although\"/concession (F11267 @31); misc (F14837 @31) |  a hodge-podge of terms related to chemistry, sewing, misfortune and advice | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/14837) |
| [L12:F12606](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) | 31 | Layer 12: political/stories/State cluster (F12606 @31); \"not only\" (F3005 @7) |  phrases related to political conspiracy/organizations, mental conditions and storytelling terms | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) |
| [L12:F3005](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/3005) | 7 | Layer 12: political/stories/State cluster (F12606 @31); \"not only\" (F3005 @7) |  the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/3005) |
| [L14:F10765](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10765) | 7 | Layer 14: \"not only\" (F10765 @7); \"but\"/\"also\" (F11020 @13) | the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10765) |
| [L14:F11020](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11020) | 13 | Layer 14: \"not only\" (F10765 @7); \"but\"/\"also\" (F11020 @13) | the word "but". and "also" | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11020) |
| [L15:F12905](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) | 13 | Layer 15: contrastive \"but\" (F12905 @13, F12905 @12) |  the word "but" along with surrounding words that indicate a contrasting or consequential relationship. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) |
| [L15:F12905](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) | 12 | Layer 15: contrastive \"but\" (F12905 @13, F12905 @12) |  the word "but" along with surrounding words that indicate a contrasting or consequential relationship. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) |
| [L15:F1990](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/1990) | 7 | Layer 15: contrastive \"but\" (F12905 @13, F12905 @12) | the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/1990) |
| [L16:F6005](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6005) | 7 | Layer 16: \"Not only\" (F6005 @7) | Not only | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6005) |
| [L17:F3763](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/3763) | 7 | Layer 17: \"only\" (F3763 @7) — late driver | only | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/3763) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L15:12905 de=-0.355 |
| 3 | `inspect_feature` ×18 | L15:12905, L0:8046, L5:7144, L2:13565, L4:12847, L3:2782, L0:15525, L17:3763, L1:1500, L0:6131, L1:11907, L12:12606, L4:6000, L10:6670, L4:5347, L0:2961, L1:1090, L0:1910 |
| 4 | `get_upstream_features` | L15:F1990 (de=10.38) +9 more |
| 5 | `get_upstream_features` | Emb:" only"@7 (de=5.97) +9 more |
| 6 | `get_upstream_features` | Emb:" only"@7 (de=6.91) +9 more |
| 7 | `inspect_feature` ×12 | L15:1990, L14:10765, L9:12274, L2:5627, L4:2884, L14:11020, L7:4284, L10:6078, L4:5347, L16:6005, L6:3655, L12:3005 |
| 8 | `get_upstream_features` | Emb:" only"@7 (de=8.94) +9 more |
| 9 | `get_upstream_features` | Emb:" will"@8 (de=37.75) +9 more |
| 10 | `get_upstream_features` | L3:F16191 (de=2.97) +9 more |
| 11 | `get_upstream_features` | Emb:" program"@5 (de=16.75) +9 more |
| 12 | `get_upstream_features` | Emb:" program"@5 (de=27.00) +9 more |
| 13 | `get_upstream_features` | Emb:" said"@3 (de=4.41) +9 more |
| 14 | `get_upstream_features` | Emb:" program"@5 (de=21.62) +9 more |
| 15 | `get_upstream_features` | Emb:" not"@6 (de=15.62) +9 more |
| 16 | `get_upstream_features` | Emb:" not"@6 (de=16.88) +9 more |
| 17 | `get_upstream_features` | Emb:" only"@7 (de=6.31) +7 more |
| 18 | `get_upstream_features` | Emb:" said"@3 (de=12.88) +7 more |
| 19 | `get_upstream_features` | Emb:" program"@5 (de=24.38) +7 more |
| 20 | `get_upstream_features` | Emb:"<bos>"@0 (de=6.19) +7 more |
| 21 | `get_upstream_features` | Emb:" improve"@31 (de=-2.97) +7 more |
| 22 | `inspect_feature` ×14 | L0:6236, L3:16191, L3:41, L0:12483, L3:3755, L2:5434, L2:4481, L11:11267, L11:14837, L7:2088, L4:5007, L4:14393, L4:2422, L3:6227 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L17:F3763@7` | ✅ reported | 7 | 13 | Trace the path of the "not only" feature at L17:F3763 (pos 7) all the way back t… |
| SA-2 | `L15:F12905@13` | ✅ reported | 4 | 13 | Trace the path of the "but" contrast feature at L15:F12905 (pos 13) all the way … |
| SA-3 | `L5:F7144@3` | ✅ reported | 4 | 10 | Trace the path of L5:F7144 (the "proper noun + said" feature at pos 3 "Wagonheim… |
| SA-4 | `L0:F1910@7` | ❌ error | — | — | Trace the path of L0:F1910 (the "not only" feature at pos 7) back to the embeddi… |
| SA-5 | `L0:F1910@7` | ❌ error | — | — | Trace the path of the L0 feature 1910 ("not only" phrase detector) at position 7… |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L17, F3763 | "only" |
| 2 | `get_upstream_features` | L17:F3763@7, k=10 | L15:F1990 (de=10.38) +9 more |
| 3 | `inspect_feature` | L15, F1990 | "the phrase "not only"" |
| 4 | `inspect_feature` | L14, F10765 | "the phrase "not only"" |
| 5 | `inspect_feature` | L9, F12274 | " the phrase "not only"" |
| 6 | `inspect_feature` | L2, F5627 | " instances of the phrase "not only"" |
| 7 | `inspect_feature` | L16, F6005 | "Not only" |
| 8 | `get_upstream_features` | L2:F5627@7, k=10 | Emb:" only"@7 (de=21.25) +9 more |
| 9 | `inspect_feature` | L6, F3655 | " the word "just" and surrounding words" |
| 10 | `inspect_feature` | L0, F12483 | "the word "only"" |
| 11 | `get_upstream_features` | L6:F3655@7, k=10 | Emb:" only"@7 (de=8.94) +9 more |
| 12 | `get_upstream_features` | L0:F12483@7, k=10 | Emb:" not"@6 (de=23.50) +9 more |

**Findings:** The trace starts at the downstream "only" feature (L17:F3763, pos 7) which receives strong excitatory input from the raw " not" and " only" token embeddings. The most influential upstream drivers are higher‑layer phrase detectors (L15:F1990, L14:F10765, L9:F12274) that each recognise the full "not only" construction. This signal propagates down to an early‑layer detector (L2:F5627) that aggregates…

</details>

<details>
<summary><b>SA-2</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L15, F12905 | " the word "but" along with surrounding words that indicate a contrasti" |
| 2 | `get_upstream_features` | L15:F12905@13, k=10 | Emb:" only"@7 (de=5.97) +9 more |
| 3 | `inspect_feature` | L2, F5627 | " instances of the phrase "not only"" |
| 4 | `get_upstream_features` | L2:F5627@7, k=10 | Emb:" only"@7 (de=21.25) +9 more |
| 5 | `inspect_feature` | L4, F2884 | "the word "but" and other contrastive conjunctions and adverbs." |
| 6 | `get_upstream_features` | L4:F2884@13, k=10 | Emb:" but"@13 (de=17.75) +9 more |
| 7 | `get_upstream_features` | L0:F12483@7, k=10 | Emb:" not"@6 (de=23.50) +9 more |
| 8 | `inspect_feature` | L0, F12483 | "the word "only"" |

**Findings:** The L15:F12905 "but" contrast feature receives its strongest excitatory drive from three sources: (1) the raw token embedding of "only" (pos7) and "but" (pos13), which directly inject the lexical items into the contrast circuit; (2) the lower‑layer (L2) feature 5627 that detects the "not only" construction, itself driven by the embeddings of "only" and "not"; and (3) a broader contrast detector at…

</details>

<details>
<summary><b>SA-3</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L5, F7144 | " proper nouns followed by the word "said"" |
| 2 | `get_upstream_features` | L5:F7144@3, k=15 | L3:F16191 (de=2.97) +14 more |
| 3 | `inspect_feature` | L3, F16191 | " verbs or legal names, pointing to its use in citing facts or sources" |
| 4 | `inspect_feature` | L4, F5007 | "words and phrases used in legal contexts, like testimony and arguments" |
| 5 | `get_upstream_features` | L3:F16191@3, k=10 | Emb:" said"@3 (de=1.76) +9 more |
| 6 | `get_upstream_features` | L4:F5007@3, k=10 | Emb:" said"@3 (de=4.28) +9 more |
| 7 | `inspect_feature` | L0, F4789 | " names, especially last names, which often contain "thaler"" |

**Findings:** L5:F7144 (“proper noun + said”) is driven predominantly by a lower‑layer citation‑verb detector (L3:F16191) and a legal‑testimonial language detector (L4:F5007). Both of these receive strong positive contributions from the token embeddings for " said" and the start‑of‑sequence token, as well as from the name‑token embeddings that compose the proper noun "Wagonheim" ("Wagon" and "heim"). The pathwa…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L1:F1090@5, k=8 → Emb:" program"@5 (de=14.88) +7 more |
| 2 | `get_upstream_features` | L1:F1500@5, k=8 → ❌ Feature (layer=1, feature_idx=1500) not found at pos=5. This |
| 3 | `get_upstream_features` | L0:F15525@3, k=8 → Emb:" said"@3 (de=20.25) +7 more |
| 4 | `get_upstream_features` | L0:F6131@3, k=8 → Emb:" said"@3 (de=7.47) +7 more |
| 5 | `get_upstream_features` | L0:F4723@7, k=8 → Emb:" only"@7 (de=29.88) +7 more |
| 6 | `get_upstream_features` | L0:F10875@3, k=8 → Emb:" said"@3 (de=11.81) +7 more |
| 7 | `inspect_feature` ×4 | L0:4789, L0:437, L0:7448, L0:1982 |
| 8 | `get_upstream_features` | L12:F12606@31, k=8 → Emb:"<bos>"@0 (de=6.19) +7 more |
| 9 | `get_upstream_features` | L10:F6670@31, k=8 → Emb:" improve"@31 (de=-2.97) +7 more |
| 10 | `get_upstream_features` | L1:F1500@7, k=8 → Emb:" only"@7 (de=6.31) +7 more |
| 11 | `inspect_feature` ×3 | L0:4958, L0:3247, L0:4723 |
| 12 | `get_upstream_features` | L0:F8046@8, k=8 → Emb:" will"@8 (de=37.75) +7 more |

### Build

`build_circuit` → 33 nodes, 64 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 204,493 | 11,249 | 662,033 | 0 | $0.1146 | — | — |
| SA-3 | openai/gpt-oss-120b | 65,656 | 4,802 | 3,456 | 0 | $0.0128 | ✅ 4F/10E | Trace the path of L5:F7144 (the "proper noun + said" feature… |
| SA-1 | openai/gpt-oss-120b | 172,456 | 12,428 | 49,504 | 0 | $0.0341 | ✅ 7F/13E | Trace the path of the "not only" feature at L17:F3763 (pos 7… |
| SA-2 | openai/gpt-oss-120b | 69,478 | 5,636 | 7,808 | 0 | $0.0139 | ✅ 4F/13E | Trace the path of the "but" contrast feature at L15:F12905 (… |
| **Total** | | **512,083** | **34,115** | **722,801** | **0** | **$0.1753** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 33s