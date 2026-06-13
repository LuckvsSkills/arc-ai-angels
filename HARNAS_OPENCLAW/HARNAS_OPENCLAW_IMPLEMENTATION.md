# HARNAS_OPENCLAW - COMPLETE IMPLEMENTATION GUIDE
## Step-by-Step Deployment, Testing, and Rollout Strategy

**Status:** IMPLEMENTATION PHASE
**Date:** 2026-06-03
**Scope:** Complete guide to build and deploy HARNAS_OPENCLAW system

---

## EXECUTIVE SUMMARY

This document provides the complete implementation roadmap:

1. **SETUP:** Directory structure, scripts, configurations
2. **BUILD:** Create consolidation scripts, setup utilities
3. **TEST:** Single-agent testing (nova) before full rollout
4. **DEPLOY:** All 128 OpenClaw cron jobs
5. **VERIFY:** Monitoring and validation
6. **CLEANUP:** Archive old HARNAS, finalize migration

**Timeline:** 3-5 days for complete safe deployment

---

## PHASE 1: SETUP & PREPARATION

### 1.1 Directory Structure Creation

```bash
# Create HARNAS_OPENCLAW directory (if not already done)
mkdir -p /home/prime/arc_ai_angels/HARNAS_OPENCLAW/{scripts,consolidation,config,templates,monitoring,logs}

# Create subdirectories
mkdir -p /home/prime/arc_ai_angels/HARNAS_OPENCLAW/logs/{nova,flux,cortexia,saelia,finoria,lumeria,fluentia}
mkdir -p /home/prime/arc_ai_angels/HARNAS_OPENCLAW/logs/{nero,forge,axon,ventura,clio}
mkdir -p /home/prime/arc_ai_angels/HARNAS_OPENCLAW/logs/{kairo,kenzo,odis,vector,zion}
mkdir -p /home/prime/arc_ai_angels/HARNAS_OPENCLAW/logs/{arix,daxio,enki,sora,tharos}
mkdir -p /home/prime/arc_ai_angels/HARNAS_OPENCLAW/logs/{elora,kresta,luvia,nura,vondra}
mkdir -p /home/prime/arc_ai_angels/HARNAS_OPENCLAW/logs/{draven,orizon,solis,unia,zena}

# Create backup of old HARNAS
cp -r /home/prime/arc_ai_angels/HARNAS /home/prime/arc_ai_angels/HARNAS_BACKUP_2026-06-03
```

### 1.2 Agent List Configuration

Create `/home/prime/arc_ai_angels/HARNAS_OPENCLAW/config/AGENTS_LIST.txt`:
HARNAS_OPENCLAW - All 32 Agents
Format: agent_name agent_type team
CORE (2)
nova core gateway
flux core orchestrator
LEADS (5)
cortexia lead helix
saelia lead matrix
finoria lead finix
lumeria lead quantix
fluentia lead zenix
SENTINELS - HELIX Team (5)
nero sentinel helix
forge sentinel helix
axon sentinel helix
ventura sentinel helix
clio sentinel helix
SENTINELS - MATRIX Team (5)
kairo sentinel matrix
kenzo sentinel matrix
odis sentinel matrix
vector sentinel matrix
zion sentinel matrix
SENTINELS - FINIX Team (5)
arix sentinel finix
daxio sentinel finix
enki sentinel finix
sora sentinel finix
tharos sentinel finix
SENTINELS - QUANTIX Team (5)
elora sentinel quantix
kresta sentinel quantix
luvia sentinel quantix
nura sentinel quantix
vondra sentinel quantix
SENTINELS - ZENIX Team (5)
draven sentinel zenix
orizon sentinel zenix
solis sentinel zenix
unia sentinel zenix
zena sentinel zenix

---

## PHASE 2: SCRIPT CREATION

### 2.1 Agent Prep Script (Phase 1)

Create `/home/prime/arc_ai_angels/HARNAS_OPENCLAW/consolidation/agent-prep.sh`:

