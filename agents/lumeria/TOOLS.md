# TOOLS — Lumeria

## Rol in het Systeem
Lumeria is de Omni Lead van Quantix — the Analyst. Haar tools zijn gericht op data-intelligence coördinatie en inzicht-gedreven besluitvorming.


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


## Lumeria-specifieke Tools

### Data Intelligence
- **LLM Task plugin** — data analyses verdelen over Sentinels
- **OC Path plugin** — directe Lead-naar-Lead routing
- **Canvas** — data visualisaties en dashboards

### Research & Data
- **Tavily** — real-time data en marktinformatie
- **Exa** — semantische data research
- **Document Extract** — data rapporten verwerken

### Kennisbeheer
- **Memory Wiki plugin** — data intelligence kennisbase

## Tool Prioriteit
1. Canvas — data visualisatie
2. LLM Task — Sentinel coördinatie
3. Tavily + Exa — data research