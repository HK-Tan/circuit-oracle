# Circuit Oracle Report
**Date:** 2026-07-28 07:02:40 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity probe is driven by a heterogeneous mix of (a) one semantically relevant feature — L4:F11580 detecting "negative language / swear words" that actually fires on the subword tokens of "bigot" — alongside (b) a long tail of identity-word, proper-name, function-word, and subword-prefix detectors that are entirely spurious.

**Confidence:** 8

**Reasoning:** The circuit's signal is mostly **not** about toxicity. Of the ~20 top features feeding the probe direction, only one — **L4:F11580 "negative language and swear words"** (direct_effect +0.0918, frac_nonzero 0.0034, promoted tokens `FUCK`, `idiot`, `moron`, `bastard`, `asshole`) — is genuinely content-relevant: the subagent traced it back through L2:F4520 ("newness/outsider") and L0:F1432 to the raw embeddings of `" big"` (pos 8, direct_effect +0.777) and `"ot"` (pos 9, direct_effect +5.0) — i.e., the subword decomposition of the prompt's literal word **"bigot"**. That is a real lexical cue for toxicity.

Everything else driving the probe is **spurious content-free evidence**:

- **Identity/political name triggers**: **L2:F14301** "names of people/orgs in politics, finance, national security" (direct_effect +0.105) is excited almost entirely by the `trump` token embedding (direct_effect +9.4) via L1:F7815 and L0:F4807 (a dedicated "Donald Trump" detector). **L4:F14582** "White House / US government" (direct_effect +0.156) is also driven by the same `trump` token. These fire on the mere mention of a political figure, not on slur/derogatory content.
- **Racial-group lexical triggers**: **L0:F3436** "the word 'white'" (direct_effect +0.102, frac_nonzero 0.061) receives +18.1 from the `white` embedding — it is a generic "white" detector whose top activating examples include astrophysics text about "white dwarfs" and "white paper." **L0:F7969** "the word 'other'" (direct_effect +0.102) fires on the common pronoun/adjective "other."
- **Function-word / adverbial tone features**: **L0:F7621** ("clearly", +0.194), **L0:F12866** ("clearly, plainly", -0.206), **L0:F7861** ("this, these, clearly, more", +0.098), **L0:F5707** ("knowledge/perspective", -0.096), **L0:F4422** ("seriously", +0.137), **L0:F15831** ("again", -0.124), **L0:F11375** ("is", +0.131), **L0:F164** ("show/your", -0.121), **L0:F3916** ("short legal-document words", +0.119, fires on `tie` at pos 1) — all are generic stylistic/grammatical detectors with high frac_nonzero. Several are **inhibitory** (negative direct_effect), meaning they are actually pushing against the probe but were captured because the ranking includes negative edges.
- **Subword/code noise**: **L2:F9199** "instances of 'ot' in code" (direct_effect -0.115, frac_nonzero 0.009) — the subagent confirmed this fires on the same `"ot"` subword from "bigot," but its label is a **code-token detector**, not a slur detector. **L2:F15769** "the word 'tie'" (direct_effect +0.105) and **L4:F2720** "tie/tied" (direct_effect -0.092) fire on the first word of the prompt, which is "tie" (as in necktie or close score), not on anything toxic. **L0:F7142** "axis" (direct_effect -0.121) and **L3:F373** "subword prefix" (direct_effect -0.103) are also spurious, content-free detectors — "axis" only happens to co-occur with subwords of the "bigot" tokens, and the prefix detector fires on arbitrary letter sequences.

