# Circuit Oracle Report
**Date:** 2026-07-28 07:22:53 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven primarily by shallow, position-keyed lexical/syntactic detectors of function words ("not", "only", "but", "will", "isn't", "said", "program") in the input — particularly the "not only … but" pattern in the premise and the standalone "but" + "isn't" in the hypothesis — rather than by any entity/semantic/world-knowledge representation of the proposition, exactly the spurious-lexical-cue worry the user raised.

**Confidence:** 8

**Reasoning:**

The circuit flows from raw token embeddings up through four supernodes that feed the probe logit (layer 26, synthetic target):

1. **Premise content** (pos 3, 5) — layer-0..2 features that detect "Wagonheim", "said", "program" (L0:F12154 "program/President", L1:F11907 "program", L2:F13565 "programs", L0:F15525 "explanation/reporting contexts", L0:F15461 "court proceedings"). These are entity-agnostic — they fire on the noun itself, not on a representation of what the program does.

2. **Speech attribution** (pos 3 "said") — a chain of features from L3:L16191 (citing facts/sources), L4:F12847 (reporting verb + "that"), L4:F14393 (direct quotes/reports), L4:F15629 (speech attribution), L4:F8258 and L5:F11718 (people speaking/being quoted), L6:F4419 (people providing information in official capacity), L5:F7144 (proper nouns + "said"). Each of these is a low-frac_nonzero (0.008–0.020) reporter/speech pattern detector that just confirms the premise is a quotation.

3. **"not only … but" / contrastive construction** (pos 6-8) — the strongest POSITIVE driver. This is the user's worry materialised as a circuit: L0:F8046 "the word 'will'", L0:F1910 "not only", L0:F2961 "qualifications/negations (necessarily, only)", L0:F4723 "only", L0:F6859 "negated/absent words", L1:F13438 "only", L2:F5627 "not only", L6:F3655 "just/surrounding words" (promoted tokens: lisäksi, だけでなく, だけではなく — all "additionally/also"), L8:F8775 "either" in negation contexts, L9:F12274 "not only", L12:F3005 "not only", L14:F10765 "not only", L15:F1990 "not only", L16:F6005 "Not only", L17:F3763 "only" (promoted: "but"). These features are essentially phrase-templates ("not only X but also Y"). They are activated by the surface string and project positively onto the contradiction probe.

4. **Negation/'but' at hypothesis** (pos 12-13, 28) — the strongest NEGATIVE driver (L15:F12905 pos 13 direct_effect -0.356, the single largest-magnitude feature in the entire graph). This supernode is exactly the "negation word" the user flagged: L4:F2884/L4:F5347 "but" conjunction detectors, L7:F4284 parenthetical commas, L10:F6078 "multiple ideas being contrasted", L14:F11020 "but also", L15:F12905 "but + surrounding contrasting words" (frac_nonzero 0.005, fires on "but" anywhere), L16:F7295 "but also", plus L0:F6236 firing on the "t" of "isn't" at pos 28 (its label is literally "the letter t when it follows 'isn'' or 'doesn''" — a textbook negation-spurious feature). The upstream of L15:F12905 includes the embedding node " but" (pos 13, direct_effect 4) and " not" (pos 6).

**Source-influence check confirms the user's hypothesis.** get_source_influence on the negation cluster (pos 6, 7, 12, 13) returns S_pct_of_total = 2.6% and S_over_R = 0.62 — comparable to, but a bit less than, the strongest non-source driver. The broader premise+contrast span (pos 3, 5, 6, 7, 8, 13) gives S_pct = 5.9% with S_over_R = 1.56 (slightly over the top non-source driver), but the dominant contributors are L2:F5627 "not only", L6:F3655 "just/also", and the L0 "only/not" detectors — again pure phrase templates, not semantic entailment. The actual hypothesis-content features (pos 26 "isn", 28-31 "improve", "lawyers'") only enter through the high-layer L10:F6670/L12:F12606, which fire on "improve" but with very small direct_effect (~0.14) and the L0:F6236 "t-of-isn't" again.

