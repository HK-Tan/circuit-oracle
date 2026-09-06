# Circuit Oracle Report
**Date:** 2026-07-28 07:21:39 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction probe is driven primarily by a tall L4 feature on the word "castle" (pos 2) that encodes "land ownership / ancient fortifications" semantics, chained into L5–L6 Irish/Scottish geographic features on the singular "house" at pos 14 — i.e., the circuit is responding to **lexical co-occurrence of castle/early-fortification vocabulary with archaic "house" usage**, not to the actual semantic contradiction between premise and hypothesis.

**Confidence:** 6

**Reasoning:** The user's hypothesis is **partially supported but incomplete** — the circuit is not the textbook "negation-word" shortcut, but it is still a largely surface-level shortcut rather than a true contradiction detector.

**Direct evidence for content-related signal:**
- The single largest positive driver, **L4:F13244** (0.287 direct_effect, "land ownership / ancient fortifications / slavery"), traces cleanly back to the embedding of the word `▁ castle` (pos 2, direct_effect 18.5). The "castle" token is genuinely content-relevant and this feature does encode something domain-appropriate.
- An L2 cluster on "castle" (F8185 "places for shopping/military activities", F9529 "slavery", F12263 "agriculture/mining/slavery", F8734 "geographical/political centers", F6878 "nature-related locations") and L2:F4429 firing on `▁ early` at both pos 6 (premise) and pos 39 (hypothesis "early 17th-century") all reflect real lexical content of the prompt.

**Direct evidence for the user's "spurious" concern:**
- The L2:F1430 "U.S. White House or generic house" at pos 14 has a **negative** direct_effect (-0.221) on the contradiction score — it is suppressing the probe. The premise uses the singular "house" (in "tower house"), so the model is treating this *absence* of a "real" house concept as evidence *against* contradiction, which is a content-sensitive signal.
- However, the **chain that pushes the score up** runs: L4 castle-property → L5:F3316 "Irish/Scottish geographic/cultural" on `▁ house` (pos 14) → L6:F486 "Scottish locations". This chain fires because the words "castle" + "tower" + "house" + "early" are typical of Wikipedia text about Irish/Scottish/British historic estates — the LLM is essentially classifying the *register* (heritage-Wikipedia style) rather than the entailment logic.
- The hypothesis mentions "does not contain any early 17th-century tower houses" (pos 35-39). The `▁ any` detector (L0:F10815, +0.117), `▁ does` (pos 35), `▁ not` (pos 36), and the L2:F4429 re-firing on the second "early" (pos 39, +0.119) do contribute — these are partly negation/quantifier signals but they fire on legitimate content words too.
- L3:F10598 "himself" (pos 3) has a negative effect (-0.114), pushing the prompt away from contradiction — this is anaphora tracking, content-relevant.
- L8:F8406 on the BOS token (pos 1, "I/Exactly", -0.108) is a generic prior that mildly suppresses the score.

