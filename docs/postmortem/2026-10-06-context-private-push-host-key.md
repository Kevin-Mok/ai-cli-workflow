# Private repository push host identity mismatch

Preserve the completed local knowledge commit when SSH cannot verify the configured Git server. Verify the server identity independently before changing trust or retrying delivery.

## Symptom and impact

The explicitly authorized private repository push exited 128: REMOTE HOST IDENTIFICATION HAS CHANGED for git.example-user-mok.com; strict checking rejected its ED25519 key. Known-hosts entry 49 conflicts. Local commit f327d0c remains intact; no private payload was pushed. Linux-config implementation commit fcc62d9 pushed successfully to origin/main.

## Lookup and evidence

postmortem-memory search "SSH host identification changed strict host key verification" returned local-endpoint-empty-probe-handling (verified_fix, runtime): compare fingerprints at the intended endpoint. This supports preserving identity verification; it does not establish trust in the newly presented key. Server console or another independently trusted channel is required.

## Status and next steps

Unresolved external identity mismatch. Presented ED25519 fingerprint: SHA256:jBy4AUXSoa07mqkXB7fzUbpIMh9IU3cwpC3Nj2GWyu0. No known-hosts edits, deletion, strict-check bypass or retry performed. Verify the server's key independently, update trust only if confirmed, then push origin/main from the private repository. Underlying cause may be legitimate key rotation or a wrong endpoint; neither is established.
