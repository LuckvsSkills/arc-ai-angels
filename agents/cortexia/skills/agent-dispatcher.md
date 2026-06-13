---
name: agent-dispatcher
description: "Stuur Helix sentinels aan via LLM Task en OC Path voor gecoördineerde taakuitvoering."
metadata: { "openclaw": { "emoji": "📡" } }
---
# Agent Dispatcher

Gebruik deze skill om sentinels aan te sturen voor specifieke taken.

## Wanneer parallel spawnen (LLM Task)
Spawn tegelijk wanneer taken onafhankelijk zijn:
- Forge (code) + Axon (database) → kunnen tegelijk
- Nero (security) → alleen NA code gereed
- Ventura (deploy) → alleen NA Nero groen licht
- Clio (docs) → alleen NA succesvolle deploy

## Dispatch formaat
Geef elke sentinel een duidelijke instructie:
Agent: forge
Taak: Bouw de frontend voor project X
Specs: [specs JSON]
Verwachte output: GitHub repo URL
Deadline: zo snel mogelijk
## Wachten op resultaat
Na dispatch via LLM Task:
1. Wacht op bevestiging van elke sentinel
2. Check TASKS.md voor voortgang updates
3. Bij blokkade: escaleer direct
4. Bij voltooiing: volgende fase starten

## OC Path voor sequentiële taken
Gebruik OC Path voor taken die op volgorde moeten:
1. Forge klaar → trigger Nero
2. Nero groen → trigger Ventura
3. Ventura deployed → trigger Clio

## Communicatie formaat terug naar Flux
Project: [naam]
Status: [voltooid/in progress/geblokkeerd]
Live URL: [url of pending]
Sentinels: forge ✅ | axon ✅ | nero ✅ | ventura ✅ | clio ⏳
Volgende stap: [wat er nog moet]
