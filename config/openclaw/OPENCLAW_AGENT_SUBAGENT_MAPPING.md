# M04 — Agent & Subagent Mapping

## Scope
Dit document definieert de concrete agent- en subagentstructuur voor de ARC Model Control Layer binnen OpenClaw.

Doel:
- hoofdagents en worker-rollen structureren
- modelkeuze per agenttype vastleggen
- fallbackrichting expliciet maken
- basis leggen voor latere config-implementatie

## 1. Main agents

### Nova
Rol:
- frontdoor
- user communication
- intake
- task translation

Model policy:
- primary: Gemini
- fallback: Moonshot
- strategy: quality-first, cloud-first

Subagent policy:
- toegestaan voor voorbereidende deeltaken
- subagents goedkoper dan Nova primary
- geen premium escalation zonder reden

### Flux
Rol:
- execution
- technical implementation
- analysis
- operator tasks

Model policy:
- primary: Moonshot/Kimi
- fallback: Gemini
- strategy: hybrid

Subagent policy:
- toegestaan voor deelanalyse en verwerking
- local-first zodra Ollama actief is
- cloud fallback toegestaan indien local niet voldoet

## 2. Future specialist agents

### Atlas
Voorgestelde rol:
- architecture
- systems planning
- design coordination

Model policy:
- primary: Gemini
- fallback: Moonshot

### Sentinel
Voorgestelde rol:
- security analysis
- hardening review
- policy validation

Model policy:
- primary: Gemini
- fallback: Moonshot
- local support: mogelijk voor eenvoudige checks

### Archivist
Voorgestelde rol:
- memory structure
- document organization
- context preparation

Model policy:
- primary: local-first zodra Ollama actief is
- fallback: Gemini

## 3. Worker / subagent class

### Worker class purpose
Workers zijn bedoeld voor:
- samenvatten
- classificeren
- transformeren
- extraction
- deelverwerking
- batch routines

### Worker class model policy
- primary: local provider
- fallback: Gemini of Moonshot, afhankelijk van taaktype
- premium modellen niet standaard gebruiken

### Worker class security posture
- beperkte tools
- beperkte scope
- deny-by-default waar mogelijk
- sandbox strakker dan main agents

## 4. Mapping rules

### Regel 1
Main agents krijgen een duidelijke hoofdverantwoordelijkheid.

### Regel 2
Subagents mogen alleen afgebakende deeltaken uitvoeren.

### Regel 3
User-facing werk blijft bij voorkeur bij Nova of vergelijkbare high-quality agent.

### Regel 4
Execution-heavy werk blijft bij Flux of technische specialists.

### Regel 5
Workers gebruiken de goedkoopste bruikbare modelroute.

### Regel 6
Fallbacks worden vooraf bepaald en niet ad hoc gekozen.

## 5. Eerste concrete mappingrichting

### Huidig
- Nova → Gemini
- Flux → Moonshot/Kimi

### Volgende uitbreiding
- Atlas → Gemini
- Sentinel → Gemini
- Archivist → Ollama local zodra beschikbaar, anders Gemini
- Workers → Ollama local zodra beschikbaar, anders goedkoopste cloud fallback

## 6. Output van M04

M04 levert:
- agent/subagent structuur
- concrete modelrichting
- fallbackrichting
- basis voor OpenClaw config updates
---

## Hierarchy

\`\`\`mermaid
graph TD
    A[Master] --> B[Sub1]
    A --> C[Sub2]
\`\`\`