# Circuit Oracle Report
**Date:** 2026-07-28 07:20:19 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven primarily by *identity group* signals at the input (the token "Indians" and the word "abusers") rather than by deep semantic content of the toxic message, with a generic "are/is" grammatical scaffold amplifying the signal.

**Confidence:** 7

**Reasoning:**

The user is right to be concerned, but the picture is more nuanced than purely spurious.

**What the top features actually encode (circuit evidence):**

The two largest *positive* direct effects on the probe come from L0:F11375 ("the word 'is'", frac_nonzero 0.01, fired on "is" at pos 8 with DE=0.22) and L0:F11668 ("Baseball terminology", frac_nonzero 0.009, fired on "Indians" at pos 1 with DE=0.18). The baseball-term feature is a clear spurious-correlation artifact — it fires on the token "Indians" simply because in pretraining "Indians" often appeared in baseball contexts (Cleveland Indians). Its top activating examples are all about baseball, and its only meaningful upstream signal on this input is the "Indians" embedding itself (DE=12.4). So part of the probe's score is being driven by a feature that mislabels the entity.

The "Indians" token also drives L2:F2123 ("words ending in 'ian'" — promoted tokens include "Canadian", "American"), L0:F10155 ("words related to membership in a group"), and crucially L3:F13473 ("mentions of racial and ethnic groups, especially in the United States", DE=+0.12). The downstream L6:F10545 ("political rhetoric related to race, historical states, government control", DE=+0.14) and L6:F1600 ("negative words and phrases related to problems", DE=-0.10, at "problems" pos 12) form the final supernode feeding the probe.

**Is this spurious?** Partially yes:
- L0:F11668 (baseball) is clearly off-target for toxicity — it's a nationality/entity cue from pretraining co-occurrence statistics.
- L0:F11375 ("is") and L0:F11154 ("are") are grammatical scaffolding — they fire on any copular sentence, not on hateful content specifically. Their contribution is structural rather than semantic.
- L3:F14281 (French "comment"/how-to questions) fires here purely as a "how/to/know" pattern and contributes negatively — another generic pattern leaking in.

**Is there genuine toxic content?** Yes, but it's narrow:
- L3:F4852 ("the term 'abuse'", DE=+0.097 firing on "abusers" pos 3) is content-relevant.
- L4:F148 ("sexual assault and abuse", DE=+0.14) and L5:F3229 ("violent assault and murder", DE=-0.12) engage with the "abusers" token meaningfully.
- L3:F4327 fires on "-ive" suffix in "abusive" and "destructive."

**Mechanism summary:** Signal flows from token embeddings "Indians" (pos 1) and "abusers" (pos 3) → L0 identity/grammatical detectors (L0:F10155 group-membership, L0:F11154 "are", L0:F11668 baseball, L0:F1847 scientific terms) → L2 affix features (F2123 "-ian", F1680 "Canadians/consumers", F5368 legal trouble) → L3 keyword features (F13473 racial/ethnic group mentions, F4852 "abuse") → L4–L5 abuse/violence rhetoric (F148 abuse, F3229 assault, F8793 strong opinion) → L6 F10545 race-politics detector → probe.

