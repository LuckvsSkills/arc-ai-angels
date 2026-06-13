#!/bin/bash

# HARNAS MONITORING DASHBOARD
# Real-time system health & performance tracking

HARNAS_PATH="/home/prime/arc_ai_angels/HARNAS"
AGENTS_PATH="/home/prime/arc_ai_angels/agents"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║           HARNAS MONITORING DASHBOARD                          ║"
echo "║           $TIMESTAMP                              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# ===== SECTION 1: CRONJOB STATUS =====
echo "📅 CRONJOB STATUS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

CRON_COUNT=$(crontab -l 2>/dev/null | grep -c "consolidate-memory" || echo "0")
echo "Active cronjobs: $CRON_COUNT"
echo "Expected: 128 (4 per agent × 32 agents)"

if [ $CRON_COUNT -eq 128 ]; then
  echo "Status: ✅ ALL CRONJOBS ACTIVE"
else
  echo "Status: ⚠️  WARNING - Missing cronjobs"
fi
echo ""

# ===== SECTION 2: AGENT HEALTH =====
echo "🏥 AGENT HEALTH CHECK"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

AGENTS_WITH_MEMORY=0
AGENTS_WITH_JOURNAL=0
AGENTS_WITH_LOGS=0

for agent_dir in "$AGENTS_PATH"/*/; do
  agent=$(basename "$agent_dir")
  [ -f "$agent_dir/MEMORY.md" ] && ((AGENTS_WITH_MEMORY++))
  [ -d "$agent_dir/JOURNAL/closed" ] && ((AGENTS_WITH_JOURNAL++))
  [ -f "$agent_dir/consolidation.log" ] && ((AGENTS_WITH_LOGS++))
done

echo "Agents with MEMORY.md:      $AGENTS_WITH_MEMORY/32"
echo "Agents with JOURNAL/closed: $AGENTS_WITH_JOURNAL/32"
echo "Agents with consolidation logs: $AGENTS_WITH_LOGS/32"

if [ $AGENTS_WITH_MEMORY -eq 32 ] && [ $AGENTS_WITH_JOURNAL -eq 32 ]; then
  echo "Status: ✅ ALL AGENTS HEALTHY"
else
  echo "Status: ⚠️  WARNING - Some agents incomplete"
fi
echo ""

# ===== SECTION 3: MEMORY GROWTH =====
echo "📈 MEMORY GROWTH ANALYSIS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "Top 5 agents by MEMORY size:"
ls -lhS "$AGENTS_PATH"/*/MEMORY.md 2>/dev/null | head -5 | awk '{print $9, "(" $5 ")"}'
echo ""

# ===== SECTION 4: CONSOLIDATION ACTIVITY =====
echo "🔄 CONSOLIDATION ACTIVITY (Last 24h)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

TOTAL_CONSOLIDATIONS=0
for log_file in "$AGENTS_PATH"/*/consolidation.log; do
  [ -f "$log_file" ] && TOTAL_CONSOLIDATIONS=$(( TOTAL_CONSOLIDATIONS + $(wc -l < "$log_file") ))
done

echo "Total consolidation entries: $TOTAL_CONSOLIDATIONS"
echo ""

# ===== SECTION 5: SUCCESS RATES =====
echo "✅ SUCCESS METRICS (Sample agents)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

for agent in nova arix cortexia; do
  MEMORY="$AGENTS_PATH/$agent/MEMORY.md"
  if [ -f "$MEMORY" ]; then
    SUCCESS=$(grep -i "success rate" "$AGENTS_PATH/$agent/consolidation.log" 2>/dev/null | tail -1 || echo "Not found")
    echo "$agent: $SUCCESS"
  fi
done
echo ""

# ===== SECTION 6: LATEST ACTIVITY =====
echo "⏱️  LATEST ACTIVITY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "Last consolidations:"
for log_file in "$AGENTS_PATH"/*/consolidation.log; do
  [ -f "$log_file" ] || continue
  agent=$(basename $(dirname "$log_file"))
  last_entry=$(tail -1 "$log_file")
  echo "  $agent: $last_entry"
done | head -5
echo ""

# ===== SECTION 7: SYSTEM STATUS =====
echo "🎯 SYSTEM STATUS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $AGENTS_WITH_MEMORY -eq 32 ] && [ $CRON_COUNT -eq 128 ]; then
  echo "✅ HARNAS SYSTEM: FULLY OPERATIONAL"
  echo "✅ All 32 agents active"
  echo "✅ All 128 cronjobs scheduled"
  echo "✅ Consolidation running automatically"
else
  echo "⚠️  HARNAS SYSTEM: NEEDS ATTENTION"
fi
echo ""

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  Dashboard generated: $TIMESTAMP                   ║"
echo "╚════════════════════════════════════════════════════════════════╝"

