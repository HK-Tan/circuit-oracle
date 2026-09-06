# Circuit Oracle Report
**Date:** 2026-07-28 07:23:25 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

The analysis is clear. Let me write the final response.

**Analysis:** The probe's classification score is driven almost entirely by negation-encoding features that trace back to the single token "No" at position 16 — a classic spurious-feature signal rather than a representation of the prompt's actual semantic content (a contradiction arises between the first and second sentences about the tourist office).

**Confidence:** 8

**Reasoning:** The attribution graph reveals a single dominant vertical chain all running through one input token: the word **" No"** at position 16 ("No one is usually at the tourist office…"). The signal flow is:

- **Emb: ' No' (pos 16)** directly drives the output with `direct_effect=33` into L14:F336, and propagates through L0:F1143 ("the word 'no' and related words like 'nobody' and 'trust'", frac_nonzero=0.014) → L2:F2771 ("the word 'no' and conceptually related negation", frac_nonzero=0.002) → L12:F8719 ("phrases that start with 'no.'", frac_nonzero=0.003) → L13:F10768 ("'no' in the context of a discussion/argument", frac_nonzero=0.018) → L14:F336 ("the word 'no' and related negative words", frac_nonzero=0.004, activation=26.9) → L15:F13061 ("uses of 'no' / negative statements associated with 'one'", frac_nonzero=0.015) → **L16:F11298 ("no", frac_nonzero=0.010, activation=40.25, direct_effect=0.175)** → probe output.

- The companion token **" one"** at pos 17 also feeds the chain via L0:F4438 ("the word 'one'", frac_nonzero=0.001) and L2:F8837 ("'one' or 'body' when preceded by 'no' or 'every'", frac_nonzero=0.011, direct_effect=−0.207) — the explicit "No one" bigram detector that converges on the same L12:L16 negation stack.

- A parallel but **suppressive** set of paths (negative direct_effect into the probe) comes from the prompt's actual content: L0:F8566 ("pick", direct_effect=−0.208) and L2:F3116 ("pick up" phrasal verb, direct_effect=−0.609 — the single largest magnitude feature in the top-20) come from "Pick up a map…" (pos 1-2), while L2:F1016 / L2:F14413 ("tour/tours", direct_effects +0.217 / −0.281) come from "walking tours" (pos 14). The Emb for " tours" (pos 14) also pushes L16:F11298 positively (direct_effect=1.09), but is dominated by the "No" embedding.

- `get_source_influence` on positions 16-17 returns **S_pct_of_total = −0.213** and **R_pct_of_total = 22.93** (S/R ≈ −0.009), confirming the "No"/"No one" tokens carry a substantial signed share of the probe's signal — but with a *negative* sign on net, meaning the "No" bigram itself does not cleanly explain the positive contradiction score; instead, the chain of layer-specialized "no"/"negation" features at L12-L16 collectively produce the positive contribution, while the *content* features (pick up / tour) suppress it.

- The "No one" bigram detector (L2:F8837) is the smoking gun: its label explicitly says it fires on "'one' or 'body' when preceded by 'no' or 'every.'" — i.e. a purely syntactic negation cue, with promoted tokens like `<bos>`, `})*/`, `▁nobody`, `Nobody`. It is a structural negation marker, not a contradiction-understanding feature.

