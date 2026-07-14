#!/usr/bin/env python3

import json
import re
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VAULT_ROOT = REPO_ROOT / "second-brain"
TODAY = "2026-07-14"

EXPECTED_FILES = (
    "README.md",
    ".obsidian/.gitignore",
    ".obsidian/app.json",
    ".obsidian/appearance.json",
    ".obsidian/snippets/example-user.css",
    "00 Context/About Me.md",
    "00 Context/Writing Style.md",
    "00 Context/Memory Map.md",
    "00 Context/Decisions.md",
    "00 Context/Learnings.md",
    "00 Context/AI Workflow.md",
    "00 Context/Audience and Privacy.md",
    "00 Context/External Locations.md",
    "01 Inbox/Brain Dump.md",
    "02 Projects/Linux Config AI Workflow.md",
    "02 Projects/ExampleProject.md",
    "02 Projects/Beginner Python Teaching Sites.md",
    "03 Areas/Work and Career.md",
    "03 Areas/AI Workflow.md",
    "03 Areas/Teaching.md",
    "03 Areas/Wellbeing.md",
    "03 Areas/Relationship.md",
    "04 Resources/AI Agents and Prompting.md",
    "04 Resources/Education Product Design.md",
    "04 Resources/CEMC Math Contest Prep.md",
    "04 Resources/Beginner Programming Pedagogy.md",
    "04 Resources/Software Architecture and UX.md",
    "04 Resources/Linux Automation.md",
    "04 Resources/Parent Facing Sales and Marketing.md",
    "04 Resources/CBT and Wellbeing.md",
    f"05 Daily Notes/{TODAY}.md",
    "06 Archive/README.md",
    "06 Archive/backups/README.md",
    "07 Attachments/README.md",
    "07 Attachments/External Media Index.md",
)

CONTEXT_NOTES = tuple(
    path for path in EXPECTED_FILES if path.startswith("00 Context/")
)
STATUS_NOTES = tuple(
    path
    for path in EXPECTED_FILES
    if path.startswith(
        (
            "01 Inbox/",
            "02 Projects/",
            "03 Areas/",
            "04 Resources/",
            "05 Daily Notes/",
        )
    )
)


def read(relative_path: str) -> str:
    path = VAULT_ROOT / relative_path
    if not path.is_file():
        raise AssertionError(f"required vault file is missing: {relative_path}")
    return path.read_text(encoding="utf-8")


def frontmatter(content: str) -> str:
    if not content.startswith("---\n"):
        raise AssertionError("note must begin with YAML frontmatter")
    parts = content.split("---\n", 2)
    if len(parts) != 3:
        raise AssertionError("note frontmatter must have a closing delimiter")
    return parts[1]


