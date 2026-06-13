# HARNAS_OPENCLAW - COMPLETE DESIGN SPECIFICATION
## Architecture, Payloads, Configuration, and Workflows

**Status:** DESIGN PHASE
**Date:** 2026-06-03
**Scope:** Detailed design for OpenClaw-native HARNAS implementation

---

## EXECUTIVE SUMMARY

HARNAS_OPENCLAW is a complete redesign of the agent autonomy system built from scratch for OpenClaw.

Key aspects:
- **Agent-Centric:** Agents receive consolidation messages from OpenClaw
- **Message-Driven:** Payloads define what consolidation task to run
- **OpenClaw-Native:** Uses OpenClaw cron, messaging, and logging
- **Scalable:** Easy to manage 32 agents and 128 cron jobs
- **Observable:** All activity visible in OpenClaw dashboard

---

## PART 1: DIRECTORY STRUCTURE
✅ DOCUMENT 1 COMPLETE!
✅ HARNAS_OPENCLAW_ANALYSIS.md - AANGEMAAKT
   - Huido HARNAS problemen geanalyseerd
   - OpenClaw capabilities onderzocht
   - New design principles vastgesteld
   - Implementation strategy gepland

🔥 NU DOCUMENT 2: DESIGN
Run dit:
bashcat > /home/prime/arc_ai_angels/HARNAS_OPENCLAW/HARNAS_OPENCLAW_DESIGN.md << 'EOF'
# HARNAS_OPENCLAW - COMPLETE DESIGN SPECIFICATION
## Architecture, Payloads, Configuration, and Workflows

**Status:** DESIGN PHASE
**Date:** 2026-06-03
**Scope:** Detailed design for OpenClaw-native HARNAS implementation

---

## EXECUTIVE SUMMARY

HARNAS_OPENCLAW is a complete redesign of the agent autonomy system built from scratch for OpenClaw.

Key aspects:
- **Agent-Centric:** Agents receive consolidation messages from OpenClaw
- **Message-Driven:** Payloads define what consolidation task to run
- **OpenClaw-Native:** Uses OpenClaw cron, messaging, and logging
- **Scalable:** Easy to manage 32 agents and 128 cron jobs
- **Observable:** All activity visible in OpenClaw dashboard

---

## PART 1: DIRECTORY STRUCTURE
/home/prime/arc_ai_angels/HARNAS_OPENCLAW/
├── README.md                           (Overview & quick start)
├── HARNAS_OPENCLAW_ANALYSIS.md        (Analysis phase - completed)
├── HARNAS_OPENCLAW_DESIGN.md          (This file - design)
├── HARNAS_OPENCLAW_IMPLEMENTATION.md  (Implementation - next)
│
├── scripts/
│   ├── setup-harnas-openclaw.sh       (Create all 128 cron jobs)
│   ├── agent-consolidate.sh           (Consolidation executor)
│   ├── agent-wrap-up.sh               (Daily wrap-up executor)
│   ├── verify-harnas-setup.sh         (Verification script)
│   └── cleanup-old-harnas.sh          (Archive old HARNAS)
│
├── consolidation/
│   ├── consolidate-memory-openclaw.sh (Phase 2: Auto-consolidation REFACTORED)
│   ├── intelligent-consolidation-openclaw.sh (Phase 3: Intelligent REFACTORED)
│   └── agent-prep.sh                  (Phase 1: Prep)
│
├── config/
│   ├── HARNAS_OPENCLAW_CONFIG.md      (All agent configurations)
│   ├── agent-message-payloads.md      (Message format specifications)
│   └── cron-job-spec.md               (OpenClaw cron job specifications)
│
├── templates/
│   ├── agent-harnas-init.sh           (Agent initialization template)
│   ├── cron-job-template.sh           (Cron job creation template)
│   └── agent-consolidation-handler.md (Agent-side handler template)
│
└── monitoring/
├── harnas-dashboard.md            (OpenClaw dashboard setup)
└── harnas-alerts.md               (Alert configuration)

---

## PART 2: AGENT MESSAGE PAYLOAD SPECIFICATION

### 2.1 Core Message Structure

