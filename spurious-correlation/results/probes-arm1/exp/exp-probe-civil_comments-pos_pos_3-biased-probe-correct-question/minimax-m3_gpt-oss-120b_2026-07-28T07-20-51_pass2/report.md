# Circuit Oracle Report
**Date:** 2026-07-28 07:20:51 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** This is a probe attribution graph for the input "Self-hating liberal Jew — a stain on his brethren and his country." The probe's "toxic" classification is driven primarily by a constellation of identity-group and slur-adjacent features firing on the token "Jew" (pos 6) — discrimination-against-religious/ethnic-groups (L6:F648), religious-identity (L4:F2405), race/ethnicity (L2:F13158), Israel-Palestine (L4:F14733), and racism/social-justice (L4:F117) — supplemented by negative-reputation features firing on the token "stain" (pos 10) and love/hate features firing on the "hat" substring of "Self-hating" (pos 3).

**Confidence:** 8

**Reasoning:** The user's suspicion is strongly corroborated. The circuit reaches token-embedding nodes (Emb: "Jew" at pos 6) and shows that the largest direct contributors to the probe are **identity-group detectors** rather than features encoding the *content* of the slur or the *sentiment valence* of the sentence. Specifically:

- **L6:F648** (frac_nonzero 0.016) is a "discrimination against particular religious or ethnic groups" feature with the single largest direct effect (0.74) on the probe; it fires on the literal "Jew" token and is fed by L3:F12151 (a capitalized-suffix detector), L4:F2405 (religious identity), L4:F14733 (Israel-Palestine), L4:F117 (race/racism), L2:F13158 (race/ethnicity), L2:F8236 (Jewish-specific), and L0:F11290 (Jewish/Israeli mentions) — i.e., a stack of low-frac_nonzero features that all activate on **identity tokens**, with no "slur" or "attitude" feature in the path.
- **L2:F13158** (race/ethnicity, frac_nonzero 0.0099) and **L4:F2405** (religious identity, frac_nonzero 0.007) also push the probe directly with positive direct_effects (0.29 and 0.24), reinforced by L2:F8236 (Jewish-specific, frac_nonzero 0.0044) and L4:F14733 (Israel-Palestine, frac_nonzero 0.0096). These features have **no discrimination/sentiment valence** baked in — they fire on any mention of "Jew," "Muslim," "Black," etc. Their top-activating examples include neutral or even pro-civil-rights contexts.
- The only **non-identity** contributors are (a) **L8:F13875** on "stain" (pos 10) — a legitimate negative-reputation feature; (b) **L3:F592** (love/hate vocabulary) firing on the "hat" suffix of "hating" at pos 3; and (c) **L0:F9369** (dash detector) and **L1:F1774** / **L2:F3983** (literal "hat" token detectors — including a LaTeX \hat detector!). These literal-substring detectors are particularly striking: the model is treating the four characters h-a-t inside "Self-**hat**-ing" as the noun "hat" (clothing item, LaTeX accent), which is the wrong sense but contributes 0.13–0.28 of positive direct effect.
- Critically, **no feature in the top 15 specifically encodes slurs, hateful intent, or a "this person hates group X" composition.** The discrimination feature (L6:F648) is the closest, but its own top-activating examples are anti-discrimination *discussions* (Jäger report on Šeduva, posts about Jewish identity, civil-rights contexts) — it is essentially an "identity group mentioned alongside a possibly-charged context" detector, not a toxicity detector. It just happens to fire here because the prompt contains the identity token "Jew."

