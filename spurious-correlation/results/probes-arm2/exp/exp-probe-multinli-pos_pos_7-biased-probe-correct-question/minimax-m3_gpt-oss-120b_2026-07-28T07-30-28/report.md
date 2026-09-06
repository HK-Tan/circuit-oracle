# Circuit Oracle Report
**Date:** 2026-07-28 07:30:28 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_7 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction-classification score is driven overwhelmingly by a deep tower of features anchored on the literal "not" tokens at positions 23 ("will not forget") and 29 ("is not of great height"), with secondary contributions from entity-binding features on "abbey" and the "you"/"is" tokens — i.e. the circuit uses the *presence of negation words* (and a contradictory-attribute pattern) as its primary signal, not deep lexical/semantic comparison of the premise ("towering, steepled abbey") and hypothesis ("lacks a steeple", "not of great height").

**Confidence:** 8

**Reasoning:** 
- The two largest positive direct-effect features on the probe are **L16:F12358 (0.36)** and **L16:F9779 (0.24)** — both fire *only* at the two positions holding the word **"not"** (pos 23 and 29). Their direct upstream is dominated by `Emb: "not" (pos 29) = 19.5` and `Emb: "not" (pos 23) = 6.8`, then by a chain of L0–L3 features (L0:F4958, L2:F12021, L2:F12694, L3:F8011, L3:F1101, L3:F9803) whose top-1 upstream is again `Emb: "not"`. These mid-layer "negation-anchor" features are then amplified through deeper L4–L15 detectors (L4:F4492 "not + agreement", L4:F2422 anti-affirmation, L4:F2332/F7500, L9:F14687, L11:F420, L12:F14750, L13:F3295, L14:F12021, L14:F15790, L15:F10071) which are again driven primarily by `Emb: "not"` (e.g. L13:F3295 ← `Emb: "not"=17.75`, L12:F14750 ← `Emb: "not"=9.875`, L14:F13077 ← `Emb: "not"=7.8`).
- A second large contribution comes from L13:F3295 (+0.19, pos 29), an explicit "is-not" auxiliary detector whose direct upstream is `Emb: "not"=17.75` + `Emb: "is"=3.3`. L15:F10071 (+0.15) is the same pattern.
- The hypothesis content (the *negated* attributes themselves — "steepled", "of great height", "towering") is *not* carried by the dominant path. The "towering" / "steepled" / "abbey" tokens are present in the graph (Emb "abbey" pos 10, Emb "steep" pos 8, Emb "towering" pos 6) and feed features like L4:F4605 (abbey-feature, 0.18 direct), L4:F3833 (steepled-compound, 0.16), L1:F15005 (comma-towering, –0.15), and the L6–L10 sea-feature chain (L14:F10408, +0.18). But these features have *negative* or only small positive direct effect on the probe: the L4:L4605 abbey-feature has no clear positive downstream to the L13–L16 negation features, and L5:F14591 (anti-abbey, –0.17) actually *suppresses* the contradiction score.
- The L4:L3833 "first glimpse/steepled" compound-adjective feature (0.17/0.16) and the L4:L11810 "That"-boundary feature (0.16) feed the negation chain at low magnitude — these features encode the *premise's* claim but contribute to the probe only via their link into the negation-anchor group, not via any independent "premise-vs-hypothesis" comparator circuit.
- L0:F7710 at pos 21 ("you") is the only strong *negative* direct-effect feature (–0.25), indicating the probe recognizes "moment you will not forget" as a *non-contradicting* assertion pattern and subtracts it.
- The two "not" tokens are the largest single source of positive signal: `Emb: "not" (pos 29) = 34.25` into L0:F4958, and `Emb: "not" (pos 23) = 33.5` into the same feature at pos 23. There is no parallel "steepled↔not steepled" or "great height↔not great height" matching path — the contradiction classification is essentially a "negation-word detector" applied twice in the second sentence, *not* a comparison of the premise's "steepled/towering" content with the hypothesis's "lacks a steeple/is not of great height".

