# CH19 — Model Routing Strategy

**Status:** Active  
**Eigenaar:** Supreme Fea  
**Versie:** 1.0 — Juni 2026  
**Van toepassing op:** Alle 33 ARC AI AGENTS agents

---

## 1. Doel van dit hoofdstuk

Dit hoofdstuk beschrijft hoe ARC AI AGENTS omgaat met modelkeuzes. Het legt vast:

- Hoe tiers zijn opgebouwd en wat ze betekenen
- Hoe een agent bepaalt welk tier en model hij gebruikt
- Wat de baseline is per agent en waarom
- Hoe nieuwe agents in de toekomst worden geconfigureerd

Dit document is de enige bron van waarheid voor modelkeuzes binnen ARC.

---

## 2. De drie tiers

### Tier A — Absoluut best

Tier A is gereserveerd voor taken waarbij kwaliteit boven alles gaat. Als een Tier A model de taak niet kan uitvoeren, kan geen enkel ander model dat ook. Tier A wordt ingezet bij:

- Kritieke beslissingen met directe impact (financieel, security, strategie)
- Complexe redenering waarbij nuance essentieel is
- Taken waarbij een fout cascadeert door het systeem
- Nieuwe of onduidelijke vraagstukken zonder precedent

**Modellen in Tier A (goedkoopste eerst):**

| Model | Provider | Sterk in | Input/1M | Output/1M |
|-------|----------|----------|----------|----------|
| Kimi K2.6 | Moonshot | Lange context, redeneren | $0.44 | $2.00 |
| GPT-4o | OpenAI | Structuur, cijfers, code | $2.50 | $10.00 |
| Claude Sonnet 4.6 | Anthropic | Taal, nuance, instructies | $3.00 | $15.00 |
| DeepSeek V4 Pro | DeepSeek | Code, engineering | $0.44 | $0.87 |

> **Keuzeregel Tier A:** Gebruik de goedkoopste optie die de taak aankan. DeepSeek V4 Pro voor code-taken. Kimi K2.6 voor research en redeneren. GPT-4o voor cijfers en structuur. Claude Sonnet alleen als de taak specifiek taalkundige diepgang vereist.

---

### Tier B — Sterk, 90% van de taken

Tier B is de werkhorslaag van ARC. De meeste dagelijkse taken worden hier afgehandeld. Tier B wordt ingezet bij:

- Gestructureerde taken met duidelijke verwachting
- Coördinatie en routing zonder hoge risicodrempel
- Analyses waarbij context groot is maar redenering beperkt
- Taken die herhaalbaar zijn maar nog LLM-intelligentie vereisen

**Modellen in Tier B (goedkoopste eerst):**

| Model | Provider | Sterk in | Input/1M | Output/1M |
|-------|----------|----------|----------|----------|
| Gemini 2.5 Flash | Google | Lange context, snel | $0.30 | $2.50 |
| GPT-4o-mini | OpenAI | Structuur, goedkoop | $0.15 | $0.60 |
| Claude Haiku 4.5 | Anthropic | Taal, instructies | $1.00 | $5.00 |

> **Keuzeregel Tier B:** Gemini 2.5 Flash is de standaard goedkoopste keuze. GPT-4o-mini bij OpenAI-specifieke taken. Claude Haiku voor taaldomein agents waar instructienauwkeurigheid telt.

---

### Tier C — Snel en goedkoop

Tier C is voor routinetaken met lage complexiteit en hoog volume. Fouten hier zijn herstelbaar en hebben weinig impact. Tier C wordt ingezet bij:

- Documentatie, logging, kennisbeheer
- Signaalverwerking en patroondetectie op hoog volume
- Eenvoudige classificatie en routing
- Taken die volledig gestructureerd en voorspelbaar zijn

**Modellen in Tier C (goedkoopste eerst):**

| Model | Provider | Sterk in | Kosten |
|-------|----------|----------|--------|
| Llama 3.3 70B | OpenRouter | Algemeen, gratis | EUR 0 |
| Gemini 3.1 Flash Lite | Google | Snel, goedkoop | $0.10/$0.40 |
| DeepSeek V4 Flash | DeepSeek | Code, structuur | $0.14/$0.28 |

> **Keuzeregel Tier C:** Llama 3.3 70B is altijd de eerste keuze — volledig gratis via OpenRouter. Alleen naar Gemini Flash Lite of DeepSeek Flash als Llama rate-limited is.

