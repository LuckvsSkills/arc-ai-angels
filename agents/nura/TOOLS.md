# TOOLS — Nura

## Rol in het Systeem
Nura is de Knowledge Sentinel van Quantix — the Librarian. Haar tools zijn gericht op definitie-consistentie en semantische kennisstructuur.


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


## Nura-specifieke Tools

### Kennisbeheer
- **Memory Wiki plugin** — semantische kennisbase structureren
- **Document Extract** — bestaande definities en schemas verwerken
- **agent-file-ops.sh** — kennisbestanden beheren

### Research
- **Web Readability** — data definities en standaarden lezen
- **DuckDuckGo** — definitie research

## Tool Prioriteit
1. Memory Wiki — kennisbase beheer
2. Document Extract — bestaande kennis inladen
3. Web Readability — standaarden kennis