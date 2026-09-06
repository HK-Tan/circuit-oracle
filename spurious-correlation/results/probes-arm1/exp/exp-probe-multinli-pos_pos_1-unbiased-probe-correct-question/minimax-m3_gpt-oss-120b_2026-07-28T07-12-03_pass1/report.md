# Circuit Oracle Report
**Date:** 2026-07-28 07:12:03 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "contradiction" classification is driven by *entity-content* features (conspiracy-theorist terminology, financial/payment entities, technology) extracted from the prompt's named entities, NOT by generic "negation word" signals.

**Confidence:** 8

**Reasoning:** The circuit traces from the probe direction back through three supernodes that feed the late-layer entity detectors. At the bottom, token embeddings (Cons pos 1, piracy pos 2, theorists pos 3, Master pos 5, Card pos 6, is pos 7, investing pos 8, that pos 12, chip pos 11) feed layer-0 lexical detectors (sn_lexical_low) — including the "cons"-prefix detector (L0:F16015, activation 16.25, frac_nonzero 0.015), the function-word "is" (L0:F11375), the word "that" (L0:F3635), and the word "invest" (L1:F8696, frac_nonzero 0.0022). These are not generic negation cues; they are content-specific lexical fragments.

The next tier is the entity-content detector supernode (sn_money_chip_detectors): L4:F4153 ("currency and banking transactions", activation 15.6), L4:F1248 ("brand names of companies"), L2:F15808 ("credit cards and payment"), L2:F10189 ("payment and financial information especially credit cards"), L6:F10419 ("technology and access-related terms"), L4:F9976 ("computer hardware and software"). These are driven by the *MasterCard* brand and the *chip* entity (e.g., L4:F4153 gets direct_effect 11.06 from "Card" embedding).

Above them sit semantic-concept detectors (sn_semantic_conspiracy): L3:F9739 ("words related to conspiracies", direct_effect -0.35 on probe, firing on "piracy"), L1:F13684 ("the word 'theory'"), L2:F16028 ("speculation, lies, false information, conspiracy theories"), L7:F2730 ("rumors"), L7:F13859 ("legal documents, pro se"), L4:F5181 ("political parties or ideologies"), L5:F8329 ("hearsay, gossip, predictions"). The L3:F9739 path is anchored by L2 fragment detectors (L2:F1741 "ction/notes fragments", L2:F16241 "constructor/dering fragments", L2:F11313 "cent/consu substrings") that all light up on the *conspiracy* subword pieces.

The final-tier supernode (sn_conspiracy_financial_entity) contains L8:F12761 ("QAnon conspiracy theory" — activation 22.1, fires on "theorists") and L7:F1062 ("credit cards, loans, gambling, money" — activation 27.1, fires on "Master" and on "card"). These are the strongest output drivers. The financial-entity signal is INHIBITORY (L7:F1062 direct_effect -0.24) on the probe, while the conspiracy-theory signal is also mildly inhibitory (-0.16) — but the negative weight is consistent across both the named entity detectors and the L3 conspiracy detector, meaning the probe direction treats their co-occurrence as a contradiction signature.

