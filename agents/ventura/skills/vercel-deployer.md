---
name: vercel-deployer
description: "Beheer Vercel deployments voor ARC AI Agents projecten — deploy, monitor en rollback."
metadata: { "openclaw": { "emoji": "▲" } }
---
# Vercel Deployer

Gebruik deze skill voor alle Vercel deployment operaties.

## Deployment workflow

### Stap 1 — Pre-deploy check
- Is de code in GitHub gepusht?
- Heeft Nero groen licht gegeven?
- Is Vercel token beschikbaar in .env?

### Stap 2 — Deploy commando
```bash
Ventura heeft maar 3 skills en 1 worker. Voor Infrastructure specialist is dat te weinig.
VENTURA ANALYSE:
HEEFT AL:
✅ healthcheck     — host security audit
✅ wiki-maintainer — kennisbase
✅ tmux            — terminal sessies
✅ health_check.sh — services checken (werkt!)

ONTBREEKT:
❌ vercel-deployer    — Vercel deployments beheren
❌ service-manager    — services starten/stoppen/monitoren
❌ infra-reporter     — rapporten aan Cortexia
❌ cloudflare-manager — DNS en tunnel beheer
bash# Skill 1 — vercel-deployer
cat > /home/prime/arc_ai_angels/agents/ventura/skills/vercel-deployer.md << 'EOF'
---
name: vercel-deployer
description: "Beheer Vercel deployments voor ARC AI Agents projecten — deploy, monitor en rollback."
metadata: { "openclaw": { "emoji": "▲" } }
---
# Vercel Deployer

Gebruik deze skill voor alle Vercel deployment operaties.

## Deployment workflow

### Stap 1 — Pre-deploy check
- Is de code in GitHub gepusht?
- Heeft Nero groen licht gegeven?
- Is Vercel token beschikbaar in .env?

### Stap 2 — Deploy commando
```bash
VERCEL_TOKEN=$(grep "^VERCEL_TOKEN" ~/.openclaw/.env | cut -d= -f2)
cd /pad/naar/project
vercel --token $VERCEL_TOKEN --prod --yes
```

### Stap 3 — Deploy verificatie
```bash
# Check of site bereikbaar is
curl -s -o /dev/null -w "%{http_code}" https://project.vercel.app
# Moet 200 teruggeven
```

### Stap 4 — Rapporteer aan Cortexia
DEPLOY RESULTAAT — [project]
URL: https://[project].vercel.app
Status: ✅ LIVE / ❌ FOUT
HTTP: [status code]
Tijd: [tijdstip]

## Rollback procedure
```bash
# Via Vercel dashboard of CLI
vercel rollback --token $VERCEL_TOKEN
```

## Vercel project management
```bash
# Lijst alle projecten
vercel list --token $VERCEL_TOKEN

# Project details
vercel inspect [project-naam] --token $VERCEL_TOKEN

# Verwijder deployment
vercel remove [deployment-url] --token $VERCEL_TOKEN
```

## Environment variables instellen
```bash
# Voeg env var toe aan Vercel project
vercel env add VARIABLE_NAME --token $VERCEL_TOKEN
```
