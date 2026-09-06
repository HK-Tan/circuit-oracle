# Circuit Oracle Report
**Date:** 2026-07-28 07:21:12 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_10 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity score is driven almost entirely by a chain of low/mid-layer features that detect *the mere presence of race-identity vocabulary* (the words "race", "black", "people", plus identity-group labels like "race/Black/white") at positions 5, 16, 17 — none of the circuit branches meaningfully encode harm, threat, or abuse semantics. The strongest positive contributors to the probe are L6:F3902 ("terms referring to race and ethnicity", frac_nonzero 0.018, +0.586 to probe), L4:F117 ("race, racism, and social justice … focus on Black people", frac_nonzero 0.012, +0.27), and L3:F13061 ("race, gender and social issues", +0.19), with reinforcing signal from L6:F343, L7:F8030, L6:F9228, L4:F5584, and L2:F13158 — every one of these features has "race" or "Black people" or "social issues" in its autointerp label, and the *promoted_tokens* columns show what each feature "wants to output" are words like "minorities", "racially", "racial", "racist", "racism", "ethnic", "black", "Latino", "Hispanic", "African" — i.e., these features output *more identity-talk*, not toxicity-laden tokens like "slur" or "violent" or "hate". Tracing upstream, these detectors are driven by token embeddings: `Emb: race (pos 5)` (direct_effect 11.0 into L6:F3902, 30.1 into L2:F10509, 16.6 into L4:F5584), `Emb: black (pos 16)` (11.4 into L3:F13061), `Emb: people (pos 17)` (3.45 into L3:F13061), and `Emb: force (pos 13)` through L2:F13653. The only off-ramp from race-detection into "mentions" semantics is L3:F6517 ("words related to mentioning something"), itself directly activated by `Emb: mentioning (pos 3)` — a content word, not a toxicity word.

**Confidence:** 8

