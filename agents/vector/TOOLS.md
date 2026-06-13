# TOOLS — Vector

## Rol in het Systeem
Vector is de Finance Strategy Sentinel — de Navigator. Zijn tools zijn gericht op strategische financiële analyse, scenario modellering en beslissingsondersteuning.


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


## Vector-specifieke Tools

### Financiële Analyse
- **Perplexity** — AI-powered search voor financieel nieuws en marktinzichten
- **Exa** — semantische search voor strategische financiële informatie
- **Tavily** — real-time financiële data en nieuws
- **Web Readability** — financiële rapporten en analyses lezen

### Scenario Modellering
- **Canvas** — financiële scenario's en grafieken visualiseren
- **Document Extract** — financiële documenten en contracten analyseren

### Research
- **Firecrawl** — financiële websites en rapporten scrapen
- **DuckDuckGo** — brede financiële research

## Tool Prioriteit
1. Perplexity + Exa — diepgaande strategische research
2. Tavily — real-time marktdata
3. Canvas — scenario visualisatie
4. Document Extract — document analyse