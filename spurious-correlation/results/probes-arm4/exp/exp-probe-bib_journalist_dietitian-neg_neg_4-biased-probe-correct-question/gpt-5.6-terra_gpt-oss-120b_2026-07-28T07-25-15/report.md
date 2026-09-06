# Circuit Oracle Report
**Date:** 2026-07-28 07:25:15 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The profession-probe score is driven chiefly by a male-pronoun circuit centered on repeated instances of “he,” with only weak, nonspecific lexical evidence from the defence/writing biography.

**Confidence:** 9/10

**Reasoning:** The saved circuit shows a direct path from **Emb: “ he” (pos 22)** through early and mid-layer pronoun detectors into the linear probe score, rather than a robust semantic circuit for freelance writing, journalism, or defence expertise.

- The dominant late contributor is **L18:F14743** at positions **22, 39, and 67**, all activated at occurrences of *he*. Its label is simply **“He”**, it is fairly selective (`frac_nonzero=0.01809`), and its promoted tokens include *himself* while suppressed tokens include *she* and *her*. This is a gender/masculine-reference feature, not a profession feature. Although its direct effects on the probe are negative (e.g. −0.1157 at pos 22), their magnitude makes it among the strongest determinants of the score: the probe uses masculine reference strongly, whether as positive evidence for an alternative class or as evidence against this class.

- The upstream trace is unusually direct: the raw **“ he” embedding at pos 22** has a **+28.625** effect on L18:F14743—far larger than any other upstream contributor. Thus, the late feature is primarily a transformed copy/detector of the local token, not an inference assembled from the person’s work history.

- The intermediate circuit corroborates this:
  - **L0:F12768 (pos 22)** is labeled **“mentions of ‘he’ and ‘she’ in close proximity”** (`frac_nonzero=0.01091`) and feeds both L14 and L18 pronoun circuitry.
  - **L14:F14097 (pos 22)** is labeled **“occurrences of the word ‘he’”** (`frac_nonzero=0.01967`) and has a direct negative effect on the probe (−0.0903). It receives positive input from the same *he* embedding (+2.7031) and from L0:F12768 (+1.3516), then positively feeds L18:F14743 (+2.875).
  - This creates the circuit **Emb: he → early male-pronoun representation → mid-layer he detector → late masculine-reference detector → probe score**.

- A direct raw-embedding route also exists from **Emb: he** to the late L18 detector, so the model does not need any contextual professional interpretation to create the highly influential signal.

- There is one modestly relevant lexical feature, **L0:F5288 at “Services” (pos 6)**, labeled **service/Services-related terminology** (`frac_nonzero=0.00074`). But its examples span *community service*, *health services*, and generic organizational “Services”; it is not specifically a defence-institute, journalist, author, or security-analyst detector. The circuit evidence therefore does not establish it as meaningful profession recognition.

- Other high-ranked features are also largely irrelevant lexical/stylistic artifacts: **L1:F15323** detects *starting* in academic papers; **L0:F7124** detects *at*; and **L0:F15661** is labeled *spin*. These do not form a coherent path from the document’s genuine profession cues—“freelance writer,” “written for,” named newspapers, “defence publications,” or “Defense News”—to the probe.

Overall, the user concern is supported: this attribution graph indicates that the probe substantially relies on **gendered pronouns and shallow lexical correlations**, not a clean profession-specific mechanism. The presence of relevant biography content does not appear to be the main causal driver in the traced high-effect circuit.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 22 | Early male-pronoun representation |  mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L14:F14097](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) | 22 | Mid-layer he detector |  occurrences of the word "he" | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 22 | Late he / masculine-reference detector | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 39 | Late he / masculine-reference detector | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 67 | Late he / masculine-reference detector | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L0:F5288](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5288) | 6 | Service/Services lexical cue |  the word "service" and related terms in different contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5288) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:7124 de=-0.160 |
| 3 | `inspect_feature` ×4 | L18:14743, L14:14097, L1:15323, L0:7124 |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14743@22` | ❌ error | — | — | Trace this repeatedly active late feature upstream to embeddings. Determine whet… |
| SA-2 | `L14:F14097@22` | ❌ error | — | — | Trace this influential negative late-mid feature upstream to embeddings. Identif… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14743@22, k=20 → Emb:" he"@22 (de=28.62) +19 more |
| 2 | `get_upstream_features` | L14:F14097@22, k=20 → Emb:" he"@22 (de=2.70) +19 more |
| 3 | `inspect_feature` ×4 | L0:12768, L7:14946, L0:15661, L0:5288 |

### Build

`build_circuit` → 6 nodes, 9 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 15,136 | 2,077 | 44,404 | 0 | $0.0801 | — | — |
| **Total** | | **15,136** | **2,077** | **44,404** | **0** | **$0.0801** | | |

**Oracle wall-clock time:** 0m 52s