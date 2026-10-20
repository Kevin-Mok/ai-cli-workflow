# Description evidence excerpt missing after redaction

A pre-write evidence check rejected one missing source excerpt. Preserve safe evidence lines separately when removing credential-bearing research content, then rerun the full quote comparison before changing metadata.

- Symptom/evidence: independent source-quote validation found 1 missing excerpt among 213 entries and exited 1 before producing the reviewed write manifest.
- Impact: no remote writes occurred; all other source quotes matched.
- Lookup/applicability: the already-read postmortem-memory boundary and artifact-verification guidance requires actual supporting evidence, not an agent assurance; this was a local artifact omission rather than API failure.
- Root cause: full Spotify settings were deliberately removed from temporary research to exclude a committed development secret, but its safe PostgreSQL engine line had not been retained independently.
- Resolution: researcher saved only the safe engine-line excerpt with the exact commit and path; full credential-bearing content remains excluded.
- Verification: `python3 /tmp/recruiter_review.py` exited 0; 52 repositories, 218 evidence entries, zero missing/mismatched quoted excerpts, maximum changed description length 179.
- Status: resolved before remote writes. Subsequent 45 description-only updates and final 52/52 exact readbacks passed; no outstanding action.
- Learning decision: no new reusable finding; retain safe evidence during redaction and let independent pre-write validation block unsupported publication.
