"""Arm registry for the ablation grid.

One ``ArmSpec`` per (task, arm). An arm is a task key (which selects the orchestrator system prompt through the registry
in orchestrator.py) plus an orchestrator model, a subagent model, a tool
surface, and a discovery-annotation mode. Entry scripts resolve ``--arm``
through ``resolve_arm`` and refuse ad-hoc model/tool flags alongside it, so a
run's identity is one registry key rather than a hand-assembled flag set.

Sixteen arms: five on probes, five on refusal, and six on ELK, where each of
the three orchestrators runs both the closed and the open protocol.

Model IDs are the exact OpenRouter slugs verified live against the catalog on
2026-07-26. Do not "fix" them to display names.
"""

from __future__ import annotations

from dataclasses import dataclass

from .tool_schemas import TOOLS

M3 = "minimax/minimax-m3"
TERRA = "openai/gpt-5.6-terra"
GEMMA4 = "google/gemma-4-31b-it"
GPT_OSS = "openai/gpt-oss-120b"

# ELK runs two protocols over the same graphs, and they differ in the tool
# surface, not just the prompt. Closed mode shows the oracle the 20-word menu,
# so get_candidate_vote_tally (which tallies stems against that menu) is
# meaningful; open mode hides the menu, so the tally would leak it. Both drop
# the output-side tools, because the taboo LoRA is trained to steer its own
# logits away from the secret, and trace_path_subagent, because the track runs
# no subagent layer. These are the lists the two runner scripts pass, and they
# live here so the arm and the script cannot disagree about what a protocol is.
ELK_CLOSED_EXCLUDED_TOOLS = (
    "get_top_logits",
    "get_top_features",
    "trace_path_subagent",
)
ELK_OPEN_EXCLUDED_TOOLS = ELK_CLOSED_EXCLUDED_TOOLS + ("get_candidate_vote_tally",)

# What to record as the subagent model on a track whose ArmSpec says
# subagent_model=None. saving.py puts config.subagent_model in
# oracle_result.json, in the report header, and (shortened) in the run
# directory name, so naming a real model there would claim a layer that never
# ran. A literal None is not an option either: shorten_model_name rejects it.
# Safe because the string can never reach an API call. It is only ever passed
# on where trace_path_subagent is excluded, which the registry guarantees for
# every ELK arm, and nothing else in the package reads it.
NO_SUBAGENT = "none"


@dataclass(frozen=True)
class ArmSpec:
    """One arm of the ablation grid."""

    name: str
    task: str  # prompt-registry key: refusal | elk | probes | hallucination
    mode: str  # "causal" | "observational"
    orchestrator_model: str
    subagent_model: str | None = GPT_OSS  # None = track runs no subagent layer
    pipeline: str = "agentic"  # "agentic" | "oneshot"
    excluded_tools: tuple[str, ...] = ()
    annotation: str = "full"  # "full" | "shift_only" (arm 2's label-leak fix)
    # Sub-variant of a task that is a separate run rather than a separate
    # analysis: ELK's "closed" (menu shown) and "open" (menu hidden). Each has
    # its own runner script, prompt, and tool surface, so each orchestrator is
    # two arms. None on tracks that have only one protocol.
    protocol: str | None = None
    description: str = ""


