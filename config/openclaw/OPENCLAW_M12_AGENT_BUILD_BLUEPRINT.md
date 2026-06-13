# M12 — Agent Build Blueprint

## Scope
Dit document definieert de bouwblauwdruk voor agents binnen ARC / OpenClaw.

Doel:
- vastleggen hoe nieuwe agents gebouwd worden
- minimale baseline per agenttype definiëren
- structuur voor lead agents en workers standaardiseren
- uitbreiding van sentinels voorspelbaar maken

## 1. Bouwprincipes

Elke nieuwe agent moet:
- een duidelijke rol hebben
- een vaste plek in de architectuur hebben
- een minimale file-baseline krijgen
- onder governance van ARC / OpenClaw vallen
- uitbreidbaar blijven zonder de hoofdstructuur te breken

## 2. Agenttypen

We onderscheiden:

### A. Direct Interface Agents
Voorbeelden:
- Nova
- James
- Jim

Kenmerken:
- direct menscontact
- intake
- terugkoppeling
- geen standaard workerteam nodig

### B. Central Intelligence
- Flux

Kenmerken:
- centrale intelligentie
- routing
- orchestration
- sentinelsturing
- integratie van resultaten

### C. Sentinel Lead AI Agents
Voorbeelden:
- Nero
- Sora
- Forge
- Clio

Kenmerken:
- domeineigenaar
- sturen workers aan
- bewaken domeinkwaliteit
- rapporteren aan Flux

### D. Workers
Voorbeelden:
- Prompt Defense Worker
- Web Research Worker
- Code Generation Worker
- Doc Cleanup Worker

Kenmerken:
- smalle subtaak
- parent-bound
- geen domeinbrede autonomie
- kostenbewuste uitvoering

## 3. Minimale baseline voor lead agents

Verplicht:
- AGENTS.md
- IDENTITY.md
- MEMORY.md
- SECURITY.md
- PROTOCOL.md
- SOUL.md
- TOOLS.md
- USER.md
- HEARTBEAT.md

Optioneel:
- SENTINEL.md
- LAYERS.md
- NETWORK_POLICY.md
- TASKS.md
- DEPLOYMENT.md
- ENVIRONMENT.md
- ALLOWLIST.md

## 4. Minimale baseline voor workers

Verplicht:
- AGENTS.md
- IDENTITY.md
- SECURITY.md
- PROTOCOL.md
- TOOLS.md

Optioneel:
- MEMORY.md
- HEARTBEAT.md
- TASKS.md

## 5. Directory blueprint

### Direct Interface Agent
arc_ai_angels/agents/<agent-name>/
- agent/
- runtime/
- workspace/

### Sentinel Lead Agent
arc_ai_angels/agents/<sentinel-name>/lead-<lead-name>/
- agent/
- runtime/
- workspace/

### Worker
arc_ai_angels/agents/<sentinel-name>/workers/<worker-name>/
- AGENTS.md
- IDENTITY.md
- SECURITY.md
- PROTOCOL.md
- TOOLS.md

## 6. Bouwflow voor nieuwe sentinel

Stap 1
Bepaal sentinel domein.

Stap 2
Kies lead AI agent.

Stap 3
Definieer workers.

Stap 4
Maak directorystructuur aan.

Stap 5
Genereer baseline files.

Stap 6
Voeg SENTINEL.md en LAYERS.md toe.

Stap 7
Registreer sentinel in registry.

Stap 8
Koppel sentinel aan Flux routinglogica.

## 7. Governance koppeling

Elke nieuwe agent moet gekoppeld zijn aan:
- model governance
- security governance
- protocol governance
- task routing
- Mission Control zichtbaarheid

## 8. Mission Control richting

Mission Control moet later kunnen tonen:
- agentnaam
- agenttype
- sentinelrelatie
- lead/worker relatie
- modelkeuze
- status
- enable/disable
- workspace health

## 9. Eerste referentie-implementaties

Reeds gebouwd als eerste blueprint-voorbeelden:
- Sentinel Security / Nero
- Sentinel Research / Sora
- Sentinel Engineering / Forge
- Sentinel Documentation / Clio

Deze vormen de referentie voor volgende sentinels.

## 10. Output van M12

M12 levert:
- agent build blueprint
- standaard buildflow
- baseline per agenttype
- basis voor schaalbare sentinel-uitbreiding


---

## Diagram

\`\`\`mermaid
flowchart TB
    A --> B
\`\`\`
