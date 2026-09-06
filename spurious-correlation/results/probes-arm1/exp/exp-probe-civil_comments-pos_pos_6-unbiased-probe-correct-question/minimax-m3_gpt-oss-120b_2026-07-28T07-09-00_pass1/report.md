# Circuit Oracle Report
**Date:** 2026-07-28 07:09:00 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_6 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's positive classification is driven by an aggregation of low-layer identity-token detectors (notably "white" and "black") combined with a "dude"-centric insult/negative-opinion pathway — the model is essentially reading the presence of racial-identity terms and an ingroup/outgroup framing as a toxicity signal, independent of any slur or profanity.

**Confidence:** 7

**Reasoning:**

The probe's most positive direct drivers are all at very low layers and are nearly all identity- or slur-adjacent features, not lexical toxicity detectors:

- **L0:F3436 (direct_effect +0.289, frac_nonzero 0.061)** — a dedicated detector for the token "white" that activates on it regardless of context. Upstream is the raw token embedding for " white" (pos 2), confirming this is a *surface identity token* signal, not a meaning-conditioned one.
- **L4:F15204 (+0.228, frac_nonzero 0.0048)** — labeled "White House / museums" but its activating examples are dominated by " white" in racial contexts (slavery, racial makeup, white minorities, etc.); it inherits a direct_effect=43.5 from the " white" embedding and small bumps from L0:F3436 and L0:F10910.
- **L6:F4008 (+0.143, frac_nonzero 0.031)** — "expletives, strong opinions and negative words", but on this prompt it is firing on the colloquial address term "dude" at pos 3. Tracing upstream shows it integrates (a) a "group-of-people term" detector (L2:F9909, "guy/guys/dude"), (b) L5:F10172 — labeled "ethnic slurs and terms related to the American South", and (c) L3:F13061 — explicitly labeled "words related to race, gender and social issues". The "dude" embedding feeds both the group-term feature and the insult feature directly. In other words, the model's "negative-word" detector is *being primed* by race/gender features, not by any profanity.
- **L3:F13061 (+0.122, pos 7)** — race/gender/social-issues word detector. Traced upstream, its biggest direct_effect (15.7) is the raw embedding of the **preceding** token " black" (pos 6), not the word "thunder" (pos 7) the feature nominally sits on. It also receives input from L2:F13158 ("words about race and ethnicity") which itself fires on the " black" embedding, and L2:F9837 ("references to men") which fires on " man" (pos 8).
- **L9:F11035 (+0.094)** — "mentions of different racial or ethnic groups… news, payments, political concepts"; upstream: " white" embedding (+2.4), " dude" embedding (-1.4), " Another" embedding (+1.0), and a L8 racial-news feature (F13464, +2.6). So the late-layer "race-in-news" signal is literally being driven by reading the words "Another white" together.
- Supporting features: L0:F1015 (+0.116) — the token "black" at pos 6; L6:F1330 (+0.113) — "opinions/commentary on current events with negative tone", fed by the insult pathway; L0:F15621 (+0.104) — the token "noise" at pos 4 (the elided "thun**der**" tail picks up a spurious "noise" co-activation). L0:F4090 (-0.273) is *inhibitory* on the probe (the "another" token pushes the score *down*).

**Path convergence:** The circuit shows two parallel identity-token pathways that merge at the probe:
1. *White* token path: `Emb:white` → L0:F3436 → L4:F15204 → probe; also `Emb:white` → L9:F11035 → probe.
2. *Black/man social-issues* path: `Emb:black` → L2:F13158 → L3:F13061 → probe, with `Emb:man` → L2:F9837 → L3:F13061.
3. *"Dude" insult* path: `Emb:dude` → L2:F9909 + L5:F10172(slur) + L3:F13061(social-issues) → L6:F4008 → probe, with L6:F1330 downstream.