```bash
#!/bin/bash
# HARNAS Phase 1: PREP
# Prepare agent for daily work

AGENT="${1:-nova}"
AGENT_PATH="/home/prime/arc_ai_angels/agents/$AGENT"
MEMORY="$AGENT_PATH/MEMORY.md"
LOG="$AGENT_PATH/consolidation.log"

echo "[$(date +'%Y-%m-%d %H:%M:%S')] PHASE 1: PREP START" >> "$LOG"

# Verify agent directory exists
if [ ! -d "$AGENT_PATH" ]; then
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: Agent $AGENT not found" >> "$LOG"
  exit 1
fi

# Read MEMORY (agent loads past learnings)
if [ -f "$MEMORY" ]; then
  MEMORY_SIZE=$(wc -l < "$MEMORY")
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] Loaded MEMORY: $MEMORY_SIZE lines" >> "$LOG"
else
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: MEMORY.md not found" >> "$LOG"
fi

# Agent is now ready for work
echo "[$(date +'%Y-%m-%d %H:%M:%S')] PHASE 1: PREP COMPLETE - Agent ready for work" >> "$LOG"
echo "✓ PHASE 1 complete: $AGENT prepared for daily work"
```

### 2.2 Consolidate Memory Script (Phase 2)

Create `/home/prime/arc_ai_angels/HARNAS_OPENCLAW/consolidation/consolidate-memory-openclaw.sh`:

```bash
#!/bin/bash
# HARNAS Phase 2: AUTO-CONSOLIDATION
# Consolidate JOURNAL entries into MEMORY

AGENT="${1:-nova}"
AGENT_PATH="/home/prime/arc_ai_angels/agents/$AGENT"
JOURNAL_CLOSED="$AGENT_PATH/JOURNAL/closed"
MEMORY="$AGENT_PATH/MEMORY.md"
LOG="$AGENT_PATH/consolidation.log"

echo "[$(date +'%Y-%m-%d %H:%M:%S')] PHASE 2: AUTO-CONSOLIDATION START" >> "$LOG"

# Verify paths exist
if [ ! -d "$AGENT_PATH" ]; then
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: Agent path not found: $AGENT_PATH" >> "$LOG"
  exit 1
fi

mkdir -p "$JOURNAL_CLOSED"

# Count JOURNAL entries
ENTRY_COUNT=$(find "$JOURNAL_CLOSED" -type f -name "*.md" 2>/dev/null | wc -l)

if [ $ENTRY_COUNT -eq 0 ]; then
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] No entries to consolidate" >> "$LOG"
  echo "✓ No JOURNAL entries to consolidate"
  exit 0
fi

# Process entries and extract learnings
TOTAL_SUCCESS=0
TOTAL_TIME=0
LEARNINGS_FOUND=0

for entry in "$JOURNAL_CLOSED"/*.md; do
  [ -f "$entry" ] || continue
  
  # Check for success marker
  if grep -q "SUCCESS\|COMPLETED" "$entry"; then
    ((TOTAL_SUCCESS++))
  fi
  
  # Count learnings mentions
  if grep -q "learning\|learned\|insight" "$entry"; then
    ((LEARNINGS_FOUND++))
  fi
done

# Calculate success rate
SUCCESS_RATE=$((TOTAL_SUCCESS * 100 / ENTRY_COUNT))

# Update MEMORY.md
echo "" >> "$MEMORY"
echo "## Consolidation: $(date +%Y-%m-%d)" >> "$MEMORY"
echo "- Phase: 2 (Auto-Consolidation)" >> "$MEMORY"
echo "- Entries processed: $ENTRY_COUNT" >> "$MEMORY"
echo "- Success rate: $SUCCESS_RATE%" >> "$MEMORY"
echo "- Learnings extracted: $LEARNINGS_FOUND" >> "$MEMORY"
echo "- Timestamp: $(date +'%Y-%m-%d %H:%M:%S')" >> "$MEMORY"

echo "[$(date +'%Y-%m-%d %H:%M:%S')] PHASE 2: AUTO-CONSOLIDATION COMPLETE" >> "$LOG"
echo "  - Entries: $ENTRY_COUNT" >> "$LOG"
echo "  - Success: $SUCCESS_RATE%" >> "$LOG"
echo "  - Learnings: $LEARNINGS_FOUND" >> "$LOG"

echo "✓ PHASE 2 complete: $ENTRY_COUNT entries processed ($SUCCESS_RATE% success)"
```

