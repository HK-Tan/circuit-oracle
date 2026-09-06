# Circuit Oracle Report
**Date:** 2026-07-28 07:24:00 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_7 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction score is driven by a tangle of partially-content features (L4 church/building/settlement detectors triggered by "steepled abbey", L0 "first" feature at pos 2, L17 start-of-sentence) and a large mass of clearly spurious, context-mismatched features — "I"/"Exactly" (L8:8406, frac_nonzero 0.0086), code-documentation/import blocks (L7:462, L7:5741, L15:851, L16:10989), code-token/curly-brace (L9:15819, L10:14174), scientific/technical tokens (L11:11186), left-curly-bracket (L10:14174), and software-code terms (L0:11835) — which all activate on the *probe position* (pos 1 = "That") despite the actual text being a travel description, indicating the probe is reading boilerplate format features at the sentence-initial residual rather than the semantic content of the premise/hypothesis.

**Confidence:** 7

**Reasoning:** The circuit confirms the user's concern. Token-embedding nodes show the "contentful" signal is small: only `emb_abbey_10` (37.5) and `emb_steepled_led_9` (6.4) contribute strongly to content detectors (L4:4605 churches/chapels, L4:5749 settlements, L4:13244 estates/land-ownership). The "first" embedding at pos 2 strongly drives L4:2581 and L1:5053 (both "first" detectors) with direct_effect 26.25 and 33.16 activation. Crucially, however, the LATE-layer features feeding the probe logit are predominantly NOT content features:

- **L17:451** (start-of-sentence, frac_nonzero 0.0067, direct_effect 0.118) is the largest *positive* late contributor. Its upstream is dominated by L16:10989 ("the", direct_effect −12.3 to the layer-17 feature) and L13:8128 ("In"-sentence-starts, −4.9) — i.e. generic sentence-initial templates, not NLI content.
- **L8:8406** ("I"/"Exactly", direct_effect −0.164, the single largest absolute late contributor) fires on the word "That" at pos 1 — completely spurious; the model has no NLI justification for "I/Exactly" here.
- **L4:4605/5749/13244** (church/settlement/estate detectors at pos 9-10) are *inhibitory* (direct_effect −0.10 to −0.12) — they push AGAINST the contradiction class despite the text mentioning an abbey with a steeple and lacking height, which is exactly the semantic signal a faithful probe should use.
- **L0:11835** (software code terms, frac_nonzero 0.29, direct_effect 0.098) and **L0:9026** (technical/numeric, frac_nonzero 0.41) are dense, generic features firing on "abbey" — they treat the travel text like a technical document.

