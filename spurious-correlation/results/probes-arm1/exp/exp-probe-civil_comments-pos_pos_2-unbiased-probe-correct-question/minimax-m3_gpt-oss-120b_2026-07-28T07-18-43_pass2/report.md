# Circuit Oracle Report
**Date:** 2026-07-28 07:18:43 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by the literal token "white" plus the race/ethnicity label "Hispanic" — identity-group tokens act as a spurious shortcut, while the toxic/derogatory semantics (the "problem" framing, the conditional complaint) contribute only via generic opinion / 'if' features.

**Confidence:** 7

**Reasoning:** The output logit node is fed by a strikingly identity-token-dominated chain. The single largest direct effect comes from the *raw embedding of "white" at pos 4* (direct_effect = 40.5 into L4:15204, 43.5 into L4:7136, 29.4 into L2:585, 18 into L0:3436, 15.75 into L1:1480). That embedding signal is propagated up through a stack of "white"-detector features that are almost all *not* about the sentence's toxic content:

- L0:3436 (frac=0.061, label "mentions of the word 'white'") and L0:10910 (frac=0.015, label "the word 'possession' and the words 'white', 'immediate', 'once'") are pure lexical triggers on the word "white". They also have large direct effects on the probe directly (+0.17 and +0.10).
- L1:1480 (frac=0.004, label "the color 'white', sometimes in a context involving race") — promoted tokens are non-topical; this is a color/race cue.
- L2:13158 (frac=0.010, label "words about race and ethnicity") with promoted tokens `▁ethnic, ▁Hispanic, ▁Latino, ▁Muslim, ▁Jewish, ▁LGBT` — exactly an identity-group detector. It has a direct +0.06 to the probe.
- L2:6983 (frac=0.033, label "words related to race and slavery") and L2:585 (frac=0.005, "the word 'white', often in association with 'white dwarf'") — both lexical/identity, not semantic.
- L3:11768 (frac=0.003, label "'white' and related contexts such as diversity") and L4:7136 (frac=0.003, label "the color white") are higher-layer refinements of the same identity token.
- L4:15204 (frac=0.005, label "art galleries, museums and the White House") is the strongest late-layer driver — the autointerp says it merges cultural-institution tokens with a "White" cue; the top activating examples are all about "white" in racial / political contexts ("White House", "White Man", "whites and blacks"). Its direct effect on the probe is +0.12.

The *semantic* content of the sentence — that the speaker is saying being non-Hispanic is the *problem*, which is the actual toxic claim — is barely represented. The only non-identity features that reach the probe with meaningful weight are L6:7896 (label "sentences expressing opinions about whether something is good", direct -0.07) and L2:11539/L3:12404 ("if", direct +0.08), both of which are generic structural/grammatical cues that fire on countless innocuous sentences. The pronoun features (L0:12768 "he/she", L0:310 "she/her/he") and L0:8673 fire on the word "he" and have direct effects on the probe of +0.21 and -0.07, again with no dependence on how the pronoun is used.

Critically, the embedding of "Hispanic" at pos 7 (direct_effect 0.68 into L0:880) is the *only* signal from the second identity group in the sentence, and it is consumed by a generic "it" detector rather than by a Hispanic/ethnicity feature — so the circuit recognises that a group label is present but routes it through the same identity-token channel as "white". There is no feature anywhere in the traced circuit that encodes the *comparison* ("if he was white it would be a problem"), the negative-evaluation-of-other, or any hostility construct. The probe scores high because two identity-group tokens co-occur, not because the model is reading the derogation.

