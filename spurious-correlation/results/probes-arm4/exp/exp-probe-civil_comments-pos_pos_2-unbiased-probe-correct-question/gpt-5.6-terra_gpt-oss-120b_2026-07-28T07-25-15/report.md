# Circuit Oracle Report
**Date:** 2026-07-28 07:25:15 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe’s positive classification score is driven primarily by shallow lexical identity markers—especially **“white”** and, secondarily, **“he”**—plus generic conditional/copular wording, rather than a coherent semantic evaluation of the sentence’s toxicity.

**Confidence:** 8/10

**Reasoning:** The synthetic probe label has probability 1, so its attribution graph directly identifies features aligned with the probe direction rather than a vocabulary prediction. The saved circuit shows a largely shallow, token-local mechanism.

* The dominant identity-related path is `Emb: white (pos 4)` → **White-token / race-term lexical detectors** → probe.  
  * L0:3436 at position 4 is explicitly a detector for **“white”** (fraction nonzero **0.06114**) and is a major positive direct driver of the probe score (**+0.1719**). Its strongest upstream source is the literal ` white` embedding (**+18**), which establishes that this is not inferred race-related meaning: it is directly keyed to the word form.
  * L0:10910 at the same position is another broad lexical feature that fires for **“white”** among a small collection of unrelated words (fraction nonzero **0.01494**). It also feeds the L4 feature and positively drives the probe (**+0.1035**).

* A deeper but still word-triggered route is `Emb: white (pos 4)` → **White-associated contextual feature** L4:15204 → probe. L4:15204 has a positive direct effect of **+0.1177**. Its autointerp headline is “art galleries, museums and the White House,” but its activating examples include racial uses of *white* and “White Man”; its strongest upstream edge here is directly from the ` white` embedding (**+40.5**). Thus, in this prompt it is best read as an ambiguous high-level continuation/context feature activated by the *white* token, not evidence that the model has composed the full proposition “white and not Hispanic.”

* A separate positive path is `Emb: he (pos 2)` → **Male-pronoun detector** L0:12768 → probe. L0:12768 is a selective “he/she” pronoun feature (fraction nonzero **0.01091**) and is the single strongest listed positive feature (**+0.2051**). Its activation is directly dominated by the literal ` he` embedding (**+37**). This supports the concern that the probe score has a demographic-/identity-adjacent shortcut: gendered-reference wording itself contributes materially.

* The remaining positive pathway is mainly grammatical template evidence: `Emb: If (pos 1)` and `Emb: was (pos 3)` → **Conditional/copular-template features** → probe.  
  * L0:2458 and L0:14369 are both **“was”** detectors (fraction nonzero **0.02488** and **0.003**, respectively).
  * L0:2303 is an **“if”** detector (fraction nonzero **0.01112`).
  * L2:1139 is a sparse feature for **“so”**/related constructions (fraction nonzero **0.00501**) and adds **+0.0933** to the probe. Its strongest upstream inputs are `If` (**+27.625**) and `was` (**+21.375**), with only a very small positive input from the pronoun feature (**+0.9297**). This looks like a conditional sentence-form detector, not a detector of hostile or abusive intent.

There are also countervailing signals—for example L0:13663 (“pregnancy and related terms,” **−0.1660**) and multiple negative *was*- and local-context features—but they do not overturn the main pattern.

Overall, this circuit does **not** reveal a strong, distributed semantic toxicity mechanism that integrates the comparison, negation (“not”), and the actual claim. It instead reveals that the classification probe direction is substantially aligned with the presence of the literal racial descriptor **“white”**, a male pronoun, and the generic “If he was …” template. The prompt does contain identity-group content, so these features are prompt-grounded in the narrow lexical sense; however, the graph provides little evidence that the high score is specifically caused by semantic toxicity rather than a spurious correlation between identity mentions/conditional demographic statements and the training label.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 4 | White-token / race-term lexical detectors |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F10910](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) | 4 | White-token / race-term lexical detectors | the word "possession" and the words "white", "immediate" and "once" regardless of context | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 2 | Male-pronoun detector |  mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L0:F2458](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2458) | 3 | Conditional/copular-template features |  the word "was" and sometimes "were." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2458) |
| [L0:F14369](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14369) | 3 | Conditional/copular-template features |  the word "was" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14369) |
| [L0:F2303](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2303) | 1 | Conditional/copular-template features |  the word "if" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2303) |
| [L2:F1139](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1139) | 3 | Conditional/copular-template features |  various usages of the word "so", as well as some instances of the word "come" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1139) |
| [L4:F15204](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) | 4 | White-associated contextual feature |  art galleries, museums and the White House | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 12 features; top: L0:12768 de=0.205 |
| 3 | `inspect_feature` ×6 | L0:12768, L0:3436, L4:15204, L0:880, L2:1139, L0:13663 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F15204@4` | ❌ error | — | — | Trace the strongest later-layer positive feature driving the synthetic probe lab… |
| SA-2 | `L2:F1139@3` | ❌ error | — | — | Trace this positive L2 feature driving the probe label to identify its input-tok… |
| SA-3 | `L0:F12768@2` | ❌ error | — | — | Determine the semantic meaning and direct embedding/input origin of this stronge… |
| SA-4 | `L0:F3436@4` | ❌ error | — | — | Determine the semantic meaning and direct embedding/input origin of this positiv… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F15204@4, k=15 → Emb:" white"@4 (de=40.50) +14 more |
| 2 | `get_upstream_features` | L2:F1139@3, k=15 → Emb:"If"@1 (de=27.62) +14 more |
| 3 | `get_upstream_features` | L0:F12768@2, k=15 → Emb:" he"@2 (de=37.00) +14 more |
| 4 | `get_upstream_features` | L0:F3436@4, k=15 → Emb:" white"@4 (de=18.00) +14 more |
| 5 | `get_upstream_features` | L0:F880@8, k=15 → Emb:" it"@8 (de=42.50) +14 more |
| 6 | `inspect_feature` ×4 | L0:10910, L0:2458, L0:14369, L0:2303 |

### Build

`build_circuit` → 9 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 20,269 | 2,695 | 68,454 | 0 | $0.1082 | — | — |
| **Total** | | **20,269** | **2,695** | **68,454** | **0** | **$0.1082** | | |

**Oracle wall-clock time:** 0m 50s