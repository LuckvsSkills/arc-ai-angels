---
name: pre-deploy-security-gate
description: "Security gate voor website deploys. Voert volledige security scan uit, past hardening toe en geeft groen/geel/rood licht. VERPLICHT voor elke website deploy."
metadata: { "openclaw": { "emoji": "🔒" } }
---
# Pre-Deploy Security Gate

Gebruik deze skill voor elke website build die naar productie gaat.

## Uitvoering
```bash
python3 /home/prime/arc_ai_angels/agents/nero/workers/scan_template_security.py PROJECT_BRIEF.json
bash /home/prime/arc_ai_angels/agents/nero/workers/harden_deployment.sh /pad/naar/code
bash /home/prime/arc_ai_angels/agents/nero/workers/check_secrets.sh /pad/naar/code
```

## Status betekenis
- 🟢 GROEN — deploy goedgekeurd
- 🟡 GEEL — deploy mogelijk, fix warnings
- 🔴 ROOD — deploy geblokkeerd, los kritieke issues op

## Kritieke blockers
- Hardcoded secrets/tokens
- .env in repo
- Stripe live keys in code
- GitHub tokens in code
