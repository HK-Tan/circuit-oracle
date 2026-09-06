# Circuit Oracle Report
**Date:** 2026-07-28 07:01:38 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** This probe — apparently trained to detect a profession (likely "professor/academic") — drives its classification score from a mix of genuine academic-content signals (L5/L6 academic-field features) and **dominant spurious gender cues** (the repeated "He/his" pronoun chain at L0/L4/L6/L7/L18), with the male-pronoun pathway being the largest single source of positive drive toward the probe.

**Confidence:** 6

**Reasoning:**

The circuit is dominated by gender signals at multiple layers:

- **L0:F2994** ("his"/"he" pronoun feature) is the **single largest positive contributor** to the probe (direct_effect +0.297 at pos 3, +0.161 at pos 44, +0.144 at pos 23). Crucially, its `promoted_tokens` list *suppresses* "▁his" and "his" while promoting punctuation/whitespace — meaning it acts as a "non-pronoun context" gate. Its strongest upstream drive is the embedding of " his" (direct_effect 42.5), then secondary inputs from "He", "received", "<bos>". It fires wherever the subject pronoun is absent, a pattern that the probe apparently has learned to associate with the profession.
- **L7:F14946** ("his/him" male-pronoun) contributes strongly negatively (−0.171 at pos 2, −0.144 at pos 1) — its `promoted_tokens` confirm it actively promotes "▁his"/"himself" while suppressing "▁she"/"▁her". Its upstream path (via the subagent) goes: **Emb("He") → L6:F12990 (male pronouns/titles) → L7:F14946**, with further excitation from L4:F993 (third-person "be" contractions) and L4:F15567 (pronoun/possessive bridge).
- **L7:F14893** (generic pronoun detector) contributes positively (+0.167, +0.123) and is driven directly by the **Emb("He") at pos 1 (direct_effect 14.75)**, then by L6:F12990 and L4:F15567.
- **L6:F12990** ("male pronouns and titles") sits at the core of the male-pronoun pathway, with the subagent confirming it receives direct drive from L5:F645 (past-tense verbs, which co-occur with biographical "He received…" sentences) and propagates the male-gender signal upward.
- **L18:F14743** ("He" pronoun gate) contributes strongly **negatively** (−0.148, −0.129). The subagent traced its strongest drive to **Emb("He") at pos 21 with direct_effect 23.375**, plus L0:F1069 (the early male-person detector, activation 17.75) and L17:F5889 (pronoun/possessive context). So even the late "He" detector is being directly driven by the pronoun token itself, not by profession content.
- **L12:F2175** ("words referring to gender" — male/feminine/masculine) also contributes negatively (−0.156) at pos 2.

The **genuine profession pathway** is comparatively small:
- **L5:F10392** ("fields of academic study", activation 24.1) and **L5:F15490** ("academic subjects and professions", activation 8.4) fire on "Mathematics" at pos 10, with upstream embedding direct_effect only 1.44 — small relative to the pronoun embeddings.
- **L5:F10392 → L6:F170 → probe_out** is a real academic-field → humanities/field detector chain contributing only +0.120 to the probe at the output (the L6:F170 direct_effect is +0.1196).

**Net pattern:** The probe's classification is driven by a "this text is about a male academic" heuristic. The model has learned that biographical Wikipedia sentences about professors tend to start with "He received his B.A.…" — so the repeated "He/his" pronoun tokens at positions 1, 2, 3, 21, 23, 42, 44 light up a multi-layer male-gender circuit that overwhelms the weaker academic-field signal from the single token "Mathematics" at position 10. The female-suppression signatures in F14946 (suppresses ▁she/▁her) and F14893 (promotes ▁herself) confirm the circuit is genuinely gendered, not profession-specific.

