#!/usr/bin/env bash
# ssh-audit.sh - Detects new failed SSH logins

LOG_FILE="/var/log/auth.log"
STATE_FILE="/home/openclaw/.openclaw/workspace/scripts/ssh-audit.state"

# Check if log file exists and is readable
if [ ! -r "$LOG_FILE" ]; then
    echo "ERROR: Cannot read $LOG_FILE. Check permissions."
    exit 1
fi
LAST_LINE=$(cat "$STATE_FILE" 2>/dev/null || echo 0)
CURRENT_LINES=$(wc -l < "$LOG_FILE")

if [ "$CURRENT_LINES" -lt "$LAST_LINE" ]; then
    # Log rotated, reset
    LAST_LINE=0
fi

# Search for "Failed password" or "Connection closed by authenticating user" (common for bots)
# in the new lines only
NEW_FAILURES=$(sed -n "$((LAST_LINE + 1)),\$p" "$LOG_FILE" | grep -E "Failed password|Connection closed by authenticating user")

if [ -n "$NEW_FAILURES" ]; then
    echo "SECURITY ALERT: New failed SSH login attempts detected:"
    echo "$NEW_FAILURES"
fi

# Update state
echo "$CURRENT_LINES" > "$STATE_FILE"
