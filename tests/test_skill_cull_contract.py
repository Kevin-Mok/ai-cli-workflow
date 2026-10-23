"""Protect survivor behavior when approved overlapping skills are removed."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "dot_agents/skills"


class SkillCullContractTest(unittest.TestCase):
    def test_commit_planning_only_stops_before_delivery(self):
        skill = (SKILLS / "commit-plan-push/SKILL.md").read_text()
        planning = skill.split("## Planning-only mode", 1)[1].split("## Required Workflow", 1)[0]
        planning += "\n" + (SKILLS / "commit-plan-push/references/planning-only.md").read_text()
        for requirement in ("commit-plan", "no Git writes", "Do not stage, commit, push",
                            "oldest-to-newest", "README", "warnings", "files",
                            "Conventional Commit", "chronology", "return"):
            self.assertIn(requirement, planning)
        self.assertIn("explicit execution request", planning)
        self.assertNotIn("use `commit-plan` instead", skill)

    def test_context_handoff_retains_long_task_acceptance_and_review(self):
        skill = (SKILLS / "context-handoff/SKILL.md").read_text()
        for requirement in ("task.md", "acceptance criteria", "checks.md", "progress.md",
                            "evidence-reviewer", "incorrect", "unresolved", "goal",
                            "existing goal", "Do not publish, push, send, or deploy",
                            "DC1", "met = verified pass", "unknown = evidence is unavailable or stale",
                            "Owner:", "Action:", "Expected:", "Stop if:"):
            self.assertIn(requirement, skill)
        self.assertIn("read `progress.md`", skill)

    def test_frontend_trigger_and_context_setup_have_a_survivor(self):
        skill = (SKILLS / "frontend-design/SKILL.md").read_text()
        description = re.search(r"^description: (.*)$", skill, re.M).group(1)
        self.assertIn("frontend", description)
        self.assertNotIn("posters", description)
        self.assertNotIn("artifacts", description)
        self.assertNotIn("teach-impeccable", skill)
        for requirement in (".impeccable.md", "audience", "brand", "ask", "backend"):
            self.assertIn(requirement, skill.lower())

    def test_readme_trigger_matches_the_gate_and_public_drift(self):
        skill = (SKILLS / "readme-recruiter-sync/SKILL.md").read_text()
        description = re.search(r"^description: (.*)$", skill, re.M).group(1)
        for requirement in ("README", "commit", "push", "public"):
            self.assertIn(requirement, description)
        self.assertNotIn("Assume it applies when changes touch", skill)
        self.assertIn("Always apply before commit or push", skill)


if __name__ == "__main__":
    unittest.main()
