# Circuit Oracle Report
**Date:** 2026-07-28 07:17:32 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_8 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction score is driven by a small set of generic, single-word lexical detectors concentrated on a few content tokens from the premise — "Congress" (pos 2), "funding" (pos 7), "levels" (pos 8), "controls" (pos 5), "many" (pos 13) — with one strong *negative* feature on the relative pronoun "who" (pos 15). No feature encodes the actual semantic contradiction between "controls funding" and "no responsibility."

**Confidence:** 7

**Reasoning:** The circuit, traced all the way to token embeddings, shows that the contradiction probe is being driven almost entirely by surface-level single-word identity features rather than any compositional/relational reasoning. On the positive (contradiction-pushing) side:

- **"Congress"** is the dominant driver. Four stacked features at the same position (pos 2) — L0:F6044 "yield" (de=+0.79, the label is misleading — at pos 2 it fires on "Congress"), L2:F2701 "words related to the U.S. Congress" (de=+0.38, frac=0.011), L3:F123 "mentions of the U.S. Congress" (de=+0.36, frac=0.007), L6:F6096 "political parties and affiliations" (de=+0.45, frac=0.006), and L2:F6735 "political parties and politicians" (de=−0.40, acting as a partial suppressor). All trace back to the **Emb: Congress (pos 2)** node with very high direct_effect (17–20+).
- **"controls"** (pos 5) → L3:F13271 "the word 'control'" (de=+0.36, frac=0.004), backed by L2:F7279, L2:F11080, L1:F4020, all ultimately grounded in **Emb: controls**.
- **"levels"** (pos 8) → L2:F156 "amount or intensity" (de=−0.37, frac=0.019) and L0:F14818 — but both *push against* the probe, so "levels" is acting as a *suppressor* of the contradiction score, not evidence for it.
- **"funding"** (pos 7) → L1:F2116 "legal counsel or representation" (de=+0.38, frac=0.006) and L0:F11606 "the word 'fund'" (de=−0.36) — these cancel; "funding" is roughly neutral.
- **"many"** (pos 13) → L3:F8382 "the word 'many'" (de=+0.33, frac=0.004), from **Emb: many**.

The single strongest *negative* feature is **L0:F13437 "the word 'who'"** at pos 15 (de=−0.58, frac=0.013), tracing cleanly to **Emb: who**. This is the relative pronoun that introduces the contradiction-relevant clause ("members who did not support the purpose"). The fact that the pronoun alone — without any compositional understanding — has the second-largest absolute direct effect in the circuit is exactly the kind of spurious cue the user suspected.