---

## 3. Hoe een agent zijn tier kiest

### 3.1 Complexiteitsweging

Elke agent weegt een binnenkomende taak op vier criteria:

| Criterium | Score 1 | Score 2 | Score 3 |
|-----------|---------|---------|---------|
| **Scope** | Enkelvoudige actie | Meerdere stappen | Systeem-breed impact |
| **Risico** | Informatief/herstelbaar | Actie met beperkt risico | Financieel/kritiek/onomkeerbaar |
| **Context** | Geen history nodig | Gedeeltelijke context | Volledige context vereist |
| **Complexiteit** | Template/herhaalbaar | Redenering vereist | Strategisch/nieuw vraagstuk |

**Totaalscore bepaalt tier:**

- Score 4-6 — Tier C
- Score 7-9 — Tier B
- Score 10-12 — Tier A

### 3.2 Escalatieregel

Een agent start altijd op zijn baseline tier. Als het resultaat onvoldoende is:
Download het bestand hierboven en zet het dan op Silver-Surfer:
bashcat > /home/prime/arc_ai_angels/CODEX/CH19_MODEL_ROUTING_STRATEGY.md << 'EOF'
# CH19 — Model Routing Strategy

**Status:** Active  
**Eigenaar:** Supreme Fea  
**Versie:** 1.0 — Juni 2026  
**Van toepassing op:** Alle 33 ARC AI AGENTS agents

---

## 1. Doel van dit hoofdstuk

Dit hoofdstuk beschrijft hoe ARC AI AGENTS omgaat met modelkeuzes. Het legt vast:

- Hoe tiers zijn opgebouwd en wat ze betekenen
- Hoe een agent bepaalt welk tier en model hij gebruikt
- Wat de baseline is per agent en waarom
- Hoe nieuwe agents in de toekomst worden geconfigureerd

Dit document is de enige bron van waarheid voor modelkeuzes binnen ARC.

---

## 2. De drie tiers

### Tier A — Absoluut best

Tier A is gereserveerd voor taken waarbij kwaliteit boven alles gaat. Als een Tier A model de taak niet kan uitvoeren, kan geen enkel ander model dat ook. Tier A wordt ingezet bij:

- Kritieke beslissingen met directe impact (financieel, security, strategie)
- Complexe redenering waarbij nuance essentieel is
- Taken waarbij een fout cascadeert door het systeem
- Nieuwe of onduidelijke vraagstukken zonder precedent

**Modellen in Tier A (goedkoopste eerst):**

| Model | Provider | Sterk in | Input/1M | Output/1M |
|-------|----------|----------|----------|----------|
| Kimi K2.6 | Moonshot | Lange context, redeneren | $0.44 | $2.00 |
| GPT-4o | OpenAI | Structuur, cijfers, code | $2.50 | $10.00 |
| Claude Sonnet 4.6 | Anthropic | Taal, nuance, instructies | $3.00 | $15.00 |
| DeepSeek V4 Pro | DeepSeek | Code, engineering | $0.44 | $0.87 |

> **Keuzeregel Tier A:** Gebruik de goedkoopste optie die de taak aankan. DeepSeek V4 Pro voor code-taken. Kimi K2.6 voor research en redeneren. GPT-4o voor cijfers en structuur. Claude Sonnet alleen als de taak specifiek taalkundige diepgang vereist.

---

### Tier B — Sterk, 90% van de taken

Tier B is de werkhorslaag van ARC. De meeste dagelijkse taken worden hier afgehandeld. Tier B wordt ingezet bij:

- Gestructureerde taken met duidelijke verwachting
- Coördinatie en routing zonder hoge risicodrempel
- Analyses waarbij context groot is maar redenering beperkt
- Taken die herhaalbaar zijn maar nog LLM-intelligentie vereisen

**Modellen in Tier B (goedkoopste eerst):**

| Model | Provider | Sterk in | Input/1M | Output/1M |
|-------|----------|----------|----------|----------|
| Gemini 2.5 Flash | Google | Lange context, snel | $0.30 | $2.50 |
| GPT-4o-mini | OpenAI | Structuur, goedkoop | $0.15 | $0.60 |
| Claude Haiku 4.5 | Anthropic | Taal, instructies | $1.00 | $5.00 |

> **Keuzeregel Tier B:** Gemini 2.5 Flash is de standaard goedkoopste keuze. GPT-4o-mini bij OpenAI-specifieke taken. Claude Haiku voor taaldomein agents waar instructienauwkeurigheid telt.

