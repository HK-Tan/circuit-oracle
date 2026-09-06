# Circuit Oracle Report
**Date:** 2026-07-28 07:21:34 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_10 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity classification is driven primarily by a "discrimination language" circuit (L6:F9228, L5:F12135, L5:F1431, L4:F117, L4:F5584) that activates off the single word "race" at position 5 — even though the prompt uses it neutrally to describe cops using force on Black people — combined with lexical detectors for "mention" (position 3) and "question" (position 10), and not by any features that encode the actual semantic content of the sentence.

**Confidence:** 6

**Reasoning:** The dominant path is the L4→L5→L6 chain rooted in the token "race" at pos 5. The L0 race-token detector (L0:F10682, direct_effect=22.6 on F15173's upstream) and L2:F10509 fire almost entirely off the Emb:" race" embedding (direct_effect=30.1), then feed the L4 supernode (F5584 "race/ethnicity/nationality groups", F117 "race/racism/social-justice, focused on Black people", F15899 "LGBTQ/gender/identity language") at the same position. The L4 features then excite L5:F12135 ("terms related to discrimination based on identity", frac_nonzero=0.017) and L5:F1431 ("phrases from equal-opportunity employment law", frac_nonzero=0.011), which converge on L6:F9228 ("language regarding discrimination based on race, gender, religion, and disability", frac_nonzero=0.597, direct_effect=-0.093 to logit). F9228 is generic — its top activating examples are EEOC/Fair Housing Act boilerplate ("regardless of race or gender", "discriminate based on race, color, national origin, religion"), not toxic speech — and it has a very high frac_nonzero (0.60), so it fires on any civil-rights vocabulary regardless of whether the surrounding text is hateful, neutral, or anti-racist.

The other top contributors to the probe logit are L3:F672 ("the word question", direct_effect=0.105) at position 10, and L4:F15173 ("statements about mentioning or discussing something", direct_effect=0.135) at position 3. Tracing F672 shows the L3 "question" feature is driven almost entirely by the Emb:" question" embedding (direct_effect=38.75) and the question-word family, not by any comprehension of the surrounding clause "in question using undue force". F15173 is similarly anchored to the Emb:" mentioning" embedding (direct_effect=17.5).

Critically, the circuit contains no features for "Black", "cops", "force", "helpless", or the predicate "bad cops are white". The only identity-related feature that names a specific group is L4:F117 ("focus on terms related to Black people"), but it is a generic civil-rights vocabulary detector (its top activations are "color", "racists", "color" in EEOC discussions) and fires on the word "race" alone, not on the word "Black".

This is the user's concern confirmed: the probe reads the prompt as toxic almost entirely because it contains the word "race" plus the framing verbs "mentioning" and "in question", which trigger the model's "discrimination-language" detector. The circuit is largely **identity-lexicon driven, not semantics-driven** — the actual content of the sentence (that not mentioning race implies bad cops are white) is not represented anywhere in the attributed path. However, the most direct pushers toward the probe (F15173 "mentioning" +0.135, F672 "question" +0.105, F5475 "race" +0.105) are generic function-word detectors with frac_nonzero in the 0.003-0.043 range, so they are selective but not entity-specific; the probe is reading a familiar civil-rights template, not racial slurs. Whether this is "spurious" depends on definition: the features are real lexical patterns, but the model is pattern-matching on template words rather than judging whether the proposition is hateful.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L6:F9228](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9228) | 6 | Discrimination language (race/gender/religion/disability) |  language regarding discrimination based on race, gender, religion, and disability | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9228) |
| [L5:F12135](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12135) | 6 | Discrimination by identity |  terms related to discrimination based on identity | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12135) |
| [L5:F1431](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1431) | 6 | Equal employment / civil-rights legal language |  phrases or words from employment law, especially equal opportunity employment law | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1431) |
| [L4:F5584](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5584) | 6 | Race/ethnicity/nationality terms |  words related to race, ethnicity, nationality or population groups | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5584) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 6 | Race/ethnicity/nationality terms |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F15899](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) | 6 | Race/ethnicity/nationality terms |  language associated with the LGBTQ community and discussions of gender and identity. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) |
| [L4:F15173](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15173) | 3 | Statements about mentioning/discussing |  statements about mentioning or discussing something | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15173) |
| [L3:F6517](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6517) | 3 | Statements about mentioning/discussing |  words related to mentioning something | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6517) |
| [L3:F11194](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11194) | 3 | Statements about mentioning/discussing |  words related to stating or communicating information | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11194) |
| [L2:F11639](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11639) | 3 | Statements about mentioning/discussing | the word "mention" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11639) |
| [L2:F6539](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6539) | 3 | Statements about mentioning/discussing | the word "mention" and words or phrases related to opinions or significance, as well as the word "matter." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6539) |
| [L3:F672](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/672) | 10 | Word "question" / legal context |  the word "question" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/672) |
| [L2:F12770](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12770) | 10 | Word "question" / legal context | the word "question" and related words | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12770) |
| [L0:F4368](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4368) | 10 | Word "question" / legal context |  mentions of questions, references, generalities, or doubts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4368) |
| [L0:F819](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/819) | 10 | Word "question" / legal context |  the word "question" specifically in the context of legal documents or investigations | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/819) |
| [L0:F10682](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10682) | 5 | Word "race" detectors |  the word "race" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10682) |
| [L2:F10509](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10509) | 5 | Word "race" detectors |  the word "race." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10509) |
| [L0:F14813](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14813) | 5 | Word "race" detectors |  mentions of race, racial issues, or racism | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14813) |
| [L3:F5475](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5475) | 5 | Word "race" detectors |  occurrences of the word "race" in different contexts | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5475) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 2 | Function-word detectors (not, By, The, of) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F15267](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15267) | 2 | Function-word detectors (not, By, The, of) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15267) |
| [L2:F2713](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2713) | 2 | Function-word detectors (not, By, The, of) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2713) |
| [L3:F12410](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12410) | 1 | Function-word detectors (not, By, The, of) | the word "By" at the start of a phrase or sentence | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12410) |
| [L0:F1903](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1903) | 1 | Function-word detectors (not, By, The, of) | instances of sentences starting with "The" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1903) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 4 | Function-word detectors (not, By, The, of) | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 6 | Function-word detectors (not, By, The, of) | the word "of" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F2317](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2317) | 3 | Function-word detectors (not, By, The, of) |  words or phrases expressing uncertainty or doubt | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2317) |
| [L0:F2455](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2455) | 1 | Function-word detectors (not, By, The, of) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2455) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:4958 de=-0.227 |
| 3 | `inspect_feature` ×20 | L0:4958, L2:10509, L0:10682, L4:15173, L3:12410, L2:11639, L0:1903, L0:14813, L3:672, L3:5475, L4:573, L2:6539, L4:2668, L0:2317, L0:819, L6:9228, L0:15267, L3:11194, L0:3820, L2:2713 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F9228@6` | ❌ error | — | — | Trace the path from L6:F9228 (discrimination language feature - fires on "race, … |
| SA-2 | `L0:F10682@5` | ❌ error | — | — | Trace the path from L0:F10682 (the word "race" feature at pos 5). What tokens an… |
| SA-3 | `L2:F10509@5` | ✅ reported | 5 | 4 | Trace the path from L2:F10509 (the word "race" feature at pos 5). What tokens an… |
| SA-4 | `L3:F672@10` | ❌ error | — | — | Trace the path from L3:F672 (the word "question" feature at pos 10). What does t… |
| SA-5 | `L4:F15173@3` | ❌ error | — | — | Trace the path from L4:F15173 (statements about mentioning/discussing something,… |

<details>
<summary><b>SA-3</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F10509 | " the word "race."" |
| 2 | `get_upstream_features` | L2:F10509@5, k=10 | Emb:" race"@5 (de=30.12) +9 more |
| 3 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 4 | `get_upstream_features` | L0:F9026@5, k=10 | Emb:" race"@5 (de=5.88) +9 more |
| 5 | `inspect_feature` | L0, F8747 | " the word "pair"" |

**Findings:** The L2 race feature (L2:F10509) is driven primarily by the direct embedding of the token " race" (positive direct effect 30.1). A small contribution also comes from the BOS embedding. Two low‑layer (layer 0) features provide minor additional excitation: a generic technical‑document detector (F9026) and a "pair" detector (F8747). Both are in the lower third of the model (≤8) and have positive direc…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F9228@6, k=10 → L5:F12135 (de=2.75) +9 more |
| 2 | `get_upstream_features` | L0:F10682@5, k=10 → Emb:" race"@5 (de=22.62) +9 more |
| 3 | `get_upstream_features` | L3:F672@10, k=10 → Emb:" question"@10 (de=38.75) +9 more |
| 4 | `get_upstream_features` | L4:F15173@3, k=10 → Emb:" mentioning"@3 (de=17.50) +9 more |
| 5 | `inspect_feature` ×10 | L5:12135, L5:1431, L4:5584, L4:117, L4:14857, L3:6517, L2:12770, L2:12030, L2:636, L0:4368 |
| 6 | `get_upstream_features` | L5:F12135@6, k=10 → Emb:" race"@5 (de=4.84) +9 more |
| 7 | `get_upstream_features` | L4:F4@4, k=5 → ❌ Feature (layer=4, pos=4, feature_idx=4) not found in graph's |
| 8 | `get_upstream_features` | L4:F574@2, k=5 → ❌ Feature (layer=4, pos=2, feature_idx=574) not found in graph |
| 9 | `inspect_feature` ×4 | L0:2848, L4:15899, L4:88, L3:3678 |

### Build

`build_circuit` → 19 nodes, 20 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 81,757 | 8,778 | 373,253 | 0 | $0.0575 | — | — |
| SA-3 | openai/gpt-oss-120b | 37,921 | 3,072 | 5,120 | 0 | $0.0076 | ✅ 5F/4E | Trace the path from L2:F10509 (the word "race" feature at po… |
| **Total** | | **119,678** | **11,850** | **378,373** | **0** | **$0.0651** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 40s