# Replace metaprompt with the selected Sentry skill

## Purpose and observable outcome

Replace the current Majkey-based `$metaprompt` with the pinned Sentry
`prompt-optimizer` selected in `docs/metaprompt-selection.md`, retaining the
`metaprompt` invocation. Deploy the tracked source to the installed skill and
verify exact package identity and local invocation behavior.

## Context and scope

The user explicitly requested replacement after the completed benchmark. This
supersedes the earlier benchmark's no-install boundary for this skill only.
The baseline `git status --short` was captured before edits. The existing
metaprompt import, docs, tests, benchmark, phone SSH work and `aliases/key_dirs.tmpl`
are already dirty. Preserve unrelated work and back up the outgoing source and
installed package before replacing owned files. No worktree, commit or push.

## Settled decisions

- Use getsentry/skills revision `d18b7aa8ba878354e5c348310230e652f7690f9c`,
  `skills/prompt-optimizer`, from the verified local benchmark snapshot.
- Preserve the native entrypoint byte-for-byte as `UPSTREAM.md`, its complete
  references and provenance/spec files, and Apache-2.0 license.
- Keep a thin local `metaprompt` entrypoint: native eight-section package,
  prompt-only saved artifacts, collision-safe filenames, canonical template
  variables and no implicit execution of the user's embedded production task.
- Keep `$metaprompt-alxve` and every frozen benchmark input/result unchanged.
- Replace obsolete Majkey-only helpers/resources after inventory/caller review;
  preserve recoverable backups outside the tracked tree.
- Run required `refresh-config` after checking its live-to-source snapshot and
  target scope. Verify actual installed files; a running picker may need a new
  session to reload its description.

## Checklist

- [x] Capture initial status and inspect source, report and instructions.
- [x] Back up outgoing files and define failing replacement integrity checks.
- [x] Install the pinned native content behind the existing metaprompt name.
- [x] Update focused tests, provenance, update procedure and user documentation.
- [x] Verify tests and frozen evidence; review refresh scope and run refresh-config.
- [x] Verify deployed bytes, references and discovery metadata; close out docs.

## Risks and rollback

The previous package is uncommitted; deleting it without a backup would lose
work. Chezmoi may retain obsolete unmanaged children; compare complete live
inventories before removing only backed-up outgoing package files. Refresh
snapshots live Codex configuration into the repo and may apply other pending
configuration, so inspect the dry-run and avoid overwriting unrelated live edits.
Rollback restores the recorded outgoing source backup and refreshes its exact
skill target, preserving unrelated paths. Benchmark native scores do not prove
the local adapter's full behavior; validate the adapter separately and do not
rerun or revise the closed benchmark.

## Verification

Observe a defining integration test fail on the old repo/pin/content, then pass
after replacement. Verify native byte equality, full manifest/license, local
links, alias and metadata, guarded update staging, and untouched alxve/frozen
inventories. Run focused metaprompt contract/integration tests and relevant
broader tests. Inspect actual installed bytes after refresh. Update
`docs/smoke-tests.md` with new eight-section output expectations and verify the
README gate. Record exact commands/results below.

## Progress and review

2026-10-04: Replacement authorized. Parent owns implementation and deployment;
a read-only reviewer checks tests, native-package fidelity and migration hazards.

Outgoing source (49 files) and installed package (50 files) are preserved at
`/tmp/metaprompt-sentry-migration-mp4gysfi`, with SHA-256 inventories. All source
files are attributable to the old manifest or local adapter/updater; there are
no unknown non-cache files. Claude's metaprompt link resolves to the shared
`~/.agents/skills/metaprompt`; no separate Codex-specific copy exists. No nested
instruction file adds a local constraint. Reviewer confirms exactly eight native
Sentry files, no upstream scripts/assets/UI metadata, and eight required sections.

RED/GREEN: the replacement integration suite first failed three assertions
(Majkey identity, missing Sentry adapter contract, obsolete resource inventory)
and raised the expected missing-entrypoint compatibility error from the old
updater. After importing the eight verified native files, retargeting the local
updater and preserving the local alias/save contract, all eight tests pass.
`python3 -m unittest discover -s tests -p 'test_metaprompt*.py' -q` passed all
129 tests in 20.730s. Skill-creator metadata validation and
`bash tests/test_claude_skill_links.sh` both exit 0.

Independent adapter smoke check: one fresh gpt-6.1-sol/medium agent used the
new source for a reusable checkout investigation template. Parent read back
`/tmp/metaprompt-sentry-smoke-lem94yky/prompts/checkout-flake-template-2.md`
(SHA-256 `f360e8818a409096764c0609a805e9c9dd04199b0bb66716de2cfc28668c2326`).
The existing unsuffixed file is unchanged; the workspace contains only those
two prompt files. Both variables, payment preservation, no deployment, unknown
root cause and focused-check stopping survive. The response has all eight
native sections and clearly labels its five prepared cases as unexecuted.
This is a single adapter check, not additional held-out benchmark evidence.

Broader suite: 551 tests / 549 passed in 83.612s (exit 1), with the same two
pre-existing failures: `test_push_policy_is_consistent_in_active_workflows`
and `test_exact_sanitized_tree_exists_without_unapproved_files`. The complete
log was inspected and attribution is recorded in the replacement postmortem.

Deployment: snapshot dry-run passed. Preflight showed only the intended skill
changes, task docs/tests, the standard Claude-link installer, and the live
Codex model/reasoning/service-tier snapshot. Git source/live bytes agreed.
`fish -c 'source /home/example/linux-config/dot_config/fish/functions/refresh-config.fish; refresh-config'`
exited 0 with `REFRESH COMPLETE`; the ten-line log is
`/tmp/refresh-config-20261004-142517-312906.log`, with no errors or adoption.
After apply, 43 obsolete files still present under the live package were
removed only after verifying each against the backup. All 13 installed
non-cache files match source and there are no extra non-cache files. Claude's
complete-directory link resolves to that installation.

Live Codex and Git settings, tracked Git config, and the pre-existing dirty
alias source remain unchanged. The required tracked Codex snapshot differs
from the initial source in model/reasoning/service-tier keys and equals the
preserved live config. Treat it as incidental existing live state in any later
commit workflow; no model setting was chosen or changed by this replacement.
Both frozen inventories (54 new and 82 historical files) match. No skill-picker
hot reload is claimed; a new session loads the installed instructions. No
commit, push or new benchmark request occurred.

Final closeout: README gate returned `pass_no_change`; scoped diff checks passed.
All 19 checked local replacement/provenance/guide links resolve and no checked
document has trailing whitespace. Final installed-byte comparison found zero
mismatches across 13 files; both frozen 54/82-file inventories still match.

## Handoff

Cursor prompt: Read this plan and `dot_agents/skills/metaprompt/SOURCE.md`.
Verify that `$metaprompt` resolves to the pinned Sentry package with its native
eight-section workflow and local artifact-saving contract. Preserve frozen
benchmarks, alxve, backup files and unrelated dirty changes. Run the documented
tests and compare installed hashes; do not run new benchmark trials or commit.

Suggested commit when separately requested: `feat(skills): use Sentry for metaprompt`.
