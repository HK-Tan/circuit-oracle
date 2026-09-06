# Circuit Oracle Report
**Date:** 2026-07-28 07:20:04 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_7 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

The circuit is now saved. Let me write the final analysis.

**Analysis:** The probe's "contradiction" classification score is driven almost entirely by **syntactic/structural features** (notably L17:F451 "start of sentence" + L4:F4605 "churches/abbeys" + L0:L1 "first" / "That" / "you" detectors) and by **lexical-position features** anchored to the first sentence — with the actual semantic content (the "abbey lacks a steeple" / "is not of great height" negation) contributing only weak, indirect signals via generic suffix/structure features (L2:F5878 "le" suffix from "steepled" / "lacks"). The user's concern is **partially correct but overstated**: the circuit does exploit a "spurious" start-of-sentence / first-ordinal bias inherited from the model's pretraining, but the most negative contributions to the probe come from generic lexical features (L4:F4605 church/abbey, L4:F5749 settlements, L2:F5878 "le" suffix on "steepled"/"lacks"), not from "negation words" as such.

**Confidence:** 5/10 — the circuit is genuinely complex and the autointerp labels for many features (church, settlements, abbey, steepled) clearly DO semantically engage with the prompt content, so the picture is mixed. The "negation words" hypothesis in the user concern is not well supported — there is no feature here whose top-activating examples center on "not", "no", "lacks", or other negators; the negation cue "lacks" (pos 29) is almost invisible in the upstream features (no L0 feature for "lacks" appears in the top-50).

**Reasoning:**

**What the circuit looks like and where the signal flows:**

1. **Output driver (the late-layer feature closest to the probe):** The strongest single feature is L8:F8406 (direct_effect = -0.164, i.e. it PUSHES AGAINST the probe target). Its autointerp is "the first-person pronoun 'I' and the word 'Exactly'" — completely unrelated to the prompt. Tracing its upstream chain: L7:F462 (code-doc/import blocks, +4.75), L7:F5741 (copyright headers, +4.47), L5:F3992 ("/**" doc-block opener, +3.22 from upstream), L6:F14585 ("the"/"it" at start of sentence, +1.86), all converging on the first token position ("That", pos 1) and receiving strong excitation from the `<bos>` embedding. The first sentence opening with "That first glimpse…" supplies a structural "start-of-sentence" signal that the model routes through code/import detectors — a textbook spurious feature.

2. **The "first" cluster (genuine lexical content, modest contribution):** A long chain of layers (L0:F7056, L0:F3820, L0:F2848 → L1:F5053, L1:F9854 → L2:F8518, L2:F5878 → L3:F11165, L3:F3205 → L4:F2581, L4:F488, L4:F10564 → L6:F5342 → L17:F451) all activate on the word "first" at pos 2. Many of these are dedicated "first" detectors (frac_nonzero ~0.007-0.016, highly specific). The L4 features like F2581 ("mentions of things being 'first'") and F488 ("player's first appearance/debut") ARE contextually relevant — sentence 1 contains "That **first** glimpse", a temporal/anecdotal framing that primes the reader for the eventual contrast in sentence 2 ("**is not of great height**"). So part of the circuit is genuinely encoding the temporal setup that supports a contradiction reading.

3. **The "abbey/steepled" entity content (drives L4:F4605 negatively):** L4:F4605 ("words related to churches, chapels and other buildings") activates on "led" of "steepled" at pos 9 and on "abbey" at pos 10 (direct_effect = -0.116 and -0.103). L4:F5749 ("ancient settlements/fortifications") also activates on "steepled" and "towering" (direct_effect = -0.115, -1.16). L2:F5878 ("le" suffix) on "led"/"steepled". These features ARE semantically engaged with the prompt's subject matter (an abbey/church building). They contribute negatively to the probe, which is interesting — it suggests the probe has learned that "church/chapel" subject matter pushes AGAINST a contradiction classification, perhaps because the training set contains many entailed/neutral pairs about church buildings.

