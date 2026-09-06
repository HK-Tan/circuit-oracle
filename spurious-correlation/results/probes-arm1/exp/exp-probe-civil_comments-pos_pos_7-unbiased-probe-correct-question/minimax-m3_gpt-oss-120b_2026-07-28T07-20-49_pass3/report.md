# Circuit Oracle Report
**Date:** 2026-07-28 07:20:49 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_7 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity classification is driven almost entirely by identity-group lexical cues (Black/White/Gay/Pride) and a generic "racism discussion" pattern detector — not by the actual content of the final sentence about hypocrisy.

**Confidence:** 8

**Reasoning:**

The output is the probe's classification score (toxicity direction). The top transcoder features feeding the probe logit are dominated by:

1. **Identity-token detectors at L0** (frac_nonzero 0.003–0.06): L0:F1015 ("the word 'black'"), L0:F3436 ("the word 'white'", pos 17), L0:F13069 ("the word 'black'", pos 1) — all activated by *raw token embeddings* of the identity words themselves, not by their toxic context. They feed forward as pure "this is an identity word" signals.

2. **Race/gender/demographic supernode at L3** (L3:F13061 "words related to race, gender and social issues", L3:F16373 "mentions of demographic identity, especially race and gender") — these are entity-category abstractions. L3:F15701 ("proud") and L3:F11279 (math/scientific symbols — spurious firing on the "=" token) round out the group. This is the "spurious identity-group" pattern the user flagged: a generic detector that fires whenever *any* race/gender identity term appears.

3. **Race/slavery discussion feature L1:F9113** — labeled "discussions about race and slavery," which fires on the literal token "black" here. Its promoted tokens include "black/Black" and suppressed tokens include "white" — a classic spurious race-correlation feature. Upstream: this feature activates on the token "black" at position 5 with a 17.5 direct_effect from the embedding, completely ignoring the surrounding "being" / "proud" / "=" structure.

4. **L6:F15295 "HIV/AIDS + gay-related terms"** with promoted tokens `gays, homosexuality, gay, homosexual, lesbian` — fires on the "Pride" token (pos 2) with direct_effect 0.08 because of training-corpus co-occurrence of "Pride" with gay/HIV contexts, not because of the prompt's actual content. Upstream is essentially just the "Pride" embedding (10.75 direct_effect).

5. **L5:F615 "named holidays/days"** — fires on "Pride" because Pride is in its training-distribution as a holiday. Upstream is dominated by the Pride embedding (12.69 direct_effect).

6. **L4:F192 "equals signs adjacent to numbers/letters"** — fires on the "=" in the formula. Upstream is the "=" embedding (15.94 direct_effect). Orthogonal to the toxic content.

7. **Off-topic noise**: L0:F10074 ("San Diego"), L0:F10164 ("relative pronouns — whom"), L0:F7894 ("paragraph newline"), L0:F1088 ("meal"), L2:F1311 ("LaTeX math mode"), L2:F6014 (misc technical) — pure lexical/format artifacts.

The user's concern is confirmed by the circuit. The probe score is being driven by:
- Raw embeddings of identity words (Black, White, Gay, Pride) activating identity-token features
- A generic "demographic identity" feature (L3:F13061, L3:F16373) — a category-detector that fires on the mere mention of identity groups
- A race/slavery feature (L1:F9113) firing on the word "black" alone
- HIV/gay and holiday features co-firing on "Pride" via training-corpus association

None of the high-importance features encode "NAZI", "hypocrisy", "racism is worse than X", or any sentiment about the actual final sentence. The "proud/being/=" lexical features exist but are diluted by larger negative-direct_effect features (L0:F12717 "pride" contributes −0.13, L0:F45 "being" contributes −0.10) while the positive direct_effect is dominated by the spurious identity-category signals. The classifier has learned "mentions of an identity group + Pride/gay tokens → toxic" rather than reading the actual rhetorical content.

