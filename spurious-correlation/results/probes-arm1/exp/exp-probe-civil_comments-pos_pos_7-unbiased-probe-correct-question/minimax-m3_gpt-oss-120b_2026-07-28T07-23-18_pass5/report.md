# Circuit Oracle Report
**Date:** 2026-07-28 07:23:18 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_7 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe is a toxicity classifier whose score is driven primarily by the presence of an *identity-group label* ("Black"/"black") and the *identity-pride compound* "Black Pride", routed through late-layer features that are selective for race/gender discourse and that project "Pride" toward gay/lesbian/HIV-related identity vocabulary — the model is classifying toxicity from identity-category cues, not from the actual hateful content ("NAZI!", "Hypocrisy is worse than racism.") or the contrastive structure of the prompt.

**Confidence:** 7

**Reasoning:**

**Late-layer drive (L6).** The single most identity-specific late feature is **L6:F15295** ("HIV/AIDS words", pos 2, direct_effect **+0.0806**). Despite its literal label, its *promoted tokens* are `▁gays`, `▁homosexuality`, `▁gay`, `▁photolibrary`, `▁homosexual`, `▁lesbian` — it has been repurposed in this context as an LGBT/sexual-orientation identity feature. Upstream it is dominated by the **" Pride"** token embedding at pos 2 (direct_effect **+10.75**), the strongest single edge in the graph, and by intermediate "Pride"-context features (L3:F13061, L3:F16373, L4:F5217). The "NAZI!" content, the dash, and the concluding "Hypocrisy is worse than racism." line contribute **nothing** to this late feature.

**Mid-layer "Pride" compound (L3-L4).** Features **L3:F13061** (pos 2, direct_effect from "Black" embedding = **+12.06**, from " Pride" = +5.28) and **L3:F16373** (driven almost entirely by the "Black" embedding, direct_effect = **+15.625** from Emb:"Black") are *compound* detectors for the *Black Pride* identity phrase, not for the word "pride" alone. **L3:F12034** ("technical terms, graphs/figures", pos 2, direct_effect **+0.0874**) is a generic feature, but here it is co-opted because the *Pride = …* definitional format fires it.

**Identity-discourse detectors (L1-L2).** **L1:F9113** ("discussions about race and slavery", pos 5, direct_effect **+0.0898**) and **L1:F13069** ("the word 'black'", pos 5, direct_effect **-0.1211** — *inhibitory* toward the probe direction) are the two key race-detecting features. Critically, F9113 is not a generic color word detector — its top activating examples are race-discourse contexts (slavery, racial slurs, anti-white extremism), and it is driven directly by the " black" embedding at pos 5 (direct_effect **+17.5**). Its sister feature **L2:F10371** ("race and gender, Stanford Clayman institute") is the cleanest identity-cue feature in the graph, firing specifically on the capitalised "Black" at pos 1 (direct_effect from Emb:"Black" = **+25.0**). **L2:F11363** ("colors and words like Diamond") is the only generic color feature here, but the probe mostly ignores it in favor of the race-specific features.

**The "being" words are a distractor.** L0:F45 and L2:F5266 fire on the literal word "being" in *all three* definitional lines (Black/Gay/White). They have only modest direct effects (-0.099 and -0.086) and the graph shows them as roughly *anti-pride* signals. They cannot explain the probe's differential response to the three lines — and indeed, the word "being" appears identically in the "Gay Pride" and "White Pride" lines that the probe presumably *does not* flag the same way.