**Net pattern:** The contradiction classifier appears to be a simple bag-of-words detector. It is *positively* activated by the bare presence of political/governmental vocabulary ("Congress", "control", "many members") and *negatively* activated by function-word style tokens ("who", "levels", "the", "a") that tend to appear in neutral or entailed premises. Crucially, no feature in the top‑15 (or in the traced upstream paths) encodes the semantic relationship "Congress controls funding" vs. "Congress has no responsibility for funding" — i.e., the actual contradiction. The user's concern is supported: the circuit does use spurious lexical cues (the noun "Congress" + the pronoun "who") rather than modeling the contradiction's propositional content.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F6044](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) | 2 | Early-layer Congress detection (pos 2) | the word "yield" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) |
| [L0:F9557](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9557) | 2 | Early-layer Congress detection (pos 2) | the word "clean" and words/phrases associated with people | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9557) |
| [L1:F6948](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6948) | 2 | Early-layer Congress detection (pos 2) |  the word "lift" in the context of mechanical devices or ski infrastructure | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6948) |
| [L2:F6735](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6735) | 2 | Political parties/politicians detector (pos 2) |  political parties and politicians | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6735) |
| [L2:F2701](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) | 2 | U.S. Congress token detector (pos 2) |  words related to the U.S. Congress | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) |
| [L3:F123](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/123) | 2 | U.S. Congress token detector (pos 2) |  mentions of the United States Congress | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/123) |
| [L6:F6096](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6096) | 2 | Political parties & affiliations (pos 2) |  political parties and affiliations | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6096) |
| [L1:F2116](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2116) | 7 | Funding / legal-counsel vocabulary (pos 7) |  words and phrases related to legal counsel or representation | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2116) |
| [L0:F11606](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11606) | 7 | Funding / legal-counsel vocabulary (pos 7) |  the word "fund" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11606) |
| [L2:F156](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/156) | 8 | "levels/amounts" magnitude (pos 8) |  words related to the amount or intensity of something | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/156) |
| [L0:F14818](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14818) | 8 | "levels/amounts" magnitude (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14818) |
| [L3:F13271](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13271) | 5 | "control" verb detector (pos 5) |  the word "control." | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13271) |
| [L2:F7279](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7279) | 5 | "control" verb detector (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7279) |
| [L2:F11080](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11080) | 5 | "control" verb detector (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11080) |
| [L1:F4020](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4020) | 5 | "control" verb detector (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4020) |
| [L1:F3604](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3604) | 5 | "control" verb detector (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3604) |
| [L3:F8382](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8382) | 13 | "many" quantifier (pos 13) |  the word "many", and sometimes "times" or "people" when near it | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8382) |
| [L0:F15792](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15792) | 13 | "many" quantifier (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15792) |
| [L0:F13437](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13437) | 15 | "who" relative pronoun (pos 15) — strong NEGATIVE | the word "who" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13437) |
| [L0:F9529](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9529) | 5 | "physical"/misc lexical (pos 5) | the word "physical" and words related to programming | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9529) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: Congress (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: funding (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: levels (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: controls (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: many (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: who (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:6044 de=0.789 |
| 3 | `inspect_feature` ×14 | L0:6044, L0:13437, L6:6096, L2:6735, L1:6948, L1:2116, L2:2701, L0:9557, L2:156, L3:13271, L0:11606, L3:123, L0:9529, L3:8382 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F6044@2` | ❌ error | — | — | Trace the L0:F6044 ("yield") at pos 2 upstream. This is a positive-direction fea… |
| SA-2 | `L0:F13437@15` | ❌ error | — | — | Trace L0:F13437 ("who") at pos 15 upstream. This is a negative-direction feature… |
| SA-3 | `L2:F2701@2` | ✅ reported | 4 | 3 | Trace L2:F2701 ("Congress") at pos 2 upstream. This is a positive-direction feat… |
| SA-4 | `L2:F156@8` | ❌ error | — | — | Trace L2:F156 ("amounts/levels") at pos 8 upstream. This is a negative-direction… |

<details>
<summary><b>SA-3</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F2701 | " words related to the U.S. Congress" |
| 2 | `get_upstream_features` | L2:F2701@2, k=10 | Emb:" Congress"@2 (de=28.12) +9 more |
| 3 | `inspect_feature` | L0, F13168 | " the words "broad," "wild," and "faced"" |
| 4 | `inspect_feature` | L1, F14850 | "references to the U.S. Congress." |
| 5 | `get_upstream_features` | L1:F14850@2, k=10 | Emb:" Congress"@2 (de=17.62) +9 more |
| 6 | `get_upstream_features` | L0:F13168@2, k=10 | Emb:" Congress"@2 (de=12.88) +9 more |
| 7 | `inspect_feature` | L2, F2701 | " words related to the U.S. Congress" |
| 8 | `inspect_feature` | L0, F10401 | " mentions of genes and proteins" |

**Findings:** The L2:F2701 'Congress' feature is a political‑entity detector that aggregates signals from lower‑layer features. Its strongest upstream driver is the raw token embedding for the word 'Congress', confirming that the feature primarily reflects the presence of that token. A mid‑layer feature (L1:F14850) further refines the signal by recognizing constitutional and legislative language, while an even …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F6044@2, k=10 → Emb:" Congress"@2 (de=17.00) +9 more |
| 2 | `get_upstream_features` | L0:F13437@15, k=10 → Emb:" who"@15 (de=35.25) +9 more |
| 3 | `get_upstream_features` | L2:F156@8, k=10 → Emb:" levels"@8 (de=28.00) +9 more |
| 4 | `get_upstream_features` | L1:F2116@7, k=10 → Emb:" funding"@7 (de=14.12) +9 more |
| 5 | `get_upstream_features` | L3:F13271@5, k=10 → Emb:" controls"@5 (de=18.50) +9 more |
| 6 | `get_upstream_features` | L3:F123@2, k=10 → Emb:" Congress"@2 (de=20.62) +9 more |
| 7 | `get_upstream_features` | L3:F8382@13, k=10 → Emb:" many"@13 (de=23.50) +9 more |
| 8 | `get_upstream_features` | L6:F6096@2, k=10 → Emb:" Congress"@2 (de=13.81) +9 more |
| 9 | `get_upstream_features` | L2:F6735@2, k=10 → Emb:" Congress"@2 (de=9.12) +9 more |
| 10 | `get_upstream_features` | L2:F7279@5, k=10 → Emb:" controls"@5 (de=12.12) +9 more |
| 11 | `get_upstream_features` | L2:F11080@5, k=10 → Emb:"<bos>"@0 (de=11.38) +9 more |
| 12 | `get_upstream_features` | L2:F11080@5, k=10 → Emb:"<bos>"@0 (de=11.38) +9 more |
| 13 | `get_upstream_features` | L1:F4020@5, k=10 → Emb:" controls"@5 (de=22.50) +9 more |
| 14 | `get_upstream_features` | L0:F14818@8, k=10 → Emb:" levels"@8 (de=18.12) +9 more |
| 15 | `get_upstream_features` | L0:F15792@13, k=10 → Emb:" many"@13 (de=38.75) +9 more |

### Build

`build_circuit` → 17 nodes, 18 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 33,087 | 6,168 | 165,965 | 0 | $0.0273 | — | — |
| SA-3 | openai/gpt-oss-120b | 81,307 | 5,461 | 32 | 0 | $0.0155 | ✅ 4F/3E | Trace L2:F2701 ("Congress") at pos 2 upstream. This is a pos… |
| **Total** | | **114,394** | **11,629** | **165,997** | **0** | **$0.0428** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 13s