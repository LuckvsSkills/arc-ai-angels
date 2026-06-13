#!/bin/bash

# AGENT CRONJOB OPERATIONS LIBRARY
# Allows agents to manage their own cronjobs
# Usage: agent-cronjob-ops.sh <agent> <operation> [args]

AGENT=$1
OPERATION=$2
HARNAS_PATH="/home/prime/arc_ai_angels/HARNAS"
AGENT_PATH="/home/prime/arc_ai_angels/agents/$AGENT"
CRONJOB_LOG="/home/prime/arc_ai_angels/logs/cronjobs/$AGENT"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Create logs directory
mkdir -p "$CRONJOB_LOG"

# Verify agent exists
if [ ! -d "$AGENT_PATH" ]; then
  echo "ERROR: Agent $AGENT not found at $AGENT_PATH"
  exit 1
fi

# Cronjob metadata file
CRONJOB_META="$AGENT_PATH/cronjobs.json"

case $OPERATION in
  
  # SCHEDULE: schedule_cronjob <agent> <time> <command>
  schedule)
    TIME=$3
    COMMAND=$4
    CRONJOB_ID="cron-$(date +%s)"
    
    # Validate time format (HH:MM)
    if ! [[ $TIME =~ ^[0-9]{2}:[0-9]{2}$ ]]; then
      echo "ERROR: Invalid time format. Use HH:MM (e.g., 06:00)"
      exit 1
    fi
    
    # Create crontab entry
    HOUR=$(echo $TIME | cut -d: -f1)
    MINUTE=$(echo $TIME | cut -d: -f2)
    CRON_ENTRY="$MINUTE $HOUR * * * /home/prime/arc_ai_angels/HARNAS/Phase2_CronjobAPI/agent-cronjob-runner.sh $AGENT $CRONJOB_ID \"$COMMAND\" >> $CRONJOB_LOG/$CRONJOB_ID.log 2>&1"
    
    # Add to crontab
    (crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -
    
    # Log metadata
    echo "[$TIMESTAMP] Scheduled: $CRONJOB_ID at $TIME for command: $COMMAND" >> "$CRONJOB_LOG/schedule.log"
    
    echo "✓ Cronjob scheduled: $CRONJOB_ID at $TIME"
    echo "$CRONJOB_ID"
    ;;
  
  # TRIGGER: trigger_cronjob <agent> <cronjob_id>
  trigger)
    CRONJOB_ID=$3
    
    if [ ! -f "$CRONJOB_LOG/schedule.log" ]; then
      echo "ERROR: No cronjobs found for $AGENT"
      exit 1
    fi
    
    # Get command from schedule log
    COMMAND=$(grep "Scheduled: $CRONJOB_ID" "$CRONJOB_LOG/schedule.log" | grep -oP 'command: \K.*')
    
    if [ -z "$COMMAND" ]; then
      echo "ERROR: Cronjob $CRONJOB_ID not found"
      exit 1
    fi
    
    # Execute command
    eval "$COMMAND" >> "$CRONJOB_LOG/$CRONJOB_ID.log" 2>&1
    
    echo "✓ Cronjob triggered: $CRONJOB_ID"
    ;;
  
  # STATUS: check_cronjob_status <agent> <cronjob_id>
  status)
    CRONJOB_ID=$3
    
    if [ ! -f "$CRONJOB_LOG/schedule.log" ]; then
      echo "ERROR: No cronjobs found for $AGENT"
      exit 1
    fi
    
    # Check if cronjob exists in crontab
    if crontab -l | grep -q "$CRONJOB_ID"; then
      STATUS="active"
    else
      STATUS="inactive"
    fi
    
    # Get last run time
    if [ -f "$CRONJOB_LOG/$CRONJOB_ID.log" ]; then
      LAST_RUN=$(tail -1 "$CRONJOB_LOG/$CRONJOB_ID.log")
    else
      LAST_RUN="Never"
    fi
    
    echo "Status: $STATUS"
    echo "Last run: $LAST_RUN"
    ;;
  
  # LOGS: read_cronjob_logs <agent> <cronjob_id>
  logs)
    CRONJOB_ID=$3
    
    if [ ! -f "$CRONJOB_LOG/$CRONJOB_ID.log" ]; then
      echo "ERROR: No logs found for cronjob $CRONJOB_ID"
      exit 1
    fi
    
    cat "$CRONJOB_LOG/$CRONJOB_ID.log"
    ;;
  
  # DELETE: delete_cronjob <agent> <cronjob_id>
  delete)
    CRONJOB_ID=$3
    
    # Remove from crontab
    crontab -l | grep -v "$CRONJOB_ID" | crontab -
    
    echo "[$TIMESTAMP] Deleted: $CRONJOB_ID" >> "$CRONJOB_LOG/schedule.log"
    
    echo "✓ Cronjob deleted: $CRONJOB_ID"
    ;;
  
  # LIST: list_cronjobs <agent>
  list)
    if [ ! -f "$CRONJOB_LOG/schedule.log" ]; then
      echo "No cronjobs scheduled for $AGENT"
      exit 0
    fi
    
    echo "=== Cronjobs for $AGENT ==="
    grep "Scheduled:" "$CRONJOB_LOG/schedule.log" | sed 's/\[.*\] //' | tail -20
    ;;
  
  *)
    echo "ERROR: Unknown operation: $OPERATION"
    echo "Operations: schedule, trigger, status, logs, delete, list"
    exit 1
    ;;
esac

