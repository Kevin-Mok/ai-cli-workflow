# Live Codex overviews above Kitty windows

Show a compact answer to “what are we doing?” above each Kitty terminal. Expose
i3 titlebars, use native Codex task names for live summaries, deploy the settings,
and verify the runtime and shared documentation without disturbing other work.

## Purpose and observable outcome

Each Kitty window has a single titlebar. Each Codex conversation uses a short
current-work summary that changes at meaningful task/phase transitions. Examples:
“Build budget tracker”, “Categorize card transactions”, “Verify expense totals”.
The activity indicator remains; the project suffix is removed. Saved conversation
names change with the summary, explicitly accepted by the user.

## Context and scope

Kitty 0.49.2, i3 4.23, Codex 0.160.0. Current i3 rules give every window a pixel
border, hiding titles in split layouts. Native Codex names already reach X11.
The calling task has mcp__codex_tui__set_thread_title; omitting threadId targets
only that conversation. Native first-prompt names do not track later work.

Change the managed i3 template, canonical Codex instructions, live/managed title
setting, README and smoke checklist. Use the existing refresh-config workflow.
No new summarizer, timer, model calls, /btw injection, Kitty plugin, or worktree.
The user subsequently requested commit-session; ship only attributable changes,
including this plan and matching documentation, to the configured upstream.

## Assumptions and decisions

- Add for_window [class="^kitty$"] border normal 3 after the general pixel rule;
  keep existing font/colors and other application borders.
- Use tui.terminal_title = ["activity", "thread-name"].
- Agents summarize their current objective/phase in 3–5 words, <=36 characters;
  update at task start/resume, meaningful goal/phase changes and completion.
  Omit threadId; skip repeated names and keep the native name if the tool is absent.
- The native tool also renames saved conversations. Fullscreen hides i3 chrome.
- Instructions/settings take effect for new/resumed Codex processes. Existing
  window chrome can be updated immediately without restarting conversations.
- Live/tracked Codex settings differ and config.toml has skip-worktree. Edit only
  the live title option, then refresh-config snapshots it into the tracked source;
  preserve unrelated settings, index flags, existing staged work and dirty edits.
- Config/instruction changes use an executable runtime RED/GREEN probe plus
  existing regressions and manual checks, without tests mirroring config literals.

## Ordered implementation checklist

- [x] Capture current status, relevant source/policy and protected dirty state.
- [x] Observe defining RED: all 12 Kitty windows have pixel borders; 8 have zero
  title-decoration height. Live terminal_title uses the native default.
- [x] Run baseline terminal-workflow and dictation-binding checks (both exit 0).
- [x] Add Kitty-specific titlebars and compact native-summary instructions.
- [x] Add the title option without changing unrelated live settings.
- [x] Update README and grouped smoke checks with fallback/activation limits.
- [x] Validate rendered i3 and Codex settings; run required refresh-config.
- [x] Reload i3 and update existing Kitty borders; verify native self-title updates.
- [x] Run fresh focused regressions and runtime probes; record remaining manual checks.
- [x] Review the session diff and finalize evidence/rollback notes.

## Protected state, risks and rollback

Initial dirty files include README.md, aliases/key_dirs.tmpl,
docs/phone-ssh-public-ip.md, docs/smoke-tests.md, dot_agents/skills/README.md and
dot_codex/AGENTS.md, with untracked postmortem-memory work, prompts, tests and plans.
Full initial status and private baselines are in /tmp/kitty-codex-overview-01a10c8c.
Make additive edits to shared files and preserve concurrent changes. refresh-config
snapshots live Codex/Git config, applies chezmoi, regenerates shortcuts and reloads
fish; inspect its resulting diff and do not discard unrelated adopted local work.

Rollback removes this task's Kitty override, title option and instruction section,
refreshes config and changes Kitty borders back to pixel 3. Conversation names
already changed require manual /rename. Native title summaries follow agent
instruction compliance, not an independent clock. Missing title tools keep the
existing name; /rename is the documented fallback. Do not rename other active
conversations or interrupt their work during verification.

## Exact verification

- RED/GREEN: python3 probe over i3-msg -t get_tree checks Kitty border=normal and
  positive actual_deco_rect height for rendered split-layout windows. Before: assertion fails
  for the expected missing titlebars; after: all current Kitty borders are normal.
- Render template using chezmoi execute-template, then i3 -C -c RENDERED_FILE;
  after deployment run i3 -C -c /home/example/.config/i3/config (expect exit 0).
- Parse live and managed TOML with Python tomllib; assert terminal_title exactly
  ["activity", "thread-name"] and alternate_screen remains "never".
- bash tests/test_st_terminal_workflow.sh and
  bash tests/test_i3_speechnotes_dictation_binding.sh (expect exit 0).
- Native calling-task rename updates this conversation's X11 title; compare
  another conversation's saved name before/after to establish isolation.
- Manually check two same-repo conversations, a changed objective, narrow splits,
  busy/attention/completion, resume persistence and existing scrolling gestures.
  Do not claim unperformed model/visual acceptance checks pass.
- Targeted postmortem-memory check and git diff --check must pass.

## Progress, evidence and review notes

