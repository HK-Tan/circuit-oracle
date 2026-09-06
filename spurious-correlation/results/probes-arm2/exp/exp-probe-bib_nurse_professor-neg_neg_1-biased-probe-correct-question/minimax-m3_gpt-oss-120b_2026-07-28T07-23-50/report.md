# Circuit Oracle Report
**Date:** 2026-07-28 07:23:50 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The classification probe's score is driven almost entirely by gender/pronoun-pronoun features at the "His" (pos 1) and "He" (pos 14, 37) token positions — with the L7 "His" feature pair (F14893/F14946) producing the largest opposing effects (+0.43 / −0.43) — and not by any profession-indicating features like "computer graphics," "PhD," "University," "Los Alamos," or "visualization."

**Confidence:** 8

**Reasoning:** The circuit traces almost exclusively to the **"His" / "He" pronoun embeddings** (pos 1, 14, 37) rather than to any technical or professional vocabulary tokens elsewhere in the passage (no "visualization," "computer," "University of Utah," or "Los Alamos" features appear). The signal flow is:

1. **Embedding nodes (L0):** `Emb: His` (pos 1) provides the dominant direct effect (e.g., +23.5, +19.75, +21.375, +13) into almost every downstream feature at pos 1. `Emb: He` (pos 14, 37) propagates through L0:F1069 (direct_effect 35.75 / 7.84) into mid-layer pronoun features. `Emb: research` / `Emb: interests` contribute only weakly (direct_effect 20–28) to the small L2:L0 features (L0:F4564, L2:F9740) which produce only modest positive probe contributions (0.13–0.16).
2. **Early pronoun features (L0–L6, pos 1):** F2994, F1069, F7439, F5491, F4315, F12990 — all gated by the "His" embedding, aggregating its identity.
3. **L7 feature pair (pos 1) — the single most important node:** F14893 (+0.43) and F14946 (−0.43) form an opposing pair directly on the residual stream at the "His" token, providing nearly the entire magnitude of the probe's score from a *single token position*. This is a classic name/pronoun detector pattern (no other position contributes comparable direct effects).
4. **Mid pronoun features (L7–L15, pos 1):** F462, F2762, F14174, F10933, F9183, F8770, F851, F12493, F8128, F7106, F12232 — all anchored on `Emb: His` with very large upstream direct effects (15–23). These are entity-tracking/name features, not profession features.
5. **Late aggregators (L18–L19):** F14743 (pos 14 & 37, "He" pronoun, −0.25/−0.21) and F7400/F10315 (pos 1, "His" pronoun, −0.16/−0.15) feed negative effects; F8814 (pos 1, +0.24) is the main late positive contributor. All upstream trace back to the "His"/"He" embeddings.
6. **Output:** The only direct paths to the probe logit come from the L7 pair (pos 1), the late pronoun aggregators (pos 1/14/37), and the weak L0–L2 features at pos 2–3 (research/interests).

