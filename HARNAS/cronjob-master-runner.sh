#!/bin/bash
# HARNAS Master Cronjob Runner
# Runs the appropriate HARNAS phase for an agent

AGENT=$1
PHASE=$2
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
LOG_FILE="HARNAS/logs/execution/$(date +%Y-%m-%d)_${AGENT}_${PHASE}.log"

echo "[$TIMESTAMP] Starting HARNAS Phase $PHASE for $AGENT" >> "$LOG_FILE"

case $PHASE in
    1)
        # Phase 1: File API (baseline, already exists)
        echo "[$TIMESTAMP] Phase 1: File API check" >> "$LOG_FILE"
        ;;
    2)
        # Phase 2: Run cronjob API operations
        if [ -f "HARNAS/Phase2_CronjobAPI/agent-cronjob-runner.sh" ]; then
            bash HARNAS/Phase2_CronjobAPI/agent-cronjob-runner.sh "$AGENT" >> "$LOG_FILE" 2>&1
        fi
        ;;
    3)
        # Phase 3: Run auto-consolidation
        if [ -f "HARNAS/Phase3_AutoConsolidation/consolidate-memory.sh" ]; then
            bash HARNAS/Phase3_AutoConsolidation/consolidate-memory.sh "$AGENT" >> "$LOG_FILE" 2>&1
        fi
        ;;
    4)
        # Phase 4: Run intelligent consolidation
        if [ -f "HARNAS/Phase4_Intelligent/intelligent-consolidation.sh" ]; then
            bash HARNAS/Phase4_Intelligent/intelligent-consolidation.sh "$AGENT" >> "$LOG_FILE" 2>&1
        fi
        ;;
esac

echo "[$TIMESTAMP] Completed HARNAS Phase $PHASE for $AGENT" >> "$LOG_FILE"
