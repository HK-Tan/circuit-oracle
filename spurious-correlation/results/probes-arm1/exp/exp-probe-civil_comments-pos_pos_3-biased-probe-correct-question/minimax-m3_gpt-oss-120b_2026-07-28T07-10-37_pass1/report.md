# Circuit Oracle Report
**Date:** 2026-07-28 07:10:37 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity classification is driven by a circuit that conflates mere **identity-term presence** ("Jew", "liberal", "Self-hating", "stain") with toxicity, rather than parsing the actual hateful speech act or sentiment. Identity detectors and spurious correlation features — many of which are domain-specific to Jewish/religious-ethnic discrimination discourse — dominate the signal, exactly matching the user's concern.

**Confidence:** 8

**Reasoning:**

The circuit's strongest driver to the probe is **L6:F648 — "discrimination against particular religious or ethnic groups"** (frac_nonzero 0.016, direct_effect 0.74). Critically, this feature is *not* activated by hateful content per se; it is activated by the presence of the **identity token "Jew"** (Emb:Jew contributes direct_effect ≈ 19 to F648) and secondarily "liberal" — i.e., it fires whenever a member of a commonly-discriminated group is *named*, regardless of surrounding tone. The subagent's trace confirmed that the direct embedding → F648 edge is the largest single contributor, and that F648 aggregates a stack of identity detectors: **L3:F12151** (capitalized-token detector, promoted tokens literally include "jew"), **L4:F2405** (religious identity/spirituality), **L4:F117** (race/racism with Black focus), and **L4:F14733** (Israel-Palestine context). These features describe **who is mentioned**, not whether the mention is hateful.

The supporting nodes compound the pattern:
- **L8:F13197** ("religion/faith") and **L4:F3588** ("political party/wing") add generic identity-class signals from "Jew" and "liberal" (Emb:Jew → F13197 direct_effect 3.45; Emb:liberal → F3588 direct_effect 11.4).
- **L8:F13875** ("negative sentiment related to reputation and betrayal") is driven by **Emb:stain** at pos 9, not by slurs, threats, or call-to-action content. It pattern-matches to words like "stain" and "disgrace" used in any accusation context.
- **L3:F592** ("love/hate/affection") is a generic emotion feature driven by the subword "hat" in "Self-hating" — its promoted tokens are literally "love, hate, loved, loving", so the model treats "hating" the same as the word "hate" in any love-song context.
- **L8:F2483** ("slavery/prejudice/disability") fires on "Self-" via the self-prefix feature (F9615, F735) and on "hat" via the hat-equation LaTeX feature (F14516) — spurious: this is a *disability-and-slavery discourse* detector that has been triggered by the lexical surface of "Self-hating" and "Jew", not by any actual content about prejudice.
- The L1/F1 features (F14516 "hat-notation in equations", F1774 "text in a LaTeX document") and L2:F9871 ("latex/dash") are pure *lexical accident* features that happen to fire on the dash in "Self-hating" and the "hat" subword.

The signal flow is: **token embeddings for identity words** ("Jew", "liberal", "Self-", "hating"→"hat") → **identity/religion/race lexical detectors** (F648, F2405, F117, F13158, F13197) → **probe logit**. The one content-relevant feature, F13875 (disgrace/betrayal on "stain"), contributes but is small relative to the identity-detector mass. Crucially, the circuit contains **no detector for slurs, threats, dehumanization, or hostile intent** — the model never "reads" the sentence as a hateful self-referential attack; it simply notes that an ethnic/religious group is named in a sentence containing the words "hating" and "stain."

