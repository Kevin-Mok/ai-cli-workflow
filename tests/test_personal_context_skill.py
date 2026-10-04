#!/usr/bin/env python3
"""Exercise skill metadata and its installed layout with synthetic data only."""

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "dot_agents/skills/personal-context"


class PersonalContextSkillTest(unittest.TestCase):
    def test_skill_is_explicit_only_and_has_a_usable_chat_entrypoint(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = yaml.safe_load(skill.split("---", 2)[1])
        self.assertEqual(frontmatter["name"], "personal-context")
        self.assertIsInstance(frontmatter["description"], str)
        metadata = yaml.safe_load(
            (SKILL_ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
        )
        self.assertIs(metadata["policy"]["allow_implicit_invocation"], False)
        interface = metadata["interface"]
        self.assertIn("$personal-context", interface["default_prompt"])
        self.assertGreaterEqual(len(interface["short_description"]), 25)
        self.assertLessEqual(len(interface["short_description"]), 64)

    def test_supporting_references_are_inside_the_package(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        references = re.findall(r"\]\(([^)]+)\)", skill)
        self.assertTrue(references)
        for reference in references:
            target = (SKILL_ROOT / reference.split("#", 1)[0]).resolve()
            self.assertTrue(target.is_relative_to(SKILL_ROOT.resolve()))
            self.assertTrue(target.is_file(), reference)
        self.assertFalse(list(SKILL_ROOT.rglob("context.json")))

    def test_fresh_install_links_the_whole_skill_and_reads_without_writing(self):
        with tempfile.TemporaryDirectory(prefix="personal-context-install-") as tmp:
            root = Path(tmp)
            home = root / "home"
            installed = home / ".agents/skills/personal-context"
            shutil.copytree(SKILL_ROOT, installed)
            script = root / "link-skills.sh"
            template = (REPO_ROOT / "run_after_install-claude-skills.sh.tmpl").read_text()
            script.write_text(template.replace("{{ .chezmoi.homeDir }}", str(home)))
            for _ in range(2):
                result = subprocess.run(
                    ["bash", str(script)], capture_output=True, text=True
                )
                self.assertEqual(result.returncode, 0, result.stderr)
            linked = home / ".claude/skills/personal-context"
            self.assertTrue(linked.is_symlink())
            for name in (
                "SKILL.md", "agents/openai.yaml", "references/store-format.md",
                "scripts/context_store.py",
            ):
                self.assertTrue((linked / name).is_file(), name)
            private = root / "synthetic-context"
            private.mkdir()
            result = subprocess.run(
                [sys.executable, "-B", str(linked / "scripts/context_store.py"),
                 "--root", str(private), "read"],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["entries"], [])
            self.assertFalse((private / "ai-context").exists())


if __name__ == "__main__":
    unittest.main()
