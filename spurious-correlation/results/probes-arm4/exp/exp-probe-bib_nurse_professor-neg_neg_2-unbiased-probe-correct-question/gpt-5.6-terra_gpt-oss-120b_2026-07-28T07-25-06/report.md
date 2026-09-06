# Circuit Oracle Report
**Date:** 2026-07-28 07:25:06 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe score is driven primarily by genuine engineering and academic-profile evidence, but it also receives a substantial spurious boost from Canadian-location features and a smaller generic name signal—not a demonstrated gender-marker circuit.

**Confidence:** 8/10

**Reasoning:** The constructed circuit has four separable inputs into the **profession-classification probe score** rather than a next-token logit.

1. **Direct profession evidence — strongest, most diagnostic path.**  
   **Emb: Engineering (pos 9)** directly excites L1:1372, an explicit *“engineer”* detector (fraction nonzero **0.00767**). Its top activating examples are literal occurrences of *engineer* and *engineering*, including “engineering types.” The embedding contribution from `Engineering` into this feature is very large (**+19** direct effect), and L1:1372 itself contributes **+0.064** to the probe direction. This is clear semantic evidence genuinely relevant to an engineering-profession classification.  
   A caveat is that this feature’s decoder-promoted tokens are not engineering-related and it suppresses “engineering” variants, but its activating examples and direct embedding attribution make the feature interpretation reliable here.

2. **Academic-credential / research-profile evidence — relevant, but generic to educated professions.**  
   **Emb: Ph (pos 48)** feeds the Ph.D./degree branch: L1:10132 is a rare (**0.00233**) Ph.D.-abbreviation detector, with examples explicitly containing “Ph.D.” It and L2:10852 feed L6:2254, a rare (**0.00412**) detector for academic degrees, which then supports L7:14129. L7:14129 is also highly selective (**0.00417**) and represents *academic degrees, universities, and people associated with them*; its examples include Ph.D.s, Stanford faculty, graduate education, and postgraduate students. This late feature has a positive probe effect of **+0.0439**.  
   This is not specific to engineering—someone with a Ph.D. in history, biology, or law could trigger related patterns—but it is a reasonable proxy for an academic/research professional biography. In the supplied text it coheres with the explicit degree sequence and research interests in robotics/computer vision.

3. **Canadian / Waterloo route — substantial but spurious profession evidence.**  
   **Emb: Waterloo (pos 14)** robustly drives a Canada-associated pathway. It has direct positive effects into L4:8439 (**+17.25**) and L7:8870 (**+8.25**). L4:8439 is a Canadian-geography/Canadian-ticker feature (fraction nonzero **0.01032**) whose promoted tokens include *Canadian, Canada, Montreal, Quebec, Ontario,* and *Toronto*. It feeds L7:8870, a low-frequency (**0.00654**) location/organization-name feature whose promoted tokens are strongly Canadian (*Canada, Canadian, provincial, Ottawa, Edmonton*). These converge into L14:5600, a selective (**0.01726**) Canada/Canadian-place feature. L14:5600 is one of the largest positive drivers of the probe score (**+0.064**); its promoted tokens include *Canada, Canadian, Toronto,* and *Ontario*.  
   This is compelling evidence of a **dataset correlation or probe shortcut**: “University of Waterloo” should not, by itself, establish the target profession. It may be correlated with the labeled profession in the training set, particularly if Canadian engineering biographies are overrepresented, but it is not a profession indicator in the relevant causal sense.

4. **Name/person route — weak and generic; no specific gender feature was found.**  
   **Emb: Daniel (pos 1)** drives L2:16309 with a strong local embedding edge (**+12.94**). L2:16309 has a positive score effect (**+0.0493**) and is a selective (**0.00627**) generic *people’s names* detector. Its examples cover many names across languages and genders; nothing in its label, examples, or upstream source establishes that it encodes masculinity or the particular name “Daniel” as a gender proxy. Thus, it is best interpreted as a **generic biographical-person/name-format cue**, not evidence that gender markers are the operative mechanism. Still, since personal names are irrelevant to profession in principle, this path is another weak spurious input.

The negative top drivers also reinforce that the probe is not purely profession-semantic: L0:2743, a *“later”* feature, contributes **−0.0688**, and several generic lexical/contextual features have comparably sized signed effects. Overall, the circuit mixes a valid explicit **Mechanical Engineering / Engineering** detector with broader academic-biography evidence, and it is materially contaminated by the unrelated **Waterloo/Canada** shortcut. The user’s concern is therefore partly validated—there are spurious features—but the available evidence does **not** support the narrower claim that gender markers dominate this specific prediction.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L1:F1372](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1372) | 9 | Explicit engineering lexical detector | the word "engineer" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1372) |
| [L4:F8439](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8439) | 14 | Waterloo→Canadian-geography features |  stock ticker symbols and Canadian geography | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8439) |
| [L7:F8870](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8870) | 14 | Waterloo→Canadian-geography features |  locations and names of organizations or people | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8870) |
| [L14:F5600](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5600) | 14 | Canadian-place feature |  places and regions, particularly in Canada | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5600) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 50 | Ph.D. and degree evidence | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L1:F10132](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) | 50 | Ph.D. and degree evidence |  the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") written as "D" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 50 | Academic-degree/profile feature | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 50 | Academic-degree/profile feature |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L2:F16309](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16309) | 1 | Generic personal-name feature |  people's names | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16309) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2743 de=-0.069 |
| 3 | `inspect_feature` ×4 | L14:5600, L7:14129, L1:1372, L2:16309 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F5600@14` | ❌ error | — | — | Trace this positive driver of the synthetic profession-probe score fully upstrea… |
| SA-2 | `L7:F14129@50` | ❌ error | — | — | Trace this positive driver of the synthetic profession-probe score upstream to e… |
| SA-3 | `L1:F1372@9` | ❌ error | — | — | Trace this early positive driver of the probe score to input embeddings and iden… |
| SA-4 | `L2:F16309@1` | ❌ error | — | — | Trace this positive feature at the Daniel/name position to embeddings. Assess wh… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F5600@14, k=15 → L7:F8870 (de=15.94) +14 more |
| 2 | `get_upstream_features` | L7:F14129@50, k=15 → L6:F2254 (de=7.31) +14 more |
| 3 | `get_upstream_features` | L1:F1372@9, k=15 → Emb:" Engineering"@9 (de=19.00) +14 more |
| 4 | `get_upstream_features` | L2:F16309@1, k=15 → Emb:"Daniel"@1 (de=12.94) +14 more |
| 5 | `inspect_feature` ×7 | L0:15320, L0:2743, L0:4687, L7:8870, L4:8439, L6:2254, L1:10132 |
| 6 | `get_upstream_features` | L7:F8870@14, k=15 → L4:F8439 (de=9.00) +14 more |
| 7 | `get_upstream_features` | L4:F8439@14, k=15 → Emb:" Waterloo"@14 (de=17.25) +14 more |
| 8 | `get_upstream_features` | L6:F2254@50, k=15 → L2:F10852 (de=12.31) +14 more |

### Build

`build_circuit` → 11 nodes, 10 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 26,450 | 2,954 | 64,627 | 0 | $0.1266 | — | — |
| **Total** | | **26,450** | **2,954** | **64,627** | **0** | **$0.1266** | | |

**Oracle wall-clock time:** 0m 46s