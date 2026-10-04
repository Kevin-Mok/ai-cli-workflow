# Runtime RED test unintentionally used the official transport

- Date: 2026-10-03.
- Symptom: a new RED test for the reasoning-effort guard instantiated the proxy
  without injecting a fake upstream. Since that guard was not yet implemented,
  an unauthenticated POST reached the official Codex responses route and returned
  HTTP 401 instead of the expected local 403.
- Impact: one unintended unauthenticated network request, conservatively reserved
  against the user's 50-request cap; 49 requests remain for benchmark execution.
  No credentials were supplied, read, or logged. Observed evidence is HTTP401
  and no model output; server-side execution/billing is not independently known.
  No installed configuration change occurred. Benchmark trials remain unstarted.
- Evidence: the defining test failed `401 != 403`; its HTTP request contained
  only a synthetic model/tools/reasoning payload and no authorization header.
- Root cause: a safety-boundary test relied on the as-yet absent guard to prevent
  real network access instead of injecting a fake transport unconditionally.
- Resolution: inject a fake upstream in every proxy test, including cases
  expected to reject locally. Add a suite-level prohibition on the real upstream.
- Verification: corrected fake-only RED returned 200 versus the expected403,
  demonstrating the missing guard without network; subsequent guard tests pass
  with the real upstream prohibited for the complete suite.
- Follow-up: boundary tests must remain incapable of public network access even
  when the feature under test is absent or regresses.