The conclusion: the probe is largely being driven by the **mere presence of the identity token "Jew"** plus the literal "hat" substring, not by features that would recognize the actual hateful construction (a self-referential insult combining a group identity with a degradation predicate). The single most diagnostic non-identity feature (L8:F13875 on "stain") only contributes 0.23, and the race/ethnicity + religion + Israel-Palestine + racism features collectively contribute more than 1.0 of direct effect, meaning the identity-membership signal dominates the sentiment signal. This is exactly the spurious-feature concern the user raised.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 6 | Probe Output (toxicity direction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L6:F648](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/648) | 6 | L6:F648 — discrimination against religious/ethnic groups (pos 6) |  words related to discrimination against particular religious or ethnic groups | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/648) |
| [L8:F13875](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13875) | 10 | L8:F13875 — negative sentiment / reputation / betrayal (pos 10) | negative sentiment related to reputation and betrayal of trust. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13875) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 6 | L2:F13158 — words about race and ethnicity (pos 6) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L4:F2405](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) | 6 | L4:F2405 — religious identity / affiliation (pos 6) |  words related to religious identity/affiliation or spirituality including related holidays | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) |
| [L4:F14733](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14733) | 6 | L4:F14733 — Israel-Palestine conflict content (pos 6) |  content related to the Israel-Palestine conflict and possibly some related topics like NBA trades. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14733) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 6 | L4:F117 — race/racism/social-justice terms (pos 6) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L3:F12151](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12151) | 6 | L3:F12151 — capitalized suffix detector (pos 6) |  capitalized common letter sequences such as "SEM", "ISM", "WF", "ISH", "WE", "SE" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12151) |
| [L2:F8236](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8236) | 6 | L2:F8236 — Jewish-specific detector (pos 6) |  mentions of Jewish people, culture, or religion, along with associated figures and locations | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8236) |
| [L0:F11290](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11290) | 6 | L0:F11290 — Jewish/Israeli/Christian mentions (pos 6) | mentions of Jewish people, Israel, and Christianity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11290) |
| [L6:F1561](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1561) | 10 | L6:F1561 — respect/status/dignity/shame (pos 10) |  words related to respect, status, and pride, both positive and negative | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1561) |
| [L5:F7488](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7488) | 10 | L5:F7488 — legal/accusation language incl. "stain" (pos 10) |  legal language, specifically terms related to evidence and accusations | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7488) |
| [L3:F592](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) | 3 | L3:F592 — love/affection/hate vocabulary (pos 3) | words related to love, affection, and hate, including foreign language | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) |
| [L2:F3983](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3983) | 3 | L2:F3983 — literal "hat" token detector (pos 3) | the word "hat" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3983) |
| [L1:F1774](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1774) | 3 | L1:F1774 — LaTeX "hat" detector (pos 3) |  text in a Latex document | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1774) |
| [L0:F9369](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9369) | 7 | L0:F9369 — dash/subtraction symbol detector (pos 7) |  subtraction symbols | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9369) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:648 de=0.738 |
| 3 | `inspect_feature` ×4 | L6:648, L2:13158, L4:2405, L8:13875 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F648@6` | ✅ reported | 5 | 9 | Trace the full path upstream from L6:F648 ("words related to discrimination agai… |
| SA-2 | `L2:F13158@6` | ❌ error | — | — | Trace the full path upstream from L2:F13158 ("words about race and ethnicity") a… |
| SA-3 | `L4:F2405@6` | ✅ reported | 6 | 7 | Trace the full path upstream from L4:F2405 ("words related to religious identity… |
| SA-4 | `L8:F13875@10` | ✅ reported | 3 | 7 | Trace the full path upstream from L8:F13875 ("negative sentiment related to repu… |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F648 | " words related to discrimination against particular religious or ethni" |
| 2 | `get_upstream_features` | L6:F648@6, k=10 | Emb:" Jew"@6 (de=19.38) +9 more |
| 3 | `inspect_feature` | L3, F12151 | " capitalized common letter sequences such as "SEM", "ISM", "WF", "ISH"" |
| 4 | `inspect_feature` | L4, F2405 | " words related to religious identity/affiliation or spirituality inclu" |
| 5 | `get_upstream_features` | L3:F12151@6, k=10 | Emb:" Jew"@6 (de=11.00) +9 more |
| 6 | `get_upstream_features` | L4:F2405@6, k=10 | Emb:" liberal"@5 (de=6.75) +9 more |
| 7 | `inspect_feature` | L4, F14733 | " content related to the Israel-Palestine conflict and possibly some re" |
| 8 | `get_upstream_features` | L3:F12151@6, k=10 | Emb:" Jew"@6 (de=11.00) +9 more |
| 9 | `get_upstream_features` | L4:F14733@6, k=10 | Emb:" Jew"@6 (de=5.47) +9 more |
| 10 | `inspect_feature` | L4, F117 | " terms related to race, racism, and social justice, with a particular " |

**Findings:** The target token 'Jew' at position 6 is driven primarily by a direct embedding influence (19.4) and by a cascade of higher‑level features. L6:F648 captures discrimination‑related language and receives strong excitation from the raw 'Jew' embedding and from lower‑layer detectors. The most influential upstream node is L3:12151, a low‑frequency capitalized‑token detector that also promotes 'Jew'. Thi…

</details>

<details>
<summary><b>SA-3</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F2405 | " words related to religious identity/affiliation or spirituality inclu" |
| 2 | `get_upstream_features` | L4:F2405@6, k=10 | Emb:" liberal"@5 (de=6.75) +9 more |
| 3 | `inspect_feature` | L3, F12151 | " capitalized common letter sequences such as "SEM", "ISM", "WF", "ISH"" |
| 4 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 5 | `get_upstream_features` | L3:F12151@6, k=10 | Emb:" Jew"@6 (de=11.00) +9 more |
| 6 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 7 | `get_upstream_features` | L2:F13158@6, k=10 | Emb:" Jew"@6 (de=6.81) +9 more |
| 8 | `get_upstream_features` | L0:F9026@6, k=10 | Emb:" Jew"@6 (de=31.38) +9 more |
| 9 | `inspect_feature` | L0, F11290 | "mentions of Jewish people, Israel, and Christianity" |
| 10 | `inspect_feature` | L2, F8236 | " mentions of Jewish people, culture, or religion, along with associate" |

**Findings:** The target feature L4:F2405 that flags religious identity (e.g., the token "Jew") is driven primarily by the raw token embedding of "Jew" itself, with additional amplification from a chain of upstream detectors: a capitalized‑suffix feature (L3:F12151), a race/ethnicity feature (L2:F13158), and a highly specific Jewish‑mention feature (L2:F8236). Lower‑layer (≤8) features are present (L3, L2, L0),…

</details>

<details>
<summary><b>SA-4</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L8, F13875 | "negative sentiment related to reputation and betrayal of trust." |
| 2 | `get_upstream_features` | L8:F13875@10, k=10 | L6:F1561 (de=3.42) +9 more |
| 3 | `inspect_feature` | L6, F1561 | " words related to respect, status, and pride, both positive and negati" |
| 4 | `inspect_feature` | L5, F7488 | " legal language, specifically terms related to evidence and accusation" |
| 5 | `get_upstream_features` | L6:F1561@10, k=10 | L5:F7488 (de=6.19) +9 more |
| 6 | `get_upstream_features` | L5:F7488@10, k=10 | Emb:" stain"@9 (de=6.59) +9 more |

**Findings:** The negative‑sentiment feature L8:F13875 is driven primarily by the token 'stain' (position 9). The embedding of 'stain' strongly excites a legal‑accusation detector (L5:F7488), which in turn activates a respect/ dignity detector (L6:F1561). Both intermediate features funnel positive influence into the target sentiment gate. All traced nodes lie at layers ≤ 8, satisfying the lower‑third floor, and…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L8:F13875@10, k=5 → L6:F1561 (de=3.42) +4 more |
| 2 | `inspect_feature` ×11 | L6:1561, L5:7488, L2:3983, L1:1774, L0:9369, L8:2483, L3:13819, L3:592, L4:8407, L2:3588, L2:9871 |
| 3 | `get_upstream_features` | L3:F592@3, k=8 → Emb:"hat"@3 (de=14.56) +7 more |
| 4 | `get_upstream_features` | L2:F3983@3, k=5 → Emb:"hat"@3 (de=25.12) +4 more |
| 5 | `get_upstream_features` | L1:F1774@3, k=5 → Emb:"hat"@3 (de=14.50) +4 more |
| 6 | `get_upstream_features` | L0:F9369@7, k=5 → Emb:" -"@7 (de=21.50) +4 more |
| 7 | `get_upstream_features` | L2:F3588@5, k=5 → Emb:" liberal"@5 (de=11.44) +4 more |
| 8 | `get_upstream_features` | L4:F8407@4, k=5 → Emb:"hat"@3 (de=10.75) +4 more |
| 9 | `inspect_feature` ×5 | L2:8236, L3:12151, L4:14733, L4:117, L0:11290 |

### Build

`build_circuit` → 22 nodes, 37 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 58,027 | 5,980 | 138,092 | 0 | $0.0329 | — | — |
| SA-1 | openai/gpt-oss-120b | 101,337 | 7,255 | 7,968 | 0 | $0.0197 | ✅ 5F/9E | Trace the full path upstream from L6:F648 ("words related to… |
| SA-3 | openai/gpt-oss-120b | 108,793 | 7,481 | 7,632 | 0 | $0.0209 | ✅ 6F/7E | Trace the full path upstream from L4:F2405 ("words related t… |
| SA-4 | openai/gpt-oss-120b | 44,361 | 4,219 | 10,176 | 0 | $0.0093 | ✅ 3F/7E | Trace the full path upstream from L8:F13875 ("negative senti… |
| **Total** | | **312,518** | **24,935** | **163,868** | **0** | **$0.0828** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 36s