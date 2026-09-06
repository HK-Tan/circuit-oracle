# Circuit Oracle Report
**Date:** 2026-07-28 07:22:54 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven predominantly by mid-layer features that detect race/ethnicity identity terms and a racism-adjacent vocabulary feature, rather than by features encoding the prompt's lexical content, syntax, or its actual argument structure about bigotry.

**Confidence:** 7

**Reasoning:**

The top-feature list and `get_upstream_features` traces reveal a circuit whose dominant positive drivers are **identity-group detectors**, not toxicity-content detectors.

**The race/ethnicity identity supernode** (direct effects 0.32, 0.23, 0.20, 0.19, 0.17) is the largest single contributor. L2:F13158 ("words about race and ethnicity", frac_nonzero=0.0099) fires at four positions (15, 25, 32, 40) and its top upstream source is the raw embedding of "black" (direct_effect=10.5 at pos 32) and "white" (1.19, 1.82 at pos 15/25). L6:F3902 ("terms referring to race and ethnicity", frac_nonzero=0.018) is driven by the "white" embedding (10.81 at pos 25) and inherits L2:F13158 (direct_effect=2.5). These features do not distinguish between mentions of "white/black" in a neutral description versus a slur; they activate on the mere presence of racial identity tokens, as confirmed by their autointerp examples (e.g., demographic tables, "We're not just 'white'").

**The racism/race-term supernode** L4:F117 ("terms related to race, racism, and social justice, with a particular focus on terms related to Black people", frac_nonzero=0.012) fires at pos 9 ("bigot"), 25 ("white"), 32 ("black") with direct effects up to 0.22. Its upstream at pos 9 is the "ot" subword embedding (3.52) — i.e., it is triggered by the morphological suffix of "bigot"/"bigots", but its label explicitly notes it covers race/racism/social-justice vocabulary broadly. This means the feature fires on the word "bigot" **because bigot co-occurs with race terms in training data**, not because it encodes hostility per se.

**Entity/named-political features** L4:F14582 (White House/government, "Trump" promoted) and L5:F8030 (clarity/definition language) contribute modestly (0.21–0.22) and are also identity-adjacent or generic.

**Lexical/function-word features** (L0 "and", "other", periods; L1 "clearly"; L0-L6 adverbs/qualifiers) carry substantial direct effects (0.16–0.24 positive, 0.15–0.35 negative). But these are not content-bearing — they are generic lexical triggers whose top-activating examples (scientific writing, legal briefs, code) show no toxicity signal. They add noise that partially cancels (L0:F5707 −0.35, L0:F12866 −0.21, L0:F247 −0.15).

**Mechanism:** The probe fires strongly on the combination of (a) explicit racial identity tokens ("white", "black") and (b) a vocabulary feature associated with race/racism discourse. It does **not** activate a feature encoding slurs, hostile intent, dehumanization, calls for discrimination, or other lexical/semantic indicators of actual toxic content. The signal path runs Emb("white"/"black") → L2:F13158 → L4:F117 / L6:F3902 → probe, and Emb("Trump") → L4:F14582 → probe. The user's concern is validated: the circuit depends on **identity-mention features** (low-frac_nonzero, high specificity to race/ethnicity vocabulary) as a proxy for toxicity, which is a classic spurious-correlation shortcut. A benign sentence like "Census data on white and black populations" would activate the same upstream features (cf. F3902's demographics example) and likely yield a similar probe score, even though it contains no toxic content. The actual toxic content (accusations of bigotry, calls to "make America white again", framing a group as against nonwhites) is captured only indirectly via the co-occurrence of the word "bigot" with race terms, not via any dedicated hostility detector.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Input Token Embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Input Token Embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Input Token Embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 25 | Input Token Embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 32 | Input Token Embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 40 | Input Token Embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 15 | Race/Ethnicity Identity Features (L2:L6) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 25 | Race/Ethnicity Identity Features (L2:L6) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 32 | Race/Ethnicity Identity Features (L2:L6) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 40 | Race/Ethnicity Identity Features (L2:L6) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 25 | Race/Ethnicity Identity Features (L2:L6) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 40 | Race/Ethnicity Identity Features (L2:L6) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 9 | Racism/Race Term Feature (L4:F117) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 25 | Racism/Race Term Feature (L4:F117) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 32 | Racism/Race Term Feature (L4:F117) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F14582](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14582) | 5 | Named-Entity / Political Features (L4-L5) |  references to the White House and the US government | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14582) |
| [L5:F8030](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/8030) | 3 | Named-Entity / Political Features (L4-L5) |  language discussing differences, clarity, and definition | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/8030) |
| [L0:F3255](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) | 10 | Lexical / Function-Word Features (Positive, L0-L1) |  the word "and" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) |
| [L0:F7969](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7969) | 14 | Lexical / Function-Word Features (Positive, L0-L1) |  the word "other" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7969) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 18 | Lexical / Function-Word Features (Positive, L0-L1) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F6154](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6154) | 2 | Lexical / Function-Word Features (Positive, L0-L1) |  uses of 'clearly' and nearby words that are related to arguments and writing | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6154) |
| [L0:F7142](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7142) | 2 | Lexical / Function-Word Features (Positive, L0-L1) |  the word "axis" and its plural form, often in the context of scientific or technical documents | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7142) |
| [L1:F2407](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2407) | 2 | Lexical / Function-Word Features (Positive, L0-L1) |  the word "clearly" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2407) |
| [L0:F5707](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5707) | 2 | Lexical / Function-Word Features (Negative, L0-L6) |  words or phrases related to knowledge or perspective | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5707) |
| [L0:F12866](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12866) | 2 | Lexical / Function-Word Features (Negative, L0-L6) |  adverbs such as "clearly," "plainly," and "as" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12866) |
| [L0:F247](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/247) | 2 | Lexical / Function-Word Features (Negative, L0-L6) |  the word "assume" in academic writing | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/247) |
| [L6:F1707](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1707) | 1 | Lexical / Function-Word Features (Negative, L0-L6) | a variety of discourse markers, qualifiers, intensifiers, or words expressing an opinion. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1707) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe Classification Output | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:5707 de=-0.346 |

