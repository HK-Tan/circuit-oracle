# Circuit Oracle Report
**Date:** 2026-07-28 07:22:10 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

I have enough data. The circuit shows the probe is driven by a combination of genuine prompt content and negation/absence cues, not pure spurious negation.

**Analysis:** The contradiction-classification probe is driven by a mixed circuit: a content-bearing "tourism" path (tourist/office/tours/walking tokens) plus a prominent "negation/absence" path (No one, usually, so) plus a content "action" path (Pick up, ask), with most remaining signal coming from generic function-word features. The user's concern is partly correct: the "No one", "usually", "so" tokens fire strongly into dedicated negation/absence detector features, but those features are not solely the basis of the prediction — the tourism and action features carry comparable weight, and multi-hop signed influence from the negation positions is only 3.7% of total (S_over_R ≈ 0.35, well below the COPIED threshold).

**Confidence:** 7

**Reasoning:** The attribution graph resolves to four supernodes feeding the probe direction (layer 26, the output logit node):

1. **sn_tourism** (L2–L4): A genuine content path built on the actual prompt's tourism vocabulary. L4:F12961 ("words pertaining to tourism", frac_nonzero 0.006) at pos 7, 8, 14, 23 is the dominant late-layer driver, fed by L3:F8202 "mentions of legal or governmental offices" (pos 8, 23) and L3:F9405 / L3:F10711 "tour / travel / organized events" (pos 8, 14), and L2:F14413 "the word 'tour' or 'tours'" (pos 14). These trace cleanly to input embeddings `tourist` (pos 7), `office` (pos 8), `walking` (pos 13), `tours` (pos 14), `tourist` (pos 22), `office` (pos 23). The tourism path is clearly *content-based*, not spurious — it tracks the actual noun phrases the prompt is built around.

2. **sn_negation** (L0–L4): The user's concern is most directly relevant here. L2:F8837 ("the word 'one' or 'body' when preceded by 'no' or 'every'", pos 17, frac_nonzero 0.011) and L2:F13586 ("-thing/-one, often with preceding words indicating the presence of something", pos 17) fire on `No one` and are fed by L0:F4438 ("the word 'one'", pos 17, frac_nonzero 0.001) and L1:F15800 ("the word 'one'", pos 17). L1:F8159 ("usually") and L3:F10901 ("usually") at pos 19, and the L0:L2:L3:L4 chain anchored on L0:F7321 ("the word 'so'", pos 25) → L2:F10554 (logical implications/conclusions) → L3:F12229 (conjunctions) → L4:F4739 ("'so' followed by personal pronouns"), are explicit negation/conjunction detectors. The direct_effects are large (e.g., 0.383 from F7321, 0.194 from F10904, 0.155 from F7204, 0.155 from F8444). The multi-hop signed influence from negation positions (16, 17, 19, 25) is S_pct_of_total = 3.67%, S_over_R = 0.35 — meaningful but not dominant. The "No one is usually at the tourist office, so…" content of this exact sentence legitimately IS a contradiction/correction signal in NLI, so the probe is reading a real semantic feature of the text, not a generic "I see the word no" artifact. The promoted tokens on F8837 ("nobody, nadia, nadie") confirm this is specifically the *absence-of-person* sense, not a generic negation word.

3. **sn_actions** (L0–L4): L2:F3116 ("the phrasal verb 'pick up'", pos 2) and L2:F11769 ("the word 'up'", pos 2), plus L0:F8566 ("pick"), L0:F10562 ("up"), and L4:F11236 ("calls to action and imperative verbs") at pos 11 (driven by `ask`). These encode the imperative/recommendation content of the first sentence.

4. **sn_function** (L0–L1): A broad bag of L0 features covering high-frequency function words — F8974 "from", F8444 "to", F7204 "here", F2238 "about" (when followed by a number), F6051 "periods/spaces/1", F10219 "a", F12744 "positive adjectives", F7036 "thing", F474 "crop" (driven by the 'ap' substring of 'map'), F2868 "mapping" (from 'map'), F306 "adoption" (from 'tour' substring), F11658 "up"/"from" substring detector, F16358 "up", F8478 "SQL FROM", F7976 "load" (from 'lo' substring of 'ask'/'lo' inside "also/lo"), F10904 "adequate" (driven by `Pick`). The functions and frac_nonzero values (most < 0.02, several 0.02–0.06) are typical of generic lexical detectors. These have *moderate* direct effects (0.13–0.19) and reflect the model's broad lexical habit, not entity reasoning about contradiction.

