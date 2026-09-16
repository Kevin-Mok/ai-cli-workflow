#!/usr/bin/env bash

# Find all audio sink inputs belonging to mGBA (case-insensitive search)
INPUT_IDS=$(pactl list sink-inputs | awk '
  /Sink Input #/ { id=$3; sub("#", "", id) }
  /application.name/ && /[mM][gG][bB][aA]/ { print id }
')

if [ -z "$INPUT_IDS" ]; then
  notify-send -u low "mGBA Mute" "mGBA audio stream not found."
  exit 1
fi

# Toggle mute status for each mGBA audio stream
for ID in $INPUT_IDS; do
  pactl set-sink-input-mute "$ID" toggle
done
