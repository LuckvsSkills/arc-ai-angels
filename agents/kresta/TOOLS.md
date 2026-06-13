# TOOLS — Kresta

## Rol in het Systeem
Kresta is de Analytics Sentinel — the Interpreter. Haar tools zijn gericht op data analyse, patroonextractie en onderbouwde inzichten.


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


## Kresta-specifieke Tools

### Data Analyse
- **Canvas** — data patronen en trends visualiseren
- **Document Extract** — data rapporten en datasets verwerken
- **Tavily** — aanvullende data en benchmarks opzoeken

### Research
- **Exa** — semantische search voor analytische inzichten
- **Web Readability** — analytische publicaties lezen
- **DuckDuckGo** — brede data research

## Tool Prioriteit
1. Canvas — data visualisatie
2. Document Extract — data verwerking
3. Exa + Tavily — aanvullende research