#!/bin/bash
# HARNAS Phase 1: PREP - Prepare agent for daily work

AGENT="${1:-nova}"
AGENT_PATH="/home/prime/arc_ai_angels/agents/$AGENT"
MEMORY="$AGENT_PATH/MEMORY.md"
LOG="$AGENT_PATH/consolidation.log"

echo "[$(date +'%Y-%m-%d %H:%M:%S')] PHASE 1: PREP START" >> "$LOG"

if [ ! -d "$AGENT_PATH" ]; then
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: Agent $AGENT not found" >> "$LOG"
  exit 1
fi

if [ -f "$MEMORY" ]; then
  MEMORY_SIZE=$(wc -l < "$MEMORY")
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] Loaded MEMORY: $MEMORY_SIZE lines" >> "$LOG"
else
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: MEMORY.md not found" >> "$LOG"
fi

echo "[$(date +'%Y-%m-%d %H:%M:%S')] PHASE 1: PREP COMPLETE" >> "$LOG"
echo "✓ PHASE 1 complete: $AGENT prepared"
