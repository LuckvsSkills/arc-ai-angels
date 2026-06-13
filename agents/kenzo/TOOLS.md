# TOOLS — Kenzo

## Rol in het Systeem
Kenzo is de Controls Sentinel — de Watchman. Zijn tools zijn gericht op interne controles, validatie en financiële consistentiecheck.


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


## Kenzo-specifieke Tools

### Controles & Validatie
- **Document Extract** — financiële documenten en rapporten controleren
- **Policy plugin** — controle-regels en standaarden toepassen
- **agent-file-ops.sh** — controle-rapporten schrijven en archiveren

### Research
- **Web Readability** — accounting standaarden en regelgeving lezen
- **DuckDuckGo** — compliance informatie opzoeken

## Tool Prioriteit
1. Document Extract — documenten controleren
2. Policy — controle-standaarden
3. Web Readability — regelgeving kennis