**Conclusion:** The contradiction probe is **not** a pure negation-word detector. The strongest positive path is the L4 castle-property feature chained to Irish/Scottish heritage features on the singular "house" — this is a *topical/register* shortcut, not a semantic-contradiction circuit. The model is classifying "this looks like heritage-property Wikipedia text" rather than "premise and hypothesis contradict". The user's concern about non-content-based features is right in spirit: the actual entailment logic ("does not contain any" = negation) is barely represented (only weak contributions from `any` + `not` + second `early`), while lexical/heritage-register features dominate.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: ' castle' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: ' house' (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: ' tower' (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: 'century' (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: ' early' (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 39 | Emb: ' early' (pos 39, hypothesis) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: ' with' (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 26 | Emb: ' together' (pos 26) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 38 | Emb: ' any' (pos 38) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 16 | Emb: ' restored' (pos 16) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: ' itself' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: ' an' (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F1027](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1027) | 13 | Layer 0 single-word lexical detectors (content + function) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1027) |
| [L0:F4079](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4079) | 13 | Layer 0 single-word lexical detectors (content + function) |  the words "exposure," "tower" and words related to legal trials | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4079) |
| [L0:F10633](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10633) | 13 | Layer 0 single-word lexical detectors (content + function) |  the word "hill" and words associated with tall structures such as "tower" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10633) |
| [L0:F13200](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13200) | 13 | Layer 0 single-word lexical detectors (content + function) | mentions of archeology or the history of early civilization. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13200) |
| [L0:F2158](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) | 17 | Layer 0 single-word lexical detectors (content + function) | the word "with" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) |
| [L0:F7513](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7513) | 26 | Layer 0 single-word lexical detectors (content + function) | the word "together" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7513) |
| [L0:F10815](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10815) | 38 | Layer 0 single-word lexical detectors (content + function) |  the word "any". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10815) |
| [L0:F4367](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4367) | 12 | Layer 0 single-word lexical detectors (content + function) |  references to centuries | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4367) |
| [L0:F5494](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5494) | 6 | Layer 0 single-word lexical detectors (content + function) | the word "early" often related to time | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5494) |
| [L0:F8082](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8082) | 3 | Layer 0 single-word lexical detectors (content + function) | the word "itself" and sometimes words ending in "ing" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8082) |
| [L0:F11220](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11220) | 16 | Layer 0 single-word lexical detectors (content + function) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11220) |
| [L0:F14108](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14108) | 2 | Layer 0 single-word lexical detectors (content + function) | the word "appropriate" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14108) |
| [L0:F9604](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9604) | 14 | Layer 0 'house' word detectors (pos 14) |  the word "house" along with words about social class/gatherings | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9604) |
| [L0:F5198](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5198) | 14 | Layer 0 'house' word detectors (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5198) |
| [L1:F8479](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8479) | 13 | Layer 1 lexical composition: tower/house |  the word "rate" in the context of technical documents | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8479) |
| [L1:F14694](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14694) | 13 | Layer 1 lexical composition: tower/house | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14694) |
| [L1:F12474](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12474) | 2 | Layer 1 lexical composition: tower/house |  the word "technology" near other related words like "computer" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12474) |
| [L1:F8633](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8633) | 2 | Layer 1 lexical composition: tower/house |  words or phrases related to tourism and historical places | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8633) |
| [L1:F13073](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13073) | 2 | Layer 1 lexical composition: tower/house |  the word "projection" and words associated with it | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13073) |
| [L1:F12702](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12702) | 14 | Layer 1 lexical composition: tower/house | the word "house" or "homes" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12702) |
| [L2:F1430](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1430) | 14 | Layer 2 'house' (generic) at pos 14 — NEGATIVE driver | mentions of the U.S. White House or a generic house | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1430) |
| [L2:F1563](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1563) | 13 | Layer 2 'house' (generic) at pos 14 — NEGATIVE driver |  the word "tower" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1563) |
| [L2:F4429](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) | 6 | Layer 2 'beginning of period / early' (pos 6 & 39) |  mentions of the beginning of a period | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) |
| [L2:F4429](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) | 39 | Layer 2 'beginning of period / early' (pos 6 & 39) |  mentions of the beginning of a period | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) |
| [L2:F8185](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8185) | 2 | Layer 2 geographical / cultural / property features on ' castle' | places for shopping or military activities | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8185) |
| [L2:F9529](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9529) | 2 | Layer 2 geographical / cultural / property features on ' castle' |  words related to slavery and slave ownership | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9529) |
| [L2:F12263](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12263) | 2 | Layer 2 geographical / cultural / property features on ' castle' |  words related to agriculture/mining and to slavery/plantations | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12263) |
| [L2:F8734](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8734) | 2 | Layer 2 geographical / cultural / property features on ' castle' |  geographical names and political centers | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8734) |
| [L2:F6878](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6878) | 2 | Layer 2 geographical / cultural / property features on ' castle' |  nature-related locations and objects. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6878) |
| [L2:F9989](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9989) | 13 | Layer 2 geographical / cultural / property features on ' castle' |  the word "molecular" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9989) |
| [L3:F10598](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10598) | 3 | Layer 3 'himself/itself' (pos 3) — NEGATIVE driver | the word "himself" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10598) |
| [L3:F14368](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14368) | 14 | Layer 3 'himself/itself' (pos 3) — NEGATIVE driver | the word "house" (or houses). | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14368) |
| [L4:F13244](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) | 2 | Layer 4 'land ownership / ancient fortifications' on ' castle' (pos 2) — TOP POSITIVE driver |  terms related to land ownership and administration, possibly including slavery or other forms of forced labor | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) |
| [L4:F5749](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) | 2 | Layer 4 'land ownership / ancient fortifications' on ' castle' (pos 2) — TOP POSITIVE driver |  terms that describe ancient settlements and fortifications | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) |
| [L4:F3089](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3089) | 14 | Layer 4 'land ownership / ancient fortifications' on ' castle' (pos 2) — TOP POSITIVE driver |  words related to housing, especially apartments and condominiums | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3089) |
| [L4:F8583](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8583) | 14 | Layer 4 'land ownership / ancient fortifications' on ' castle' (pos 2) — TOP POSITIVE driver |  historical references including people, titles, and dates | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8583) |
| [L5:F3316](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3316) | 14 | Layer 5 Irish/Scottish geographic & noble-name features on ' house' (pos 14) | Irish or Scottish geographical or cultural references, including names and places. | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3316) |
| [L5:F1794](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1794) | 14 | Layer 5 Irish/Scottish geographic & noble-name features on ' house' (pos 14) |  titles and names of people, especially of nobility, often including first names and surnames | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1794) |
| [L6:F486](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/486) | 14 | Layer 6 'Scottish locations' (pos 14) |  Scottish locations and political terms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/486) |
| [L8:F8406](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) | 1 | Layer 8 'I/Exactly' on BOS (pos 1) — NEGATIVE driver | the first-person pronoun "I" and the word "Exactly" | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe direction (contradiction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:13244 de=0.287 |
| 3 | `inspect_feature` ×19 | L4:13244, L2:1430, L0:2158, L0:7360, L1:1027, L0:5494, L1:11220, L0:14108, L2:4429, L0:7513, L6:486, L0:8974, L4:5749, L3:10598, L0:4367, L0:10815, L0:8082, L0:4079, L8:8406 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F13244@2` | ❌ error | — | — | Trace the top positive feature L4:F13244 at pos 2 (label: 'land ownership/admini… |
| SA-2 | `L0:F10815@38` | ❌ error | — | — | Trace the feature L0:F10815 (word 'any') at position 38. Determine whether this … |
| SA-3 | `L0:F7513@26` | ❌ error | — | — | Trace the feature L0:F7513 (word 'together') at position 26. Determine if this i… |
| SA-4 | `L0:F2158@17` | ❌ error | — | — | Trace L0:F2158 (word 'with') at position 17. Find out if this is the 'with' in '… |
| SA-5 | `L2:F1430@14` | ❌ error | — | — | Trace L2:F1430 (label: 'U.S. White House or generic house') at pos 14. This has … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F13244@2, k=15 → Emb:" castle"@2 (de=18.50) +14 more |
| 2 | `get_upstream_features` | L2:F1430@14, k=15 → Emb:" house"@14 (de=30.88) +14 more |
| 3 | `get_upstream_features` | L0:F2158@17, k=15 → Emb:" with"@17 (de=33.75) +14 more |
| 4 | `get_upstream_features` | L0:F10815@38, k=15 → Emb:" any"@38 (de=40.50) +14 more |
| 5 | `get_upstream_features` | L0:F7513@26, k=15 → Emb:" together"@26 (de=43.00) +14 more |
| 6 | `get_upstream_features` | L0:F7360@5, k=15 → Emb:" an"@5 (de=27.38) +14 more |
| 7 | `get_upstream_features` | L1:F1027@13, k=15 → Emb:" tower"@13 (de=23.12) +14 more |
| 8 | `get_upstream_features` | L0:F5494@6, k=15 → Emb:" early"@6 (de=21.12) +14 more |
| 9 | `get_upstream_features` | L1:F11220@16, k=15 → Emb:" restored"@16 (de=20.00) +14 more |
| 10 | `get_upstream_features` | L0:F14108@2, k=15 → Emb:" castle"@2 (de=11.81) +14 more |
| 11 | `get_upstream_features` | L0:F4367@12, k=15 → Emb:"century"@12 (de=23.12) +14 more |
| 12 | `get_upstream_features` | L0:F8082@3, k=15 → Emb:" itself"@3 (de=19.88) +14 more |
| 13 | `get_upstream_features` | L0:F4079@13, k=15 → Emb:" tower"@13 (de=19.12) +14 more |
| 14 | `get_upstream_features` | L3:F10598@3, k=15 → Emb:" itself"@3 (de=30.12) +14 more |
| 15 | `get_upstream_features` | L6:F486@14, k=15 → L5:F3316 (de=-2.38) +14 more |
| 16 | `get_upstream_features` | L4:F5749@2, k=15 → Emb:" castle"@2 (de=14.75) +14 more |
| 17 | `get_upstream_features` | L8:F8406@1, k=15 → Emb:"<bos>"@0 (de=9.50) +14 more |
| 18 | `inspect_feature` ×23 | L2:8185, L1:8633, L1:12702, L0:9604, L0:2738, L3:14368, L2:1563, L2:9989, L4:3089, L4:8583, L5:1794, L5:3316, L0:14694, L0:4129, L1:8479, L2:8185, L2:9529, L2:12263, L2:8734, L2:6878, L1:12474, L1:13073, L1:5899 |
| 19 | `get_upstream_features` | L2:F4429@39, k=15 → Emb:" early"@39 (de=36.50) +14 more |
| 20 | `get_upstream_features` | L3:F10598@3, k=15 → Emb:" itself"@3 (de=30.12) +14 more |
| 21 | `get_upstream_features` | L4:F5749@2, k=15 → Emb:" castle"@2 (de=14.75) +14 more |
| 22 | `inspect_feature` ×5 | L1:1027, L0:10633, L0:13200, L0:11835, L0:8974 |

### Build

`build_circuit` → 24 nodes, 30 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 129,353 | 9,576 | 374,278 | 0 | $0.0728 | — | — |
| **Total** | | **129,353** | **9,576** | **374,278** | **0** | **$0.0728** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 19s