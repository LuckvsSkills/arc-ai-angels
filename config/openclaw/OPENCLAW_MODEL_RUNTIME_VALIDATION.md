# M06 — Model Runtime Validation

## Scope
Dit document valideert de actuele modelruntime van OpenClaw op Magneto.

## 1. Bevestigde configbasis

Actieve providers in `openclaw.json`:
- Google
- Moonshot

Actieve modelrefs:
- `google/gemini-2.0-flash`
- `moonshot/kimi-k2.5`

Per-agent assignments:
- Nova → `google/gemini-2.0-flash`
- Flux → `moonshot/kimi-k2.5`

## 2. Niet actief als provider

Wel aanwezig in env/context, maar niet actief in `models.providers`:
- OpenAI
- Ollama

## 3. Runtime conclusie

De huidige ARC Model Control Layer runtime is op dit moment:
- cloud-active
- Google + Moonshot gestuurd
- OpenClaw-native opgezet
- nog zonder actieve Ollama providerintegratie
- nog zonder expliciete fallbackconfig in `openclaw.json`

## 4. Validatiestatus

Bevestigd:
- providerstructuur
- modelrefs
- agent primary assignments
- OpenClaw-native control points

Nog niet bevestigd als live config:
- expliciete fallbacks
- specialist agents
- worker/subagent modelconfig
- Ollama als echte provider

## 5. Output van M06

M06 levert:
- runtime validatie
- onderscheid tussen actieve en toekomstige providerlagen
- afrondende basis voor dit hoofdstuk
---

## Validation

\`\`\`mermaid
flowchart LR
    A[Input] --> B{Check}
    B -->|ok| C[Accept]
    B -->|fail| D[Reject]
\`\`\`