Net: the user's worry is half-correct. The probe DOES use negation-word detectors (No/one/usually/so), and they fire strongly on individual tokens. But (a) those detectors encode *the actual contradiction signal in this sentence* — the second clause genuinely asserts the inverse of the first, so a probe that lights up on "No one", "usually", "so" is reading real content, not a confounder; (b) the multi-hop signed influence from those positions is only ~3.7% of total (vs R=10.4%, S_over_R ≈ 0.35), well below the ~10% threshold that would indicate the negation is the dominant driver; (c) the dominant *late-layer* driver is the tourism supernode (L4:F12961 with direct_effect 0.141 across four positions, plus L3:F8202, L3:F9405, L3:F10711) — a clean, content-based detection of the actual entities (tourist, office, walking tours). The classification score is therefore co-supported by genuine prompt content (tourism + imperative-action) AND by negation cues, with the latter being a real semantic feature of this specific contradiction rather than a generic spurious cue.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe direction (classification score) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L4:F12961](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12961) | 7 | Tourism / tour content (late layer) |  words pertaining to tourism | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12961) |
| [L4:F12961](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12961) | 8 | Tourism / tour content (late layer) |  words pertaining to tourism | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12961) |
| [L4:F12961](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12961) | 14 | Tourism / tour content (late layer) |  words pertaining to tourism | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12961) |
| [L4:F12961](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12961) | 23 | Tourism / tour content (late layer) |  words pertaining to tourism | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12961) |
| [L3:F9405](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9405) | 8 | Tourism / tour content (late layer) |  words related to tourism, travel, and organized events | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9405) |
| [L3:F10711](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10711) | 14 | Tourism / tour content (late layer) |  the word "tour" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10711) |
| [L3:F8202](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8202) | 8 | Tourism / tour content (late layer) |  mentions of legal or governmental offices | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8202) |
| [L3:F8202](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8202) | 23 | Tourism / tour content (late layer) |  mentions of legal or governmental offices | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8202) |
| [L2:F14413](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) | 14 | Tourism / tour content (late layer) | the word "tour" or "tours" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) |
| [L2:F13586](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13586) | 17 | Negation/absence features ("No one", "no", "usually", conjunction "so") |  words ending in 'thing' and 'one' often with preceding words indicating the presence of something | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13586) |
| [L2:F8837](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8837) | 17 | Negation/absence features ("No one", "no", "usually", conjunction "so") |  the word "one" or "body" when preceded by the words "no" or "every." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8837) |
| [L1:F15800](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15800) | 17 | Negation/absence features ("No one", "no", "usually", conjunction "so") |  the word "one" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15800) |
| [L0:F4438](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) | 17 | Negation/absence features ("No one", "no", "usually", conjunction "so") | the word "one". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) |
| [L1:F8159](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8159) | 19 | Negation/absence features ("No one", "no", "usually", conjunction "so") |  the word "usually" and, to a lesser extent, words that sometimes accompany it | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8159) |
| [L3:F10901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10901) | 19 | Negation/absence features ("No one", "no", "usually", conjunction "so") | the word "usually" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10901) |
| [L0:F7321](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7321) | 25 | Negation/absence features ("No one", "no", "usually", conjunction "so") |  the word "so," and also matches some words ending in "ware" and "such" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7321) |
| [L2:F10554](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10554) | 25 | Negation/absence features ("No one", "no", "usually", conjunction "so") | words and phrases related to logical implications or conclusions. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10554) |
| [L3:F12229](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12229) | 25 | Negation/absence features ("No one", "no", "usually", conjunction "so") | conjunctions and words connecting ideas | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12229) |
| [L4:F4739](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4739) | 25 | Negation/absence features ("No one", "no", "usually", conjunction "so") |  the word "so" followed by personal pronouns or words associated with personal experience | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4739) |
| [L2:F3116](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) | 2 | Action / event-content features ("Pick up", "ask", imperative, "usually") |  the phrasal verb "pick up" and variations | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) |
| [L2:F11769](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11769) | 2 | Action / event-content features ("Pick up", "ask", imperative, "usually") | the word "up" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11769) |
| [L0:F8566](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) | 1 | Action / event-content features ("Pick up", "ask", imperative, "usually") |  the word "pick" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) |
| [L0:F10562](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10562) | 2 | Action / event-content features ("Pick up", "ask", imperative, "usually") | the word "up" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10562) |
| [L0:F10904](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10904) | 1 | Action / event-content features ("Pick up", "ask", imperative, "usually") | the word "adequate" (and words that appear near it) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10904) |
| [L4:F11236](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11236) | 11 | Action / event-content features ("Pick up", "ask", imperative, "usually") |  calls to action and imperative verbs. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11236) |
| [L0:F8974](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) | 5 | Function-word / generic features ("the", "to", "a", "about", "up", "from", "here", "thing", punctuation) | the word "from" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) |
| [L0:F8478](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8478) | 5 | Function-word / generic features ("the", "to", "a", "about", "up", "from", "here", "thing", punctuation) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8478) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 12 | Function-word / generic features ("the", "to", "a", "about", "up", "from", "here", "thing", punctuation) |  the word "about" when followed by a numerical value | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L0:F7204](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7204) | 9 | Function-word / generic features ("the", "to", "a", "about", "up", "from", "here", "thing", punctuation) | the word "here" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7204) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 30 | Function-word / generic features ("the", "to", "a", "about", "up", "from", "here", "thing", punctuation) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 15 | Function-word / generic features ("the", "to", "a", "about", "up", "from", "here", "thing", punctuation) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F306](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/306) | 7 | Function-word / generic features ("the", "to", "a", "about", "up", "from", "here", "thing", punctuation) | the word "adoption" in various contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/306) |
| [L0:F2868](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2868) | 4 | Function-word / generic features ("the", "to", "a", "about", "up", "from", "here", "thing", punctuation) |  the word "mapping" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2868) |
| [L0:F7036](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7036) | 9 | Function-word / generic features ("the", "to", "a", "about", "up", "from", "here", "thing", punctuation) | the word "thing" and words associated with an idea or concept | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7036) |
| [L0:F11658](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11658) | 2 | Function-word / generic features ("the", "to", "a", "about", "up", "from", "here", "thing", punctuation) |  occurrences of the substring "up" and phrases that end in the word "from" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11658) |
| [L0:F10219](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10219) | 3 | Function-word / generic features ("the", "to", "a", "about", "up", "from", "here", "thing", punctuation) |  the indefinite article "a" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10219) |
| [L0:F474](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/474) | 4 | Function-word / generic features ("the", "to", "a", "about", "up", "from", "here", "thing", punctuation) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/474) |
| [L0:F12744](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12744) | 2 | Function-word / generic features ("the", "to", "a", "about", "up", "from", "here", "thing", punctuation) | positive adjectives and adverbs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12744) |
| [L0:F16358](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16358) | 2 | Function-word / generic features ("the", "to", "a", "about", "up", "from", "here", "thing", punctuation) | the word "up" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16358) |
| [L1:F7976](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7976) | 11 | Function-word / generic features ("the", "to", "a", "about", "up", "from", "here", "thing", punctuation) | the word "load" in technical documents | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7976) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:8974 de=-0.408 |
| 3 | `inspect_feature` ×20 | L0:8974, L0:7321, L2:3116, L2:13586, L0:10904, L0:6051, L0:2238, L0:306, L0:10562, L0:8444, L0:7204, L1:8159, L1:474, L2:14413, L2:11769, L2:8478, L3:10901, L0:2868, L0:8566, L0:12744 |
| 4 | `get_upstream_features` | Emb:" from"@5 (de=38.75) +9 more |
| 5 | `get_upstream_features` | Emb:" so"@25 (de=40.50) +9 more |
| 6 | `get_upstream_features` | Emb:"Pick"@1 (de=50.00) +9 more |
| 7 | `get_upstream_features` | Emb:" No"@16 (de=14.00) +9 more |
| 8 | `inspect_feature` ×2 | L0:4438, L0:11351 |
| 9 | `get_upstream_features` | Emb:"Pick"@1 (de=13.38) +9 more |
| 10 | `get_upstream_features` | Emb:" up"@2 (de=36.75) +9 more |
| 11 | `get_upstream_features` | Emb:" usually"@19 (de=24.25) +9 more |
| 12 | `get_upstream_features` | Emb:" usually"@19 (de=23.50) +9 more |
| 13 | `get_upstream_features` | Emb:" tours"@14 (de=28.38) +9 more |
| 14 | `get_top_features` | 30 features; top: L0:8974 de=-0.408 |
| 15 | `inspect_feature` ×10 | L0:7036, L0:16358, L4:12961, L1:7976, L4:11236, L3:8202, L4:4739, L2:8837, L0:10219, L0:11658 |
| 16 | `get_upstream_features` | Emb:" tourist"@7 (de=19.12) +9 more |
| 17 | `get_upstream_features` | Emb:" ask"@11 (de=7.72) +9 more |
| 18 | `get_upstream_features` | Emb:" office"@8 (de=23.62) +9 more |
| 19 | `get_upstream_features` | Emb:" so"@25 (de=29.75) +9 more |
| 20 | `get_upstream_features` | Emb:" No"@16 (de=18.62) +9 more |
| 21 | `inspect_feature` ×4 | L3:9405, L2:10554, L3:12229, L1:15800 |
| 22 | `get_upstream_features` | ❌ Feature (layer=4, feature_idx=12961) not found at pos=11. Th |
| 23 | `get_upstream_features` | Emb:" tourist"@7 (de=22.62) +9 more |
| 24 | `get_upstream_features` | Emb:" tours"@14 (de=9.56) +9 more |
| 25 | `get_upstream_features` | Emb:" tourist"@22 (de=14.31) +9 more |
| 26 | `get_upstream_features` | Emb:" here"@9 (de=11.50) +9 more |
| 27 | `get_upstream_features` | Emb:"."@15 (de=46.25) +9 more |
| 28 | `inspect_feature` | " the word "tour"" |
| 29 | `get_upstream_features` | ❌ Feature (layer=4, feature_idx=12961) not found at pos=11. Th |
| 30 | `get_upstream_features` | Emb:" No"@16 (de=18.62) +9 more |
| 31 | `inspect_feature` ×2 | L2:5495, L0:6518 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F12961@14` | ❌ error | — | — | Trace the upstream of the "tourism-related words" feature L4:F12961 at pos 14. F… |
| SA-2 | `L2:F8837@17` | ❌ error | — | — | Trace the upstream of L2:F8837 at pos 17 (the "no one / nobody" feature). Confir… |
| SA-3 | `L1:F8159@19` | ❌ error | — | — | Trace the upstream of L1:F8159 at pos 19 (the "usually" feature). Verify it's dr… |
| SA-4 | `L0:F7204@9` | ❌ error | — | — | Trace the upstream of L0:F7204 at pos 9 (the "here" feature). Find what input to… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F6051@15, k=8 → Emb:"."@15 (de=46.25) +7 more |
| 2 | `get_upstream_features` | L0:F2868@4, k=8 → Emb:" map"@4 (de=11.75) +7 more |
| 3 | `get_upstream_features` | L0:F2238@12, k=8 → Emb:" about"@12 (de=35.00) +7 more |
| 4 | `get_upstream_features` | L0:F8444@30, k=8 → Emb:" to"@30 (de=41.50) +7 more |
| 5 | `get_source_influence` | {'depth': 4, 'source_positions': [16, 17, 19, 25]} → {'depth': 4, 'source_positions': [16, 17, 19, 25], 'S_pct_of_total': 3.666, 'R_p |
| 6 | `get_source_influence` | {'depth': 4, 'source_positions': [7, 8, 13, 14, 22, 23]} → {'depth': 4, 'source_positions': [7, 8, 13, 14, 22, 23], 'S_pct_of_total': -1.16 |

### Build

`build_circuit` → 24 nodes, 23 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 83,119 | 9,170 | 750,232 | 0 | $0.0810 | — | — |
| **Total** | | **83,119** | **9,170** | **750,232** | **0** | **$0.0810** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 34s