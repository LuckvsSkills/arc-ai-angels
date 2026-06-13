---
name: daily-wrap-up-cron
description: "Workflow for executing daily wrap-up cron jobs to maintain and consolidate memory."
metadata: { "openclaw": { "emoji": "⭐", "approved_by": "Supreme Fea", "approved_at": "2026-06-11" } }
---
# Daily Wrap-up Cron Job

Workflow for executing daily wrap-up cron jobs to maintain and consolidate memory.

## Workflow

1. Trigger daily wrap-up cron job. 2. Review daily memory files (e.g., `memory/YYYY-MM-DD.md`). 3. Check for new content to consolidate into `MEMORY.md`. If no new content is found, note that no entries were found. 4. Identify and close any open tasks. If none exist, note this as well. 5. Update `MEMORY.md` based on findings from the review.
