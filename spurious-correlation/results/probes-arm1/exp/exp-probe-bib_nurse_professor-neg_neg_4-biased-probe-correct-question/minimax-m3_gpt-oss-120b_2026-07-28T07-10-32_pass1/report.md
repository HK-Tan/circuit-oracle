# Circuit Oracle Report
**Date:** 2026-07-28 07:10:32 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by raw gendered-pronoun tokens ("He", "His", "his") and generic function-word detectors ("of", "is") — with no profession-, research-, or academic-content features present in the top circuit.

**Confidence:** 9

**Reasoning:**

**The user's concern is strongly confirmed.** The attribution graph contains *zero* profession-, CS-, or research-related features in its top 15 contributors. Instead, every dominant feature is either a male-pronoun detector or a generic function-word detector:

**Excitatory features (push toward the probe's classification):**
- **L0:F2994 (×2 occurrences, direct_effect +0.254, +0.154)** — the single most impactful feature — is literally a "possessive pronoun 'his' / 'he'" detector (frac_nonzero 0.073, top activating tokens all "his"). It is driven *purely* by the raw embedding of the token "his" (direct_effect +45.25 at pos 37, +45.0 at pos 55 — in "He received his Ph.D." and "his M.S.").
- **L0:F2848** — generic word "of" detector (pos 5, "Director of Mobile Grid..."). It is a content-free function-word feature, not a profession indicator.
- **L0:F11024** — labeled "word 'clock'" but activated by the token "Director" (direct_effect +12.81 from the Director embedding) — a generic, non-semantic word detector.
- **L0:F8658** — generic word "is" detector at "He is also Director" (direct_effect +8.0 from the "He" embedding, +6.28 from "is").
- **L7:F14893** — "pronouns or possessive pronouns" detector (positive +0.132 at pos 13 "His research interests...").

**Inhibitory features (all push the probe AWAY from its classification — they are anti-gender-marker signals):**
- L6:F12990 — "male pronouns and titles" detector (direct_effect −0.166)
- L4:F4315 — "his" pronoun mention (direct_effect −0.109)
- L7:F14946 — "his" possessive detector (direct_effect −0.125)
- L12:F2175 — "words referring to gender" (direct_effect −0.108)
- L18:F14743 — "He" pronoun feature (direct_effect −0.141)

**Signal flow:** The input tokens "He" (pos 1), "His" (pos 13), "He" (pos 35), and "his" (pos 37, 55) feed embeddings directly into L0 pronoun detectors, which sit *at the embedding layer* and have no intermediate profession-recognition features. The mid/high-layer features (L6, L7, L12, L18) are all *negative* — they are abstract gender detectors that *suppress* the probe score. The net effect is that the probe is being driven by low-level surface-form gender markers rather than by any deep semantic understanding of the person's profession (computer science, grid computing, Ph.D.).

**Critical absence:** There are no features in the top 15 whose label concerns research, academia, computer science, engineering, director, professor, or any profession. The probe appears to be latching onto "He received his Ph.D." style surface patterns — essentially counting male pronouns. This is a textbook **spurious-correlation / gender-bias** failure mode: if the same paragraph were rewritten with "She received her Ph.D.", the same circuit would presumably fire negatively (or fail to fire) even though the profession is identical. The user is correct that the circuit uses gender markers, not profession indicators.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe output (target direction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 37 | L0:F2994 — possessive pronoun "his" detector (pos 37) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 55 | L0:F2994 — possessive pronoun "his" detector (pos 55) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 5 | L0:F2848 — generic word "of" (pos 5) | the word "of" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F11024](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11024) | 4 | L0:F11024 — generic word "clock" (pos 4) |  the word "clock", especially in a technical context | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11024) |
| [L0:F8658](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8658) | 2 | L0:F8658 — generic word "is" (pos 2) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8658) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 13 | L7:F14893 — pronouns/possessives detector (pos 13) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | L7:F14893 — pronouns/possessives detector (pos 13) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 13 | L6:F12990 — male pronouns/titles (inhibitory) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 35 | L6:F12990 — male pronouns/titles (inhibitory) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 2 | L6:F12990 — male pronouns/titles (inhibitory) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 35 | L18:F14743 — "He" pronoun feature (inhibitory) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 2 | L7:F14946 — "his" possessive detector (inhibitory) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | L7:F14946 — "his" possessive detector (inhibitory) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 13 | L4:F4315 — "his" pronoun mention (inhibitory at pos 13) |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L12:F2175](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) | 2 | L12:F2175 — gender-word detector (inhibitory) |  words referring to gender | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 37 | Emb: his (pos 37) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 55 | Emb: his (pos 55) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: of (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: Director (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: He (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: is (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: His (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 35 | Emb: He (pos 35) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2994 de=0.254 |
| 3 | `inspect_feature` ×10 | L0:2994, L0:2848, L0:11024, L0:8658, L7:14893, L6:12990, L18:14743, L7:14946, L4:4315, L12:2175 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F2994@37` | ❌ error | — | — | Trace L0:F2994 (pronoun "his" feature) upstream to confirm its origin at the emb… |
| SA-2 | `L6:F12990@13` | ✅ reported | 3 | 5 | Trace L6:F12990 (male pronouns/titles) upstream. This is a mid-layer gender feat… |
| SA-3 | `L18:F14743@35` | ✅ reported | 8 | 12 | Trace L18:F14743 ("He" pronoun feature) upstream. This is a high-layer feature w… |
| SA-4 | `L12:F2175@2` | ✅ reported | 8 | 12 | Trace L12:F2175 (gender words) upstream. Does this gender feature connect to any… |
| SA-5 | `L7:F14893@13` | ✅ reported | 3 | 6 | Trace L7:F14893 (pronouns or possessive pronouns) upstream. Check whether this h… |

<details>
<summary><b>SA-2</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 2 | `get_upstream_features` | L6:F12990@13, k=10 | Emb:" His"@13 (de=5.28) +9 more |
| 3 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 4 | `get_upstream_features` | L4:F4315@13, k=10 | Emb:" His"@13 (de=21.25) +9 more |
| 5 | `inspect_feature` | L0, F2749 | " references to ownership or association with a person or group of peop" |
| 6 | `get_upstream_features` | L0:F2749@13, k=10 | Emb:" His"@13 (de=23.75) +9 more |
| 7 | `inspect_feature` | L5, F14955 | " text about people's free time that mentions both family and hobbies" |
| 8 | `get_upstream_features` | L5:F14955@13, k=10 | Emb:" His"@13 (de=4.47) +9 more |
| 9 | `inspect_feature` | L4, F15438 | " mentions and declarations of conflicts of interest, study design, and" |
| 10 | `get_upstream_features` | L4:F15438@13, k=10 | Emb:" His"@13 (de=3.67) +9 more |

**Findings:** The male‑pronoun feature L6:F12990 is driven primarily by the raw token embedding "His" (direct effect 5.28) and by upstream mid‑layer feature L4:F4315 (direct effect 1.29). L4:F4315 itself receives a strong excitatory input from the same "His" embedding (21.25). A later contextual feature L5:F14955 also contributes (0.77) and is positively excited by the "His" embedding (4.47). All pathways inclu…

</details>

<details>
<summary><b>SA-3</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@35, k=15 | Emb:" He"@35 (de=23.62) +14 more |
| 3 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 4 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 5 | `get_upstream_features` | L0:F1069@35, k=10 | Emb:" He"@35 (de=36.50) +9 more |
| 6 | `get_upstream_features` | L0:F1069@35, k=10 | Emb:" He"@35 (de=36.50) +9 more |
| 7 | `inspect_feature` | L13, F6622 | " pronouns." |
| 8 | `inspect_feature` | L6, F2267 | "words that appear in programming code, legal jargon, or scientific tex" |
| 9 | `get_upstream_features` | L17:F5889@35, k=10 | Emb:" He"@35 (de=22.62) +9 more |
| 10 | `inspect_feature` | L17, F3683 | "biographies" |
| 11 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 12 | `get_upstream_features` | L6:F2267@35, k=10 | Emb:"<bos>"@0 (de=-9.31) +9 more |
| 13 | `inspect_feature` | L11, F8266 | " mentions of people with professional titles or descriptions, especial" |

**Findings:** The high‑layer pronoun feature L18:F14743 receives its strongest positive drive from the raw token embedding for " He" (23.6) and from the low‑layer male‑pronoun detector L0:F1069 (7.5). Tracing upstream from L0:F1069 reaches the same raw embedding (36.5), which satisfies the required lower‑third‑layer (layer 0 ≤ 8) and embedding‑positive‑effect condition. Mid‑layer pronoun/context features add mo…

</details>

<details>
<summary><b>SA-4</b> — tool trace (20 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F2175 | " words referring to gender" |
| 2 | `get_upstream_features` | L12:F2175@2, k=10 | L7:F14946 (de=5.41) +9 more |
| 3 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 4 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 5 | `inspect_feature` | L4, F993 | "contractions of the verb to be in the third person singular" |
| 6 | `get_upstream_features` | L7:F14946@2, k=10 | Emb:"He"@1 (de=9.00) +9 more |
| 7 | `inspect_feature` | L5, F645 | " verbs in past tense" |
| 8 | `get_upstream_features` | L6:F12990@2, k=10 | L5:F645 (de=1.95) +9 more |
| 9 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |
| 10 | `inspect_feature` | L10, F6109 | " references to males or male-related terms" |
| 11 | `get_upstream_features` | L6:F12990@2, k=10 | L5:F645 (de=1.95) +9 more |
| 12 | `get_upstream_features` | L5:F645@2, k=10 | Emb:"He"@1 (de=3.98) +9 more |
| 13 | `get_upstream_features` | L10:F6109@2, k=10 | L7:F14946 (de=8.38) +9 more |
| 14 | `get_upstream_features` | L4:F993@2, k=10 | Emb:"He"@1 (de=7.72) +9 more |
| 15 | `inspect_feature` | L6, F10944 | " text in languages other than English" |
| 16 | `inspect_feature` | L9, F12373 | " words or names referring to relationships, particularly marriage or f" |
| 17 | `inspect_feature` | L6, F3426 | "sentences that refer to people" |
| 18 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 19 | `inspect_feature` | L3, F5393 | "two- or three-letter sequences" |
| 20 | `get_upstream_features` | L4:F15567@2, k=10 | Emb:"He"@1 (de=11.38) +9 more |

**Findings:** The gender token L12:F2175 is driven primarily by lower‑layer male pronoun detectors (L7:F14946, L6:F12990, L0:F1069) and a generic past‑tense verb feature. No profession‑related features (e.g., doctor, engineer) appear in the positive upstream chain, and the trace reaches layer ≤8 (features at layers 0,4,5,6,7). Therefore, L12:F2175 does not connect to any profession‑related features.

</details>

<details>
<summary><b>SA-5</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@13, k=10 | Emb:" His"@13 (de=22.75) +9 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `get_upstream_features` | L6:F12990@13, k=10 | Emb:" His"@13 (de=5.28) +9 more |
| 5 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 6 | `inspect_feature` | L5, F14955 | " text about people's free time that mentions both family and hobbies" |
| 7 | `get_upstream_features` | L4:F4315@13, k=10 | Emb:" His"@13 (de=21.25) +9 more |

**Findings:** Tracing from L7:F14893 (pronoun detector) shows that its strongest upstream influence is the raw token embedding for the word "His" (positive direct_effect 22.75). The signal then passes through a cascade of gender‑specific pronoun features: L6:F12990 (male‑pronoun detector) and L4:F4315 ("his" mention detector). All upstream connections are positive and the path reaches the embedding layer (layer…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L7:F14893@13, k=15 → Emb:" His"@13 (de=22.75) +14 more |
| 2 | `get_upstream_features` | L0:F2994@37, k=15 → Emb:" his"@37 (de=45.25) +14 more |
| 3 | `get_upstream_features` | L0:F11024@4, k=10 → Emb:" Director"@4 (de=12.81) +9 more |
| 4 | `get_upstream_features` | L0:F8658@2, k=10 → Emb:"He"@1 (de=8.00) +9 more |
| 5 | `get_upstream_features` | L0:F2848@5, k=10 → Emb:" of"@5 (de=34.75) +9 more |
| 6 | `get_upstream_features` | L0:F2994@55, k=10 → Emb:" his"@55 (de=45.00) +9 more |
| 7 | `inspect_feature` | L0, F1069 → " references to a male person, particularly when using the pronoun "He"" |

### Build

`build_circuit` → 20 nodes, 21 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 59,468 | 7,549 | 170,601 | 0 | $0.0371 | — | — |
| SA-2 | openai/gpt-oss-120b | 89,234 | 7,857 | 36,864 | 0 | $0.0187 | ✅ 3F/5E | Trace L6:F12990 (male pronouns/titles) upstream. This is a m… |
| SA-4 | openai/gpt-oss-120b | 407,615 | 10,659 | 27,840 | 0 | $0.0680 | ✅ 8F/12E | Trace L12:F2175 (gender words) upstream. Does this gender fe… |
| SA-3 | openai/gpt-oss-120b | 248,205 | 22,780 | 15,296 | 0 | $0.0511 | ✅ 8F/12E | Trace L18:F14743 ("He" pronoun feature) upstream. This is a … |
| SA-5 | openai/gpt-oss-120b | 62,407 | 4,166 | 5,280 | 0 | $0.0119 | ✅ 3F/6E | Trace L7:F14893 (pronouns or possessive pronouns) upstream. … |
| **Total** | | **866,929** | **53,011** | **255,881** | **0** | **$0.1868** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 11m 39s