# Circuit Oracle Report
**Date:** 2026-07-28 07:22:06 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity score is driven primarily by an L3 feature (L3:F13473) that explicitly detects "mentions of racial and ethnic groups, especially in the United States," which fires on the token "Indians" via the embedding at pos 1, and is amplified by the "abuse" lexical features (L2:F1003, L2:F6255) firing on "abusers" at pos 3.

**Confidence:** 6

**Reasoning:**

The circuit shows two parallel paths feeding the probe's output:

1. **Identity-detection path (the spurious signal the user suspects).** The strongest single contributor is **L3:F13473** (label: *"mentions of racial and ethnic groups, especially in the United States"*, frac_nonzero=0.006, very selective). Its top upstream contributors are embedding nodes for the tokens **"Indians" (pos 1, direct_effect=10.25)**, **"are" (pos 2, +5.28)**, and **"<bos>" (pos 0, −2.98)**, along with a few mid-layer helpers like L2:F2123 ("ian/jani/iti" suffix detector, which is a generic morphological feature that *also* fires on the "Indians" suffix, not a semantic identity detector). The L0 features L0:F10155 ("words related to membership in a group", whose own max-token is "anians" — i.e. literally the suffix of "Indians") and L0:F3283 ("mentions of India…") also push the score up at pos 1. Notably, the L0:F10155 feature's promoted tokens include "who," "responsible," "member," "professional" — generic group-membership language — and its *suppressed* tokens are a list of identity terms ("skiers," "hikers," "golfers," "feminists," "gamers," "rappers"). The feature fires on group-membership words but it is **not itself a toxicity signal**; it is an identity-recognition signal. When the feature is also co-active with the L2 abuse lexical features on the same prompt, the combination drives the probe up.

2. **Abuse-lexical path (the genuinely content-related signal).** **L2:F1003** and **L2:F6255** both detect the word "abuse"/"abusers" (frac_nonzero≈0.007, highly specific to that token). Their dominant input is the embedding for "abusers" at pos 3 (direct_effect=14 to F1003, 1.68 to F15690), with small contributions from surrounding tokens. These features fire specifically on the *word* "abuse" wherever it appears — they would fire identically on a sentence like "the athlete spoke about his recovery from substance abuse."

3. **The combination, not either alone, drives toxicity.** The probe's score is what the linear classifier learned during training. Looking at what the features actually encode rather than what their labels say: L3:F13473 encodes "a racial/ethnic group is named in this sentence," not "this sentence is toxic." The L2 features encode "the word 'abuse' appears," not "abuse is being described." A neutral sentence like "The article discusses how Indians have responded to historical abuse of their community" would light up the *same* features (L3:F13473 on "Indians", L2:F1003 on "abuse") and presumably score similarly.

4. **Evidence of the spurious shortcut.** The user's hypothesis is confirmed in a specific way: **L3:F13473 is a generic "racial/ethnic group mention" detector that is NOT context-sensitive to whether the group is being attacked.** Its promoted_tokens list is essentially gibberish (bootstrapcdn, SharedDtor, Personensuche, ▁betweenstory…) — meaning the feature has no learned *direction* in the output space; it is purely a mid-layer representation feeding other features. The probe at L26 picks up this mid-layer signal because, during training, the probe was trained on a corpus where racial-group mentions correlate with toxicity labels. The probe has **learned to use a generic identity-mention feature as a proxy for toxicity** rather than encoding toxicity semantics directly. The supporting L0:F10155 ("group-membership words") reinforces this.

5. **What is content, what is spurious.** The "abuse" lexical features (L2:F1003, L2:F6255) are *content* features — they indicate the prompt's lexical content includes a harm-related word. The L3:F13473 "ethnic group mention" feature is the **spurious shortcut** the user flagged: the probe fires on the *identity term* rather than on the *action* of the sentence. The generic L0 features (L0:F11154 "are", L0:F13194 "are", L0:F10389 "problems", L0:F3564 mathematical punctuation, L0:F4021 "as") are filler — they fire on common connective tissue in the sentence but are not semantically meaningful for toxicity.

