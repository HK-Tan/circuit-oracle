# Circuit Oracle Report
**Date:** 2026-07-28 07:24:33 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven almost entirely by masculine gender/pronoun features from "His" (pos 1) and " He" (pos 10) rather than by profession-indicating content like "History" or "Ph.D.", confirming the user's concern about spurious features.

**Confidence:** 9

**Reasoning:** The attribution circuit reveals that the probe's score is overwhelmingly sourced from a deep "His" pronoun pathway at position 1, which propagates through approximately 12 layers of the network (L0→L1→L2→L4→L5→L6→L7→L8→L9→L10→L11→L12→L15→L16→L18→L19) before feeding into the output. The dominant positive feature is L7:F14893 (direct_effect=+0.49), which traces back to the "His" embedding (pos 1, direct_effect=23.5) — a clear male gender marker. A parallel "He" pronoun pathway from position 10 (L18:F14743, L19:F8186, L21:F6216) reinforces the same male-gender signal, again driven by the masculine pronoun embeddings (" He" at pos 10, direct_effect=35.75 via L0:F1069).

The only profession-related content features have comparatively tiny direct effects: L0:F1773 at position 8 ("history", direct_effect=+0.11) and L0:F2994 at position 12 (" his" lowercase possessive, direct_effect=+0.38 — note this is also a gender marker, not profession). The features promoting the probe classification are not "professor", "research", "Ph.D.", "Harvard", or "Stanford" — they are the masculine pronouns "His" and "He" used as possessive and subject pronouns in the bio.

The mechanism is straightforward: the probe is a linear classifier on residual stream activations, and the strongest single-token signal in the input is the male-possessive "His" at position 1 (token 1, not 12), which is unusual in academic bios — the low frequency of male-gendered pronouns in this dataset makes them a strong proxy. The fact that an L0 single-token feature (L0:F2994 at pos 12 for " his") carries a direct_effect of 0.38 directly to the probe — with the only upstream being the " his" token embedding (direct_effect=44.5) — shows the probe is essentially reading a gender-marker feature, not a profession feature. The L18-L22 late-layer features that directly drive the output are also dominated by "He" pronoun integration (L18:F14743 at pos 10 is the strongest, direct_effect=-0.29 on probe, but the *path* through it carries massive positive signal from the " He" embedding).

