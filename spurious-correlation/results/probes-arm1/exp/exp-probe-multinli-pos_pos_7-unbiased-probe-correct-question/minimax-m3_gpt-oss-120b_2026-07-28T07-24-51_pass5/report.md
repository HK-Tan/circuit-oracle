# Circuit Oracle Report
**Date:** 2026-07-28 07:24:51 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_7 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "contradiction" classification is driven by a mix of entity/subject features for "abbey" and generic surface features for function words ("of", "the"), opening clauses ("That", "first", "glimpse"), with several opposing generic-syntax and person-pronoun features; **no feature encoding negation ("not", "lacks", "no") appears anywhere in the top 20 features driving the probe direction.**

**Confidence:** 7

**Reasoning:** The attribution graph traces cleanly to token-embedding nodes and shows two opposing streams:

1. **Pro-contradiction (positive direct_effect) features** are overwhelmingly content- and surface-form features tied to the *premise* side of the contrast (sentence 1), not to the negation in sentence 2. Key drivers:
   - **L0:F9026 (DE=+0.124), L0:F11835 (DE=+0.098), L4:F13244 (DE=+0.107)** all fire on the token "abbey" at pos 10 and trace to the **Emb: "abbey" (pos 10)** node — these are entity/subject detectors, not negation detectors.
   - **L0:F2848 (DE=+0.153) and L0:F3820 (DE=+0.143)** fire on the function words "of" and "the" at pos 4–5 and pos 5, tracing to the **Emb: "of" (pos 4)** and **Emb: "the" (pos 5)** embedding nodes. These are high-frac_nonzero generic function-word features (frac=0.020 and 0.030) that fire on most English text.
   - **L4:F3833 (DE=+0.127–+0.142)** fires at pos 3–4 on "glimpse/first" and traces to **Emb: "glimpse" (pos 3)** and **Emb: "first" (pos 2)** — labeled "plot points / courtroom insights", frac=0.011.
   - **L6:F5342 (DE=+0.123)** at pos 4 ("glimpse of") traces to **Emb: "first" (pos 2)** — labeled "first and following words", promoted tokens include "First/first/FIRST".
   - **L2:F8046 (DE=+0.098)** at pos 1 = "That" — start-of-clause t-word detector (frac=0.006).
   - **L0:F9854 (DE=+0.094)** at pos 2 = "first" but the autointerp is "will/may/would" future-tense; this is a generic modal/possibility detector.

