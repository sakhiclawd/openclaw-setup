# HEARTBEAT.md

# Checklist for Sakhi to run periodically:
- [ ] Check `session_status`. If tokens > 700k, perform Deep Compaction automatically and notify Sou after completion.
- [ ] Check logs for "handler failed" or "API limit reached" errors.
- [ ] Check for new research files in `knowledge-base/` and suggest `qmd update`.
