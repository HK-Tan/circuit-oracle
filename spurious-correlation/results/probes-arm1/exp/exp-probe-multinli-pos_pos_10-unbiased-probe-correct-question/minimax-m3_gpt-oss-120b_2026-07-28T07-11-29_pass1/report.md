# Circuit Oracle Report
**Date:** 2026-07-28 07:11:29 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_10 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** This probe classifies the pair as contradiction, and the circuit is driven primarily by two cheap, surface-level shortcuts — the presence of the word **"not"** in the second sentence and the superlative **"strangest"** in the first — with a secondary boost from lexical role/reversal cues, rather than by any deep semantic comparison of the two sentences' content.

**Confidence:** 8

**Reasoning:**

The probe direction (layer 26) is fed by three positive supernodes and one negative supernode:

1. **Negation supernode (`neg_features`, L10–L12, total direct effect ≈ +0.66).** The top single features on the probe are L10:F6670 (pos 19, +0.275) and L12:F12606 (pos 19/21, +0.213). Tracing upstream shows both are essentially "negation detectors": F6670's strongest upstream is the embedding of **"not"** (pos 17, direct effect +6.78), and it aggregates L4:F4492 (multilingual negations) and L3:F8011 (negation tokens, top promoted "not"). F12606 is even more explicit — its three largest drivers are the embeddings of **"not"** (+6.56), **"<bos>"** (+3.41), and **"on"** (+3.06), with no content-word from sentence 1 in the top 4. L9:F14687 ("not… because/but") also fires on pos 21. So the second sentence's negation word is doing the bulk of the late-layer work, with **zero contribution from the actual semantic content** of sentence 1.

2. **Role-reversal supernode (`role_reversal_features`, L0–L8, ≈ +0.55 net).** L6:F12420 (pos 4, "conventions/role reversal") is driven by the embeddings of **"role"** (+5.59) and **"reversal"** (+0.43), reinforced by L4:F14368 (role/importance, embedding "role" +12.3) and L4:F7409 (reverse/inverse, embedding "reversal"). L7:F905 (amounts/changes, +6.88 from "reversal") and L8:F16033 (reversal/irony, +13 from "reversal") encode the same lexical signal. L0:F6013 and L0:F6902 fire on the bare "role" token (+15.6 and +15.1). These features fire on the surface words of sentence 1, not on any inferred semantic content.

3. **Strangest/superlative supernode (`superlative_features`, L2–L4, ≈ +0.30 net).** L4:F12799 (pos 2, direct effect +0.30) is the "-ly / oddities" feature, and its dominant driver is the embedding of **"strangest"** (+31.0). Upstream, L2:F16097 (-est superlatives, +24 from "strangest"), L2:F10827 (interesting/intriguing, +10.9 from "strangest"), and L3:F319 (comparative/superlative suffix) all fire on the morphology of the same single word.

4. **Inhibit supernode (`inhibit_features`, L0–L7, ≈ -1.0 net, but dominated by label noise).** The strong-negative features are L4:F5709 ("astronomy terms," pos 9, −0.37), L6:F12420-pos-4 (here firing on the *other* sense, −0.34), and L2:F16097 (−0.28). L4:F6072 is dominated by the embedding of **"now"** (+49.75) — a pure function-word. L0:F6051 is the literal period token (embedding "." +46.25) at pos 14. L2:F10705 fires on **"concerns"** (pos 11, +25.75). These are clearly context-irrelevant: an astronomy/now/period feature cannot be a legitimate contradiction signal, and the fact that it acts as the *largest* negative counterweight confirms the probe is latching on token-level statistics rather than meaning.

