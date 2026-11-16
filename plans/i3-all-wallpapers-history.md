# All i3 wallpapers and recent history

Make every wallpaper shortcut choose from the entire image collection and keep an automatic history that lists the newest wallpaper at the bottom.

## Outcome and scope

i3 wallpaper bindings use ~/Pictures/Backgrounds recursively, independent of editing/brightness categories. Preserve special black-background shortcut and startup behavior, palette policy, fonts, source images, and all prior dirty work. Existing shuffler gains an image-only mode so other external uses retain generic behavior. History records successful applications through apply-pywal-theme, skips consecutive duplicate restores and uses persistent private state. No historical reconstruction, image moving, commit or push.

## Decisions and protected state

Initial status saved /tmp/i3-all-wallpapers-evidence/initial-status.txt. Pre-existing README/smoke/postmortem-ledger/lessons edits remain protected. Installed config is newer by mtime: review its diff before activation and patch only exact binding lines if full refresh remains blocked. Use six existing brightness/editing keybindings for full collection; black shortcut remains separate. Image candidates exclude .git, shuffle.txt, scripts, metadata and incomplete downloads; numbered image suffixes such as .jpg.1 remain eligible. Cached invalid/deleted selections must be removed. Names with spaces must reach apply as one argument.

## Ordered work

- [x] Inspect bindings/helper/callers and capture state.
- [x] Observe defining RED for image-only selection, stale cache and quoted all-root bindings.
- [x] Implement smallest shuffler/i3 change and history CLI/wrapper with GREEN tests.
- [x] Update README and grouped smoke checks.
- [x] Attempt refresh-config, safely install scoped changes if blocked, validate/reload i3 once and verify actual bindings/history.
- [x] Review final diffs/evidence and record limitations.

## Risks and rollback

No prior usage exists to reconstruct; history starts with current wallpaper then successful future helper applications. Direct feh/upstream wal bypass history. Existing MIME duplicate targets may block refresh; don't delete unrelated files. Avoid moving focus or repeatedly changing live wallpaper. Preserve backups of affected installed scripts/config; one reload activates bindings. Tracker write failure must not misreport successful wallpaper application as failed. New files join after shuffle cache regenerates.

## Verification

Tests: python3 -m unittest discover -s tests -p test_shuffler_images.py; python3 -m unittest discover -s tests -p test_wallpaper_history.py; bash tests/test_apply_pywal_theme.sh; focused existing pywal regressions. Isolated fixture exercises root/nested/space/numbered-suffix images, metadata, .git, stale/deleted entries, no-repeat cycle and empty root. Real candidate list compared against fresh verifier discovery. Actual runtime: deployed i3 -C validation, one i3-msg reload, GET_BINDING_STATE/config inspect without changing wallpaper; installed shuffler path returns an eligible image; wallpaper-history --record followed by wallpaper-history shows current wallpaper newest at bottom. Rollback files under /tmp/i3-all-wallpapers-evidence.

## Progress and review notes

Search agent confirmed active tracked shuffler callers are wallpaper-only. Native pywal directory selection is nonrecursive and supports fewer types, so cannot meet all-images scope. Retain generic helper semantics through -i rather than changing external callers. An exploratory command ended2 because an optional .chezmoi.toml.tmpl read targeted an absent file; it changed nothing and is recorded separately with activation incidents if any.

Selection RED: four tests, three expected failures (unsupported-i, empty-image output, initial binding selector also included unrelated restore binding). Selector narrowed to shuffler-based bindings; six branches define random selection. GREEN: four tests pass; existing apply wrapper smoke exits0. New recursive filter compared against fresh existing verifier discovery: exact667candidates, zero missing/extra. Shell syntax and diff checks pass. Source/live i3 differ beyond machine paths (local shortcut additions and private settings); preserve all such local work by patching only four matching live random-selection lines. Do not import machine-local/private values into tracked source.

History RED→GREEN observed by worker/tests agent before implementation; final9history tests pass. Full final focused checks:4shuffler+9history+11pywal+19verifier=43tests, allpass; existing Bash apply integration exits0. Tests isolated XDG_STATE_HOME and unset inherited PYWAL_CACHE_DIR. Logs final-*.log under evidence directory. History JSONL uses restrictive permissions and flock; validates existing records, escapes control characters and tolerates valid newline-less final records. Full refresh exit1 confirms pre-existing duplicate MIME targets (/tmp/refresh-config.w5sHsxNl.log); scoped deployment will preserve local i3-only changes/private values.

Runtime verified: candidate i3 config validation0; installed shuffler/apply/history match source; one current-theme restore0 seeds history and reloads i3 once. Raw `i3-msg -r -t get_config` verifies all4active desktop random bindings use quoted full-root -i selection. Default/plain history command exits0; repeat --record leaves file unchanged. Actual installed shuffler returns eligible beach.png; selection does not record usage. Default GET_CONFIG verification was initially JSON-parsed incorrectly; installed manpage and raw IPC correction verified loaded bindings without another reload. Source images unchanged; only ordinary root shuffle cache advanced.

Isolation follow-up:3testfixture history rows exposed inherited XDG_STATE_HOME in existing pywal integration fixtures. Confirmed RED with poisoned external state despite11passing tests; added fixture override. Final11tests pass and poisoned parent directory remains empty (including Neovim state). Removed only3exact test-generated rows under flock, backing up original history; retained real current entry. No historical use invented. Final shuffler4/history9/Bash checks pass again; earlier unchanged verifier19passed this turn.

Rollback: /tmp/i3-all-wallpapers-evidence/rollback contains previous installed i3 config and helper scripts, a history cleanup backup and executable restore.sh (syntax checked, not executed). New history command/data stay available on rollback. Full refresh remains blocked by unrelated duplicate MIME targets; scoped activation is verified. No physical keypress or different live wallpaper was needed; isolated shell-command tests cover all6source branch bindings with spaces. History tracks completed theme processing, not asynchronous feh success; direct feh/wal bypass it and decoded XCF may appear as cache PNG. No commit/push performed. Independent source review found no material defect.

Atomic plan: RED selection/history → minimal helper/binding/record hook → GREEN+isolation checks → docs → backup/scoped deploy → live IPC/history checks. Automated commands: `python3 -m unittest discover -s tests -p test_shuffler_images.py`; equivalent for test_wallpaper_history.py, test_pywal_readable.py, test_verify_wallpaper_merge.py; `bash tests/test_apply_pywal_theme.sh`; `bash -n scripts/executable_shuffler scripts/executable_apply-pywal-theme`; `git diff --check`. Manual Action/Expected checks are in docs/smoke-tests.md.

Paste-ready Cursor prompt: Review plans/i3-all-wallpapers-history.md and the scoped i3/shuffler/history changes, preserve all unrelated dirty work, keep whole-collection image selection and newest-at-bottom history, and rerun recorded tests with poisoned XDG state before any follow-up. No commit/push authorized by this prompt. Suggested commit: feat(wallpaper): use all backgrounds and track recent applications.

Follow-up: the duplicate MIME full-refresh blocker was subsequently resolved and actual refresh completed0. See [identical MIME recovery](refresh-config-identical-duplicates.md) for implementation, backup and verification. Earlier scoped-activation evidence remains accurate for its original run.
