# HANDOFF.md

## Agent Handoff Protocol & Knowledge Transfer

### Purpose
Defines the process for handing off tasks, knowledge transfer, and coordination between agents.

### Handoff Types
1. **Task Handoff** - Passing incomplete tasks to another agent
2. **Knowledge Transfer** - Sharing learned information and insights
3. **State Transfer** - Passing current execution context
4. **Authority Handoff** - Delegating decision-making authority

### Handoff Checklist
- [ ] Task status documented
- [ ] Context provided
- [ ] Resources transferred
- [ ] Confirmation received
- [ ] History updated

### Communication Protocol
- Use AGENTS.md for agent registry
- Reference IDENTITY.md for agent capabilities
- Document in TASK_HISTORY.md
- Maintain MEMORY.md state

### Handoff Format
FROM: [Agent Name]
TO: [Recipient Agent]
TASK_ID: [Task Identifier]
STATUS: [Current Status]
CONTEXT: [Relevant Details]
DEADLINE: [If Applicable]
### Follow-up
- Confirm receipt within 1 hour
- Report progress to originating agent
- Document lessons learned
- Update shared memory

### Dependencies
- AGENTS.md (agent directory)
- IDENTITY.md (capabilities)
- MEMORY.md (state management)
- TASK_HISTORY.md (execution log)

---
*Last updated: 2026-05-17*
*Handoff Protocol version: 1.0*

