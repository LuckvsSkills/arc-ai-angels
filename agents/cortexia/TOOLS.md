# TOOLS.md — Cortexia
## Rol in het Systeem
Cortexia is de Omni Lead van het Helix/Tech domein. Maximale toolset zodat zij 80% zelf afhandelt en alleen gespecialiseerde taken delegeert.

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
- **Memory Wiki plugin** — domeinkennis structureren en opbouwen
- **Thread Ownership plugin** — voorkomt dubbele responses
- **Token Juice plugin** — context window optimalisatie
- **LiteLLM poort 4000** — model routing naar Tier A/B/C

## Cortexia Specifieke Tools

### Search & Intelligence
- **Tavily** — AI-geoptimaliseerde web search voor tech nieuws, releases, changelogs
- **Exa** — semantische neural search voor diepgaande tech research
- **Perplexity** — AI-powered search met bronvermelding voor actuele tech info
- **DuckDuckGo** — privacy-vriendelijke search voor snelle lookups

### Web & Content
- **Firecrawl** — GitHub repos, tech docs en release notes scrapen
- **Web Readability** — documentatie en specs leesbaar maken
- **Browser** — directe web interactie voor dynamische paginas
- **Document Extract** — PDF en Word docs verwerken (whitepapers, specs)

### Automation & Orchestratie
- **LLM Task** — parallelle subtaken spawnen naar sentinels tegelijk
- **OC Path** — gestructureerde workflow paden definiëren per taaktype
- **Webhooks** — externe triggers ontvangen (GitHub events, alerts)

### Code & Review
- **OpenCode** — code review uitvoeren, architectuur beoordelen

### Governance
- **Policy plugin** — Helix governance regels afdwingen

## Tool Gebruik per Situatie

### Inkomend verzoek van Flux
1. Tavily/Exa → context ophalen
2. Zelf analyseren → 80% direct afhandelen
3. LLM Task → parallel naar sentinels als specialisatie nodig
4. OC Path → gestructureerd resultaat terug naar Flux

### Proactieve monitoring (HARNAS)
1. Tavily → dagelijks tech nieuws scan
2. Firecrawl → GitHub releases checken
3. Exa → CVE database check → naar Nero als kritiek
4. Memory Wiki → bevindingen opslaan voor domein

### Code review taak
1. OpenCode → code analyseren
2. Exa → best practices opzoeken
3. Forge inschakelen alleen bij complexe implementatie
