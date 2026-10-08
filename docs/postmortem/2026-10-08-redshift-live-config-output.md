# i3 live-config output parsing

The Redshift live verification parsed human-readable output as JSON. Request raw IPC JSON explicitly before decoding.

## Symptom and impact

After refresh-config and successful reload, `json.loads` on `i3-msg -t get_config` raised JSONDecodeError. The installed config mapping already passed; this failed diagnostic did not modify bindings.

## Lookup and status

The canonical postmortem-memory skill applies. Searched `JSONDecodeError output contract`; reviewed matches about CLI/output contracts apply to explicit output selection. Root cause: the diagnostic assumed JSON output without requesting raw mode. Retry with `i3-msg -r -t get_config`; verification passed: raw IPC JSON parsed successfully and all ten running bindings matched, exit 0. No new reusable learning beyond existing output-contract guidance.
