# Circuit Oracle Report
**Date:** 2026-07-28 07:24:46 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_9 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity probe is driven almost entirely by a chain of features that detect the literal presence of racial / ethnic / gender identity words (especially "white" at pos 9, "guy" at pos 10, "oriental" at pos 27, "last name" at pos 14–15, "women"/"men" at pos 28/33), rather than by features that encode the *toxic semantics* (the slur "self hater," the derogatory framing "lust after white men," the demeaning stereotype about Asian women). The signal flows: token embeddings → L0 word detectors → L1 word/race detectors → L2 race/ethnicity/gender concepts → L3 "race-and-social-issues" features → L4 race/racism detectors → L6 identity-aggregation → probe logit.

**Confidence:** 8

**Reasoning:** The circuit reaches token-embedding nodes. The dominant drive is the **"white"** embedding at pos 9 (direct_effect 11.0 → 13.6 → 12.1 → 23.9 → 12.1 → 4.1 at successive layers), which is amplified at every layer by features whose only semantic content is "this token names a racial group":
- L0: lexical detectors F6548 ("national" — fires on "white"), F16013 ("blue/color" — incidental), F13663 at pos 9, plus the "guy"/"guys" detectors F3024/F2242/F5247/F9076 at pos 10.
- L1: F13007 ("white" with "black" fallback), F13023 ("transition" — incidental), F4668 ("white in image params"), F7821 ("fans" — incidental), F9113 ("discussions about race and slavery"). F9113 directly attacks the toxic racial-discourse frame but is doing so by detecting the *word* "white," not the prejudicial content.
- L2: F13158 ("words about race and ethnicity", de=2.1 at pos 9), F585 ("the word 'white'", de=30.75), F1708 ("mentions of colors" — incidentally), F15317/F10986/F10433 ("guy"/"guys"/men"), F15558 ("forms of 'settle' and 'married'"), F9961 ("html name elements" — incidental), F9320 ("self" detector at pos 21 feeding the L3 "self-hater" feature, de=1.8).
- L3: F13061 ("words related to race, gender and social issues", de=0.39 at pos 10) and F16373 ("mentions of demographic identity, especially race and gender", de=0.39) — these are the strongest late-layer identity aggregators. F11768 ("white" and diversity, de negative on the upstream), F15520 (people terms), F4512 ("first names, last names, phone numbers", de=0.22 at pos 15 — fires on "name"/"last").
- L4: F117 ("race, racism, and social justice, with a particular focus on Black people", de=0.31 at pos 10, frac_nonzero 0.012), F10004 ("hyphenated words beginning with 'self'", de=0.16 at pos 22 — fires on "self" only), F15204 ("art galleries, museums and the White House", de=4.1 at pos 9 but mostly negative), F7136 ("the color white"), F12975 ("Asian countries, calendars, and paganism/eastern religions", de=1.9 at pos 27, frac_nonzero 0.007), F14329 (color terms).
- L6: F3902 ("terms referring to race and ethnicity", de=0.34 at pos 9, 0.21 at pos 10, 0.19 at pos 27 — this is the strongest single late-layer feature), F15948 ("words and entities referring to gender and pronouns", de=0.17 at pos 10, also de=13.8 at pos 28 "women", de=10.9 at pos 33 "men"), F5671 ("references to people, with an emphasis on gender and family relations", de=0.17 at pos 10).

Critically, the only feature that engages with the *toxic* part of the prompt ("self hater") is L4:F10004, a feature whose autointerp is literally "hyphenated words beginning with 'self'" (frac_nonzero 0.004, very specific) — it fires on the word "self" at pos 21/22 and has no notion of the prejudicial content. Likewise, the strongly negative upstream from L3:F11768 ("white and related contexts such as diversity") and L4:F15204 ("art galleries, museums and the White House") suggests the white-detection branch actually competes with the toxic branch — the racism detector is the *excitatory* contribution, not the slur detector.

**Confirming the user's concern:** The circuit is dominated by **identity-token detector features** ("white," "white guy," "oriental," "last name," "woman"/"women," "men," "married," "author") that fire on the demographic lexemes regardless of whether the surrounding text is hateful, neutral, or positive. The probe's toxicity score is essentially the count of *identity group mentions* in the prompt. The actual toxicity signal ("self hater," "oriental women who lust after white men") barely registers — only the "self" word detector (F10004) and the "Asian countries" detector (F12975, which is about Asian countries/paganism) come close, and both fire on lexical surface features, not on the prejudicial semantics. This means the probe would assign roughly the same score to a benign sentence that mentions "white," "Asian," "her," and "name" — it is using **identity-token presence as a proxy for toxicity**, exactly the spurious-correlation concern raised.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: white (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: guy (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: married (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: appears (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: author (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: last (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: name (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 27 | Emb: oriental (pos 27) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: self (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 22 | Emb: hater (pos 22) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 28 | Emb: women (pos 28) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 33 | Emb: men (pos 33) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F6548](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6548) | 9 | L0 lexical feature detectors (white, guy, author, married, last, name, appears) |  the word "national" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6548) |
| [L0:F16013](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16013) | 9 | L0 lexical feature detectors (white, guy, author, married, last, name, appears) |  mentions of the color blue, and perhaps colors in general or the components of a graphic image | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16013) |
| [L0:F13663](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13663) | 9 | L0 lexical feature detectors (white, guy, author, married, last, name, appears) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13663) |
| [L0:F9076](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9076) | 10 | L0 lexical feature detectors (white, guy, author, married, last, name, appears) |  mentions of men, boys, areas, or general locations in a text | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9076) |
| [L0:F3024](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3024) | 10 | L0 lexical feature detectors (white, guy, author, married, last, name, appears) | the word "guy" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3024) |
| [L0:F2242](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2242) | 10 | L0 lexical feature detectors (white, guy, author, married, last, name, appears) |  the word "guys" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2242) |
| [L0:F5247](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5247) | 10 | L0 lexical feature detectors (white, guy, author, married, last, name, appears) |  references to ordinary people, especially men and women | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5247) |
| [L0:F11009](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11009) | 2 | L0 lexical feature detectors (white, guy, author, married, last, name, appears) | the word "author" and related words like "book." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11009) |
| [L0:F3612](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3612) | 2 | L0 lexical feature detectors (white, guy, author, married, last, name, appears) | the words "author", "authority", and "agency", often in a legal or academic context | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3612) |
| [L0:F753](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/753) | 2 | L0 lexical feature detectors (white, guy, author, married, last, name, appears) | the word "author" and words related to selling and prices | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/753) |
| [L0:F15578](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15578) | 6 | L0 lexical feature detectors (white, guy, author, married, last, name, appears) | mentions of marriage and related ideas | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15578) |
| [L0:F241](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/241) | 6 | L0 lexical feature detectors (white, guy, author, married, last, name, appears) | mentions of marriage | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/241) |
| [L0:F7773](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7773) | 3 | L0 lexical feature detectors (white, guy, author, married, last, name, appears) |  the word "lower" or "higher" in the context of comparisons | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7773) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 4 | L0 lexical feature detectors (white, guy, author, married, last, name, appears) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F1142](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1142) | 14 | L0 lexical feature detectors (white, guy, author, married, last, name, appears) |  the word "last" and the word "finally" or "next" within a short range | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1142) |
| [L0:F6127](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6127) | 15 | L0 lexical feature detectors (white, guy, author, married, last, name, appears) |  instances of the word "degree" and words associated with academia, especially higher education | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6127) |
| [L0:F4312](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4312) | 15 | L0 lexical feature detectors (white, guy, author, married, last, name, appears) | the word "names" as well as related terms like "surnames", and pronouns referring to people. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4312) |
| [L1:F384](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/384) | 2 | L1 lexical & early race detectors |  the string "ash" or "pund" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/384) |
| [L1:F5220](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5220) | 2 | L1 lexical & early race detectors |  references to authors and publications | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5220) |
| [L1:F6576](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6576) | 3 | L1 lexical & early race detectors |  the word "appearance" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6576) |
| [L1:F13759](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13759) | 4 | L1 lexical & early race detectors | the word 'to' | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13759) |
| [L1:F13007](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13007) | 9 | L1 lexical & early race detectors |  mentions of the word "white" and to a lesser extent "black" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13007) |
| [L1:F13023](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13023) | 10 | L1 lexical & early race detectors |  the word, "transition" in the context of scientific documents | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13023) |
| [L1:F4668](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4668) | 9 | L1 lexical & early race detectors |  the color white being used to describe image parameters | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4668) |
| [L1:F7821](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7821) | 9 | L1 lexical & early race detectors |  mentions of computer fans. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7821) |
| [L1:F9113](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) | 9 | L1 lexical & early race detectors |  discussions about race and slavery | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 9 | L2 race/ethnicity/gender concept features |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F1708](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1708) | 9 | L2 race/ethnicity/gender concept features |  mentions of colors | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1708) |
| [L2:F585](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) | 9 | L2 race/ethnicity/gender concept features | the word "white", often in association with "dwarf" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) |
| [L2:F15317](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15317) | 10 | L2 race/ethnicity/gender concept features |  gendered words, with a slight bias toward female-gendered words | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15317) |
| [L2:F10986](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10986) | 10 | L2 race/ethnicity/gender concept features | the word "guys" or "guy" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10986) |
| [L2:F10433](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10433) | 10 | L2 race/ethnicity/gender concept features | mentions of people, especially men or groups of people | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10433) |
| [L2:F14965](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14965) | 10 | L2 race/ethnicity/gender concept features |  words related to clothing and fabrics. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14965) |
| [L2:F15558](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15558) | 6 | L2 race/ethnicity/gender concept features |  forms of the word "settle" and the word "married." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15558) |
| [L2:F12633](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12633) | 3 | L2 race/ethnicity/gender concept features | a present or past tense verb of appearing, or a related adjective | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12633) |
| [L2:F12927](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12927) | 4 | L2 race/ethnicity/gender concept features | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12927) |
| [L2:F9961](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9961) | 15 | L2 race/ethnicity/gender concept features |  html elements containing the word "name" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9961) |
| [L2:F9320](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9320) | 21 | L2 race/ethnicity/gender concept features |  the word "self" and words meaning "internal" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9320) |
| [L2:F16224](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16224) | 22 | L2 race/ethnicity/gender concept features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16224) |
| [L2:F189](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/189) | 22 | L2 race/ethnicity/gender concept features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/189) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 10 | L3 race/social-issues features |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L3:F16373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) | 10 | L3 race/social-issues features |  mentions of demographic identity, especially race and gender | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) |
| [L3:F10286](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10286) | 4 | L3 race/social-issues features |  instances of the word 'seem' around 'to', as well as "R&B" in all caps | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10286) |
| [L3:F4512](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4512) | 15 | L3 race/social-issues features |  mentions of first names, last names, and phone numbers | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4512) |
| [L3:F11768](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11768) | 9 | L3 race/social-issues features |  the word "white" and related contexts such as diversity | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11768) |
| [L3:F15520](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15520) | 10 | L3 race/social-issues features |  mentions of general terms for people | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15520) |
| [L3:F8492](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8492) | 22 | L3 race/social-issues features | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8492) |
| [L3:F735](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) | 22 | L3 race/social-issues features | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) |
| [L3:F5808](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5808) | 22 | L3 race/social-issues features | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5808) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 10 | L4 race/racism & social-justice features |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F10004](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10004) | 22 | L4 race/racism & social-justice features |  hyphenated words beginning with "self" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10004) |
| [L4:F15204](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) | 9 | L4 race/racism & social-justice features |  art galleries, museums and the White House | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) |
| [L4:F14329](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14329) | 9 | L4 race/racism & social-justice features |  mentions of the colors black, white, or another color with "or" in its name | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14329) |
| [L4:F7136](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7136) | 9 | L4 race/racism & social-justice features |  the color white | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7136) |
| [L4:F12975](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12975) | 27 | L4 race/racism & social-justice features | mentions of Asian countries, calendars, and paganism/eastern religions | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12975) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 9 | L6 late race/identity aggregation |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 10 | L6 late race/identity aggregation |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 27 | L6 late race/identity aggregation |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F5671](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5671) | 10 | L6 late race/identity aggregation |  references to people, with an emphasis on gender and family relations. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5671) |
| [L6:F15948](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15948) | 10 | L6 late race/identity aggregation |  words and entities referring to gender and pronouns | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15948) |
| [L6:F15948](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15948) | 28 | L6 late race/identity aggregation |  words and entities referring to gender and pronouns | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15948) |
| [L6:F15948](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15948) | 33 | L6 late race/identity aggregation |  words and entities referring to gender and pronouns | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15948) |
| [L6:F5671](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5671) | 28 | L6 late race/identity aggregation |  references to people, with an emphasis on gender and family relations. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5671) |
| [L6:F5671](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5671) | 33 | L6 late race/identity aggregation |  references to people, with an emphasis on gender and family relations. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5671) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe classification score (toxicity) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L1:5220 de=-0.453 |
| 3 | `inspect_feature` ×12 | L3:13061, L6:3902, L4:117, L1:384, L0:7773, L0:753, L1:6576, L1:5220, L2:13158, L3:4512, L3:10286, L2:15558 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L3:F13061@10` | ❌ error | — | — | Trace this race/gender/social-issues feature at pos 10 upstream through the circ… |
| SA-2 | `L6:F3902@9` | ❌ error | — | — | Trace this race/ethnicity feature at pos 9 upstream through the circuit. Identif… |
| SA-3 | `L4:F117@10` | ❌ error | — | — | Trace this race/racism feature at pos 10 upstream. Identify input tokens driving… |
| SA-4 | `L1:F5220@2` | ❌ error | — | — | Trace this "author" feature at pos 2 (it has -0.45 direct effect) upstream. Iden… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L3:F13061@10, k=15 → Emb:" white"@9 (de=11.00) +14 more |
| 2 | `get_upstream_features` | L6:F3902@9, k=15 → Emb:" white"@9 (de=13.56) +14 more |
| 3 | `get_upstream_features` | L4:F117@10, k=15 → Emb:" white"@9 (de=12.12) +14 more |
| 4 | `get_upstream_features` | L1:F5220@2, k=15 → Emb:" author"@2 (de=19.12) +14 more |
| 5 | `get_upstream_features` | L3:F4512@15, k=10 → Emb:" last"@14 (de=24.75) +9 more |
| 6 | `get_upstream_features` | L2:F15558@6, k=10 → Emb:" married"@6 (de=25.12) +9 more |
| 7 | `get_upstream_features` | L1:F6576@3, k=10 → Emb:" appears"@3 (de=19.00) +9 more |
| 8 | `get_upstream_features` | L0:F7773@3, k=10 → Emb:" appears"@3 (de=14.81) +9 more |
| 9 | `get_upstream_features` | L3:F10286@4, k=10 → Emb:" appears"@3 (de=20.62) +9 more |
| 10 | `get_upstream_features` | L2:F13158@9, k=10 → Emb:" white"@9 (de=13.62) +9 more |
| 11 | `get_upstream_features` | L4:F10004@22, k=10 → Emb:" self"@21 (de=46.75) +9 more |
| 12 | `get_upstream_features` | L1:F384@2, k=10 → Emb:" author"@2 (de=13.94) +9 more |
| 13 | `get_upstream_features` | L1:F9113@9, k=10 → Emb:" white"@9 (de=14.44) +9 more |
| 14 | `get_upstream_features` | L0:F753@2, k=10 → Emb:" author"@2 (de=18.38) +9 more |
| 15 | `get_upstream_features` | L6:F3902@10, k=10 → L4:F117 (de=3.78) +9 more |
| 16 | `get_upstream_features` | L6:F3902@27, k=10 → Emb:" oriental"@27 (de=8.75) +9 more |
| 17 | `get_upstream_features` | L6:F15948@10, k=10 → Emb:" guy"@10 (de=9.62) +9 more |
| 18 | `get_upstream_features` | L6:F5671@10, k=10 → Emb:" guy"@10 (de=5.03) +9 more |
| 19 | `get_upstream_features` | L3:F16373@10, k=10 → Emb:" white"@9 (de=23.88) +9 more |
| 20 | `get_upstream_features` | L2:F9961@15, k=10 → Emb:" name"@15 (de=18.12) +9 more |
| 21 | `get_upstream_features` | L0:F241@6, k=10 → Emb:" married"@6 (de=12.81) +9 more |
| 22 | `get_upstream_features` | L4:F12975@27, k=10 → Emb:" oriental"@27 (de=13.25) +9 more |
| 23 | `get_upstream_features` | L0:F2242@10, k=10 → Emb:" guy"@10 (de=19.62) +9 more |
| 24 | `get_upstream_features` | L2:F15317@10, k=10 → Emb:" guy"@10 (de=9.44) +9 more |
| 25 | `get_upstream_features` | L3:F16373@27, k=5 → ❌ Feature (layer=3, feature_idx=16373) not found at pos=27. Th |
| 26 | `get_upstream_features` | L1:F7821@9, k=8 → Emb:" white"@9 (de=15.75) +7 more |
| 27 | `get_upstream_features` | L0:F16013@9, k=5 → Emb:" white"@9 (de=15.56) +4 more |
| 28 | `get_upstream_features` | L0:F6548@9, k=5 → Emb:" white"@9 (de=20.25) +4 more |
| 29 | `get_upstream_features` | L2:F585@9, k=5 → Emb:" white"@9 (de=30.75) +4 more |
| 30 | `get_upstream_features` | L2:F1708@9, k=5 → Emb:" white"@9 (de=18.50) +4 more |
| 31 | `get_upstream_features` | L0:F9076@10, k=5 → Emb:" white"@9 (de=7.91) +4 more |
| 32 | `get_upstream_features` | L0:F3024@10, k=5 → Emb:" guy"@10 (de=25.50) +4 more |
| 33 | `inspect_feature` ×3 | L3:16373, L4:12975, L2:9961 |
| 34 | `get_upstream_features` | L4:F10004@22, k=5 → Emb:" self"@21 (de=46.75) +4 more |
| 35 | `inspect_feature` ×4 | L4:10004, L6:15948, L6:5671, L1:9113 |
| 36 | `get_upstream_features` | L3:F10286@4, k=5 → Emb:" appears"@3 (de=20.62) +4 more |
| 37 | `get_upstream_features` | L0:F8444@4, k=5 → Emb:" to"@4 (de=40.25) +4 more |
| 38 | `get_upstream_features` | L2:F12927@4, k=5 → Emb:" to"@4 (de=6.16) +4 more |
| 39 | `get_upstream_features` | L2:F12633@3, k=5 → Emb:" appears"@3 (de=27.25) +4 more |
| 40 | `get_upstream_features` | L1:F13759@4, k=5 → Emb:" to"@4 (de=15.44) +4 more |
| 41 | `inspect_feature` ×4 | L0:8444, L2:12633, L1:13759, L2:12927 |
| 42 | `get_upstream_features` | L3:F8890@21, k=5 → Emb:" self"@21 (de=27.12) +4 more |
| 43 | `get_upstream_features` | L2:F9320@21, k=5 → Emb:" self"@21 (de=32.50) +4 more |
| 44 | `get_upstream_features` | L2:F9320@22, k=5 → ❌ Feature (layer=2, feature_idx=9320) not found at pos=22. Thi |
| 45 | `get_upstream_features` | L2:F16224@22, k=5 → Emb:" self"@21 (de=11.75) +4 more |
| 46 | `get_upstream_features` | L3:F8492@22, k=5 → Emb:" hater"@22 (de=24.62) +4 more |
| 47 | `get_upstream_features` | L3:F735@22, k=5 → Emb:" self"@21 (de=29.38) +4 more |
| 48 | `get_upstream_features` | L2:F189@22, k=5 → Emb:" hater"@22 (de=6.47) +4 more |
| 49 | `get_upstream_features` | L3:F5808@22, k=5 → Emb:" hater"@22 (de=7.78) +4 more |
| 50 | `get_upstream_features` | L0:F241@6, k=5 → Emb:" married"@6 (de=12.81) +4 more |
| 51 | `inspect_feature` ×8 | L0:241, L0:2242, L0:3024, L2:15317, L0:16013, L0:6548, L0:9076, L1:384 |
| 52 | `get_upstream_features` | L0:F3612@2, k=5 → Emb:" author"@2 (de=16.62) +4 more |
| 53 | `get_upstream_features` | L2:F585@9, k=5 → Emb:" white"@9 (de=30.75) +4 more |
| 54 | `get_upstream_features` | L2:F15317@10, k=5 → Emb:" guy"@10 (de=9.44) +4 more |
| 55 | `get_upstream_features` | L3:F16373@10, k=5 → Emb:" white"@9 (de=23.88) +4 more |
| 56 | `get_upstream_features` | L2:F9320@27, k=5 → ❌ Feature (layer=2, feature_idx=9320) not found at pos=27. Thi |
| 57 | `get_upstream_features` | L4:F15204@9, k=5 → Emb:" white"@9 (de=43.00) +4 more |
| 58 | `get_upstream_features` | L3:F11768@9, k=5 → Emb:" white"@9 (de=26.50) +4 more |
| 59 | `inspect_feature` ×4 | L4:15204, L3:11768, L2:585, L1:13007 |
| 60 | `get_upstream_features` | L2:F1708@9, k=5 → Emb:" white"@9 (de=18.50) +4 more |
| 61 | `get_upstream_features` | L2:F1708@10, k=5 → ❌ Feature (layer=2, feature_idx=1708) not found at pos=10. Thi |
| 62 | `get_upstream_features` | L2:F14965@10, k=5 → Emb:" guy"@10 (de=13.00) +4 more |
| 63 | `get_upstream_features` | L4:F14329@9, k=5 → Emb:" white"@9 (de=12.69) +4 more |
| 64 | `get_upstream_features` | L4:F7136@9, k=5 → Emb:" white"@9 (de=46.00) +4 more |
| 65 | `get_upstream_features` | L5:F14942@10, k=5 → Emb:" guy"@10 (de=5.09) +4 more |
| 66 | `get_upstream_features` | L5:F9988@9, k=5 → Emb:" white"@9 (de=14.62) +4 more |
| 67 | `inspect_feature` ×8 | L2:1708, L2:14965, L4:14329, L4:7136, L5:9988, L2:9301, L5:14942, L1:13023 |
| 68 | `get_upstream_features` | L0:F3612@2, k=5 → Emb:" author"@2 (de=16.62) +4 more |
| 69 | `get_upstream_features` | L0:F11009@2, k=5 → Emb:" author"@2 (de=7.97) +4 more |
| 70 | `get_upstream_features` | L2:F11233@9, k=5 → Emb:" white"@9 (de=5.38) +4 more |
| 71 | `get_upstream_features` | L2:F10433@10, k=5 → Emb:" guy"@10 (de=12.19) +4 more |
| 72 | `get_upstream_features` | L0:F1142@14, k=5 → Emb:" last"@14 (de=35.50) +4 more |
| 73 | `get_upstream_features` | L0:F6127@15, k=5 → Emb:" name"@15 (de=14.31) +4 more |
| 74 | `get_upstream_features` | L0:F4312@15, k=5 → Emb:" name"@15 (de=16.12) +4 more |
| 75 | `get_upstream_features` | L1:F13023@10, k=5 → Emb:" guy"@10 (de=18.25) +4 more |
| 76 | `inspect_feature` ×13 | L0:3612, L0:11009, L2:10433, L2:11233, L0:15578, L1:7821, L1:4668, L0:5247, L0:1142, L0:6127, L0:4312, L2:9320, L2:13158 |
| 77 | `get_upstream_features` | L2:F13158@9, k=5 → Emb:" white"@9 (de=13.62) +4 more |
| 78 | `get_upstream_features` | L2:F13158@27, k=5 → Emb:" oriental"@27 (de=6.28) +4 more |
| 79 | `inspect_feature` | L2, F10986 → "the word "guys" or "guy"" |
| 80 | `get_upstream_features` | L2:F10986@10, k=5 → Emb:" guy"@10 (de=26.50) +4 more |
| 81 | `get_upstream_features` | L6:F15948@10, k=3 → Emb:" guy"@10 (de=9.62) +2 more |
| 82 | `get_upstream_features` | L6:F3902@27, k=3 → Emb:" oriental"@27 (de=8.75) +2 more |
| 83 | `get_upstream_features` | L6:F15948@9, k=3 → ❌ Feature (layer=6, feature_idx=15948) not found at pos=9. Thi |
| 84 | `get_upstream_features` | L6:F3902@9, k=3 → Emb:" white"@9 (de=13.56) +2 more |
| 85 | `get_upstream_features` | L6:F5671@9, k=3 → ❌ Feature (layer=6, feature_idx=5671) not found at pos=9. This |
| 86 | `get_upstream_features` | L6:F5671@27, k=3 → ❌ Feature (layer=6, feature_idx=5671) not found at pos=27. Thi |
| 87 | `get_upstream_features` | L6:F15948@11, k=3 → Emb:"<bos>"@0 (de=3.02) +2 more |
| 88 | `get_upstream_features` | L6:F15948@28, k=3 → Emb:" women"@28 (de=13.81) +2 more |
| 89 | `get_upstream_features` | L6:F15948@33, k=3 → Emb:" men"@33 (de=10.88) +2 more |
| 90 | `get_upstream_features` | L6:F5671@28, k=3 → Emb:" women"@28 (de=10.62) +2 more |
| 91 | `get_upstream_features` | L6:F5671@33, k=3 → Emb:" men"@33 (de=9.94) +2 more |
| 92 | `get_upstream_features` | L3:F15520@10, k=3 → Emb:" guy"@10 (de=17.25) +2 more |
| 93 | `inspect_feature` ×4 | L3:15520, L3:15606, L3:7891, L2:774 |

### Build

`build_circuit` → 19 nodes, 15 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 142,874 | 17,837 | 1,585,163 | 0 | $0.1594 | — | — |
| **Total** | | **142,874** | **17,837** | **1,585,163** | **0** | **$0.1594** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 46s