4. **The "That"/"That first glimpse" opening:** L2:F8046 (clauses starting with 't'), L3:F1806 ("That's"-style), L1:F10498 ("That"), L3:F10959 ("at"-containing words), and L9:F8770 ("It"/"In"/"There" sentence-starters) all activate on the first token "That". L4:F3833 (fired at pos 3, "glimpse", direct_effect = +0.142 — strongly positive) and L4:F3395 ("idiomatic/figures of speech", fired on "glimpse") contribute positively. The L0:F7710 "you" detector fires on "you" at pos 21 with direct_effect = -0.112, contributing AGAINST the contradiction reading (the personal address makes the text feel like an entailed/entailed advertisement).

5. **The downstream L17 chain that connects to the output:** L8:F8406 (start-of-sentence-ish) → L9:F8770 ("It/In/There") → L10:F14174 ("{") → L11:F11186 (sci/tech terms) → L13:F8128 (inhibitor) → L14:F2510 ("using") → L15:F751 (code-snippet/import) → L16:F10989 ("the" — strong NEGATIVE -12.3) → L17:F451 (start of sentences, +0.118). The L17:F451 is in the get_top_features list with direct_effect = +0.118. This confirms the circuit terminates in a "start-of-sentence" feature that is heavily modulated by code/structure detectors inherited from the pretraining distribution. The autointerp "start of sentences" (frac_nonzero = 0.0067) is a generic but specific feature; its contribution to the probe is the largest single late-layer signal in the graph.

**Assessment of the user concern:**

The user is RIGHT that the circuit uses spurious features, but the specific claim "negation words" is not supported. The dominant late-layer driver (L17:F451 "start of sentences") and its upstream chain (L8:F8406 "I/Exactly" + L7:F462 "code-doc/imports" + L6:F14585 "the/it sentence-initial") are spurious in the sense that they are *structural / lexical-position features* that are not about the proposition. The L4 church-abbey features (F4605) and the "steepled"/"le" suffix detector (L2:F5878) DO engage with the prompt's semantic content, but they push the probe AWAY from the contradiction label, not toward it. The "first" chain is a mixture — it reflects the genuine first/then temporal setup in the prompt.

