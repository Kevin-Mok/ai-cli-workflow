"""The plumbing commit caller must scan its frozen tree before commit creation."""
import os
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from second_brain import checkpoint
from second_brain.checkpoint_contract import CheckpointError


class CheckpointPrivacyTests(unittest.TestCase):
    def test_shared_gate_accepts_frozen_safe_tree_and_refuses_private_tree(self):
        self.assertTrue(hasattr(checkpoint, "_run_privacy_gate"), "checkpoint shared privacy gate is absent")
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "repo"
            repo.mkdir()
            scripts = repo / "scripts"
            scripts.mkdir()
            source = Path(__file__).resolve().parents[1] / "scripts"
            for name in ("executable_privacy-gate", "privacy_gate.py", "executable_audit-public-history", "privacy_gate_approvals.json"):
                shutil.copyfile(source / name, scripts / name)
            env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
            env.update(HOME=directory, GIT_CONFIG_NOSYSTEM="1")
            with patch.dict(os.environ, env, clear=True), patch.object(checkpoint, "__file__", str(repo / "installed" / "checkpoint.py")):
                def git(*args):
                    result = subprocess.run(["git", *args], cwd=repo, capture_output=True)
                    self.assertEqual(result.returncode, 0, "fixture Git operation failed")
                    return result.stdout.strip().decode()
                git("init", "-q")
                git("config", "user.name", "Example Maintainer")
                git("config", "user.email", "fixture@example.invalid")
                file = repo / "safe.txt"
                file.write_text("safe public bytes\n")
                git("add", "safe.txt")
                safe = git("write-tree")
                checkpoint._run_privacy_gate(repo, safe)
                file.write_text("ghp_" + "aB7C9dE2" * 5)
                git("add", "safe.txt")
                unsafe = git("write-tree")
                with self.assertRaises(CheckpointError):
                    checkpoint._run_privacy_gate(repo, unsafe)
                # A private index cannot substitute for the frozen safe tree.
                checkpoint._run_privacy_gate(repo, safe)
