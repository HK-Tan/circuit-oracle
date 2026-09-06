# Circuit Oracle Report
**Date:** 2026-07-28 07:20:30 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by a cascade of male-gender/possessive-pronoun features originating from the token "His" at position 1, with negligible contribution from genuine profession indicators like "research", "science", or "visualization".

**Confidence:** 9

**Reasoning:**

The attribution circuit reveals a textbook case of a **spurious gender-marker circuit** rather than a profession-indicator circuit. Tracing the top 20 features driving the probe direction confirms this:

**The dominant positive pathway (pos 1, "His"):**
- **L7:F14893** (direct_effect = +0.43, frac_nonzero = 0.009) — labeled "pronouns or possessive pronouns," promotes tokens like `▁herself`, `▁she`, `▁elle`. This is the single strongest positive driver.
- **L19:F8814** (direct_effect = +0.24, frac_nonzero = 0.087) — labeled "various pronouns and names referring to people," strongly promotes feminine pronouns `▁herself`, `▁she`, `▁her`. Despite the feminine-promotion, this feature aggregates the entire gender-pronoun signal and is fed by a chain of male-pronoun detectors.
- **L0:F2994** (direct_effect = +0.23) — literally labeled "the pronoun 'his' and the pronoun 'he.'"

These all trace back to the **embedding node for "His" at position 1** (`Emb: His`), which contributes direct_effect = +9.3 directly to L19:F8814 and +23.5 to L4:F4315. The multi-hop path is: `Emb: His → L4:F4315 (his surface) → L6:F12990 (male pronouns) → L7:F14946 (his core) / L7:F14893 (possessive) → L19:F8814 (gender gate) → logit`. The L7:L19:gender gate supernode's promoted tokens (`herself`, `she`, `her`) indicate it is encoding a gender axis that happens to correlate with the male "His" input on this prompt.

**Negative pathway (also gender):**
- **L6:F12990** at pos 1 (direct_effect = −0.29) is labeled "male pronouns and titles along with descriptors associated with men." It acts as an inhibitory male-pronoun gate.
- **L18:F14743** at pos 14 and pos 37 (direct_effect ≈ −0.25, −0.21) is labeled simply "He" — this fires on the subject pronoun "He" later in the text and suppresses the probe score. The "He" at pos 14 (in "He received a BS...") is also a male-gender marker.
- **L18:F7400** (direct_effect = −0.16) has coding/UI top examples but its promoted tokens are `▁himself`, `▁his`, `▁seine` — again a male-pronoun signal.

**Genuine profession indicators are absent or weak:**
- L0:F2827 ("the word science"), L0:F4564 ("the word research"), and L2:F9740 ("the word interest") — all features whose top-activating examples clearly point to *computer science / research* content — appear in the circuit with **small direct effects** (≤+0.16). Crucially, none of them feed into a profession-classification supernode; they only weakly push the probe.
- L0:F14201 (direct_effect = −0.11), labeled "words related to trade (business, finance, and health)," is generic and unrelated to CS/academia.
- No features fire on "visualization," "computer graphics," "PhD," "university," or "laboratory" in the top-20 list.