2. **Anti-contradiction (negative direct_effect) features** are also generic syntax/function-word features, including:
   - **L8:F8406 (DE=−0.164)** at pos 1 ("That") — labeled "I/Exactly", but its top-activating examples are not actually I/Exactly tokens; it is fed by **Emb: \<bos\>** and multiple code-documentation features (L7:F462 "code docs", L7:F5741 "code docs", L5:F3992 "code docs", L6:F14585 "the/it at sentence start"). It behaves as a generic start-of-sequence feature, **not a negation feature**.
   - **L17:F451 (DE=+0.118 but acting on suppression side via upstream feed)** — "start of sentences" (frac=0.0067), a syntax feature.
   - **L4:F4605 (DE=−0.116), L4:F5749 (DE=−0.115)** at pos 9 ("steepled") — "churches/chapels" and "ancient settlements" — interesting: they are entity-typed features that fire on the "steepled abbey" content, but their *direct_effect is negative*, which suggests they represent a "consistent/true" prior on religious-architecture sentences that opposes the contradiction label.
   - **L0:F7710 (DE=−0.112)** at pos 21 — the "you" pronoun feature (Emb: "you" pos 21 is in the premise's "you will not forget").
   - **L4:F2581 (DE=−0.101)** at pos 2 = "first" — promoted tokens include "first/First/FIRST".
   - **L5:F7444 (DE=−0.094)** at pos 2 — "words one thinks/says", generic.

**Crucial observation regarding the user's concern:** The user hypothesized that the circuit might use negation words like "not" or "lacks" as spurious contradiction signals. However, **inspection of the top 20 features (all of which directly drive the probe direction) and all traced upstream paths reveals no feature whose autointerp, top-activating examples, or promoted tokens reference negation, "not", "no", "lacks", or any antonym/contrast marker.** Position 25 ("not" in "is not of great height") and position 28 ("lacks") do not surface in the top 20 features at all, and no upstream tracing leads to them. Instead, the contradiction signal is carried by:
- A content-entity feature on "abbey" (pos 10)
- Multiple high-frequency function-word features on "of"/"the" in the premise
- A "first/glimpse" opening-clause feature (L4:F3833, L6:F5342, L0:F9854) — interestingly, these could be interpreted as a *first-sentence-vs-second-sentence position feature* (the first sentence is detailed/evocative, the second is a flat denial), which is a structural rather than semantic cue to contradiction.

So the circuit does not rely on negation words. The contradiction classification is driven by a mix of (a) entity/subject recognition of "abbey" and (b) generic function-word and clause-opening features that happen to distinguish premise from hypothesis, plus a negation of religious-architecture priors. This is a partly-valid content signal (the "abbey" feature is real-world knowledge) layered with mostly generic surface features — it is not a negation-word shortcut, but it is also not a clean semantic understanding of the contradiction.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L8:F8406](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) | 1 | L8:F8406 'I/Exactly' start-of-input generic (pushes AWAY) | the first-person pronoun "I" and the word "Exactly" | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) |
| [L17:F451](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) | 1 | L17:F451 'start of sentences' generic syntax (pushes AWAY) | start of sentences | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) |
| [L4:F4605](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) | 9 | L4:F4605 'church/chapel' (pushes AWAY) |  words related to churches, chapels and other buildings, in addition to other information of Lincolnshire | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) |
| [L4:F5749](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) | 9 | L4:F5749 'ancient fortification' (pushes AWAY) |  terms that describe ancient settlements and fortifications | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) |
| [L0:F7710](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) | 21 | L0:F7710 'you' pronoun (pushes AWAY) | the pronoun "you" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) |
| [L4:F2581](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2581) | 2 | L4:F2581 'first' detector (pushes AWAY) |  mentions of things being "first" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2581) |
| [L5:F7444](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7444) | 2 | L5:F7444 'words one thinks/says' (pushes AWAY) |  words or phrases that an individual would express or think | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7444) |
| [L0:F9854](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9854) | 2 | L0:F9854 'will' future/possibility (pushes TOWARD) |  words indicating possibility or future tense verbs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9854) |
| [L2:F8046](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8046) | 1 | L2:F8046 'That' start-clause t-word (pushes TOWARD) |  common words and phrases that include the letter 't' and are commonly used to start clauses | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8046) |
| [L0:F11835](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11835) | 10 | L0:F11835 'abbey' (pushes TOWARD) | terms used in software code such as "assembly", "using", "namespace", and "license" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11835) |
| [L4:F13244](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) | 10 | L4:F13244 'abbey' (pushes TOWARD) |  terms related to land ownership and administration, possibly including slavery or other forms of forced labor | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) |
| [L6:F5342](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5342) | 4 | L6:F5342 'first/glimpse' opening (pushes TOWARD) | the word "first" as well as words and prepositions that often follow it | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5342) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 10 | L0:F9026 'abbey' entity (pushes TOWARD) | technical documents or data, including numbers, units, and references to figures or tables. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L4:F3833](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) | 4 | L4:F3833 'glimpse/first' opening (pushes TOWARD) |  words used when summarizing plot points or providing courtroom insights | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) |
| [L4:F3833](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) | 3 | L4:F3833 'glimpse/first' opening (pushes TOWARD) |  words used when summarizing plot points or providing courtroom insights | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 5 | L0:F3820 'the' function word (pushes TOWARD) | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 4 | L0:F2848 'of' function word (pushes TOWARD) | the word "of" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 30 | L0:F2848 'of' function word (pushes TOWARD) | the word "of" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L8:8406 de=-0.164 |
| 3 | `inspect_feature` ×17 | L8:8406, L0:2848, L0:3820, L4:3833, L0:9026, L6:5342, L17:451, L4:4605, L4:5749, L0:7710, L4:13244, L4:2581, L0:11835, L2:8046, L5:7444, L0:9854, L4:9757 |

