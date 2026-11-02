# Reduce the 4K bar font

Reduce only DP-2's font while preserving live i3 additions and the other bars.
Update the tracked template and current documentation, refresh configuration,
then validate and activate the live change with one reload.

## Scope and decisions

- Initially reduce 50 to 47.8667 points (four pixels at Xft.dpi=135).
- Follow-up request: another three pixels smaller, setting 46.2667 points;
  `(47.8667 - 46.2667) * 135 / 72` is three pixels at the current DPI.
- Change `dot_config/i3/config.tmpl` and only the corresponding live font line.
- `.chezmoiignore` excludes live `.config/i3/`; do not replace the live file
  with the template, because it contains unrelated local additions.
- Update only the current font figures in README and existing smoke checks.
- Record inspection failures and reviewed incident knowledge separately.
- No changes to music fitting, workspace labels, other monitors or DPI.

## Protected state and rollback

The initial Git status was captured. README, smoke tests, incident knowledge,
music fitting, instructions and concert-video work were already dirty and are
protected. Preserve their unrelated hunks. The user subsequently requested a
session-only commit and push. Restore only DP-2 to 50 to roll back; reload once.
The pixel equivalence applies to the current 135 DPI.

## Ordered work

- [x] Confirm source and live DP-2 font 50, DPI 135 and unchanged other bars.
- [x] Change the tracked font and current documentation.
- [x] Run `fish -c refresh-config` and patch only the unmanaged live font line.
- [x] Validate deployed config with `i3 -C -c ~/.config/i3/config`.
- [x] Reload once; read all live bar fonts and verify the four-pixel delta.
- [x] Review scoped diff and record results and remaining limits.

## Verification and review

Baseline live fonts: HDMI-0 35.6, DVI-D-0 30, DP-2 50 points. A new automated
test is unnecessary for this reversible numeric setting. Use the real i3 parser
and live IPC as the defining checks. Manual: inspect the 4K bar for readability;
no workspace moves or pointer clicks are needed. No full-repository test run.

## Cursor continuation prompt

Read this plan, preserve unrelated changes, verify only the DP-2 font reduction,
and finish the authorized session-only commit and upstream push.
Suggested commit: `style(i3): reduce 4k bar font`.

## Evidence

- `fish -c refresh-config`: REFRESH COMPLETE, exit 0.
- Candidate and deployed `i3 -C -c` checks: exit 0. A separate comparison
  of stdout and stderr confirmed the same six existing wheel-command
  deprecation diagnostics in the baseline backup and updated config.
- `i3-msg reload`: success true; only one reload was performed.
- Fresh `i3-msg -t get_bar_config` for all bars: HDMI-0 remains 35.6,
  DVI-D-0 remains 30 and DP-2 is 47.8667 points. At the observed 135 DPI,
  the nominal reduction is 3.9999 pixels after rounding.
- Compared the original live backup `/tmp/i3-font-before-trlj7o5b.conf`
  with the installed file: only the DP-2 numeric font value differs.
- `./scripts/executable_readme-recruiter-sync`: pass_no_change, exit 0.
- Scoped `git diff --check`: exit 0. Production template diff is one line.
- Targeted incident-memory check: no errors, exit 0; see the
  [inspection report](../docs/postmortem/2026-10-29-4k-font-inspection.md).
- An overbroad final probe assertion compared complete workspace objects and
  failed after successful activation. Resizing the bar can change workspace
  rectangles; the probe did not persist the baseline, so focus/ID preservation
  was not independently established. No workspace moves were issued or retried.
- Physical visual inspection and a full-repository test run were skipped.
  The point-based size persists in the tracked template and unmanaged live
  config; the four-pixel equivalence depends on the current DPI.
- No commit or push performed. All pre-existing unrelated changes remain.

## Follow-up: another three pixels

- [x] Confirm live 47.8667-point DP-2 font and 135 DPI before editing.
- [x] Set tracked DP-2 font to 46.2667 and update current docs.
- [x] Refresh configuration, validate and update only the live font line.
- [x] Reload once; verify live fonts and stable workspace identity/focus fields.
- [x] Record verification evidence and review the scoped diff.

Rollback for this follow-up: restore only DP-2 to 47.8667 points, then reload.
Manual verification remains visual inspection of DP-2; no workspace moves needed.

Follow-up evidence (fresh checks in this turn):

- `fish -c refresh-config`: REFRESH COMPLETE, exit 0.
- Baseline, candidate and deployed `i3 -C -c` checks: exit 0, identical
  diagnostics. `i3-msg reload`: success true, one reload.
- Live bar IPC reads: DP-2 46.2667; HDMI-0 35.6 and DVI-D-0 30 unchanged.
- The live file differs only in the requested font value from backup
  `/tmp/i3-font-before-3px-03gb3y4s.conf`; the additional reduction is three
  pixels at the confirmed 135 DPI.
- Stable workspace IDs, names, outputs, visibility and focus were identical
  before/after; geometry was intentionally excluded from this comparison.
- README check: pass_no_change, exit 0. Scoped whitespace check: exit 0.
- Tracked production diff remains one numeric font line. No new automated test
  or full-repository run for this reversible setting; no physical visual check.
- Current README and smoke checks now use 46.2667 points (32.39 for music).
  No commit or push performed; unrelated work remains untouched.

## Delivery milestone: `style(i3): reduce 4k bar font`

- Scope fallback: helper returned `unsafe` with no detected writes for session
  `01a189e5-42b9-7572-9a48-33383a25ac21`; the conversation directly records
  changes to the font template, README, smoke tests, this plan, the inspection
  report and its incident-ledger entry. No timestamp-based attribution is used.
- Shared documentation: commit standalone font notes only. Music-fitting and
  concert-video edits remain unstaged. Remove incidental numeric music text
  from the working notes so font documentation can be staged independently.
- Incident ledger: include only this report's entry, preserving other sessions'
  findings, reports and formatting changes outside the candidate.
- Completed: source/live font reduction, refresh, fresh parser and runtime
  checks, README gate for both working and isolated candidate versions, scoped
  whitespace checks and incident-memory validation against committed references.
  Candidate review confirms exactly six files with only standalone font notes
  and this report entry in mixed files. Remaining: stage the reviewed candidate,
  pass the privacy gate, commit and push once to `origin/main`.
  Blockers: none identified. This milestone is ready for the authorized commit;
  the resulting SHA and actual push result are reported in the conversation.
- No additional activation or workspace movement is needed. Physical visual
  inspection and full-repository tests remain outside this numeric change.
