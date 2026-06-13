# TOOLS — Finoria

## Rol in het Systeem
Finoria is de Omni Lead van Finix — de financieel regisseur. Haar tools zijn gericht op financiële coördinatie, risicoafbakening en domein-aansturing.


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


## Finoria-specifieke Tools

### Financieel Beheer
- **LLM Task plugin** — complexe financiële analyses verdelen over Sentinels
- **OC Path plugin** — directe Lead-naar-Lead routing bij financiële cross-domain vragen
- **Policy plugin** — financiële governance regels afdwingen

### Analyse & Rapportage
- **Document Extract** — financiële rapporten en contracten lezen
- **Web Readability** — financieel nieuws en marktinformatie

### Communicatie
- **Telegram** — grote financiële beslissingen escaleren naar Supreme Fea

## Tool Prioriteit
1. Policy — financiële governance
2. LLM Task — Sentinel coördinatie
3. Document Extract — financiële documenten
4. Telegram — escalaties