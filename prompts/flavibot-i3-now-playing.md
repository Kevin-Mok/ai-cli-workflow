Fix the i3 now-playing display in /home/example/linux-config so it follows FlaviBot.

Observed:
- FlaviBot’s website shows “Soul Food” by Logic playing.
- The i3 bar shows “Drake - Janice STFU”.
- Expected: “Logic - Soul Food”, updating automatically as tracks change.
- FlaviBot also runs as a Discord app. Its messages show queue additions and link to its website. Queue additions alone do not establish what is currently playing.

Inspect:
- dot_config/i3blocks/scripts/executable_spotify_mpris, which hardcodes Spotify’s MPRIS destination.
- dot_config/i3blocks/i3blocks-4k.conf.tmpl, which polls it every five seconds.
- The active i3 configuration and available live player metadata.

Find the simplest reliable source of FlaviBot’s current-track and playback state. Investigate Chrome/MPRIS and supported FlaviBot interfaces. You may create a companion Discord bot to query or interact with FlaviBot if supported. Verify that bot-to-bot interaction actually works before building around it; do not assume a bot can invoke another app’s slash commands. Do not use a user-token self-bot.

If a companion bot is needed, implement it with minimal permissions, environment-based secrets, reproducible setup, and clear installation instructions. Ask only for indispensable Discord identifiers or setup actions that cannot be discovered. Do not change the queue or interrupt playback merely to obtain metadata.

Prefer actively playing FlaviBot over Spotify, retaining Spotify fallback when FlaviBot is inactive. Preserve the bar’s appearance and safe text escaping. Block clicks must target the displayed player when supported; otherwise disable those actions. Keep global media-key bindings unchanged.

Follow repository instructions, reproduce the mismatch, and test before implementing. Cover track changes, paused/disconnected FlaviBot, simultaneous players, stale or missing metadata, special characters, and Spotify fallback. Update relevant plans, documentation, and smoke tests; run refresh-config after tracked configuration changes.

Deliver the implementation, setup instructions, verification evidence, and any remaining limitations. Distinguish mocked checks from live verification.

Choose an approach based on evidence. Before delivering, identify and fix the result’s single biggest weakness; show only the final result.
