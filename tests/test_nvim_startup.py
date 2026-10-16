"""Exercise the real Neovim init and clipboard provider with disposable commands."""

import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
NVIM = shutil.which("nvim")


@unittest.skipUnless(NVIM, "Neovim is required")
class NeovimStartupTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="nvim-startup-")
        self.addCleanup(self.directory.cleanup)
        self.home = Path(self.directory.name)
        self.bin = self.home / "bin"
        self.bin.mkdir()
        (self.home / ".vimrc").write_text("set clipboard+=unnamedplus\n")
        self.probed = self.home / "xsel-probed"
        self.command("xsel", f": > '{self.probed}'\n/bin/sleep 1\n")
        self.command("xclip", "exit 0\n")
        self.env = {
            **os.environ,
            "HOME": str(self.home),
            "XDG_CONFIG_HOME": str(self.home / ".config"),
            "XDG_DATA_HOME": str(self.home / ".local/share"),
            "XDG_STATE_HOME": str(self.home / ".local/state"),
            "XDG_CACHE_HOME": str(self.home / ".cache"),
            "PATH": str(self.bin),
            "SHELL": "/bin/sh",
            "DISPLAY": ":999",
            "WAYLAND_DISPLAY": "",
            "TMUX": "",
        }

    def command(self, name, body):
        path = self.bin / name
        path.write_text("#!/bin/sh\n" + body)
        path.chmod(0o755)

    def provider(self, *commands, nvim=NVIM):
        result_path = self.home / "provider"
        result = subprocess.run(
            [nvim, "--headless", "-i", "NONE", "-n",
             *[arg for command in commands for arg in ("--cmd", command)],
             "-u", str(ROOT / "dot_config/nvim/init.vim"),
             "-c", f"call writefile([provider#clipboard#Executable()], '{result_path}')",
             "-c", "qa!"],
            env=self.env, capture_output=True, text=True, timeout=5,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result_path.read_text().strip()

    def test_x11_startup_skips_slow_xsel_clipboard_read(self):
        self.assertEqual(self.provider(), "xclip")
        self.assertFalse(self.probed.exists(), "Startup read the desktop clipboard")

    def test_wayland_keeps_native_provider(self):
        self.env["WAYLAND_DISPLAY"] = "wayland-999"
        self.command("wl-copy", "exit 0\n")
        self.command("wl-paste", "exit 0\n")
        self.assertEqual(self.provider(), "wl-copy")

    def test_without_xclip_keeps_automatic_detection(self):
        (self.bin / "xclip").unlink()
        self.assertEqual(self.provider(), "xsel")

    def test_without_display_does_not_choose_xclip(self):
        self.env["DISPLAY"] = ""
        self.assertNotEqual(self.provider(), "xclip")
        self.assertFalse(self.probed.exists())

    def test_explicit_provider_is_preserved(self):
        provider = "let g:clipboard = {'name': 'explicit', 'copy': {}, 'paste': {}}"
        self.assertEqual(self.provider(provider), "explicit")
        self.assertFalse(self.probed.exists())

    def test_legacy_neovim_keeps_automatic_detection(self):
        legacy = Path("/usr/bin/nvim")
        if not legacy.exists():
            self.skipTest("No distro Neovim installed")
        version = subprocess.run([str(legacy), "--version"], capture_output=True, text=True, check=True)
        match = re.search(r"NVIM v(\d+)\.(\d+)\.(\d+)", version.stdout)
        if not match or tuple(map(int, match.groups())) >= (0, 11, 1):
            self.skipTest("No legacy Neovim installed")
        self.assertEqual(self.provider(nvim=str(legacy)), "xsel")


if __name__ == "__main__":
    unittest.main()
