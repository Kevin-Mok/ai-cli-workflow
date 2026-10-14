# Router evaluation environment checks

This records read-only inspection failures during the router evaluation and the
scoped workarounds used without changing live configuration.

## Symptom and impact

- Initial `git status --short` failed: Git LFS tried to create
  `/home/example/linux-config/.git/lfs/tmp/2046508005` in the read-only common Git
  directory. No tracked files had been edited.
- A personal-context lookup used a guessed helper name, `personal_context.py`,
  which does not exist. No private context was read or written by that call.
- A guessed Claude skill-link script filename did not exist; discovery found
  `run_after_install-claude-skills.sh.tmpl` and it was read successfully.
- Sandbox registry download was blocked; a scoped read-only npm registry
  download succeeded with normal escalation and the release hash verified.
- A disposable native SQLite build lacked `/usr/include/node/common.gypi`.
  Fetching official Node 22.15 headers into `/tmp` allowed the build and real
  isolated CLI checks. No live package installation or GitHub fetch occurred.
- Chezmoi inspection with `/dev/null` initially lacked an explicit config
  format. Adding `--config-format toml` fixed parsing, but target inspection
  then attempted existing GitHub externals and was blocked before output.
  An isolated source containing only new targets avoided existing externals.
  The first seed filename used attributes in the wrong order; inspection
  exposed `.claude-code-router/create_config.json` instead of `config.json`.
  Official attribute documentation and a defining RED test established the
  correct `create_private_config.json` order. GREEN inspection verifies 0600
  mode and existing private JSON contents preserved without apply.
- The existing-content test initially compared a fixture with mode 0664 to a
  private target, producing an expected permission-only diff. The fixture was
  corrected to private mode; JSON contents were never overwritten.
- The missing-npm fixture removed Bash from PATH too. Invoking `/bin/bash`
  independently of the fixture PATH corrected this test harness error.
- The reusable real smoke checker initially hit sandbox loopback restrictions.
  Scoped escalation succeeded: temporary HOME, no providers, management ready,
  disabled gateway/profiles/logging persisted, invalid token rejected 401, no
  Claude/Codex writes, cleanup complete (exit 0).
- An ancillary full postmortem-memory suite ran 26 checks, with 25 passing and
  `test_actual_ledger_reference_status_and_coverage` failing on repository-wide
  coverage of external incident aliases. This is a shared corpus gate outside
  router behavior; do not change other sessions' ledger/reports to hide it.
  Record targeted current-report coverage separately and report this warning.
- Serializing a ledger append initially introduced unrelated key-order and
  Unicode-escaping noise. The branch diff was reduced to one report entry.
  Auto-review rejected an unguarded rewrite of the shared canonical ledger;
  a prepared formatting-only correction with identical semantic JSON,
  file lock, exact-byte concurrency checks and atomic replacement was approved
  and succeeded. All pre-existing ledger values/entries were preserved.
- The supplied tweet and guessed hosted CLI-doc URL were inaccessible through
  the web tool. The published package README supplies primary install docs;
  the tweet remains an unverified motivation, not evidence of savings.

## Lookup and evidence

The canonical postmortem-memory helper was searched for
`git-lfs read-only file system status filter-process`. Results included sandbox
and path-discovery guidance, but no matching LFS status remedy was established.
The LFS error itself identifies the common Git directory permission boundary.
The helper-name error supports discovering actual paths before invocation.

## Resolution, verification and follow-up

The scoped status workaround succeeded with exit 0:
`git -c filter.lfs.process= -c filter.lfs.required=false -c filter.lfs.clean=cat status --short`.
It reported four protected pre-existing media changes: the last30days dog JPEG
and `scripts/can-i-ask-you-a-question.mp3`, `scripts/Voice Contributor-celebrate.mp3`, and
`scripts/Voice Contributor-intro.mp3`. These will not be staged or altered.

Path discovery found `context_store.py`; its topics/brief reads succeeded.
Nine router fixture checks pass, including the real chezmoi mapping/create-only
check. The published package with native SQLite passes the reusable real
management smoke checker. No repo-wide Git config or LFS asset changes are
warranted. Use scoped approval for common Git index/object writes at commit
time. Paid provider behavior remains outside these verification results.

Learning decision: these are scoped environment, path/attribute discovery and
test-fixture failures, not new router runtime defects. Existing environment and
path-discovery guidance remains applicable; no new generalized remedy is
inferred from the command-local LFS bypass. Register this report's reviewed
hash/alias with that explicit no-new-learning decision and check coverage.
