# summary/

Supporting material for `SUMMARY.md` at the repository root. `SUMMARY.md` holds the result
tables. This directory holds `details.md`, the longer notes behind those tables, the
aggregates that back them, one generated detail page, and one figure.

```
summary/
├── details.md                                    the notes behind every table in SUMMARY.md
├── data/
│   ├── task1-probes/arm_scores.json              five arm scores, one canonical run each, plus cost
│   ├── task1-probes/stability_probes_arm1.json   traversal stability, 80 slugs by 5 passes
│   ├── task1-baselines/baseline_scores.json      Trans-cos and SAE-cos totals
│   ├── task2-elk/elk_arm_scores.json             six arm scores, cost, turn and duration medians
│   └── task2-elk/stability_elk_arm1.json         repeat and answer-stability blocks
├── task3-arditi-baseline.md                      generated, per-slug baseline detail
├── gen_task3_arditi.py                           the generator for that file
└── task3-best-of-n.png                           attempt-budget figure
```

## Why these JSON files exist

Most numbers in `SUMMARY.md` are recomputable from the committed archives under
`<task>/results/`. Two groups are not, and `data/` is what backs those.

The first group is anything derived from per-run `oracle_result.json` files. The archives
keep that file for three example slugs per arm, so orchestrator cost, tool-call counts,
turn medians and the grader-context character counts cannot be recomputed at full fidelity.

The second group is the task 1 traversal-stability table. Its aggregator enumerates runs by
globbing `oracle_result.json`, so on the sampled archive it sees three slugs rather than 80.
`data/task1-probes/stability_probes_arm1.json` is a byte-for-byte copy of the committed
`spurious-correlation/results/stability_probes_arm1.json`, kept here so every number cited
in `SUMMARY.md` and `details.md` has a file in one place.

`data/task2-elk/stability_elk_arm1.json` is likewise a copy of the `repeats` blocks inside
the committed `secret-elicitation/results/aggregate.json`.

## Why only one generator ships

Every table in `SUMMARY.md` and `details.md` was originally produced by a script that read on-disk
artifacts, so no number was ever typed by hand. Only one of those scripts can still
reproduce its own output from this repository, and it is the one kept here.

`gen_task3_arditi.py` reads `refusal-jailbreaking/baselines/arditi/runs/judge_summary.json`
and `refusal-jailbreaking/weights/arditi/refusal/summary.json`. Both are committed and
complete, so it runs offline and regenerates `task3-arditi-baseline.md` exactly.

```bash
python summary/gen_task3_arditi.py
python summary/gen_task3_arditi.py --out /tmp/check.md
```

`--out` repoints the destination, which is how you diff a fresh run against the committed
file without overwriting it. `--help` exits before the script reads or writes anything.

The other six generators were dropped rather than shipped half-working, because each needs
an input the release does not carry and would otherwise average a sample while labelling it
a whole.

| Dropped generator | Missing input |
|---|---|
| Task 1 combined tables | the ranked feature dumps under `probe_artifacts/`, available upon request, and `oracle_result.json` for all 400 arm-1 runs |
| Task 1 arm grid | `oracle_result.json` for every run, present for 15 of 400 on arm 1 and 3 of 80 on the others |
| Task 1 baselines | the ranked feature dumps under `probe_artifacts/` |
| Task 2 arms | `oracle_result.json` for every run, present for 15 of 240 on arm 1 and 3 of 48 on the others |
| Task 3 oracle arm 1 | `elicitation.json` for every run, present for 3 of 50 |
| Task 3 best-of-N | `elicitation.json` for every run, plus a noise-null measurement that is not committed |

The numbers those six produced are all still checkable. Task 1 and task 3 recompute from
the per-run judge files, which are complete, and task 2 recomputes from each arm's
`eval.json`. `details.md` names the backing file under every table.
