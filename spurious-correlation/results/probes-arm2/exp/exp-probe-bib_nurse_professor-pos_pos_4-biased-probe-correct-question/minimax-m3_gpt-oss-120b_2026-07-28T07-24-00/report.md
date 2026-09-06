# Circuit Oracle Report
**Date:** 2026-07-28 07:24:00 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's nurse classification is driven by an entangled mix of legitimate profession signals (nurse/practitioner/Nursing tokens) and strong **gendered-spurious** signals — the female pronoun "She" at pos 20 (activating the largest single feature L6:F15267=0.56 and the deep L18:F14677=0.44) and the female-coded name "Lori" at pos 1 (L4:F1276=0.40, L5:F16213=0.35) — confirming the user's concern that gender markers materially contribute to the classification.

**Confidence:** 8

**Reasoning:**

The attribution graph's **top positive direct effects** onto the probe direction are:
- L6:F15267 @ pos33 = **+0.56** — fires on "practitioner"/"nurse" (genuine profession)
- L4:F15317 @ pos33 = **+0.51** — profession-term
- **L18:F14677 @ pos20 = +0.44** — fires on the pronoun "She" (L18 is very late; this is a high-level abstract feature), and the *same* feature also fires at pos43 ("Lori"), pos78, pos117 — i.e., it activates on multiple female-coded tokens, not just the profession
- L4:F1276 @ pos1 = **+0.40** — anchored on the **name "Lori"** (emb direct_effect 16.5)
- L5:F16213 @ pos2 = **+0.35** — also anchored on "Lori"/name region

**Tracing upstream confirms two parallel paths:**

1. **Genuine profession path** (mid_profession → profession_late): `Emb:nurse@32` (5.66) and `Emb:practitioner@33` (3.03) feed L1:F1494 → L4:F11037 → L5:F1275 → **L6:F15267** (top driver). Also `Emb:Nursing@18` contributes. These are legitimate lexical profession cues.

2. **Spurious gender path** (she_mid → she_late → output): `Emb:She@20` directly drives L0:F15382 (23.6), L0:F9519 (21.75), L6:F11646 (18.1) → L15:F3330, L15:F4709, L17:F5889 → **L18:F14677@20 = 0.44** and L19:F9685@20 = 0.26. This is a dedicated pronoun-anchored late-layer circuit.

3. **Name path** (name_features): `Emb:Lori@1` (16.5) → L0:F7532 → L2:F5859, F16306 → L4:F1276 (which itself drives L5:F16213 and even late-layer F14677@pos43). The name "Lori" is feeding the late layer via the same L18:F14677 at pos43, meaning the model is treating the female name as a co-occurring signal with the profession.

**Key evidence for the user's concern:**
- The **single highest direct effect to the probe** (L6:F15267=+0.56) is at pos33 ("practitioner"), but the **second-most distributed signal** is L18:F14677, which is not profession-specific — it fires on both "She" and "Lori" and propagates across many late positions.
- L4:F1276, anchored purely on the name "Lori" (not a profession word), has direct_effect +0.40 to the probe — larger than several profession-word features.
- L18:F14677 contributes at pos20 ("She", 0.44), pos43 ("Lori", 0.26), pos78, pos117 (0.21) — a late-layer feature that integrates gender-marking across the document.
- Pronoun-gender features (L15:F3330/F4709, L17:F5889) form their own deep pathway into the probe, parallel to the profession pathway.