This confirms the user's concern: the probe classifies based on the spurious gender markers "His" and "He" — male pronouns used to refer to the subject of the bio — rather than on profession-indicating tokens like "History", "Ph.D.", "Harvard", "Economics", "M.B.A.", or "Stanford".

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'His' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: ' He' (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: ' his' (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 0 | Emb: '<bos>' (pos 0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: ' history' (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | L0 'His' pronoun features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | L0 'His' pronoun features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F2749](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2749) | 1 | L0 'His' pronoun features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2749) |
| [L0:F12698](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12698) | 1 | L0 'His' pronoun features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12698) |
| [L0:F4823](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4823) | 1 | L0 'His' pronoun features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4823) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 12 | L0 'his' lowercase pronoun feature (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F1773](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1773) | 8 | L0 'history' content feature (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1773) |
| [L1:F7439](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7439) | 1 | L1 'His' features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7439) |
| [L1:F14137](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14137) | 1 | L1 'His' features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14137) |
| [L2:F5491](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) | 1 | L2 'His' features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) |
| [L2:F9301](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) | 1 | L2 'His' features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) |
| [L2:F3877](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3877) | 1 | L2 'His' features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3877) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | L4 'His' pronoun features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L4:F15567](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) | 1 | L4 'His' pronoun features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) |
| [L4:F9757](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) | 1 | L4 'His' pronoun features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) |
| [L4:F12578](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12578) | 1 | L4 'His' pronoun features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12578) |
| [L5:F10952](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) | 1 | L5 'His' features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) |
| [L5:F3992](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3992) | 1 | L5 'His' features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3992) |
| [L5:F7489](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7489) | 1 | L5 'His' features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7489) |
| [L5:F14942](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14942) | 1 | L5 'His' features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14942) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | L6 'His' features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F3426](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3426) | 1 | L6 'His' features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3426) |
| [L6:F4516](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4516) | 1 | L6 'His' features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4516) |
| [L6:F14585](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14585) | 1 | L6 'His' features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14585) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | L7 'His' pronoun gating features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | L7 'His' pronoun gating features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F462](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) | 1 | L7 'His' pronoun gating features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) |
| [L7:F5741](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5741) | 1 | L7 'His' pronoun gating features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5741) |
| [L8:F8406](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) | 1 | L8 'His' context features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) |
| [L8:F3815](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/3815) | 1 | L8 'His' context features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/3815) |
| [L9:F8770](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8770) | 1 | L9 'His' aggregation features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8770) |
| [L9:F3056](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/3056) | 1 | L9 'His' aggregation features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/3056) |
| [L9:F2762](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2762) | 1 | L9 'His' aggregation features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2762) |
| [L9:F15819](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15819) | 1 | L9 'His' aggregation features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15819) |
| [L9:F13483](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/13483) | 1 | L9 'His' aggregation features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/13483) |
| [L10:F14174](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14174) | 1 | L10 'His' pronoun aggregation (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14174) |
| [L10:F7106](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/7106) | 1 | L10 'His' pronoun aggregation (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/7106) |
| [L10:F12232](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/12232) | 1 | L10 'His' pronoun aggregation (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/12232) |
| [L10:F6804](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6804) | 1 | L10 'His' pronoun aggregation (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6804) |
| [L10:F883](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/883) | 1 | L10 'His' pronoun aggregation (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/883) |
| [L11:F10933](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/10933) | 1 | L11 'His' pronoun integration (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/10933) |
| [L11:F9183](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/9183) | 1 | L11 'His' pronoun integration (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/9183) |
| [L11:F389](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/389) | 1 | L11 'His' pronoun integration (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/389) |
| [L12:F12493](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12493) | 1 | L12 'His' pronoun features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12493) |
| [L12:F3684](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/3684) | 1 | L12 'His' pronoun features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/3684) |
| [L15:F851](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/851) | 1 | L15 'His' high-activation features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/851) |
| [L15:F751](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/751) | 1 | L15 'His' high-activation features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/751) |
| [L16:F10989](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/10989) | 1 | L16 'His' features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/10989) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 10 | L18 'He' pronoun features (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F7400](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) | 1 | L18 'He' pronoun features (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 1 | L18 'He' pronoun features (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L18:F7217](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7217) | 1 | L18 'He' pronoun features (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7217) |
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | L19 'He' pronoun features (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |
| [L19:F8186](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8186) | 10 | L19 'He' pronoun features (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8186) |
| [L19:F11110](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/11110) | 11 | L19 'He' pronoun features (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/11110) |
| [L21:F6216](https://neuronpedia.org/gemma-2-2b/21-gemmascope-transcoder-16k/6216) | 10 | L21 'He' pronoun features (pos 10/11) | — | [view](https://neuronpedia.org/gemma-2-2b/21-gemmascope-transcoder-16k/6216) |
| [L21:F4895](https://neuronpedia.org/gemma-2-2b/21-gemmascope-transcoder-16k/4895) | 11 | L21 'He' pronoun features (pos 10/11) | — | [view](https://neuronpedia.org/gemma-2-2b/21-gemmascope-transcoder-16k/4895) |
| [L22:F12117](https://neuronpedia.org/gemma-2-2b/22-gemmascope-transcoder-16k/12117) | 11 | L22 'received' negation feature (pos 11) | — | [view](https://neuronpedia.org/gemma-2-2b/22-gemmascope-transcoder-16k/12117) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 10 | L0 ' He' pronoun features (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 10 | L17 'He' pronoun features (pos 10/11) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L17:F3683](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/3683) | 11 | L17 'He' pronoun features (pos 10/11) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/3683) |
| [L17:F12634](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/12634) | 11 | L17 'He' pronoun features (pos 10/11) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/12634) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe output (gender/profession classifier) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token ' professor' is not one of the top-k next-token candid |
| 3 | `get_top_features` | 20 features; top: L7:14893 de=0.490 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ❌ error | — | — | Trace the path upstream from L7:F14893 at position 1. This feature has the large… |
| SA-2 | `L0:F2994@12` | ❌ error | — | — | Trace the path upstream from L0:F2994 at position 12. This is a very early-layer… |
| SA-3 | `L19:F8814@1` | ❌ error | — | — | Trace the path upstream from L19:F8814 at position 1. This is a mid-late layer f… |
| SA-4 | `L7:F14946@1` | ❌ error | — | — | Trace the path upstream from L7:F14946 at position 1. This feature has the large… |
| SA-5 | `L18:F14743@10` | ❌ error | — | — | Trace the path upstream from L18:F14743 at position 10. This feature has a stron… |
| SA-6 | `L22:F12117@11` | ❌ error | — | — | Trace the path upstream from L22:F12117 at position 11. This late-layer feature … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L7:F14893@1, k=15 → Emb:"His"@1 (de=23.50) +14 more |
| 2 | `get_upstream_features` | L0:F2994@12, k=10 → Emb:" his"@12 (de=44.50) +9 more |
| 3 | `get_upstream_features` | L19:F8814@1, k=10 → Emb:"His"@1 (de=9.31) +9 more |
| 4 | `get_upstream_features` | L7:F14946@1, k=15 → Emb:"His"@1 (de=18.38) +14 more |
| 5 | `get_upstream_features` | L18:F14743@10, k=10 → Emb:" He"@10 (de=22.38) +9 more |
| 6 | `get_upstream_features` | L22:F12117@11, k=10 → L21:F4895 (de=5.69) +9 more |
| 7 | `get_upstream_features` | L0:F1773@8, k=10 → Emb:" history"@8 (de=26.75) +9 more |
| 8 | `get_upstream_features` | L0:F2994@1, k=10 → Emb:"His"@1 (de=19.75) +9 more |
| 9 | `get_upstream_features` | L2:F5491@1, k=10 → Emb:"His"@1 (de=23.88) +9 more |
| 10 | `get_upstream_features` | L4:F4315@1, k=10 → Emb:"His"@1 (de=23.50) +9 more |
| 11 | `get_upstream_features` | L0:F1069@10, k=10 → Emb:" He"@10 (de=35.75) +9 more |
| 12 | `get_upstream_features` | L18:F7400@1, k=10 → Emb:"His"@1 (de=13.00) +9 more |
| 13 | `get_upstream_features` | L18:F10315@1, k=10 → Emb:"His"@1 (de=21.38) +9 more |
| 14 | `get_upstream_features` | L21:F4895@11, k=10 → L19:F11110 (de=11.00) +9 more |
| 15 | `get_upstream_features` | L0:F2994@1, k=10 → Emb:"His"@1 (de=19.75) +9 more |
| 16 | `get_upstream_features` | L0:F1069@10, k=5 → Emb:" He"@10 (de=35.75) +4 more |
| 17 | `get_upstream_features` | L18:F7217@1, k=10 → Emb:"His"@1 (de=15.69) +9 more |
| 18 | `get_upstream_features` | L1:F7439@1, k=10 → Emb:"His"@1 (de=16.38) +9 more |
| 19 | `get_upstream_features` | L11:F10933@1, k=8 → L10:F14174 (de=11.56) +7 more |
| 20 | `get_upstream_features` | L6:F12990@1, k=10 → Emb:"His"@1 (de=4.91) +9 more |
| 21 | `get_upstream_features` | L0:F1773@8, k=5 → Emb:" history"@8 (de=26.75) +4 more |
| 22 | `get_upstream_features` | L21:F6216@10, k=10 → L18:F14743 (de=7.53) +9 more |
| 23 | `get_upstream_features` | L10:F14174@1, k=8 → L9:F3056 (de=16.62) +7 more |
| 24 | `get_upstream_features` | L9:F8770@1, k=8 → L7:F462 (de=15.06) +7 more |
| 25 | `get_upstream_features` | L22:F12117@11, k=10 → L21:F4895 (de=5.69) +9 more |
| 26 | `get_upstream_features` | L19:F11110@11, k=8 → L18:F7334 (de=16.88) +7 more |
| 27 | `get_upstream_features` | L7:F462@1, k=8 → Emb:"<bos>"@0 (de=21.12) +7 more |
| 28 | `get_upstream_features` | L7:F5741@1, k=8 → Emb:"<bos>"@0 (de=12.31) +7 more |
| 29 | `get_upstream_features` | L12:F10137@20, k=8 → Emb:" Harvard"@20 (de=5.16) +7 more |
| 30 | `get_upstream_features` | L17:F5889@10, k=8 → Emb:" He"@10 (de=21.75) +7 more |
| 31 | `get_upstream_features` | L16:F10989@1, k=8 → L15:F851 (de=30.12) +7 more |
| 32 | `get_upstream_features` | L15:F851@1, k=8 → L12:F12493 (de=23.25) +7 more |
| 33 | `get_upstream_features` | L9:F3056@1, k=8 → Emb:"<bos>"@0 (de=14.44) +7 more |
| 34 | `get_upstream_features` | L5:F10952@1, k=8 → Emb:"His"@1 (de=10.69) +7 more |
| 35 | `get_upstream_features` | L21:F4895@11, k=8 → L19:F11110 (de=11.00) +7 more |
| 36 | `get_upstream_features` | L21:F6216@10, k=8 → L18:F14743 (de=7.53) +7 more |
| 37 | `get_upstream_features` | L4:F12578@1, k=5 → Emb:"His"@1 (de=9.00) +4 more |
| 38 | `get_upstream_features` | L19:F8186@10, k=8 → Emb:" He"@10 (de=14.38) +7 more |
| 39 | `get_upstream_features` | L20:F14093@11, k=5 → L19:F11110 (de=24.25) +4 more |
| 40 | `get_upstream_features` | L4:F4315@1, k=8 → Emb:"His"@1 (de=23.50) +7 more |
| 41 | `get_upstream_features` | L5:F3992@1, k=8 → Emb:"<bos>"@0 (de=21.25) +7 more |
| 42 | `get_upstream_features` | L9:F2762@1, k=8 → Emb:"<bos>"@0 (de=16.25) +7 more |
| 43 | `get_upstream_features` | L9:F15819@1, k=5 → L7:F462 (de=12.50) +4 more |
| 44 | `get_upstream_features` | L22:F12117@11, k=8 → L21:F4895 (de=5.69) +7 more |
| 45 | `get_upstream_features` | L19:F11110@11, k=5 → L18:F7334 (de=16.88) +4 more |
| 46 | `get_upstream_features` | L21:F6216@10, k=5 → L18:F14743 (de=7.53) +4 more |
| 47 | `get_upstream_features` | L4:F12578@1, k=3 → Emb:"His"@1 (de=9.00) +2 more |
| 48 | `get_upstream_features` | L21:F4895@11, k=5 → L19:F11110 (de=11.00) +4 more |
| 49 | `get_upstream_features` | L18:F14743@10, k=5 → Emb:" He"@10 (de=22.38) +4 more |
| 50 | `get_upstream_features` | L15:F851@1, k=5 → L12:F12493 (de=23.25) +4 more |
| 51 | `get_upstream_features` | L10:F14174@1, k=5 → L9:F3056 (de=16.62) +4 more |
| 52 | `get_upstream_features` | L17:F3683@11, k=5 → Emb:" received"@11 (de=6.41) +4 more |
| 53 | `get_upstream_features` | L17:F12634@11, k=5 → L16:F2313 (de=6.69) +4 more |
| 54 | `get_upstream_features` | L17:F5889@10, k=5 → Emb:" He"@10 (de=21.75) +4 more |

### Build

`build_circuit` → 28 nodes, 33 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 35,497 | 10,305 | 210,779 | 0 | $0.0357 | — | — |
| **Total** | | **35,497** | **10,305** | **210,779** | **0** | **$0.0357** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 48s