#!/bin/bash
# system_monitor.sh — Nero worker
# Bewaakt het ARC AI Agents systeem
echo "🛡️ Nero Systeem Monitor: $(date)"
echo "================================"

# Service checks
echo ""
echo "📡 SERVICE STATUS:"
services=("50506:OpenClaw" "4000:LiteLLM" "8000:MCC-Backend" "3002:Vite")
for svc in "${services[@]}"; do
    port="${svc%%:*}"
    name="${svc##*:}"
    if curl -s --connect-timeout 2 http://localhost:$port > /dev/null 2>&1; then
        echo "  ✅ $name (poort $port)"
    else
        echo "  ❌ $name (poort $port) — NIET BEREIKBAAR"
    fi
done

# Config hash check
echo ""
echo "🔐 CONFIG BEWAKING:"
OC_HASH=$(md5sum ~/.openclaw/openclaw.json 2>/dev/null | cut -d' ' -f1)
ENV_HASH=$(md5sum ~/.openclaw/.env 2>/dev/null | cut -d' ' -f1)
HASH_FILE="/home/prime/arc_ai_angels/agents/nero/workers/.config_hashes"

if [ -f "$HASH_FILE" ]; then
    OLD_OC=$(grep "openclaw:" "$HASH_FILE" | cut -d: -f2)
    OLD_ENV=$(grep "env:" "$HASH_FILE" | cut -d: -f2)
    if [ "$OC_HASH" = "$OLD_OC" ]; then
        echo "  ✅ openclaw.json — ongewijzigd"
    else
        echo "  ⚠️  openclaw.json — GEWIJZIGD"
    fi
    if [ "$ENV_HASH" = "$OLD_ENV" ]; then
        echo "  ✅ .env — ongewijzigd"
    else
        echo "  ⚠️  .env — GEWIJZIGD"
    fi
fi
echo "openclaw:$OC_HASH" > "$HASH_FILE"
echo "env:$ENV_HASH" >> "$HASH_FILE"

# Disk check
echo ""
echo "💾 DISK GEBRUIK:"
df -h /home/prime | tail -1 | awk '{print "  Gebruikt: "$3" / "$2" ("$5" vol)"}'

# Cron job errors
echo ""
echo "⏰ CRON STATUS:"
ERROR_COUNT=$(openclaw cron list 2>/dev/null | grep -c "error" || echo "0")
TOTAL=$(openclaw cron list 2>/dev/null | grep -c "cron" || echo "0")
echo "  Jobs: $TOTAL totaal, $ERROR_COUNT errors"

echo ""
echo "================================"
echo "✅ Systeem monitor voltooid"
