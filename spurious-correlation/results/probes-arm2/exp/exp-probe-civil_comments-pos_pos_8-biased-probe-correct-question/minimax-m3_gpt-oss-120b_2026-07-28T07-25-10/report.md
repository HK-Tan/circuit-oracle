# Circuit Oracle Report
**Date:** 2026-07-28 07:25:10 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_8 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity probe's classification score is driven primarily by features that fire on the token "Islam" (pos 4), with a secondary contribution from features firing on "false" (pos 10) and the literal period at pos 12, confirming the user's concern that the circuit relies heavily on identity-group signal rather than the prompt's toxic content (e.g., "Lucifer", "false religion").

**Confidence:** 8

**Reasoning:** The top-3 features by direct effect on the probe score (L6:F7282 = +0.41, L4:F2405 = +0.32, L8:F13197 = +0.26) all activate at pos 4 — the word "Islam". Tracing L6:F7282 upstream reveals an almost-clean feed from the `Emb: Islam (pos 4)` token embedding (direct_effect 18.5 from the embedding itself), which propagates through L0:F13885 (also firing on the Islam token embedding, direct_effect 12.25 from that embedding) into L4:F2405 (which itself receives 21.5 direct effect from the "Islam" embedding) and L5:F14348. These mid-layer features compose with L1:F4314 and L2:F7214 — both of which also receive nearly their entire activation from the "Islam" token embedding (direct_effects 16.5 and 12.4 from that embedding, respectively). The "Islam"-centered path is overwhelmingly lexical/identity-based: the model's representation of the word "Islam" alone, rather than its semantic context, drives the probe.

A secondary path runs through "false" (pos 10). L12:F7779 (direct_effect 0.14 to probe) receives its strongest input from the "false" embedding (direct_effect 7.16), via L2:F13635 (which receives 27.6 from the "false" embedding) and L2:F2266 (18.9 from "false"). The syntactic period L0:F6051 (direct_effect 0.16) receives nearly all its input from the "." embedding (direct_effect 46.5) — a pure punctuation artifact. Even the inhibitory features on "Islam" (e.g., L1:F4314 at -0.24, L3:F12024 at -0.22) trace back to the "Islam" token embedding.

