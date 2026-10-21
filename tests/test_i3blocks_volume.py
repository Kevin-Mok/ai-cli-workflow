"""Exercise volume click dispatch without touching the host mixer."""
import os
from pathlib import Path
import subprocess
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "dot_config/i3blocks/scripts/executable_volume"


class VolumeClicks(unittest.TestCase):
    def test_click_actions(self):
        for button, action in [(1, "unmute"), (3, "mute"), (2, "15%"), (4, "3%+"), (5, "3%-")]:
            with self.subTest(button=button):
                result = subprocess.run(
                    ["bash", "-c", '''
amixer() {
    if [[ $1 == -q ]]; then printf 'ACTION: %s\\n' "$*"; fi
    if [[ $* == *get* ]]; then printf '  Capabilities: pvolume pswitch\\n  Mono: Playback 50 [50%%] [on]\\n'; fi
    if [[ $* == *scontrols* ]]; then echo "Simple mixer control 'Master',0"; fi
}
pacmd() {
    if [[ $1 == list-sinks ]]; then printf '  * index: 0\\n    index: 1\\n'; fi
    echo "PACMD: $*"
}
source "$1"
''', "volume-test", str(SCRIPT)],
                    env={**os.environ, "BLOCK_BUTTON": str(button), "SUBSCRIBE": "0", "AUDIO_DELTA": "3", "MIXER": "default", "SCONTROL": "Master"},
                    capture_output=True, text=True, check=True,
                )
                self.assertIn(f"ACTION: -q -D default sset Master {action}\n", result.stdout)
                self.assertNotIn("PACMD:", result.stdout)


if __name__ == "__main__":
    unittest.main()
