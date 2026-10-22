# Public metadata blocked a scoped cap-fix commit

Track the privacy gate false positives, the explicitly authorized policy correction, and the checks needed before releasing the dependent cap fix.

## Symptom and impact

A ten-file reviewed cap-fix candidate was blocked by eighteen existing findings: ten home-directory references, six ordinary recovery-named source/doc paths, and author/committer identity emails counted separately. No provider-token or credential category appeared. Nothing was committed or pushed while the gate was blocked.

## Evidence and applicability

The gate scans the complete staged tree, not only changed files. All sixteen flagged file paths were unchanged from HEAD. private_path classified any path component containing recovery; check retained the shared scanner's home_path heuristic and rejected unapproved identity emails. The user explicitly requested allowing these metadata/source cases, followed by commit-session.

Memory lookup privacy gate home_path recovery identity matched local-privacy-reviewed-content-approvals. Its explicit-private-policy precedence and snapshot-refresh lessons apply. Its older metadata allowlist requirement is superseded by the requested gate defaults. Initial guessed installed skill/test reads found unavailable paths; the repo mapper identified canonical paths before changes.

## Status and next steps

Policy implementation is verified at the source and installed-hook boundaries. Allow public metadata and ordinary recovery filenames while preserving actual authentication-secret detection, blob-email checks, explicit private rules and private archive directories. Keep the standalone history auditor unchanged. Verify installed snapshots, scoped staging and upstream delivery; no history rewrite or live Discord activation.


Additional execution evidence: a read-only fish function inspection launched fish with normal startup, which attempted fnm multishell/universal-variable/alias writes outside the sandbox and printed read-only filesystem errors despite exit 0. No successful configuration refresh is inferred. Subsequent refresh/inspection will use fish --no-config with only necessary functions and approved filesystem scope, avoiding startup side effects. No existing listener or desktop layout was changed.


Deployment attempt: refresh-config was invoked with fish --no-config and the explicit installed function directory. It exited 1 during chezmoi apply, before shortcut synchronization, leaving a private log at /tmp/refresh-config.Qn2wYPIn.log. The canonical/source skill update is verified but broad refresh activation is not claimed. The newer-looking Kitty/service/audio/tmux files were inspected and match source text, so no unrelated content adoption was needed. Diagnose the apply failure before retry; deploy only the requested skill and policy snapshots if the blocker is unrelated.


## Resolution and final verification

The gate permits the built-in home-path heuristic for indexed bytes and local LFS payloads, permits effective Git name/email metadata without an allowlist, and no longer treats arbitrary recovery-named source/docs as private paths. Exact private archive directories, real authentication secrets, blob-email findings and explicit private rules remain blocking. Explicit rules are reapplied after public allowances, including LFS and Git metadata. Legacy identity-policy files remain validated for compatibility. The standalone history auditor is unchanged.

The test worker observed seven intentional RED failures before implementation. Final independent checks passed 49 gate tests, 14 history-audit tests and one immutable-tree checkpoint test. Source checks pass on both real candidates. The actual installed pre-commit hook passed without changing HEAD or index, and status confirms the scanner snapshot is current. Independent review found no correctness/security blocker. The canonical and installed commit-session skill/scanner bytes match.

Basedpyright reports one existing dynamic-import typing error and 110 warnings; the HEAD baseline has the same error and 114 warnings. Complete outputs are retained privately under /tmp. No clean type-check result is claimed. Two historical evidence claims were initially available to the reviewer only as worker summaries; type-check primary logs were subsequently retained.

The refresh failure was permission-only drift: reviewed live/source bytes were identical, but source modes were 0664/0775 versus live 0644/0755. Only the four exact targets were reconciled; the broad apply remained unforced. A subsequent refresh-config completed apply, shortcut regeneration and shell reload with exit 0. The existing privacy-hook snapshot was reinstalled and verified current. No unrelated source content was adopted or discarded. Normal fish startup was avoided after its sandboxed inspection attempted unwritable fnm/alias/universal-variable paths.

Status: policy fix and installed activation verified. Scoped commit/push delivery is tracked in plans/privacy-gate-public-metadata.md. The dependent bot still requires a restart and live private-channel smoke check. Rollback: revert this focused gate/skill change and reinstall the snapshot; no Git history or credentials were changed.


Memory-registration verification caught a schema error in the new entry: symptoms and diagnostics must be nonempty lists, but the initial authoring used strings. Corrected those two fields and updated the reviewed report hash; this was a local metadata-authoring failure, not a privacy gate or product regression. Targeted validation is rerun before commit.


A later optional broad refresh encountered a new unrelated mimeapps.list conflict. Read-only inspection confirms identical bytes but live mode0600 versus source0664. The more restrictive live permissions were preserved rather than broadened. The earlier full refresh and subsequent installed skill/scanner/hook verification remain valid for this policy; broad MIME permission drift remains outside scope. No further configuration changes are needed for the requested policy.
