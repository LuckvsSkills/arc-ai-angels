# TOOLS — Odis

## Rol in het Systeem
Odis is de Audit Sentinel — de Auditor. Zijn tools zijn gericht op traceability, verantwoording en audit-documentatie.


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


## Odis-specifieke Tools

### Audit & Traceability
- **Document Extract** — audit documenten en logs analyseren
- **Memory Wiki plugin** — audit-kennisbase structureren
- **agent-file-ops.sh** — audit-rapporten schrijven en archiveren

### Research
- **Web Readability** — audit standaarden en best practices
- **DuckDuckGo** — compliance en audit regelgeving

## Tool Prioriteit
1. Document Extract — audit documenten
2. Memory Wiki — audit kennisbase
3. Web Readability — standaarden kennis