---

### Tier C — Snel en goedkoop

Tier C is voor routinetaken met lage complexiteit en hoog volume. Fouten hier zijn herstelbaar en hebben weinig impact. Tier C wordt ingezet bij:

- Documentatie, logging, kennisbeheer
- Signaalverwerking en patroondetectie op hoog volume
- Eenvoudige classificatie en routing
- Taken die volledig gestructureerd en voorspelbaar zijn

**Modellen in Tier C (goedkoopste eerst):**

| Model | Provider | Sterk in | Kosten |
|-------|----------|----------|--------|
| Llama 3.3 70B | OpenRouter | Algemeen, gratis | EUR 0 |
| Gemini 3.1 Flash Lite | Google | Snel, goedkoop | $0.10/$0.40 |
| DeepSeek V4 Flash | DeepSeek | Code, structuur | $0.14/$0.28 |

> **Keuzeregel Tier C:** Llama 3.3 70B is altijd de eerste keuze — volledig gratis via OpenRouter. Alleen naar Gemini Flash Lite of DeepSeek Flash als Llama rate-limited is.

---

## 3. Hoe een agent zijn tier kiest

### 3.1 Complexiteitsweging

Elke agent weegt een binnenkomende taak op vier criteria:

| Criterium | Score 1 | Score 2 | Score 3 |
|-----------|---------|---------|---------|
| **Scope** | Enkelvoudige actie | Meerdere stappen | Systeem-breed impact |
| **Risico** | Informatief/herstelbaar | Actie met beperkt risico | Financieel/kritiek/onomkeerbaar |
| **Context** | Geen history nodig | Gedeeltelijke context | Volledige context vereist |
| **Complexiteit** | Template/herhaalbaar | Redenering vereist | Strategisch/nieuw vraagstuk |

**Totaalscore bepaalt tier:**

- Score 4-6 — Tier C
- Score 7-9 — Tier B
- Score 10-12 — Tier A

### 3.2 Escalatieregel

Een agent start altijd op zijn baseline tier. Als het resultaat onvoldoende is:
Tier C mislukt → escaleer naar Tier B
Tier B mislukt → escaleer naar Tier A
Tier A mislukt → rapporteer aan Lead Agent / Flux

Escalatie wordt gelogd zodat patronen zichtbaar worden over tijd.

### 3.3 De-escalatieregel

Bij hoog volume van gelijksoortige taken mag een agent proactief de-escaleren:
Als dezelfde taaksoort 5x succesvol op Tier B → probeer Tier C
Als Tier C 3x succesvol → blijf op Tier C voor dit taaktype

---

## 4. Baseline per agent

### 4.1 Systeem / Orchestratie

| Agent | Domain | Baseline | Tier A | Tier B | Tier C |
|-------|--------|----------|--------|--------|--------|
| nova | system/intake | Tier B — GPT-4o-mini | GPT-4o | GPT-4o-mini | Llama 3.3 70B |
| flux | system/orchestratie | Tier A — Kimi K2.6 | Kimi K2.6 | GPT-4o-mini | Llama 3.3 70B |
| flux_core | system/operations | Tier C — Llama (wordt vervangen) | GPT-4o | Gemini 2.5 Flash | Llama 3.3 70B |

### 4.2 Helix / Tech Domain

**Speciale status:** Tech agents hebben maximale flexibiliteit. Cortexia bepaalt de initiële tierkeuze maar agents mogen overrulen. Alle modellen in alle tiers beschikbaar. DeepSeek uitgesloten voor nero vanwege security.

