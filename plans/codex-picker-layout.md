# Compact Codex picker layout

Make saved sessions easier to scan with abbreviated directories, tight spacing,
full titles and a readable recap preview.

## Context and decisions

User screenshot shows truncated titles and wide tab gaps in fzf 0.44.1.
Abbreviate parent components to their first character, preserve final basename,
and append >: /mnt/usb-8tb/ becomes /m/usb-8tb>. Preserve original directory for
preview and resume. Show directory, title, compact Toronto timestamp; recap
status/headline belong in preview. Use one-column tabs, no horizontal auto-scroll,
and responsive preview below the list on narrow windows, right on wide windows.
Full title remains available in wrapped preview at every width. Existing dirty
work captured before editing; no staging, commit or unrelated edits.

## Checklist

- [x] Inspect current layout, fzf help and existing terminal fixtures.
- [x] Observe path/display regression RED: all three raw-path versus abbreviated-path cases failed, exit 1.
- [x] Implement compact path and responsive layout; update docs.
- [x] Run Codex regressions and real-terminal fixtures at narrow/wide sizes.
- [x] Apply exact installed module and record evidence.

## Risks and rollback

fzf 0.44 cannot wrap list items; arbitrarily long titles require wrapped preview.
Abbreviated parents may collide; full path and UUID remain authoritative.
Revert only these renderer/options/test/docs hunks and reinstall the module.
The man-page lookup failed due to an absent assumed path; recorded separately.

## Verification and handoff

Run python3 -m unittest discover -s tests -p 'test_codex_search*.py'.
Manual: reopen crg; inspect /m/usb-8tb> and complete selected title; resize narrow
and wide, filter by title/directory/date, Ctrl-G then Enter/Esc; resume real cwd.
Cursor prompt: Finish plans/codex-picker-layout.md, preserve all unrelated work,
run the stated regressions and real fzf fixture, activate only the picker module.
Suggested commit: fix(codex): tighten recent picker layout.

## Final evidence and review

- python3 -m unittest discover -s tests -p 'test_codex_search*.py':
  91 tests passed in 17.035s, exit 0.
- python3 tests/scripts/codex_recent_live_check.py: exit 0 after using longer
  complete titles; real fzf at 150 and 80 columns verifies query, selection,
  recap reloads, Ctrl-G, Enter, cancellation and worker cleanup.
- chezmoi apply --force -- /home/example/scripts/codex_search_recent.py: exit 0.
  Installed bytes match source; real render verifies /m/usb-8tb>, full title,
  short Toronto timestamp and original directory in preview.
- git diff --check: exit 0. Incident targeted learning check: exit 0, no errors.

Only preview/list formatting changes; stored entries and exact UUID resume
remain intact. Search now uses abbreviated directory text as documented. Full
titles wrap in preview; extremely long list titles still require Ctrl-/ or a wider
window because installed fzf cannot wrap list items. No personal-history interactive
inspection, broad config refresh (no configuration changes), commit or push.

## Authorized delivery

On 2026-10-08 the user invoked commit-session and explicitly approved including
the pre-existing recent-picker implementation and required modules/tests. The
scope helper returned unsafe because it could not observe function-wrapped
writes; direct conversation write evidence plus that approval establishes scope.
Session: 01a11c3a-cb20-7082-94dc-2750703a5978. Preserve all unrelated hunks in
README, aliases, smoke tests, learning ledger and lessons. Include associated
plans, specification and nine reviewed incident reports with this implementation.

Fresh working-tree validation: 91 Codex tests passed in 17.356s, shell launcher
regression passed. README recruiter-sync: pass_no_change. Required scoped
refresh-config: REFRESH COMPLETE, exit 0; log
/tmp/refresh-config-20261008-123924-1658082.log. Exact picker modules applied,
live Codex/Git snapshots retained and shortcuts reloaded. Index scope audited
against explicit manifest, excluding unrelated features/configuration.
Commit subject: feat(codex): browse recent sessions with compact previews.
Push destination: origin/main. Local rollback is a normal future revert; no
history rewrite. No external model smoke request repeated during delivery.

Exact staged-code snapshot verification: 91 tests passed in 18.498s, exit 0.
All nine related postmortem learning checks passed. Shared-file staged hunks
were independently checked to exclude Second Brain, directory-size, backup and
unrelated alias changes. Final staged whitespace check passed.