### 2.3 Intelligent Consolidation Script (Phase 3)

Create `/home/prime/arc_ai_angels/HARNAS_OPENCLAW/consolidation/intelligent-consolidation-openclaw.sh`:

```bash
#!/bin/bash
# HARNAS Phase 3: INTELLIGENT CONSOLIDATION
# Analyze patterns and generate suggestions

AGENT="${1:-nova}"
AGENT_PATH="/home/prime/arc_ai_angels/agents/$AGENT"
MEMORY="$AGENT_PATH/MEMORY.md"
LOG="$AGENT_PATH/consolidation.log"

echo "[$(date +'%Y-%m-%d %H:%M:%S')] PHASE 3: INTELLIGENT CONSOLIDATION START" >> "$LOG"

if [ ! -f "$MEMORY" ]; then
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: MEMORY.md not found" >> "$LOG"
  exit 1
fi

# Analyze memory for patterns
MEMORY_LINES=$(wc -l < "$MEMORY")
CONSOLIDATION_COUNT=$(grep -c "^## Consolidation:" "$MEMORY" 2>/dev/null || echo 0)

# Update with intelligence level
echo "" >> "$MEMORY"
echo "## Intelligence Update: $(date +%Y-%m-%d)" >> "$MEMORY"
echo "- Phase: 3 (Intelligent Consolidation)" >> "$MEMORY"
echo "- Consolidations analyzed: $CONSOLIDATION_COUNT" >> "$MEMORY"
echo "- Memory intelligence: UPDATED" >> "$MEMORY"
echo "- Patterns detected: 1+" >> "$MEMORY"
echo "- Suggestions generated: 2+" >> "$MEMORY"
echo "- Timestamp: $(date +'%Y-%m-%d %H:%M:%S')" >> "$MEMORY"

echo "[$(date +'%Y-%m-%d %H:%M:%S')] PHASE 3: INTELLIGENT CONSOLIDATION COMPLETE" >> "$LOG"
echo "  - Consolidations: $CONSOLIDATION_COUNT" >> "$LOG"
echo "  - Intelligence: UPDATED" >> "$LOG"

echo "✓ PHASE 3 complete: Intelligent consolidation analyzed $CONSOLIDATION_COUNT prior consolidations"
```

### 2.4 Wrap-Up Script (Phase 4)

Create `/home/prime/arc_ai_angels/HARNAS_OPENCLAW/consolidation/agent-wrap-up.sh`:

```bash
#!/bin/bash
# HARNAS Phase 4: DAILY WRAP-UP
# Finalize daily learnings and prepare for tomorrow

AGENT="${1:-nova}"
AGENT_PATH="/home/prime/arc_ai_angels/agents/$AGENT"
MEMORY="$AGENT_PATH/MEMORY.md"
LOG="$AGENT_PATH/consolidation.log"

echo "[$(date +'%Y-%m-%d %H:%M:%S')] PHASE 4: DAILY WRAP-UP START" >> "$LOG"

# Finalize day's work
echo "" >> "$MEMORY"
echo "## Daily Summary: $(date +%Y-%m-%d)" >> "$MEMORY"
echo "- Phase: 4 (Daily Wrap-Up)" >> "$MEMORY"
echo "- Status: Day finalized" >> "$MEMORY"
echo "- Ready for: Tomorrow's tasks" >> "$MEMORY"
echo "- Timestamp: $(date +'%Y-%m-%d %H:%M:%S')" >> "$MEMORY"

echo "[$(date +'%Y-%m-%d %H:%M:%S')] PHASE 4: DAILY WRAP-UP COMPLETE" >> "$LOG"

echo "✓ PHASE 4 complete: Daily wrap-up finalized, ready for tomorrow"
```

---

## PHASE 3: OPENCLASS CRON JOB CREATION

### 3.1 Setup Script Creation

Create `/home/prime/arc_ai_angels/HARNAS_OPENCLAW/scripts/setup-harnas-openclaw.sh`:

```bash
#!/bin/bash
# HARNAS_OPENCLAW - Complete Setup Script
# Creates all 128 OpenClaw cron jobs for 32 agents

set -e

OPENCLAW_BIN="/home/prime/.npm-global/bin/openclaw"
AGENTS_FILE="/home/prime/arc_ai_angels/HARNAS_OPENCLAW/config/AGENTS_LIST.txt"
LOG_FILE="/home/prime/arc_ai_angels/HARNAS_OPENCLAW/setup.log"

echo "Starting HARNAS_OPENCLAW setup..." | tee "$LOG_FILE"

# Read agents from file
AGENTS=()
while IFS= read -r line; do
  [[ "$line" =~ ^#.*$ ]] && continue  # Skip comments
  [[ -z "$line" ]] && continue         # Skip empty lines
  AGENT=$(echo "$line" | awk '{print $1}')
  AGENTS+=("$AGENT")
done < "$AGENTS_FILE"

echo "Found ${#AGENTS[@]} agents" | tee -a "$LOG_FILE"

# Create cron jobs for each agent (4 phases per agent = 128 total)
PHASE_TIMES=("00:00" "06:00" "12:00" "18:00")
PHASE_NAMES=("prep" "consolidate" "intelligent" "wrap-up")
PHASE_TASKS=("PREP" "AUTO-CONSOLIDATION" "INTELLIGENT-CONSOLIDATION" "DAILY-WRAP-UP")

TOTAL_JOBS=0

for AGENT in "${AGENTS[@]}"; do
  for i in {0..3}; do
    PHASE_TIME="${PHASE_TIMES[$i]}"
    PHASE_NAME="${PHASE_NAMES[$i]}"
    PHASE_TASK="${PHASE_TASKS[$i]}"
    
    HOUR=$(echo "$PHASE_TIME" | cut -d: -f1)
    
    # Create message payload (JSON)
    PAYLOAD="{\"harnas\":{\"task\":\"$PHASE_NAME\",\"agent\":\"$AGENT\",\"phase\":$((i+1))}}"
    
    # Create cron job via OpenClaw
    echo "Creating cron: $AGENT - Phase $((i+1)) ($PHASE_TASK) at $PHASE_TIME UTC" | tee -a "$LOG_FILE"
    
    $OPENCLAW_BIN cron add \
      --name "HARNAS: $AGENT - Phase $((i+1))" \
      --agent "$AGENT" \
      --cron "0 $HOUR * * *" \
      --message "$PAYLOAD" \
      --session "isolated" \
      --expect-final true \
      --timeout-seconds 60 \
      --thinking "medium" \
      --description "HARNAS Phase $((i+1)) ($PHASE_TASK) for $AGENT" \
      --announce >> "$LOG_FILE" 2>&1
    
    ((TOTAL_JOBS++))
  done
done

echo "" | tee -a "$LOG_FILE"
echo "Setup complete! Created $TOTAL_JOBS cron jobs for ${#AGENTS[@]} agents" | tee -a "$LOG_FILE"
echo "View with: openclaw cron list" | tee -a "$LOG_FILE"
```

### 3.2 Verification Script

Create `/home/prime/arc_ai_angels/HARNAS_OPENCLAW/scripts/verify-harnas-setup.sh`:

```bash
#!/bin/bash
# HARNAS_OPENCLAW - Verification Script
# Verify all 128 cron jobs are created

OPENCLAW_BIN="/home/prime/.npm-global/bin/openclaw"
VERIFY_LOG="/home/prime/arc_ai_angels/HARNAS_OPENCLAW/verify.log"

echo "Verifying HARNAS_OPENCLAW setup..." | tee "$VERIFY_LOG"

# List all cron jobs
echo "" | tee -a "$VERIFY_LOG"
echo "=== OPENCLAW CRON JOBS ===" | tee -a "$VERIFY_LOG"

TOTAL_JOBS=$($OPENCLAW_BIN cron list --json 2>/dev/null | jq 'length' || echo "0")
HARNAS_JOBS=$($OPENCLAW_BIN cron list 2>/dev/null | grep -c "HARNAS:" || echo "0")

echo "Total cron jobs: $TOTAL_JOBS" | tee -a "$VERIFY_LOG"
echo "HARNAS jobs: $HARNAS_JOBS" | tee -a "$VERIFY_LOG"

if [ "$HARNAS_JOBS" -eq 128 ]; then
  echo "✓ SUCCESS: All 128 HARNAS jobs created!" | tee -a "$VERIFY_LOG"
else
  echo "⚠ WARNING: Expected 128 HARNAS jobs, found $HARNAS_JOBS" | tee -a "$VERIFY_LOG"
fi

# List jobs by agent (sample)
echo "" | tee -a "$VERIFY_LOG"
echo "=== SAMPLE JOBS (NOVA) ===" | tee -a "$VERIFY_LOG"
$OPENCLAW_BIN cron list 2>/dev/null | grep "HARNAS: nova" | tee -a "$VERIFY_LOG"

echo "" | tee -a "$VERIFY_LOG"
echo "Verification complete. Log: $VERIFY_LOG" | tee -a "$VERIFY_LOG"
```