_SPECS = [
    # ── Task 1, spurious probes (Gemma-2-2B, observational) ─────────────────
    ArmSpec(
        name="probes-arm1", task="probes", mode="observational",
        orchestrator_model=M3,
        description="Full pipeline (traversal + inspect).",
    ),
    ArmSpec(
        name="probes-arm2", task="probes", mode="observational",
        orchestrator_model=M3, excluded_tools=("inspect_feature",),
        description="Traversal with inspect_feature off.",
    ),
    ArmSpec(
        name="probes-arm3", task="probes", mode="observational",
        orchestrator_model=M3, pipeline="oneshot",
        description="One-shot top-k, no edge traversal.",
    ),
    ArmSpec(
        name="probes-arm4", task="probes", mode="observational",
        orchestrator_model=TERRA,
        description="Full pipeline, second orchestrator.",
    ),
    ArmSpec(
        name="probes-arm5", task="probes", mode="observational",
        orchestrator_model=GEMMA4,
        description="Full pipeline, open-weights orchestrator.",
    ),
    # ── Task 2, secret elicitation (Qwen3-8B taboo, observational) ──────────
    # The ELK arms vary only the orchestrator (settled 2026-07-26, no
    # tool-ablation arm on this track; its ablation is the phase 4 ranking
    # ladder). Each orchestrator is TWO arms, because closed and open are
    # separate runs with separate scripts, prompts, and tool surfaces, and a
    # run has to be able to say which one it was. Both runners pass their own
    # TABOO prompt, so task="elk" here is provenance rather than a prompt
    # lookup. No subagent layer on this track.
    ArmSpec(
        name="elk-arm1-closed", task="elk", mode="observational",
        orchestrator_model=M3, subagent_model=None, protocol="closed",
        excluded_tools=ELK_CLOSED_EXCLUDED_TOOLS,
        description="Published skill, closed protocol (20-word menu shown).",
    ),
    ArmSpec(
        name="elk-arm1-open", task="elk", mode="observational",
        orchestrator_model=M3, subagent_model=None, protocol="open",
        excluded_tools=ELK_OPEN_EXCLUDED_TOOLS,
        description="Published skill, open protocol (top-10 from open vocabulary).",
    ),
    ArmSpec(
        name="elk-arm2-closed", task="elk", mode="observational",
        orchestrator_model=TERRA, subagent_model=None, protocol="closed",
        excluded_tools=ELK_CLOSED_EXCLUDED_TOOLS,
        description="Second orchestrator, closed protocol.",
    ),
    ArmSpec(
        name="elk-arm2-open", task="elk", mode="observational",
        orchestrator_model=TERRA, subagent_model=None, protocol="open",
        excluded_tools=ELK_OPEN_EXCLUDED_TOOLS,
        description="Second orchestrator, open protocol.",
    ),
    ArmSpec(
        name="elk-arm3-closed", task="elk", mode="observational",
        orchestrator_model=GEMMA4, subagent_model=None, protocol="closed",
        excluded_tools=ELK_CLOSED_EXCLUDED_TOOLS,
        description="Open-weights orchestrator, closed protocol.",
    ),
    ArmSpec(
        name="elk-arm3-open", task="elk", mode="observational",
        orchestrator_model=GEMMA4, subagent_model=None, protocol="open",
        excluded_tools=ELK_OPEN_EXCLUDED_TOOLS,
        description="Open-weights orchestrator, open protocol.",
    ),
    # ── Task 3, suppression jailbreak (Qwen3-4B, causal) ────────────────────
    ArmSpec(
        name="refusal-arm1", task="refusal", mode="causal",
        orchestrator_model=M3,
        # The 5x repeat pass is a batch-level loop over this arm, not something
        # a single run_all.py invocation does. Nothing here schedules it.
        description="Full pipeline (traversal + inspect). Headline arm, repeated 5x.",
    ),
    ArmSpec(
        name="refusal-arm2", task="refusal", mode="causal",
        orchestrator_model=M3, excluded_tools=("inspect_feature",),
        annotation="shift_only",
        description="Traversal, no inspect, shift-only discovery annotation.",
    ),
    ArmSpec(
        name="refusal-arm3", task="refusal", mode="causal",
        orchestrator_model=M3, pipeline="oneshot",
        description="One-shot top-k, no traversal.",
    ),
    ArmSpec(
        name="refusal-arm4", task="refusal", mode="causal",
        orchestrator_model=TERRA,
        description="Full pipeline, second orchestrator.",
    ),
    ArmSpec(
        name="refusal-arm5", task="refusal", mode="causal",
        orchestrator_model=GEMMA4,
        description="Full pipeline, open-weights orchestrator.",
    ),
]

ARMS: dict[str, ArmSpec] = {spec.name: spec for spec in _SPECS}


