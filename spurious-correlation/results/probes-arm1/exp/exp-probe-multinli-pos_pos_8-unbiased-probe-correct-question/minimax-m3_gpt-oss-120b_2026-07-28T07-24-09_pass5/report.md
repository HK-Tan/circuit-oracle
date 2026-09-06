# Circuit Oracle Report
**Date:** 2026-07-28 07:24:09 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_8 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "contradiction" score is driven by a mixture of (a) genuine topical features detecting that the premise is about the U.S. Congress and the verb "include," and (b) highly generic function-word/relative-clause features (the word "which," commas, "to" after a verb, "include," generic hair/pronoun features) — exactly the kind of spurious surface signals the user flagged.

**Confidence:** 6

**Reasoning:** The top positive contributors to the probe (in the top_features list) are L2:F2701 "U.S. Congress words" (+0.85, activation 22.25, frac_nonzero 0.011), L3:F5753 "the word 'includes'" (+0.53, frac 0.002), L0:F15411 political bodies (+0.49, frac 0.008), L0:F6044 "yield" (+0.49), and L4:F59 "to preceded by verb/start/begin" (+0.41, frac 0.020). Tracing them upstream, the Congress-style features cleanly chain to the `Emb: Congress (pos 2)` token (direct_effect 28.1 on L2:F2701, 20.6 on L3:F123, 9.1 on L2:F6735) — so the L0→L3 "Congress/political-body" supernode *is* tied to a real input token and looks like legitimate topical evidence. However, several other large positive features are the kind the user worried about: L0:F13564 (the word "which", frac 0.017, pos 4), L0:F8444 ("to", pos 11, frac 0.017), L0:F195/L0:F13437 ("who", pos 15, frac 0.0017/0.013), L0:F10783 ("include", pos 12, frac 0.007), L0:F10536 ("approved"/governing bodies, pos 12, frac 0.009), L0:F11640 ("multi", pos 7, frac 0.017), L0:F10401 ("genes", pos 2, frac 0.017), and L4:F7775 "various forms of punctuation" (pos 9, frac 0.011) — i.e., **function words, the "to" infinitive, commas, and polysemantic lookalikes** (genes/clean/hair/multi firing incidentally at the "Congress" position) that don't encode premise-vs-hypothesis content at all. Their high *activation* but tiny frac_nonzero means they are extremely specific to surface form, not semantics, and they fire because the premise happens to use a relative-clause "which" + "began to include" structure. The negative-side features (L0:F10401 genes, L0:F3204 proper nouns, L0:F9557 "clean", L0:F13417 military, L1:F4224 "registration", L3:F8351 "include" code-symbol, L2:F6735 political parties at pos 2) **suppress** the probe — they're competing polysemantic detectors at the same "Congress" position that pull the residual stream away from the "contradiction" direction. So the user's concern is confirmed: the circuit is *not* a clean semantic contradiction detector. It is dominated by (i) a legitimate-looking but partly surface-driven "this is about Congress and uses 'include'" path, and (ii) several function-word/punctuation/generic features ("which", "to", "began to", commas, "include" as a generic word, plus incidental gensym/clean/registration lookalikes) that ride on top of the same residual stream. The probe classification is real (these features sum to a large net effect), but the mechanism mixes topical content with surface-form artifacts of the premise's syntax — exactly the "spurious negation/function-word" failure mode the user described.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: Congress (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: include (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: began (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 11 | Emb: to (pos 11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: , (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: which (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: who (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F10198](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10198) | 2 | L0: 'Congress' word + U.S. Congress/Congress political context |  the word "Congress" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10198) |
| [L0:F15411](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15411) | 2 | L0: 'Congress' word + U.S. Congress/Congress political context |  terms relating to political bodies, figures, and processes | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15411) |
| [L0:F6044](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) | 2 | L0: 'Congress' word + U.S. Congress/Congress political context | the word "yield" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) |
| [L0:F14565](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14565) | 2 | L0: 'Congress' word + U.S. Congress/Congress political context | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14565) |
| [L0:F12456](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12456) | 2 | L0: 'Congress' word + U.S. Congress/Congress political context | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12456) |
| [L0:F2089](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2089) | 2 | L0: 'Congress' word + U.S. Congress/Congress political context | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2089) |
| [L0:F13168](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13168) | 2 | L0: 'Congress' word + U.S. Congress/Congress political context | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13168) |
| [L0:F767](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/767) | 2 | L0: 'Congress' word + U.S. Congress/Congress political context | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/767) |
| [L0:F4476](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4476) | 2 | L0: 'Congress' word + U.S. Congress/Congress political context |  mentions of personal pronouns and hair | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4476) |
| [L0:F3231](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3231) | 2 | L0: 'Congress' word + U.S. Congress/Congress political context | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3231) |
| [L0:F10401](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10401) | 2 | L0: anti-political entity features (genes/pronouns, suppress probe) |  mentions of genes and proteins | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10401) |
| [L0:F3204](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3204) | 2 | L0: anti-political entity features (genes/pronouns, suppress probe) |  proper nouns, especially including titles of works and organizations | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3204) |
| [L0:F9557](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9557) | 2 | L0: anti-political entity features (genes/pronouns, suppress probe) | the word "clean" and words/phrases associated with people | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9557) |
| [L0:F13417](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13417) | 2 | L0: anti-political entity features (genes/pronouns, suppress probe) | mentions of the military, or occasionally other types of conflict | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13417) |
| [L1:F2089](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2089) | 2 | L1: Congress / political-body / constructor polysemantic features |  mentions of `constructor` or `congress` | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2089) |
| [L1:F14565](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14565) | 2 | L1: Congress / political-body / constructor polysemantic features |  locations, government positions, and organizations | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14565) |
| [L1:F12456](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12456) | 2 | L1: Congress / political-body / constructor polysemantic features |  names of organizations, particularly governmental or religious institutions, especially of Indian origin. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12456) |
| [L1:F14850](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14850) | 2 | L1: Congress / political-body / constructor polysemantic features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14850) |
| [L1:F14217](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14217) | 2 | L1: Congress / political-body / constructor polysemantic features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14217) |
| [L1:F3231](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3231) | 2 | L1: Congress / political-body / constructor polysemantic features |  discussions of political unrest and curfews in districts | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3231) |
| [L1:F9361](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9361) | 2 | L1: Congress / political-body / constructor polysemantic features |  proper nouns and place names, especially those related to India | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9361) |
| [L1:F3276](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3276) | 2 | L1: Congress / political-body / constructor polysemantic features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3276) |
| [L2:F2701](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) | 2 | L2: U.S. Congress/legislative-body features (pos 2) |  words related to the U.S. Congress | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) |
| [L2:F6735](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6735) | 2 | L2: U.S. Congress/legislative-body features (pos 2) |  political parties and politicians | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6735) |
| [L3:F123](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/123) | 2 | L3: U.S. Congress mention + 'include(s)' word features |  mentions of the United States Congress | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/123) |
| [L3:F5753](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5753) | 12 | L3: U.S. Congress mention + 'include(s)' word features |  the word "includes" or "containing". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5753) |
| [L3:F8351](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8351) | 12 | L3: U.S. Congress mention + 'include(s)' word features |  words related to including and code language symbols | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8351) |
| [L0:F13564](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13564) | 4 | L0: 'which' / relative-clause + generic-function-word features | the word "which" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13564) |
| [L0:F195](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/195) | 15 | L0: 'which' / relative-clause + generic-function-word features | the word "who" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/195) |
| [L0:F10783](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10783) | 12 | L0: 'which' / relative-clause + generic-function-word features |  the word "include" (and variations of the word) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10783) |
| [L0:F13437](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13437) | 15 | L0: 'which' / relative-clause + generic-function-word features | the word "who" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13437) |
| [L0:F11640](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11640) | 7 | L0: 'which' / relative-clause + generic-function-word features | the word "multi" and words that commonly occur with "multi" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11640) |
| [L0:F10536](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10536) | 12 | L0: 'which' / relative-clause + generic-function-word features |  the word "approved" and words related to governing bodies | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10536) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 11 | L0: 'which' / relative-clause + generic-function-word features | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L2:F11469](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11469) | 11 | L2: 'began'/'to'/punctuation surrounding verbs |  the word "to" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11469) |
| [L2:F11734](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11734) | 9 | L2: 'began'/'to'/punctuation surrounding verbs |  phrases containing punctuation such as quotes and dashes | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11734) |
| [L2:F4680](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4680) | 9 | L2: 'began'/'to'/punctuation surrounding verbs | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4680) |
| [L2:F6493](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6493) | 9 | L2: 'began'/'to'/punctuation surrounding verbs | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6493) |
| [L2:F7279](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7279) | 5 | L2: 'began'/'to'/punctuation surrounding verbs |  forms of the word "control" and words related to rulers | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7279) |
| [L3:F12596](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12596) | 11 | L3: 'to' followed by action/method feature |  actions or methods, sometimes preceeded by the preposition 'a' or 'to'. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12596) |
| [L3:F4374](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4374) | 11 | L3: 'to' followed by action/method feature | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4374) |
| [L3:F1124](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1124) | 11 | L3: 'to' followed by action/method feature | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1124) |
| [L3:F7499](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7499) | 11 | L3: 'to' followed by action/method feature | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7499) |
| [L3:F13272](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13272) | 11 | L3: 'to' followed by action/method feature | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13272) |
| [L3:F3658](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3658) | 11 | L3: 'to' followed by action/method feature | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3658) |
| [L3:F2392](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2392) | 11 | L3: 'to' followed by action/method feature | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2392) |
| [L3:F5506](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5506) | 11 | L3: 'to' followed by action/method feature | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5506) |
| [L3:F10633](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10633) | 3 | L3: 'to' followed by action/method feature | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10633) |
| [L3:F10633](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10633) | 4 | L3: 'to' followed by action/method feature | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10633) |
| [L4:F59](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/59) | 11 | L4: 'to' preceded by verb/start/begin phrases |  phrases with the word 'to' preceded by a verb or the word 'start' or 'begin'. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/59) |
| [L4:F7775](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7775) | 9 | L4: 'to' preceded by verb/start/begin phrases |  various forms of punctuation | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7775) |
| [L1:F4224](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4224) | 2 | L1: registration/Indian-org features (inhibit probe at pos 2) |  the word "registration" and its variations | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4224) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L2:2701 de=0.848 |
| 3 | `inspect_feature` ×5 | L2:2701, L3:5753, L0:6044, L0:15411, L4:59 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F2701@2` | ❌ error | — | — | Trace upstream from L2:F2701 (Congress-related words) at pos 2. Find what earlie… |
| SA-2 | `L3:F5753@12` | ❌ error | — | — | Trace upstream from L3:F5753 ("includes" word) at pos 12. Find what earlier-laye… |
| SA-3 | `L4:F59@11` | ❌ error | — | — | Trace upstream from L4:F59 ("to" word preceded by verb) at pos 11. Find what ear… |
| SA-4 | `L4:F7775@9` | ❌ error | — | — | Trace upstream from L4:F7775 at pos 9. Find what this feature encodes and what d… |
| SA-5 | `L2:F2701@2` | ❌ error | — | — | Trace upstream from L2:F2701 (Congress-related words) at pos 2. Find what earlie… |
| SA-6 | `L3:F5753@12` | ❌ error | — | — | Trace upstream from L3:F5753 ("includes" word) at pos 12. Find what earlier-laye… |
| SA-7 | `L4:F59@11` | ❌ error | — | — | Trace upstream from L4:F59 ("to" word preceded by verb) at pos 11. Find what ear… |
| SA-8 | `L4:F7775@9` | ❌ error | — | — | Trace upstream from L4:F7775 at pos 9. Find what this feature encodes and what d… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L2:F2701@2, k=15 → Emb:" Congress"@2 (de=28.12) +14 more |
| 2 | `get_upstream_features` | L3:F5753@12, k=15 → Emb:" include"@12 (de=41.00) +14 more |
| 3 | `get_upstream_features` | L4:F59@11, k=15 → Emb:" began"@10 (de=13.31) +14 more |
| 4 | `get_upstream_features` | L4:F7775@9, k=15 → Emb:","@9 (de=4.94) +14 more |
| 5 | `inspect_feature` ×20 | L4:7775, L3:123, L0:4870, L0:8444, L0:10401, L2:6735, L3:8351, L3:12596, L2:11469, L2:11734, L0:10783, L0:195, L0:3204, L0:9557, L1:4224, L0:10198, L1:2089, L1:5475, L1:14565, L1:12456 |
| 6 | `get_top_features` | token="", k=30 → 30 features; top: L2:2701 de=0.848 |
| 7 | `inspect_feature` ×10 | L0:11640, L0:13564, L0:13437, L1:4020, L0:4476, L0:10536, L0:13417, L1:9361, L2:7279, L1:3231 |
| 8 | `get_upstream_features` | L3:F123@2, k=10 → Emb:" Congress"@2 (de=20.62) +9 more |
| 9 | `get_upstream_features` | L2:F6735@2, k=10 → Emb:" Congress"@2 (de=9.12) +9 more |
| 10 | `inspect_feature` | L0, F10401 → " mentions of genes and proteins" |

### Build

`build_circuit` → 18 nodes, 31 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 83,665 | 8,011 | 380,092 | 0 | $0.0575 | — | — |
| **Total** | | **83,665** | **8,011** | **380,092** | **0** | **$0.0575** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 49s