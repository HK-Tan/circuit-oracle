# Circuit Oracle Report
**Date:** 2026-07-28 07:23:32 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe direction is driven by a long, deeply structured "journalist" circuit rooted in the word "writer" at pos 28 and the name "Guardian" at pos 44, fed by genuine journalism/writing features and by gender- and institution-adjacent context tokens, rather than by direct career-title features.

**Confidence:** 7

**Reasoning:** The output logit (L26, no features) is primarily driven by **L14:F4420 at pos 28** (direct_effect = −0.068), labeled "words and phrases related to journalism and newspapers" (frac_nonzero = 0.0165; promoted tokens: journalists, journalism, journalist, reporter, reporters). Its upstream chain traces cleanly back to the input: the "writer" embedding at pos 28 (direct_effect 5.75 into L14:F4420) feeds through L4:F13253 ("things related to journalism and the media"), L2:F9210 ("words related to journalism, writing, and articles"), and L6:F12712 ("titles of editors and publishers in scientific publications") — a textbook profession-internal stack for "journalist / writer". The "freelance" embedding (pos 27) also contributes (3.375 into L14:F4420), and the L4:F10849 path passes through the "Guardian" token embedding at pos 44 (direct_effect 18.125) via L2:F9545 ("newspaper names or press organizations") and L3:F10366 ("words related to official status such as job title, contract, or award"). These paths converge on a legitimate "this person is a journalist" signal driven by the self-description of being a freelance writer for the Guardian/Times/etc.

However, the circuit also reveals the gender / generic-context concerns the user flagged. The largest direct-effect at pos 22 is **L0:F12768** (direct_effect 0.0747, but the dominant *upstream* is the "he" embedding at pos 22 with direct_effect 40.25), whose Neuronpedia label is literally "mentions of 'he' and 'she' in close proximity" — a pronomial gender marker, not a profession indicator. Several other L0 features in the top list (F3007 at pos 14 "middle", F10881 at pos 12 "coverage", F1229 at pos 14 "shake/middle", F15880/F12713 at pos 15 "Middle East") signal topic rather than profession, and a constellation of generic function-word / punctuation / pronoun-context features (F9297 "ministries", F13096 "the", F2348 "Royal", F15323 "starting", F8690 "studies", etc.) on the "Royal United Services Institute" institution span carry meaningful direct effect into the logit without clearly distinguishing profession from setting.