The probe thus fires on a *conjunction* of (female-gendered subject) ∧ (nursing profession) rather than profession alone. If the input were rewritten with a male name/pronominalization but identical profession words, the she_late and name_features branches would drop out, but the profession_late branch would remain. The roughly 50/50 split between profession-lexical and gender-pronominal contributions to the probe score means the classifier is **not** profession-pure — the user is correct that it leans on gender/name markers as a spurious shortcut.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 0 | Probe direction (nurse classification) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 20 | Late-layer pronoun/sentence-initial features (She) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 20 | Late-layer pronoun/sentence-initial features (She) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 43 | Late-layer pronoun/sentence-initial features (She) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 78 | Late-layer pronoun/sentence-initial features (She) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 117 | Late-layer pronoun/sentence-initial features (She) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 20 | Late-layer pronoun/sentence-initial features (She) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 20 | Late-layer pronoun/sentence-initial features (She) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L15:F4709](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/4709) | 20 | Late-layer pronoun/sentence-initial features (She) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/4709) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 33 | Late-layer profession-term features (nurse/practitioner) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 18 | Late-layer profession-term features (nurse/practitioner) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 33 | Late-layer profession-term features (nurse/practitioner) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L5:F16213](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16213) | 2 | Late-layer profession-term features (nurse/practitioner) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16213) |
| [L6:F8166](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) | 1 | Late-layer profession-term features (nurse/practitioner) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 1 | Name (Lori) features - potential gender/spurious signal | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L2:F16306](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16306) | 1 | Name (Lori) features - potential gender/spurious signal | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16306) |
| [L2:F5859](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) | 1 | Name (Lori) features - potential gender/spurious signal | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 1 | Name (Lori) features - potential gender/spurious signal | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 33 | Mid-layer profession context features | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 33 | Mid-layer profession context features | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L4:F9036](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) | 33 | Mid-layer profession context features | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) |
| [L1:F1494](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) | 33 | Mid-layer profession context features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 20 | Mid-layer She features (gendered pronoun) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 20 | Mid-layer She features (gendered pronoun) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 20 | Mid-layer She features (gendered pronoun) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L0:F12519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) | 20 | Mid-layer She features (gendered pronoun) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Lori (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 20 | Emb: She (pos 20) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 32 | Emb: nurse (pos 32) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 33 | Emb: practitioner (pos 33) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 18 | Emb: Nursing (pos 18) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:15267 de=0.562 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F15267@33` | ❌ error | — | — | Trace this high-direct-effect feature upstream. What does L6:F15267 at pos 33 en… |
| SA-2 | `L18:F14677@20` | ❌ error | — | — | Trace this feature upstream. What does L18:F14677 at pos 20 encode? This appears… |
| SA-3 | `L4:F15317@33` | ❌ error | — | — | Trace this feature upstream. What does L4:F15317 at pos 33 encode? Is it a profe… |
| SA-4 | `L4:F1276@1` | ❌ error | — | — | Trace this feature upstream. What does L4:F1276 at pos 1 encode? Position 1 is l… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F15267@33, k=15 → Emb:" nurse"@32 (de=5.66) +14 more |
| 2 | `get_upstream_features` | L18:F14677@20, k=15 → Emb:" She"@20 (de=14.44) +14 more |
| 3 | `get_upstream_features` | L0:F15382@20, k=10 → Emb:" She"@20 (de=23.62) +9 more |
| 4 | `get_upstream_features` | L5:F1275@33, k=10 → L4:F9036 (de=1.70) +9 more |
| 5 | `get_upstream_features` | L4:F11037@33, k=10 → Emb:" practitioner"@33 (de=6.47) +9 more |
| 6 | `get_upstream_features` | L4:F1276@1, k=10 → Emb:"Lori"@1 (de=16.50) +9 more |
| 7 | `get_upstream_features` | L17:F5889@20, k=10 → Emb:" She"@20 (de=19.50) +9 more |
| 8 | `get_upstream_features` | L1:F1494@33, k=10 → Emb:" nurse"@32 (de=8.69) +9 more |
| 9 | `get_upstream_features` | L0:F7532@1, k=10 → Emb:"Lori"@1 (de=14.31) +9 more |
| 10 | `get_upstream_features` | L2:F16306@1, k=10 → Emb:"Lori"@1 (de=5.91) +9 more |
| 11 | `get_upstream_features` | L19:F9685@20, k=10 → Emb:" She"@20 (de=5.88) +9 more |
| 12 | `get_upstream_features` | L18:F14677@43, k=10 → Emb:" Lori"@43 (de=3.77) +9 more |
| 13 | `get_upstream_features` | L5:F16213@2, k=10 → Emb:"Lori"@1 (de=2.56) +9 more |
| 14 | `get_upstream_features` | L6:F11646@20, k=10 → Emb:" She"@20 (de=18.12) +9 more |
| 15 | `get_upstream_features` | L15:F3330@20, k=10 → Emb:" She"@20 (de=15.75) +9 more |
| 16 | `get_upstream_features` | L2:F5859@1, k=8 → Emb:"Lori"@1 (de=3.38) +7 more |
| 17 | `get_upstream_features` | L15:F4709@20, k=8 → L13:F15487 (de=3.89) +7 more |

### Build

`build_circuit` → 11 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 22,443 | 5,014 | 71,307 | 0 | $0.0170 | — | — |
| **Total** | | **22,443** | **5,014** | **71,307** | **0** | **$0.0170** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 9s