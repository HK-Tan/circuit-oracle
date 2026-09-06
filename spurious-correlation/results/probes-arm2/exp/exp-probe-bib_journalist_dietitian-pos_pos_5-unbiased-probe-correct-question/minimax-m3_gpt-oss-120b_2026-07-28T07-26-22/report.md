# Circuit Oracle Report
**Date:** 2026-07-28 07:26:22 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of "dietician/nutritionist" is driven primarily by genuine profession-indicating content tokens ("nutrition", "sports", "Dietetics", "Academy of Nutrition", "spokesperson") flowing through a clean 19-layer concept-formation chain, while the "Her" pronoun at pos 1 contributes only through shallow, low-magnitude L0 features that compete with negative inhibitors.

**Confidence:** 8

**Reasoning:** I traced the top output-driving features from L19:F1589 (pos 7/26) back through L17:L18:L16 → L14:F4197/F16195 ("dietician" profession concept) → L8:L7 abstract nutrition-expertise features → L5:L6 mid-layer dietitian features → L3:L4 early conceptual "nutrition" features (e.g., L4:F10494 de=0.176, L4:F13412) → L1:L2 compound features → L0 token-level features → embedding nodes. The dominant positive signal at every layer is driven by the input tokens "nutrition" (pos 7, de ~11-32 at each hop), "sports" (pos 6, de ~3-9), and "Die/tetics"/"Nutrition" (pos 25-26, 23, de up to 22). These converge into profession-evidence features (L14:L18) that culminate in L19:F1589 (a "dietician" output concept) with activations of 42-55 and direct effects of 0.066-0.069 on the probe.

