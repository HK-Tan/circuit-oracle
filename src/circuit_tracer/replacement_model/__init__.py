"""
ReplacementModel implementations for different backends.
"""

from .batched import (
    BatchedInterventionBackend,
    BatchedInterventionMixin,
    BatchedInterventionResult,
    _compact_kv_cache,
    _normalize_intervention_row,
)
from .replacement_model import ReplacementModel

# BATCHED PORT: the batched names below are ours, re-exported at package level so
# `from circuit_tracer.replacement_model import _compact_kv_cache` keeps resolving
# against the package layout upstream adopted at v0.3.0. circuit_oracle/tools.py
# and the track_bc tests import them from exactly this path.
__all__ = [
    "ReplacementModel",
    "BatchedInterventionBackend",
    "BatchedInterventionMixin",
    "BatchedInterventionResult",
    "_compact_kv_cache",
    "_normalize_intervention_row",
]
