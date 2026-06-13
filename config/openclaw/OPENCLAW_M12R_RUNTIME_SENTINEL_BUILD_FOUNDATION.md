# M12r — Runtime & Sentinel Build Foundation

## Scope
Dit document beschrijft de gecorrigeerde build foundation voor ARC / OpenClaw op basis van de live omgeving.

Belangrijke uitgangspunten:
- Flux is de centrale intelligentie van het systeem
- Nova is een direct interface AI agent
- Sentinels zijn domeinstructuren
- Elke sentinel bevat een Lead AI agent, workers, layers, skills en policies
- Nieuwe sentinels moeten aansluiten op de bestaande Nova/Flux runtime-structuur

## 1. Top-level AI structuur

Operator
- praat direct met:
  - Nova
  - James
  - Jim
- complexe en domein-overstijgende sturing loopt uiteindelijk via Flux

Flux:
- centrale intelligentie
- verdeelt taken
- bewaakt voortgang
- combineert resultaten
- stuurt sentinels aan

## 2. Direct Interface Agents

Direct Interface Agents zijn geen sentinels.

Voor nu:
- Nova
- James
- Jim

Kenmerken:
- direct menscontact
- intake / begeleiding / terugkoppeling
- leiden niet per definitie een workerteam
- kunnen later beperkt uitbreiden, maar dat is niet het uitgangspunt

## 3. Sentinel definitie

Een Sentinel is een AI domeincluster.

Naamstructuur:
- Sentinel + Domein

Voorbeelden:
- Sentinel Security
- Sentinel Research
- Sentinel Engineering
- Sentinel Multimedia
- Sentinel Finance
- Sentinel Trading
- Sentinel Terms & Conditions

Elke sentinel bevat:
- Lead AI agent
- workers
- layers
- skills
- policies
- workspace
- model/governance

## 4. Voorbeeld Sentinel Security

Sentinel Security

Lead AI agent:
- Nero

Workers:
- prompt injection worker
- runtime audit worker
- secrets monitor worker
- incident response worker
- policy validation worker

Layers:
- Prompt Defense Layer
- Runtime Security Layer
- Secrets Exposure Layer
- Incident Response Layer
- Policy Validation Layer

## 5. Live baseline uit bestaande agents

Nova en Flux bestaan al live en vormen de referentie voor nieuwe lead agents.

Nova workspace bevat o.a.:
- AGENTS.md
- ALLOWLIST.md
- BOOTSTRAP.md
- ENVIRONMENT.md
- HEARTBEAT.md
- IDENTITY.md
- MEMORY.md
- NETWORK_POLICY.md
- PROTOCOL.md
- SECURITY.md
- SOUL.md
- TASKS.md
- TOOLS.md
- USER.md

Flux workspace bevat o.a.:
- AGENTS.md
- DEPLOYMENT.md
- HEARTBEAT.md
- IDENTITY.md
- MEMORY.md
- PROTOCOL.md
- SECURITY.md
- SOUL.md
- TOOLS.md
- USER.md

## 6. Minimale baseline voor nieuwe Lead AI agents

Minimaal verplicht:
- AGENTS.md
- IDENTITY.md
- MEMORY.md
- SECURITY.md
- PROTOCOL.md
- SOUL.md
- TOOLS.md
- USER.md
- HEARTBEAT.md

Optioneel / sentinel-afhankelijk:
- NETWORK_POLICY.md
- TASKS.md
- DEPLOYMENT.md
- ENVIRONMENT.md
- ALLOWLIST.md

## 7. Minimale baseline voor workers

Workers zijn lichter dan lead agents.

Minimaal:
- AGENTS.md
- IDENTITY.md
- SECURITY.md
- PROTOCOL.md
- TOOLS.md

Optioneel:
- MEMORY.md
- HEARTBEAT.md
- TASKS.md

## 8. Sentinel directory structuur

Voorbeeld structuur:

arc_ai_angels/agents/
- sentinel-security/
  - lead-nero/
    - agent/
    - runtime/
    - workspace/
  - workers/
    - prompt-defense/
    - runtime-audit/
    - secrets-monitor/
    - incident-response/
    - policy-validation/

Nieuwe sentinels moeten aansluiten op deze structuur.

## 9. Model Runtime aansluiting

Huidige actieve model/providerlaag:
- Gemini
- Moonshot / Kimi

Modellen zijn nu per agent zichtbaar in:
- agent/models.json
- runtime/agent/models.json

Toekomstig:
- modelkeuze moet overridebaar worden via Mission Control
- workermodellen moeten onder parent/lead governance vallen

## 10. Parent / worker regel

Workers bestaan niet los.

Workers hangen altijd onder:
- een lead agent
- en dus onder een sentinel

Dus:
- Sentinel Security
  - Lead AI agent: Nero
  - workers onder Nero

## 11. Expansion wave

Nova en Flux worden niet opnieuw gebouwd.
Ze worden:
- behouden
- geaudit
- waar nodig aangevuld
- als foundation gebruikt

Eerste nieuwe sentinels om te bouwen:
- Sentinel Security
- Sentinel Research
- Sentinel Engineering
- Sentinel Documentation / Knowledge

## 12. Belangrijke ontwerpregels

Regel 1
Flux is geen sentinel maar centrale intelligentie.

Regel 2
Nova is geen sentinel maar direct interface AI agent.

Regel 3
Een sentinel is een domeincluster met een vaste structuur.

Regel 4
Elke sentinel heeft een Lead AI agent.

Regel 5
Workers hangen altijd onder een lead agent.

Regel 6
Nieuwe sentinels moeten aansluiten op de live Nova/Flux baseline.

Regel 7
De architectuur moet uitbreidbaar blijven per domein.

## 13. Output van M12r

M12r levert:
- gecorrigeerde runtime build foundation
- sentinel-definitie
- minimale agent baseline
- worker baseline
- aansluiting op live Nova/Flux structuur
- basis voor M13
---

## Sequence

\`\`\`mermaid
sequenceDiagram
    Flux->>Sentinel: Init
    Sentinel-->>Flux: Ready
\`\`\`