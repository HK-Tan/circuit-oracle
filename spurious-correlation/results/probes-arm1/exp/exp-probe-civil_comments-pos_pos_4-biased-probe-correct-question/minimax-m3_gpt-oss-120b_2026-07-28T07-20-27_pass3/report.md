# Circuit Oracle Report
**Date:** 2026-07-28 07:20:27 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity score is driven by a confluent signal that begins at the input token `Indians` (pos 1) and `abusers` (pos 3), passes through two parallel supernodes — a cluster of identity/nationality detectors (L3:13473 "racial and ethnic groups", L4:12975 "Asian countries", L6:1509 "countries and nationalities", L0:3283 "mentions of India", L0:14740 "names of places/people/orgs", L0:10155 "membership in a group", L0:9480 "named countries") and a cluster of `abuse`-lexical features (L2:1003, L2:6255, L4:5206, L4:4021) — and is integrated by a late-layer "public sentiment and action in response to a problem" feature (L7:15690) before being read out by the probe direction.

**Confidence:** 7

**Reasoning:** The user's concern is largely *not* confirmed as a clean bug, but it is partially correct and worth flagging:

1. **Identity-group signal is genuinely prominent.** The single token `Indians` (pos 1) directly drives several features whose labels are *purely* about identity/nationality groups, not about toxicity semantics: L0:3283 ("mentions of India"), L0:14740 (place/person/org names), L0:9480 (named countries), L6:1509 (countries/nationalities), L4:12975 (Asian countries), L3:13473 (racial/ethnic groups, frac_nonzero=0.006, very selective), and L0:10155 ("membership in a group", frac_nonzero=0.046, suppresses "skiers/golfers/feminists/gamers" — i.e., it flags a labeled group identity). These features fire on `Indians` *regardless* of what the surrounding text says. Upstream of L3:13473 the `Indians` embedding contributes direct_effect=10.25 and `are` contributes +5.28, confirming a strong ethnic-identity detection pathway that is independent of abuse content.

2. **Abuse content also matters, but in a generic way.** The `abusers` token (pos 3) feeds L2:1003 and L2:6255 (both literally "the word 'abuse'"). These are lexical — they fire on the word form, not on toxic intent. Combined with `Indians` they are exactly the pattern a toxicity probe has learned to key on.

3. **Late integration is mediated by a "public sentiment/action in response to a problem" feature (L7:15690, pos 3).** Its top upstream contributors are the `abusers` embedding (direct_effect=1.68) and the `Indians` embedding (1.23), with L4:5206, L0:10155 (group-membership), and L3:13473 (racial/ethnic groups, 0.34) also feeding it. So the final decision combines the identity signal and the abuse lexical.

4. **Spurious off-target features appear too.** L0:11668 (baseball, "innings"), L0:10389 (legal/technical "faults"), L0:3564 (mathematical notation), L1:7492 ("departments"), L0:4199 ("quantity"), L3:150 (verbs/past participles) and the pure function-word detectors L0:11154 ("are") and L0:1053 ("as") have small but nonzero direct_effect on the probe. These are generic, low-signal L0 noise that attribution graphs routinely include; they are not specific to this prompt.

