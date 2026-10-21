# Fix Fish login startup

Prevent missing-argument errors when login shells have no virtual-terminal
number. Reproduce the guard failure, quote its scalar operand, and verify the
deployed guard without starting a real X session.

## Scope and decisions

Change only `dot_config/fish/config.fish.tmpl` guard behavior, a focused runtime
regression in `tests/test_fish_startup.py`, the smoke checklist, incident and
tracked incident knowledge. No changes to X startup eligibility or other shell
settings. No commit or push requested.

The initial status contains unrelated dirty README, media-screensaver, prompts,
plans, lessons and incident-knowledge files. Preserve those changes and append
only this task's entries to shared documents. The installed Fish config is older
than the source but differs in private/local values: never replace it wholesale
with the sanitized public template.

## Atomic checklist

- [x] Capture initial status; read source, applicable guidance and prior findings.
- [x] Add behavior regression: missing/empty VT, console 1, other console,
  active display and non-login shell. Run it and observe the expected RED.
- [x] Quote `$XDG_VTNR` in the existing guard; run focused/regression checks.
- [x] Apply only the reviewed guard to the installed configuration. Full refresh
  withheld: sanitized target would replace unrelated local settings.
- [x] Update smoke checks, postmortem and its reviewed knowledge/hash; verify.

## Verification

Use real Fish with the source login block and a disposable `startx` executable
that prints its arguments. Assert no diagnostics and exact startup eligibility.
Run `python3 -B tests/test_fish_startup.py`, the existing Fish alias/GPG checks,
and `fish --no-config --no-execute` on the extracted login block. Then start
installed login shells with DISPLAY set and VT unset/empty, plus both variables
unset, and a non-login shell. A real graphical server must never run in checks.
Targeted incident-memory check must accept the final report hash.

## Risks and rollback

The only production edit adds quotes to a scalar comparison; rollback removes
those quotes in source and installed guard. Global refresh could replace private
settings with public placeholders, so inspect and bound deployment first.
Physical console X startup remains untested; a harmless executable verifies its
exact argv. Source changes and evidence remain together for any later commit.

## Progress and review

RED: `python3 -B tests/test_fish_startup.py` exited 1 with two scenario failures:
login shells with VT unset, both DISPLAY set and unset, emitted exactly
`test: Missing argument at index 6`. Six other scenarios passed. The test catches
removal of the scalar quotes and changes to X startup eligibility. Source now
quotes the comparison operand.

GREEN: focused regression passes all eight cases, exit 0; refresh-helper
regressions pass, exit 0. Alias regression cannot collect because its unchanged
method name contains a hyphen; GPG regression cannot find its expected config.
These are reported baseline blockers, not passing coverage. A sandboxed real
startup reached its marker but failed the no-stderr assertion due to normal
startup writes outside the workspace. Approved startup probes then passed all
three installed login cases with exit 0 and zero stderr bytes. Exact one-line
replacement preserved every other installed-config byte, with a private backup.

README still accurately describes Fish and refresh; no public command changed.
Smoke checks and the linked incident document the unset-VT path and deployment
limit. Physical-console X startup and unrelated repository suites were not run.

Final review: fresh `python3 -B tests/test_fish_startup.py` passed (exit 0),
extracted Fish guard syntax passed (exit 0), and scoped whitespace validation
passed (exit 0). `postmortem_memory.py check --postmortem` on the incident passed
(exit 0, empty errors/changed/new/unregistered lists). Reviewed SHA-256:
`2eb78312c1c65c3237adbb88ecd6912ad797e62c470fcd8fd21d6567e104b207`;
finding `local-fish-optional-scalar-test`, verified_fix/runtime. Tracked topic
guidance and reciprocal ledger links are current. No outstanding fix work;
baseline regression limitations and broad-refresh safety exception are recorded.

Safe installed manual probes (any working directory, no sudo):

- `env -u XDG_VTNR DISPLAY=:1 fish --login -c 'printf "✅ Desktop login reached\n"'`
- `env -u DISPLAY -u XDG_VTNR fish --login -c 'printf "✅ Headless login reached\n"'`
- `env DISPLAY=:1 XDG_VTNR=1 fish --login -c 'printf "✅ Existing display respected\n"'`

All three equivalent probes were executed through a subprocess wrapper and
returned exit 0, their success marker and zero stderr bytes. Terminal palette
sequences may precede the marker on stdout. No sudo or real X launch is needed.

Suggested commit: `fix(fish): quote optional VT number during login`.

Cursor continuation prompt: Review the source guard, focused Fish startup test,
smoke entries, incident and its knowledge record against this plan. Preserve
unrelated dirty work and private installed settings. Run the focused regression
and the three safe installed startup probes; do not launch X or force a global
refresh. No implementation work remains when the documented checks pass.

## Session delivery milestone

Commit subject: `fix(fish): handle unset virtual terminal during login`.
The latest commit-session request authorizes committing and pushing this work.
Its scope helper returned unsafe because no successful writes were parsed from
the session log; the captured pre-write status and directly observed edits
establish the fallback scope. Only this session's hunks in shared docs/knowledge
are eligible. Unrelated changes remain protected. Focused startup/refresh checks
and README gate passed; no current delivery blocker is known before privacy
inspection. Push the single verified commit to origin/main.

Scope correction: actual chezmoi rules preserve local Fish configuration;
the raw-template warning above was an initial assumption. The follow-up plan
records the successful full refresh after exact launcher mode reconciliation.
