#!/usr/bin/env python3

from __future__ import annotations

import importlib
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPO_ROOT / "scripts"
SOURCE_VAULT = REPO_ROOT / "second-brain"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))


class SecondBrainConcurrentEditTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        (self.repo / ".git").mkdir()
        shutil.copytree(SOURCE_VAULT, self.repo / "second-brain")
        self.state = self.root / "state"
        self.env = {
            **os.environ,
            "HOME": str(self.root / "home"),
            "XDG_STATE_HOME": str(self.state),
            "SECOND_BRAIN_REPO_ROOT": str(self.repo),
            "SECOND_BRAIN_NOW": "2026-07-14T09:30:00-04:00",
        }
        Path(self.env["HOME"]).mkdir()
        self.vault = importlib.import_module("second_brain.vault")
        self.paths = importlib.import_module("second_brain.paths")

    @staticmethod
    def common(event_id: str) -> dict[str, object]:
        return {
            "schema_version": 1,
            "event_id": event_id,
            "source": "codex",
            "timestamp": "2026-07-14T09:30:00-04:00",
        }

    def test_capture_preserves_manual_edit_after_read(self) -> None:
        target = self.repo / "second-brain/00 Context/Decisions.md"
        before = target.read_bytes()
        manual = before + b"\nMANUAL_EDIT_SENTINEL\n"
        real_replace = self.paths.atomic_replace_if_unchanged

        def inject(root, path, expected_sha256, content, mode=0o644):
            path.write_bytes(manual)
            return real_replace(root, path, expected_sha256, content, mode)

        payload = {
            **self.common("decision-concurrent-001"),
            "title": "Preserve concurrent edits",
            "summary": "Abort tracked capture when the protected note changes.",
            "target": "00 Context/Decisions.md",
            "links": [],
            "visibility": "public-sanitized",
            "confirmed": True,
        }
        with mock.patch.dict(os.environ, self.env, clear=True):
            with mock.patch.object(
                self.vault,
                "atomic_replace_if_unchanged",
                side_effect=inject,
                create=True,
            ):
                with self.assertRaises(self.paths.PathError):
                    self.vault.capture("personal-decision", payload)

        self.assertEqual(target.read_bytes(), manual)
        self.assertNotIn(b"decision-concurrent-001", target.read_bytes())

    def test_focus_preserves_manual_edit_after_read(self) -> None:
        target = self.repo / "second-brain/05 Daily Notes/2026-07-14.md"
        before = target.read_bytes()
        manual = before + b"\nMANUAL_FOCUS_EDIT_SENTINEL\n"
        real_replace = self.paths.atomic_replace_if_unchanged

        def inject(root, path, expected_sha256, content, mode=0o644):
            path.write_bytes(manual)
            return real_replace(root, path, expected_sha256, content, mode)

        payload = {
            **self.common("focus-concurrent-001"),
            "date": "2026-07-14",
            "project": "ExampleProject",
            "outcome": "Validate 20 contest questions.",
            "done_when": "Twenty validations are complete.",
            "evidence": "https://example.invalid/evidence",
            "confirmed": True,
        }
        with mock.patch.dict(os.environ, self.env, clear=True):
            with mock.patch.object(
                self.vault,
                "atomic_replace_if_unchanged",
                side_effect=inject,
            ):
                with self.assertRaises(self.paths.PathError):
                    self.vault.focus(payload)

        self.assertEqual(target.read_bytes(), manual)
        self.assertNotIn(b"focus-concurrent-001", target.read_bytes())

    def test_closeout_rolls_back_own_write_and_preserves_manual_edit(self) -> None:
        focus_payload = {
            **self.common("focus-closeout-race-001"),
            "date": "2026-07-14",
            "project": "ExampleProject",
            "outcome": "Validate 20 contest questions.",
            "done_when": "Twenty validations are complete.",
            "evidence": "https://example.invalid/evidence",
            "confirmed": True,
        }
        with mock.patch.dict(os.environ, self.env, clear=True):
            self.vault.focus(focus_payload)

        daily = self.repo / "second-brain/05 Daily Notes/2026-07-14.md"
        project = self.repo / "second-brain/02 Projects/ExampleProject.md"
        daily_before = daily.read_bytes()
        project_manual = project.read_bytes() + b"\nMANUAL_PROJECT_EDIT_SENTINEL\n"
        real_replace = self.paths.atomic_replace_if_unchanged

        def inject(root, path, expected_sha256, content, mode=0o644):
            if path == project:
                path.write_bytes(project_manual)
            return real_replace(root, path, expected_sha256, content, mode)

        closeout_payload = {
            **self.common("closeout-concurrent-001"),
            "date": "2026-07-14",
            "project": "ExampleProject",
            "planned": "Validate 20 contest questions.",
            "completed": "Seventeen validations completed.",
            "evidence": "https://example.invalid/evidence",
            "blocker": "Three remain.",
            "decisions": [],
            "open": [],
            "next": "Finish three validations.",
            "confirmed": True,
        }
        with mock.patch.dict(os.environ, self.env, clear=True):
            with mock.patch.object(
                self.vault,
                "atomic_replace_if_unchanged",
                side_effect=inject,
            ):
                with self.assertRaises(self.paths.PathError):
                    self.vault.closeout(closeout_payload)

        self.assertEqual(daily.read_bytes(), daily_before)
        self.assertEqual(project.read_bytes(), project_manual)
        self.assertNotIn(b"closeout-concurrent-001", daily.read_bytes())
        self.assertNotIn(b"closeout-concurrent-001", project.read_bytes())

    def test_structure_rejects_required_heading_inside_frontmatter(self) -> None:
        target = self.repo / "second-brain/00 Context/Decisions.md"
        text = target.read_text(encoding="utf-8")
        text = text.replace("\n## Entries\n", "\n", 1).replace(
            "visibility: public-sanitized\n",
            "visibility: public-sanitized\n## Entries\n",
            1,
        )
        target.write_text(text, encoding="utf-8")
        before = target.read_bytes()
        payload = {
            **self.common("decision-frontmatter-001"),
            "title": "Reject hidden section",
            "summary": "Stable headings must appear after frontmatter.",
            "target": "00 Context/Decisions.md",
            "links": [],
            "visibility": "public-sanitized",
            "confirmed": True,
        }

        with mock.patch.dict(os.environ, self.env, clear=True):
            with self.assertRaises(self.paths.PathError):
                self.vault.capture("personal-decision", payload)

        self.assertEqual(target.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
