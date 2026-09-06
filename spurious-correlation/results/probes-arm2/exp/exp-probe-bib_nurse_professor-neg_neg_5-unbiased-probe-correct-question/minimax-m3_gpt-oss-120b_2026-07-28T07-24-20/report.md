# Circuit Oracle Report
**Date:** 2026-07-28 07:24:20 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by a mix of genuine profession-related signals (academic degrees and field tokens) and a spurious gender-marker signal from "His", with the largest single positive driver being the pronoun rather than any profession content word.

**Confidence:** 7

**Reasoning:** The user concern is partially supported by the circuit. Tracing the top features feeding the probe reveals several distinct pathways:

1. **Gender marker (spurious):** L0:F1069 at pos 1 fires on the "His" embedding (direct_effect 21.6 from "His" → this feature, then +0.055 direct effect to the probe). L0:F6051 at pos 9 (the period after "history.") also gets large positive direct effect (+0.075), partly driven by pos-1 features that themselves respond to "His" — so the period's activation is entangled with the "His" context via the bos-attending L0 features. These are the largest *positive* single-token contributors to the probe.

2. **Genuine profession indicators:** The "interests" token feature (L1:F10986, L0:F6113) at pos 3 contributes positively (+0.065), and the "transnational" / "history" / "Harvard" features (L6:L4–L8 layers) form a real academic-field pathway. The "Ph.D." token at pos 15 activates a strong circuit (L1:L7 features including L7:F14129, L2:F10852, L1:F10132) that also feeds positively. "B.A." at pos 29 follows the same pattern.

3. **Mixed/late-layer features:** L20:F14235 at pos 19 and 33 (very high activation ~105 and ~89) feeds *negatively* into the probe (-0.056, -0.051) — this feature attends to "from" tokens and late-layer education-context, suggesting it represents a generic "degree-institution" template rather than profession content.

