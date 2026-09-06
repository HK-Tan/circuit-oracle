# Circuit Oracle Report
**Date:** 2026-07-28 07:25:10 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_8 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction score is driven by features encoding the *actual prompt content* — the entity "Congress", the relational verbs "controls" / "no responsibility", the premise content "funding levels", and the counterexample "many members" — not by spurious negation-word detectors.

**Confidence:** 7

**Reasoning:** The top positive driver for the contradiction probe is L0:F6044 (pos 2, direct_effect=+0.79), whose sole large upstream is the embedding of the token " Congress" (pos 2, direct_effect=+17). This entity is then propagated up through a clear semantic hierarchy: L0 'Congress' features (F6044, F7021, F10198, F767, F15411, F13168, F9557) → L1 'Congress' features (F6853, F7245, F2408, F14850, F6948, F3276, F2652, F2335, F14217, F12187, F1528, F3231, F8982, F12456) → L2 features F6735 (direct_effect=+5.38) and F2701 → L3 feature F123 → L4 feature F5265 → L6 feature F6096 (direct_effect=+0.45). This is a clean, content-driven chain rooted in the premise's named subject, not in any negation cue.

The negative driver L0:F13437 (pos 15, direct_effect=-0.58) traces to the embedding of " who" (direct_effect=+35) — a relative-pronoun connective, not a negation word. Its only other large upstream is <bos>. The other strong features similarly root in semantic content:
- L0:F11606 (pos 7) → " funding" (direct_effect=+20)
- L0:F15773 (pos 6) → " our" (direct_effect=+40, the largest single embedding effect in the graph)
- L0:F15792 (pos 13) → " many" (direct_effect=+38)
- L0:F9529 (pos 5) → " controls" (direct_effect=+14)
- L2:F156 (pos 8) → " levels" (direct_effect=+28)
- L3:F13271 (pos 5) → " controls" (direct_effect=+18)
- L3:F8382 (pos 13) → " many" (direct_effect=+23)
- L1:F2116 (pos 7) → " funding" (direct_effect=+14)

Critically, the user flagged concern about "negation words" like "no" or "not". The contradiction target *does* contain "no" in the hypothesis ("has no responsibility when it comes to controlling funding levels"), but the circuit contains no L0 or L1 feature dominated by a negation-token embedding. The pos-15 negative feature is " who", not "no". Instead, the probe activates on the *repeated entity* "Congress" appearing in both premise and hypothesis, the *shared* content word "funding" (which the hypothesis negates — pos 7 is in the premise and the L1:F2116 path links "funding" embeddings into the congress-entity stack), and the *counterexample* quantifier "many" plus the relational "controls" verb. This is the canonical lexical-overlap-plus-negation signature a real contradiction probe should detect.

The strongest single signal (F6044 → " Congress", +17) is also the most semantic: it says the same entity appears in both sentences, which is exactly the structural cue a contradiction classifier needs to identify shared topic. There is no "no"/"not"/"never" embedding dominating any high-magnitude upstream in the circuit. The " who" feature at pos 15 has a large embedding effect (+35) but a small downstream direct effect (-0.58) and is being *suppressed*, not promoted — consistent with a syntactic rather than negation role.

