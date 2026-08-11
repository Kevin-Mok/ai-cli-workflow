#!/usr/bin/env python3

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "dot_agents" / "skills" / "commit-plan-push"
SKILL_PATH = SKILL_ROOT / "SKILL.md"
METADATA_PATH = SKILL_ROOT / "agents" / "openai.yaml"
CATALOG_PATH = REPO_ROOT / "dot_agents" / "skills" / "README.md"
SMOKE_PATH = REPO_ROOT / "docs" / "smoke-tests.md"


def read_required(path: Path) -> str:
    if not path.is_file():
        raise AssertionError(f"required file is missing: {path}")
    return path.read_text(encoding="utf-8")


class CommitPlanPushSkillTest(unittest.TestCase):
    def test_skill_frontmatter_preserves_the_stable_slug(self) -> None:
        skill = read_required(SKILL_PATH)
        self.assertTrue(skill.startswith("---\n"))
        frontmatter = skill.split("---", 2)[1]
        keys = re.findall(r"^([a-z_]+):", frontmatter, re.MULTILINE)
        self.assertEqual(keys, ["name", "description"])
        self.assertIn("name: commit-plan-push", frontmatter)
        self.assertRegex(frontmatter, r"description: Use when")

    def test_picker_metadata_uses_the_requested_title(self) -> None:
        metadata = read_required(METADATA_PATH)
        expected = (
            'interface:\n'
            '  display_name: "Commit Plan & Push"\n'
            '  short_description: "Plan, commit, and push dirty Git work"\n'
            '  default_prompt: "Use $commit-plan-push to inspect the current '
            'dirty Git worktree, create the smallest safe commit series, and '
            'push it after verification."\n'
            'policy:\n'
            '  allow_implicit_invocation: false\n'
        )
        self.assertEqual(metadata, expected)

    def test_catalog_and_smoke_check_document_the_picker_metadata(self) -> None:
        catalog = read_required(CATALOG_PATH)
        self.assertIn(
            "[`commit-plan-push`](commit-plan-push/SKILL.md)", catalog
        )
        smoke_tests = read_required(SMOKE_PATH)
        self.assertIn("Commit Plan & Push", smoke_tests)
        self.assertIn("agents/openai.yaml", smoke_tests)


if __name__ == "__main__":
    unittest.main()