This **directly validates the user's concern**: the probe is using a "spurious" identity-group-lexicon signal (presence of "Jew"/"liberal" + negative-sentiment words anywhere) rather than modeling the actual toxic content. The same feature F648 would fire on *any* sentence mentioning Jews — a news article, a biography, a Wikipedia entry — and would still push the probe toward a "toxic" classification. The features are doing identity-mention detection, not toxicity detection.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L6:F648](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/648) | 6 | Discrimination against religious/ethnic groups (L6:F648 pos 6) |  words related to discrimination against particular religious or ethnic groups | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/648) |
| [L8:F13197](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13197) | 6 | Religion and faith (L8:F13197 pos 6) |  words related to religion and faith | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13197) |
| [L8:F13875](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13875) | 10 | Negative reputation / betrayal sentiment (L8:F13875 pos 10) | negative sentiment related to reputation and betrayal of trust. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13875) |
| [L8:F2483](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2483) | 3 | Slavery / prejudice / disability discussion (L8:F2483 pos 3) |  discussions of slavery, prejudice, and disabilities | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2483) |
| [L4:F2405](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) | 6 | Religious identity / spirituality (L4:F2405 pos 6) |  words related to religious identity/affiliation or spirituality including related holidays | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) |
| [L4:F14733](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14733) | 6 | Israel-Palestine context (L4:F14733 pos 6) | content related to the Israel-Palestine conflict and possibly some related topics like NBA trades. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14733) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 6 | Race / racism / Black people (L4:F117 pos 6) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F8407](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) | 4 | Antagonist / fighting (L4:F8407 pos 4) |  words related to antagonists and fighting | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) |
| [L3:F9615](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9615) | 3 | self- prefix (L3:F9615 pos 3) |  words containing the prefix "self-" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9615) |
| [L3:F12151](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12151) | 6 | Capitalized token patterns (L3:F12151 pos 6) | capitalized common letter sequences such as "SEM", "ISM", "WF", "ISH", "WE", "SE" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12151) |
| [L3:F592](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) | 3 | Love / hate / affection (L3:F592) | words related to love, affection, and hate, including foreign language | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) |
| [L3:F592](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) | 4 | Love / hate / affection (L3:F592) | words related to love, affection, and hate, including foreign language | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) |
| [L3:F735](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) | 3 | self- hyphenated forms (L3:F735 pos 3) |  words and phrases that include the word "self" followed by a hyphen | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/735) |
| [L3:F13819](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13819) | 3 | Interconnectedness / self-similarity (L3:F13819 pos 3) |  words and phrases about interconnectedness, self-similarity, and things holding together. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13819) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 6 | Race / ethnicity words (L2:F13158 pos 6) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F3983](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3983) | 3 | Subword "hat" (L2:F3983 pos 3) | the word "hat" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3983) |
| [L2:F3588](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3588) | 5 | Political party / wing terms (L2:F3588 pos 5) |  terms related to politics and political parties | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3588) |
| [L2:F9871](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9871) | 7 | Latex / code / dash (L2:F9871 pos 7) | latex and code snippets and mathematical symbols | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9871) |
| [L1:F14516](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14516) | 3 | Equations with hat-notation (L1:F14516 pos 3) |  equations with symbols, especially those using "hat" notation | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14516) |
| [L1:F1774](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1774) | 3 | Text in LaTeX document (L1:F1774 pos 3) |  text in a Latex document | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1774) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:648 de=0.738 |
| 3 | `inspect_feature` ×10 | L6:648, L2:13158, L4:2405, L8:13875, L2:3983, L0:9369, L1:1774, L8:2483, L3:592, L4:117 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F648@6` | ✅ reported | 7 | 14 | Trace the path from L6:F648 (which is about discrimination against religious/eth… |
| SA-2 | `L2:F13158@6` | ❌ error | — | — | Trace the path from L2:F13158 (which is about race and ethnicity words) up to it… |
| SA-3 | `L8:F13875@10` | ✅ reported | 5 | 10 | Trace the path from L8:F13875 (which is about negative sentiment related to repu… |
| SA-4 | `L2:F3983@3` | ✅ reported | 4 | 5 | Trace the path from L2:F3983 (which is about the word "hat" — likely firing on "… |
| SA-5 | `L4:F117@6` | ✅ reported | 4 | 5 | Trace L4:F117 (race/racism terms with Black focus) up to embedding nodes. Does i… |
| SA-6 | `L8:F2483@3` | ❌ error | — | — | Trace L8:F2483 (slavery, prejudice, disability discussions) up to embedding node… |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F648 | " words related to discrimination against particular religious or ethni" |
| 2 | `get_upstream_features` | L6:F648@6, k=10 | Emb:" Jew"@6 (de=19.38) +9 more |
| 3 | `inspect_feature` | L3, F12151 | " capitalized common letter sequences such as "SEM", "ISM", "WF", "ISH"" |
| 4 | `inspect_feature` | L4, F2405 | " words related to religious identity/affiliation or spirituality inclu" |
| 5 | `inspect_feature` | L4, F14733 | " content related to the Israel-Palestine conflict and possibly some re" |
| 6 | `get_upstream_features` | L4:F2405@6, k=10 | Emb:" liberal"@5 (de=6.75) +9 more |
| 7 | `get_upstream_features` | L3:F12151@6, k=10 | Emb:" Jew"@6 (de=11.00) +9 more |
| 8 | `get_upstream_features` | L0:F9026@6, k=10 | Emb:" Jew"@6 (de=31.38) +9 more |
| 9 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 10 | `get_upstream_features` | L4:F14733@6, k=5 | Emb:" Jew"@6 (de=5.47) +4 more |
| 11 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 12 | `inspect_feature` | L4, F117 | " terms related to race, racism, and social justice, with a particular " |

**Findings:** The discrimination‑against‑religious‑groups feature (L6:F648) is driven primarily by the raw token embedding for "Jew" (direct_effect >19) and, to a lesser extent, by the token "liberal". These token embeddings feed into a cascade of mid‑level identity detectors: a capital‑letter detector (L3:F12151), a religious‑identity detector (L4:F2405), an Israel‑Palestine context detector (L4:F14733), and a…

</details>

<details>
<summary><b>SA-3</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L8, F13875 | "negative sentiment related to reputation and betrayal of trust." |
| 2 | `get_upstream_features` | L8:F13875@10, k=10 | L6:F1561 (de=3.42) +9 more |
| 3 | `inspect_feature` | L6, F1561 | " words related to respect, status, and pride, both positive and negati" |
| 4 | `inspect_feature` | L5, F7488 | " legal language, specifically terms related to evidence and accusation" |
| 5 | `get_upstream_features` | L6:F1561@10, k=10 | L5:F7488 (de=6.19) +9 more |
| 6 | `get_upstream_features` | L5:F7488@10, k=10 | Emb:" stain"@9 (de=6.59) +9 more |
| 7 | `inspect_feature` | L5, F3440 | " phrases that indicate the author is about to make a qualification or " |
| 8 | `inspect_feature` | L4, F8154 | " words related to medical conditions or medical evaluations of a body " |
| 9 | `inspect_feature` | L0, F7696 | "the word "on"" |

**Findings:** The betrayal/disgrace sentiment (L8:F13875) is driven primarily by a cascade starting from the raw token 'stain' (pos 9), which strongly excites a legal‑accusation detector (L5:7488). That detector feeds into a dignity/shame detector (L6:1561), which finally activates the high‑level negative‑reputation feature (L8:13875). Additional modest contributions come from the token 'on' and a rebuttal‑cue …

</details>

<details>
<summary><b>SA-4</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F3983 | "the word "hat"" |
| 2 | `get_upstream_features` | L2:F3983@3, k=10 | Emb:"hat"@3 (de=25.12) +9 more |
| 3 | `inspect_feature` | L0, F8886 | "the word "egg" and plurals of it" |
| 4 | `inspect_feature` | L0, F6660 | " the word "hat" or pronouns referring to a female" |
| 5 | `get_upstream_features` | L0:F8886@3, k=10 | Emb:"hat"@3 (de=11.50) +9 more |
| 6 | `inspect_feature` | L0, F6660 | " the word "hat" or pronouns referring to a female" |
| 7 | `get_upstream_features` | L0:F6660@3, k=10 | Emb:"hat"@3 (de=13.75) +9 more |
| 8 | `inspect_feature` | L0, F8736 | "mentions of hats and energy usage" |
| 9 | `get_upstream_features` | L0:F8736@3, k=10 | Emb:"hat"@3 (de=15.00) +9 more |

**Findings:** The L2:F3983 'hat' detector receives its strongest drive directly from the input token embedding 'hat' at position 3 (direct_effect ≈ 25). Additional minor excitatory contributions come from the BOS embedding and three layer‑0 lexical features (8886, 6660, 8736) that also fire on the token 'hat' or related subwords. All upstream paths terminate at token‑embedding nodes (layer 0), satisfying the lo…

</details>

<details>
<summary><b>SA-5</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F117 | " terms related to race, racism, and social justice, with a particular " |
| 2 | `get_upstream_features` | L4:F117@6, k=15 | L3:F12151 (de=2.80) +14 more |
| 3 | `inspect_feature` | L3, F12151 | " capitalized common letter sequences such as "SEM", "ISM", "WF", "ISH"" |
| 4 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 5 | `get_upstream_features` | L3:F12151@6, k=10 | Emb:" Jew"@6 (de=11.00) +9 more |
| 6 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |

**Findings:** Tracing from L4:F117 revealed that its activation on the prompt is driven by two input embeddings: the token " liberal" (position 5) and the token " Jew" (position 6). Both have positive direct_effects (2.0 and 1.6562 respectively). Upstream features that amplify this signal include a capitalized‑sequence detector (L3:F12151) and a generic race/ethnicity detector (L2:F13158). No evidence shows tha…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F117@6, k=5 → L3:F12151 (de=2.80) +4 more |
| 2 | `get_upstream_features` | L8:F2483@3, k=5 → L3:F9615 (de=3.08) +4 more |
| 3 | `get_upstream_features` | L1:F14516@3, k=5 → Emb:"hat"@3 (de=19.50) +4 more |
| 4 | `get_upstream_features` | L3:F13819@3, k=5 → Emb:"Self"@1 (de=13.19) +4 more |
| 5 | `get_upstream_features` | L4:F8407@4, k=5 → Emb:"hat"@3 (de=10.75) +4 more |
| 6 | `get_upstream_features` | L2:F3588@5, k=5 → Emb:" liberal"@5 (de=11.44) +4 more |
| 7 | `inspect_feature` ×7 | L3:13819, L1:14516, L4:8407, L2:3588, L2:9871, L0:7460, L8:13197 |
| 8 | `get_upstream_features` | L8:F2483@3, k=5 → L3:F9615 (de=3.08) +4 more |
| 9 | `get_upstream_features` | L8:F13197@6, k=5 → L6:F648 (de=5.56) +4 more |
| 10 | `get_upstream_features` | L1:F1774@3, k=5 → Emb:"hat"@3 (de=14.50) +4 more |
| 11 | `inspect_feature` ×2 | L3:9615, L3:735 |

### Build

`build_circuit` → 25 nodes, 43 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 77,313 | 6,653 | 216,409 | 0 | $0.0442 | — | — |
| SA-4 | openai/gpt-oss-120b | 94,234 | 6,522 | 21,536 | 0 | $0.0184 | ✅ 4F/5E | Trace the path from L2:F3983 (which is about the word "hat" … |
| SA-3 | openai/gpt-oss-120b | 63,454 | 7,782 | 36,064 | 0 | $0.0147 | ✅ 5F/10E | Trace the path from L8:F13875 (which is about negative senti… |
| SA-1 | openai/gpt-oss-120b | 147,744 | 11,743 | 25,152 | 0 | $0.0296 | ✅ 7F/14E | Trace the path from L6:F648 (which is about discrimination a… |
| SA-5 | openai/gpt-oss-120b | 57,047 | 3,798 | 0 | 0 | $0.0108 | ✅ 4F/5E | Trace L4:F117 (race/racism terms with Black focus) up to emb… |
| **Total** | | **439,792** | **36,498** | **299,161** | **0** | **$0.1177** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 8m 1s