**Addressing the user concern:** The circuit is NOT relying on spurious negation-word features. There is no "no", "not", "n't", or "nothing"-style detector among the top features. The most "function-word-looking" features (L0:F3635 "that", L0:F11375 "is", L0:F8444 "to", L1:F8696 "invest") are present but their direct_effects on the probe (0.22, 0.15, 0.13, 0.14) are smaller than those of the entity-content features. The dominant features are clearly entity-semantic: conspiracy-theorist terminology and the MasterCard/financial-entity pattern. The mechanism is the *co-presence* of the *Conspiracy theorists* framing with the *MasterCard* financial entity — a real content-level contradiction signal — not a generic negation heuristic. That said, the financial-entity detector L7:F1062 fires with a relatively generic "Master" prompt (not specific to this exact entity), and several of the early-layer features are subword-prefix detectors (L0:F16015 "cons-") that will activate on any "cons*" word, so there is some lexical-surface-level generalization rather than deep entity-specificity. The user's worry about spurious negation features is not supported by this circuit, but the circuit does show a mix of entity-specific and lexical-substring features.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L8:F12761](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/12761) | 3 | Entity-specific late-layer features (conspiracy theory + financial entity) |  words associated with the QAnon conspiracy theory | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/12761) |
| [L7:F1062](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1062) | 6 | Entity-specific late-layer features (conspiracy theory + financial entity) |  words and phrases related to credit cards, loans, spending, gambling, and money in general. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1062) |
| [L7:F1062](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1062) | 11 | Entity-specific late-layer features (conspiracy theory + financial entity) |  words and phrases related to credit cards, loans, spending, gambling, and money in general. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1062) |
| [L3:F9739](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9739) | 2 | Semantic content detectors (conspiracy/chip/theory) |  words related to conspiracies | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9739) |
| [L2:F16230](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16230) | 11 | Semantic content detectors (conspiracy/chip/theory) |  mentions of semiconductor chips and devices | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16230) |
| [L1:F13684](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13684) | 3 | Semantic content detectors (conspiracy/chip/theory) |  the word "theory" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13684) |
| [L1:F8696](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8696) | 8 | Semantic content detectors (conspiracy/chip/theory) |  the word "invest" and its derivatives | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8696) |
| [L2:F16028](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16028) | 3 | Semantic content detectors (conspiracy/chip/theory) |  terms related to speculation, lies, false information, and conspiracy theories | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16028) |
| [L7:F2730](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2730) | 3 | Semantic content detectors (conspiracy/chip/theory) |  mentions of rumors and reports | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2730) |
| [L7:F13859](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13859) | 3 | Semantic content detectors (conspiracy/chip/theory) |  legal documents, especially ones related to people representing themselves | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13859) |
| [L4:F5181](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5181) | 3 | Semantic content detectors (conspiracy/chip/theory) |  terms relating to political parties or ideologies | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5181) |
| [L5:F8329](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/8329) | 3 | Semantic content detectors (conspiracy/chip/theory) |  words indicating hearsay, gossip, or predictions about the future, often followed by "that." | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/8329) |
| [L7:F382](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/382) | 3 | Semantic content detectors (conspiracy/chip/theory) |  words related to discovering information | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/382) |
| [L2:F1741](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1741) | 2 | Conspiracy fragment detectors (piracy, cons prefix, Conspiracy theory fragments) | fragments of words ending in "ction", "notes," or "ual." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1741) |
| [L2:F16241](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16241) | 2 | Conspiracy fragment detectors (piracy, cons prefix, Conspiracy theory fragments) |  partial strings of the word "constructor" or words ending in "dering" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16241) |
| [L2:F11313](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11313) | 2 | Conspiracy fragment detectors (piracy, cons prefix, Conspiracy theory fragments) | words containing the "cent" or "consu" substrings | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11313) |
| [L2:F7100](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7100) | 3 | Conspiracy fragment detectors (piracy, cons prefix, Conspiracy theory fragments) |  words denoting people/groups involved in politics/occupations/status | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7100) |
| [L2:F2988](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2988) | 3 | Conspiracy fragment detectors (piracy, cons prefix, Conspiracy theory fragments) |  words related to searching, research, or investigation | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2988) |
| [L2:F13362](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13362) | 11 | Conspiracy fragment detectors (piracy, cons prefix, Conspiracy theory fragments) |  terms related to identification, security, and access | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13362) |
| [L4:F4153](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4153) | 6 | Money/card/chip/brand detectors |  words or phrases related to currency and banking transactions | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4153) |
| [L4:F1248](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1248) | 6 | Money/card/chip/brand detectors |  brand names of companies or products | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1248) |
| [L2:F15808](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15808) | 6 | Money/card/chip/brand detectors | mentions of credit cards and payment. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15808) |
| [L2:F10189](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10189) | 6 | Money/card/chip/brand detectors | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10189) |
| [L6:F10419](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10419) | 11 | Money/card/chip/brand detectors | technology and access-related terms across multiple contexts. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10419) |
| [L4:F9976](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9976) | 11 | Money/card/chip/brand detectors |  technical words related to computer hardware and software | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9976) |
| [L1:F6066](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6066) | 11 | Money/card/chip/brand detectors |  the word 'chip', possibly in the context of hardware | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6066) |
| [L0:F16015](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16015) | 1 | Low-level lexical features (function words, prefixes, subwords) | the prefix "cons" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16015) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 7 | Low-level lexical features (function words, prefixes, subwords) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F3635](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) | 12 | Low-level lexical features (function words, prefixes, subwords) | the word "that" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) |
| [L0:F4287](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4287) | 1 | Low-level lexical features (function words, prefixes, subwords) |  words or phrases that relate to marketing or advertising | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4287) |
| [L0:F939](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/939) | 8 | Low-level lexical features (function words, prefixes, subwords) | verbs related to cognitive or recreational activities | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/939) |
| [L0:F4802](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4802) | 4 | Low-level lexical features (function words, prefixes, subwords) |  large blocks of whitespace and numbers | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4802) |
| [L0:F12377](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12377) | 4 | Low-level lexical features (function words, prefixes, subwords) |  large gaps of whitespace | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12377) |
| [L0:F15958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15958) | 3 | Low-level lexical features (function words, prefixes, subwords) |  the word "tomorrow" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15958) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 24 | Low-level lexical features (function words, prefixes, subwords) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F3937](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3937) | 11 | Low-level lexical features (function words, prefixes, subwords) |  the phrase "from scratch", sometimes activating on words nearby | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3937) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L3:9739 de=-0.348 |
| 3 | `inspect_feature` ×19 | L3:9739, L2:16230, L7:1062, L0:3635, L1:13684, L4:1602, L0:16015, L2:16241, L0:4287, L8:12761, L0:15958, L0:11375, L1:8696, L0:4802, L2:15808, L0:12377, L0:3937, L0:8444, L1:9693 |
| 4 | `get_top_features` | 20 features; top: L3:9739 de=-0.348 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L3:F9739@2` | ✅ reported | 5 | 6 | Trace the path upstream from L3:F9739 (conspiracy-related words, position 2 = "s… |
| SA-2 | `L2:F16230@11` | ✅ reported | 3 | 2 | Trace the path upstream from L2:F16230 (semiconductor chip mentions, position 11… |
| SA-3 | `L7:F1062@6` | ✅ reported | 4 | 5 | Trace the path upstream from L7:F1062 (credit card/loans/money detector, positio… |
| SA-4 | `L0:F3635@12` | ❌ error | — | — | Trace the path upstream from L0:F3635 (the word "that", position 12 = "that" in … |

<details>
<summary><b>SA-1</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F9739 | " words related to conspiracies" |
| 2 | `get_upstream_features` | L3:F9739@2, k=10 | Emb:"Cons"@1 (de=8.75) +9 more |
| 3 | `inspect_feature` | L2, F1741 | "fragments of words ending in "ction", "notes," or "ual."" |
| 4 | `inspect_feature` | L2, F16241 | " partial strings of the word "constructor" or words ending in "dering"" |
| 5 | `inspect_feature` | L2, F11313 | "words containing the "cent" or "consu" substrings" |
| 6 | `get_upstream_features` | L2:F1741@2, k=10 | Emb:"Cons"@1 (de=22.88) +9 more |
| 7 | `get_upstream_features` | L2:F16241@2, k=10 | Emb:"Cons"@1 (de=17.25) +9 more |
| 8 | `get_upstream_features` | L2:F11313@2, k=10 | Emb:"Cons"@1 (de=21.25) +9 more |
| 9 | `inspect_feature` | L0, F11835 | "terms used in software code such as "assembly", "using", "namespace", " |
| 10 | `inspect_feature` | L0, F16015 | "the prefix "cons"" |
| 11 | `get_upstream_features` | L2:F1741@2, k=10 | Emb:"Cons"@1 (de=22.88) +9 more |
| 12 | `inspect_feature` | L0, F538 | " words within scientific texts about chemical and biological function," |
| 13 | `get_upstream_features` | L0:F16015@1, k=10 | Emb:"Cons"@1 (de=21.12) +9 more |
| 14 | `inspect_feature` | L1, F13148 | " code snippets or HTML" |

**Findings:** The conspiracy detector (L3:F9739) is driven primarily by the raw embeddings for the surrounding tokens "Cons" and "piracy". Those embeddings feed into three mid‑layer fragment detectors (L2:F1741, L2:F16241, L2:F11313), each capturing suffixes, interior fragments, or substrings that together reconstruct the full conspiracy word. All three receive support from the prefix detector (L0:F16015) which…

</details>

<details>
<summary><b>SA-2</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F16230 | " mentions of semiconductor chips and devices" |
| 2 | `get_upstream_features` | L2:F16230@11, k=10 | Emb:" chip"@11 (de=27.00) +9 more |
| 3 | `inspect_feature` | L1, F6066 | " the word 'chip', possibly in the context of hardware" |
| 4 | `inspect_feature` | L0, F351 | " the word "expert"" |
| 5 | `get_upstream_features` | L1:F6066@11, k=10 | Emb:" chip"@11 (de=21.38) +9 more |
| 6 | `get_upstream_features` | L0:F351@11, k=10 | Emb:" chip"@11 (de=19.25) +9 more |
| 7 | `inspect_feature` | L0, F3937 | " the phrase "from scratch", sometimes activating on words nearby" |

**Findings:** Tracing upstream from L2:F16230 (layer 2, position 11) revealed that its strongest positive upstream driver is the raw token embedding for " chip" (direct_effect ≈ 27), which resides at the input layer. The next most influential upstream features are a layer‑1 chip‑word detector (F6066, direct_effect 0.75) and a layer‑0 generic token detector for "expert" (F351, direct_effect 0.4141). Both of thes…

</details>

<details>
<summary><b>SA-3</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F1062 | " words and phrases related to credit cards, loans, spending, gambling," |
| 2 | `get_upstream_features` | L7:F1062@6, k=10 | Emb:"Card"@6 (de=14.00) +9 more |
| 3 | `inspect_feature` | L6, F10189 | " phrases related to payment and financial information (especially cred" |
| 4 | `get_upstream_features` | L6:F10189@6, k=10 | Emb:"Card"@6 (de=13.31) +9 more |
| 5 | `inspect_feature` | L4, F4153 | " words or phrases related to currency and banking transactions" |
| 6 | `get_upstream_features` | L4:F4153@6, k=10 | Emb:"Card"@6 (de=11.06) +9 more |
| 7 | `inspect_feature` | L4, F1248 | " brand names of companies or products" |

**Findings:** The financial‑entity detector (L7:F1062) is driven primarily by the token embedding for "Card" (positive direct effect 14.0). Upstream, the strongest feature is L6:F10189, a payment‑information detector, which itself receives strong excitation from the same "Card" embedding and a smaller contribution from the "Master" token. L4:F4153 (currency/banking terms) and L4:F1248 (brand names) also feed in…

</details>

### Re-dispatch (round 2): 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-5 | `L8:F12761@3` | ✅ reported | 5 | 11 | Trace the path upstream from L8:F12761 (QAnon/conspiracy theory words, position … |
| SA-6 | `L1:F13684@3` | ❌ error | — | — | Trace the path upstream from L1:F13684 (the word "theory", position 3 = "theoris… |
| SA-7 | `L0:F16015@1` | ❌ error | — | — | Trace the path upstream from L0:F16015 (the prefix "cons", position 1 = "Cons" i… |
| SA-8 | `L0:F11375@7` | ❌ error | — | — | Trace the path upstream from L0:F11375 (the word "is", position 7 = "is"). Find … |
| SA-9 | `L1:F8696@8` | ✅ reported | 5 | 4 | Trace the path upstream from L1:F8696 (the word "invest" and its derivatives, po… |

<details>
<summary><b>SA-5</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L8, F12761 | " words associated with the QAnon conspiracy theory" |
| 2 | `get_upstream_features` | L8:F12761@3, k=10 | Emb:" theorists"@3 (de=4.56) +9 more |
| 3 | `inspect_feature` | L2, F16028 | " terms related to speculation, lies, false information, and conspiracy" |
| 4 | `inspect_feature` | L7, F13859 | " legal documents, especially ones related to people representing thems" |
| 5 | `inspect_feature` | L7, F2730 | " mentions of rumors and reports" |
| 6 | `get_upstream_features` | L2:F16028@3, k=10 | Emb:" theorists"@3 (de=11.75) +9 more |
| 7 | `get_upstream_features` | L7:F13859@3, k=10 | Emb:"piracy"@2 (de=5.22) +9 more |
| 8 | `inspect_feature` | L7, F2730 | " mentions of rumors and reports" |
| 9 | `inspect_feature` | L7, F382 | " words related to discovering information" |

**Findings:** The QAnon/conspiracy‑theory detector (L8:F12761) is chiefly driven by low‑frequency speculative language (L2:F16028) and rumor‑related signals (L7:F2730, L7:F13859). All major upstream paths originate from raw token embeddings for "theorists" and "piracy", satisfying the requirement to reach a lower‑third layer embedding. The traced circuit reveals how conspiracy‑theory wording is assembled from t…

</details>

<details>
<summary><b>SA-9</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F8696 | " the word "invest" and its derivatives" |
| 2 | `get_upstream_features` | L1:F8696@8, k=10 | Emb:" investing"@8 (de=21.88) +9 more |
| 3 | `inspect_feature` | L0, F939 | "verbs related to cognitive or recreational activities" |
| 4 | `inspect_feature` | L0, F5939 | "mentions of errors in code" |
| 5 | `get_upstream_features` | L0:F939@8, k=10 | Emb:" investing"@8 (de=9.69) +9 more |
| 6 | `inspect_feature` | L0, F4053 | " references to money and illegal activities" |
| 7 | `inspect_feature` | L0, F11835 | "terms used in software code such as "assembly", "using", "namespace", " |
| 8 | `get_upstream_features` | L0:F5939@8, k=10 | Emb:" investing"@8 (de=13.06) +9 more |
| 9 | `inspect_feature` | L0, F4053 | " references to money and illegal activities" |

**Findings:** The L1 feature 8696 that flags the word "invest" receives its strongest excitatory input from four layer‑0 features: 939 (verb form detector), 5939 (pattern detector that activates on '-ing' tokens), 4053 (financial‑money detector), and 11835 (code‑term detector). Feature 4053 is especially notable because it explicitly tracks money‑related language, a key component of policy‑sensitive handling of…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F3635@12, k=10 → Emb:" that"@12 (de=41.00) +9 more |
| 2 | `get_upstream_features` | L7:F1062@11, k=10 → Emb:"Card"@6 (de=7.31) +9 more |
| 3 | `get_upstream_features` | L6:F10189@6, k=10 → Emb:"Card"@6 (de=13.31) +9 more |
| 4 | `get_upstream_features` | L4:F4153@6, k=8 → Emb:"Card"@6 (de=11.06) +7 more |
| 5 | `inspect_feature` ×9 | L2:1741, L2:11313, L1:6066, L6:10419, L6:10189, L4:1248, L4:4153, L2:15808, L2:13362 |
| 6 | `get_upstream_features` | L0:F16015@1, k=5 → Emb:"Cons"@1 (de=21.12) +4 more |
| 7 | `get_upstream_features` | L0:F11375@7, k=5 → Emb:" is"@7 (de=31.38) +4 more |
| 8 | `get_upstream_features` | L1:F8696@8, k=5 → Emb:" investing"@8 (de=21.88) +4 more |
| 9 | `get_upstream_features` | L2:F16028@3, k=5 → Emb:" theorists"@3 (de=11.75) +4 more |
| 10 | `get_upstream_features` | L1:F6066@11, k=5 → Emb:" chip"@11 (de=21.38) +4 more |
| 11 | `get_upstream_features` | L4:F1248@6, k=5 → Emb:"Master"@5 (de=3.33) +4 more |
| 12 | `get_upstream_features` | L4:F4153@6, k=5 → Emb:"Card"@6 (de=11.06) +4 more |
| 13 | `get_upstream_features` | L2:F15808@6, k=5 → Emb:"Card"@6 (de=6.09) +4 more |
| 14 | `get_upstream_features` | L3:F9739@2, k=5 → Emb:"Cons"@1 (de=8.75) +4 more |
| 15 | `get_upstream_features` | L2:F1741@2, k=5 → Emb:"Cons"@1 (de=22.88) +4 more |
| 16 | `get_upstream_features` | L2:F16241@2, k=5 → Emb:"Cons"@1 (de=17.25) +4 more |
| 17 | `get_upstream_features` | L2:F11313@2, k=5 → Emb:"Cons"@1 (de=21.25) +4 more |
| 18 | `get_upstream_features` | L2:F16230@11, k=5 → Emb:" chip"@11 (de=27.00) +4 more |
| 19 | `get_upstream_features` | L6:F10189@6, k=5 → Emb:"Card"@6 (de=13.31) +4 more |
| 20 | `get_upstream_features` | L8:F12761@3, k=5 → Emb:" theorists"@3 (de=4.56) +4 more |
| 21 | `inspect_feature` ×9 | L2:16028, L7:13859, L7:2730, L3:3595, L2:7725, L6:6539, L3:8417, L4:5181, L5:8329 |
| 22 | `get_upstream_features` | L7:F1062@11, k=5 → Emb:"Card"@6 (de=7.31) +4 more |
| 23 | `get_upstream_features` | L4:F1602@3, k=5 → Emb:" theorists"@3 (de=3.23) +4 more |
| 24 | `get_upstream_features` | L8:F12761@3, k=5 → Emb:" theorists"@3 (de=4.56) +4 more |
| 25 | `get_upstream_features` | L6:F10419@11, k=5 → Emb:" chip"@11 (de=13.69) +4 more |
| 26 | `inspect_feature` ×10 | L4:1602, L2:7100, L2:2988, L3:5808, L7:382, L4:9976, L2:1124, L2:12409, L0:2115, L4:5181 |
| 27 | `get_source_influence` | {'depth': 3, 'source_positions': [2, 3]} → {'depth': 3, 'source_positions': [2, 3], 'S_pct_of_total': -12.309, 'R_pct_of_to |
| 28 | `get_upstream_features` | L4:F1602@3, k=5 → Emb:" theorists"@3 (de=3.23) +4 more |
| 29 | `inspect_feature` ×3 | L4:1602, L4:5181, L5:8329 |

### Build

`build_circuit` → 15 nodes, 15 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 125,378 | 8,094 | 828,372 | 0 | $0.0970 | — | — |
| SA-2 | openai/gpt-oss-120b | 73,504 | 4,668 | 5,856 | 0 | $0.0139 | ✅ 3F/2E | Trace the path upstream from L2:F16230 (semiconductor chip m… |
| SA-1 | openai/gpt-oss-120b | 143,196 | 10,781 | 68,096 | 0 | $0.0290 | ✅ 5F/6E | Trace the path upstream from L3:F9739 (conspiracy-related wo… |
| SA-3 | openai/gpt-oss-120b | 60,095 | 4,742 | 5,184 | 0 | $0.0119 | ✅ 4F/5E | Trace the path upstream from L7:F1062 (credit card/loans/mon… |
| SA-5 | openai/gpt-oss-120b | 89,426 | 7,839 | 34,336 | 0 | $0.0186 | ✅ 5F/11E | Trace the path upstream from L8:F12761 (QAnon/conspiracy the… |
| SA-9 | openai/gpt-oss-120b | 108,128 | 6,880 | 13,088 | 0 | $0.0205 | ✅ 5F/4E | Trace the path upstream from L1:F8696 (the word "invest" and… |
| **Total** | | **599,727** | **43,004** | **954,932** | **0** | **$0.1910** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 8m 30s