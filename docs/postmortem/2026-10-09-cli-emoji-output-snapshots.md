# CLI emoji rollout old-output snapshot failures

Some existing regression fixtures still expect undecorated prose. Inspect each failure to distinguish intentional output changes from behavioral regressions before updating expectations.

## Symptom, impact and evidence

- Python agent: `tests/test_largest_day_file_size.py` had four strict expected-output failures after adding the approved calendar prefix. Logic regressions have not been established; review is ongoing.
- Shell agent: `tests/test_rsync_media_date.sh` exited 1 without output; captured log `/tmp/emoji-test_rsync_media_date.sh.log` is empty. Agent inspection confirmed the fixture stops at `test -x`: the source script has tracked mode 100644 and working mode 664. This predates the emoji changes; no script output is reached. Preserve that unrelated mode.
- New defining emoji/default/plain tests pass according to agent reports. Root independently verifies final suites before completion.

## Lookup and applicability

Canonical postmortem-memory safe editing and artifact verification guidance applies: examine complete assertions, preserve their semantic checks, and change expected text only for deliberately approved decoration. Never weaken assertions to hide unrelated failures.

## Current status and next steps

Unresolved at recording. Agents inspect failed assertions before retrying. Record exact causes, reviewed expectation changes and fresh suite results here; retain all machine/protocol assertions unchanged.

## Learning decision

No verified new learning yet; intentional new-output contracts require expectation alignment, while unexpected regressions remain open until checks pass.

## Additional baseline contract finding

Root ran `python3 -B tests/test_ai_workflow_contract.py`: 11 passed and one failed because `dot_agents/skills/commit-dirty/SKILL.md` lacks the exact full multi-commit push-cadence sentence required by an existing test. This task does not modify that skill or the cadence assertion. Verify the same absence in HEAD before labeling it baseline; do not widen the output task to rewrite commit policy.

## Additional inspection and regression outcomes

- `tests/test_metaprompt_integration.py`: four digest failures in untouched legacy `metaprompt-alxve` reference files; eight test methods ran. Imported active-package integrity and the modified local update helper behavior passed. Confirm legacy hashes match HEAD before classifying these baseline failures.
- Root attempted `tests/test_leetcode_init.py`, which does not exist. No tests ran; locate the actual fixture with `rg --files` before the next run. This is an invocation mistake, not a product failure.
- Independent reviewer used `rg` against nonexistent `scripts/lib`, returning 2. No writes occurred; use the observed script tree before adaptive follow-up. Review is ongoing.

- Installed fish invocation with `fish --no-config -c cli-message...` exited 127 because the isolated shell did not discover the user helper. Check the installed function file and function search path before remediation; explicitly source the installed helper for no-config verification. This does not yet establish a missing install or regular-shell failure.

## Reviewed resolutions and remaining baseline checks

Largest-day exact prose expectations were aligned with the approved calendar cue; six tests pass. Root independently verified the commit-dirty sentence is absent in HEAD and all four legacy metaprompt reference bytes exactly match HEAD. The missing LeetCode path was corrected to the skill-local fixture; all 11 tests pass. Installed `cli-message.fish` exists; `fish --no-config` has only `/usr/share/fish/functions` on its search path. Explicitly sourcing the installed helper passes default and plain checks. No regular-shell or install defect was shown.

Root `tests/test_postmortem_memory.py` ran 26 tests: 25 pass; whole-corpus coverage failed. One changed alias was this living report, whose current hash must be registered immediately. The check also sees historical missing/unregistered aliases outside this task; targeted checks isolate current-session evidence. Keep unrelated historical entries unchanged and report broad coverage limits rather than treating them as emoji failures.

No new reusable learning beyond existing fixture/contract evidence rules: approved presentation expectations changed; baseline policy/digests/mode and corpus coverage remain outside task scope. Invocation mistakes are corrected and direct installed output is verified.

- Root attempted to syntax-check the raw `cd.fish.tmpl` with fish, which rejected its chezmoi conditional. This was a verifier invocation error; render templates with chezmoi before parsing, and parse ordinary `.fish` files separately. Existing runtime fixtures already render the cd template. No source change is needed.

## Full-suite snapshot findings

The sync-isolated full suite ran 1088 tests in 465.009 seconds: 15 failure reports and one optional backend skip. Eight failures are exact old human-output assertions in config-snapshot (one), Second Brain timer (four) and Superpowers release timer (three); code business assertions otherwise pass. Align these expected prose strings with the approved error/timer prefixes and rerun those entire suites without weakening security or activation assertions. Seven other failure reports are the known policy/digests/corpus coverage plus an untouched sanitized-vault expected-file inventory mismatch; verify the additional daily-note file exists in HEAD before labeling it baseline. The complete log is `/tmp/cli-emoji-isolated-python.log`.

- Standalone `python3 tests/test_second_brain_config_snapshot.py` could not resolve `scripts.second_brain`; the repository suite had imported it successfully through unittest discovery. Use `python3 -B -m unittest discover -s tests -p test_second_brain_config_snapshot.py` so the repo root stays on the module path; no package source change is needed.

## Final output-related verification

Aligned only the eight exact human-prose expectations. Full targeted reruns passed: config snapshot 22 (`python3 -B -m unittest discover -s tests -p test_second_brain_config_snapshot.py`), Second Brain timer 34 (`python3 -B tests/test_second_brain_timer.py`) and Superpowers release timer 20 (`python3 -B tests/test_superpowers_release_timer.py`). Security/no-secret and unit activation assertions remain intact. The additional vault note is byte-identical to HEAD, confirming its expected-tree failure is baseline. Full-suite failure reports remaining outside this task are push policy (one), untouched legacy reference digests (four), historical memory corpus coverage (one), and unchanged vault inventory (one). The separate shell rsync executable-mode precondition also predates the rollout.

## Commit-snapshot verifier limitation

The prospective commit export passed all 27 defining tests, 22 config-snapshot and 20 Superpowers timer checks, but the Second Brain timer suite had 26 state-path failures. Inspection of second_brain/paths.py confirmed repository discovery requires a .git marker; git archive exports deliberately lack that marker. This is a verification-fixture limitation, not evidence of a timer regression. Add only an empty repository marker to the disposable export, then rerun the unchanged 34-test suite; never weaken production safety checks. A read-only rg lookup also referenced removed second_brain/state.py; use observed module paths for further inspection. Existing artifact-verification guidance applies; no new reusable finding.
