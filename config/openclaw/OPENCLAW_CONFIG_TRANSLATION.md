# M05 — OpenClaw Config Translation

## Scope
Dit document vertaalt de ARC Model Control Layer naar concrete OpenClaw-configuratieprincipes.

Doel:
- huidige OpenClaw-config structureren
- toekomstige agentuitbreidingen voorbereiden
- model/fallback-config OpenClaw-native definiëren
- basis leggen voor latere implementatie in `~/.openclaw/openclaw.json`

## 1. Huidige confirmed basis

### Providers in gebruik
De huidige config bevat:

- `google/gemini-2.0-flash`
- `moonshot/kimi-k2.5`

### Huidige agent assignments
- Nova → `google/gemini-2.0-flash`
- Flux → `moonshot/kimi-k2.5`

### Global default
- `agents.defaults.model.primary` → `google/gemini-2.0-flash`

## 2. OpenClaw-native control points

### Routing
Kanaalroutering gebeurt via:
- `bindings`

### Default model policy
Globale modelkeuze gebeurt via:
- `agents.defaults.model.primary`
- later ook: `agents.defaults.model.fallbacks`

### Per-agent override
Agent-specifieke modelkeuze gebeurt via:
- `agents.list[].model.primary`
- later ook per agent: `model.fallbacks`

### Known model catalog
Model refs en aliases worden beheerd via:
- `agents.defaults.models`

## 3. Governance translation

### Nova
OpenClaw-doelrichting:
- behoud primary: `google/gemini-2.0-flash`
- voeg later fallback toe:
  - `moonshot/kimi-k2.5`

### Flux
OpenClaw-doelrichting:
- behoud primary: `moonshot/kimi-k2.5`
- voeg later fallback toe:
  - `google/gemini-2.0-flash`

### Future specialists
Toekomstige agents toevoegen via:
- `agents.list[]`

Verwachte eerste specialist agents:
- Atlas
- Sentinel
- Archivist

## 4. Subagent direction

Subagents moeten niet los buiten OpenClaw worden ontworpen.
Ze moeten passen binnen:

- main agent rol
- goedkopere modelroute
- beperkte taakscope
- strengere tool/sandbox posture

Richtlijn:
- subagents standaard goedkoper dan main agents
- user-facing output niet standaard via subagent primary
- local-first zodra Ollama echt als provider wordt toegevoegd

## 5. Future provider expansion

### Nog niet actief als provider in huidige config
Hoewel aanwezig in env/configcontext, zijn deze nog niet actief als provider in `models.providers`:

- OpenAI
- Ollama

### Betekenis
Deze kunnen pas deel worden van de ARC Model Control Layer zodra ze expliciet in OpenClaw model/providerconfig worden opgenomen.

## 6. Concrete next implementation targets

### Target A
Voeg expliciete fallbacks toe aan modelbeleid.

### Target B
Definieer specialist agents in `agents.list[]`.

### Target C
Voeg Ollama pas toe als echte provider zodra runtime bevestigd en bruikbaar is.

### Target D
Werk subagentbeleid uit met cost-first en security-first defaults.

## 7. Belangrijke ontwerpregel

De ARC Model Control Layer is geen aparte engine naast OpenClaw.

De ARC Model Control Layer is:
- configuratiegovernance
- modelbeleid
- fallbackbeleid
- roltoewijzing
- operatorstandaardisatie

bovenop OpenClaw-native config.

## 8. Output van M05

M05 levert:
- config translation layer
- implementatierichting voor `openclaw.json`
- basis voor latere concrete config changes
---

## Pipeline

\`\`\`mermaid
flowchart LR
    A[Config] --> B[Parse]
    B --> C[Deploy]
\`\`\`