The single largest direct-effect feature on the probe is L0:F6051 (period punctuation, +0.075), whose upstream is dominated by the "His"-pos-1 L0 features and the "." token itself. The "His" pronoun at pos 1, through L0:F1069, is the second-largest positive single-feature contributor (+0.055). This is a textbook spurious-correlation signature: a probe supposedly classifying profession leans on a gendered pronoun, with profession-relevant features (degree names, "History", "transnational") present but secondary in magnitude. However, the *negative*-direct-effect features (L8:F2383 on "history" at -0.090, L6:F14747 at -0.065, L2:F10852 at pos 15 at -0.065) are also substantial, complicating the picture — the probe direction is being pushed in opposing directions by different content tokens. The overall pattern supports the user's concern that gender/pronominal context is one of the strongest single signals, though genuine field/degree tokens also contribute.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Gender Marker: 'His' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 9 | Generic period/punctuation features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F1903](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1903) | 1 | Generic period/punctuation features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1903) |
| [L0:F2405](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2405) | 1 | Generic period/punctuation features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2405) |
| [L0:F310](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/310) | 1 | Generic period/punctuation features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/310) |
| [L1:F10986](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) | 3 | 'interests' token feature (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) |
| [L0:F6113](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6113) | 3 | 'interests' token feature (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6113) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 15 | 'Ph.D.' token recognition (pos 13-15) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 15 | 'Ph.D.' token recognition (pos 13-15) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L1:F10132](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) | 15 | 'Ph.D.' token recognition (pos 13-15) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) |
| [L3:F8294](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8294) | 15 | 'Ph.D.' token recognition (pos 13-15) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8294) |
| [L4:F13943](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13943) | 15 | 'Ph.D.' token recognition (pos 13-15) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13943) |
| [L2:F13360](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13360) | 15 | 'Ph.D.' token recognition (pos 13-15) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13360) |
| [L3:F15899](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15899) | 15 | 'Ph.D.' token recognition (pos 13-15) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15899) |
| [L8:F2383](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2383) | 8 | 'History' / 'transnational business history' field tokens (pos 6-8) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2383) |
| [L6:F14747](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14747) | 8 | 'History' / 'transnational business history' field tokens (pos 6-8) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14747) |
| [L6:F13001](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/13001) | 8 | 'History' / 'transnational business history' field tokens (pos 6-8) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/13001) |
| [L4:F14134](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14134) | 8 | 'History' / 'transnational business history' field tokens (pos 6-8) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14134) |
| [L6:F2161](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2161) | 6 | 'transnational' token (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2161) |
| [L4:F16301](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/16301) | 6 | 'transnational' token (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/16301) |
| [L6:F3235](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) | 20 | 'Harvard' university token (pos 20) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) |
| [L4:F9333](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9333) | 20 | 'Harvard' university token (pos 20) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9333) |
| [L4:F5150](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5150) | 20 | 'Harvard' university token (pos 20) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5150) |
| [L20:F14235](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) | 19 | 'received his Ph.D. ... from' / 'B.A. ... from' (pos 11-19, 27-33) | — | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) |
| [L20:F14235](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) | 33 | 'received his Ph.D. ... from' / 'B.A. ... from' (pos 11-19, 27-33) | — | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) |
| [L17:F11003](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) | 19 | 'received his Ph.D. ... from' / 'B.A. ... from' (pos 11-19, 27-33) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) |
| [L17:F11003](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) | 33 | 'received his Ph.D. ... from' / 'B.A. ... from' (pos 11-19, 27-33) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) |
| [L19:F2496](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2496) | 19 | 'received his Ph.D. ... from' / 'B.A. ... from' (pos 11-19, 27-33) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2496) |
| [L19:F2496](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2496) | 33 | 'received his Ph.D. ... from' / 'B.A. ... from' (pos 11-19, 27-33) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2496) |
| [L17:F7973](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7973) | 19 | 'received his Ph.D. ... from' / 'B.A. ... from' (pos 11-19, 27-33) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7973) |
| [L17:F7973](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7973) | 33 | 'received his Ph.D. ... from' / 'B.A. ... from' (pos 11-19, 27-33) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7973) |
| [L14:F3956](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3956) | 19 | 'received his Ph.D. ... from' / 'B.A. ... from' (pos 11-19, 27-33) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3956) |
| [L14:F3956](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3956) | 33 | 'received his Ph.D. ... from' / 'B.A. ... from' (pos 11-19, 27-33) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3956) |
| [L16:F6447](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6447) | 19 | 'received his Ph.D. ... from' / 'B.A. ... from' (pos 11-19, 27-33) | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6447) |
| [L15:F14312](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/14312) | 19 | 'received his Ph.D. ... from' / 'B.A. ... from' (pos 11-19, 27-33) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/14312) |
| [L15:F4934](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/4934) | 15 | 'received his Ph.D. ... from' / 'B.A. ... from' (pos 11-19, 27-33) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/4934) |
| [L8:F12026](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/12026) | 15 | 'received his Ph.D. ... from' / 'B.A. ... from' (pos 11-19, 27-33) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/12026) |
| [L3:F4213](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) | 19 | 'received his Ph.D. ... from' / 'B.A. ... from' (pos 11-19, 27-33) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 29 | 'B.A.' / degree token (pos 27-29) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F13360](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13360) | 29 | 'B.A.' / degree token (pos 27-29) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13360) |
| [L9:F988](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/988) | 29 | 'B.A.' / degree token (pos 27-29) | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/988) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 29 | 'B.A.' / degree token (pos 27-29) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 29 | 'B.A.' / degree token (pos 27-29) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L8:2383 de=-0.090 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L20:F14235@19` | ❌ error | — | — | Trace the path from L20:F14235 at position 19 upstream. This feature has a very … |
| SA-2 | `L0:F6051@9` | ❌ error | — | — | Trace the path from L0:F6051 at position 9 upstream. This is a positive direct e… |
| SA-3 | `L1:F10986@3` | ❌ error | — | — | Trace the path from L1:F10986 at position 3 upstream. This is a positive direct … |
| SA-4 | `L0:F1069@1` | ❌ error | — | — | Trace the path from L0:F1069 at position 1 upstream. This is a positive direct e… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F6051@9, k=15 → Emb:"."@9 (de=45.50) +14 more |
| 2 | `get_upstream_features` | L1:F10986@3, k=15 → Emb:" research"@2 (de=6.62) +14 more |
| 3 | `get_upstream_features` | L0:F1069@1, k=15 → Emb:"His"@1 (de=21.62) +14 more |
| 4 | `get_upstream_features` | L7:F14129@15, k=15 → L6:F2254 (de=7.09) +14 more |
| 5 | `get_upstream_features` | L20:F14235@19, k=15 → L17:F11003 (de=34.00) +14 more |
| 6 | `get_upstream_features` | L17:F11003@19, k=15 → Emb:"<bos>"@0 (de=-6.72) +14 more |
| 7 | `get_upstream_features` | L19:F2496@19, k=15 → L17:F11003 (de=15.69) +14 more |
| 8 | `get_upstream_features` | L6:F2254@15, k=15 → L2:F10852 (de=12.31) +14 more |
| 9 | `get_upstream_features` | L5:F13801@15, k=10 → L2:F10852 (de=7.22) +9 more |
| 10 | `get_upstream_features` | L1:F10132@15, k=10 → Emb:" Ph"@13 (de=16.25) +9 more |
| 11 | `get_upstream_features` | L3:F8294@15, k=10 → L2:F10852 (de=7.09) +9 more |
| 12 | `get_upstream_features` | L2:F10852@15, k=10 → Emb:" Ph"@13 (de=14.00) +9 more |
| 13 | `get_upstream_features` | L4:F13943@15, k=10 → L2:F10852 (de=7.72) +9 more |
| 14 | `get_upstream_features` | L8:F2383@8, k=15 → Emb:" history"@8 (de=5.59) +14 more |
| 15 | `get_upstream_features` | L6:F14747@8, k=10 → Emb:" history"@8 (de=6.25) +9 more |
| 16 | `get_upstream_features` | L8:F11284@9, k=10 → Emb:" research"@2 (de=3.89) +9 more |
| 17 | `get_upstream_features` | L14:F3956@19, k=10 → Emb:"<bos>"@0 (de=-4.84) +9 more |
| 18 | `get_upstream_features` | L6:F2161@6, k=10 → Emb:" transnational"@6 (de=8.12) +9 more |
| 19 | `get_upstream_features` | L6:F3235@20, k=10 → Emb:" Harvard"@20 (de=7.78) +9 more |
| 20 | `get_upstream_features` | L6:F13001@8, k=10 → Emb:" history"@8 (de=14.06) +9 more |
| 21 | `get_upstream_features` | L4:F14134@8, k=10 → Emb:" history"@8 (de=23.00) +9 more |
| 22 | `get_upstream_features` | L3:F4213@19, k=10 → Emb:" from"@19 (de=11.12) +9 more |
| 23 | `get_upstream_features` | L2:F13360@15, k=10 → Emb:" Ph"@13 (de=8.00) +9 more |
| 24 | `get_upstream_features` | L0:F6113@3, k=10 → Emb:" interests"@3 (de=14.19) +9 more |
| 25 | `get_upstream_features` | L17:F7973@19, k=10 → L16:F6447 (de=10.44) +9 more |
| 26 | `get_upstream_features` | L9:F988@29, k=10 → L6:F2254 (de=5.50) +9 more |
| 27 | `get_upstream_features` | L20:F14235@33, k=10 → L17:F11003 (de=23.62) +9 more |
| 28 | `get_upstream_features` | L20:F14235@29, k=5 → ❌ Feature (layer=20, feature_idx=14235) not found at pos=29. T |
| 29 | `get_upstream_features` | L17:F11003@33, k=5 → L15:F4934 (de=7.81) +4 more |
| 30 | `get_upstream_features` | L19:F2496@33, k=5 → L17:F11003 (de=11.19) +4 more |
| 31 | `get_upstream_features` | L16:F6447@19, k=10 → L15:F14312 (de=11.12) +9 more |
| 32 | `get_upstream_features` | L7:F14291@19, k=10 → L5:F5725 (de=-1.41) +9 more |
| 33 | `get_upstream_features` | L2:F13360@29, k=10 → Emb:"A"@29 (de=2.58) +9 more |
| 34 | `get_upstream_features` | L2:F10852@29, k=5 → Emb:" B"@27 (de=12.38) +4 more |

### Build

`build_circuit` → 23 nodes, 24 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 25,719 | 8,228 | 117,823 | 0 | $0.0247 | — | — |
| **Total** | | **25,719** | **8,228** | **117,823** | **0** | **$0.0247** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 34s