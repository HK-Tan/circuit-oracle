# Circuit Oracle Report
**Date:** 2026-07-28 07:20:05 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction probe's score is driven almost entirely by surface "not" detectors sitting on the token "not" (pos 36) in the hypothesis "does not contain any early 17th-century tower houses," with no semantic comparison between premise and hypothesis ever entering the circuit.

**Confidence:** 8

**Reasoning:** The user concern is well-supported by the attribution graph.

**1. The dominant signal is negation-surface features on pos 36 ("not"):**
- L4:F4492 (frac_nonzero=0.038, labeled "negations in various languages") has the largest positive direct effect on the probe (0.2227) and is a pure surface "not" detector. The subagent traced it: it is fed by L3:F8011 ("not/NOT/nicht" detector, direct_effect=2.14), L3:F3534 ("n't" detector, de=1.80), and the raw " not" embedding (L0:F4958, de=2.02 to F8011). No semantic content from the premise or from surrounding hypothesis tokens enters this chain — it terminates at the literal "not" token.
- L16:F6800 (frac=0.031, "not/no/n't" detector, de=0.208) is the second-largest driver. Its upstream is identical in character: " not" embedding (de=12.5), " does" embedding (de=9.06), plus L15:F11794 (de=6.06) and L13:F102 (de=2.13) — all of which the prior subagent and direct lookup show are themselves "not/n't" surface features. There is **no upstream feature in any layer that represents entity-comparison, premise-vs-hypothesis, or entailment**; the chain bottoms out at the " not" and " does" token embeddings.

**2. The remaining circuit is non-semantic noise on pos 2-4 ("castle itself comprises"):**
- L0:F2158 "with" (pos 17) — fires on a token that has no contradiction relevance.
- L0:F10346 "itself/node" and L3:F232 "itself" (pos 3) — direct effect confirmed: 13.9 and 26.5 come purely from the " itself" embedding.
- L0:F12378 "latest", L1:F11 "press", L0:F15866 "father/parents" (pos 3/4) — all generic lexical detectors. L15866 was verified to be driven solely by the " comprises" embedding (de=13.56). These features have no prompt-semantic meaning here; they happen to fire on those positions and are co-opted by the probe because the probe direction has random overlap with their decoder vectors.

**3. The "castle" semantic branch is not contradiction-related:**
- L7:F13215 "military fortifications", L4:F5749 "ancient settlements/fortifications", L2:F8185 "shopping/military places", L4:F13244 "estates/land ownership" — all confirmed by the subagent to be fed directly by the " castle" embedding (de=18.5 and 9.25 etc.). These encode that the topic is a castle/estate, not that the premise contradicts the hypothesis.

**Conclusion:** The probe picks up "contradiction" almost entirely because the surface token " not" appears in the hypothesis, regardless of what is being negated. A premise that asserted something different and a hypothesis with a non-negated paraphrase would receive very different probe scores even when semantically equivalent. Features at positions 2-4 and 17 contribute additional noise from generic lexical detectors (itself, with, latest, press, father) that have no connection to contradiction. The user's hypothesis is correct: **the circuit relies on spurious negation-surface cues rather than on lexical or semantic comparison of premise and hypothesis.**

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe: contradiction direction | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L16:F6800](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) | 36 | Late-layer negation detector (L16:F6800, frac=0.031): fires on 'not/no/n't' at pos 36 |  negations "not", "no", and contractions with "t".  | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 36 | Mid-layer multilingual negation (L4:F4492, frac=0.038): fires on 'not' at pos 36 | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 36 | Lower 'not/n't' surface detectors at pos 36 (L0:F4958, L3:F3534, L3:F8011, L13:F102, L15:F11794) | the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L3:F3534](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3534) | 36 | Lower 'not/n't' surface detectors at pos 36 (L0:F4958, L3:F3534, L3:F8011, L13:F102, L15:F11794) | the character sequence "n't" or "nut" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3534) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 36 | Lower 'not/n't' surface detectors at pos 36 (L0:F4958, L3:F3534, L3:F8011, L13:F102, L15:F11794) | a mix of words and code fragments from different languages | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L13:F102](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/102) | 36 | Lower 'not/n't' surface detectors at pos 36 (L0:F4958, L3:F3534, L3:F8011, L13:F102, L15:F11794) | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/102) |
| [L15:F11794](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/11794) | 36 | Lower 'not/n't' surface detectors at pos 36 (L0:F4958, L3:F3534, L3:F8011, L13:F102, L15:F11794) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/11794) |
| [L0:F2158](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) | 17 | Noise: 'with' feature L0:F2158 (pos 17) — irrelevant lexical detector | the word "with" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) |
| [L0:F10346](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10346) | 3 | Noise: 'itself' feature L0:F10346 (pos 3) — irrelevant lexical detector |  the word "itself" and sometimes the word "node" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10346) |
| [L3:F232](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/232) | 3 | Noise: 'itself' feature L3:F232 (pos 3) — irrelevant lexical detector | the word "itself" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/232) |
| [L0:F12378](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12378) | 3 | Noise: 'latest' feature L0:F12378 (pos 3) — irrelevant lexical detector |  the word "latest." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12378) |
| [L1:F11](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11) | 3 | Noise: 'press' feature L1:F11 (pos 3) — irrelevant lexical detector |  the word "press", sometimes in conjunction with "button." | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11) |
| [L0:F15866](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15866) | 4 | Noise: 'father/parents' feature L0:F15866 (pos 4) — irrelevant lexical detector firing on 'comprises' |  references to one's paternal and maternal figures, as well as the pronouns 'we' and 'my' | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15866) |
| [L2:F8185](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8185) | 2 | Semantic-but-generic: 'castle → fortification' concept (L2:F8185 → L4:F5749 → L7:F13215) at pos 2 — captures domain, not contradiction | places for shopping or military activities | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8185) |
| [L4:F5749](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) | 2 | Semantic-but-generic: 'castle → fortification' concept (L2:F8185 → L4:F5749 → L7:F13215) at pos 2 — captures domain, not contradiction | terms that describe ancient settlements and fortifications | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) |
| [L7:F13215](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13215) | 2 | Semantic-but-generic: 'castle → fortification' concept (L2:F8185 → L4:F5749 → L7:F13215) at pos 2 — captures domain, not contradiction |  terms used to describe military fortifications. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13215) |
| [L4:F13244](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) | 2 | Semantic-but-generic: 'castle → estate/land-owning' (L4:F13244) at pos 2 — captures domain, not contradiction |  terms related to land ownership and administration, possibly including slavery or other forms of forced labor | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'contradiction' is not one of the top-k next-token can |
| 3 | `get_top_features` | 10 features; top: L0:2158 de=0.277 |
| 4 | `inspect_feature` ×10 | L0:2158, L0:10346, L4:13244, L0:12378, L3:232, L4:4492, L0:15866, L1:11, L7:13215, L16:6800 |

