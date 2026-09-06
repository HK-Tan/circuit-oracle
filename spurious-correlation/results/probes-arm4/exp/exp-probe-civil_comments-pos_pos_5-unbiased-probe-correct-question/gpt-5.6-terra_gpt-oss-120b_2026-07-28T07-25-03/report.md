# Circuit Oracle Report
**Date:** 2026-07-28 07:25:03 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe score is driven mainly by shallow lexical/style correlations—especially a political/ideological cue around “social … warrior” and an imperative conditional template—rather than by a robust representation of the prompt’s full derogatory/hostile implication.

**Confidence:** 7/10

**Reasoning:** The saved circuit has several distinct components feeding the synthetic toxicity-probe direction.

* **Social/political cue:** `Emb: social (pos 5)` feeds the **Social/political-ideological cue** node, especially L6:F2674 at “warrior” (pos 7). This feature has the label *“political or ideological content, particularly with negative connotations”* (`frac_nonzero=0.01656`) and its strongest activating examples contain politically charged, hostile material such as “liberal lying,” “politically correct,” and racial/political commentary. It makes a **positive** contribution to the probe (`+0.0674`). This is the clearest evidence of a likely spurious topical shortcut: the probe is responding to the lexical neighborhood of “social justice warrior,” a politicized phrase, not specifically to the utterance’s target, intent, or pragmatic offensiveness.

* **Conditional/directive form:** `Emb: If (pos 1)`, `Emb: you (pos 2)`, `Emb: a (pos 4)`, and `Emb: warrior (pos 7)` feed **Generic self-description / conditional-action templates**. L3:F16254 at the comma position is labeled *“conditional statements followed by actions the speaker will take”* (`frac_nonzero=0.01715`) and contributes positively (`+0.1040`). Its direct upstream attribution is dominated by “If” (`+9.875`), “you” (`+5.156`), and “warrior” (`+2.406`). L3:F10868, though autointerpreted as an “I’m a / I am a” pattern, is actually receiving overwhelmingly strong direct input from the generic tokens “a” (`+18.625`) and “you” (`+10.875`) and also pushes the score up (`+0.1348`). These show the probe is sensitive to the sentence’s *if-you-are-X, then-do-Y* construction and direct-address form. That may correlate with toxic prompts in the probe’s training distribution, but it is not semantic evidence of toxicity by itself.

* **Low-level artifacts also matter:** In the circuit, L0:F7710 is simply the token “you” (`frac_nonzero=0.01884`) and is a large **negative** direct contribution (`-0.1543`). L0:F8444 is “to” (`frac_nonzero=0.01705`) and is even more negative (`-0.2236`). The comma feature L0:F3850, broadly “punctuation marks” (`frac_nonzero=0.07205`), is positive (`+0.0723`). These large direct effects from ordinary function words and punctuation indicate the probe direction is substantially entangled with surface-form directions, rather than cleanly isolating toxic semantics.

* **Actual topical content is not consistently treated as toxic evidence:** The one strongly identifiable content feature L6:F9005 is *desserts* (`frac_nonzero=0.00685`), driven predominantly by `Emb: bakery (pos 13)` with an upstream direct effect of `+22.375`. Yet it contributes **negatively** to the toxicity direction (`-0.1128`): bakery/cake semantics act as a countervailing benign-topic signal. The direct upstream effect from `Emb: Muslim (pos 12)` into that dessert feature is also negative (`-1.9844`), so this trace does **not** establish that “Muslim” is being positively used as a toxicity marker through the bakery/dessert path.

* There is, however, a shallow identity-adjacent feature: L0:F4478 at “justice” is autointerpreted as *ownership and belief systems* and includes high-activation examples involving “sexual orientation,” “gender,” and “religious organizations” (`frac_nonzero=0.01367`). It has a negative direct effect (`-0.0918`) here. Thus the available evidence does not show a simple “identity group → higher toxicity” route; it shows a noisy, mixed-sign association direction that touches identity-related material.

Overall, the positive evidence is dominated by **political/ideological language** and **conditional/directive phrasing**, while concrete bakery/cake content suppresses the score. The circuit therefore supports the user’s concern in a qualified form: this probe appears to rely materially on spurious lexical and stylistic correlates, especially the phrase “social justice warrior,” rather than a compositional representation that the speaker is directing a provocative action involving Muslim and gay identities.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F7710](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) | 2 | Direct-address and conditional syntax | the pronoun "you" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 10 | Direct-address and conditional syntax | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F13310](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13310) | 3 | Direct-address and conditional syntax |  sentences that include forms of the verb "are" indicating a present state of being or necessity. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13310) |
| [L3:F10868](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10868) | 4 | Generic self-description / conditional-action templates |  the phrase "I'm a" or "I am a" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10868) |
| [L3:F16254](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16254) | 8 | Generic self-description / conditional-action templates |  conditional statements followed by actions the speaker will take | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16254) |
| [L2:F14541](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14541) | 8 | Generic self-description / conditional-action templates |  code snippets and logical statements, especially those involving "then," along with some citation markers and bracketed references. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14541) |
| [L2:F14209](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14209) | 9 | Generic self-description / conditional-action templates | the verb "go" in its various forms. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14209) |
| [L6:F2674](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2674) | 7 | Social/political-ideological cue |  political or ideological content, particularly with negative connotations. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2674) |
| [L3:F1526](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1526) | 6 | Social/political-ideological cue |  references to academic disciplines related to social science | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1526) |
| [L6:F9005](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9005) | 13 | Bakery/dessert content (opposes probe direction) |  words and phrases related to desserts | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9005) |
| [L0:F4478](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4478) | 6 | Identity/orientation association feature (opposes probe direction) |  terms related to ownership and belief systems. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4478) |
| [L0:F3850](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3850) | 8 | Punctuation/form artifact | punctuation marks | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3850) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:8444 de=-0.224 |
| 3 | `inspect_feature` ×10 | L0:8444, L0:7710, L3:10868, L3:16254, L6:9005, L0:9934, L0:4478, L0:13310, L2:14209, L6:2674 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F9005@13` | ❌ error | — | — | Trace this strongest later-layer negative contributor to the synthetic toxicity-… |
| SA-2 | `L3:F10868@4` | ❌ error | — | — | Trace this strongest positive mid-layer contributor to the probe direction back … |
| SA-3 | `L3:F16254@8` | ❌ error | — | — | Trace this positive feature at the identity-related region upstream to embedding… |
| SA-4 | `L6:F2674@7` | ❌ error | — | — | Trace this positive later-layer path to embeddings, determining whether it track… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F9005@13, k=15 → Emb:" bakery"@13 (de=22.38) +14 more |
| 2 | `get_upstream_features` | L6:F2674@7, k=15 → Emb:" social"@5 (de=2.12) +14 more |
| 3 | `get_upstream_features` | L3:F10868@4, k=15 → Emb:" a"@4 (de=18.62) +14 more |
| 4 | `get_upstream_features` | L3:F16254@8, k=15 → Emb:"If"@1 (de=9.88) +14 more |
| 5 | `inspect_feature` ×3 | L0:3850, L3:1526, L2:14541 |

### Build

`build_circuit` → 13 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 51,829 | 2,720 | 35,517 | 0 | $0.1793 | — | — |
| **Total** | | **51,829** | **2,720** | **35,517** | **0** | **$0.1793** | | |

**Oracle wall-clock time:** 0m 35s