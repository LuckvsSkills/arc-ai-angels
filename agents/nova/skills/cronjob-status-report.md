---
name: cronjob-status-report
description: "Fetches and summarizes the status of OpenClaw cronjobs, including success/failure, last run details,"
metadata: { "openclaw": { "emoji": "⭐", "approved_by": "Supreme Fea", "approved_at": "2026-06-11" } }
---
# Report OpenClaw Cronjob Status

Fetches and summarizes the status of OpenClaw cronjobs, including success/failure, last run details, next scheduled run, and error diagnostics.

## Workflow

- List all cron jobs using `cron(action='list')`.
- For each job, extract and present:
    - `name`
    - `lastRunStatus` (e.g., "ok", "error")
    - `nextRunAtMs` (convert to human-readable date/time, specify UTC if applicable)
    - `lastDiagnosticSummary` or `lastErrorReason` if `lastRunStatus` is "error".
- Format the information clearly, highlighting any issues.
- Example output format:
    ```
    **[Job Name]:**
    * Laatste run: [Status] ([Error details if any])
    * Volgende run: [Next Run Time]
    ```