So the picture is: a *core* genuine profession-circuit (writer → journalist → newspapers, with direct_effect magnitudes summing to ~0.10) does exist and reaches all the way to embedding nodes ("writer" pos 28, "freelance" pos 27, "Guardian" pos 44, "written" pos 41), but it is *intermixed* with a **gender-marker path** (he/she co-occurrence feature → logit, fed almost entirely by the "he" token at pos 22 with direct_effect 40.25) and a **generic institutional / topic / function-word path** ("Royal United Services Institute" tokens → logit via institute/L0 features, plus "Middle East" topic features). The user's concern is partially supported: gender pronouns and topic/setting tokens are not negligible contributors, but the dominant profession-identifying signal in the circuit is still the journalism/writer stack anchored at L14:F4420 and L6:F12712 rather than a "he → journalist" shortcut.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F15661](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15661) | 7 | Institute/institution token features (pos 7) | the word "spin" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15661) |
| [L0:F6484](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6484) | 7 | Institute/institution token features (pos 7) |  the word "sky" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6484) |
| [L0:F2127](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2127) | 7 | Institute/institution token features (pos 7) |  the word "dream" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2127) |
| [L0:F10439](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10439) | 7 | Institute/institution token features (pos 7) |  the word "agenda" and sometimes the word "Institute" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10439) |
| [L0:F5288](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5288) | 6 | Org/Institution-name features at pos 6 (Services) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5288) |
| [L0:F10228](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10228) | 6 | Org/Institution-name features at pos 6 (Services) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10228) |
| [L0:F487](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/487) | 6 | Org/Institution-name features at pos 6 (Services) |  words ending in "ment," particularly in technical contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/487) |
| [L0:F13754](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13754) | 9 | Defence/word features (pos 9) | words related to official or functional bodies and their actions, often involving government, structure, or critique. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13754) |
| [L0:F8690](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8690) | 10 | Defence/word features (pos 9) |  mentions of research studies | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8690) |
| [L0:F14581](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14581) | 10 | Defence/word features (pos 9) |  words synonymous with governing bodies, regulations, and policies, particularly in government and media contexts. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14581) |
| [L0:F3007](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3007) | 14 | Middle East topic features (pos 14, 15) |  the word "middle", and sometimes the word "character", and "camp" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3007) |
| [L0:F10881](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10881) | 12 | Middle East topic features (pos 14, 15) |  the word "coverage" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10881) |
| [L0:F15880](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15880) | 15 | Middle East topic features (pos 14, 15) | mentions of the Middle East | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15880) |
| [L0:F12713](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12713) | 15 | Middle East topic features (pos 14, 15) | mentions of "New York City." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12713) |
| [L0:F1229](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1229) | 14 | Middle East topic features (pos 14, 15) |  the word "shake," and words related to the middle of something | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1229) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 22 | He/she gender pronoun feature (pos 22) |  mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L0:F2348](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2348) | 4 | Adjacent pronoun-context tokens (pos 1, 2, 3) |  the word "rapid" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2348) |
| [L0:F13096](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13096) | 3 | Adjacent pronoun-context tokens (pos 1, 2, 3) |  instances of the word "the", often followed by nouns or other determiners | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13096) |
| [L0:F9297](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9297) | 7 | Adjacent pronoun-context tokens (pos 1, 2, 3) |  mentions of government ministries and ministers. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9297) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 38 | Adjacent pronoun-context tokens (pos 1, 2, 3) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F14824](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) | 40 | Adjacent pronoun-context tokens (pos 1, 2, 3) | the word "has" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) |
| [L0:F4870](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4870) | 11 | Adjacent pronoun-context tokens (pos 1, 2, 3) |  commas and sometimes reach (context not clear) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4870) |
| [L0:F4308](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4308) | 1 | Adjacent pronoun-context tokens (pos 1, 2, 3) |  the word "partial" and related usages like "partially" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4308) |
| [L0:F7770](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7770) | 15 | Adjacent pronoun-context tokens (pos 1, 2, 3) | the abbreviation "Con." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7770) |
| [L0:F6770](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6770) | 12 | Adjacent pronoun-context tokens (pos 1, 2, 3) |  the word "visual" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6770) |
| [L0:F9866](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9866) | 12 | Adjacent pronoun-context tokens (pos 1, 2, 3) |  the word "latter" and possibly the word "such" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9866) |
| [L0:F1053](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1053) | 25 | Adjacent pronoun-context tokens (pos 1, 2, 3) |  the word "as." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1053) |
| [L0:F16087](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16087) | 20 | Adjacent pronoun-context tokens (pos 1, 2, 3) |  the word "topic" or "topics" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16087) |
| [L0:F13740](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13740) | 7 | Adjacent pronoun-context tokens (pos 1, 2, 3) | the word "absorb" and its derivations | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13740) |
| [L0:F8873](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8873) | 6 | Adjacent pronoun-context tokens (pos 1, 2, 3) | the word "hand" and a few somewhat related words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8873) |
| [L0:F14709](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14709) | 6 | Adjacent pronoun-context tokens (pos 1, 2, 3) |  sentences related to industrial accidents, injuries, and legal proceedings | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14709) |
| [L0:F765](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/765) | 5 | Adjacent pronoun-context tokens (pos 1, 2, 3) |  the word "straight" and words related to direction or alignment | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/765) |
| [L0:F7973](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7973) | 28 | Adjacent pronoun-context tokens (pos 1, 2, 3) | uses of the word "guarantee" and related abstract nouns. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7973) |
| [L0:F7269](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7269) | 1 | Adjacent pronoun-context tokens (pos 1, 2, 3) |  the word "entry" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7269) |
| [L0:F3850](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3850) | 11 | Adjacent pronoun-context tokens (pos 1, 2, 3) | punctuation marks | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3850) |
| [L1:F1445](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1445) | 7 | Military/vehicles/weapons (pos 7) |  terms related to the military, especially vehicles and weapons | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1445) |
| [L1:F4459](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4459) | 7 | Research institutes (pos 7) |  mentions of research institutes | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4459) |
| [L1:F14993](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14993) | 7 | Research institutes (pos 7) |  words related to drainage systems | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14993) |
| [L1:F15323](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15323) | 1 | "Starting"/"Starting point" word features (pos 1, 2) | the word "starting" in academic papers | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15323) |
| [L2:F12068](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12068) | 2 | "Starting"/"Starting point" word features (pos 1, 2) |  words related to starting points, beginnings, or initiations in various contexts. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12068) |
| [L1:F975](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/975) | 2 | "Starting"/"Starting point" word features (pos 1, 2) | the word "at" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/975) |
| [L2:F15811](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15811) | 2 | "Starting"/"Starting point" word features (pos 1, 2) |  the word "off", and also possibly "Vision", and "pla" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15811) |
| [L2:F13783](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13783) | 7 | Institute/Institution higher-layer (pos 7) |  the word "Institute" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13783) |
| [L3:F10489](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10489) | 7 | Institute/Institution higher-layer (pos 7) |  the word "Institute" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10489) |
| [L3:F3205](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3205) | 7 | Institute/Institution higher-layer (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3205) |
| [L4:F5060](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5060) | 7 | Institute/Institution higher-layer (pos 7) | references to institutions and technology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5060) |
| [L0:F2485](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2485) | 7 | Institute/Institution higher-layer (pos 7) | the word "play" in various tenses/forms, often associated with the word "role" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2485) |
| [L0:F4562](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4562) | 7 | Institute/Institution higher-layer (pos 7) | the word "strong" and words that mean almost the same as it | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4562) |
| [L2:F12901](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12901) | 15 | Middle East phrase feature (pos 15) |  the phrase "Middle East" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12901) |
| [L2:F8690](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8690) | 15 | Middle East phrase feature (pos 15) |  references to wars and the military in the 20th century | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8690) |
| [L2:F9210](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9210) | 28 | Journalism/articles/writing (pos 28) | words related to journalism, writing, and articles | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9210) |
| [L2:F12020](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12020) | 28 | Journalism/articles/writing (pos 28) |  code that writes XML or RSS feeds | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12020) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 28 | Journalism/articles/writing (pos 28) |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L4:F661](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/661) | 28 | Journalism/articles/writing (pos 28) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/661) |
| [L4:F10849](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10849) | 44 | Journalism/articles/writing (pos 28) |  newspaper names | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10849) |
| [L2:F9545](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9545) | 44 | Journalism/articles/writing (pos 28) |  newspaper names or press organizations | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9545) |
| [L3:F10366](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10366) | 42 | Journalism/articles/writing (pos 28) | words related to official status such as job title, contract, or award | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10366) |
| [L0:F15492](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15492) | 42 | Journalism/articles/writing (pos 28) |  the word "for" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15492) |
| [L4:F7056](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7056) | 71 | Newscast/broadcasting features (pos 71) |  references to radio broadcasting | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7056) |
| [L4:F13482](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13482) | 71 | Newscast/broadcasting features (pos 71) |  references to news broadcasts | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13482) |
| [L4:F9065](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9065) | 71 | Newscast/broadcasting features (pos 71) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9065) |
| [L5:F3573](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3573) | 71 | Newscast/broadcasting features (pos 71) |  mentions of news broadcasts on television networks | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3573) |
| [L5:F119](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/119) | 71 | Newscast/broadcasting features (pos 71) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/119) |
| [L5:F4319](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/4319) | 71 | Newscast/broadcasting features (pos 71) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/4319) |
| [L5:F11506](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/11506) | 71 | Newscast/broadcasting features (pos 71) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/11506) |
| [L6:F12712](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) | 28 | Editors/publishers (pos 28) |  titles of editors and publishers in scientific publications | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) |
| [L6:F5849](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5849) | 28 | Editors/publishers (pos 28) |  references to blogs and blog posts | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5849) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 28 | News organizations / journalists (pos 28) |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F9521](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9521) | 71 | News organizations / journalists (pos 28) |  news sources and people involved in journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9521) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 28 | News organizations / journalists (pos 28) |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L9:F7435](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/7435) | 28 | News organizations / journalists (pos 28) |  words and phrases related to news production and media | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/7435) |
| [L9:F2845](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2845) | 28 | News organizations / journalists (pos 28) |  mentions of news organizations and journalists | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2845) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 28 | Journalism/newspapers (pos 28, drives logit) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:7124 de=-0.157 |
| 3 | `inspect_feature` ×8 | L0:7124, L0:15661, L0:12768, L0:3007, L0:10881, L0:6051, L6:12712, L14:4420 |
| 4 | `get_upstream_features` | Emb:" he"@22 (de=40.25) +9 more |
| 5 | `get_upstream_features` | Emb:" writer"@28 (de=5.75) +9 more |
| 6 | `get_upstream_features` | Emb:" writer"@28 (de=6.22) +9 more |
| 7 | `get_upstream_features` | Emb:" covering"@12 (de=16.25) +9 more |
| 8 | `get_upstream_features` | Emb:" Middle"@14 (de=20.75) +9 more |
| 9 | `get_top_features` | 30 features; top: L0:7124 de=-0.157 |
| 10 | `inspect_feature` ×12 | L0:6484, L0:2348, L1:4459, L0:1229, L2:12901, L0:9297, L3:10489, L6:10984, L0:13096, L0:8690, L0:15880, L0:12713 |
| 11 | `get_upstream_features` | Emb:" Middle"@14 (de=20.75) +9 more |
| 12 | `get_upstream_features` | Emb:" he"@22 (de=40.25) +9 more |
| 13 | `get_upstream_features` | Emb:" East"@15 (de=11.00) +9 more |
| 14 | `get_upstream_features` | Emb:" Middle"@14 (de=17.12) +9 more |
| 15 | `get_upstream_features` | Emb:" East"@15 (de=26.75) +9 more |
| 16 | `get_upstream_features` | Emb:" covering"@12 (de=16.25) +9 more |
| 17 | `get_upstream_features` | Emb:" at"@2 (de=31.38) +9 more |
| 18 | `get_upstream_features` | Emb:" Studies"@10 (de=11.88) +9 more |
| 19 | `inspect_feature` ×16 | L8:8855, L4:13253, L7:13646, L9:7435, L9:2845, L2:9210, L6:5849, L4:5060, L1:1445, L1:15323, L2:12068, L0:2127, L0:4870, L0:14824, L0:4308, L0:9728 |

