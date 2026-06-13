# TOOLS — Saelia

## Rol in het Systeem
Saelia is de Omni Lead van Matrix — de Oracle. Haar tools zijn gericht op intelligence coördinatie, patroonherkenning en diepgaande analyse.


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


## Saelia-specifieke Tools

### Intelligence Coördinatie
- **LLM Task plugin** — parallelle intelligence analyses verdelen
- **OC Path plugin** — directe Lead-naar-Lead routing
- **Exa** — semantische neural search voor intelligence

### Analyse
- **Perplexity** — AI-powered research met bronvermelding
- **Tavily** — real-time informatie
- **Document Extract** — rapporten en intelligence documenten

### Kennisbeheer
- **Memory Wiki plugin** — intelligence kennisbase structureren

## Tool Prioriteit
1. Exa + Perplexity — diepgaande intelligence
2. LLM Task — Sentinel coördinatie
3. Memory Wiki — kennisbeheer