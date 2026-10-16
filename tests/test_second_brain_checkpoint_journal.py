#!/usr/bin/env python3

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "executable_second-brain"
SOURCE_VAULT = REPO_ROOT / "second-brain"


class SecondBrainCheckpointJournalTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        self.repo = self.root / "repo"
        self.remote = self.root / "remote.git"
        self.home = self.root / "home"
        self.state = self.root / "state"
        self.fake_bin = self.root / "bin"
        self.repo.mkdir()
        self.home.mkdir()
        self.fake_bin.mkdir()
        subprocess.run(
            ["git", "init", "--bare", str(self.remote)],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "init", "-b", "main", str(self.repo)],
            check=True,
            capture_output=True,
        )
        self.git("config", "user.name", "Checkpoint Journal Test")
        self.git("config", "user.email", "journal@example.invalid")
        shutil.copytree(SOURCE_VAULT, self.repo / "second-brain")
        (self.repo / "dot_codex").mkdir()
        self.target_config = self.repo / "dot_codex/config.toml"
        self.target_config.write_text('model = "target"\n', encoding="utf-8")
        (self.repo / "README.md").write_text("# Fixture\n", encoding="utf-8")
        gate = self.repo / "scripts/executable_readme-recruiter-sync"
        gate.parent.mkdir()
        gate.write_text(
            "#!/usr/bin/env bash\nprintf 'pass_no_change\\n'\n",
            encoding="utf-8",
        )
        gate.chmod(0o755)
        self.git("add", ".")
        self.git("commit", "-m", "chore: initialize fixture")
        self.git("remote", "add", "origin", str(self.remote))
        self.git("push", "-u", "origin", "main")

        self.live_config = self.home / ".codex/config.toml"
        self.live_config.parent.mkdir()
        self.config_sentinel = "PRIVATE_CONFIG_CONTENT_SENTINEL"
        self.live_config.write_text(
            f'model = "fixture"\nmessage = "{self.config_sentinel}"\n',
            encoding="utf-8",
        )
        chezmoi = self.fake_bin / "chezmoi"
        chezmoi.write_text(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "if [ \"${1:-}\" = source-path ] && "
            "[ \"${2:-}\" = \"$HOME/.codex/config.toml\" ]; then\n"
            "  printf '%s\\n' \"$TEST_CODEX_CONFIG_TARGET\"\n"
            "  exit 0\n"
            "fi\n"
            "exit 64\n",
            encoding="utf-8",
        )
        chezmoi.chmod(0o755)
        self.note_sentinel = "PRIVATE_NOTE_CONTENT_SENTINEL"
        decisions = self.repo / "second-brain/00 Context/Decisions.md"
        with decisions.open("a", encoding="utf-8") as stream:
            stream.write(f"\n- {self.note_sentinel}\n")
        self.env = {
            **os.environ,
            "HOME": str(self.home),
            "PATH": f"{self.fake_bin}{os.pathsep}{os.environ['PATH']}",
            "XDG_STATE_HOME": str(self.state),
            "SECOND_BRAIN_REPO_ROOT": str(self.repo),
            "SECOND_BRAIN_NOW": "2026-07-14T16:20:00-04:00",
            "TEST_CODEX_CONFIG_TARGET": str(self.target_config),
            "PYTHONDONTWRITEBYTECODE": "1",
        }

    def git(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *arguments],
            cwd=self.repo,
            check=True,
            capture_output=True,
            text=True,
        )

    def test_journal_output_never_echoes_note_or_config_content(self) -> None:
        completed = subprocess.run(
            [sys.executable, "-B", str(SCRIPT), "checkpoint", "--no-push"],
            cwd=self.root,
            env=self.env,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertNotIn(self.note_sentinel, completed.stdout)
        self.assertNotIn(self.note_sentinel, completed.stderr)
        self.assertNotIn(self.config_sentinel, completed.stdout)
        self.assertNotIn(self.config_sentinel, completed.stderr)
        self.assertEqual(completed.stderr, "")
        report = json.loads(completed.stdout)
        self.assertEqual(report["result"], "committed")
        self.assertEqual(
            report["paths"],
            ["second-brain/00 Context/Decisions.md"],
        )


if __name__ == "__main__":
    unittest.main()