### Dispatch: 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@28` | ❌ error | — | — | Trace upstream from the journalism/newspapers feature at L14:F4420, pos 28 ("wri… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F15880@15, k=10 → Emb:" Middle"@14 (de=17.12) +9 more |
| 2 | `get_upstream_features` | L0:F12713@15, k=10 → Emb:" East"@15 (de=11.00) +9 more |
| 3 | `get_upstream_features` | L1:F4459@7, k=10 → Emb:" Institute"@7 (de=27.50) +9 more |
| 4 | `get_upstream_features` | L6:F12712@28, k=10 → Emb:" writer"@28 (de=6.22) +9 more |
| 5 | `get_upstream_features` | L6:F10984@71, k=10 → Emb:" broadcasting"@71 (de=13.06) +9 more |
| 6 | `get_upstream_features` | L1:F1445@7, k=10 → Emb:" Institute"@7 (de=5.25) +9 more |
| 7 | `get_upstream_features` | L3:F10489@7, k=10 → Emb:" Institute"@7 (de=27.12) +9 more |
| 8 | `get_upstream_features` | L4:F5060@7, k=10 → Emb:" Institute"@7 (de=16.12) +9 more |
| 9 | `get_upstream_features` | L0:F2127@7, k=10 → Emb:" Institute"@7 (de=10.12) +9 more |
| 10 | `get_upstream_features` | L0:F2348@4, k=10 → Emb:" Royal"@4 (de=14.44) +9 more |
| 11 | `get_upstream_features` | L0:F13096@3, k=10 → Emb:" the"@3 (de=28.00) +9 more |
| 12 | `get_upstream_features` | L1:F15323@1, k=10 → Emb:"Starting"@1 (de=16.38) +9 more |
| 13 | `get_upstream_features` | L0:F8690@10, k=10 → Emb:" Studies"@10 (de=11.88) +9 more |
| 14 | `get_upstream_features` | L2:F12068@2, k=10 → Emb:"Starting"@1 (de=13.75) +9 more |
| 15 | `inspect_feature` ×10 | L2:12020, L5:6306, L4:7056, L4:13482, L5:3573, L2:13783, L1:14993, L0:10439, L0:2485, L0:4562 |
| 16 | `get_top_features` | token="", k=50 → 50 features; top: L0:7124 de=-0.157 |
| 17 | `inspect_feature` ×20 | L2:8690, L0:7770, L0:6770, L0:9866, L0:487, L0:765, L0:1053, L4:10849, L0:16087, L0:7973, L7:9521, L0:14581, L0:13740, L0:13754, L4:1047, L3:3495, L0:3850, L0:14709, L0:8873, L0:7269 |
| 18 | `get_upstream_features` | L4:F10849@44, k=10 → Emb:" Guardian"@44 (de=18.12) +9 more |
| 19 | `get_upstream_features` | L0:F16087@20, k=10 → Emb:" topics"@20 (de=23.38) +9 more |
| 20 | `get_upstream_features` | L0:F1053@25, k=10 → Emb:" as"@25 (de=35.75) +9 more |
| 21 | `get_upstream_features` | L4:F1047@2, k=10 → Emb:"Starting"@1 (de=8.06) +9 more |
| 22 | `get_upstream_features` | L0:F487@6, k=10 → Emb:" Services"@6 (de=13.62) +9 more |
| 23 | `get_upstream_features` | L0:F13754@9, k=10 → Emb:" Defence"@9 (de=24.12) +9 more |
| 24 | `inspect_feature` ×9 | L2:9545, L3:10366, L0:15492, L3:6961, L3:7499, L2:15811, L3:3658, L1:975, L2:12020 |

### Build

`build_circuit` → 41 nodes, 48 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 155,641 | 12,377 | 939,526 | 0 | $0.1179 | — | — |
| **Total** | | **155,641** | **12,377** | **939,526** | **0** | **$0.1179** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 32s