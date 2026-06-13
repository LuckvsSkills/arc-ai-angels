#!/bin/bash
# HARNAS_OPENCLAW - Creates 128 OpenClaw cron jobs
# Simplified version - works!

set -e

BASE_PATH="/home/prime/arc_ai_angels"
CONFIG="$BASE_PATH/HARNAS_OPENCLAW/config/AGENTS_LIST.txt"
LOG="/tmp/harnas-setup-$(date +%s).log"

echo "🚀 HARNAS_OPENCLAW SETUP - Creating 128 cron jobs"
echo "Log: $LOG"
echo ""

CREATED=0
FAILED=0

# Phase definitions: cron_expr|task_name
PHASES=(
  "0 0 * * *|prep"
  "0 6 * * *|consolidate"
  "0 12 * * *|intelligent"
  "0 18 * * *|wrap-up"
)

echo "[$(date)] Starting setup" >> "$LOG"

while IFS=' ' read -r agent_name agent_type agent_team; do
  [[ "$agent_name" =~ ^# ]] && continue
  [ -z "$agent_name" ] && continue

  for phase_info in "${PHASES[@]}"; do
    IFS='|' read -r cron_expr task_name <<< "$phase_info"
    
    JOB_NAME="HARNAS-$agent_name-$task_name"
    
    MSG="{\"harnas\":{\"task\":\"$task_name\",\"agent\":\"$agent_name\"}}"
    
    echo -n "Creating: $JOB_NAME... "
    
    if openclaw cron add \
      --name "$JOB_NAME" \
      --agent "$agent_name" \
      --cron "$cron_expr" \
      --message "$MSG" \
      --session "isolated" \
      >> "$LOG" 2>&1; then
      ((CREATED++))
      echo "✓"
    else
      ((FAILED++))
      echo "❌"
    fi
  done
done < <(grep -v '^#' "$CONFIG" | grep -v '^$')

echo ""
echo "=========================================="
echo "✅ HARNAS_OPENCLAW Setup Complete!"
echo "=========================================="
echo "Created: $CREATED / 128"
echo "Failed: $FAILED"
echo "Log: $LOG"
echo ""
echo "Verify: openclaw cron list | grep HARNAS | wc -l"

