# M03 — Agent Role & Model Governance

## Scope
Dit document definieert hoe agentrollen, modelkeuze en subagentgedrag OpenClaw-native worden ingericht binnen de ARC Model Control Layer.

Doel:
- per agent een duidelijke rol toewijzen
- per rol een passend modelbeleid bepalen
- subagents bewust inzetten
- local/cloud keuzes structureren
- basis leggen voor latere config-implementatie

## 1. OpenClaw-native uitgangspunt

De structuur loopt via:

- bindings → agent routing
- agent → primary model
- defaults → gedeelde standaard
- subagents → goedkopere of gespecialiseerde uitvoer waar passend
- tools/sandbox → per agent afgestemd

Agents krijgen dus niet alleen een naam, maar een operationeel profiel.

## 2. Hoofdrollen

### Nova
Rol:
- frontdoor
- user-facing communicatie
- intake
- vertaling van gebruiker naar taak

Modelbeleid:
- cloud-first
- hoge kwaliteit
- stabiele output
- geschikt voor conversatie en reasoning

Waarom:
- direct contact met gebruiker
- reputatierisico bij zwakke output
- betrouwbaarheid belangrijker dan minimale kost

### Flux
Rol:
- execution agent
- technische uitvoering
- diepere analyse
- operator / implementatie taken

Modelbeleid:
- hybrid
- alternate cloud primary toegestaan
- fallback naar andere cloud of local waar logisch

Waarom:
- mix van kwaliteit, kosten en uitvoerbaarheid
- sommige technische taken kunnen goedkoper
- zwaardere taken hebben soms sterk model nodig

### Specialist / future agents
Rol:
- domeinspecifieke taken
- afgebakende expertise
- duidelijke responsibility boundaries

Modelbeleid:
- per specialisme instellen
- alleen cloud-first als de taak dat vereist
- anders local-first of cost-sensitive

### Worker agents
Rol:
- smalle deeltaken
- repetitieve verwerking
- hulproutines
- batch / transform / extraction

Modelbeleid:
- local-first
- goedkoopste bruikbare model
- beperkte fallback ladder

Waarom:
- kostencontrole
- hoge schaalbaarheid
- beperkte risico’s per taak

## 3. Subagent governance

Subagents mogen gebruikt worden voor:
- research prep
- samenvatten
- transformatie
- classificatie
- deeltaken met lage risico’s

Subagents mogen niet automatisch de hoogste-cost modellen gebruiken.

Richtlijn:
- main agent mag sterker model hebben
- subagents moeten standaard goedkoper of lokaler zijn
- alleen uitzonderen als taakinhoud dit vereist

## 4. Eerste modelrichting per rol

### Nova
- primary: hoge kwaliteit cloud
- fallback: tweede cloud provider
- subagents: goedkoper cloud of local waar veilig

### Flux
- primary: alternate cloud / technical strong model
- fallback: default cloud provider
- subagents: local-first waar mogelijk

### Workers
- primary: local provider zodra operationeel
- fallback: goedkoopste toegestane cloud
- geen premium model tenzij expliciet nodig

## 5. Governance regels

### Regel 1
Elke agent moet één duidelijke hoofdrol hebben.

### Regel 2
Modelkeuze volgt rol, niet alleen beschikbaarheid.

### Regel 3
User-facing agents krijgen kwaliteit voorrang.

### Regel 4
Batch/repetitieve agents krijgen kosten voorrang.

### Regel 5
Subagents draaien standaard goedkoper dan hoofdagents.

### Regel 6
Fallbacks moeten expliciet zijn en niet impliciet “alles mag”.

## 6. Huidige basis in deze omgeving

Huidig zichtbaar:
- Nova → Gemini
- Flux → Moonshot/Kimi
- global default → Gemini

Dit is een bruikbare start, maar nog geen volledig governance-model voor subagents en workers.

## 7. Output van M03

M03 levert:
- agent role framework
- model policy per rol
- subagent governance
- basis voor latere concrete OpenClaw config
---

## Roles

\`\`\`mermaid
classDiagram
    class Agent
    class Lead
    class Worker
    Agent <|-- Lead
    Agent <|-- Worker
\`\`\`