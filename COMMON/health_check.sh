#!/bin/bash
# System Health Check - Comprehensive Status Report

set -e

echo "🏥 SYSTEM HEALTH CHECK"
echo "===================="
echo ""
timestamp=$(date '+%Y-%m-%d %H:%M:%S')
echo "Check time: $timestamp"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

status_ok() { echo -e "${GREEN}✅${NC} $1"; }
status_fail() { echo -e "${RED}❌${NC} $1"; }
status_warn() { echo -e "${YELLOW}⚠️${NC} $1"; }

# Track overall status
FAILED=0

echo "1. OpenClaw Gateway"
echo "==================="
if curl -s http://127.0.0.1:50506/health > /dev/null 2>&1; then
  status_ok "Gateway reachable (127.0.0.1:50506)"
else
  status_fail "Gateway NOT reachable"
  FAILED=$((FAILED + 1))
fi

# Check agents
agent_count=$(jq '.agents | length' /home/prime/.openclaw/openclaw.json 2>/dev/null || echo "0")
status_ok "Agents bootstrapped: $agent_count/32"

# Check cronjobs
cronjob_count=$(jq '.jobs | length' /home/prime/.openclaw/cron/jobs.json 2>/dev/null || echo "0")
status_ok "Cronjobs configured: $cronjob_count"

echo ""
echo "2. MCC Backend"
echo "=============="
if curl -s http://127.0.0.1:8000/api/health > /dev/null 2>&1; then
  status_ok "Backend responding"
else
  status_fail "Backend NOT responding"
  FAILED=$((FAILED + 1))
fi

echo ""
echo "3. MCC Frontend"
echo "==============="
if curl -s http://localhost:3003 > /dev/null 2>&1; then
  status_ok "Frontend responding"
else
  status_fail "Frontend NOT responding"
  FAILED=$((FAILED + 1))
fi

echo ""
echo "4. Configuration"
echo "================"
if [ -f /home/prime/.openclaw/openclaw.json ]; then
  if jq empty /home/prime/.openclaw/openclaw.json 2>/dev/null; then
    status_ok "OpenClaw config: valid JSON"
    binding=$(jq -r '.gateway.bind' /home/prime/.openclaw/openclaw.json 2>/dev/null || echo "unknown")
    status_ok "Binding: $binding"
  else
    status_fail "OpenClaw config: invalid JSON"
    FAILED=$((FAILED + 1))
  fi
else
  status_fail "OpenClaw config: NOT FOUND"
  FAILED=$((FAILED + 1))
fi

if [ -f /home/prime/arc_ai_angels/mission_control/mcc-backend/.env ]; then
  if grep -q "GOOGLE_REDIRECT_URI" /home/prime/arc_ai_angels/mission_control/mcc-backend/.env; then
    status_ok "MCC OAuth config: present"
  else
    status_warn "MCC OAuth config: missing GOOGLE_REDIRECT_URI"
  fi
else
  status_fail "MCC .env: NOT FOUND"
  FAILED=$((FAILED + 1))
fi

echo ""
echo "5. Network"
echo "=========="
if netstat -tlnp 2>/dev/null | grep -q "50506"; then
  status_ok "Port 50506: in use (OpenClaw)"
else
  status_fail "Port 50506: NOT listening"
  FAILED=$((FAILED + 1))
fi

if netstat -tlnp 2>/dev/null | grep -q "3003"; then
  status_ok "Port 3003: in use (MCC Frontend)"
else
  status_fail "Port 3003: NOT listening"
  FAILED=$((FAILED + 1))
fi

if netstat -tlnp 2>/dev/null | grep -q "8000"; then
  status_ok "Port 8000: in use (MCC Backend)"
else
  status_fail "Port 8000: NOT listening"
  FAILED=$((FAILED + 1))
fi

echo ""
echo "6. Processes"
echo "============"
if pgrep -f "openclaw.*gateway" > /dev/null; then
  status_ok "OpenClaw process: running"
else
  status_fail "OpenClaw process: NOT running"
  FAILED=$((FAILED + 1))
fi

if pgrep -f "vite.*3003" > /dev/null; then
  status_ok "MCC Frontend process: running"
else
  status_fail "MCC Frontend process: NOT running"
  FAILED=$((FAILED + 1))
fi

if pgrep -f "app.main" > /dev/null; then
  status_ok "MCC Backend process: running"
else
  status_fail "MCC Backend process: NOT running"
  FAILED=$((FAILED + 1))
fi

echo ""
echo "===================="
if [ $FAILED -eq 0 ]; then
  echo -e "${GREEN}✅ ALL SYSTEMS OPERATIONAL${NC}"
  exit 0
else
  echo -e "${RED}❌ $FAILED ISSUE(S) FOUND${NC}"
  echo ""
  echo "SUGGESTIONS:"
  echo "  1. Run: /home/prime/arc_ai_angels/COMMON/startup_all.sh"
  echo "  2. Check logs: tail -50 /tmp/openclaw.log"
  echo "  3. Check config: cat ~/.openclaw/openclaw.json | jq"
  exit 1
fi
