# TOOLS — Tharos

## Rol in het Systeem
Tharos is de Strategic Intelligence Sentinel — the Thinker. Zijn tools zijn gericht op strategische analyse, intelligence interpretatie en beslissingsimplicaties.


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


## Tharos-specifieke Tools

### Strategische Research
- **Perplexity** — AI-powered search voor strategische inzichten
- **Exa** — semantische search voor strategische intelligence
- **Tavily** — real-time strategisch nieuws
- **Firecrawl** — strategische rapporten en analyses scrapen

### Analyse & Visualisatie
- **Canvas** — strategische scenario's en frameworks visualiseren
- **Document Extract** — strategische documenten analyseren
- **Web Readability** — strategische publicaties lezen

## Tool Prioriteit
1. Perplexity + Exa — diepgaande strategische research
2. Firecrawl — rapporten scrapen
3. Canvas — scenario visualisatie