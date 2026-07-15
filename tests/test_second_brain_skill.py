#!/usr/bin/env python3

import re
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "dot_agents" / "skills" / "second-brain-session"
SKILL_PATH = SKILL_ROOT / "SKILL.md"
ROUTING_PATH = SKILL_ROOT / "references" / "routing.md"
SOURCE_PATH = SKILL_ROOT / "SOURCE.md"
METADATA_PATH = SKILL_ROOT / "agents" / "openai.yaml"
CANONICAL_PATH = REPO_ROOT / "dot_codex" / "AGENTS.md"
CATALOG_PATH = REPO_ROOT / "dot_agents" / "skills" / "README.md"
CLAUDE_INSTALLER = REPO_ROOT / "run_after_install-claude-skills.sh.tmpl"


def read_required(path: Path) -> str:
    if not path.is_file():
        raise AssertionError(f"required file is missing: {path}")
    return path.read_text(encoding="utf-8")


class SecondBrainSkillTest(unittest.TestCase):
    def test_skill_frontmatter_and_word_budget(self) -> None:
        skill = read_required(SKILL_PATH)
        self.assertLess(len(skill.split()), 500)
        self.assertTrue(skill.startswith("---\n"))
        frontmatter = skill.split("---", 2)[1]
        keys = re.findall(r"^([a-z_]+):", frontmatter, re.MULTILINE)
        self.assertEqual(keys, ["name", "description"])
        self.assertIn("name: second-brain-session", frontmatter)
        self.assertRegex(frontmatter, r"description: Use when")
        self.assertNotRegex(skill, r"(?i)\b(?:TODO|TBD)\b|replace with")

    def test_skill_uses_targeted_reads_and_one_example-project_outcome(self) -> None:
        skill = read_required(SKILL_PATH)
        normalized = " ".join(skill.split())
        for required in (
            "second-brain/README.md",
            "last two or three Daily Notes",
            "active project summaries",
            "Do not load the entire vault",
            "exactly one measurable ExampleProject outcome",
            "Done when",
            "Evidence",
            "wait for example-user's confirmation",
            "second-brain focus --payload -",
        ):
            self.assertIn(required, normalized)

    def test_skill_routes_capture_and_closeout_without_committing(self) -> None:
        skill = read_required(SKILL_PATH)
        routing = read_required(ROUTING_PATH)
        combined = " ".join((skill + "\n" + routing).split())
        for required in (
            "second-brain capture --kind raw-session --payload -",
            "second-brain focus --payload -",
            "second-brain closeout --payload -",
            "feedback-memory/feedback.log",
            "tasks/lessons.md",
            "plans/",
            "Graphiti",
            "Taskwarrior/Taskopen",
            '"confirmed": true',
            "private raw",
            "redact",
            "Do not turn an interest into a project or task",
            "Never commit or push",
        ):
            self.assertIn(required, combined)

    def test_closeout_shape_is_boss_readable_and_confirmation_gated(self) -> None:
        routing = read_required(ROUTING_PATH)
        normalized = " ".join(routing.split())
        for required in (
            "Planned",
            "Completed",
            "Evidence",
            "Blocker",
            "boss-readable",
            "confirmation",
            "event_id",
            "schema_version",
        ):
            self.assertIn(required, normalized)
        closeout = routing.split("## Closeout", 1)[1]
        for field in (
            "schema_version",
            "event_id",
            "source",
            "timestamp",
            "date",
            "project",
            "planned",
            "completed",
            "evidence",
            "blocker",
            "decisions",
            "open",
            "next",
            "confirmed",
        ):
            self.assertIn(f'"{field}"', closeout)

    def test_tracked_capture_reference_is_complete_and_checkpoint_is_conditional(
        self,
    ) -> None:
        routing = read_required(ROUTING_PATH)
        tracked = routing.split("## Confirmed Tracked Capture", 1)[1].split(
            "## Confirmed Daily Focus", 1
        )[0]
        for field in (
            "schema_version",
            "event_id",
            "source",
            "timestamp",
            "title",
            "summary",
            "target",
            "links",
            "visibility",
            "confirmed",
        ):
            self.assertIn(f'"{field}"', tracked)
        self.assertIn("once installed", " ".join(routing.split()))

    def test_source_provenance_records_exact_audited_revision(self) -> None:
        source = read_required(SOURCE_PATH)
        for required in (
            "MIT",
            "/home/example/coding/second-brain-setup",
            "https://github.com/Alxve99/second-brain-setup",
            "90584269f7a4a47ea19f85a9029246873365aaf8",
            "README.md",
            "setup.md",
            "2026-07-14",
        ):
            self.assertIn(required, source)
        for field in (
            "- Upstream repo:",
            "- Upstream commit:",
            "- Original source path:",
            "- Supporting source paths:",
            "- Adapted on:",
            "- Adaptation basis:",
            "- Local adaptation:",
        ):
            self.assertIn(field, source)
        self.assertIn("once installed", source)
        self.assertNotIn("tested systemd checkpoint", source)

        completed = subprocess.run(
            [
                str(REPO_ROOT / "scripts" / "executable_ai-workflow-doctor"),
                "--repo",
                str(REPO_ROOT),
                "--format",
                "json",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        findings = {
            finding["key"] for finding in json.loads(completed.stdout)["findings"]
        }
        self.assertNotIn(
            "invalid_source_provenance:second-brain-session", findings
        )
        self.assertNotIn(
            "missing_source_provenance:second-brain-session", findings
        )

    def test_openai_metadata_is_valid_and_implicitly_discoverable(self) -> None:
        metadata = read_required(METADATA_PATH)
        expected = (
            'interface:\n'
            '  display_name: "Second Brain Session"\n'
            '  short_description: "Keep session context and closeouts reliable"\n'
            '  default_prompt: "Use $second-brain-session to start, capture, or '
            'close out work with the shared Second Brain."\n'
            'policy:\n'
            '  allow_implicit_invocation: true\n'
        )
        self.assertEqual(metadata, expected)
        short_description = "Keep session context and closeouts reliable"
        self.assertGreaterEqual(len(short_description), 25)
        self.assertLessEqual(len(short_description), 64)

    def test_canonical_route_is_concise_and_claude_uses_shared_directory(self) -> None:
        canonical = read_required(CANONICAL_PATH)
        route_matches = re.findall(r"second-brain-session", canonical)
        self.assertGreaterEqual(len(route_matches), 1)
        self.assertLessEqual(len(route_matches), 3)
        self.assertIn("conditional session", canonical.lower())

        installer = read_required(CLAUDE_INSTALLER)
        self.assertIn(".agents/skills", installer)
        self.assertRegex(installer, r"ln\s+-s")

    def test_skill_is_catalogued(self) -> None:
        catalog = read_required(CATALOG_PATH)
        self.assertIn(
            "[`second-brain-session`](second-brain-session/SKILL.md)",
            catalog,
        )

    def test_claude_installer_links_complete_skill_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            home = root / "home"
            agents = home / ".agents" / "skills"
            claude = home / ".claude" / "skills"
            agents.mkdir(parents=True)
            claude.mkdir(parents=True)
            target = agents / "second-brain-session"
            subprocess.run(
                ["cp", "-a", str(SKILL_ROOT), str(target)],
                check=True,
                capture_output=True,
            )
            rendered = root / "install-claude-skills.sh"
            template = read_required(CLAUDE_INSTALLER)
            rendered.write_text(
                template.replace("{{ .chezmoi.homeDir }}", str(home)),
                encoding="utf-8",
            )
            for _ in range(2):
                subprocess.run(
                    ["bash", str(rendered)],
                    check=True,
                    capture_output=True,
                    text=True,
                )
            installed = claude / "second-brain-session"
            self.assertTrue(installed.is_symlink())
            for relative_path in (
                "SKILL.md",
                "SOURCE.md",
                "agents/openai.yaml",
                "references/routing.md",
            ):
                self.assertTrue((installed / relative_path).is_file())


if __name__ == "__main__":
    unittest.main()
