# Circuit Oracle Report
**Date:** 2026-07-28 07:24:17 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_7 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by a low-level "identity-group" template — recognizing the surface pattern "[Group] Pride = being [group] and proud" — and is largely insensitive to either the specific identity named or to the editorial valence (the prompt equates "White Pride" with "NAZI!" yet the probe routes the signal through generic Black/Pride template features anyway).

**Confidence:** 7

**Reasoning:** The circuit reaches down to embedding nodes (`Emb: Black (pos 1)`, `Emb: Pride (pos 2)`, `Emb: = (pos 3)`, `Emb: being (pos 4)`, `Emb: black (pos 5)`, `Emb: White (pos 17)`, `Emb: \n (pos 8)`), and at every layer the top features converge on the *structural template* rather than on semantic content. L0 sub-token features on "Pride" (10164, 1088, 13145, 12292, 12717, 7019, 10074) and on "=" (6704, 5463, 9222, 2905, 15285) dominate. L1 builds the "X Pride =" structural pattern (`L1 'X Pride =' structural features`, e.g. 12078/15447/14137/12542) and a parallel "Black+Pride" grouping node (13069, 9113, 1129). By L2 (`L2 'identity-group concept'`) the model has abstracted to an identity-group concept (1644, 11363, 10596, 9528) — note that 11363 and 9528 fire on "Black" and 1644 on "Pride". L3 (12034, 15701, 11279, 12020, 7084, 13601, 13061, 16373) and L4 (192, 5217) instantiate the "Pride = …" completion and the "X = Y" pattern; L5 (615) acts as a group-identity classifier; L6 (15295) assembles the identity signal and feeds the probe logit. Crucially, the inhibition of the " black" embedding (Emb:black pos 5, direct_effect 22.25) by the L1 feature 13069 (direct_effect -0.1211) and the strong positive drive from "Pride" embeddings (e.g. Emb:Pride pos 2 → L3:13061 direct_effect 5.28, → L6:15295 direct_effect 10.75) shows the signal is carried by the *pride-equals-definition* template, not by the "NAZI!" content. Even the "White" token at pos 17 only contributes via a low-level sub-token feature (L0:3436, direct_effect 0.067) and the newline at pos 8 (L0:7894, direct_effect -0.079, inhibitory). The probe therefore fires on a generic "identity-group definition" pattern — confirming the user concern: the mechanism uses spurious "identity group" template features rather than lexical/semantic features tied to the prompt's actual anti-racist content (e.g. "NAZI!", "Hypocrisy is worse than racism", the moral judgment). The "White Pride = NAZI!" line, which is the toxic content, does not produce any negative feature; the only L0 feature on "White" (3436) is mildly *pro*-probe. This is a textbook case of a probe riding a structurally correlated but semantically misaligned feature: the model classifies the prompt as "identity-related" and the linear probe learned exactly that direction, missing the toxicity signal entirely.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Black (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: Pride (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: = (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: being (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: black (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: White (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: \n (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F10164](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10164) | 2 | L0 sub-token features on 'Pride' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10164) |
| [L0:F1088](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1088) | 2 | L0 sub-token features on 'Pride' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1088) |
| [L0:F13145](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13145) | 2 | L0 sub-token features on 'Pride' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13145) |
| [L0:F12292](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12292) | 2 | L0 sub-token features on 'Pride' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12292) |
| [L0:F12717](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12717) | 2 | L0 sub-token features on 'Pride' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12717) |
| [L0:F7019](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7019) | 2 | L0 sub-token features on 'Pride' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7019) |
| [L0:F10074](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10074) | 2 | L0 sub-token features on 'Pride' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10074) |
| [L0:F6704](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6704) | 3 | L0 sub-token features on '=' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6704) |
| [L0:F5463](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5463) | 3 | L0 sub-token features on '=' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5463) |
| [L0:F9222](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9222) | 3 | L0 sub-token features on '=' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9222) |
| [L0:F2905](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2905) | 3 | L0 sub-token features on '=' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2905) |
| [L0:F15285](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15285) | 3 | L0 sub-token features on '=' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15285) |
| [L0:F45](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/45) | 4 | L0 sub-token features on 'being' (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/45) |
| [L0:F12054](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12054) | 4 | L0 sub-token features on 'being' (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12054) |
| [L0:F1015](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1015) | 5 | L0 sub-token features on 'black' (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1015) |
| [L0:F13380](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13380) | 5 | L0 sub-token features on 'black' (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13380) |
| [L0:F16013](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16013) | 5 | L0 sub-token features on 'black' (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16013) |
| [L0:F1444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1444) | 5 | L0 sub-token features on 'black' (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1444) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 17 | L0 sub-token features on 'White' (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F7894](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7894) | 8 | L0 sub-token features on '\n' (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7894) |
| [L1:F12078](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12078) | 2 | L1 'X Pride =' structural features (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12078) |
| [L1:F15447](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15447) | 2 | L1 'X Pride =' structural features (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15447) |
| [L1:F14137](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14137) | 2 | L1 'X Pride =' structural features (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14137) |
| [L1:F12542](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12542) | 2 | L1 'X Pride =' structural features (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12542) |
| [L1:F2380](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2380) | 4 | L1 'X Pride =' structural features (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2380) |
| [L1:F13069](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13069) | 5 | L1 'Black+Pride' grouping features (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13069) |
| [L1:F13069](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13069) | 1 | L1 'Black+Pride' grouping features (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13069) |
| [L1:F9113](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) | 5 | L1 'Black+Pride' grouping features (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) |
| [L1:F1129](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1129) | 2 | L1 'Black+Pride' grouping features (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1129) |
| [L2:F1644](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1644) | 2 | L2 'identity-group concept' features (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1644) |
| [L2:F10596](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10596) | 2 | L2 'identity-group concept' features (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10596) |
| [L2:F11363](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11363) | 1 | L2 'identity-group concept' features (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11363) |
| [L2:F9528](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) | 1 | L2 'identity-group concept' features (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) |
| [L2:F14025](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14025) | 3 | L2 'identity-group concept' features (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14025) |
| [L2:F5266](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5266) | 4 | L2 'identity-group concept' features (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5266) |
| [L2:F12360](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12360) | 3 | L2 'identity-group concept' features (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12360) |
| [L2:F1311](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1311) | 3 | L2 'identity-group concept' features (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1311) |
| [L3:F12034](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12034) | 2 | L3 'Pride = ...' completion (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12034) |
| [L3:F15701](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15701) | 2 | L3 'Pride = ...' completion (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15701) |
| [L3:F11279](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11279) | 3 | L3 'Pride = ...' completion (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11279) |
| [L3:F12020](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12020) | 4 | L3 'Pride = ...' completion (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12020) |
| [L3:F7084](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7084) | 2 | L3 'Pride = ...' completion (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7084) |
| [L3:F13601](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13601) | 2 | L3 'Pride = ...' completion (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13601) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 2 | L3 'Pride = ...' completion (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L3:F16373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) | 2 | L3 'Pride = ...' completion (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) |
| [L4:F192](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/192) | 3 | L4 'X = Y' pattern features | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/192) |
| [L4:F5217](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5217) | 2 | L4 'X = Y' pattern features | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5217) |
| [L5:F615](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/615) | 2 | L5 'group-identity' classification features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/615) |
| [L6:F15295](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15295) | 2 | L6 identity assembly (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15295) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe Logit | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:12717 de=-0.133 |
| 3 | `get_top_features` | 30 features; top: L0:12717 de=-0.133 |
| 4 | `get_upstream_features` | Emb:" ="@3 (de=11.31) +9 more |
| 5 | `get_upstream_features` | Emb:" Pride"@2 (de=18.62) +9 more |
| 6 | `get_upstream_features` | Emb:" black"@5 (de=22.25) +9 more |
| 7 | `get_upstream_features` | Emb:" Pride"@2 (de=10.75) +9 more |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L3:F11279@3` | ❌ error | — | — | Trace this feature upstream to understand what it represents and what input toke… |
| SA-2 | `L6:F15295@2` | ❌ error | — | — | Trace this feature upstream. It's at pos 2 ("Pride") and has a positive direct_e… |
| SA-3 | `L1:F13069@5` | ❌ error | — | — | Trace upstream. This feature at pos 5 (the " black" token in "being black and pr… |
| SA-4 | `L0:F3436@17` | ❌ error | — | — | Trace upstream. This is at pos 17 (near the end of the prompt, after the dash an… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L2:F1644@2, k=8 → Emb:" Pride"@2 (de=16.62) +7 more |
| 2 | `get_upstream_features` | L0:F12292@2, k=8 → Emb:"Black"@1 (de=12.31) +7 more |
| 3 | `get_upstream_features` | L3:F16373@2, k=8 → Emb:"Black"@1 (de=15.62) +7 more |
| 4 | `get_upstream_features` | L3:F13061@2, k=8 → Emb:"Black"@1 (de=12.06) +7 more |
| 5 | `get_upstream_features` | L5:F615@2, k=8 → Emb:" Pride"@2 (de=12.69) +7 more |
| 6 | `get_upstream_features` | L0:F45@4, k=8 → Emb:" being"@4 (de=32.75) +7 more |
| 7 | `get_upstream_features` | L0:F3436@17, k=8 → Emb:"White"@17 (de=16.75) +7 more |
| 8 | `get_upstream_features` | L0:F7894@8, k=8 → Emb:"
"@8 (de=26.38) +7 more |
| 9 | `get_upstream_features` | L4:F192@3, k=8 → Emb:" ="@3 (de=15.94) +7 more |
| 10 | `get_upstream_features` | L3:F12020@4, k=8 → Emb:" being"@4 (de=20.12) +7 more |
| 11 | `get_upstream_features` | L3:F12034@2, k=8 → Emb:"Black"@1 (de=7.25) +7 more |
| 12 | `get_upstream_features` | L0:F10164@2, k=8 → Emb:" Pride"@2 (de=11.50) +7 more |
| 13 | `get_upstream_features` | L0:F1088@2, k=8 → Emb:" Pride"@2 (de=11.88) +7 more |
| 14 | `get_upstream_features` | L0:F5463@3, k=8 → Emb:" ="@3 (de=11.38) +7 more |

### Build

`build_circuit` → 21 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 16,583 | 6,441 | 58,062 | 0 | $0.0162 | — | — |
| **Total** | | **16,583** | **6,441** | **58,062** | **0** | **$0.0162** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 8s