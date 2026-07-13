#!/usr/bin/env python3

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "dot_agents" / "skills" / "metaprompt"
SKILL_PATH = SKILL_ROOT / "SKILL.md"
REFERENCE_NAMES = (
    "compilation-rules.md",
    "execution-routing.md",
    "examples.md",
)
OUTPUT_GATE_SENTINEL = "<!-- metaprompt-contract: output-gate-v1 -->"
ROUTING_SENTINEL = "<!-- metaprompt-contract: execution-routing-v1 -->"
LOADING_SENTINEL = "<!-- metaprompt-contract: reference-loading-v1 -->"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class MetapromptContractTest(unittest.TestCase):
    def test_skill_is_compact_with_minimal_frontmatter(self) -> None:
        skill = read(SKILL_PATH)
        self.assertLess(len(skill.split()), 500)

        frontmatter = skill.split("---", 2)[1]
        keys = set(re.findall(r"^([a-z_]+):", frontmatter, re.MULTILINE))
        self.assertEqual(keys, {"name", "description"})
        normalized_frontmatter = " ".join(frontmatter.lower().split())
        self.assertIn("follow-up standalone `go`", normalized_frontmatter)
        self.assertIn(
            "do not trigger for a one-word fact lookup", normalized_frontmatter
        )

    def test_references_exist_are_one_hop_and_preserve_detail(self) -> None:
        skill = read(SKILL_PATH)
        for name in REFERENCE_NAMES:
            path = SKILL_ROOT / "references" / name
            self.assertTrue(path.is_file(), f"missing reference: {name}")
            self.assertIn(f"references/{name}", skill)
            content = read(path)
            self.assertNotIn("references/", content)

    def test_always_loaded_skill_preserves_compile_and_gate_contract(self) -> None:
        skill = read(SKILL_PATH)
        normalized_skill = " ".join(skill.split())
        for required in (
            OUTPUT_GATE_SENTINEL,
            ROUTING_SENTINEL,
            LOADING_SENTINEL,
            "Every invocation returns a compiled prompt",
            "Complexity changes prompt weight, never whether",
            "standalone affirmative",
            "revision and re-gate",
            "Logistics riders",
            "first match wins",
            "```prompt",
            "Run:",
            "Weight:",
            "Assumptions:",
            "`go`",
        ):
            self.assertIn(required, normalized_skill)

        for loading_rule in (
            "Read [compilation rules](references/compilation-rules.md) "
            "for Standard or Complex compilation, sharpening, or evaluation.",
            "Read [execution routing](references/execution-routing.md) "
            "only after a standalone run signal.",
            "Read [examples](references/examples.md) only when an example "
            "would resolve a compilation choice.",
        ):
            self.assertIn(loading_rule, skill)

    def test_compilation_reference_preserves_quality_rules(self) -> None:
        rules = read(SKILL_ROOT / "references" / "compilation-rules.md")
        for required in (
            "Two input modes",
            "Complexity gate",
            "Quality core",
            "Compile recipe",
            "<quality_bar>",
            "Treat your first complete answer as a draft floor",
            "Behandle deine erste vollstaendige Antwort als Boden",
            "contradiction-check tail",
            "Separate judge from author",
            "Prompt mechanics",
            "Zeig nur die finale Version",
            "Eine Revision, keine Schleife",
            "<!-- metaprompt-reference: compilation-rules-v1 -->",
        ):
            self.assertIn(required, rules)

    def test_execution_reference_preserves_first_match_routing(self) -> None:
        routing = read(SKILL_ROOT / "references" / "execution-routing.md")
        for required in (
            "first match wins",
            "Recurring or time-driven",
            "Substantial work with a verifiable end-state",
            "Research, audit, broad parallel fan-out",
            "destructive or hard to reverse",
            "Otherwise (the common case)",
            "never claim you invoked a user-only command",
            "exact command",
            "Logistics riders",
            "reversibility check",
            "<!-- metaprompt-reference: execution-routing-v1 -->",
        ):
            self.assertIn(required, routing)

    def test_examples_reference_keeps_weight_and_failure_examples(self) -> None:
        examples = read(SKILL_ROOT / "references" / "examples.md")
        for required in (
            "Example 1 (Standard",
            "Example 2 (Trivial)",
            "Example 3 (Complex",
            "Anti-patterns",
            "artifact without an explicit slot",
            "Hardcoding model mechanics",
            "<!-- metaprompt-reference: examples-v1 -->",
        ):
            self.assertIn(required, examples)

    def test_metadata_is_discoverable_and_no_redundant_research_policy_exists(self) -> None:
        metadata = read(SKILL_ROOT / "agents" / "openai.yaml")
        for required in (
            'display_name: "Metaprompt"',
            "short_description:",
            'default_prompt: "Use $metaprompt',
        ):
            self.assertIn(required, metadata)

        self.assertFalse(
            (SKILL_ROOT / "references" / "research-routing.md").exists()
        )
        all_text = read(SKILL_PATH)
        for name in REFERENCE_NAMES:
            all_text += read(SKILL_ROOT / "references" / name)
        self.assertNotIn("system_prompts_leaks", all_text)
        self.assertNotIn("metaprompt-baseline-report", all_text)


if __name__ == "__main__":
    unittest.main()