**Verdict on the user concern (confirmed).** The mechanism is exactly the "negation words / cue-words" pathology: the probe reads "not only … but also" in the premise (pos 6-8) and "isn't" + "but" in the hypothesis (pos 12-13, 28) as a contradiction pattern, independent of whether the content of the second sentence actually negates the first. There is no entity/semantic feature comparing "Wagonheim" to "the second sentence's author" or "program's image-improvement effect" to "the second sentence's denial." Late-layer features are all generic phrase-templates with frac_nonzero ≤ 0.07 (most ≤ 0.01), and their activated-token patterns are surface strings ("not", "only", "but", "isn't", "t") rather than world-knowledge entities. The probe is acting as a heuristic negation/conjunction detector, not a NLI semantic classifier.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F12154](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12154) | 5 | Premise content tokens: 'Wagonheim said the program' (pos 1-5) | instances of the words "program", "programme", and "President", sometimes in conjunction with adverbial modifiers | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12154) |
| [L1:F11907](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11907) | 5 | Premise content tokens: 'Wagonheim said the program' (pos 1-5) |  the word "program" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11907) |
| [L2:F13565](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13565) | 5 | Premise content tokens: 'Wagonheim said the program' (pos 1-5) |  the word "program(me)s" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13565) |
| [L1:F1090](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1090) | 5 | Premise content tokens: 'Wagonheim said the program' (pos 1-5) |  the word "approval" and its variants | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1090) |
| [L4:F6000](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6000) | 5 | Premise content tokens: 'Wagonheim said the program' (pos 1-5) |  the word "program" and its plural form | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6000) |
| [L0:F15525](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15525) | 3 | Premise content tokens: 'Wagonheim said the program' (pos 1-5) |  places where something is being explained or reported | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15525) |
| [L0:F10875](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10875) | 3 | Premise content tokens: 'Wagonheim said the program' (pos 1-5) | words related to being somewhat like something but not entirely or always. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10875) |
| [L3:F2782](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2782) | 5 | Premise content tokens: 'Wagonheim said the program' (pos 1-5) |  references to television and news programming | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2782) |
| [L0:F15461](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15461) | 5 | Premise content tokens: 'Wagonheim said the program' (pos 1-5) |  words related to court proceedings, especially those involving testimony and legal arguments. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15461) |
| [L4:F12847](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12847) | 3 | Speech/quotation attribution: 'said', reporting verbs (pos 3) | sentences with some reporting verb and the word 'that' | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12847) |
| [L3:F16191](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16191) | 3 | Speech/quotation attribution: 'said', reporting verbs (pos 3) |  verbs or legal names, pointing to its use in citing facts or sources | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16191) |
| [L3:F41](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/41) | 3 | Speech/quotation attribution: 'said', reporting verbs (pos 3) |  citations to other papers, specifically looking for "*et al.*" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/41) |
| [L4:F5007](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5007) | 3 | Speech/quotation attribution: 'said', reporting verbs (pos 3) | words and phrases used in legal contexts, like testimony and arguments, and actions such as describing someone's mood or facial expression. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5007) |
| [L4:F14393](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14393) | 3 | Speech/quotation attribution: 'said', reporting verbs (pos 3) |  direct quotes or reports of people speaking | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14393) |
| [L4:F15629](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15629) | 3 | Speech/quotation attribution: 'said', reporting verbs (pos 3) |  speech attribution, such as the word "said" and phrases like "talking about" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15629) |
| [L4:F8258](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8258) | 3 | Speech/quotation attribution: 'said', reporting verbs (pos 3) | sentences including verbs having to do with speaking or stating | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8258) |
| [L5:F11718](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/11718) | 3 | Speech/quotation attribution: 'said', reporting verbs (pos 3) |  references to people speaking or being quoted | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/11718) |
| [L6:F4419](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4419) | 3 | Speech/quotation attribution: 'said', reporting verbs (pos 3) |  instances of people providing information during an official capacity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4419) |
| [L5:F7144](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7144) | 3 | Speech/quotation attribution: 'said', reporting verbs (pos 3) |  proper nouns followed by the word "said" | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7144) |
| [L0:F10614](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10614) | 3 | Speech/quotation attribution: 'said', reporting verbs (pos 3) |  the word "everyday" and words that often come before it | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10614) |
| [L0:F7874](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7874) | 3 | Speech/quotation attribution: 'said', reporting verbs (pos 3) |  words related to technical modifications or repairs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7874) |
| [L2:F5781](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5781) | 3 | Speech/quotation attribution: 'said', reporting verbs (pos 3) |  words related to opinions, assertions, and declarations | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5781) |
| [L0:F8046](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8046) | 8 | 'not only ... but also' / contrastive-construction features (pos 6-8) |  the word "will." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8046) |
| [L0:F1910](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1910) | 7 | 'not only ... but also' / contrastive-construction features (pos 6-8) |  the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1910) |
| [L0:F2961](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2961) | 7 | 'not only ... but also' / contrastive-construction features (pos 6-8) |  words that act as qualifications or negations, with a high preference for "necessarily" and "uncommon." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2961) |
| [L0:F4723](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4723) | 7 | 'not only ... but also' / contrastive-construction features (pos 6-8) |  the word "only" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4723) |
| [L1:F13438](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13438) | 7 | 'not only ... but also' / contrastive-construction features (pos 6-8) |  the word "only" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13438) |
| [L1:F1500](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1500) | 7 | 'not only ... but also' / contrastive-construction features (pos 6-8) | the word "stress" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1500) |
| [L0:F6859](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6859) | 7 | 'not only ... but also' / contrastive-construction features (pos 6-8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6859) |
| [L2:F5627](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5627) | 7 | 'not only ... but also' / contrastive-construction features (pos 6-8) |  instances of the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5627) |
| [L6:F3655](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3655) | 7 | 'not only ... but also' / contrastive-construction features (pos 6-8) |  the word "just" and surrounding words | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3655) |
| [L8:F8775](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8775) | 7 | 'not only ... but also' / contrastive-construction features (pos 6-8) | the word "either" (and some related words) possibly in the context of alternatives or negation | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8775) |
| [L9:F12274](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12274) | 7 | 'not only ... but also' / contrastive-construction features (pos 6-8) |  the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12274) |
| [L12:F3005](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/3005) | 7 | 'not only ... but also' / contrastive-construction features (pos 6-8) |  the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/3005) |
| [L14:F10765](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10765) | 7 | 'not only ... but also' / contrastive-construction features (pos 6-8) | the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10765) |
| [L15:F1990](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/1990) | 7 | 'not only ... but also' / contrastive-construction features (pos 6-8) | the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/1990) |
| [L16:F6005](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6005) | 7 | 'not only ... but also' / contrastive-construction features (pos 6-8) | Not only | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6005) |
| [L17:F3763](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/3763) | 7 | 'not only ... but also' / contrastive-construction features (pos 6-8) | only | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/3763) |
| [L14:F9644](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/9644) | 8 | 'not only ... but also' / contrastive-construction features (pos 6-8) |  words and phrases that express overcoming adversity and negative situations. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/9644) |
| [L4:F2884](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2884) | 13 | Negation/'but' at hypothesis (pos 12-13) and 'isn't' (pos 28) - strongest NEGATIVE driver | the word "but" and other contrastive conjunctions and adverbs. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2884) |
| [L4:F5347](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5347) | 13 | Negation/'but' at hypothesis (pos 12-13) and 'isn't' (pos 28) - strongest NEGATIVE driver |  the conjunction "but" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5347) |
| [L7:F4284](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4284) | 13 | Negation/'but' at hypothesis (pos 12-13) and 'isn't' (pos 28) - strongest NEGATIVE driver | instances of parenthetical commas and phrases | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4284) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 28 | Negation/'but' at hypothesis (pos 12-13) and 'isn't' (pos 28) - strongest NEGATIVE driver | the letter "t" when it follows the word "isn'" or "doesn'" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L10:F6078](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6078) | 13 | Negation/'but' at hypothesis (pos 12-13) and 'isn't' (pos 28) - strongest NEGATIVE driver |  sections where multiple ideas are being contrasted | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6078) |
| [L14:F11020](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11020) | 13 | Negation/'but' at hypothesis (pos 12-13) and 'isn't' (pos 28) - strongest NEGATIVE driver | the word "but". and "also" | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11020) |
| [L15:F12905](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) | 13 | Negation/'but' at hypothesis (pos 12-13) and 'isn't' (pos 28) - strongest NEGATIVE driver |  the word "but" along with surrounding words that indicate a contrasting or consequential relationship. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) |
| [L15:F12905](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) | 12 | Negation/'but' at hypothesis (pos 12-13) and 'isn't' (pos 28) - strongest NEGATIVE driver |  the word "but" along with surrounding words that indicate a contrasting or consequential relationship. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) |
| [L16:F7295](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/7295) | 13 | Negation/'but' at hypothesis (pos 12-13) and 'isn't' (pos 28) - strongest NEGATIVE driver | the phrase "but also" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/7295) |
| [L10:F6670](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) | 31 | Hypothesis content (pos 11, 22, 26, 28-31) - weak mixed-sign | technical terms, especially within scientific or medical contexts | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) |
| [L12:F12606](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) | 31 | Hypothesis content (pos 11, 22, 26, 28-31) - weak mixed-sign |  phrases related to political conspiracy/organizations, mental conditions and storytelling terms | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) |
| [L2:F1131](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1131) | 22 | Hypothesis content (pos 11, 22, 26, 28-31) - weak mixed-sign |  the word "arrest" and variants of it | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1131) |
| [L5:F14173](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14173) | 11 | Hypothesis content (pos 11, 22, 26, 28-31) - weak mixed-sign |  words related to buying, selling, or the condition of items | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14173) |
| [L0:F6131](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6131) | 3 | Hypothesis content (pos 11, 22, 26, 28-31) - weak mixed-sign |  the word "trick", often within the context of telling or describing a trick | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6131) |
| [L4:F4080](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4080) | 5 | Hypothesis content (pos 11, 22, 26, 28-31) - weak mixed-sign |  words within legal or science documents | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4080) |
| [L0:F3273](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3273) | 5 | Hypothesis content (pos 11, 22, 26, 28-31) - weak mixed-sign | the word "subject," and sometimes words directly related to it | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3273) |
| [L3:F6227](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) | 30 | Hypothesis content (pos 11, 22, 26, 28-31) - weak mixed-sign |  sentence fragments and informal or ungrammatical language, often including abbreviations. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L15:12905 de=-0.355 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L15:F12905@13` | ❌ error | — | — | Trace L15:F12905 (pos 13) upstream. This feature has the largest magnitude direc… |
| SA-2 | `L0:F8046@8` | ❌ error | — | — | Trace L0:F8046 (pos 8) upstream. This is a layer-0 feature with large negative d… |
| SA-3 | `L5:F7144@3` | ❌ error | — | — | Trace L5:F7144 (pos 3) upstream. This is a top positive driver. Position 3 is "t… |
| SA-4 | `L2:F13565@5` | ❌ error | — | — | Trace L2:F13565 (pos 5) upstream. Top positive driver. Position 5 in this prompt… |
| SA-5 | `L17:F3763@7` | ❌ error | — | — | Trace L17:F3763 (pos 7) upstream. This is the highest-layer positive feature. Po… |
| SA-6 | `L3:F2782@5` | ❌ error | — | — | Trace L3:F2782 (pos 5) upstream. This is a top negative driver. Position 5 is "p… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×7 | L15:12905, L0:8046, L5:7144, L17:3763, L3:2782, L2:13565, L4:12847 |
| 2 | `get_upstream_features` | L15:F12905@13, k=10 → Emb:" only"@7 (de=5.97) +9 more |
| 3 | `get_upstream_features` | L0:F8046@8, k=15 → Emb:" will"@8 (de=37.75) +14 more |
| 4 | `get_upstream_features` | L17:F3763@7, k=10 → L15:F1990 (de=10.38) +9 more |
| 5 | `get_upstream_features` | L5:F7144@3, k=10 → L3:F16191 (de=2.97) +9 more |
| 6 | `inspect_feature` ×11 | L2:5627, L9:12274, L4:2884, L14:11020, L7:4284, L15:1990, L14:10765, L16:6005, L6:3655, L10:6078, L2:13565 |
| 7 | `get_upstream_features` | L2:F13565@5, k=10 → Emb:" program"@5 (de=16.75) +9 more |
| 8 | `get_upstream_features` | L3:F2782@5, k=10 → Emb:" program"@5 (de=27.00) +9 more |
| 9 | `get_upstream_features` | L15:F12905@12, k=10 → Emb:" only"@7 (de=6.91) +9 more |
| 10 | `get_upstream_features` | L4:F12847@3, k=10 → Emb:" said"@3 (de=4.41) +9 more |
| 11 | `inspect_feature` ×13 | L1:11907, L1:1090, L1:1500, L3:16191, L0:10875, L0:12154, L0:2961, L10:6670, L12:12606, L0:1910, L0:15525, L4:5347, L0:6131 |
| 12 | `get_top_features` | token="", k=40 → 40 features; top: L15:12905 de=-0.355 |
| 13 | `inspect_feature` ×21 | L4:6000, L4:4080, L4:15629, L1:6859, L1:13438, L4:14393, L4:8258, L2:5781, L5:11718, L0:10614, L0:15461, L0:10846, L16:7295, L14:9644, L2:1131, L5:14173, L0:7874, L6:4419, L0:3273, L4:5007, L3:41 |
| 14 | `get_upstream_features` | L5:F7144@3, k=10 → L3:F16191 (de=2.97) +9 more |
| 15 | `get_upstream_features` | L17:F3763@7, k=10 → L15:F1990 (de=10.38) +9 more |
| 16 | `get_upstream_features` | L10:F6670@31, k=10 → Emb:" improve"@31 (de=-2.97) +9 more |
| 17 | `get_upstream_features` | L12:F12606@31, k=10 → Emb:"<bos>"@0 (de=6.19) +9 more |
| 18 | `get_source_influence` | {'depth': 2, 'source_positions': [13]} → {'depth': 2, 'source_positions': [13], 'S_pct_of_total': -2.359, 'R_pct_of_total |
| 19 | `get_source_influence` | {'depth': 2, 'source_positions': [6, 7, 12, 13]} → {'depth': 2, 'source_positions': [6, 7, 12, 13], 'S_pct_of_total': 2.614, 'R_pct |
| 20 | `get_source_influence` | {'depth': 2, 'source_positions': [3, 5, 6, 7, 8, 13]} → {'depth': 2, 'source_positions': [3, 5, 6, 7, 8, 13], 'S_pct_of_total': 5.891, ' |
| 21 | `inspect_feature` ×8 | L0:4723, L12:3005, L8:8775, L7:2088, L3:6227, L0:6236, L4:10252, L4:2422 |

### Build

`build_circuit` → 13 nodes, 16 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 128,609 | 14,654 | 823,706 | 0 | $0.1056 | — | — |
| **Total** | | **128,609** | **14,654** | **823,706** | **0** | **$0.1056** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 15s