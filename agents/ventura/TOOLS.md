# TOOLS.md — Ventura
## Rol in het Systeem
Ventura is de Infrastructure specialist van Helix. Deploy beheer, systeem gezondheid en infrastructure monitoring.

## Basis Tools
### Bestandsbeheer
- **agent-file-ops.sh** — eigen bestanden beheren
- **MEMORY.md** — infra patronen en systeem status history
- **JOURNAL/** — deploy logs en systeem events
- **TASKS.md** — actieve infra taken

### OpenClaw Gateway
- **Active Memory plugin** — MEMORY.md automatisch geïnjecteerd
- **Skill Workshop plugin** — infra procedures als skills opslaan
- **Thread Ownership plugin** — voorkomt dubbele responses
- **Token Juice plugin** — context optimalisatie voor grote logs
- **LiteLLM poort 4000** — model routing

## Ventura Specifieke Tools

### Monitoring & Health
- **Webhooks** — health alerts en deploy triggers ontvangen
- **Browser** — monitoring dashboards bekijken

### Infrastructure Research
- **Web Readability** — infra docs en runbooks lezen
- **Tavily** — infra best practices en troubleshooting
- **DuckDuckGo** — snelle infra lookups

### Governance
- **Policy plugin** — infrastructure policies controleren
- **Token Juice** — grote log bestanden efficiënt verwerken

## Tool Gebruik per Situatie

### Dagelijkse health check (HARNAS)
1. health_check.sh uitvoeren
2. Webhooks → alerts checken
3. Rapporteer status aan Cortexia
4. Escaleer kritieke issues direct

### Deploy uitvoeren
1. Policy → pre-deploy checks
2. Webhooks → deploy trigger ontvangen
3. Browser → deploy status monitoren
4. Rapporteer resultaat aan Cortexia