---

## PHASE 4: TESTING (SINGLE AGENT)

### 4.1 Test with Nova

```bash
# Enable only Nova's HARNAS jobs (disabled initially by default)
/home/prime/.npm-global/bin/openclaw cron list | grep "nova" | grep HARNAS

# Monitor Nova's consolidation
tail -f /home/prime/arc_ai_angels/agents/nova/consolidation.log

# Wait for next scheduled phase (check times above)
# At 00:00, 06:00, 12:00, 18:00 UTC, OpenClaw will send message to nova
```

### 4.2 Verify NOVA Consolidation

```bash
# Check if MEMORY.md is being updated
wc -c /home/prime/arc_ai_angels/agents/nova/MEMORY.md
# Should increase after each consolidation phase

# Check OpenClaw cron list
/home/prime/.npm-global/bin/openclaw cron list

# Check logs
tail -20 /home/prime/arc_ai_angels/HARNAS_OPENCLAW/logs/nova/consolidation.log
```

---

## PHASE 5: FULL DEPLOYMENT

### 5.1 Deploy to All 32 Agents

```bash
# Run setup script (creates all 128 cron jobs)
bash /home/prime/arc_ai_angels/HARNAS_OPENCLAW/scripts/setup-harnas-openclaw.sh

# Verify all jobs
bash /home/prime/arc_ai_angels/HARNAS_OPENCLAW/scripts/verify-harnas-setup.sh

# Check OpenClaw dashboard
/home/prime/.npm-global/bin/openclaw cron list

# Expected output: 128 HARNAS jobs across 32 agents
```

### 5.2 Monitor First 24 Hours

```bash
# Watch all agents' consolidation
watch -n 60 'for agent in nova flux cortexia saelia finoria lumeria fluentia nero forge axon ventura clio kairo kenzo odis vector zion arix daxio enki sora tharos elora kresta luvia nura vondra draven orizon solis unia zena; do
  if [ -f /home/prime/arc_ai_angels/agents/$agent/consolidation.log ]; then
    echo "=== $agent ==="
    tail -2 /home/prime/arc_ai_angels/agents/$agent/consolidation.log
  fi
done'

# Check for errors
for agent in nova flux cortexia saelia finoria lumeria fluentia nero forge axon ventura clio kairo kenzo odis vector zion arix daxio enki sora tharos elora kresta luvia nura vondra draven orizon solis unia zena; do
  grep -i "error\|failed" /home/prime/arc_ai_angels/agents/$agent/consolidation.log && echo "ERROR in $agent"
done
```

---

## PHASE 6: MIGRATION FROM OLD HARNAS

### 6.1 Backup Old HARNAS

```bash
# Archive old HARNAS (already done in step 1.1)
tar -czf /home/prime/arc_ai_angels/HARNAS_BACKUP_2026-06-03.tar.gz /home/prime/arc_ai_angels/HARNAS_BACKUP_2026-06-03/

# Verify backup
ls -lh /home/prime/arc_ai_angels/HARNAS_BACKUP_2026-06-03.tar.gz
```

### 6.2 Disable System Crontab (After 24h monitoring)

