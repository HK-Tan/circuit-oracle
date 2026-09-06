# Circuit Oracle Report
**Date:** 2026-07-28 07:22:15 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's positive score is driven almost entirely by the *presence of identity/targeted entity tokens* (Trump, white, race, other) and political-tribal cues, with the top late-layer features (L6:F15063 "American politics/elections", L6:F5753 "political viewpoints & figures") being activated by the entity token "trump" propagating through L4:F14582 "White House / US government" — i.e., naming a political figure + an identity label, not any actual toxic lexicon.

**Confidence:** 7

**Reasoning:** The circuit is strikingly thin on toxic-language content and thick on identity/political-entity content.

**What the late layers (where the probe lives) actually encode.** The two largest positive direct-effect features into the probe are L0:F12866 "adverbs like 'clearly','plainly'" (+0.194 via L0:F7621 at pos 2), L4:F14582 "White House/US government" (+0.156), and L0:F4422 "the word 'seriously'" (+0.137), all firing on **"tie clearly shows that trump is a bigot"** (the first sentence). L4:F14582's strongest driver is the *Emb: trump* token (direct_effect=18.125 from position 5), with sub-contributions from L2:F14301 (politics/finance names) and L3:F3136 (Trump administration names). L4:F14582 then feeds L6:F15063 ("American politics / elections / politicians") with direct_effect=6.81 — so the Trump-name token, the political-names detector, and an "American-politics" supernode combine to push the probe. L6:F5753 ("political viewpoints & figures", suppressed_tokens including Trump/Biden) is in the *negative*-effect tail, partially cancelling the L6:F15063 boost.

**Identity tokens dominate.** Emb: "white" (pos 15, in "other white bigots") drives L0:F3436 ("mentions of 'white'", direct_effect=18.125), L4:F7136 ("the color white", direct_effect=43.5) and L4:F15204 ("art galleries, museums and the White House", direct_effect=40.75). The second "white" at pos 25 ("white again") drives L0:F3436 again with direct_effect=18.25. Emb: "race" (pos 40) drives L3:F5475 ("occurrences of the word 'race'", direct_effect=22.125). Emb: "other" (pos 14) drives L0:F7969 ("the word 'other'", direct_effect=42.25). These are not slur or slur-suffix detectors; they are identity-label detectors.

**Generic lexical features crowd the top.** The #1 positive feature L0:F12866 (adverbs "clearly","plainly") and #2 L0:F7621 ("the word 'clearly'") both fire on "clearly" at pos 2. L0:F11375 ("is") at pos 6 (+0.131), L0:F15831 ("again") at pos 26 (−0.124, suppressive), L0:F11603 ("too") at pos 31 (+0.062), L1:F15609 ("came") at pos 30 — these are extremely common words with high frac_nonzero (0.004–0.029). They fire on most English sentences; they are not toxicity-specific.

