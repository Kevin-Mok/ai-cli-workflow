import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "executable_codex-model-status"


class DotCodexModelStatusFilterTest(unittest.TestCase):
    @staticmethod
    def _run(*cmd: str, cwd: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(SCRIPT), *cmd],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,
        )

    @staticmethod
    def _init_repo(repo: Path) -> Path:
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        subprocess.run(
            ["git", "config", "user.name", "Codex Test"],
            cwd=repo,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.email", "test@example.invalid"],
            cwd=repo,
            check=True,
        )

        tracked_file = repo / "dot_codex" / "config.toml"
        tracked_file.parent.mkdir(parents=True)
        tracked_file.write_text(
            "model = \"gpt-5\"\n"
            "model_reasoning_effort = \"high\"\n"
            "personality = \"friendly\"\n"
        )
        subprocess.run(
            ["git", "add", "dot_codex/config.toml"],
            cwd=repo,
            check=True,
        )
        subprocess.run(
            ["git", "commit", "-qm", "chore: seed tracked config"],
            cwd=repo,
            check=True,
        )

        return tracked_file

    def test_model_only_edit_is_hidden(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            repo = Path(temporary_dir) / "repo"
            repo.mkdir()
            tracked_file = self._init_repo(repo)

            tracked_file.write_text(
                "model = \"model-hidden-in-status\"\n"
                "model_reasoning_effort = \"high\"\n"
                "personality = \"friendly\"\n"
            )

            status = self._run("--short", "-u", cwd=repo)
            self.assertEqual(status.stdout, "")

    def test_non_model_edit_remains_visible(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            repo = Path(temporary_dir) / "repo"
            repo.mkdir()
            tracked_file = self._init_repo(repo)

            tracked_file.write_text(
                "model = \"gpt-5\"\n"
                "model_reasoning_effort = \"low\"\n"
                "personality = \"friendly\"\n"
            )

            status = self._run("--short", "-u", cwd=repo)
            self.assertIn("dot_codex/config.toml", status.stdout)
            self.assertIn("M dot_codex/config.toml", status.stdout)

    def test_clean_file_is_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            repo = Path(temporary_dir) / "repo"
            repo.mkdir()
            self._init_repo(repo)

            status = self._run("--short", "-u", cwd=repo)
            self.assertEqual(status.stdout, "")


if __name__ == "__main__":
    unittest.main()
