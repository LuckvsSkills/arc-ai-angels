---
name: service-manager
description: "Beheer ARC AI Agents services — starten, stoppen, herstarten en monitoren."
metadata: { "openclaw": { "emoji": "⚙️" } }
---
# Service Manager

Gebruik deze skill voor het beheren van ARC AI Agents services.

## Services overzicht

| Service | Type | Poort | Commando |
|---------|------|-------|---------|
| OpenClaw Gateway | systemd | 50506 | systemctl --user start openclaw-gateway |
| LiteLLM Proxy | systemd | 4000 | systemctl --user start litellm |
| MCC Backend | process | 8000 | python3 -m app.main |
| Vite Frontend | process | 3002 | npx vite --port 3002 |
| Cloudflare Tunnel | process | - | cloudflared tunnel run |

## Service commando's

### OpenClaw Gateway
```bash
systemctl --user start openclaw-gateway
systemctl --user stop openclaw-gateway
systemctl --user restart openclaw-gateway
systemctl --user status openclaw-gateway
```

### LiteLLM
```bash
systemctl --user start litellm
systemctl --user restart litellm
journalctl --user -u litellm -f  # logs
```

### MCC Backend
```bash
pkill -f "app.main"
cd /home/prime/arc_ai_angels/mission_control/mcc-backend
nohup python3 -m app.main > /tmp/mcc-backend.log 2>&1 &
```

## Health check procedure
1. Ping elke service poort
2. Check systemd status
3. Check process lijst
4. Rapporteer status aan Cortexia

## Alerting regels
Escaleer naar Cortexia bij:
- Service down > 5 minuten
- Memory gebruik > 80%
- Disk gebruik > 90%
- Gateway unreachable
