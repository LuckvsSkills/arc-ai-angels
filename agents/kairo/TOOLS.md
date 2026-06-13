# TOOLS — Kairo

## Rol in het Systeem
Kairo is de Treasury Sentinel — de Treasurer. Zijn tools zijn gericht op liquiditeitsbewaking, cashflow monitoring en treasury-afwijkingen detecteren.


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


## Kairo-specifieke Tools

### Treasury Monitoring
- **Tavily** — real-time financiële marktdata en rentetarieven
- **Web Readability** — treasury rapporten en financieel nieuws
- **DuckDuckGo** — brede treasury research

### Rapportage
- **Canvas** — cashflow grafieken en treasury dashboards
- **Document Extract** — treasury documenten en contracten verwerken

### Alerting
- **Telegram** — treasury afwijkingen direct melden aan Finoria

## Tool Prioriteit
1. Tavily — real-time marktdata
2. Canvas — treasury visualisatie
3. Telegram — afwijkings-alerts