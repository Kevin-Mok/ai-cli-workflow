# Wallpaper verifier isolation and test environment

Keep exhaustive wallpaper validation isolated from user configuration and ensure its test fixtures exercise the intended production paths.

## Symptom, impact and cause

First GREEN attempt had two CLI fixture failures because changing HOME hid the installed pywal package; test PYTHONPATH omitted its actual installation parent. Independent review then found real isolation risk: pywal3.3.0 honors PYWAL_CACHE_DIR ahead of HOME/XDG variables. A deliberately poisoned fake-live-cache RED caused0/2checks to find their private outputs. No real cache was used in the reproducer.

## Resolution

Tests pass the existing installed package path; production children explicitly override HOME, XDG paths and PYWAL_CACHE_DIR. Parent cache fingerprints and report guards use the effective parent override. Reports refuse existing files, protected image/cache paths and symlinks, using exclusive creation. Unknown/traversal/nonregular source entries fail closed. Test expectations were reconciled with intentional new background/vivid policy instead of changing contrast goals.

Temporary graphical preview fixtures initially omitted wal theme name and an airline helper, then hit a stale swap prompt; these were fixture errors. After adding production dependencies and disabling temporary swaps, headless preview exited0 and actual Kitty/Nvim screenshot /tmp/pywal-vivid-editor.png showed distinct vivid syntax on dark background. Earlier default/error screenshots were not accepted as evidence. One documentation patch missed stale context; narrow reapplication preserved unrelated hunks.

## Verification and status

Resolved:19 verifier tests (including poisoned cache, real multi-image CLI, report overwrite guards, FIFO and directory errors),11 palette tests,1actual XCF integration and adjacent wrapper/i3/Vim/runtime checks pass. Fresh four-worker actual run checked667/667,0failures/0collisions, source and active cache fingerprints unchanged; report /tmp/wallpaper-all-final-parallel-2026-11-16.json. Required refresh later stopped before writes on pre-existing duplicate MIME chezmoi targets; reviewed helper/verifier and Vim function were activated narrowly with backup /tmp/pywal-vivid-live-backup-rnxe97oe. Theme restore exited0.

## Learning

Lookup isolated HOME PYTHONPATH returned unrelated temp-root/runtime/integration findings; no matching pywal remedy. Existing environment/installed-artifact validation guidance applies. Record task-specific explicit-cache-override lesson in tasks/lessons.md; register this final reviewed hash with no new generalized finding. No installed skill copy edited.

## Commit evidence schema follow-up

During commit-session, the read-only staged-content validator correctly matched all15staged paths but then assumed fresh test metadata used exit_code. The worker's result JSON used a different exit-status key, producing KeyError before the metadata assertion. No staged or working code was altered, and the actual tests remain separately observed passing. Inspect the producer's exact keys before retrying; repair only this evidence-reader assumption and refresh this reviewed report hash in the same commit.

Resolved: inspected keys name/command/log/exit_status; all eight recorded commands have exit_status0. Reader now uses exit_status directly. Lookup KeyError result schema exit status did not establish a task-specific remedy; actual producer keys are the diagnostic evidence. The previous exact-candidate privacy check also passed, and is repeated after refreshing this report/ledger.
