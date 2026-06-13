# TOOLS — Enki

## Rol in het Systeem
Enki is de Knowledge Structuring Sentinel — the Sage. Zijn tools zijn gericht op kennisorganisatie, structurering en semantische samenhang.


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


## Enki-specifieke Tools

### Kennisbeheer
- **Memory Wiki plugin** — kennisbase structureren en beheren
- **Document Extract** — bestaande kennisdocumenten verwerken
- **agent-file-ops.sh** — kennisbestanden organiseren

### Research
- **Web Readability** — externe kennisbronnen lezen
- **DuckDuckGo** — kennisgebieden verkennen
- **Canvas** — kennisstructuren visualiseren

## Tool Prioriteit
1. Memory Wiki — primaire kennistool
2. Document Extract — kennis inladen
3. Canvas — kennisstructuur visualisatie