# TOOLS — Zion

## Rol in het Systeem
Zion is de Accounting Sentinel — the Keeper. Zijn tools zijn gericht op boekhoudkundige registratie en cijferconsistentie.


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


## Zion-specifieke Tools

### Boekhouding
- **Document Extract** — financiële documenten en facturen verwerken
- **agent-file-ops.sh** — boekhoudkundige registraties bijhouden

### Research
- **Web Readability** — boekhoudkundige standaarden lezen
- **DuckDuckGo** — accounting regelgeving opzoeken

## Tool Prioriteit
1. Document Extract — documenten verwerken
2. agent-file-ops — registraties bijhouden
3. Web Readability — standaarden kennis