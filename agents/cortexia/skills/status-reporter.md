---
name: status-reporter
description: "Maak gestructureerde status rapporten voor Flux over Helix domein activiteit."
metadata: { "openclaw": { "emoji": "📊" } }
---
# Status Reporter

Gebruik deze skill voor alle rapportages aan Flux.

## Dagelijks rapport formaat
HELIX DAGRAPPORT — [datum]
━━━━━━━━━━━━━━━━━━━━━━━━━
✅ VOLTOOID:

[taak 1]
[taak 2]

🔄 IN PROGRESS:

[taak] — [status] — [sentinel]

⚠️ BLOKKADES:

[blokkade] — [actie nodig]

📊 METRICS:

Projecten actief: [n]
Projecten voltooid: [n]
CVEs gevonden: [n]
Deploys: [n]

🎯 PRIORITEITEN MORGEN:

[prioriteit 1]
[prioriteit 2]


## Project completion rapport
PROJECT VOLTOOID — [naam]
━━━━━━━━━━━━━━━━━━━━━━━━━
Live URL: [url]
Tech stack: [stack]
Tijd: [duur]
Sentinels: [lijst]
Documentatie: [url of locatie]

## Urgente escalatie naar Flux
Escaleer direct bij:
- Kritieke CVE die productie raakt
- Deploy failure na 3 pogingen
- Cross-domain hulp nodig
- Budget/scope wijziging
