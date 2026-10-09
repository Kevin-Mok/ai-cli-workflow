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

## Current revision: 600K intervals and zero filter

The latest user decision supersedes the original mapping: Alt+Super+1–9
selects 1200–6000K at 600K intervals; 0 and grave reset with `redshift -x`.
The low endpoint follows f.lux Windows Ember (1200K); nine presets cannot
include its 6500K neutral reference with exact 600K steps. This is accepted
by the explicit requested interval. Preserve all other shortcuts.

- [x] Capture dirty state and confirm defining RED: `/tmp/check-redshift-keys.py`
  exits 1 on the original ten temperature presets.
- [x] Update i3 block, README and keyboard smoke check.
- [x] Run GREEN against tracked, installed and running configuration.
- [x] Run refresh-config, validate i3 syntax and reload.

Protected baseline: README, feedback log, sources ledger and canonical AGENTS
were already dirty, plus untracked October 8 smoke-policy incident and session
insights. Preserve their contents. commit-session now authorizes commit and push. Rollback only this
revision's binding/docs changes, refresh and reload. Physical tint remains a
manual check. Verification will record commands and results below.

### Revision verification and handoff

`python3 /tmp/check-redshift-keys.py dot_config/i3/config.tmpl` exited 1
for the expected old mapping before editing, then exited 0 after editing.
Reusable `python3 scripts/smoke_redshift_keys.py` (tracked), the same command
with `~/.config/i3/config` (installed), and `--live` (running IPC) each exited 0.
`fish -ic refresh-config` exited 0 with REFRESH COMPLETE;
`i3 -C -c ~/.config/i3/config` exited 0 with existing wheel command deprecations;
`i3-msg reload` returned success true; `git diff --check` exited 0.
The incident ledger targeted check exited 0. Refresh introduced no additional
tracked dirty paths. Manual: Alt+Super+1 through 9 should get progressively
cooler at the documented temperatures; Alt+Super+0 and grave remove the filter.
Physical key/tint verification remains for the user. Delivery is authorized below.

Documentation updates: README mapping, smoke tests and reusable checker,
this plan amendment, runner incident and its reviewed ledger entry.
Commit suggestion: `feat(i3): use 600K Redshift steps and zero-filter reset`.
Paste-ready Cursor prompt: “Review the current Redshift revision in
plans/i3-redshift-spectrum.md. Verify Alt+Super+1–9 selects 1200–6000K in
600K steps and 0/grave run redshift -x. Run scripts/smoke_redshift_keys.py
against tracked, installed and live configs plus i3 syntax validation.
Preserve all unrelated dirty work; do not commit without authorization.”

### Delivery milestone: feat(i3): use 600K Redshift steps and zero-filter reset

Completed: config, README mapping, smoke checker/docs, incident and reviewed
ledger entry. Verified: all three mapping checks, i3 syntax (existing warnings),
refresh/reload, whitespace, targeted incident check; README gate pass_no_change.
Scope helper could not identify wrapped writes; use direct observed edits for
session 01a1214d-646b-7873-874e-dd9663faebf5. Stage only the Redshift README
hunk and this incident's ledger entry; preserve baseline policy/learning changes.
Remaining: physical tint/key check; no implementation blocker. Next: create the
focused commit, push main to origin/main, then report its hash and push result.
