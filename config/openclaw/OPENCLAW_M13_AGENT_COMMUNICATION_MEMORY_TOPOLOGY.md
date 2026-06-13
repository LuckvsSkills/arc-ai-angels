# M13 — Agent Communication & Memory Topology

## Scope
Dit document definieert hoe agents, sentinels, workers en geheugenlagen met elkaar communiceren binnen ARC / OpenClaw.

Doel:
- communicatiestromen expliciet maken
- shared vs per-agent memory structureren
- routing tussen Nova, Flux, sentinels en workers vastleggen
- basis leggen voor latere Mission Control integratie

## 1. Hoofdcommunicatiestroom

De basisstroom is:

Operator
-> Direct Interface Agent
-> Flux
-> Sentinel
-> Lead AI agent
-> workers
-> terug via lead
-> terug via Flux
-> terug naar interface agent
-> terug naar operator

## 2. Direct Interface laag

Direct Interface Agents:
- Nova
- James
- Jim

Taken:
- ontvangen input van mens
- herkennen intent
- geven simpele antwoorden direct
- sturen complexe domein- of projecttaken door naar Flux
- verzorgen terugkoppeling naar de mens

## 3. Flux communicatierol

Flux:
- ontvangt input van interface agents
- classificeert taak
- bepaalt welk domein geraakt wordt
- routeert naar juiste sentinel
- bewaakt voortgang
- combineert output van meerdere sentinels
- geeft samengevoegde output terug

Flux is dus:
- centrale intelligentie
- routing- en integratielaag
- geen sentinel

## 4. Sentinel communicatierol

Elke sentinel ontvangt werk via Flux.

Sentinel-niveau:
- domeincontext
- beleidsregels
- teamstructuur
- layers
- skills

Binnen de sentinel loopt de taak eerst naar de Lead AI agent.

## 5. Lead AI agent communicatierol

Lead AI agent:
- ontvangt taak van Flux
- vertaalt taak naar domeinspecifieke uitvoering
- zet workers in waar nodig
- bewaakt kwaliteit en samenhang
- koppelt resultaat terug aan Flux

Voorbeeld:
- Sentinel Security
- Lead AI agent: Nero

Flux -> Nero -> security workers -> Nero -> Flux

## 6. Worker communicatierol

Workers:
- voeren afgebakende subtaken uit
- communiceren primair met hun Lead AI agent
- niet rechtstreeks met operator
- in principe niet rechtstreeks met Flux

Workers zijn:
- uitvoeringslaag
- smal en taakgericht
- parent-bound aan hun lead agent

## 7. Huidige live communicatierichting

In de live omgeving is al zichtbaar:

Nova -> Flux via OpenClaw session communicatie
sessionKey voorbeeld:
- agent:flux:main

En terug:
Flux -> Nova
- agent:nova:main

Er bestaan ook oudere aanwijzingen voor file-based of queue-based flow, maar OpenClaw-native session communicatie is nu de duidelijkste actieve route.

## 8. Communicatieniveaus

Niveau 1
Operator ↔ Direct Interface Agent

Niveau 2
Direct Interface Agent ↔ Flux

Niveau 3
Flux ↔ Lead AI agent van sentinel

Niveau 4
Lead AI agent ↔ workers

Niveau 5
Lead AI agent ↔ andere lead agents alleen via Flux, tenzij later expliciet anders ontworpen

## 9. Shared memory vs per-agent memory

We onderscheiden 3 hoofdtypen geheugen.

### A. Per-agent memory
Elke agent heeft een eigen MEMORY.md of equivalent contextgeheugen.

Doel:
- identiteit
- voorkeuren
- agent-specifieke notities
- relevante lopende context

### B. Sentinel memory
Een sentinel moet een gedeelde domeincontext kunnen hebben.

Bijvoorbeeld:
- sentinel policies
- domeinstatus
- teamcontext
- lopende domeinacties

### C. Shared system memory
Systeembreed geheugen voor:
- projectstatus
- gedeelde beslissingen
- globale prioriteiten
- inter-sentinel context

## 10. Workspace-lagen

We gaan uit van meerdere workspaceniveaus.

### Agent workspace
Voor individuele agentfiles zoals:
- AGENTS.md
- IDENTITY.md
- MEMORY.md
- SECURITY.md

### Sentinel workspace
Voor domeingedeelde files zoals:
- policies
- layers
- workflows
- team state

### Shared system workspace
Voor systeembrede uitwisseling zoals:
- project queues
- result sets
- coordination data
- gedeelde memory

## 11. Voorlopig shared structuurvoorstel

arc_ai_angels/shared/
- memory/
- tasks/
- results/
- sentinel-queues/
- projects/

Dit is nog conceptueel en wordt later concreter gemaakt.

## 12. Memory ontwerpregels

Regel 1
Niet alle memory is shared.

Regel 2
Persoonlijke en gevoelige context blijft zoveel mogelijk per agent beperkt.

Regel 3
Domeinrelevante context kan op sentinel-niveau gedeeld worden.

Regel 4
Project- en operatiecontext kan systeembreed gedeeld worden waar nodig.

Regel 5
Workers krijgen alleen de context die nodig is voor hun subtaak.

## 13. Communicatie ontwerpregels

Regel 1
Menselijke communicatie loopt via Direct Interface Agents.

Regel 2
Complexe routing loopt via Flux.

Regel 3
Sentinels ontvangen taken via hun Lead AI agent.

Regel 4
Workers communiceren in principe niet direct met operator.

Regel 5
Workers communiceren primair met hun parent lead agent.

Regel 6
Cross-sentinel samenwerking loopt in beginsel via Flux.

## 14. Mission Control koppeling

Mission Control moet later zicht geven op:
- welke sentinels actief zijn
- welke lead agents actief zijn
- welke workers actief zijn
- modelconfiguratie per agent
- memory / workspace status
- queue / taakstatus
- communicatiepaden

Mission Control moet ook override-mogelijkheden krijgen voor:
- modelkeuze
- fallbackkeuze
- enable/disable van workers
- sentinel status

## 15. Output van M13

M13 levert:
- communicatiearchitectuur
- memory-topologie
- workspace-lagen
- operator tot worker routingmodel
- basis voor latere build en Mission Control integratie


---

## Diagram

\`\`\`mermaid
flowchart TB
    A --> B
\`\`\`
