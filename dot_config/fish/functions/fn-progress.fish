function fn-progress
    set -l plain_index (contains -i -- --plain $argv)
    if test -n "$plain_index"
        set -e argv[$plain_index]
        set -fx CLI_PLAIN 1
    end
    set SEASON_START "2026-08-20 00:00:00"
    set SEASON_END "2026-11-01 00:00:00"

    set START_SECONDS (date -d "$SEASON_START" +%s)
    set END_SECONDS (date -d "$SEASON_END" +%s)
    set CURRENT_SECONDS (date +%s)
    set CURRENT_DATE_TIME (date)

    if test "$CURRENT_SECONDS" -lt "$START_SECONDS"
        cli-message 🎯 "Fortnite C7S4 hasn't started yet! (Starts on $SEASON_START)"
        return
    end

    if test "$CURRENT_SECONDS" -ge "$END_SECONDS"
        cli-message 🎉 "Fortnite C7S4 has ended! (Ended on $SEASON_END)"
        return
    end

    set TOTAL_DURATION (math "$END_SECONDS - $START_SECONDS")
    set TIME_PASSED (math "$CURRENT_SECONDS - $START_SECONDS")
    set ELAPSED_DAYS (math -s0 "$TIME_PASSED / 86400")
    set REMAINING_DAYS (math -s0 "($END_SECONDS - $CURRENT_SECONDS) / 86400")
    set PROGRESS_PERCENT (math -s0 "(($TIME_PASSED * 100) + ($TOTAL_DURATION / 2)) / $TOTAL_DURATION")

    cli-message 📅 "Current Date/Time: $CURRENT_DATE_TIME"
    cli-message 🚀 "Season Start: $SEASON_START"
    cli-message 🛑 "Season End: $SEASON_END"
    echo "---"
    cli-message ⏱️ "Days: $ELAPSED_DAYS elapsed, $REMAINING_DAYS remaining"
    cli-message ✅ "Fortnite C7S4 is $PROGRESS_PERCENT% complete!"

    if test (count $argv) -gt 0
        set CURRENT_LEVEL $argv[1]
        set LEVEL_PACE_SECONDS (math "$CURRENT_LEVEL * $TOTAL_DURATION / 200")
        set PACE_DAYS (math -s0 "($LEVEL_PACE_SECONDS - $TIME_PASSED) / 86400")
        set CURRENT_PACE_DAYS (math -s0 "((200 - $CURRENT_LEVEL) * $TIME_PASSED) / $CURRENT_LEVEL / 86400")
        set AVG_LEVELS_PER_DAY (math -s2 "$CURRENT_LEVEL * 86400 / $TIME_PASSED")

        if test "$PACE_DAYS" -ge 0
            cli-message 🎮 "Level $CURRENT_LEVEL is $PACE_DAYS days ahead of level 200 pace."
        else
            cli-message 🎮 "Level $CURRENT_LEVEL is "(math "-$PACE_DAYS")" days behind level 200 pace."
        end

        cli-message 📊 "Average pace: $AVG_LEVELS_PER_DAY levels/day."
        cli-message 📈 "At current pace, $CURRENT_PACE_DAYS days left to reach level 200."
    end

    echo "---"
end