Critically, the social-issues feature (L3:F13061) feeds *into* the slur feature (L5:F10172), which then feeds the insult feature (L6:F4008). This is the smoking gun for the user's concern: a generic "insult/negative-opinion" feature is being *topped up* by race/gender-word detectors, so any sentence that names two identity groups plus a colloquial address term will be partly scored as toxic regardless of whether anything toxic was actually said. There is **no profanity, no slur, and no syntactic/lexical-toxicity feature** in the top positive drivers — the probe's classification is being driven almost entirely by (a) the surface identity tokens "white" and "black" being present, (b) a race/gender "social-issues" feature (L3:F13061) that fires on the mere co-occurrence of those tokens, and (c) a "dude"-keyed negative-opinion feature that was primed by the same social-issues signal. The "white" identity detector alone (L0:F3436 + L4:F15204) contributes a combined direct_effect of ~+0.52, more than 30% of the total positive signal in the top-15 list. This is a textbook spurious-correlation / "identity-group cue" failure: the probe (and whatever classifier it underlies) has learned that racially-charged two-group framings correlate with toxicity, so it reads the framing as toxic content.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe classification score (output direction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L4:F15204](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) | 2 | "white" / White House racial context (L4:F15204) |  art galleries, museums and the White House | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 2 | "white" token detector (L0:F3436) |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F4090](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4090) | 1 | "another" token detector (L0:F4090) - inhibitory | the word "another" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4090) |
| [L0:F1015](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1015) | 6 | "black" token detector (L0:F1015) |  the word "black" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1015) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 6 | race/ethnicity words (L2:F13158) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F9837](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9837) | 7 | references to men (L2:F9837) |  references to men | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9837) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 7 | race/gender/social-issues words (L3:F13061) | words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L2:F9909](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9909) | 3 | group-of-people term - dude/guys (L2:F9909) | terms used to describe groups of people or places | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9909) |
| [L5:F10172](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10172) | 3 | ethnic slur / Southern-US terms (L5:F10172) | ethnic slurs and terms related to the American South | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10172) |
| [L5:F14851](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14851) | 3 | rap / aggressive slang (L5:F14851) | slang terms and phrases used in rap music | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14851) |
| [L6:F4008](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4008) | 3 | expletives / negative-opinion words - dude (L6:F4008) |  expletives, strong opinions and negative words | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4008) |
| [L6:F1330](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1330) | 3 | negative commentary on current events (L6:F1330) |  opinions and commentary about current events, possibly with a negative tone | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1330) |
| [L9:F11035](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/11035) | 3 | racial/ethnic-group mentions in news context (L9:F11035) |  mentions of different racial or ethnic groups, news, payments, political concepts and geographical locations. | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/11035) |
| [L0:F15621](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15621) | 4 | "noise" token detector (L0:F15621) | the word "noise," sometimes "noisy," and occasionally a related word like "improvement." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15621) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: white (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: dude (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: black (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: man (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:3436 de=0.289 |
| 3 | `inspect_feature` ×4 | L0:3436, L4:15204, L0:4090, L6:4008 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F4008@3` | ✅ reported | 7 | 15 | Trace upstream from L6:F4008 at pos 3 — "expletives, strong opinions and negativ… |
| SA-2 | `L4:F15204@2` | ✅ reported | 4 | 4 | Trace upstream from L4:F15204 at pos 2 — "art galleries, museums and the White H… |
| SA-3 | `L0:F3436@2` | ❌ error | — | — | Trace upstream from L0:F3436 at pos 2 — "mentions of the word 'white'". Confirm … |
| SA-4 | `L3:F13061@7` | ✅ reported | 4 | 3 | Trace upstream from L3:F13061 at pos 7. Inspect this feature to learn its label,… |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F4008 | " expletives, strong opinions and negative words" |
| 2 | `get_upstream_features` | L6:F4008@3, k=10 | Emb:" dude"@3 (de=10.56) +9 more |
| 3 | `inspect_feature` | L2, F9909 | " terms used to describe groups of people or places" |
| 4 | `inspect_feature` | L5, F10172 | " ethnic slurs and terms related to the American South" |
| 5 | `inspect_feature` | L3, F13061 | " words related to race, gender and social issues" |
| 6 | `inspect_feature` | L5, F14851 | "slang terms and phrases used in rap music" |
| 7 | `get_upstream_features` | L2:F9909@3, k=10 | Emb:" dude"@3 (de=12.56) +9 more |
| 8 | `get_upstream_features` | L2:F9909@3, k=10 | Emb:" dude"@3 (de=12.56) +9 more |
| 9 | `inspect_feature` | L1, F9058 | " various slang and strong language." |
| 10 | `get_upstream_features` | L5:F10172@3, k=10 | Emb:" white"@2 (de=3.12) +9 more |

**Findings:** Tracing from L6:F4008 (position 3) shows that it aggregates multiple identity- and slur‑related upstream signals (group terms, ethnic slurs, race/gender terms, rap slang) rather than being a single generic insult detector. The deepest source is the input token embedding for "dude" at position 3, which has the highest direct effect on the upstream group‑reference feature (L2:F9909) and also a stron…

</details>

<details>
<summary><b>SA-2</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F15204 | " art galleries, museums and the White House" |
| 2 | `get_upstream_features` | L4:F15204@2, k=10 | Emb:" white"@2 (de=43.50) +9 more |
| 3 | `inspect_feature` | L0, F10910 | "the word "possession" and the words "white", "immediate" and "once" re" |
| 4 | `get_upstream_features` | L0:F10910@2, k=10 | Emb:" white"@2 (de=14.31) +9 more |
| 5 | `inspect_feature` | L0, F3436 | " mentions of the word "white"" |
| 6 | `get_upstream_features` | L0:F3436@2, k=10 | Emb:" white"@2 (de=17.88) +9 more |
| 7 | `inspect_feature` | L0, F3241 | " contexts related to "agreement", especially in a collaborative or pol" |
| 8 | `get_upstream_features` | L0:F3241@2, k=10 | Emb:" white"@2 (de=13.06) +9 more |

**Findings:** The target L4:F15204 is primarily driven by the embedding of the token ' white' at position 2 (direct_effect 43.5), confirming that the feature inherits directly from the raw token. Additional modest contributions come from three layer‑0 features: F3436, a dedicated 'white' detector; F10910, a low‑level lexical co‑activation feature; and F3241, a political‑agreement detector with incidental overla…

</details>

<details>
<summary><b>SA-4</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F13061 | " words related to race, gender and social issues" |
| 2 | `get_upstream_features` | L3:F13061@7, k=10 | Emb:" black"@6 (de=15.69) +9 more |
| 3 | `inspect_feature` | L2, F9837 | " references to men" |
| 4 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 5 | `get_upstream_features` | L2:F9837@7, k=10 | Emb:" man"@7 (de=21.50) +9 more |
| 6 | `inspect_feature` | L0, F9076 | " mentions of men, boys, areas, or general locations in a text" |
| 7 | `inspect_feature` | L0, F10849 | " the words "man", "men", or "woman"" |

**Findings:** Tracing upstream from L3:F13061 (position 7, the word "thunder") quickly reveals a dominant positive contribution from the raw embedding of the preceding token "black" (pos 6). Two intermediate features also feed into the target: L2:F9837 (gender‑reference to men) and L2:F13158 (race/ethnicity detector). All three upstream nodes lie at layers ≤ 8 (the embedding is layer 0, the other two are layer …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×5 | L2:13158, L0:1015, L0:15621, L9:11035, L6:1330 |
| 2 | `get_upstream_features` | L9:F11035@3, k=10 → L8:F13464 (de=2.59) +9 more |
| 3 | `inspect_feature` | L2, F9837 → " references to men" |

### Build

`build_circuit` → 19 nodes, 24 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 43,704 | 7,674 | 128,168 | 0 | $0.0300 | — | — |
| SA-4 | openai/gpt-oss-120b | 66,894 | 3,847 | 5,056 | 0 | $0.0124 | ✅ 4F/3E | Trace upstream from L3:F13061 at pos 7. Inspect this feature… |
| SA-1 | openai/gpt-oss-120b | 123,313 | 8,361 | 22,720 | 0 | $0.0239 | ✅ 7F/15E | Trace upstream from L6:F4008 at pos 3 — "expletives, strong … |
| SA-2 | openai/gpt-oss-120b | 69,135 | 4,879 | 10,208 | 0 | $0.0135 | ✅ 4F/4E | Trace upstream from L4:F15204 at pos 2 — "art galleries, mus… |
| **Total** | | **303,046** | **24,761** | **166,152** | **0** | **$0.0797** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 56s