**Net picture:** The probe fires for contradiction because it sees (a) a "strange/superlative" token in the premise, (b) "role reversal" lexical tokens in the premise, and (c) a "not" token in the hypothesis — three surface cues that trivially co-occur with contradiction in training data. The **content-bearing premise tokens** ("democracy," "concerns") and the **syntactic cue** "." do *not* drive the positive score; they ride the inhibit supernode with multi-purpose, off-target features (astronomy, now, period). The user's concern is correct: the circuit is not reading the sentences; it is keying on **"not" in the hypothesis** and on **oddness + role-reversal vocabulary in the premise** as a contradiction shortcut.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L10:F6670](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) | 19 | Late-layer negation & technical-term features (push probe positive) | technical terms, especially within scientific or medical contexts | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) |
| [L12:F12606](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) | 21 | Late-layer negation & technical-term features (push probe positive) | phrases related to political conspiracy/organizations, mental conditions and storytelling terms | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) |
| [L12:F12606](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) | 19 | Late-layer negation & technical-term features (push probe positive) | phrases related to political conspiracy/organizations, mental conditions and storytelling terms | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) |
| [L6:F12420](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12420) | 4 | Role-reversal / change / roles semantic features (push probe positive) |  artistic elements that break established guidelines | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12420) |
| [L4:F14368](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14368) | 4 | Role-reversal / change / roles semantic features (push probe positive) | words related to importance or roles in a system | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14368) |
| [L7:F905](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/905) | 4 | Role-reversal / change / roles semantic features (push probe positive) | words indicating amounts, changes, or trends | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/905) |
| [L8:F16033](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16033) | 4 | Role-reversal / change / roles semantic features (push probe positive) | figurative language related to reversals of fortune | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16033) |
| [L4:F7409](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7409) | 4 | Role-reversal / change / roles semantic features (push probe positive) | words like "vice versa", "inverse", "reverse", "around", or directions | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7409) |
| [L0:F6013](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6013) | 3 | Role-reversal / change / roles semantic features (push probe positive) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6013) |
| [L0:F6902](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6902) | 3 | Role-reversal / change / roles semantic features (push probe positive) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6902) |
| [L4:F12799](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12799) | 2 | Strangest / -est / oddness features (push probe positive) |  words ending in "-ly" along with phrases that contain the word 'odd' or 'oddities' | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12799) |
| [L2:F16097](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) | 2 | Strangest / -est / oddness features (push probe positive) | superlative adjectives and the words "test" or "point" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) |
| [L2:F10827](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10827) | 2 | Strangest / -est / oddness features (push probe positive) | words that reflect strikingness or emotional impact | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10827) |
| [L3:F319](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/319) | 2 | Strangest / -est / oddness features (push probe positive) | words ending in the suffix "-est" or "-ier" (the superlative and comparative suffixes). | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/319) |
| [L3:F12079](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) | 17 | Mid/low-layer negation detectors (not/not_in) | negations and Chinese names | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 17 | Mid/low-layer negation detectors (not/not_in) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 17 | Mid/low-layer negation detectors (not/not_in) | a mix of words and code fragments from different languages | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 17 | Mid/low-layer negation detectors (not/not_in) | the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L9:F14687](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/14687) | 21 | Mid/low-layer negation detectors (not/not_in) | phrases using the word "not", often followed by "because" or "but." | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/14687) |
| [L4:F5709](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) | 9 | Mixed multi-meaning features (push probe negative, weaker) | astronomy terms | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) |
| [L4:F6072](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6072) | 9 | Mixed multi-meaning features (push probe negative, weaker) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6072) |
| [L0:F5188](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5188) | 9 | Mixed multi-meaning features (push probe negative, weaker) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5188) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 14 | Mixed multi-meaning features (push probe negative, weaker) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L2:F10705](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10705) | 11 | Mixed multi-meaning features (push probe negative, weaker) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10705) |
| [L2:F9872](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9872) | 2 | Mixed multi-meaning features (push probe negative, weaker) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9872) |
| [L7:F4526](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4526) | 4 | Mixed multi-meaning features (push probe negative, weaker) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4526) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:5709 de=-0.371 |
| 3 | `inspect_feature` ×4 | L4:5709, L6:12420, L4:12799, L2:16097 |

