# Refresh Config Conflict Parser Failure

- Symptom: The add-and-retry path passed the entire chezmoi prompt line instead of only the target path to `chezmoi add`.
- Impact: Local MIME adoption failed and refresh returned before retrying.
- Evidence: The attempted target included `.config/mimeapps.list has changed since ... EOF`.
- Root cause: The conflict parser removed only a suffix, but chezmoi appends the prompt text and EOF on the same line.
- Resolution: Parse the first whitespace-delimited field from matching conflict lines.
- Verification: Fish syntax, the focused regression, and a live run all pass; `.config/mimeapps.list` was adopted and the retry reached `REFRESH COMPLETE`.
- Follow-up: Keep parser tests grounded in the exact prompt format emitted by chezmoi and review adopted source diffs before committing.
