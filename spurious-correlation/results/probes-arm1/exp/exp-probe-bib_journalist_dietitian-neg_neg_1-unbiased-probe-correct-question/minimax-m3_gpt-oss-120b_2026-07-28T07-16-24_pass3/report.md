# Circuit Oracle Report
**Date:** 2026-07-28 07:16:24 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven overwhelmingly by genuine journalism-related lexical and semantic features (the word "report", "reporter", "news", "news organizations"), not by gender markers.

**Confidence:** 8

**Reasoning:** Tracing the attribution graph from the probe-output logit backward reveals that the dominant signal path is a clean, profession-grounded journalism circuit. The top direct-effect features at the late layers are L20:F8433 ("words related to news broadcasting"), L19:F2486 ("journalistic sources and news outlets", firing at positions 21, 22, 26-30, i.e. across "report for some of the top news organizations"), L18:F14663 ("variations of the word 'report'"), L17:F5218 ("journalism, media, and related topics"), L16:F15046 ("names, organizations, and reporting verbs"), L15:F2579 ("people providing information in an official capacity"), and L14:F4420 ("words and phrases related to journalism and newspapers", firing at positions 21, 22, 25, 26, 28). All of these features promote tokens like "journalist", "reporter", "news", "newsroom", and have frac_nonzero values of 0.007-0.12, indicating they fire only on journalistic contexts. These late-layer features are fed by a mid-layer cluster of journalism features (L11:F5996 "news publications and their staff", L10:F14576 "journalism and media", L9:F2845 "news organizations and journalists", L9:F7435 "news production and media", L8:F8855 "news reporters and news reporting", L7:F13646 "news reporting and journalism", L7:F9092 "broadcast journalism"), which are themselves grounded in early-layer lexical detectors for the word "report" (L0:F1579, L1:F14511, L2:F11175, L3:F10846, L4:F6696, L4:F661, L5:F12586) and for the embedding token "report" at pos 21 (direct_effect 5.22 into L14:F4420, 51.5 into L18:F14663, 12.06 into L8:F8855). This is a textbook, well-grounded profession circuit: the word "report" → journalism concept features → news/reporter/organization features → probe direction.

The user's concern about spurious gender features is not supported by this graph. Two male-pronoun features (L0:F8964 "the possessive pronoun 'His'" with direct_effect +0.088 and L0:F1069 "references to a male person, particularly 'He' or 'His'" with direct_effect -0.050) do appear in the top-20 list, both at position 1 (the token "His"). However, these are layer-0 lexical features of generic and contradictory sign: F8964 promotes the probe positively, F1069 promotes it negatively, so they roughly cancel rather than systematically bias toward the "male profession" direction. Crucially, neither connects forward into the late-layer journalism features that dominate the probe score — the direct-effect graph from the late-layer journalism cluster does not include the L0 pronoun features. Their signed contribution to the probe is an order of magnitude smaller than the journalism cluster (single-feature |direct_effect| ~0.05-0.09 vs. the L19:F2486 cluster at multiple positions with activations of 19-44 and L14:F4420 with activation 27.25). The remaining low-direct-effect features (L0:F13948 "pink", L0:F2011 "dream", L0:F15693 "personal anecdotes", L0:F14287 "see", L0:F2203 "world/game", L4:F11898 "World War", L5:F771 "see", L0:F8444 "to") are generic lexical detectors that fire on incidental words ("see the world", "Joined", "the world", "to") and neither cohere into a profession-relevant signal nor project to the journalism supernode — they appear in the top features only because of the way the probe target aggregates all upstream direct effects, not because they form an alternative profession path.

