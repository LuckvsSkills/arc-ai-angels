# NOVA - Agent Rules & Protocols

## Core Operating Principles

### 1. Autonomy with Oversight
- Each agent operates autonomously within their domain
- NOVA monitors aggregate behavior and system health
- Escalation to FLUX/Supreme Fea only when needed

### 2. Communication Protocols
- **Status Flow:** Bottom-up (Sentinels → Leads → FLUX → NOVA)
- **Command Flow:** Top-down (NOVA/FLUX → Leads → Sentinels)
- **Peer Coordination:** Direct agent-to-agent via shared state
- **Cronjob Cadence:** 4x daily (00:00, 06:00, 12:00, 18:00)

### 3. Memory & Learning
- Each agent maintains MEMORY.md (local state)
- TASKS.md tracks ongoing work
- JOURNAL/ captures execution logs
- intelligent-consolidation.sh learns patterns daily

### 4. Error Handling
- Errors logged to agent/logs/
- NERO (Error Handler) escalates critical failures
- Retry logic built into cronjob runner
- Silent failures prevented by health_check.sh

### 5. System Resilience
- health_check.sh validates port conflicts, stuck processes
- startup_all.sh ensures clean boot
- CORTEXIA owns system operations
- Backup/archive protocols on schedule

### 6. Escalation Hierarchy
Self-Resolution (Agent)
↓ [Fails]
Domain Lead (Omni Lead)
↓ [Fails]
FLUX (Underboss)
↓ [Fails]
NOVA (Consigliere)
↓ [Critical]
Supreme Fea (Human)
### 7. Code & Configuration Standards
- All agent code in agents/[AGENT]/
- Configuration in agents/[AGENT]/runtime/.env
- Authentication in agents/[AGENT]/agent/auth.json
- Models in agents/[AGENT]/agent/models.json

### 8. Data Integrity
- No direct filesystem access during cronjob
- Use agent-file-ops.sh for safe I/O
- LUVIA manages memory consolidation
- Version control on all critical files

### 9. Performance Baselines
- Each agent targets <2s task execution
- Cronjob overhead <100ms
- Memory footprint <500MB per agent
- KENZO monitors these SLAs

### 10. Transparency & Auditing
- All actions logged
- JOURNAL entries timestamped
- Session trajectories saved
- Audit reports in reports/

---
**Version:** 1.0
**Effective Date:** June 1, 2026
**Enforced By:** NOVA + CORTEXIA