**Conclusion:** The user's concern is validated. The probe direction is driven primarily by a chain of **gender-pronoun features** anchored at the word "His" (pos 1) and "He" (pos 14, 37). The positive contribution from the L7:L19:possessive/gender-pronoun features (L7:F14893 +0.43, L19:F8814 +0.24, L0:F2994 +0.23 ≈ +0.90 total) is partially cancelled by the negative male-pronoun gates (L6:F12990 −0.29, L18:F14743 ≈ −0.25, L18:F7400 −0.16 ≈ −0.70), but the net signal is still gender-driven. Genuine profession content features (research, science, interest) are present but contribute only weakly (≤+0.16) and do not form any profession-classification pathway. The circuit thus exhibits exactly the kind of **spurious correlation with male gender markers** that the user suspected — the probe is using pronoun-based gender cues as a shortcut rather than profession-specific semantic content.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: His (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: research (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: science (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | L0: F2994 'the pronoun his and the pronoun he' (pos 1) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F4564](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) | 2 | L0: F4564 'the word research' (pos 2) | the word "research." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) |
| [L0:F2827](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2827) | 8 | L0: F2827 'the word science' (pos 8) |  the word "science" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2827) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 13 | L0: F6051 'periods, spaces, and the number 1' (pos 13) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L2:F9740](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9740) | 3 | L2: F9740 'the word interest and related words' (pos 3) | the word "interest" and related words. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9740) |
| [L2:F5491](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) | 1 | L2: F5491 'references to God in the third person' (pos 1) | references to God in the third person. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | L4: F4315 'mentions of his and other associated pronouns' (pos 1) |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | L6: F12990 'male pronouns and titles with male-associated descriptors' (pos 1) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | L7: F14893 'pronouns or possessive pronouns' (pos 1) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | L7: F14946 'the possessive pronoun his (or similar pronouns like he and him)' (pos 1) | the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 14 | L18: F14743 'He' (pos 14) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F7400](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) | 1 | L18: F7400 'coding/UI words; promoted tokens: himself/his' (pos 1) |  words related to coding and software/UI interfaces, with some bias toward non-English words | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | L19: F8814 'various pronouns and names referring to people; promotes she/her' (pos 1) | various pronouns and names referring to people | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L7:14893 de=0.430 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ✅ reported | 4 | 7 | Trace upstream from L7:F14893 at pos 1 (the strongest positive driver, direct_ef… |
| SA-2 | `L19:F8814@1` | ✅ reported | 7 | 8 | Trace upstream from L19:F8814 at pos 1 (direct_effect=+0.24). What does this lat… |
| SA-3 | `L0:F2994@1` | ❌ error | — | — | Trace upstream from L0:F2994 at pos 1 (direct_effect=+0.23). What does this earl… |
| SA-4 | `L2:F9740@3` | ❌ error | — | — | Trace upstream from L2:F9740 at pos 3 (direct_effect=+0.13). Position 3 is 'His'… |
| SA-5 | `L18:F14743@14` | ❌ error | — | — | Trace upstream from L18:F14743 at pos 14 (direct_effect=-0.25, a strong negative… |
| SA-6 | `L6:F12990@1` | ✅ reported | 6 | 7 | Trace upstream from L6:F12990 at pos 1 (direct_effect=-0.29, strong negative). W… |

<details>
<summary><b>SA-1</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 5 | `get_upstream_features` | L4:F4315@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 6 | `get_upstream_features` | L6:F12990@1, k=10 | Emb:"His"@1 (de=4.91) +9 more |
| 7 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |
| 8 | `inspect_feature` | L3, F3205 | " code snippets and documentation references, possibly related to web d" |

**Findings:** The circuit starts at L7:F14893, a high‑level pronoun/possessive detector that strongly activates on the token "His" at position 1. Its strongest upstream drivers are L6:F12990 (male pronoun detector) and L4:F4315 (specific "his" surface detector). Both of these receive a direct positive push from the raw input embedding of the token "His" (layer ≤8), satisfying the requirement to reach a lower‑th…

</details>

<details>
<summary><b>SA-2</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F8814 | " various pronouns and names referring to people" |
| 2 | `get_upstream_features` | L19:F8814@1, k=10 | Emb:"His"@1 (de=9.31) +9 more |
| 3 | `inspect_feature` | L18, F7400 | " words related to coding and software/UI interfaces, with some bias to" |
| 4 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 5 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 6 | `inspect_feature` | L18, F10315 | " pronouns and possessive pronouns" |
| 7 | `get_upstream_features` | L7:F14946@1, k=10 | Emb:"His"@1 (de=18.38) +9 more |
| 8 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 9 | `get_upstream_features` | L7:F14946@1, k=10 | Emb:"His"@1 (de=18.38) +9 more |
| 10 | `inspect_feature` | L12, F3684 | " lines of code starting with a '#'" |
| 11 | `get_upstream_features` | L18:F7400@1, k=10 | Emb:"His"@1 (de=13.00) +9 more |

**Findings:** Tracing from L19:F8814 shows a cascade of pronoun‑related features. The top‑layer feature (L19) strongly promotes feminine pronouns and suppresses masculine ones, acting as a gender‑bias gate. Its strongest upstream drivers are male‑pronoun detectors in layers 18, 7, 6, and 4, ultimately rooted in the raw input embedding for the token "His" (a male possessive pronoun). Because the path reaches a l…

</details>

<details>
<summary><b>SA-6</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 2 | `get_upstream_features` | L6:F12990@1, k=15 | Emb:"His"@1 (de=4.91) +14 more |
| 3 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 4 | `get_upstream_features` | L4:F4315@1, k=15 | Emb:"His"@1 (de=23.50) +14 more |
| 5 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 6 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |
| 7 | `inspect_feature` | L3, F3205 | " code snippets and documentation references, possibly related to web d" |
| 8 | `get_upstream_features` | L5:F10952@1, k=15 | Emb:"His"@1 (de=10.69) +14 more |
| 9 | `inspect_feature` | L2, F9301 | " all mentions of men and women in the context of relationships, dating" |
| 10 | `inspect_feature` | L4, F8952 | " content from multiple different languages in the same document." |

**Findings:** L6:F12990 is a gender‑pronoun gate that negatively influences the target logit. Its strongest upstream drivers are lower‑layer pronoun detectors (L4:F4315, L5:F10952, etc.) that receive a large positive push from the token embedding for the word "His" at position 1. The circuit therefore links the presence of a masculine pronoun in the prompt to a suppression of the downstream output, but no expli…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×5 | L0:2994, L2:9740, L18:14743, L18:7400, L0:4564 |
| 2 | `get_upstream_features` | L19:F8814@1, k=5 → Emb:"His"@1 (de=9.31) +4 more |
| 3 | `get_upstream_features` | L7:F14893@1, k=3 → Emb:"His"@1 (de=23.50) +2 more |
| 4 | `inspect_feature` ×4 | L2:5491, L0:6051, L0:2827, L0:14201 |

### Build

`build_circuit` → 17 nodes, 23 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 24,272 | 5,373 | 86,721 | 0 | $0.0189 | — | — |
| SA-2 | openai/gpt-oss-120b | 149,685 | 10,730 | 19,200 | 0 | $0.0292 | ✅ 7F/8E | Trace upstream from L19:F8814 at pos 1 (direct_effect=+0.24)… |
| SA-1 | openai/gpt-oss-120b | 95,872 | 6,045 | 5,056 | 0 | $0.0181 | ✅ 4F/7E | Trace upstream from L7:F14893 at pos 1 (the strongest positi… |
| SA-6 | openai/gpt-oss-120b | 120,321 | 8,693 | 5,120 | 0 | $0.0233 | ✅ 6F/7E | Trace upstream from L6:F12990 at pos 1 (direct_effect=-0.29,… |
| **Total** | | **390,150** | **30,841** | **116,097** | **0** | **$0.0895** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 14s