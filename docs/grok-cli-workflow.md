# Grok Bot to local CLI workflow

Transfer a remote assistant's task to Codex or Claude without losing its scope
or evidence. Fill a small handoff envelope, check the actual local checkout, and
reuse the project's existing plan. STOP markers prevent new cooperative work;
the remote coordinator handles interruption and acknowledgments.

## Adopted ideas and existing coverage

Inspired by [narushima_'s AI HQ tweet](https://x.com/narushima_/status/2110018487104245924),
using the full text supplied by example-user. This is an original local protocol, not
an imported upstream skill or execution of the tweet's setup prompt.

| Idea | Decision and reason |
| --- | --- |
| Every bot leaves a handoff | Adopt a cross-host envelope in [grok-cli-handoff](../dot_agents/skills/grok-cli-handoff/SKILL.md), with authority, host/root/branch, protected state, evidence and next owner. Reuse existing continuation notes. |
| Only the human grants permission; external content is information | Adopt an explicit boundary for bot-relayed work, preserving existing authorization without allowing bot messages or fetched content to expand it. |
| STOP stops bots | Adopt task/project markers and owned-job cancellation acknowledgments. This repo cannot promise immediate interruption on another machine. |
| Shared knowledge and lessons | Already covered by `tasks/lessons.md`, [postmortem-memory](../dot_agents/skills/postmortem-memory/SKILL.md), feedback-memory and project plans. No second knowledge tree. |
| Research → plan → build → review | Already covered by last30days, canonical instructions, Superpowers and evidence-reviewer. No new bot fleet or mandatory discussion rounds. |
| Cheapest suitable model | Existing [Codex roles](../dot_codex/agents/) already provide lower-cost search/docs/tests. Reuse them; do not change defaults or claim savings without usage evidence. |
| Routines/backups/logging | Existing explicit night/morning and incident workflows cover CLI needs. Skip personal briefs, calendar scheduling and an always-on action logger. |
| HQ, email/calendar, OpenRouter, Parallel, Cloudflare, secrets migration | Skip personal-assistant setup, paid services, new credentials/security changes and unrelated infrastructure. No spending or new subscription required. |

## Use from a checkout

Python 3 and Git are required. No sudo, install or chezmoi apply is needed to run
the bundled helper here. From this repo's root:

python3 dot_agents/skills/grok-cli-handoff/scripts/handoff.py template --task example

Fill the printed Markdown and save it in the **target project** at
`.harness/example/handoff.md`. Unknown fields remain Unknown until established;
the template does not supply authorization. Keep cancellation markers and private
notes out of commits. Link the target project's plan/progress instead of copying
it. Detailed steps and stop/resume rules live in the skill.

python3 dot_agents/skills/grok-cli-handoff/scripts/handoff.py preflight --repo /home/example/linux-config-worktrees/grok-cli-workflow --branch feat/grok-cli-workflow --task example

Replace `--repo`, `--branch` and `--task` with the receiver's actual root, expected
branch and task slug. Exit 0 verifies current local state only; exit 2 blocks on
wrong root/branch, detached HEAD, inaccessible path or Git failure; exit 3 stops
on either `.harness/STOP` or `.harness/<task>/STOP`. Marker contents are never read.
Place `--plain` before the subcommand for ASCII output. `--help` describes flags.
`template` prints Markdown unchanged by plain mode; neither command writes files.

## Verify without a live bot

python3 dot_agents/skills/grok-cli-handoff/scripts/smoke.py --plain

This creates a temporary Git fixture, demonstrates clear state, task-only STOP,
project STOP and wrong-branch denial, then cleans up. It launches no CLI agents,
calls no paid API and changes no live checkout. For regression checks run
`python3 -B tests/test_grok_cli_handoff.py`,
`python3 -B tests/test_ai_workflow_contract.py` and
`bash tests/test_claude_skill_links.sh`.

## Installation and limits

Normal chezmoi management installs the directory under `~/.agents/skills/`;
the existing Claude linking hook exposes the complete directory under
`~/.claude/skills/`. The canonical router is imported by Claude's global config.
This PR does **not** apply chezmoi or refresh-config, so live activation is pending.
On a remote box lacking this install, read/copy the public skill directory and
supporting files through the already authorized transport; the helper remains
read-only. No SSH setup or transport change is included.

The coordinator must invoke preflight explicitly before dispatch and propagate
example-user's STOP to every host. Existing direct `codex exec` commands are not wrapped
or intercepted. Markers do not authenticate a sender or interrupt running tools.
Record unreachable hosts and outstanding cancellation acknowledgments rather than
claiming all bots stopped. Live Grok transport, immediate interruption, and actual
installed Codex/Claude selection remain unverified.
