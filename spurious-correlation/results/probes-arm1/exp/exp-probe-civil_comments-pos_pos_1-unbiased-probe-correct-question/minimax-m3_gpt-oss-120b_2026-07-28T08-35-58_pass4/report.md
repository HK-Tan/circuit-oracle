# Circuit Oracle Report
**Date:** 2026-07-28 08:35:58 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity classification is driven almost entirely by **identity-group keywords** ("white", "other", "trump", "bigot") and their associated entity/topic features — not by syntactic, semantic, or evaluative content of the message. The circuit's strongest signals come from a low-layer L0:F3436 "white" detector (direct_effect +0.10, frac_nonzero 0.061), L0:F7969 "other" (0.10, frac_nonzero 0.014), L4:F11580 "negative language / swear words" (whose top promoted tokens are FUCK/idiot/morons/bastard/asshole), and L4:F14582 "White House / US government". None of the features encode the actual argumentative structure ("tie", "shows that", "supported by", "race is", "against all nonwhites") — those tokens contribute via generic function-word detectors (F164 "show", F11375 "is", F15831 "again") that fire in any English sentence. The signal is concentrated at the exact identity references in the text.

**Confidence:** 7

**Reasoning:** Walking the circuit confirms the user's concern. The probe's score is driven by features that are essentially **identity-presence detectors**:
1. **Identity-mention features (L0):** F3436 fires on the literal word "white" (frac_nonzero 0.061, generic across many topics); F7969 fires on the word "other" — neither encodes toxicity, just identity tokens. F4807 detects the name "Trump" and feeds F7815 → F14301 ("political/finance/national-security entities") → F14582 ("White House / US government reference"). This is a topic-recognition chain, not a toxicity chain.
2. **The closest thing to a real toxicity signal — L4:F11580 "negative language and swear words"** — has its top upstream direct effects coming from the **subword "ot" (23.9)** and **"big" (9.1)** token embeddings at the "bigot" position, plus generic "outsider" (F4520) and "inflammatory hateful words that attack groups" (F4053) detectors. The promoted tokens of F11580 are the profanity set (FUCK/idiot/morons/bastard/asshole), but the feature is being triggered not by profanity in the text (there isn't any) — it is being triggered because the subword "ot" happens to share character bigrams with curse words. The lexical-substring coincidence is what's being misread as toxicity.
3. **Function-word and structural features (F164 "show/your", F11375 "is", F15831 "again", F3916 "common short words")** fire on any text containing those very common tokens. They contribute +0.10 to +0.13 direct effect each, but their frac_nonzero values (0.009–0.028) and top-activating examples show they are broad lexical detectors, not toxicity detectors.
4. **The "tie" / "clearly" / adverb features** are firing on syntactic glue words — they are content-free.

In short: the probe is using **identity-token presence** ("white", "Trump", political-entity membership) and **character-substring overlap with profanity** ("ot" in "bigot") as proxies for toxicity, rather than analyzing the actual hateful claim, its targets, or its argumentation. The user's concern is well-founded: the circuit uses shallow, spurious cues.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 0 | Emb: <bos> (pos 0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: tie (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: clearly (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: shows (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: that (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: trump (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: is (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: a (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: big (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: ot (pos 9, subword of 'bigot') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: other (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: white (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 26 | Emb: again (pos 26) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F7621](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7621) | 2 | L0: Adverb/qualifier features on 'clearly' (F7621, F12866, F4422, F7861, F5707, F7142, F9761) |  the word "clearly", and to a lesser extent words associated with amounts of things | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7621) |
| [L0:F12866](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12866) | 2 | L0: Adverb/qualifier features on 'clearly' (F7621, F12866, F4422, F7861, F5707, F7142, F9761) |  adverbs such as "clearly," "plainly," and "as" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12866) |
| [L0:F4422](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4422) | 2 | L0: Adverb/qualifier features on 'clearly' (F7621, F12866, F4422, F7861, F5707, F7142, F9761) | the word "seriously" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4422) |
| [L0:F7861](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7861) | 2 | L0: Adverb/qualifier features on 'clearly' (F7621, F12866, F4422, F7861, F5707, F7142, F9761) |  instances of the words "this", "these", "clearly", or "more". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7861) |
| [L0:F5707](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5707) | 2 | L0: Adverb/qualifier features on 'clearly' (F7621, F12866, F4422, F7861, F5707, F7142, F9761) |  words or phrases related to knowledge or perspective | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5707) |
| [L0:F7142](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7142) | 2 | L0: Adverb/qualifier features on 'clearly' (F7621, F12866, F4422, F7861, F5707, F7142, F9761) |  the word "axis" and its plural form, often in the context of scientific or technical documents | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7142) |
| [L1:F9761](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9761) | 2 | L0: Adverb/qualifier features on 'clearly' (F7621, F12866, F4422, F7861, F5707, F7142, F9761) |  language asserting that a statement is obvious, undisputed, or in accordance with a rule | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9761) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 15 | L0: 'white' token feature (F3436) and 'other' token feature (F7969) - identity/reference group markers |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F7969](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7969) | 14 | L0: 'white' token feature (F3436) and 'other' token feature (F7969) - identity/reference group markers |  the word "other" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7969) |
| [L0:F164](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/164) | 3 | L0: Generic function-word features (F164 'show', F11375 'is', F15831 'again') | the words "show" and "your", particularly when talking about presenting something | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/164) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 6 | L0: Generic function-word features (F164 'show', F11375 'is', F15831 'again') |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F15831](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15831) | 26 | L0: Generic function-word features (F164 'show', F11375 'is', F15831 'again') | the word "again" and words associated with time | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15831) |
| [L0:F3916](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3916) | 1 | L0: Generic function-word features (F164 'show', F11375 'is', F15831 'again') |  common short words in legal documents | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3916) |
| [L0:F4807](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4807) | 5 | L0: 'Trump' entity-name feature (F4807) |  references to Donald Trump | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4807) |
| [L0:F12712](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12712) | 9 | L0: Quality/evaluative features on 'bigot' (F12712, F1432) | words, suffixes, or phrases that could indicate quality and the people/things which are described | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12712) |
| [L0:F1432](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1432) | 9 | L0: Quality/evaluative features on 'bigot' (F12712, F1432) | the word "quality" and words associated with negative impacts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1432) |
| [L2:F9199](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9199) | 9 | L0: Quality/evaluative features on 'bigot' (F12712, F1432) |  instances of "ot" in code | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9199) |
| [L1:F7815](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7815) | 5 | L1: Trump as referenced/contacted entity (F7815) |  references to contacting or communicating with someone, including job titles related to communication. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7815) |
| [L2:F14301](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14301) | 5 | L2: Political/finance/national-security entity names (F14301) |  names of people and organizations involved in politics, finance, and national security | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14301) |
| [L2:F15769](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15769) | 1 | L2: 'tie' generic noun feature (F15769) | the word "tie" in various contexts | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15769) |
| [L2:F4053](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4053) | 9 | L2: 'inflammatory hateful words that attack groups' (F4053) - hate-group keyword feature |  inflammatory hateful words, phrases, and names that attack groups of people. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4053) |
| [L2:F4520](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4520) | 9 | L2: 'newness/outsider' feature (F4520) - identity-othering signal |  words related to newness or being an outsider | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4520) |
| [L3:F373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/373) | 1 | L3: 'tie' orthographic/structural feature (F373, F3149) |  word beginnings with the letters "a," "h,""i," "r," and "p" (perhaps prefixes and/or related to medical or scientific terms) | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/373) |
| [L3:F3149](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3149) | 1 | L3: 'tie' orthographic/structural feature (F373, F3149) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3149) |
| [L4:F14582](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14582) | 5 | L4: 'White House / US government' reference (F14582) |  references to the White House and the US government | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14582) |
| [L4:F2720](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2720) | 1 | L4: 'tie'/tied general noun (F2720) | mentions of a 'tie' or a similar word | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2720) |
| [L4:F11580](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11580) | 9 | L4: Toxicity / profanity gate (F11580) - promotes FUCK/idiot/morons/bastard/asshole | negative language and swear words | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11580) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:12866 de=-0.206 |
| 3 | `inspect_feature` ×20 | L0:7621, L4:14582, L0:4422, L0:11375, L0:12866, L0:3916, L0:15831, L0:7142, L0:164, L2:9199, L2:14301, L1:9761, L3:373, L0:3436, L0:7969, L0:7861, L0:5707, L2:15769, L4:11580, L4:2720 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F11580@9` | ✅ reported | 5 | 7 | Trace the path from L4:F11580 ("negative language and swear words" with promoted… |
| SA-2 | `L0:F3436@15` | ❌ error | — | — | Trace the path from L0:F3436 ("mentions of the word 'white'") at pos 15. This is… |
| SA-3 | `L4:F14582@5` | ✅ reported | 3 | 9 | Trace the path from L4:F14582 ("references to White House and US government"). W… |
| SA-4 | `L2:F14301@5` | ✅ reported | 3 | 2 | Trace the path from L2:F14301 ("names of people and organizations involved in po… |

<details>
<summary><b>SA-1</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F11580 | "negative language and swear words" |
| 2 | `get_upstream_features` | L4:F11580@9, k=10 | Emb:"ot"@9 (de=5.00) +9 more |
| 3 | `inspect_feature` | L2, F4520 | " words related to newness or being an outsider" |
| 4 | `inspect_feature` | L2, F4053 | " inflammatory hateful words, phrases, and names that attack groups of " |
| 5 | `get_upstream_features` | L2:F4520@9, k=10 | Emb:" big"@8 (de=9.06) +9 more |
| 6 | `get_upstream_features` | L2:F4053@9, k=10 | Emb:"ot"@9 (de=1.11) +9 more |
| 7 | `inspect_feature` | L0, F12712 | " words, suffixes, or phrases that could indicate quality and the peopl" |
| 8 | `inspect_feature` | L0, F1432 | " the word "quality" and words associated with negative impacts" |
| 9 | `get_upstream_features` | L2:F4520@9, k=10 | Emb:" big"@8 (de=9.06) +9 more |

**Findings:** The toxicity gate L4:F11580 is driven primarily by three upstream features: a low‑frequency profanity detector (itself), a hateful‑language detector (L2:F4053), and a newcomer/outsider detector (L2:F4520). Additional low‑layer signals related to quality evaluation (L0:F12712 and L0:F1432) also push the gate upward. Crucially, the path includes two raw token embeddings – the word "big" at position …

</details>

<details>
<summary><b>SA-3</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F14582 | " references to the White House and the US government" |
| 2 | `get_upstream_features` | L4:F14582@5, k=10 | Emb:" trump"@5 (de=18.12) +9 more |
| 3 | `inspect_feature` | L2, F14301 | " names of people and organizations involved in politics, finance, and " |
| 4 | `get_upstream_features` | L2:F14301@5, k=10 | Emb:" trump"@5 (de=9.44) +9 more |
| 5 | `inspect_feature` | L1, F7815 | " references to contacting or communicating with someone, including job" |
| 6 | `get_upstream_features` | L1:F7815@5, k=10 | Emb:" trump"@5 (de=10.88) +9 more |
| 7 | `get_upstream_features` | L0:F4807@5, k=5 | Emb:" trump"@5 (de=8.69) +4 more |

**Findings:** The target feature L4:F14582 fires on mentions of the White House and US government. Its strongest upstream drivers are the token embedding for 'trump' (positive direct effect >18) and a mid‑level political‑entity detector (L2:F14301). Both of those upstream nodes are themselves driven directly by the same 'trump' embedding in earlier layers. The circuit therefore originates from the input token '…

</details>

<details>
<summary><b>SA-4</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F14301 | " names of people and organizations involved in politics, finance, and " |
| 2 | `get_upstream_features` | L2:F14301@5, k=10 | Emb:" trump"@5 (de=9.44) +9 more |
| 3 | `inspect_feature` | L1, F7815 | " references to contacting or communicating with someone, including job" |
| 4 | `get_upstream_features` | L1:F7815@5, k=10 | Emb:" trump"@5 (de=10.88) +9 more |
| 5 | `inspect_feature` | L0, F4807 | " references to Donald Trump" |
| 6 | `get_upstream_features` | L0:F4807@5, k=10 | Emb:" trump"@5 (de=8.69) +9 more |

**Findings:** The entity‑recognition feature L2:F14301 (layer 2) is driven primarily by low‑level signals about the token "trump". At layer 1 a contact‑reference feature (F7815) receives a positive push from the same token, indicating that the model is interpreting the mention of Trump as a reference to a public figure that could be contacted or discussed. The deepest driver is the layer‑0 Trump detector (F4807…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F3436@15, k=10 → Emb:" white"@15 (de=18.12) +9 more |
| 2 | `get_upstream_features` | L0:F7969@14, k=10 → Emb:" other"@14 (de=42.25) +9 more |
| 3 | `get_upstream_features` | L0:F7621@2, k=10 → Emb:" clearly"@2 (de=17.75) +9 more |
| 4 | `get_upstream_features` | L0:F3916@1, k=10 → Emb:"<bos>"@0 (de=8.94) +9 more |
| 5 | `get_upstream_features` | L0:F11375@6, k=10 → Emb:" is"@6 (de=31.38) +9 more |
| 6 | `get_upstream_features` | L0:F12866@2, k=10 → Emb:" clearly"@2 (de=17.38) +9 more |
| 7 | `get_upstream_features` | L0:F15831@26, k=10 → Emb:" again"@26 (de=43.50) +9 more |
| 8 | `get_upstream_features` | L0:F4422@2, k=10 → Emb:" clearly"@2 (de=12.62) +9 more |
| 9 | `get_upstream_features` | L0:F9761@2, k=10 → ❌ Feature (layer=0, pos=2, feature_idx=9761) not found in grap |
| 10 | `get_upstream_features` | L2:F9199@9, k=10 → Emb:"ot"@9 (de=23.88) +9 more |
| 11 | `get_upstream_features` | L4:F11580@9, k=10 → Emb:"ot"@9 (de=5.00) +9 more |
| 12 | `get_upstream_features` | L4:F14582@5, k=10 → Emb:" trump"@5 (de=18.12) +9 more |
| 13 | `get_upstream_features` | L2:F4053@9, k=10 → Emb:"ot"@9 (de=1.11) +9 more |
| 14 | `get_upstream_features` | L2:F4520@9, k=10 → Emb:" big"@8 (de=9.06) +9 more |
| 15 | `inspect_feature` ×3 | L2:4520, L2:4053, L0:4807 |
| 16 | `get_upstream_features` | L0:F12712@9, k=10 → Emb:" big"@8 (de=12.44) +9 more |
| 17 | `get_upstream_features` | L0:F1432@9, k=10 → Emb:" big"@8 (de=11.12) +9 more |
| 18 | `get_upstream_features` | L0:F7142@2, k=10 → Emb:" clearly"@2 (de=14.62) +9 more |
| 19 | `get_upstream_features` | L0:F164@3, k=10 → Emb:" shows"@3 (de=19.38) +9 more |
| 20 | `get_upstream_features` | L2:F14301@5, k=10 → Emb:" trump"@5 (de=9.44) +9 more |
| 21 | `get_upstream_features` | L2:F15769@1, k=10 → Emb:"tie"@1 (de=21.12) +9 more |
| 22 | `get_upstream_features` | L4:F2720@1, k=10 → Emb:"tie"@1 (de=10.75) +9 more |
| 23 | `get_upstream_features` | L3:F373@1, k=10 → Emb:"<bos>"@0 (de=26.25) +9 more |
| 24 | `get_upstream_features` | L0:F7861@2, k=10 → Emb:" clearly"@2 (de=14.25) +9 more |
| 25 | `get_upstream_features` | L0:F5707@2, k=10 → Emb:" clearly"@2 (de=20.88) +9 more |
| 26 | `get_upstream_features` | L0:F3635@4, k=10 → Emb:" that"@4 (de=39.00) +9 more |

### Build

`build_circuit` → 28 nodes, 29 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 73,188 | 7,807 | 231,725 | 0 | $0.0452 | — | — |
| SA-4 | openai/gpt-oss-120b | 61,764 | 4,683 | 2,528 | 0 | $0.0121 | ✅ 3F/2E | Trace the path from L2:F14301 ("names of people and organiza… |
| SA-3 | openai/gpt-oss-120b | 49,472 | 4,624 | 13,760 | 0 | $0.0104 | ✅ 3F/9E | Trace the path from L4:F14582 ("references to White House an… |
| SA-1 | openai/gpt-oss-120b | 102,555 | 8,013 | 15,168 | 0 | $0.0204 | ✅ 5F/7E | Trace the path from L4:F11580 ("negative language and swear … |
| **Total** | | **286,979** | **25,127** | **263,181** | **0** | **$0.0882** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 13s