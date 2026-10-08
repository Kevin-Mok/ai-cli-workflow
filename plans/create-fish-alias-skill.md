# Create fish alias skill

Create and install `fish-alias` so an abbreviation plus command or path updates the correct shortcut template, preserves conflicts as comments, and refreshes the deployed environment. Tests use disposable fixtures; the example is not installed into live aliases.

## Context and boundaries

Canonical sources are aliases/key_aliases.tmpl, key_dirs.tmpl, key_files.tmpl. sync-shortcuts reads chezmoi-rendered sources; file keys gain an n prefix. Existing generator strips quoted hashes and truncates spaced paths. Protected pre-existing dirty files include README, smoke tests, aliases, lessons and memory; initial git status captured. No commit, push, worktree, metaprompt changes, or example alias activation.

## Decisions

- Use fish-alias with a JSON-stdin Python helper to avoid shell interpolation and loss of the command remainder.
- User key follows existing source conventions: file key re produces nre. Report the effective fish name.
- Route by path existence, trailing slash or recognizable file suffix; ask for ambiguous nonexistent paths. Commands route to existing nearest executable-family section; ties remain reviewable and allow a section override.
- Render each candidate line with chezmoi to identify currently active conditional definitions. Comment only active conflicting generated fish names with exact '# '; insert unconditional new entries outside template branches. Reject inline/multiline definition layouts requiring manual review.
- An identical active mapping with no other effective-name conflict is a byte-identical no-op. If an identical mapping coexists with a different active conflict, retain it and comment the conflicting mapping.
- Repair parsing in the existing generator, retaining source order and command quoting; paths keep their whole shell expression. Do not execute supplied commands.

## Checklist

- [x] Read prompt, instructions, dirty state, creator guidance, lessons and feedback; independently inspect generator.
- [x] Add isolated defining tests; observe expected RED before implementation.
- [x] Implement helper, minimal skill metadata and generator parsing repair.
- [x] Update README, skill inventory and grouped smoke checks.
- [x] Run focused fixture/regression checks, validator and generated fish syntax.
- [x] Run refresh-config; compare deployed skill bytes and Claude link.
- [x] Reconcile final diff, preserved state, evidence and limitations.

## Risks and rollback

Conditional activation depends on current chezmoi data; inactive definitions are preserved and may conflict on another host. Multiline commands, malformed templates, unsafe abbreviations and ambiguous paths fail before writes. Generator parsing is exercised against current rendered sources and disposable home outputs. Refresh snapshots live Codex/Git and may adopt unrelated local conflicts; capture ownership before refresh. Rollback only session-added files/hunks; preserve original dirty state. Default shell sandbox remains unavailable; approved scoped route documented in linked postmortem.

## Verification

`python3 -B tests/test_fish_alias.py`: command/directory/file routing, work-section placement, effective-name conflicts, exact comments, idempotence, missing input, quoting, conditions, content preservation and generator syntax without executing commands. `bash tests/test_refresh_config_function.sh`, `bash tests/test_claude_skill_links.sh`, skill creator quick_validate; fresh isolated generation and `fish -n`. Runtime `fish -c 'refresh-config'`; exact source/installed byte comparison and Claude symlink check.

## Progress and review

Inspection confirms generator issues; changes are necessary to honor spaced-path and quoted-hash contract. Plan Mode is unavailable in this execution harness; living decision-complete plan used in Default mode. Sandbox incident: docs/postmortem/2026-10-08-fish-alias-skill-sandbox.md. No supplied user command will be executed.

User updated canonical instructions during implementation: added readable default CLI, explicit --json, --plain and --details after deliberate RED flag test.

Independent forward test /tmp/fish-alias-forward-sf3raztc passed with real template copies. Review demonstrated template delimiter injection via harmless hostname-expression preview. Defining guard test observed RED (input accepted); reject request delimiters before any rendering. Current source generator and fish -n both pass using /tmp/fish-alias-current-5z3s506c.

Refresh preflight: dot_codex/config.toml has skip-worktree and differs from HEAD and live config. Preserve its original bytes after the refresh's required live snapshot/apply, while keeping installed live settings unchanged. This restoration preserves pre-existing work rather than introducing a new configuration change. Git source equals live.

