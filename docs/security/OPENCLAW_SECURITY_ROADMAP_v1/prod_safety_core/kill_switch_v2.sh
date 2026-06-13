#!/usr/bin/env bash
set -u

echo "================================="
echo "OPENCLAW INCIDENT KILL SWITCH V2"
echo "================================="

TS=$(date +"%Y%m%d_%H%M%S")
OUT="$HOME/arc_ai_angels/OPENCLAW_SECURITY_ROADMAP_v1/prod_safety_core/incident_$TS"
mkdir -p "$OUT"

echo "Saving incident evidence to:"
echo "$OUT"

echo
echo "=== SERVICE STATUS BEFORE ==="
{
  systemctl status openclaw-nova --no-pager || true
  systemctl status openclaw-flux --no-pager || true
  systemctl list-units --type=service | grep 'openclaw-agent@' || true
} > "$OUT/service_status_before.txt" 2>&1

echo
echo "=== JOURNAL SNAPSHOT ==="
journalctl -u openclaw-nova -n 100 --no-pager > "$OUT/journal_nova.txt" 2>&1 || true
journalctl -u openclaw-flux -n 100 --no-pager > "$OUT/journal_flux.txt" 2>&1 || true

echo
echo "=== HEALTH CHECK ==="
~/arc_ai_angels/OPENCLAW_SECURITY_ROADMAP_v1/prod_safety_core/runtime_health_check.sh > "$OUT/healthcheck.txt" 2>&1 || true

echo
echo "=== STOPPING NOVA/FLUX ==="
sudo systemctl stop openclaw-nova openclaw-flux || true

echo
echo "=== STOPPING ALL OPENCLAW AGENT SERVICES ==="
mapfile -t AGENT_UNITS < <(systemctl list-units --type=service --all --no-legend | awk '/openclaw-agent@/ {print $1}')
if [ "${#AGENT_UNITS[@]}" -gt 0 ]; then
  sudo systemctl stop "${AGENT_UNITS[@]}" || true
else
  echo "No openclaw-agent@ units found"
fi

echo
echo "=== STOPPING GATEWAY ==="
sudo pkill -f openclaw-gateway || true

echo
echo "=== LAST-RESORT PROCESS CONTAINMENT ==="
sudo pkill -f '/usr/local/bin/openclaw-agent-' || true
sudo pkill -f '/usr/local/lib/openclaw/agent_runner.sh' || true
sudo pkill -f '/usr/local/lib/openclaw/redact_stdout.py' || true

echo
echo "=== VERIFY STOP ==="
ps -ef | grep openclaw | grep -v grep > "$OUT/processes_after.txt" || true
if [ -s "$OUT/processes_after.txt" ]; then
  cat "$OUT/processes_after.txt"
else
  echo "All OpenClaw processes stopped"
fi

echo
echo "Incident snapshot stored at:"
echo "$OUT"

echo
echo "KILL SWITCH V2 COMPLETE"
