"""Run inside Kitty with +runpy to check real retained-history selection."""
from pathlib import Path
import runpy
from types import SimpleNamespace

from kitty.fast_data_types import Screen
from kitty_tests.base import parse_bytes

ROOT = Path(__file__).resolve().parents[1]
adapter = runpy.run_path(str(ROOT / 'dot_config/kitty/tmux_copy.py'))
for history_limit, count in ((1000, 200), (10, 200), (1000, 1)):
    screen = Screen(None, 5, 20, history_limit)
    # Soft wrapping must not add newlines to the copied logical text.
    lines = [f'LINE {n:04d} ' + 'word ' * 8 for n in range(count)]
    parse_bytes(screen, '\r\n'.join(lines).encode())
    child = SimpleNamespace(child_fd=-1, foreground_cmdline=['fish'], foreground_processes=[])
    window = SimpleNamespace(screen=screen, child=child)
    boss = SimpleNamespace(window_id_map={1: window})
    for _ in range(2):
        adapter['handle_result'](['tmux_copy.py', 'select-all'], None, 1, boss)
        selected = ''.join(screen.text_for_selection(False, True)).rstrip('\n')
        assert screen.has_selection()
        assert selected.endswith(lines[-1]), repr(selected[-100:])
        if history_limit == 1000:
            assert selected == '\n'.join(lines), repr(selected)
        else:
            assert not selected.startswith(lines[0]), 'Evicted text must not reappear'
    print(f'✅ Selected retained history: {count} lines, limit {history_limit}; repeat and wrapping passed')
