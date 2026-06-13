---
name: inter-agent-message-handling
description: "Provides a repeatable procedure for an agent to correctly handle incoming inter-session messages by "
metadata: { "openclaw": { "emoji": "⭐", "approved_by": "Supreme Fea", "approved_at": "2026-06-11" } }
---
# Handle inter-agent messages and route based on recipient

Provides a repeatable procedure for an agent to correctly handle incoming inter-session messages by inspecting the message payload for an intended recipient and acting accordingly.

## Workflow

- When an inter-session message is received, parse its content, typically a JSON payload describing the task and its target agent.
- Check if the message payload contains an 'agent' field or similar explicit recipient identifier.
- If the 'agent' field explicitly names an agent other than the current one, log the message's receipt and acknowledge that the task is not intended for this agent; do not proceed with task execution.
- If the 'agent' field matches the current agent, or is absent/general, proceed to process the task as usual.
