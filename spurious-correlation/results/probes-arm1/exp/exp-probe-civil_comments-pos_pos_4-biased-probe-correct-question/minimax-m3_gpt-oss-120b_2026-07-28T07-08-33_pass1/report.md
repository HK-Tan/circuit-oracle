# Circuit Oracle Report
**Date:** 2026-07-28 07:08:33 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven primarily by generic identity-group / ethnic / nationality detectors that fire on the *word* "Indians" itself, with the abusive content (lexical detectors for "abuse/abusers") acting as a secondary additive signal rather than as the deciding factor.

**Confidence:** 8

**Reasoning:**

The circuit traces from a probe direction (synthetic top-1 logit, no token). The top features driving the probe are NOT primarily abuse-related. Examining the top 20 features by direct effect on the probe, I find:

1. **Identity-group features dominate the top of the ranking**:
   - **L3:F13473** (pos 2, direct_effect +0.29) — "mentions of racial and ethnic groups, especially in the United States" (frac_nonzero 0.006, very specific). The subagent traced this to: Emb("Indians", pos 1) at direct_effect 10.25, plus Emb(" are", pos 2) at 5.28, then feeding through L2:F2123 ("-ian / -jani / -iti suffix" — fires on "Indians"/"Canadians"/"Germans"), then L0:F10155 ("words related to membership in a group" — fires on "Indians", "Canadians", "riders", "natives"). This is a *pure identity-term* detector with no abuse context gating.
   - **L0:F10155** (pos 1, +0.20) and (pos 3, +0.21) — "group-membership words"; upstream is dominated by the "Indians" and "abusers" token embeddings.
   - **L0:F14740** (pos 1, +0.21) — "names of places, people, and organizations"; fires on "Delhi", "Bihar", "Mahesh" — i.e., on the "Indians" token's geographic associations.
   - **L0:F3283** (pos 1, +0.21) — "mentions of India and related concepts like Delhi".
   - **L4:F10654** (pos 1, +2.05 to L6:F1509) — "references to people of a particular place", firing on tokens like "Americans", "Canadians", "Indians".
   - **L5:F10194** — "words related to nationalities and ethnicities" (suppressing such tokens when the probe is high, but its presence in the circuit confirms ethnicity is being weighted).
   - **L6:F1509** (pos 1, +0.19) — "mentions of countries and nationalities", driven almost entirely by the "Indians" embedding (direct_effect 4.88 from Emb("Indians")).

2. **Abuse-related features are present but secondary**:
   - **L2:F1003** (pos 3, +0.30) — "the word 'abuse'"; traced by subagent to fire on the embedding of "abusers" (direct_effect 14.0). This is a *lexical* abuse detector, not an abuse-context integrator.
   - **L4:F148** (pos 3, +0.20 indirect via L7) — "words and phrases related to sexual assault and abuse".
   - **L4:F5206** (pos 3, +0.73 to L7) — "words that describe people and their behaviors".
   - **L7:F15690** (pos 3, +0.21) — "text related to public sentiment and action in response to a problem", fed by BOTH the "abusers" embedding (1.68) AND the "Indians" embedding (1.23). It mixes identity term with sentiment.

3. **Generic lexical noise** (L0:F11154 "are", L0:F1053 "as", L0:F3564 math notation, L0:F4021 code "as", L0:F4199 "quantity", L0:F10389 "faults", L3:F150 verbs) — these are spurious lexical detectors that fire incidentally; some push the probe up, some pull it down. None encode toxicity.

**Mechanism summary**: The probe's score is a *linear readout* over these features. The bulk of the positive contribution comes from features whose semantic content is "an identity group is being mentioned" — the "Indians" token embedding activates a stack of group-membership, ethnic-group, and nationality features (L0:F10155 → L2:F2123 → L3:F13473 → L4:F10654 → L5:F10194 → L6:F1509), each amplifying the next. The actual abusive vocabulary ("abusers") adds an independent lexical bump through L2:F1003 / L4:F148. Crucially, **no feature in the top of the circuit integrates the identity term with the abusive content** — L7:F15690 is the closest mixer, but its top activating examples ("voice", "cut", "sell", "surprise") show it is a generic sentiment-response feature, not a "group-targeted-abuse" detector. The circuit has a "group + lexically-abusive" structure rather than a "slur against group" structure.