The user's concern is well-supported: the **majority of the probe's classification score is causally driven by gender-marker features (L0:F2994, L7:F14946, L7:F14893, L6:F12990, L18:F14743, L12:F2175) rather than the actual profession/field indicator (L5:F10392, L6:F170)**. A counterfactual where the subject were "She" would likely flip the classification despite identical academic content.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | L0: Male pronoun detector (F1069) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 21 | L0: Male pronoun detector (F1069) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 3 | L0: Non-pronoun context (F2994, suppressed on 'his') | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 23 | L0: Non-pronoun context (F2994, suppressed on 'his') | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 44 | L0: Non-pronoun context (F2994, suppressed on 'his') | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F6270](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) | 13 | L0: Function word 'whom' (F6270) | the word "whom", sometimes also activating on nearby punctuation, sentence starts, discourse markers, and other function words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) |
| [L2:F9301](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) | 1 | L2: Subject/sentence-initial pronoun (F9301) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) |
| [L3:F4113](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4113) | 9 | L3: Question/inquiry context (F4113) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4113) |
| [L4:F993](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/993) | 2 | L4: 's contractions / generic (F993) | contractions of the verb to be in the third person singular | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/993) |
| [L4:F15567](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) | 1 | L4: Pronoun/possessive bridge (F15567) | sentences with male or female pronouns and possessives, especially ones referring to writing | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) |
| [L4:F15567](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) | 2 | L4: Pronoun/possessive bridge (F15567) | sentences with male or female pronouns and possessives, especially ones referring to writing | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) |
| [L4:F14796](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14796) | 1 | L4: Capitalized name/initials (F14796) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14796) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 10 | L5: Academic field detector (F10392, F15490) |  fields of academic study | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L5:F15490](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/15490) | 10 | L5: Academic field detector (F10392, F15490) |  academic subjects and professions | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/15490) |
| [L5:F645](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/645) | 2 | L5: Past-tense verbs (F645) |  verbs in past tense | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/645) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | L6: Male pronouns/titles (F12990) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 2 | L6: Male pronouns/titles (F12990) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 21 | L6: Male pronouns/titles (F12990) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 10 | L6: Academic field / humanities (F170) |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | L7: 'his' male-pronoun positive drive (F14946) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 2 | L7: 'his' male-pronoun positive drive (F14946) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | L7: Generic pronoun positive drive (F14893) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 3 | L7: Generic pronoun positive drive (F14893) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L12:F2175](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) | 2 | L12: Gender words (F2175, inhibitory) |  words referring to gender | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 21 | L17: Pronoun/possessive context (F5889) |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 21 | L18: 'He' gate, inhibitory (F14743) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 42 | L18: 'He' gate, inhibitory (F14743) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2994 de=0.297 |
| 3 | `inspect_feature` ×8 | L0:2994, L6:12990, L7:14946, L7:14893, L0:6270, L12:2175, L18:14743, L6:170 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F2994@3` | ❌ error | — | — | Trace L0:F2994 — "his/he" pronoun feature. What input tokens drive it? Confirm w… |
| SA-2 | `L7:F14946@2` | ✅ reported | 6 | 6 | Trace L7:F14946 — "his/him" male-pronoun feature. Confirm what this encodes and … |
| SA-3 | `L6:F170@10` | ❌ error | — | — | Trace L6:F170 — "academic field" feature firing on "Mathematics" at pos 10. Veri… |
| SA-4 | `L18:F14743@21` | ✅ reported | 4 | 4 | Trace L18:F14743 — "He" pronoun feature. Note it has NEGATIVE direct_effect (-0.… |

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 2 | `get_upstream_features` | L7:F14946@2, k=10 | Emb:"He"@1 (de=7.72) +9 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `inspect_feature` | L6, F10944 | " text in languages other than English" |
| 5 | `inspect_feature` | L4, F993 | "contractions of the verb to be in the third person singular" |
| 6 | `get_upstream_features` | L6:F12990@2, k=10 | Emb:" received"@2 (de=3.23) +9 more |
| 7 | `inspect_feature` | L5, F645 | " verbs in past tense" |
| 8 | `get_upstream_features` | L4:F993@2, k=10 | Emb:"He"@1 (de=6.28) +9 more |
| 9 | `get_upstream_features` | L6:F12990@2, k=10 | Emb:" received"@2 (de=3.23) +9 more |
| 10 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |
| 11 | `get_upstream_features` | L6:F12990@2, k=10 | Emb:" received"@2 (de=3.23) +9 more |
| 12 | `get_upstream_features` | L5:F645@2, k=10 | Emb:"He"@1 (de=3.88) +9 more |

**Findings:** L7:F14946 is a late‑layer feature that signals male pronouns (his/him/he). Its strongest upstream driver is L6:F12990, an earlier gendered pronoun detector, which itself receives strong excitation from the input embedding of the token "He" and from L5:F645 (past‑tense verb detector). Additional supporting signals come from L4:F993 (third‑person "be" contractions), L4:F15567 (sentence‑level pronoun…

</details>

<details>
<summary><b>SA-4</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@21, k=10 | Emb:" He"@21 (de=23.38) +9 more |
| 3 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 4 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 5 | `get_upstream_features` | L0:F1069@21, k=10 | Emb:" He"@21 (de=37.25) +9 more |
| 6 | `get_upstream_features` | L0:F1069@21, k=10 | Emb:" He"@21 (de=37.25) +9 more |

**Findings:** The target L18:F14743 ('He' pronoun gate) receives its strongest positive drive from the raw token embedding of ' He' (direct_effect ~23) and from an ultra‑early layer feature (L0:F1069) that explicitly detects male pronouns. Both of these upstream nodes are in the lower third of the model (layer 0) and provide a clear embedding shortcut. A mid‑high layer pronoun‑context feature (L17:F5889) also c…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F2994@3, k=10 → Emb:" his"@3 (de=42.50) +9 more |
| 2 | `get_upstream_features` | L6:F170@10, k=10 → L5:F10392 (de=11.38) +9 more |
| 3 | `inspect_feature` ×5 | L0:1069, L4:993, L17:5889, L5:10392, L5:15490 |
| 4 | `get_upstream_features` | L7:F14893@1, k=8 → Emb:"He"@1 (de=14.75) +7 more |

### Build

`build_circuit` → 22 nodes, 26 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 34,627 | 5,631 | 107,287 | 0 | $0.0236 | — | — |
| SA-4 | openai/gpt-oss-120b | 47,765 | 4,066 | 8,160 | 0 | $0.0097 | ✅ 4F/4E | Trace L18:F14743 — "He" pronoun feature. Note it has NEGATIV… |
| SA-2 | openai/gpt-oss-120b | 148,058 | 6,750 | 10,752 | 0 | $0.0264 | ✅ 6F/6E | Trace L7:F14946 — "his/him" male-pronoun feature. Confirm wh… |
| **Total** | | **230,450** | **16,447** | **126,199** | **0** | **$0.0597** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 46s