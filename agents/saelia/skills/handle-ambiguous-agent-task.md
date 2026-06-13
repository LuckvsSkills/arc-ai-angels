---
name: handle-ambiguous-agent-task
description: "When an inter-agent message requests a system-specific task without providing detailed steps, this s"
metadata: { "openclaw": { "emoji": "⭐", "approved_by": "Supreme Fea", "approved_at": "2026-06-11" } }
---
# Handle ambiguous inter-agent task requests

When an inter-agent message requests a system-specific task without providing detailed steps, this skill outlines how to search for context and escalate if necessary.

## Workflow

When receiving an inter-agent message requesting a named system task (e.g., 'HARNAS prep') without specific execution steps:
- Perform `memory_search` using the task name as the query to find any existing context or past instructions.
- If relevant context is found, use it to infer next steps or formulate a clarifying question.
- If no clear instructions or sufficient context are found:
    - Acknowledge the task request.
    - State that specific instructions for the task are missing.
    - Request clarification from the originating agent or confirm escalation to a defined lead/omnilead if the originating agent indicates they are escalating.
    - Await further instructions.
