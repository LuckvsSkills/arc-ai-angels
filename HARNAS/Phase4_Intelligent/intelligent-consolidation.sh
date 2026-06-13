#!/bin/bash

# INTELLIGENT CONSOLIDATION SCRIPT
# Phase 4: Self-optimizing agents with pattern recognition
# Usage: intelligent-consolidation.sh <agent>

AGENT=$1
AGENT_PATH="/home/prime/arc_ai_angels/agents/$AGENT"
JOURNAL_CLOSED="$AGENT_PATH/JOURNAL/closed"
MEMORY="$AGENT_PATH/MEMORY.md"
INTELLIGENT_LOG="$AGENT_PATH/intelligent-consolidation.log"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Verify agent exists
if [ ! -d "$AGENT_PATH" ]; then
  echo "ERROR: Agent $AGENT not found"
  exit 1
fi

mkdir -p "$(dirname "$MEMORY")" "$JOURNAL_CLOSED"

echo "[$TIMESTAMP] Starting intelligent consolidation for $AGENT..." >> "$INTELLIGENT_LOG"

# ===== PHASE 3 FUNCTIONALITY (Consolidation) =====

# STEP 1: Count and analyze JOURNAL entries
TOTAL_TASKS=0
TOTAL_SUCCESS=0
TOTAL_TIME=0

