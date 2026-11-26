# Vole Spotify continuity check stopped

The first 60-second verification exited before it could confirm continuity. The earlier paired capture measured Spotify at the virtual microphone and silence when paused.

## Evidence and status

- The continuity probe exited 1 at its first assertion that an uncorked Firefox stream played on `spotify_cable`. This interrupted verification. The result alone does not distinguish a pause from a routing change.
- Postmortem lookup for `Spotify Firefox playback stream corked PipeWire continuity assertion` returned the known muted recorder finding. It does not explain a failed Firefox playback assertion. Inspect Firefox's player and PipeWire routes before changing either.
- Firefox's MPRIS player and Spotify Web both showed playback paused at 0:54. PipeWire showed its stream corked and still assigned to the correct sink. Chrome's recording stream was still on the named virtual input. The pause trigger is unknown.
- Spotify was resumed once and the continuity probe was launched immediately. No audio routes were changed during the recovery.
- The follow-up through Firefox's desktop media control passed checkpoints at one and 15 seconds, then stopped at the 30-second checkpoint. Firefox was paused on a different track. The stream remained on the cable.

## Resolution and limits

- Resumed Spotify with the in-page Play button, then restored the previous window. The probe exited 0 with signal in 60 of 60 one-second samples and a minimum peak of 7150. Firefox remained on the cable, Chrome playback remained analog, and active Chrome capture stayed on the named mic at each checkpoint. Spotify reported Playing at the end.
- The pause trigger remains unknown. No general media-control defect or fix was established. If it happens again, check Spotify's playback state and selected playback device before changing PipeWire.
