# Circuit Oracle Report
**Date:** 2026-07-28 07:24:24 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

The circuit is saved. Here is my analysis:

**Analysis:** The probe's toxicity classification is driven by a small set of low/mid-layer features that fire specifically on racial-identity vocabulary tokens ("black", "white", "race") and the entity "trump," with no involvement of features encoding the actual toxic content (e.g., slurs, dehumanizing language, calls for exclusion).

**Confidence:** 7

**Reasoning:** The attribution graph shows that the top positively-contributing features to the probe score are almost entirely token- or lemma-identity detectors anchored to demographic-group words:

- **L2:F13158** (direct_effect +0.318 at pos 32) is anchored by the "black" embedding (direct_effect 10.5) and also fires on "white" and "race" embeddings at other positions. It is a multi-position racial-vocabulary feature, not a toxicity feature.
- **L4:F117** (+0.219) is anchored by the "bigot"/"ot" subword (Emb "ot" at pos 9, +3.52) — again, a lexical detector.
- **L0:F3255** (+0.231) is essentially the "and" embedding (direct_effect 36.75 from Emb "and" at pos 10) — a pure function-word detector that contributes positively to the toxicity score.
- **L5:F8030** (+0.211) is the "clearly"/"shows" embedding (Emb "clearly" direct_effect 18.25) — another generic content-free word.
- **L0:F7969** (+0.209) is the "other" embedding (direct_effect 42.25) — a generic quantifier.
- **L0:F6051** (+0.159) is the "." period embedding (direct_effect 45.75) — punctuation.
- **L0:F6154** and **L0:F7142** (+0.239, +0.214) are the "clearly" embedding detector at pos 2.
- **L6:F3902** (+0.202) is the "white" embedding (direct_effect 10.81) at pos 25.
- **L4:F14582** (+0.218) is the "trump" entity detector (Emb "trump" direct_effect 18.13).

None of the top features have upstream inputs from lexical items like "hate", "want", "make America white again", or other toxic-content-carrying spans of the prompt. The inhibitory features (L0:F5707, L1:F2407, L0:F12866 at pos 2) are also purely "clearly"-embedding-anchored.

