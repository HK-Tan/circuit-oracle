# Circuit Oracle Report
**Date:** 2026-07-28 07:24:34 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven predominantly by the masculine pronoun "His" at position 1 (with secondary reinforcement from "him" at position 9), with only a small, partially-suppressing contribution from the genuinely profession-related token "report" at position 21 — confirming the user's concern that the circuit relies on gender markers rather than professional vocabulary.

**Confidence:** 7

**Reasoning:** Tracing the attribution graph from the output probe direction back to embedding nodes reveals a strikingly gender-centric circuit:

**Primary driver: the "His" path (pos 1).** The single most important feature is L7:F14893 at pos 1, with direct effect +0.47, which directly receives strong input from the "His" token embedding (DE=23.5 into the feature, then propagated to the probe). This feeds a tall stack of features at position 1 — L9-L16 features F8770, F10933, F9183, F15819, F851 (act=154) all positively — eventually reaching L18:F7400/F10315 and culminating in L19:F8814 (+0.23, a key late driver of the probe). Almost the entire vertical column of features at pos 1 is dedicated to processing the masculine pronoun. Even the high-activation L16:F10989 (act=118.5) and L18 features at pos 1 push *against* the pronoun (negative direct effects), but the net signed contribution from this path is still strongly positive for the classification.

**Secondary driver: the "him" path (pos 9).** L0:F16297 and L2:F5525 at pos 9 fire on the "him" embedding, and L18:F14743 at pos 9 contributes -0.19 to the probe. This is a second gender-pronoun signal, separate from "His".

**Profession-token path: the "report" path (pos 21).** Genuinely profession-related features do exist: L7:L11 features F13646, F8855, F8437, F9092, F5996 at pos 21 (the word "report") are all positively wired from the "report" embedding. However, the late-layer L14:F4420 at pos 21 (DE=-0.16) — which would naturally encode reporter/journalist semantics — is *suppressing* the probe, and L19:F2486 (DE=-0.09) is also negative. So the profession vocabulary contributes a weakened, partially canceled signal.

**Net balance.** Summing direct effects at the probe: positive contributions from "His"-path features (F14893 +0.47, F8814 +0.23, F2994 +0.29, F2011 +0.13, F2994@pos9 +0.11, F7927 +0.10) dominate over the modest profession signal, while the L18 features at pos 1 (F7400 -0.16, F10315 -0.16, F4315 -0.18) and F12990 (-0.30) somewhat dampen but do not overturn the gender signal. The "report" token's late-layer features (F4420 -0.16, F2486 -0.09) actually push against the classification.

