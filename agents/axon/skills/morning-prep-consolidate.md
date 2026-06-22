---
name: morning-prep-consolidate
description: "Automates the daily morning preparation and consolidation routine for the axon agent. This includes "
metadata: { "openclaw": { "emoji": "⭐", "approved_by": "Supreme Fea", "approved_at": "2026-06-22" } }
---
# Morning Prep and Consolidation Routine

Automates the daily morning preparation and consolidation routine for the axon agent. This includes reviewing memory and tasks, planning the day, updating documentation (MEMORY.md, TASKS.md), and reporting to a lead agent.

## Workflow

- **Trigger:** Scheduled daily.
- **Phase 1: PREP**
  - Review `MEMORY.md` for core learnings.
  - Review `TASKS.md` for active and blocked tasks.
  - Create a mental overview of the day's priorities.
- **Phase 2: CONSOLIDATE**
  - Update `MEMORY.md` with learnings from the previous day.
  - Update `TASKS.md`:
    - Mark completed tasks as `DONE` with a `result_summary`.
    - Update the status of outstanding tasks.
  - Report a concise daily overview to the lead agent.
- **Constraints:**
  - Avoid resource-intensive tools (e.g., firecrawl, exa, perplexity).
  - Ensure the final report to the lead agent is brief.
