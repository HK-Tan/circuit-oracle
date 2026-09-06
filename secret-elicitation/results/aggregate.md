# Taboo (ELK) eval aggregate

Source: `results/`, 6 arm(s).

## Headline

| arm | protocol | n | headline | top-5 | top-3 | top-1 | any-of-N | all-of-N | abstained |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| elk-arm1-closed | closed | 240 | **69.2%** | - | - | - | 8/8 | 0/8 | 0 |
| elk-arm1-open | open | 240 | **27.9%** | 25.8% | 23.3% | 20.4% | 7/8 | 0/8 | 4 |
| elk-arm2-closed | closed | 48 | **70.8%** | - | - | - | 8/8 | 1/8 | 0 |
| elk-arm2-open | open | 48 | **22.9%** | 20.8% | 16.7% | 14.6% | 6/8 | 0/8 | 0 |
| elk-arm3-closed | closed | 48 | **68.8%** | - | - | - | 8/8 | 0/8 | 0 |
| elk-arm3-open | open | 48 | **25.0%** | 22.9% | 22.9% | 22.9% | 5/8 | 0/8 | 1 |

Headline is exact-match accuracy for closed mode and top-10 recall for open mode. `any-of-N` counts secret words recovered on at least one prompt, `all-of-N` on every prompt.

## Run-to-run stability (repeated arms)

| arm | passes | mean | SD | 95% CI | min | max | answer flip | verdict flip | modal agree |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| elk-arm1-closed | 5 | 69.2% | ±0.9 | ±1.2 | 68.8% | 70.8% | 22.9% | 10.4% | 91.2% |

`elk-arm1-closed` per-pass: p1=68.8%, p2=68.8%, p3=68.8%, p4=70.8%, p5=68.8%

| elk-arm1-open | 5 | 27.9% | ±3.2 | ±3.9 | 22.9% | 31.2% | 81.2% | 41.7% | 52.5% |

`elk-arm1-open` shortlist stability: mean pairwise Jaccard **0.162** (median 0.121), 3.21 distinct rank-1 answers per item out of 5 passes.


`elk-arm1-open` per-pass: p1=29.2%, p2=27.1%, p3=29.2%, p4=31.2%, p5=22.9%


**answer flip** is the share of items whose rank-1 answer is not identical on every pass. **verdict flip** is the share whose correctness changes. Answer flip well above verdict flip means the oracle is stably wrong in varying ways.

