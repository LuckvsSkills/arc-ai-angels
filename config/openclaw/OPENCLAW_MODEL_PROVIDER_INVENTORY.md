# M02 — OpenClaw Model & Provider Inventory

## Scope
Dit document beschrijft de native OpenClaw model- en providerstructuur zoals die in `~/.openclaw/openclaw.json` is geconfigureerd.

Doel:
- OpenClaw-native modelarchitectuur vastleggen
- configured providers inventariseren
- actieve modelrefs documenteren
- agent-to-model basis zichtbaar maken
- basis leggen voor mapping, fallback en operator controls

## 1. Native OpenClaw modelstructuur

OpenClaw gebruikt voor modelselectie:

- `models.providers`
- modelrefs in formaat `provider/model`
- `agents.defaults.model.primary`
- per-agent `model.primary`

Bindings routeren berichten naar agents.
De agentconfig bepaalt vervolgens welk model gebruikt wordt.

## 2. Configured providers

### Google
- provider_id: `google`
- api: `google-generative-ai`
- endpoint: `https://generativelanguage.googleapis.com/v1beta`
- configured model:
  - `google/gemini-2.0-flash`
- rol:
  - global default
  - Nova primary
  - algemene cloud inference

### Moonshot
- provider_id: `moonshot`
- api: `openai-completions`
- endpoint: `https://api.moonshot.ai/v1`
- configured model:
  - `moonshot/kimi-k2.5`
- rol:
  - Flux primary
  - alternate cloud inference

## 3. Agent defaults

### Global default
- `agents.defaults.model.primary`
- waarde: `google/gemini-2.0-flash`

### Known aliases
- `google/gemini-2.0-flash` → `Gemini`
- `moonshot/kimi-k2.5` → `Kimi`

## 4. Per-agent assignments

### Nova
- primary model: `google/gemini-2.0-flash`

### Flux
- primary model: `moonshot/kimi-k2.5`

## 5. Observaties

- OpenAI credential bestaat in env, maar OpenAI staat niet actief in `models.providers`
- Ollama host bestaat in env, maar Ollama staat niet actief in `models.providers`
- de huidige actieve providerlaag bestaat dus uit:
  - Google
  - Moonshot

## 6. Conclusie

De huidige OpenClaw model control werkt via:
- providerconfig in `models.providers`
- modelrefs per agent
- defaults + per-agent overrides

De ARC Model Control Layer moet daarom worden gezien als:
- configuratiegovernance
- modelbeleid
- fallbackbeleid
- roltoewijzing
- operatorstandaardisatie

bovenop OpenClaw-native config.

## 7. Output van M02

M02 levert:
- provider inventory
- actieve modelrefs
- per-agent modelbasis
- basis voor verdere runtime validatie
---

## Inventory

\`\`\`mermaid
erDiagram
    PROVIDER ||--o{ MODEL : has
\`\`\`