# M15 — Sentinel Protocol Enrichment

## Scope
Dit document verrijkt het protocol voor sentinels, lead agents en workers binnen ARC / OpenClaw.

## 1. Doel

Elke sentinel moet niet alleen bestaan als directorystructuur, maar ook als operationeel protocol.

Dit protocol definieert:
- hoe een lead agent taken ontvangt
- hoe workers worden ingezet
- hoe resultaten terugkomen
- hoe escalatie plaatsvindt
- hoe domeinregels bewaakt worden

## 2. Sentinel protocol kern

Elke sentinel bevat:
- Sentinel naam
- Lead AI agent
- workers
- layers
- domeinregels
- communicatieregels
- taakverdelingsregels

## 3. Lead agent protocol

De Lead AI agent:
- ontvangt taken van Flux
- bepaalt of de taak enkelvoudig of opgesplitst moet worden
- kiest de juiste worker of workers
- bewaakt samenhang en kwaliteit
- combineert worker-output
- koppelt resultaat terug aan Flux

## 4. Worker protocol

Workers:
- ontvangen alleen subtaakscope
- gebruiken alleen noodzakelijke context
- geven resultaat terug aan hun lead agent
- escaleren alleen naar hun lead agent
- nemen geen domeinbrede beslissingen zelfstandig

## 5. Escalatieprotocol

Escalatie loopt als volgt:
- worker -> lead agent
- lead agent -> Flux
- Flux -> Direct Interface Agent
- Direct Interface Agent -> operator

## 6. Sentinel-specifieke regels

Sentinels mogen extra regels toevoegen in:
- SECURITY.md
- PROTOCOL.md
- SENTINEL.md
- LAYERS.md

## 7. Voorbeeld Sentinel Security

Sentinel Security:
- Lead AI agent: Nero
- workers:
  - Prompt Defense Worker
  - Runtime Audit Worker
  - Secrets Monitor Worker
  - Incident Response Worker
  - Policy Validation Worker

Protocolrichting:
- Flux -> Nero
- Nero -> workers
- workers -> Nero
- Nero -> Flux

## 8. Voorbeeld Sentinel Research

Sentinel Research:
- Lead AI agent: Sora
- workers:
  - Web Research Worker
  - Competitor Scan Worker
  - Source Validation Worker
  - Dataset Collection Worker

Protocolrichting:
- Flux -> Sora
- Sora -> workers
- workers -> Sora
- Sora -> Flux

## 9. Ontwerpregels

Regel 1
Lead agents zijn domeineigenaar binnen hun sentinel.

Regel 2
Workers blijven strikt parent-bound.

Regel 3
Cross-worker coördinatie loopt via de lead agent.

Regel 4
Cross-sentinel coördinatie loopt via Flux.

Regel 5
Sentinel protocol mag per domein verrijkt worden, maar niet de hoofdarchitectuur breken.

## 10. Output van M15

M15 levert:
- verrijkt sentinel protocol
- duidelijke lead/worker regels
- escalatieroute
- basis voor task queue ontwerp
---

## State

\`\`\`mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Active
    Active --> [*]
\`\`\`