### Dispatch: 11 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F5709@9` | ❌ error | — | — | Trace L4:F5709 (at pos 9). What input tokens does this feature connect to? Is th… |
| SA-2 | `L4:F12799@2` | ✅ reported | 5 | 8 | Trace L4:F12799 (at pos 2). This is a -ly / 'strangest' / 'oddly' word feature. … |
| SA-3 | `L6:F12420@4` | ✅ reported | 6 | 8 | Trace L6:F12420 (at pos 4). This seems to encode 'roles' / 'conventions' / 'role… |
| SA-4 | `L2:F16097@2` | ❌ error | — | — | Trace L2:F16097 (at pos 2). This is a superlative feature ('-est' endings). Find… |
| SA-5 | `L3:F12079@17` | ✅ reported | 3 | 6 | Trace L3:F12079 at pos 17. This is one of the highest direct-effect positive fea… |
| SA-6 | `L10:F6670@19` | ✅ reported | 5 | 10 | Trace L10:F6670 at pos 19. This is a high direct-effect positive feature (+0.275… |
| SA-7 | `L12:F12606@21` | ✅ reported | 3 | 8 | Trace L12:F12606 at pos 21. High direct-effect positive feature (+0.2129). What … |
| SA-8 | `L4:F6072@9` | ❌ error | — | — | Trace L4:F6072 at pos 9. Direct effect +0.248. What does it encode and what inpu… |
| SA-9 | `L0:F6013@3` | ❌ error | — | — | Trace L0:F6013 at pos 3. Direct effect +0.22. What does this early-layer feature… |
| SA-10 | `L8:F16033@4` | ✅ reported | 3 | 5 | Trace L8:F16033 at pos 4. Direct effect +0.216. What does it encode and what inp… |
| SA-11 | `L7:F905@4` | ✅ reported | 5 | 7 | Trace L7:F905 at pos 4. Direct effect +0.223. What does it encode and what input… |

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F12799 | " words ending in "-ly" along with phrases that contain the word 'odd' " |
| 2 | `get_upstream_features` | L4:F12799@2, k=10 | Emb:" strangest"@2 (de=31.00) +9 more |
| 3 | `inspect_feature` | L2, F10827 | " words that reflect strikingness or emotional impact" |
| 4 | `inspect_feature` | L2, F16097 | "superlative adjectives and the words "test" or "point"" |
| 5 | `get_upstream_features` | L2:F10827@2, k=10 | Emb:" strangest"@2 (de=10.94) +9 more |
| 6 | `get_upstream_features` | L2:F10827@2, k=10 | Emb:" strangest"@2 (de=10.94) +9 more |
| 7 | `inspect_feature` | L3, F319 | " words ending in the suffix "-est" or "-ier" (the superlative and comp" |
| 8 | `inspect_feature` | L2, F3565 | " adjectives describing how often something happens" |
| 9 | `inspect_feature` | L0, F12381 | " the words "lowest" and "highest"" |
| 10 | `get_upstream_features` | L0:F12381@2, k=10 | Emb:" strangest"@2 (de=11.06) +9 more |
| 11 | `get_upstream_features` | L2:F16097@2, k=10 | Emb:" strangest"@2 (de=24.00) +9 more |
| 12 | `get_upstream_features` | L3:F319@2, k=10 | Emb:" strangest"@2 (de=18.88) +9 more |

**Findings:** The target feature L4:F12799 (pos2) is driven primarily by the input token 'strangest' which directly excites it (direct_effect 31.0). Upstream, the signal passes through a cascade of lower‑layer features that detect superlative morphology: L3:319 identifies the -est suffix, L2:16097 and L2:10827 capture superlative and striking adjectives, and L0:12381 supplies an early extremal adjective cue. Al…

</details>

<details>
<summary><b>SA-3</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F12420 | " artistic elements that break established guidelines" |
| 2 | `get_upstream_features` | L6:F12420@4, k=10 | Emb:" role"@3 (de=5.59) +9 more |
| 3 | `inspect_feature` | L4, F14368 | " words related to importance or roles in a system" |
| 4 | `inspect_feature` | L5, F9068 | "words and phrases related to populations" |
| 5 | `get_upstream_features` | L4:F14368@4, k=10 | Emb:" role"@3 (de=12.31) +9 more |
| 6 | `get_upstream_features` | L5:F9068@4, k=10 | Emb:" reversal"@4 (de=3.00) +9 more |
| 7 | `inspect_feature` | L1, F2580 | "the word "reverse" in code snippets" |
| 8 | `inspect_feature` | L4, F7409 | " words like "vice versa", "inverse", "reverse", "around", or direction" |
| 9 | `get_upstream_features` | L1:F2580@4, k=10 | Emb:" reversal"@4 (de=16.75) +9 more |
| 10 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |

**Findings:** The target L6:F12420 (pos 4) is a high‑level semantic node that fires on the idea of ‘conventions’ and ‘role reversal’. Its strongest positive drivers are the input token embeddings for the words \u2581role (pos 3) and \u2581reversal (pos 4), which directly push the node’s activation. Intermediate features that amplify this signal include L4:F14368 (a role‑importance detector) and L5:F9068 (a popu…

</details>

<details>
<summary><b>SA-5</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F12079 | "negations and Chinese names" |
| 2 | `get_upstream_features` | L3:F12079@17, k=10 | Emb:" There"@15 (de=15.00) +9 more |
| 3 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 4 | `get_upstream_features` | L0:F4958@17, k=10 | Emb:" not"@17 (de=32.75) +9 more |
| 5 | `inspect_feature` | L2, F12021 | ""not" or negative terms, with some bonus for sports-related terms and " |
| 6 | `inspect_feature` | L2, F7550 | " comparative adjectives and adverbs" |
| 7 | `get_upstream_features` | L2:F12021@17, k=10 | Emb:" not"@17 (de=22.62) +9 more |

**Findings:** The L3:F12079 feature is driven primarily by the input token "not" at position 17 (direct_effect 6.22) and also receives a strong boost from the preceding token "There" (direct_effect 15.0). The main upstream source is the layer‑0 feature 4958, which itself is almost entirely excited by the "not" embedding (direct_effect 32.75). A secondary upstream path goes through layer‑2 feature 12021, also st…

</details>

<details>
<summary><b>SA-6</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L10, F6670 | "technical terms, especially within scientific or medical contexts" |
| 2 | `get_upstream_features` | L10:F6670@19, k=10 | Emb:" not"@17 (de=6.78) +9 more |
| 3 | `inspect_feature` | L4, F4492 | "negations in various languages" |
| 4 | `inspect_feature` | L9, F742 | "negation, uncertainty, or sensory statements" |
| 5 | `get_upstream_features` | L4:F4492@17, k=10 | Emb:" not"@17 (de=18.00) +9 more |
| 6 | `inspect_feature` | L3, F8011 | " a mix of words and code fragments from different languages" |
| 7 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 8 | `get_upstream_features` | L3:F8011@17, k=10 | Emb:" not"@17 (de=21.00) +9 more |

**Findings:** The target feature L10:F6670 (a technical‑term detector) receives a strong excitatory signal from a cascade of negation detectors. The most influential upstream node is the raw embedding of the word "not" (pos 17), which feeds directly into L10:F6670 (+6.78) and also into earlier negation‑focused features L3:F8011 (+21) and L4:F4492 (+18). Both L3:F8011 and L4:F4492 are specialized negation detect…

</details>

<details>
<summary><b>SA-7</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F12606 | " phrases related to political conspiracy/organizations, mental conditi" |
| 2 | `get_upstream_features` | L12:F12606@21, k=10 | Emb:" not"@17 (de=6.56) +9 more |
| 3 | `inspect_feature` | L4, F4492 | "negations in various languages" |
| 4 | `get_upstream_features` | L4:F4492@17, k=10 | Emb:" not"@17 (de=18.00) +9 more |
| 5 | `inspect_feature` | L9, F14687 | "phrases using the word "not", often followed by "because" or "but."" |
| 6 | `get_upstream_features` | L9:F14687@21, k=10 | Emb:" not"@17 (de=10.88) +9 more |
| 7 | `inspect_feature` | L3, F8011 | " a mix of words and code fragments from different languages" |

**Findings:** L12:F12606 is a higher‑level composite that aggregates negation signals. Its strongest upstream drivers are the literal token " not" (pos 17) and a low‑layer multilingual negation detector (L4:F4492). Both upstream sources are pure embedding contributions with large positive direct effects, satisfying the requirement to reach a lower‑third layer feature and an embedding node. The presence of " not…

</details>

<details>
<summary><b>SA-10</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L8, F16033 | " figurative language related to reversals of fortune" |
| 2 | `get_upstream_features` | L8:F16033@4, k=10 | Emb:" reversal"@4 (de=13.00) +9 more |
| 3 | `inspect_feature` | L4, F7409 | " words like "vice versa", "inverse", "reverse", "around", or direction" |
| 4 | `inspect_feature` | L6, F12420 | " artistic elements that break established guidelines" |
| 5 | `get_upstream_features` | L4:F7409@4, k=10 | Emb:" reversal"@4 (de=25.75) +9 more |
| 6 | `inspect_feature` | L7, F11459 | " sentences where someone is metaphorically putting themselves in anoth" |
| 7 | `get_upstream_features` | L6:F12420@4, k=10 | Emb:" role"@3 (de=5.59) +9 more |
| 8 | `inspect_feature` | L2, F3690 | " words related to collaboration or separation, in technical contexts." |
| 9 | `inspect_feature` | L6, F2743 | " scientific terms and phrases related to symmetry and equivalence" |
| 10 | `inspect_feature` | L1, F1382 | " words associated with situations where something is changing or has c" |
| 11 | `get_upstream_features` | L2:F3690@4, k=10 | Emb:" reversal"@4 (de=10.69) +9 more |
| 12 | `inspect_feature` | L5, F9068 | "words and phrases related to populations" |

**Findings:** The target feature L8:F16033 fires strongly when the prompt contains language about reversal or turning (e.g., "turn", "reversed", "ironic"). Its strongest upstream drivers are the raw token embedding for the word "reversal" (direct effect 13.0) and the token "role" (direct effect ~3.9). At the intermediate layer, feature L4:F7409 captures explicit reversal words like "vice versa" and "inverse" an…

</details>

<details>
<summary><b>SA-11</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F905 | " words indicating amounts, changes, or trends" |
| 2 | `get_upstream_features` | L7:F905@4, k=10 | Emb:" reversal"@4 (de=6.88) +9 more |
| 3 | `inspect_feature` | L5, F11495 | " the word "turn" in various conjugations and contexts" |
| 4 | `inspect_feature` | L5, F5175 | " the phrase "how times have changed" and another more diffuse phrase l" |
| 5 | `inspect_feature` | L4, F9851 | " words related to altering a situation" |
| 6 | `get_upstream_features` | L5:F11495@4, k=10 | Emb:" reversal"@4 (de=9.19) +9 more |
| 7 | `inspect_feature` | L6, F2743 | " scientific terms and phrases related to symmetry and equivalence" |
| 8 | `get_upstream_features` | L5:F11495@4, k=10 | Emb:" reversal"@4 (de=9.19) +9 more |
| 9 | `inspect_feature` | L5, F5175 | " the phrase "how times have changed" and another more diffuse phrase l" |
| 10 | `get_upstream_features` | L5:F5175@4, k=10 | Emb:" role"@3 (de=1.54) +9 more |
| 11 | `inspect_feature` | L4, F14706 | " words related to math, dance, and politics" |

**Findings:** L7:F905 encodes quantitative/change language and is chiefly driven by the input token "reversal" at position 4 (direct_effect +6.875). Additional weaker influences come from other tokens ("strangest", "The") and from higher-layer features that themselves detect turning, explicit change phrases, and alteration. All upstream paths terminate in embeddings, satisfying the required lower-layer and embe…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F6072@9, k=10 → Emb:" now"@9 (de=49.75) +9 more |
| 2 | `get_upstream_features` | L0:F6013@3, k=10 → Emb:" role"@3 (de=15.56) +9 more |
| 3 | `get_upstream_features` | L2:F10705@11, k=10 → Emb:" concerns"@11 (de=25.75) +9 more |
| 4 | `get_upstream_features` | L0:F6051@14, k=10 → Emb:"."@14 (de=46.25) +9 more |
| 5 | `get_upstream_features` | L0:F6902@3, k=10 → Emb:" role"@3 (de=15.06) +9 more |
| 6 | `get_upstream_features` | L0:F5188@9, k=10 → Emb:" now"@9 (de=15.94) +9 more |

### Build

`build_circuit` → 14 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 22,219 | 5,464 | 89,519 | 0 | $0.0186 | — | — |
| SA-5 | openai/gpt-oss-120b | 52,255 | 4,119 | 14,816 | 0 | $0.0105 | ✅ 3F/6E | Trace L3:F12079 at pos 17. This is one of the highest direct… |
| SA-2 | openai/gpt-oss-120b | 153,436 | 7,628 | 352 | 0 | $0.0276 | ✅ 5F/8E | Trace L4:F12799 (at pos 2). This is a -ly / 'strangest' / 'o… |
| SA-3 | openai/gpt-oss-120b | 125,661 | 9,869 | 7,776 | 0 | $0.0249 | ✅ 6F/8E | Trace L6:F12420 (at pos 4). This seems to encode 'roles' / '… |
| SA-7 | openai/gpt-oss-120b | 54,629 | 4,058 | 12,672 | 0 | $0.0108 | ✅ 3F/8E | Trace L12:F12606 at pos 21. High direct-effect positive feat… |
| SA-11 | openai/gpt-oss-120b | 150,431 | 9,886 | 12,704 | 0 | $0.0287 | ✅ 5F/7E | Trace L7:F905 at pos 4. Direct effect +0.223. What does it e… |
| SA-10 | openai/gpt-oss-120b | 147,337 | 7,950 | 15,168 | 0 | $0.0271 | ✅ 3F/5E | Trace L8:F16033 at pos 4. Direct effect +0.216. What does it… |
| SA-6 | openai/gpt-oss-120b | 87,482 | 8,290 | 17,696 | 0 | $0.0184 | ✅ 5F/10E | Trace L10:F6670 at pos 19. This is a high direct-effect posi… |
| **Total** | | **793,450** | **57,264** | **170,703** | **0** | **$0.1666** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 20s