"""The batched intervention hooks and the tool surface built on them.

Covers `feature_intervention_batched`, `pin_features`, `batched_anchor_sweep`
and `batched_supernode_sweep`. The load-bearing tests are the batched-vs-single
parity ones, which pin that a K x 4 batched pass returns row for row what K x 4
separate single calls would.
"""
