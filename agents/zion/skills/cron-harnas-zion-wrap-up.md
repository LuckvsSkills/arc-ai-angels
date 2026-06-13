---
name: cron-harnas-zion-wrap-up
description: "Perform daily consolidation of journal entries and update MEMORY.md."
metadata: { "openclaw": { "emoji": "⭐", "approved_by": "Supreme Fea", "approved_at": "2026-06-11" } }
---
# Daily Wrap-up for Zion Cron Job

Perform daily consolidation of journal entries and update MEMORY.md.

## Workflow

1. Check for open JOURNAL entries in the `memory/` directory. 2. If entries exist, consolidate them into `MEMORY.md`. 3. Attempt to close completed TASKS (acknowledge limitations if tools are not available). 4. Append a summary of the day's activities to `MEMORY.md`. 5. Do not send external Telegram messages as per instructions. 6. Ensure Nova collects statuses for a combined overview.
