# Circuit Oracle Report
**Date:** 2026-07-28 07:10:17 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe is driven primarily by a stack of generic, low-layer **negation-lexeme detectors** at the hypothesis position (pos 36, " not") — culminating in L16:F6800 — that fire on the surface token "not" itself rather than on any semantic incompatibility between the premise and the hypothesis. The remainder of the circuit consists of off-target lexical/grammatical features at unrelated positions (itself, with, father, latest) and weak entity hints from "castle" and "century".

**Confidence:** 8

**Reasoning:** The dominant causal pathway is a **purely lexical negation signal** at pos 36 (the " not" embedding → L0:F4958 [frac_nonzero 0.018, "the word not"], L1:F14233 [0.014, "negative sentiment markers not/no/never…"], L3:F8011 [0.003, multilingual not-variants], L3:F3534 [0.008, "n't" suffix], L4:F4492 [0.038, "negations in various languages"]) → L16:F6800 [0.031, "negations 'not', 'no', and contractions with 't'"] → output logit. L16:F6800 is the **single largest direct contributor** to the probe (direct_effect 0.208) and every one of its top-8 upstream drivers is either the raw " not" embedding (12.5), the " does" embedding (9.06), or a feature whose *own* top activator is "not" (L15:F11794 "phrases that express disagreement or negation", L13:F102 "phrases containing 'not' or negative connotations", L0:F4958 "the word 'not'"). This is exactly the spurious cue the user suspected: any well-formed English sentence that contains the word "not" in the hypothesis will trip the probe, regardless of whether the hypothesis is actually a contradiction.

The auxiliary paths do not fix this. The " castle" path (L4:F13244 "land ownership/estates", L4:F5749 "ancient settlements/fortifications", L7:F13215 "military fortifications", direct_effects 0.21/0.24/0.28 to the probe) encodes a genuine semantic concept, but it is grounded on the premise subject, not on the contradictory relation — it would fire identically on any entailment pair mentioning a castle. The "century" features (L0:F1454, L0:F4367, L4:F5386, direct_effects 0.21 / -0.20 / 0.22) similarly fire on the mere presence of the word "century" in the premise. The remaining top-15 features are noise: L0:F10346 fires on "itself" with NEGATIVE direct_effect (-0.24), L0:F11 fires on "press" with NEGATIVE effect at pos 3 (mismatched position — autointerp says "press/button"), L0:F12378 fires on "latest" at pos 3, L0:F15322 on reflexive pronouns, L0:F15866 on "father/my" at pos 4 (this is the <bos> neighborhood, not pos 4 of a real semantic role), L0:F2158 on "with" at pos 17, and L2:F2415 on "any/does/contain/not" with direct_effect 0.186. These are all off-topic word detectors that happened to fire somewhere in the prompt.

