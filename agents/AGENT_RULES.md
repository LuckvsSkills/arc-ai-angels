# ARC AI ANGELS — Agent Governance Rules

## Purpose

This file defines the canonical operating rules for all active ARC AI ANGELS agents.

It applies to:
- Nova
- Flux
- Omni Leads
- Sentinels
- Workers when added to runtime execution

The purpose is to ensure that every agent behaves predictably, respects hierarchy, uses the correct files, and does not lose continuity across sessions.

---

## Source of Truth

Each agent operates from these local files:

- `IDENTITY.md` — who the agent is
- `README.md` — local governance contract
- `TASKS.md` — actionable obligations
- `JOURNAL/` — operational continuity and event history
- `MEMORY.md` — durable reusable knowledge
- `HANDOFF.md` — transfer and collaboration rules
- `TASK_HISTORY.md` — completed task history when present

Priority order:

1. Canon
2. AGENT_RULES.md
3. Agent README.md
4. IDENTITY.md
5. TASKS.md
6. HANDOFF.md
7. MEMORY.md
8. JOURNAL/

---

## Core Rule

Agents must never rely on chat memory for operational obligations.

If something must happen later, it must become a task.

If something happened, it must be journaled.

If something should be remembered long term, it must be promoted to memory.

---

## Task Rules

`TASKS.md` is the authoritative source for active work.

An agent may act only on tasks where:

- `owner` matches the agent identity
- `status` is `scheduled` or `active`
- `next_action` is clear

Allowed task states:

- `scheduled`
- `active`
- `waiting`
- `blocked`
- `done`
- `canceled`
- `escalated`

A task is incomplete until its status is explicitly changed.

---

## Scheduled Task Rule

Any time-based promise must be recorded in `TASKS.md`.

Examples:

- “come back in 5 minutes”
- “check this later”
- “retry tomorrow”
- “follow up after validation”
- “wait and respond when ready”

These must include:

- `task_id`
- `owner`
- `status`
- `execute_at`
- `next_action`
- `retry_count`
- `max_retries`
- `escalate_after`

No time-based commitment may exist only in chat, memory, or journal.

---

## Journal Rules

`JOURNAL/` stores operational continuity.

Agents must write journal entries for:

- task activation
- task completion
- execution failure
- retry decision
- escalation
- handoff-relevant context
- important interpretation or decision

Agents must not use journal as:

- raw log dump
- task list
- permanent memory
- duplicate transcript archive

Required journal lifecycle:

```text
JOURNAL/
  README.md
  INDEX.md
  open/
  closed/
  archived/

