# Discord embed notification history access

Inspect notification payload shape before deciding how embedded tweet text can reach local speech. This report tracks the restricted history probe and its resolution.

## Symptom and impact

A restricted `dunstctl history` probe reported “Dunst is not running”; the downstream JSON reader then exited1 on empty input. No configuration or notification state changed. Embed availability is not yet established.

## Evidence and current status

The probe requested only SaucyBot payload field names, body length, line count and URL-only classification, without printing message text. Existing direction-isolate incident records the same sandbox D-Bus restriction; daemon absence is not established. Lookup query: `Discord notification speech embed links SaucyBot`; matching local-discord-direction-isolates applies to access diagnostics and title normalization, while local-dunst-overlapping-audio-rules documents the current intentional bot exclusion. The new user request supersedes SaucyBot exclusion.

## Next steps

Repeat a read-only shape probe with desktop D-Bus access. Do not treat a screenshot of an embed as proof that notification bodies contain embed text. Record the outcome and reviewed learning before completion.

## Resolution and verification

Approved desktop D-Bus access returned20 notifications, including two SaucyBot payload shapes. A second content-free probe found one body with91 visible characters, no URL, and both screenshot keywords; the other had133 characters/three lines/one URL. Both probes exited0. No raw notification text was printed or persisted. Root cause is sandbox access, not an absent daemon. Continue using the existing callback body; no external embed retrieval is needed for inspected samples. This is an access workaround, not proof of live speech or universal embed inclusion.

## Learning

The D-Bus boundary is already documented; no new access finding is needed. The private-daemon display-capacity failure yields local-dunst-fixture-display-capacity. Future payloads lacking embed text remain a limitation.

## Private verification environment

The first private-daemon regression launch failed before tests: dbus-daemon could not bind a /tmp session socket (Operation not permitted). This is the known restricted-socket boundary, not a speech regression. Retry only with approved socket access and record its exit status.

## Verification and deployment follow-ups

Focused unit89 and type0 passed. Approved private-daemon run reached the new SaucyBot fixture but expected playback22 and observed21; investigate display queue capacity before retrying. No successful daemon regression claim yet. Required refresh-config exited1 and stopped safely during chezmoi apply; private log /tmp/refresh-config.7pq3KBEv.log. Inspect its exact conflict and reconcile only authorized changes; do not force unrelated live files.

## Diagnostic and bounded remedies

Dunst configuration limits displayed notifications to5. Existing final fixture sequence leaves DM/channel and muted bot popups displayed; the added positive fixture can queue instead of invoking its callback. Drain prior fixture popups before the new block, retaining production suppression and queue behavior unchanged. The refresh log identifies only scripts/audio-mute; exact diff is mode0755 live versus0775 source, with equal timestamps and no content diff. Prior local-refresh-snapshot-ownership guidance supports exact owned deployment. Ran unforced chezmoi apply for scripts/codex-notification-sound only; exit0. Do not modify unrelated permissions. Full refresh remains blocked.

## First-turn evidence and limits

Private-daemon rerun passed1 test, exit0, after draining earlier popups before the new positive fixture. Focused89/broader notification111/type0 passed. Installed source/live bytes match. Installed public callback probes, using real Ryan/Piper/mpv, observed one WAV each for human text with a Markdown link and SaucyBot tweet text, and zero WAV for a URL-only message; zero MP3 throughout, all callbacks exit0, no stderr. No subjective listening or next real incoming tweet acceptance is claimed. Broad refresh remains blocked on unrelated audio-mute mode drift; exact owned unforced deployment succeeded. Preserve unrelated live/source permissions. No commit or push requested.

Ledger validation initially rejected the new finding because diagnostics must be a nonempty list; converted that field from a string without changing its meaning and repeated the targeted check. This is an authoring correction, not a runtime failure or additional learning.

## Latest wording correction

User now requests sender sends tweet/link only, superseding body reading and link-only silence. Defining RED89/54 expected failures observed; parser/docs/tests updated. Required refresh retry again stopped on the same audio-mute conflict, exit1 (/tmp/refresh-config.XtE3pjNb.log); no unrelated overwrite. Exact owned deployment and fresh final checks follow. This is a known bounded refresh conflict, not a new incident.

Final correction verification: focused89, broader111, type0, private Dunst1 pass. Installed parser exact strings and real playback confirmed Alex sends link, SaucyBot sends tweet and URL-only Alex sends link, each WAV1/MP3 0, exit0 with no stderr. No change to queue remedy or access finding. Exact owned helper apply exit0; full refresh remains stopped safely on unrelated mode drift. No additional reusable learning.
