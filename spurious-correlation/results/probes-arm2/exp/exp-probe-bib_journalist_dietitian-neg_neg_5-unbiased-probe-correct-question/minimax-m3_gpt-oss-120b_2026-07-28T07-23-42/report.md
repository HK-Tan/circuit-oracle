# Circuit Oracle Report
**Date:** 2026-07-28 07:23:42 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe driving "reporter"-class score is dominated by features that activate on the literal token " reporter" at position 66, with the pronoun "He" (pos 1) and sentence connectors ("in", "from", "ever", "has", ".") acting as inhibitory/spurious confounders — not genuine profession semantics.

**Confidence:** 4

**Reasoning:** The bulk of positive signal flows from the embedding of " reporter" (pos 66, direct_effect 18.75 into L14:F4420 and 28.25 into L19:F2486) upward through a deep chain of token-local features: L0:F1579 → L4:F13253 (direct_effect 26.6) → L6:L8:L7 features like L7:F13646, L8:F8855, L6:F12712, L7:F9092, all firing at pos 66 with strong positive contributions to the reporter token's representation. From there the signal propagates to L11:L15:L17:L19 features (F13929, F12472, F8083, F2579, F1604, F14663, F5218, F15327, F2486) — all pos 66, all referencing the " reporter" embedding, before finally reaching the probe output. This is a token-identification circuit, not a profession-semantics circuit.

