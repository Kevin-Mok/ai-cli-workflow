Implement a Redshift temperature control block on my main 4K screen’s i3bar in /home/kevin/linux-config.

Behavior
- Place the block only on the dedicated DP-2 4K bar.
- Use the same Redshift controller and display scope as the existing Windows+2 preset shortcut.
- Show a compact thermometer icon and temperature, such as “🌡️ 4500 K”, matching the existing bar styling.
- Scroll up (BLOCK_BUTTON=4) increases temperature by 250 K; scroll down (5) decreases it by 250 K. Higher values are cooler; lower values are warmer.
- Apply each adjustment immediately and refresh the displayed value without reloading i3.
- Retain the controller’s 1000–6500 K limits and default of 6500 K when no saved state exists.
- Refresh at least once per second so existing keyboard presets, adjustments and reset are reflected too.

Implementation
- Follow the repository’s AGENTS.md instructions.
- Reuse scripts/executable_redshift-control, which already owns adjustment, locking, saved state and backend error handling. Add a read-only status action for the block; it must not apply Redshift, send notifications or create state.
- Add a small block script under dot_config/i3blocks/scripts/ and register it in dot_config/i3blocks/i3blocks-4k.conf.tmpl, between volume and Spotify.
- Handle wheel adjustments through the shared controller. Preserve correct accumulated changes during rapid scrolling. Other mouse buttons must not alter temperature.
- Keep stdout valid for i3blocks. Show a compact error on backend or malformed-state failures; never report an unsuccessful target as applied.
- Update dot_config/i3blocks/scripts/executable_4k_status so every layout fallback accounts for the new block’s width. Preserve volume and Redshift visibility before Spotify and calendar when space is tight.
- Display the controller’s saved manual target; do not claim it measures hardware temperature or tracks raw external Redshift commands.
- Preserve existing persistence and keyboard behavior. The screenshot illustrates temperature control; no separate GUI or automatic day/night scheduling is requested.

Verification
- Write defining tests first and observe RED.
- Test read-only status, both wheel directions, bounds, rapid adjustments, keyboard-to-block synchronization, invalid state and backend failure.
- Extend the existing Redshift and 4K bar tests, including scheduler fixtures and crowded-bar layout cases.
- Update the relevant documentation and docs/smoke-tests.md. Run refresh-config as required, then verify the actual running bar, scrolling and existing Windows+2 shortcut together.
- Report observed results and any display-session checks that could not run.