Therefore the user's hypothesis (that the circuit uses spurious negation-word signals) is **not supported** by this graph. The circuit is dominated by entity-recognition, content-word, and structural features that genuinely reflect the prompt's semantic content.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F6044](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) | 2 | L0 'Congress' entity features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) |
| [L0:F7021](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7021) | 2 | L0 'Congress' entity features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7021) |
| [L0:F10198](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10198) | 2 | L0 'Congress' entity features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10198) |
| [L0:F767](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/767) | 2 | L0 'Congress' entity features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/767) |
| [L0:F15411](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15411) | 2 | L0 'Congress' entity features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15411) |
| [L0:F13168](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13168) | 2 | L0 'Congress' entity features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13168) |
| [L0:F9557](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9557) | 2 | L0 'Congress' entity features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9557) |
| [L0:F13437](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13437) | 15 | L0 ' who' feature (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13437) |
| [L0:F11640](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11640) | 7 | L0 ' funding' features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11640) |
| [L0:F13929](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13929) | 7 | L0 ' funding' features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13929) |
| [L0:F4766](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4766) | 7 | L0 ' funding' features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4766) |
| [L0:F7833](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7833) | 7 | L0 ' funding' features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7833) |
| [L0:F10440](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10440) | 7 | L0 ' funding' features (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10440) |
| [L0:F15773](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15773) | 6 | L0 ' our' features (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15773) |
| [L0:F636](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/636) | 6 | L0 ' our' features (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/636) |
| [L0:F15792](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15792) | 13 | L0 ' many' features (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15792) |
| [L0:F676](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/676) | 13 | L0 ' many' features (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/676) |
| [L1:F6853](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6853) | 2 | L1 'Congress' features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6853) |
| [L1:F7245](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7245) | 2 | L1 'Congress' features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7245) |
| [L1:F2408](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2408) | 2 | L1 'Congress' features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2408) |
| [L1:F14850](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14850) | 2 | L1 'Congress' features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14850) |
| [L1:F6948](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6948) | 2 | L1 'Congress' features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6948) |
| [L1:F3276](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3276) | 2 | L1 'Congress' features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3276) |
| [L1:F2652](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2652) | 2 | L1 'Congress' features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2652) |
| [L1:F2335](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2335) | 2 | L1 'Congress' features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2335) |
| [L1:F14217](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14217) | 2 | L1 'Congress' features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14217) |
| [L1:F12187](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12187) | 2 | L1 'Congress' features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12187) |
| [L1:F1528](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1528) | 2 | L1 'Congress' features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1528) |
| [L1:F3231](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3231) | 2 | L1 'Congress' features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3231) |
| [L1:F8982](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8982) | 2 | L1 'Congress' features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8982) |
| [L1:F12456](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12456) | 2 | L1 'Congress' features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12456) |
| [L2:F6735](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6735) | 2 | L2 'Congress' context features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6735) |
| [L2:F2701](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) | 2 | L2 'Congress' context features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) |
| [L2:F156](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/156) | 8 | L2 'Congress' context features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/156) |
| [L3:F13271](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13271) | 5 | L3 'Congress' / ' many' / ' levels' features | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13271) |
| [L3:F123](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/123) | 2 | L3 'Congress' / ' many' / ' levels' features | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/123) |
| [L3:F8382](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8382) | 13 | L3 'Congress' / ' many' / ' levels' features | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8382) |
| [L3:F13620](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13620) | 2 | L3 'Congress' / ' many' / ' levels' features | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13620) |
| [L3:F10669](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10669) | 2 | L3 'Congress' / ' many' / ' levels' features | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10669) |
| [L3:F6462](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6462) | 13 | L3 'Congress' / ' many' / ' levels' features | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6462) |
| [L4:F5265](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5265) | 2 | L4 'Congress' composed feature (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5265) |
| [L6:F6096](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6096) | 2 | L6 mid-layer features driving probe | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6096) |
| [L6:F13778](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/13778) | 6 | L6 mid-layer features driving probe | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/13778) |
| [L5:F842](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/842) | 2 | L6 mid-layer features driving probe | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/842) |
| [L5:F13331](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13331) | 2 | L6 mid-layer features driving probe | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13331) |
| [L4:F8160](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8160) | 6 | L6 mid-layer features driving probe | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8160) |
| [L4:F2813](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2813) | 6 | L6 mid-layer features driving probe | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2813) |
| [L4:F5952](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5952) | 6 | L6 mid-layer features driving probe | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5952) |
| [L1:F160](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/160) | 13 | L6 mid-layer features driving probe | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/160) |
| [L1:F4438](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4438) | 6 | L6 mid-layer features driving probe | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4438) |
| [L1:F4020](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4020) | 5 | L6 mid-layer features driving probe | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4020) |
| [L2:F7279](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7279) | 5 | L6 mid-layer features driving probe | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7279) |
| [L2:F11080](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11080) | 5 | L6 mid-layer features driving probe | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11080) |
| [L2:F7490](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7490) | 5 | L6 mid-layer features driving probe | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7490) |
| [L2:F14310](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14310) | 5 | L6 mid-layer features driving probe | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14310) |
| [L1:F3604](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3604) | 5 | L6 mid-layer features driving probe | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3604) |
| [L2:F12692](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12692) | 2 | L6 mid-layer features driving probe | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12692) |
| [L5:F6376](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6376) | 6 | L6 mid-layer features driving probe | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6376) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:6044 de=0.789 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F6044@2` | ❌ error | — | — | Trace the strongest positive driver at L0:F6044 pos 2 (the "Congress" token). De… |
| SA-2 | `L6:F6096@2` | ❌ error | — | — | Trace L6:F6096 pos 2 - second strongest positive driver. Determine what mid-laye… |
| SA-3 | `L0:F13437@15` | ❌ error | — | — | Trace the strongest negative driver at L0:F13437 pos 15. What is pos 15 in the p… |
| SA-4 | `L1:F2116@7` | ❌ error | — | — | Trace L1:F2116 pos 7 - a strong positive driver. What is pos 7 in the prompt? De… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F6044@2, k=10 → Emb:" Congress"@2 (de=17.00) +9 more |
| 2 | `get_upstream_features` | L6:F6096@2, k=10 → Emb:" Congress"@2 (de=13.81) +9 more |
| 3 | `get_upstream_features` | L2:F6735@2, k=10 → Emb:" Congress"@2 (de=9.12) +9 more |
| 4 | `get_upstream_features` | L4:F5265@2, k=10 → Emb:" Congress"@2 (de=6.91) +9 more |
| 5 | `get_upstream_features` | L0:F13437@15, k=10 → Emb:" who"@15 (de=35.25) +9 more |
| 6 | `get_upstream_features` | L1:F2116@7, k=10 → Emb:" funding"@7 (de=14.12) +9 more |
| 7 | `get_upstream_features` | L2:F2701@2, k=10 → Emb:" Congress"@2 (de=28.12) +9 more |
| 8 | `get_upstream_features` | L3:F13620@2, k=10 → L2:F6735 (de=3.56) +9 more |
| 9 | `get_upstream_features` | L1:F6853@2, k=10 → Emb:" Congress"@2 (de=9.88) +9 more |
| 10 | `get_upstream_features` | L3:F13271@5, k=10 → Emb:" controls"@5 (de=18.50) +9 more |
| 11 | `get_upstream_features` | L2:F156@8, k=10 → Emb:" levels"@8 (de=28.00) +9 more |
| 12 | `get_upstream_features` | L0:F11606@7, k=10 → Emb:" funding"@7 (de=20.12) +9 more |
| 13 | `get_upstream_features` | L3:F123@2, k=10 → Emb:" Congress"@2 (de=20.62) +9 more |
| 14 | `get_upstream_features` | L1:F6948@2, k=10 → Emb:" Congress"@2 (de=16.00) +9 more |
| 15 | `get_upstream_features` | L6:F13778@6, k=10 → Emb:" our"@6 (de=13.62) +9 more |
| 16 | `get_upstream_features` | L0:F9529@5, k=10 → Emb:" controls"@5 (de=14.00) +9 more |
| 17 | `get_upstream_features` | L1:F3276@2, k=10 → Emb:" Congress"@2 (de=21.88) +9 more |
| 18 | `get_upstream_features` | L3:F8382@13, k=10 → Emb:" many"@13 (de=23.50) +9 more |
| 19 | `get_upstream_features` | L0:F10198@2, k=10 → Emb:" Congress"@2 (de=17.25) +9 more |
| 20 | `get_upstream_features` | L0:F767@2, k=10 → Emb:" Congress"@2 (de=26.50) +9 more |
| 21 | `get_upstream_features` | L0:F11640@7, k=10 → Emb:" funding"@7 (de=13.19) +9 more |
| 22 | `get_upstream_features` | L0:F9557@2, k=10 → Emb:" Congress"@2 (de=11.12) +9 more |
| 23 | `get_upstream_features` | L0:F4766@7, k=10 → Emb:" funding"@7 (de=12.88) +9 more |
| 24 | `get_upstream_features` | L0:F15773@6, k=10 → Emb:" our"@6 (de=40.00) +9 more |
| 25 | `get_upstream_features` | L0:F15792@13, k=10 → Emb:" many"@13 (de=38.75) +9 more |
| 26 | `get_upstream_features` | L2:F6462@13, k=10 → Emb:" many"@13 (de=34.50) +9 more |
| 27 | `get_upstream_features` | L1:F160@13, k=10 → Emb:" many"@13 (de=22.38) +9 more |
| 28 | `get_upstream_features` | L0:F7021@2, k=10 → Emb:" Congress"@2 (de=21.00) +9 more |
| 29 | `get_upstream_features` | L0:F15411@2, k=10 → Emb:" Congress"@2 (de=17.00) +9 more |
| 30 | `get_upstream_features` | L0:F13168@2, k=10 → Emb:" Congress"@2 (de=12.88) +9 more |

### Build

`build_circuit` → 18 nodes, 22 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 36,865 | 7,395 | 96,181 | 0 | $0.0257 | — | — |
| **Total** | | **36,865** | **7,395** | **96,181** | **0** | **$0.0257** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 42s