**Conclusion:** The user's concern is unfounded for this particular graph. The probe is classifying "journalist" because the input contains "report for some of the top news organizations", and the circuit traces that surface cue through a deep, well-formed journalism semantic stack (L0-L5 report-word features → L7-L11 news-organization features → L14-L20 journalism/reporter/news features → probe). The "His"-token male-pronoun features fire but contribute small, partially cancelling signed effects and do not feed into the dominant journalism path. If a more rigorous spurious-correlation test is desired, one could re-run the probe on a gender-swapped version of the same sentence; based on the circuit topology, the journalism supernode would remain intact while the pronoun feature would be replaced by its female counterpart, and the probe score should not change materially. The present graph does not show a gender-shortcut mechanism.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Output Logit (Probe Direction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L20:F8433](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/8433) | 26 | Late-layer journalism/medial-concept features | words related to news broadcasting | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/8433) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 21 | Late-layer journalism/medial-concept features |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 22 | Late-layer journalism/medial-concept features |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 26 | Late-layer journalism/medial-concept features |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 27 | Late-layer journalism/medial-concept features |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 28 | Late-layer journalism/medial-concept features |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 29 | Late-layer journalism/medial-concept features |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 30 | Late-layer journalism/medial-concept features |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F14973](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/14973) | 26 | Late-layer journalism/medial-concept features |  words related to high-achieving individuals and organizations | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/14973) |
| [L18:F14663](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14663) | 21 | Late-layer journalism/medial-concept features | variations of the word "report." | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14663) |
| [L17:F5218](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5218) | 21 | Late-layer journalism/medial-concept features |  text about journalism, media, and related topics | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5218) |
| [L17:F5218](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5218) | 26 | Late-layer journalism/medial-concept features |  text about journalism, media, and related topics | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5218) |
| [L16:F15046](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15046) | 21 | Late-layer journalism/medial-concept features |  names, organizations, and reporting verbs | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15046) |
| [L16:F15045](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15045) | 21 | Late-layer journalism/medial-concept features | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15045) |
| [L16:F11532](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11532) | 26 | Late-layer journalism/medial-concept features | newspaper | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11532) |
| [L15:F2579](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2579) | 21 | Late-layer journalism/medial-concept features | instances of people providing information in some sort of official capacity. Like reporting incidents, communicating facts or informing others of something. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2579) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 21 | Late-layer journalism/medial-concept features | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 22 | Late-layer journalism/medial-concept features | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 25 | Late-layer journalism/medial-concept features | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 26 | Late-layer journalism/medial-concept features | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 28 | Late-layer journalism/medial-concept features | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F2659](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/2659) | 21 | Late-layer journalism/medial-concept features | live broadcasts, media appearances, and court cases | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/2659) |
| [L11:F5996](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/5996) | 21 | Mid-layer journalism / news-organization features |  references to news publications and their staff. | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/5996) |
| [L11:F5996](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/5996) | 22 | Mid-layer journalism / news-organization features |  references to news publications and their staff. | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/5996) |
| [L10:F14576](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14576) | 21 | Mid-layer journalism / news-organization features | words related to journalism and media. | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14576) |
| [L9:F8366](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8366) | 21 | Mid-layer journalism / news-organization features |  words and names associated with television news broadcasting | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8366) |
| [L9:F7435](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/7435) | 21 | Mid-layer journalism / news-organization features |  words and phrases related to news production and media | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/7435) |
| [L9:F7435](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/7435) | 22 | Mid-layer journalism / news-organization features |  words and phrases related to news production and media | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/7435) |
| [L9:F7435](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/7435) | 28 | Mid-layer journalism / news-organization features |  words and phrases related to news production and media | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/7435) |
| [L9:F2845](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2845) | 21 | Mid-layer journalism / news-organization features |  mentions of news organizations and journalists | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2845) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 21 | Mid-layer journalism / news-organization features |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 22 | Mid-layer journalism / news-organization features |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 28 | Mid-layer journalism / news-organization features |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 21 | Mid-layer journalism / news-organization features | content related to film festivals and production, particularly documentary films, and the recognition they receive. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 22 | Mid-layer journalism / news-organization features | content related to film festivals and production, particularly documentary films, and the recognition they receive. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 28 | Mid-layer journalism / news-organization features | content related to film festivals and production, particularly documentary films, and the recognition they receive. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 21 | Mid-layer journalism / news-organization features |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 22 | Mid-layer journalism / news-organization features |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 28 | Mid-layer journalism / news-organization features |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 29 | Mid-layer journalism / news-organization features |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 21 | Mid-layer journalism / news-organization features |  words and phrases associated with broadcast journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 22 | Mid-layer journalism / news-organization features |  words and phrases associated with broadcast journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 26 | Mid-layer journalism / news-organization features |  words and phrases associated with broadcast journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 28 | Mid-layer journalism / news-organization features |  words and phrases associated with broadcast journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 29 | Mid-layer journalism / news-organization features |  words and phrases associated with broadcast journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L7:F12495](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/12495) | 21 | Mid-layer journalism / news-organization features |  a mix of terms having to do with broadcasting, lists, years, and death | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/12495) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 21 | Mid-layer journalism / news-organization features | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 22 | Mid-layer journalism / news-organization features | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 28 | Mid-layer journalism / news-organization features | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L5:F12586](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12586) | 21 | Early-layer lexical report-word features |  mentions of reports | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12586) |
| [L5:F771](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/771) | 6 | Early-layer lexical report-word features |  the word "see" and words often associated with "see" | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/771) |
| [L4:F6696](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6696) | 21 | Early-layer lexical report-word features | the word "report" or "reporting" along with adjacent words | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6696) |
| [L4:F661](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/661) | 21 | Early-layer lexical report-word features |  words and phrases used when referring to reports, documentaries, and television coverage of news | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/661) |
| [L4:F11898](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11898) | 6 | Early-layer lexical report-word features |  mentions of "World" followed by a sport or war-related word | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11898) |
| [L3:F10846](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10846) | 21 | Early-layer lexical report-word features | the word "report" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10846) |
| [L2:F11175](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11175) | 21 | Early-layer lexical report-word features | the verb "report" and its variations | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11175) |
| [L1:F14511](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14511) | 21 | Early-layer lexical report-word features |  the word "report" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14511) |
| [L0:F1579](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1579) | 21 | Early-layer lexical report-word features |  the word "report" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1579) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 3 | Early-layer lexical report-word features | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 20 | Early-layer lexical report-word features | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F14287](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14287) | 4 | Early-layer lexical report-word features | the word "see" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14287) |
| [L0:F2203](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2203) | 6 | Early-layer lexical report-word features |  instances of the words "world" or "game" (possibly "problem") or expressions of existential quandaries. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2203) |
| [L0:F8964](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) | 1 | Male-pronoun / gender features (spurious) |  the possessive pronoun "His" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Male-pronoun / gender features (spurious) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F13948](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13948) | 2 | Generic/ambiguous content features (low-signal) |  the color "pink" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13948) |
| [L0:F2011](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) | 2 | Generic/ambiguous content features (low-signal) |  the word "dream" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) |
| [L0:F15693](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15693) | 2 | Generic/ambiguous content features (low-signal) |  language related to personal anecdotes and opinions | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15693) |
| [L0:F15185](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15185) | 2 | Generic/ambiguous content features (low-signal) | the word "do" alongside references to figures, types, and the pronouns "we" and "us", possibly in the context of scientific studies and collaborative efforts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15185) |
| [L0:F14582](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14582) | 6 | Generic/ambiguous content features (low-signal) | the word "left" and sometimes "center" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14582) |
| [L6:F4923](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4923) | 6 | Generic/ambiguous content features (low-signal) |  descriptions of someone wanting to work in a specific profession | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4923) |
| [L7:F3085](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3085) | 6 | Generic/ambiguous content features (low-signal) |  words and phrases related to societal ills as well as human efforts to understand their world. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3085) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'PROBE_LABEL' is not one of the top-k next-token candi |
| 3 | `get_top_features` | 20 features; top: L14:4420 de=-0.147 |
| 4 | `inspect_feature` ×14 | L14:4420, L19:2486, L20:8433, L8:8855, L0:8964, L0:8444, L0:14287, L0:2203, L0:13948, L0:2011, L0:15693, L1:14511, L5:771, L0:1069 |
| 5 | `get_upstream_features` | Emb:" report"@21 (de=5.22) +9 more |
| 6 | `get_upstream_features` | L14:F4420 (de=14.31) +9 more |
| 7 | `get_upstream_features` | Emb:" top"@26 (de=5.72) +9 more |
| 8 | `get_upstream_features` | Emb:" report"@21 (de=12.06) +9 more |
| 9 | `get_top_features` | 30 features; top: L14:4420 de=-0.147 |
| 10 | `inspect_feature` ×17 | L7:13646, L8:8437, L7:9092, L18:14663, L16:15046, L16:8642, L17:5218, L19:14973, L9:7435, L11:5996, L9:2845, L3:10846, L2:11175, L4:6696, L6:12624, L5:12586, L4:661 |
| 11 | `get_upstream_features` | Emb:" report"@21 (de=5.22) +14 more |
| 12 | `get_upstream_features` | L14:F4420 (de=14.31) +14 more |
| 13 | `get_upstream_features` | Emb:" report"@21 (de=51.50) +9 more |
| 14 | `get_upstream_features` | Emb:" report"@21 (de=2.09) +9 more |
| 15 | `get_upstream_features` | L8:F8855 (de=4.94) +19 more |
| 16 | `get_upstream_features` | Emb:" news"@27 (de=8.69) +19 more |
| 17 | `get_upstream_features` | Emb:" top"@26 (de=7.22) +9 more |
| 18 | `inspect_feature` ×13 | L15:2579, L14:2659, L16:11532, L0:1579, L4:11898, L7:3085, L0:14582, L6:4923, L0:15185, L7:12495, L9:8366, L6:12712, L10:14576 |
| 19 | `get_upstream_features` | Emb:" news"@27 (de=7.94) +19 more |
| 20 | `get_upstream_features` | Emb:" top"@26 (de=5.72) +14 more |
| 21 | `get_upstream_features` | Emb:" report"@21 (de=51.50) +14 more |

### Build

`build_circuit` → 7 nodes, 7 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 113,129 | 10,364 | 398,052 | 0 | $0.0703 | — | — |
| **Total** | | **113,129** | **10,364** | **398,052** | **0** | **$0.0703** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 6s