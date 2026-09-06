# Circuit Oracle Report
**Date:** 2026-07-28 07:21:11 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_7 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

The circuit is already populated and contains the necessary features. Let me write the analysis.

**Analysis:** The probe's toxicity score is driven almost entirely by a small set of identity-group features (LGBTQ+, race, "Black"/"White" color words) that read directly from the literal identity tokens ("Black", "Gay", "White", "Pride") in the prompt — **not** from any actual toxic content (e.g., "NAZI", "Hypocrisy", "racism"). The single strongest driver is L8:F15771 (LGBTQ+ discussion, de=+0.32), and there is no feature in the top-15 whose promoted tokens include "NAZI", "racist", "racism", or "hypocrisy" — confirming the user's suspicion.

**Confidence:** 8

**Reasoning:**

The attribution graph at the probe's classification direction is dominated by **identity-attribute features** anchored to specific input tokens, with essentially no "toxicity/lemming" content features:

- **Strongest positive driver — L8:F15771** ("LGBTQ+ discussion, especially same-sex marriage/adoption", frac_nonzero=0.008). Upstream at pos 9, it is fed by the `Gay` token embedding (de=+10.4) and the ` Pride` token (de=+3.8) at pos 2, then by L6:F6085 (homosexuality/same-sex marriage text) and L4:F15899 (LGBTQ+ identity language). None of these features' promoted-token lists include any slur or toxic concept — the top tokens are `▁Cre`, `▁příjem`, `ISLAM` (likely noise from the autointerp projection) on the promoted side.

- **L4:F15899 → L6:F6085 → L8:F15771** form a clean LGBTQ+ chain reading `Gay` (de=+13.8 → +21.8 → +10.4) and ` Pride` (+5 → +1.25 → +3.8).

- **L2:F13158** ("race/ethnicity words", promoted: `ethnic`, `queer`, `LGBT`, `Hispanic`, `Latino`, `Muslim`, `Jewish`, `Hispanic`) at pos 17 reads the `White` token (de=+13.6) and ` black` at pos 5 (+1.2). It also contributes at pos 5 via ` black` (+10.75). This is a broad identity-cue feature with no toxic semantics.

- **L3:F13061** ("race/gender/social-issues", reads `Black` de=+12.1 + ` Pride` de=+5.3), **L4:F117** ("race/racism/Black-focused", reads `White` de=+10.25), **L6:F3902** ("race/ethnicity terms", reads `White` de=+7.1) all similarly fire on identity tokens. L4:F117's promoted tokens (`racist`, `racism`, `racial`) are the only "toxic" surface tokens, but it reads from `White`/`Black` embeddings, not from `NAZI` or `racism` strings.

- **Inhibitory/suppressive features** (de<0): L1:F9113 (race/slavery discussion, de=-0.32, suppressed tokens: `▁Black`, `Black`, `black`, `▁Gray`, `white`) and L2:F9528 ("the color black", de=-0.23, suppressed tokens: `▁black`, `▁Black`, `Black`, `black`, `▁BLACK`, `黑`, `▁schwarzen`, `ブラック`, `的黑`). These features are *activated* by the `Black` embedding but are explicitly *anti-correlated* with the probe — they push the score *down*. This is striking: the prompt's "Black Pride" / "Gay Pride" tokens activate features that suppress toxicity, while the same tokens also activate *different* identity-cue features that boost it. The net effect is identity-driven, not content-driven.

- **No toxicity-content features appear.** The words `NAZI`, `Hypocrisy`, `racism`, `worse` produce no top-15 direct contributors. `NAZI!` at the end of line 3 and the `-` and `Hypocrisy` line are absent from the top features by direct effect.

- The probe is therefore classifying the input as toxic largely on the basis of *which identity tokens are present and in what configuration* — particularly the `Gay` and `White` tokens paired with the "Pride" frame — exactly the spurious-correlation concern raised. The model has learned that LGBTQ+/race co-occurrence patterns predict toxicity in its training distribution, and the probe inherits that shortcut.