Critically, **no feature in the top-15 direct-effect list or in their upstream chains activates on "Lucifer" (pos 13) or "religion" (pos 11) with positive direct effect on the probe score.** The phrase "Allah is Lucifer" — the actual toxic content of the prompt — is essentially absent from the probe-driving circuit. The dominant signal is "the token Islam is present," with auxiliary contributions from "the word false is present" and "a period appears after a non-religious content word." This confirms the user's concern: the probe classification is driven by **identity-group tokens and generic syntactic/lexical cues**, not by the prompt's actual hateful or toxic semantic content.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L6:F7282](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) | 4 | Late-layer 'Islam' detectors (pos 4) — drive probe | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) |
| [L4:F2405](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) | 4 | Late-layer 'Islam' detectors (pos 4) — drive probe | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) |
| [L8:F13197](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13197) | 4 | Late-layer 'Islam' detectors (pos 4) — drive probe | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13197) |
| [L10:F2716](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/2716) | 4 | Late-layer 'Islam' detectors (pos 4) — drive probe | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/2716) |
| [L6:F3265](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3265) | 4 | Late-layer 'Islam' detectors (pos 4) — drive probe | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3265) |
| [L7:F14049](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14049) | 4 | Late-layer 'Islam' detectors (pos 4) — drive probe | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14049) |
| [L5:F14348](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14348) | 4 | Mid-layer 'Islam' compositional features (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14348) |
| [L5:F6490](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6490) | 4 | Mid-layer 'Islam' compositional features (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6490) |
| [L5:F6331](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6331) | 4 | Mid-layer 'Islam' compositional features (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6331) |
| [L4:F7545](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7545) | 4 | Mid-layer 'Islam' compositional features (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7545) |
| [L4:F16231](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/16231) | 4 | Mid-layer 'Islam' compositional features (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/16231) |
| [L4:F14857](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14857) | 4 | Mid-layer 'Islam' compositional features (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14857) |
| [L4:F9806](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9806) | 4 | Mid-layer 'Islam' compositional features (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9806) |
| [L4:F5065](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5065) | 4 | Mid-layer 'Islam' compositional features (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5065) |
| [L3:F12024](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12024) | 4 | Mid-layer 'Islam' compositional features (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12024) |
| [L3:F3205](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3205) | 4 | Mid-layer 'Islam' compositional features (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3205) |
| [L7:F12448](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/12448) | 4 | Mid-layer 'Islam' compositional features (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/12448) |
| [L7:F4618](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4618) | 4 | Mid-layer 'Islam' compositional features (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4618) |
| [L6:F1152](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1152) | 4 | Mid-layer 'Islam' compositional features (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1152) |
| [L6:F2267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2267) | 4 | Mid-layer 'Islam' compositional features (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2267) |
| [L6:F8487](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8487) | 4 | Mid-layer 'Islam' compositional features (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8487) |
| [L6:F14783](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14783) | 4 | Mid-layer 'Islam' compositional features (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14783) |
| [L6:F11713](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11713) | 4 | Mid-layer 'Islam' compositional features (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11713) |
| [L8:F3099](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/3099) | 4 | Mid-layer 'Islam' compositional features (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/3099) |
| [L0:F13885](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13885) | 4 | Early 'Islam' token-embedding features (L0-L2, pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13885) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 4 | Early 'Islam' token-embedding features (L0-L2, pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F3031](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3031) | 4 | Early 'Islam' token-embedding features (L0-L2, pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3031) |
| [L0:F4470](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4470) | 4 | Early 'Islam' token-embedding features (L0-L2, pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4470) |
| [L0:F10120](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10120) | 4 | Early 'Islam' token-embedding features (L0-L2, pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10120) |
| [L0:F3512](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3512) | 4 | Early 'Islam' token-embedding features (L0-L2, pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3512) |
| [L1:F4314](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4314) | 4 | Early 'Islam' token-embedding features (L0-L2, pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4314) |
| [L1:F12107](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12107) | 4 | Early 'Islam' token-embedding features (L0-L2, pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12107) |
| [L1:F2352](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2352) | 4 | Early 'Islam' token-embedding features (L0-L2, pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2352) |
| [L1:F14137](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14137) | 4 | Early 'Islam' token-embedding features (L0-L2, pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14137) |
| [L2:F7214](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7214) | 4 | Early 'Islam' token-embedding features (L0-L2, pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7214) |
| [L2:F15823](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15823) | 4 | Early 'Islam' token-embedding features (L0-L2, pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15823) |
| [L2:F6894](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6894) | 4 | Early 'Islam' token-embedding features (L0-L2, pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6894) |
| [L12:F7779](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/7779) | 10 | Late-layer 'false' detectors (pos 10) — secondary driver | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/7779) |
| [L8:F16036](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16036) | 10 | Late-layer 'false' detectors (pos 10) — secondary driver | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16036) |
| [L8:F4462](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/4462) | 10 | Late-layer 'false' detectors (pos 10) — secondary driver | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/4462) |
| [L2:F2266](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2266) | 10 | Late-layer 'false' detectors (pos 10) — secondary driver | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2266) |
| [L2:F4053](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4053) | 10 | Late-layer 'false' detectors (pos 10) — secondary driver | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4053) |
| [L2:F13635](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13635) | 10 | Late-layer 'false' detectors (pos 10) — secondary driver | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13635) |
| [L0:F2703](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2703) | 10 | Early 'false' token-embedding features (L0-L1, pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2703) |
| [L0:F7445](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7445) | 10 | Early 'false' token-embedding features (L0-L1, pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7445) |
| [L0:F5977](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5977) | 10 | Early 'false' token-embedding features (L0-L1, pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5977) |
| [L0:F12087](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12087) | 10 | Early 'false' token-embedding features (L0-L1, pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12087) |
| [L1:F9521](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9521) | 10 | Early 'false' token-embedding features (L0-L1, pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9521) |
| [L1:F11171](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11171) | 10 | Early 'false' token-embedding features (L0-L1, pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11171) |
| [L3:F14698](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14698) | 3 | Phrase-context features on 'problem with' (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14698) |
| [L3:F8595](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8595) | 3 | Phrase-context features on 'problem with' (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8595) |
| [L3:F1395](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1395) | 3 | Phrase-context features on 'problem with' (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1395) |
| [L2:F12222](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12222) | 3 | Phrase-context features on 'problem with' (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12222) |
| [L0:F14656](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14656) | 2 | Phrase-context features on 'problem with' (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14656) |
| [L0:F6855](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6855) | 2 | Phrase-context features on 'problem with' (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6855) |
| [L1:F9523](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9523) | 3 | Phrase-context features on 'problem with' (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9523) |
| [L1:F16351](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/16351) | 2 | Phrase-context features on 'problem with' (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/16351) |
| [L1:F7816](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7816) | 3 | Phrase-context features on 'problem with' (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7816) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 12 | Syntactic period (pos 12) — neutral punctuation | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:7282 de=0.410 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F7282@4` | ❌ error | — | — | Trace the path from L6:F7282 (pos 4, on 'Islam'). This feature has the highest p… |
| SA-2 | `L4:F2405@4` | ❌ error | — | — | Trace the path from L4:F2405 (pos 4, on 'Islam'). This feature has the second-hi… |
| SA-3 | `L8:F13197@4` | ❌ error | — | — | Trace the path from L8:F13197 (pos 4, on 'Islam'). This feature has the third-hi… |
| SA-4 | `L0:F6051@12` | ❌ error | — | — | Trace the path from L0:F6051 (pos 12, high activation 38.75). This early-layer f… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F7282@4, k=10 → Emb:" Islam"@4 (de=18.50) +9 more |
| 2 | `get_upstream_features` | L4:F2405@4, k=10 → Emb:" Islam"@4 (de=21.50) +9 more |
| 3 | `get_upstream_features` | L8:F13197@4, k=10 → Emb:" Islam"@4 (de=9.25) +9 more |
| 4 | `get_upstream_features` | L0:F6051@12, k=10 → Emb:"."@12 (de=46.50) +9 more |
| 5 | `get_upstream_features` | L0:F13885@4, k=10 → Emb:" Islam"@4 (de=12.25) +9 more |
| 6 | `get_upstream_features` | L6:F3265@4, k=10 → Emb:" Islam"@4 (de=6.12) +9 more |
| 7 | `get_upstream_features` | L7:F14049@4, k=10 → Emb:" Islam"@4 (de=5.88) +9 more |
| 8 | `get_upstream_features` | L0:F880@7, k=10 → Emb:" it"@7 (de=44.00) +9 more |
| 9 | `get_upstream_features` | L5:F14348@4, k=10 → Emb:" Islam"@4 (de=6.72) +9 more |
| 10 | `get_upstream_features` | L4:F7545@4, k=10 → Emb:" Islam"@4 (de=8.25) +9 more |
| 11 | `get_upstream_features` | L4:F16231@4, k=10 → Emb:" Islam"@4 (de=7.66) +9 more |
| 12 | `get_upstream_features` | L10:F2716@4, k=10 → Emb:" Islam"@4 (de=3.03) +9 more |
| 13 | `get_upstream_features` | L3:F12024@4, k=10 → Emb:" Islam"@4 (de=8.44) +9 more |
| 14 | `get_upstream_features` | L1:F4314@4, k=10 → Emb:" Islam"@4 (de=16.50) +9 more |
| 15 | `get_upstream_features` | L1:F12107@4, k=10 → Emb:" Islam"@4 (de=14.31) +9 more |
| 16 | `get_upstream_features` | L1:F2352@4, k=10 → Emb:" Islam"@4 (de=15.69) +9 more |
| 17 | `get_upstream_features` | L2:F7214@4, k=10 → Emb:" Islam"@4 (de=12.38) +9 more |
| 18 | `get_upstream_features` | L4:F15997@3, k=10 → L3:F14698 (de=3.64) +9 more |
| 19 | `get_upstream_features` | L7:F12448@4, k=10 → Emb:" Islam"@4 (de=3.77) +9 more |
| 20 | `get_upstream_features` | L5:F6490@4, k=10 → Emb:" Islam"@4 (de=3.45) +9 more |
| 21 | `get_upstream_features` | L5:F6331@4, k=10 → Emb:" Islam"@4 (de=7.00) +9 more |
| 22 | `get_upstream_features` | L0:F9026@4, k=10 → Emb:" Islam"@4 (de=17.62) +9 more |
| 23 | `get_upstream_features` | L0:F2158@3, k=10 → Emb:" with"@3 (de=32.50) +9 more |
| 24 | `get_upstream_features` | L0:F10120@4, k=10 → Emb:" Islam"@4 (de=9.88) +9 more |
| 25 | `get_upstream_features` | L0:F4470@4, k=10 → Emb:" Islam"@4 (de=8.75) +9 more |
| 26 | `get_upstream_features` | L0:F3031@4, k=10 → Emb:" Islam"@4 (de=13.31) +9 more |
| 27 | `get_upstream_features` | L4:F14857@4, k=10 → Emb:"<bos>"@0 (de=-17.62) +9 more |
| 28 | `get_upstream_features` | L3:F3205@4, k=10 → Emb:"<bos>"@0 (de=-7.09) +9 more |
| 29 | `get_upstream_features` | L1:F14137@4, k=10 → Emb:"<bos>"@0 (de=16.88) +9 more |
| 30 | `get_upstream_features` | L3:F8595@3, k=10 → Emb:" problem"@2 (de=6.97) +9 more |
| 31 | `get_upstream_features` | L3:F14698@3, k=10 → Emb:" problem"@2 (de=14.62) +9 more |
| 32 | `get_upstream_features` | L3:F1395@3, k=10 → Emb:" with"@3 (de=15.44) +9 more |
| 33 | `get_upstream_features` | L12:F7779@10, k=10 → Emb:" false"@10 (de=7.16) +9 more |
| 34 | `get_upstream_features` | L2:F13635@10, k=10 → Emb:" false"@10 (de=27.62) +9 more |
| 35 | `get_upstream_features` | L8:F16036@10, k=10 → Emb:" Islam"@4 (de=1.48) +9 more |
| 36 | `get_upstream_features` | L8:F4462@10, k=10 → Emb:" false"@10 (de=3.28) +9 more |
| 37 | `get_upstream_features` | L1:F9521@10, k=10 → Emb:" false"@10 (de=16.25) +9 more |
| 38 | `get_upstream_features` | L2:F4053@10, k=10 → Emb:" false"@10 (de=6.81) +9 more |
| 39 | `get_upstream_features` | L0:F2703@10, k=10 → Emb:" false"@10 (de=19.50) +9 more |
| 40 | `get_upstream_features` | L1:F11171@10, k=10 → Emb:" false"@10 (de=15.00) +9 more |
| 41 | `get_upstream_features` | L0:F5977@10, k=10 → Emb:" false"@10 (de=16.75) +9 more |
| 42 | `get_upstream_features` | L2:F2266@10, k=10 → Emb:" false"@10 (de=18.88) +9 more |
| 43 | `get_upstream_features` | L0:F7445@10, k=10 → Emb:" false"@10 (de=11.88) +9 more |
| 44 | `get_upstream_features` | L1:F9523@3, k=10 → Emb:" problem"@2 (de=8.06) +9 more |
| 45 | `get_upstream_features` | L2:F12222@3, k=10 → Emb:"The"@1 (de=8.00) +9 more |
| 46 | `get_upstream_features` | L0:F14656@2, k=10 → Emb:" problem"@2 (de=16.38) +9 more |
| 47 | `get_upstream_features` | L0:F6855@2, k=10 → Emb:" problem"@2 (de=21.88) +9 more |
| 48 | `get_upstream_features` | L0:F15530@2, k=10 → Emb:" problem"@2 (de=15.50) +9 more |
| 49 | `get_upstream_features` | L1:F16351@2, k=10 → Emb:" problem"@2 (de=25.75) +9 more |
| 50 | `get_upstream_features` | L6:F2267@4, k=10 → Emb:"<bos>"@0 (de=-6.31) +9 more |
| 51 | `get_upstream_features` | L8:F3099@4, k=10 → Emb:"<bos>"@0 (de=-31.38) +9 more |
| 52 | `get_upstream_features` | L6:F1152@4, k=10 → Emb:" Islam"@4 (de=4.47) +9 more |
| 53 | `get_upstream_features` | L6:F8487@4, k=10 → Emb:" Islam"@4 (de=6.84) +9 more |
| 54 | `get_upstream_features` | L6:F14783@4, k=10 → Emb:"<bos>"@0 (de=2.66) +9 more |
| 55 | `get_upstream_features` | L3:F14698@3, k=8 → Emb:" problem"@2 (de=14.62) +7 more |
| 56 | `get_upstream_features` | L3:F8595@3, k=8 → Emb:" problem"@2 (de=6.97) +7 more |
| 57 | `get_upstream_features` | L6:F5889@10, k=8 → Emb:" false"@10 (de=5.25) +7 more |
| 58 | `get_upstream_features` | L7:F4618@4, k=8 → Emb:" Islam"@4 (de=12.56) +7 more |

### Build

`build_circuit` → 17 nodes, 17 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 35,306 | 8,599 | 211,456 | 0 | $0.0336 | — | — |
| **Total** | | **35,306** | **8,599** | **211,456** | **0** | **$0.0336** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 0s