# Circuit Oracle Report
**Date:** 2026-07-28 07:21:05 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_10 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's positive score is driven almost entirely by transcoder features that detect identity-group language (race/ethnicity vocabulary, "black" as a racial term, "force" as a violent-crime cue, "cops" paired with violent-crime contexts), traced back to the input tokens *race*, *of*, *black*, *people*, *force*, and *cops*.

**Confidence:** 8/10

**Reasoning:** The circuit is overwhelmingly an *identity-mention* circuit rather than a toxicity/hate-semantics circuit. The top driver of the probe is **L6:F3902** (label: "terms referring to race and ethnicity"; frac_nonzero 0.018), with direct effect +0.586 at the probe. Its immediate upstream feed is dominated by: the raw token embedding for **"race"** at pos 5 (direct_effect 11), **L4:F5584** ("race/ethnicity/nationality group"; frac 0.007, +5.0), **L4:F117** ("race/racism/social justice, with a particular focus on terms related to Black people"; frac 0.012, +4.5), and **L5:F12135** ("discrimination based on identity"; +2.5). These mid-layer detectors in turn trace cleanly down to L0:L10682 ("the word 'race'"), and to the **"race"**, **"of"**, **"black"**, and **"people"** token embeddings — i.e., the lexical bigram "race of" plus the noun phrase "black people" supplies the entire excitatory signal.

A second branch is the **"force" / "cops" / violent-crime** pathway. **L2:F13653** ("the word 'force'") activates with +0.17 direct effect to the probe; it receives +30.0 from the **"force"** token embedding at pos 13 and additional positive input from **L1:F14824** ("descriptions of violent crimes, particularly shootings, and their legal outcomes, often including racial demographics"; frac 0.011), which is itself fed by both the **"force"** and **"cops"** token embeddings (≈+6.3 each). F14824 then also feeds positively into L4:F117. Together this means the model treats the co-occurrence of "cops … force" as a violent-crime/race-coded trigger, regardless of the surrounding semantic frame (here: a critique of media bias, which is *anti*-racist in stance, not a hate statement).

Notably absent from the positive circuit are features that encode *hateful sentiment, slurs, aggression-as-stance, or dehumanization*. Instead, every positive-driving feature is a generic identity-term detector: F3902, F117, F5584, F13158 (L2 "race/ethnicity"), F13061 (L3 "race/gender/social issues"), F14329 (L4 "black/white color"), F12135 (L5 "discrimination based on identity"), and F9228 (L6 "discrimination based on race, gender, religion, and disability"). Their autointerp labels all reduce to the same thing — *the mere presence of an identity group token* — and their promoted tokens (minorities, ethnicity, racial, racist, racism, ethnicity, Hispanic, etc.) are *neutral to activist*, not hateful.