### Dispatch: 9 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F13158@32` | ❌ error | — | — | Trace this feature deeply. L2:F13158 appears at multiple positions (pos 15, 25, … |
| SA-2 | `L0:F3255@10` | ❌ error | — | — | Trace this feature deeply. L0:F3255 at pos 10 is a strong positive driver. Find … |
| SA-3 | `L6:F3902@25` | ❌ error | — | — | Trace this feature deeply. L6:F3902 at pos 25 and 40. Find its semantic meaning,… |
| SA-4 | `L5:F8030@3` | ❌ error | — | — | Trace this feature deeply. L5:F8030 at pos 3. Find semantic meaning and upstream… |
| SA-5 | `L4:F117@9` | ❌ error | — | — | Trace this feature deeply. L4:F117 at pos 9 and 32. Find semantic meaning and up… |
| SA-6 | `L0:F7969@14` | ❌ error | — | — | Trace this feature deeply. L0:F7969 at pos 14. Find semantic meaning and upstrea… |
| SA-7 | `L0:F6051@18` | ❌ error | — | — | Trace this feature deeply. L0:F6051 at pos 18. Find semantic meaning and upstrea… |
| SA-8 | `L0:F6154@2` | ❌ error | — | — | Trace this feature deeply. L0:F6154 at pos 2. Find semantic meaning and upstream… |
| SA-9 | `L0:F7142@2` | ❌ error | — | — | Trace this feature deeply. L0:F7142 at pos 2. Find semantic meaning and upstream… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×15 | L2:13158, L0:3255, L0:7969, L6:3902, L5:8030, L4:117, L0:6051, L0:6154, L0:7142, L0:5707, L1:2407, L0:12866, L4:14582, L6:1707, L0:247 |
| 2 | `get_upstream_features` | L2:F13158@32, k=12 → Emb:" black"@32 (de=10.50) +11 more |
| 3 | `get_upstream_features` | L6:F3902@25, k=10 → Emb:" white"@25 (de=10.81) +9 more |
| 4 | `get_upstream_features` | L4:F117@9, k=10 → Emb:"ot"@9 (de=3.52) +9 more |
| 5 | `get_upstream_features` | L5:F8030@3, k=10 → Emb:" clearly"@2 (de=18.25) +9 more |
| 6 | `get_upstream_features` | L4:F14582@5, k=10 → Emb:" trump"@5 (de=18.12) +9 more |
| 7 | `get_upstream_features` | L0:F3255@10, k=10 → Emb:" and"@10 (de=36.75) +9 more |
| 8 | `get_upstream_features` | L0:F7969@14, k=10 → Emb:" other"@14 (de=42.25) +9 more |
| 9 | `get_upstream_features` | L0:F6051@18, k=10 → Emb:"."@18 (de=45.75) +9 more |
| 10 | `get_upstream_features` | L6:F1707@1, k=10 → L4:F8223 (de=4.09) +9 more |
| 11 | `get_upstream_features` | L0:F6154@2, k=10 → Emb:" clearly"@2 (de=13.62) +9 more |

### Build

`build_circuit` → 7 nodes, 10 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 35,371 | 5,296 | 87,503 | 0 | $0.0222 | — | — |
| **Total** | | **35,371** | **5,296** | **87,503** | **0** | **$0.0222** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 8s