Regarding the user's concern about spurious gender markers: "Her" at pos 1 does appear in the L0 supernode (L0:F9519, F10148, F2208, F2107, F34, F2189, F2107), and the circuit contains edges from emb_her → l0_her_gender → output_logit, BUT this connection is only because these L0 features (operating on the residual stream at the "Her" position) have residual direct effects on the probe — they are not part of the deep profession-evidence chain. Critically, L0:F6051 (pos 14, "de=-0.091"), L0:F8975 (pos 4, "de=-0.089"), L0:F2268 (pos 18, "de=-0.081"), L0:F8028 (pos 2, "de=-0.074"), and L0:F15322 (pos 4, "de=-0.074") are all NEGATIVE direct-effect inhibitors — the L0 "Her"/pronoun-related features do not show up as strongly positive drivers of the probe. The L14:F16195 upstream even shows L0:F5201 and L0:F2267 as negative contributors. The genuinely positive, large-magnitude path flows through content tokens (nutrition, sports, Dietetics, Academy of Nutrition, spokesperson) and produces a coherent "dietician/nutrition professional" concept, not a gender prediction. The user's concern is largely not supported: the circuit is dominated by legitimate profession content, with gender/pronoun signals appearing as a thin, low-magnitude, partially inhibitory side-channel rather than the primary mechanism.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: nutrition (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: sports (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Her (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: expertise (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 25 | Emb: Die/tetics + Nutrition (pos 25-26, 23) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 26 | Emb: Die/tetics + Nutrition (pos 25-26, 23) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 23 | Emb: Die/tetics + Nutrition (pos 25-26, 23) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 18 | Emb: spokesperson (pos 18) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: Academy / Nutrition (pos 21, 23) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 1 | L0: Her-token features (gender/female pronoun) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L0:F10148](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10148) | 1 | L0: Her-token features (gender/female pronoun) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10148) |
| [L0:F2208](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2208) | 1 | L0: Her-token features (gender/female pronoun) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2208) |
| [L0:F2189](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2189) | 0 | L0: Her-token features (gender/female pronoun) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2189) |
| [L0:F2107](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2107) | 1 | L0: Her-token features (gender/female pronoun) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2107) |
| [L0:F34](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/34) | 1 | L0: Her-token features (gender/female pronoun) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/34) |
| [L0:F5201](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5201) | 7 | L0: nutrition-token features (food/health field) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5201) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 7 | L0: nutrition-token features (food/health field) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F7843](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7843) | 7 | L0: nutrition-token features (food/health field) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7843) |
| [L0:F11835](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11835) | 7 | L0: nutrition-token features (food/health field) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11835) |
| [L0:F10146](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10146) | 7 | L0: nutrition-token features (food/health field) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10146) |
| [L0:F10254](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10254) | 6 | L0: sports-token features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10254) |
| [L0:F1654](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1654) | 6 | L0: sports-token features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1654) |
| [L0:F14240](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14240) | 6 | L0: sports-token features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14240) |
| [L0:F14538](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14538) | 7 | L0: sports-token features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14538) |
| [L0:F8975](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8975) | 4 | L0: expertise-token features (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8975) |
| [L0:F15322](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15322) | 4 | L0: expertise-token features (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15322) |
| [L0:F4030](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4030) | 4 | L0: expertise-token features (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4030) |
| [L0:F2083](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2083) | 4 | L0: expertise-token features (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2083) |
| [L0:F8153](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8153) | 26 | L0-1: Dietetics / Academy of Nutrition features (pos 23-26) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8153) |
| [L0:F7670](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7670) | 26 | L0-1: Dietetics / Academy of Nutrition features (pos 23-26) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7670) |
| [L0:F1083](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1083) | 26 | L0-1: Dietetics / Academy of Nutrition features (pos 23-26) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1083) |
| [L0:F2745](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2745) | 26 | L0-1: Dietetics / Academy of Nutrition features (pos 23-26) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2745) |
| [L1:F5251](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5251) | 26 | L0-1: Dietetics / Academy of Nutrition features (pos 23-26) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5251) |
| [L1:F11764](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11764) | 25 | L0-1: Dietetics / Academy of Nutrition features (pos 23-26) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11764) |
| [L1:F6631](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6631) | 25 | L0-1: Dietetics / Academy of Nutrition features (pos 23-26) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6631) |
| [L0:F4058](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4058) | 25 | L0-1: Dietetics / Academy of Nutrition features (pos 23-26) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4058) |
| [L0:F6129](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6129) | 25 | L0-1: Dietetics / Academy of Nutrition features (pos 23-26) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6129) |
| [L0:F14068](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14068) | 26 | L0-1: Dietetics / Academy of Nutrition features (pos 23-26) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14068) |
| [L0:F2420](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2420) | 25 | L0-1: Dietetics / Academy of Nutrition features (pos 23-26) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2420) |
| [L0:F2115](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2115) | 25 | L0-1: Dietetics / Academy of Nutrition features (pos 23-26) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2115) |
| [L0:F7843](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7843) | 23 | L0-1: Dietetics / Academy of Nutrition features (pos 23-26) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7843) |
| [L0:F5201](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5201) | 23 | L0-1: Dietetics / Academy of Nutrition features (pos 23-26) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5201) |
| [L0:F2268](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2268) | 18 | L0: spokesperson (pos 18) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2268) |
| [L1:F6461](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6461) | 7 | L1-2: 'sports nutrition' compound / food+activity features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6461) |
| [L1:F14581](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14581) | 7 | L1-2: 'sports nutrition' compound / food+activity features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14581) |
| [L1:F165](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/165) | 7 | L1-2: 'sports nutrition' compound / food+activity features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/165) |
| [L1:F6895](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6895) | 7 | L1-2: 'sports nutrition' compound / food+activity features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6895) |
| [L1:F15310](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15310) | 7 | L1-2: 'sports nutrition' compound / food+activity features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15310) |
| [L1:F6631](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6631) | 7 | L1-2: 'sports nutrition' compound / food+activity features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6631) |
| [L1:F2245](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2245) | 7 | L1-2: 'sports nutrition' compound / food+activity features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2245) |
| [L1:F10958](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10958) | 7 | L1-2: 'sports nutrition' compound / food+activity features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10958) |
| [L1:F5055](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5055) | 6 | L1-2: 'sports nutrition' compound / food+activity features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5055) |
| [L1:F808](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/808) | 6 | L1-2: 'sports nutrition' compound / food+activity features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/808) |
| [L1:F9131](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9131) | 6 | L1-2: 'sports nutrition' compound / food+activity features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9131) |
| [L1:F12000](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12000) | 6 | L1-2: 'sports nutrition' compound / food+activity features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12000) |
| [L2:F9995](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9995) | 7 | L1-2: 'sports nutrition' compound / food+activity features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9995) |
| [L2:F15770](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15770) | 7 | L1-2: 'sports nutrition' compound / food+activity features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15770) |
| [L2:F2589](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) | 7 | L1-2: 'sports nutrition' compound / food+activity features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) |
| [L2:F14533](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14533) | 6 | L1-2: 'sports nutrition' compound / food+activity features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14533) |
| [L2:F7473](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7473) | 26 | L1-2: 'sports nutrition' compound / food+activity features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7473) |
| [L2:F46](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/46) | 6 | L1-2: 'sports nutrition' compound / food+activity features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/46) |
| [L3:F6920](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6920) | 7 | L3-4: 'nutrition' conceptual features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6920) |
| [L3:F3205](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3205) | 7 | L3-4: 'nutrition' conceptual features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3205) |
| [L3:F2694](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2694) | 7 | L3-4: 'nutrition' conceptual features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2694) |
| [L3:F14480](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14480) | 6 | L3-4: 'nutrition' conceptual features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14480) |
| [L3:F11774](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11774) | 26 | L3-4: 'nutrition' conceptual features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11774) |
| [L3:F10028](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10028) | 26 | L3-4: 'nutrition' conceptual features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10028) |
| [L4:F10494](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) | 7 | L3-4: 'nutrition' conceptual features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 7 | L3-4: 'nutrition' conceptual features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 13 | L3-4: 'nutrition' conceptual features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 26 | L3-4: 'nutrition' conceptual features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 7 | L3-4: 'nutrition' conceptual features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 26 | L3-4: 'nutrition' conceptual features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 26 | L3-4: 'nutrition' conceptual features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L4:F14857](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14857) | 7 | L3-4: 'nutrition' conceptual features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14857) |
| [L5:F9121](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9121) | 7 | L5-6: mid-layer nutrition/dietitian features (pos 7 & 26) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9121) |
| [L5:F9121](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9121) | 26 | L5-6: mid-layer nutrition/dietitian features (pos 7 & 26) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9121) |
| [L5:F10462](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10462) | 7 | L5-6: mid-layer nutrition/dietitian features (pos 7 & 26) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10462) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 7 | L5-6: mid-layer nutrition/dietitian features (pos 7 & 26) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 26 | L5-6: mid-layer nutrition/dietitian features (pos 7 & 26) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 25 | L5-6: mid-layer nutrition/dietitian features (pos 7 & 26) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F12967](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12967) | 7 | L5-6: mid-layer nutrition/dietitian features (pos 7 & 26) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12967) |
| [L6:F10585](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10585) | 6 | L5-6: mid-layer nutrition/dietitian features (pos 7 & 26) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10585) |
| [L6:F10585](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10585) | 7 | L5-6: mid-layer nutrition/dietitian features (pos 7 & 26) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10585) |
| [L6:F2267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2267) | 7 | L5-6: mid-layer nutrition/dietitian features (pos 7 & 26) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2267) |
| [L6:F8614](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8614) | 7 | L5-6: mid-layer nutrition/dietitian features (pos 7 & 26) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8614) |
| [L7:F11540](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/11540) | 7 | L7-9: abstract nutrition-expertise / dietician features | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/11540) |
| [L7:F13562](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13562) | 7 | L7-9: abstract nutrition-expertise / dietician features | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13562) |
| [L7:F6277](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/6277) | 7 | L7-9: abstract nutrition-expertise / dietician features | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/6277) |
| [L7:F10463](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/10463) | 26 | L7-9: abstract nutrition-expertise / dietician features | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/10463) |
| [L7:F3217](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3217) | 26 | L7-9: abstract nutrition-expertise / dietician features | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3217) |
| [L7:F1107](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1107) | 26 | L7-9: abstract nutrition-expertise / dietician features | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1107) |
| [L8:F7057](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7057) | 7 | L7-9: abstract nutrition-expertise / dietician features | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7057) |
| [L8:F14230](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/14230) | 7 | L7-9: abstract nutrition-expertise / dietician features | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/14230) |
| [L8:F10253](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/10253) | 26 | L7-9: abstract nutrition-expertise / dietician features | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/10253) |
| [L9:F15926](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15926) | 7 | L7-9: abstract nutrition-expertise / dietician features | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15926) |
| [L9:F7732](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/7732) | 7 | L7-9: abstract nutrition-expertise / dietician features | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/7732) |
| [L10:F14691](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14691) | 7 | L10-11: topic/context integration | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14691) |
| [L11:F15272](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/15272) | 7 | L10-11: topic/context integration | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/15272) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 7 | L14: 'dietician' / nutrition profession concept | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 26 | L14: 'dietician' / nutrition profession concept | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F16195](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/16195) | 7 | L14: 'dietician' / nutrition profession concept | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/16195) |
| [L15:F12472](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12472) | 7 | L14: 'dietician' / nutrition profession concept | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12472) |
| [L16:F12752](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12752) | 7 | L16-18: dietician abstract / profession-evidence features | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12752) |
| [L16:F2393](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/2393) | 26 | L16-18: dietician abstract / profession-evidence features | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/2393) |
| [L17:F14680](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/14680) | 7 | L16-18: dietician abstract / profession-evidence features | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/14680) |
| [L17:F7545](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) | 26 | L16-18: dietician abstract / profession-evidence features | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) |
| [L18:F6105](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) | 7 | L16-18: dietician abstract / profession-evidence features | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 7 | L19: 'dietician' output concept at nutrition & Dietetics positions | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 26 | L19: 'dietician' output concept at nutrition & Dietetics positions | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:10494 de=0.176 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F10494@7` | ❌ error | — | — | Trace L4:F10494 at position 7. What does this feature encode? What input tokens/… |
| SA-2 | `L14:F4197@7` | ❌ error | — | — | Trace L14:F4197 at position 7. What does this feature encode? What input tokens/… |
| SA-3 | `L14:F16195@7` | ❌ error | — | — | Trace L14:F16195 at position 7. What does this feature encode? What input tokens… |
| SA-4 | `L6:F11327@7` | ❌ error | — | — | Trace L6:F11327 at position 7. What does this feature encode? What input tokens/… |
| SA-5 | `L19:F1589@7` | ❌ error | — | — | Trace L19:F1589 at position 7. What does this feature encode? What input tokens/… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F10494@7, k=10 → Emb:" nutrition"@7 (de=11.25) +9 more |
| 2 | `get_upstream_features` | L4:F13412@7, k=10 → Emb:" nutrition"@7 (de=12.62) +9 more |
| 3 | `get_upstream_features` | L14:F4197@7, k=10 → Emb:" nutrition"@7 (de=12.88) +9 more |
| 4 | `get_upstream_features` | L6:F11327@7, k=10 → Emb:" nutrition"@7 (de=17.50) +9 more |
| 5 | `get_upstream_features` | L14:F16195@7, k=10 → Emb:" nutrition"@7 (de=7.97) +9 more |
| 6 | `get_upstream_features` | L19:F1589@7, k=10 → Emb:" nutrition"@7 (de=32.25) +9 more |
| 7 | `get_upstream_features` | L19:F1589@26, k=10 → L17:F7545 (de=10.38) +9 more |
| 8 | `get_upstream_features` | L8:F7057@7, k=10 → Emb:" nutrition"@7 (de=8.88) +9 more |
| 9 | `get_upstream_features` | L19:F1589@7, k=10 → Emb:" nutrition"@7 (de=32.25) +9 more |
| 10 | `get_upstream_features` | L7:F13562@7, k=10 → Emb:" nutrition"@7 (de=8.12) +9 more |
| 11 | `get_upstream_features` | L7:F11540@7, k=10 → Emb:" nutrition"@7 (de=15.88) +9 more |
| 12 | `get_upstream_features` | L0:F6051@14, k=10 → Emb:"."@14 (de=47.00) +9 more |
| 13 | `get_upstream_features` | L0:F8975@4, k=10 → Emb:" expertise"@4 (de=20.88) +9 more |
| 14 | `get_upstream_features` | L0:F9519@1, k=10 → Emb:"Her"@1 (de=16.75) +9 more |
| 15 | `get_upstream_features` | L0:F10148@1, k=10 → Emb:"Her"@1 (de=10.06) +9 more |
| 16 | `get_upstream_features` | L0:F2268@18, k=8 → Emb:" spokesperson"@18 (de=23.50) +7 more |
| 17 | `get_upstream_features` | L0:F15322@4, k=8 → Emb:" expertise"@4 (de=14.81) +7 more |
| 18 | `get_upstream_features` | L0:F4030@4, k=8 → Emb:" expertise"@4 (de=7.53) +7 more |
| 19 | `get_upstream_features` | L0:F2083@4, k=8 → Emb:" expertise"@4 (de=11.88) +7 more |
| 20 | `get_upstream_features` | L0:F10254@6, k=8 → Emb:" sports"@6 (de=25.50) +7 more |
| 21 | `get_upstream_features` | L17:F14680@7, k=8 → Emb:" nutrition"@7 (de=27.88) +7 more |
| 22 | `get_upstream_features` | L18:F6105@7, k=8 → Emb:" nutrition"@7 (de=31.88) +7 more |
| 23 | `get_upstream_features` | L17:F7545@26, k=8 → L4:F13412 (de=5.28) +7 more |
| 24 | `get_upstream_features` | L16:F12752@7, k=8 → Emb:" nutrition"@7 (de=8.50) +7 more |
| 25 | `get_upstream_features` | L9:F15926@7, k=8 → Emb:" nutrition"@7 (de=8.06) +7 more |
| 26 | `get_upstream_features` | L6:F10585@6, k=8 → Emb:" sports"@6 (de=29.62) +7 more |
| 27 | `get_upstream_features` | L1:F6461@7, k=8 → Emb:" sports"@6 (de=9.19) +7 more |
| 28 | `get_upstream_features` | L4:F9554@7, k=8 → Emb:" nutrition"@7 (de=14.88) +7 more |
| 29 | `get_upstream_features` | L0:F5201@7, k=8 → Emb:" nutrition"@7 (de=27.12) +7 more |
| 30 | `get_upstream_features` | L3:F6920@7, k=8 → Emb:" nutrition"@7 (de=10.19) +7 more |
| 31 | `get_upstream_features` | L4:F11037@26, k=8 → L3:F11774 (de=2.61) +7 more |
| 32 | `get_upstream_features` | L15:F12472@7, k=8 → Emb:" sports"@6 (de=7.88) +7 more |
| 33 | `get_upstream_features` | L3:F11774@26, k=8 → Emb:" Die"@25 (de=5.53) +7 more |
| 34 | `get_upstream_features` | L1:F165@7, k=8 → Emb:" sports"@6 (de=8.44) +7 more |
| 35 | `get_upstream_features` | L0:F9026@7, k=8 → Emb:" nutrition"@7 (de=22.75) +7 more |
| 36 | `get_upstream_features` | L16:F2393@26, k=8 → L6:F11327 (de=7.31) +7 more |
| 37 | `get_upstream_features` | L6:F11327@26, k=8 → L4:F13412 (de=6.69) +7 more |
| 38 | `get_upstream_features` | L4:F13412@26, k=8 → L3:F11774 (de=4.72) +7 more |
| 39 | `get_upstream_features` | L6:F2267@7, k=8 → Emb:"<bos>"@0 (de=-3.64) +7 more |
| 40 | `get_upstream_features` | L6:F12967@7, k=8 → Emb:" nutrition"@7 (de=7.75) +7 more |
| 41 | `get_upstream_features` | L3:F10028@26, k=8 → Emb:" Die"@25 (de=7.12) +7 more |
| 42 | `get_upstream_features` | L1:F11764@25, k=8 → Emb:" Nutrition"@23 (de=7.75) +7 more |
| 43 | `get_upstream_features` | L1:F1083@26, k=8 → Emb:"te"@26 (de=22.25) +7 more |
| 44 | `get_upstream_features` | L2:F7473@26, k=8 → Emb:" Die"@25 (de=17.50) +7 more |
| 45 | `get_upstream_features` | L0:F2189@1, k=8 → Emb:"<bos>"@0 (de=5.25) +7 more |
| 46 | `get_upstream_features` | L0:F2208@1, k=8 → Emb:"Her"@1 (de=10.62) +7 more |
| 47 | `get_upstream_features` | L1:F6895@7, k=8 → Emb:" nutrition"@7 (de=13.38) +7 more |
| 48 | `get_upstream_features` | L0:F7843@7, k=8 → Emb:" nutrition"@7 (de=22.00) +7 more |
| 49 | `get_upstream_features` | L0:F11835@7, k=8 → Emb:" nutrition"@7 (de=4.34) +7 more |
| 50 | `get_upstream_features` | L11:F15272@7, k=8 → Emb:" expertise"@4 (de=1.98) +7 more |
| 51 | `get_upstream_features` | L1:F14581@7, k=8 → Emb:" sports"@6 (de=8.31) +7 more |
| 52 | `get_upstream_features` | L1:F5055@6, k=8 → Emb:" sports"@6 (de=14.81) +7 more |
| 53 | `get_upstream_features` | L3:F14480@6, k=8 → Emb:" sports"@6 (de=24.62) +7 more |
| 54 | `get_upstream_features` | L0:F1654@6, k=8 → Emb:" sports"@6 (de=19.62) +7 more |
| 55 | `get_upstream_features` | L3:F3205@7, k=8 → L0:F5201 (de=-3.62) +7 more |
| 56 | `get_upstream_features` | L2:F14533@6, k=8 → Emb:" sports"@6 (de=26.62) +7 more |
| 57 | `get_upstream_features` | L10:F14691@7, k=8 → Emb:"Her"@1 (de=2.66) +7 more |
| 58 | `get_upstream_features` | L7:F6277@7, k=8 → Emb:" nutrition"@7 (de=5.47) +7 more |
| 59 | `get_upstream_features` | L5:F9121@7, k=8 → Emb:" nutrition"@7 (de=5.72) +7 more |
| 60 | `get_upstream_features` | L2:F15770@7, k=8 → Emb:" nutrition"@7 (de=8.44) +7 more |
| 61 | `get_upstream_features` | L5:F9121@26, k=8 → L4:F9554 (de=1.48) +7 more |
| 62 | `get_upstream_features` | L2:F2589@7, k=8 → Emb:" nutrition"@7 (de=4.50) +7 more |
| 63 | `get_upstream_features` | L9:F15926@7, k=8 → Emb:" nutrition"@7 (de=8.06) +7 more |
| 64 | `get_upstream_features` | L5:F10462@7, k=8 → Emb:" nutrition"@7 (de=1.71) +7 more |
| 65 | `get_upstream_features` | L4:F14857@7, k=8 → Emb:"<bos>"@0 (de=-9.06) +7 more |
| 66 | `get_upstream_features` | L17:F7021@7, k=8 → ❌ Feature (layer=17, pos=7, feature_idx=7021) not found in gra |
| 67 | `get_upstream_features` | L3:F2694@7, k=8 → Emb:" sports"@6 (de=4.47) +7 more |
| 68 | `get_upstream_features` | L0:F10146@7, k=8 → Emb:" nutrition"@7 (de=13.06) +7 more |
| 69 | `get_upstream_features` | L0:F14240@6, k=8 → Emb:" sports"@6 (de=14.62) +7 more |
| 70 | `get_upstream_features` | L0:F14538@7, k=8 → Emb:" sports"@6 (de=3.17) +7 more |
| 71 | `get_upstream_features` | L2:F9995@7, k=8 → Emb:" nutrition"@7 (de=7.94) +7 more |
| 72 | `get_upstream_features` | L1:F2245@7, k=8 → Emb:" nutrition"@7 (de=13.56) +7 more |
| 73 | `get_upstream_features` | L1:F15310@7, k=8 → Emb:" nutrition"@7 (de=8.56) +7 more |
| 74 | `get_upstream_features` | L1:F10958@7, k=8 → Emb:" sports"@6 (de=5.34) +7 more |
| 75 | `get_upstream_features` | L0:F8028@2, k=8 → Emb:" areas"@2 (de=18.00) +7 more |
| 76 | `get_upstream_features` | L0:F8028@2, k=8 → Emb:" areas"@2 (de=18.00) +7 more |
| 77 | `get_upstream_features` | L0:F10254@6, k=8 → Emb:" sports"@6 (de=25.50) +7 more |
| 78 | `get_upstream_features` | L0:F8153@26, k=8 → Emb:"te"@26 (de=23.38) +7 more |
| 79 | `get_upstream_features` | L0:F2107@1, k=8 → Emb:"Her"@1 (de=8.38) +7 more |
| 80 | `get_upstream_features` | L0:F1424@1, k=8 → Emb:"Her"@1 (de=8.31) +7 more |
| 81 | `get_upstream_features` | L0:F34@1, k=8 → Emb:"Her"@1 (de=8.44) +7 more |
| 82 | `get_upstream_features` | L0:F2115@7, k=8 → Emb:" nutrition"@7 (de=2.66) +7 more |
| 83 | `get_upstream_features` | L1:F11764@25, k=8 → Emb:" Nutrition"@23 (de=7.75) +7 more |
| 84 | `get_upstream_features` | L1:F6631@25, k=8 → Emb:" Nutrition"@23 (de=7.47) +7 more |
| 85 | `get_upstream_features` | L1:F5251@26, k=8 → Emb:"te"@26 (de=8.19) +7 more |
| 86 | `get_upstream_features` | L0:F2745@26, k=8 → Emb:" Die"@25 (de=10.38) +7 more |
| 87 | `get_upstream_features` | L0:F4058@25, k=8 → Emb:" Die"@25 (de=13.25) +7 more |
| 88 | `get_upstream_features` | L0:F6129@25, k=8 → Emb:" Die"@25 (de=14.12) +7 more |
| 89 | `get_upstream_features` | L0:F14068@26, k=8 → Emb:"te"@26 (de=13.00) +7 more |
| 90 | `get_upstream_features` | L0:F2420@25, k=8 → Emb:" Die"@25 (de=11.00) +7 more |
| 91 | `get_upstream_features` | L0:F2115@25, k=8 → Emb:" Die"@25 (de=9.81) +7 more |
| 92 | `get_upstream_features` | L0:F2115@7, k=8 → Emb:" nutrition"@7 (de=2.66) +7 more |
| 93 | `get_upstream_features` | L0:F7843@23, k=8 → Emb:" Nutrition"@23 (de=15.44) +7 more |
| 94 | `get_upstream_features` | L0:F5201@23, k=8 → Emb:" Nutrition"@23 (de=18.88) +7 more |
| 95 | `get_upstream_features` | L0:F5201@23, k=8 → Emb:" Nutrition"@23 (de=18.88) +7 more |
| 96 | `get_upstream_features` | L0:F7843@23, k=8 → Emb:" Nutrition"@23 (de=15.44) +7 more |
| 97 | `get_upstream_features` | L8:F14230@7, k=8 → Emb:" nutrition"@7 (de=2.97) +7 more |
| 98 | `get_upstream_features` | L6:F8614@7, k=8 → Emb:" expertise"@4 (de=1.19) +7 more |

### Build

`build_circuit` → 23 nodes, 20 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 99,484 | 24,660 | 653,140 | 0 | $0.0986 | — | — |
| **Total** | | **99,484** | **24,660** | **653,140** | **0** | **$0.0986** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 45s