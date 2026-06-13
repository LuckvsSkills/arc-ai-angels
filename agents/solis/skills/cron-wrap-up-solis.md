---
name: cron-wrap-up-solis
description: "Updates the HARNAS-solis-wrap-up cron job to use an allowed model, resolving a previous execution er"
metadata: { "openclaw": { "emoji": "⭐", "approved_by": "Supreme Fea", "approved_at": "2026-06-11" } }
---
# Update HARNAS-solis-wrap-up cron job model

Updates the HARNAS-solis-wrap-up cron job to use an allowed model, resolving a previous execution error.

## Workflow

- Update the cron job named 'HARNAS-solis-wrap-up' to use the model 'google/gemini-2.5-flash'.
- This resolves the error caused by an disallowed model in the job's payload.