| Agent | Domain | Baseline | Tier A | Tier B | Tier C |
|-------|--------|----------|--------|--------|--------|
| cortexia | helix/tech | Tier A — DeepSeek V4 Pro | DeepSeek V4 Pro / GPT-4o / Claude Sonnet | GPT-4o-mini / DeepSeek V4 Flash / Gemini 2.5 Flash | Llama 3.3 70B |
| forge | helix/tech/engineering | Tier A — DeepSeek V4 Pro | DeepSeek V4 Pro / GPT-4o / Claude Sonnet | GPT-4o-mini / DeepSeek V4 Flash / Gemini 2.5 Flash | Llama 3.3 70B |
| nero | helix/tech/security | Tier A — GPT-4o | GPT-4o / Claude Sonnet | GPT-4o-mini | Gemini 3.1 Flash Lite |
| ventura | helix/tech/infrastructure | Tier A — DeepSeek V4 Pro | DeepSeek V4 Pro / GPT-4o / Claude Sonnet | GPT-4o-mini / DeepSeek V4 Flash | Llama 3.3 70B |
| axon | helix/tech/automation | Tier A — DeepSeek V4 Pro | DeepSeek V4 Pro / GPT-4o / Claude Sonnet | GPT-4o-mini / DeepSeek V4 Flash / Gemini 2.5 Flash | Llama 3.3 70B |
| clio | helix/tech/documentation | Tier C — Llama 3.3 70B | GPT-4o / Claude Sonnet | GPT-4o-mini / Gemini 2.5 Flash | Llama 3.3 70B |

### 4.3 Finix / Finance Domain

| Agent | Domain | Baseline | Tier A | Tier B | Tier C |
|-------|--------|----------|--------|--------|--------|
| finoria | finix/finance | Tier B — Gemini 2.5 Flash | GPT-4o | Gemini 2.5 Flash | Llama 3.3 70B |
| vector | finix/finance/strategy | Tier A — GPT-4o | GPT-4o | Gemini 2.5 Flash | Llama 3.3 70B |
| kairo | finix/finance/treasury | Tier B — Gemini 2.5 Flash | GPT-4o | Gemini 2.5 Flash | Llama 3.3 70B |
| kenzo | finix/finance/controls | Tier B — Gemini 2.5 Flash | GPT-4o | Gemini 2.5 Flash | Llama 3.3 70B |
| odis | finix/finance/audit | Tier B — Gemini 2.5 Flash | GPT-4o | Gemini 2.5 Flash | Llama 3.3 70B |
| zion | finix/finance/accounting | Tier C — Llama 3.3 70B | GPT-4o | Gemini 2.5 Flash | Llama 3.3 70B |

### 4.4 Matrix / Intelligence Domain

| Agent | Domain | Baseline | Tier A | Tier B | Tier C |
|-------|--------|----------|--------|--------|--------|
| saelia | matrix/intelligence | Tier B — Gemini 2.5 Flash | Kimi K2.6 | Gemini 2.5 Flash | Llama 3.3 70B |
| tharos | matrix/intelligence/strategic | Tier A — Kimi K2.6 | Kimi K2.6 | Gemini 2.5 Flash | Llama 3.3 70B |
| sora | matrix/intelligence/synthesis | Tier B — Gemini 2.5 Flash | Kimi K2.6 | Gemini 2.5 Flash | Llama 3.3 70B |
| arix | matrix/intelligence/research | Tier B — Gemini 2.5 Flash | Kimi K2.6 | Gemini 2.5 Flash | Llama 3.3 70B |
| enki | matrix/intelligence/knowledge | Tier C — Llama 3.3 70B | Kimi K2.6 | Gemini 2.5 Flash | Llama 3.3 70B |
| daxio | matrix/intelligence/signals | Tier C — Llama 3.3 70B | Kimi K2.6 | Gemini 2.5 Flash | Llama 3.3 70B |

### 4.5 Quantix / Data-Intelligence Domain

| Agent | Domain | Baseline | Tier A | Tier B | Tier C |
|-------|--------|----------|--------|--------|--------|
| lumeria | quantix/data-intelligence | Tier B — Gemini 2.5 Flash | Kimi K2.6 | Gemini 2.5 Flash | Llama 3.3 70B |
| kresta | quantix/data-intelligence/analytics | Tier B — Gemini 2.5 Flash | Kimi K2.6 | Gemini 2.5 Flash | Llama 3.3 70B |
| elora | quantix/data-intelligence/research | Tier B — Gemini 2.5 Flash | Kimi K2.6 | Gemini 2.5 Flash | Llama 3.3 70B |
| luvia | quantix/data-intelligence/forecasting | Tier B — Gemini 2.5 Flash | Kimi K2.6 | Gemini 2.5 Flash | Llama 3.3 70B |
| nura | quantix/data-intelligence/knowledge | Tier C — Llama 3.3 70B | Kimi K2.6 | Gemini 2.5 Flash | Llama 3.3 70B |
| vondra | quantix/data-intelligence/signals | Tier C — Llama 3.3 70B | Kimi K2.6 | Gemini 2.5 Flash | Llama 3.3 70B |

### 4.6 Zenix / Language-Communication Domain

