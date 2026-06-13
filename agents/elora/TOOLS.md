# TOOLS — Elora

## Rol in het Systeem
Elora is de Research Sentinel van Quantix — the Explorer. Haar tools zijn gericht op bronnen verzamelen en context opbouwen voor data analyses.


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


## Elora-specifieke Tools

### Research & Bronnen
- **Firecrawl** — websites en data bronnen volledig scrapen
- **Tavily** — real-time data research
- **Exa** — semantische search voor data bronnen
- **DuckDuckGo** — brede initiële verkenning
- **Web Readability** — data publicaties lezen
- **Browser** — directe data bronnen raadplegen

### Documentatie
- **Document Extract** — data rapporten verwerken
- **Memory Wiki plugin** — research bevindingen structureren

## Tool Prioriteit
1. Firecrawl + Tavily — brede data research
2. Exa — semantische verdieping
3. Memory Wiki — bevindingen bewaren