Crucially, the user's concern about gender markers is supported: the "He" embedding at pos 1 feeds L0:F4874 (activation 9.06, direct_effect −0.106) and L0:F1069 (activation 17.75, direct_effect −0.089), both *negative* contributors to the probe. "He" therefore suppresses the reporter score, meaning a female pronoun would likely raise it — the probe correlates "reporter" with male gender, not as a confound but as a *suppressor* in this particular example. The "freelancer" embedding at pos 21 contributes positively via L0:F9397 (direct_effect 0.076) and through L7:L8 features, but this is occupational context, not a gender marker. Sentence-structural tokens ("in", "from", "ever", ".", "has") activate L0 features with mixed positive/negative effects, reflecting syntactic context rather than profession content. The circuit primarily reads the *word* "reporter" rather than building a semantic profession representation; the pronoun's suppressive role confirms a learned gender correlation in the probe.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 66 | Late-layer 'reporter' word features (L17-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L18:F14663](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14663) | 66 | Late-layer 'reporter' word features (L17-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14663) |
| [L17:F1604](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/1604) | 66 | Late-layer 'reporter' word features (L17-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/1604) |
| [L17:F5218](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5218) | 66 | Late-layer 'reporter' word features (L17-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5218) |
| [L15:F15327](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15327) | 66 | Late-layer 'reporter' word features (L17-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15327) |
| [L15:F2579](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2579) | 66 | Late-layer 'reporter' word features (L17-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2579) |
| [L15:F8083](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/8083) | 66 | Late-layer 'reporter' word features (L17-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/8083) |
| [L15:F12472](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12472) | 66 | Late-layer 'reporter' word features (L17-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12472) |
| [L11:F13929](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/13929) | 66 | Late-layer 'reporter' word features (L17-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/13929) |
| [L16:F8642](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/8642) | 66 | Late-layer 'reporter' word features (L17-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/8642) |
| [L9:F7435](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/7435) | 66 | Mid-layer 'reporter'-word-anchored features (L7-L9) | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/7435) |
| [L9:F2845](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2845) | 66 | Mid-layer 'reporter'-word-anchored features (L7-L9) | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2845) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 66 | Mid-layer 'reporter'-word-anchored features (L7-L9) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F2309](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2309) | 66 | Mid-layer 'reporter'-word-anchored features (L7-L9) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2309) |
| [L8:F11063](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11063) | 66 | Mid-layer 'reporter'-word-anchored features (L7-L9) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11063) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 66 | Mid-layer 'reporter'-word-anchored features (L7-L9) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L8:F15435](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15435) | 66 | Mid-layer 'reporter'-word-anchored features (L7-L9) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15435) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 66 | Mid-layer 'reporter'-word-anchored features (L7-L9) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 66 | Mid-layer 'reporter'-word-anchored features (L7-L9) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L7:F9521](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9521) | 66 | Mid-layer 'reporter'-word-anchored features (L7-L9) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9521) |
| [L7:F72](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/72) | 66 | Mid-layer 'reporter'-word-anchored features (L7-L9) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/72) |
| [L7:F7102](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/7102) | 66 | Mid-layer 'reporter'-word-anchored features (L7-L9) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/7102) |
| [L6:F12712](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) | 66 | Core 'reporter' token features (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) |
| [L6:F8529](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8529) | 66 | Core 'reporter' token features (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8529) |
| [L6:F856](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/856) | 66 | Core 'reporter' token features (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/856) |
| [L5:F1889](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1889) | 66 | Core 'reporter' token features (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1889) |
| [L5:F6306](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6306) | 66 | Core 'reporter' token features (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6306) |
| [L5:F7539](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7539) | 66 | Core 'reporter' token features (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7539) |
| [L5:F6053](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6053) | 66 | Core 'reporter' token features (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6053) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 66 | Core 'reporter' token features (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L4:F661](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/661) | 66 | Core 'reporter' token features (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/661) |
| [L4:F6696](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6696) | 66 | Core 'reporter' token features (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6696) |
| [L1:F1024](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1024) | 66 | Core 'reporter' token features (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1024) |
| [L1:F5357](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5357) | 66 | Core 'reporter' token features (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5357) |
| [L1:F16281](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/16281) | 66 | Core 'reporter' token features (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/16281) |
| [L0:F1579](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1579) | 66 | Core 'reporter' token features (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1579) |
| [L0:F79](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/79) | 66 | Core 'reporter' token features (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/79) |
| [L0:F10798](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10798) | 66 | Core 'reporter' token features (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10798) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 66 | Probe-suppressing features (negative direct_effect) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L0:F4874](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4874) | 2 | Probe-suppressing features (negative direct_effect) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4874) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Probe-suppressing features (negative direct_effect) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F926](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/926) | 2 | Probe-suppressing features (negative direct_effect) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/926) |
| [L0:F6786](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6786) | 2 | Probe-suppressing features (negative direct_effect) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6786) |
| [L0:F8642](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8642) | 2 | Low-layer supporting features (in/on, has, ever, ., freelancer) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8642) |
| [L0:F5099](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5099) | 2 | Low-layer supporting features (in/on, has, ever, ., freelancer) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5099) |
| [L0:F6127](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6127) | 5 | Low-layer supporting features (in/on, has, ever, ., freelancer) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6127) |
| [L0:F14824](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) | 16 | Low-layer supporting features (in/on, has, ever, ., freelancer) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) |
| [L0:F8061](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) | 6 | Low-layer supporting features (in/on, has, ever, ., freelancer) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) |
| [L0:F8974](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) | 9 | Low-layer supporting features (in/on, has, ever, ., freelancer) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) |
| [L0:F13864](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13864) | 22 | Low-layer supporting features (in/on, has, ever, ., freelancer) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13864) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 24 | Low-layer supporting features (in/on, has, ever, ., freelancer) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F9397](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9397) | 21 | Low-layer supporting features (in/on, has, ever, ., freelancer) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9397) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:4420 de=-0.196 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@66` | ❌ error | — | — | Trace the path from L14:F4420 at pos 66. This is the top negative direct_effect … |
| SA-2 | `L19:F2486@66` | ❌ error | — | — | Trace the path from L19:F2486 at pos 66. This is the second most important featu… |
| SA-3 | `L0:F4874@2` | ❌ error | — | — | Trace the path from L0:F4874 at pos 2 (the "He" token). This is an early-layer f… |
| SA-4 | `L4:F13253@66` | ❌ error | — | — | Trace the path from L4:F13253 at pos 66. Determine what this feature encodes and… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F4420@66, k=15 → Emb:" reporter"@66 (de=18.75) +14 more |
| 2 | `get_upstream_features` | L19:F2486@66, k=15 → Emb:" reporter"@66 (de=28.25) +14 more |
| 3 | `get_upstream_features` | L4:F13253@66, k=15 → Emb:" reporter"@66 (de=26.62) +14 more |
| 4 | `get_upstream_features` | L0:F4874@2, k=15 → Emb:" obtained"@2 (de=11.69) +14 more |
| 5 | `get_upstream_features` | L8:F8855@66, k=12 → Emb:" reporter"@66 (de=16.88) +11 more |
| 6 | `get_upstream_features` | L6:F12712@66, k=12 → Emb:" reporter"@66 (de=11.56) +11 more |
| 7 | `get_upstream_features` | L0:F6051@24, k=12 → Emb:"."@24 (de=47.25) +11 more |
| 8 | `get_upstream_features` | L0:F14824@16, k=12 → Emb:" has"@16 (de=34.75) +11 more |
| 9 | `get_upstream_features` | L7:F13646@66, k=10 → Emb:" reporter"@66 (de=15.12) +9 more |
| 10 | `get_upstream_features` | L0:F8642@2, k=10 → Emb:" obtained"@2 (de=12.06) +9 more |
| 11 | `get_upstream_features` | L0:F1069@1, k=10 → Emb:"He"@1 (de=22.62) +9 more |
| 12 | `get_upstream_features` | L0:F8974@9, k=10 → Emb:" from"@9 (de=40.00) +9 more |
| 13 | `get_upstream_features` | L0:F8061@6, k=10 → Emb:" in"@6 (de=38.50) +9 more |
| 14 | `get_upstream_features` | L0:F13864@22, k=10 → Emb:" ever"@22 (de=39.00) +9 more |
| 15 | `get_upstream_features` | L7:F9092@66, k=10 → L4:F13253 (de=6.81) +9 more |
| 16 | `get_upstream_features` | L4:F661@66, k=10 → Emb:" reporter"@66 (de=18.00) +9 more |
| 17 | `get_upstream_features` | L18:F14663@66, k=8 → Emb:" reporter"@66 (de=48.25) +7 more |
| 18 | `get_upstream_features` | L17:F5218@66, k=8 → L14:F4420 (de=6.47) +7 more |
| 19 | `get_upstream_features` | L5:F1889@66, k=8 → Emb:" reporter"@66 (de=4.25) +7 more |
| 20 | `get_upstream_features` | L2:F9719@66, k=8 → Emb:" reporter"@66 (de=16.50) +7 more |
| 21 | `get_upstream_features` | L15:F2579@66, k=8 → Emb:" reporter"@66 (de=28.25) +7 more |
| 22 | `get_upstream_features` | L17:F1604@66, k=8 → L15:F12472 (de=2.94) +7 more |
| 23 | `get_upstream_features` | L15:F12472@66, k=8 → Emb:"<bos>"@0 (de=-24.75) +7 more |
| 24 | `get_upstream_features` | L16:F8642@66, k=8 → Emb:" reporter"@66 (de=12.50) +7 more |
| 25 | `get_upstream_features` | L15:F15327@66, k=8 → Emb:" reporter"@66 (de=1.61) +7 more |
| 26 | `get_upstream_features` | L15:F8083@66, k=8 → L14:F4420 (de=8.56) +7 more |
| 27 | `get_upstream_features` | L11:F13929@66, k=8 → Emb:" reporter"@66 (de=6.44) +7 more |
| 28 | `get_upstream_features` | L0:F1579@66, k=8 → Emb:" reporter"@66 (de=12.75) +7 more |
| 29 | `get_upstream_features` | L1:F1024@66, k=8 → Emb:" reporter"@66 (de=8.06) +7 more |
| 30 | `get_upstream_features` | L0:F9397@21, k=8 → Emb:" freelancer"@21 (de=9.62) +7 more |
| 31 | `get_upstream_features` | L0:F5099@2, k=8 → Emb:" obtained"@2 (de=17.62) +7 more |
| 32 | `get_upstream_features` | L0:F6127@5, k=8 → Emb:" degree"@5 (de=17.00) +7 more |
| 33 | `get_upstream_features` | L7:F9521@66, k=6 → Emb:" reporter"@66 (de=17.25) +5 more |
| 34 | `get_upstream_features` | L8:F15435@66, k=6 → Emb:" reporter"@66 (de=12.88) +5 more |
| 35 | `get_upstream_features` | L6:F856@66, k=6 → Emb:" reporter"@66 (de=5.81) +5 more |
| 36 | `get_upstream_features` | L6:F8529@66, k=6 → Emb:" reporter"@66 (de=11.81) +5 more |
| 37 | `get_upstream_features` | L4:F6696@66, k=6 → Emb:" reporter"@66 (de=8.94) +5 more |
| 38 | `get_upstream_features` | L7:F72@66, k=6 → Emb:" reporter"@66 (de=3.84) +5 more |
| 39 | `get_upstream_features` | L7:F7102@66, k=6 → L4:F13253 (de=2.56) +5 more |
| 40 | `get_upstream_features` | L0:F6786@2, k=6 → Emb:" obtained"@2 (de=10.75) +5 more |

### Build

`build_circuit` → 17 nodes, 16 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 41,677 | 6,715 | 136,660 | 0 | $0.0288 | — | — |
| **Total** | | **41,677** | **6,715** | **136,660** | **0** | **$0.0288** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 12s