```json
{
  "harnas": {
    "version": "1.0",
    "timestamp": "2026-06-03T06:00:00Z",
    "task": "consolidate",
    "agent": "nova",
    "phase": 2,
    "payload": {
      "action": "consolidate-memory",
      "journalPath": "/home/prime/arc_ai_angels/agents/nova/JOURNAL/closed",
      "memoryPath": "/home/prime/arc_ai_angels/agents/nova/MEMORY.md",
      "logPath": "/home/prime/arc_ai_angels/agents/nova/consolidation.log",
      "timeout": 30,
      "metadata": {
        "hostname": "Silver-Surfer",
        "user": "prime",
        "runTime": "2026-06-03T06:00:00Z"
      }
    }
  }
}
```

### 2.2 Message Variations by Phase

#### Phase 1: PREP (00:00 UTC)
```json
{
  "harnas": {
    "task": "prep",
    "phase": 1,
    "payload": {
      "action": "read-memory",
      "memoryPath": "/agents/nova/MEMORY.md",
      "prepareFor": "daily-work"
    }
  }
}
```

#### Phase 2: AUTO-CONSOLIDATION (06:00 UTC)
```json
{
  "harnas": {
    "task": "consolidate",
    "phase": 2,
    "payload": {
      "action": "consolidate-memory",
      "journalPath": "/agents/nova/JOURNAL/closed",
      "memoryPath": "/agents/nova/MEMORY.md",
      "method": "auto"
    }
  }
}
```

#### Phase 3: INTELLIGENT CONSOLIDATION (12:00 UTC)
```json
{
  "harnas": {
    "task": "intelligent",
    "phase": 3,
    "payload": {
      "action": "intelligent-consolidation",
      "journalPath": "/agents/nova/JOURNAL/closed",
      "memoryPath": "/agents/nova/MEMORY.md",
      "method": "pattern-analysis",
      "thinkingLevel": "medium"
    }
  }
}
```

#### Phase 4: WRAP-UP (18:00 UTC)
```json
{
  "harnas": {
    "task": "wrap-up",
    "phase": 4,
    "payload": {
      "action": "daily-finalization",
      "memoryPath": "/agents/nova/MEMORY.md",
      "reportTo": "fea",
      "generateReport": true
    }
  }
}
```

---

## PART 3: OPENCLAW CRON JOB SPECIFICATION

### 3.1 Cron Job Template

```bash
openclaw cron add \
  --name "HARNAS: ${AGENT} - Phase ${PHASE}" \
  --agent "${AGENT}" \
  --cron "0 ${HOUR} * * *" \
  --message "${PAYLOAD_JSON}" \
  --session "isolated" \
  --expect-final true \
  --timeout-seconds 60 \
  --thinking "medium" \
  --description "HARNAS Phase ${PHASE} consolidation for ${AGENT}" \
  --announce
```

### 3.2 Complete Cron Schedule (128 Jobs)
PHASE 1 (00:00 UTC) - PREP

32 jobs (1 per agent)
Command: openclaw cron add ... --cron "0 0 * * *" ... --message '{"task":"prep",...}'

PHASE 2 (06:00 UTC) - AUTO-CONSOLIDATION

32 jobs (1 per agent)
Command: openclaw cron add ... --cron "0 6 * * *" ... --message '{"task":"consolidate",...}'

PHASE 3 (12:00 UTC) - INTELLIGENT CONSOLIDATION

32 jobs (1 per agent)
Command: openclaw cron add ... --cron "0 12 * * *" ... --message '{"task":"intelligent",...}'

PHASE 4 (18:00 UTC) - WRAP-UP

32 jobs (1 per agent)
Command: openclaw cron add ... --cron "0 18 * * *" ... --message '{"task":"wrap-up",...}'

TOTAL: 128 cron jobs across 32 agents

### 3.3 Cron Job Configuration Table

| Phase | Time | Agent Count | Total Jobs | Action | Duration |
|-------|------|-------------|------------|--------|----------|
| **1** | 00:00 UTC | 32 | 32 | Prep | <5s per agent |
| **2** | 06:00 UTC | 32 | 32 | Auto-consolidate | <15s per agent |
| **3** | 12:00 UTC | 32 | 32 | Intelligent consolidate | <20s per agent |
| **4** | 18:00 UTC | 32 | 32 | Daily wrap-up | <10s per agent |
| **TOTAL** | | | **128** | | |