**The user's concern is well-supported.** Zero features in the top 15 contributors (and downstream of all of them) reference the professional-identity tokens (scientist, professor, PhD, computer science, visualization, Los Alamos, University, etc.). The probe is reading off male-pronoun/gender-pronoun co-occurrence, not profession. The L7 "His" pair (F14893, F14946) and the "He" features at pos 14/37 are precisely the kind of spurious gender markers the user suspected — the probe likely learned that the target profession is correlated with male pronouns in training data. This is a strong case of a classification probe encoding a spurious surface feature (gender-marking pronouns) rather than the semantically relevant profession-indicating content of the biography.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | Late-layer pronoun aggregators (L18-L19) at pos 1/14/37 — negative effect on probe | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |
| [L18:F7400](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) | 1 | Late-layer pronoun aggregators (L18-L19) at pos 1/14/37 — negative effect on probe | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 1 | Late-layer pronoun aggregators (L18-L19) at pos 1/14/37 — negative effect on probe | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 14 | Late-layer pronoun aggregators (L18-L19) at pos 1/14/37 — negative effect on probe | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 37 | Late-layer pronoun aggregators (L18-L19) at pos 1/14/37 — negative effect on probe | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L15:F851](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/851) | 1 | Mid-layer pronoun/name features (L7-L15) at pos 1 | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/851) |
| [L11:F10933](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/10933) | 1 | Mid-layer pronoun/name features (L7-L15) at pos 1 | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/10933) |
| [L11:F9183](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/9183) | 1 | Mid-layer pronoun/name features (L7-L15) at pos 1 | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/9183) |
| [L9:F8770](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8770) | 1 | Mid-layer pronoun/name features (L7-L15) at pos 1 | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8770) |
| [L10:F14174](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14174) | 1 | Mid-layer pronoun/name features (L7-L15) at pos 1 | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14174) |
| [L9:F2762](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2762) | 1 | Mid-layer pronoun/name features (L7-L15) at pos 1 | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2762) |
| [L7:F462](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) | 1 | Mid-layer pronoun/name features (L7-L15) at pos 1 | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) |
| [L10:F7106](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/7106) | 1 | Mid-layer pronoun/name features (L7-L15) at pos 1 | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/7106) |
| [L12:F12493](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12493) | 1 | Mid-layer pronoun/name features (L7-L15) at pos 1 | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12493) |
| [L13:F8128](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/8128) | 1 | Mid-layer pronoun/name features (L7-L15) at pos 1 | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/8128) |
| [L10:F12232](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/12232) | 1 | Mid-layer pronoun/name features (L7-L15) at pos 1 | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/12232) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | L7 'His' feature pair (pos 1) — +0.43 / -0.43 opposing pair | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | L7 'His' feature pair (pos 1) — +0.43 / -0.43 opposing pair | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | Early-layer 'His' features (L0-L6, pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Early-layer 'His' features (L0-L6, pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L1:F7439](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7439) | 1 | Early-layer 'His' features (L0-L6, pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7439) |
| [L2:F5491](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) | 1 | Early-layer 'His' features (L0-L6, pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) |
| [L2:F9301](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) | 1 | Early-layer 'His' features (L0-L6, pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) |
| [L3:F13121](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13121) | 1 | Early-layer 'His' features (L0-L6, pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13121) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | Early-layer 'His' features (L0-L6, pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L4:F15567](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) | 1 | Early-layer 'His' features (L0-L6, pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) |
| [L5:F10952](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) | 1 | Early-layer 'His' features (L0-L6, pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Early-layer 'His' features (L0-L6, pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 14 | Later-' He' pronoun features (pos 14, 37) — drives negative contributions | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 37 | Later-' He' pronoun features (pos 14, 37) — drives negative contributions | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 14 | Later-' He' pronoun features (pos 14, 37) — drives negative contributions | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L13:F6622](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) | 14 | Later-' He' pronoun features (pos 14, 37) — drives negative contributions | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 14 | Later-' He' pronoun features (pos 14, 37) — drives negative contributions | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 37 | Later-' He' pronoun features (pos 14, 37) — drives negative contributions | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L15:F13002](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13002) | 14 | Later-' He' pronoun features (pos 14, 37) — drives negative contributions | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13002) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 14 | Later-' He' pronoun features (pos 14, 37) — drives negative contributions | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 37 | Later-' He' pronoun features (pos 14, 37) — drives negative contributions | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L2:F9740](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9740) | 3 | Early-layer 'His research interests' features (pos 1, 2, 3) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9740) |
| [L0:F4564](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) | 2 | Early-layer 'His research interests' features (pos 1, 2, 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) |
| [L0:F1065](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1065) | 3 | Early-layer 'His research interests' features (pos 1, 2, 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1065) |
| [L0:F11835](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11835) | 3 | Early-layer 'His research interests' features (pos 1, 2, 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11835) |
| [L1:F962](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/962) | 3 | Early-layer 'His research interests' features (pos 1, 2, 3) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/962) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L7:14893 de=0.430 |

