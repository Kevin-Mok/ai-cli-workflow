#!/usr/bin/env python3
"""Send one labeled visual probe; run in Kitty, inside or outside tmux."""
import argparse
import os
import subprocess
import sys
import time


def main() -> int:
    plain = '--plain' in sys.argv or os.environ.get('CLI_PLAIN') == '1'
    parser = argparse.ArgumentParser(description=('' if plain else '🔔 ') + (__doc__ or 'Visual probe'))
    parser.add_argument('--case', choices=('desktop', 'terminal'), default='terminal')
    parser.add_argument('--plain', action='store_true', help='use ASCII output')
    args = parser.parse_args()
    def say(icon: str, text: str) -> None:
        print(('' if plain else icon + ' ') + text, flush=True)
    if args.case == 'terminal' and not sys.stdout.isatty():
        say('❌', 'Run the terminal probe in an interactive Kitty terminal.')
        return 1
    route = 'desktop' if args.case == 'desktop' else ('tmux' if os.environ.get('TMUX') else 'Kitty')
    for remaining in range(5, 0, -1):
        say('🔔', f'{route} visual probe in {remaining}s; focus another app now.')
        time.sleep(1)
    title = 'Codex visual probe: ' + route
    try:
        if args.case == 'desktop':
            subprocess.run(['notify-send', '-a', 'codex-visual-probe', '-t', '15000', title,
                            'Desktop baseline; verify a visible popup.'], check=True, timeout=5)
        else:
            sequence = b'\x1b]9;' + title.encode() + b'\x07'
            if os.environ.get('TMUX'):
                sequence = b'\x1bPtmux;' + sequence.replace(b'\x1b', b'\x1b\x1b') + b'\x1b\\'
            sys.stdout.buffer.write(sequence)
            sys.stdout.buffer.flush()
    except (OSError, subprocess.SubprocessError):
        say('❌', 'Probe send failed; check the desktop notification service.')
        return 1
    say('👀', 'Probe sent; confirm the popup visually. Sending alone does not prove display.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
