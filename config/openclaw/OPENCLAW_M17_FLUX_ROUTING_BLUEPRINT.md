# M17 — Flux Routing Blueprint

## Scope
Dit document beschrijft hoe Flux taken logisch routeert binnen ARC / OpenClaw.

## 1. Rol van Flux

Flux:
- ontvangt input van direct interface agents
- herkent domein
- kiest juiste sentinel
- kiest juiste lead agent
- bewaakt taakverdeling
- combineert resultaten

## 2. Eerste routinglogica

Voorbeeldmapping:

- security vraagstuk -> Sentinel Security -> Nero
- research vraagstuk -> Sentinel Research -> Sora
- engineering vraagstuk -> Sentinel Engineering -> Forge
- documentatie vraagstuk -> Sentinel Documentation -> Clio

## 3. Routingstappen

Stap 1
Flux ontvangt taak.

Stap 2
Flux classificeert taaktype.

Stap 3
Flux bepaalt sentinel.

Stap 4
Flux bepaalt lead agent.

Stap 5
Flux routeert taak.

Stap 6
Lead agent splitst eventueel op naar workers.

Stap 7
Lead agent levert samengevoegd resultaat terug aan Flux.

## 4. Multi-sentinel routing

Wanneer meerdere domeinen geraakt worden:
- Flux verdeelt naar meerdere sentinels
- bewaakt deelresultaten
- combineert eindresultaat
- levert één coherente terugkoppeling

## 5. Prioriteitslogica

Voorlopig:
- high
- medium
- low

Flux gebruikt prioriteit voor:
- routingvolgorde
- escalatie
- zichtbaarheid in Mission Control

## 6. Eerste vaste mappings

- Sentinel Security -> Nero
- Sentinel Research -> Sora
- Sentinel Engineering -> Forge
- Sentinel Documentation -> Clio

## 7. Toekomstige uitbreidingen

Later toevoegen:
- model-aware routing
- cost-aware routing
- queue-aware routing
- availability-aware routing
- fallback routing

## 8. Output van M17

M17 levert:
- eerste routingmodel voor Flux
- sentinel mapping
- basis voor Mission Control routingweergave
---

## Routing

\`\`\`mermaid
flowchart TB
    R[Router] --> S1[Security]
    R --> S2[Research]
\`\`\`