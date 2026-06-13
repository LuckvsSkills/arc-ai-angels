# M14 — Flux Sentinel Integration

## Scope
Dit document beschrijft hoe Flux als centrale intelligentie gekoppeld is aan de gebouwde sentinels.

## 1. Positie van Flux

Flux is:
- centrale intelligentie
- routeringslaag
- integratielaag
- voortgangsbewaker
- geen sentinel

## 2. Huidige directe koppelingen

Flux moet kunnen aansturen:
- Sentinel Security -> Nero
- Sentinel Research -> Sora
- Sentinel Engineering -> Forge
- Sentinel Documentation -> Clio

## 3. Routingprincipe

Stroom:
- Operator -> Nova / andere direct interface agent
- Direct Interface Agent -> Flux
- Flux -> juiste sentinel lead agent
- lead agent -> workers
- workers -> lead agent
- lead agent -> Flux
- Flux -> interface agent
- interface agent -> operator

## 4. Eerste lead mappings

- Sentinel Security -> lead-nero
- Sentinel Research -> lead-sora
- Sentinel Engineering -> lead-forge
- Sentinel Documentation -> lead-clio

## 5. Shared structuur

Gedeelde structuur:
- shared/memory
- shared/tasks
- shared/results
- shared/sentinel-queues
- shared/projects
- shared/registry
- shared/logs

Bestaande compatibiliteitspaden:
- shared/nova_to_flux
- shared/flux_to_nova

## 6. Registry rol

sentinel_registry.json wordt de eerste bron voor:
- welke sentinels bestaan
- welke lead agent erbij hoort
- welke workers erbij horen
- welke buildstatus actief is

## 7. Communicatie-opmerking

Er zijn nu twee relevante communicatierichtingen zichtbaar:
- OpenClaw-native session communicatie
- bestaande file/queue compatibiliteit via nova_to_flux en flux_to_nova

Voorlopige ontwerpkeuze:
- OpenClaw sessions blijven primaire live communicatieroute
- shared queue paths blijven beschikbaar als compatibiliteit of latere routinglaag

## 8. Volgende implementatiestap

Na deze documentatie volgt:
- sentinel-specifieke protocolverrijking
- task queue ontwerp
- Flux-side routeringslogica
- Mission Control zichtbaarheid


---

## Diagram

\`\`\`mermaid
flowchart TB
    A --> B
\`\`\`