## Final evidence

- RED: initial 11 tests produced 10 expected failures (missing helper and broken quoted-hash fish syntax). Corrected invalid file-prefix fixture based on generator evidence, not implementation accommodation. Readable-default and template-input guard tests each observed RED before their changes.
- GREEN: `python3 -B tests/test_fish_alias.py` — 19 tests, exit 0; `basedpyright dot_agents/skills/fish-alias/scripts/fish_alias.py` — 0 errors/0 warnings, exit 0.
- `quick_validate.py dot_agents/skills/fish-alias` — valid, exit 0. `bash tests/test_refresh_config_function.sh` and `bash tests/test_claude_skill_links.sh` — exit 0. Scoped `git diff --check` — exit 0.
- Full current-template isolated generator and fish syntax — exit 0. Independent forward fixture command/file/idempotence/conditions all passed and generated effective definitions were inspected without expansion.
- Runtime refresh — `REFRESH COMPLETE`, exit 0; log `/tmp/refresh-config-20261008-130254-1743693.log`. Codex source bytes captured at refresh entry were restored exactly (True immediately after). Earlier preflight hash later differs amid concurrent session writes; preserve the newer shared state rather than restore an older checkpoint. Other concurrent README/notification/memory changes were left untouched.
- Installed SKILL.md, agents/openai.yaml, helper and sync-shortcuts match source bytes; Claude directory symlink resolves to installed skill. `fish -n ~/.config/fish/key_abbr.fish` — exit 0. All three shortcut source hashes unchanged across refresh; cbn example not installed.

## Handoff

Atomic plan is this file; all task documentation and helper/generator changes form one uncommitted unit. Paste-ready follow-up prompt: `Review plans/create-fish-alias-skill.md and run python3 -B tests/test_fish_alias.py plus basedpyright dot_agents/skills/fish-alias/scripts/fish_alias.py; preserve unrelated dirty work and do not install example aliases.` Manual preview is documented in docs/smoke-tests.md#fish-alias-skill. Suggested eventual subject: `feat(skills): add fish shortcut workflow`. No commit/push/worktree performed. Limits: host-specific condition activation; file-key n prefix; multiline/template-delimiter requests need clarification/manual literal handling; existing out-of-template fish definitions are outside the three-source conflict scope.


## Completion review follow-up

A fresh independent review found absolute executables with arguments routed as paths and backticks acquiring backslashes in stored fish abbreviations. Defining regressions observed RED, then minimal routing/quoting changes passed. A concurrent template-delimiter safeguard was preserved and its rejection reason verified. Current completion work reruns installation after these two helper changes; prior 15-test evidence does not cover them. The stronger template rejection assertion has a distinct test name so it cannot shadow the existing regression.

Final shared-source checks: 19 tests pass, including additional absolute-executable routing, template rejection reason, and stored-backtick preservation cases contributed concurrently and independently rerun. Final refresh log `/tmp/refresh-config-20261008-130640-1761914.log` reports REFRESH COMPLETE (exit 0); all installed fish-alias bytes and generator match final source, fish syntax and quick validator exit 0. Optional native parent-thread status message failed at transport; no retry, unrelated to implementation. Recorded in docs/postmortem/2026-10-08-fish-alias-handoff-transport.md and reviewed ledger. Native title tool uses the same unavailable transport, so existing task title retained.


Fresh completion evidence: 19 shortcut tests pass (including stored backtick text and absolute commands); basedpyright 0 errors/0 warnings; skill validator valid; refresh/link fixtures exit 0; 22 snapshot regressions pass with PYTHONPATH=.; current-template disposable generation and fish -n exit 0. Runtime refresh log /tmp/refresh-config-20261008-130716-1764107.log reports REFRESH COMPLETE, exit 0; protected config and alias source bytes preserved. Installed skill metadata/helper/generator match source; Claude link resolves correctly; installed cbn preview selects work and does not apply. Review incident and learned stored-text checks recorded in postmortem memory. No commands supplied as shortcut text were executed and no commit or push was made.

Final post-learning refresh also exited 0 with REFRESH COMPLETE; installed fish-alias and updated postmortem-memory bytes match source, installed fish syntax passes, and scoped whitespace checks exit 0.
