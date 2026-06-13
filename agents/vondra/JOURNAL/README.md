# JOURNAL Governance

## Purpose
This JOURNAL stores operational continuity records for this agent.

It captures:
- scheduled task lifecycle events
- handoff-relevant continuity
- decision context
- missed, retry, and escalation events
- temporary execution context that should survive a session

## This JOURNAL is not
- a permanent memory store
- a task board
- a raw log dump
- a replacement for TASKS.md
- a replacement for MEMORY.md

## Structure
- open/: active or unresolved continuity entries
- closed/: resolved entries with short-term reference value
- archived/: historical entries retained for audit

## Rules
- Time-bound obligations belong in TASKS.md.
- Durable knowledge belongs in MEMORY.md.
- Operational continuity belongs in JOURNAL.
- Scheduler events are written by system_process.
- Entries may be closed only when the related task is done, canceled, or escalated.