**Verdict on the user's concern:** The concern is substantially confirmed. The probe leans heavily on identity-presence features (the word "Indians", an L0 feature nominally about baseball, an L2 feature about "-ian" nationality words, and an L3 feature for racial/ethnic group mentions) plus generic grammatical features ("is"/"are") to fire its toxic score. While genuine abuse-related features (L3:F4852, L4:F148) do contribute, the identity-group signal — including a clearly spurious baseball feature and a generic grammar scaffold — is a substantial component of the classification. This means the probe would likely also score benign sentences about Indians or any group as toxic whenever copular grammar appears, illustrating the very kind of identity-based shortcut the user suspected.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F10155](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10155) | 1 | Generic identity / nationality detectors (L0) |  words related to membership in a group | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10155) |
| [L0:F11154](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11154) | 2 | Generic identity / nationality detectors (L0) |  the word "are" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11154) |
| [L0:F11668](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11668) | 1 | Generic identity / nationality detectors (L0) |  Baseball terminology | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11668) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 7 | Generic identity / nationality detectors (L0) |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 8 | Generic identity / nationality detectors (L0) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F3498](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) | 5 | Generic identity / nationality detectors (L0) |  the pronoun "they" or its possessive form. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) |
| [L0:F8381](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8381) | 23 | Generic identity / nationality detectors (L0) |  the word 'by' | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8381) |
| [L0:F1847](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1847) | 3 | Generic identity / nationality detectors (L0) | scientific terms and experimental details related to biological and chemical research | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1847) |
| [L0:F11835](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11835) | 3 | Generic identity / nationality detectors (L0) | terms used in software code such as "assembly", "using", "namespace", and "license" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11835) |
| [L2:F2123](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2123) | 1 | Affix detectors (L2) |  words ending in "ian", "jani", "iti", "ino", or "olan" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2123) |
| [L2:F1680](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1680) | 1 | Affix detectors (L2) |  words that refer to people participating in some activity, such as consumers, patients in healthcare, or voters | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1680) |
| [L2:F5368](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5368) | 3 | Affix detectors (L2) |  words related to legal trouble and crime | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5368) |
| [L2:F11475](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11475) | 2 | Affix detectors (L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11475) |
| [L2:F15369](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15369) | 2 | Affix detectors (L2) |  the verb "are" and also words from German | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15369) |
| [L3:F13473](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13473) | 2 | Content keyword features (L3) |  mentions of racial and ethnic groups, especially in the United States | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13473) |
| [L3:F4852](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4852) | 3 | Content keyword features (L3) | the term "abuse." | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4852) |
| [L3:F4327](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4327) | 3 | Content keyword features (L3) | words and phrases that end with "ive", and also a few words that end in "ices" or "ishes", and also the phrase "advantage of the". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4327) |
| [L3:F9646](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9646) | 2 | Content keyword features (L3) | verbs and associated nouns. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9646) |
| [L3:F14281](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14281) | 18 | Content keyword features (L3) |  questions about how to do things, and some French words | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14281) |
| [L3:F5853](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5853) | 7 | Content keyword features (L3) |  instances of people speaking and making statements | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5853) |
| [L4:F148](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/148) | 3 | Abuse/violence/racial rhetoric (L4-L5) |  words and phrases related to sexual assault and abuse | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/148) |
| [L5:F3229](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3229) | 3 | Abuse/violence/racial rhetoric (L4-L5) |  words related to violent assault and murder | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3229) |
| [L5:F8793](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/8793) | 3 | Abuse/violence/racial rhetoric (L4-L5) |  language expressing strong opinions or negativity, potentially related to political, social, or historical issues. | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/8793) |
| [L6:F10545](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10545) | 3 | Identity/race-political content detectors (L6) |  political rhetoric related to race, historical states, and government control | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10545) |
| [L6:F1600](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1600) | 12 | Identity/race-political content detectors (L6) |  negative words and phrases related to problems and imperfections | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1600) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:11375 de=0.221 |
| 3 | `inspect_feature` ×6 | L0:11375, L0:11668, L3:14281, L0:11154, L6:10545, L3:13473 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F11375@8` | ❌ error | — | — | Trace from L0:F11375 (the word "is") at pos 8. Determine what drives this featur… |
| SA-2 | `L0:F11668@1` | ❌ error | — | — | Trace from L0:F11668 (baseball terminology) at pos 1. This appears spurious — in… |
| SA-3 | `L3:F13473@2` | ❌ error | — | — | Trace from L3:F13473 ("mentions of racial and ethnic groups, especially in the U… |
| SA-4 | `L6:F10545@3` | ❌ error | — | — | Trace from L6:F10545 ("political rhetoric related to race, historical states, go… |
| SA-5 | `L3:F14281@18` | ❌ error | — | — | Trace from L3:F14281 (French "comment" + how-to questions) at pos 18. This appea… |
| SA-6 | `L0:F11154@2` | ❌ error | — | — | Trace from L0:F11154 (the word "are") at pos 2. Investigate whether this is a ge… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F11375@8, k=10 → Emb:" is"@8 (de=32.50) +9 more |
| 2 | `get_upstream_features` | L0:F11668@1, k=10 → Emb:"Indians"@1 (de=12.38) +9 more |
| 3 | `get_upstream_features` | L3:F13473@2, k=10 → Emb:"Indians"@1 (de=10.25) +9 more |
| 4 | `get_upstream_features` | L6:F10545@3, k=10 → Emb:" abusers"@3 (de=1.90) +9 more |
| 5 | `get_upstream_features` | L3:F14281@18, k=10 → Emb:" how"@17 (de=31.38) +9 more |
| 6 | `get_upstream_features` | L2:F2123@1, k=10 → Emb:"Indians"@1 (de=17.12) +9 more |
| 7 | `get_upstream_features` | L2:F2123@2, k=5 → ❌ Feature (layer=2, feature_idx=2123) not found at pos=2. This |
| 8 | `inspect_feature` ×5 | L4:148, L5:8793, L0:1847, L2:5368, L2:2123 |
| 9 | `get_upstream_features` | L3:F9646@2, k=8 → Emb:"Indians"@1 (de=3.97) +7 more |
| 10 | `get_upstream_features` | L3:F13473@3, k=15 → ❌ Feature (layer=3, feature_idx=13473) not found at pos=3. Thi |
| 11 | `get_upstream_features` | L3:F4327@3, k=8 → Emb:" abusers"@3 (de=12.75) +7 more |
| 12 | `inspect_feature` ×5 | L2:1680, L2:15369, L3:4327, L0:8381, L0:3436 |
| 13 | `get_upstream_features` | L4:F148@3, k=8 → Emb:" abusers"@3 (de=19.12) +7 more |
| 14 | `get_upstream_features` | L2:F5368@3, k=8 → Emb:" abusers"@3 (de=9.00) +7 more |
| 15 | `get_upstream_features` | L2:F1680@1, k=5 → Emb:"Indians"@1 (de=8.56) +4 more |
| 16 | `get_upstream_features` | L2:F11475@2, k=5 → Emb:" are"@2 (de=5.00) +4 more |
| 17 | `inspect_feature` ×4 | L0:11835, L0:10155, L0:8796, L3:9646 |
| 18 | `get_upstream_features` | L3:F4852@3, k=5 → Emb:" abusers"@3 (de=9.25) +4 more |
| 19 | `inspect_feature` | L3, F4852 → "the term "abuse."" |
| 20 | `get_upstream_features` | L6:F1600@12, k=5 → Emb:" problems"@12 (de=21.25) +4 more |
| 21 | `inspect_feature` ×4 | L6:1600, L0:3498, L3:5853, L5:3229 |
| 22 | `get_upstream_features` | L0:F11835@3, k=5 → Emb:" abusers"@3 (de=7.09) +4 more |
| 23 | `get_upstream_features` | L2:F1680@1, k=5 → Emb:"Indians"@1 (de=8.56) +4 more |
| 24 | `get_upstream_features` | L0:F11668@1, k=5 → Emb:"Indians"@1 (de=12.38) +4 more |

### Build

`build_circuit` → 13 nodes, 14 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 68,026 | 5,992 | 320,549 | 0 | $0.0468 | — | — |
| **Total** | | **68,026** | **5,992** | **320,549** | **0** | **$0.0468** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 53s