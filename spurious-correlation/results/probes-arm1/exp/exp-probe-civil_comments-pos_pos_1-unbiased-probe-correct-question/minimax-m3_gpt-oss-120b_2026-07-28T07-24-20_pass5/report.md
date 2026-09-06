# Circuit Oracle Report
**Date:** 2026-07-28 07:24:20 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a circuit that mixes two superficially plausible signals with a much weaker, mostly lexical-instruction signal — the strongest direct contributions come from L0 features that fire on the adverb "clearly" and other generic discourse markers, on the identity-group word "white," and on the political-entity features that fire on the literal token "trump" and on the suffix of "bigot"; not on any deeper semantic composition.

**Confidence:** 6

**Reasoning:** Tracing the top direct-effect features feeding the output logit reveals four late/mid-layer supernodes plus a large pile of L0 "word features" whose upstream is almost always the embedding of a single input token:

1. **Output-driving late/mid features (the supposedly "semantic" half of the circuit):**
   - **late_politics** (L4:14582, L5:2146, L6:15063, L4:5265) — labels read "White House / US government," "references to American politics, elections, and politicians," etc. All of them fire at pos 5 = the token "trump." Upstream of L4:14582 the dominant signal is the "trump" embedding itself (direct_effect 18.1), plus L2:14301 ("names of people involved in politics, finance, national security") and L3:3136 ("names of people in the Trump administration"). This is essentially an entity-recognition feature for the name "Trump" — it does not encode the *content* of the statement about Trump, only that the name occurs. The mid_politics_names supernode (L2:14301, L3:3136) feeds it from the "trump" embedding.
   - **mid_racial_white** (L4:15204, autointerp "art galleries, museums and the White House," but its top activating examples all include the bare word "white" in racial contexts) — fires at pos 15 on the "white" token, with the "white" embedding as its single biggest upstream input (direct_effect 40.75). L0:3436 ("mentions of the word 'white'") is the only earlier feature feeding it. This is a "white" lexical feature whose identity-group sense is established by the L0 word-feature and then re-confirmed, not enriched, at L4.
   - **mid_swears_extremism** (L4:11580 "negative language and swear words," L4:7545 "religious extremism, violence, terrorism") — fires at pos 9, the suffix "ot" of "bigot." L2:9199 ("ot" in code) and L2:4520 feed it from the "ot" embedding. The negative-language label is misleading; in the actual top-activating examples these features are activated by sequences like "donkey butt arrogant," "F**k," etc. — i.e., by general invective patterns, not by the meaning of the surrounding sentence.

