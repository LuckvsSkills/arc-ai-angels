# TOOLS — Flux

## Rol in het Systeem
Flux is de Underboss — de brain die orkestreert. Zijn tools zijn gericht op routing, projectbeheer, cross-domain coördinatie en governance handhaving.


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


## Flux-specifieke Tools

### Orchestratie
- **LLM Task plugin** — parallelle sub-agent taken spawnen voor complexe projecten
- **OC Path plugin** — gestructureerde routing paden naar Omni Leads
- **Thread Ownership plugin** — bewaakt dat cross-domain taken correct worden afgehandeld

### Governance
- **Policy plugin** — bewaakt dat alle routing beslissingen binnen de governance vallen
- **Approval Gates** — grote financiële, security en cross-domain acties vereisen expliciete goedkeuring

### Projectbeheer
- **TASKS.md** — overzicht van alle actieve projecten en hun status
- **JOURNAL/** — routing beslissingen met rationale gelogd

### Monitoring
- **health_check.sh** — systeem status check
- **agent-status.py** — status van alle 32 agents

## Tool Prioriteit
1. LLM Task — voor complexe multi-domain orchestratie
2. OC Path — voor gestructureerde routing
3. Policy — voor governance bewaking
4. Bestandsbeheer — voor project tracking