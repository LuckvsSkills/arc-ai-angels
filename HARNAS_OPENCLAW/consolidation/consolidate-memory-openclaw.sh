#!/bin/bash
# HARNAS Phase 2: AUTO-CONSOLIDATION - Consolidate JOURNAL→MEMORY

AGENT="${1:-nova}"
AGENT_PATH="/home/prime/arc_ai_angels/agents/$AGENT"
JOURNAL_CLOSED="$AGENT_PATH/JOURNAL/closed"
MEMORY="$AGENT_PATH/MEMORY.md"
LOG="$AGENT_PATH/consolidation.log"

echo "[$(date +'%Y-%m-%d %H:%M:%S')] PHASE 2: AUTO-CONSOLIDATION START" >> "$LOG"

if [ ! -d "$AGENT_PATH" ]; then
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: Agent path not found" >> "$LOG"
  exit 1
fi

mkdir -p "$JOURNAL_CLOSED"

ENTRY_COUNT=$(find "$JOURNAL_CLOSED" -type f -name "*.md" 2>/dev/null | wc -l)

if [ $ENTRY_COUNT -eq 0 ]; then
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] No entries to consolidate" >> "$LOG"
  echo "✓ No JOURNAL entries"
  exit 0
fi

TOTAL_SUCCESS=0
for entry in "$JOURNAL_CLOSED"/*.md; do
  [ -f "$entry" ] || continue
  if grep -q "SUCCESS\|COMPLETED" "$entry"; then
    ((TOTAL_SUCCESS++))
  fi
done

SUCCESS_RATE=$((TOTAL_SUCCESS * 100 / ENTRY_COUNT))

echo "" >> "$MEMORY"
echo "## Consolidation: $(date +%Y-%m-%d)" >> "$MEMORY"
echo "- Phase: 2 (Auto-Consolidation)" >> "$MEMORY"
echo "- Entries processed: $ENTRY_COUNT" >> "$MEMORY"
echo "- Success rate: $SUCCESS_RATE%" >> "$MEMORY"
echo "- Timestamp: $(date +'%Y-%m-%d %H:%M:%S')" >> "$MEMORY"

echo "[$(date +'%Y-%m-%d %H:%M:%S')] PHASE 2: AUTO-CONSOLIDATION COMPLETE" >> "$LOG"
echo "✓ PHASE 2 complete: $ENTRY_COUNT entries ($SUCCESS_RATE% success)"
