#!/bin/bash

# Daily Consolidation Cronjob
# Runs every day at 06:00
# Purpose: Each agent consolidates learnings from yesterday into MEMORY

TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
LOG_FILE="/home/prime/arc_ai_angels/logs/consolidation-$(date +%Y%m%d).log"

echo "[$TIMESTAMP] Starting daily consolidation cronjob..." >> $LOG_FILE

# All 32 agents
AGENTS=(nova flux arix axon clio cortexia daxio draven elora enki finoria fluentia forge kairo kenzo kresta lumeria luvia nero nura odis orizon saelia solis sora tharos unia vector ventura vondra zena zion)

for agent in "${AGENTS[@]}"; do
  echo "[$TIMESTAMP] Consolidating $agent..." >> $LOG_FILE
  
  # Send consolidation message to agent
  openclaw agent --agent $agent --message "
    Daily Consolidation (06:00):
    
    1. Read all JOURNAL/closed/ entries from yesterday
    2. Extract learnings:
       - Success rates
       - Average timings
       - Methods that worked
       - Issues encountered
    3. Update MEMORY.md with learnings
    4. Archive yesterday's closed JOURNAL entries
    5. Report: Done
  " --json >> $LOG_FILE 2>&1
done

echo "[$TIMESTAMP] Daily consolidation complete" >> $LOG_FILE