This validates the user's concern: the circuit relies primarily on **spurious negation-word features** (the literal tokens "not" and the "is-not"/"will-not" syntactic patterns built on them), not on the actual semantic/lexical relationship between the premise's positive descriptors and the hypothesis's negated counterparts. A prompt that contains "not" without a true contradiction (e.g., "The abbey is not red, it is grey" — which is *entailment*, not contradiction) would likely still light up this circuit.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Output Logit (probe direction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 29 | L13–L16: Syntactic/Negation-grouped late features at pos 29 | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |
| [L15:F10071](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) | 29 | L13–L16: Syntactic/Negation-grouped late features at pos 29 | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) |
| [L13:F3295](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) | 29 | L13–L16: Syntactic/Negation-grouped late features at pos 29 | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) |
| [L14:F12021](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12021) | 29 | L13–L16: Syntactic/Negation-grouped late features at pos 29 | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12021) |
| [L12:F14750](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14750) | 29 | L13–L16: Syntactic/Negation-grouped late features at pos 29 | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14750) |
| [L16:F9779](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/9779) | 23 | L12–L16: Negation-grouped late features at pos 23 | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/9779) |
| [L15:F3521](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3521) | 23 | L12–L16: Negation-grouped late features at pos 23 | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3521) |
| [L13:F102](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/102) | 23 | L12–L16: Negation-grouped late features at pos 23 | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/102) |
| [L12:F9489](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/9489) | 23 | L12–L16: Negation-grouped late features at pos 23 | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/9489) |
| [L14:F15135](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/15135) | 23 | L12–L16: Negation-grouped late features at pos 23 | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/15135) |
| [L11:F420](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/420) | 29 | L2–L12: Mid-layer negation/agreement detectors at pos 23/29 | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/420) |
| [L9:F15289](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15289) | 29 | L2–L12: Mid-layer negation/agreement detectors at pos 23/29 | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15289) |
| [L8:F3907](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/3907) | 29 | L2–L12: Mid-layer negation/agreement detectors at pos 23/29 | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/3907) |
| [L9:F14687](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/14687) | 29 | L2–L12: Mid-layer negation/agreement detectors at pos 23/29 | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/14687) |
| [L6:F12349](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12349) | 29 | L2–L12: Mid-layer negation/agreement detectors at pos 23/29 | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12349) |
| [L7:F2981](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2981) | 29 | L2–L12: Mid-layer negation/agreement detectors at pos 23/29 | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2981) |
| [L5:F2678](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/2678) | 29 | L2–L12: Mid-layer negation/agreement detectors at pos 23/29 | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/2678) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 29 | L2–L12: Mid-layer negation/agreement detectors at pos 23/29 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 23 | L2–L12: Mid-layer negation/agreement detectors at pos 23/29 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L2:F12694](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12694) | 23 | L2–L12: Mid-layer negation/agreement detectors at pos 23/29 | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12694) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 29 | L2–L12: Mid-layer negation/agreement detectors at pos 23/29 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 23 | L2–L12: Mid-layer negation/agreement detectors at pos 23/29 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L4:F2332](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2332) | 29 | L2–L12: Mid-layer negation/agreement detectors at pos 23/29 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2332) |
| [L4:F7500](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7500) | 29 | L2–L12: Mid-layer negation/agreement detectors at pos 23/29 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7500) |
| [L3:F1101](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) | 29 | L2–L12: Mid-layer negation/agreement detectors at pos 23/29 | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) |
| [L3:F1101](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) | 23 | L2–L12: Mid-layer negation/agreement detectors at pos 23/29 | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) |
| [L2:F12021](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) | 29 | L2–L12: Mid-layer negation/agreement detectors at pos 23/29 | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) |
| [L2:F12021](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) | 23 | L2–L12: Mid-layer negation/agreement detectors at pos 23/29 | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) |
| [L2:F4044](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4044) | 23 | L2–L3: Negation-anchor paired features (pos 23 & 29) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4044) |
| [L2:F6993](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6993) | 23 | L2–L3: Negation-anchor paired features (pos 23 & 29) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6993) |
| [L2:F6993](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6993) | 29 | L2–L3: Negation-anchor paired features (pos 23 & 29) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6993) |
| [L2:F8541](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8541) | 29 | L2–L3: Negation-anchor paired features (pos 23 & 29) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8541) |
| [L2:F4544](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4544) | 29 | L2–L3: Negation-anchor paired features (pos 23 & 29) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4544) |
| [L2:F573](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/573) | 29 | L2–L3: Negation-anchor paired features (pos 23 & 29) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/573) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 23 | L2–L3: Negation-anchor paired features (pos 23 & 29) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 29 | L2–L3: Negation-anchor paired features (pos 23 & 29) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L3:F9803](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9803) | 23 | L2–L3: Negation-anchor paired features (pos 23 & 29) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9803) |
| [L3:F9803](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9803) | 29 | L2–L3: Negation-anchor paired features (pos 23 & 29) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9803) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 29 | L0 token-bound "not"/"will"/"is" feature at pos 23, 29 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 23 | L0 token-bound "not"/"will"/"is" feature at pos 23, 29 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F10965](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10965) | 23 | L0 token-bound "not"/"will"/"is" feature at pos 23, 29 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10965) |
| [L0:F4453](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4453) | 22 | L0 token-bound "not"/"will"/"is" feature at pos 23, 29 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4453) |
| [L0:F9203](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9203) | 23 | L0 token-bound "not"/"will"/"is" feature at pos 23, 29 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9203) |
| [L0:F8046](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8046) | 22 | L0 token-bound "not"/"will"/"is" feature at pos 23, 29 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8046) |
| [L0:F15267](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15267) | 23 | L0 token-bound "not"/"will"/"is" feature at pos 23, 29 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15267) |
| [L0:F10999](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10999) | 23 | L0 token-bound "not"/"will"/"is" feature at pos 23, 29 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10999) |
| [L0:F12854](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12854) | 23 | L0 token-bound "not"/"will"/"is" feature at pos 23, 29 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12854) |
| [L1:F14233](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) | 29 | L1 ancillary negation/will auxiliary features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) |
| [L1:F14233](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) | 23 | L1 ancillary negation/will auxiliary features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) |
| [L1:F5108](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5108) | 29 | L1 ancillary negation/will auxiliary features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5108) |
| [L1:F5108](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5108) | 23 | L1 ancillary negation/will auxiliary features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5108) |
| [L1:F14680](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14680) | 29 | L1 ancillary negation/will auxiliary features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14680) |
| [L1:F14680](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14680) | 23 | L1 ancillary negation/will auxiliary features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14680) |
| [L1:F423](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/423) | 29 | L1 ancillary negation/will auxiliary features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/423) |
| [L0:F7257](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7257) | 29 | L1 ancillary negation/will auxiliary features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7257) |
| [L0:F6027](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6027) | 29 | L1 ancillary negation/will auxiliary features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6027) |
| [L0:F6027](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6027) | 23 | L1 ancillary negation/will auxiliary features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6027) |
| [L0:F15454](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15454) | 29 | L1 ancillary negation/will auxiliary features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15454) |
| [L0:F15454](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15454) | 23 | L1 ancillary negation/will auxiliary features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15454) |
| [L0:F15005](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15005) | 23 | L1 ancillary negation/will auxiliary features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15005) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 18 | L0 token-bound "is" feature at pos 18, 28 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 28 | L0 token-bound "is" feature at pos 18, 28 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L14:F10408](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10408) | 14 | L14:L10408 → sea-feature | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10408) |
| [L10:F6708](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6708) | 14 | L6–L10 sea/neutral entity feature chain at pos 14 | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6708) |
| [L8:F3174](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/3174) | 14 | L6–L10 sea/neutral entity feature chain at pos 14 | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/3174) |
| [L8:F14717](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/14717) | 14 | L6–L10 sea/neutral entity feature chain at pos 14 | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/14717) |
| [L7:F3258](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3258) | 14 | L6–L10 sea/neutral entity feature chain at pos 14 | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3258) |
| [L7:F5770](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5770) | 14 | L6–L10 sea/neutral entity feature chain at pos 14 | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5770) |
| [L6:F3848](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3848) | 14 | L6–L10 sea/neutral entity feature chain at pos 14 | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3848) |
| [L7:F9840](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9840) | 14 | L6–L10 sea/neutral entity feature chain at pos 14 | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9840) |
| [L5:F3488](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3488) | 14 | L6–L10 sea/neutral entity feature chain at pos 14 | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3488) |
| [L5:F5540](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5540) | 14 | L6–L10 sea/neutral entity feature chain at pos 14 | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5540) |
| [L4:F4173](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4173) | 14 | L6–L10 sea/neutral entity feature chain at pos 14 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4173) |
| [L4:F11425](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11425) | 14 | L6–L10 sea/neutral entity feature chain at pos 14 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11425) |
| [L3:F16223](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16223) | 14 | L6–L10 sea/neutral entity feature chain at pos 14 | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16223) |
| [L2:F8338](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8338) | 14 | L6–L10 sea/neutral entity feature chain at pos 14 | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8338) |
| [L0:F4912](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4912) | 14 | L6–L10 sea/neutral entity feature chain at pos 14 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4912) |
| [L5:F14591](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14591) | 10 | L5:L14591 (anti-abbey, at pos 10 & 27, NEGATIVE direct effect on probe) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14591) |
| [L5:F14591](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14591) | 27 | L5:L14591 (anti-abbey, at pos 10 & 27, NEGATIVE direct effect on probe) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14591) |
| [L4:F4605](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) | 10 | L4:L4605 abbey-feature at pos 8/9/10/27 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) |
| [L4:F4605](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) | 27 | L4:L4605 abbey-feature at pos 8/9/10/27 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) |
| [L4:F4605](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) | 9 | L4:L4605 abbey-feature at pos 8/9/10/27 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) |
| [L4:F4605](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) | 8 | L4:L4605 abbey-feature at pos 8/9/10/27 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) |
| [L4:F1104](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1104) | 10 | L4:L4605 abbey-feature at pos 8/9/10/27 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1104) |
| [L4:F4872](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4872) | 10 | L4:L4605 abbey-feature at pos 8/9/10/27 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4872) |
| [L4:F13244](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) | 10 | L4:L4605 abbey-feature at pos 8/9/10/27 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) |
| [L2:F8185](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8185) | 10 | L4:L4605 abbey-feature at pos 8/9/10/27 | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8185) |
| [L2:F8185](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8185) | 27 | L4:L4605 abbey-feature at pos 8/9/10/27 | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8185) |
| [L2:F12263](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12263) | 10 | L4:L4605 abbey-feature at pos 8/9/10/27 | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12263) |
| [L1:F7934](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7934) | 10 | L4:L4605 abbey-feature at pos 8/9/10/27 | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7934) |
| [L0:F3512](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3512) | 10 | L4:L4605 abbey-feature at pos 8/9/10/27 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3512) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 10 | L4:L4605 abbey-feature at pos 8/9/10/27 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F11835](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11835) | 10 | L4:L4605 abbey-feature at pos 8/9/10/27 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11835) |
| [L0:F9320](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9320) | 10 | L4:L4605 abbey-feature at pos 8/9/10/27 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9320) |
| [L0:F9320](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9320) | 27 | L4:L4605 abbey-feature at pos 8/9/10/27 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9320) |
| [L0:F4470](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4470) | 10 | L4:L4605 abbey-feature at pos 8/9/10/27 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4470) |
| [L0:F8633](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8633) | 27 | L4:L4605 abbey-feature at pos 8/9/10/27 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8633) |
| [L4:F3833](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) | 4 | L4:L3833 'steepled/led' compound-adjective feature | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) |
| [L4:F3833](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) | 3 | L4:L3833 'steepled/led' compound-adjective feature | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) |
| [L3:F6616](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6616) | 4 | L4:L3833 'steepled/led' compound-adjective feature | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6616) |
| [L3:F11165](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11165) | 2 | L4:L3833 'steepled/led' compound-adjective feature | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11165) |
| [L3:F4081](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4081) | 9 | L4:L3833 'steepled/led' compound-adjective feature | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4081) |
| [L3:F7650](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7650) | 9 | L4:L3833 'steepled/led' compound-adjective feature | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7650) |
| [L2:F5878](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5878) | 9 | L4:L3833 'steepled/led' compound-adjective feature | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5878) |
| [L2:F6145](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6145) | 9 | L4:L3833 'steepled/led' compound-adjective feature | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6145) |
| [L1:F14394](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14394) | 9 | L4:L3833 'steepled/led' compound-adjective feature | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14394) |
| [L1:F1950](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1950) | 9 | L4:L3833 'steepled/led' compound-adjective feature | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1950) |
| [L1:F13902](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13902) | 9 | L4:L3833 'steepled/led' compound-adjective feature | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13902) |
| [L1:F13974](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13974) | 9 | L4:L3833 'steepled/led' compound-adjective feature | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13974) |
| [L1:F12586](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12586) | 9 | L4:L3833 'steepled/led' compound-adjective feature | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12586) |
| [L1:F4103](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4103) | 9 | L4:L3833 'steepled/led' compound-adjective feature | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4103) |
| [L2:F4081](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4081) | 9 | L4:L3833 'steepled/led' compound-adjective feature | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4081) |
| [L0:F2159](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2159) | 9 | L4:L3833 'steepled/led' compound-adjective feature | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2159) |
| [L0:F13126](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13126) | 9 | L4:L3833 'steepled/led' compound-adjective feature | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13126) |
| [L0:F11952](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11952) | 9 | L4:L3833 'steepled/led' compound-adjective feature | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11952) |
| [L0:F13874](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13874) | 9 | L4:L3833 'steepled/led' compound-adjective feature | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13874) |
| [L0:F3790](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3790) | 9 | L4:L3833 'steepled/led' compound-adjective feature | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3790) |
| [L0:F31](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/31) | 9 | L4:L3833 'steepled/led' compound-adjective feature | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/31) |
| [L0:F12421](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12421) | 9 | L4:L3833 'steepled/led' compound-adjective feature | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12421) |
| [L0:F3371](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3371) | 9 | L4:L3833 'steepled/led' compound-adjective feature | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3371) |
| [L0:F7056](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7056) | 2 | L4:L3833 'steepled/led' compound-adjective feature | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7056) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 4 | L4:L3833 'steepled/led' compound-adjective feature | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 5 | L4:L3833 'steepled/led' compound-adjective feature | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F7710](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) | 21 | L0:L7710 'you'-feature (NEGATIVE direct effect on probe) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) |
| [L0:F5060](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5060) | 1 | L0:L5060 'That'-feature (boundary marker) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5060) |
| [L4:F11810](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11810) | 1 | L0:L5060 'That'-feature (boundary marker) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11810) |
| [L2:F6186](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6186) | 1 | L0:L5060 'That'-feature (boundary marker) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6186) |
| [L2:F5414](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5414) | 1 | L0:L5060 'That'-feature (boundary marker) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5414) |
| [L2:F8094](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8094) | 2 | L0:L5060 'That'-feature (boundary marker) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8094) |
| [L2:F48](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/48) | 2 | L0:L5060 'That'-feature (boundary marker) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/48) |
| [L1:F15005](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15005) | 7 | L1:L15005' 'comma-towering' (NEG) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15005) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 29 | Emb: not (pos 29) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 23 | Emb: not (pos 23) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 18 | Emb: is (pos 18) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 28 | Emb: is (pos 28) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 22 | Emb: will (pos 22) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: abbey (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: sea (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: steep (pos 8) / led (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: steep (pos 8) / led (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: first (pos 2) / glimpse (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: first (pos 2) / glimpse (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: you (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L16:12358 de=0.359 |
| 3 | `get_upstream_features` | Emb:" not"@29 (de=19.50) +9 more |
| 4 | `get_upstream_features` | Emb:" you"@21 (de=42.25) +9 more |
| 5 | `get_upstream_features` | Emb:" the"@5 (de=34.25) +9 more |
| 6 | `get_upstream_features` | Emb:" will"@22 (de=7.31) +9 more |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F12358@29` | ❌ error | — | — | Trace the path from L16:F12358 at pos 29. This feature directly drives the probe… |
| SA-2 | `L16:F9779@23` | ❌ error | — | — | Trace the path from L16:F9779 at pos 23. This feature directly drives the probe … |
| SA-3 | `L13:F3295@29` | ❌ error | — | — | Trace the path from L13:F3295 at pos 29. This mid-layer feature drives the probe… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L15:F10071@29, k=10 → Emb:" not"@29 (de=9.75) +9 more |
| 2 | `get_upstream_features` | L3:F8011@29, k=10 → Emb:" not"@29 (de=21.62) +9 more |
| 3 | `get_upstream_features` | L0:F4958@29, k=10 → Emb:" not"@29 (de=34.25) +9 more |
| 4 | `get_upstream_features` | L0:F11375@18, k=10 → Emb:" is"@18 (de=32.50) +9 more |
| 5 | `get_upstream_features` | L0:F2848@4, k=10 → Emb:" of"@4 (de=35.25) +9 more |
| 6 | `get_upstream_features` | L0:F5060@1, k=10 → Emb:"That"@1 (de=11.88) +9 more |
| 7 | `get_upstream_features` | L14:F10408@14, k=10 → Emb:" sea"@14 (de=22.88) +9 more |
| 8 | `get_upstream_features` | L4:F3833@4, k=10 → Emb:" glimpse"@3 (de=7.03) +9 more |
| 9 | `get_upstream_features` | L4:F11810@1, k=10 → Emb:"That"@1 (de=14.31) +9 more |
| 10 | `get_upstream_features` | L13:F3295@29, k=10 → Emb:" not"@29 (de=17.75) +9 more |
| 11 | `get_upstream_features` | L13:F102@23, k=10 → Emb:" not"@23 (de=9.06) +9 more |
| 12 | `get_upstream_features` | L0:F4958@23, k=10 → Emb:" not"@23 (de=33.50) +9 more |
| 13 | `get_upstream_features` | L15:F3521@23, k=10 → Emb:" will"@22 (de=5.91) +9 more |
| 14 | `get_upstream_features` | L4:F4492@23, k=10 → Emb:" not"@23 (de=18.50) +9 more |
| 15 | `get_upstream_features` | L4:F4173@14, k=10 → Emb:" sea"@14 (de=21.62) +9 more |
| 16 | `get_upstream_features` | L6:F3848@14, k=10 → Emb:" sea"@14 (de=14.69) +9 more |
| 17 | `get_upstream_features` | L3:F16223@14, k=10 → Emb:" sea"@14 (de=19.88) +9 more |
| 18 | `get_upstream_features` | L4:F3833@3, k=10 → Emb:" glimpse"@3 (de=13.56) +9 more |
| 19 | `get_upstream_features` | L6:F5342@4, k=10 → Emb:" first"@2 (de=12.06) +9 more |
| 20 | `get_upstream_features` | L5:F14591@10, k=10 → Emb:" abbey"@10 (de=10.00) +9 more |
| 21 | `get_upstream_features` | L1:F15005@7, k=10 → Emb:","@7 (de=6.12) +9 more |
| 22 | `get_upstream_features` | L4:F4605@9, k=10 → Emb:"led"@9 (de=6.44) +9 more |
| 23 | `get_upstream_features` | L3:F8011@23, k=10 → Emb:" not"@23 (de=19.62) +9 more |
| 24 | `get_upstream_features` | L2:F12021@29, k=10 → Emb:" not"@29 (de=22.50) +9 more |
| 25 | `get_upstream_features` | L2:F12694@23, k=10 → Emb:" will"@22 (de=15.38) +9 more |
| 26 | `get_upstream_features` | L2:F4044@23, k=10 → Emb:" will"@22 (de=7.31) +9 more |
| 27 | `get_upstream_features` | L3:F1101@23, k=10 → Emb:" not"@23 (de=12.12) +9 more |
| 28 | `get_upstream_features` | L8:F3174@14, k=10 → Emb:" sea"@14 (de=9.81) +9 more |
| 29 | `get_upstream_features` | L7:F5770@14, k=10 → Emb:" sea"@14 (de=13.31) +9 more |
| 30 | `get_upstream_features` | L2:F8338@14, k=10 → Emb:" sea"@14 (de=24.38) +9 more |
| 31 | `get_upstream_features` | L1:F10498@1, k=10 → Emb:"That"@1 (de=15.69) +9 more |
| 32 | `get_upstream_features` | L2:F6186@1, k=10 → Emb:"That"@1 (de=19.50) +9 more |
| 33 | `get_upstream_features` | L0:F4870@7, k=10 → Emb:","@7 (de=30.00) +9 more |
| 34 | `get_upstream_features` | L3:F4081@9, k=10 → Emb:" steep"@8 (de=11.44) +9 more |
| 35 | `get_upstream_features` | L3:F6616@4, k=10 → Emb:" glimpse"@3 (de=18.38) +9 more |
| 36 | `get_upstream_features` | L3:F11165@2, k=10 → Emb:" first"@2 (de=23.75) +9 more |
| 37 | `get_upstream_features` | L14:F13077@29, k=10 → Emb:" not"@29 (de=7.81) +9 more |
| 38 | `get_upstream_features` | L14:F15790@29, k=10 → Emb:" not"@29 (de=6.16) +9 more |
| 39 | `get_upstream_features` | L14:F15135@23, k=10 → Emb:" not"@23 (de=4.44) +9 more |
| 40 | `get_upstream_features` | L14:F12021@29, k=10 → Emb:" not"@29 (de=10.31) +9 more |
| 41 | `get_upstream_features` | L10:F6708@14, k=10 → Emb:" sea"@14 (de=6.47) +9 more |
| 42 | `get_upstream_features` | L2:F6993@23, k=10 → Emb:" not"@23 (de=6.56) +9 more |
| 43 | `get_upstream_features` | L1:F14233@23, k=10 → Emb:" not"@23 (de=6.50) +9 more |
| 44 | `get_upstream_features` | L0:F10965@23, k=10 → Emb:" will"@22 (de=13.62) +9 more |
| 45 | `get_upstream_features` | L0:F15454@23, k=10 → Emb:" will"@22 (de=8.00) +9 more |
| 46 | `get_upstream_features` | L0:F15005@23, k=10 → Emb:" will"@22 (de=15.19) +9 more |
| 47 | `get_upstream_features` | L12:F14750@29, k=10 → Emb:" not"@29 (de=9.88) +9 more |
| 48 | `get_upstream_features` | L7:F3258@14, k=10 → Emb:" sea"@14 (de=7.81) +9 more |
| 49 | `get_upstream_features` | L8:F14717@14, k=10 → Emb:" sea"@14 (de=11.38) +9 more |
| 50 | `get_upstream_features` | L2:F5878@9, k=10 → Emb:" steep"@8 (de=8.56) +9 more |
| 51 | `get_upstream_features` | L4:F4605@10, k=10 → Emb:" abbey"@10 (de=7.97) +9 more |
| 52 | `get_upstream_features` | L0:F2159@9, k=10 → Emb:"led"@9 (de=16.50) +9 more |
| 53 | `get_upstream_features` | L2:F5878@10, k=10 → ❌ Feature (layer=2, feature_idx=5878) not found at pos=10. Thi |
| 54 | `get_upstream_features` | L0:F4912@14, k=10 → Emb:" sea"@14 (de=21.38) +9 more |
| 55 | `get_upstream_features` | L0:F7007@14, k=10 → Emb:" sea"@14 (de=13.88) +9 more |
| 56 | `get_upstream_features` | L0:F7056@2, k=10 → Emb:" first"@2 (de=30.62) +9 more |
| 57 | `get_upstream_features` | L11:F420@29, k=10 → Emb:" not"@29 (de=7.25) +9 more |
| 58 | `get_upstream_features` | L12:F9489@23, k=10 → Emb:" not"@23 (de=8.50) +9 more |
| 59 | `get_upstream_features` | L4:F2422@23, k=10 → Emb:" not"@23 (de=16.88) +9 more |
| 60 | `get_upstream_features` | L9:F15289@29, k=10 → Emb:" not"@29 (de=2.58) +9 more |
| 61 | `get_upstream_features` | L1:F5108@23, k=10 → Emb:" not"@23 (de=14.81) +9 more |
| 62 | `get_upstream_features` | L0:F8046@22, k=10 → Emb:" will"@22 (de=39.25) +9 more |
| 63 | `get_upstream_features` | L2:F6145@9, k=10 → Emb:"led"@9 (de=35.75) +9 more |
| 64 | `get_upstream_features` | L2:F8185@10, k=10 → Emb:" abbey"@10 (de=9.44) +9 more |
| 65 | `get_upstream_features` | L5:F3488@14, k=10 → Emb:" sea"@14 (de=3.31) +9 more |
| 66 | `get_upstream_features` | L4:F11425@14, k=10 → Emb:" sea"@14 (de=14.00) +9 more |
| 67 | `get_upstream_features` | L9:F14687@29, k=10 → Emb:" not"@29 (de=7.44) +9 more |
| 68 | `get_upstream_features` | L6:F12349@29, k=10 → Emb:" not"@29 (de=7.94) +9 more |
| 69 | `get_upstream_features` | L4:F2332@29, k=10 → Emb:" not"@29 (de=21.25) +9 more |
| 70 | `get_upstream_features` | L1:F14394@9, k=10 → Emb:"led"@9 (de=18.38) +9 more |
| 71 | `get_upstream_features` | L8:F3907@29, k=10 → Emb:" not"@29 (de=5.91) +9 more |
| 72 | `get_upstream_features` | L0:F9203@23, k=10 → Emb:" not"@23 (de=8.94) +9 more |
| 73 | `get_upstream_features` | L0:F11375@28, k=10 → Emb:" is"@28 (de=34.00) +9 more |
| 74 | `get_upstream_features` | L0:F9646@29, k=10 → Emb:" is"@28 (de=13.69) +9 more |
| 75 | `get_upstream_features` | L4:F7500@29, k=10 → Emb:" not"@29 (de=14.75) +9 more |
| 76 | `get_upstream_features` | L2:F4544@29, k=10 → Emb:" not"@29 (de=11.31) +9 more |
| 77 | `get_upstream_features` | L2:F8541@29, k=10 → Emb:" not"@29 (de=9.06) +9 more |
| 78 | `get_upstream_features` | L7:F2981@29, k=10 → Emb:" not"@29 (de=4.12) +9 more |
| 79 | `get_upstream_features` | L5:F2678@29, k=10 → L2:F12021 (de=2.17) +9 more |
| 80 | `get_upstream_features` | L0:F7710@23, k=10 → ❌ Feature (layer=0, feature_idx=7710) not found at pos=23. Thi |
| 81 | `get_upstream_features` | L3:F9803@29, k=10 → Emb:" not"@29 (de=13.94) +9 more |
| 82 | `get_upstream_features` | L3:F9803@23, k=10 → Emb:" not"@23 (de=13.12) +9 more |
| 83 | `get_upstream_features` | L0:F7257@29, k=10 → Emb:" is"@28 (de=9.38) +9 more |
| 84 | `get_upstream_features` | L0:F6027@29, k=10 → Emb:" not"@29 (de=14.06) +9 more |
| 85 | `get_upstream_features` | L0:F15267@23, k=10 → Emb:" not"@23 (de=11.69) +9 more |
| 86 | `get_upstream_features` | L0:F12854@23, k=10 → Emb:" not"@23 (de=11.81) +9 more |
| 87 | `get_upstream_features` | L0:F10965@22, k=10 → ❌ Feature (layer=0, feature_idx=10965) not found at pos=22. Th |
| 88 | `get_upstream_features` | L0:F4453@22, k=10 → Emb:" will"@22 (de=13.50) +9 more |
| 89 | `get_upstream_features` | L0:F978@1, k=10 → ❌ Feature (layer=0, pos=1, feature_idx=978) not found in graph |
| 90 | `get_upstream_features` | L0:F4870@6, k=10 → ❌ Feature (layer=0, feature_idx=4870) not found at pos=6. This |
| 91 | `get_upstream_features` | L1:F14680@23, k=10 → Emb:" not"@23 (de=17.25) +9 more |
| 92 | `get_upstream_features` | L1:F14680@29, k=10 → Emb:" not"@29 (de=17.38) +9 more |
| 93 | `get_upstream_features` | L1:F423@29, k=10 → Emb:" is"@28 (de=8.69) +9 more |
| 94 | `get_upstream_features` | L9:F14687@23, k=10 → ❌ Feature (layer=9, feature_idx=14687) not found at pos=23. Th |
| 95 | `get_upstream_features` | L5:F14591@9, k=10 → ❌ Feature (layer=5, feature_idx=14591) not found at pos=9. Thi |
| 96 | `get_upstream_features` | L4:F4605@9, k=10 → Emb:"led"@9 (de=6.44) +9 more |
| 97 | `get_upstream_features` | L0:F2332@29, k=10 → Emb:" is"@28 (de=5.19) +9 more |
| 98 | `get_upstream_features` | L0:F6051@25, k=10 → Emb:"."@25 (de=47.50) +9 more |
| 99 | `get_upstream_features` | L0:F11331@29, k=10 → Emb:" is"@28 (de=11.81) +9 more |
| 100 | `get_upstream_features` | L0:F10999@23, k=10 → Emb:" not"@23 (de=5.91) +9 more |
| 101 | `get_upstream_features` | L0:F8974@12, k=10 → Emb:" from"@12 (de=39.50) +9 more |
| 102 | `get_upstream_features` | L0:F3371@9, k=10 → Emb:"led"@9 (de=19.12) +9 more |
| 103 | `get_upstream_features` | L1:F12586@9, k=10 → Emb:"led"@9 (de=10.38) +9 more |
| 104 | `get_upstream_features` | L1:F4103@9, k=10 → Emb:"led"@9 (de=14.38) +9 more |
| 105 | `get_upstream_features` | L1:F13902@9, k=10 → Emb:"led"@9 (de=16.50) +9 more |
| 106 | `get_upstream_features` | L1:F13974@9, k=10 → Emb:"led"@9 (de=5.94) +9 more |
| 107 | `get_upstream_features` | L0:F3423@10, k=10 → ❌ Feature (layer=0, pos=10, feature_idx=3423) not found in gra |
| 108 | `get_upstream_features` | L5:F14591@10, k=10 → Emb:" abbey"@10 (de=10.00) +9 more |
| 109 | `get_upstream_features` | L0:F3423@10, k=10 → ❌ Feature (layer=0, pos=10, feature_idx=3423) not found in gra |
| 110 | `get_upstream_features` | L1:F7934@10, k=10 → Emb:" abbey"@10 (de=9.06) +9 more |
| 111 | `get_upstream_features` | L0:F11835@10, k=10 → Emb:" abbey"@10 (de=7.19) +9 more |
| 112 | `get_upstream_features` | L0:F9320@10, k=10 → Emb:" abbey"@10 (de=8.88) +9 more |
| 113 | `get_upstream_features` | L2:F12263@10, k=10 → Emb:" abbey"@10 (de=8.88) +9 more |
| 114 | `get_upstream_features` | L2:F8185@10, k=10 → Emb:" abbey"@10 (de=9.44) +9 more |
| 115 | `get_upstream_features` | L4:F1104@10, k=10 → Emb:" abbey"@10 (de=3.45) +9 more |
| 116 | `get_upstream_features` | L4:F13244@10, k=10 → Emb:" abbey"@10 (de=9.06) +9 more |
| 117 | `get_upstream_features` | L4:F4872@10, k=10 → Emb:" abbey"@10 (de=7.44) +9 more |
| 118 | `get_upstream_features` | L4:F1104@10, k=10 → Emb:" abbey"@10 (de=3.45) +9 more |
| 119 | `get_upstream_features` | L0:F577@10, k=10 → ❌ Feature (layer=0, pos=10, feature_idx=577) not found in grap |
| 120 | `get_upstream_features` | L0:F577@6, k=10 → ❌ Feature (layer=0, pos=6, feature_idx=577) not found in graph |
| 121 | `get_upstream_features` | L4:F4605@9, k=10 → Emb:"led"@9 (de=6.44) +9 more |
| 122 | `get_upstream_features` | L3:F4081@9, k=10 → Emb:" steep"@8 (de=11.44) +9 more |
| 123 | `get_upstream_features` | L3:F7650@9, k=10 → Emb:"led"@9 (de=5.81) +9 more |
| 124 | `get_upstream_features` | L3:F15164@9, k=10 → Emb:" steep"@8 (de=10.06) +9 more |
| 125 | `get_upstream_features` | L1:F14394@9, k=10 → Emb:"led"@9 (de=18.38) +9 more |
| 126 | `get_upstream_features` | L0:F13126@9, k=10 → Emb:"led"@9 (de=11.38) +9 more |
| 127 | `get_upstream_features` | L0:F11952@9, k=10 → Emb:"led"@9 (de=11.12) +9 more |
| 128 | `get_upstream_features` | L0:F13874@9, k=10 → Emb:"led"@9 (de=14.38) +9 more |
| 129 | `get_upstream_features` | L0:F3790@9, k=10 → Emb:"led"@9 (de=8.44) +9 more |
| 130 | `get_upstream_features` | L0:F31@9, k=10 → Emb:"led"@9 (de=10.56) +9 more |
| 131 | `get_upstream_features` | L0:F2159@9, k=10 → Emb:"led"@9 (de=16.50) +9 more |
| 132 | `get_upstream_features` | L13:F3295@29, k=10 → Emb:" not"@29 (de=17.75) +9 more |
| 133 | `get_upstream_features` | L4:F4492@29, k=10 → Emb:" not"@29 (de=19.38) +9 more |
| 134 | `get_upstream_features` | L4:F4492@23, k=10 → Emb:" not"@23 (de=18.50) +9 more |
| 135 | `get_upstream_features` | L2:F12021@23, k=10 → Emb:" not"@23 (de=22.50) +9 more |
| 136 | `get_upstream_features` | L3:F1101@29, k=10 → Emb:" not"@29 (de=13.69) +9 more |
| 137 | `get_upstream_features` | L3:F1101@23, k=10 → Emb:" not"@23 (de=12.12) +9 more |
| 138 | `get_upstream_features` | L13:F102@23, k=10 → Emb:" not"@23 (de=9.06) +9 more |
| 139 | `get_upstream_features` | L0:F978@1, k=10 → ❌ Feature (layer=0, pos=1, feature_idx=978) not found in graph |
| 140 | `get_upstream_features` | L0:F1695@1, k=10 → Emb:"That"@1 (de=8.25) +9 more |
| 141 | `get_upstream_features` | L0:F1847@1, k=10 → Emb:"That"@1 (de=-3.83) +9 more |
| 142 | `get_upstream_features` | L0:F4958@29, k=10 → Emb:" not"@29 (de=34.25) +9 more |
| 143 | `get_upstream_features` | L0:F4958@23, k=10 → Emb:" not"@23 (de=33.50) +9 more |
| 144 | `get_upstream_features` | L0:F4958@28, k=10 → ❌ Feature (layer=0, feature_idx=4958) not found at pos=28. Thi |
| 145 | `get_upstream_features` | L0:F4958@27, k=10 → ❌ Feature (layer=0, feature_idx=4958) not found at pos=27. Thi |
| 146 | `get_upstream_features` | L0:F4958@18, k=10 → ❌ Feature (layer=0, feature_idx=4958) not found at pos=18. Thi |
| 147 | `get_upstream_features` | L0:F4958@17, k=10 → ❌ Feature (layer=0, feature_idx=4958) not found at pos=17. Thi |
| 148 | `get_upstream_features` | L0:F4958@14, k=10 → ❌ Feature (layer=0, feature_idx=4958) not found at pos=14. Thi |
| 149 | `get_upstream_features` | L0:F4958@10, k=10 → ❌ Feature (layer=0, feature_idx=4958) not found at pos=10. Thi |
| 150 | `get_upstream_features` | L0:F4958@9, k=10 → ❌ Feature (layer=0, feature_idx=4958) not found at pos=9. This |
| 151 | `get_upstream_features` | L0:F4958@7, k=10 → ❌ Feature (layer=0, feature_idx=4958) not found at pos=7. This |
| 152 | `get_upstream_features` | L3:F1101@29, k=10 → Emb:" not"@29 (de=13.69) +9 more |
| 153 | `get_upstream_features` | L3:F1101@23, k=10 → Emb:" not"@23 (de=12.12) +9 more |
| 154 | `get_upstream_features` | L3:F8011@29, k=10 → Emb:" not"@29 (de=21.62) +9 more |
| 155 | `get_upstream_features` | L3:F8011@23, k=10 → Emb:" not"@23 (de=19.62) +9 more |
| 156 | `get_upstream_features` | L3:F9803@29, k=10 → Emb:" not"@29 (de=13.94) +9 more |
| 157 | `get_upstream_features` | L3:F9803@23, k=10 → Emb:" not"@23 (de=13.12) +9 more |
| 158 | `get_upstream_features` | L4:F2422@29, k=10 → Emb:" not"@29 (de=17.50) +9 more |
| 159 | `get_upstream_features` | L4:F2422@23, k=10 → Emb:" not"@23 (de=16.88) +9 more |
| 160 | `get_upstream_features` | L2:F6993@23, k=10 → Emb:" not"@23 (de=6.56) +9 more |
| 161 | `get_upstream_features` | L2:F6993@29, k=10 → Emb:" not"@29 (de=6.22) +9 more |
| 162 | `get_upstream_features` | L0:F7710@21, k=10 → Emb:" you"@21 (de=42.25) +9 more |
| 163 | `get_upstream_features` | L0:F11375@18, k=10 → Emb:" is"@18 (de=32.50) +9 more |
| 164 | `get_upstream_features` | L0:F3820@5, k=10 → Emb:" the"@5 (de=34.25) +9 more |
| 165 | `get_upstream_features` | L0:F2848@4, k=10 → Emb:" of"@4 (de=35.25) +9 more |
| 166 | `get_upstream_features` | L0:F5060@1, k=10 → Emb:"That"@1 (de=11.88) +9 more |
| 167 | `get_upstream_features` | L14:F10408@14, k=10 → Emb:" sea"@14 (de=22.88) +9 more |
| 168 | `get_upstream_features` | L4:F3833@4, k=10 → Emb:" glimpse"@3 (de=7.03) +9 more |
| 169 | `get_upstream_features` | L4:F11810@1, k=10 → Emb:"That"@1 (de=14.31) +9 more |
| 170 | `get_upstream_features` | L3:F16223@14, k=10 → Emb:" sea"@14 (de=19.88) +9 more |
| 171 | `get_upstream_features` | L6:F5342@4, k=10 → Emb:" first"@2 (de=12.06) +9 more |
| 172 | `get_upstream_features` | L5:F14591@10, k=10 → Emb:" abbey"@10 (de=10.00) +9 more |
| 173 | `get_upstream_features` | L4:F4605@10, k=10 → Emb:" abbey"@10 (de=7.97) +9 more |
| 174 | `get_upstream_features` | L4:F4605@9, k=10 → Emb:"led"@9 (de=6.44) +9 more |
| 175 | `get_upstream_features` | L4:F4605@27, k=10 → Emb:" abbey"@27 (de=6.56) +9 more |
| 176 | `get_upstream_features` | L5:F14591@27, k=10 → Emb:" abbey"@27 (de=8.81) +9 more |
| 177 | `get_upstream_features` | L4:F4605@14, k=10 → ❌ Feature (layer=4, feature_idx=4605) not found at pos=14. Thi |
| 178 | `get_upstream_features` | L4:F4605@4, k=10 → ❌ Feature (layer=4, feature_idx=4605) not found at pos=4. This |
| 179 | `get_upstream_features` | L6:F5342@4, k=10 → Emb:" first"@2 (de=12.06) +9 more |
| 180 | `get_upstream_features` | L4:F3833@3, k=10 → Emb:" glimpse"@3 (de=13.56) +9 more |
| 181 | `get_upstream_features` | L4:F4605@8, k=10 → Emb:" steep"@8 (de=13.50) +9 more |
| 182 | `get_upstream_features` | L4:F4605@27, k=10 → Emb:" abbey"@27 (de=6.56) +9 more |
| 183 | `get_upstream_features` | L4:F4605@9, k=10 → Emb:"led"@9 (de=6.44) +9 more |
| 184 | `get_upstream_features` | L4:F4605@10, k=10 → Emb:" abbey"@10 (de=7.97) +9 more |
| 185 | `get_upstream_features` | L2:F8185@27, k=10 → Emb:" abbey"@27 (de=8.38) +9 more |
| 186 | `get_upstream_features` | L0:F9320@27, k=10 → Emb:" abbey"@27 (de=8.94) +9 more |
| 187 | `get_upstream_features` | L1:F8633@27, k=10 → Emb:" abbey"@10 (de=2.44) +9 more |
| 188 | `get_upstream_features` | L4:F1104@27, k=10 → Emb:" abbey"@10 (de=3.36) +9 more |
| 189 | `get_upstream_features` | L0:F3512@10, k=10 → Emb:" abbey"@10 (de=9.88) +9 more |
| 190 | `get_upstream_features` | L0:F9026@10, k=10 → Emb:" abbey"@10 (de=37.50) +9 more |
| 191 | `get_upstream_features` | L5:F14591@27, k=10 → Emb:" abbey"@27 (de=8.81) +9 more |
| 192 | `get_upstream_features` | L4:F4173@14, k=10 → Emb:" sea"@14 (de=21.62) +9 more |
| 193 | `get_upstream_features` | L6:F3848@14, k=10 → Emb:" sea"@14 (de=14.69) +9 more |
| 194 | `get_upstream_features` | L10:F6708@14, k=10 → Emb:" sea"@14 (de=6.47) +9 more |
| 195 | `get_upstream_features` | L0:F6609@2, k=10 → ❌ Feature (layer=0, pos=2, feature_idx=6609) not found in grap |
| 196 | `get_upstream_features` | L1:F5053@2, k=10 → Emb:" first"@2 (de=20.62) +9 more |
| 197 | `get_upstream_features` | L0:F4040@2, k=10 → Emb:"That"@1 (de=16.88) +9 more |
| 198 | `get_upstream_features` | L3:F11165@2, k=10 → Emb:" first"@2 (de=23.75) +9 more |
| 199 | `get_upstream_features` | L0:F7056@2, k=10 → Emb:" first"@2 (de=30.62) +9 more |
| 200 | `get_upstream_features` | L2:F5878@9, k=10 → Emb:" steep"@8 (de=8.56) +9 more |
| 201 | `get_upstream_features` | L2:F6145@9, k=10 → Emb:"led"@9 (de=35.75) +9 more |
| 202 | `get_upstream_features` | L3:F4081@9, k=10 → Emb:" steep"@8 (de=11.44) +9 more |
| 203 | `get_upstream_features` | L1:F5053@2, k=10 → Emb:" first"@2 (de=20.62) +9 more |
| 204 | `get_upstream_features` | L4:F4605@8, k=10 → Emb:" steep"@8 (de=13.50) +9 more |
| 205 | `get_upstream_features` | L4:F4605@9, k=10 → Emb:"led"@9 (de=6.44) +9 more |
| 206 | `get_upstream_features` | L4:F4605@10, k=10 → Emb:" abbey"@10 (de=7.97) +9 more |
| 207 | `get_upstream_features` | L4:F4605@27, k=10 → Emb:" abbey"@27 (de=6.56) +9 more |
| 208 | `get_upstream_features` | L5:F14591@10, k=10 → Emb:" abbey"@10 (de=10.00) +9 more |
| 209 | `get_upstream_features` | L5:F14591@27, k=10 → Emb:" abbey"@27 (de=8.81) +9 more |
| 210 | `get_upstream_features` | L4:F4605@8, k=10 → Emb:" steep"@8 (de=13.50) +9 more |
| 211 | `get_upstream_features` | L4:F4605@27, k=10 → Emb:" abbey"@27 (de=6.56) +9 more |
| 212 | `get_upstream_features` | L5:F14591@10, k=10 → Emb:" abbey"@10 (de=10.00) +9 more |
| 213 | `get_upstream_features` | L5:F14591@27, k=10 → Emb:" abbey"@27 (de=8.81) +9 more |
| 214 | `get_upstream_features` | L9:F15289@29, k=10 → Emb:" not"@29 (de=2.58) +9 more |
| 215 | `get_upstream_features` | L6:F12349@29, k=10 → Emb:" not"@29 (de=7.94) +9 more |
| 216 | `get_upstream_features` | L8:F3907@29, k=10 → Emb:" not"@29 (de=5.91) +9 more |
| 217 | `get_upstream_features` | L9:F14687@29, k=10 → Emb:" not"@29 (de=7.44) +9 more |
| 218 | `get_upstream_features` | L4:F2332@29, k=10 → Emb:" not"@29 (de=21.25) +9 more |
| 219 | `get_upstream_features` | L5:F14591@10, k=10 → Emb:" abbey"@10 (de=10.00) +9 more |
| 220 | `get_upstream_features` | L5:F14591@27, k=10 → Emb:" abbey"@27 (de=8.81) +9 more |
| 221 | `get_upstream_features` | L15:F10071@29, k=10 → Emb:" not"@29 (de=9.75) +9 more |
| 222 | `get_upstream_features` | L4:F4492@23, k=10 → Emb:" not"@23 (de=18.50) +9 more |
| 223 | `get_upstream_features` | L15:F3521@23, k=10 → Emb:" will"@22 (de=5.91) +9 more |
| 224 | `get_upstream_features` | L4:F2422@29, k=10 → Emb:" not"@29 (de=17.50) +9 more |
| 225 | `get_upstream_features` | L4:F2422@23, k=10 → Emb:" not"@23 (de=16.88) +9 more |
| 226 | `get_upstream_features` | L14:F15790@29, k=10 → Emb:" not"@29 (de=6.16) +9 more |
| 227 | `get_upstream_features` | L5:F14591@10, k=10 → Emb:" abbey"@10 (de=10.00) +9 more |
| 228 | `get_upstream_features` | L5:F14591@27, k=10 → Emb:" abbey"@27 (de=8.81) +9 more |
| 229 | `get_upstream_features` | L4:F4605@10, k=10 → Emb:" abbey"@10 (de=7.97) +9 more |
| 230 | `get_upstream_features` | L4:F4605@9, k=10 → Emb:"led"@9 (de=6.44) +9 more |
| 231 | `get_upstream_features` | L4:F4605@8, k=10 → Emb:" steep"@8 (de=13.50) +9 more |
| 232 | `get_upstream_features` | L4:F4605@27, k=10 → Emb:" abbey"@27 (de=6.56) +9 more |

### Build

`build_circuit` → 26 nodes, 25 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 175,045 | 30,837 | 1,296,681 | 0 | $0.1673 | — | — |
| **Total** | | **175,045** | **30,837** | **1,296,681** | **0** | **$0.1673** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 2s