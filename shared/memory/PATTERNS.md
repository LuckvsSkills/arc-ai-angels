# PATTERNS.md

## Recurring System Patterns

### Pattern 1: Input Validation
- Trigger: External input arrives
- Action: Nova validates and sanitizes
- Result: Safe structured request to Flux
- Frequency: Every session

### Pattern 2: Memory Consolidation
- Trigger: Daily cronjob (24h)
- Action: JOURNAL/open → MEMORY.md
- Result: Agent learns from experience
- Frequency: Daily per agent

### Pattern 3: Cross-Domain Requests
- Trigger: Task spans multiple domains
- Action: Flux orchestrates Sentinels
- Result: Coordinated multi-domain response
- Frequency: As needed

### Pattern 4: Escalation
- Trigger: Worker exceeds scope
- Action: Escalate to Lead Agent → Flux
- Result: Task rerouted or rejected
- Frequency: When boundaries exceeded