class SecondBrainVaultTest(unittest.TestCase):
    def test_exact_sanitized_tree_exists_without_unapproved_files(self) -> None:
        actual = tuple(
            sorted(
                path.relative_to(VAULT_ROOT).as_posix()
                for path in VAULT_ROOT.rglob("*")
                if path.is_file() and not path.is_symlink()
            )
        )
        self.assertEqual(actual, tuple(sorted(EXPECTED_FILES)))
        self.assertFalse(
            any(path.is_symlink() for path in VAULT_ROOT.rglob("*")),
            "the tracked vault must not contain symlinks",
        )

    def test_frontmatter_schema_is_consistent(self) -> None:
        for relative_path in CONTEXT_NOTES:
            metadata = frontmatter(read(relative_path))
            self.assertRegex(metadata, r"(?m)^tags: \[[^]]+\]$")
            self.assertRegex(metadata, rf"(?m)^date: {TODAY}$")
            self.assertRegex(metadata, r"(?m)^visibility: public-sanitized$")

        for relative_path in STATUS_NOTES:
            metadata = frontmatter(read(relative_path))
            self.assertRegex(metadata, r"(?m)^tags: \[[^]]+\]$")
            self.assertRegex(metadata, r"(?m)^status: [a-z-]+$")
            self.assertRegex(metadata, rf"(?m)^date: {TODAY}$")
            self.assertRegex(metadata, r"(?m)^visibility: public-sanitized$")

    def test_daily_note_has_stable_sections_in_order(self) -> None:
        daily = read(f"05 Daily Notes/{TODAY}.md")
        positions = []
        for heading in ("## Focus", "## Done", "## Decisions", "## Open", "## Next"):
            self.assertEqual(daily.count(heading), 1)
            positions.append(daily.index(heading))
        self.assertEqual(positions, sorted(positions))

    def test_front_door_surfaces_navigation_without_policy_duplication(self) -> None:
        front_door = read("README.md")
        for required in (
            "[[00 Context/About Me]]",
            "[[01 Inbox/Brain Dump]]",
            "[[02 Projects/Linux Config AI Workflow]]",
            "[[02 Projects/ExampleProject]]",
            "[[02 Projects/Beginner Python Teaching Sites]]",
            "[[05 Daily Notes/2026-07-14]]",
            "[[00 Context/Memory Map]]",
            "second-brain status",
        ):
            self.assertIn(required, front_door)
        for forbidden in (
            "# Canonical Codex Instructions",
            "## Git And Delivery",
            "## Bugs, Tests, And Implementation",
        ):
            self.assertNotIn(forbidden, front_door)

    def test_memory_map_links_every_canonical_owner_without_copying_content(self) -> None:
        memory_map = read("00 Context/Memory Map.md")
        for owner in (
            "dot_agents/skills/feedback-memory/feedback.log",
            "tasks/lessons.md",
            "plans/",
            "context-handoff",
            "Graphiti",
            "Taskwarrior/Taskopen",
            "second-brain/",
        ):
            self.assertIn(owner, memory_map)
        for link_target in (
            "../../dot_agents/skills/feedback-memory/feedback.log",
            "../../tasks/lessons.md",
            "../../plans/",
            "../../dot_agents/skills/context-handoff/SKILL.md",
            "../../docs/graphiti-mcp-codex.md",
        ):
            self.assertIn(f"]({link_target})", memory_map)
        self.assertNotIn(
            "Single-commit workflows push after the commit passes verification",
            memory_map,
        )

    def test_personalization_is_truthful_and_public_safe(self) -> None:
        about = " ".join(read("00 Context/About Me.md").split())
        for required in (
            "education AI",
            "Example Employer intern",
            "University of Toronto",
            "3.84",
            "AI-first",
        ):
            self.assertIn(required, about)
        self.assertNotRegex(about, r"(?i)hasn.t read (a line of )?code")

        privacy = read("00 Context/Audience and Privacy.md")
        for required in (
            "proprietary",
            "sanitized",
            "students",
            "parents",
            "teachers",
            "recruiters",
            "No credentials",
        ):
            self.assertIn(required, privacy)

        all_markdown = "\n".join(
            path.read_text(encoding="utf-8")
            for path in VAULT_ROOT.rglob("*.md")
        )
        self.assertNotRegex(all_markdown, r"sk-[A-Za-z0-9_-]{16,}")
        self.assertNotRegex(
            all_markdown,
            r"(?i)password\s*[:=]|api[_ -]?key\s*[:=]|private relationship detail",
        )

    def test_external_locations_and_migration_boundaries_are_explicit(self) -> None:
        locations = read("00 Context/External Locations.md")
        for required in (
            "/home/example/Documents/journal/",
            "/home/example/Documents/",
            "/home/example/Pictures/",
            "/mnt/linux-files-3/",
            "/mnt/linux-files-3/hevin/",
            "/home/example/coding/",
            "1,000,000 bytes",
            "reference-only",
        ):
            self.assertIn(required, locations)

    def test_obsidian_configuration_is_minimal_and_device_state_is_ignored(self) -> None:
        app = json.loads(read(".obsidian/app.json"))
        appearance = json.loads(read(".obsidian/appearance.json"))
        self.assertEqual(app["attachmentFolderPath"], "07 Attachments")
        self.assertIn("cssTheme", appearance)

        ignored = read(".obsidian/.gitignore")
        self.assertIn("workspace", ignored)
        self.assertIn("plugins/", ignored)

        css = read(".obsidian/snippets/example-user.css").lower()
        self.assertIn("hack", css)
        self.assertIn("#ee0000", css)
        self.assertNotIn("Example Employer logo", css)

    def test_attachment_policy_is_lfs_ready_but_initially_text_only(self) -> None:
        attachments = VAULT_ROOT / "07 Attachments"
        non_text = [
            path
            for path in attachments.rglob("*")
            if path.is_file() and path.suffix.lower() != ".md"
        ]
        self.assertEqual(non_text, [])
        policy = read("07 Attachments/README.md")
        self.assertIn("Git LFS", policy)
        self.assertIn("manual", policy.lower())
        self.assertIn("External Media Index", policy)

    def test_attachment_media_patterns_are_enforced_by_git_lfs(self) -> None:
        attributes = REPO_ROOT / ".gitattributes"
        self.assertTrue(attributes.is_file(), "Git LFS attributes are missing")
        extensions = (
            "png", "jpg", "jpeg", "gif", "webp", "avif", "svg", "pdf",
            "mp3", "wav", "m4a", "flac", "ogg", "opus", "aac",
            "mp4", "mov", "mkv", "webm", "avi",
        )
        for extension in extensions:
            relative = f"second-brain/07 Attachments/fixture.{extension}"
            completed = subprocess.run(
                [
                    "git", "check-attr", "filter", "diff", "merge", "text",
                    "--", relative,
                ],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                completed.stdout.splitlines(),
                [
                    f"{relative}: filter: lfs",
                    f"{relative}: diff: lfs",
                    f"{relative}: merge: lfs",
                    f"{relative}: text: unset",
                ],
            )

        markdown = "second-brain/07 Attachments/fixture.md"
        completed = subprocess.run(
            ["git", "check-attr", "filter", "--", markdown],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.stdout, f"{markdown}: filter: unspecified\n")

    def test_no_unresolved_placeholders_exist(self) -> None:
        placeholder = re.compile(
            r"\{\{[^}]+\}\}|(?i:\b(?:TBD|TODO)\b|replace with|your name here)"
        )
        for relative_path in EXPECTED_FILES:
            if not relative_path.endswith((".md", ".json", ".css", ".gitignore")):
                continue
            self.assertIsNone(
                placeholder.search(read(relative_path)),
                f"placeholder in {relative_path}",
            )


if __name__ == "__main__":
    unittest.main()