| Agent | Domain | Baseline | Tier A | Tier B | Tier C |
|-------|--------|----------|--------|--------|--------|
| fluentia | zenix/language-communication | Tier B — Gemini 2.5 Flash | Kimi K2.6 | Gemini 2.5 Flash | Llama 3.3 70B |
| draven | zenix/language-communication/copy | Tier B — GPT-4o-mini | Kimi K2.6 | GPT-4o-mini | Llama 3.3 70B |
| solis | zenix/language-communication/storytelling | Tier B — Gemini 2.5 Flash | Kimi K2.6 | Gemini 2.5 Flash | Llama 3.3 70B |
| orizon | zenix/language-communication/strategy | Tier B — Gemini 2.5 Flash | Kimi K2.6 | Gemini 2.5 Flash | Llama 3.3 70B |
| unia | zenix/language-communication/editorial | Tier C — Llama 3.3 70B | Kimi K2.6 | GPT-4o-mini | Llama 3.3 70B |
| zena | zenix/language-communication/localization | Tier C — Llama 3.3 70B | Kimi K2.6 | GPT-4o-mini | Llama 3.3 70B |

---

## 5. Hoe een nieuwe agent geconfigureerd wordt

### Stap 1 — Bepaal domain en rol
- In welk domain? (helix / finix / matrix / quantix / zenix / system)
- Wat is de primaire taak?
- Hoe kritiek zijn fouten?

### Stap 2 — Bepaal taakcategorie

| Taakcategorie | Voorbeelden | Startpunt tier |
|---------------|-------------|----------------|
| Orchestratie/routing | Flux, Omni Leads | A of B |
| Code/Engineering | Forge, Axon | A |
| Security/Kritiek | Nero, Vector | A |
| Analyse/Research | Kresta, Arix | B |
| Coördinatie | Cortexia, Finoria | B |
| Documentatie/Kennisbeheer | Clio, Enki | C |
| Signalen/Volume | Daxio, Vondra | C |

### Stap 3 — Kies modellen op basis van domeinprofiel

| Domain profiel | Tier A | Tier B | Tier C |
|----------------|--------|--------|--------|
| Code/Tech | DeepSeek V4 Pro | GPT-4o-mini | Llama 3.3 70B |
| Finance/Cijfers | GPT-4o | Gemini 2.5 Flash | Llama 3.3 70B |
| Research/Lange context | Kimi K2.6 | Gemini 2.5 Flash | Llama 3.3 70B |
| Taal/Content | Kimi K2.6 | GPT-4o-mini | Llama 3.3 70B |
| Strategie/Nuance | Kimi K2.6 / Claude Sonnet | Gemini 2.5 Flash | Llama 3.3 70B |

### Stap 4 — Vastleggen in models.json en MODEL.md

Elke nieuwe agent krijgt:
- `agent/models.json` met alle providers en modellen
- `MODEL.md` met baseline tier, beschikbare modellen, escalatieregels

---

## 6. Uitzonderingen

- **Tech domain:** Maximale flexibiliteit, agents overrulen Cortexia indien nodig
- **Nero:** DeepSeek uitgesloten — geen gevoelige data op Chinese infra
- **Nova:** Credit budget bewaken, bij uitputting naar Tier C Llama
- **Flux:** Kimi K2.6 credit bewaken, bij uitputting naar Tier B GPT-4o-mini

---

## 7. LiteLLM model namen (localhost:4000)

| LiteLLM naam | Model | Tier |
|--------------|-------|------|
| arc-nova | Claude Sonnet 4.6 via OpenRouter | A |
| arc-high | Claude Haiku 4.5 via OpenRouter | B |
| arc-mid | Gemini 2.0 Flash via OpenRouter | B |
| arc-mid-openai | GPT-4o-mini direct | B |
| arc-mid-moonshot | Kimi K2.5 via Moonshot | B |
| arc-low | Llama 3.3 70B via OpenRouter | C |
| gemini-flash | Gemini 3.1 Flash Lite direct | C |
| gemini-pro | Gemini 2.5 Flash direct | B |

---

## 8. Revisiehistorie

| Versie | Datum | Wijziging |
|--------|-------|-----------|
| 1.0 | Juni 2026 | Initiële versie — alle 33 agents geconfigureerd |

---

*Dit document is onderdeel van de ARC AI AGENTS CODEX. Beheerd door Supreme Fea.*
