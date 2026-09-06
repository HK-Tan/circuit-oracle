# Circuit Oracle Report
**Date:** 2026-07-28 07:24:44 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe score is primarily driven by a genuine journalism/writer occupation circuit centered on “freelance writer,” with a smaller but real direct gender/pronoun feature that provides a spurious auxiliary signal.

**Confidence:** 8/10

**Reasoning:** The synthetic output label is the probe direction, not a next-token prediction. The strongest interpretable content pathway converges on the phrase **“freelance writer”**:

- **Emb: `freelance` (pos 27)** and **Emb: `writer` (pos 28)** directly excite the L6 publishing feature **L6:12712**. In the upstream attribution, `writer` contributes **+6.22** and `freelance` **+3.38** to this feature.
- **L6:12712** (activation 8.69; direct effect on the probe −0.0593) is labelled as an editor/publisher-title detector. Its examples include “deputy editor,” “Editor-in-Chief,” and scientific publishing; it has `frac_nonzero=0.01747`. It is not a clean *journalist* detector, but it is plausibly an intermediate writing/publishing occupation representation.
- This feeds the more specific late feature **L14:4420**, whose direct effect is substantial (**−0.0679**) and whose label is “words and phrases related to journalism and newspapers.” Its promoted tokens are strongly occupation-specific: `journalist`, `journalism`, `reporter`, `editorial`, and plural/capitalized variants. Its activating examples include “reporter,” “newspaper,” and “reporting,” with `frac_nonzero=0.0165`.
- The direct upstream evidence for **L14:4420** is particularly clear: `writer` (pos 28) contributes **+5.75**, `freelance` (pos 27) **+2.69**, and L6:12712 **+1.30**. Thus the primary circuit is not merely detecting generic biography prose or defence vocabulary: it recognizes the explicit occupation phrase and maps it into a journalism/newspaper concept, which then drives the probe score.

The saved circuit captures this as:

`Emb: freelance` + `Emb: writer` → **Writer/editorial-title detector** (L6:12712) → **Journalism/newspaper occupation detector** (L14:4420) → **synthetic profession-probe score**,

with direct `freelance`/`writer` input also entering L14:4420.

There **is** evidence relevant to the user’s concern. At L0, **L0:12768** at `he` (pos 22) is explicitly a male-pronoun feature: its top examples are dominated by “he/him/his,” it suppresses `he` variants, and it fires relatively selectively (`frac_nonzero=0.01091`). It has a positive direct effect on the probe (**+0.0747**), the largest positive feature among the initially surfaced features. This means the probe direction contains a gender-associated component. The surrounding phrase also contains a direct negative embedding contribution from `he` to the L6 writing feature (**−0.52**), so the gender signal does not appear to be what builds the main writing/journalism representation; rather, it is an additional direct probe-aligned feature.

Other high-ranked L0 features are mostly lexical or weakly related: “at” (L0:7124), “middle” (L0:3007), and “rapid” (L0:2348), while L1:4459 detects “Institute” and L0:9297 government ministries. These are not compelling profession evidence in this circuit. In particular, no high-impact feature examined provides a strong defence-specific classification route; the decisive semantic evidence is the explicit writer/journalism wording.

So the conclusion is **mixed but favorable**: the score is chiefly supported by genuine profession indicators—especially *freelance writer* and the downstream journalism detector—but the probe is not gender-invariant, because a male-pronoun feature also directly shifts its score. The spurious gender path should be treated as a bias/confound to test by counterfactual pronoun substitution or by evaluating gender-balanced biographies.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 22 | Male-pronoun/gender signal |  mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L6:F12712](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) | 28 | Writer/editorial-title detector |  titles of editors and publishers in scientific publications | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 28 | Journalism/newspaper occupation detector | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 12 features; top: L0:7124 de=-0.157 |
| 3 | `inspect_feature` ×8 | L0:7124, L0:15661, L0:12768, L14:4420, L6:12712, L0:3007, L0:2348, L1:4459 |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@28` | ❌ error | — | — | Trace this negative contribution to the probe score upstream to embeddings. Dete… |
| SA-2 | `L6:F12712@28` | ❌ error | — | — | Trace this negative probe-driving path upstream to embeddings and characterize w… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F4420@28, k=15 → Emb:" writer"@28 (de=5.75) +14 more |
| 2 | `get_upstream_features` | L6:F12712@28, k=15 → Emb:" writer"@28 (de=6.22) +14 more |
| 3 | `inspect_feature` ×4 | L0:6484, L0:10881, L0:1229, L0:9297 |

### Build

`build_circuit` → 7 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 24,799 | 2,115 | 51,760 | 0 | $0.1067 | — | — |
| **Total** | | **24,799** | **2,115** | **51,760** | **0** | **$0.1067** | | |

**Oracle wall-clock time:** 0m 31s