# Notification speech internal-thread classification

Independent review found two provenance-classification errors before activation. Reproduce them with focused tests, fix precedence and classification, then verify internal threads remain silent.

- Symptom: differing duplicate metadata for the same identity returned eligible MP3-only before internal provenance was checked. Also worker nickname `review` matched an overbroad regex and suppressed an ordinary spawned agent.
- Impact: internal guardian could sound; ordinary agent could be silent. Speech has not been enabled, so no active user notification impact.
- Lookup: postmortem-memory search `identity metadata precedence reviewer`; existing title/source identity lessons are generally relevant, but no directly verified fix for these branches. Exact RED repro is authoritative.
- Evidence: 35 notification tests ran with exactly two new failing cases: duplicate_internal_metadata_stays_silent and worker_nickname_is_not_internal_provenance.
- Root cause: ambiguity branch preceded internal exclusion; regex serialized all source values, including nickname.
- Resolution: inspect source discriminants and explicit roles only; collect internal provenance before resolving ambiguous metadata. Focused suite now passes all 35 tests; basedpyright --level error reports 0 errors/warnings. Final broader Codex suite passes 135 tests.
- Status: verified_fix at code scope; live activation remains pending manual hook trust.

- Verification: two RED failures became GREEN without changing test expectations. Permission hook trust and live audio acceptance remain manual.

- Follow-up review: actual internal metadata uses source.subagent.other=guardian/session_review; tightened discriminator parser initially omitted `other`. The existing internal-silence test now reproduces this shape and fails RED. Handle this explicit discriminator while continuing to ignore nickname fields.

- Final nested-discriminator verification: guardian/session_review shapes now pass with ordinary nickname case unchanged; focused 35, broader 135, private Dunst and type checks pass. Installed hook remains untrusted pending user /hooks review.