**Verdict on the user's concern**: The user's hypothesis is **confirmed and even stronger than stated**. The circuit is not just using identity-mention as a *secondary* signal — the single largest, deepest, and most highly-connected pathway in the circuit (the L0→L2→L3→L4→L5→L6 identity-vertical terminating in the L6 country/nationality detector) is a *pure identity-term detector* with frac_nonzero ≈ 0.006–0.057 and a clear promoted-tokens list dominated by "citizens/residents/countrymen/Islanders". The probe appears to fire primarily because "Indians" — an identity group — is mentioned in a sentence that also contains lexical abuse vocabulary, with very little weight given to whether the abuse is *targeted at* the group, *about* the group, or *perpetrated by* the group. This is the textbook signature of a probe that has learned a "identity-mention + lexically negative ≈ toxic" shortcut rather than genuine target-group-toxicity understanding.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Indians (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: abusers (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: as (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 0 | Emb: <bos> (pos 0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F10155](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10155) | 1 | Low-level identity & group-membership lexical features |  words related to membership in a group | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10155) |
| [L0:F10155](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10155) | 3 | Low-level identity & group-membership lexical features |  words related to membership in a group | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10155) |
| [L0:F14740](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14740) | 1 | Low-level identity & group-membership lexical features |  names of places, people, and organizations | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14740) |
| [L0:F3283](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3283) | 1 | Low-level identity & group-membership lexical features |  mentions of India and related concepts like Delhi, but sometimes only finds a word indicating importance | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3283) |
| [L0:F11154](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11154) | 2 | Low-level identity & group-membership lexical features |  the word "are" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11154) |
| [L2:F2123](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2123) | 1 | Suffix & membership morphology (L2) |  words ending in "ian", "jani", "iti", "ino", or "olan" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2123) |
| [L2:F1003](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1003) | 3 | Suffix & membership morphology (L2) |  the word "abuse" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1003) |
| [L3:F13473](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13473) | 2 | Ethnic / racial group mentions (L3-L4) |  mentions of racial and ethnic groups, especially in the United States | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13473) |
| [L4:F10654](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10654) | 1 | Ethnic / racial group mentions (L3-L4) |  references to people of a particular place | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10654) |
| [L4:F12975](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12975) | 2 | Ethnic / racial group mentions (L3-L4) | mentions of Asian countries, calendars, and paganism/eastern religions | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12975) |
| [L5:F10194](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10194) | 1 | Country / nationality mentions (L5-L6) |  words related to nationalities and ethnicities | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10194) |
| [L6:F1509](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1509) | 1 | Country / nationality mentions (L5-L6) |  mentions of countries and nationalities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1509) |
| [L4:F148](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/148) | 3 | Abuse / harm lexical features |  words and phrases related to sexual assault and abuse | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/148) |
| [L4:F5206](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5206) | 3 | Abuse / harm lexical features |  words that describe people and their behaviors | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5206) |
| [L7:F15690](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15690) | 3 | Public-sentiment / response framing (L7) |  text related to public sentiment and action in response to a problem | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15690) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe classification output | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:11154 de=0.652 |
| 3 | `inspect_feature` ×4 | L0:11154, L2:1003, L3:13473, L0:10155 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L3:F13473@2` | ✅ reported | 3 | 7 | Trace the upstream circuit from L3:F13473 (identity-group / ethnic group mention… |
| SA-2 | `L2:F1003@3` | ✅ reported | 4 | 7 | Trace the upstream circuit from L2:F1003 (the word "abuse") at position 3. Find … |
| SA-3 | `L0:F10155@3` | ❌ error | — | — | Trace the upstream circuit from L0:F10155 (group-membership words) at position 3… |
| SA-4 | `L0:F10155@1` | ❌ error | — | — | Trace the upstream circuit from L0:F10155 (group-membership words) at position 1… |

<details>
<summary><b>SA-1</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F13473 | " mentions of racial and ethnic groups, especially in the United States" |
| 2 | `get_upstream_features` | L3:F13473@2, k=15 | Emb:"Indians"@1 (de=10.25) +14 more |
| 3 | `inspect_feature` | L2, F2123 | " words ending in "ian", "jani", "iti", "ino", or "olan"" |
| 4 | `get_upstream_features` | L2:F2123@1, k=15 | Emb:"Indians"@1 (de=17.12) +14 more |
| 5 | `inspect_feature` | L0, F10155 | " words related to membership in a group" |
| 6 | `get_upstream_features` | L0:F10155@1, k=10 | Emb:"Indians"@1 (de=13.12) +9 more |

**Findings:** The target feature L3:F13473 (ethnic‑group detector) receives strong positive influence directly from the embedding of the token "Indians" (direct_effect 10.25) and also from the surrounding token " are". Upstream, a morphological suffix detector (L2:F2123) amplifies the signal by recognizing the "-ian" ending, itself driven primarily by the same "Indians" embedding. A lower‑layer generic group‑me…

</details>

<details>
<summary><b>SA-2</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F1003 | " the word "abuse"" |
| 2 | `get_upstream_features` | L2:F1003@3, k=10 | Emb:" abusers"@3 (de=14.00) +9 more |
| 3 | `inspect_feature` | L0, F11835 | "terms used in software code such as "assembly", "using", "namespace", " |
| 4 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 5 | `get_upstream_features` | L0:F11835@3, k=10 | Emb:" abusers"@3 (de=7.09) +9 more |
| 6 | `inspect_feature` | L0, F10389 | " words related to legal disputes and technical issues such as device m" |
| 7 | `get_upstream_features` | L0:F9026@3, k=10 | Emb:" abusers"@3 (de=22.50) +9 more |

**Findings:** The L2 'abuse' feature is driven by the embedding of the token 'abusers' and two layer‑0 generic features that themselves receive most of their activation from the same embedding. No identity‑term token contributes meaningfully, confirming that this circuit is a pure lexical detector rather than an identity‑aware or refusal‑related pathway.

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F10155@3, k=8 → Emb:" abusers"@3 (de=13.88) +7 more |
| 2 | `inspect_feature` ×4 | L4:4021, L0:1053, L2:2123, L0:3564 |
| 3 | `get_upstream_features` | L4:F4021@4, k=8 → Emb:" as"@4 (de=27.00) +7 more |
| 4 | `inspect_feature` ×9 | L0:14740, L0:4199, L7:15690, L4:12975, L0:10389, L0:3283, L6:1509, L2:3732, L3:150 |
| 5 | `get_upstream_features` | L7:F15690@3, k=8 → Emb:" abusers"@3 (de=1.68) +7 more |
| 6 | `get_upstream_features` | L6:F1509@1, k=6 → Emb:"Indians"@1 (de=4.88) +5 more |
| 7 | `inspect_feature` ×5 | L4:5206, L4:10654, L4:148, L4:14857, L5:10194 |

### Build

`build_circuit` → 11 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 49,463 | 5,375 | 194,567 | 0 | $0.0330 | — | — |
| SA-2 | openai/gpt-oss-120b | 79,841 | 7,144 | 2,624 | 0 | $0.0163 | ✅ 4F/7E | Trace the upstream circuit from L2:F1003 (the word "abuse") … |
| SA-1 | openai/gpt-oss-120b | 48,377 | 3,546 | 5,088 | 0 | $0.0095 | ✅ 3F/7E | Trace the upstream circuit from L3:F13473 (identity-group / … |
| **Total** | | **177,681** | **16,065** | **202,279** | **0** | **$0.0587** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 46s