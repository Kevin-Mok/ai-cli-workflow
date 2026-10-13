# Render notification Markdown bold

Convert terminal notification strong-emphasis markers into Dunst bold text, then verify the real Kitty dispatch and desktop samples.

## Purpose, context and scope
Kitty 0.49.2 sends OSC notifications as plain text and FreeDesktopIntegration.notify neutralizes angle brackets/ampersands. Dunst supports Pango body markup. Extend the existing dot_config/kitty/notifications.py callback to format terminal popup title/body while preserving permissions, focus/click behavior, native identifiers, updates, urgency and audio provenance tagging. Bold syntax **text** is the defining request; preserve escaped markers and code spans/fences, escape literal HTML. No dependency installation or global Kitty patch. Desktop apps outside Kitty retain their native formatting.

## Decisions and assumptions
Use a str subclass for generated body markup that only bypasses Kitty's two known markup-neutralizing replace calls. This keeps native dispatch and actions; only escaped, generated markup reaches Dunst. Guard on desktop integration supports_body_markup; unsupported APIs/platforms retain plain original text. Transform all terminal bold-text samples through the existing callback, retaining Codex-specific app tagging. Do not claim full Markdown support; only strong emphasis requested.

## Checklist
- [x] Capture Git status and inspect source, tests, installed API and official source.
- [x] Define RED for bold rendering, literal/code escaping, safe backend dispatch and metadata preservation.
- [x] Implement minimal safe formatter and callback wiring.
- [x] Add reusable desktop sample helper and usage/smoke documentation.
- [x] Run tests and real installed backend dispatch checks.
- [x] Refresh configuration, reload affected Kitty processes or verify fresh process, send desktop samples.
- [x] Reconcile evidence and review notes.

## Protected work, risks and rollback
Many unrelated instruction, tmux, pstack and memory/doc files were already dirty. Preserve their hunks. Notification callback itself was clean at entry. The body str adapter relies on verified Kitty 0.49.2 replace behavior; regression exercises the actual installed backend. Future escaping changes should fail visibly in tests and leave original popups deliverable. Restore callback and remove sample helper, refresh and reopen/reload Kitty to roll back.

## Verification
Automated: python3 -B tests/test_notification_markdown.py must observe RED then GREEN; existing tests/test_codex_notification_sound.py protects native metadata/tagging. Native backend verification runs the installed sample CLI under a scoped DBus capture and confirms generated bold tags reach Dunst intact; literal/plain samples and unit checks protect original escaping. Live: installed sample helper sends bold, literal/code and plain cases to Dunst; Kitty OSC probe must show transformed body in Dunst history and preserve native actions. No sudo. Add exact commands/evidence when implemented.

## Progress and review
Inspection failures recorded in docs/postmortem/2026-10-13-notification-markdown-inspection.md; installed frozen module found rather than guessing distribution paths. Plan is decision-complete for bold-only scope; inspect new behavior before claiming live activation. Commit-session is now authorized for this follow-up.

## Activation refinement
The callback is loaded once at Kitty startup, so config reload alone cannot update existing processes. Add a small no-UI custom kitten that reloads only notification_manager.filter_script from the installed callback without resetting notification state, then optionally sends a native bold/literal/plain test through that same manager. A wrapper CLI selects the current reachable Kitty socket and can activate all reachable instances. This preserves existing terminals and native identifiers/actions while making the result active now.

## Verification evidence and final handoff
Seven focused Markdown checks pass after defining RED; activation fixture also observed RED with __file__ deliberately absent, then GREEN with Kitty config_dir. Existing tests/test_codex_notification_sound.py passes, exit 0, preserving tagging/actions/audio policy. Refresh completed and installed callback/custom kitten/helper are applied. `notification-markdown-test --activate-all --details` succeeded with 12 instances. A scoped dbus-monitor capture of native sample delivery confirms the exact body `Normal text; <b>this should be bold</b>; normal again.` reaches Dunst, with no Kitty neutralization. Literal/code and plain samples each send successfully. No terminal restarted and no manager state reset.
Documentation: README, docs/smoke-tests.md, notification sound guide (if its text contract needs correction), and this plan. Final visual bold/font-weight acceptance and real Codex focus-suppression check remain manual; native payload and metadata parity verified. Commit-session is now authorized for this follow-up.

## Atomic change, rollback and Cursor prompt
Keep callback, no-UI activation kitten, helper, focused tests, matching docs/plan and inspection incident/learning together. Suggested subject: `feat(notifications): render Markdown bold in Kitty popups`.
Cursor prompt: Review plans/notification-markdown.md and changed notification files while preserving unrelated dirty work. Run tests/test_notification_markdown.py and tests/test_codex_notification_sound.py, then native bold/literal/plain CLI samples. Confirm generated bold tags reach Dunst through Kitty and plain input/code remain literal. Keep native focus, identifiers, updates and audio provenance. Verify unsupported markup backends retain originals. Do not commit unless requested.
Exact automated plan: python3 -B tests/test_notification_markdown.py; python3 -B tests/test_codex_notification_sound.py; targeted postmortem-memory check for the inspection incident. Exact manual plan: ~/scripts/notification-markdown-test --activate-all, then --case literal --plain and --case plain --plain. No sudo; each popup expires after 15 seconds. Roll back tracked callback to previous version, refresh, then use the activation kitten once to reload that version in existing processes before removing the activation files.

Final review: README gate and scoped diff check pass; targeted incident-learning check returns no errors. Sound guide now describes bold formatting and existing-instance activation accurately. Deferred manual checks are subjective font-weight acceptance and a real Codex focus-suppression/click check; actual native payload, existing metadata regression, safe instance activation and desktop sample delivery are verified.

## Commit milestone: feat(notifications): render Markdown bold in popups
Scope uses directly observed writes in session 01a13605-2f04-7db2-aaa9-1e3a40a6c13d because the helper reports unsafe (nested orchestration writes not detected). Include 10 paths: callback, activation kitten, sample CLI, tests, sound guide, this plan, inspection incident, and only our additions in README, smoke tests and memory ledger. Preserve all unrelated pre-existing/concurrent work.
Completed and verified: eight defining tests, sixty existing sound regressions, incident-learning check, README gate, refresh, activation in 12 live instances and native DBus bold delivery. No implementation blockers. Next: isolated staged checks, create one focused commit and push main to origin/main. Commit hash and push result will be reported in Codex output. Rollback remains documented above.

Final commit verification refinement: isolated old sound tests require ignored Codex config; supply only the public notify stanza in the temporary snapshot, never stage the local file. Eight Markdown checks now pass, including SupportsIndex string-replacement regression. Basedpyright passes with only frozen-Kitty import diagnostics locally excluded; native API activation/DBus checks validate that boundary. Reverify staged tests, incident learning and README before commit.

Final commit preflight: exact staged snapshot passes 68 tests using the explicitly documented public temporary Codex fixture, type checker and README gate. Fresh native bold payload verified after final fixes; 11 reachable Kitty instances acknowledged activation. Incident record/hash and scoped diff check are current. No blockers; ready to commit and push only the reviewed 10 paths.
