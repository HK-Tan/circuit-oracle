# Circuit Oracle Report
**Date:** 2026-07-28 07:19:48 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity probe is driven primarily by a sparse set of identity- and entity-mention features (the literal token "white" at pos 15, the token "trump" at pos 5, the "ot" suffix of "bigot" at pos 9, and the intensifier "clearly" at pos 2) which directly excite downstream "White House," "profanity," and "extremism" detectors, rather than by any compositional semantic understanding of the proposition that "trump is a bigot … this race is bigoted whites against all nonwhites."

**Confidence:** 8

**Reasoning:** The circuit is shallow and lexical. The terminal probe score (layer 26) is fed by mid-layer L4/L6 supernodes whose top features are entity- and slur-cued:

- **L4:14582** "references to the White House and the US government" (direct_effect 0.156, promoted: Biden/Trump/Obama) and **L4:11580** "negative language and swear words" (direct_effect 0.092, promoted: FUCK/idiot/moron) are the strongest semantic-class signals.
- **L4:7545** "religious extremism, violence, and terrorism" (direct_effect 0.079) and **L4:15204** "art galleries, museums and the White House" (direct_effect 0.077) further reinforce the identity-conditioned response.
- **L6:15063** "American politics, elections, and politicians" (direct_effect 0.079) consolidates the entity-signal story at the top.

These all root in early-layer lexical detectors:
- **Emb:" white" (pos 15)** → L0:3436 "mentions of the word 'white'" (frac_nonzero 0.061) and L0:10910 "the word 'possession' and the words 'white', 'immediate' and 'once'" — i.e., a near-pure color-word detector whose top activating examples are literally about Black/white wage and racial-context passages.
- **Emb:" trump" (pos 5)** → L0:4807 "references to Donald Trump" (frac_nonzero 0.017) and L0:1858 (a mix of holiday terms, geographical references, religiously charged terms) → L2:4507 "mentions of Donald Trump, and occasionally of Hillary Clinton" (frac_nonzero 0.0019, very sparse).
- **Emb:"ot" (pos 9, the suffix of "bigot")** → L2:4053 "inflammatory hateful words, phrases, and names that attack groups of people" (frac_nonzero 0.011) → L4:7545 "extremism" (frac_nonzero 0.012).
- **Emb:" clearly" (pos 2)** drives a cluster of "clearly"-detectors (L0:12866, L0:7621, L0:4422, L0:5707, L0:7861, L0:164 "show/your", L1:9761 "obvious/undisputed", L1:2407 "clearly") — discourse-marker lexical features.

