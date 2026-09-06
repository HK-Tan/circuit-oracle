# Circuit Oracle Report
**Date:** 2026-07-28 07:23:34 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by a mix of the gendered possessive marker "his" (L0:F2994, the single largest direct effect of 0.2969, firing on every "his" token in the text), the male pronoun "He" (L7:F14893, direct effect 0.167), and weak generic academic-degree surface features ("University", "degree", "Mathematics" entity), with no feature that specifically encodes the actual profession (Computer Science / Assistant Professor).

**Confidence:** 7

**Reasoning:** The user's concern is largely confirmed by the circuit. The dominant positive driver of the probe score is **L0:F2994 ("Gender/Possessive Marker — ' his'")**, which fires at positions 3, 23, and 44 — every occurrence of "his" in the input — with massive direct effects of 0.30, 0.16, and 0.14 respectively. Upstream tracing shows this feature derives almost entirely from the raw " his" token embedding (direct_effect 42.5 from `Emb: his (pos 3)`), confirming it is a low-level gendered surface marker, not a profession indicator. The second-largest positive contributor is **L7:F14893 ("He / He received" pronoun feature)** at pos 1 (direct_effect 0.167), which also traces to the `Emb: He` token (direct_effect 14.75). Together, the pronoun/possessive pathway accounts for ~0.46 of the direct logit effect — by far the largest share of the probe's positive signal.

In contrast, the genuine content features are much weaker. The **Mathematics entity supernode** (L5:F10392 → L6:F170) encodes a subject-matter entity, not a profession, and contributes only modestly (L6:F170 direct_effect 0.12). The **degree/in/university** surface tokens (L0:F6270 "University" at 0.15, L0:F6127 " degree" at −0.11, L2:F10852 and L3:F4113 "in X degree" pattern) are generic academic-template features that would fire for any faculty biography regardless of discipline or rank. Notably, the text explicitly contains "Computer Science" and "Assistant Professor" at later positions, but **no feature in the top 20 encodes these profession-specific tokens** — the probe is being driven by the gendered framing of the bio rather than by the professional role.

This is a textbook spurious-correlation finding: a linear profession probe is reading out male-coded pronouns/possessives because academic biographies in its training distribution are heavily gendered (a known bias in biography corpora), not because it has learned to detect "professor" as a profession. If "his" tokens were swapped to "her" or "their" while keeping "Assistant Professor of Computer Science" intact, the probe score would likely flip despite the profession being identical.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 3 | Gender/Possessive Marker (' his') — L0:F2994 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 23 | Gender/Possessive Marker (' his') — L0:F2994 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 44 | Gender/Possessive Marker (' his') — L0:F2994 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Pronoun 'He' / 'He received' — L7:F14893 | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 2 | Pronoun 'He' / 'He received' — L7:F14893 | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 3 | Pronoun 'He' / 'He received' — L7:F14893 | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L0:F6270](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) | 13 | 'University' token — L0:F6270 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) |
| [L0:F6127](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6127) | 8 | ' degree' token — L0:F6127 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6127) |
| [L3:F4113](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4113) | 9 | 'in X degree' pattern — L3:F4113, L2:F10852 | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4113) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 9 | 'in X degree' pattern — L3:F4113, L2:F10852 | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 10 | Mathematics entity — L5:F10392, L6:F170 | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 10 | Mathematics entity — L5:F10392, L6:F170 | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2994 de=0.297 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F2994@3` | ❌ error | — | — | Trace L0:F2994 which fires on position 3 (likely 'He' token) with high direct_ef… |
| SA-2 | `L0:F6270@13` | ❌ error | — | — | Trace L0:F6270 at pos 13 ('Mathematics' or similar). Determine what this feature… |
| SA-3 | `L0:F1069@21` | ❌ error | — | — | Trace L0:F1069 at pos 21 (likely 'Utah' or 'State'). What does it encode? |
| SA-4 | `L6:F170@10` | ❌ error | — | — | Trace L6:F170 at pos 10 (likely 'Peking University'). What does it encode? |
| SA-5 | `L7:F14893@1` | ❌ error | — | — | Trace L7:F14893 at pos 1 with direct_effect 0.167. What does it encode — profess… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F2994@3, k=5 → Emb:" his"@3 (de=42.50) +4 more |
| 2 | `get_upstream_features` | L0:F6270@13, k=5 → Emb:" University"@13 (de=22.88) +4 more |
| 3 | `get_upstream_features` | L0:F1069@21, k=5 → Emb:" He"@21 (de=37.25) +4 more |
| 4 | `get_upstream_features` | L6:F170@10, k=5 → L5:F10392 (de=11.38) +4 more |
| 5 | `get_upstream_features` | L7:F14893@1, k=5 → Emb:"He"@1 (de=14.75) +4 more |
| 6 | `get_upstream_features` | L5:F10392@10, k=5 → L3:F4113 (de=3.34) +4 more |
| 7 | `get_upstream_features` | L3:F4113@9, k=5 → Emb:" in"@9 (de=11.94) +4 more |
| 8 | `get_upstream_features` | L0:F2994@44, k=5 → Emb:" his"@44 (de=45.50) +4 more |
| 9 | `get_upstream_features` | L0:F2994@23, k=5 → Emb:" his"@23 (de=45.25) +4 more |
| 10 | `get_upstream_features` | L7:F14893@3, k=5 → Emb:" his"@3 (de=26.00) +4 more |
| 11 | `get_upstream_features` | L2:F10852@9, k=5 → Emb:" in"@9 (de=12.62) +4 more |
| 12 | `get_upstream_features` | L0:F6127@8, k=5 → Emb:" degree"@8 (de=16.88) +4 more |

### Build

`build_circuit` → 14 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 14,847 | 3,750 | 38,792 | 0 | $0.0113 | — | — |
| **Total** | | **14,847** | **3,750** | **38,792** | **0** | **$0.0113** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 51s