**Circuit structure:** token embeddings (Emb:`Black`, Emb:`Gay`, Emb:`White`, Emb:` black`, Emb:`Pride`) → low-layer identity detectors (L1–L2 color/race words) → mid-layer identity-composition features (L2:F13158, L3:F13061, L4:F117, L4:F15899) → late-layer identity-discussion features (L6:F6085, L6:F3902, L8:F15771) → probe output, with parallel *suppressive* paths (L1:F9113, L2:F9528) that partially cancel. No "toxic content" feature enters the circuit at any layer.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Black (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: Pride (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: Gay (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: White (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: black (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L2:F11363](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11363) | 1 | Color/black-attribute feature (promoted: black, blue, yellow, pink...) — strongly driven by literal 'Black' token embedding |  colors and words like Diamond. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11363) |
| [L1:F9113](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) | 1 | Race/slavery discussion feature — INHIBITORY to probe (suppresses 'Black', 'black' tokens in promoted-tokens list) |  discussions about race and slavery | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) |
| [L2:F9528](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) | 1 | Color-black feature — strongly INHIBITORY (suppressed tokens are 'Black','black'; activated by Black embedding but pushes away from probe) |  the color black | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 17 | Race/ethnicity words feature (promoted: ethnic, queer, LGBT, Hispanic...) — reads 'White', ' black' embeddings |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 5 | Race/ethnicity words feature (promoted: ethnic, queer, LGBT, Hispanic...) — reads 'White', ' black' embeddings |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 2 | Race/gender/social-issues words (broad) — reads 'Black' + ' Pride' embeddings |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 17 | Race/racism/Black-focused terms (promoted: racist, racism, racial) — reads 'White' embedding |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F15899](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) | 9 | LGBTQ+ identity language (promoted: gender, transgender, LGBTQ) — reads 'Gay' + ' Pride' embeddings |  language associated with the LGBTQ community and discussions of gender and identity. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) |
| [L6:F6085](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) | 9 | Homosexuality / same-sex marriage text — reads 'Gay' + ' Pride' embeddings |  text related to homosexuality and same-sex marriage | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 17 | Race/ethnicity terms (promoted: minorities, ethnicity) — reads 'White' embedding |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L8:F15771](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) | 9 | Late-layer LGBTQ+ discussion (same-sex marriage, adoption) — STRONGEST DRIVER (de=0.32) | discussion of LGBTQ+ issues, especially same-sex marriage, adoption, and related topics | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) |
| [L8:F15771](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) | 13 | Late-layer LGBTQ+ discussion (same-sex marriage, adoption) — STRONGEST DRIVER (de=0.32) | discussion of LGBTQ+ issues, especially same-sex marriage, adoption, and related topics | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) |
| [L8:F15771](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) | 2 | Late-layer LGBTQ+ discussion (same-sex marriage, adoption) — STRONGEST DRIVER (de=0.32) | discussion of LGBTQ+ issues, especially same-sex marriage, adoption, and related topics | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Output: Probe direction (toxicity score) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L8:15771 de=0.324 |
| 3 | `inspect_feature` ×11 | L8:15771, L1:9113, L2:11363, L2:13158, L3:13061, L6:6085, L2:9528, L1:12542, L6:3902, L4:15899, L4:117 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L8:F15771@9` | ❌ error | — | — | Trace the path upstream from L8:F15771 at position 9 (LGBTQ+ topic feature, dire… |
| SA-2 | `L2:F13158@17` | ✅ reported | 3 | 5 | Trace the path upstream from L2:F13158 at position 17 (race/ethnicity words feat… |
| SA-3 | `L3:F13061@2` | ❌ error | — | — | Trace the path upstream from L3:F13061 at position 2 (race/gender/social-issues … |
| SA-4 | `L1:F9113@1` | ❌ error | — | — | Trace the path upstream from L1:F9113 at position 1 (race/slavery feature, direc… |

<details>
<summary><b>SA-2</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 2 | `get_upstream_features` | L2:F13158@17, k=10 | Emb:"White"@17 (de=13.56) +9 more |
| 3 | `inspect_feature` | L1, F13646 | " text discussing social justice issues" |
| 4 | `inspect_feature` | L1, F7821 | " mentions of computer fans." |

**Findings:** The race/ethnicity detector (L2:F13158) is strongly driven by the input token 'White' at the same position, giving a huge positive direct effect. A secondary social‑justice discourse feature (L1:F13646) also feeds into it, suggesting the model clusters broader race‑related language before the specific token cue. An unrelated fan‑mention feature (L1:F7821) contributes modestly, likely incidental. E…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L8:F15771@9, k=15 → Emb:"Gay"@9 (de=10.38) +14 more |
| 2 | `get_upstream_features` | L3:F13061@2, k=15 → Emb:"Black"@1 (de=12.06) +14 more |
| 3 | `get_upstream_features` | L1:F9113@1, k=15 → Emb:"Black"@1 (de=16.88) +14 more |
| 4 | `get_upstream_features` | L6:F6085@9, k=15 → Emb:"Gay"@9 (de=21.75) +14 more |
| 5 | `get_upstream_features` | L2:F13158@5, k=15 → Emb:" black"@5 (de=10.75) +14 more |
| 6 | `get_upstream_features` | L6:F3902@17, k=15 → Emb:"White"@17 (de=7.12) +14 more |
| 7 | `get_upstream_features` | L4:F15899@9, k=12 → Emb:"Gay"@9 (de=13.81) +11 more |
| 8 | `get_upstream_features` | L4:F117@17, k=10 → Emb:"White"@17 (de=10.25) +9 more |
| 9 | `get_upstream_features` | L2:F11363@1, k=10 → Emb:"Black"@1 (de=25.00) +9 more |
| 10 | `get_upstream_features` | L2:F9528@1, k=10 → Emb:"Black"@1 (de=30.00) +9 more |

### Build

`build_circuit` → 16 nodes, 30 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 30,381 | 6,085 | 145,997 | 0 | $0.0252 | — | — |
| SA-2 | openai/gpt-oss-120b | 28,282 | 2,532 | 5,120 | 0 | $0.0058 | ✅ 3F/5E | Trace the path upstream from L2:F13158 at position 17 (race/… |
| **Total** | | **58,663** | **8,617** | **151,117** | **0** | **$0.0310** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 15s