The "demographic identity" L3 supernode and the race/slavery L1 supernode are the most concerning — they are exactly the kind of "spurious 'identity group' signals" the user warned about, abstracting away the prompt's specific comparison of Black Pride = OK, Gay Pride = OK, White Pride = NAZI to a flat "race words present" trigger.

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
| [L0:F1015](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1015) | 1 | L0 identity-token detectors |  the word "black" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1015) |
| [L0:F1015](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1015) | 5 | L0 identity-token detectors |  the word "black" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1015) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 17 | L0 identity-token detectors |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F13069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13069) | 1 | L0 identity-token detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13069) |
| [L0:F12717](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12717) | 2 | L0 pride/being/equals token detectors |  the word "pride" in different contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12717) |
| [L0:F45](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/45) | 4 | L0 pride/being/equals token detectors | the word "being" in different contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/45) |
| [L0:F12054](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12054) | 4 | L0 pride/being/equals token detectors | the word "being" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12054) |
| [L0:F9222](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9222) | 3 | L0 pride/being/equals token detectors |  the equals sign | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9222) |
| [L0:F5463](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5463) | 3 | L0 pride/being/equals token detectors |  uses of the equals sign in mathematical contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5463) |
| [L0:F10074](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10074) | 2 | L0 unrelated lexical features (San Diego, pronouns, paragraph newline) |  mentions of a specific city, San Diego | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10074) |
| [L0:F10164](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10164) | 2 | L0 unrelated lexical features (San Diego, pronouns, paragraph newline) |  relative pronouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10164) |
| [L0:F7894](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7894) | 8 | L0 unrelated lexical features (San Diego, pronouns, paragraph newline) |  line breaks that indicate a paragraph or section beginning | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7894) |
| [L0:F2177](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2177) | 2 | L0 unrelated lexical features (San Diego, pronouns, paragraph newline) |  capitalized words or phrases | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2177) |
| [L0:F1088](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1088) | 2 | L0 unrelated lexical features (San Diego, pronouns, paragraph newline) | mentions of "meal" and, to a lesser extent, words indicating a fondness for something | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1088) |
| [L1:F9113](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) | 5 | L1: race/slavery discussion feature |  discussions about race and slavery | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) |
| [L1:F12078](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12078) | 2 | L1: race/slavery discussion feature |  the word "proud" and words associated with oaths or declarations of loyalty | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12078) |
| [L2:F5266](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5266) | 4 | L2: 'being' phrases + LaTeX/code noise | phrases that include the word "being" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5266) |
| [L2:F1311](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1311) | 3 | L2: 'being' phrases + LaTeX/code noise |  LaTeX math mode code | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1311) |
| [L2:F6014](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6014) | 8 | L2: 'being' phrases + LaTeX/code noise | technical words from a variety of fields including physics, data recovery, programming, and German grammar. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6014) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 2 | L3: demographic identity (race/gender) features |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L3:F16373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) | 2 | L3: demographic identity (race/gender) features |  mentions of demographic identity, especially race and gender | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) |
| [L3:F15701](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15701) | 2 | L3: demographic identity (race/gender) features | instances of the word "proud" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15701) |
| [L3:F11279](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11279) | 3 | L3: demographic identity (race/gender) features |  symbols common in scientific research papers, such as p-values and replicates | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11279) |
| [L3:F12020](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12020) | 4 | L3: demographic identity (race/gender) features |  the word "being" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12020) |
| [L4:F192](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/192) | 3 | L4: equals/maths formula feature | equal signs adjacent to numbers, letters and symbols, which may be mathematical formulas | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/192) |
| [L4:F5217](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5217) | 2 | L4: equals/maths formula feature |  words and abbreviations that often appear in URLs or website names | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5217) |
| [L5:F615](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/615) | 2 | L5: named holidays/days feature |  named holidays or days of the year | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/615) |
| [L6:F15295](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15295) | 2 | L6: HIV/AIDS + gay-promoted words feature (fires on 'Pride') |  words and abbreviations related to HIV/AIDS and viral infections. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15295) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:12717 de=-0.133 |
| 3 | `inspect_feature` ×19 | L3:15701, L3:11279, L0:12717, L1:13069, L0:9222, L0:45, L1:9113, L3:12034, L0:1088, L0:2177, L2:5266, L0:12054, L0:10164, L6:15295, L0:1015, L5:615, L0:10074, L0:7894, L4:192 |
| 4 | `get_upstream_features` | Emb:" Pride"@2 (de=10.75) +9 more |
| 5 | `get_upstream_features` | Emb:" Pride"@2 (de=12.69) +9 more |
| 6 | `get_upstream_features` | Emb:" ="@3 (de=15.94) +9 more |
| 7 | `get_upstream_features` | Emb:" black"@5 (de=17.50) +9 more |
| 8 | `inspect_feature` ×4 | L3:13061, L4:5217, L3:16373, L3:12034 |
| 9 | `get_top_features` | 30 features; top: L0:12717 de=-0.133 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F15295@2` | ❌ error | — | — | Trace this feature — HIV/AIDS words feature. Why is it firing on the "Pride" tok… |
| SA-2 | `L5:F615@2` | ❌ error | — | — | Trace this "named holidays" feature firing on "Pride". Why is it firing? What is… |
| SA-3 | `L3:F13061@2` | ❌ error | — | — | Trace this "race/gender/social issues" feature. What input does it pick up on? |
| SA-4 | `L1:F9113@5` | ❌ error | — | — | Trace this "race/slavery discussions" feature at position 5. What's the upstream… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F12717@2, k=10 → Emb:" Pride"@2 (de=11.69) +9 more |
| 2 | `get_upstream_features` | L3:F15701@2, k=10 → Emb:" Pride"@2 (de=18.62) +9 more |
| 3 | `get_upstream_features` | L3:F11279@3, k=10 → Emb:" ="@3 (de=11.31) +9 more |
| 4 | `get_upstream_features` | L1:F13069@1, k=10 → Emb:"Black"@1 (de=19.38) +9 more |
| 5 | `get_upstream_features` | L0:F3436@17, k=5 → Emb:"White"@17 (de=16.75) +4 more |
| 6 | `inspect_feature` ×13 | L2:1311, L0:6704, L0:1088, L0:12054, L0:10074, L0:3436, L2:6014, L3:7084, L3:12020, L0:5463, L1:12078, L0:7019, L0:12292 |

### Build

`build_circuit` → 16 nodes, 31 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 80,557 | 10,710 | 465,114 | 0 | $0.0649 | — | — |
| **Total** | | **80,557** | **10,710** | **465,114** | **0** | **$0.0649** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 52s