The user is therefore correct. The probe classifies this input as toxic primarily because it contains the words "race", "black", "people", "force", and "cops" — not because the model has detected any toxic, dehumanizing, or hateful content. The circuit is "identity-mention" gating: the model classifies *whether identity groups are being discussed in a charged context* (police force + Black + race), and that is being read as a proxy for toxicity. The L7 feature **F8030** ("words about people's races, origins, and demographic groups"; frac 0.11) does fire later and *inhibits* the probe, but its negative direct_effect is much smaller in magnitude than the cumulative positive drive from F3902, F117, F5584, and the force/cops path, so the net signal remains strongly positive. A toxicity probe that lights up on a sentence criticizing media bias against Black communities, on the basis of identity-token co-occurrence, is exhibiting exactly the spurious-correlation behavior the user suspected.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: race (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: of (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 16 | Emb: black (pos 16) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: people (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: force (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: cops (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F10682](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10682) | 5 | L0: lexical "race" detector (F10682) |  the word "race" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10682) |
| [L1:F14824](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14824) | 13 | L1: violent crime / shooting context (F14824) |  descriptions of violent crimes, particularly shootings, and their legal outcomes, often including racial demographics | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14824) |
| [L1:F14824](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14824) | 8 | L1: violent crime / shooting context (F14824) |  descriptions of violent crimes, particularly shootings, and their legal outcomes, often including racial demographics | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14824) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 5 | L2: race/ethnicity term detector (F13158) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 16 | L2: race/ethnicity term detector (F13158) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13653](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13653) | 13 | L2: lexical "force" detector (F13653) | the word "force" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13653) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 17 | L3: race/gender/social-issue detector (F13061) |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 5 | L4: race/racism/Black social-justice (F117) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 6 | L4: race/racism/Black social-justice (F117) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 8 | L4: race/racism/Black social-justice (F117) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 16 | L4: race/racism/Black social-justice (F117) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 17 | L4: race/racism/Black social-justice (F117) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F5584](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5584) | 6 | L4: race/ethnicity/nationality group (F5584) |  words related to race, ethnicity, nationality or population groups | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5584) |
| [L4:F14329](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14329) | 16 | L4: black/white color token detector (F14329) |  mentions of the colors black, white, or another color with "or" in its name | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14329) |
| [L5:F12135](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12135) | 6 | L5: identity-based discrimination (F12135) |  terms related to discrimination based on identity | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12135) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 5 | L6: race/ethnicity terms (F3902) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 6 | L6: race/ethnicity terms (F3902) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 16 | L6: race/ethnicity terms (F3902) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:3902 de=0.586 |
| 3 | `inspect_feature` ×15 | L6:3902, L2:10509, L4:117, L0:7820, L6:9228, L0:1823, L3:13061, L7:8030, L4:11200, L3:6517, L0:2961, L2:13158, L2:13653, L0:1910, L6:343 |
| 4 | `get_upstream_features` | Emb:" race"@5 (de=11.00) +9 more |
| 5 | `get_upstream_features` | Emb:" race"@5 (de=19.00) +9 more |
| 6 | `get_upstream_features` | Emb:" black"@16 (de=11.38) +9 more |
| 7 | `get_upstream_features` | Emb:" race"@5 (de=30.12) +9 more |
| 8 | `get_upstream_features` | Emb:" race"@5 (de=16.62) +9 more |
| 9 | `get_upstream_features` | Emb:" black"@16 (de=10.94) +9 more |
| 10 | `get_upstream_features` | Emb:"By"@1 (de=16.25) +9 more |
| 11 | `get_upstream_features` | L5:F12135 (de=3.27) +9 more |
| 12 | `get_upstream_features` | Emb:" mentioning"@3 (de=23.12) +9 more |
| 13 | `get_upstream_features` | L6:F3902 (de=8.38) +9 more |
| 14 | `get_upstream_features` | L5:F12135 (de=2.75) +9 more |
| 15 | `inspect_feature` ×13 | L5:12135, L4:5584, L5:1431, L0:2848, L2:13653, L0:11851, L0:16013, L0:9026, L0:10682, L0:9076, L0:47, L1:3020, L1:13069 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F3902@6` | ✅ reported | 7 | 17 | Trace the upstream path from L6:F3902 (label: "terms referring to race and ethni… |
| SA-2 | `L4:F117@17` | ❌ error | — | — | Trace the upstream path from L4:F117 (label: "terms related to race, racism, and… |
| SA-3 | `L7:F8030@6` | ❌ error | — | — | Trace the upstream path from L7:F8030 (label: "words about people's races, origi… |
| SA-4 | `L2:F13653@13` | ✅ reported | 3 | 6 | Trace the upstream path from L2:F13653 (label: "the word 'force'") at position 1… |

<details>
<summary><b>SA-1</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F3902 | " terms referring to race and ethnicity" |
| 2 | `get_upstream_features` | L6:F3902@6, k=10 | Emb:" race"@5 (de=11.00) +9 more |
| 3 | `inspect_feature` | L4, F5584 | " words related to race, ethnicity, nationality or population groups" |
| 4 | `get_upstream_features` | L4:F5584@6, k=10 | Emb:" race"@5 (de=16.62) +9 more |
| 5 | `inspect_feature` | L0, F2848 | "the word "of"" |
| 6 | `inspect_feature` | L4, F117 | " terms related to race, racism, and social justice, with a particular " |
| 7 | `get_upstream_features` | L4:F117@6, k=10 | Emb:" race"@5 (de=19.00) +9 more |
| 8 | `get_upstream_features` | L0:F2848@6, k=5 | Emb:" of"@6 (de=36.75) +4 more |
| 9 | `get_upstream_features` | L0:F10682@5, k=5 | Emb:" race"@5 (de=22.62) +4 more |
| 10 | `inspect_feature` | L5, F12135 | " terms related to discrimination based on identity" |
| 11 | `get_upstream_features` | L5:F12135@6, k=10 | Emb:" race"@5 (de=4.84) +9 more |
| 12 | `inspect_feature` | L0, F10682 | " the word "race"" |
| 13 | `inspect_feature` | L5, F1431 | " phrases or words from employment law, especially equal opportunity em" |

**Findings:** The probe's top driver L6:F3902 (race/ethnicity detector) receives its strongest excitation from the raw token embedding for "race" (pos 5) and from two mid‑layer detectors L4:F5584 and L4:F117, both of which specialize in race/ethnicity vocabulary. Those mid‑layer detectors in turn draw heavily from the low‑layer token embedding for "race" (L0:F10682) and from a function‑word detector for "of" (L…

</details>

<details>
<summary><b>SA-4</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F13653 | "the word "force"" |
| 2 | `get_upstream_features` | L2:F13653@13, k=10 | Emb:" force"@13 (de=30.00) +9 more |
| 3 | `inspect_feature` | L1, F14824 | " descriptions of violent crimes, particularly shootings, and their leg" |
| 4 | `inspect_feature` | L0, F11335 | " technical documents with the word "using" in them" |
| 5 | `get_upstream_features` | L1:F14824@13, k=10 | Emb:" force"@13 (de=6.31) +9 more |
| 6 | `inspect_feature` | L0, F1438 | "words related to royalty, confinement, or a situation with hidden mean" |

**Findings:** The probe L2:F13653 (detecting the word 'force') is primarily driven by the raw token embedding for 'force' (direct effect 30.0). A secondary pathway flows from the same 'force' embedding (and the related 'cops' embedding) into a layer‑1 feature (F14824) that encodes violent‑crime contexts, which then positively excites the probe (0.31). A modest contribution also comes from a low‑level layer‑0 fe…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F117@17, k=10 → Emb:" black"@16 (de=11.56) +9 more |
| 2 | `get_upstream_features` | L2:F13158@5, k=10 → Emb:" race"@5 (de=15.44) +9 more |
| 3 | `get_upstream_features` | L7:F8030@6, k=10 → L6:F3902 (de=8.38) +9 more |
| 4 | `get_upstream_features` | L3:F13061@17, k=10 → Emb:" black"@16 (de=11.38) +9 more |
| 5 | `get_upstream_features` | L2:F13653@5, k=10 → ❌ Feature (layer=2, feature_idx=13653) not found at pos=5. Thi |
| 6 | `get_upstream_features` | L6:F9228@6, k=10 → L5:F12135 (de=2.75) +9 more |
| 7 | `get_upstream_features` | L2:F10509@5, k=10 → Emb:" race"@5 (de=30.12) +9 more |
| 8 | `get_upstream_features` | L4:F117@5, k=10 → Emb:" race"@5 (de=25.12) +9 more |
| 9 | `get_upstream_features` | L4:F14857@6, k=5 → Emb:"<bos>"@0 (de=-12.38) +4 more |
| 10 | `get_upstream_features` | L6:F3902@16, k=10 → Emb:" black"@16 (de=14.00) +9 more |
| 11 | `get_upstream_features` | L4:F117@8, k=10 → Emb:" cops"@8 (de=10.12) +9 more |
| 12 | `get_upstream_features` | L4:F117@16, k=5 → Emb:" black"@16 (de=15.38) +4 more |
| 13 | `inspect_feature` ×4 | L4:14329, L1:14824, L3:7993, L0:1438 |
| 14 | `get_upstream_features` | L4:F14329@16, k=10 → Emb:" black"@16 (de=19.62) +9 more |
| 15 | `get_upstream_features` | L2:F13653@13, k=10 → Emb:" force"@13 (de=30.00) +9 more |

### Build

`build_circuit` → 17 nodes, 39 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 86,741 | 12,398 | 733,425 | 0 | $0.0849 | — | — |
| SA-4 | openai/gpt-oss-120b | 52,871 | 4,479 | 2,336 | 0 | $0.0107 | ✅ 3F/6E | Trace the upstream path from L2:F13653 (label: "the word 'fo… |
| SA-1 | openai/gpt-oss-120b | 179,044 | 11,491 | 11,008 | 0 | $0.0339 | ✅ 7F/17E | Trace the upstream path from L6:F3902 (label: "terms referri… |
| **Total** | | **318,656** | **28,368** | **746,769** | **0** | **$0.1295** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 11s