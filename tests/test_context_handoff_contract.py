#!/usr/bin/env python3

import json
import re
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "dot_agents" / "skills" / "context-handoff"
SKILL_PATH = SKILL_ROOT / "SKILL.md"
SOURCE_PATH = SKILL_ROOT / "SOURCE.md"
METADATA_PATH = SKILL_ROOT / "agents" / "openai.yaml"
CATALOG_PATH = REPO_ROOT / "dot_agents" / "skills" / "README.md"
DOCTOR_PATH = REPO_ROOT / "scripts" / "executable_ai-workflow-doctor"
HEADINGS = (
    "Goal and Done Criteria",
    "Constraints",
    "Decisions",
    "Current State",
    "Evidence and Failed Attempts",
    "Artifacts",
    "Blockers",
    "Ordered Next Actions",
)


class ContextHandoffContractTest(unittest.TestCase):
    def read_required(self, path: Path) -> str:
        self.assertTrue(path.is_file(), f"required file is missing: {path}")
        return path.read_text(encoding="utf-8")

    def test_required_files_frontmatter_sentinel_and_word_budget(self) -> None:
        skill = self.read_required(SKILL_PATH)
        self.read_required(SOURCE_PATH)
        self.read_required(METADATA_PATH)

        self.assertLess(len(skill.split()), 500)
        frontmatter = skill.split("---", 2)[1]
        keys = re.findall(r"^([a-z_]+):", frontmatter, re.MULTILINE)
        self.assertEqual(keys, ["name", "description"])
        self.assertIn("name: context-handoff", frontmatter)
        self.assertRegex(frontmatter, r"description: Use when")
        self.assertEqual(skill.count("<!-- context-handoff: adapted -->"), 1)
        self.assertNotRegex(skill, r"(?i)\bTODO\b|replace with")

    def test_output_contract_has_exact_heading_order_and_budget(self) -> None:
        skill = self.read_required(SKILL_PATH)
        positions: list[int] = []
        for heading in HEADINGS:
            matches = list(
                re.finditer(rf"^## {re.escape(heading)}$", skill, re.MULTILINE)
            )
            self.assertEqual(len(matches), 1, heading)
            positions.append(matches[0].start())
        self.assertEqual(positions, sorted(positions))
        self.assertIn("at most 600 words", skill)
        self.assertIn("Return only the handoff", " ".join(skill.split()))

    def test_done_criteria_truth_and_evidence_contract(self) -> None:
        skill = self.read_required(SKILL_PATH)
        normalized = " ".join(skill.split())
        for required in (
            "DC1",
            "met = verified pass",
            "open = known incomplete",
            "failed = latest evidence contradicts it",
            "unknown = evidence is unavailable or stale",
            "exactly one evidence record for every listed DC",
            "check → observed result → evidence link or recovery action",
            "Use None only after an explicit check confirmed absence",
            "Use Unknown when something was not checked",
            "Do not infer from absent or stale evidence",
        ):
            self.assertIn(required, normalized)

    def test_low_context_failure_and_next_action_contract(self) -> None:
        skill = self.read_required(SKILL_PATH)
        normalized = " ".join(skill.split())
        for required in (
            "authoritative plan, status, log, or source artifact",
            "stable failure signature",
            "attempt count",
            "what changed between attempts",
            "observable retry condition",
            "Link artifacts instead of copying",
            "Owner:",
            "Action:",
            "Expected:",
            "Stop if:",
            "literal executable command or a precise path-scoped edit",
            "Never use anaphora such as original command, same command, or as above",
        ):
            self.assertIn(required, normalized)

    def test_openai_metadata_contract(self) -> None:
        metadata = self.read_required(METADATA_PATH)
        expected = (
            'interface:\n'
            '  display_name: "Context Handoff"\n'
            '  short_description: "Create compact, evidence-linked work handoffs"\n'
            '  default_prompt: "Use $context-handoff to create a compact, '
            'evidence-linked handoff for the current work."\n'
            'policy:\n'
            '  allow_implicit_invocation: true\n'
        )
        self.assertEqual(metadata, expected)
        short = "Create compact, evidence-linked work handoffs"
        self.assertGreaterEqual(len(short), 25)
        self.assertLessEqual(len(short), 64)

    def test_source_catalog_and_doctor_are_compatible(self) -> None:
        source = self.read_required(SOURCE_PATH)
        for required in (
            "- Upstream repo: `/home/example/coding/system_prompts_leaks`",
            "- Upstream commit: `5c86715f453f0eca188451a48bf5b165831d8b29`",
            "- Original source path: `Anthropic/Claude Code/compact-continuation-message-2.1.207.md`",
            "- Adapted on: `2026-07-13`",
            "- Adaptation basis:",
            "- Local adaptation:",
        ):
            self.assertIn(required, source)

        catalog = self.read_required(CATALOG_PATH)
        self.assertIn("[`context-handoff`](context-handoff/SKILL.md)", catalog)

        completed = subprocess.run(
            [str(DOCTOR_PATH), "--repo", str(REPO_ROOT), "--format", "json"],
            check=True,
            capture_output=True,
            text=True,
        )
        report = json.loads(completed.stdout)
        forbidden_keys = {
            "missing_source_provenance:context-handoff",
            "invalid_source_provenance:context-handoff",
            "uncatalogued_skill:context-handoff",
        }
        finding_keys = {finding["key"] for finding in report["findings"]}
        self.assertTrue(forbidden_keys.isdisjoint(finding_keys))


if __name__ == "__main__":
    unittest.main()
