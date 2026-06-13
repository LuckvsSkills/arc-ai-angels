---
name: cloud-deployer
description: "Deploy een website naar Vercel via GitHub. Maakt automatisch GitHub repo aan, pusht code en deployt naar Vercel. Gebruik na Nero groen licht."
metadata: { "openclaw": { "emoji": "🚀" } }
---
# Cloud Deployer

Gebruik deze skill voor elke website deploy na security goedkeuring.

## Volgorde
1. Nero geeft groen licht (security gate)
2. bash provision_cloud_service.sh PROJECT_BRIEF.json
3. bash setup_custom_domain.sh PROJECT_BRIEF.json (indien custom domein)
4. python3 monitor_live_site.py PROJECT_BRIEF.json

## Vereisten
- VERCEL_TOKEN in /home/prime/.openclaw/.env
- GITHUB_TOKEN in /home/prime/.openclaw/.env
- code_dir aanwezig in PROJECT_BRIEF.json

## Output
- Live URL: https://[naam].vercel.app
- GitHub repo: https://github.com/LuckvsSkills/[naam]
