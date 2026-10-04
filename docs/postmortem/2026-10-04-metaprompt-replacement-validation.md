# Metaprompt replacement validation

## Sandbox startup during independent inspection

- Date: 2026-10-04.
- Symptom: the read-only review agent's first shell command failed before startup
  with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`.
- Impact: no files changed and no benchmark/model inference was invoked by that
  command. Source inspection had not run.
- Root cause: the environment's default shell sandbox cannot initialize its
  loopback interface, consistent with the earlier documented environment issue.
- Resolution/status: use the available automatically reviewed elevated shell
  for the same bounded read-only inspection. Parent shell reads already work
  through that route. No user approval was rejected.
- Verification: reviewer confirmed the same read succeeds with escalation.
- Follow-up: use the known working execution route in this environment.

## Guessed documentation path in review

- Symptom: a broad reviewer search included nonexistent
  `docs/skill-provenance.md`, causing `rg` to exit 2.
- Impact: read-only; relevant existing-file matches were still returned.
- Root cause: an undocumented path was guessed instead of discovered first.
- Resolution: use the known `dot_agents/skills/metaprompt/SOURCE.md` and
  `docs/metaprompt-skills.md`; reviewer was instructed to avoid guessed paths.
- Verification/status: existing provenance and guide paths are readable;
  no implementation or benchmark artifact was affected.

The parent also included absent `.chezmoiremove` and `.chezmoiscripts` paths in
a read-only search. Their absence is now established; future inspection uses
discovered files. The command changed nothing. The final nested-instruction
search returned no files, subsequently confirmed with a filesystem inventory.

## Broader repository tests retain two existing failures

- Symptom: `python3 -m unittest discover -s tests -q` ran 551 tests in 83.612s
  and exited 1: 549 passed, two failed.
- Evidence: complete output read from
  `/tmp/metaprompt-sentry-migration-mp4gysfi/repo-tests.log`.
- Attribution: `test_push_policy_is_consistent_in_active_workflows` still
  expects an exact sentence missing from the unrelated commit-dirty skill;
  `test_exact_sanitized_tree_exists_without_unapproved_files` still finds the
  existing July 22 second-brain daily note outside its expected inventory.
  These are the same two failures documented before this replacement.
- Status/resolution: preserve those unrelated surfaces and report the failures.
  All 129 metaprompt-focused tests pass, including the updated eight-test
  integration suite. No new failure was introduced.
- Follow-up: resolve those policy/vault issues in their own authorized scope.

## Replacement verification

The defining integration checks first failed against the Majkey repository,
adapter, inventory and updater path; the Sentry replacement passes all eight.
Metadata validation and Claude-link tests also pass. One independent
gpt-6.1-sol/medium smoke check preserved a collision, saved a prompt-only
template, retained both variables and task constraints, returned all eight
sections and accurately labeled prepared evaluations. No downstream task or
closed benchmark was run by the check.

`refresh-config` exited 0 with `REFRESH COMPLETE`; log
`/tmp/refresh-config-20261004-142517-312906.log` contains no errors, conflicts or
adoption steps. All 13 installed non-cache files match source. The 43 obsolete
live files were removed only after their bytes matched the outgoing backup.
Claude's link resolves to the updated shared skill. Live Codex/Git settings,
the tracked Git config and pre-existing alias source remain byte-identical to
preflight; tracked Codex configuration now matches the live snapshot as required.
Both frozen benchmark inventories remain unchanged.
