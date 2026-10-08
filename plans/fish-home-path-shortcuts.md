# Normalize fish directory shortcuts

Add `tcs` for the session-tracking directory and teach fish-alias to store pasted example-user home directory paths using `~`. Add defining regressions, update source/documentation, then refresh and inspect installed abbreviations.

## Context and scope

Source: dot_agents/skills/fish-alias/SKILL.md and scripts/fish_alias.py, aliases/key_dirs.tmpl, tests/test_fish_alias.py. README and smoke docs receive minimal additions. Initial git status captured; numerous pre-existing dirty/untracked files, including the skill/tests and documentation, are protected. Initial implementation requested no commit; subsequent `$commit-session` authorizes the scoped commit and upstream push. Plan Mode unavailable in Default mode; this living plan captures decisions.

## Decisions

Normalize directory mappings only, after routing by actual path type. Replace only the leading `/home/example` at a path boundary. Keep command arguments, files, other users and embedded occurrences unchanged. Quoted/spaced paths must still roundtrip; repeated absolute requests must be no-ops once normalized. Add tcs to existing cdn section. Preserve conflicting definitions as comments.

## Checklist

- [x] Capture status and read helper, tests, docs, feedback, lessons and refresh implementation.
- [x] Observe normalization test RED (21 tests; 5 expected normalization assertions fail).
- [x] Implement helper and skill instructions; preview/apply tcs; update docs. Preview selected cdn, normalized target, zero conflicts.
- [x] Run regressions, type/syntax checks and refresh with protected source preservation.
- [x] Verify installed skill and tcs, record evidence and handoff.

## Risks and rollback

Prefix lookalikes and quoted tilde expansion require tests. Preserve all pre-existing content and staged state. Refresh has standing authorization and snapshots live Codex/Git before chezmoi apply; preserve differing protected source bytes at refresh entry. Roll back only task hunks. Sandbox workaround recorded in docs/postmortem/2026-10-08-fish-home-path-sandbox.md.

## Verification and review

RED/GREEN: python3 -B tests/test_fish_alias.py. Type check: basedpyright dot_agents/skills/fish-alias/scripts/fish_alias.py. Runtime: fish -c refresh-config; fish -n ~/.config/fish/key_abbr.fish; inspect tcs definition without invoking it. Installed helper/skill must match source. No supplied shortcut commands execute.

## Final evidence and handoff

- Defining RED: 21 tests, five expected failures showing absolute directory targets unchanged.
- First GREEN exposed an unrelated fixture section tie; recorded in incident. Explicit existing section override keeps normalization/no-op assertions intact. Live template preview independently selected cdn.
- `python3 -B tests/test_fish_alias.py`: 21 tests pass, exit 0.
- `basedpyright dot_agents/skills/fish-alias/scripts/fish_alias.py`: 0 errors/warnings, exit 0. Skill quick validator: valid, exit 0.
- Preview/apply: normalized target ~/coding/track-codex-sessions, cdn section, zero conflicts. Installed absolute request preview: changed false.
- Runtime refresh: REFRESH COMPLETE, exit 0; log /tmp/refresh-config-20261008-152719-2185323.log. Protected Codex source unchanged. Installed helper and skill bytes match source.
- fish syntax exits 0; live abbreviation is `abbr -a -- tcs 'cd ~/coding/track-codex-sessions'`. Inspect using abbr --show piped to rg because fish prints the full inventory even when a name follows --show.
- Targeted postmortem ledger check and scoped diff whitespace check exit 0. README and grouped smoke tests match implementation. Initial implementation was left uncommitted; subsequent delivery is recorded below.

Atomic unit: this plan, helper/skill changes, two defining tests, tcs mapping, README/smoke documentation and incidental failure ledger. Rollback only these additions, preserving pre-existing skill and other dirty work.

Paste-ready Cursor prompt: `Review plans/fish-home-path-shortcuts.md; verify directory-only /home/example prefix normalization, quoted/escaped spaces and repeated absolute no-op behavior. Run python3 -B tests/test_fish_alias.py and basedpyright dot_agents/skills/fish-alias/scripts/fish_alias.py; inspect installed tcs without executing it. Preserve pre-existing dirty work.`

Suggested eventual Conventional Commit: `feat(fish): normalize home directory shortcuts`.
Manual checks (repo cwd, no sudo): rg source tcs; fish -n generated file; inspect abbr --show filtered for tcs; installed helper JSON preview of original absolute request must be a no-op; fixture tests and type check must pass. Remaining limit: section heuristic and conditional activation follow existing host-specific rules.

## Delivery milestone — feat(fish): normalize home directory shortcuts

Session: `01a11cf7-4e1f-7e62-82a1-6c7fc66328df`. Scope helper returns unsafe because wrapper-mediated writes were not recognized (first_write/baseline null). Direct conversation write evidence establishes ownership for the normalization implementation, tests, tcs, skill guidance, README change, tcs smoke checks, this plan and the fish-home-path incident/ledger record. HEAD now includes prior unrelated work committed by other sessions. Exclude ctp alias, ctp smoke check, ctp incident and its ledger record. Existing index is empty at delivery entry.

Completed: normalized home directory mappings and installed tcs; fixture suite, type check, installed syntax and incident ledger verified. README gate: pass_no_change. Remaining: create this scoped commit and push main to origin/main (user@example.invalid:example-user/ai-cli-dotfiles.git`). No implementation blockers. Preserve unrelated ctp changes. Review rollback: revert only this scoped commit; no history rewrite.

Fresh delivery checks: `python3 -B tests/test_fish_alias.py`, `basedpyright dot_agents/skills/fish-alias/scripts/fish_alias.py`, `fish -n ~/.config/fish/key_abbr.fish`, live tcs inventory filtered with rg, targeted incident check and `./scripts/executable_readme-recruiter-sync`. Delivery results: 21 tests pass; type checker reports 0 errors/warnings; fish syntax and targeted incident check exit 0; live tcs maps to normalized cd target. Exact final staged diff will be reviewed before commit. Commit/push SHA and result will be reported in Codex output without a follow-up status-only commit.


## Concurrent delivery correction and follow-up milestone

During shared-index staging, cached smoke patch failed because another session staged ctp content. That session then committed our already staged implementation in `5451db5 feat(aliases): add Codex time projects shortcut`. This includes tcs, normalization helper/skill, tests, README, this plan and initial report; we preserve that history. Details: docs/postmortem/2026-10-08-fish-session-concurrent-index.md. Remaining session changes are tcs smoke docs, incident ledger coverage, the concurrency report and this status update. The follow-up subject is `docs(fish): finalize home shortcut verification`. No unrelated staged changes will be included in this follow-up.

Completed and verified: implementation, installed tcs, 21 passing tests, zero type errors, fish syntax, README gate. Remaining at commit creation: one upstream push to origin/main. No functional blockers; atomic separation was lost in concurrent shared-index commit, accurately reported without rewriting history. Exact follow-up content is reviewed against HEAD and the directly observed task writes. Subsequent push result and SHA are reported in Codex output.
