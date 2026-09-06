# Circuit Oracle Report
**Date:** 2026-07-28 07:24:49 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity score is driven by a sparse set of identity-token detectors at the word-embedding level — specifically " gay" (pos 17), " Muslim" (pos 12), " justice" (pos 6), " social" (pos 5) and " warrior" (pos 7) — with a negative " you" feature partially counteracting it; the circuit contains no features encoding the hostile intent, imperative structure, or the "go to a X bakery" scenario that actually makes the sentence toxic.

**Confidence:** 8/10

**Reasoning:** Tracing the top-15 features driving the probe reveals they are overwhelmingly anchored at the raw token embeddings of *identity-bearing* content words:

- **` gay` (pos 17)** is the single largest positive contributor. Its embedding directly drives L4:F8645 (direct_effect 22.9), L4:F15899 (21.1), L6:F6085 (37.0), and L8:F15771 (17.0), all of which sit on top of the ` gay` token and feed the output. None of these features required contextual composition with other tokens — they fire directly on the identity word itself.
- **` Muslim` (pos 12)** is the second major contributor. Its embedding drives L4:F2405 (15.8), L6:F7282 (22.6), and L3:F12024 (10.6). The "Muslim" features are pure identity-token detectors — L3:F12024 actually *suppresses* the probe (negative direct_effect), but L4:F2405 and L6:F7282 push strongly positive.
- **` justice` (pos 6) / ` social` (pos 5)** drive L1:F13646 (4.2 from ` justice`) → L4:F117 (5.1 from ` justice` embedding). L4:F117 is the prototypical "identity-group" feature the user warned about — it fires at positions 6, 7, AND 13 (i.e., on ` justice`, ` warrior`, and ` bakery`), all tokens that are part of the "social justice warrior / Muslim / gay wedding / cake" demographic-targeting cluster, regardless of which specific identity word is present.
- **` warrior` (pos 7)** drives L11:F1291 (24.5 activation), another late-layer identity-cluster detector.
- **Counter-signal:** L0:F7710 on ` you` (pos 2) is the strongest *negative* contributor (-0.28), followed by L0:F6764 and L0:F3215 on ` justice` (pos 6) — all low-layer pronoun/function-word features that mildly push *against* the probe.

Critically, the **lexical and semantic content of the toxicity itself** — the imperative "go to," the demand ordering a cake, the hostility toward the targeted group — is essentially absent from the high-direct-effect features. The directional "go to" feature (L3:F5959) has a *negative* direct_effect (-0.12) toward the probe. There is no feature encoding "refusal scenario," "anti-LGBTQ directive," or the hostile imperative structure. The probe's score is constructed almost entirely from:

1. Token-embedding-level identity detectors (` gay`, ` Muslim`, ` justice`, ` social`, ` warrior`)
2. A multi-position identity-cluster feature (L4:F117) that generalizes across identity tokens
3. Mild suppression from a pronoun feature (` you`)

