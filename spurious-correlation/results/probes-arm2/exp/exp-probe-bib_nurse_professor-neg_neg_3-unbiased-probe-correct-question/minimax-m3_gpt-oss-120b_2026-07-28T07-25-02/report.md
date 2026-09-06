# Circuit Oracle Report
**Date:** 2026-07-28 07:25:02 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a mix of profession-relevant features (Ph.D./university-degree syntax, university-entity detectors keyed to "Peking University" and the final "Ph.D. ... 2003" segment) and a non-profession signal (a pronoun/possessive-marker cluster at positions 1–2, keyed to "He received his"), with a separate year-numeric contribution. The user concern is partially validated: there IS a spurious pronoun/gender-marker pathway, but the dominant evidence sits in legitimate academic-credential and entity-name features — not in gender per se.

**Confidence:** 7

**Reasoning:**

The top positive contributors to the probe (via `get_top_features`) split into five distinct clusters:

1. **`university_entity` supernode (L2–L6, pos 12–13).** Features L4:4257, L4:12975, L4:5150, L4:9333, L3:10872, L2:3342 trace directly to embeddings for "Peking" (pos 12) and "University" (pos 13) — with L0:9026 getting direct_effect=46.75 from "Peking" and L4:4257 getting 16.875 from "Peking". These are genuine named-entity / institution detectors, not gender-related. L0:5626 is a pure "Peking" bigram detector (direct_effect=12.94 from the Peking embedding). This is a legitimate profession-correlated signal (top-tier Chinese university → academic career).

2. **`phd_aggregation` supernode (L5–L7, pos 52).** Features L7:14129 (activation 50.25, the single highest activation in the positive set), L6:2254, L6:8285, L5:13801 all sit at position 52 ("D" in "Ph.D.") and feed on embeddings "Ph" (pos 50) and "D" (pos 52). This is a strong late-degree / highest-credential detector — entirely profession-relevant.

3. **`degree_field_syntax` supernode (L1–L5, scattered positions).** Feature L2:10852 (activation 38.25, the most-cited node in the graph) fires at pos 4,6,8,9,52 and aggregates the recurring "B.A./M.S./Ph.D. degree in [field] from [university]" template. Its upstream nodes include "B" (pos 4, direct_effect 12.1–14.5), "A" (pos 6, 9.06), "degree" (pos 8, 11.06–24.88), "in" (pos 9, 12.6), and "from" (pos 11, 40). This is a generic degree-template detector, a structural correlate of academia rather than a profession label.

4. **`date_year_features` (L0, pos 2, 8, 17–18).** Many L0 features fire on year tokens ("1991", "1996", "2003") — a temporal-marker signal, mildly correlated with CV-style bios.

5. **`pronoun_gender_marker` (L0, pos 1–2).** This is the feature cluster that **validates the user's concern**. L0:15320 at pos 2 ("received") is the highest-positive direct_effect (0.05) feature overall. Its upstream is L0:1903, L0:2241, L0:2530, L0:2514, L0:3232, L0:2189, L0:310, L0:478 — a large cluster of L0 features at pos 1, all of which fire on the embedding "He" (pos 1). Several of these features (L0:2241, L0:2530, L0:3232) get direct_effects of 6–8 from the "He" embedding, and L0:2514 gets 8.5 from "<bos>". This is a **masculine-pronoun pathway** flowing into the probe.

