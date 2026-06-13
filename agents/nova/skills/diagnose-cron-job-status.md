---
name: diagnose-cron-job-status
description: "Check OpenClaw cron job execution status, identify common errors, and provide a clear summary and in"
metadata: { "openclaw": { "emoji": "⭐", "approved_by": "Supreme Fea", "approved_at": "2026-06-11" } }
---
# Diagnose Cron Job Status

Check OpenClaw cron job execution status, identify common errors, and provide a clear summary and initial troubleshooting guidance.

## Workflow

- List all cron jobs: `cron(action='list')`
- Iterate through jobs and extract: `id`, `name`, `enabled`, `lastRunStatus`, `lastDiagnosticSummary`, `nextRunAtMs`.
- Format output clearly, highlighting successful and failed jobs.
- For failed jobs, explicitly mention `lastDiagnosticSummary` (e.g., 'OutboundDeliveryError', 'API rate limit reached').
- Suggest checking the specific adapter or waiting if rate limit is the cause.