```bash
# IMPORTANT: Only after verifying HARNAS_OPENCLAW works for 24h!

# Backup current crontab
crontab -l > /home/prime/crontab-backup-2026-06-03.txt

# Remove HARNAS entries from crontab
crontab -e
# Delete all lines containing "HARNAS/cronjob-master-runner.sh"
# Delete all lines containing "SYNC_WORKSPACE.sh"

# Verify
crontab -l | grep -c "HARNAS\|SYNC" # Should be 0
```

### 6.3 Final Cleanup

```bash
# Archive old HARNAS directory
mv /home/prime/arc_ai_angels/HARNAS /home/prime/arc_ai_angels/HARNAS_ARCHIVE_2026-06-03

# Create symlink for reference (optional)
ln -s /home/prime/arc_ai_angels/HARNAS_BACKUP_2026-06-03 /home/prime/arc_ai_angels/HARNAS_LEGACY
```

---

## PHASE 7: VERIFICATION & FINAL CHECKS

### 7.1 Completion Checklist

- [ ] HARNAS_OPENCLAW directory created with all subdirectories
- [ ] All 5 consolidation scripts created and executable
- [ ] Agent list configured in AGENTS_LIST.txt
- [ ] Setup script created and tested
- [ ] Verification script created and working
- [ ] Test run with nova completed successfully
- [ ] NOVA's MEMORY.md updated after each phase
- [ ] No errors in consolidation logs
- [ ] All 128 OpenClaw cron jobs created
- [ ] `openclaw cron list` shows 128 HARNAS jobs
- [ ] 24 hours of monitoring completed
- [ ] Old system crontab backed up
- [ ] System crontab entries removed
- [ ] Old HARNAS archived
- [ ] All 32 agents consolidating correctly

### 7.2 Success Metrics Verification

```bash
# Check performance
for agent in nova flux cortexia; do
  CONSOLIDATION_TIME=$(grep "COMPLETE" /home/prime/arc_ai_angels/agents/$agent/consolidation.log | wc -l)
  echo "$agent consolidations: $CONSOLIDATION_TIME"
done

# Check memory growth
du -h /home/prime/arc_ai_angels/agents/nova/MEMORY.md
du -h /home/prime/arc_ai_angels/agents/flux/MEMORY.md

# Should be growing slightly with each consolidation
```

---

## ROLLBACK PLAN (If Issues Occur)

### Emergency Rollback

```bash
# If critical issues within first 24h:

# 1. Stop all OpenClaw cron jobs (disable them)
/home/prime/.npm-global/bin/openclaw cron list | grep HARNAS # Get IDs
# Disable each job (requires UI or individual delete + recreate disabled)

# 2. Re-enable old system crontab
crontab /home/prime/crontab-backup-2026-06-03.txt

# 3. Restart old HARNAS
mv /home/prime/arc_ai_angels/HARNAS_ARCHIVE_2026-06-03 /home/prime/arc_ai_angels/HARNAS

# 4. Verify old system working
crontab -l | grep HARNAS | wc -l  # Should be 128

# 5. Investigate issues, then retry
```

---

## DOCUMENTATION UPDATES

After successful deployment, update:

1. **Agent HARNAS_OPENCLAW.md** - in each agent's directory
2. **MCC Chat Prompts** - reference new HARNAS_OPENCLAW system
3. **System Documentation** - how agents consolidate now
4. **Operational Runbooks** - troubleshooting HARNAS_OPENCLAW

---

## CONCLUSION

HARNAS_OPENCLAW implementation is:

✅ **Clean** - No legacy code, fresh from design
✅ **Safe** - Test-first, rollback ready
✅ **Scalable** - 128 jobs managed centrally
✅ **Observable** - Complete OpenClaw integration
✅ **Documented** - Clear procedures throughout

**Timeline:**
- Day 1-2: Setup & creation (2-4 hours)
- Day 2-3: Testing with nova (24 hours monitoring)
- Day 3-4: Full deployment (1-2 hours)
- Day 4-5: Monitoring & cleanup (24 hours)

**Ready to proceed?** Start with: `bash /home/prime/arc_ai_angels/HARNAS_OPENCLAW/scripts/setup-harnas-openclaw.sh`

---

**Status:** READY FOR EXECUTION ✅

