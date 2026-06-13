# TOOLS — Luvia

## Rol in het Systeem
Luvia is de Forecasting Sentinel — the Prophet. Haar tools zijn gericht op voorspellingen, scenario-analyses en trendprojecties.


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


## Luvia-specifieke Tools

### Forecasting & Modellering
- **Canvas** — forecast modellen en scenario's visualiseren
- **Tavily** — real-time trend data ophalen
- **Exa** — historische patronen en precedenten zoeken
- **Perplexity** — AI-powered research voor forecast input

### Data Input
- **Document Extract** — historische data rapporten verwerken
- **Web Readability** — forecast publicaties lezen
- **DuckDuckGo** — brede trend research

## Tool Prioriteit
1. Canvas — scenario visualisatie
2. Tavily + Perplexity — trend data
3. Exa — historische patronen