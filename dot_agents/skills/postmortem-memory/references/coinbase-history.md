# Coinbase candle history

Diagnose prematurely shortened Coinbase history by tracing page sizes and backward cursor progress before changing provider limits.

## api-coinbase-short-page-history

**id:** api-coinbase-short-page-history

**reference:** references/coinbase-history.md#api-coinbase-short-page-history

**status:** verified_fix

**symptoms:** Coinbase aggregated intraday charts load only100 candles or stop short of requested history.

**applicability:** Coinbase Exchange historical candle paging where intervals without trades are omitted.

**diagnostics:** Trace requested windows and row counts; verify whether loader stops after a nonempty short page.

**confidence:** confirmed

**remedy:** Continue backward through nonempty short pages. Retain row caps, cursor progress validation, empty-page termination and explicit start bounds.

**verification:** Missing-minute fixture went from100 to1500 aggregated3m bars; direct live trace continued past298 rows and returned1500. Fresh app API returned1500; browser confirmed visible price and PMO time axes.735 root tests and typecheck passed.

**verification_scope:** runtime

**limitations:** No synthetic gap filling or unlimited-history guarantee. Old server processes require restart; concurrent Vite instances can need isolated dependency caches.

**sources:** 47156bee0ad25a2f357d415f21aeda4b8f238de40aa209095a2ec24c31480048

Evidence: /home/example/coding/chartclutch/docs/postmortem/2026-11-01-coinbase-short-history.md
