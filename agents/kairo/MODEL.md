# MODEL — KAIRO Model Routing

## Baseline
- **Tier:** B
- **Model:** gemini-2.5-flash

## Beschikbare modellen per tier

| Tier | Modellen |
|------|---------|
| A — Absoluut best | gpt-4o |
| B — Sterk, 90% van taken | gemini-2.5-flash |
| C — Snel en goedkoop | meta-llama/llama-3.3-70b-instruct:free |

## Wanneer welk tier gebruiken

### Tier A — inzetten bij:
- Kritieke beslissingen met directe impact
- Complexe redenering waarbij nuance essentieel is
- Taken waarbij een fout cascadeert
- Nieuwe of onduidelijke vraagstukken

### Tier B — inzetten bij:
- Gestructureerde taken met duidelijke verwachting
- Coördinatie en routing zonder hoge risicodrempel
- Analyses met grote context maar beperkte redenering
- Herhaalbare taken die LLM-intelligentie vereisen

### Tier C — inzetten bij:
- Documentatie, logging, kennisbeheer
- Signaalverwerking op hoog volume
- Eenvoudige classificatie en routing
- Volledig gestructureerde voorspelbare taken

## Complexiteitsweging

Score elke taak op deze 4 criteria (1-3 per criterium):

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
Tier A mislukt → rapporteer aan Lead Agent / Flux
## Referentie
Zie CODEX CH19 voor het volledige model routing framework.
