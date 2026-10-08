# Extend i3 Redshift temperature keys

Extend the current Alt+Super number shortcuts across 1 through 0, apply the configuration, and verify its syntax and live installation.

## Scope and decisions

The existing bindings use `$mod` = Mod1 (Alt) plus Mod4 (Super), and reset Redshift before setting temperature. Interpret 10–100 using the existing redshift-set convention (value times 100 Kelvin): 1000K through 10000K in 1000K increments. Keep grave reset and other shortcuts.

## Implementation

- [x] Capture initial git status; preserve all unrelated dirty files and existing README/smoke/ledger edits.
- [x] Check the defining mapping before editing, then extend the i3 block.
- [x] Add concise README and keyboard smoke instructions.
- [x] Run refresh-config, validate rendered i3 syntax, reload i3, and verify the live binding map.

## Verification

Check tracked and live i3 configs with this reproducible mapping check (the session ran its identical `/tmp/check-redshift-spectrum.py` version):

```python
import re
from pathlib import Path
expected = [(key, str(n * 1000)) for n, key in enumerate("1234567890", 1)]
for path in ("dot_config/i3/config.tmpl", "/home/example/.config/i3/config"):
    text = Path(path).read_text()
    actual = re.findall(r"^bindsym \$mod\+Mod4\+([0-9]) exec redshift -x && redshift -O (\d+)$", text, re.M)
    assert actual == expected
    assert "bindsym $mod+Mod4+grave exec redshift -x" in text
```

 Run `i3 -C -c ~/.config/i3/config`, then `i3-msg reload` and compare `get_config` bindings. Manually hold Alt+Super and press 1 through 0; expect warmer-to-cooler 1000K steps, then grave resets. Physical key presses remain user verification.

## Risks and rollback

10000K has a strong cool tint. Preserve modifiers and reset. Undo only the Redshift block and added documentation to roll back, refresh, reload. Session-only commit and push authorized through commit-session. Refresh snapshots live Codex and Git configuration; preflight shows no content drift. Initial sandbox failure is documented separately; approved scoped execution succeeds.

## Evidence and review

Initial inspection found only keys 1–5, with key 1 at 1100K. Defining RED check exited 1 for the expected five-key/1100K mismatch. Extended all ten keys and added documentation. GREEN mapping passed for tracked, installed, and running i3 configs. `fish -ic refresh-config` exited 0; `i3-msg reload` returned success. i3 syntax validation emitted existing deprecated wheel-command warnings. Live IPC verification passed with `i3-msg -r -t get_config`; initial human-output parsing failure documented separately. Physical keyboard/tint checks remain manual. README and smoke checks match the mapping.

Commit review: helper returned unsafe because it did not detect wrapped writes. Use direct-write attribution for the seven scoped files and only this session’s README, smoke-test, and ledger additions. README gate returned pass_no_change. Leave all unrelated baseline work dirty.
