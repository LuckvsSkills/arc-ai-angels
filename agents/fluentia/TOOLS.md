# TOOLS — Fluentia

## Rol in het Systeem
Fluentia is de Omni Lead van Zenix — the Voice. Haar tools zijn gericht op taal-coördinatie, toon-bewaking en communicatie-aansturing.


## Basis Tools (alle agents)

### Bestandsbeheer
- **agent-file-ops.sh** — lezen, schrijven, toevoegen en verwijderen van eigen bestanden
- **MEMORY.md** — geconsolideerde kennisbase, dagelijks bijgewerkt via HARNAS
- **JOURNAL/** — uitvoeringslogboeken per taak
- **TASKS.md** — voortgangsregistratie actieve en voltooide taken

### OpenClaw Gateway
- **Gateway poort 50506** — alle agent-communicatie loopt via OpenClaw
- **Active Memory plugin** — MEMORY.md automatisch geïnjecteerd bij elke sessie
- **Skill Workshop plugin** — herhaalbare workflows opslaan als skills
- **Thread Ownership plugin** — voorkomt dubbele responses

### Communicatie
- **Telegram** — statusberichten en escalaties naar Supreme Fea
- **LiteLLM poort 4000** — model routing naar Tier A/B/C modellen


## Fluentia-specifieke Tools

### Taal & Communicatie
- **LLM Task plugin** — parallelle tekst-taken verdelen over Sentinels
- **OC Path plugin** — directe Lead-naar-Lead routing
- **ElevenLabs** — voice output voor taal-gerelateerde taken

### Research & Inspiratie
- **Web Readability** — communicatie trends en best practices
- **Exa** — semantische search voor messaging strategieën
- **Tavily** — actuele communicatie en marketing nieuws

### Productie
- **Canvas** — communicatie overzichten en frameworks visualiseren
- **Document Extract** — bestaande communicatie materialen analyseren

## Tool Prioriteit
1. LLM Task — Sentinel coördinatie
2. ElevenLabs — voice output
3. Exa + Web Readability — taal research