This confirms the user's concern: the classifier is relying on **"identity group present"** as a proxy for toxicity rather than the sentence's actual hostile imperative. The model could achieve a similar probe score on a sentence like "Muslims, gay people, and social justice warriors deserve respect" — which would activate the same identity embeddings but in a non-toxic context — suggesting the probe is **spuriously correlated with demographic terminology** rather than with toxic intent. The circuit contains no counterfactual-checking features that would distinguish "celebrate identity groups" from "target identity groups with a hostile demand."

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L8:F15771](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) | 17 | 'gay' identity-group detector (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) |
| [L6:F6085](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) | 17 | 'gay' identity detector (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) |
| [L6:F7282](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) | 12 | 'Muslim' identity detector (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) |
| [L4:F2405](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) | 12 | Muslim-religion-context feature (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 6 | 'justice'/'social' identity-group feature (pos 6, fires 6,7,13) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 7 | 'justice'/'social' identity-group feature (pos 6, fires 6,7,13) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 13 | 'justice'/'social' identity-group feature (pos 6, fires 6,7,13) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L3:F5157](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5157) | 6 | 'social' adjective feature (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5157) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 13 | 'social' adjective feature (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L4:F8645](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8645) | 17 | 'gay' embedding-fed feature (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8645) |
| [L4:F15899](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) | 17 | 'gay' embedding-fed feature (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) |
| [L7:F16171](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/16171) | 17 | 'gay' late-layer feature (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/16171) |
| [L11:F1291](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/1291) | 7 | 'warrior' late-layer feature (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/1291) |
| [L1:F13646](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) | 6 | 'justice' early feature (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) |
| [L3:F5959](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5959) | 10 | 'go to' / directional feature (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5959) |
| [L3:F12024](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12024) | 12 | 'Muslim' negative-direction feature (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12024) |
| [L0:F7710](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) | 2 | Negative 'social justice' / pronoun L0 features (pos 2,6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) |
| [L0:F6764](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6764) | 6 | Negative 'social justice' / pronoun L0 features (pos 2,6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6764) |
| [L0:F3215](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3215) | 6 | Negative 'social justice' / pronoun L0 features (pos 2,6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3215) |
| [L0:F10421](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10421) | 6 | Positive 'social'/'justice' L0 features (pos 5,6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10421) |
| [L0:F7519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7519) | 6 | Positive 'social'/'justice' L0 features (pos 5,6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7519) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:6085 de=0.326 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F6085@17` | ❌ error | — | — | Trace from L6:F6085 at position 17 (the 'gay' token). Determine what this featur… |
| SA-2 | `L8:F15771@17` | ❌ error | — | — | Trace from L8:F15771 at position 17 (the 'gay' token). Determine what this featu… |
| SA-3 | `L4:F117@6` | ❌ error | — | — | Trace from L4:F117 at position 6 (the 'justice' token). This feature fires at mu… |
| SA-4 | `L4:F117@12` | ❌ error | — | — | Trace from L4:F117 at position 12 (the 'Muslim' token). Determine what this feat… |
| SA-5 | `L6:F7282@12` | ❌ error | — | — | Trace from L6:F7282 at position 12 (the 'Muslim' token). Determine what this fea… |
| SA-6 | `L0:F7710@2` | ❌ error | — | — | Trace from L0:F7710 at position 2 (the 'you' token). This is an L0 feature with … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F6085@17, k=10 → Emb:" gay"@17 (de=37.00) +9 more |
| 2 | `get_upstream_features` | L8:F15771@17, k=10 → Emb:" gay"@17 (de=17.00) +9 more |
| 3 | `get_upstream_features` | L4:F117@6, k=10 → Emb:" justice"@6 (de=5.12) +9 more |
| 4 | `get_upstream_features` | L6:F7282@12, k=10 → Emb:" Muslim"@12 (de=22.62) +9 more |
| 5 | `get_upstream_features` | L4:F8645@17, k=5 → Emb:" gay"@17 (de=22.88) +4 more |
| 6 | `get_upstream_features` | L4:F15899@17, k=5 → Emb:" gay"@17 (de=21.12) +4 more |
| 7 | `get_upstream_features` | L4:F2405@12, k=5 → Emb:" Muslim"@12 (de=15.75) +4 more |
| 8 | `get_upstream_features` | L3:F5157@6, k=5 → Emb:" social"@5 (de=24.12) +4 more |
| 9 | `get_upstream_features` | L1:F13646@6, k=5 → Emb:" justice"@6 (de=4.22) +4 more |
| 10 | `get_upstream_features` | L11:F1291@7, k=5 → L8:F16036 (de=4.00) +4 more |
| 11 | `get_upstream_features` | L3:F12024@12, k=5 → Emb:" Muslim"@12 (de=10.62) +4 more |
| 12 | `get_upstream_features` | L4:F117@7, k=5 → Emb:" justice"@6 (de=4.12) +4 more |
| 13 | `get_upstream_features` | L4:F117@13, k=5 → Emb:" Muslim"@12 (de=5.25) +4 more |
| 14 | `get_upstream_features` | L7:F16171@17, k=5 → L6:F6085 (de=5.72) +4 more |
| 15 | `get_upstream_features` | L8:F16036@7, k=5 → L7:F8154 (de=2.61) +4 more |
| 16 | `get_upstream_features` | L3:F5959@10, k=5 → Emb:" go"@9 (de=9.88) +4 more |
| 17 | `get_upstream_features` | L0:F10421@6, k=5 → Emb:" social"@5 (de=13.50) +4 more |
| 18 | `get_upstream_features` | L0:F7710@2, k=5 → Emb:" you"@2 (de=40.50) +4 more |
| 19 | `get_upstream_features` | L0:F6764@6, k=5 → Emb:" justice"@6 (de=14.38) +4 more |
| 20 | `get_upstream_features` | L0:F3215@6, k=5 → Emb:" social"@5 (de=7.94) +4 more |
| 21 | `get_upstream_features` | L0:F7519@6, k=5 → Emb:" justice"@6 (de=11.50) +4 more |

### Build

`build_circuit` → 24 nodes, 28 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 15,904 | 9,357 | 64,986 | 0 | $0.0199 | — | — |
| **Total** | | **15,904** | **9,357** | **64,986** | **0** | **$0.0199** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 47s