2. **L0 lexical/discourse supernodes (the user's concern, confirmed):**
   - **l0_clarity_cluster** at pos 2 (" clearly") — the *largest* direct-effect contributor in the entire graph. L0:7621 ("the word 'clearly'") has direct_effect 0.194, L0:12866 ("adverbs such as clearly, plainly") has direct_effect −0.206 (note the opposite sign — this feature is *suppressing* the probe score from the same token). Together with L0:4422 ("seriously"), L0:7861 ("this/these/clearly"), L0:5707 ("knowledge/perspective"), L0:4517 ("destroyed"), L0:7142 ("axis"), L0:11375 ("is"), and L1:9761 ("asserting that a statement is obvious"), the probe is being driven by a small cluster of features that *only* detect the word "clearly" and other generic discourse adverbs. They take almost all their signal directly from the " clearly" embedding (L0:7621's upstream is 17.75 from " clearly," 0.6 from bos, 0.1 from "tie" — i.e., the rest of the sentence contributes ~3%). These features do not encode that the content following "clearly" is toxic; they encode that the word "clearly" is present.
   - **l0_white_token** at pos 14–15 (" other", " white") — direct effects 0.10 each. L0:3436 ("mentions of the word 'white'") and L0:7969 ("the word 'other'") are the literal-token features; the "white" embedding contributes direct_effect 15.25 to L0:3436 and 40.75 to L4:15204, while the "other" embedding contributes 42.25 to L0:7969. L0:13663 ("mentions of pregnancy and related terms") sits at pos 15 with direct_effect −0.088 — it is essentially an unrelated off-target feature activated by accident at that position.
   - **l0_again_token** (L0:15831, "the word 'again' and words associated with time") at pos 26 — direct_effect −0.124 (suppressing). The "again" embedding contributes 43.5 to it. Once again a single-token lexical feature with strong direct effect.
   - **l0_shows_token** (L0:164 "show/your," L0:3916 "common short words in legal documents," L0:2411 "phone calls and complaints," L0:425 "pitch/sensitivity") at pos 1–3 — all fire on the "tie"/"shows" region and are general short-word features (frac_nonzero 0.011–0.037).
   - **l0_neg_ot_token** (L2:9199 "ot in code," L2:15769 and L4:2720 "the word 'tie'") at pos 1 and pos 9 — the "ot" embedding contributes direct_effect 23.88 to L2:9199, and the "tie" embedding contributes 21.13 to L2:15769. These features are subword/word detectors, not semantic ones.

The user's concern is **substantially validated by the circuit topology**. The "toxicity" probe is being driven by:
- A cluster of single-word L0 features on the adverb "clearly" (the *biggest* single contributor, with mixed positive/negative direct effects at the same token),
- The bare identity-group word "white" (both at L0 and again at L4),
- A "Trump-name" entity-recognition feature that only confirms the name is present, not that the statement is derogatory,
- A "negative language / swear words" feature that is actually triggered by the suffix "ot" of "bigot" and by code-like patterns,
- Several generic short-word features ("other," "is," "shows," "tie") with no toxicity-relevant semantics.

The genuine content of the message — the causal claim that Trump is a bigot, the political argument structure, the slur-by-association — is essentially **not represented** in the circuit. Instead, the probe latches onto (a) a generic assertion-of-obviousness discourse marker, (b) the presence of a specific identity-group word, and (c) the presence of a specific politician's name. This is exactly the "spurious identity-group signal" failure mode the user flagged: the model's probe does not appear to be reading the *content* of the toxic claim, it is reading lexical cues that happen to correlate with toxic framings in its training distribution, with mixed signs even on the same token (L0:12866 pushes the opposite direction from L0:7621 on the very same word "clearly"), which is also a sign of an unstable, surface-driven readout.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F14582](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14582) | 5 | Late-layer political-entity features (L4-L6): Trump administration / White House / US politics |  references to the White House and the US government | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14582) |
| [L4:F15063](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15063) | 5 | Late-layer political-entity features (L4-L6): Trump administration / White House / US politics | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15063) |
| [L4:F5265](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5265) | 5 | Late-layer political-entity features (L4-L6): Trump administration / White House / US politics | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5265) |
| [L4:F14100](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14100) | 5 | Late-layer political-entity features (L4-L6): Trump administration / White House / US politics | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14100) |
| [L5:F2146](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/2146) | 5 | Late-layer political-entity features (L4-L6): Trump administration / White House / US politics | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/2146) |
| [L6:F15063](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15063) | 5 | Late-layer political-entity features (L4-L6): Trump administration / White House / US politics |  references to American politics, elections, and politicians | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15063) |
| [L6:F1707](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1707) | 1 | Late-layer political-entity features (L4-L6): Trump administration / White House / US politics | a variety of discourse markers, qualifiers, intensifiers, or words expressing an opinion. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1707) |
| [L4:F15204](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) | 15 | Mid-layer 'white' entity / museum-context feature (L4:15204) firing on the racial term 'white' (pos 15) |  art galleries, museums and the White House | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) |
| [L3:F11768](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11768) | 15 | Mid-layer 'white' entity / museum-context feature (L4:15204) firing on the racial term 'white' (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11768) |
| [L2:F585](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) | 15 | Mid-layer 'white' entity / museum-context feature (L4:15204) firing on the racial term 'white' (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) |
| [L2:F6983](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6983) | 15 | Mid-layer 'white' entity / museum-context feature (L4:15204) firing on the racial term 'white' (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6983) |
| [L0:F10910](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) | 15 | Mid-layer 'white' entity / museum-context feature (L4:15204) firing on the racial term 'white' (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) |
| [L4:F11580](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11580) | 9 | Mid-layer negative-language / extremism features (L4:11580 'negative language / swear words' at pos 9; L4:7545 'religious extremism / violence' at pos 9) | negative language and swear words | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11580) |
| [L4:F7545](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7545) | 9 | Mid-layer negative-language / extremism features (L4:11580 'negative language / swear words' at pos 9; L4:7545 'religious extremism / violence' at pos 9) |  words or phrases relating to religious extremism, violence, and terrorism. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7545) |
| [L2:F4520](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4520) | 9 | Mid-layer negative-language / extremism features (L4:11580 'negative language / swear words' at pos 9; L4:7545 'religious extremism / violence' at pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4520) |
| [L2:F11039](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11039) | 9 | Mid-layer negative-language / extremism features (L4:11580 'negative language / swear words' at pos 9; L4:7545 'religious extremism / violence' at pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11039) |
| [L2:F4053](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4053) | 9 | Mid-layer negative-language / extremism features (L4:11580 'negative language / swear words' at pos 9; L4:7545 'religious extremism / violence' at pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4053) |
| [L2:F10198](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10198) | 9 | Mid-layer negative-language / extremism features (L4:11580 'negative language / swear words' at pos 9; L4:7545 'religious extremism / violence' at pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10198) |
| [L1:F13974](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13974) | 9 | Mid-layer negative-language / extremism features (L4:11580 'negative language / swear words' at pos 9; L4:7545 'religious extremism / violence' at pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13974) |
| [L0:F12712](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12712) | 9 | Mid-layer negative-language / extremism features (L4:11580 'negative language / swear words' at pos 9; L4:7545 'religious extremism / violence' at pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12712) |
| [L0:F5660](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5660) | 9 | Mid-layer negative-language / extremism features (L4:11580 'negative language / swear words' at pos 9; L4:7545 'religious extremism / violence' at pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5660) |
| [L2:F14301](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14301) | 5 | Mid-layer 'Trump administration' / 'politics/finance names' features (L2:14301, L3:3136) — entity-recognition of Trump |  names of people and organizations involved in politics, finance, and national security | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14301) |
| [L3:F3136](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3136) | 5 | Mid-layer 'Trump administration' / 'politics/finance names' features (L2:14301, L3:3136) — entity-recognition of Trump |  names of people involved in the Trump administration | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3136) |
| [L2:F13271](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13271) | 5 | Mid-layer 'Trump administration' / 'politics/finance names' features (L2:14301, L3:3136) — entity-recognition of Trump | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13271) |
| [L2:F4838](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4838) | 5 | Mid-layer 'Trump administration' / 'politics/finance names' features (L2:14301, L3:3136) — entity-recognition of Trump | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4838) |
| [L1:F7815](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7815) | 5 | Mid-layer 'Trump administration' / 'politics/finance names' features (L2:14301, L3:3136) — entity-recognition of Trump | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7815) |
| [L1:F10801](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10801) | 5 | Mid-layer 'Trump administration' / 'politics/finance names' features (L2:14301, L3:3136) — entity-recognition of Trump | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10801) |
| [L0:F1858](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1858) | 5 | Mid-layer 'Trump administration' / 'politics/finance names' features (L2:14301, L3:3136) — entity-recognition of Trump | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1858) |
| [L0:F7621](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7621) | 2 | L0 'clearly' / 'seriously' / discourse-marker cluster at pos 2 (' clearly') — strongest single direct-effect node (L0:7621, L0:12866, L0:4422, L0:7861, L0:5707, L0:11375, L0:7142, L0:4517) |  the word "clearly", and to a lesser extent words associated with amounts of things | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7621) |
| [L0:F12866](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12866) | 2 | L0 'clearly' / 'seriously' / discourse-marker cluster at pos 2 (' clearly') — strongest single direct-effect node (L0:7621, L0:12866, L0:4422, L0:7861, L0:5707, L0:11375, L0:7142, L0:4517) |  adverbs such as "clearly," "plainly," and "as" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12866) |
| [L0:F4422](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4422) | 2 | L0 'clearly' / 'seriously' / discourse-marker cluster at pos 2 (' clearly') — strongest single direct-effect node (L0:7621, L0:12866, L0:4422, L0:7861, L0:5707, L0:11375, L0:7142, L0:4517) | the word "seriously" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4422) |
| [L0:F7861](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7861) | 2 | L0 'clearly' / 'seriously' / discourse-marker cluster at pos 2 (' clearly') — strongest single direct-effect node (L0:7621, L0:12866, L0:4422, L0:7861, L0:5707, L0:11375, L0:7142, L0:4517) |  instances of the words "this", "these", "clearly", or "more". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7861) |
| [L0:F5707](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5707) | 2 | L0 'clearly' / 'seriously' / discourse-marker cluster at pos 2 (' clearly') — strongest single direct-effect node (L0:7621, L0:12866, L0:4422, L0:7861, L0:5707, L0:11375, L0:7142, L0:4517) |  words or phrases related to knowledge or perspective | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5707) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 6 | L0 'clearly' / 'seriously' / discourse-marker cluster at pos 2 (' clearly') — strongest single direct-effect node (L0:7621, L0:12866, L0:4422, L0:7861, L0:5707, L0:11375, L0:7142, L0:4517) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F7142](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7142) | 2 | L0 'clearly' / 'seriously' / discourse-marker cluster at pos 2 (' clearly') — strongest single direct-effect node (L0:7621, L0:12866, L0:4422, L0:7861, L0:5707, L0:11375, L0:7142, L0:4517) |  the word "axis" and its plural form, often in the context of scientific or technical documents | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7142) |
| [L0:F4517](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4517) | 2 | L0 'clearly' / 'seriously' / discourse-marker cluster at pos 2 (' clearly') — strongest single direct-effect node (L0:7621, L0:12866, L0:4422, L0:7861, L0:5707, L0:11375, L0:7142, L0:4517) |  the word "destroyed" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4517) |
| [L1:F9761](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9761) | 2 | L0 'clearly' / 'seriously' / discourse-marker cluster at pos 2 (' clearly') — strongest single direct-effect node (L0:7621, L0:12866, L0:4422, L0:7861, L0:5707, L0:11375, L0:7142, L0:4517) |  language asserting that a statement is obvious, undisputed, or in accordance with a rule | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9761) |
| [L1:F2407](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2407) | 2 | L0 'clearly' / 'seriously' / discourse-marker cluster at pos 2 (' clearly') — strongest single direct-effect node (L0:7621, L0:12866, L0:4422, L0:7861, L0:5707, L0:11375, L0:7142, L0:4517) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2407) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 15 | L0 'white' word-feature (L0:3436 at pos 15) + L0 'other' word-feature (L0:7969 at pos 14) — identity-group lexical triggers |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F7969](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7969) | 14 | L0 'white' word-feature (L0:3436 at pos 15) + L0 'other' word-feature (L0:7969 at pos 14) — identity-group lexical triggers |  the word "other" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7969) |
| [L0:F13663](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13663) | 15 | L0 'white' word-feature (L0:3436 at pos 15) + L0 'other' word-feature (L0:7969 at pos 14) — identity-group lexical triggers | mentions of pregnancy and related terms | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13663) |
| [L0:F15831](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15831) | 26 | L0 'again' word-feature (L0:15831 at pos 26) — negatively weighted identity-temporal marker | the word "again" and words associated with time | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15831) |
| [L0:F164](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/164) | 3 | L0 'shows' / 'show' / 'your' word-feature (L0:164 at pos 3) and L0 'legal short words' (L0:3916 at pos 1) — surface lexical features | the words "show" and "your", particularly when talking about presenting something | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/164) |
| [L0:F3916](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3916) | 1 | L0 'shows' / 'show' / 'your' word-feature (L0:164 at pos 3) and L0 'legal short words' (L0:3916 at pos 1) — surface lexical features |  common short words in legal documents | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3916) |
| [L0:F2411](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2411) | 3 | L0 'shows' / 'show' / 'your' word-feature (L0:164 at pos 3) and L0 'legal short words' (L0:3916 at pos 1) — surface lexical features |  words related to phone calls and making statements or complaints | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2411) |
| [L0:F425](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/425) | 3 | L0 'shows' / 'show' / 'your' word-feature (L0:164 at pos 3) and L0 'legal short words' (L0:3916 at pos 1) — surface lexical features |  instances of the word "pitch" and "sensitivity" in technical contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/425) |
| [L2:F9199](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9199) | 9 | L0/L2 'ot' subword feature (L2:9199 at pos 9) and L2 'tie' feature (L2:15769 at pos 1) and L4 'tie' (L4:2720 at pos 1) — surface tokens on the suffix of 'bigot' and the literal word 'tie' |  instances of "ot" in code | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9199) |
| [L2:F15769](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15769) | 1 | L0/L2 'ot' subword feature (L2:9199 at pos 9) and L2 'tie' feature (L2:15769 at pos 1) and L4 'tie' (L4:2720 at pos 1) — surface tokens on the suffix of 'bigot' and the literal word 'tie' | the word "tie" in various contexts | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15769) |
| [L4:F2720](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2720) | 1 | L0/L2 'ot' subword feature (L2:9199 at pos 9) and L2 'tie' feature (L2:15769 at pos 1) and L4 'tie' (L4:2720 at pos 1) — surface tokens on the suffix of 'bigot' and the literal word 'tie' | mentions of a 'tie' or a similar word | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2720) |
| [L3:F373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/373) | 1 | L0/L2 'ot' subword feature (L2:9199 at pos 9) and L2 'tie' feature (L2:15769 at pos 1) and L4 'tie' (L4:2720 at pos 1) — surface tokens on the suffix of 'bigot' and the literal word 'tie' |  word beginnings with the letters "a," "h,""i," "r," and "p" (perhaps prefixes and/or related to medical or scientific terms) | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/373) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:12866 de=-0.206 |
| 3 | `inspect_feature` ×20 | L0:12866, L0:7621, L4:14582, L0:4422, L0:11375, L0:15831, L0:7142, L0:164, L0:3916, L2:9199, L2:14301, L1:9761, L3:373, L0:3436, L0:7969, L0:7861, L0:5707, L2:15769, L4:11580, L4:2720 |
| 4 | `get_top_features` | 30 features; top: L0:12866 de=-0.206 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F14582@5` | ❌ error | — | — | Trace the "White House / US government" feature (L4:14582 at pos 5, direct_effec… |
| SA-2 | `L0:F3436@15` | ❌ error | — | — | Trace the "white" feature (L0:3436 at pos 15, direct_effect=0.10) upstream. The … |
| SA-3 | `L4:F11580@9` | ❌ error | — | — | Trace the "negative language and swear words" feature (L4:11580 at pos 9, direct… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F14582@5, k=15 → Emb:" trump"@5 (de=18.12) +14 more |
| 2 | `get_upstream_features` | L4:F11580@9, k=15 → Emb:"ot"@9 (de=5.00) +14 more |
| 3 | `get_upstream_features` | L4:F2720@1, k=15 → Emb:"tie"@1 (de=10.75) +14 more |
| 4 | `get_upstream_features` | L3:F373@1, k=15 → Emb:"<bos>"@0 (de=26.25) +14 more |
| 5 | `get_upstream_features` | L2:F14301@5, k=15 → Emb:" trump"@5 (de=9.44) +14 more |
| 6 | `get_upstream_features` | L2:F15769@1, k=15 → Emb:"tie"@1 (de=21.12) +14 more |
| 7 | `get_upstream_features` | L0:F7621@2, k=12 → Emb:" clearly"@2 (de=17.75) +11 more |
| 8 | `get_upstream_features` | L0:F12866@2, k=10 → Emb:" clearly"@2 (de=17.38) +9 more |
| 9 | `get_upstream_features` | L0:F11375@6, k=10 → Emb:" is"@6 (de=31.38) +9 more |
| 10 | `get_upstream_features` | L0:F15831@26, k=10 → Emb:" again"@26 (de=43.50) +9 more |
| 11 | `get_upstream_features` | L0:F7969@14, k=10 → Emb:" other"@14 (de=42.25) +9 more |
| 12 | `get_upstream_features` | L0:F4422@2, k=10 → Emb:" clearly"@2 (de=12.62) +9 more |
| 13 | `get_upstream_features` | L0:F3916@1, k=10 → Emb:"<bos>"@0 (de=8.94) +9 more |
| 14 | `get_upstream_features` | L0:F164@3, k=10 → Emb:" shows"@3 (de=19.38) +9 more |
| 15 | `get_upstream_features` | L0:F7142@2, k=10 → Emb:" clearly"@2 (de=14.62) +9 more |
| 16 | `get_upstream_features` | L0:F5707@2, k=10 → Emb:" clearly"@2 (de=20.88) +9 more |
| 17 | `get_upstream_features` | L0:F7861@2, k=10 → Emb:" clearly"@2 (de=14.25) +9 more |
| 18 | `get_upstream_features` | L2:F9199@9, k=10 → Emb:"ot"@9 (de=23.88) +9 more |
| 19 | `get_upstream_features` | L1:F9761@2, k=10 → Emb:" clearly"@2 (de=13.38) +9 more |
| 20 | `get_upstream_features` | L0:F13663@15, k=10 → Emb:" white"@15 (de=15.25) +9 more |
| 21 | `get_upstream_features` | L1:F2407@2, k=10 → Emb:" clearly"@2 (de=22.00) +9 more |
| 22 | `get_upstream_features` | L4:F14582@5, k=10 → Emb:" trump"@5 (de=18.12) +9 more |
| 23 | `get_upstream_features` | L4:F15204@15, k=10 → Emb:" white"@15 (de=40.75) +9 more |
| 24 | `get_upstream_features` | L4:F7545@9, k=10 → Emb:"ot"@9 (de=2.50) +9 more |
| 25 | `get_upstream_features` | L6:F15063@5, k=10 → Emb:" trump"@5 (de=12.75) +9 more |
| 26 | `get_upstream_features` | L0:F4517@2, k=10 → Emb:" clearly"@2 (de=15.38) +9 more |
| 27 | `get_upstream_features` | L0:F2411@3, k=10 → Emb:" shows"@3 (de=13.25) +9 more |
| 28 | `inspect_feature` ×9 | L4:15204, L6:15063, L4:7545, L0:13663, L0:4517, L0:2411, L0:425, L6:1707, L3:3136 |

### Build

`build_circuit` → 19 nodes, 18 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 77,274 | 13,003 | 357,979 | 0 | $0.0603 | — | — |
| **Total** | | **77,274** | **13,003** | **357,979** | **0** | **$0.0603** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 34s