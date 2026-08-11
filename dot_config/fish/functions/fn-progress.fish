function fn-progress
    # --- Season Dates (Fortnite Chapter 7 Season 3) ---
    set SEASON_START "2026-06-06 00:00:00"
    set SEASON_END "2026-08-19 00:00:00"

    # --- Calculate Unix Timestamps ---
    set START_SECONDS (date -d "$SEASON_START" +%s)
    set END_SECONDS (date -d "$SEASON_END" +%s)
    set CURRENT_SECONDS (date +%s)
    set CURRENT_DATE_TIME (date)

    # --- Check if the season is over or hasn't started ---
    if test "$CURRENT_SECONDS" -lt "$START_SECONDS"
        echo "🎯 Fortnite C7S3 hasn't started yet! (Starts on $SEASON_START)"
        return
    end

    if test "$CURRENT_SECONDS" -ge "$END_SECONDS"
        echo "🎉 Fortnite C7S3 has ended! (Ended on $SEASON_END)"
        return
    end

    # --- Calculate Progress ---
    set TOTAL_DURATION (math "$END_SECONDS - $START_SECONDS")
    set TIME_PASSED (math "$CURRENT_SECONDS - $START_SECONDS")

    # --- Calculate whole-day progress and a nearest whole percentage ---
    set ELAPSED_DAYS (math -s0 "$TIME_PASSED / 86400")
    set REMAINING_DAYS (math -s0 "($END_SECONDS - $CURRENT_SECONDS) / 86400")
    set PROGRESS_PERCENT (echo "scale=0; (($TIME_PASSED * 100) + ($TOTAL_DURATION / 2)) / $TOTAL_DURATION" | bc)

    # --- Output Result ---
    echo "📅 Current Date/Time: $CURRENT_DATE_TIME"
    echo "🚀 Season Start: $SEASON_START"
    echo "🛑 Season End: $SEASON_END"
    echo "---"
    echo "⏱️ Days: $ELAPSED_DAYS elapsed, $REMAINING_DAYS remaining"
    echo "✅ Fortnite C7S3 is **$PROGRESS_PERCENT%** complete!"
    echo "---"
end