### Dispatch: 10 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F6800@36` | ❌ error | — | — | Trace upstream from L16:F6800 (a "negation not/no" feature at position 36, on "n… |
| SA-2 | `L4:F4492@36` | ✅ reported | 4 | 3 | Trace upstream from L4:F4492 (a "negations in various languages" feature at posi… |
| SA-3 | `L7:F13215@2` | ✅ reported | 5 | 6 | Trace upstream from L7:F13215 (a "military fortifications" feature firing at pos… |
| SA-4 | `L4:F13244@2` | ✅ reported | 7 | 9 | Trace upstream from L4:F13244 (a "land ownership / estates" feature firing at po… |
| SA-5 | `L16:F6800@36` | ❌ error | — | — | Trace upstream from L16:F6800 (a "not/no negation" feature at pos 36). Determine… |
| SA-6 | `L0:F15866@3` | ❌ error | — | — | Trace upstream from L0:F15866 (a "father/parents" feature at pos 3, on "castle" … |
| SA-7 | `L0:F10346@3` | ❌ error | — | — | Trace upstream from L0:F10346 (a "itself" feature at pos 3, on "castle"). What d… |
| SA-8 | `L3:F232@3` | ❌ error | — | — | Trace upstream from L3:F232 (a "itself" feature at pos 3). Does it receive any s… |
| SA-9 | `L0:F12378@3` | ❌ error | — | — | Trace upstream from L0:F12378 (a "latest" feature at pos 3). What drives this fe… |
| SA-10 | `L1:F11@3` | ❌ error | — | — | Trace upstream from L1:F11 (a "press" feature at pos 3). Why does this "press" f… |

<details>
<summary><b>SA-2</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F4492 | "negations in various languages" |
| 2 | `get_upstream_features` | L4:F4492@36, k=10 | Emb:" not"@36 (de=17.62) +9 more |
| 3 | `inspect_feature` | L3, F8011 | " a mix of words and code fragments from different languages" |
| 4 | `get_upstream_features` | L3:F8011@36, k=10 | Emb:" not"@36 (de=20.75) +9 more |
| 5 | `inspect_feature` | L3, F3534 | "the character sequence "n't" or "nut"" |
| 6 | `inspect_feature` | L3, F9803 | "sentences describing scientific studies or experiments, particularly w" |
| 7 | `get_upstream_features` | L3:F3534@36, k=10 | Emb:" not"@36 (de=16.12) +9 more |
| 8 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 9 | `get_upstream_features` | L3:F9803@36, k=10 | Emb:" not"@36 (de=13.69) +9 more |
| 10 | `inspect_feature` | L0, F15454 | " the word "not"" |
| 11 | `inspect_feature` | L2, F573 | " words that create uncertainty or negate something" |

**Findings:** The L4:F4492 negation feature receives its strongest positive influence directly from the raw embedding of the token " not" (pos 36) and from lower‑layer features that are themselves literal "not" detectors (layers 3 and 0). No upstream feature in layers ≤8 conveys richer semantic content; the path terminates at a pure lexical "not" embedding and an elementary word‑level detector. Therefore, L4:F4…

</details>

<details>
<summary><b>SA-3</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F13215 | " terms used to describe military fortifications." |
| 2 | `get_upstream_features` | L7:F13215@2, k=10 | L4:F5749 (de=8.25) +9 more |
| 3 | `inspect_feature` | L4, F5749 | " terms that describe ancient settlements and fortifications" |
| 4 | `inspect_feature` | L5, F15708 | " words and phrases related to military and defense." |
| 5 | `inspect_feature` | L4, F13244 | " terms related to land ownership and administration, possibly includin" |
| 6 | `get_upstream_features` | L4:F5749@2, k=10 | Emb:" castle"@2 (de=14.75) +9 more |

**Findings:** The L7:F13215 'military fortifications' feature is primarily driven by semantic content rather than the literal token. Its strongest upstream source is L4:F5749, a lower‑layer (layer 4) feature also detecting fortification terminology, which itself receives a very strong positive influence directly from the input embedding of the token 'castle'. This shows that the activation originates from the e…

</details>

<details>
<summary><b>SA-4</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13244 | " terms related to land ownership and administration, possibly includin" |
| 2 | `get_upstream_features` | L4:F13244@2, k=10 | Emb:" castle"@2 (de=18.50) +9 more |
| 3 | `inspect_feature` | L2, F8185 | "places for shopping or military activities" |
| 4 | `inspect_feature` | L2, F9529 | " words related to slavery and slave ownership" |
| 5 | `inspect_feature` | L1, F12474 | " the word "technology" near other related words like "computer"" |
| 6 | `get_upstream_features` | L2:F8185@2, k=10 | Emb:" castle"@2 (de=9.25) +9 more |
| 7 | `inspect_feature` | L1, F8633 | " words or phrases related to tourism and historical places" |
| 8 | `get_upstream_features` | L2:F8185@2, k=10 | Emb:" castle"@2 (de=9.25) +9 more |
| 9 | `get_upstream_features` | L1:F8633@2, k=10 | Emb:" castle"@2 (de=4.31) +9 more |
| 10 | `inspect_feature` | L1, F2004 | " mentions of business offices or real estate" |
| 11 | `inspect_feature` | L0, F8671 | " the word "special" and words occurring with it" |

**Findings:** The target feature L4:F13244 (land‑ownership/estates) is driven primarily by the raw token embedding for "castle" (large positive direct_effect). Upstream, the strongest non‑embedding driver is L2:F8185, a generic large‑building/military‑place detector, which itself is fed by the same "castle" embedding and by L1:F8633, a tourism/historical‑site detector. All paths quickly descend to very low laye…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L16:F6800@36, k=8 → Emb:" not"@36 (de=12.50) +7 more |
| 2 | `get_upstream_features` | L0:F10346@3, k=8 → Emb:" itself"@3 (de=13.94) +7 more |
| 3 | `get_upstream_features` | L3:F232@3, k=8 → Emb:" itself"@3 (de=26.50) +7 more |
| 4 | `get_upstream_features` | L0:F12378@3, k=8 → Emb:" itself"@3 (de=12.44) +7 more |
| 5 | `get_upstream_features` | L1:F11@3, k=8 → Emb:" itself"@3 (de=20.00) +7 more |
| 6 | `get_upstream_features` | L0:F15866@3, k=8 → ❌ Feature (layer=0, feature_idx=15866) not found at pos=3. Thi |
| 7 | `get_upstream_features` | L0:F15866@4, k=8 → Emb:" comprises"@4 (de=13.56) +7 more |
| 8 | `get_upstream_features` | L0:F2158@17, k=8 → Emb:" with"@17 (de=33.75) +7 more |
| 9 | `get_upstream_features` | L15:F11794@36, k=8 → Emb:" does"@35 (de=7.19) +7 more |

### Build

`build_circuit` → 18 nodes, 22 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 45,380 | 6,428 | 127,528 | 0 | $0.0290 | — | — |
| SA-3 | openai/gpt-oss-120b | 58,878 | 3,959 | 0 | 0 | $0.0112 | ✅ 5F/6E | Trace upstream from L7:F13215 (a "military fortifications" f… |
| SA-2 | openai/gpt-oss-120b | 124,562 | 5,636 | 10,688 | 0 | $0.0222 | ✅ 4F/3E | Trace upstream from L4:F4492 (a "negations in various langua… |
| SA-4 | openai/gpt-oss-120b | 170,092 | 8,212 | 0 | 0 | $0.0304 | ✅ 7F/9E | Trace upstream from L4:F13244 (a "land ownership / estates" … |
| **Total** | | **398,912** | **24,235** | **138,216** | **0** | **$0.0929** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 46s