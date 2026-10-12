# Imported upstream whitespace check warning

The staged whitespace check found eight pre-existing whitespace-only lines in the imported package. Preserve upstream bytes for this import and report the warning; offline functionality and integrity checks pass.

## Symptom and impact

During commit-session, git diff --cached --check reported trailing whitespace at providers.py lines 489, 501, 515 and watchlist.py lines 30, 33, 60, 249, 252. No runtime failure or credential exposure was observed. Earlier unstaged checks did not cover untracked imported files.

## Lookup and decision

Searched tracked postmortem-memory for imported upstream trailing whitespace diff check. No exact prior finding was established. Every original imported file has a matching SHA-256 against the installed original and rendered chezmoi source. The whitespace is upstream content, so avoid a package rewrite in this copy-only task. The commit-session skill explicitly treats ordinary validation failures as warnings and continues eligible work.

## Verification and status

Known warning retained. Installed CLI help, 158 original-file byte comparisons, executable-status checks, README gate and targeted incident coverage pass. There is no whitespace-fix claim; an upstream cleanup can be a separate task.

## Learning

No new reusable learning: check staged imported files rather than claiming an unstaged check covers untracked package content. Existing completion policy requires final staged evidence and accurate reporting.
