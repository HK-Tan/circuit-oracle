# Circuit Oracle Report
**Date:** 2026-07-28 07:24:50 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe’s positive classification is driven predominantly by a female-biographical-subject circuit—“Her,” “She,” and “Heather”—with only a smaller genuine nutrition/diet signal, so the user’s concern about gender-spurious reliance is well supported.

**Confidence:** 9/10

**Reasoning:** The target is a synthetic probe score rather than a next-token logit. Its largest positive direct drivers show a clear gender pattern:

- **Female-reference detectors** are the strongest route into the probe. L6:11646 at **pos 1** has direct effect **+0.2832**, and at **pos 15** has **+0.2031**. Its label is “references to women,” it is selective (`frac_nonzero=0.01976`), its strongest examples fire on *her*, and it promotes **“she,” “her,” and “herself.”**  
  - It is directly driven chiefly by **Emb: Her (pos 1)**: +18.125 upstream attribution, with supporting early female feature **L0:15382** (+2.1719). L0:15382 is explicitly a female-person feature (`frac_nonzero=0.0088`) that fires on *Her* and promotes *her/she*.
  - This establishes that the early route is not detecting nutrition or a profession; it is recognizing the gendered pronoun itself.

- The later **female subject / accomplishment detector** strengthens the same signal. **L18:14677 at pos 15** contributes **+0.1709** to the probe and is labeled “instances of women or girls being mentioned” (`frac_nonzero=0.01225`), promoting *she/her/herself* and suppressing male forms such as *his/himself*. It receives its dominant upstream signal directly from **Emb: She (pos 15)** (+15.25), plus **Emb: Her (pos 1)** (+6.5312) and L6:11646 (+2.9531).

- At the name position, **L19:9685 at pos 46** contributes **+0.1328**. It is labeled “references to women’s names and their roles or accomplishments,” is selective (`frac_nonzero=0.01351`), and promotes *she/her/herself*. It is driven by **Emb: Heather (pos 46)** (+4.625), **Emb: Her (pos 1)** (+2.4688), and **Emb: She (pos 15)** (+1.6719). Thus this late feature represents a *female person in a biographical/accomplishment framing*, rather than a specific profession.

- The **person-name / biographical-subject** path supplies further non-professional evidence. **L12:14970 at pos 46** has a probe effect of **+0.1553** and is a rare person-name feature (`frac_nonzero=0.00269`); **L16:6025** detects capitalized first names (`frac_nonzero=0.01251`); and **L4:1276** is another name/title detector (`frac_nonzero=0.00341`). These are driven by **Emb: Heather (pos 46)**—e.g., direct upstream effects +3.2031 into L12:14970 and +1.8516 into L19:9685. These features identify that the passage is a named-person biography, but do not identify dietetics, sports nutrition, or a particular occupational role.

There **is** genuine profession-relevant evidence: **L4:13412 at “nutrition” (pos 7)** contributes **+0.1367** to the probe. It is a diet/dietary-health feature (`frac_nonzero=0.01216`), promotes **“diet,” “diets,” “DIET,” and “dieting,”** and receives an extremely large direct upstream contribution from **Emb: nutrition (pos 7)** (+12.625). This is an authentic semantic cue for nutrition/dietetics. However, its direct probe effect is smaller than the leading gender effects and is not the dominant circuit.

The saved circuit therefore separates:

1. **Genuine profession cue:** `Emb: nutrition → Diet/nutrition evidence (L4:13412) → Probe`.
2. **Dominant spurious cue:** `Emb: Her/She → Female-reference detectors (L0:15382; L6:11646) → Female subject detector (L18:14677) → Probe`.
3. **Biographical gender/name cue:** `Emb: Heather → name detectors (L0:7532, L4:1276, L12:14970, L16:6025) → female-accomplishment detector (L19:9685) → Probe`.

Overall, the probe does not appear to be cleanly profession-specific. It does use a real nutrition indicator, but its strongest causal evidence is broad female-reference and female-biography structure—signals that would generalize across many professions and can therefore produce gender-associated, spurious classification behavior.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 7 | Diet/nutrition evidence |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 1 | Female-reference detectors | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Female-reference detectors |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 15 | Female-reference detectors |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 15 | Female subject / accomplishment detector |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 46 | Female subject / accomplishment detector |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 46 | Person-name / biographical-subject detectors |  proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 46 | Person-name / biographical-subject detectors | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 46 | Person-name / biographical-subject detectors |  names of people, both first and last names | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L16:F6025](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6025) | 46 | Person-name / biographical-subject detectors |  capitalized first names, sometimes followed by last names | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6025) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 12 features; top: L6:11646 de=0.283 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@1` | ❌ error | — | — | Trace this strongest positive probe-driving path to embeddings. Determine whethe… |
| SA-2 | `L18:F14677@15` | ❌ error | — | — | Trace this late positive probe-driving path to embeddings; identify profession v… |
| SA-3 | `L12:F14970@46` | ❌ error | — | — | Trace this positive path at the later Heather/biographical position to embedding… |
| SA-4 | `L19:F9685@46` | ❌ error | — | — | Trace late positive path to embeddings and identify what drives the probe. |
| SA-5 | `L4:F13412@7` | ❌ error | — | — | Trace early positive feature to raw embeddings and inspect whether it encodes ge… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×8 | L6:11646, L18:14677, L12:14970, L19:9685, L4:13412, L4:1276, L0:10148, L0:6051 |
| 2 | `get_upstream_features` | L6:F11646@1, k=15 → Emb:"Her"@1 (de=18.12) +14 more |
| 3 | `get_upstream_features` | L18:F14677@15, k=15 → Emb:" She"@15 (de=15.25) +14 more |
| 4 | `get_upstream_features` | L19:F9685@46, k=15 → Emb:" Heather"@46 (de=4.62) +14 more |
| 5 | `get_upstream_features` | L4:F13412@7, k=15 → Emb:" nutrition"@7 (de=12.62) +14 more |
| 6 | `get_upstream_features` | L12:F14970@46, k=15 → Emb:"<bos>"@0 (de=-5.22) +14 more |
| 7 | `inspect_feature` ×5 | L4:7864, L17:5889, L16:6025, L0:15382, L0:7532 |

### Build

`build_circuit` → 9 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 25,680 | 2,577 | 85,849 | 0 | $0.1243 | — | — |
| **Total** | | **25,680** | **2,577** | **85,849** | **0** | **$0.1243** | | |

**Oracle wall-clock time:** 0m 35s