**Verdict on the user concern:** The probe *does* use identity-group features as a positive driver — it is not purely content-based. However, the circuit is not a degenerate "group name → toxic" shortcut alone: it also requires the `abuse`/`abusers` token to fire the abuse-lexical features and the L7:15690 integrator. The probe is largely behaving as a bag-of-cues classifier over (identity group) + (abuse word), which is a *plausibly* correct pattern for the actual toxicity it was trained to detect, but it does mean a benign sentence that just *mentions* an identity group together with the word "abuse" (e.g., "Indians who experience abuse…") would score highly — the same conflation the user is flagging. This is an artifact of the probe's training data, not of the underlying model per se, but the model faithfully represents the pattern.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 3 | Probe classification score | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L7:F15690](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15690) | 3 | Late-layer semantic framings (L7:15690 public sentiment/action in response to problem at pos 3) |  text related to public sentiment and action in response to a problem | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15690) |
| [L6:F1509](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1509) | 1 | Identity / nationality group detectors on 'Indians' (L6:1509 countries/nationalities pos 1; L4:12975 Asian countries pos 2; L3:13473 racial/ethnic groups pos 2; L0:3283 mentions of India pos 1) |  mentions of countries and nationalities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1509) |
| [L4:F12975](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12975) | 2 | Identity / nationality group detectors on 'Indians' (L6:1509 countries/nationalities pos 1; L4:12975 Asian countries pos 2; L3:13473 racial/ethnic groups pos 2; L0:3283 mentions of India pos 1) | mentions of Asian countries, calendars, and paganism/eastern religions | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12975) |
| [L3:F13473](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13473) | 2 | Identity / nationality group detectors on 'Indians' (L6:1509 countries/nationalities pos 1; L4:12975 Asian countries pos 2; L3:13473 racial/ethnic groups pos 2; L0:3283 mentions of India pos 1) |  mentions of racial and ethnic groups, especially in the United States | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13473) |
| [L0:F3283](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3283) | 1 | Identity / nationality group detectors on 'Indians' (L6:1509 countries/nationalities pos 1; L4:12975 Asian countries pos 2; L3:13473 racial/ethnic groups pos 2; L0:3283 mentions of India pos 1) |  mentions of India and related concepts like Delhi, but sometimes only finds a word indicating importance | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3283) |
| [L0:F10155](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10155) | 1 | Identity / nationality group detectors on 'Indians' (L6:1509 countries/nationalities pos 1; L4:12975 Asian countries pos 2; L3:13473 racial/ethnic groups pos 2; L0:3283 mentions of India pos 1) |  words related to membership in a group | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10155) |
| [L0:F10155](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10155) | 3 | Identity / nationality group detectors on 'Indians' (L6:1509 countries/nationalities pos 1; L4:12975 Asian countries pos 2; L3:13473 racial/ethnic groups pos 2; L0:3283 mentions of India pos 1) |  words related to membership in a group | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10155) |
| [L0:F14740](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14740) | 1 | Identity / nationality group detectors on 'Indians' (L6:1509 countries/nationalities pos 1; L4:12975 Asian countries pos 2; L3:13473 racial/ethnic groups pos 2; L0:3283 mentions of India pos 1) |  names of places, people, and organizations | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14740) |
| [L0:F9480](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9480) | 1 | Identity / nationality group detectors on 'Indians' (L6:1509 countries/nationalities pos 1; L4:12975 Asian countries pos 2; L3:13473 racial/ethnic groups pos 2; L0:3283 mentions of India pos 1) |  named countries | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9480) |
| [L2:F1003](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1003) | 3 | Abuse-lexical features (L2:1003 'abuse' pos 3; L2:6255 'abuse' pos 3; L4:5206 upstream of L7:15690) |  the word "abuse" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1003) |
| [L2:F6255](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6255) | 3 | Abuse-lexical features (L2:1003 'abuse' pos 3; L2:6255 'abuse' pos 3; L4:5206 upstream of L7:15690) |  the word "abuse", or phrases related to genitalia | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6255) |
| [L4:F5206](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5206) | 3 | Abuse-lexical features (L2:1003 'abuse' pos 3; L2:6255 'abuse' pos 3; L4:5206 upstream of L7:15690) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5206) |
| [L4:F4021](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4021) | 4 | Abuse-lexical features (L2:1003 'abuse' pos 3; L2:6255 'abuse' pos 3; L4:5206 upstream of L7:15690) |  code snippets or configurations with the word "as". | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4021) |
| [L0:F11154](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11154) | 2 | Generic function-word / off-target features (L0:11154 'are' pos 2; L0:1053 'as' pos 4; L1:7492 departments/animals pos 1; L0:10389 faults/technical pos 12; L0:3564 math notation pos 13; L3:150 verbs pos 7; L0:4199 'quantity' pos 7; L0:11668 baseball pos 1) |  the word "are" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11154) |
| [L0:F1053](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1053) | 4 | Generic function-word / off-target features (L0:11154 'are' pos 2; L0:1053 'as' pos 4; L1:7492 departments/animals pos 1; L0:10389 faults/technical pos 12; L0:3564 math notation pos 13; L3:150 verbs pos 7; L0:4199 'quantity' pos 7; L0:11668 baseball pos 1) |  the word "as." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1053) |
| [L1:F7492](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7492) | 1 | Generic function-word / off-target features (L0:11154 'are' pos 2; L0:1053 'as' pos 4; L1:7492 departments/animals pos 1; L0:10389 faults/technical pos 12; L0:3564 math notation pos 13; L3:150 verbs pos 7; L0:4199 'quantity' pos 7; L0:11668 baseball pos 1) | words referring to administrative divisions, animals, or commercial elements | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7492) |
| [L0:F10389](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10389) | 12 | Generic function-word / off-target features (L0:11154 'are' pos 2; L0:1053 'as' pos 4; L1:7492 departments/animals pos 1; L0:10389 faults/technical pos 12; L0:3564 math notation pos 13; L3:150 verbs pos 7; L0:4199 'quantity' pos 7; L0:11668 baseball pos 1) |  words related to legal disputes and technical issues such as device malfunctions or program errors | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10389) |
| [L0:F3564](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3564) | 13 | Generic function-word / off-target features (L0:11154 'are' pos 2; L0:1053 'as' pos 4; L1:7492 departments/animals pos 1; L0:10389 faults/technical pos 12; L0:3564 math notation pos 13; L3:150 verbs pos 7; L0:4199 'quantity' pos 7; L0:11668 baseball pos 1) | mathematical notation symbols | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3564) |
| [L3:F150](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/150) | 7 | Generic function-word / off-target features (L0:11154 'are' pos 2; L0:1053 'as' pos 4; L1:7492 departments/animals pos 1; L0:10389 faults/technical pos 12; L0:3564 math notation pos 13; L3:150 verbs pos 7; L0:4199 'quantity' pos 7; L0:11668 baseball pos 1) | verbs, particularly past participles, and also some words in French | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/150) |
| [L0:F4199](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4199) | 7 | Generic function-word / off-target features (L0:11154 'are' pos 2; L0:1053 'as' pos 4; L1:7492 departments/animals pos 1; L0:10389 faults/technical pos 12; L0:3564 math notation pos 13; L3:150 verbs pos 7; L0:4199 'quantity' pos 7; L0:11668 baseball pos 1) |  the word "quantity" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4199) |
| [L0:F11668](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11668) | 1 | Generic function-word / off-target features (L0:11154 'are' pos 2; L0:1053 'as' pos 4; L1:7492 departments/animals pos 1; L0:10389 faults/technical pos 12; L0:3564 math notation pos 13; L3:150 verbs pos 7; L0:4199 'quantity' pos 7; L0:11668 baseball pos 1) |  Baseball terminology | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11668) |
| [L2:F2123](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2123) | 1 | Generic function-word / off-target features (L0:11154 'are' pos 2; L0:1053 'as' pos 4; L1:7492 departments/animals pos 1; L0:10389 faults/technical pos 12; L0:3564 math notation pos 13; L3:150 verbs pos 7; L0:4199 'quantity' pos 7; L0:11668 baseball pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2123) |
| [L4:F10654](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10654) | 1 | Generic function-word / off-target features (L0:11154 'are' pos 2; L0:1053 'as' pos 4; L1:7492 departments/animals pos 1; L0:10389 faults/technical pos 12; L0:3564 math notation pos 13; L3:150 verbs pos 7; L0:4199 'quantity' pos 7; L0:11668 baseball pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10654) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:11154 de=0.652 |
| 3 | `inspect_feature` ×19 | L0:11154, L0:1053, L2:1003, L3:13473, L2:6255, L1:7492, L0:10155, L0:14740, L0:10389, L4:4021, L0:3283, L7:15690, L0:4199, L0:3564, L3:150, L6:1509, L0:9480, L0:11668, L4:12975 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F15690@3` | ❌ error | — | — | Trace from L7:F15690 (public sentiment/action in response to problem, at pos 3) … |
| SA-2 | `L6:F1509@1` | ❌ error | — | — | Trace from L6:F1509 (countries/nationalities at pos 1) upstream. What input toke… |
| SA-3 | `L3:F13473@2` | ❌ error | — | — | Trace from L3:F13473 (racial/ethnic groups at pos 2) upstream. What input tokens… |
| SA-4 | `L2:F1003@3` | ❌ error | — | — | Trace from L2:F1003 (the word 'abuse' at pos 3) upstream. What input tokens driv… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L7:F15690@3, k=15 → Emb:" abusers"@3 (de=1.68) +14 more |
| 2 | `get_upstream_features` | L6:F1509@1, k=15 → Emb:"Indians"@1 (de=4.88) +14 more |
| 3 | `get_upstream_features` | L3:F13473@2, k=15 → Emb:"Indians"@1 (de=10.25) +14 more |
| 4 | `get_upstream_features` | L2:F1003@3, k=15 → Emb:" abusers"@3 (de=14.00) +14 more |
| 5 | `get_upstream_features` | L4:F12975@2, k=10 → Emb:"Indians"@1 (de=11.88) +9 more |
| 6 | `get_upstream_features` | L4:F5206@3, k=10 → Emb:" abusers"@3 (de=7.88) +9 more |
| 7 | `get_upstream_features` | L2:F2123@1, k=10 → Emb:"Indians"@1 (de=17.12) +9 more |
| 8 | `get_upstream_features` | L4:F10654@1, k=10 → Emb:"Indians"@1 (de=15.12) +9 more |

### Build

`build_circuit` → 9 nodes, 10 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 45,878 | 5,049 | 166,659 | 0 | $0.0298 | — | — |
| **Total** | | **45,878** | **5,049** | **166,659** | **0** | **$0.0298** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 11s