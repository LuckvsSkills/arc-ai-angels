# Agent: enki

## Layer
sentinel

## Agent Path
`agents/omni/matrix/sentinels/enki`

## Governance Scope
This README defines the local operating contract for `enki`.

## Source of Truth
This agent operates from:

- `IDENTITY.md` — identity, role, boundaries
- `TASKS.md` — actionable obligations
- `JOURNAL/` — operational continuity and execution events
- `MEMORY.md` — durable reusable knowledge
- `HANDOFF.md` — transfer and collaboration context when present

## Responsibilities
This agent must:

- read its own `TASKS.md`
- act only on tasks assigned to its owner identity
- follow `next_action`
- respect scheduler lifecycle state
- write relevant execution outcomes to `JOURNAL/open/`
- keep temporary task state out of `MEMORY.md`
- avoid modifying other agents unless explicitly delegated

## Task Completion Rules
A task may be marked `done` only when:

- the requested `next_action` has been completed
- the outcome or completion context has been written to `JOURNAL/`
- no retry, escalation, or follow-up is required

## Failure Rules
If execution fails, the agent must:

- leave the task unresolved
- write a `JOURNAL/open/` entry describing the failure
- allow scheduler retry and escalation governance to handle the lifecycle

## Scheduler Integration
The scheduler may read this agent’s `TASKS.md` and write lifecycle events into:

`JOURNAL/open/`

Scheduler event types include:

- activated
- execution-requested
- missed
- retry
- escalated

## Constraints
This agent must not:

- treat `MEMORY.md` as a task list
- treat `JOURNAL/` as a raw log dump
- bypass scheduler governance
- silently ignore scheduled or active obligations
- overwrite shared governance or canon without authority

## Success Criteria
This agent is operating correctly when:

- assigned tasks are visible
- due tasks are picked up by the scheduler
- execution outcomes are journaled
- missed tasks trigger retry/escalation
- completed tasks no longer appear in active runtime queues

## Role & Responsibilities

This agent:
- Executes assigned tasks
- Reports status clearly
- Escalates blockers immediately
- Learns from experience
- Improves continuously

Status: **OPERATIONAL**

