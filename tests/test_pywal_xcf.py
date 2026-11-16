"""Exercise the XCF decoder fallback against the installed wallpaper asset."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path.home() / "Pictures/Backgrounds/fn-squid-game-bar.xcf"
ADAPTER = ROOT / "scripts/executable_pywal-readable"


@unittest.skipUnless(SOURCE.is_file() and shutil.which("gimp-console"),
                     "requires the local XCF wallpaper and GIMP Console")
class PywalXcfIntegrationTest(unittest.TestCase):
    def test_actual_xcf_is_decoded_into_cache_and_extracted(self):
        source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory(prefix="pywal-xcf-test-") as temporary:
            home = Path(temporary)
            cache = home / "pywal-cache"
            env = {
                **os.environ,
                "HOME": str(home),
                "PYWAL_CACHE_DIR": str(cache),
                "XDG_CACHE_HOME": str(home / ".cache"),
                "XDG_CONFIG_HOME": str(home / ".config"),
                "GIMP2_DIRECTORY": str(home / ".config/GIMP/2.10"),
                "PYTHONPATH": str(Path(__import__("pywal").__file__).parent.parent),
            }
            result = subprocess.run(
                [sys.executable, str(ADAPTER), "--saturate", "0.8", "-n", "-s", "-e", "-i", str(SOURCE)],
                env=env, capture_output=True, text=True, timeout=180,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            palette = json.loads((cache / "colors.json").read_text())
            decoded = Path(palette["wallpaper"])
            self.assertTrue(decoded.is_relative_to(cache))
            self.assertEqual(decoded.suffix.lower(), ".png")
            with Image.open(decoded) as image:
                self.assertEqual(image.size, (1920, 1080))
                self.assertNotEqual(image.getpixel((0, 0)), image.getpixel((1000, 500)))
            self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(), source_hash)


if __name__ == "__main__":
    unittest.main()
