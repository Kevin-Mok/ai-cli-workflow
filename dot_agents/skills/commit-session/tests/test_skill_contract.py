import unittest
from pathlib import Path


SKILL_PATH = Path(__file__).resolve().parents[1] / "SKILL.md"


class CommitSessionSkillContractTestCase(unittest.TestCase):
    def test_safe_scoped_commit_continues_after_best_effort_checks(self):
        skill = SKILL_PATH.read_text(encoding="utf-8")

        self.assertIn(
            "Record failed focused validation as a warning and continue to staging.",
            skill,
        )
        self.assertIn(
            "If it fails, repair only truthful, repo-supported README issues before staging.",
            skill,
        )
        self.assertIn(
            "Do not skip a safe scoped commit solely because best-effort validation fails.",
            skill,
        )


if __name__ == "__main__":
    unittest.main()
