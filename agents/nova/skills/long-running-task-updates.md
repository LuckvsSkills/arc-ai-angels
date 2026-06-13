---
name: long-running-task-updates
description: "Provides a repeatable workflow for managing user expectations and providing structured updates for t"
metadata: { "openclaw": { "emoji": "⭐", "approved_by": "Supreme Fea", "approved_at": "2026-06-11" } }
---
# Manage Long-Running Task Updates with Cron

Provides a repeatable workflow for managing user expectations and providing structured updates for tasks that require more time, using cronjobs for proactive communication.

## Workflow

- When a task requires more than immediate completion, inform the user that it will take time.
- Do not simply state "I'll let you know."
- Instead, set a cronjob (e.g., for 5-10 minutes, adjust as needed) to check task progress and provide a concrete update.
- Clearly state what specific action is being taken and what the user can expect (e.g., "I'm performing a deep search," "I've set a cronjob for 5 minutes to update you on the search results.").
- Confirm the current status of the task when providing the update.
