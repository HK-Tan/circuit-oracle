"""Leaf module for cross-cutting constants.

Lives below config.py and subagent.py in the import graph so both can
share constants without inducing a circular import. Must remain
dependency-free.
"""

from __future__ import annotations


# Single flip-point for swapping subagent backend (Sonnet -> GPT-OSS-120B etc).
# Imported by subagent.py (used as the default model for trace_path_subagent /
# reinterpret_subagent) and by config.py (RunConfig.subagent_model default).
#
# Flipped sonnet-4-6 -> gpt-oss-120b 2026-07-28, which is the swap this constant
# was created for. gpt-oss-120b is the standard "everything else"
# model. Every ArmSpec already carries subagent_model=GPT_OSS by default, so an
# --arm run never reached the old value, but a RunConfig built without an
# explicit subagent_model did, and it routed to a model in no arm at roughly
# 20x the input price. Use the full slug so llm_client routing and
# saving.MODEL_PRICING both resolve it.
DEFAULT_SUBAGENT_MODEL = "openai/gpt-oss-120b"


__all__ = ["DEFAULT_SUBAGENT_MODEL"]