### Dispatch: 13 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L8:F8406@1` | ❌ error | — | — | Trace L8:F8406 — labeled as "I" pronoun / "Exactly". Investigate whether this is… |
| SA-2 | `L0:F2848@4` | ❌ error | — | — | Trace L0:F2848 — labeled as the word "of". This fires at position 4 ("glimpse of… |
| SA-3 | `L4:F3833@4` | ❌ error | — | — | Trace L4:F3833 at position 4. Labeled as "plot points / courtroom insights". Con… |
| SA-4 | `L4:F4605@9` | ❌ error | — | — | Trace L4:F4605 at position 9 — labeled "churches / chapels / Lincolnshire". Posi… |
| SA-5 | `L4:F5749@9` | ❌ error | — | — | Trace L4:F5749 at pos 9 — labeled "ancient settlements and fortifications". Posi… |
| SA-6 | `L0:F7710@21` | ❌ error | — | — | Trace L0:F7710 at pos 21 — labeled "you". Position 21 likely contains "not" or "… |
| SA-7 | `L17:F451@1` | ❌ error | — | — | Trace L17:F451 at pos 1 — labeled "start of sentences". This is a high-activatio… |
| SA-8 | `L0:F9026@10` | ❌ error | — | — | Trace L0:F9026 at pos 10 — "technical documents/numbers". Pos 10 is "sea" or "ro… |
| SA-9 | `L6:F5342@4` | ❌ error | — | — | Trace L6:F5342 at pos 4 — labeled "first and following words". Pos 4 is "glimpse… |
| SA-10 | `L4:F13244@10` | ❌ error | — | — | Trace L4:F13244 at pos 10 — "land ownership / administration". Pos 10 is "sea" o… |
| SA-11 | `L4:F2581@2` | ❌ error | — | — | Trace L4:F2581 at pos 2 — "mentions of first". Pos 2 is "first". Trace upstream. |
| SA-12 | `L2:F8046@1` | ❌ error | — | — | Trace L2:F8046 at pos 1 — "t-words starting clauses". Pos 1 is "That". Trace ups… |
| SA-13 | `L5:F7444@2` | ❌ error | — | — | Trace L5:F7444 at pos 2 — "words an individual expresses". Pos 2 is "first". Tra… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L8:F8406@1, k=15 → Emb:"<bos>"@0 (de=10.69) +14 more |
| 2 | `get_upstream_features` | L0:F2848@4, k=15 → Emb:" of"@4 (de=35.25) +14 more |
| 3 | `get_upstream_features` | L0:F3820@5, k=15 → Emb:" the"@5 (de=34.25) +14 more |
| 4 | `get_upstream_features` | L4:F3833@4, k=15 → Emb:" glimpse"@3 (de=7.03) +14 more |
| 5 | `get_upstream_features` | L17:F451@1, k=15 → L16:F10989 (de=-12.31) +14 more |
| 6 | `get_upstream_features` | L4:F4605@9, k=15 → Emb:"led"@9 (de=6.44) +14 more |
| 7 | `get_upstream_features` | L4:F5749@9, k=15 → L2:F5878 (de=2.50) +14 more |
| 8 | `get_upstream_features` | L0:F7710@21, k=15 → Emb:" you"@21 (de=42.25) +14 more |
| 9 | `get_upstream_features` | L4:F2581@2, k=15 → Emb:" first"@2 (de=26.25) +14 more |
| 10 | `get_upstream_features` | L4:F13244@10, k=15 → Emb:" abbey"@10 (de=9.06) +14 more |
| 11 | `get_upstream_features` | L6:F5342@4, k=15 → Emb:" first"@2 (de=12.06) +14 more |
| 12 | `get_upstream_features` | L0:F9026@10, k=15 → Emb:" abbey"@10 (de=37.50) +14 more |
| 13 | `inspect_feature` ×4 | L2:5878, L3:4081, L2:8185, L7:462 |
| 14 | `get_upstream_features` | L8:F8406@1, k=10 → Emb:"<bos>"@0 (de=10.69) +9 more |
| 15 | `inspect_feature` ×4 | L7:5741, L5:3992, L6:14585, L0:7056 |
| 16 | `get_top_features` | token="", k=10 → 10 features; top: L8:8406 de=-0.164 |
| 17 | `get_upstream_features` | L8:F8406@1, k=5 → Emb:"<bos>"@0 (de=10.69) +4 more |
| 18 | `get_upstream_features` | L17:F451@1, k=5 → L16:F10989 (de=-12.31) +4 more |
| 19 | `inspect_feature` ×5 | L16:10989, L14:2510, L15:751, L10:14174, L13:8128 |
| 20 | `get_upstream_features` | L0:F2848@30, k=3 → Emb:" of"@30 (de=37.25) +2 more |
| 21 | `get_upstream_features` | L4:F3833@3, k=3 → Emb:" glimpse"@3 (de=13.56) +2 more |
| 22 | `get_upstream_features` | L0:F11835@10, k=3 → Emb:" abbey"@10 (de=7.19) +2 more |
| 23 | `get_upstream_features` | L8:F8406@1, k=5 → Emb:"<bos>"@0 (de=10.69) +4 more |

### Build

`build_circuit` → 25 nodes, 30 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 76,398 | 12,051 | 719,367 | 0 | $0.0805 | — | — |
| **Total** | | **76,398** | **12,051** | **719,367** | **0** | **$0.0805** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 33s