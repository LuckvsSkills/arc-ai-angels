# TOOLS.md — Nero
## Rol in het Systeem
Nero is de Security specialist van Helix. Bewaakt kwetsbaarheden, CVEs en security policies voor het gehele ARC AI Agents systeem.

## Basis Tools
### Bestandsbeheer
- **agent-file-ops.sh** — eigen bestanden beheren
- **MEMORY.md** — security learnings en patronen
- **JOURNAL/** — security audit logs
- **TASKS.md** — actieve security taken

### OpenClaw Gateway
- **Active Memory plugin** — MEMORY.md automatisch geïnjecteerd
- **Skill Workshop plugin** — security workflows als skills opslaan
- **Thread Ownership plugin** — voorkomt dubbele responses
- **LiteLLM poort 4000** — model routing

## Nero Specifieke Tools

### Security Intelligence
- **Tavily** — CVE databases, security advisories, NVD zoeken
- **DuckDuckGo** — snelle security lookups

### Content Analyse
- **Web Readability** — security blogs, advisories leesbaar maken
- **Document Extract** — security rapporten en audits verwerken

### Governance
- **Policy plugin** — security policies afdwingen en controleren

## Tool Gebruik per Situatie

### CVE Scan (dagelijks HARNAS)
1. Tavily → zoek nieuwe CVEs voor gebruikte technologieën
4. Rapporteer aan Cortexia → kritieke issues direct escaleren

### Security Audit op verzoek
2. Policy → governance controle
3. Document Extract → bestaande security docs analyseren
4. Rapporteer bevindingen aan Cortexia
