#!/usr/bin/env python3
"""Behavior checks for the largest-day-file-size command."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "executable_largest-day-file-size"


class LargestDayFileSizeTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)

    def make_file(self, name, size, day):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"x" * size)
        timestamp = datetime.fromisoformat(f"{day}T12:00:00+00:00").timestamp()
        os.utime(path, (timestamp, timestamp))
        return path

    def run_script(self, *args):
        env = dict(os.environ, TZ="UTC")
        return subprocess.run(
            [sys.executable, str(SCRIPT), *map(str, args)],
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )

    def test_sums_nested_files_by_modification_day(self):
        self.make_file("a", 5, "2026-07-28")
        self.make_file("nested/file with space", 7, "2026-07-28")
        self.make_file("other", 11, "2026-07-29")
        (self.root / "linked").symlink_to(self.root / "other")

        result = self.run_script(self.root)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "📅 2026-07-28 12 B\n📅 2026-07-29 11 B\n")

    def test_tie_uses_earliest_date(self):
        self.make_file("later", 3, "2026-07-29")
        self.make_file("earlier", 3, "2026-07-28")

        result = self.run_script(self.root)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "📅 2026-07-28 3 B\n📅 2026-07-29 3 B\n")

    def test_shows_only_three_largest_days_with_human_readable_sizes(self):
        self.make_file("first", 5000, "2026-07-26")
        self.make_file("second", 2048, "2026-07-27")
        self.make_file("third", 1024, "2026-07-28")
        self.make_file("fourth", 512, "2026-07-29")

        result = self.run_script(self.root)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout,
            "📅 2026-07-26 4.9 KiB\n"
            "📅 2026-07-27 2.0 KiB\n"
            "📅 2026-07-28 1.0 KiB\n",
        )

    def test_displays_large_total_in_gib(self):
        path = self.make_file("large", 0, "2026-08-21")
        with path.open("wb") as file:
            file.truncate(32734342861)
        timestamp = datetime.fromisoformat("2026-08-21T12:00:00+00:00").timestamp()
        os.utime(path, (timestamp, timestamp))

        result = self.run_script(self.root)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "📅 2026-08-21 30.5 GiB\n")

    def test_empty_directory_has_actionable_error(self):
        result = self.run_script(self.root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no regular files", result.stderr)

    def test_missing_directory_has_actionable_error(self):
        result = self.run_script(self.root / "missing")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("directory", result.stderr)


if __name__ == "__main__":
    unittest.main()
