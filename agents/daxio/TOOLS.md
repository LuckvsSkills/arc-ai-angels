# TOOLS — Daxio

## Rol in het Systeem
Daxio is de Signals Sentinel — the Detector. Zijn tools zijn gericht op signaaldetectie, afwijkingsherkenning en vroege waarschuwing.


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


## Daxio-specifieke Tools

### Signaal Detectie
- **Tavily** — real-time nieuws en signalen monitoren
- **Exa** — semantische search voor zwakke signalen
- **DuckDuckGo** — brede signaal monitoring
- **Web Readability** — signaal bronnen lezen

### Alerting
- **Telegram** — kritieke signalen direct escaleren naar Saelia
- **Webhooks** — externe signalen ontvangen

### Analyse
- **Canvas** — signaal patronen visualiseren

## Tool Prioriteit
1. Tavily — real-time signalen
2. Exa — semantische signaaldetectie
3. Telegram — kritieke escalaties
4. Webhooks — externe signaalinput