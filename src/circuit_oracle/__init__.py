"""Circuit Oracle: Automated mechanism analysis of LLM circuits."""

from .config import RunConfig, ToolContext
from .query import build_oracle_query
from .neuronpedia_link import feature_url, feature_link

# Pure data plus an import-time validator, no torch or SDK underneath. Kept out
# of the try/except below so a broken heavy dependency cannot make ARMS vanish
# while __all__ still advertises it.
from .arms import ARMS, ArmSpec, get_arm

# These imports require external dependencies (openai, torch). Nothing here
# imports the anthropic SDK: LLMClient speaks the OpenAI chat-completions
# protocol and only the response SHAPE is Anthropic-like.
# They are re-exported for convenience but will raise ImportError if deps missing.
try:
    from .llm_client import LLMClient
    from .orchestrator import (
        run_circuit_oracle,
        ORACLE_SYSTEM_PROMPT,
        OBSERVATIONAL_SYSTEM_PROMPT,
        GENERIC_ORACLE_SYSTEM_PROMPT,
        generic_oracle_system_prompt,
        resolve_system_prompt,
    )
    from .control import run_control_analysis
except ImportError as ex:
    print(">>>", ex)
    pass

try:
    from .saving import save_run_results
except ImportError as ex:
    print(">>>", ex)
    pass

try:
    from .graph_compute import load_model, format_chat, compute_or_load_graph, generate_response
except ImportError as ex:
    print(">>>", ex)
    pass

try:
    from .self_rating import run_self_rating, extract_score_from_text
except ImportError as ex:
    print(">>>", ex)
    pass

__all__ = [
    "RunConfig",
    "ToolContext",
    "LLMClient",
    "run_circuit_oracle",
    "ORACLE_SYSTEM_PROMPT",
    "OBSERVATIONAL_SYSTEM_PROMPT",
    "GENERIC_ORACLE_SYSTEM_PROMPT",
    "generic_oracle_system_prompt",
    "resolve_system_prompt",
    "ARMS",
    "ArmSpec",
    "get_arm",
    "load_model",
    "format_chat",
    "compute_or_load_graph",
    "generate_response",
    "save_run_results",
    "build_oracle_query",
    "run_control_analysis",
    "run_self_rating",
    "extract_score_from_text",
    "feature_url",
    "feature_link",
]
