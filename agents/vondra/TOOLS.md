# TOOLS — Vondra

## Rol in het Systeem
Vondra is de Signals Sentinel van Quantix — the Watcher. Haar tools zijn gericht op kansen en risico-indicatoren detecteren in data.


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


## Vondra-specifieke Tools

### Signaal Detectie
- **Tavily** — real-time data signalen monitoren
- **Exa** — semantische signaaldetectie in data
- **DuckDuckGo** — brede signaal monitoring
- **Webhooks** — externe data signalen ontvangen

### Visualisatie & Alerting
- **Canvas** — signaal patronen visualiseren
- **Telegram** — kritieke data-afwijkingen escaleren naar Lumeria

## Tool Prioriteit
1. Tavily — real-time signalen
2. Canvas — patroon visualisatie
3. Telegram — escalaties