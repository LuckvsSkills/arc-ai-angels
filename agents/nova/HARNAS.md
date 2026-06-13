# HARNAS — Nova's Autonomy Through Consolidation

## What is HARNAS?
HARNAS = Hierarchical Agent Reasoning and Normalization Architecture System

Self-improvement system that:
- Consolidates raw activity logs
- Extracts learning patterns
- Updates performance baselines
- Improves future decisions

## How HARNAS Works for Nova

### Input: Raw JOURNAL.md
- Every action logged with timestamp
- Decisions made and their outcomes
- Learning moments captured
- Patterns observed

### Processing (Every 6 hours)
1. **Consolidation Process** runs at 00:00, 06:00, 12:00, 18:00 UTC
2. **Extract learnings** from JOURNAL entries
3. **Update MEMORY.md** with actionable patterns
4. **Measure improvements** against baselines
5. **Log results** for tracking

### Output: Updated MEMORY.md
- Compressed knowledge base
- Performance metrics
- Pattern recognition results
- Actionable insights

## Consolidation Cycle

**Every 6 hours:**
1. Read JOURNAL.md (raw activity)
2. Extract: Patterns, successes, failures
3. Write: MEMORY.md (compressed knowledge)
4. Update: TASK_HISTORY.md (metrics)
5. Calculate: Success rates, improvement trends

## Your Growth Through HARNAS
- Each cycle: Smarter pattern recognition
- Each cycle: Better intake efficiency
- Each cycle: Improved security accuracy
- Measurable: Performance baselines tracked
- Automatic: No manual intervention

## Status
- Cronjobs: 128 active (32 agents × 4/day)
- Nova's schedule: 00:00, 06:00, 12:00, 18:00 UTC
- Logs: HARNAS/logs/execution/
- Next consolidation: Check cronjob logs