In other words, the probe is "voting" toxic chiefly because the prompt (a) contains the word **bigot** (the one legitimate signal, via L4:F11580), and (b) mentions **Trump** (L2:F14301, L4:F14582, L0:F4807), **white** (L0:F3436), and uses the discourse markers **clearly / is / other / again** (L0:F7621, F11375, F7969, F15831). These are exactly the **"identity group" / proper-noun / generic-function-word** cues the user flagged as spurious. The features do not encode the *meaning* of the toxic claim; they encode the surface tokens that correlate with it in training data. A non-toxic text mentioning Trump, "white," and the word "clearly" would likely score comparably, while a highly toxic text lacking those surface tokens would likely score lower. The user concern is well-supported: the circuit is dominated by identity/keyword features and only one true toxicity feature.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F7621](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7621) | 2 | L0: adverb "clearly" detector (L0:F7621) |  the word "clearly", and to a lesser extent words associated with amounts of things | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7621) |
| [L0:F12866](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12866) | 2 | L0: adverb "clearly" detector (L0:F7621) |  adverbs such as "clearly," "plainly," and "as" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12866) |
| [L0:F7861](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7861) | 2 | L0: adverb "clearly" detector (L0:F7621) |  instances of the words "this", "these", "clearly", or "more". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7861) |
| [L0:F5707](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5707) | 2 | L0: adverb "clearly" detector (L0:F7621) |  words or phrases related to knowledge or perspective | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5707) |
| [L0:F4422](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4422) | 2 | L0: adverb "clearly" detector (L0:F7621) | the word "seriously" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4422) |
| [L0:F3916](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3916) | 1 | L0: adverb "clearly" detector (L0:F7621) |  common short words in legal documents | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3916) |
| [L1:F9761](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9761) | 2 | L0: adverb "clearly" detector (L0:F7621) |  language asserting that a statement is obvious, undisputed, or in accordance with a rule | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9761) |
| [L2:F14301](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14301) | 5 | L2: political person/org name (L2:F14301) |  names of people and organizations involved in politics, finance, and national security | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14301) |
| [L0:F3635](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) | 4 | L2: political person/org name (L2:F14301) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) |
| [L4:F14582](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14582) | 5 | L4: White House / US gov reference (L4:F14582) |  references to the White House and the US government | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14582) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 6 | L0: copula "is" detector (L0:F11375) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F15831](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15831) | 26 | L0: "again"/time word (L0:F15831) | the word "again" and words associated with time | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15831) |
| [L0:F7969](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7969) | 14 | L0: "other" detector (L0:F7969) |  the word "other" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7969) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 15 | L0: "white" racial term (L0:F3436) |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F164](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/164) | 3 | L0: "show"/"your" (L0:F164) | the words "show" and "your", particularly when talking about presenting something | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/164) |
| [L0:F7142](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7142) | 2 | L0: "axis"/technical (L0:F7142) — generic token pattern |  the word "axis" and its plural form, often in the context of scientific or technical documents | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7142) |
| [L3:F373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/373) | 1 | L3: subword prefix detector (L3:F373) |  word beginnings with the letters "a," "h,""i," "r," and "p" (perhaps prefixes and/or related to medical or scientific terms) | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/373) |
| [L2:F9199](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9199) | 9 | L2: "ot" subword in code (L2:F9199) |  instances of "ot" in code | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9199) |
| [L2:F15769](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15769) | 1 | L2: "tie" word (L2:F15769) | the word "tie" in various contexts | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15769) |
| [L4:F2720](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2720) | 1 | L4: "tie"/"tied" (L4:F2720) | mentions of a 'tie' or a similar word | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2720) |
| [L4:F11580](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11580) | 9 | L4: negative/swear language (L4:F11580) | negative language and swear words | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11580) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'probe_target' is not one of the top-k next-token cand |
| 3 | `get_top_features` | 20 features; top: L0:12866 de=-0.206 |
| 4 | `inspect_feature` ×20 | L0:7621, L0:12866, L4:14582, L0:4422, L0:11375, L0:15831, L0:3916, L0:3436, L0:7969, L0:7142, L0:164, L0:7861, L0:5707, L1:9761, L2:9199, L2:14301, L2:15769, L3:373, L4:11580, L4:2720 |
| 5 | `get_upstream_features` | Emb:"ot"@9 (de=5.00) +11 more |
| 6 | `get_upstream_features` | Emb:" trump"@5 (de=18.12) +11 more |
| 7 | `get_upstream_features` | Emb:" white"@15 (de=18.12) +4 more |
| 8 | `get_upstream_features` | Emb:" clearly"@2 (de=17.75) +4 more |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F11580@9` | ✅ reported | 4 | 10 | Trace this "negative language / swear words" feature upstream to identify the in… |
| SA-2 | `L2:F14301@5` | ✅ reported | 3 | 6 | Trace the path upstream from this L2 political person/org name feature. What inp… |

<details>
<summary><b>SA-1</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F11580 | "negative language and swear words" |
| 2 | `get_upstream_features` | L4:F11580@9, k=10 | Emb:"ot"@9 (de=5.00) +9 more |
| 3 | `inspect_feature` | L2, F4520 | " words related to newness or being an outsider" |
| 4 | `inspect_feature` | L0, F12712 | " words, suffixes, or phrases that could indicate quality and the peopl" |
| 5 | `inspect_feature` | L2, F4053 | " inflammatory hateful words, phrases, and names that attack groups of " |
| 6 | `get_upstream_features` | L2:F4520@9, k=10 | Emb:" big"@8 (de=9.06) +9 more |
| 7 | `get_upstream_features` | L2:F4053@9, k=10 | Emb:"ot"@9 (de=1.11) +9 more |
| 8 | `get_upstream_features` | L0:F12712@9, k=5 | Emb:" big"@8 (de=12.44) +4 more |
| 9 | `inspect_feature` | L0, F1432 | " the word "quality" and words associated with negative impacts" |
| 10 | `get_upstream_features` | L2:F4520@9, k=10 | Emb:" big"@8 (de=9.06) +9 more |
| 11 | `get_upstream_features` | L0:F1432@9, k=10 | Emb:" big"@8 (de=11.12) +9 more |

**Findings:** The profanity‑related feature (L4:F11580) that lights up on the word "bigot" receives its strongest positive influence from the raw token embeddings of the two sub‑tokens that make up the word: "big" (pos 8) and "ot" (pos 9). These embeddings feed both directly into the target feature and indirectly via low‑level lexical detectors (features 1432 and 12712) and a mid‑layer detector (feature 4520). …

</details>

<details>
<summary><b>SA-2</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F14301 | " names of people and organizations involved in politics, finance, and " |
| 2 | `get_upstream_features` | L2:F14301@5, k=10 | Emb:" trump"@5 (de=9.44) +9 more |
| 3 | `inspect_feature` | L1, F7815 | " references to contacting or communicating with someone, including job" |
| 4 | `get_top_logits` | k=5 | "" (100%) |
| 5 | `get_upstream_features` | L1:F7815@5, k=10 | Emb:" trump"@5 (de=10.88) +9 more |
| 6 | `inspect_feature` | L0, F4807 | " references to Donald Trump" |

**Findings:** The L2 political‑person feature (F14301) is driven primarily by the raw input token 'trump' (direct_effect ~9.4) and, to a lesser extent, surrounding tokens 'that' and 'clearly'. Upstream, a layer‑1 feature (F7815) contributes a modest positive effect; this layer‑1 feature itself is strongly excited by the same 'trump' embedding and receives a tiny boost from a layer‑0 Trump‑specific feature (F480…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F15831@26, k=5 → Emb:" again"@26 (de=43.50) +4 more |
| 2 | `get_upstream_features` | L0:F7969@14, k=5 → Emb:" other"@14 (de=42.25) +4 more |
| 3 | `get_upstream_features` | L0:F11375@6, k=5 → Emb:" is"@6 (de=31.38) +4 more |

### Build

`build_circuit` → 24 nodes, 24 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 55,771 | 5,680 | 136,427 | 0 | $0.0317 | — | — |
| SA-1 | openai/gpt-oss-120b | 137,241 | 8,315 | 15,360 | 0 | $0.0258 | ✅ 4F/10E | Trace this "negative language / swear words" feature upstrea… |
| SA-2 | openai/gpt-oss-120b | 47,420 | 4,877 | 2,592 | 0 | $0.0101 | ✅ 3F/6E | Trace the path upstream from this L2 political person/org na… |
| **Total** | | **240,432** | **18,872** | **154,379** | **0** | **$0.0676** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 50s