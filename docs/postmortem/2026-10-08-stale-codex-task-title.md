# Stale Codex title from a pasted session report

A conversation working on Second Brain review retained a title about a quoted historical video repair. Inspect native metadata before changing terminal configuration, correct the native task name, and make current-intent title checks explicit.

## Symptom and impact

The user saw `Repair video transition freeze` above a session reporting 59 passing Second Brain session tests. The title misidentified the running task.

## Lookup and evidence

Read the canonical postmortem-memory skill. Searches `kitty stale session title` and `native title current task stale quoted transcript` returned no applicable title-specific remedy; keyboard, attribution and patch findings do not explain this symptom. Inspecting the original user request confirmed that it pasted Second Brain review output starting with a historical video repair. The original rollout's tool-call records contained no `set_thread_title` invocation. Native thread metadata and Kitty remote-control ls both displayed the same stale video title.

## Root cause and resolution

The initial title reflected a task mentioned in pasted output, and the agent omitted the required native title update while performing a different task. This is an instruction-compliance failure. Kitty faithfully displayed the native conversation name. The user-requested native rename to `Verify Second Brain sessions` succeeded, and `kitty @ --to unix:/tmp/kitty-1561320 ls` then showed that exact name with its native activity glyph (exit 0).

## Prevention and current status

The canonical instructions now put title reconciliation near the top and require it on each turn, resume, compaction recovery and before substantive progress updates. They distinguish live intent from quoted historical tasks and require discovery of deferred native title tools. README and the smoke checklist describe the same behavior. Activation and independent review completed; the runtime correction is a verified workaround. Future compliance cannot be guaranteed by a Markdown or config test.

## Verification and follow-up

The original runtime mismatch is the RED reproducer; native correction and observed Kitty propagation are GREEN. Run existing terminal checks, targeted ledger verification and required config activation. The new smoke scenario must be exercised in future new/resumed sessions; do not claim that manual model-driven check has already passed. Keep the plan, incident and related documentation with the instruction change if committed.

## Final verification evidence

- `fish -c refresh-config` printed `REFRESH COMPLETE` and exited 0; log `/tmp/refresh-config-20261008-121817-1596689.log`. It snapshotted live Codex/Git configs, applied managed targets, regenerated shortcuts and reloaded Fish.
- Installed `/home/example/.codex/AGENTS.md` matched the tracked source byte for byte after refresh.
- `bash tests/test_st_terminal_workflow.sh` and `bash tests/test_i3_speechnotes_dictation_binding.sh` each exited 0.
- Targeted incident-ledger check and `git diff --check` exited 0.
- Independent read-only review found no blocking issue. Its fresh-context reasoning probe selected `Improve Second Brain review` and then `Verify Second Brain sessions` for the quoted-video scenario. This is reasoning evidence, not a new/resumed TUI runtime smoke.
- No additional title service or CLI enforcement was added. Future model-driven smoke remains an operator acceptance check; existing processes may need a new process/resume to load the rules.
