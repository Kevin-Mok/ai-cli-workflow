"""Keep the newer main repository rule through conditional policy integration."""

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_exact_main_repository_rule_retained_in_mandatory_delivery_reference():
    original = subprocess.check_output(
        ["git", "show", "410feaa:dot_codex/AGENTS.md"], cwd=ROOT, text=True)
    start = original.index("- When asked to create a new GitHub repository,")
    rule = original[start:original.index("\n\n", start)]
    core = (ROOT / "dot_codex/AGENTS.md").read_text()
    delivery = (ROOT / "dot_codex/references/delivery.md").read_text()
    assert rule in delivery
    assert (core + delivery).count(rule) == 1
    route = next(line for line in core.splitlines() if "](references/delivery.md)" in line)
    assert "MUST read" in route
    assert "commit, push, merge or task handoff" in route
    assert "repo creation" in route