Implementation started 2026-10-05 after user approval of the in-chat plan. Native
self-title call returned threadId 01a10c8c-4193-7cc2-9517-11b8e0a76cd4 and title
“Implement live Codex overviews”. Baseline regressions both exited 0. Deliberate
RED is exempt from postmortem policy. Inspection failures are recorded in
../docs/postmortem/2026-10-05-kitty-overview-inspection.md.

## Handoff

Suggested commit: feat: show live Codex task summaries in Kitty. Keep this plan
and related documentation with the implementation if a commit is requested.
Cursor prompt: Implement or continue this plan using native task titles and the
Kitty-specific i3 rule; preserve shared dirty work/live settings, run refresh-config,
execute the listed checks, and reconcile this plan, README and smoke documentation.

### Deployment and runtime evidence

- refresh-config returned 0, log /tmp/refresh-config-20261005-112135-2191548.log;
  it snapshotted live config, applied chezmoi, regenerated shortcuts and reloaded fish.
- Rendered i3 validation and focused regressions each exit 0. i3 reports existing
  wheel_up_cmd/wheel_down_cmd deprecation messages; no titlebar parse errors.
  The exact i3 Node/CLI pair reports Codex 0.160.0 and mcp list --json exits 0
  without exposing MCP settings or starting inference.
- i3 reload and Kitty-only border update return success:true. All 11 then-open
  Kitty windows report normal borders. Native titles changed through the calling
  task tool; 9/10 other existing titles stayed unchanged across one phase check,
  while another active conversation progressed independently during that interval.
- Showing the previously hidden calling workspace confirmed actual_deco_rect
  1280x30 and a visible live titlebar. The old process retains the project suffix
  until relaunch; corrected README/smoke wording explicitly requires a new process.
- A temporary new Kitty/Codex process resumed only this task with no model prompt.
  Its title was exactly “Review live Codex overviews” after stripping the activity
  glyph: saved name persisted and project suffix was absent. Tabbed layout,
  a 320x30 narrow titlebar and fullscreen return checks passed (exit 0).
  Screenshot fresh-narrow.png visibly shows safe ellipsis. Temporary view closed,
  original desktop focus restored; other conversations were not restarted.
- Live/managed title settings match, alternate_screen remains never, and deployed
  instruction section matches source. The targeted live edit preserved every
  other semantic setting. Kitty configuration itself was not changed.
- Independent read-only review found no critical implementation issue. Its useful
  activation-wording correction is incorporated. Remaining operator acceptance:
  model-driven summaries over future task changes, awaiting-input indicator, and
  real scrollbar/selection/paging gestures. Native self-title, activity rendering,
  persistence and window layout mechanics were tested directly.
- The in-chat approved plan is the design authority. The ExecPlan is the durable
  execution ledger; no additional branch/worktree was created. The later
  commit-session request authorizes a focused commit and upstream push.

### Final verification

- Fresh bash tests/test_st_terminal_workflow.sh: exit 0.
- Fresh bash tests/test_i3_speechnotes_dictation_binding.sh: exit 0.
- Fresh i3 -C -c /home/example/.config/i3/config: exit 0; only the existing
  wheel-command deprecation messages noted above.
- Session-baseline comparison shows only the approved additive i3 rule,
  task-title instruction section and README/smoke additions in shared files.
  Live Codex semantics exactly equal the private pre-task baseline plus the
  terminal_title option; live and managed semantic contents match.
- Postmortem-memory targeted check: exit 0, no errors/new/changed/unregistered
  source aliases. The resolved diagnostic finding has reciprocal source links.
- No implementation or required deployment work remains. Operator acceptance
  scenarios listed above remain documented; they are not represented as tested.

### Session commit scope and checks

- Session: 01a10c8c-4193-7cc2-9517-11b8e0a76cd4; branch main; upstream origin/main.
- session_scope.py returned status unsafe (exit 0): no successful repo-writing
  actions detected. Nested tool orchestration/direct Python writes were not
  attributed by the helper. Use the observed writes and pre-write status/private
  file baselines captured in this conversation; do not infer scope from timestamps.
- README gate ./scripts/executable_readme-recruiter-sync: pass_no_change, exit 0.
  Fresh terminal-workflow and dictation-binding regressions: both exit 0.
- Eligible: Kitty-specific i3 override; native title instruction section; only
  terminal_title/comment against HEAD in skip-worktree Codex config; overview
  README and smoke section; own lesson, inspection postmortem and this ExecPlan.
- A parallel session already committed this task's reviewed incident finding and
  hash/alias in 2b48044. Confirm exact matching HEAD records rather than restaging
  the ledger's unrelated follow-up changes. Include the matching report here.
- Exclude the pre-existing phone-SSH smoke section, aliases, phone guide, unrelated
  incident-memory updates/reports, other plans and benchmark prompt. Current index
  is initially empty; preserve all worktree bytes while staging selected content.
- Review candidate blobs, run candidate i3/config/README and incident checks, and
  inspect the exact staged diff before committing. Commit subject:
  feat: show live Codex task summaries in Kitty. Push once to origin/main.

- Commit-candidate verification: rendered i3 parse exit 0 (existing wheel-command
  deprecations only); native Codex title-option validation exit 0; TOML retains
  inline scrolling; incident targeted check exit 0; README pass_no_change.
  No deployment or scope issue blocks the requested commit/push.
