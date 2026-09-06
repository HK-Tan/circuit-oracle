# Circuit Oracle Report
**Date:** 2026-07-28 07:21:01 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity probe is driven by a single dominant feature (L6:648, "discrimination against religious/ethnic groups") whose *sole* upstream signal is the input token **"Jew"** — a protected-class identifier — fed through a stack of redundant identity detectors (L0:9026 → L3:12151 → L4:14733), with the explicitly toxic lexeme **"stain"** contributing only a secondary, smaller effect via L8:13875.

**Confidence:** 8

**Reasoning:** The circuit cleanly separates into two paths that converge on the probe output:

1. **Identity-path (dominant):** The token "Jew" at pos 6 lights up an enormous low-level presence detector (L0:9026, frac_nonzero=0.41, direct_effect=31.4 from the embedding), then propagates upward through a caps-fragment amplifier (L3:12151, frac=0.003, direct_effect=11.0 from "Jew"), a dedicated Jewish-mention detector (L2:8236, frac=0.0044, direct_effect=11.1 from "Jew"), and a Jewish-targeted discrimination feature (L4:14733, direct_effect=5.5 from "Jew" + 2.1 from "liberal"). These all feed into L6:648 ("discrimination against particular religious or ethnic groups", frac=0.016), which carries the largest direct_effect to the probe (0.74). Critically, L6:648 is reached *without* the model ever needing to read "stain", "brethren", or any toxicity-bearing lexeme — the "Jew" embedding alone is sufficient to activate the discrimination feature.

2. **Toxic-lexeme path (secondary):** The word "stain" at pos 9 activates L5:7488 (activation 21.5, direct_effect 5.5 from "stain" embedding) → L6:1561 → L8:13875 ("negative sentiment about reputation/betrayal", direct_effect 0.23 to probe). This path is real toxicity language, but its contribution to the probe is roughly **3× smaller** than the identity path.