**Reasoning:** The circuit validates the user's concern directly. The probe direction is being driven not by features that encode actual toxic content (slurs, threats, dehumanization, violence-as-target) but by a tightly interlocking *identity-group detection* circuit. The mid-layer supernode (`mid_race`) is dominated by L4:F117 — whose own label explicitly says "focus on terms related to Black people" — and L3:F13061 ("race, gender and social issues"). The late-layer supernode (`late_race`) consists entirely of race/ethnicity/demographic detectors (L6:F3902, L7:F8030, L6:F343, L6:F9228, L5:F12135) with frac_nonzero values in the 0.01–0.11 range (entity-specific enough to be reliable, not generic noise). Critically, the *promoted* tokens for these features are identity terms themselves ("minorities", "racially", "ethnic", "Hispanic", "Latino", "Black") — they push the model to *produce* identity-group vocabulary, not to classify the prompt as toxic. The signal flow is Emb:`race`/`black`/`people` → L2:L13158/L2:L13653 + L3:L13061 + L4:L117/L4:L5584 → L6:L3902/L7:L8030 → probe output. There is no separate "harm" or "slur" or "threat" pathway visible; the polarity comes from how heavily the probe weights the *identity-mention* direction, not from any content-bearing toxicity feature. The text's actual semantic content (a sentence complaining that the race of Black victims is being omitted by a headline) contains exactly the keywords "race", "black", "people", "force" — and those four tokens alone are sufficient to fully light up the circuit. The low-layer lexical nodes (L0:F1823, L0:F2961, L0:F1910, L0:F7820) fire on function words ("By", "not", "mentioning") but only contribute weakly and via negation-flavored detectors (L0:F2961 "necessarily/uncommon", L0:F1910 "not only") that suppress the score rather than driving it. This is a textbook example of an **identity-group spurious feature**: the probe is essentially a "does this text mention race?" detector dressed up as a toxicity classifier, and the circuit confirms the mechanism is lexical/identity-cue-driven rather than semantics-of-harm-driven.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 6 | Late-layer race / identity-group detectors (L6-L7) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 5 | Late-layer race / identity-group detectors (L6-L7) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 16 | Late-layer race / identity-group detectors (L6-L7) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F343](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/343) | 6 | Late-layer race / identity-group detectors (L6-L7) |  references to patient demographics and characteristics | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/343) |
| [L7:F8030](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8030) | 6 | Late-layer race / identity-group detectors (L6-L7) |  words about people's races, origins, and demographic groups | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8030) |
| [L6:F9228](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9228) | 6 | Late-layer race / identity-group detectors (L6-L7) |  language regarding discrimination based on race, gender, religion, and disability | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9228) |
| [L5:F12135](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12135) | 6 | Late-layer race / identity-group detectors (L6-L7) | terms related to discrimination based on identity | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12135) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 6 | Mid-layer race / social-justice / Black-focused detectors (L3-L4) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 5 | Mid-layer race / social-justice / Black-focused detectors (L3-L4) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 17 | Mid-layer race / social-justice / Black-focused detectors (L3-L4) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 8 | Mid-layer race / social-justice / Black-focused detectors (L3-L4) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F5584](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5584) | 6 | Mid-layer race / social-justice / Black-focused detectors (L3-L4) | words related to race, ethnicity, nationality or population groups | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5584) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 17 | Mid-layer race / social-justice / Black-focused detectors (L3-L4) |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 5 | Mid-layer race / social-justice / Black-focused detectors (L3-L4) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 16 | Mid-layer race / social-justice / Black-focused detectors (L3-L4) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13653](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13653) | 13 | Mid-layer race / social-justice / Black-focused detectors (L3-L4) | the word "force" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13653) |
| [L2:F10509](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10509) | 5 | Low-layer lexical detectors (L0-L2) |  the word "race." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10509) |
| [L0:F7820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7820) | 3 | Low-layer lexical detectors (L0-L2) |  words indicating uncertainty or tentativeness | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7820) |
| [L0:F1823](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1823) | 5 | Low-layer lexical detectors (L0-L2) |  occurances of the word 'Bureau' | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1823) |
| [L0:F2961](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2961) | 3 | Low-layer lexical detectors (L0-L2) |  words that act as qualifications or negations, with a high preference for "necessarily" and "uncommon." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2961) |
| [L0:F1910](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1910) | 3 | Low-layer lexical detectors (L0-L2) |  the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1910) |
| [L3:F6517](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6517) | 3 | Low-layer lexical detectors (L0-L2) |  words related to mentioning something | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6517) |
| [L4:F11200](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11200) | 1 | Low-layer lexical detectors (L0-L2) |  a variety of words and phrases related to authorship and origination of something. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11200) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:3902 de=0.586 |
| 3 | `inspect_feature` ×8 | L6:3902, L2:10509, L4:117, L0:7820, L6:9228, L0:1823, L3:13061, L7:8030 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F3902@6` | ✅ reported | 4 | 5 | Trace this race-terms feature upstream. Where does the signal originate — which … |
| SA-2 | `L4:F117@17` | ❌ error | — | — | Trace this race/racism/Black feature upstream. Where does its signal originate? |
| SA-3 | `L3:F13061@17` | ❌ error | — | — | Trace this race/gender/social-issues feature upstream to its input-token origins… |
| SA-4 | `L7:F8030@6` | ✅ reported | 4 | 5 | Trace this demographic/race feature upstream to its input-token origins. |

<details>
<summary><b>SA-1</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F3902 | " terms referring to race and ethnicity" |
| 2 | `get_upstream_features` | L6:F3902@6, k=10 | Emb:" race"@5 (de=11.00) +9 more |
| 3 | `inspect_feature` | L4, F5584 | " words related to race, ethnicity, nationality or population groups" |
| 4 | `inspect_feature` | L4, F117 | " terms related to race, racism, and social justice, with a particular " |
| 5 | `get_upstream_features` | L4:F5584@6, k=10 | Emb:" race"@5 (de=16.62) +9 more |
| 6 | `get_upstream_features` | L4:F117@6, k=10 | Emb:" race"@5 (de=19.00) +9 more |
| 7 | `inspect_feature` | L5, F12135 | " terms related to discrimination based on identity" |

**Findings:** The race‑terms feature (L6:F3902) receives its strongest excitatory input directly from the input token embedding ' race' at position 5 (direct_effect 11.0). Upstream transformer features that further amplify this signal are L4:F5584 (words about race/ethnicity) and L4:F117 (race‑related social‑justice language), both in lower layers (≤8). Tracing one hop further upstream from L4:F5584 again point…

</details>

<details>
<summary><b>SA-4</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F8030 | " words about people's races, origins, and demographic groups" |
| 2 | `get_upstream_features` | L7:F8030@6, k=10 | L6:F3902 (de=8.38) +9 more |
| 3 | `inspect_feature` | L6, F3902 | " terms referring to race and ethnicity" |
| 4 | `get_upstream_features` | L6:F3902@6, k=10 | Emb:" race"@5 (de=11.00) +9 more |
| 5 | `inspect_feature` | L4, F117 | " terms related to race, racism, and social justice, with a particular " |
| 6 | `get_upstream_features` | L4:F117@6, k=10 | Emb:" race"@5 (de=19.00) +9 more |
| 7 | `inspect_feature` | L4, F5584 | " words related to race, ethnicity, nationality or population groups" |
| 8 | `inspect_feature` | L5, F12135 | " terms related to discrimination based on identity" |

**Findings:** The target demographic/race feature (L7:F8030) receives its strongest excitatory drive from a lower‑layer race/ethnicity detector (L6:F3902), which in turn is directly activated by the input token embedding " race" at position 5. Additional upstream contributors include two mid‑layer race‑related features (L4:F117 and L4:F5584) that encode more nuanced social‑justice and demographic group semantic…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×7 | L4:11200, L3:6517, L0:2961, L2:13158, L2:13653, L0:1910, L6:343 |
| 2 | `get_upstream_features` | L0:F7820@3, k=8 → Emb:" not"@2 (de=12.50) +7 more |
| 3 | `get_upstream_features` | L4:F5584@6, k=8 → Emb:" race"@5 (de=16.62) +7 more |
| 4 | `get_upstream_features` | L2:F13158@5, k=8 → Emb:" race"@5 (de=15.44) +7 more |
| 5 | `get_upstream_features` | L2:F10509@5, k=8 → Emb:" race"@5 (de=30.12) +7 more |
| 6 | `get_upstream_features` | L3:F13061@17, k=8 → Emb:" black"@16 (de=11.38) +7 more |
| 7 | `get_upstream_features` | L3:F6517@3, k=8 → Emb:" mentioning"@3 (de=23.12) +7 more |
| 8 | `get_upstream_features` | L4:F11200@1, k=8 → Emb:"By"@1 (de=16.25) +7 more |
| 9 | `get_upstream_features` | L6:F9228@6, k=8 → L5:F12135 (de=2.75) +7 more |
| 10 | `get_upstream_features` | L7:F8030@6, k=6 → L6:F3902 (de=8.38) +5 more |
| 11 | `get_upstream_features` | L5:F12135@6, k=6 → Emb:" race"@5 (de=4.84) +5 more |
| 12 | `get_upstream_features` | L0:F1823@5, k=5 → Emb:" race"@5 (de=13.50) +4 more |
| 13 | `get_upstream_features` | L0:F2961@3, k=5 → Emb:" not"@2 (de=12.19) +4 more |
| 14 | `get_upstream_features` | L0:F1910@3, k=5 → Emb:" not"@2 (de=11.38) +4 more |
| 15 | `get_upstream_features` | L6:F343@6, k=5 → L5:F12135 (de=3.27) +4 more |

### Build

`build_circuit` → 11 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 48,941 | 4,739 | 153,526 | 0 | $0.0296 | — | — |
| SA-1 | openai/gpt-oss-120b | 63,318 | 3,819 | 2,528 | 0 | $0.0118 | ✅ 4F/5E | Trace this race-terms feature upstream. Where does the signa… |
| SA-4 | openai/gpt-oss-120b | 93,376 | 7,036 | 2,624 | 0 | $0.0183 | ✅ 4F/5E | Trace this demographic/race feature upstream to its input-to… |
| **Total** | | **205,635** | **15,594** | **158,678** | **0** | **$0.0597** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 51s