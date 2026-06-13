# HANDOFF.md — Agent Communication Protocol
## How we brief each other

---

## VOOR NOVA

### Handoff TO Flux
INTAKE COMPLETE → ROUTING NEEDED
Sender: Nova (Gateway)
Recipient: Flux (Orchestrator)
Type: Task routing request
What Nova sends

Input normalized ✓
Security checked ✓
Intent identified ✓
Domain(s) suggested (if known)
Priority/urgency level
Any constraints/dependencies
Full context for routing decision

What Nova needs back

Which Omni/Domain confirmed
Which Lead Agent selected
Routing chain confirmed
Task ID for tracing


### Handoff FROM Flux
ROUTING COMPLETE → EXECUTION STARTING
Sender: Flux (Orchestrator)
Recipient: Relevant Lead Agent(s)
Type: Task dispatch
What Flux sends

Task details (normalized)
Domain routing confirmed
Lead Agent assigned
Any cross-domain dependencies
Constraints & boundaries
Task ID for tracing
Expected timeline


---

## VOOR LEADS (Cortexia, Saelia, Finoria, Lumeria, Fluentia)

### Handoff TO Sentinels
TASK RECEIVED → SENTINEL DISPATCH
Sender: Lead Agent
Recipient: Selected Sentinels
Type: Work assignment
What Lead sends

Task breakdown
Which Sentinels assigned (and why)
Dependencies between Sentinels
Quality standards expected
Timeline/urgency
Escalation triggers

What Lead needs back

Task acknowledgment
Blocker identification
Progress updates
Quality validation ready


### Handoff TO Flux
EXECUTION COMPLETE → AGGREGATION
Sender: Lead Agent
Recipient: Flux
Type: Task completion report
What Lead sends

Task completion status
Results from all Sentinels
Any issues encountered
Quality validation passed
Output ready for next phase
Timeline performance


---

## VOOR SENTINELS

### Handoff TO Lead
WORK COMPLETE → VALIDATION
Sender: Sentinel
Recipient: Their Lead Agent
Type: Work completion
What Sentinel sends

Task completed/incomplete status
Output quality metrics
Any blockers encountered
Recommendations
Timeline performance
Escalation if needed


---

