# TOOLS — Arix

## Rol in het Systeem
Arix is de Research Sentinel — the Scholar. Zijn tools zijn gericht op grondig onderzoek, bronvalidatie en onderbouwde kennisopbouw.


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


## Arix-specifieke Tools

### Research & Bronnen
- **Exa** — semantische neural search voor diepgaand onderzoek
- **Perplexity** — AI-powered search met bronvermelding
- **Tavily** — real-time research data
- **Firecrawl** — websites en papers volledig scrapen
- **DuckDuckGo** — brede initiële research
- **Browser** — directe website interactie
- **Web Readability** — artikelen en papers leesbaar maken

### Documentatie
- **Document Extract** — PDFs en rapporten verwerken
- **Memory Wiki plugin** — research kennisbase opbouwen

## Tool Prioriteit
1. Exa + Perplexity — diepgaande onderbouwde research
2. Firecrawl — volledige content extractie
3. Tavily — real-time aanvulling
4. Memory Wiki — kennis bewaren