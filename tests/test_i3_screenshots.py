from pathlib import Path
import os, subprocess, tempfile
script=Path('scripts/executable_i3-screenshot').resolve()
assert script.is_file(), 'missing shared i3 screenshot helper'
assert os.access(script, os.X_OK), 'screenshot helper must be executable'
source=Path('dot_config/i3/config.tmpl').read_text()
lines=[x for x in source.splitlines() if x.startswith('bindsym ') and 'i3-screenshot ' in x]
assert len(lines)==4
with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp)
    for name,body in {'maim':'printf "%s\\n" "$@" > "$HOME/maim-args"\n[ "$CANCEL" != 1 ] || exit 1\nfor arg; do last=$arg; done\nprintf PNG > "$last"','xclip':'for arg; do last=$arg; done\ncat "$last" > "$HOME/clipboard"','xdotool':'echo 123','date':'echo 2026-11-03_12:34:56'}.items():
        p=root/name;p.write_text('#!/bin/sh\n'+body+'\n');p.chmod(0o755)
    env={**os.environ,'HOME':tmp,'PATH':tmp+':'+os.environ['PATH']}
    for mode in ['region','window']:
        for folder in [root/'Pictures/screenshots/desktop/unsorted',root/'tmp with spaces']:
            subprocess.run([str(script),mode,str(folder)],env=env,check=True)
            assert (folder/'screenshot-2026-11-03_12:34:56.png').read_bytes()==b'PNG'
            args=(root/'maim-args').read_text().splitlines()
            if mode=='region':
                assert '--shader=i3-dim' in args and '--highlight' in args, 'region selector must shade outside selection'
            else:
                assert '--shader=i3-dim' not in args
            assert (root/'clipboard').read_bytes()==b'PNG'
            (root/'clipboard').write_bytes(b'unchanged')
            result=subprocess.run([str(script),mode,str(folder)],env={**env,'CANCEL':'1'})
            assert result.returncode != 0
            assert (root/'clipboard').read_bytes()==b'unchanged'
print('PASS: region/window preserve filenames, directories, clipboard and cancellation')
