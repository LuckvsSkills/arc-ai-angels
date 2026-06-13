---
name: proactive-task-updates
description: "Guides the agent on how to manage user expectations for tasks, especially those that might take long"
metadata: { "openclaw": { "emoji": "⭐", "approved_by": "Supreme Fea", "approved_at": "2026-06-11" } }
---
# Proactive Task Management and Communication

Guides the agent on how to manage user expectations for tasks, especially those that might take longer, by setting explicit tasks, scheduling reminders (cronjobs), and providing concrete updates instead of vague assurances.

## Workflow

- When a task might take longer than a single turn or requires background processing:
  - Immediately inform the user about the current status and expected duration or next update time.
  - If more time is needed, explicitly communicate this.
  - Create an internal task or use `sessions_spawn` for long-running processes.
  - Set a `cron` job to remind yourself to provide an update at a specific interval or time.
  - Provide concrete feedback and specific timelines, avoiding vague phrases like 'I'll let you know' or 'I'll get back to you.'
  - If the user explicitly requests a task/cronjob for follow-up, *always* do it.
- When a user expresses frustration about a lack of updates:
  - Acknowledge their frustration and apologize sincerely.
  - Take full responsibility for the communication failure.
  - Explain the current status transparently.
  - Immediately correct the communication lapse by providing a concrete plan for the next update or action.
  - Prioritize setting up a `cron` job or reminder for subsequent updates.
