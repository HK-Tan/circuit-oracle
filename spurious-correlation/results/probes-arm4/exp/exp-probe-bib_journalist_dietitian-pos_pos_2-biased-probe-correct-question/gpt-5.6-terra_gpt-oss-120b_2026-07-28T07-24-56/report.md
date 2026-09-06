# Circuit Oracle Report
**Date:** 2026-07-28 07:24:56 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The profession-probe score is driven predominantly by a repeated female-pronoun/female-biography circuit, with only a much smaller direct contribution from genuine nutrition content.

**Confidence:** 9/10

**Reasoning:** The output is a synthetic probe target (not a next-token prediction), and the circuit saved above identifies the features that push its profession-classification direction.

The dominant mechanism is clearly gender-coded:

- **Emb: `She` (pos 1)** and **Emb: ` She` (pos 23)** directly excite the circuit. In particular, the late feature **L18:F14677** at pos 23 receives a very large positive contribution directly from ` She` at pos 23 (**+14.31**) and from `She` at pos 1 (**+6.81**); its pos-1 instance receives **+27.13** directly from `She`.
- These embeddings feed the **Early female-reference detectors** supernode:
  - **L6:F11646** (pos 1, 2, and 23) is specifically a female-reference detector: its activating examples center on *her*, it promotes `she`, `her`, and `herself`, and it is fairly selective (**frac_nonzero 0.01976**). It is also the single strongest positive output-driving feature at pos 1 (**direct effect +0.3574**) and again strongly positive at pos 2 (**+0.2852**) and pos 23 (**+0.1367**).
  - **L12:F12940** at pos 2, another highly selective female-pronoun feature (**frac_nonzero 0.00652**), contributes **+0.2891** directly to the probe. Upstream it is strongly driven by `She` (**+6.03**) and by L6:F11646 at pos 2 (**+3.86**).
  - **L10:F14965** at pos 2 is also a woman/female-term feature and contributes **+0.1602**.
  - **L4:F15317** at pos 2 contributes **+0.2334**; although its label is broad “person/entity” recognition, its promoted tokens and its specific use here are female-coded. It strongly feeds both the L6 and L12 female detectors (e.g. **+8.75** into L6:F11646 at pos 2, **+4.97** into L12:F12940).
- This early gender signal is consolidated in the **Late woman / female-biography representation**:
  - **L18:F14677** at pos 23 is the strongest later semantic driver (**+0.2422**; also **+0.2031** at pos 1). Its examples are unambiguously female mentions, it promotes `she`, `her`, and `herself`, and its firing rate is **0.01225**.
  - It receives positive causal input from L6:F11646 at positions 1/2/23 and L12:F12940, as well as directly from the repeated `She` embeddings.
  - **L19:F9685** at pos 23 adds **+0.1455** to the score. It is labeled as women’s names, roles, and accomplishments (**frac_nonzero 0.01351**) and receives input from both `She` positions and the earlier female features. Thus it appears to represent the genre “biographical description of a woman,” not the nutrition profession itself.
  - **L14:F12501** at pos 2 is another feminine-pronoun feature (**frac_nonzero 0.0144**) contributing **+0.1475**.

There *is* genuine task-relevant evidence: **Emb: ` nutrition` (pos 13)** drives **L6:F11327** directly and very strongly (**+21** into that feature). L6:F11327 is a selective food/nutrition concept feature (**frac_nonzero 0.01166**), with activating examples involving nutrition, healthy eating, food, and health education; its promoted tokens include `food`, `foods`, `eating`, and `meals`. It does positively affect the probe (**+0.1523**). This establishes that the circuit is not wholly spurious.

However, nutrition is represented by essentially one moderate direct-output feature, while the leading output features and the main multi-layer path are a dense, repeated female-pronoun circuit. The top two positive effects are L6:F11646 (**+0.3574**) and L12:F12940 (**+0.2891**), both explicitly female-pronoun features; L18:F14677 (**+0.2422**) is likewise a woman-reference feature. The repeated pronouns therefore do not merely coexist with the professional content: they causally and substantially drive the probe direction.

**Conclusion:** the user’s concern is supported. This classification score combines authentic nutrition/food evidence with a much stronger proxy for “female subject / woman-centered biography.” The circuit is not entity-specific knowledge of Brittany, nor is the main route a robust profession representation; it substantially exploits gender markers that are plausibly correlated with the probe’s profession label in its training data.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Early female-reference detectors |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Early female-reference detectors |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Early female-reference detectors |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 23 | Early female-reference detectors |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L10:F14965](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) | 2 | Early female-reference detectors |  terms relating to women | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Early female-reference detectors | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 13 | Nutrition/food semantic evidence |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Late woman / female-biography representation |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 23 | Late woman / female-biography representation |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 23 | Late woman / female-biography representation |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L14:F12501](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) | 2 | Late woman / female-biography representation |  uses of the feminine pronoun. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11646 de=0.357 |
| 3 | `inspect_feature` ×5 | L6:11646, L12:12940, L18:14677, L4:15317, L4:7864 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@23` | ❌ error | — | — | Trace the strongest late profession-probe-driving path upstream to embeddings. D… |
| SA-2 | `L12:F12940@2` | ❌ error | — | — | Trace this high positive probe-driving feature upstream to embeddings, testing w… |
| SA-3 | `L6:F11646@1` | ❌ error | — | — | Trace this recurrent positive early-layer feature upstream to token embeddings a… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14677@23, k=20 → Emb:" She"@23 (de=14.31) +19 more |
| 2 | `get_upstream_features` | L12:F12940@2, k=20 → Emb:"She"@1 (de=6.03) +19 more |
| 3 | `get_upstream_features` | L6:F11646@1, k=20 → Emb:"She"@1 (de=19.25) +19 more |
| 4 | `get_upstream_features` | L6:F11646@2, k=20 → L4:F15317 (de=8.75) +19 more |
| 5 | `get_upstream_features` | L18:F14677@1, k=20 → Emb:"She"@1 (de=27.12) +19 more |
| 6 | `get_upstream_features` | L6:F11327@13, k=15 → Emb:" nutrition"@13 (de=21.00) +14 more |
| 7 | `inspect_feature` ×4 | L6:11327, L19:9685, L10:14965, L14:12501 |
| 8 | `get_upstream_features` | L19:F9685@23, k=12 → Emb:" She"@23 (de=5.72) +11 more |
| 9 | `get_upstream_features` | L10:F14965@2, k=12 → L4:F15317 (de=5.56) +11 more |

### Build

`build_circuit` → 7 nodes, 6 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 20,980 | 2,459 | 71,120 | 0 | $0.1071 | — | — |
| **Total** | | **20,980** | **2,459** | **71,120** | **0** | **$0.1071** | | |

**Oracle wall-clock time:** 0m 40s