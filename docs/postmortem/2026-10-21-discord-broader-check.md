# Discord broader notification regression check

Run the broader Codex checks to distinguish Discord regressions from environment and existing fixture failures. Keep unrelated search UI behavior unchanged.

## Symptom and impact

Restricted broader unittest run: 284 tests, four failures, one error, one skip, exit 1. Three actual-CLI search tests could not listen on 127.0.0.1:0. The tmux notification test could not create a session. A directory abbreviation assertion expected /h/k/linux-config but observed /h/e/linux-config. Focused Discord unit tests (75), private Dunst integration (1) and helper type check passed.

## Status and next steps

Socket-bound checks are rerunning through approved socket-capable execution. Inspect the path fixture for baseline placeholder mismatch before attributing it to this change. No search/tmux files changed by this task. Final evidence pending.

## Knowledge lookup

The current task already consulted local-sandbox-loopback-approved-route; appropriate for socket errors before product behavior. A fresh path failure requires baseline comparison, not a Discord parser change. Do not claim broader suite green until final rerun evidence.

## Final broader evidence

Elevated rerun: 284 tests, one failure, no errors/skips. Socket and tmux errors disappear with approved execution. Remaining test_codex_search_recent_picker.py:160 expects /h/k/linux-config for input /home/example/linux-config; current compact_directory correctly returns /h/e/linux-config. Both files are unchanged from HEAD. This is an existing placeholder expectation mismatch; no unrelated fix made. A subsequent helper type check identified HTMLParser.get_starttag_text optional return; handling None with empty text restored zero type errors. Focused unit75, notification subset97, question12, private Dunst1 all pass at this milestone. No whole-suite-green claim.