for journal_file in "$JOURNAL_CLOSED"/*.md; do
  [ -f "$journal_file" ] || continue
  ((TOTAL_TASKS++))
  
  if grep -q "SUCCESS" "$journal_file"; then
    ((TOTAL_SUCCESS++))
  fi
done

if [ $TOTAL_TASKS -gt 0 ]; then
  SUCCESS_RATE=$((TOTAL_SUCCESS * 100 / TOTAL_TASKS))
else
  SUCCESS_RATE=0
fi

echo "[$TIMESTAMP] Base metrics: $TOTAL_TASKS tasks, $SUCCESS_RATE% success" >> "$INTELLIGENT_LOG"

# ===== PHASE 4 FUNCTIONALITY (Intelligence) =====

echo "[$TIMESTAMP] Starting intelligent analysis..." >> "$INTELLIGENT_LOG"

# STEP 2: Pattern Recognition
echo "Analyzing patterns..."

PATTERNS=""
SUCCESS_PATTERN=""
SPEED_PATTERN=""
QUALITY_PATTERN=""

# Detect success patterns
if [ $SUCCESS_RATE -gt 90 ]; then
  SUCCESS_PATTERN="High success rate ($SUCCESS_RATE%) - Current method working well"
  PATTERNS="$PATTERNS\n- Pattern: Current method successful ($SUCCESS_RATE%)"
elif [ $SUCCESS_RATE -gt 80 ]; then
  SUCCESS_PATTERN="Moderate success ($SUCCESS_RATE%) - Consider optimization"
  PATTERNS="$PATTERNS\n- Pattern: Method effective but can improve ($SUCCESS_RATE%)"
else
  SUCCESS_PATTERN="Low success ($SUCCESS_RATE%) - Needs improvement"
  PATTERNS="$PATTERNS\n- Pattern: Method needs review ($SUCCESS_RATE%)"
fi

# Detect performance patterns
if grep -q "parallel\|fast\|quick" "$JOURNAL_CLOSED"/*.md 2>/dev/null; then
  SPEED_PATTERN="Parallel processing detected - Effective for this agent"
  PATTERNS="$PATTERNS\n- Pattern: Parallel processing beneficial"
fi

if grep -q "error\|fail\|bottleneck" "$JOURNAL_CLOSED"/*.md 2>/dev/null; then
  QUALITY_PATTERN="Bottleneck detected - Optimization needed"
  PATTERNS="$PATTERNS\n- Pattern: Bottleneck in execution flow"
fi

echo "[$TIMESTAMP] Patterns detected: $PATTERNS" >> "$INTELLIGENT_LOG"

# STEP 3: Bottleneck Detection
echo "Detecting bottlenecks..."

BOTTLENECKS=""
if grep -q "validation\|check\|verify" "$JOURNAL_CLOSED"/*.md 2>/dev/null; then
  BOTTLENECKS="$BOTTLENECKS\n- Bottleneck: Validation step consumes resources"
fi

if [ ! -z "$BOTTLENECKS" ]; then
  echo "[$TIMESTAMP] Bottlenecks found: $BOTTLENECKS" >> "$INTELLIGENT_LOG"
fi

# STEP 4: Optimization Suggestions
echo "Generating optimization suggestions..."

SUGGESTIONS=""

if [ $SUCCESS_RATE -lt 95 ]; then
  SUGGESTIONS="$SUGGESTIONS\n- Suggestion: Improve success rate to 95%+ (currently $SUCCESS_RATE%)"
fi

if grep -q "parallel" "$JOURNAL_CLOSED"/*.md 2>/dev/null; then
  SUGGESTIONS="$SUGGESTIONS\n- Suggestion: Continue using parallel processing (+20% speed)"
fi

if [ $TOTAL_TASKS -gt 5 ]; then
  SUGGESTIONS="$SUGGESTIONS\n- Suggestion: Implement result caching (seen in tasks, could save time)"
fi

SUGGESTIONS="$SUGGESTIONS\n- Suggestion: Review failed tasks for patterns"

echo "[$TIMESTAMP] Optimization suggestions generated: $SUGGESTIONS" >> "$INTELLIGENT_LOG"

# STEP 5: Update MEMORY with Intelligence
echo "Updating MEMORY with intelligence..."

if [ -f "$MEMORY" ]; then
  echo "" >> "$MEMORY"
  echo "## Intelligent Consolidation: $TIMESTAMP" >> "$MEMORY"
  echo "### Patterns Discovered" >> "$MEMORY"
  echo -e "$PATTERNS" >> "$MEMORY"
  echo "" >> "$MEMORY"
  echo "### Bottlenecks Identified" >> "$MEMORY"
  if [ ! -z "$BOTTLENECKS" ]; then
    echo -e "$BOTTLENECKS" >> "$MEMORY"
  else
    echo "- No major bottlenecks detected" >> "$MEMORY"
  fi
  echo "" >> "$MEMORY"
  echo "### Optimization Suggestions" >> "$MEMORY"
  echo -e "$SUGGESTIONS" >> "$MEMORY"
  echo "" >> "$MEMORY"
  echo "### Performance Metrics" >> "$MEMORY"
  echo "- Success Rate: $SUCCESS_RATE%" >> "$MEMORY"
  echo "- Tasks Today: $TOTAL_TASKS" >> "$MEMORY"
  echo "- Intelligence Score: $(( (SUCCESS_RATE / 10) + (TOTAL_TASKS / 2) ))/20" >> "$MEMORY"
else
  cat > "$MEMORY" << 'ENDMEM'
# MEMORY.md — Intelligent Agent Learning

## Intelligent Consolidation System

This agent learns and optimizes automatically.

ENDMEM
  echo "" >> "$MEMORY"
  echo "## Intelligent Consolidation: $TIMESTAMP" >> "$MEMORY"
  echo "### Patterns" >> "$MEMORY"
  echo -e "$PATTERNS" >> "$MEMORY"
  echo "### Suggestions" >> "$MEMORY"
  echo -e "$SUGGESTIONS" >> "$MEMORY"
fi

# STEP 6: Archive and prepare for next cycle
ARCHIVE_DIR="$AGENT_PATH/JOURNAL/archive/$(date +%Y-%m-%d)"
mkdir -p "$ARCHIVE_DIR"

for journal_file in "$JOURNAL_CLOSED"/*.md; do
  [ -f "$journal_file" ] && mv "$journal_file" "$ARCHIVE_DIR/"
done

# STEP 7: Log completion
echo "[$TIMESTAMP] Intelligent consolidation complete. MEMORY updated with intelligence." >> "$INTELLIGENT_LOG"

echo "✓ Intelligent consolidation complete for $AGENT"
echo "  - Tasks analyzed: $TOTAL_TASKS"
echo "  - Success rate: $SUCCESS_RATE%"
echo "  - Patterns found: $(echo -e "$PATTERNS" | grep -c "Pattern:")"
echo "  - Suggestions: $(echo -e "$SUGGESTIONS" | grep -c "Suggestion:")"
echo "  - MEMORY intelligence level: UPDATED"

