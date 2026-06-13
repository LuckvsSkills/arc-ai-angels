#!/bin/bash

# AGENT CRONJOB RUNNER
# Executes cronjob commands for agents
# Called by crontab at scheduled time

AGENT=$1
CRONJOB_ID=$2
COMMAND=$3
CRONJOB_LOG="/home/prime/arc_ai_angels/logs/cronjobs/$AGENT"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Create log entry
mkdir -p "$CRONJOB_LOG"

# Log execution
echo "[$TIMESTAMP] STARTED: $COMMAND" >> "$CRONJOB_LOG/$CRONJOB_ID.log"

# Execute command
if eval "$COMMAND"; then
  echo "[$TIMESTAMP] SUCCESS" >> "$CRONJOB_LOG/$CRONJOB_ID.log"
else
  echo "[$TIMESTAMP] FAILED" >> "$CRONJOB_LOG/$CRONJOB_ID.log"
fi

