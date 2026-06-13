#!/usr/bin/env bash
set -u

echo "== OPENCLAW RUNTIME HEALTH CHECK =="

echo
echo "-- Services --"
for svc in openclaw-nova openclaw-flux; do
  state="$(systemctl is-active "$svc" 2>/dev/null || true)"
  echo "$svc: ${state:-unknown}"
done

echo
echo "-- Gateway Process --"
pgrep -af openclaw-gateway || echo "openclaw-gateway: not running"

echo
echo "-- Ports --"
ss -ltnp 2>/dev/null | grep 50506 || echo "port 50506: not listening"
ss -ltnp 2>/dev/null | grep 50509 || echo "port 50509: not listening"

echo
echo "-- Critical Files --"
for f in \
  "$HOME/.openclaw/.env" \
  "$HOME/.openclaw/openclaw.json"
do
  if [ -f "$f" ]; then
    echo "OK file: $f"
  else
    echo "MISSING file: $f"
  fi
done

echo
echo "-- Memory DBs --"
ls "$HOME/.openclaw/memory/"*.sqlite 2>/dev/null || echo "No sqlite memory DBs found"

echo
echo "-- Gatekeeper Paths --"
for d in \
  "$HOME/arc_ai_angels/gatekeeper/logs" \
  "$HOME/arc_ai_angels/gatekeeper/policies"
do
  if [ -d "$d" ]; then
    echo "OK dir: $d"
  else
    echo "MISSING dir: $d"
  fi
done

echo
echo "-- Capacity --"
df -h / "$HOME" 2>/dev/null || true
echo
free -h 2>/dev/null || true

echo
echo "== END HEALTH CHECK =="
