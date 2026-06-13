---
name: daily-enki-wrapup
description: "This skill outlines the steps for performing a daily wrap-up for the 'enki' agent. It includes conso"
metadata: { "openclaw": { "emoji": "⭐", "approved_by": "Supreme Fea", "approved_at": "2026-06-11" } }
---
# Perform Daily Enki Wrap-up

This skill outlines the steps for performing a daily wrap-up for the 'enki' agent. It includes consolidating open journal entries, marking completed tasks, and summarizing daily achievements in a memory file. It also specifies to avoid sending Telegram messages as a consolidated overview will be sent by Nova.

## Workflow

- **Consolidate Open Journal Entries:**
  - Locate all open JOURNAL entries.
  - Append their content to `MEMORY.md`.
- **Close Completed Tasks:**
  - Identify tasks marked as complete.
  - Update their status to closed.
- **Record Daily Achievements:**
  - Write a brief summary of actions performed during the day.
  - Append this summary to `MEMORY.md`.
- **Do NOT send Telegram messages.** Nova will handle consolidated overviews.
