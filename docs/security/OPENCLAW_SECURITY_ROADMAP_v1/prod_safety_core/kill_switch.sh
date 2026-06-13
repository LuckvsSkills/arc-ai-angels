#!/usr/bin/env bash
set -u

echo "================================="
echo "OPENCLAW INCIDENT KILL SWITCH"
echo "================================="

TS=$(date +"%Y%m%d_%H%M%S")
OUT="$HOME/arc_ai_angels/OPENCLAW_SECURITY_ROADMAP_v1/prod_safety_core/incident_$TS"

mkdir -p "$OUT"

echo
echo "Saving incident evidence to:"
echo "$OUT"

echo
echo "=== SERVICE STATUS BEFORE ===" | tee "$OUT/service_status_before.txt"
systemctl status openclaw-nova --no-pager >> "$OUT/service_status_before.txt" 2>&1 || true
systemctl status openclaw-flux --no-pager >> "$OUT/service_status_before.txt" 2>&1 || true

echo
echo "=== JOURNAL SNAPSHOT ==="
journalctl -u openclaw-nova -n 100 --no-pager > "$OUT/journal_nova.txt" 2>&1 || true
journalctl -u openclaw-flux -n 100 --no-pager > "$OUT/journal_flux.txt" 2>&1 || true

echo
echo "=== HEALTH CHECK ==="
~/arc_ai_angels/OPENCLAW_SECURITY_ROADMAP_v1/prod_safety_core/runtime_health_check.sh > "$OUT/healthcheck.txt" 2>&1 || true

echo
echo "=== STOPPING SERVICES ==="

sudo systemctl stop openclaw-nova
sudo systemctl stop openclaw-flux

echo
echo "=== STOPPING GATEWAY ==="

pkill -f openclaw-gateway || true

echo
echo "=== VERIFY STOP ==="

pgrep -af openclaw || echo "All OpenClaw processes stopped"

echo
echo "Incident snapshot stored at:"
echo "$OUT"

echo
echo "KILL SWITCH COMPLETE"
