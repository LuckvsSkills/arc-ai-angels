# GOVERNANCE.md

## Shared Memory Governance

### Access Rules
- All agents can READ shared_learning/
- All agents can WRITE own learning entries
- Flux ORCHESTRATES cross-domain consolidation
- No agent modifies another agent's MEMORY

### Update Frequency
- SYSTEM_STATE: Daily (when cronjobs run)
- CROSS_LEARNING: Weekly (pattern analysis)
- PATTERNS: Monthly (system analysis)
- DECISIONS: As needed (governance changes)

### Audit Trail
- All writes timestamped
- All changes logged in shared/logs/
- Reversible (backup kept 7 days)

### Escalation
- Memory conflicts: Resolved by Flux
- Cross-domain disputes: Via Mission Control
- System integrity: Automatic validation

## Enforcement
- Read-only for sentinels (except own domain)
- Write-only for authorized agents
- Delete protection (7-day retention)
