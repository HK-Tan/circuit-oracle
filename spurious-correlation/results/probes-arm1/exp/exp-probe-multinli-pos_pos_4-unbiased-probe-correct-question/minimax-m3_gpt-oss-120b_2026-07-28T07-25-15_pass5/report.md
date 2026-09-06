# Circuit Oracle Report
**Date:** 2026-07-28 07:25:15 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction classification is driven by a combination of surface-level lexical cues and pragmatic/syntactic patterns, not by deep semantic understanding of the entailment relationship; "No one is usually at the tourist office" — a negative frequency statement — is a dominant signal, alongside bag-of-content-word features for "map/pick up/tourist/office".

**Confidence:** 6

**Reasoning:** The circuit shows a clear mixture of two signal types. On the **negation/lexical surface** side, the most positively-contributing features are highly corpus-frequent, low-content function-word and bigram detectors: L0:F8974 "from" (pos 5, direct_effect = -0.41), L0:F7321 "so" (pos 25, +0.38), L2:F13586 "one"/"body" (pos 17, -0.21), L2:F8837 "No one"/"everybody" (pos 17, -0.13), L2:F11769 "up" (pos 2, -0.20), and L1:F8159 + L2:F5495 + L3:F10901 + L4:F9952 all firing on "usually" at pos 19 (the "No one is **usually** at…" adverb-of-frequency stack). These directly feed the output logit.

Critically, the user's hypothesis is **partially supported but not fully correct**. The circuit is NOT purely "negation-word" features. It also contains genuine content features: L2:F3116 "pick up" (pos 2, -0.35), L1:F13179 "pick" (pos 1), L2:F14413 "tour" (pos 14, -0.17), L0:F306 "adoption" (a false-positive that fires here, pos 7, +0.19), L0:F7204 "here" (pos 9, +0.16), L3:F8202 + L4:F12961 "office" (pos 8), L0:F2868 "mapping" (pos 4, +0.14), and the L6:F10619 "map/navigation/travel" feature (pos 4, with frac_nonzero = 0.59 — broad context). A higher-level L14:F7909 (review-sentiment, frac_nonzero 0.027) and L10:F6670 (technical/scientific) also contribute small amounts.

The "No one is usually at the tourist office" sub-sentence is over-represented in the top features (L0:F7321 "so", L1:F8159 "usually", L2:F8837 "No one", L2:F13586 "one", L0:F306 "adoption" (a generic ambiguity), L0:F15047 "often/usually/typically"). These are **spurious surface cues** — they reflect the form of a hedging negation more than its meaning. However, the *content-word* path (L2:F3116 "pick up", L2:F14413 "tours", L3:F8202 "office", L6:F10619 "maps/travel") is *also* a substantial driver, and that path is *not* a spurious negation feature — it encodes the actual lexical-semantic content of the premise/hypothesis pair.

The most negative direct_effects come from the "from" (L0:F8974, -0.41) and "pick up" (L2:F3116, -0.35) features, which push *against* the contradiction label — likely because the *premise* and *hypothesis* share this content (both mention picking up a map at a tourist office), which is what a proper NLI model should use. But the largest *positive* contributions (driving "contradiction") come from the "so" (L0:F7321, +0.38), "adoption" (L0:F306, +0.19), and "here" (L0:F7204, +0.16) features, which are shallow function-word/keyword patterns rather than entailment reasoning.

