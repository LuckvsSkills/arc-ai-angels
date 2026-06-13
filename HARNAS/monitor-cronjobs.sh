#!/bin/bash

# HARNAS CRONJOB MONITOR - Real-time monitoring

clear
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║        HARNAS CRONJOB MONITOR - LIVE STATUS               ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if logs directory exists
if [ ! -d "HARNAS/logs/cronjobs" ]; then
    echo "⚠️  HARNAS/logs/cronjobs directory NOT FOUND"
    echo "Create it with: mkdir -p HARNAS/logs/cronjobs"
    exit 1
fi

echo "📊 CRONJOB STATUS CHECK:"
echo ""

# Count total log files (one per agent per day)
TOTAL_LOGS=$(find HARNAS/logs/cronjobs -name "*.log" 2>/dev/null | wc -l)
echo "Total log files found: $TOTAL_LOGS"
echo ""

# Show recent cronjob executions
echo "📋 RECENT CRONJOB EXECUTIONS (last 20 lines across all logs):"
echo "─────────────────────────────────────────────────────────────"
find HARNAS/logs/cronjobs -name "*.log" -exec tail -5 {} \; 2>/dev/null | tail -20
echo ""

# Check specific agent logs
echo "🔍 AGENT-SPECIFIC CHECKS:"
echo "─────────────────────────────────────────────────────────────"

AGENTS=("nova" "flux" "flux_core" "cortexia" "saelia" "finoria" "lumeria" "fluentia")

for agent in "${AGENTS[@]}"; do
    AGENT_LOGS=$(find HARNAS/logs/cronjobs -name "*${agent}*" 2>/dev/null | wc -l)
    if [ $AGENT_LOGS -gt 0 ]; then
        echo "✅ $agent: $AGENT_LOGS execution(s)"
    else
        echo "⚠️  $agent: NO LOGS FOUND"
    fi
done
echo ""

# Check for errors
echo "⚠️  ERROR CHECK:"
echo "─────────────────────────────────────────────────────────────"
ERROR_COUNT=$(find HARNAS/logs -name "*error*" -o -name "*ERROR*" 2>/dev/null | wc -l)
if [ $ERROR_COUNT -gt 0 ]; then
    echo "Found $ERROR_COUNT error files"
    find HARNAS/logs -name "*error*" -o -name "*ERROR*" 2>/dev/null
else
    echo "No error files found"
fi
echo ""

# Crontab status
echo "⏰ CRONTAB STATUS:"
echo "─────────────────────────────────────────────────────────────"
CRON_AGENT_JOBS=$(crontab -l 2>/dev/null | grep -c "agent-cronjob" || echo "0")
echo "Agent cronjob entries in crontab: $CRON_AGENT_JOBS"
echo ""

echo "═════════════════════════════════════════════════════════════"
echo "Use 'tail -f HARNAS/logs/cronjobs/*.log' for real-time watch"