**What is *not* prominent.** There is *no* explicit-slur feature (the L4:F7545 "extremism/violence" feature is present with +0.079, but the subagent trace showed it is actually being driven by the subword tokens "big" + "ot" (i.e., the *word* "bigots" — the lexical surface), not by an abstract hate-speech concept; its top activating examples are genuine religious-extremism content. L4:F11580 "negative language and profanity" (+0.092) is similarly driven by the *literal tokens* "big" and "ot" rather than by a profanity concept: its top activated examples are FUCK/idiot/moron — none of which appear in this prompt. The promoted-token analysis confirms the abstract: even where a "profanity" feature is positively contributing, the prompt contains no profanity; the model is using a subword-lexical coincidence.

**Spurious-feature verdict.** The user is largely correct. The probe's classification rests on a **bag of identity/political-entity tokens** (trump, white, race, other, is, too, bigots-as-subwords) plus an American-politics supernode, rather than on any actual toxic semantics. The "profanity/extremism" features that *do* appear are lexical-surface fires on "big"/"ot" and "tie" (pos 1), not semantic fires on hateful content. Removing the entity names "Trump" and "white" from this prompt would suppress the dominant L4:F14582 / L6:F15063 / L0:F3436 / L4:F7136 / L4:F15204 / L3:F5475 supernodes, but the probe would still likely fire on the remaining generic "clearly shows… bigots" lexical pattern — i.e., the model has learned a shortcut where *named-political-entity + identity adjective + assertive adverb* triggers the toxicity probe, regardless of whether the surrounding text actually advocates harm.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 15 | L0: 'white' word detector (pos 15 & 25) |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 25 | L0: 'white' word detector (pos 15 & 25) |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F7969](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7969) | 14 | L0: 'other' word detector (pos 14) |  the word "other" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7969) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 6 | L0: 'is' word detector (pos 6) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F11603](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11603) | 31 | L0: 'too' word detector (pos 31) |  the word "too" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11603) |
| [L0:F7621](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7621) | 2 | L0: 'clearly'/'plainly' adverb detectors (pos 2) |  the word "clearly", and to a lesser extent words associated with amounts of things | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7621) |
| [L0:F7861](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7861) | 2 | L0: 'clearly'/'plainly' adverb detectors (pos 2) |  instances of the words "this", "these", "clearly", or "more". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7861) |
| [L0:F4422](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4422) | 2 | L0: 'clearly'/'plainly' adverb detectors (pos 2) | the word "seriously" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4422) |
| [L0:F12866](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12866) | 2 | L0: 'clearly'/'plainly' adverb detectors (pos 2) |  adverbs such as "clearly," "plainly," and "as" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12866) |
| [L1:F2407](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2407) | 2 | L1: 'clearly' in evidence/assertion sense (pos 2) |  the word "clearly" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2407) |
| [L1:F9761](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9761) | 2 | L1: 'clearly' in evidence/assertion sense (pos 2) |  language asserting that a statement is obvious, undisputed, or in accordance with a rule | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9761) |
| [L1:F13458](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13458) | 2 | L1: 'clearly' in evidence/assertion sense (pos 2) |  the word "clear" in legal contexts | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13458) |
| [L1:F15609](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15609) | 30 | L1: forms of 'come' (pos 30) |  various forms of the verb "to come" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15609) |
| [L2:F4507](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4507) | 5 | L2: Donald Trump / Hillary Clinton name (pos 5) |  mentions of Donald Trump, and occasionally of Hillary Clinton | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4507) |
| [L2:F14301](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14301) | 5 | L2: people/orgs in politics & finance (pos 5) |  names of people and organizations involved in politics, finance, and national security | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14301) |
| [L3:F5475](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5475) | 40 | L3: 'race' (pos 40) |  occurrences of the word "race" in different contexts | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5475) |
| [L3:F3136](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3136) | 5 | L3: Trump administration names (pos 5) |  names of people involved in the Trump administration | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3136) |
| [L4:F14582](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14582) | 5 | L4: White House / US government (pos 5) |  references to the White House and the US government | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14582) |
| [L4:F11580](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11580) | 9 | L4: negative language & profanity (pos 9) | negative language and swear words | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11580) |
| [L4:F7545](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7545) | 9 | L4: extremism / violence / hate-speech detector (pos 9) |  words or phrases relating to religious extremism, violence, and terrorism. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7545) |
| [L4:F15204](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) | 15 | L4: 'white' as color/White-House entity (pos 15) |  art galleries, museums and the White House | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) |
| [L4:F7136](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7136) | 15 | L4: 'white' as color/White-House entity (pos 15) |  the color white | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7136) |
| [L6:F15063](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15063) | 5 | L6: American politics / elections / politicians (pos 5) |  references to American politics, elections, and politicians | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15063) |
| [L6:F5753](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5753) | 5 | L6: political viewpoints & figures (pos 5) |  political viewpoints and associated figures | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5753) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:12866 de=-0.206 |
| 3 | `inspect_feature` ×20 | L0:12866, L0:7621, L4:14582, L0:4422, L0:11375, L0:15831, L0:7142, L0:164, L0:3916, L2:9199, L2:14301, L1:9761, L3:373, L0:3436, L0:7969, L0:7861, L0:5707, L2:15769, L4:11580, L4:2720 |
| 4 | `get_top_features` | 40 features; top: L0:12866 de=-0.206 |
| 5 | `inspect_feature` ×20 | L0:4517, L0:425, L0:13663, L3:3136, L1:2407, L0:2411, L6:15063, L4:7545, L6:1707, L4:15204, L0:6870, L4:8072, L6:5753, L1:1808, L4:7136, L0:8740, L1:13458, L0:247, L0:8444, L2:4507 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F15063@5` | ❌ error | — | — | Trace from L6:F15063 (American politics / elections / politicians). What input t… |
| SA-2 | `L4:F11580@9` | ✅ reported | 3 | 7 | Trace from L4:F11580 (negative language and swear words, with promoted tokens li… |
| SA-3 | `L4:F14582@5` | ❌ error | — | — | Trace from L4:F14582 (White House / US government). Which input tokens feed it (… |
| SA-4 | `L4:F7545@9` | ✅ reported | 7 | 10 | Trace from L4:F7545 (religious extremism / violence / terrorism). With promoted … |

<details>
<summary><b>SA-2</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F11580 | "negative language and swear words" |
| 2 | `get_upstream_features` | L4:F11580@9, k=10 | Emb:"ot"@9 (de=5.00) +9 more |
| 3 | `inspect_feature` | L0, F12712 | " words, suffixes, or phrases that could indicate quality and the peopl" |
| 4 | `get_upstream_features` | L2:F4520@9, k=10 | Emb:" big"@8 (de=9.06) +9 more |
| 5 | `get_upstream_features` | L0:F12712@9, k=10 | Emb:" big"@8 (de=12.44) +9 more |
| 6 | `inspect_feature` | L2, F4520 | " words related to newness or being an outsider" |
| 7 | `inspect_feature` | L0, F1432 | " the word "quality" and words associated with negative impacts" |
| 8 | `get_upstream_features` | L0:F1432@9, k=10 | Emb:" big"@8 (de=11.12) +9 more |

**Findings:** The target feature L4:F11580 is primarily a profanity/negative‑language detector. Its strongest positive drivers are the raw token embeddings for "ot" (the suffix of the negation word "not") and "big" (an intensifier). These embeddings feed directly into the target and also upstream through two low‑level lexical features (L2:4520 and L0:1432) that capture adjective/intensifier cues. The path reach…

</details>

<details>
<summary><b>SA-4</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F7545 | " words or phrases relating to religious extremism, violence, and terro" |
| 2 | `get_upstream_features` | L4:F7545@9, k=10 | Emb:"ot"@9 (de=2.50) +9 more |
| 3 | `inspect_feature` | L3, F15558 | " words that indicate feelings or qualities" |
| 4 | `get_upstream_features` | L3:F15558@9, k=10 | Emb:"ot"@9 (de=2.38) +9 more |
| 5 | `inspect_feature` | L0, F6628 | " superlative adjectives and nouns associated with a high degree of qua" |
| 6 | `inspect_feature` | L2, F4053 | " inflammatory hateful words, phrases, and names that attack groups of " |
| 7 | `inspect_feature` | L2, F964 | " words relating to sports teams, players, and performance" |
| 8 | `get_upstream_features` | L2:F964@9, k=10 | Emb:" big"@8 (de=6.28) +9 more |
| 9 | `get_upstream_features` | L0:F6628@9, k=10 | Emb:" big"@8 (de=9.56) +9 more |
| 10 | `get_upstream_features` | L2:F4053@9, k=10 | Emb:"ot"@9 (de=1.11) +9 more |

**Findings:** The L4:F7545 circuit, annotated as an extremist/terrorism detector, is being driven primarily by the input token embeddings for the subwords 'big' (pos8) and 'ot' (pos9) that compose the word 'bigots' in the prompt. These embeddings strongly excite a cascade of lower‑layer features: a hate‑speech detector (L2:F4053), an affective qualifier (L3:F15558), a superlative intensifier (L0:F6628), and eve…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F14582@5, k=15 → Emb:" trump"@5 (de=18.12) +14 more |
| 2 | `get_upstream_features` | L0:F11375@6, k=15 → Emb:" is"@6 (de=31.38) +14 more |
| 3 | `get_upstream_features` | L0:F3436@15, k=15 → Emb:" white"@15 (de=18.12) +14 more |
| 4 | `get_upstream_features` | L0:F7969@14, k=15 → Emb:" other"@14 (de=42.25) +14 more |
| 5 | `get_upstream_features` | L4:F11580@9, k=15 → Emb:"ot"@9 (de=5.00) +14 more |
| 6 | `get_upstream_features` | L4:F7545@9, k=15 → Emb:"ot"@9 (de=2.50) +14 more |
| 7 | `get_upstream_features` | L6:F15063@5, k=15 → Emb:" trump"@5 (de=12.75) +14 more |
| 8 | `get_upstream_features` | L2:F14301@5, k=10 → Emb:" trump"@5 (de=9.44) +9 more |
| 9 | `get_upstream_features` | L3:F3136@5, k=10 → Emb:" trump"@5 (de=10.62) +9 more |
| 10 | `get_upstream_features` | L4:F15204@15, k=10 → Emb:" white"@15 (de=40.75) +9 more |
| 11 | `get_upstream_features` | L4:F7136@15, k=10 → Emb:" white"@15 (de=43.50) +9 more |
| 12 | `get_upstream_features` | L2:F4507@5, k=10 → Emb:" trump"@5 (de=17.88) +9 more |
| 13 | `get_upstream_features` | L6:F1707@1, k=10 → L4:F8223 (de=4.09) +9 more |
| 14 | `get_upstream_features` | L0:F712@1, k=10 → ❌ Feature (layer=0, pos=1, feature_idx=712) not found in graph |
| 15 | `get_top_features` | token="", k=60 → 60 features; top: L0:12866 de=-0.206 |
| 16 | `get_upstream_features` | L0:F11603@31, k=10 → Emb:" too"@31 (de=32.50) +9 more |
| 17 | `inspect_feature` ×4 | L0:11603, L0:9062, L3:5475, L1:15609 |
| 18 | `get_upstream_features` | L3:F5475@40, k=10 → Emb:" race"@40 (de=22.12) +9 more |
| 19 | `get_upstream_features` | L0:F9062@19, k=10 → Emb:"."@18 (de=15.44) +9 more |
| 20 | `get_upstream_features` | L1:F15609@30, k=10 → Emb:" came"@30 (de=23.12) +9 more |
| 21 | `get_upstream_features` | L0:F3436@25, k=10 → Emb:" white"@25 (de=18.25) +9 more |
| 22 | `get_upstream_features` | L6:F5753@5, k=10 → Emb:" trump"@5 (de=7.25) +9 more |
| 23 | `get_upstream_features` | L4:F5323@5, k=10 → Emb:" trump"@5 (de=3.41) +9 more |
| 24 | `get_upstream_features` | L0:F3916@1, k=10 → Emb:"<bos>"@0 (de=8.94) +9 more |
| 25 | `get_upstream_features` | L3:F373@1, k=10 → Emb:"<bos>"@0 (de=26.25) +9 more |

### Build

`build_circuit` → 29 nodes, 40 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 183,394 | 8,960 | 629,169 | 0 | $0.1035 | — | — |
| SA-4 | openai/gpt-oss-120b | 118,427 | 6,176 | 2,592 | 0 | $0.0215 | ✅ 7F/10E | Trace from L4:F7545 (religious extremism / violence / terror… |
| SA-2 | openai/gpt-oss-120b | 91,891 | 6,754 | 2,528 | 0 | $0.0179 | ✅ 3F/7E | Trace from L4:F11580 (negative language and swear words, wit… |
| **Total** | | **393,712** | **21,890** | **634,289** | **0** | **$0.1429** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 29s