#!/bin/bash
# HARNAS_OPENCLAW - PARALLEL Setup (FAST!)

BASE_PATH="/home/prime/arc_ai_angels"
CONFIG="$BASE_PATH/HARNAS_OPENCLAW/config/AGENTS_LIST.txt"
LOG_DIR="/tmp/harnas-jobs"
mkdir -p "$LOG_DIR"

CREATED=0
FAILED=0

# Phase definitions
PHASES=(
  "0 0 * * *:prep"
  "0 6 * * *:consolidate"
  "0 12 * * *:intelligent"
  "0 18 * * *:wrap-up"
)

create_job() {
  local agent="$1"
  local cron="$2"
  local task="$3"
  local job_name="HARNAS-$agent-$task"
  local log_file="$LOG_DIR/$agent-$task.log"
  
  openclaw cron add \
    --name "$job_name" \
    --agent "$agent" \
    --cron "$cron" \
    --message "{\"harnas\":{\"task\":\"$task\",\"agent\":\"$agent\"}}" \
    --session "isolated" \
    > "$log_file" 2>&1
}

export -f create_job
export LOG_DIR

echo "🚀 HARNAS_OPENCLAW PARALLEL SETUP"
echo "Creating 128 cron jobs in PARALLEL..."
echo ""

# Read agents and create jobs in parallel (8 at a time)
while IFS=' ' read -r agent_name agent_type agent_team; do
  [[ "$agent_name" =~ ^# ]] && continue
  [ -z "$agent_name" ] && continue

  for phase_info in "${PHASES[@]}"; do
    IFS=':' read -r cron_expr task_name <<< "$phase_info"
    
    # Run in background (max 8 parallel)
    create_job "$agent_name" "$cron_expr" "$task_name" &
    
    # Limit to 8 parallel jobs
    if (( $(jobs -r -p | wc -l) >= 8 )); then
      wait -n
    fi
  done
done < <(grep -v '^#' "$CONFIG" | grep -v '^$')

# Wait for all background jobs to finish
wait

echo ""
echo "=========================================="
echo "✅ HARNAS_OPENCLAW Setup Complete!"
echo "=========================================="
echo ""
echo "Verify:"
openclaw cron list | grep HARNAS | wc -l