def _validate_registry() -> None:
    """Fail loud at import if a spec names a tool that does not exist.

    A stale tool name in an exclusion list is a silent no-op downstream
    (build_orchestrator_tools does a plain set difference), which is exactly
    how the dead "get_diff_specific_features" entry survived in the ELK
    scripts. The registry refuses to carry one.
    """
    known = {t["name"] for t in TOOLS}
    for spec in ARMS.values():
        unknown = [name for name in spec.excluded_tools if name not in known]
        if unknown:
            raise ValueError(
                f"arm {spec.name!r} excludes unknown tool(s) {unknown}; "
                f"known tools: {sorted(known)}"
            )
        if spec.mode not in ("causal", "observational"):
            raise ValueError(f"arm {spec.name!r} has unknown mode {spec.mode!r}")
        if spec.pipeline not in ("agentic", "oneshot"):
            raise ValueError(
                f"arm {spec.name!r} has unknown pipeline {spec.pipeline!r}"
            )
        if spec.annotation not in ("full", "shift_only"):
            raise ValueError(
                f"arm {spec.name!r} has unknown annotation {spec.annotation!r}"
            )
        # Protocol and name must agree. The suffix is what a person reads off a
        # results directory, the field is what the runner checks, and a run
        # labelled -open that carried the closed tool surface would be
        # unfalsifiable after the fact.
        if spec.protocol is not None:
            if spec.protocol not in ("closed", "open"):
                raise ValueError(
                    f"arm {spec.name!r} has unknown protocol {spec.protocol!r}"
                )
            if not spec.name.endswith(f"-{spec.protocol}"):
                raise ValueError(
                    f"arm {spec.name!r} declares protocol {spec.protocol!r} but "
                    f"its name does not end in '-{spec.protocol}'"
                )
        if (spec.task == "elk") != (spec.protocol is not None):
            raise ValueError(
                f"arm {spec.name!r}: protocol is required on task 'elk' (closed "
                f"or open) and must be None elsewhere, got task={spec.task!r} "
                f"protocol={spec.protocol!r}"
            )


_validate_registry()


def get_arm(name: str) -> ArmSpec:
    """Resolve an arm by registry key. Unknown keys raise, listing the options."""
    try:
        return ARMS[name]
    except KeyError:
        raise KeyError(
            f"unknown arm {name!r}; known arms: {', '.join(sorted(ARMS))}"
        ) from None


def arm_names(task: str | None = None, protocol: str | None = None) -> list[str]:
    """Sorted registry keys, optionally narrowed to one task and protocol."""
    return sorted(
        name
        for name, spec in ARMS.items()
        if (task is None or spec.task == task)
        and (protocol is None or spec.protocol == protocol)
    )


def resolve_arm(
    name: str, *, task: str, protocol: str | None = None,
    pipeline: str | tuple[str, ...] = "agentic",
) -> ArmSpec:
    """Resolve ``--arm`` for an entry script that serves exactly one arm family.

    Every runner is single-task (and, on ELK, single-protocol), so passing it a
    foreign arm is a typo whose symptom would otherwise be a full batch of runs
    labelled with the wrong arm. Raises ValueError with a message an entry
    script can hand straight to ``parser.error``; shared here so the three
    runners cannot drift in which mismatches they catch.
    """
    try:
        spec = get_arm(name)
    except KeyError as e:
        raise ValueError(e.args[0]) from None
    if spec.task != task:
        raise ValueError(
            f"--arm {spec.name} belongs to task {spec.task!r}; this runner is "
            f"{task}-only ({task} arms: {', '.join(arm_names(task=task))})"
        )
    if protocol is not None and spec.protocol != protocol:
        raise ValueError(
            f"--arm {spec.name} is a {spec.protocol!r}-protocol arm; this runner "
            f"is the {protocol!r} one ({protocol} arms: "
            f"{', '.join(arm_names(task=task, protocol=protocol))})"
        )
    allowed = (pipeline,) if isinstance(pipeline, str) else tuple(pipeline)
    if spec.pipeline not in allowed:
        raise ValueError(
            f"--arm {spec.name} runs the {spec.pipeline!r} pipeline and this "
            f"entry script serves only {allowed}. Use the entry script that "
            "implements that pipeline."
        )
    return spec