This is exactly the spurious-feature pattern the user suspected: the toxicity probe is being activated by "an identity group is being mentioned" (a bag-of-identity-tokens cue) rather than by anything semantically toxic in the prompt. The circuit shows white → identity/race features → probe, with the toxic semantics (problem, opinion, conditional grievance) reduced to generic grammatical features.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: white (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: he (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: was (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: it (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: Hispanic (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: If (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 4 | L0 white-mention detectors (fires on the token 'white') |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F10910](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) | 4 | L0 white-mention detectors (fires on the token 'white') | the word "possession" and the words "white", "immediate" and "once" regardless of context | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) |
| [L0:F8673](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8673) | 2 | L0 white-mention detectors (fires on the token 'white') | sentences that contain the word 'she' or 'he' followed by a verb | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8673) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 2 | L0 pronoun detectors (he / she) |  mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L0:F310](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/310) | 2 | L0 pronoun detectors (he / she) |  the pronouns "she", "her", and "he" and sometimes the word "therefore" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/310) |
| [L0:F2458](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2458) | 3 | L0 'was' detector | the word "was" and sometimes "were." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2458) |
| [L0:F880](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/880) | 8 | L0 'it' detector |  references to the pronoun "it", and sometimes "that", suggesting observation of the subject of a discussion | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/880) |
| [L0:F15499](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15499) | 11 | L0 's + non-space' detector (pos 11) | the letter "s" followed by a non-whitespace character | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15499) |
| [L0:F3255](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) | 5 | L0 'and' detector (pos 5) |  the word "and" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) |
| [L1:F1480](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1480) | 4 | L1 'white' (color / race) detector | the color 'white', sometimes in a context involving race | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1480) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 4 | L2 race & ethnicity detector (white / black / Hispanic / race) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F6983](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6983) | 4 | L2 race & ethnicity detector (white / black / Hispanic / race) |  words related to race and slavery | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6983) |
| [L2:F585](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) | 4 | L2 'white' (often 'white dwarf') | the word "white", often in association with "dwarf" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) |
| [L2:F11539](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11539) | 1 | L2 'if' detector | the word "if" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11539) |
| [L2:F1139](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1139) | 3 | L2 'if' detector |  various usages of the word "so", as well as some instances of the word "come" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1139) |
| [L2:F12691](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12691) | 8 | L2 generic 'show/using' (activated by 'it') |  programming or mathematics contexts of showing, using, finding, needing, letting, and being able to do something | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12691) |
| [L2:F10178](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10178) | 1 | L2 'scope' detector (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10178) |
| [L3:F11768](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11768) | 4 | L3 'white' + diversity/race context |  the word "white" and related contexts such as diversity | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11768) |
| [L3:F12404](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12404) | 1 | L3 'white' + diversity/race context |  instances of the conditional word "if" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12404) |
| [L4:F7136](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7136) | 4 | L4 'the color white' |  the color white | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7136) |
| [L4:F15204](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) | 4 | L4 'art galleries / White House' — high probe driver |  art galleries, museums and the White House | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) |
| [L6:F7896](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7896) | 3 | L6 'sentences expressing opinions about whether something is good' |  sentences expressing opinions about whether something is good | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7896) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe direction (toxicity classifier) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:12768 de=0.205 |
| 3 | `get_upstream_features` | Emb:" he"@2 (de=37.00) +9 more |
| 4 | `get_upstream_features` | Emb:" white"@4 (de=18.00) +9 more |
| 5 | `get_upstream_features` | Emb:" white"@4 (de=15.00) +9 more |
| 6 | `get_upstream_features` | Emb:" white"@4 (de=40.50) +9 more |
| 7 | `get_upstream_features` | Emb:" it"@8 (de=42.50) +9 more |
| 8 | `get_upstream_features` | Emb:" white"@4 (de=14.56) +9 more |
| 9 | `get_upstream_features` | Emb:"If"@1 (de=27.62) +9 more |
| 10 | `get_upstream_features` | Emb:"If"@1 (de=10.06) +9 more |
| 11 | `get_upstream_features` | Emb:"If"@1 (de=15.75) +9 more |
| 12 | `get_upstream_features` | Emb:"If"@1 (de=9.56) +9 more |
| 13 | `inspect_feature` ×19 | L0:12768, L0:3436, L0:13663, L4:15204, L0:880, L0:10910, L2:1139, L2:6983, L0:310, L2:11539, L0:3255, L1:1480, L4:7136, L2:12691, L0:15499, L0:10178, L3:12404, L6:7896, L0:8673 |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F15204@4` | ✅ reported | 5 | 4 | Trace the full circuit feeding the L4:15204 "white house / art galleries" featur… |
| SA-2 | `L2:F12691@8` | ✅ reported | 3 | 5 | Trace the L2:12691 feature (at pos 8, "it") which seems to be a generic showing/… |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F15204 | " art galleries, museums and the White House" |
| 2 | `get_upstream_features` | L4:F15204@4, k=10 | Emb:" white"@4 (de=40.50) +9 more |
| 3 | `inspect_feature` | L0, F10910 | "the word "possession" and the words "white", "immediate" and "once" re" |
| 4 | `get_upstream_features` | L0:F10910@4, k=10 | Emb:" white"@4 (de=14.56) +9 more |
| 5 | `inspect_feature` | L0, F2458 | " the word "was" and sometimes "were."" |
| 6 | `get_upstream_features` | L4:F15204@4, k=30 | Emb:" white"@4 (de=40.50) +29 more |
| 7 | `get_upstream_features` | L0:F2458@3, k=10 | Emb:" was"@3 (de=36.75) +9 more |
| 8 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 9 | `inspect_feature` | L0, F3436 | " mentions of the word "white"" |
| 10 | `inspect_feature` | L0, F3241 | " contexts related to "agreement", especially in a collaborative or pol" |
| 11 | `get_upstream_features` | L2:F13158@4, k=20 | Emb:" white"@4 (de=13.12) +19 more |
| 12 | `get_upstream_features` | L0:F3436@4, k=10 | Emb:" white"@4 (de=18.00) +9 more |

**Findings:** The L4:15204 probe is primarily fed by the raw embedding of the token " white" (direct_effect = 40.5). The embedding signal propagates through low‑layer features: a generic white‑detector (L0:10910), a dedicated white‑mention detector (L0:3436), a past‑tense detector (L0:2458) and a race‑ethnicity detector (L2:13158). All sit in layers ≤ 8 and have positive direct_effect, satisfying the terminatio…

</details>

<details>
<summary><b>SA-2</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F12691 | " programming or mathematics contexts of showing, using, finding, needi" |
| 2 | `get_upstream_features` | L2:F12691@8, k=10 | Emb:"If"@1 (de=10.06) +9 more |
| 3 | `inspect_feature` | L1, F8307 | " first person pronouns and words communicating doubt" |
| 4 | `get_upstream_features` | L1:F8307@8, k=10 | Emb:" it"@8 (de=7.62) +9 more |
| 5 | `inspect_feature` | L0, F880 | " references to the pronoun "it", and sometimes "that", suggesting obse" |
| 6 | `get_upstream_features` | L0:F880@8, k=10 | Emb:" it"@8 (de=42.50) +9 more |

**Findings:** The probe's L2:12691 feature receives its strongest excitatory input from the raw token embedding for "it" (direct_effect ~9.8) and a smaller contribution from the preceding token "If". A mid‑level L1 feature (8307) adds a modest contextual bias related to first‑person or doubtful phrasing, but its influence is minor (≈1.9). The bottom‑layer feature 880 is a pure pronoun detector, supplying the bu…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L2:F11539@1, k=8 → Emb:"If"@1 (de=15.06) +7 more |
| 2 | `get_upstream_features` | L1:F1480@4, k=8 → Emb:" white"@4 (de=15.75) +7 more |
| 3 | `get_upstream_features` | L2:F585@4, k=8 → Emb:" white"@4 (de=29.38) +7 more |
| 4 | `get_upstream_features` | L3:F11768@4, k=8 → Emb:" white"@4 (de=23.62) +7 more |
| 5 | `inspect_feature` ×2 | L2:585, L3:11768 |
| 6 | `get_upstream_features` | L4:F7136@4, k=8 → Emb:" white"@4 (de=43.50) +7 more |
| 7 | `get_upstream_features` | L0:F2458@3, k=5 → Emb:" was"@3 (de=36.75) +4 more |
| 8 | `get_upstream_features` | L2:F13158@4, k=8 → Emb:" white"@4 (de=13.12) +7 more |
| 9 | `inspect_feature` | L2, F13158 → " words about race and ethnicity" |

### Build

`build_circuit` → 23 nodes, 27 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 88,592 | 6,357 | 114,263 | 0 | $0.0411 | — | — |
| SA-2 | openai/gpt-oss-120b | 52,716 | 3,365 | 0 | 0 | $0.0099 | ✅ 3F/5E | Trace the L2:12691 feature (at pos 8, "it") which seems to b… |
| SA-1 | openai/gpt-oss-120b | 174,537 | 8,739 | 0 | 0 | $0.0314 | ✅ 5F/4E | Trace the full circuit feeding the L4:15204 "white house / a… |
| **Total** | | **315,845** | **18,461** | **114,263** | **0** | **$0.0824** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 33s