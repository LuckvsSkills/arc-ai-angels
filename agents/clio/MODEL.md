# MODEL — CLIO Model Routing

## Baseline
- **Tier:** C
- **Model:** gemini-flash-lite
- **LiteLLM route:** litellm/arc-low

## Beschikbare modellen per tier

| Tier | Model | LiteLLM | Prijs |
|------|-------|---------|-------|
| A — Zwaar | gemini/gemini-2.5-pro | litellm/arc-flux | €1.15/1M |
| B — Balans | gpt-4o-mini | litellm/arc-mid | €0.14/1M |
| C — Snel/goedkoop | gemini-flash-lite | litellm/arc-low | €0.023/1M |
| Cron | gemini-flash-lite | litellm/arc-cron | €0.023/1M |

## Wanneer welk tier gebruiken

### Tier A — inzetten bij:
- Kritieke beslissingen met directe impact
- Complexe code schrijven of architectuur beoordelen
- Taken waarbij een fout cascadeert
- Nieuwe of onduidelijke vraagstukken

### Tier B — inzetten bij:
- Gestructureerde taken met duidelijke verwachting
- Coördinatie, routing en analyse
- Herhaalbare taken die LLM-intelligentie vereisen

### Tier C — inzetten bij:
- Documentatie en logging
- Eenvoudige classificatie en routing
- HARNAS cronjobs

## Complexiteitsweging
Score elke taak (1-3 per criterium):

| Criterium | 1 | 2 | 3 |
|-----------|---|---|---|
| Scope | Enkelvoudige actie | Meerdere stappen | Systeem-breed |
| Risico | Informatief/herstelbaar | Beperkt risico | Kritiek/onomkeerbaar |
| Context | Geen history | Gedeeltelijke context | Volledige context |
| Complexiteit | Template/herhaalbaar | Redenering vereist | Strategisch/nieuw |

- Score 4-6 → Tier C
- Score 7-9 → Tier B
- Score 10-12 → Tier A

## Escalatieregel
Tier C mislukt → escaleer naar Tier B
Tier B mislukt → escaleer naar Tier A
Tier A mislukt → rapporteer aan Cortexia / Flux

## Referentie
Zie CODEX CH19 voor het volledige model routing framework.
