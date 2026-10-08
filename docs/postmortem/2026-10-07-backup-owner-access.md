# Backup artifacts unreadable by invoking user

Explain root-owned backup access and fix ownership without changing copied-home restoration metadata.

## Symptom, impact and lookup

Listing/tailing the latest bundle as example-user failed with Permission denied. Sudo read attempts reported a password is required. The bundle is root-owned mode 700; archive/log mode 600 are also root-owned. No writes occurred in those attempts. Search `backup permissions owner root sudo` matched ext-container-host-ownership (unresolved): explicit host UID and narrow ownership scope apply, but its remedy is not verified for this case. A piped lookup hit BrokenPipeError when head closed; use bounded JSON rendering rather than head. A nonexistent optional access-helper search returned no match. Independent source review confirms archive creation/inspection precedes failed home copying.

## Cause and plan

Backup creates private files as root and never assigns the invoking sudo account. Add account-based ownership for known generated files, keep copied-home metadata unchanged, and provide a scoped authenticated repair. Resolution implemented: resolve invoking sudo account through pwd, assign only generated regular artifacts and bundle directory, skip symlinks and preserve copied-home ownership/modes/ACLs. `backup-pc access --bundle PATH --user example-user` repairs existing bundle access after local sudo authentication. Ownership is applied at startup, after archive creation, before publication and in failure cleanup.

## Verification and remaining limits

Defining tests observed RED with missing ownership helper/account lookup. python3 -B -m unittest discover -s tests -p 'test_backup_pc*.py' passed all 62 tests (exit 0), covering generated file scope, skipped symlinks, interrupted archive cleanup and completed publication. bash -n, installed access --help, cmp of repository/installed script, and git diff --check each passed (exit 0). fish -c refresh-config completed with REFRESH COMPLETE (exit 0). The prior read-only source review establishes root/EFI checks passed before home failure; no fresh read of the real archive or restored boot was performed. Existing bundle access repair remains blocked by local sudo authentication; no password requested. Inspection failures changed no backup data. An independent read search also used a nonexistent optional glob; correcting the scoped source path succeeded, with no new engineering learning beyond path checks.
