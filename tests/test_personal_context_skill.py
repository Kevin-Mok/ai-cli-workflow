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
    def test_skill_has_relevant_automatic_use_and_a_usable_chat_entrypoint(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = yaml.safe_load(skill.split("---", 2)[1])
        self.assertEqual(frontmatter["name"], "personal-context")
        self.assertIsInstance(frontmatter["description"], str)
        metadata = yaml.safe_load(
            (SKILL_ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
        )
        self.assertIs(metadata["policy"]["allow_implicit_invocation"], True)
        interface = metadata["interface"]
        self.assertIn("$personal-context", interface["default_prompt"])
        self.assertGreaterEqual(len(interface["short_description"]), 25)
        self.assertLessEqual(len(interface["short_description"]), 64)

    def test_relevance_routing_and_private_learning_are_explicit(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        canonical = (REPO_ROOT / "dot_codex/AGENTS.md").read_text(encoding="utf-8")
        for target in set(re.findall(r"\]\((references/[^)#]+\.md)(?:#[^)]*)?\)", canonical)):
            canonical += "\n" + (REPO_ROOT / "dot_codex" / target).read_text(encoding="utf-8")
        for text in (skill, canonical):
            normalized = " ".join(text.split())
            for trigger in ("direction", "scope", "architecture", "design", "tooling", "milestones", "collaboration"):
                self.assertIn(trigger, normalized)
            self.assertIn("Mechanical work", normalized)
            self.assertIn("plausible personal or cross-project connection", normalized)
        self.assertIn("unconfirmed", skill)
        self.assertIn("Current instructions and project", skill)
        self.assertIn("Do not infer ownership", skill)
        self.assertIn("temporary", skill)
        self.assertIn("Second Brain", skill)
        self.assertNotIn("Activate only on an explicit", skill)
        self.assertNotIn("Ordinary coding requests do not activate", canonical)

    def test_storage_reference_documents_bounded_evidence_and_private_foundation(self):
        reference = (SKILL_ROOT / "references/store-format.md").read_text(encoding="utf-8")
        normalized = " ".join(reference.split())
        for required in (
            "ai-context/context.json", "ai-context/project-knowledge.json",
            "ai-context/cache/topic-briefs.json", "topics", "projects --query",
            "brief --topic", "brief --project", "detail --id", "foundation --coding-root",
            "--batch-size", "--limit", "--char-budget", "6,000", "eight records",
            "input hashes", "input revisions", "read-only", "content hashes",
            "suppression", "dependent findings", "Missing", "atomic",
        ):
            self.assertIn(required, normalized)

    def test_foundation_requires_source_level_example-user_mok_commit_evidence(self):
        for path in (SKILL_ROOT / "SKILL.md", SKILL_ROOT / "references/store-format.md"):
            normalized = " ".join(path.read_text(encoding="utf-8").split())
            for required in (
                "example-user Mok", "case-insensitive", "latest modifying commit",
                "HEAD", "untracked", "nested", "email", "author_evidence",
                "exclusive ownership", "unavailable",
            ):
                self.assertIn(required, normalized)
        reference = (SKILL_ROOT / "references/store-format.md").read_text(encoding="utf-8")
        for required in ("repo_relative_path", "provenance_version", "blob_sha256", "historical"):
            self.assertIn(required, reference)
        for relative in ("README.md", "docs/smoke-tests.md", "dot_codex/AGENTS.md"):
            source = (REPO_ROOT / relative).read_text(encoding="utf-8")
            if relative == "dot_codex/AGENTS.md":
                for target in set(re.findall(r"\]\((references/[^)#]+\.md)(?:#[^)]*)?\)", source)):
                    source += "\n" + (REPO_ROOT / "dot_codex" / target).read_text(encoding="utf-8")
            self.assertIn("example-user Mok", source)

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