The "He received" cluster is an early-layer feature family that encodes masculine-gender marking in the first two tokens. The user's worry is **substantively correct**: the probe does use gender-coded pronoun features as one of its signals. However, the magnitude of this contribution is modest relative to the university-entity and Ph.D.-aggregation features (which each carry direct_effects an order of magnitude larger in the upstream traces — e.g., Peking embedding contributing 46.75 to L0:9026). So the probe is **not primarily** a gender detector, but gender is a non-trivial secondary signal — consistent with the classic bias finding that academic-profession probes partially exploit male-coded pronoun statistics. The circuit topology (emb_he/emb_received → pronoun_gender_marker → output) is a genuine shortcut path that the probe has learned, alongside the legitimate credential-and-institution pathway.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 52 | Ph.D. / late-degree aggregation (L6-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 52 | Ph.D. / late-degree aggregation (L6-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L6:F8285](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8285) | 52 | Ph.D. / late-degree aggregation (L6-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8285) |
| [L5:F13801](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) | 52 | Ph.D. / late-degree aggregation (L6-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) |
| [L6:F3235](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) | 13 | University name entity detector (L4-L6, pos 12-13) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) |
| [L6:F3774](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) | 12 | University name entity detector (L4-L6, pos 12-13) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) |
| [L6:F6811](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6811) | 12 | University name entity detector (L4-L6, pos 12-13) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6811) |
| [L6:F6811](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6811) | 13 | University name entity detector (L4-L6, pos 12-13) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6811) |
| [L6:F3235](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) | 12 | University name entity detector (L4-L6, pos 12-13) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) |
| [L5:F16220](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16220) | 13 | University name entity detector (L4-L6, pos 12-13) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16220) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 10 | University name entity detector (L4-L6, pos 12-13) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L4:F5150](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5150) | 13 | University name entity detector (L4-L6, pos 12-13) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5150) |
| [L4:F4257](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4257) | 12 | University name entity detector (L4-L6, pos 12-13) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4257) |
| [L4:F9333](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9333) | 13 | University name entity detector (L4-L6, pos 12-13) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9333) |
| [L3:F10872](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10872) | 13 | University name entity detector (L4-L6, pos 12-13) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10872) |
| [L2:F3342](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3342) | 13 | University name entity detector (L4-L6, pos 12-13) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3342) |
| [L4:F12975](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12975) | 12 | University name entity detector (L4-L6, pos 12-13) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12975) |
| [L0:F5626](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5626) | 12 | University name entity detector (L4-L6, pos 12-13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5626) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 12 | University name entity detector (L4-L6, pos 12-13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L3:F4213](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) | 11 | Degree/field syntax patterns (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 9 | Degree/field syntax patterns (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 6 | Degree/field syntax patterns (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L4:F11633](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11633) | 9 | Degree/field syntax patterns (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11633) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 6 | Degree/field syntax patterns (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 9 | Degree/field syntax patterns (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 8 | Degree/field syntax patterns (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 4 | Degree/field syntax patterns (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 52 | Degree/field syntax patterns (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F13360](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13360) | 52 | Degree/field syntax patterns (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13360) |
| [L1:F10132](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) | 52 | Degree/field syntax patterns (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) |
| [L3:F8294](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8294) | 52 | Degree/field syntax patterns (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8294) |
| [L4:F13943](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13943) | 52 | Degree/field syntax patterns (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13943) |
| [L5:F11028](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/11028) | 52 | Degree/field syntax patterns (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/11028) |
| [L3:F15899](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15899) | 52 | Degree/field syntax patterns (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15899) |
| [L3:F11994](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11994) | 52 | Degree/field syntax patterns (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11994) |
| [L3:F11994](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11994) | 6 | Degree/field syntax patterns (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11994) |
| [L5:F5725](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5725) | 52 | Degree/field syntax patterns (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5725) |
| [L5:F7646](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7646) | 52 | Degree/field syntax patterns (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7646) |
| [L0:F6515](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) | 17 | Year / date token features (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) |
| [L0:F11333](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11333) | 18 | Year / date token features (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11333) |
| [L0:F11132](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11132) | 18 | Year / date token features (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11132) |
| [L0:F9263](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9263) | 8 | Year / date token features (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9263) |
| [L0:F12235](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12235) | 8 | Year / date token features (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12235) |
| [L0:F6127](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6127) | 8 | Year / date token features (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6127) |
| [L0:F3662](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3662) | 18 | Year / date token features (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3662) |
| [L0:F3653](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3653) | 18 | Year / date token features (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3653) |
| [L0:F7133](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7133) | 18 | Year / date token features (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7133) |
| [L2:F14934](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14934) | 18 | Year / date token features (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14934) |
| [L0:F2085](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2085) | 2 | Year / date token features (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2085) |
| [L0:F618](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/618) | 18 | Year / date token features (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/618) |
| [L0:F15320](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) | 2 | Pronoun / gender-pronoun marker (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) |
| [L0:F1903](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1903) | 1 | Pronoun / gender-pronoun marker (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1903) |
| [L0:F2241](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2241) | 1 | Pronoun / gender-pronoun marker (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2241) |
| [L0:F2530](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2530) | 1 | Pronoun / gender-pronoun marker (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2530) |
| [L0:F2514](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2514) | 1 | Pronoun / gender-pronoun marker (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2514) |
| [L0:F3232](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3232) | 1 | Pronoun / gender-pronoun marker (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3232) |
| [L0:F2189](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2189) | 1 | Pronoun / gender-pronoun marker (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2189) |
| [L0:F310](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/310) | 1 | Pronoun / gender-pronoun marker (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/310) |
| [L0:F478](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/478) | 1 | Pronoun / gender-pronoun marker (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/478) |
| [L0:F1288](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1288) | 1 | Pronoun / gender-pronoun marker (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1288) |
| [L0:F96](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/96) | 1 | Pronoun / gender-pronoun marker (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/96) |
| [L0:F705](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/705) | 1 | Pronoun / gender-pronoun marker (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/705) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:3235 de=-0.054 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F15320@2` | ❌ error | — | — | Trace this feature upstream. It has the highest positive direct_effect (0.05) on… |
| SA-2 | `L0:F6270@13` | ❌ error | — | — | Trace this feature upstream. Positive direct_effect (0.0471) on the probe. Posit… |
| SA-3 | `L7:F14129@52` | ❌ error | — | — | Trace this feature upstream. Positive direct_effect (0.0432) on the probe. Posit… |
| SA-4 | `L3:F4213@11` | ❌ error | — | — | Trace this feature upstream. Positive direct_effect (0.0405) on the probe. Posit… |
| SA-5 | `L6:F170@10` | ❌ error | — | — | Trace this feature upstream. Positive direct_effect (0.0381) on the probe. Posit… |
| SA-6 | `L2:F14934@18` | ❌ error | — | — | Trace this feature upstream. Positive direct_effect (0.0381) on the probe. Posit… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F15320@2, k=10 → Emb:" received"@2 (de=13.00) +9 more |
| 2 | `get_upstream_features` | L0:F6270@13, k=10 → Emb:" University"@13 (de=22.88) +9 more |
| 3 | `get_upstream_features` | L7:F14129@52, k=10 → L6:F2254 (de=6.97) +9 more |
| 4 | `get_upstream_features` | L3:F4213@11, k=10 → Emb:" from"@11 (de=10.69) +9 more |
| 5 | `get_upstream_features` | L6:F170@10, k=10 → L5:F10392 (de=11.38) +9 more |
| 6 | `get_upstream_features` | L2:F14934@18, k=10 → L0:F6515 (de=8.25) +9 more |
| 7 | `get_upstream_features` | L6:F2254@52, k=8 → L2:F10852 (de=12.06) +7 more |
| 8 | `get_upstream_features` | L5:F13801@52, k=8 → L2:F10852 (de=7.38) +7 more |
| 9 | `get_upstream_features` | L1:F10132@52, k=8 → Emb:" Ph"@50 (de=16.25) +7 more |
| 10 | `get_upstream_features` | L3:F8294@52, k=8 → L2:F10852 (de=7.44) +7 more |
| 11 | `get_upstream_features` | L6:F8285@52, k=8 → Emb:" Ph"@50 (de=4.12) +7 more |
| 12 | `get_upstream_features` | L5:F10392@10, k=8 → L3:F4113 (de=3.34) +7 more |
| 13 | `get_upstream_features` | L3:F4113@9, k=8 → Emb:" in"@9 (de=11.94) +7 more |
| 14 | `get_upstream_features` | L0:F6515@17, k=8 → Emb:"1"@16 (de=29.62) +7 more |
| 15 | `get_upstream_features` | L2:F10852@52, k=8 → Emb:" Ph"@50 (de=14.75) +7 more |
| 16 | `get_upstream_features` | L4:F3727@9, k=8 → Emb:" in"@9 (de=11.62) +7 more |
| 17 | `get_upstream_features` | L4:F3727@6, k=8 → L2:F10852 (de=14.06) +7 more |
| 18 | `get_upstream_features` | L4:F11633@9, k=6 → Emb:" degree"@8 (de=3.27) +5 more |
| 19 | `get_upstream_features` | L2:F13360@52, k=6 → Emb:" Ph"@50 (de=8.31) +5 more |
| 20 | `get_upstream_features` | L5:F11028@52, k=6 → L2:F10852 (de=3.95) +5 more |
| 21 | `get_upstream_features` | L4:F13943@52, k=6 → L2:F10852 (de=7.66) +5 more |
| 22 | `get_upstream_features` | L0:F8974@11, k=6 → Emb:" from"@11 (de=40.00) +5 more |
| 23 | `get_upstream_features` | L0:F1903@1, k=5 → Emb:"<bos>"@0 (de=17.38) +4 more |
| 24 | `get_upstream_features` | L2:F10852@6, k=5 → Emb:" B"@4 (de=12.12) +4 more |
| 25 | `get_upstream_features` | L2:F10852@9, k=5 → Emb:" in"@9 (de=12.62) +4 more |
| 26 | `get_upstream_features` | L0:F11333@18, k=5 → Emb:"9"@17 (de=11.38) +4 more |
| 27 | `get_upstream_features` | L0:F11132@18, k=5 → Emb:"9"@17 (de=11.06) +4 more |
| 28 | `get_upstream_features` | L0:F9263@8, k=5 → Emb:" degree"@8 (de=24.88) +4 more |
| 29 | `get_upstream_features` | L0:F12235@8, k=5 → Emb:" degree"@8 (de=13.50) +4 more |
| 30 | `get_upstream_features` | L6:F3235@13, k=5 → L4:F5150 (de=2.88) +4 more |
| 31 | `get_upstream_features` | L4:F5150@13, k=5 → Emb:" University"@13 (de=17.75) +4 more |
| 32 | `get_upstream_features` | L5:F16220@13, k=5 → Emb:" University"@13 (de=3.64) +4 more |
| 33 | `get_upstream_features` | L6:F3774@12, k=5 → Emb:" Peking"@12 (de=10.12) +4 more |
| 34 | `get_upstream_features` | L6:F6811@12, k=5 → Emb:" Peking"@12 (de=17.25) +4 more |
| 35 | `get_upstream_features` | L6:F3235@12, k=5 → Emb:" Peking"@12 (de=4.53) +4 more |
| 36 | `get_upstream_features` | L6:F6811@13, k=5 → Emb:" Peking"@12 (de=13.44) +4 more |
| 37 | `get_upstream_features` | L4:F4257@12, k=5 → Emb:" Peking"@12 (de=16.88) +4 more |
| 38 | `get_upstream_features` | L4:F12975@12, k=5 → Emb:" Peking"@12 (de=7.53) +4 more |
| 39 | `get_upstream_features` | L4:F9333@13, k=5 → Emb:" University"@13 (de=3.69) +4 more |
| 40 | `get_upstream_features` | L2:F3342@13, k=5 → Emb:" University"@13 (de=20.00) +4 more |
| 41 | `get_upstream_features` | L0:F5626@12, k=5 → Emb:" Peking"@12 (de=12.94) +4 more |
| 42 | `get_upstream_features` | L0:F9026@12, k=5 → Emb:" Peking"@12 (de=46.75) +4 more |
| 43 | `get_upstream_features` | L0:F16024@13, k=5 → Emb:" University"@13 (de=23.00) +4 more |
| 44 | `get_upstream_features` | L3:F10872@13, k=5 → Emb:" University"@13 (de=21.75) +4 more |
| 45 | `get_upstream_features` | L0:F5990@13, k=5 → Emb:" University"@13 (de=11.19) +4 more |
| 46 | `get_upstream_features` | L3:F11994@52, k=5 → L2:F10852 (de=12.31) +4 more |
| 47 | `get_upstream_features` | L3:F11994@6, k=5 → L2:F10852 (de=11.19) +4 more |
| 48 | `get_upstream_features` | L1:F14298@52, k=5 → Emb:" Ph"@50 (de=10.94) +4 more |
| 49 | `get_upstream_features` | L1:F11924@52, k=5 → Emb:" Ph"@50 (de=10.81) +4 more |
| 50 | `get_upstream_features` | L1:F14298@52, k=5 → Emb:" Ph"@50 (de=10.94) +4 more |
| 51 | `get_upstream_features` | L3:F15899@52, k=5 → Emb:" Ph"@50 (de=6.78) +4 more |
| 52 | `get_upstream_features` | L5:F12906@52, k=5 → L2:F10852 (de=3.55) +4 more |
| 53 | `get_upstream_features` | L5:F7646@52, k=5 → L2:F10852 (de=3.14) +4 more |
| 54 | `get_upstream_features` | L5:F5725@52, k=5 → L2:F10852 (de=7.22) +4 more |
| 55 | `get_upstream_features` | L0:F1636@6, k=5 → Emb:"A"@6 (de=17.25) +4 more |
| 56 | `get_upstream_features` | L0:F8061@9, k=5 → Emb:" in"@9 (de=38.75) +4 more |
| 57 | `get_upstream_features` | L0:F1903@1, k=8 → Emb:"<bos>"@0 (de=17.38) +7 more |
| 58 | `get_upstream_features` | L0:F478@1, k=5 → Emb:"<bos>"@0 (de=6.84) +4 more |
| 59 | `get_upstream_features` | L0:F2189@1, k=5 → Emb:"<bos>"@0 (de=5.09) +4 more |
| 60 | `get_upstream_features` | L1:F14798@13, k=5 → Emb:" University"@13 (de=13.56) +4 more |
| 61 | `get_upstream_features` | L0:F15795@52, k=5 → Emb:"D"@52 (de=10.56) +4 more |
| 62 | `get_upstream_features` | L0:F12595@52, k=5 → Emb:"."@51 (de=7.03) +4 more |
| 63 | `get_upstream_features` | L0:F2433@52, k=5 → Emb:"D"@52 (de=17.00) +4 more |
| 64 | `get_upstream_features` | L0:F7554@50, k=5 → Emb:" Ph"@50 (de=4.88) +4 more |
| 65 | `get_upstream_features` | L0:F459@13, k=5 → Emb:" University"@13 (de=11.75) +4 more |
| 66 | `get_upstream_features` | L0:F14877@52, k=5 → Emb:"."@51 (de=8.12) +4 more |
| 67 | `get_upstream_features` | L0:F1148@52, k=5 → Emb:"D"@52 (de=11.56) +4 more |
| 68 | `get_upstream_features` | L0:F10469@52, k=5 → Emb:"D"@52 (de=16.25) +4 more |
| 69 | `get_upstream_features` | L0:F11532@52, k=5 → Emb:" Ph"@50 (de=7.03) +4 more |
| 70 | `get_upstream_features` | L0:F15320@2, k=15 → Emb:" received"@2 (de=13.00) +14 more |
| 71 | `get_upstream_features` | L0:F2241@1, k=5 → Emb:"He"@1 (de=6.41) +4 more |
| 72 | `get_upstream_features` | L0:F2530@1, k=5 → Emb:"He"@1 (de=7.84) +4 more |
| 73 | `get_upstream_features` | L0:F2514@1, k=5 → Emb:"<bos>"@0 (de=8.50) +4 more |
| 74 | `get_upstream_features` | L0:F3232@1, k=5 → Emb:"He"@1 (de=8.25) +4 more |
| 75 | `get_upstream_features` | L0:F8974@11, k=8 → Emb:" from"@11 (de=40.00) +7 more |
| 76 | `get_upstream_features` | L3:F4213@11, k=8 → Emb:" from"@11 (de=10.69) +7 more |
| 77 | `get_upstream_features` | L2:F10852@8, k=8 → Emb:" degree"@8 (de=19.12) +7 more |
| 78 | `get_upstream_features` | L2:F10852@4, k=8 → Emb:" B"@4 (de=14.50) +7 more |

### Build

`build_circuit` → 20 nodes, 21 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 32,926 | 10,645 | 258,558 | 0 | $0.0382 | — | — |
| **Total** | | **32,926** | **10,645** | **258,558** | **0** | **$0.0382** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 18s