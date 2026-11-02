# Backup cache suite failures

Track unrelated backup fixture failures observed while verifying Snap cache exclusions; no real backups or disks were modified.

## Symptoms and impact

2026-10-31: sandbox backup suite ran 69 tests with two failures and one error: ACL setfacl invalid argument in tar roundtrip; dynamic mount-name exclusion fixture expects alice while passing example; PTY progress missing expected output. Focused new cache behavior passes. Follow-up host test showed ACL roundtrip passes and dynamic fixture still fails; the PTY targeted invocation used an incorrect import path and failed before the test ran.

## Lookup and investigation

Postmortem-memory query: setfacl Invalid argument sandbox rsync mounted disk tty. Broad token matches were unrelated to ACL/PTY behavior; known backup findings concern vanished files and swap aliases. Sandbox-specific ACL limitation supported by successful host fixture. Dynamic fixture passes ./home/example/mounted [disk] but asserts exclusion of alice/mounted [disk], an apparent pre-existing fixture inconsistency; verify against HEAD before attributing. PTY failure needs host run with correct test discovery/import path.

## Status

Investigating; preserve failures and avoid changing unrelated fixtures. Next run clean baseline and host suite where possible, record exact results. No recovery or user data touched.

Host suite confirmed only the pre-existing dynamic fixture failed:68passed/1failed, ACL and PTY passed. HEAD proves fixture inconsistency predates this change. Corrected fixture path to alice so it exercises the intended literal mount exclusion; no production assertion relaxed. Pending fresh host suite.

## Resolution and verification

The only host-suite failure was an existing test fixture mismatch: HEAD used ./home/example/mounted [disk] while creating and asserting alice/mounted [disk]. Corrected the fixture to alice, preserving its assertion and the production exclusion logic. Fresh unsandboxed backup suite: 69 tests passed. ACL and PTY failures from the sandbox did not recur on host; no host-wide backup was performed. The test invocation import error was a diagnostic command mistake, not a product defect.

Review: no new reusable finding; a literal fixture typo and sandbox-specific test behavior do not establish a broader remedy. This report is registered with its reviewed hash. Preserved unrelated dirty postmortem-memory work.
