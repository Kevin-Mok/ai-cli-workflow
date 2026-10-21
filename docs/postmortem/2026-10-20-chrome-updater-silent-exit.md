# Chrome updater silent exit

The updater first returned silently, then incorrectly rejected a successful Chrome upgrade. This report tracks both repairs and their checks, including the user's confirmed package installation.

## Symptom and impact

- User ran `sudo /home/example/linux-config/scripts/executable_update-chrome.sh` twice and saw no script output.
- The earlier small mocked-output tests passed and did not cover producer failure or large policy output.
- Local unprivileged `--check` succeeds: installed 146.0.7680.177-1, cached candidate 155.0.8059.84-1. This does not reproduce the user's sudo environment.

## Investigation and lookup

- Query: `pipefail SIGPIPE awk early exit`.
- Relevant reviewed finding: `ext-pipefail-full-output-drain` in `references/editing-shell-transport.md`. Applicable hypothesis: `awk` exits after Candidate while `apt-cache` still writes, triggering SIGPIPE under `set -euo pipefail` before any status text.
- Only one caller of `get_candidate_version` exists, inside the updater. No tracked BASH_ENV or sudo environment overrides found.

## Resolution and verification

- Confirmed code defect: a fake apt-cache emitting 10,000 policy rows after Candidate reproduced a silent exit (status 1 from the Bash producer's broken pipe; status 141 is not guaranteed). The original small fixture missed it.
- Changed the parser to consume all output, select only the first Candidate, and use the C locale. That regression passed; the separate failed-query test then failed because no actionable diagnostic appeared.
- Added an initial activity message and explicit handling of a failed candidate query. `bash tests/test_update_chrome_script.sh` now exits 0, covering help, check-only, upgrade, already-current, large policy output and query failure. Bash syntax checks also exit 0.
- Live `--check` and `--help` exit 0. The check visibly reports activity and installed 146.0.7680.177-1 / cached candidate 155.0.8059.84-1.
- Status: verified fix at code scope for the reproduced silent pipeline failure. The exact user's sudo environment, real package installation, and Chrome relaunch remain operator verification; do not claim those are fixed.

## Diagnostic limitations

A diagnostic read also attempted a nonexistent `scripts/executable_refresh-config`; the actual helper is a Fish function. Inspecting that function with ordinary Fish startup emitted read-only-filesystem errors for `/run/user/1000/fnm_multishells`, universal variables, and `/home/example/aliases/.key_aliases`. These are sandbox startup effects, not Chrome evidence. Do not repeat full Fish startup for read-only function inspection; use source inspection or `fish --no-config`. No configuration files were changed and no refresh is needed for this directly invoked script repair.

## Follow-up and learning

Rerun the original sudo command, confirm visible progress or its actionable error, then relaunch Chrome. Added regressions and updated README/shared smoke checks. Link this report to existing `ext-pipefail-full-output-drain` guidance; no separate finding is needed for the already documented pipeline pattern or incidental diagnostic-path/startup constraints.

## Follow-up: stale candidate verification

The user's sudo run now prints activity and successfully installs 156.0.8078.47-1. Verification incorrectly compares that with 155.0.8059.84-1 saved before apt update, then fails. GitHub CLI repository signature warnings did not block Chrome's installation. Cause confirmed by output and source: the candidate is read only before metadata refresh, and equality rejects newer versions. User requests a fresh latest candidate and acceptance of installed versions greater than the candidate. Lookups `candidate stale apt metadata version verification` and `package candidate metadata` found no directly applicable reviewed stale-candidate remedy; the prior full-output-drain finding remains applicable to the earlier defect.

- RED: metadata-advancement fixture fails at verification. After refreshing candidate reads, the newer-installed fixture fails because installation is attempted instead of skipped.
- Resolution: normal runs refresh APT metadata before reading/displaying the candidate and deciding whether to install, including when cached versions initially match. Verification re-reads the candidate after installation. Both comparisons use `dpkg --compare-versions ... ge`; an incomplete upgrade still fails. Candidate query validation is centralized in the existing helper. `--check` stays read-only and explicitly uses cached metadata.
- GREEN: all eleven scenarios in `bash tests/test_update_chrome_script.sh` pass (exit 0); Bash syntax checks for script and test pass (exit 0). New cases cover refreshed candidate advancement, initially equal cached versions, initially newer installed versions, newer post-install versions and genuinely incomplete upgrades.
- Live evidence: `./scripts/executable_update-chrome.sh --check` exits 0 with installed and candidate both 156.0.8078.47-1; `google-chrome-stable --version` exits 0 with Google Chrome 156.0.8078.47. No additional privileged update was run by the agent. Browser relaunch/loaded-browser version remains operator verification.
- Reviewed learning: retain `ext-pipefail-full-output-drain`, add `local-package-candidate-refresh` for metadata freshness and Debian comparison semantics. Targeted memory check verifies this report's new hash and reciprocal finding links.

## Delivery permission boundary

The initial git apply --cached attempt failed with exit128 because the sandbox exposes .git read-only and could not create index.lock. No index changes occurred. Retry only the reviewed session patch with the normal repository-write escalation. This adds no new engineering finding: the failure is the configured permission boundary, not an updater defect.

The initial delivery privacy check intentionally blocked local home identifiers and IP-shaped version fixtures. Neutral public paths and version fixtures with non-IP build numbers replace them; no gate exemptions or hook bypasses are used. Source aliases use the neutral public root, with local path substitution only in an ephemeral verification copy.
