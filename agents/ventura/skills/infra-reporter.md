---
name: infra-reporter
description: "Maak gestructureerde infrastructure rapporten voor Cortexia."
metadata: { "openclaw": { "emoji": "📊" } }
---
# Infra Reporter

Gebruik deze skill voor alle rapportages aan Cortexia.

## Dagelijks infra rapport
VENTURA INFRA RAPPORT — [datum]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🟢 SERVICES STATUS:

OpenClaw Gateway: ✅ reachable
LiteLLM Proxy:    ✅ reachable
MCC Backend:      ✅ reachable
Vite Frontend:    ✅ reachable
Cloudflare:       ✅ actief

💾 SYSTEEM:

Disk: [n]% gebruikt
Memory: [n]% gebruikt
CPU: [n]% gemiddeld

▲ VERCEL DEPLOYMENTS:

Actieve projecten: [n]
Laatste deploy: [project] — [tijd]

⚠️ AANDACHTSPUNTEN:

[geen / beschrijving]

STATUS: [ALLES OK / AANDACHT NODIG]

## Deploy rapport
DEPLOY VOLTOOID — [project]
━━━━━━━━━━━━━━━━━━━━━━━━━━
URL: https://[url]
Status: ✅ LIVE
HTTP: 200
Deploy tijd: [seconden]s

## Incident rapport
🚨 INFRA INCIDENT
Service: [naam]
Status: DOWN
Sinds: [tijd]
Impact: [beschrijving]
Actie: [wat wordt gedaan]
