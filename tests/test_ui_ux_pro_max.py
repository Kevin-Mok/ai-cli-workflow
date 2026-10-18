"""Offline packaging checks for the explicit-only shared design search skill."""
import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "dot_agents/skills/ui-ux-pro-max"


class UiUxProMaxTest(unittest.TestCase):
    def test_shared_skill_is_explicit_only_and_attributed(self):
        text = (SKILL / "SKILL.md").read_text()
        self.assertIn("disable-model-invocation: true", text)
        self.assertIn("allow_implicit_invocation: false", (SKILL / "agents/openai.yaml").read_text())
        self.assertIn("56ea9cf174ed86786187daa9de0e6247cb0747e4", (SKILL / "SOURCE.md").read_text())
        self.assertIn("Copyright (c) 2024 Next Level Builder", (SKILL / "LICENSE").read_text())

    def test_offline_search_and_no_match_are_honest(self):
        for query, expected in [("keyboard focus", True), ("zxqvnevermatch987654321", False)]:
            with self.subTest(query=query):
                result = subprocess.run(["python3", str(SKILL / "scripts/search.py"), query,
                                         "--domain", "ux", "--json"],
                                        capture_output=True, text=True, check=True)
                payload = json.loads(result.stdout)
                self.assertEqual(payload["count"] > 0, expected)
                self.assertEqual(len(payload["results"]), payload["count"])


if __name__ == "__main__":
    unittest.main()
