# Firstmate CTO attaches to a shell

Record why the operator cannot reach the saved CTO chat and verify a direct recovery
command while preserving the existing fleet and workers.

## Symptom and impact

User repeatedly lands in 0:fish and 1:fleet. Historical advice sent them to an
unspecified main conversation instead of providing recovery. Live approved tmux
metadata confirms cto-master has fish and fleet with no cto window.
The initial sandbox metadata read was denied (Operation not permitted); approved
read-only inspection succeeded. No worker or hook changes were made.

## Lookup and root cause

Lookup: firstmate cto fish missing chat tmux. No matching chat-recovery finding;
2026-11-05-firstmate-cto-startup documents selector grammar and preserving partial
sessions, which apply to safe inspection but do not restore a missing chat.
attach only attaches to the session; start deliberately refuses a missing cto.
Window navigation cannot create the absent conversation.

## Status and next steps

Implemented: explicit chat creates a separate Codex resume picker
in the original control directory and select it. Preserve fish, Fleet and all
workers. Never guess the latest thread across directories or resend task prompts.

## Validation findings

The first GREEN run exposed an overly strict test assertion: attach rechecks
ownership after selecting the window. Corrected the assertion to require the exact
CTO selection before the final attach, allowing the existing ownership checks.
The real-tmux test initially hit the same sandbox socket denial; host execution is
required to validate that boundary. These are validation issues, not worker errors.
Required refresh-config exited 1 before apply; private log
/tmp/refresh-config.ds4JyQcH.log is being inspected. Preserve unrelated sources.

## Resolution and verification

chat creates the missing cto window using codex resume -C with the original control
cwd, without a prompt, --last, or permission overrides. Repeated chat reuses it;
chat selects cto by name before attaching. --no-attach avoids changing client focus.

Final real isolated tmux suite: 26 tests passed, exit 0, 11.527s. Live recovery and
repeat both exited 0. Capture shows the cwd-filtered picker with exactly one saved
conversation: Drawing-night approval blocked. Live windows remain 0:fish, 1:fleet,
2:cto. The operator still needs to press Enter to resume; chat input and hook
approval after that selection are not verified. No worker or goal was resumed.

Full refresh is blocked by pre-existing duplicate source mappings for
.config/mimeapps.list (dot_config/mimeapps.list and private_mimeapps.list).
The existing /home/kevin/scripts/firstmate-cto dated November 5 differed only by
this task's additions. It was backed up to /tmp/firstmate-cto-before-chat-recovery
and replaced with the reviewed source; bytes matched. No MIME file was changed.
An initial guessed ~/.local/bin path was absent; chezmoi target-path and fish
resolved the real path. Sandbox fish startup also emitted write-permission errors;
no startup configuration was changed. Future discovery should prefer target-path.

Learning decision: no new general finding; existing partial-state ownership,
command-specific tmux target and path-discovery guidance apply. The new recovery
interface and its limits are documented in the operator guide and smoke checks.
This report records code and picker activation evidence, not active supervision.
