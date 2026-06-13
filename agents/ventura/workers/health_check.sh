#!/bin/bash
echo "🏥 Health Check: $(date)"
for svc in "50506:OpenClaw" "4000:LiteLLM" "8000:MCC-Backend" "3002:Vite"; do
    port="${svc%%:*}"; name="${svc##*:}"
    if curl -s --connect-timeout 2 http://localhost:$port > /dev/null 2>&1; then
        echo "  ✅ $name"
    else
        echo "  ❌ $name — NIET BEREIKBAAR"
    fi
done