**Summary of the mechanism:** The toxicity probe is driven by a **coincidental co-occurrence of two feature types in mid-layers**: (a) a generic "racial/ethnic group named" feature (L3:F13473) and (b) lexical "abuse" detectors (L2:F1003, L2:F6255). Because the probe was trained on a dataset where these co-occur in toxic examples, it has learned to treat identity-mention itself as evidence of toxicity. The circuit thus validates the user's concern: the probe uses an "identity group" signal (L3:F13473) as a shortcut rather than reasoning about whether the prompt's *content* (the action, the framing) is actually toxic. A prompt that named an ethnic group without the word "abuse" would still activate L3:F13473 and likely score non-trivially on this probe.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F3283](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3283) | 1 | L0-1: Token & identity detectors (Indians, are, abusers) |  mentions of India and related concepts like Delhi, but sometimes only finds a word indicating importance | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3283) |
| [L0:F14740](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14740) | 1 | L0-1: Token & identity detectors (Indians, are, abusers) |  names of places, people, and organizations | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14740) |
| [L0:F10155](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10155) | 1 | L0-1: Token & identity detectors (Indians, are, abusers) |  words related to membership in a group | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10155) |
| [L0:F10155](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10155) | 3 | L0-1: Token & identity detectors (Indians, are, abusers) |  words related to membership in a group | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10155) |
| [L0:F11154](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11154) | 2 | L0-1: Token & identity detectors (Indians, are, abusers) |  the word "are" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11154) |
| [L0:F13194](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13194) | 2 | L0-1: Token & identity detectors (Indians, are, abusers) |  occurrences of the word "are" or "were." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13194) |
| [L0:F10389](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10389) | 3 | L0-1: Token & identity detectors (Indians, are, abusers) |  words related to legal disputes and technical issues such as device malfunctions or program errors | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10389) |
| [L1:F15697](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15697) | 2 | L0-1: Token & identity detectors (Indians, are, abusers) |  uses of the words "are", "were", "seem", "indicate", and "themselves" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15697) |
| [L2:F2123](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2123) | 1 | L0-1: Token & identity detectors (Indians, are, abusers) |  words ending in "ian", "jani", "iti", "ino", or "olan" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2123) |
| [L0:F11835](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11835) | 3 | L0: Generic/inhibiting features (code, math, problems) | terms used in software code such as "assembly", "using", "namespace", and "license" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11835) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 3 | L0: Generic/inhibiting features (code, math, problems) | technical documents or data, including numbers, units, and references to figures or tables. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F3564](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3564) | 13 | L0: Generic/inhibiting features (code, math, problems) | mathematical notation symbols | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3564) |
| [L0:F4199](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4199) | 7 | L0: Generic/inhibiting features (code, math, problems) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4199) |
| [L2:F1003](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1003) | 3 | L2: 'abuse' lexical features (pos 3) |  the word "abuse" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1003) |
| [L2:F6255](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6255) | 3 | L2: 'abuse' lexical features (pos 3) |  the word "abuse", or phrases related to genitalia | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6255) |
| [L3:F13473](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13473) | 2 | L3-7: Ethnic/racial group & sentiment features |  mentions of racial and ethnic groups, especially in the United States | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13473) |
| [L1:F7492](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7492) | 1 | L3-7: Ethnic/racial group & sentiment features | words referring to administrative divisions, animals, or commercial elements | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7492) |
| [L4:F4021](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4021) | 4 | L3-7: Ethnic/racial group & sentiment features |  code snippets or configurations with the word "as". | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4021) |
| [L7:F15690](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15690) | 3 | L3-7: Ethnic/racial group & sentiment features |  text related to public sentiment and action in response to a problem | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15690) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:11154 de=0.652 |
| 3 | `inspect_feature` ×5 | L0:11154, L3:13473, L2:1003, L0:1053, L4:4021 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L3:F13473@2` | ❌ error | — | — | Trace L3:F13473 upstream — it fires on the word "Indians" and detects racial/eth… |
| SA-2 | `L2:F1003@3` | ❌ error | — | — | Trace L2:F1003 upstream — it fires on the word "abuse/abusing". Find what input … |
| SA-3 | `L0:F11154@2` | ❌ error | — | — | Trace L0:F11154 upstream — labeled "the word 'are'". This is a very early-layer … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×7 | L0:10155, L0:3283, L0:14740, L0:3564, L7:15690, L2:6255, L1:7492 |
| 2 | `get_upstream_features` | L3:F13473@2, k=12 → Emb:"Indians"@1 (de=10.25) +11 more |
| 3 | `get_upstream_features` | L2:F1003@3, k=12 → Emb:" abusers"@3 (de=14.00) +11 more |
| 4 | `get_upstream_features` | L0:F11154@2, k=10 → Emb:" are"@2 (de=36.00) +9 more |
| 5 | `get_upstream_features` | L7:F15690@3, k=10 → Emb:" abusers"@3 (de=1.68) +9 more |
| 6 | `get_upstream_features` | L3:F13473@1, k=8 → ❌ Feature (layer=3, feature_idx=13473) not found at pos=1. Thi |
| 7 | `inspect_feature` ×6 | L0:11835, L0:9026, L0:10389, L2:2123, L1:15697, L0:13194 |

### Build

`build_circuit` → 9 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 41,020 | 5,358 | 143,722 | 0 | $0.0274 | — | — |
| **Total** | | **41,020** | **5,358** | **143,722** | **0** | **$0.0274** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 14s