This confirms the user's concern: the probe's classification is largely driven by spurious identity-group and high-frequency-function-word features, not by the actual toxic semantic content of the prompt. The signal is best characterized as "identity term presence" + "standard English fluency signals" rather than genuine toxicity detection. A robustness check would be to test whether permuting/removing these specific identity tokens flips the probe's classification.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 32 | Identity-term group detectors (white, black, race) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 40 | Identity-term group detectors (white, black, race) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 25 | Identity-term group detectors (white, black, race) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 15 | Identity-term group detectors (white, black, race) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 9 | Identity-term group detectors (white, black, race) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 32 | Identity-term group detectors (white, black, race) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 25 | Identity-term group detectors (white, black, race) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 40 | Identity-term group detectors (white, black, race) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L0:F3255](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) | 10 | Function-word / subword detectors (and, other, ., bigot) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) |
| [L0:F7969](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7969) | 14 | Function-word / subword detectors (and, other, ., bigot) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7969) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 18 | Function-word / subword detectors (and, other, ., bigot) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L5:F8030](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/8030) | 3 | Function-word / subword detectors (and, other, ., bigot) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/8030) |
| [L4:F14582](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14582) | 5 | Entity-specific feature (trump) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14582) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 32 | Emb: black (pos 32) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 25 | Emb: white (pos 15, 25) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: white (pos 15, 25) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 40 | Emb: race (pos 40) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: and (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: other (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 18 | Emb: . (pos 18) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: clearly (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: trump (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: bigot/bigots (pos 8/9/16/17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: bigot/bigots (pos 8/9/16/17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 16 | Emb: bigot/bigots (pos 8/9/16/17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: bigot/bigots (pos 8/9/16/17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe classification direction | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:5707 de=-0.346 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F13158@32` | ❌ error | — | — | Trace the upstream circuit from L2:F13158 at position 32. This feature has a ver… |
| SA-2 | `L0:F3255@10` | ❌ error | — | — | Trace the upstream circuit from L0:F3255 at position 10. This feature has direct… |
| SA-3 | `L4:F117@9` | ❌ error | — | — | Trace the upstream circuit from L4:F117 at position 9. This feature has direct_e… |
| SA-4 | `L5:F8030@3` | ❌ error | — | — | Trace the upstream circuit from L5:F8030 at position 3. This feature has direct_… |
| SA-5 | `L0:F7969@14` | ❌ error | — | — | Trace the upstream circuit from L0:F7969 at position 14. This feature has direct… |
| SA-6 | `L6:F3902@25` | ❌ error | — | — | Trace the upstream circuit from L6:F3902 at position 25. This feature has direct… |
| SA-7 | `L0:F6051@18` | ❌ error | — | — | Trace the upstream circuit from L0:F6051 at position 18. This feature has direct… |
| SA-8 | `L0:F5707@2` | ❌ error | — | — | Trace the upstream circuit from L0:F5707 at position 2. This is the top negative… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L2:F13158@32, k=15 → Emb:" black"@32 (de=10.50) +14 more |
| 2 | `get_upstream_features` | L0:F3255@10, k=15 → Emb:" and"@10 (de=36.75) +14 more |
| 3 | `get_upstream_features` | L4:F117@9, k=15 → Emb:"ot"@9 (de=3.52) +14 more |
| 4 | `get_upstream_features` | L5:F8030@3, k=15 → Emb:" clearly"@2 (de=18.25) +14 more |
| 5 | `get_upstream_features` | L0:F7969@14, k=15 → Emb:" other"@14 (de=42.25) +14 more |
| 6 | `get_upstream_features` | L6:F3902@25, k=15 → Emb:" white"@25 (de=10.81) +14 more |
| 7 | `get_upstream_features` | L0:F6051@18, k=15 → Emb:"."@18 (de=45.75) +14 more |
| 8 | `get_upstream_features` | L0:F6154@2, k=15 → Emb:" clearly"@2 (de=13.62) +14 more |
| 9 | `get_upstream_features` | L0:F7142@2, k=15 → Emb:" clearly"@2 (de=14.62) +14 more |
| 10 | `get_upstream_features` | L4:F14582@5, k=10 → Emb:" trump"@5 (de=18.12) +9 more |
| 11 | `get_upstream_features` | L2:F13158@40, k=10 → Emb:" race"@40 (de=13.62) +9 more |
| 12 | `get_upstream_features` | L2:F13158@15, k=10 → Emb:" white"@15 (de=12.81) +9 more |
| 13 | `get_upstream_features` | L1:F2407@2, k=10 → Emb:" clearly"@2 (de=22.00) +9 more |
| 14 | `get_upstream_features` | L0:F12866@2, k=10 → Emb:" clearly"@2 (de=17.38) +9 more |
| 15 | `get_upstream_features` | L6:F1707@1, k=10 → L4:F8223 (de=4.09) +9 more |
| 16 | `get_upstream_features` | L4:F117@32, k=10 → Emb:" black"@32 (de=12.06) +9 more |
| 17 | `get_upstream_features` | L4:F14582@5, k=5 → Emb:" trump"@5 (de=18.12) +4 more |
| 18 | `get_upstream_features` | L1:F2407@2, k=5 → Emb:" clearly"@2 (de=22.00) +4 more |
| 19 | `get_upstream_features` | L0:F247@2, k=5 → Emb:" clearly"@2 (de=13.81) +4 more |
| 20 | `get_upstream_features` | L0:F5707@2, k=5 → Emb:" clearly"@2 (de=20.88) +4 more |

### Build

`build_circuit` → 13 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 19,874 | 5,244 | 78,619 | 0 | $0.0170 | — | — |
| **Total** | | **19,874** | **5,244** | **78,619** | **0** | **$0.0170** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 30s