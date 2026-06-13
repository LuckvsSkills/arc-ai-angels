# Model Runtime & Providers
## Block 01 — Model runtime architecture

### Purpose
Dit block beschrijft hoe de OpenClaw installatie wordt gebruikt als runtimebasis voor ARC AI Agents en hoe AI agents daarin logisch worden opgebouwd, verbonden en aangestuurd.

De focus van dit block ligt op:
- waar agents draaien
- hoe de hoofdstructuur is opgebouwd
- hoe routing tussen Nova, Flux, Omni, Sentinels en Workers verloopt
- hoe OpenClaw en ARC AI Agents zich tot elkaar verhouden

### OpenClaw runtime context
OpenClaw is binnen dit project de technische runtimebasis waarop AI agents worden geplaatst en geconfigureerd.

ARC AI Agents is de organisatielaag bovenop OpenClaw. Die laag bepaalt niet de runtime zelf, maar wel:
- de hiërarchie
- de domeinverdeling
- de routinglogica
- de samenwerking tussen agents

Kort gezegd:
- OpenClaw = technische basis
- ARC AI Agents = operationele structuur

### Full system flow
```text
Fea (gebruiker)
  ↓
Nova (Gateway / Interface)
  ↓
Flux (Master Orchestrator)
  ↓
Omni (Domain Layer)
  ↓
Sentinel (Specialist Layer)
  ↓
Workers (Execution Layer)
```

Terugkoppeling:

```text
Workers → Sentinel → Omni → Flux → Nova → Fea
```

### Core architecture logic
De architectuur is opgebouwd als een gecontroleerde AI-hiërarchie.

Belangrijkste logica:
- Fea communiceert niet direct met Flux, maar via Nova of Mission Control
- Nova beslist of een taak lokaal afgehandeld kan worden of naar Flux moet
- Flux bepaalt welk domein verantwoordelijk is
- Omni neemt domeincoördinatie over
- Sentinels voeren specialistische taken uit
- Workers doen de uitvoerende handelingen

### Nova decision logic
```text
Input komt binnen bij Nova
├ simpele taak → Nova handelt zelf af
└ complexe / domeintaak → Flux
```

Nova is dus een filterlaag, niet de centrale orchestrator.

### Flux orchestration logic
Flux is het centrale brein dat overzicht houdt over alle domeinen en taakstromen.

Flux doet het volgende:
- interpreteert taakintentie
- kiest de juiste Omni
- bewaakt routing en terugkoppeling
- kan in uitzonderlijke gevallen direct een Sentinel aanspreken

### Omni overview
```text
Flux
 ├ Omni Helix   → Tech         → Lead AI Agent: Cortexia
 ├ Omni Matrix  → Intelligence → Lead AI Agent: Saelia
 ├ Omni Quantix → Growth       → Lead AI Agent: Lumeria
 ├ Omni Zenix   → Operations   → Lead AI Agent: Fluentia
 └ Omni Finix   → Assets       → Lead AI Agent: Finoria
```

Elke Omni is verantwoordelijk voor één domein en stuurt de Sentinels binnen dat domein aan.

### Sentinel relationship to Omni
Alle Omni’s met hun bijbehorende Sentinels:

```text
Omni Helix (Tech)
 ├ Sentinel Security       → Lead AI Agent: Nero
 ├ Sentinel Engineering    → Lead AI Agent: Forge
 ├ Sentinel Infrastructure → Lead AI Agent: Ventura
 ├ Sentinel Automation     → Lead AI Agent: Axon
 └ Sentinel Documentation  → Lead AI Agent: Clio

Omni Matrix (Intelligence)
 ├ Sentinel Research          → Lead AI Agent: Sora
 ├ Sentinel Data Analysis     → Lead AI Agent: Daxio
 ├ Sentinel Strategy          → Lead AI Agent: Enki
 └ Sentinel Knowledge Systems → Lead AI Agent: Tharos

Omni Quantix (Growth)
 ├ Sentinel Marketing         → Lead AI Agent: Vondra
 ├ Sentinel Content Creation  → Lead AI Agent: Nura
 ├ Sentinel SEO               → Lead AI Agent: Elora
 ├ Sentinel Affiliate Systems → Lead AI Agent: Luvia
 └ Sentinel Audience Growth   → Lead AI Agent: Kresta

Omni Zenix (Operations)
 ├ Sentinel Workflow             → Lead AI Agent: Solis
 ├ Sentinel Process Systems      → Lead AI Agent: Orizon
 ├ Sentinel Project Coordination → Lead AI Agent: Zena
 └ Sentinel System Monitoring    → Lead AI Agent: Unia

Omni Finix (Assets)
 ├ Sentinel Trading              → Lead AI Agent: Vector
 ├ Sentinel Crypto Assets        → Lead AI Agent: Zion
 ├ Sentinel Real Estate          → Lead AI Agent: Odis
 └ Sentinel Portfolio Management → Lead AI Agent: Kenzo
```

Elke Sentinel:
- heeft een specialistisch domein
- heeft een Lead AI Agent
- stuurt Workers aan
- rapporteert terug aan de Omni

### Worker relationship to Sentinels
Workers zijn de uitvoerende laag.

Workers kunnen onder meer worden ingezet voor:
- code generatie
- validatie
- research
- analyse
- documentatie
- automatisering

Workers rapporteren niet rechtstreeks aan Flux, maar lopen via Sentinel en Omni terug omhoog.

### Agent placement & installatie
Binnen OpenClaw moeten agents volgens vaste structuur worden ingericht.

Elke agent moet minimaal logisch gekoppeld zijn aan:
- domein
- rol
- naam
- hiërarchische positie

Dit voorkomt losse, onduidelijke agentconfiguraties zonder heldere verantwoordelijkheid.

### Mission entry points
Fea kan het systeem op twee hoofdmanieren bereiken:

```text
1. Via Nova
   - Telegram
   - UI / Gateway

2. Via Mission Control
   - directe besturing / overzicht
```

Beide routes komen uiteindelijk uit bij Flux wanneer domeinlogica nodig is.

### Key rules
- Nova stuurt nooit direct Omni’s of Sentinels aan
- Flux stuurt primair Omni’s aan
- Omni’s sturen Sentinels aan
- Sentinels sturen Workers aan
- directe Flux → Sentinel routing is alleen een uitzonderingsroute
- terugkoppeling verloopt altijd omhoog in de hiërarchie

### Known verification point
Er moet later nog gecontroleerd worden:
- waar OpenClaw fysiek op het systeem is geïnstalleerd
- of die installatie binnen ARC AI Agents staat of daarbuiten
- welke mapstructuur leidend is voor deployment en configuratie

Dit punt moet later expliciet worden gevalideerd op de pc.

### Why it exists
Deze structuur bestaat om chaos te voorkomen.

Zonder deze architectuur zouden agents:
- dubbel werk doen
- onduidelijk aangestuurd worden
- zonder domeinverantwoordelijkheid opereren
- moeilijk schaalbaar zijn

Met deze opbouw ontstaat:
- duidelijke verantwoordelijkheid
- schaalbaarheid
- voorspelbare routing
- controle over uitvoering en terugkoppeling

### Dependencies
- Agent & subagent mapping
- Direct interface & command routing
- Flux orchestration map
- Flux routing blueprint
- Team & subagent architecture

### Decisions made
- OpenClaw is runtimebasis
- ARC AI Agents is organisatielaag
- Nova is gateway en beslisfilter
- Flux is centrale orchestrator
- Omni’s zijn domeinverantwoordelijken
- Sentinels zijn specialistische lagen
- Workers zijn uitvoeringslaag
- routing verloopt hiërarchisch van boven naar beneden en terug

### Decision locked
Owner: Fea
Status: ARC AI Agents — Model Runtime baseline v2
