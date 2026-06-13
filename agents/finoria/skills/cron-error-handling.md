---
name: cron-error-handling
description: "This skill provides a structured approach to troubleshoot and correct issues arising during cron job"
metadata: { "openclaw": { "emoji": "⭐", "approved_by": "Supreme Fea", "approved_at": "2026-06-11" } }
---
# Cron Error Handling for Notifications

This skill provides a structured approach to troubleshoot and correct issues arising during cron job executions.

## Workflow

- Handle model rejection errors:
  - Check allowed models list.
  - Update cron job model to one from the allowlist.
- Fix Telegram notification delivery issues:
  - Ensure a valid target <chatId> is specified for Telegram deliveries.
  - Test delivery with an appropriate chat ID.
- Document all errors and fixes for future reference.