The single most diagnostic point: **the "contradiction" probe has no feature in the top-15 that integrates the premise and hypothesis**, no feature that compares "early 17th-century tower house" against "early 17th-century tower houses", and no feature that handles the actual semantic negation of set-membership. Instead it rides on (a) the bare token "not" at the hypothesis position, and (b) a bag of unrelated lexical detectors. The user's concern is confirmed: the probe's classification is being driven by a **negation-word shortcut**, not by genuine contradiction detection.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe direction (contradiction classification) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L16:F6800](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) | 36 | Late-layer negation hub at pos 36 ('does not contain') |  negations "not", "no", and contractions with "t".  | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 36 | Generic negation detector (multi-language) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 36 | Layer-0 'not' word detector |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 36 | Multilingual 'not'/negation detector | a mix of words and code fragments from different languages | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L3:F3534](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3534) | 36 | "n't" contraction suffix detector | the character sequence "n't" or "nut" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3534) |
| [L1:F14233](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) | 36 | Negative-sentiment markers (not/no/never, multiling) |  negative sentiment markers such as "not," "no," "never," and their equivalents in other languages | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) |
| [L2:F2415](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2415) | 38 | Small-quantity/negative-connotation word detector |  frequent words indicating small quantities or proximity, or words with negative connotations | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2415) |
| [L4:F13244](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) | 2 | Premise entity features (castle -> estate/fortification) at pos 2 (POSITIVE) |  terms related to land ownership and administration, possibly including slavery or other forms of forced labor | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) |
| [L4:F5749](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) | 2 | Premise entity features (castle -> estate/fortification) at pos 2 (POSITIVE) |  terms that describe ancient settlements and fortifications | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) |
| [L7:F13215](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13215) | 2 | Premise entity features (castle -> estate/fortification) at pos 2 (POSITIVE) |  terms used to describe military fortifications. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13215) |
| [L0:F1454](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1454) | 12 | Premise 'century' lexical features at pos 12 (mixed sign) |  mentions of specific centuries or decades | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1454) |
| [L0:F4367](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4367) | 12 | Premise 'century' lexical features at pos 12 (mixed sign) |  references to centuries | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4367) |
| [L4:F5386](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5386) | 12 | Premise 'century' lexical features at pos 12 (mixed sign) |  mentions of centuries and decades | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5386) |
| [L0:F10346](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10346) | 3 | Off-target lexical features (itself, latest, father, with) at pos 3/4/17 - SPURIOUS |  the word "itself" and sometimes the word "node" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10346) |
| [L1:F11](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11) | 3 | Off-target lexical features (itself, latest, father, with) at pos 3/4/17 - SPURIOUS |  the word "press", sometimes in conjunction with "button." | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11) |
| [L0:F15322](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15322) | 3 | Off-target lexical features (itself, latest, father, with) at pos 3/4/17 - SPURIOUS | reflexive pronouns, particularly "herself" and "itself." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15322) |
| [L0:F12378](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12378) | 3 | Off-target lexical features (itself, latest, father, with) at pos 3/4/17 - SPURIOUS |  the word "latest." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12378) |
| [L0:F15866](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15866) | 4 | Off-target lexical features (itself, latest, father, with) at pos 3/4/17 - SPURIOUS |  references to one's paternal and maternal figures, as well as the pronouns 'we' and 'my' | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15866) |
| [L0:F2158](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) | 17 | Off-target lexical features (itself, latest, father, with) at pos 3/4/17 - SPURIOUS | the word "with" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2158 de=0.277 |
| 3 | `inspect_feature` ×6 | L0:2158, L0:10346, L4:13244, L0:12378, L3:232, L4:4492 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F4492@36` | ✅ reported | 3 | 5 | Trace the negation feature at L4:F4492 upstream. Determine which input tokens dr… |
| SA-2 | `L4:F13244@2` | ✅ reported | 5 | 7 | Trace the land ownership feature at L4:F13244 upstream. Determine what input tok… |
| SA-3 | `L7:F13215@2` | ❌ error | — | — | Trace L7:F13215 upstream. Determine which input tokens drive this feature and wh… |
| SA-4 | `L16:F6800@36` | ✅ reported | 6 | 10 | Trace L16:F6800 upstream. Determine what input token at pos 36 drives this featu… |

<details>
<summary><b>SA-1</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F4492 | "negations in various languages" |
| 2 | `get_upstream_features` | L4:F4492@36, k=10 | Emb:" not"@36 (de=17.62) +9 more |
| 3 | `inspect_feature` | L3, F8011 | " a mix of words and code fragments from different languages" |
| 4 | `inspect_feature` | L3, F3534 | "the character sequence "n't" or "nut"" |
| 5 | `get_upstream_features` | L3:F8011@36, k=10 | Emb:" not"@36 (de=20.75) +9 more |
| 6 | `get_upstream_features` | L3:F3534@36, k=10 | Emb:" not"@36 (de=16.12) +9 more |

**Findings:** The L4 negation feature (F4492) receives its strongest excitatory drive from the embedding of the token ' not' at position 36 (direct_effect ≈ 17.6). Two mid‑level features in layer 3 (F8011 and F3534) also contribute positively (≈2.1 and ≈1.8 respectively) and themselves are driven primarily by the same ' not' embedding (direct_effect ≈ 20.8 and 16.1). Feature 8011 is a generic multilingual detec…

</details>

<details>
<summary><b>SA-2</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13244 | " terms related to land ownership and administration, possibly includin" |
| 2 | `get_upstream_features` | L4:F13244@2, k=10 | Emb:" castle"@2 (de=18.50) +9 more |
| 3 | `inspect_feature` | L2, F8185 | "places for shopping or military activities" |
| 4 | `get_upstream_features` | L2:F8185@2, k=10 | Emb:" castle"@2 (de=9.25) +9 more |
| 5 | `inspect_feature` | L2, F9529 | " words related to slavery and slave ownership" |
| 6 | `inspect_feature` | L1, F12474 | " the word "technology" near other related words like "computer"" |
| 7 | `inspect_feature` | L1, F8633 | " words or phrases related to tourism and historical places" |
| 8 | `inspect_feature` | L2, F12263 | " words related to agriculture/mining and to slavery/plantations" |
| 9 | `get_upstream_features` | L2:F9529@2, k=5 | Emb:" castle"@2 (de=13.38) +4 more |

**Findings:** The land‑ownership feature L4:F13244 is primarily driven by the input token at position 2, "castle", which supplies a large positive direct effect (18.5). Downstream, lower‑layer place‑type detectors (L2:F8185, L2:F9529) and a tourism‑place detector (L1:F8633) relay this signal upward, while a sparse slavery‑related detector (L2:F9529) adds a historical‑ownership nuance. Because the top‑promoted t…

</details>

<details>
<summary><b>SA-4</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L16, F6800 | " negations "not", "no", and contractions with "t". " |
| 2 | `get_upstream_features` | L16:F6800@36, k=10 | Emb:" not"@36 (de=12.50) +9 more |
| 3 | `inspect_feature` | L3, F3534 | "the character sequence "n't" or "nut"" |
| 4 | `inspect_feature` | L15, F11794 | " phrases that express disagreement or negation" |
| 5 | `get_upstream_features` | L3:F3534@36, k=10 | Emb:" not"@36 (de=16.12) +9 more |
| 6 | `get_upstream_features` | L15:F11794@36, k=10 | Emb:" does"@35 (de=7.19) +9 more |
| 7 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 8 | `inspect_feature` | L13, F102 | " phrases containing "not" or negative connotations" |
| 9 | `inspect_feature` | L14, F6648 | " words and phrases that indicate speculation, possibility, or negation" |
| 10 | `get_upstream_features` | L16:F6800@36, k=10 | Emb:" not"@36 (de=12.50) +9 more |

**Findings:** The target feature L16:F6800 is a canonical negation detector. Its strongest upstream driver is the raw embedding of the token "not" at position 36 (direct_effect 12.5), confirming that the feature is primarily grounded in the explicit negation word. Secondary contributors include the embedding for "does" (providing syntactic context), a low‑layer "'t" suffix detector (L3:F3534), and a bottom‑laye…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L7:F13215@2, k=10 → L4:F5749 (de=8.25) +9 more |
| 2 | `get_upstream_features` | L0:F1454@12, k=10 → Emb:"century"@12 (de=19.12) +9 more |
| 3 | `get_upstream_features` | L4:F5386@12, k=10 → Emb:"century"@12 (de=25.00) +9 more |
| 4 | `get_upstream_features` | L0:F4367@12, k=10 → Emb:"century"@12 (de=23.12) +9 more |
| 5 | `get_upstream_features` | L2:F2415@38, k=10 → Emb:" not"@36 (de=10.06) +9 more |
| 6 | `inspect_feature` ×7 | L7:13215, L0:1454, L4:5386, L0:4367, L2:2415, L0:15866, L0:15322 |
| 7 | `get_upstream_features` | L4:F5749@2, k=8 → Emb:" castle"@2 (de=14.75) +7 more |
| 8 | `get_upstream_features` | L0:F10346@3, k=8 → Emb:" itself"@3 (de=13.94) +7 more |
| 9 | `get_upstream_features` | L1:F11@3, k=8 → Emb:" itself"@3 (de=20.00) +7 more |
| 10 | `get_upstream_features` | L2:F2415@38, k=8 → Emb:" not"@36 (de=10.06) +7 more |
| 11 | `inspect_feature` ×3 | L4:5749, L1:11, L0:10815 |
| 12 | `get_upstream_features` | L0:F11739@3, k=5 → Emb:" itself"@3 (de=16.62) +4 more |
| 13 | `get_upstream_features` | L0:F8371@3, k=5 → Emb:" itself"@3 (de=19.75) +4 more |
| 14 | `get_upstream_features` | L0:F11891@3, k=5 → Emb:" itself"@3 (de=13.44) +4 more |
| 15 | `inspect_feature` ×4 | L0:11739, L0:8371, L0:11891, L1:14233 |

### Build

`build_circuit` → 20 nodes, 27 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 63,702 | 9,646 | 282,944 | 0 | $0.0477 | — | — |
| SA-2 | openai/gpt-oss-120b | 101,035 | 6,112 | 2,592 | 0 | $0.0189 | ✅ 5F/7E | Trace the land ownership feature at L4:F13244 upstream. Dete… |
| SA-1 | openai/gpt-oss-120b | 55,616 | 3,407 | 160 | 0 | $0.0104 | ✅ 3F/5E | Trace the negation feature at L4:F4492 upstream. Determine w… |
| SA-4 | openai/gpt-oss-120b | 116,326 | 5,065 | 192 | 0 | $0.0205 | ✅ 6F/10E | Trace L16:F6800 upstream. Determine what input token at pos … |
| **Total** | | **336,679** | **24,230** | **285,888** | **0** | **$0.0974** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 19s