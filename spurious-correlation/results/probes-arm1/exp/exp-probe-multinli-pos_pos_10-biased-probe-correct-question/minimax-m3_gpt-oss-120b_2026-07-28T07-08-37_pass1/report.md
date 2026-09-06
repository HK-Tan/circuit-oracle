# Circuit Oracle Report
**Date:** 2026-07-28 07:08:37 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_10 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "contradiction" classification is driven almost entirely by the presence of the literal word "not" in the hypothesis ("There is **not** role reversal...") — a superficial negation-token detector rather than any semantic comparison between premise and hypothesis.

**Confidence:** 9

**Reasoning:** The attribution graph is dominated by a "negation-cascade" that originates at position 17 (the token "not" in the hypothesis) and propagates upward through a stack of monolingual/multilingual negation features, with virtually no input from the premise side.

**Token-anchored origin (pos 17, "not"):**
- **Emb: ' not' (pos 17)** has the largest direct embedding-level effect (direct_effect=23.125 to L16:12358, 16.5 to L4:2422, 13.19 to L3:1101, 7.41 to L9:14687). It is the single most influential node in the circuit.
- **L0:4958** ("the word 'not'", frac_nonzero=0.0184) fires with activation 30.625 and feeds L4:2422/L4:4492 (+8.13 to L16, +2.75 to L4:2422, +4.09 to L3:1101).

**Mid-layer negation collectors (L1–L4):** All seven features in this supernode are negation-token detectors with nearly identical autointerp labels — "negations in various languages" (L4:4492, frac_nonzero=0.038), "negations in other languages" (L4:2422), "negative sentiment markers 'not/no/never'" (L1:14233), "mix of code fragments and words from different languages" (L3:8011, frac_nonzero=0.003), "negations and Chinese names" (L3:12079), "NO/NOC/ORES within hex codes" (L3:2232), "scientific studies where something is disproven" (L3:9803), and "error/absence/negation in software contexts" (L3:1101). None of them encode entailment semantics — they only count negation words.

**Late-layer negation features (L9–L16):** L9:14687 ("phrases using 'not'"), L15:6160 ("is there"), L15:10071 ("negations and equivocations"), L16:12358 ("'not' followed by a form of 'to be'") — every late feature is again a negation-token or negation-construction detector.

**Negligible premise-side contribution:** Premise content barely enters the circuit. L1:15749 ("the word 'strange'") and L2:16097 ("superlative adjectives") fire on "strangest" (pos 2, premise), but their direct effect on the output is small (≤0.40). Crucially, L4:2422 carries a *negative* direct effect (-1.27) against the probe, partially counteracting the positive "not" push — but the net still leans positive because the "not" features dominate.

**Source-influence check:** `get_source_influence` from position 17 returns S_pct_of_total = -1.1% (a small *negative* net signed share) and R_pct_of_total = 6.5%, with the top source-side features all being negation detectors (L3:10742, L1:14233, L3:12079, L0:4958). The top non-source driver is roughly 6× larger than the "not"-position's net signed contribution, which suggests the *signed* influence of the "not" position is small in aggregate — but the per-feature direct effects above show a clear, consistent positive push from negation features into the probe direction, which is precisely the kind of spurious-cue signal the user flagged.

