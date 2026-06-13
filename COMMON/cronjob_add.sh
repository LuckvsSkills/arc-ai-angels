#!/bin/bash
# Safe cronjob creator - valideert VOOR toevoegen

TEMPLATE='
{
  "agentId": "AGENT_NAME",
  "name": "JOB_NAME",
  "enabled": true,
  "schedule": {
    "kind": "cron",
    "expr": "SCHEDULE_EXPR",
    "tz": "Europe/Amsterdam"
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "MESSAGE_HERE",
    "model": "google/gemini-2.5-flash"
  },
  "delivery": {
    "to": "openclaw-control-ui",
    "channel": "webchat",
    "mode": "announce"
  }
}
'

if [ $# -lt 4 ]; then
  echo "Usage: cronjob_add.sh AGENT NAME SCHEDULE MESSAGE"
  echo ""
  echo "Example:"
  echo "  cronjob_add.sh nova 'Nova Memory' '0 */6 * * *' 'Run memory pipeline'"
  echo ""
  echo "Schedule examples:"
  echo "  '0 7 * * 1' = Every Monday at 7:00"
  echo "  '0 */6 * * *' = Every 6 hours"
  echo "  'every 1d' = Every day"
  exit 1
fi

AGENT="$1"
NAME="$2"
SCHEDULE="$3"
MESSAGE="$4"

# Create job
JOB=$(echo "$TEMPLATE" | \
  sed "s/AGENT_NAME/$AGENT/g" | \
  sed "s/JOB_NAME/$NAME/g" | \
  sed "s/SCHEDULE_EXPR/$SCHEDULE/g" | \
  sed "s/MESSAGE_HERE/$MESSAGE/g")

echo "Job to be created:"
echo "$JOB" | jq .

echo ""
read -p "Create this cronjob? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  echo "Creating via Telegram @Nova_Lens_bot:"
  echo "openclaw cron add --agent $AGENT --name '$NAME' --schedule '$SCHEDULE' --message '$MESSAGE'"
  echo ""
  echo "Then send to @Nova_Lens_bot OR run:"
  echo "  openclaw cron add --json '$JOB'"
else
  echo "Cancelled"
  exit 1
fi