Crucially, the **content** of the prompt (the predicative structure "X is a bigot," "race is bigoted whites against nonwhites") is not encoded by any feature that would require compositional semantics. There is no L5+ feature for "identity-group-as-target" or "hateful proposition." The probe essentially fires because the input contains the names/keywords (white, Trump, bigot→ot) that the L4 toxicity features were trained to associate with hate speech. This is exactly the user's concern: the classifier's causal features are **spurious identity mentions** and **single-word slur cues** rather than a representation of the proposition's meaning. Removing the words "white," "trump," or "bigot" would, per this circuit, eliminate almost the entire positive signal — even though the remaining text would still carry the hateful proposition. Conversely, swapping the words "Obama" / "Jews" into the same syntactic frame would, by these same L4 features, produce a comparable score, confirming the identity-mention shortcut.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F12866](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12866) | 2 | Lexical detectors: 'clearly' / 'white' / Trump name / 'show' (pos 2/3/5/15) |  adverbs such as "clearly," "plainly," and "as" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12866) |
| [L0:F7621](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7621) | 2 | Lexical detectors: 'clearly' / 'white' / Trump name / 'show' (pos 2/3/5/15) |  the word "clearly", and to a lesser extent words associated with amounts of things | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7621) |
| [L0:F4422](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4422) | 2 | Lexical detectors: 'clearly' / 'white' / Trump name / 'show' (pos 2/3/5/15) | the word "seriously" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4422) |
| [L0:F5707](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5707) | 2 | Lexical detectors: 'clearly' / 'white' / Trump name / 'show' (pos 2/3/5/15) |  words or phrases related to knowledge or perspective | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5707) |
| [L0:F7861](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7861) | 2 | Lexical detectors: 'clearly' / 'white' / Trump name / 'show' (pos 2/3/5/15) |  instances of the words "this", "these", "clearly", or "more". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7861) |
| [L0:F164](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/164) | 3 | Lexical detectors: 'clearly' / 'white' / Trump name / 'show' (pos 2/3/5/15) | the words "show" and "your", particularly when talking about presenting something | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/164) |
| [L0:F3916](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3916) | 1 | Lexical detectors: 'clearly' / 'white' / Trump name / 'show' (pos 2/3/5/15) |  common short words in legal documents | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3916) |
| [L0:F7142](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7142) | 2 | Lexical detectors: 'clearly' / 'white' / Trump name / 'show' (pos 2/3/5/15) |  the word "axis" and its plural form, often in the context of scientific or technical documents | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7142) |
| [L0:F2407](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2407) | 2 | Lexical detectors: 'clearly' / 'white' / Trump name / 'show' (pos 2/3/5/15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2407) |
| [L0:F4807](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4807) | 5 | Lexical detectors: 'clearly' / 'white' / Trump name / 'show' (pos 2/3/5/15) |  references to Donald Trump | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4807) |
| [L0:F1858](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1858) | 5 | Lexical detectors: 'clearly' / 'white' / Trump name / 'show' (pos 2/3/5/15) |  a mix of holiday terms, internet-related terms, geographical references, and religiously charged terms | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1858) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 5 | Lexical detectors: 'clearly' / 'white' / Trump name / 'show' (pos 2/3/5/15) | technical documents or data, including numbers, units, and references to figures or tables. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 15 | Lexical detectors: 'clearly' / 'white' / Trump name / 'show' (pos 2/3/5/15) |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F10910](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) | 15 | Lexical detectors: 'clearly' / 'white' / Trump name / 'show' (pos 2/3/5/15) | the word "possession" and the words "white", "immediate" and "once" regardless of context | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) |
| [L0:F7969](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7969) | 14 | Lexical detectors: 'clearly' / 'white' / Trump name / 'show' (pos 2/3/5/15) |  the word "other" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7969) |
| [L1:F9761](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9761) | 2 | Discourse/intensifier features (pos 1/2/5) |  language asserting that a statement is obvious, undisputed, or in accordance with a rule | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9761) |
| [L1:F887](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/887) | 5 | Discourse/intensifier features (pos 1/2/5) | the word "ideas" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/887) |
| [L1:F2407](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2407) | 2 | Discourse/intensifier features (pos 1/2/5) |  the word "clearly" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2407) |
| [L2:F4507](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4507) | 5 | Identity/political-entity detectors: Trump name, political figures, hateful/outsider words (pos 5/9) |  mentions of Donald Trump, and occasionally of Hillary Clinton | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4507) |
| [L2:F14301](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14301) | 5 | Identity/political-entity detectors: Trump name, political figures, hateful/outsider words (pos 5/9) |  names of people and organizations involved in politics, finance, and national security | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14301) |
| [L2:F15769](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15769) | 1 | Identity/political-entity detectors: Trump name, political figures, hateful/outsider words (pos 5/9) | the word "tie" in various contexts | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15769) |
| [L2:F4520](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4520) | 9 | Identity/political-entity detectors: Trump name, political figures, hateful/outsider words (pos 5/9) |  words related to newness or being an outsider | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4520) |
| [L2:F4053](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4053) | 9 | Identity/political-entity detectors: Trump name, political figures, hateful/outsider words (pos 5/9) |  inflammatory hateful words, phrases, and names that attack groups of people. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4053) |
| [L2:F9199](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9199) | 9 | Identity/political-entity detectors: Trump name, political figures, hateful/outsider words (pos 5/9) |  instances of "ot" in code | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9199) |
| [L3:F3136](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3136) | 5 | Mid-layer political-actor / Trump admin features (pos 1/5/9) |  names of people involved in the Trump administration | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3136) |
| [L3:F15558](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15558) | 9 | Mid-layer political-actor / Trump admin features (pos 1/5/9) | words that indicate feelings or qualities | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15558) |
| [L3:F373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/373) | 1 | Mid-layer political-actor / Trump admin features (pos 1/5/9) |  word beginnings with the letters "a," "h,""i," "r," and "p" (perhaps prefixes and/or related to medical or scientific terms) | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/373) |
| [L4:F14582](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14582) | 5 | Toxicity-relevant mid-layer features: profanity/extremism/White House references (pos 5/9/15) |  references to the White House and the US government | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14582) |
| [L4:F11580](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11580) | 9 | Toxicity-relevant mid-layer features: profanity/extremism/White House references (pos 5/9/15) | negative language and swear words | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11580) |
| [L4:F7545](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7545) | 9 | Toxicity-relevant mid-layer features: profanity/extremism/White House references (pos 5/9/15) |  words or phrases relating to religious extremism, violence, and terrorism. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7545) |
| [L4:F15204](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) | 15 | Toxicity-relevant mid-layer features: profanity/extremism/White House references (pos 5/9/15) |  art galleries, museums and the White House | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) |
| [L4:F9832](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9832) | 1 | Toxicity-relevant mid-layer features: profanity/extremism/White House references (pos 5/9/15) |  parts of words that do not form recognizable English words, and some foreign words | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9832) |
| [L4:F2720](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2720) | 1 | Toxicity-relevant mid-layer features: profanity/extremism/White House references (pos 5/9/15) | mentions of a 'tie' or a similar word | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2720) |
| [L4:F5323](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5323) | 5 | Toxicity-relevant mid-layer features: profanity/extremism/White House references (pos 5/9/15) |  location name and programing terms | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5323) |
| [L6:F15063](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15063) | 5 | American politics / discourse markers (pos 1/5) |  references to American politics, elections, and politicians | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15063) |
| [L6:F1707](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1707) | 1 | American politics / discourse markers (pos 1/5) | a variety of discourse markers, qualifiers, intensifiers, or words expressing an opinion. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1707) |
| [L6:F5753](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5753) | 5 | American politics / discourse markers (pos 1/5) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5753) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:12866 de=-0.206 |
| 3 | `inspect_feature` ×6 | L0:12866, L0:7621, L4:14582, L0:4422, L0:11375, L0:15831 |
| 4 | `get_top_features` | 50 features; top: L0:12866 de=-0.206 |
| 5 | `inspect_feature` ×27 | L0:7142, L0:164, L0:3916, L2:9199, L2:14301, L3:373, L1:9761, L0:3436, L0:7969, L0:7861, L4:11580, L4:2720, L6:15063, L6:1707, L2:15769, L0:8444, L1:2407, L0:5707, L0:4517, L0:425, L0:13663, L3:3136, L4:7545, L4:15204, L2:4507, L4:5323, L4:9832 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F11580@9` | ✅ reported | 4 | 3 | Trace upstream from this 'negative language / swear words' feature. Determine wh… |
| SA-2 | `L4:F7545@9` | ✅ reported | 5 | 6 | Trace upstream from this 'religious extremism / violence / terrorism' feature. D… |
| SA-3 | `L4:F15204@15` | ✅ reported | 3 | 5 | Trace upstream from this 'art galleries, museums, and the White House' / 'white'… |
| SA-4 | `L4:F14582@5` | ❌ error | — | — | Trace upstream from this 'references to the White House and the US government' f… |
| SA-5 | `L2:F4507@5` | ✅ reported | 6 | 7 | Trace upstream from this 'mentions of Donald Trump, and occasionally of Hillary … |
| SA-6 | `L0:F3436@15` | ❌ error | — | — | Trace upstream from this 'mentions of the word white' feature. Determine which i… |

<details>
<summary><b>SA-1</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F11580 | "negative language and swear words" |
| 2 | `get_upstream_features` | L4:F11580@9, k=10 | Emb:"ot"@9 (de=5.00) +9 more |
| 3 | `inspect_feature` | L2, F4520 | " words related to newness or being an outsider" |
| 4 | `inspect_feature` | L0, F12712 | " words, suffixes, or phrases that could indicate quality and the peopl" |
| 5 | `get_upstream_features` | L2:F4520@9, k=10 | Emb:" big"@8 (de=9.06) +9 more |
| 6 | `inspect_feature` | L0, F1432 | " the word "quality" and words associated with negative impacts" |
| 7 | `get_upstream_features` | L0:F12712@9, k=10 | Emb:" big"@8 (de=12.44) +9 more |
| 8 | `get_upstream_features` | L0:F1432@9, k=10 | Emb:" big"@8 (de=11.12) +9 more |

**Findings:** The profanity detection feature (L4:11580) receives its strongest excitatory drive from three upstream sources: (1) the embedding token 'ot' (pos 9) and the embedding 'big' (pos 8) directly excite it, satisfying the embedding‑connection requirement; (2) a low‑layer (L2) feature 4520 that flags outsider/newcomer language contributes positively; (3) an even lower‑layer (L0) quality‑descriptor featur…

</details>

<details>
<summary><b>SA-2</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F7545 | " words or phrases relating to religious extremism, violence, and terro" |
| 2 | `get_upstream_features` | L4:F7545@9, k=15 | Emb:"ot"@9 (de=2.50) +14 more |
| 3 | `inspect_feature` | L3, F15558 | " words that indicate feelings or qualities" |
| 4 | `inspect_feature` | L2, F4053 | " inflammatory hateful words, phrases, and names that attack groups of " |
| 5 | `inspect_feature` | L0, F6628 | " superlative adjectives and nouns associated with a high degree of qua" |
| 6 | `get_upstream_features` | L3:F15558@9, k=15 | Emb:"ot"@9 (de=2.38) +14 more |
| 7 | `inspect_feature` | L2, F964 | " words relating to sports teams, players, and performance" |
| 8 | `inspect_feature` | L3, F6150 | " words that end in "or", "ers", "ist", "ess", "man", "ter", or "ider"" |
| 9 | `get_upstream_features` | L2:F964@9, k=15 | Emb:" big"@8 (de=6.28) +14 more |
| 10 | `inspect_feature` | L0, F865 | " text related to well-being" |

**Findings:** The extremist‑content detector (L4:F7545) is driven primarily by a strong positive contribution from the input token 'ot' (embedding). Upstream, an affective‑language detector (L3:F15558) amplifies the signal, itself receiving input from a hateful‑slur detector (L2:F4053) and a superlative intensifier (L0:F6628). This chain shows how low‑level token embeddings and mid‑layer semantic features combi…

</details>

<details>
<summary><b>SA-3</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F15204 | " art galleries, museums and the White House" |
| 2 | `get_upstream_features` | L4:F15204@15, k=10 | Emb:" white"@15 (de=40.75) +9 more |
| 3 | `inspect_feature` | L0, F10910 | "the word "possession" and the words "white", "immediate" and "once" re" |
| 4 | `inspect_feature` | L0, F3436 | " mentions of the word "white"" |
| 5 | `get_upstream_features` | L0:F10910@15, k=10 | Emb:" white"@15 (de=14.75) +9 more |
| 6 | `get_upstream_features` | L0:F3436@15, k=10 | Emb:" white"@15 (de=18.12) +9 more |

**Findings:** The target L4 feature (art galleries, museums and the White House) is driven primarily by the input token " white" at position 15. The token feeds two low‑layer detectors (L0:F10910 and L0:F3436) that are generic white‑token detectors. Their activations then positively influence the L4 feature, with a direct embedding contribution that dominates the effect. Both upstream detectors reside in layer …

</details>

<details>
<summary><b>SA-5</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F4507 | " mentions of Donald Trump, and occasionally of Hillary Clinton" |
| 2 | `get_upstream_features` | L2:F4507@5, k=10 | Emb:" trump"@5 (de=17.88) +9 more |
| 3 | `inspect_feature` | L0, F1858 | " a mix of holiday terms, internet-related terms, geographical referenc" |
| 4 | `get_upstream_features` | L0:F1858@5, k=10 | Emb:" trump"@5 (de=8.69) +9 more |
| 5 | `inspect_feature` | L0, F4807 | " references to Donald Trump" |
| 6 | `get_upstream_features` | L0:F4807@5, k=10 | Emb:" trump"@5 (de=8.69) +9 more |
| 7 | `inspect_feature` | L1, F887 | "the word "ideas"" |
| 8 | `get_upstream_features` | L1:F887@5, k=10 | Emb:" trump"@5 (de=10.06) +9 more |
| 9 | `inspect_feature` | L0, F1847 | "scientific terms and experimental details related to biological and ch" |
| 10 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |

**Findings:** The political‑mention feature (L2:4507) is driven primarily by the raw input token embedding for "trump" (direct_effect ~17.9) and by three low‑layer detectors: a generic sparse entity detector (1858), a dedicated Trump‑reference detector (4807), and a technical‑document detector (9026). These feed into a mid‑layer contextual feature (L1:887) that captures the co‑occurrence of Trump with discussio…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F14582@5, k=10 → Emb:" trump"@5 (de=18.12) +9 more |
| 2 | `get_upstream_features` | L0:F3436@15, k=5 → Emb:" white"@15 (de=18.12) +4 more |
| 3 | `get_upstream_features` | L2:F4507@5, k=3 → Emb:" trump"@5 (de=17.88) +2 more |
| 4 | `get_upstream_features` | L4:F11580@9, k=5 → Emb:"ot"@9 (de=5.00) +4 more |
| 5 | `get_upstream_features` | L4:F15204@15, k=5 → Emb:" white"@15 (de=40.75) +4 more |
| 6 | `get_upstream_features` | L4:F7545@9, k=5 → Emb:"ot"@9 (de=2.50) +4 more |
| 7 | `inspect_feature` ×8 | L0:4807, L0:10910, L2:4053, L2:4520, L2:14301, L0:1858, L0:9026, L1:887 |

### Build

`build_circuit` → 11 nodes, 17 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 87,020 | 6,586 | 366,103 | 0 | $0.0560 | — | — |
| SA-3 | openai/gpt-oss-120b | 41,739 | 3,419 | 12,512 | 0 | $0.0085 | ✅ 3F/5E | Trace upstream from this 'art galleries, museums, and the Wh… |
| SA-5 | openai/gpt-oss-120b | 104,268 | 7,535 | 5,152 | 0 | $0.0202 | ✅ 6F/7E | Trace upstream from this 'mentions of Donald Trump, and occa… |
| SA-2 | openai/gpt-oss-120b | 121,677 | 6,399 | 5,056 | 0 | $0.0222 | ✅ 5F/6E | Trace upstream from this 'religious extremism / violence / t… |
| SA-1 | openai/gpt-oss-120b | 73,933 | 5,638 | 10,112 | 0 | $0.0146 | ✅ 4F/3E | Trace upstream from this 'negative language / swear words' f… |
| **Total** | | **428,637** | **29,577** | **398,935** | **0** | **$0.1215** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 34s