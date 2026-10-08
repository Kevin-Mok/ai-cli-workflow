# Codex permission-request audio flood

Stop title announcements during ordinary work by sounding only for completed turns. Preserve the selected MP3 and desktop popups, deploy the corrected event policy, and clear queued speech workers.

## Symptom and impact

User repeatedly heard “Create fish alias skill” while the task was still working. Speech was enabled. The deployed PermissionRequest hook resolves the conversation title and launches the same audio worker as completions for every request, including automatic review.

## Lookup and evidence

Postmortem-memory query: `notification permission repeated during work`; returned authorization/cache lifecycle findings were not direct matches. Reviewed notification provenance guidance: its identity checks apply, but do not distinguish task completion from permission requests. Independent investigation found two active exact-title top-level user threads with zero task_complete events and 23/17 require_escalated custom-tool payloads. Seven owned event-play workers were queued; oldest was synthesizing, six waited without children.

## Root cause and resolution plan

The initial plan explicitly included automatic permission audio. That event policy is too noisy under frequent reviewed escalations, and serialized playback accumulates stale announcements. This is an event-selection problem, not incorrect title identity. New user intent overrides the original permission-audio requirement: speak only completion events. Keep existing loaded permission-hook calls silent through the bridge, remove the configured permission hook, clear only owned detached audio process groups, and preserve speech activation after deployment.

## Status and verification

Verified fix and live activation: defining 37-test suite failed only its permission-no-spawn case, then passed after the gate. Final broader Codex suite passes 138 tests (30.829s, exit 0). Helpers type-check with zero errors/warnings. Private Dunst regression passes, README gate pass_no_change and diff check clean. refresh-config completed and chezmoi verify confirms deployment. Restored previously enabled speech. Ten actual deployed PermissionRequest calls exit 0 with no output and create no workers; live queue count is zero. Five still-queued owned audio groups were terminated after disabling new delivery; no Codex processes touched. Completion title capture before queueing remains verified with a real detached bridge subprocess. Subjective future completion playback remains covered by shared smoke checks.

## Follow-up and rollback

Record the durable completion-notification preference separately from queue-lifecycle engineering guidance. On future notification event-policy changes, stop enqueueing before clearing obsolete owned audio workers; restoring settings alone does not drain serialized stale titles. `speech disable` remains immediate rollback to existing popup MP3 behavior. No commit requested; preserve related plan/docs/incident changes together in any later commit.
