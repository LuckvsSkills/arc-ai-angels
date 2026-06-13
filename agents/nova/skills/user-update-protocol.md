---
name: user-update-protocol
description: "Protocol for communicating progress and setting follow-up reminders for tasks that require extended "
metadata: { "openclaw": { "emoji": "⭐", "approved_by": "Supreme Fea", "approved_at": "2026-06-11" } }
---
# User Update Protocol for Long Tasks

Protocol for communicating progress and setting follow-up reminders for tasks that require extended processing time or asynchronous operations. Emphasizes proactive updates, setting cronjobs, and avoiding vague commitments.

## Workflow

- When a task requires significant time or asynchronous processing:
  - Immediately acknowledge the task and set realistic expectations.
  - If more time is needed, explicitly state the estimated delay.
  - Create an internal task/session to track the work.
  - *Crucially, if a delay is expected or a follow-up is required, set a `cron` job to provide a concrete update at a specified time.
  - When scheduling a reminder, write the systemEvent text as something that will read like a reminder when it fires, and mention that it is a reminder depending on the time gap between setting and firing; include recent context in reminder text if appropriate.
  - Avoid vague phrases like "I'll let you know" or "I will get back to you."
  - Provide specific, actionable updates or declare completion.
  - If the user explicitly requests a `cronjob` for follow-up, ensure one is set.
