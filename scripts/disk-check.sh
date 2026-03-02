#!/usr/bin/env bash
# disk-check.sh - Alerts if disk usage > 90%

THRESHOLD=90
# Check root partition usage
USAGE=$(df / | grep / | awk '{ print $5 }' | sed 's/%//g')

if [ "$USAGE" -gt "$THRESHOLD" ]; then
  echo "CRITICAL: Disk usage on / is at ${USAGE}%!"
else
  echo "OK: Disk usage is at ${USAGE}%."
fi