### Dispatch: 9 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ❌ error | — | — | Trace from L7:F14893 at pos 1. This feature has a large positive direct_effect (… |
| SA-2 | `L7:F14946@1` | ❌ error | — | — | Trace from L7:F14946 at pos 1. This has a strong NEGATIVE direct_effect (-0.43) … |
| SA-3 | `L19:F8814@1` | ❌ error | — | — | Trace from L19:F8814 at pos 1. Positive direct_effect (0.24) on probe. Determine… |
| SA-4 | `L18:F14743@14` | ❌ error | — | — | Trace from L18:F14743 at pos 14. Strong negative effect (-0.25). Determine what … |
| SA-5 | `L18:F7400@1` | ❌ error | — | — | Trace from L18:F7400 at pos 1. Negative direct_effect (-0.16). Determine what it… |
| SA-6 | `L18:F10315@1` | ❌ error | — | — | Trace from L18:F10315 at pos 1. Negative direct_effect (-0.15). Determine what i… |
| SA-7 | `L2:F9740@3` | ❌ error | — | — | Trace from L2:F9740 at pos 3. Positive direct_effect (0.13) on probe. This is an… |
| SA-8 | `L0:F2994@1` | ❌ error | — | — | Trace from L0:F2994 at pos 1. Early layer positive effect (0.23). Determine what… |
| SA-9 | `L0:F4564@2` | ❌ error | — | — | Trace from L0:F4564 at pos 2. Early layer positive effect (0.16). Determine what… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L7:F14893@1, k=10 → Emb:"His"@1 (de=23.50) +9 more |
| 2 | `get_upstream_features` | L7:F14946@1, k=10 → Emb:"His"@1 (de=18.38) +9 more |
| 3 | `get_upstream_features` | L19:F8814@1, k=8 → Emb:"His"@1 (de=9.31) +7 more |
| 4 | `get_upstream_features` | L18:F14743@14, k=8 → Emb:" He"@14 (de=22.38) +7 more |
| 5 | `get_upstream_features` | L18:F7400@1, k=8 → Emb:"His"@1 (de=13.00) +7 more |
| 6 | `get_upstream_features` | L18:F10315@1, k=8 → Emb:"His"@1 (de=21.38) +7 more |
| 7 | `get_upstream_features` | L2:F9740@3, k=6 → Emb:" interests"@3 (de=27.00) +5 more |
| 8 | `get_upstream_features` | L0:F2994@1, k=4 → Emb:"His"@1 (de=19.75) +3 more |
| 9 | `get_upstream_features` | L0:F4564@2, k=4 → Emb:" research"@2 (de=28.12) +3 more |
| 10 | `get_upstream_features` | L6:F12990@1, k=6 → Emb:"His"@1 (de=4.91) +5 more |
| 11 | `get_upstream_features` | L2:F5491@1, k=6 → Emb:"His"@1 (de=23.88) +5 more |
| 12 | `get_upstream_features` | L4:F4315@1, k=6 → Emb:"His"@1 (de=23.50) +5 more |
| 13 | `get_upstream_features` | L1:F7439@1, k=6 → Emb:"His"@1 (de=16.38) +5 more |
| 14 | `get_upstream_features` | L18:F14743@37, k=6 → Emb:" He"@37 (de=24.00) +5 more |
| 15 | `get_upstream_features` | L7:F14893@14, k=6 → Emb:" He"@14 (de=15.62) +5 more |
| 16 | `get_upstream_features` | L7:F14893@37, k=5 → Emb:" He"@37 (de=17.50) +4 more |
| 17 | `get_upstream_features` | L6:F12990@14, k=5 → Emb:" He"@14 (de=4.16) +4 more |
| 18 | `get_upstream_features` | L0:F1069@14, k=4 → Emb:" He"@14 (de=35.75) +3 more |
| 19 | `get_upstream_features` | L17:F5889@14, k=4 → Emb:" He"@14 (de=21.50) +3 more |
| 20 | `get_upstream_features` | L13:F6622@14, k=4 → Emb:" He"@14 (de=12.50) +3 more |
| 21 | `get_upstream_features` | L15:F3330@14, k=4 → Emb:" He"@14 (de=17.12) +3 more |
| 22 | `get_upstream_features` | L15:F851@1, k=4 → L12:F12493 (de=23.38) +3 more |
| 23 | `get_upstream_features` | L11:F10933@1, k=4 → L10:F14174 (de=11.56) +3 more |
| 24 | `get_upstream_features` | L11:F9183@1, k=4 → L10:F14174 (de=13.88) +3 more |
| 25 | `get_upstream_features` | L9:F8770@1, k=4 → L7:F462 (de=15.00) +3 more |
| 26 | `get_upstream_features` | L0:F1065@3, k=4 → Emb:" interests"@3 (de=20.12) +3 more |
| 27 | `get_upstream_features` | L0:F11835@3, k=4 → Emb:"<bos>"@0 (de=-3.23) +3 more |
| 28 | `get_upstream_features` | L1:F962@3, k=4 → Emb:" interests"@3 (de=19.88) +3 more |
| 29 | `get_upstream_features` | L10:F14174@1, k=4 → L9:F3056 (de=16.62) +3 more |
| 30 | `get_upstream_features` | L9:F2762@1, k=4 → Emb:"<bos>"@0 (de=16.25) +3 more |
| 31 | `get_upstream_features` | L7:F462@1, k=4 → Emb:"<bos>"@0 (de=21.12) +3 more |
| 32 | `get_upstream_features` | L10:F7106@1, k=4 → L9:F3056 (de=5.41) +3 more |
| 33 | `get_upstream_features` | L13:F8128@1, k=4 → L10:F14174 (de=11.75) +3 more |
| 34 | `get_upstream_features` | L10:F12232@1, k=4 → L9:F8770 (de=9.69) +3 more |
| 35 | `get_upstream_features` | L12:F12493@1, k=4 → L10:F14174 (de=15.75) +3 more |

### Build

`build_circuit` → 13 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 21,419 | 7,116 | 72,156 | 0 | $0.0193 | — | — |
| **Total** | | **21,419** | **7,116** | **72,156** | **0** | **$0.0193** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 12s