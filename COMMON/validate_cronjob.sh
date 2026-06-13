#!/bin/bash
# Cronjob Validator - voorkomt delivery config errors

JOBS_FILE="$HOME/.openclaw/cron/jobs.json"

validate_cronjob() {
  local job_json="$1"
  local job_name=$(echo "$job_json" | grep -o '"name": "[^"]*' | cut -d'"' -f4)
  
  echo "Validating: $job_name"
  
  # Check 1: Delivery exists
  if ! echo "$job_json" | grep -q '"delivery"'; then
    echo "❌ ERROR: No delivery config in $job_name"
    return 1
  fi
  
  # Check 2: Valid delivery channel
  if echo "$job_json" | grep -q '"channel": "last"'; then
    echo "❌ ERROR: Invalid channel 'last' in $job_name"
    return 1
  fi
  
  # Check 3: Must have 'to' field
  if ! echo "$job_json" | grep -q '"to": "openclaw-control-ui"'; then
    echo "❌ ERROR: Missing 'to: openclaw-control-ui' in $job_name"
    return 1
  fi
  
  # Check 4: Must have 'channel' field
  if ! echo "$job_json" | grep -q '"channel": "webchat"'; then
    echo "❌ ERROR: Must use 'channel: webchat' in $job_name"
    return 1
  fi
  
  echo "✅ VALID: $job_name"
  return 0
}

# Run validation
jq '.jobs[] | @json' "$JOBS_FILE" | while read -r job; do
  validate_cronjob "$job" || exit 1
done

echo ""
echo "✅ ALL CRONJOBS VALID"
