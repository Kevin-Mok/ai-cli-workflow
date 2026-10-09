# Command-formatting update: sandbox startup failure

The default runner could not start the requested documentation inspection. Approved scoped execution unblocks this task; the host sandbox remains unresolved.

- Symptom and evidence: `pwd`, `git status --short`, and the required skill read exited 1 before their command bodies ran, with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`.
- Impact: context reads were delayed; failed launches changed no repository files. Initial status was captured successfully before this first write, and protected target snapshots are in `/tmp/codex-command-formatting-before`.
- Lookup: searched `bwrap loopback Failed RTM_NEWADDR`; read `ext-sandbox-loopback` and `local-sandbox-loopback-approved-route` in the tracked execution-environments reference. Both are verified workarounds, applicable to the identical pre-execution error across harmless independent commands.
- Cause: Bubblewrap loopback initialization is denied. The underlying host policy was not investigated.
- Resolution and verification: approved `require_escalated` reads and `git status --short` execute with exit 0. This verifies the alternate execution route only.
- Status and next steps: continue scoped documentation work through the approved route. Do not change host security or claim normal sandbox recovery.
- Learning: no new reusable learning; the two existing findings already cover the symptom, workaround, diagnostic distinction, and unresolved default route. Register this reviewed report with an empty findings list.

## Temporary UI probe initialization typo

- Symptom: `/tmp/formatting_runtime_probe.py end` exited 1 with `AttributeError: 'tuple' object has no attribute 'rstrip'` before any UI action ran.
- Impact: one temporary probe invocation was delayed; no product code, rendering setting, terminal state or repository content was changed by that invocation.
- Lookup: searched `temporary Python diagnostic tuple AttributeError rstrip`; returned language-validator, exec-scope, AST-coordinate and path-discovery findings do not apply to this direct tuple-method typo. No relevant prior finding was established.
- Cause: `.rstrip()` was attached to the whole mixed-case tuple instead of its command string.
- Resolution: move the method call inside the tuple. Verify module initialization and the requested bounded UI action before proceeding.
- Learning: no new reusable finding; a local authoring typo in a disposable probe supplies no product or renderer lesson. Keep its exact cause and verification in this task incident.

- Corrected tuple probe verification: `/tmp/formatting_runtime_probe.py end` initialized, ran the scoped scroll action and exited 0 with no output.

## Disposable clipboard probe: invalid initial measurement

- Symptom: the first five-case attempt returned the unchanged prior clipboard, and Kitty reported zero selected bytes. No captured command was executed.
- Evidence and cause: the grid probe emits CRLF for hard newlines and CR for soft wrapping. Replacing every CR with LF double-counted hard rows, so mouse coordinates were wrong. A window-directed synthetic copy event also did not establish a clipboard update.
- Lookup: searched `Kitty selection clipboard XSendEvent coordinates`; `local-codex-rendered-command-copy` applies to the installed Codex version and the need for real selection evidence, but contains no verified automation remedy. Historical release-key and Python exec-scope findings do not apply.
- Status and next steps: this measurement is invalid and supplies no renderer copying evidence. Normalize CRLF before mapping soft wraps, target focused XTest keyboard input and verify nonempty actual selection plus exact clipboard bytes before pasting.
- Learning: no new general product finding; temporary measurement defects are recorded here and must not be mistaken for Codex copy failures. The existing rendered-copy finding already requires actual clipboard evidence.

## Optional installed Kitty source inspection

- Symptom: an assumed `lib/kitty/kitty/window.py` read exited 2 because that optional source path is absent. This was a diagnostic read, not a terminal failure.
- Lookup and applicability: searched `optional installed source path missing discovery`; `local-discover-paths-before-reads` and optional-path discovery guidance apply to assumed installation layouts. The installed executable was present, but the Python source layout had not been discovered.
- Impact and status: no files or terminal state changed. Skip unsupported source assumptions; use advertised terminal control APIs and explicitly report unverified selection rather than claiming a renderer failure.
- Learning: no new reusable finding; existing discovery guidance covers this inspection mistake.

## Final verification status

Approved scoped execution completed the instruction/documentation update. `fish -c 'refresh-config'` exited 0 with REFRESH COMPLETE; fresh checks confirm installed/source policy equality, live/source TOML equality and an unchanged TUI table. No tracked file changed during that refresh interval.

The temporary probe typo was corrected and verified by successful initialization. Row mapping and native-copy control were corrected enough to capture actual terminal selections, but outer selection boundaries remained unreliable. Their exact-match failures are invalid command-copy verdicts; no invalid selection was executed. The current [rendering comparison](2026-10-09-codex-mixed-content-rendering.md) records actual visible colors and hard command wrapping separately, with exact paste acceptance still pending. Default sandbox startup and optional Kitty source availability remain outside this task; no host or software patch was made. No new reusable helper-failure finding is warranted.