The "is not" / "lacks" negation in sentence 2 does NOT show up clearly in the attribution graph at this top-50 cutoff — there's no dedicated "not" or "lacks" feature, and the pos 29 "lacks" token is only weakly represented. So the "negation words" framing in the user concern does not match what is actually in the circuit. Rather, the spurious signal is the **opening-sentence / code-block structure of "That first glimpse…"** combined with **first-ordinal position encoding**, which is a far weaker but still real artifact of the model's pretraining on web text.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 4 | L0 lexical: 'of', 'the', 'first', 'abbey', technical/code | the word "of" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 30 | L0 lexical: 'of', 'the', 'first', 'abbey', technical/code | the word "of" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 5 | L0 lexical: 'of', 'the', 'first', 'abbey', technical/code | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F7056](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7056) | 2 | L0 lexical: 'of', 'the', 'first', 'abbey', technical/code |  mentions of something happening for the first time | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7056) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 10 | L0 lexical: 'of', 'the', 'first', 'abbey', technical/code | technical documents or data, including numbers, units, and references to figures or tables. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F11835](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11835) | 10 | L0 lexical: 'of', 'the', 'first', 'abbey', technical/code | terms used in software code such as "assembly", "using", "namespace", and "license" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11835) |
| [L0:F9854](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9854) | 2 | L0 lexical: 'of', 'the', 'first', 'abbey', technical/code |  words indicating possibility or future tense verbs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9854) |
| [L0:F2159](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2159) | 9 | L0 lexical: 'of', 'the', 'first', 'abbey', technical/code |  words that end with "led" or are related to worth | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2159) |
| [L0:F7710](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) | 21 | L0 lexical: 'of', 'the', 'first', 'abbey', technical/code | the pronoun "you" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) |
| [L0:F13874](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13874) | 9 | L0 lexical: 'of', 'the', 'first', 'abbey', technical/code | the word "guard" and associated words like "entered," "protecting," and "borrow." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13874) |
| [L0:F8051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8051) | 9 | L0 lexical: 'of', 'the', 'first', 'abbey', technical/code |  the word "informed." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8051) |
| [L0:F9320](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9320) | 10 | L0 lexical: 'of', 'the', 'first', 'abbey', technical/code |  a wide range of technical and legal terms | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9320) |
| [L0:F11846](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11846) | 10 | L0 lexical: 'of', 'the', 'first', 'abbey', technical/code |  legal jargon related to court cases, particularly citing names of cases | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11846) |
| [L1:F5053](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5053) | 2 | L1 'first' / 'That' / code-test |  the word "first" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5053) |
| [L1:F10498](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10498) | 1 | L1 'first' / 'That' / code-test |  the word "That" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10498) |
| [L1:F10935](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10935) | 9 | L1 'first' / 'That' / code-test |  words related to Java programming and/or software testing | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10935) |
| [L1:F4103](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4103) | 9 | L1 'first' / 'That' / code-test | the word "mixed" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4103) |
| [L1:F5997](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5997) | 9 | L1 'first' / 'That' / code-test |  words referring to combining or grouping things | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5997) |
| [L2:F8518](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8518) | 2 | L2 'first' / suffix / entities | the word "first" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8518) |
| [L2:F5878](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5878) | 9 | L2 'first' / suffix / entities | the suffix "le" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5878) |
| [L2:F8185](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8185) | 10 | L2 'first' / suffix / entities | places for shopping or military activities | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8185) |
| [L2:F12263](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12263) | 10 | L2 'first' / suffix / entities |  words related to agriculture/mining and to slavery/plantations | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12263) |
| [L2:F16060](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16060) | 9 | L2 'first' / suffix / entities | words with the letters "en" at the end | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16060) |
| [L2:F14398](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14398) | 9 | L2 'first' / suffix / entities |  outdoor natural features | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14398) |
| [L2:F1924](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1924) | 9 | L2 'first' / suffix / entities | words ending in "ize" or "ise" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1924) |
| [L2:F8046](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8046) | 1 | L2 'first' / suffix / entities |  common words and phrases that include the letter 't' and are commonly used to start clauses | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8046) |
| [L3:F11165](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11165) | 2 | L3 'first'/'second' ordinal + code |  the words "first" and "second," particularly when used as ordinal indicators | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11165) |
| [L3:F3205](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3205) | 2 | L3 'first'/'second' ordinal + code |  code snippets and documentation references, possibly related to web development | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3205) |
| [L3:F4081](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4081) | 9 | L3 'first'/'second' ordinal + code | mentions of the statistical software Stata and the term "stent". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4081) |
| [L3:F7650](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7650) | 9 | L3 'first'/'second' ordinal + code | abbreviations, geographical locations, and the letter "l" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7650) |
| [L3:F689](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/689) | 9 | L3 'first'/'second' ordinal + code | the sequence "l[ae] [mn]" or "leg" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/689) |
| [L3:F373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/373) | 1 | L3 'first'/'second' ordinal + code |  word beginnings with the letters "a," "h,""i," "r," and "p" (perhaps prefixes and/or related to medical or scientific terms) | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/373) |
| [L3:F1806](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1806) | 1 | L3 'first'/'second' ordinal + code |  occurrences of "that's" or similar phrases indicating emphasis or a conversational tone, with a tendency to also pick up on related words like "calculate", "course" and "layers" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1806) |
| [L3:F6362](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6362) | 2 | L3 'first'/'second' ordinal + code | words related to research papers that refer to something previously mentioned | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6362) |
| [L3:F10959](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10959) | 1 | L3 'first'/'second' ordinal + code | words with "at" in them as well as some words with "os" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10959) |
| [L4:F3833](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) | 3 | L4 'first'/'steepled'/'steepled-abbey' clusters |  words used when summarizing plot points or providing courtroom insights | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) |
| [L4:F3833](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) | 4 | L4 'first'/'steepled'/'steepled-abbey' clusters |  words used when summarizing plot points or providing courtroom insights | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) |
| [L4:F2581](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2581) | 2 | L4 'first'/'steepled'/'steepled-abbey' clusters |  mentions of things being "first" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2581) |
| [L4:F4605](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) | 9 | L4 'first'/'steepled'/'steepled-abbey' clusters |  words related to churches, chapels and other buildings, in addition to other information of Lincolnshire | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) |
| [L4:F4605](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) | 10 | L4 'first'/'steepled'/'steepled-abbey' clusters |  words related to churches, chapels and other buildings, in addition to other information of Lincolnshire | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) |
| [L4:F5749](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) | 9 | L4 'first'/'steepled'/'steepled-abbey' clusters |  terms that describe ancient settlements and fortifications | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) |
| [L4:F13244](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) | 10 | L4 'first'/'steepled'/'steepled-abbey' clusters |  terms related to land ownership and administration, possibly including slavery or other forms of forced labor | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) |
| [L4:F9757](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) | 1 | L4 'first'/'steepled'/'steepled-abbey' clusters | various acronyms, IDs, and symbols, possibly related to scientific data | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) |
| [L4:F2053](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2053) | 4 | L4 'first'/'steepled'/'steepled-abbey' clusters |  references to components of equations or theorems | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2053) |
| [L4:F3395](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3395) | 4 | L4 'first'/'steepled'/'steepled-abbey' clusters | idiomatic expressions or figures of speech | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3395) |
| [L4:F488](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/488) | 2 | L4 'first'/'steepled'/'steepled-abbey' clusters |  information about a player's first appearance or performance in sports | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/488) |
| [L4:F10564](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10564) | 4 | L4 'first'/'steepled'/'steepled-abbey' clusters |  ordinal numbers or the word "first" coupled with a noun or preposition | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10564) |
| [L4:F553](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/553) | 2 | L4 'first'/'steepled'/'steepled-abbey' clusters | phrases expressing subtle distinctions or sentimental connections | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/553) |
| [L4:F12137](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12137) | 2 | L4 'first'/'steepled'/'steepled-abbey' clusters |  the word "one" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12137) |
| [L4:F12828](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12828) | 2 | L4 'first'/'steepled'/'steepled-abbey' clusters | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12828) |
| [L4:F4094](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4094) | 2 | L4 'first'/'steepled'/'steepled-abbey' clusters | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4094) |
| [L4:F14618](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14618) | 2 | L4 'first'/'steepled'/'steepled-abbey' clusters | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14618) |
| [L5:F4305](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/4305) | 4 | L5 sequence-of-events/inauguration | words and phrases related to a sequence of events, prior knowledge, and historical progress. | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/4305) |
| [L5:F7444](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7444) | 2 | L5 sequence-of-events/inauguration |  words or phrases that an individual would express or think | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7444) |
| [L6:F5342](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5342) | 4 | L6 sentence-initial 'first'/'that' | the word "first" as well as words and prepositions that often follow it | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5342) |
| [L6:F14585](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14585) | 1 | L6 sentence-initial 'first'/'that' |  the words "the" and "it" at the beginning of sentences | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14585) |
| [L6:F4516](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4516) | 1 | L6 sentence-initial 'first'/'that' | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4516) |
| [L6:F14531](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14531) | 1 | L6 sentence-initial 'first'/'that' | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14531) |
| [L7:F462](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) | 1 | L7 doc-block / code / sentence-initial |  code documentation and import statements | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) |
| [L7:F5741](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5741) | 1 | L7 doc-block / code / sentence-initial |  code documentation or copyright information | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5741) |
| [L7:F1673](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1673) | 1 | L7 doc-block / code / sentence-initial | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1673) |
| [L7:F3099](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3099) | 1 | L7 doc-block / code / sentence-initial | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3099) |
| [L7:F14857](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14857) | 1 | L7 doc-block / code / sentence-initial | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14857) |
| [L8:F8406](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) | 1 | L8 'I'/'Exactly' lexical | the first-person pronoun "I" and the word "Exactly" | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) |
| [L9:F8770](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8770) | 1 | L9 'It'/'In' sentence-initial + code | sentences beginning with "It" or "In" and also the word "There". | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8770) |
| [L9:F2762](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2762) | 1 | L9 'It'/'In' sentence-initial + code |  various code snippets, especially javascript | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2762) |
| [L9:F15819](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15819) | 1 | L9 'It'/'In' sentence-initial + code | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15819) |
| [L10:F14174](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14174) | 1 | L10 '{' left-bracket | left curly brackets | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14174) |
| [L11:F11186](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/11186) | 1 | L11 scientific terms | scientific and technical terms | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/11186) |
| [L11:F10933](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/10933) | 1 | L11 scientific terms | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/10933) |
| [L13:F8128](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/8128) | 1 | L13 suppressors | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/8128) |
| [L13:F14274](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/14274) | 1 | L13 suppressors | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/14274) |
| [L14:F2510](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/2510) | 1 | L14 'using' | the word "using" | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/2510) |
| [L14:F15964](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/15964) | 1 | L14 'using' | newline characters. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/15964) |
| [L15:F751](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/751) | 1 | L15 code-snippet/import | code snippets | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/751) |
| [L15:F851](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/851) | 1 | L15 code-snippet/import | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/851) |
| [L15:F10005](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10005) | 1 | L15 code-snippet/import | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10005) |
| [L16:F10989](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/10989) | 1 | L16 'the' - strong negative | the | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/10989) |
| [L17:F451](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) | 1 | L17 'start of sentence' - the main output driver | start of sentences | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L8:8406 de=-0.164 |
| 3 | `inspect_feature` ×17 | L8:8406, L0:2848, L0:3820, L4:3833, L0:9026, L6:5342, L17:451, L4:4605, L4:5749, L0:7710, L4:13244, L4:2581, L0:11835, L2:8046, L5:7444, L0:9854, L4:9757 |
| 4 | `get_upstream_features` | Emb:"<bos>"@0 (de=10.69) +14 more |
| 5 | `get_upstream_features` | L16:F10989 (de=-12.31) +14 more |
| 6 | `get_upstream_features` | Emb:" of"@4 (de=35.25) +14 more |
| 7 | `inspect_feature` ×11 | L16:10989, L14:2510, L15:751, L10:14174, L9:8770, L6:14585, L11:11186, L9:2762, L7:462, L5:3992, L7:5741 |
| 8 | `get_upstream_features` | Emb:" glimpse"@3 (de=7.03) +14 more |
| 9 | `get_upstream_features` | Emb:" abbey"@10 (de=37.50) +14 more |
| 10 | `get_upstream_features` | Emb:" first"@2 (de=12.06) +14 more |
| 11 | `get_upstream_features` | Emb:"led"@9 (de=6.44) +14 more |
| 12 | `get_upstream_features` | Emb:" first"@2 (de=26.25) +14 more |
| 13 | `inspect_feature` ×14 | L3:4081, L3:7650, L2:5878, L0:2159, L4:2053, L5:4305, L4:10564, L4:3395, L4:488, L0:7056, L3:11165, L2:8518, L1:5053, L3:3205 |
| 14 | `get_upstream_features` | Emb:" abbey"@10 (de=9.06) +14 more |
| 15 | `get_upstream_features` | Emb:" abbey"@10 (de=7.19) +14 more |
| 16 | `get_upstream_features` | Emb:"That"@1 (de=10.56) +14 more |
| 17 | `get_upstream_features` | Emb:"That"@1 (de=12.19) +14 more |
| 18 | `get_upstream_features` | Emb:"<bos>"@0 (de=15.31) +14 more |
| 19 | `get_upstream_features` | L2:F5878 (de=2.50) +14 more |
| 20 | `get_upstream_features` | Emb:" you"@21 (de=42.25) +14 more |
| 21 | `get_upstream_features` | Emb:"That"@1 (de=7.34) +14 more |
| 22 | `inspect_feature` ×8 | L3:689, L1:5997, L3:373, L3:1806, L4:12137, L3:10959, L4:553, L3:6362 |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L17:F451@1` | ✅ reported | 9 | 9 | Trace upstream from L17:F451 (start of sentences) at pos 1. Determine what contr… |
| SA-2 | `L8:F8406@1` | ✅ reported | 6 | 8 | Trace upstream from L8:F8406 at pos 1. Find what gives rise to this "I"/"Exactly… |

<details>
<summary><b>SA-1</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L17, F451 | "start of sentences" |
| 2 | `get_upstream_features` | L17:F451@1, k=10 | L16:F10989 (de=-12.31) +9 more |
| 3 | `inspect_feature` | L15, F751 | "code snippets" |
| 4 | `inspect_feature` | L10, F14174 | "left curly brackets" |
| 5 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 6 | `get_upstream_features` | L15:F751@1, k=10 | L14:F15964 (de=19.00) +9 more |
| 7 | `inspect_feature` | L6, F14585 | " the words "the" and "it" at the beginning of sentences" |
| 8 | `inspect_feature` | L9, F8770 | "sentences beginning with "It" or "In" and also the word "There"." |
| 9 | `inspect_feature` | L14, F15964 | " newline characters." |
| 10 | `get_upstream_features` | L6:F14585@1, k=10 | Emb:"That"@1 (de=7.34) +9 more |
| 11 | `inspect_feature` | L7, F462 | " code documentation and import statements" |
| 12 | `get_upstream_features` | L7:F462@1, k=10 | Emb:"<bos>"@0 (de=20.88) +9 more |
| 13 | `get_upstream_features` | L14:F15964@1, k=10 | L9:F8770 (de=8.50) +9 more |

**Findings:** Tracing from L17:F451 (the generic start‑of‑sentence detector) reveals a cascade of upstream contributors. The strongest driver is L14:F15964, a newline detector, which itself receives strong excitation from L9:F8770 (sentences beginning with "It", "In", "There") and from L7:F462 (code documentation/import blocks). L7:F462 is directly driven by the beginning‑of‑sequence token <bos>. Parallel paths…

</details>

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L8, F8406 | "the first-person pronoun "I" and the word "Exactly"" |
| 2 | `get_upstream_features` | L8:F8406@1, k=10 | Emb:"<bos>"@0 (de=10.69) +9 more |
| 3 | `inspect_feature` | L7, F462 | " code documentation and import statements" |
| 4 | `inspect_feature` | L7, F5741 | " code documentation or copyright information" |
| 5 | `get_upstream_features` | L7:F462@1, k=10 | Emb:"<bos>"@0 (de=20.88) +9 more |
| 6 | `inspect_feature` | L5, F3992 | "the start of documentation blocks in code" |
| 7 | `inspect_feature` | L5, F7489 | " the last three letters of words." |
| 8 | `get_upstream_features` | L5:F3992@1, k=10 | Emb:"<bos>"@0 (de=21.25) +9 more |
| 9 | `get_upstream_features` | L7:F462@1, k=10 | Emb:"<bos>"@0 (de=20.88) +9 more |
| 10 | `inspect_feature` | L7, F5741 | " code documentation or copyright information" |
| 11 | `inspect_feature` | L6, F14585 | " the words "the" and "it" at the beginning of sentences" |
| 12 | `get_upstream_features` | L7:F5741@1, k=10 | Emb:"<bos>"@0 (de=12.06) +9 more |

**Findings:** The L8:F8406 feature that lights up on the token "I" or "Exactly" is driven primarily by three upstream pathways: (1) a code‑documentation detector (L7:462), (2) a similar comment/copyright detector (L7:5741), and (3) lower‑layer lexical patterns such as doc‑block starts (L5:3992), suffix cues (L5:7489) and sentence‑starter words (L6:14585). All of these upstream features receive strong positive d…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F2848@30, k=15 → Emb:" of"@30 (de=37.25) +14 more |
| 2 | `get_upstream_features` | L0:F3820@5, k=15 → Emb:" the"@5 (de=34.25) +14 more |
| 3 | `get_upstream_features` | L4:F4605@10, k=15 → Emb:" abbey"@10 (de=7.97) +14 more |
| 4 | `inspect_feature` ×12 | L0:9320, L0:11846, L2:8185, L2:12263, L1:10935, L2:1924, L1:10498, L2:16060, L2:14398, L1:4103, L0:13874, L0:8051 |

### Build

`build_circuit` → 29 nodes, 28 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 148,072 | 16,656 | 954,072 | 0 | $0.1217 | — | — |
| SA-1 | openai/gpt-oss-120b | 212,809 | 8,212 | 5,376 | 0 | $0.0369 | ✅ 9F/9E | Trace upstream from L17:F451 (start of sentences) at pos 1. … |
| SA-2 | openai/gpt-oss-120b | 162,698 | 10,187 | 25,824 | 0 | $0.0309 | ✅ 6F/8E | Trace upstream from L8:F8406 at pos 1. Find what gives rise … |
| **Total** | | **523,579** | **35,055** | **985,272** | **0** | **$0.1895** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 43s