**Verdict on the user's concern:** The user's concern is **substantively correct but overstated**. The circuit does rely heavily on **non-semantic surface signals** — most prominently the combination of negation word "No" + frequency adverb "usually" + connective "so" in the second sentence. These features fire on the *form* of a hedging/corrective statement rather than the *entailment relationship*. However, the circuit is not *only* these; it also has content-word features (pick up, map, tourist, office, tours) that fire on legitimate shared-content cues. The probe appears to be a partial-spurious-feature mixture: it has learned that sentences containing a "No one is usually at X, so you'll have to go somewhere else" pattern tend to be labelled contradiction (because the hypothesis claims you can pick up a map *at* the tourist office, contradicting the premise that no one is there), but the features it uses are mix of correct content overlap (map/office/tour) and spurious pattern matching (No/usually/so concatenation). A more honest NLI probe would isolate the *entailment-violating* content rather than this mixture.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F9952](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9952) | 19 | L4: Adverbs of frequency ('usually' pos 19) | adverbs that describe how frequently something happens | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9952) |
| [L2:F5495](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5495) | 19 | L4: Adverbs of frequency ('usually' pos 19) |  adverbs of frequency | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5495) |
| [L1:F8159](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8159) | 19 | L4: Adverbs of frequency ('usually' pos 19) |  the word "usually" and, to a lesser extent, words that sometimes accompany it | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8159) |
| [L3:F10901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10901) | 19 | L4: Adverbs of frequency ('usually' pos 19) | the word "usually" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10901) |
| [L0:F12167](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12167) | 19 | L4: Adverbs of frequency ('usually' pos 19) |  the word "usually" in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12167) |
| [L0:F15047](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15047) | 19 | L4: Adverbs of frequency ('usually' pos 19) |  the words "often", "usually", and "typically." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15047) |
| [L4:F4739](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4739) | 25 | L4: Adverbs of frequency ('usually' pos 19) |  the word "so" followed by personal pronouns or words associated with personal experience | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4739) |
| [L3:F1828](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1828) | 17 | L2-3: 'No one' / 'one' / 'body' negation (pos 16-17) |  the word "one" or "body" referring to people | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1828) |
| [L2:F8837](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8837) | 17 | L2-3: 'No one' / 'one' / 'body' negation (pos 16-17) |  the word "one" or "body" when preceded by the words "no" or "every." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8837) |
| [L2:F13586](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13586) | 17 | L2-3: 'No one' / 'one' / 'body' negation (pos 16-17) |  words ending in 'thing' and 'one' often with preceding words indicating the presence of something | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13586) |
| [L0:F4438](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) | 17 | L2-3: 'No one' / 'one' / 'body' negation (pos 16-17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) |
| [L0:F8974](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) | 5 | L0: Function-word features ('from' pos 5, 'so' pos 25, 'here' pos 9, 'about' pos 12, etc.) | the word "from" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) |
| [L0:F7321](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7321) | 25 | L0: Function-word features ('from' pos 5, 'so' pos 25, 'here' pos 9, 'about' pos 12, etc.) |  the word "so," and also matches some words ending in "ware" and "such" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7321) |
| [L0:F7204](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7204) | 9 | L0: Function-word features ('from' pos 5, 'so' pos 25, 'here' pos 9, 'about' pos 12, etc.) | the word "here" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7204) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 12 | L0: Function-word features ('from' pos 5, 'so' pos 25, 'here' pos 9, 'about' pos 12, etc.) |  the word "about" when followed by a numerical value | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L0:F306](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/306) | 7 | L0: Function-word features ('from' pos 5, 'so' pos 25, 'here' pos 9, 'about' pos 12, etc.) | the word "adoption" in various contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/306) |
| [L0:F3255](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) | 10 | L0: Function-word features ('from' pos 5, 'so' pos 25, 'here' pos 9, 'about' pos 12, etc.) |  the word "and" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 30 | L0: Function-word features ('from' pos 5, 'so' pos 25, 'here' pos 9, 'about' pos 12, etc.) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F8566](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) | 1 | L0: Function-word features ('from' pos 5, 'so' pos 25, 'here' pos 9, 'about' pos 12, etc.) |  the word "pick" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) |
| [L0:F10562](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10562) | 2 | L0: Function-word features ('from' pos 5, 'so' pos 25, 'here' pos 9, 'about' pos 12, etc.) | the word "up" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10562) |
| [L0:F10219](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10219) | 3 | L0: Function-word features ('from' pos 5, 'so' pos 25, 'here' pos 9, 'about' pos 12, etc.) |  the indefinite article "a" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10219) |
| [L0:F10904](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10904) | 1 | L0: Function-word features ('from' pos 5, 'so' pos 25, 'here' pos 9, 'about' pos 12, etc.) | the word "adequate" (and words that appear near it) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10904) |
| [L2:F3116](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) | 2 | L0-2: Content-word features ('pick up' pos 1-2, 'map' pos 4, 'tourist' pos 7) |  the phrasal verb "pick up" and variations | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) |
| [L2:F11769](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11769) | 2 | L0-2: Content-word features ('pick up' pos 1-2, 'map' pos 4, 'tourist' pos 7) | the word "up" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11769) |
| [L1:F13179](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13179) | 1 | L0-2: Content-word features ('pick up' pos 1-2, 'map' pos 4, 'tourist' pos 7) | the words "pick", "picker", and forms of those words | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13179) |
| [L0:F16358](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16358) | 2 | L0-2: Content-word features ('pick up' pos 1-2, 'map' pos 4, 'tourist' pos 7) | the word "up" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16358) |
| [L0:F2868](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2868) | 4 | L0-2: Content-word features ('pick up' pos 1-2, 'map' pos 4, 'tourist' pos 7) |  the word "mapping" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2868) |
| [L0:F10891](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10891) | 14 | L0-2: Content-word features ('pick up' pos 1-2, 'map' pos 4, 'tourist' pos 7) |  words connected to excursions and professions | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10891) |
| [L2:F14413](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) | 14 | L0-2: Content-word features ('pick up' pos 1-2, 'map' pos 4, 'tourist' pos 7) | the word "tour" or "tours" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) |
| [L0:F11658](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11658) | 2 | L0-2: Content-word features ('pick up' pos 1-2, 'map' pos 4, 'tourist' pos 7) |  occurrences of the substring "up" and phrases that end in the word "from" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11658) |
| [L1:F7976](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7976) | 11 | L0-2: Content-word features ('pick up' pos 1-2, 'map' pos 4, 'tourist' pos 7) | the word "load" in technical documents | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7976) |
| [L0:F12744](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12744) | 2 | L0-2: Content-word features ('pick up' pos 1-2, 'map' pos 4, 'tourist' pos 7) | positive adjectives and adverbs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12744) |
| [L3:F8202](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8202) | 8 | L3-4: 'office' (pos 8), 'so' (pos 25) features |  mentions of legal or governmental offices | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8202) |
| [L4:F12961](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12961) | 8 | L3-4: 'office' (pos 8), 'so' (pos 25) features |  words pertaining to tourism | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12961) |
| [L3:F14712](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14712) | 25 | L3-4: 'office' (pos 8), 'so' (pos 25) features | occurrences of the word "so" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14712) |
| [L1:F15604](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15604) | 8 | L3-4: 'office' (pos 8), 'so' (pos 25) features |  words and phrases related to political elections for judicial positions | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15604) |
| [L4:F7069](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7069) | 4 | L3-4: 'office' (pos 8), 'so' (pos 25) features |  words related to the geoserver and accessing layers in it | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7069) |
| [L6:F10619](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10619) | 4 | L6-8: Higher-level context (maps/travel, 'so' decisions) |  words about maps, navigation and travel | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10619) |
| [L8:F15489](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15489) | 25 | L6-8: Higher-level context (maps/travel, 'so' decisions) | text where a person is thinking or making a decision, often signalled by the word "so." | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15489) |
| [L10:F6670](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) | 23 | L6-8: Higher-level context (maps/travel, 'so' decisions) | technical terms, especially within scientific or medical contexts | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) |
| [L14:F7909](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/7909) | 24 | L6-8: Higher-level context (maps/travel, 'so' decisions) | both positive and negative sentiment and descriptive words, especially in reviews. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/7909) |
| [L4:F15094](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15094) | 4 | L4-5: Tourism / paper / map context features (pos 4-5) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15094) |
| [L4:F11969](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11969) | 4 | L4-5: Tourism / paper / map context features (pos 4-5) |  mentions of printed advertising materials | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11969) |
| [L4:F10233](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10233) | 5 | L4-5: Tourism / paper / map context features (pos 4-5) | words and phrases related to calls to action | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10233) |
| [L0:F11236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11236) | 11 | L4-5: Tourism / paper / map context features (pos 4-5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11236) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:8974 de=-0.408 |
| 3 | `get_top_features` | 50 features; top: L0:8974 de=-0.408 |
| 4 | `inspect_feature` ×50 | L0:8974, L0:7321, L2:3116, L2:13586, L2:11769, L0:10904, L0:6051, L0:2238, L0:306, L1:8159, L0:10562, L2:14413, L0:8566, L0:7204, L0:8444, L0:12744, L1:474, L2:8478, L3:10901, L0:2868, L0:15047, L0:10891, L0:3255, L2:13998, L2:5495, L2:8837, L3:1618, L3:1828, L4:4739, L3:8202, L4:9952, L10:6670, L1:13179, L1:15604, L3:14712, L4:7069, L14:7909, L6:10619, L5:15094, L4:11969, L0:16358, L0:7036, L4:12961, L1:7976, L4:11236, L0:10219, L0:11658, L0:12167, L8:15489, L4:10233 |
| 5 | `get_upstream_features` | Emb:" from"@5 (de=38.75) +14 more |
| 6 | `get_upstream_features` | Emb:" so"@25 (de=40.50) +14 more |
| 7 | `get_upstream_features` | Emb:"Pick"@1 (de=50.00) +14 more |
| 8 | `get_upstream_features` | Emb:"Pick"@1 (de=13.38) +9 more |
| 9 | `get_upstream_features` | Emb:" tourist"@7 (de=22.00) +9 more |
| 10 | `get_upstream_features` | Emb:" here"@9 (de=41.00) +9 more |
| 11 | `get_upstream_features` | Emb:" to"@30 (de=41.50) +9 more |
| 12 | `get_upstream_features` | Emb:" tours"@14 (de=28.38) +9 more |
| 13 | `get_upstream_features` | Emb:"."@15 (de=46.25) +9 more |
| 14 | `get_upstream_features` | Emb:" about"@12 (de=35.00) +9 more |
| 15 | `get_upstream_features` | Emb:" usually"@19 (de=24.25) +9 more |
| 16 | `get_upstream_features` | Emb:" up"@2 (de=36.75) +9 more |
| 17 | `get_upstream_features` | Emb:" is"@18 (de=11.00) +9 more |
| 18 | `get_upstream_features` | L2:F8837 (de=7.16) +7 more |
| 19 | `get_upstream_features` | Emb:" usually"@19 (de=31.25) +7 more |
| 20 | `get_upstream_features` | Emb:" usually"@19 (de=38.75) +7 more |
| 21 | `get_upstream_features` | Emb:" so"@25 (de=29.75) +7 more |
| 22 | `get_upstream_features` | Emb:" here"@9 (de=33.25) +7 more |
| 23 | `get_upstream_features` | Emb:" No"@16 (de=18.62) +7 more |
| 24 | `get_upstream_features` | Emb:" No"@16 (de=29.38) +4 more |
| 25 | `get_upstream_features` | Emb:" one"@17 (de=38.50) +4 more |
| 26 | `get_upstream_features` | Emb:" No"@16 (de=14.00) +4 more |
| 27 | `get_upstream_features` | Emb:" office"@8 (de=23.62) +7 more |
| 28 | `get_upstream_features` | Emb:" tourist"@7 (de=19.12) +7 more |
| 29 | `get_upstream_features` | Emb:" so"@25 (de=24.25) +7 more |
| 30 | `get_upstream_features` | Emb:" up"@2 (de=19.50) +7 more |
| 31 | `get_upstream_features` | Emb:" usually"@19 (de=1.94) +7 more |
| 32 | `get_upstream_features` | Emb:"<bos>"@0 (de=-2.09) +7 more |
| 33 | `get_upstream_features` | Emb:"Pick"@1 (de=21.62) +7 more |
| 34 | `get_upstream_features` | Emb:" tours"@14 (de=18.12) +7 more |
| 35 | `get_upstream_features` | Emb:" so"@25 (de=18.50) +7 more |
| 36 | `get_upstream_features` | Emb:" ask"@11 (de=32.00) +7 more |
| 37 | `get_upstream_features` | Emb:" ask"@11 (de=7.72) +7 more |
| 38 | `get_upstream_features` | Emb:" map"@4 (de=22.88) +7 more |
| 39 | `get_upstream_features` | Emb:"Pick"@1 (de=2.55) +7 more |
| 40 | `get_upstream_features` | L2:F3116 (de=2.58) +7 more |
| 41 | `get_upstream_features` | Emb:" map"@4 (de=5.94) +7 more |
| 42 | `get_upstream_features` | Emb:" office"@8 (de=12.38) +7 more |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L3:F1828@17` | ❌ error | — | — | Trace the path from L3:F1828 (the word "one"/"body" referring to people, at posi… |
| SA-2 | `L4:F9952@19` | ❌ error | — | — | Trace the path from L4:F9952 (adverbs of frequency at position 19) — what featur… |
| SA-3 | `L0:F7321@25` | ❌ error | — | — | Trace the path from L0:F7321 (the word "so" at position 25) — what tokens and fe… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L10:F6670@23, k=5 → Emb:" usually"@19 (de=1.94) +4 more |
| 2 | `get_upstream_features` | L6:F10619@4, k=5 → Emb:" map"@4 (de=11.50) +4 more |
| 3 | `get_upstream_features` | L0:F10562@2, k=3 → Emb:" up"@2 (de=36.75) +2 more |
| 4 | `get_upstream_features` | L2:F5495@19, k=3 → Emb:" usually"@19 (de=31.25) +2 more |

### Build

`build_circuit` → 32 nodes, 40 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 112,754 | 14,731 | 1,201,911 | 0 | $0.1236 | — | — |
| **Total** | | **112,754** | **14,731** | **1,201,911** | **0** | **$0.1236** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 2s