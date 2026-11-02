# Refresh blocked by MIME file permissions

This report explains why refresh stopped and records the scoped repair and verification.

- Symptom: user refresh-config failed; /tmp/refresh-config.RedmTF4S.log reports mimeapps.list changed and EOF at the overwrite prompt.
- Impact: full configuration refresh stopped.
- Lookup: postmortem-memory search "chezmoi refresh local drift conflict" found local-mime-drift-reconcile; applicable prompt mechanism, but this incident is permissions-only.
- Reproducer/evidence: chezmoi diff ~/.config/mimeapps.list reports only old mode 100600/new mode 100664; cmp against dot_config/mimeapps.list exits 0. stat confirms live600/source664.
- Root cause: local mode drift triggers a noninteractive conflict; no association content drift.
- Status: verified fix (runtime).
- Resolution: applied --force only to the byte-identical MIME target; restored mode664 without changing associations. Full refresh then completed without force (exit0; REFRESH COMPLETE, log /tmp/refresh-config.WNeMB59t.log).
- Verification: target diff empty, live mode664, and generated or abbreviation retained.
- Follow-up/limits: desktop applications may reset MIME permissions again; broad conflict protection remains unchanged. No automated code regression test needed for a live permission reconciliation.
