# Circuit Oracle Report
**Date:** 2026-07-28 07:21:47 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_7 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

Based on my analysis, the circuit driving this NLI probe is largely built on **spurious, surface-level features** rather than semantic contradiction detection.

**Analysis:** The probe's score is driven by a mix of (a) a genuine church/abbey recognition signal at "steepled" + "abbey" (pushes the probe toward the labelled class) and (b) numerous spurious features — sentence-initial position, "first" as a temporal/prepositional flag, generic "I/Exactly"-style first-person feature firing on the BOS+pos-1 context, and two broad code/document-style features that fire essentially on every input.

**Confidence:** 6

**Reasoning:**

The top direct-effect contributors to the probe split into two camps.

*Real, content-bearing signal (the church/abbey recognition path):*
- **L4:4605** at positions 9 ("steepled") and 10 ("abbey"), labeled "words related to churches, chapels and other buildings" (frac_nonzero ≈ 0.005, highly specific) — direct_effect ≈ −0.116 / −0.103. Upstream of this feature are the subword features **L2:5878** ("le" suffix) at pos 9 and **L3:689** ("l[ae] [mn]"/"leg" sequence) at pos 9, fed by the "led" and "steep" token embeddings. The "abbey" embedding at pos 10 also feeds in directly (direct_effect = +37.5 on the upstream L0:9026 path). This is a real lexical entity-recognition signal — the model genuinely registers that the token sequence describes a church/abbey. The negative sign here is informative: in the probe direction, *suppressing* this feature pushes the score toward contradiction, which is consistent with the probe tracking the *absence* of contradictory markers at this position (or, more likely, a learned direction that just happens to weight this feature negatively).

*Spurious / surface-level features (the dominant signal by total direct_effect):*
- **L0:9026** (pos 10, "abbey"), direct_effect = +0.124. Autointerp says "technical documents or data, including numbers, units, and references to figures or tables" with **frac_nonzero = 0.41** — i.e., this feature fires on roughly 41% of all tokens. It's a generic, almost universal "looks like prose/document" detector, not anything specific to the abbey or to contradiction. The "abbey" embedding pushes it (direct_effect = 37.5 on this feature), but it would fire almost anywhere.
- **L0:11835** (pos 10), direct_effect = +0.098, labeled "terms used in software code" with **frac_nonzero = 0.29**. Another extremely generic feature — fires on a quarter of all tokens — and is not actually responding to the content meaning of "abbey."
- **L0:3820** ("the"), **L0:2848** ("of"), **L0:7710** ("you") — all fire on tokens at positions 4, 5, 21, 30 with positive direct_effects of 0.10–0.15. These are **closed-class function-word detectors**, not contradiction cues. The "you" embedding at pos 21 ("you will not forget") drives L0:7710, but L0:7710 has no negation/contradiction semantics — it's just a "you" detector.
- **L6:5342** at pos 4, direct_effect = +0.123, labeled "the word 'first' as well as words and prepositions that often follow it" (frac_nonzero ≈ 0.04). It is fed primarily by the **" first" embedding at pos 2** (direct_effect = +12.06 on the upstream trace) and the " glimpse" embedding (pos 3, +1.99). The feature fires on "That first glimpse…" — a **temporal/ordinal surface pattern**, not a contradiction signal.
- **L8:8406** at pos 1, direct_effect = −0.164 (the single largest-magnitude feature in the circuit). The autointerp label "the first-person pronoun 'I' and the word 'Exactly'" is misleading for this prompt — the trace shows it's fed by the **BOS embedding at pos 0** (direct_effect = +10.7 on upstream) and several **code-documentation features** at L5–L7 (L5:3992, L7:462, L7:5741, L7:3099, all with labels like "code documentation and import statements," frac_nonzero 0.008–0.025). What is actually being read here is *BOS + sentence-initial position + a non-prose signal* — again, surface, not semantic.
- **L17:451** at pos 1, direct_effect = +0.118, labeled "start of sentences" (frac_nonzero ≈ 0.007). This is literally a sentence-initial position detector, fed upstream by the "That" embedding and by the same code-documentation features. It carries no contradiction information.

**Critical observation for the user's concern:** The user's hypothesis is partially correct and partially inverted. The circuit is *not* primarily using explicit "negation words" — the words "not" and "lacks" do not appear in the top features at all (and " not" at pos 26 has no strong driver). Instead, the dominant signal is a combination of:

1. **Generic, high-firing rate features** (L0:9026 at frac_nonzero = 0.41, L0:11835 at frac_nonzero = 0.29, L0:3820 at 0.03) that fire on many tokens in many contexts — these are the most extreme cases of "spurious."
2. **Surface syntactic position features** (L17:451 "start of sentences," L8:8406 BOS+pos1, L6:5342 "first"-as-ordinal).
3. **A genuine entity-recognition feature** (L4:4605 church/chapel recognition) — this is the *only* clearly content-bearing feature, and even it has a counter-signal (L4:5749 "ancient settlements/fortifications" and L4:13244 "land ownership") that fires on the same "abbey"/"steepled" tokens but with opposite sign.