**User concern confirmed.** The probe's top positive contributors are (a) the **"Black" identity token itself** (Emb:"Black" → L2:F10371, direct_effect +25.0; Emb:" black" → L1:F9113, direct_effect +17.5), (b) a **race-discourse compound** (L3:F16373, dominated by Emb:"Black"), and (c) an **identity-orientation projector** that maps "Pride" onto gay/lesbian vocabulary (L6:F15295, "Pride" direct_effect +10.75). The actual toxic content ("NAZI!", the moralistic punchline) does not appear anywhere in the top 15 features. Two features carry *opposing* signs for the same input (L1:F13069 strongly *inhibits* the probe, L1:F9113 strongly *promotes* it, both on the same "black" position), confirming the probe is sensitive to *which* identity-discourse detector fires, not to the lexical presence of the word "black." This is a textbook **identity-group spurious correlation**: the probe is detecting "this text names a minority identity group" rather than "this text contains toxic content."

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F1015](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1015) | 1 | Lexical 'black' / 'Black' tokens (L0) |  the word "black" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1015) |
| [L0:F45](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/45) | 4 | Generic 'being' word features (L0-L2) | the word "being" in different contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/45) |
| [L2:F5266](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5266) | 4 | Generic 'being' word features (L0-L2) | phrases that include the word "being" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5266) |
| [L2:F11363](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11363) | 1 | Color words (incl. 'Black' as a color) (L2) |  colors and words like Diamond. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11363) |
| [L1:F9113](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) | 5 | Race & gender / Stanford identity-discourse features (L1-L2) |  discussions about race and slavery | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) |
| [L2:F10371](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10371) | 1 | Race & gender / Stanford identity-discourse features (L1-L2) |  words related to race and gender, as well as the Clayman institute at Stanford | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10371) |
| [L0:F12717](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12717) | 2 | 'pride' / 'proud' generic word features (L0-L3) |  the word "pride" in different contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12717) |
| [L1:F12078](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12078) | 2 | 'pride' / 'proud' generic word features (L0-L3) |  the word "proud" and words associated with oaths or declarations of loyalty | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12078) |
| [L3:F15701](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15701) | 2 | 'pride' / 'proud' generic word features (L0-L3) | instances of the word "proud" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15701) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 2 | Pride-context / identity-compound features (L3-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L3:F16373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) | 2 | Pride-context / identity-compound features (L3-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) |
| [L4:F5217](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5217) | 2 | Pride-context / identity-compound features (L3-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5217) |
| [L0:F9222](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9222) | 3 | Technical/figure-punctuation features (L0-L3) |  the equals sign | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9222) |
| [L3:F12034](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12034) | 2 | Technical/figure-punctuation features (L0-L3) | technical terms, especially those used to describe graphs and figures | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12034) |
| [L0:F10164](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10164) | 2 | Technical/figure-punctuation features (L0-L3) |  relative pronouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10164) |
| [L6:F15295](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15295) | 2 | HIV/AIDS words -> 'gay/lesbian' identity projection (L6) |  words and abbreviations related to HIV/AIDS and viral infections. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15295) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:12717 de=-0.133 |
| 3 | `inspect_feature` ×15 | L0:12717, L3:11279, L3:15701, L1:13069, L0:9222, L0:45, L1:9113, L3:12034, L0:1088, L0:2177, L2:5266, L0:12054, L0:10164, L6:15295, L0:1015 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L1:F13069@5` | ❌ error | — | — | Trace L1:F13069 (the word 'black' at pos 5 — "Black" in "Black Pride"). Find wha… |
| SA-2 | `L1:F9113@5` | ❌ error | — | — | Trace L1:F9113 (race/slavery discussions at pos 5). This is a sensitive identity… |
| SA-3 | `L6:F15295@2` | ❌ error | — | — | Trace L6:F15295 (HIV/AIDS words at pos 2, direct_effect 0.0806). Its promoted to… |
| SA-4 | `L3:F12034@2` | ❌ error | — | — | Trace L3:F12034 (technical terms / graphs and figures at pos 2, direct_effect 0.… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F15295@2, k=10 → Emb:" Pride"@2 (de=10.75) +9 more |
| 2 | `get_upstream_features` | L1:F9113@5, k=10 → Emb:" black"@5 (de=17.50) +9 more |
| 3 | `get_upstream_features` | L3:F12034@2, k=10 → Emb:"Black"@1 (de=7.25) +9 more |
| 4 | `get_upstream_features` | L3:F15701@2, k=10 → Emb:" Pride"@2 (de=18.62) +9 more |
| 5 | `get_upstream_features` | L1:F13069@5, k=10 → Emb:" black"@5 (de=22.25) +9 more |
| 6 | `get_upstream_features` | L0:F45@4, k=8 → Emb:" being"@4 (de=32.75) +7 more |
| 7 | `get_upstream_features` | L2:F5266@4, k=8 → Emb:" being"@4 (de=31.00) +7 more |
| 8 | `get_upstream_features` | L0:F1015@1, k=8 → Emb:"Black"@1 (de=16.88) +7 more |
| 9 | `get_upstream_features` | L3:F13061@2, k=8 → Emb:"Black"@1 (de=12.06) +7 more |
| 10 | `get_upstream_features` | L3:F16373@2, k=8 → Emb:"Black"@1 (de=15.62) +7 more |
| 11 | `get_upstream_features` | L4:F5217@2, k=8 → L3:F16373 (de=2.44) +7 more |
| 12 | `get_upstream_features` | L2:F11363@1, k=8 → Emb:"Black"@1 (de=25.00) +7 more |
| 13 | `inspect_feature` ×4 | L0:9026, L1:12078, L2:11363, L2:10371 |
| 14 | `get_upstream_features` | L1:F1129@2, k=6 → Emb:" Pride"@2 (de=8.75) +5 more |
| 15 | `get_upstream_features` | L1:F15447@2, k=6 → Emb:" Pride"@2 (de=13.88) +5 more |
| 16 | `get_upstream_features` | L0:F1088@2, k=6 → Emb:" Pride"@2 (de=11.88) +5 more |
| 17 | `get_upstream_features` | L0:F10164@2, k=6 → Emb:" Pride"@2 (de=11.50) +5 more |

### Build

`build_circuit` → 14 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 42,515 | 5,590 | 249,156 | 0 | $0.0344 | — | — |
| **Total** | | **42,515** | **5,590** | **249,156** | **0** | **$0.0344** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 23s