---

## PART 4: AGENT CONSOLIDATION WORKFLOW

### 4.1 Complete Agent Workflow per Phase
┌─────────────────────────────────────────────────────────┐
│              HARNAS_OPENCLAW WORKFLOW                   │
└─────────────────────────────────────────────────────────┘
00:00 UTC - PHASE 1: PREP
├─ OpenClaw sends message: { task: "prep" }
├─ Agent (nova) receives message
├─ Agent reads MEMORY.md (past learnings)
├─ Agent prepares for daily work
│  ├─ Checks IDENTITY.md (know thyself)
│  ├─ Reads SOUL.md (core values)
│  └─ Loads MEMORY.md (past patterns)
├─ Agent logs to CONSOLIDATION.log: "PREP COMPLETE"
└─ Agent ready for work
06:00 UTC - PHASE 2: AUTO-CONSOLIDATION
├─ OpenClaw sends message: { task: "consolidate" }
├─ Agent (nova) receives message
├─ Agent runs: consolidate-memory-openclaw.sh
│  ├─ Check for entries in JOURNAL/closed/
│  ├─ Extract learnings from each closed entry
│  ├─ Calculate success rates, timing, patterns
│  ├─ Update MEMORY.md with consolidated learnings
│  └─ Archive processed JOURNAL entries
├─ Agent logs: "AUTO-CONSOLIDATION COMPLETE"
│  └─ Tasks processed: X
│  └─ Success rate: Y%
│  └─ New learnings: Z
└─ OpenClaw logs to dashboard
12:00 UTC - PHASE 3: INTELLIGENT CONSOLIDATION
├─ OpenClaw sends message: { task: "intelligent" }
├─ Agent (nova) receives message
├─ Agent runs: intelligent-consolidation-openclaw.sh
│  ├─ Analyze patterns in MEMORY.md
│  ├─ Detect bottlenecks in task execution
│  ├─ Generate optimization suggestions
│  ├─ Update MEMORY with intelligence
│  └─ Log findings
├─ Agent logs: "INTELLIGENT-CONSOLIDATION COMPLETE"
│  └─ Patterns found: X
│  └─ Suggestions generated: Y
│  └─ Intelligence level: UPDATED
└─ OpenClaw logs to dashboard
18:00 UTC - PHASE 4: DAILY WRAP-UP
├─ OpenClaw sends message: { task: "wrap-up" }
├─ Agent (nova) receives message
├─ Agent runs: agent-wrap-up.sh
│  ├─ Finalize day's learnings
│  ├─ Generate daily summary
│  ├─ Archive day's entries
│  ├─ Prepare for next day
│  └─ Report back to Fea (if needed)
├─ Agent logs: "DAILY WRAP-UP COMPLETE"
│  └─ Daily summary prepared
│  └─ Archives created
│  └─ Ready for tomorrow
└─ OpenClaw logs to dashboard

### 4.2 Agent-Side Handler (Handler Template)

```bash
#!/bin/bash
# HARNAS_OPENCLAW Message Handler
# Runs in agent's OpenClaw session when receiving HARNAS message

HARNAS_MESSAGE="$1"  # JSON payload from OpenClaw

# Parse message
TASK=$(echo "$HARNAS_MESSAGE" | jq -r '.harnas.task')
PHASE=$(echo "$HARNAS_MESSAGE" | jq -r '.harnas.phase')
AGENT=$(echo "$HARNAS_MESSAGE" | jq -r '.harnas.agent')

case "$TASK" in
  "prep")
    # Phase 1: PREP
    source /home/prime/arc_ai_angels/HARNAS_OPENCLAW/consolidation/agent-prep.sh
    agent_prep "$AGENT"
    ;;
  "consolidate")
    # Phase 2: AUTO-CONSOLIDATION
    source /home/prime/arc_ai_angels/HARNAS_OPENCLAW/consolidation/consolidate-memory-openclaw.sh
    consolidate_memory "$AGENT"
    ;;
  "intelligent")
    # Phase 3: INTELLIGENT CONSOLIDATION
    source /home/prime/arc_ai_angels/HARNAS_OPENCLAW/consolidation/intelligent-consolidation-openclaw.sh
    intelligent_consolidation "$AGENT"
    ;;
  "wrap-up")
    # Phase 4: WRAP-UP
    source /home/prime/arc_ai_angels/HARNAS_OPENCLAW/consolidation/agent-wrap-up.sh
    agent_wrap_up "$AGENT"
    ;;
esac
```

