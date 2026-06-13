#!/bin/bash

# CONSOLIDATE MEMORY SCRIPT
# Agents call this to consolidate daily learnings
# Usage: consolidate-memory.sh <agent>

AGENT=$1
AGENT_PATH="/home/prime/arc_ai_angels/agents/$AGENT"
JOURNAL_CLOSED="$AGENT_PATH/JOURNAL/closed"
MEMORY="$AGENT_PATH/MEMORY.md"
CONSOLIDATION_LOG="$AGENT_PATH/consolidation.log"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Verify agent exists
if [ ! -d "$AGENT_PATH" ]; then
  echo "ERROR: Agent $AGENT not found"
  exit 1
fi

# Create directories if needed
mkdir -p "$JOURNAL_CLOSED"
mkdir -p "$(dirname "$MEMORY")"

echo "[$TIMESTAMP] Starting consolidation for $AGENT..." >> "$CONSOLIDATION_LOG"

# STEP 1: Check if there are any closed entries
if [ ! "$(ls -A $JOURNAL_CLOSED)" ]; then
  echo "[$TIMESTAMP] No entries to consolidate" >> "$CONSOLIDATION_LOG"
  exit 0
fi

# STEP 2: Extract learnings from each JOURNAL entry
echo "[$TIMESTAMP] Extracting learnings from JOURNAL entries..." >> "$CONSOLIDATION_LOG"

TOTAL_TASKS=0
TOTAL_SUCCESS=0
TOTAL_TIME=0
LEARNINGS=""

for journal_file in "$JOURNAL_CLOSED"/*.md; do
  if [ -f "$journal_file" ]; then
    ((TOTAL_TASKS++))
    
    # Extract success indicator
    if grep -q "SUCCESS" "$journal_file"; then
      ((TOTAL_SUCCESS++))
    fi
    
    # Extract timing information
    TIME_LINE=$(grep -oP '(?<=[0-9]{2}:[0-9]{2} )[^:]+' "$journal_file" | tail -1)
    if [ ! -z "$TIME_LINE" ]; then
      TOTAL_TIME=$((TOTAL_TIME + 1))
    fi
    
    # Extract method if mentioned
    METHOD=$(grep -i "method" "$journal_file" | head -1 | sed 's/.*method[: ]*//i')
    if [ ! -z "$METHOD" ]; then
      LEARNINGS="$LEARNINGS\n- Method discovered: $METHOD"
    fi
  fi
done

# STEP 3: Calculate metrics
if [ $TOTAL_TASKS -gt 0 ]; then
  SUCCESS_RATE=$((TOTAL_SUCCESS * 100 / TOTAL_TASKS))
  AVG_TIME=$((TOTAL_TIME / TOTAL_TASKS))
  
  echo "[$TIMESTAMP] Consolidation metrics:" >> "$CONSOLIDATION_LOG"
  echo "  - Tasks processed: $TOTAL_TASKS" >> "$CONSOLIDATION_LOG"
  echo "  - Success rate: $SUCCESS_RATE%" >> "$CONSOLIDATION_LOG"
  echo "  - Average time: $AVG_TIME min" >> "$CONSOLIDATION_LOG"
fi

# STEP 4: Update MEMORY.md
if [ -f "$MEMORY" ]; then
  # Append consolidation summary
  echo "" >> "$MEMORY"
  echo "## Consolidation: $TIMESTAMP" >> "$MEMORY"
  echo "- Tasks today: $TOTAL_TASKS" >> "$MEMORY"
  echo "- Success rate: $SUCCESS_RATE%" >> "$MEMORY"
  if [ ! -z "$LEARNINGS" ]; then
    echo -e "$LEARNINGS" >> "$MEMORY"
  fi
else
  # Create new MEMORY file
  cat > "$MEMORY" << 'ENDMEM'
# MEMORY.md — Agent Learning Log

## Consolidation Cycle

This file grows as you learn from tasks.

ENDMEM
  echo "" >> "$MEMORY"
  echo "## Consolidation: $TIMESTAMP" >> "$MEMORY"
  echo "- Tasks today: $TOTAL_TASKS" >> "$MEMORY"
  echo "- Success rate: $SUCCESS_RATE%" >> "$MEMORY"
fi

# STEP 5: Archive old JOURNAL entries
ARCHIVE_DIR="$AGENT_PATH/JOURNAL/archive/$(date +%Y-%m-%d)"
mkdir -p "$ARCHIVE_DIR"

echo "[$TIMESTAMP] Archiving entries to $ARCHIVE_DIR..." >> "$CONSOLIDATION_LOG"

# Move closed entries to archive
for journal_file in "$JOURNAL_CLOSED"/*.md; do
  if [ -f "$journal_file" ]; then
    mv "$journal_file" "$ARCHIVE_DIR/"
  fi
done

# STEP 6: Log completion
echo "[$TIMESTAMP] Consolidation complete. Updated MEMORY.md, archived $TOTAL_TASKS entries." >> "$CONSOLIDATION_LOG"

echo "✓ Consolidation complete for $AGENT"
echo "  - Tasks: $TOTAL_TASKS"
echo "  - Success: $SUCCESS_RATE%"
echo "  - MEMORY updated"
echo "  - Entries archived"

