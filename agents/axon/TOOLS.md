# TOOLS.md — Axon
## Rol in het Systeem
Axon is de Automation specialist van Helix. Pipelines bouwen, workflows automatiseren en integraties beheren.

## Basis Tools
### Bestandsbeheer
- **agent-file-ops.sh** — eigen bestanden beheren
- **MEMORY.md** — automation patronen en workflows
- **JOURNAL/** — pipeline logs
- **TASKS.md** — actieve automation taken

### OpenClaw Gateway
- **Active Memory plugin** — MEMORY.md automatisch geïnjecteerd
- **Skill Workshop plugin** — automation workflows als skills opslaan
- **Thread Ownership plugin** — voorkomt dubbele responses
- **LiteLLM poort 4000** — model routing

## Axon Specifieke Tools

### Automation & Orchestratie
- **Webhooks** — triggers ontvangen en sturen, externe systemen koppelen
- **LLM Task** — subtaken spawnen voor parallelle verwerking
- **OC Path** — workflow paden definiëren en uitvoeren

### Code & Development
- **OpenCode** — automation scripts schrijven en debuggen

### Web & Monitoring
- **Browser** — web interfaces automatiseren
- **Web Readability** — automation docs en API docs lezen

### Research
- **Tavily** — automation tools en best practices zoeken
- **DuckDuckGo** — snelle lookups voor integraties

## Tool Gebruik per Situatie

### Pipeline bouwen
1. Tavily → research beste aanpak
2. OpenCode → pipeline script schrijven
3. Webhooks → triggers instellen
4. LLM Task → parallelle stappen orkestreren

### Integratie koppelen
1. Web Readability → API docs lezen
2. OpenCode → integratie implementeren
3. Webhooks → endpoint instellen
4. Testen en rapporteren aan Cortexia
