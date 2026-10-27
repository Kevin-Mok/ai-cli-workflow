# Toronto dates for media transfers

## Outcome and scope

Select video modification times by the America/Toronto calendar date, regardless of the caller's timezone. Keep the existing SOURCE/DCIM interface, flat rsync behavior, and filenames. Preserve pre-existing dirty files.

## Steps and verification

- [x] Inspect the existing helper and capture Git status.
- [x] Add a real-rsync regression with a UTC caller and Toronto day boundaries; before implementation it exited 1 with no matching media.
- [x] Set the helper timezone and update the design and smoke check.
- [x] Run focused tests and refresh the tracked configuration; record outcomes.

## Risks and review

Selection uses modification time, which may differ from capture time; no filename or embedded metadata parsing is introduced. Toronto daylight-saving rules require system timezone data. Roll back the helper and documentation together if the fixed timezone is unwanted. The actual destination already has files, so verification uses disposable fixtures rather than overwriting concert media.

The boundary regression passed after the change, including a UTC caller and Toronto midnight. The existing shell test assumed the chezmoi source itself was executable, but Git tracks it as mode 100644 and the test invokes it through Bash; its precondition now checks for a file. `refresh-config` exited 0 and the installed helper matches the source. No actual concert files were copied.

Commit milestone `fix: use Toronto dates for media transfers`: both focused shell tests and `git diff --check` passed; the README gate returned `pass_no_change`. The 14 concert videos matched destination sizes and modification times; one was compared byte for byte. Remaining: the other 13 contents were not compared byte for byte.
