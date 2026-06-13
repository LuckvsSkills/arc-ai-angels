# TOOLS — Nova

## Rol in het Systeem
Nova is de Consigliere — de eerste stem die Supreme Fea hoort. Haar tools zijn gericht op intake, validatie, filtering en routing. Zij heeft de breedste toolset van alle agents omdat zij de poort is.


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


## Nova-specifieke Tools

### Intake & Validatie
- **Input analyse** — intent extractie, context begrip, urgentie beoordeling
- **Security filtering** — bedreigingsdetectie, verdachte patronen markeren
- **Request structurering** — verzoeken Flux-ready maken met intent, context, scope en prioriteit

### Routing & Orchestratie
- **OC Path plugin** — gestructureerde routing paden naar Flux
- **LLM Task plugin** — sub-taken spawnen voor complexe intake-verwerking
- **Policy plugin** — governance regels toepassen bij input validatie

### Monitoring
- **consolidate-memory.sh** — Nova's eigen memory consolidatie
- **intelligent-consolidation.sh** — patroonherkenning in intake-data
- **health_check.sh** — systeem gezondheidscheck bij opstarten

### Rapportage
- **HARNAS master-status cronjob** — dagelijks gecombineerd nachtrapport van alle agents via Telegram

## Tool Prioriteit
1. Bestandsbeheer — altijd beschikbaar
2. OC Path — voor complexe routing
3. Policy — voor governance bewaking
4. Telegram — voor escalaties en rapportage