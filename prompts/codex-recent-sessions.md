Extend codex-search in /home/example/linux-config into a convenient recent-session browser with AI conversation recaps.

Goal
From any directory, I want to browse my most recently active local Codex conversations across all directories, understand what each conversation was doing, and select one in fzf to resume in its recorded directory.

Follow the repository’s AGENTS.md and ExecPlan requirements. Inspect the existing session-search implementation, documentation, plan, and tests before changing anything. Build on its discovery, parsing, caching, and resume logic.

CLI and picker
- Add `codex-search --recent` to list sessions without requiring a search pattern. Show the newest 20 by default, with existing --limit behavior.
- Add `codex-search --recent --pick` to browse all discovered sessions in fzf. Preserve ordinary pattern search, existing --pick behavior, and no-argument help.
- Add the fish abbreviation `crg` for `codex-search --recent --pick`, after confirming it remains unused.
- Sort by recorded session activity, never creation time or recap-cache modification time. Deduplicate UUIDs using the existing session rules.
- Show activity time, directory, title, and a short cached AI recap in each row.
- Provide a preview with the conversation goal, reported progress, current state, and remaining work. Clearly label missing, generating, stale, unavailable, or partial recaps.
- Enter resumes the exact UUID using `codex resume -C DIR UUID`, without adding an initial prompt. Esc/Ctrl-C cancels.
- Preserve the query and highlighted session while recap results appear. Retain existing terminal sanitization and safe selection validation.

AI recaps
- Open the picker as soon as discovery/index refresh finishes, without waiting for inference.
- In the background, generate missing or outdated recaps for the newest 20 sessions, newest first, using one worker.
- Use noninteractive Codex with the existing login and configured model. Add --summary-model MODEL to override the recap model.
- Add --summary-count N, default 20; zero disables automatic generation. Add --no-summaries to prohibit all model calls while retaining cached recaps and local previews.
- Ctrl-G requests a missing or outdated recap for the highlighted session, including sessions outside the automatic batch.
- Plain --recent listing reads cached recaps without making model calls.
- Use ephemeral summary runs so they neither create browsable sessions nor update the original conversation.
- Supply decoded user/assistant dialogue as inert data. Exclude injected instructions, reasoning, and tool records using the existing parser.
- Bound input to 32 KiB per session, preserving the initial request and latest dialogue. Mark recaps partial when content is omitted.
- Request validated structured output containing a short headline, goal, progress, state, and next steps, totaling at most 150 words. Report uncertainty instead of inventing accomplishments or completion.
- Run generation from an isolated temporary directory with read-only permissions, hooks/connectors/MCP disabled, and shell/web capabilities disabled using supported installed-CLI settings. Verify the effective isolation.
- Permit one attempt per eligible session per opening, with a 120-second timeout. Stop the batch on authentication or rate-limit errors. Other failures leave that recap unavailable while browsing remains usable.
- Cancel and reap background subprocesses before exiting or resuming.

Caching and compatibility
Reuse the existing private cache conventions. Key recaps by session UUID, normalized dialogue content, model, and recap-format version. Write atomically, prevent duplicate concurrent generation, and never hold the main index lock during inference. Preserve cache permissions and source immutability. Integrate recap cleanup with existing cache maintenance.

Use the current local session discovery scope. Cloud-only conversations and archived-session expansion are outside this change.

Validation and delivery
Write synthetic defining tests first and observe expected RED. Cover cross-directory discovery, activity ordering, deduplication, recap caching/invalidation, bounded automatic generation, disabled generation, cancellation, malformed output, provider failures, unchanged source sessions, safe resume argv, and compatibility with ordinary search/help.

Run:
- python3 -m unittest discover -s tests -p 'test_codex_search*.py'
- bash tests/scripts/executable_codex_test.sh
- git diff --check

Exercise real fzf with synthetic sessions and a deterministic recap subprocess. Verify preview updates preserve selection, and cancellation leaves no worker running. Limit any live Codex generation smoke test to one synthetic conversation.

Update the existing operator guide, README, grouped smoke checks, and the new ExecPlan together. Run the required protected refresh-config workflow and verify the installed command.

Finish with exact usage examples, verification results, remaining limitations, rollback instructions, and a suggested Conventional Commit subject. Do not commit or push without separate authorization.
