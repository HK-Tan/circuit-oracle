# Circuit Oracle Report
**Date:** 2026-07-28 07:21:38 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_10 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity score is driven almost entirely by late-layer features that detect the mere *presence* of race- and identity-related vocabulary in the prompt — most prominently L6:3902 ("terms referring to race and ethnicity," frac_nonzero 0.018) firing on the tokens "race" (pos 5), "of" (pos 6), "black" (pos 16) and "people" (pos 17), and L4:117 ("terms related to race, racism, and social justice, with a particular focus on terms related to Black people," frac_nonzero 0.012) on the same positions — with no detectable contribution from features encoding toxicity, slur, threat, or hateful-action content (e.g. "force," "helpless," "cops" do not appear as top drivers at any layer).

**Confidence:** 8

**Reasoning:** The circuit traces cleanly to the input tokens but the signal is dominated by *identity-category* detectors rather than by anything encoding harm, threat, or negative sentiment. At the embedding level the top drivers are the literal tokens `race` (pos 5, direct_effect up to 19 on L4:117), `black` (pos 16, direct_effect ~11 on L3:13061), `people` (pos 17, direct_effect ~3.5), `of` (pos 6) and `force` (pos 13, direct_effect 30 on L2:13653), with `By` (pos 1) also contributing via L4:11200. These feed early lexical features such as L2:10509 ("the word 'race,'" frac_nonzero 0.006) and L4:5584 ("words related to race, ethnicity, nationality or population groups," frac_nonzero 0.007), which then activate the mid-layer concept features L4:117 (race/racism/Black-people concept, promotes "racist," "racism," "racial") and L5:12135 ("terms related to discrimination based on identity," promotes identity-group vocabulary). The single largest late-layer driver is L6:3902 (direct_effect 0.59 at pos 6, fires at pos 5/6/16/17) which itself is fed almost exclusively by the ` race` embedding (direct_effect 11) and L4:5584/L4:117/L5:12135. Crucially, features encoding "toxic," "hateful," "violent," or "threat" content are entirely absent from the top-20 by direct_effect, and L6:9228 / L7:8030 only weakly modulate the score. This confirms the user's concern: the probe's classification is essentially a bag-of-identity-words detector — any text mentioning race + a racial descriptor + an identity noun triggers the score regardless of whether the surrounding content is hateful, neutral, or even *arguing against* the framing (as this prompt does). The same circuit would likely fire on a benign sentence like "people of all races live here," which is the textbook signature of a spurious identity-feature shortcut.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: race (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: of (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 16 | Emb: black (pos 16) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: people (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: force (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: By (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F10682](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10682) | 5 | Early lexical: "race" / word-level detectors (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10682) |
| [L0:F1823](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1823) | 5 | Early lexical: "race" / word-level detectors (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1823) |
| [L0:F11851](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11851) | 5 | Early lexical: "race" / word-level detectors (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11851) |
| [L2:F10509](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10509) | 5 | Early lexical: "race" / word-level detectors (L0-L2) |  the word "race." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10509) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 5 | Early lexical: "race" / word-level detectors (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L3:F3678](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3678) | 6 | Mid: race/ethnicity/social-justice concept features (L3-L5) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3678) |
| [L3:F15128](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15128) | 6 | Mid: race/ethnicity/social-justice concept features (L3-L5) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15128) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 17 | Mid: race/ethnicity/social-justice concept features (L3-L5) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 5 | Mid: race/ethnicity/social-justice concept features (L3-L5) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 6 | Mid: race/ethnicity/social-justice concept features (L3-L5) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F5584](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5584) | 6 | Mid: race/ethnicity/social-justice concept features (L3-L5) |  words related to race, ethnicity, nationality or population groups | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5584) |
| [L4:F88](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/88) | 6 | Mid: race/ethnicity/social-justice concept features (L3-L5) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/88) |
| [L4:F11200](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11200) | 1 | Mid: race/ethnicity/social-justice concept features (L3-L5) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11200) |
| [L5:F12135](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12135) | 6 | Mid: race/ethnicity/social-justice concept features (L3-L5) |  terms related to discrimination based on identity | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12135) |
| [L5:F1431](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1431) | 6 | Mid: race/ethnicity/social-justice concept features (L3-L5) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1431) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 5 | Late: race-aggregator driving probe (L6-L7) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 6 | Late: race-aggregator driving probe (L6-L7) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 16 | Late: race-aggregator driving probe (L6-L7) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 17 | Late: race-aggregator driving probe (L6-L7) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F343](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/343) | 6 | Late: race-aggregator driving probe (L6-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/343) |
| [L6:F2267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2267) | 6 | Late: race-aggregator driving probe (L6-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2267) |
| [L6:F9228](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9228) | 6 | Late: race-aggregator driving probe (L6-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9228) |
| [L7:F8030](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8030) | 6 | Late: race-aggregator driving probe (L6-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8030) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe output direction | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'probe_score' is not one of the top-k next-token candi |
| 3 | `get_top_features` | 20 features; top: L6:3902 de=0.586 |
| 4 | `inspect_feature` ×4 | L6:3902, L2:10509, L4:117, L0:7820 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F3902@6` | ❌ error | — | — | Trace the L6:3902 "race and ethnicity" feature (high direct_effect 0.59 at pos 6… |
| SA-2 | `L4:F117@6` | ❌ error | — | — | Trace the L4:117 "race/racism/Black people" feature (direct_effect 0.27 at pos 6… |
| SA-3 | `L6:F9228@6` | ❌ error | — | — | Trace the L6:9228 feature (direct_effect -0.21 at pos 6, inhibitory) upstream to… |
| SA-4 | `L2:F10509@5` | ❌ error | — | — | Trace the L2:10509 "word race" feature (direct_effect -0.49 at pos 5 - inhibitor… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F3902@6, k=15 → Emb:" race"@5 (de=11.00) +14 more |
| 2 | `get_upstream_features` | L4:F117@6, k=15 → Emb:" race"@5 (de=19.00) +14 more |
| 3 | `get_upstream_features` | L4:F5584@6, k=10 → Emb:" race"@5 (de=16.62) +9 more |
| 4 | `get_upstream_features` | L5:F12135@6, k=10 → Emb:" race"@5 (de=4.84) +9 more |
| 5 | `inspect_feature` ×2 | L4:5584, L5:12135 |
| 6 | `get_upstream_features` | L7:F8030@6, k=10 → L6:F3902 (de=8.38) +9 more |
| 7 | `get_upstream_features` | L3:F13061@17, k=10 → Emb:" black"@16 (de=11.38) +9 more |
| 8 | `get_upstream_features` | L4:F11200@1, k=10 → Emb:"By"@1 (de=16.25) +9 more |
| 9 | `get_upstream_features` | L2:F13653@13, k=10 → Emb:" force"@13 (de=30.00) +9 more |
| 10 | `get_upstream_features` | L6:F2267@6, k=8 → Emb:"<bos>"@0 (de=-3.66) +7 more |
| 11 | `get_upstream_features` | L6:F9228@6, k=10 → L5:F12135 (de=2.75) +9 more |
| 12 | `get_upstream_features` | L2:F13158@16, k=8 → Emb:" black"@16 (de=10.94) +7 more |

### Build

`build_circuit` → 10 nodes, 9 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 23,959 | 4,260 | 108,135 | 0 | $0.0188 | — | — |
| **Total** | | **23,959** | **4,260** | **108,135** | **0** | **$0.0188** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 0s