---

## PART 5: CONFIGURATION & SETUP

### 5.1 Agent Configuration Template

Each agent needs HARNAS configuration in their directory:
/agents/nova/HARNAS_OPENCLAW.md
HARNAS_OPENCLAW Configuration - Nova
Consolidation Paths

JOURNAL_CLOSED: /home/prime/arc_ai_angels/agents/nova/JOURNAL/closed
MEMORY: /home/prime/arc_ai_angels/agents/nova/MEMORY.md
TASK_HISTORY: /home/prime/arc_ai_angels/agents/nova/TASK_HISTORY.md
CONSOLIDATION_LOG: /home/prime/arc_ai_angels/agents/nova/consolidation.log

Cron Job IDs (created by setup script)

Phase 1 (PREP): [job-id-1]
Phase 2 (AUTO-CONSOLIDATE): [job-id-2]
Phase 3 (INTELLIGENT): [job-id-3]
Phase 4 (WRAP-UP): [job-id-4]

Message Handler

Location: /HARNAS_OPENCLAW/templates/agent-harnas-handler.sh
Session: isolated
Timeout: 60 seconds


### 5.2 OpenClaw Configuration Integration

In agent's OpenClaw session:

```json
{
  "harnas": {
    "enabled": true,
    "version": "1.0",
    "agentId": "nova",
    "consolidationPath": "/agents/nova",
    "phases": {
      "1": { "name": "PREP", "time": "00:00", "enabled": true },
      "2": { "name": "AUTO-CONSOLIDATION", "time": "06:00", "enabled": true },
      "3": { "name": "INTELLIGENT", "time": "12:00", "enabled": true },
      "4": { "name": "WRAP-UP", "time": "18:00", "enabled": true }
    }
  }
}
```

---

## PART 6: CONSOLIDATION SCRIPTS REFACTORING

### 6.1 Consolidate-Memory (Phase 2) - Refactored for OpenClaw

**Old:** Receives agent name as shell argument
**New:** Receives JSON message from OpenClaw, executes in agent's session

```bash
#!/bin/bash
# consolidate-memory-openclaw.sh
# Phase 2: AUTO-CONSOLIDATION (OPENCLAW VERSION)

AGENT="${1:-${HARNAS_AGENT:-nova}}"
JOURNAL_CLOSED="/home/prime/arc_ai_angels/agents/$AGENT/JOURNAL/closed"
MEMORY="/home/prime/arc_ai_angels/agents/$AGENT/MEMORY.md"
LOG="/home/prime/arc_ai_angels/agents/$AGENT/consolidation.log"

echo "[$(date)] PHASE 2: AUTO-CONSOLIDATION START" >> "$LOG"

# Count JOURNAL entries
ENTRY_COUNT=$(find "$JOURNAL_CLOSED" -type f -name "*.md" | wc -l)

if [ $ENTRY_COUNT -eq 0 ]; then
  echo "[$(date)] No entries to consolidate" >> "$LOG"
  exit 0
fi

# Process entries (IMPLEMENTATION DETAIL - simplified here)
TOTAL_SUCCESS=0
for entry in "$JOURNAL_CLOSED"/*.md; do
  [ -f "$entry" ] || continue
  if grep -q "SUCCESS" "$entry"; then
    ((TOTAL_SUCCESS++))
  fi
done

SUCCESS_RATE=$((TOTAL_SUCCESS * 100 / ENTRY_COUNT))

# Update MEMORY.md
echo "" >> "$MEMORY"
echo "## Consolidation: $(date +%Y-%m-%d)" >> "$MEMORY"
echo "- Entries processed: $ENTRY_COUNT" >> "$MEMORY"
echo "- Success rate: $SUCCESS_RATE%" >> "$MEMORY"
echo "- Timestamp: $(date)" >> "$MEMORY"

echo "[$(date)] PHASE 2: AUTO-CONSOLIDATION COMPLETE" >> "$LOG"
echo "✓ Consolidation complete: $ENTRY_COUNT entries, $SUCCESS_RATE% success"
```

