"""Exercise calendar protocol output without opening its popup."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "dot_config/i3blocks/scripts/executable_calendar"


class CalendarBlock(unittest.TestCase):
    def test_full_and_compact_text_keep_color_emoji(self):
        with tempfile.TemporaryDirectory() as home:
            colors = Path(home) / ".cache/wal/colors.sh"
            colors.parent.mkdir(parents=True)
            colors.write_text("color7='#112233'\n")
            result = subprocess.run(["sh", str(SCRIPT)], capture_output=True, text=True,
                                    env={**os.environ, "HOME": home, "BLOCK_BUTTON": "", "LABEL": "",
                                         "LC_ALL": "C"})
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stderr, "")
            full, short, color = result.stdout.splitlines()
            self.assertRegex(full, r"^📅[A-Za-z]{3} [0-9]{1,2}/[0-9]{1,2} [0-9]{2}:[0-9]{2}$")
            self.assertRegex(short, r"^🕒[0-9]{2}:[0-9]{2}$")
            self.assertEqual(color, "#112233")


if __name__ == "__main__":
    unittest.main()