The probe direction in this graph is *not* primarily encoding the actual contradiction between "steepled abbey" and "lacks a steeple" — there is no feature in the top 20 that detects "lacks" or "steepled ∨ has_steeple" as a property. Instead, the score reflects a noisy combination of broad document-style features, sentence-position features, and an abbey/church recognition signal that happens to be weighted in the trained probe direction. This is consistent with a probe that learned a partially spurious shortcut rather than the true entailment-relation semantics.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 0 | Emb: <bos> (pos 0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: " first" (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: " glimpse" (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: " steep" (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: "led" (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: " abbey" (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: "That" (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: " you" (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 5 | Function/closed-class words (the, of, you) | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 4 | Function/closed-class words (the, of, you) | the word "of" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 30 | Function/closed-class words (the, of, you) | the word "of" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F7710](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) | 21 | Function/closed-class words (the, of, you) | the pronoun "you" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 10 | Generic code/document signal features (broad) | technical documents or data, including numbers, units, and references to figures or tables. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F11835](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11835) | 10 | Generic code/document signal features (broad) | terms used in software code such as "assembly", "using", "namespace", and "license" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11835) |
| [L2:F5878](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5878) | 9 | Subword/lexical at "steepled" | the suffix "le" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5878) |
| [L2:F1924](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1924) | 9 | Subword/lexical at "steepled" | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1924) |
| [L2:F8046](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8046) | 1 | Subword/lexical at "steepled" |  common words and phrases that include the letter 't' and are commonly used to start clauses | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8046) |
| [L4:F4605](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) | 9 | Church/chapel/building recognition at "steepled" (NEGATIVE driver) |  words related to churches, chapels and other buildings, in addition to other information of Lincolnshire | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) |
| [L4:F4605](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) | 10 | Church/chapel/building recognition at "steepled" (NEGATIVE driver) |  words related to churches, chapels and other buildings, in addition to other information of Lincolnshire | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) |
| [L4:F5749](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) | 9 | Church/chapel/building recognition at "steepled" (NEGATIVE driver) |  terms that describe ancient settlements and fortifications | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) |
| [L4:F13244](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) | 10 | Church/chapel/building recognition at "steepled" (NEGATIVE driver) |  terms related to land ownership and administration, possibly including slavery or other forms of forced labor | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) |
| [L4:F2581](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2581) | 2 | Church/chapel/building recognition at "steepled" (NEGATIVE driver) |  mentions of things being "first" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2581) |
| [L4:F3833](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) | 3 | Church/chapel/building recognition at "steepled" (NEGATIVE driver) |  words used when summarizing plot points or providing courtroom insights | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) |
| [L4:F3833](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) | 4 | Church/chapel/building recognition at "steepled" (NEGATIVE driver) |  words used when summarizing plot points or providing courtroom insights | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) |
| [L4:F9757](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) | 1 | Church/chapel/building recognition at "steepled" (NEGATIVE driver) | various acronyms, IDs, and symbols, possibly related to scientific data | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) |
| [L4:F2053](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2053) | 4 | Church/chapel/building recognition at "steepled" (NEGATIVE driver) |  references to components of equations or theorems | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2053) |
| [L4:F10564](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10564) | 4 | Church/chapel/building recognition at "steepled" (NEGATIVE driver) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10564) |
| [L4:F488](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/488) | 4 | Church/chapel/building recognition at "steepled" (NEGATIVE driver) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/488) |
| [L4:F3395](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3395) | 4 | Church/chapel/building recognition at "steepled" (NEGATIVE driver) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3395) |
| [L6:F5342](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5342) | 4 | "first" prepositional/early word context at pos 4 (POSITIVE driver) | the word "first" as well as words and prepositions that often follow it | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5342) |
| [L8:F8406](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) | 1 | L8 "I/Exactly" generic first-person feature (NEGATIVE driver) — fires on BOS+pos1 context | the first-person pronoun "I" and the word "Exactly" | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) |
| [L17:F451](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) | 1 | L17 "start of sentence" feature (POSITIVE driver) | start of sentences | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe (contradiction direction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L8:8406 de=-0.164 |
| 3 | `inspect_feature` ×17 | L8:8406, L0:2848, L0:3820, L4:3833, L0:9026, L6:5342, L17:451, L4:4605, L4:5749, L0:7710, L4:13244, L4:2581, L0:11835, L2:8046, L5:7444, L0:9854, L4:9757 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L8:F8406@1` | ❌ error | — | — | Trace this L8 feature (which is the top negative contributor to the probe with d… |
| SA-2 | `L17:F451@1` | ❌ error | — | — | Trace this L17 feature (direct_effect=+0.118) labeled "start of sentences" at po… |
| SA-3 | `L6:F5342@4` | ❌ error | — | — | Trace this L6 feature (direct_effect=+0.123) labeled "the word 'first' as well a… |
| SA-4 | `L4:F4605@9` | ❌ error | — | — | Trace this L4 feature (direct_effect=-0.116) labeled "words related to churches,… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L8:F8406@1, k=15 → Emb:"<bos>"@0 (de=10.69) +14 more |
| 2 | `get_upstream_features` | L17:F451@1, k=15 → L16:F10989 (de=-12.31) +14 more |
| 3 | `get_upstream_features` | L6:F5342@4, k=15 → Emb:" first"@2 (de=12.06) +14 more |
| 4 | `get_upstream_features` | L4:F4605@9, k=15 → Emb:"led"@9 (de=6.44) +14 more |
| 5 | `inspect_feature` ×13 | L7:462, L7:5741, L5:3992, L6:14585, L3:4081, L3:7650, L1:14137, L16:10989, L10:14174, L9:8770, L4:2053, L4:5749, L0:7710 |
| 6 | `get_upstream_features` | L4:F5749@9, k=10 → L2:F5878 (de=2.50) +9 more |
| 7 | `get_upstream_features` | L0:F9026@10, k=10 → Emb:" abbey"@10 (de=37.50) +9 more |
| 8 | `inspect_feature` ×4 | L2:5878, L3:689, L4:14857, L4:8952 |
| 9 | `get_upstream_features` | L0:F9026@10, k=5 → Emb:" abbey"@10 (de=37.50) +4 more |

### Build

`build_circuit` → 16 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 71,668 | 6,793 | 294,695 | 0 | $0.0473 | — | — |
| **Total** | | **71,668** | **6,793** | **294,695** | **0** | **$0.0473** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 55s