The signal-flow topology is: input embeddings → L0 generic lexical detectors ("of", "the", "first", "you", "abbey") → L2-3 sublexical chunks ("led" suffix, "first"-followers) → L4 entity detectors (churches, settlements, estates) → L5-8 "first"/"It"-context → L9-10 code/scientific tokens → L11-16 documentation/format features → L17 start-of-sentence → probe logit. The *upstream* layers (0-4) do encode some real content ("steepled abbey" → church/building), but those features mostly **oppose** the probe's contradiction score; the features that **drive** the contradiction score are L7-17 generic, format/genre features (code blocks, scientific jargon, curly braces, documentation) plus the start-of-sentence residual — the model is classifying the text by its *generic prose-style fingerprint* (looks like a wiki opening; code-flavored L7+ features happen to co-fire) rather than by the actual NLI content. The "negation" the user suspected (words like "lacks" / "is not") is not even in the top-20 features; the spuriousness is broader and more structural: format/genre/format-template features at the probe position, not lexical negation cues.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: abbey (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: steepled/led (pos 9) - "led" forms "steepled" | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: steep (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: towering (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: of (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: the (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: first (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: you (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 30 | Emb: of (pos 30) - in "of great height" | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 4 | Layer 0: Generic function-word / lexical detectors | the word "of" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 5 | Layer 0: Generic function-word / lexical detectors | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 10 | Layer 0: Generic function-word / lexical detectors | technical documents or data, including numbers, units, and references to figures or tables. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F11835](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11835) | 10 | Layer 0: Generic function-word / lexical detectors | terms used in software code such as "assembly", "using", "namespace", and "license" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11835) |
| [L0:F7710](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) | 21 | Layer 0: Generic function-word / lexical detectors | the pronoun "you" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 30 | Layer 0: Generic function-word / lexical detectors | the word "of" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F9854](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9854) | 2 | Layer 0: Generic function-word / lexical detectors |  words indicating possibility or future tense verbs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9854) |
| [L0:F7056](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7056) | 2 | Layer 0: Generic function-word / lexical detectors |  mentions of something happening for the first time | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7056) |
| [L2:F8046](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8046) | 1 | Layer 2-3: Sublexical/positional features |  common words and phrases that include the letter 't' and are commonly used to start clauses | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8046) |
| [L2:F5878](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5878) | 9 | Layer 2-3: Sublexical/positional features | the suffix "le" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5878) |
| [L2:F8185](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8185) | 10 | Layer 2-3: Sublexical/positional features | places for shopping or military activities | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8185) |
| [L3:F4081](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4081) | 9 | Layer 2-3: Sublexical/positional features | mentions of the statistical software Stata and the term "stent". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4081) |
| [L3:F3205](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3205) | 2 | Layer 2-3: Sublexical/positional features |  code snippets and documentation references, possibly related to web development | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3205) |
| [L4:F3833](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) | 3 | Layer 4: Entity/building/land-ownership detectors |  words used when summarizing plot points or providing courtroom insights | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) |
| [L4:F3833](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) | 4 | Layer 4: Entity/building/land-ownership detectors |  words used when summarizing plot points or providing courtroom insights | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) |
| [L4:F4605](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) | 9 | Layer 4: Entity/building/land-ownership detectors |  words related to churches, chapels and other buildings, in addition to other information of Lincolnshire | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) |
| [L4:F4605](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) | 10 | Layer 4: Entity/building/land-ownership detectors |  words related to churches, chapels and other buildings, in addition to other information of Lincolnshire | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) |
| [L4:F5749](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) | 9 | Layer 4: Entity/building/land-ownership detectors |  terms that describe ancient settlements and fortifications | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) |
| [L4:F13244](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) | 10 | Layer 4: Entity/building/land-ownership detectors |  terms related to land ownership and administration, possibly including slavery or other forms of forced labor | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) |
| [L4:F2581](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2581) | 2 | Layer 4: Entity/building/land-ownership detectors |  mentions of things being "first" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2581) |
| [L4:F9757](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) | 1 | Layer 4: Entity/building/land-ownership detectors | various acronyms, IDs, and symbols, possibly related to scientific data | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) |
| [L4:F5053](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5053) | 2 | Layer 4: Entity/building/land-ownership detectors | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5053) |
| [L5:F7444](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7444) | 2 | Layer 5-6: Sentence-initial and 'first' syntactic context |  words or phrases that an individual would express or think | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7444) |
| [L6:F5342](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5342) | 4 | Layer 5-6: Sentence-initial and 'first' syntactic context | the word "first" as well as words and prepositions that often follow it | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5342) |
| [L6:F14585](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14585) | 1 | Layer 5-6: Sentence-initial and 'first' syntactic context |  the words "the" and "it" at the beginning of sentences | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14585) |
| [L7:F462](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) | 1 | Layer 7-8: Generic 'code/format' features |  code documentation and import statements | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) |
| [L7:F5741](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5741) | 1 | Layer 7-8: Generic 'code/format' features |  code documentation or copyright information | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5741) |
| [L8:F8406](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) | 1 | Layer 7-8: Generic 'code/format' features | the first-person pronoun "I" and the word "Exactly" | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) |
| [L9:F8770](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8770) | 1 | Layer 9-10: Code tokens / curly braces | sentences beginning with "It" or "In" and also the word "There". | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8770) |
| [L9:F2762](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2762) | 1 | Layer 9-10: Code tokens / curly braces |  various code snippets, especially javascript | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2762) |
| [L9:F15819](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15819) | 1 | Layer 9-10: Code tokens / curly braces | code snippets | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15819) |
| [L10:F14174](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14174) | 1 | Layer 9-10: Code tokens / curly braces | left curly brackets | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14174) |
| [L11:F11186](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/11186) | 1 | Layer 11-13: Technical/scientific/format features + start-of-In-sentence | scientific and technical terms | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/11186) |
| [L13:F8128](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/8128) | 1 | Layer 11-13: Technical/scientific/format features + start-of-In-sentence |  sentences beginning with the word "In" | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/8128) |
| [L13:F14274](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/14274) | 1 | Layer 11-13: Technical/scientific/format features + start-of-In-sentence | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/14274) |
| [L14:F2510](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/2510) | 1 | Layer 14-16: 'using' / code-documentation blocks | the word "using" | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/2510) |
| [L15:F751](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/751) | 1 | Layer 14-16: 'using' / code-documentation blocks | code snippets | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/751) |
| [L15:F851](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/851) | 1 | Layer 14-16: 'using' / code-documentation blocks |  code documentation blocks in various programming languages | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/851) |
| [L16:F10989](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/10989) | 1 | Layer 14-16: 'using' / code-documentation blocks | the | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/10989) |
| [L17:F451](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) | 1 | Layer 17: Start-of-sentence detector (residual at probe position) | start of sentences | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) |

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
| SA-1 | `L17:F451@1` | ❌ error | — | — | Trace L17:F451 (start-of-sentence feature) upstream to understand what drives it… |
| SA-2 | `L8:F8406@1` | ❌ error | — | — | Trace L8:F8406 (first-person pronoun "I" / "Exactly" feature) upstream. This fea… |
| SA-3 | `L4:F4605@9` | ❌ error | — | — | Trace L4:F4605 (churches/chapels/building feature) at pos=9 upstream. This is a … |
| SA-4 | `L4:F5749@9` | ❌ error | — | — | Trace L4:F5749 (ancient settlements/fortifications) at pos=9 upstream. Has direc… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L17:F451@1, k=15 → L16:F10989 (de=-12.31) +14 more |
| 2 | `get_upstream_features` | L8:F8406@1, k=15 → Emb:"<bos>"@0 (de=10.69) +14 more |
| 3 | `get_upstream_features` | L4:F4605@9, k=15 → Emb:"led"@9 (de=6.44) +14 more |
| 4 | `get_upstream_features` | L4:F5749@9, k=15 → L2:F5878 (de=2.50) +14 more |
| 5 | `inspect_feature` ×7 | L16:10989, L14:2510, L13:8128, L3:4081, L2:5878, L15:751, L10:14174 |
| 6 | `get_upstream_features` | L16:F10989@1, k=15 → L15:F851 (de=28.75) +14 more |
| 7 | `get_upstream_features` | L17:F451@1, k=15 → L16:F10989 (de=-12.31) +14 more |
| 8 | `get_upstream_features` | L0:F2848@4, k=15 → Emb:" of"@4 (de=35.25) +14 more |
| 9 | `get_upstream_features` | L0:F3820@5, k=15 → Emb:" the"@5 (de=34.25) +14 more |
| 10 | `inspect_feature` ×14 | L15:851, L7:462, L9:2762, L9:8770, L9:15819, L6:14585, L7:5741, L11:11186, L0:9026, L0:11835, L4:13244, L6:5342, L2:8046, L0:9854 |
| 11 | `get_upstream_features` | L0:F9026@10, k=10 → Emb:" abbey"@10 (de=37.50) +9 more |
| 12 | `get_upstream_features` | L0:F11835@10, k=10 → Emb:" abbey"@10 (de=7.19) +9 more |
| 13 | `get_upstream_features` | L4:F13244@10, k=10 → Emb:" abbey"@10 (de=9.06) +9 more |
| 14 | `get_upstream_features` | L4:F4605@10, k=10 → Emb:" abbey"@10 (de=7.97) +9 more |
| 15 | `get_upstream_features` | L5:F7444@2, k=10 → Emb:"That"@1 (de=7.34) +9 more |
| 16 | `get_upstream_features` | L4:F2581@2, k=10 → Emb:" first"@2 (de=26.25) +9 more |
| 17 | `get_upstream_features` | L4:F2581@10, k=15 → ❌ Feature (layer=4, feature_idx=2581) not found at pos=10. Thi |
| 18 | `get_upstream_features` | L4:F9757@1, k=15 → Emb:"<bos>"@0 (de=15.31) +14 more |
| 19 | `get_upstream_features` | L0:F9026@21, k=15 → ❌ Feature (layer=0, feature_idx=9026) not found at pos=21. Thi |
| 20 | `get_upstream_features` | L0:F7710@21, k=15 → Emb:" you"@21 (de=42.25) +14 more |
| 21 | `get_upstream_features` | L0:F2848@30, k=15 → Emb:" of"@30 (de=37.25) +14 more |
| 22 | `get_upstream_features` | L4:F2581@2, k=10 → Emb:" first"@2 (de=26.25) +9 more |
| 23 | `get_upstream_features` | L0:F7710@21, k=10 → Emb:" you"@21 (de=42.25) +9 more |
| 24 | `get_upstream_features` | L0:F11835@10, k=5 → Emb:" abbey"@10 (de=7.19) +4 more |
| 25 | `get_upstream_features` | L0:F11835@10, k=5 → Emb:" abbey"@10 (de=7.19) +4 more |
| 26 | `get_upstream_features` | L4:F5749@10, k=10 → Emb:" abbey"@10 (de=7.31) +9 more |
| 27 | `get_upstream_features` | L4:F2581@10, k=10 → ❌ Feature (layer=4, feature_idx=2581) not found at pos=10. Thi |
| 28 | `get_upstream_features` | L4:F5749@10, k=10 → Emb:" abbey"@10 (de=7.31) +9 more |
| 29 | `get_upstream_features` | L4:F2581@2, k=15 → Emb:" first"@2 (de=26.25) +14 more |
| 30 | `inspect_feature` ×4 | L0:7056, L3:3205, L1:5053, L2:8185 |

### Build

`build_circuit` → 19 nodes, 23 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 94,586 | 8,467 | 796,322 | 0 | $0.0863 | — | — |
| **Total** | | **94,586** | **8,467** | **796,322** | **0** | **$0.0863** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 51s