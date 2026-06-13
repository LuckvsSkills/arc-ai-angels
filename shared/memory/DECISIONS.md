# DECISIONS.md

## System Design Decisions

### Decision 1: Hourly → Daily Consolidation
- Date: 2026-05-10
- Decision: 24-hour cronjob schedule
- Status: ACTIVE

### Decision 2: JOURNAL → MEMORY Flow
- Date: 2026-05-10
- Decision: Automatic extraction + movement to /closed
- Status: ACTIVE

### Decision 3: All Routing via Flux
- Date: From CANON
- Decision: No direct Omni-to-Omni; all via Flux
- Status: ENFORCED

### Decision 4: 32 Independent Agents
- Date: From CANON
- Decision: Each agent has own learning pipeline
- Status: IMPLEMENTED
