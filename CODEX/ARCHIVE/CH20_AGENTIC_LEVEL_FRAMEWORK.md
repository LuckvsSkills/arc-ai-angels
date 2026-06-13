# CH20 — Agentic Level Framework

**Status:** Active  
**Eigenaar:** Supreme Fea  
**Versie:** 1.0 — Juni 2026  
**Van toepassing op:** Alle 33 ARC AI AGENTS agents

---

## 1. Doel van dit hoofdstuk

Dit hoofdstuk beschrijft het agentic level framework van ARC AI AGENTS. Het legt vast:

- Wat elk agentic level betekent en wanneer het van toepassing is
- De routing regels tussen agents
- Het agentic level per agent
- Hoe het systeem groeit van Fase 1 naar Fase 2

---

## 2. Architectuur — hoe het systeem werkt
bashcat > /home/prime/arc_ai_angels/CODEX/CH20_AGENTIC_LEVEL_FRAMEWORK.md << 'EOF'
# CH20 — Agentic Level Framework

**Status:** Active  
**Eigenaar:** Supreme Fea  
**Versie:** 1.0 — Juni 2026  
**Van toepassing op:** Alle 33 ARC AI AGENTS agents

---

## 1. Doel van dit hoofdstuk

Dit hoofdstuk beschrijft het agentic level framework van ARC AI AGENTS. Het legt vast:

- Wat elk agentic level betekent en wanneer het van toepassing is
- De routing regels tussen agents
- Het agentic level per agent
- Hoe het systeem groeit van Fase 1 naar Fase 2

---

## 2. Architectuur — hoe het systeem werkt
Supreme Fea
↓
NOVA (vertaallaag)
↓
FLUX (brain/regisseur)
↓
Omni Leads (domein coördinatie)
↓
Sentinels (uitvoering)

**Supreme Fea** geeft richting aan NOVA. NOVA vertaalt eenvoudige verzoeken zelf af of maakt er een project van voor FLUX. FLUX is de regisseur — hij verdeelt projecten naar Omni Leads, houdt overzicht en gatekeept alle cross-domain verkeer. Omni Leads coördineren hun domein en verdelen taken naar Sentinels.

### Routing regels

**Binnen domein:**
Sentinel → Lead informeert FLUX achteraf

**Cross-domain:**
Sentinel heeft andere agent nodig → meldt aan eigen Lead → Lead vraagt aan FLUX → FLUX benadert andere Lead

**Lead naar Lead:**
Omni Lead mag direct andere Omni Lead benaderen → FLUX achteraf inlichten

**Kritieke situaties (security/financieel):**
Direct escaleren naar Lead + FLUX tegelijk

---

## 3. De vier agentic levels

### Level 1 — Uitvoerend

De agent voert alleen uit wat zijn Lead hem expliciet opdraagt. Geen eigen initiatief. Elke afwijking van instructies wordt geëscaleerd. Ideaal voor gestructureerde, herhaalbare taken met hoge nauwkeurigheidseisen.

**Kenmerken:**
- Voert instructies uit zonder eigen interpretatie
- Escaleert bij elke afwijking of onduidelijkheid
- Rapporteert altijd terug na uitvoering
- Geen cross-domain contact

**Van toepassing op:** zion, zena

---

### Level 2 — Beperkt autonoom

De agent mag kleine beslissingen nemen binnen zijn taakscope. Als iets buiten scope valt escaleert hij naar zijn Lead. Rapporteert na uitvoering. Ideaal voor taken die herhaalbaar zijn maar wel LLM-intelligentie vereisen.

**Kenmerken:**
- Kleine scope beslissingen zelfstandig
- Escaleert bij twijfel of risico
- Rapporteert resultaten aan Lead
- Geen eigen initiatieven buiten taakopdracht

**Van toepassing op:** clio, kenzo, odis, arix, enki, daxio, elora, nura, vondra, unia

---

### Level 3 — Domein autonoom

De agent mag initiatieven nemen binnen zijn domein. Bij grotere acties of conclusies die actie vereisen informeert hij zijn Lead vóórdat hij handelt. Kan aangeven dat hij andere agents nodig heeft via zijn Lead.

**Kenmerken:**
- Initiatief nemen binnen domein
- Informeert Lead vooraf bij impactvolle acties
- Geeft aan wanneer hij andere agents nodig heeft
- Rapporteert bevindingen proactief

**Van toepassing op:** ventura, axon, vector, kairo, tharos, sora, kresta, luvia, draven, solis, orizon — en Omni Leads lumeria, saelia, fluentia

---

### Level 4 — Volledig autonoom

De agent handelt zelfstandig en rapporteert achteraf. Omni Leads mogen direct andere Omni Leads benaderen met FLUX achteraf inlichten. Sentinels op Level 4 zijn specialisten waarbij wachten op goedkeuring te kostbaar is.

**Kenmerken:**
- Volledig zelfstandig handelen
- Rapporteert achteraf aan Lead of FLUX
- Omni Leads: mogen direct andere Leads benaderen
- Specialisten: directe actie bij urgente situaties

**Van toepassing op:** forge, nero — en Omni Leads cortexia, finoria

---

## 4. Agentic level per agent

### Systeem / Orchestratie

| Agent | Rol | Level | Toelichting |
|-------|-----|-------|-------------|
| nova | Vertaallaag | Speciaal | Eenvoudig: zelf afhandelen. Complex: project naar FLUX |
| flux | Brain/Regisseur | Speciaal | Orkestreert alles, gatekeept cross-domain, beheert projecten |
| flux_core | Operations | Vervangen | Nieuwe agent — naam/rol/level nog te bepalen |

