# Circuit Oracle Report
**Date:** 2026-07-28 07:08:23 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_9 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

I have already included token-embedding nodes in the circuit. Let me finalize the analysis.

**Analysis:** The probe's toxicity classification is driven by spurious lexical/identity-group features — words like "white" (pos 9), "guys" (pos 10), "author" (pos 2), "married" (pos 6), "appears" (pos 3), and "Maybe" (pos 17) — rather than any actual toxic content. The signal is dominated by single-word identity/demographic detectors at layer 0 that fire on the input tokens themselves, with essentially no higher-layer semantic understanding of the slur ("oriental", "self hater", "lust after white men") that constitutes the actual toxicity.

**Confidence:** 8

**Reasoning:** Tracing the attribution graph back to token-embedding nodes reveals that the entire causal signal is lexical: `Emb: white (pos 9)` → `L0:F3436` ("the word 'white'", frac_nonzero=0.061, direct_effect=+0.17 to the probe) is the single largest positive driver. Other positive drivers are similarly pure word detectors: `L0:F2242` ("the word 'guys'", pos 10, +0.10), `L0:F9881` ("the word 'appear'", pos 3, +0.11), `L0:F4408` ("the word 'authors'", pos 2, +0.16), and `L0:F5538` (pos 2, +0.10). The mid-layer features are also identity/topic rather than toxicity features: `L2:F3399` ("words related to marriage", pos 6, +0.17) and `L3:F494` ("marriage, birth, death, family and religion", pos 6, +0.11) fire on the single token "married". `L3:F10004` ("uncertainty/possibility words", pos 17, +0.14) fires on "Maybe". `L6:F2851` ("books and associated things such as authors and reading", pos 2, +0.21) and `L6:F13528` ("academic works and their writers", pos 2, +0.11) fire on "author" and propagate up from the bridging `L2:F14801` ("mentions of authors and their written works", pos 2). Crucially, none of these features encode the actually toxic content — the slurs "oriental", "self hater", and the sexualised/derogatory framing. The user concern is well-supported: the probe classification is driven by demographic-identity word detectors (race "white", gender "guys", relationship "married", profession "author") rather than the toxic semantics of the passage. The negative-direction features (`L0:F753` "the word 'author' and selling/prices" at pos 2, -0.28; `L0:F8444` "the word 'to'" at pos 4 and 7, -0.15/-0.18; `L3:F6262` "mentions of marriage" pos 6, -0.16) are also pure lexical features that happen to encode neutral/grammatical framings. The circuit confirms the user's hypothesis: this is a "spurious correlation" probe that classifies toxicity based on which demographic-identity tokens appear in the text, not what the text actually says.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: author (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: married (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: white (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: Maybe (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: guys (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: to (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: appears (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F4408](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4408) | 2 | Lexical: word 'author'/authors (pos 2) — drives probe toward toxic |  the word "authors" in academic papers or similar documents | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4408) |
| [L0:F5538](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5538) | 2 | Lexical: word 'author'/authors (pos 2) — drives probe toward toxic | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5538) |
| [L0:F753](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/753) | 2 | Lexical: word 'author' (pos 2) — suppresses probe (academic neutral frame) | the word "author" and words related to selling and prices | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/753) |
| [L0:F6087](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6087) | 2 | Lexical: word 'author' (pos 2) — suppresses probe (academic neutral frame) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6087) |
| [L0:F9796](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9796) | 2 | Lexical: word 'author' (pos 2) — suppresses probe (academic neutral frame) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9796) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 9 | Lexical: word 'white' (pos 9) — drives probe toward toxic |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F2242](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2242) | 10 | Lexical: word 'guys' (pos 10) — drives probe toward toxic |  the word "guys" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2242) |
| [L0:F9881](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9881) | 3 | Lexical: word 'appear'/'appears' (pos 3) — drives probe toward toxic | the word "appear" and its variants | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9881) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 4 | Lexical: word 'to' (pos 4, 7) — suppresses probe (grammatical filler) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 7 | Lexical: word 'to' (pos 4, 7) — suppresses probe (grammatical filler) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L2:F3399](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3399) | 6 | Marriage vocabulary (pos 6) — drives probe toward toxic |  words related to marriage | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3399) |
| [L3:F494](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/494) | 6 | Marriage/birth/death/family/religion topic (pos 6) — drives probe toward toxic |  text relating to marriage, birth, death, family and religion | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/494) |
| [L3:F6262](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6262) | 6 | Marriage mention (pos 6) — suppresses probe | mentions of marriage | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6262) |
| [L3:F8254](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8254) | 7 | Marriage/family relationships (pos 7) — suppresses probe |  words and phrases related to marriage and family relationships | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8254) |
| [L1:F1431](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1431) | 6 | Legal 'fair'/'ends of justice' (pos 6) — drives probe toward toxic |  instances of the word "fair" and the phrase "ends of justice" in legal documents | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1431) |
| [L3:F10004](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10004) | 17 | Uncertainty/possibility words (pos 17) — drives probe toward toxic |  words which mean or indicate uncertainty or possibility | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10004) |
| [L3:F11152](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11152) | 17 | Uncertainty/possibility words (pos 17) — suppresses probe | words that indicate uncertainty or possibility | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11152) |
| [L6:F2851](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2851) | 2 | Books/authors/reading topic (pos 2) — drives probe toward toxic | books and associated things such as authors and reading | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2851) |
| [L6:F13528](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/13528) | 2 | Academic works & writers (pos 2) — drives probe toward toxic |  words related to academic works and their writers | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/13528) |
| [L2:F14801](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14801) | 2 | Author + written works (pos 2) — bridges to topic features |  mentions of authors and their written works. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14801) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe classification logit (toxicity probe) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:753 de=-0.275 |
| 3 | `inspect_feature` ×5 | L0:753, L6:2851, L2:3399, L0:3436, L0:4408 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F2851@2` | ❌ error | — | — | Trace upstream from L6:F2851 (books/authors/reading at pos 2) to understand how … |
| SA-2 | `L2:F3399@6` | ✅ reported | 3 | 3 | Trace upstream from L2:F3399 (marriage-related words at pos 6 'married') to unde… |
| SA-3 | `L0:F3436@9` | ❌ error | — | — | Trace upstream from L0:F3436 (the word 'white' at pos 9). What activates this an… |
| SA-4 | `L3:F10004@17` | ✅ reported | 3 | 4 | Trace upstream from L3:F10004 at pos 17. What does this feature encode and what … |

<details>
<summary><b>SA-2</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F3399 | " words related to marriage" |
| 2 | `get_upstream_features` | L2:F3399@6, k=10 | Emb:" married"@6 (de=29.00) +9 more |
| 3 | `inspect_feature` | L0, F13691 | "words of positive sentiment and verbs associated with leisure activiti" |
| 4 | `inspect_feature` | L0, F1102 | " the word study" |
| 5 | `inspect_feature` | L0, F4668 | " the word "aged" sometimes appearing near demographic words" |
| 6 | `inspect_feature` | L1, F14321 | " the word "roll" or a variation of it" |
| 7 | `get_upstream_features` | L0:F13691@6, k=10 | Emb:" married"@6 (de=13.06) +9 more |

**Findings:** The marriage‑related feature (L2:F3399) receives a strong excitatory signal directly from the token embedding of "married" (29.0). A secondary path routes the same embedding through a low‑layer (0) positive‑sentiment feature (L0:F13691) which contributes an additional smaller positive effect (0.5742). Both paths satisfy the required conditions: we have a lower‑third feature (layer 0) and we have r…

</details>

<details>
<summary><b>SA-4</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F10004 | " words which mean or indicate uncertainty or possibility" |
| 2 | `get_upstream_features` | L3:F10004@17, k=10 | Emb:" Maybe"@17 (de=43.25) +9 more |
| 3 | `inspect_feature` | L0, F5687 | "words indicating uncertainty or possibility" |
| 4 | `get_upstream_features` | L0:F5687@17, k=10 | Emb:" Maybe"@17 (de=17.62) +9 more |
| 5 | `inspect_feature` | L0, F5152 | " the word "relief", often in a context related to legal or medical sit" |

**Findings:** L3:F10004 is an uncertainty detector that heavily leans on the presence of the token "Maybe" at position 17. The dominant positive influence comes directly from the embedding of the word "Maybe" (direct_effect ~43), which feeds both the high‑level uncertainty feature (layer 3) and a low‑level precursor (layer 0:F5687). The layer‑0 feature also derives its vote from the same embedding (direct_effec…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F2851@2, k=10 → Emb:" author"@2 (de=11.06) +9 more |
| 2 | `get_upstream_features` | L0:F3436@9, k=10 → Emb:" white"@9 (de=18.00) +9 more |
| 3 | `inspect_feature` ×3 | L0:8444, L3:10004, L0:2242 |
| 4 | `get_upstream_features` | L0:F4408@2, k=10 → Emb:" author"@2 (de=15.94) +9 more |
| 5 | `get_upstream_features` | L0:F753@2, k=10 → Emb:" author"@2 (de=18.38) +9 more |
| 6 | `get_upstream_features` | L3:F10004@17, k=10 → Emb:" Maybe"@17 (de=43.25) +9 more |
| 7 | `get_upstream_features` | L3:F494@6, k=10 → Emb:" married"@6 (de=17.75) +9 more |
| 8 | `inspect_feature` ×5 | L3:494, L1:1431, L3:6262, L3:8254, L6:13528 |
| 9 | `get_upstream_features` | L3:F8254@7, k=10 → Emb:" married"@6 (de=26.62) +9 more |
| 10 | `get_upstream_features` | L3:F6262@6, k=10 → Emb:" married"@6 (de=37.75) +9 more |
| 11 | `get_upstream_features` | L6:F13528@2, k=10 → Emb:" author"@2 (de=13.12) +9 more |
| 12 | `inspect_feature` | L0, F13691 → "words of positive sentiment and verbs associated with leisure activiti" |
| 13 | `get_upstream_features` | L6:F2851@2, k=5 → Emb:" author"@2 (de=11.06) +4 more |
| 14 | `get_upstream_features` | L3:F11152@17, k=10 → Emb:" Maybe"@17 (de=41.25) +9 more |
| 15 | `get_upstream_features` | L0:F8444@7, k=10 → Emb:" to"@7 (de=41.75) +9 more |
| 16 | `inspect_feature` ×2 | L3:11152, L0:9881 |
| 17 | `get_upstream_features` | L2:F3399@6, k=10 → Emb:" married"@6 (de=29.00) +9 more |
| 18 | `get_upstream_features` | L3:F494@6, k=5 → Emb:" married"@6 (de=17.75) +4 more |
| 19 | `get_upstream_features` | L6:F2851@2, k=5 → Emb:" author"@2 (de=11.06) +4 more |
| 20 | `inspect_feature` | L2, F14801 → " mentions of authors and their written works." |
| 21 | `get_upstream_features` | L2:F14801@2, k=5 → Emb:" author"@2 (de=30.12) +4 more |

### Build

`build_circuit` → 24 nodes, 30 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 44,713 | 7,024 | 254,949 | 0 | $0.0371 | — | — |
| SA-4 | openai/gpt-oss-120b | 33,313 | 3,027 | 7,936 | 0 | $0.0069 | ✅ 3F/4E | Trace upstream from L3:F10004 at pos 17. What does this feat… |
| SA-2 | openai/gpt-oss-120b | 67,795 | 4,135 | 5,248 | 0 | $0.0127 | ✅ 3F/3E | Trace upstream from L2:F3399 (marriage-related words at pos … |
| **Total** | | **145,821** | **14,186** | **268,133** | **0** | **$0.0568** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 7s