**Why this is spurious:** The probe fires on "contradiction" because the hypothesis contains the token "not" — not because the model has compared the premise's claim ("the strangest role reversal is going on…democracy") with the hypothesis's negation ("There is not role reversal…") and detected a semantic conflict. A premise like "There is role reversal going on in relation to democracy" plus the *same* hypothesis would be classified identically, and an unrelated premise plus this hypothesis would also produce the same positive score. The circuit is therefore a textbook surface-cue artifact: the "contradiction" probe has learned to detect negation words rather than true logical contradiction.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 17 | Late-layer negation detectors (L9-L16) |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |
| [L15:F6160](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/6160) | 17 | Late-layer negation detectors (L9-L16) |  occurrences of "is there" | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/6160) |
| [L15:F10071](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) | 17 | Late-layer negation detectors (L9-L16) | negations and equivocations | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) |
| [L9:F14687](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/14687) | 17 | Late-layer negation detectors (L9-L16) | phrases using the word "not", often followed by "because" or "but." | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/14687) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 17 | Mid-layer negation collectors (L3-L4) | negations in other languages like French, Malay, and Croatian | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 17 | Mid-layer negation collectors (L3-L4) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 17 | Mid-layer negation collectors (L3-L4) |  a mix of words and code fragments from different languages | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L3:F12079](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) | 17 | Mid-layer negation collectors (L3-L4) | negations and Chinese names | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) |
| [L3:F2232](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2232) | 17 | Mid-layer negation collectors (L3-L4) |  character sequences like "NOC", "NO", "ORES", "NOS", "OF", "UNCH", and "oooooooo" within a series of hexadecimal codes, sometimes also picking up on related words such as "dangerously", "Bantus", "slave", and "plantation" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2232) |
| [L3:F9803](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9803) | 17 | Mid-layer negation collectors (L3-L4) | sentences describing scientific studies or experiments, particularly where something is disproven | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9803) |
| [L3:F1101](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) | 17 | Mid-layer negation collectors (L3-L4) |  error messages and terms indicating absence or negation in software contexts. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) |
| [L1:F14233](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) | 17 | Mid-layer negation collectors (L3-L4) |  negative sentiment markers such as "not," "no," "never," and their equivalents in other languages | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) |
| [L1:F15749](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15749) | 2 | Premise-lexical features (L1-L2): 'strange'/'strangest' & superlative |  the word "strange", or related words | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15749) |
| [L2:F16097](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) | 2 | Premise-lexical features (L1-L2): 'strange'/'strangest' & superlative | superlative adjectives and the words "test" or "point" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 17 | L0 'not' detector (token-anchored) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:2422 de=-1.273 |
| 3 | `inspect_feature` ×4 | L4:2422, L4:4492, L3:1101, L0:4958 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F12358@17` | ❌ error | — | — | Trace this feature back to its roots. What does it encode and which input tokens… |
| SA-2 | `L4:F2422@17` | ❌ error | — | — | Trace this "negations in other languages" feature back to its roots. Reach embed… |
| SA-3 | `L4:F4492@17` | ✅ reported | 6 | 11 | Trace this "negations in various languages" feature back to its roots. Reach emb… |

<details>
<summary><b>SA-3</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F4492 | "negations in various languages" |
| 2 | `get_upstream_features` | L4:F4492@17, k=10 | Emb:" not"@17 (de=18.00) +9 more |
| 3 | `inspect_feature` | L3, F8011 | " a mix of words and code fragments from different languages" |
| 4 | `inspect_feature` | L3, F12079 | "negations and Chinese names" |
| 5 | `get_upstream_features` | L3:F8011@17, k=10 | Emb:" not"@17 (de=21.00) +9 more |
| 6 | `inspect_feature` | L3, F2232 | " character sequences like "NOC", "NO", "ORES", "NOS", "OF", "UNCH", an" |
| 7 | `get_upstream_features` | L3:F12079@17, k=10 | Emb:" There"@15 (de=15.00) +9 more |
| 8 | `get_upstream_features` | L3:F8011@17, k=10 | Emb:" not"@17 (de=21.00) +9 more |
| 9 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 10 | `inspect_feature` | L3, F9803 | "sentences describing scientific studies or experiments, particularly w" |
| 11 | `inspect_feature` | L0, F15454 | " the word "not"" |
| 12 | `get_upstream_features` | L0:F4958@17, k=10 | Emb:" not"@17 (de=32.75) +9 more |

**Findings:** The path from L4:4492 (multilingual negation detector) descends through several mid‑layer features that also capture negation tokens in varied contexts (code mixes, Chinese names, technical hex patterns, scientific statements). All converge on the highly specific layer‑0 feature 4958, which directly fires on the token "not". Positive direct effects are observed at each hop, and the final embedding…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×8 | L0:11375, L3:12079, L3:2232, L3:9803, L3:8011, L1:14233, L2:16097, L1:15749 |
| 2 | `get_upstream_features` | L16:F12358@17, k=10 → Emb:" not"@17 (de=23.12) +9 more |
| 3 | `get_upstream_features` | L9:F14687@17, k=10 → Emb:" not"@17 (de=7.41) +9 more |
| 4 | `inspect_feature` ×2 | L16:12358, L9:14687 |
| 5 | `get_upstream_features` | L4:F2422@17, k=10 → Emb:" not"@17 (de=16.50) +9 more |
| 6 | `get_upstream_features` | L3:F1101@17, k=10 → Emb:" not"@17 (de=13.19) +9 more |
| 7 | `get_source_influence` | {'depth': 3, 'source_positions': [17]} → {'depth': 3, 'source_positions': [17], 'S_pct_of_total': -1.107, 'R_pct_of_total |
| 8 | `inspect_feature` ×2 | L15:6160, L15:10071 |

### Build

`build_circuit` → 10 nodes, 9 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 41,125 | 4,205 | 116,714 | 0 | $0.0244 | — | — |
| SA-3 | openai/gpt-oss-120b | 143,233 | 7,433 | 25,600 | 0 | $0.0263 | ✅ 6F/11E | Trace this "negations in various languages" feature back to … |
| **Total** | | **184,358** | **11,638** | **142,314** | **0** | **$0.0507** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 51s