### 6.2 Intelligent-Consolidation (Phase 3) - Refactored for OpenClaw

**Similar refactoring:** Receives JSON from OpenClaw, executes in agent session

---

## PART 7: ERROR HANDLING & RESILIENCE

### 7.1 Error Handling Strategy

```bash
# Within each phase handler:

set -e  # Exit on error

trap 'on_error $? $LINENO' ERR

on_error() {
  local exit_code=$1
  local line_number=$2
  
  echo "[ERROR] Phase failed at line $line_number (code: $exit_code)" >> "$LOG"
  echo "HARNAS: Phase execution failed" | tee /tmp/harnas_error.log
  
  # Notify OpenClaw (will be displayed in dashboard)
  exit $exit_code
}

# Retry logic for critical operations
retry_command() {
  local max_attempts=3
  local attempt=1
  
  while [ $attempt -le $max_attempts ]; do
    if "$@"; then
      return 0
    fi
    echo "[RETRY] Attempt $attempt/$max_attempts failed" >> "$LOG"
    ((attempt++))
    sleep 5
  done
  
  return 1
}
```

### 7.2 Monitoring & Alerting
OpenClaw Dashboard automatically tracks:

Job execution time
Success/failure status
Agent response time
Error messages
Last execution timestamp

Alerts trigger if:

Consolidation timeout (>60s)
Agent returns error
Multiple consecutive failures
Memory update fails


---

## PART 8: MIGRATION PATH

### 8.1 Parallel Operation (Safety)
Phase 1: Setup HARNAS_OPENCLAW

Create directory structure
Deploy scripts
Configure agents
OpenClaw cron jobs DISABLED initially

Phase 2: Test with nova

Enable nova's HARNAS_OPENCLAW cron jobs
Monitor for 24h
Verify consolidation working
Keep old system running

Phase 3: Gradual Rollout

Enable remaining Omni Leads (cortexia, saelia, etc.)
Monitor each batch
Verify logs and consolidation

Phase 4: Full Deployment

Enable all Sentinels
Monitor full system
Verify all 128 jobs working

Phase 5: Cleanup

Disable system crontab entries (backup first)
Archive old HARNAS/
Remove Phase1-4 scripts


---

## PART 9: SUCCESS METRICS

### 9.1 Phase Completion Criteria

- [ ] All 128 OpenClaw cron jobs created
- [ ] All jobs showing in `openclaw cron list`
- [ ] Each job has correct message payload
- [ ] Agents receiving messages correctly
- [ ] Consolidation scripts refactored
- [ ] MEMORY.md being updated (not empty)
- [ ] JOURNAL entries being processed
- [ ] Error handling working
- [ ] Dashboard showing all jobs
- [ ] No system crontab entries needed

### 9.2 Performance Targets
✅ Message delivery: <1 second
✅ Phase 1 (PREP): <5 seconds
✅ Phase 2 (CONSOLIDATE): <15 seconds
✅ Phase 3 (INTELLIGENT): <20 seconds
✅ Phase 4 (WRAP-UP): <10 seconds
✅ Total daily processing: <50 seconds per agent
✅ Success rate: >99.5%
✅ Error rate: <0.1%

---

## CONCLUSION

HARNAS_OPENCLAW Design provides:

1. **Clean Architecture** - No unnecessary wrapper scripts
2. **Message-Driven** - Agents know exactly what to do from payload
3. **OpenClaw-Native** - Uses built-in cron and messaging
4. **Scalable** - Easy to manage 32 agents and 128 jobs
5. **Observable** - Complete visibility in OpenClaw dashboard
6. **Resilient** - Error handling and retry logic throughout
7. **Monitorable** - All metrics visible and trackable

**DESIGN COMPLETE - READY FOR IMPLEMENTATION** ✅

---

**Next Document:** HARNAS_OPENCLAW_IMPLEMENTATION.md
**Next Step:** Complete implementation specifications and setup procedures

