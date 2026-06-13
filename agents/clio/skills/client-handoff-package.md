---
name: client-handoff-package
description: "Genereer een volledig client handoff package inclusief README, API docs, gebruikershandleiding, SOP en agent config. Gebruik na website oplevering door Ventura."
metadata: { "openclaw": { "emoji": "📦" } }
---
# Client Handoff Package

Gebruik na website deploy door Ventura.

## Uitvoering
```bash
python3 /home/prime/arc_ai_angels/agents/clio/workers/generate_client_handoff.py PROJECT_BRIEF.json
python3 /home/prime/arc_ai_angels/agents/clio/workers/generate_sop.py PROJECT_BRIEF.json
python3 /home/prime/arc_ai_angels/agents/clio/workers/onboard_website_agent.py PROJECT_BRIEF.json
```

## Output bestanden
- HANDOFF.md — gebruikershandleiding
- DEPLOYMENT.md — deployment instructies
- SOP.md — standaard procedures
- AGENT_CONFIG.md — website agent configuratie (indien van toepassing)
