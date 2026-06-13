# M01 — Model Runtime Architecture

## Scope
Dit document definieert de architectuur van de ARC Model Control Layer voor OpenClaw / Arc AI Angels.

Doel:
- centrale modelbesturing
- scheiding tussen agents en providers
- local/cloud routing mogelijk maken
- fallback tussen providers ondersteunen
- kosten en betrouwbaarheid beheersbaar maken

## 1. Kernprincipe

Agents kiezen niet direct zelf een provider.
Agents praten tegen een logische model control layer.

Deze layer bepaalt:
- welke provider gebruikt wordt
- welk model gebruikt wordt
- of local inference mogelijk is
- welke fallback gekozen wordt
- welke provider prioriteit heeft

## 2. Provider types

### Local provider
Lokale inference via:
- Ollama

Voordelen:
- privacy
- geen externe API-kosten
- bruikbaar voor worker taken en fallback

Nadelen:
- hangt af van lokale hardware
- mogelijk lagere kwaliteit bij complexe taken

### Cloud providers
Externe inference via:
- Gemini
- Moonshot
- OpenAI

Voordelen:
- hogere kwaliteit
- betere reasoning / general capability
- snelle inzet zonder lokale modelhosting

Nadelen:
- API-kosten
- outbound dependency
- minder controle dan local

## 3. Routing model

De Model Control Layer beslist op basis van:

- agent type
- taaktype
- gewenste kwaliteit
- latency tolerantie
- kostenprofiel
- beschikbaarheid van providers

## 4. Conceptuele flow

1. agent vraagt inference aan
2. model control layer leest policy
3. primary provider wordt gekozen
4. indien primary unavailable is:
   - fallback provider kiezen
5. response teruggeven aan agent

## 5. Provider role strategy

### Nova
Voorkeur:
- cloud-first

Waarom:
- communicatiekwaliteit
- hogere betrouwbaarheid
- betere user-facing output

### Flux
Voorkeur:
- hybrid

Waarom:
- sommige taken local mogelijk
- zwaardere taken via cloud
- balans tussen kosten en kwaliteit

### Worker agents
Voorkeur:
- local-first

Waarom:
- lagere kosten
- beperkte scope
- deny-by-default internetstrategie blijft logisch

## 6. Architectuurdoelen

Deze layer moet:

- provider-agnostisch zijn
- makkelijk uitbreidbaar zijn
- centrale configuratie hebben
- fallback ondersteunen
- per agent aanpasbaar zijn
- operator-vriendelijk zijn

## 7. Eerste provider set

Initiële provider set:

- Ollama
- Gemini
- Moonshot
- OpenAI

## 8. Output van M01

M01 levert:
- runtime architectuur
- providerrollen
- routingrichting
- basis voor registry en mapping
---

## Architecture

\`\`\`mermaid
flowchart TB
    API --> Core
    Core --> Models
\`\`\`