### Helix / Tech Domain

| Agent | Rol | Level | Routing |
|-------|-----|-------|---------|
| cortexia | Omni Lead | 4 | Direct naar andere Leads. FLUX achteraf |
| forge | Engineering | 4 | Specialist. Cortexia achteraf. Cross-domain via Cortexia |
| nero | Security | 4 | Specialist. Cortexia achteraf. Kritiek: Cortexia + FLUX direct |
| ventura | Infrastructure | 3 | Cortexia vooraf bij impact acties. Routine autonoom |
| axon | Automation | 3 | Cortexia vooraf bij nieuwe pipelines. Onderhoud autonoom |
| clio | Documentation | 2 | Cortexia bij structuurwijzigingen. Schrijftaken autonoom |

### Finix / Finance Domain

| Agent | Rol | Level | Routing |
|-------|-----|-------|---------|
| finoria | Omni Lead | 4 | Direct naar andere Leads. FLUX achteraf. Grote financiële acties via FLUX vooraf |
| vector | Strategy | 3 | Finoria vooraf bij strategische aanbevelingen |
| kairo | Treasury | 3 | Finoria bij afwijkingen. Monitoring autonoom |
| kenzo | Controls | 2 | Finoria bij gevonden issues. Validaties autonoom |
| odis | Audit | 2 | Finoria bij audit bevindingen. Documenteren autonoom |
| zion | Accounting | 1 | Finoria bij elke afwijking. Registraties per instructie |

### Matrix / Intelligence Domain

| Agent | Rol | Level | Routing |
|-------|-----|-------|---------|
| saelia | Omni Lead | 3 | Informeert FLUX vooraf bij cross-domain. Kan groeien naar 4 |
| tharos | Strategic | 3 | Saelia vooraf bij strategische conclusies |
| sora | Synthesis | 3 | Saelia bij grote synthese outputs |
| arix | Research | 2 | Saelia met onderzoeksresultaten |
| enki | Knowledge | 2 | Saelia bij structuurwijzigingen |
| daxio | Signals | 2 | Saelia bij kritieke signalen. Detectie autonoom |

### Quantix / Data-Intelligence Domain

| Agent | Rol | Level | Routing |
|-------|-----|-------|---------|
| lumeria | Omni Lead | 3 | Informeert FLUX vooraf bij cross-domain. Kan groeien naar 4 |
| kresta | Analytics | 3 | Lumeria bij significante bevindingen |
| elora | Research | 2 | Lumeria met onderzoeksresultaten |
| luvia | Forecasting | 3 | Lumeria bij prognoses met actie-implicaties |
| nura | Knowledge | 2 | Lumeria bij structuurwijzigingen |
| vondra | Signals | 2 | Lumeria bij kritieke signalen |

### Zenix / Language-Communication Domain

| Agent | Rol | Level | Routing |
|-------|-----|-------|---------|
| fluentia | Omni Lead | 3 | Informeert FLUX vooraf bij cross-domain. Kan groeien naar 4 |
| draven | Copy | 3 | Fluentia bij nieuwe campagnes |
| solis | Storytelling | 3 | Fluentia bij nieuwe narratieven |
| orizon | Strategy | 3 | Fluentia bij strategische richtingsbeslissingen |
| unia | Editorial | 2 | Fluentia bij grote toonwijzigingen |
| zena | Localization | 1 | Fluentia bij toonafwijkingen. Lokalisatie per richtlijnen |

---

## 5. Approval gates

Bepaalde acties vereisen altijd goedkeuring — ongeacht het agentic level van de agent:

| Actie | Gate | Wie keurt goed |
|-------|------|----------------|
| Grote financiële beslissingen | Verplicht | FLUX vooraf |
| Security mitigatie systeem-breed | Verplicht | FLUX vooraf |
| Nieuwe cross-domain pipeline | Verplicht | FLUX vooraf |
| Kritieke dreiging | Direct escalatie | Cortexia + FLUX tegelijk |
| Deployment productie | Verplicht | Cortexia vooraf |

---

## 6. Groeipaden

Drie Omni Leads starten op Level 3 en kunnen groeien naar Level 4 zodra hun domein bewezen stabiel is:

- **lumeria** → Level 4 zodra Quantix domein 30 dagen stabiel draait
- **saelia** → Level 4 zodra Matrix domein 30 dagen stabiel draait
- **fluentia** → Level 4 zodra Zenix domein 30 dagen stabiel draait

Groei naar Level 4 wordt vastgelegd door Supreme Fea na evaluatie.

---

## 7. Fase 1 naar Fase 2 transitie

Het systeem bevindt zich nu in Fase 2 — Structured Freedom:

- Sentinels mogen lokale beslissingen nemen
- Omni Leads kunnen cross-domain routing doen
- Approval gates voor risicovolle acties
- FLUX blijft brain en regisseur

**Fase 3 (toekomst):** Agents initiëren projecten zelf op basis van signalen en memory — zonder dat Supreme Fea het verzoek doet.

---

## 8. Revisiehistorie

| Versie | Datum | Wijziging |
|--------|-------|-----------|
| 1.0 | Juni 2026 | Initiële versie — alle 33 agents geconfigureerd |

---

*Dit document is onderdeel van de ARC AI AGENTS CODEX. Beheerd door Supreme Fea.*