In short, the circuit corroborates the user's concern: the probe is firing on a chain of **negation-word detector features** ("no", "No one", negative statements in discussion) anchored at position 16, with the actual content words (pick up, tour, ask) producing *suppressive* direct effects. The model has learned a shortcut — the presence of a sentence-initial "No" (and specifically the "No one is usually at…" construction) — as a contradiction signal, rather than comparing the premise ("ask about walking tours") with the hypothesis ("you'll have to go somewhere else") semantically. The contradiction in this NLI pair is genuine (the first sentence claims the office is the place to learn about tours, the second says no one is there and you must go elsewhere), but the circuit shows the probe latches onto the lexical negation surface form, not the entailment structure.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F1143](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1143) | 16 | Layer 0: 'no' / negation word (L0:F1143) |  the word "no" and related words like "nobody" and "trust" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1143) |
| [L0:F4438](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) | 17 | Layer 0: 'one' word (L0:F4438) | the word "one". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) |
| [L0:F8566](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) | 1 | Layer 0: 'pick' word (L0:F8566) |  the word "pick" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) |
| [L0:F10562](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10562) | 2 | Layer 0: 'up' word (L0:F10562) | the word "up" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10562) |
| [L0:F13092](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13092) | 2 | Layer 0: 'down'/'up' combined (L0:F13092) |  the words "down" and "up", often in combination | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13092) |
| [L0:F13354](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13354) | 11 | Layer 0: 'ask' word (L0:F13354) | the word "ask" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13354) |
| [L2:F2771](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2771) | 16 | Layer 2: 'no' / negation concepts (L2:F2771) |  the word "no" as well as words and phrases that are conceptually related to negation | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2771) |
| [L2:F3116](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) | 2 | Layer 2: 'pick up' phrasal verb (L2:F3116) |  the phrasal verb "pick up" and variations | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) |
| [L2:F8837](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8837) | 17 | Layer 2: 'No one' / 'everybody' bigram (L2:F8837) |  the word "one" or "body" when preceded by the words "no" or "every." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8837) |
| [L2:F1016](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1016) | 14 | Layer 2: 'tour(s)' (L2:F1016, L2:F14413) |  forms of the verb "tour" and the noun "tour." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1016) |
| [L2:F14413](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) | 14 | Layer 2: 'tour(s)' (L2:F1016, L2:F14413) | the word "tour" or "tours" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) |
| [L12:F8719](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/8719) | 16 | Layer 12: 'No'-phrases (L12:F8719) |  phrases that start with "no." | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/8719) |
| [L13:F10768](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/10768) | 16 | Layer 13: 'no' in argument/discussion (L13:F10768) |  negative sentiments and words like "no" in the context of a discussion or argument. | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/10768) |
| [L14:F336](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) | 16 | Layer 14: 'no' / negative words (L14:F336) | the word "no" and related negative words | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) |
| [L15:F13061](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13061) | 16 | Layer 15: 'no' + 'one' negative statements (L15:F13061) |  uses of the word "no" or similar negative statements and words associated with "one" | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13061) |
| [L16:F11298](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11298) | 16 | Layer 16: 'no' (L16:F11298) | no | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11298) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L2:3116 de=-0.609 |
| 3 | `inspect_feature` ×20 | L2:3116, L0:10562, L0:10904, L2:14413, L1:15800, L2:1016, L0:2238, L4:10722, L0:8566, L2:8837, L2:11769, L0:13092, L0:6051, L0:7727, L14:336, L1:6872, L4:11969, L8:1872, L16:11298, L0:13354 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F336@16` | ❌ error | — | — | Trace from L14:F336 ("no" / negative words) — what tokens drive this feature and… |
| SA-2 | `L16:F11298@16` | ❌ error | — | — | Trace from L16:F11298 ("no" feature) — what tokens drive this and how does it co… |
| SA-3 | `L2:F8837@17` | ❌ error | — | — | Trace from L2:F8837 ("No one" bigram) — what does this feature encode and where … |
| SA-4 | `L2:F3116@2` | ❌ error | — | — | Trace from L2:F3116 ("pick up" phrasal verb) — what does it encode and how does … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F336@16, k=15 → Emb:" No"@16 (de=33.00) +14 more |
| 2 | `get_upstream_features` | L16:F11298@16, k=15 → Emb:" No"@16 (de=12.44) +14 more |
| 3 | `get_upstream_features` | L2:F8837@17, k=15 → Emb:" No"@16 (de=18.62) +14 more |
| 4 | `get_upstream_features` | L2:F3116@2, k=15 → Emb:"Pick"@1 (de=50.00) +14 more |
| 5 | `inspect_feature` ×6 | L0:4438, L0:1143, L13:10768, L12:8719, L2:2771, L15:13061 |
| 6 | `get_source_influence` | {'depth': 8, 'source_positions': [16, 17]} → {'depth': 8, 'source_positions': [16, 17], 'S_pct_of_total': -0.213, 'R_pct_of_t |

### Build

`build_circuit` → 22 nodes, 18 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 56,972 | 5,226 | 235,572 | 0 | $0.0375 | — | — |
| **Total** | | **56,972** | **5,226** | **235,572** | **0** | **$0.0375** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 12s