#!/bin/bash

# VERIFY HARNAS CRONJOB SETUP

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║        VERIFY CRONJOB SETUP FOR ALL AGENTS                ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check directory structure
echo "1️⃣  Directory Structure:"
echo "   Logs dir: $([ -d 'HARNAS/logs/cronjobs' ] && echo '✅ EXISTS' || echo '❌ MISSING')"
echo "   Phase scripts: $([ -f 'HARNAS/Phase2_CronjobAPI/agent-cronjob-ops.sh' ] && echo '✅ EXISTS' || echo '❌ MISSING')"
echo ""

# Check if cronjobs are in crontab
echo "2️⃣  Crontab Status:"
CRON_COUNT=$(crontab -l 2>/dev/null | grep -c "agent-cronjob" || echo "0")
echo "   Agent cronjob entries: $CRON_COUNT"
if [ "$CRON_COUNT" -eq 0 ]; then
    echo "   ⚠️  NO CRONJOBS FOUND - Need to setup!"
else
    echo "   ✅ Cronjobs found"
    echo ""
    echo "   Cronjob entries:"
    crontab -l 2>/dev/null | grep "agent-cronjob" | head -5
fi
echo ""

# Check if scripts are executable
echo "3️⃣  Script Permissions:"
echo "   agent-cronjob-ops.sh: $([ -x 'HARNAS/Phase2_CronjobAPI/agent-cronjob-ops.sh' ] && echo '✅ EXECUTABLE' || echo '❌ NOT EXECUTABLE')"
echo "   agent-cronjob-runner.sh: $([ -x 'HARNAS/Phase2_CronjobAPI/agent-cronjob-runner.sh' ] && echo '✅ EXECUTABLE' || echo '❌ NOT EXECUTABLE')"
echo ""

# Check latest logs
echo "4️⃣  Latest Execution Status:"
LATEST_LOG=$(find HARNAS/logs/cronjobs -name "*.log" -type f -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)
if [ -n "$LATEST_LOG" ]; then
    echo "   Latest log: $(basename $LATEST_LOG)"
    echo "   Content (last 3 lines):"
    tail -3 "$LATEST_LOG" | sed 's/^/   /'
else
    echo "   ⚠️  No logs found yet"
fi
echo ""

echo "═════════════════════════════════════════════════════════════"