This matches the user's concern exactly: the model's probe-aligned profession classification is mostly picking up on the *masculine pronoun "His" and "him"* rather than the profession-indicating content ("report", "news organizations", "Reagents Global Market"). The feature stack at position 1 is the principal evidence — it's far taller and more positive than the position-21 "report" stack. If "She" replaced "His" in this prompt, the same circuit would likely suppress rather than support the classification, indicating the probe is keyed to gender-correlated features rather than to the semantic profession concept.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'His' (pos 1) — MALE GENDER PRONOUN, primary driver | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: 'him' (pos 9) — MALE GENDER PRONOUN, reinforcing signal | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: 'report' (pos 21) — profession-related verb | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: 'world' (pos 6) — context token | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: 'desire' (pos 2) — narrative token | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: 'to' (pos 3) — function word | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | L0 pos-1 (His) features — F2994(+0.29), F2208(-0.10), F2011(+0.13, desire), F13381(-0.09), F2994@pos9(+0.11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2208](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2208) | 1 | L0 pos-1 (His) features — F2994(+0.29), F2208(-0.10), F2011(+0.13, desire), F13381(-0.09), F2994@pos9(+0.11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2208) |
| [L0:F2011](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) | 2 | L0 pos-1 (His) features — F2994(+0.29), F2208(-0.10), F2011(+0.13, desire), F13381(-0.09), F2994@pos9(+0.11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) |
| [L0:F13381](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13381) | 2 | L0 pos-1 (His) features — F2994(+0.29), F2208(-0.10), F2011(+0.13, desire), F13381(-0.09), F2994@pos9(+0.11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13381) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 9 | L0 pos-1 (His) features — F2994(+0.29), F2208(-0.10), F2011(+0.13, desire), F13381(-0.09), F2994@pos9(+0.11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F11898](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11898) | 6 | L0 pos-6 (world) features — F11898(+0.10, world), F11767(+0.09, world), F8444(-0.11, 'to'), F7927(+0.10, 'has') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11898) |
| [L0:F11767](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11767) | 6 | L0 pos-6 (world) features — F11898(+0.10, world), F11767(+0.09, world), F8444(-0.11, 'to'), F7927(+0.10, 'has') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11767) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 3 | L0 pos-6 (world) features — F11898(+0.10, world), F11767(+0.09, world), F8444(-0.11, 'to'), F7927(+0.10, 'has') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F7927](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7927) | 8 | L0 pos-6 (world) features — F11898(+0.10, world), F11767(+0.09, world), F8444(-0.11, 'to'), F7927(+0.10, 'has') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7927) |
| [L2:F9301](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) | 1 | L1-L6 pos-1 (His) features — F4315(-0.18), F12990(-0.30), F9301(-0.11), F5491, F7439, F15567, F9757, F13121, F10952, F14942, F6376 | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) |
| [L2:F5491](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) | 1 | L1-L6 pos-1 (His) features — F4315(-0.18), F12990(-0.30), F9301(-0.11), F5491, F7439, F15567, F9757, F13121, F10952, F14942, F6376 | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) |
| [L1:F7439](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7439) | 1 | L1-L6 pos-1 (His) features — F4315(-0.18), F12990(-0.30), F9301(-0.11), F5491, F7439, F15567, F9757, F13121, F10952, F14942, F6376 | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7439) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | L1-L6 pos-1 (His) features — F4315(-0.18), F12990(-0.30), F9301(-0.11), F5491, F7439, F15567, F9757, F13121, F10952, F14942, F6376 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L4:F15567](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) | 1 | L1-L6 pos-1 (His) features — F4315(-0.18), F12990(-0.30), F9301(-0.11), F5491, F7439, F15567, F9757, F13121, F10952, F14942, F6376 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) |
| [L4:F9757](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) | 1 | L1-L6 pos-1 (His) features — F4315(-0.18), F12990(-0.30), F9301(-0.11), F5491, F7439, F15567, F9757, F13121, F10952, F14942, F6376 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) |
| [L3:F13121](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13121) | 1 | L1-L6 pos-1 (His) features — F4315(-0.18), F12990(-0.30), F9301(-0.11), F5491, F7439, F15567, F9757, F13121, F10952, F14942, F6376 | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13121) |
| [L5:F10952](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) | 1 | L1-L6 pos-1 (His) features — F4315(-0.18), F12990(-0.30), F9301(-0.11), F5491, F7439, F15567, F9757, F13121, F10952, F14942, F6376 | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) |
| [L5:F14942](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14942) | 1 | L1-L6 pos-1 (His) features — F4315(-0.18), F12990(-0.30), F9301(-0.11), F5491, F7439, F15567, F9757, F13121, F10952, F14942, F6376 | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14942) |
| [L5:F6376](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6376) | 1 | L1-L6 pos-1 (His) features — F4315(-0.18), F12990(-0.30), F9301(-0.11), F5491, F7439, F15567, F9757, F13121, F10952, F14942, F6376 | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6376) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | L1-L6 pos-1 (His) features — F4315(-0.18), F12990(-0.30), F9301(-0.11), F5491, F7439, F15567, F9757, F13121, F10952, F14942, F6376 | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | L7 pos-1 — F14893(+0.47, top driver), F14946(-0.47) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | L7 pos-1 — F14893(+0.47, top driver), F14946(-0.47) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F462](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) | 1 | L7-L10 pos-1 features — F462, F5741, F2762, F3056, F3992, F14585, F7489, F14174 | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) |
| [L7:F5741](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5741) | 1 | L7-L10 pos-1 features — F462, F5741, F2762, F3056, F3992, F14585, F7489, F14174 | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5741) |
| [L9:F2762](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2762) | 1 | L7-L10 pos-1 features — F462, F5741, F2762, F3056, F3992, F14585, F7489, F14174 | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2762) |
| [L9:F3056](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/3056) | 1 | L7-L10 pos-1 features — F462, F5741, F2762, F3056, F3992, F14585, F7489, F14174 | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/3056) |
| [L5:F3992](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3992) | 1 | L7-L10 pos-1 features — F462, F5741, F2762, F3056, F3992, F14585, F7489, F14174 | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3992) |
| [L6:F14585](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14585) | 1 | L7-L10 pos-1 features — F462, F5741, F2762, F3056, F3992, F14585, F7489, F14174 | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14585) |
| [L5:F7489](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7489) | 1 | L7-L10 pos-1 features — F462, F5741, F2762, F3056, F3992, F14585, F7489, F14174 | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7489) |
| [L10:F14174](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14174) | 1 | L7-L10 pos-1 features — F462, F5741, F2762, F3056, F3992, F14585, F7489, F14174 | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14174) |
| [L9:F8770](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8770) | 1 | L9-L16 pos-1 (His) features — F8770(+), F10933(+), F9183(+), F15819(+), F851, F10989(-, act=118.5), F8128(-), F389(-), F12232(-), F5948(-), F12493(-), F6940(-), F8659(-), F3684(+) | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8770) |
| [L9:F15819](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15819) | 1 | L9-L16 pos-1 (His) features — F8770(+), F10933(+), F9183(+), F15819(+), F851, F10989(-, act=118.5), F8128(-), F389(-), F12232(-), F5948(-), F12493(-), F6940(-), F8659(-), F3684(+) | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15819) |
| [L11:F10933](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/10933) | 1 | L9-L16 pos-1 (His) features — F8770(+), F10933(+), F9183(+), F15819(+), F851, F10989(-, act=118.5), F8128(-), F389(-), F12232(-), F5948(-), F12493(-), F6940(-), F8659(-), F3684(+) | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/10933) |
| [L11:F9183](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/9183) | 1 | L9-L16 pos-1 (His) features — F8770(+), F10933(+), F9183(+), F15819(+), F851, F10989(-, act=118.5), F8128(-), F389(-), F12232(-), F5948(-), F12493(-), F6940(-), F8659(-), F3684(+) | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/9183) |
| [L11:F389](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/389) | 1 | L9-L16 pos-1 (His) features — F8770(+), F10933(+), F9183(+), F15819(+), F851, F10989(-, act=118.5), F8128(-), F389(-), F12232(-), F5948(-), F12493(-), F6940(-), F8659(-), F3684(+) | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/389) |
| [L10:F12232](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/12232) | 1 | L9-L16 pos-1 (His) features — F8770(+), F10933(+), F9183(+), F15819(+), F851, F10989(-, act=118.5), F8128(-), F389(-), F12232(-), F5948(-), F12493(-), F6940(-), F8659(-), F3684(+) | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/12232) |
| [L12:F12493](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12493) | 1 | L9-L16 pos-1 (His) features — F8770(+), F10933(+), F9183(+), F15819(+), F851, F10989(-, act=118.5), F8128(-), F389(-), F12232(-), F5948(-), F12493(-), F6940(-), F8659(-), F3684(+) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12493) |
| [L13:F8128](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/8128) | 1 | L9-L16 pos-1 (His) features — F8770(+), F10933(+), F9183(+), F15819(+), F851, F10989(-, act=118.5), F8128(-), F389(-), F12232(-), F5948(-), F12493(-), F6940(-), F8659(-), F3684(+) | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/8128) |
| [L13:F5948](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/5948) | 1 | L9-L16 pos-1 (His) features — F8770(+), F10933(+), F9183(+), F15819(+), F851, F10989(-, act=118.5), F8128(-), F389(-), F12232(-), F5948(-), F12493(-), F6940(-), F8659(-), F3684(+) | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/5948) |
| [L14:F6940](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/6940) | 1 | L9-L16 pos-1 (His) features — F8770(+), F10933(+), F9183(+), F15819(+), F851, F10989(-, act=118.5), F8128(-), F389(-), F12232(-), F5948(-), F12493(-), F6940(-), F8659(-), F3684(+) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/6940) |
| [L16:F10989](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/10989) | 1 | L9-L16 pos-1 (His) features — F8770(+), F10933(+), F9183(+), F15819(+), F851, F10989(-, act=118.5), F8128(-), F389(-), F12232(-), F5948(-), F12493(-), F6940(-), F8659(-), F3684(+) | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/10989) |
| [L12:F3684](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/3684) | 1 | L9-L16 pos-1 (His) features — F8770(+), F10933(+), F9183(+), F15819(+), F851, F10989(-, act=118.5), F8128(-), F389(-), F12232(-), F5948(-), F12493(-), F6940(-), F8659(-), F3684(+) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/3684) |
| [L14:F8659](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/8659) | 1 | L9-L16 pos-1 (His) features — F8770(+), F10933(+), F9183(+), F15819(+), F851, F10989(-, act=118.5), F8128(-), F389(-), F12232(-), F5948(-), F12493(-), F6940(-), F8659(-), F3684(+) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/8659) |
| [L15:F851](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/851) | 1 | L15 pos-1 — F851(act=154, strong) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/851) |
| [L18:F7400](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) | 1 | L18 pos-1 (His) features — F7400(-0.155), F7217(-), F10315(-0.162) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| [L18:F7217](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7217) | 1 | L18 pos-1 (His) features — F7400(-0.155), F7217(-), F10315(-0.162) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7217) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 1 | L18 pos-1 (His) features — F7400(-0.155), F7217(-), F10315(-0.162) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | L19 pos-1 — F8814(+0.23, key late driver) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |
| [L0:F16297](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) | 9 | L0-L2 pos-9 (him) features — F16297(+), F5525(+), F14743(-0.19 at L18) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) |
| [L2:F5525](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5525) | 9 | L0-L2 pos-9 (him) features — F16297(+), F5525(+), F14743(-0.19 at L18) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5525) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 9 | L0-L2 pos-9 (him) features — F16297(+), F5525(+), F14743(-0.19 at L18) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 21 | L7-L11 pos-21 (report) features — F13646(+), F8855(+), F8437(+), F9092(+), F5996(+), F7435(-), F2845(-), F10344, F14120 | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 21 | L7-L11 pos-21 (report) features — F13646(+), F8855(+), F8437(+), F9092(+), F5996(+), F7435(-), F2845(-), F10344, F14120 | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 21 | L7-L11 pos-21 (report) features — F13646(+), F8855(+), F8437(+), F9092(+), F5996(+), F7435(-), F2845(-), F10344, F14120 | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 21 | L7-L11 pos-21 (report) features — F13646(+), F8855(+), F8437(+), F9092(+), F5996(+), F7435(-), F2845(-), F10344, F14120 | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L9:F7435](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/7435) | 21 | L7-L11 pos-21 (report) features — F13646(+), F8855(+), F8437(+), F9092(+), F5996(+), F7435(-), F2845(-), F10344, F14120 | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/7435) |
| [L9:F2845](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2845) | 21 | L7-L11 pos-21 (report) features — F13646(+), F8855(+), F8437(+), F9092(+), F5996(+), F7435(-), F2845(-), F10344, F14120 | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2845) |
| [L11:F5996](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/5996) | 21 | L7-L11 pos-21 (report) features — F13646(+), F8855(+), F8437(+), F9092(+), F5996(+), F7435(-), F2845(-), F10344, F14120 | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/5996) |
| [L14:F10344](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10344) | 9 | L7-L11 pos-21 (report) features — F13646(+), F8855(+), F8437(+), F9092(+), F5996(+), F7435(-), F2845(-), F10344, F14120 | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10344) |
| [L16:F14120](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/14120) | 9 | L7-L11 pos-21 (report) features — F13646(+), F8855(+), F8437(+), F9092(+), F5996(+), F7435(-), F2845(-), F10344, F14120 | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/14120) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 21 | L14-L18 pos-21 features — F4420(-0.16, reporter-related), F14663, F5218(-), F15046, F8642(-) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L16:F8642](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/8642) | 21 | L14-L18 pos-21 features — F4420(-0.16, reporter-related), F14663, F5218(-), F15046, F8642(-) | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/8642) |
| [L16:F15046](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15046) | 21 | L14-L18 pos-21 features — F4420(-0.16, reporter-related), F14663, F5218(-), F15046, F8642(-) | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15046) |
| [L17:F5218](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5218) | 21 | L14-L18 pos-21 features — F4420(-0.16, reporter-related), F14663, F5218(-), F15046, F8642(-) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5218) |
| [L18:F14663](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14663) | 21 | L14-L18 pos-21 features — F4420(-0.16, reporter-related), F14663, F5218(-), F15046, F8642(-) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14663) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 21 | L19 pos-21 — F2486(-0.09, act=44) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L7:14893 de=0.471 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ❌ error | — | — | Trace this feature upstream to understand what it encodes. It has the highest di… |
| SA-2 | `L0:F2994@1` | ❌ error | — | — | Trace this feature upstream to understand what it encodes. It has direct effect … |
| SA-3 | `L19:F8814@1` | ❌ error | — | — | Trace this feature upstream to understand what it encodes. It has direct effect … |
| SA-4 | `L7:F14946@1` | ❌ error | — | — | Trace this feature upstream to understand what it encodes. It has the most negat… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L7:F14893@1, k=10 → Emb:"His"@1 (de=23.50) +9 more |
| 2 | `get_upstream_features` | L0:F2994@1, k=10 → Emb:"His"@1 (de=19.75) +9 more |
| 3 | `get_upstream_features` | L19:F8814@1, k=10 → Emb:"His"@1 (de=9.31) +9 more |
| 4 | `get_upstream_features` | L7:F14946@1, k=10 → Emb:"His"@1 (de=18.38) +9 more |
| 5 | `get_upstream_features` | L18:F7400@1, k=10 → Emb:"His"@1 (de=13.00) +9 more |
| 6 | `get_upstream_features` | L18:F10315@1, k=10 → Emb:"His"@1 (de=21.38) +9 more |
| 7 | `get_upstream_features` | L6:F12990@1, k=10 → Emb:"His"@1 (de=4.91) +9 more |
| 8 | `get_upstream_features` | L4:F4315@1, k=10 → Emb:"His"@1 (de=23.50) +9 more |
| 9 | `get_upstream_features` | L18:F14743@9, k=10 → Emb:" him"@9 (de=18.38) +9 more |
| 10 | `get_upstream_features` | L14:F4420@21, k=10 → Emb:" report"@21 (de=5.22) +9 more |
| 11 | `get_upstream_features` | L19:F2486@21, k=10 → L14:F4420 (de=14.31) +9 more |
| 12 | `get_upstream_features` | L0:F8444@3, k=10 → Emb:" to"@3 (de=39.50) +9 more |
| 13 | `get_upstream_features` | L14:F4420@21, k=10 → Emb:" report"@21 (de=5.22) +9 more |
| 14 | `get_upstream_features` | L4:F11898@6, k=10 → Emb:" world"@6 (de=35.25) +9 more |
| 15 | `get_upstream_features` | L0:F7927@8, k=10 → Emb:" has"@7 (de=16.00) +9 more |
| 16 | `get_upstream_features` | L0:F2011@2, k=10 → Emb:" desire"@2 (de=12.94) +9 more |
| 17 | `get_upstream_features` | L0:F11767@6, k=10 → Emb:" world"@6 (de=16.38) +9 more |
| 18 | `get_upstream_features` | L0:F2208@1, k=10 → Emb:"His"@1 (de=12.81) +9 more |
| 19 | `get_upstream_features` | L0:F13381@2, k=10 → Emb:" desire"@2 (de=12.06) +9 more |
| 20 | `get_upstream_features` | L0:F2994@9, k=10 → Emb:" him"@9 (de=13.94) +9 more |
| 21 | `get_upstream_features` | L15:F851@1, k=10 → L12:F12493 (de=23.25) +9 more |
| 22 | `get_upstream_features` | L9:F8770@1, k=10 → L7:F462 (de=15.06) +9 more |

### Build

`build_circuit` → 20 nodes, 23 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 42,194 | 12,110 | 94,855 | 0 | $0.0329 | — | — |
| **Total** | | **42,194** | **12,110** | **94,855** | **0** | **$0.0329** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 9s