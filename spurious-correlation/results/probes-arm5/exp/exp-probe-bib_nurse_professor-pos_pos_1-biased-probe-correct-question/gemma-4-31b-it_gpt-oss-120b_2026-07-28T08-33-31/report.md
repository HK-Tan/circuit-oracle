# Circuit Oracle Report
**Date:** 2026-07-28 08:33:31 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by a dual-pathway mechanism: a genuine profession-specific circuit triggered by the token "nurses" and a spurious gender-based circuit triggered by the token "she".

**Confidence:** 9

**Reasoning:**
The attribution circuit reveals two distinct signal flows contributing to the probe's output score:

1.  **Genuine Profession Pathway:** This is a multi-hop circuit originating from the embedding of the token **" nurses" (pos 15)**. The signal flows from the embedding into a highly specific nursing detector (**L2:F15437**), then through a broader healthcare/medical context supernode (**L4:F11037**, **L5:F1275**), and finally into a late-layer nursing profession driver (**L6:F15267**). This feature (L6:F15267) has a high direct effect (1.55) on the probe score and is semantically tied to nursing (activated by "RN", "nurse").

2.  **Spurious Gender Pathway:** A separate signal originates from the embedding of the token **" she" (pos 7)**. This signal feeds into a cluster of female gender features (**L6:F11646**, **L12:F12940**, **L18:F14677**). Specifically, **L6:F11646** (direct effect 1.55) is a strong detector for female pronouns and titles.

**Conclusion on User Concern:**
The user's concern is validated. While the model *does* utilize genuine profession indicators ("nurses" $\rightarrow$ L6:F15267), it also relies on spurious gender markers ("she" $\rightarrow$ L6:F11646) to drive the classification score. Both pathways provide roughly equal positive direct effects to the probe, indicating that the probe's classification of "nurse" is partially predicated on the subject being female.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: she (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: nurses (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 7 | Female Gender Features |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 7 | Female Gender Features |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 7 | Female Gender Features | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L2:F15437](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15437) | 15 | Specific Nursing Feature | words related to nurses and sound | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15437) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 15 | Healthcare/Medical Context | words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 15 | Healthcare/Medical Context | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 15 | Nursing Profession Driver |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 3 | `get_top_features` | 15 features; top: L6:11646 de=1.555 |
| 4 | `inspect_feature` ×5 | L6:11646, L18:14677, L12:12940, L4:7864, L6:15267 |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F15267@15` | ✅ reported | 6 | 5 | Trace the source of the nursing signal and gender signal to see which one domina… |
| SA-2 | `L6:F11646@7` | ✅ reported | 3 | 5 | Trace the source of the female pronoun signal to see which tokens trigger it. Fi… |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@15, k=10 | Emb:" nurses"@15 (de=16.12) +9 more |
| 3 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 4 | `inspect_feature` | L4, F8751 | " cell types in the brain, especially glial cells and neurons, and rela" |
| 5 | `get_upstream_features` | L4:F11037@15, k=10 | Emb:" nurses"@15 (de=5.16) +9 more |
| 6 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 7 | `inspect_feature` | L2, F15437 | " words related to nurses and sound" |
| 8 | `inspect_feature` | L2, F5224 | " words related to retail and customer service jobs" |
| 9 | `get_upstream_features` | L2:F15437@15, k=10 | Emb:" nurses"@15 (de=19.25) +9 more |
| 10 | `get_upstream_features` | L4:F8751@15, k=10 | Emb:" nurses"@15 (de=9.81) +9 more |

**Findings:** The nursing signal for the target feature L6:F15267 is driven primarily by a low‑layer (L2) nursing‑specific detector (F15437). Its input embedding ' nurses' (pos 15) contributes a direct effect of 19.25 to F15437, which then pushes L4:F11037 (health‑care context) and ultimately L6:F15267. The cumulative positive influence from the nursing pathway (~16+ from the embedding plus ~1.2 from intermedia…

</details>

<details>
<summary><b>SA-2</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@7, k=10 | Emb:" she"@7 (de=31.62) +9 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 5 | `get_upstream_features` | L4:F7864@7, k=10 | Emb:" she"@7 (de=27.25) +9 more |
| 6 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 7 | `get_upstream_features` | L5:F10952@7, k=10 | Emb:" she"@7 (de=10.00) +9 more |
| 8 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 9 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |

**Findings:** The female pronoun signal originates directly from the embedding of the token " she" at position 7, which supplies a large positive contribution (31.6) to the target feature L6:F11646. A mid‑layer (L4:F7864) and a higher‑layer (L5:F10952) pronoun‑related features also feed into the target, but they themselves are driven mainly by the same " she" embedding. All discovered paths satisfy the terminat…

</details>

### Build

`build_circuit` → 7 nodes, 6 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 88,911 | 1,219 | 0 | 0 | $0.0129 | — | — |
| SA-1 | openai/gpt-oss-120b | 90,589 | 6,475 | 21,920 | 0 | $0.0178 | ✅ 6F/5E | Trace the source of the nursing signal and gender signal to … |
| SA-2 | openai/gpt-oss-120b | 89,892 | 5,494 | 12,640 | 0 | $0.0170 | ✅ 3F/5E | Trace the source of the female pronoun signal to see which t… |
| **Total** | | **269,392** | **13,188** | **34,560** | **0** | **$0.0477** | | |

**Oracle wall-clock time:** 2m 49s