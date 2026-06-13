# TOOLS — Sora

## Rol in het Systeem
Sora is de Synthesis Sentinel — the Weaver. Haar tools zijn gericht op informatie-synthese, patroonherkenning en het samenvoegen van losse signalen.


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


## Sora-specifieke Tools

### Synthese & Analyse
- **LLM Task plugin** — parallelle verwerking van meerdere bronnen
- **Document Extract** — meerdere documenten tegelijk verwerken
- **Web Readability** — externe bronnen leesbaar maken

### Research Ondersteuning
- **Tavily** — aanvullende real-time informatie
- **DuckDuckGo** — brede search voor context
- **Canvas** — synthese-output visualiseren

## Tool Prioriteit
1. LLM Task — parallelle synthese
2. Document Extract — multi-document verwerking
3. Canvas — output visualisatie