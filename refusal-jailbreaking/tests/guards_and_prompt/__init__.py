"""System-prompt content and the end-of-turn guards.

These tests assert against `ORACLE_SYSTEM_PROMPT` and the guard functions in
`circuit_oracle.orchestrator`. Half of them check that the prompt carries the
instructions the pipeline depends on (pin coverage, the cross-route supernode
requirement, the worked examples), and half check that each guard fires on the
transcript shape it is meant to catch.

See the module docstring of each `test_guards_*.py` file for the exact symbol
it imports.
"""
