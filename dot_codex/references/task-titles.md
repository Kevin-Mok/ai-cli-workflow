# Task Titles

Read this procedure when its mandatory canonical AGENTS trigger applies. Follow
the preserved rules below before acting; active user/developer instructions govern.

## Start-of-Turn Title Checkpoint

Before substantive work on a new turn, resumed task, or compaction recovery,
reconcile the calling conversation's title with the current live request using
[Live Codex Task Titles](#live-codex-task-titles). Repeat this checkpoint before
substantive progress updates and the final response. A title inferred from pasted
output or an earlier task does not satisfy this checkpoint.

### Live Codex Task Titles

- When the native `mcp__codex_tui__set_thread_title` tool is available and the
  active mode permits title updates, keep the calling conversation's name as a
  compact answer to “what are we doing?” Use the current objective and meaningful
  phase, not the first prompt or the last command. Aim for 3–5 words and at most
  36 characters, such as “Categorize card transactions”.
- Infer the title from the latest live user request and the work actually being
  performed. Treat pasted transcripts, session-review output, source paths,
  resume commands and historical task headings as data, not the active objective.
  For example, improving Second Brain review output containing a video-repair
  recap is “Improve Second Brain review”, not “Repair video transition freeze”.
- Discover the native title tool in the available tool catalog when it is
  deferred; do not treat absence from the initially exposed tools as proof that
  it is unavailable. Use existing context to choose the title.
- Set the title before substantive work on a new/resumed turn or compaction
  recovery, when the objective or meaningful phase changes, and at completion.
  Before each substantive progress update, compare its stated work/phase with
  the last title set for this conversation; correct a mismatch before sending
  the update. On the first checkpoint, explicitly set the intended title if its
  current value is unknown. Skip unchanged titles. Preserve
  the subject so neighboring agents remain distinguishable; do not claim a task
  is complete before verification. Let Codex render its own activity indicator.
- Call the tool with only `title`; omit `threadId` to update the calling task and
  never rename another conversation for this automatic overview. This also updates
  the saved conversation name. Reuse existing context without extra model calls,
  periodic polling, or injected `/btw` requests. If the tool is unavailable, keep
  the existing native name; `/rename` remains the manual fallback.