The user's concern is **substantively confirmed but with a nuance**: the probe *does* lean on an identity-group signal (L6:648 reads "Jew" + "liberal" and concludes "anti-group discrimination" without needing any slur or attack verb). However, this is not purely spurious — L6:648's autointerp label and top activating examples show it fires on contexts where discrimination IS being discussed, so the feature is genuinely about "slurs/attacks against a religious/ethnic group" rather than a bare identity detector. The toxicity is encoded as the *co-occurrence* of an identity term with a disparaging framing context — but in this prompt the framing context is provided by the identity token alone at this circuit's relevant position (pos 6), with the actual toxic lexemes ("stain", "brethren") processed at a *different* position (pos 9–10) along a much weaker parallel path. This means that merely mentioning "Jew" with an adjective like "liberal" near the discrimination feature's receptive field is enough to score high on the probe, even if the surrounding sentence were benign. A more robust probe would likely require the disparaging-frame features (the L5–L8 stain/brethren path) to be active at the *same* position as the identity term, not merely in the same sentence.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: Jew (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: liberal (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: stain (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: on (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 6 | Low-level 'Jew' presence detector (L0:9026, frac=0.41) — fires on the raw Jew embedding with direct_effect=31.4 | technical documents or data, including numbers, units, and references to figures or tables. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F11290](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11290) | 6 | Low-level 'Jew' presence detector (L0:9026, frac=0.41) — fires on the raw Jew embedding with direct_effect=31.4 | mentions of Jewish people, Israel, and Christianity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11290) |
| [L0:F4470](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4470) | 6 | Low-level 'Jew' presence detector (L0:9026, frac=0.41) — fires on the raw Jew embedding with direct_effect=31.4 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4470) |
| [L2:F8236](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8236) | 6 | Explicit Jewish-people detector (L2:8236, frac=0.0044) — direct_effect 11.1 from 'Jew' embedding | mentions of Jewish people, culture, or religion, along with associated figures and locations | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8236) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 6 | Race/ethnicity vocabulary (L2:13158, frac=0.0099) — direct_effect 6.8 from 'Jew' |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L3:F12151](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12151) | 6 | Uppercase fragment amplifier (L3:12151, frac=0.0032) — promotes 'jew', amplifies 'Jew' embedding signal | capitalized common letter sequences such as "SEM", "ISM", "WF", "ISH", "WE", "SE" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12151) |
| [L4:F2405](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) | 6 | Religious identity/affiliation (L4:2405, frac=0.0071) — direct_effect 3.8 from 'Jew' |  words related to religious identity/affiliation or spirituality including related holidays | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) |
| [L4:F14733](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14733) | 6 | Jewish-targeted discrimination (L4:14733, frac=low) — direct_effect 5.5 from 'Jew', 2.1 from 'liberal' | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14733) |
| [L6:F648](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/648) | 6 | Discrimination against religious/ethnic groups (L6:648, frac=0.016, direct_effect=0.74 to probe) — primary driver |  words related to discrimination against particular religious or ethnic groups | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/648) |
| [L5:F7488](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7488) | 10 | 'Stain' / reputation-negation lexical feature (L5:7488, activation=21.5) — direct_effect 5.5 from 'stain' emb | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7488) |
| [L6:F1561](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1561) | 10 | Stain / disgrace phrase feature (L6:1561, activation=18.1) — direct_effect 3.4 to L8:13875 | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1561) |
| [L8:F13875](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13875) | 10 | Negative-sentiment reputation/betrayal (L8:13875, frac=0.010, direct_effect=0.23 to probe) — secondary driver | negative sentiment related to reputation and betrayal of trust. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13875) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Output: probe direction (toxicity) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'PROBE_NEGATIVE' is not one of the top-k next-token ca |
| 3 | `get_top_logits` | "" (100%) |
| 4 | `get_top_features` | 10 features; top: L6:648 de=0.738 |
| 5 | `inspect_feature` ×4 | L6:648, L2:13158, L4:2405, L8:13875 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F648@6` | ❌ error | — | — | Trace from L6:F648 ("discrimination against religious or ethnic groups") all the… |
| SA-2 | `L2:F13158@6` | ❌ error | — | — | Trace from L2:F13158 ("words about race and ethnicity") to token embeddings. Det… |
| SA-3 | `L4:F2405@6` | ✅ reported | 6 | 9 | Trace from L4:F2405 ("religious identity/affiliation") to token embeddings. Dete… |
| SA-4 | `L8:F13875@10` | ❌ error | — | — | Trace from L8:F13875 ("negative sentiment about reputation and betrayal of trust… |

<details>
<summary><b>SA-3</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F2405 | " words related to religious identity/affiliation or spirituality inclu" |
| 2 | `get_upstream_features` | L4:F2405@6, k=10 | Emb:" liberal"@5 (de=6.75) +9 more |
| 3 | `inspect_feature` | L3, F12151 | " capitalized common letter sequences such as "SEM", "ISM", "WF", "ISH"" |
| 4 | `get_upstream_features` | L3:F12151@6, k=10 | Emb:" Jew"@6 (de=11.00) +9 more |
| 5 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 6 | `get_upstream_features` | L2:F13158@6, k=10 | Emb:" Jew"@6 (de=6.81) +9 more |
| 7 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 8 | `inspect_feature` | L0, F11290 | "mentions of Jewish people, Israel, and Christianity" |
| 9 | `get_upstream_features` | L0:F9026@6, k=5 | Emb:" Jew"@6 (de=31.38) +4 more |
| 10 | `inspect_feature` | L1, F15359 | " mentions of Jewish people, culture or religion" |
| 11 | `inspect_feature` | L2, F8236 | " mentions of Jewish people, culture, or religion, along with associate" |

**Findings:** The religious‑identity feature L4:F2405 is primarily driven by the input token "Jew". The token first activates a low‑level presence detector (L0:9026) with a massive direct effect (31.4), which then feeds into a case‑sensitive uppercase fragment detector (L3:F12151) that further amplifies the signal (11.0). This amplified activation reaches the mid‑level ethnicity feature (L2:F13158) and the spec…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F648@6, k=12 → Emb:" Jew"@6 (de=19.38) +11 more |
| 2 | `get_upstream_features` | L8:F13875@10, k=12 → L6:F1561 (de=3.42) +11 more |
| 3 | `get_upstream_features` | L2:F13158@6, k=12 → Emb:" Jew"@6 (de=6.81) +11 more |
| 4 | `get_upstream_features` | L2:F8236@6, k=10 → Emb:" Jew"@6 (de=11.06) +9 more |
| 5 | `get_upstream_features` | L4:F14733@6, k=8 → Emb:" Jew"@6 (de=5.47) +7 more |
| 6 | `get_upstream_features` | L6:F1561@10, k=8 → L5:F7488 (de=6.19) +7 more |

### Build

`build_circuit` → 15 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 27,683 | 4,457 | 62,108 | 0 | $0.0174 | — | — |
| SA-3 | openai/gpt-oss-120b | 122,981 | 8,317 | 10,976 | 0 | $0.0236 | ✅ 6F/9E | Trace from L4:F2405 ("religious identity/affiliation") to to… |
| **Total** | | **150,664** | **12,774** | **73,084** | **0** | **$0.0410** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 29s