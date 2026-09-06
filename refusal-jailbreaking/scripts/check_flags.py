#!/usr/bin/env python
"""Local pre-flight: confirm the harness grader wires up and the slug resolves.

No GPU, no model load, no network. The empty-list grader guard and the tool-list build
make no LLM calls, so you can verify wiring before burning VM time.

The causal-screening tool is retired. Causal discovery now follows the run mode, via
execute_tool(..., causal_discovery=causal), and the mode defaults to "causal", so the
screen-tool flag checks are gone. This now just sanity-checks that the orchestrator tool
list equals the base TOOLS, that the mode gate is wired, and that the screen tool is
fully absent.

Usage (from the refusal-jailbreaking/ folder, with circuit-oracle installed):
    python scripts/check_flags.py --slug chlorine-gas-household-cleaners
"""
import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

SCREEN_TOOL = "screen_upstream_causality"

_passed, _failed = 0, 0


def check(label, cond, detail=""):
    global _passed, _failed
    mark = "PASS" if cond else "FAIL"
    if cond:
        _passed += 1
    else:
        _failed += 1
    print(f"  [{mark}] {label}" + (f"  ({detail})" if detail else ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", default="chlorine-gas-household-cleaners")
    args = ap.parse_args()

    print(f"\n1. Slug resolves in data/prompts.json ({args.slug!r})")
    entries = json.loads((REPO / "data" / "prompts.json").read_text())["entries"]
    by_slug = {e.get("slug"): e for e in entries}
    e = by_slug.get(args.slug)
    check("slug present", e is not None, f"{len(entries)} entries")
    if e is not None:
        check("not disabled", not e.get("disabled", False))
        check("has user_message", bool(e.get("user_message")), f"category={e.get('category')}")

    print("\n2. Screen tool retired (causal discovery follows the run mode)")
    import circuit_oracle
    from circuit_oracle import tool_schemas as ts

    # Source-text checks read the INSTALLED package, wherever it lives. After the
    # merge that is the repo-root src/circuit_oracle/, not this folder's old src/.
    PKG = Path(circuit_oracle.__file__).resolve().parent

    base_names = {t["name"] for t in ts.TOOLS}
    check("base TOOLS excludes screen tool", SCREEN_TOOL not in base_names,
          f"{len(ts.TOOLS)} base tools")
    # Argless build_orchestrator_tools() is the causal default (causal=True, no
    # exclusions), so it must still return the full TOOLS list.
    orch_names = {t["name"] for t in ts.build_orchestrator_tools()}
    check("orchestrator tool list == base TOOLS", orch_names == base_names, f"{len(orch_names)} tools")
    check("causal_screen_enabled() removed", not hasattr(ts, "causal_screen_enabled"))
    check("SCREEN_UPSTREAM_CAUSALITY_SCHEMA removed", not hasattr(ts, "SCREEN_UPSTREAM_CAUSALITY_SCHEMA"))
    sub_src = (PKG / "subagent.py").read_text()
    check("subagent dispatch no longer registers screen tool", f'"{SCREEN_TOOL}"' not in sub_src)
    orch_src = (PKG / "orchestrator.py").read_text()
    check("orchestrator no longer references the screen env var",
          "CIRCUIT_ORACLE_CAUSAL_SCREEN" not in orch_src)
    check("orchestrator passes causal_discovery=causal", "causal_discovery=causal" in orch_src)
    # Quote-style agnostic on purpose. Any implementation of the gate names the
    # observational mode somewhere in orchestrator.py.
    check("mode gate present (observational mode named)", "observational" in orch_src)

    print("\n3. Harness grader empty-list guard (no network call)")
    from circuit_oracle.saving import grade_interventions

    class _Cfg:
        orchestrator_model = "openai/gpt-5.4"
        user_message = "test question"

    # The grader always runs when there are interventions, so the only network-free
    # path to check here is the empty-list guard that returns (None, None) up front.
    r_empty = grade_interventions([], _Cfg(), "baseline")
    check("empty interventions -> (None, None) (guard before any LLM call)",
          r_empty == (None, None))

    print(f"\n{'='*54}\n  {_passed} passed, {_failed} failed\n{'='*54}")
    sys.exit(1 if _failed else 0)


if __name__ == "__main__":
    main()
