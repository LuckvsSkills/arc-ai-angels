# Masterplan: 52 Templates naar Volledige Websites — A tot Z

## KERNINZICHT
1 generieke backend-architectuur + 52 frontend-template-variaties (4 per type x 13 types)
= snelheid zit in HERGEBRUIK, niet in per-klant herbouwen.

Tijdlijn: 4 maanden voor 52 templates volledig uitgebouwd + 13 types end-to-end werkend.

---

## DEEL 1: DE 52 TEMPLATES

### 12 Clone-fahige types x 4 varianten = 48
| Type | V1 | V2 | V3 | V4 |
|---|---|---|---|---|
| landing | notion | linear | raycast | superhuman |
| portfolio | pentagram | brittanychiang | ueno | basicagency |
| blog | stripe blog | theverge | seths.blog | buffer resources |
| bedrijf | ikea | basecamp | mailchimp | monograph |
| ecommerce | patagonia | shopify | gymshark | glossier |
| booking | opentable | calendly | fresha | resy |
| marketplace | etsy | vinted | airbnb | marktplaats |
| saas | linear | figma | slack | airtable |
| community | discourse | dev.to | producthunt | indiehackers |
| dashboard | vercel | tremor.so | stripe dashboard | notion workspace |
| directory | yelp | g2 | producthunt/topics | clutch.co |
| api | stripe docs | github docs | notion developers | anthropic docs |

### 1 Hybride-Retail type x 4 sectorvarianten = 4
| Type | V1 | V2 | V3 | V4 |
|---|---|---|---|---|
| hybride-retail | bakkerij | bloemist | slagerij/traiteur | wijnhandel/delicatessen |
Techniek: kalender (Kwik-Fit-stijl) + voorraad-retail combinatie

TOTAAL: 48 + 4 = 52 templates

EXTRA (apart project, niet in de 52): sportsite Fea op basis van oddsportal.com structuur (directory comparison-aggregator)

---

## DEEL 2: DE EEN-KEER BACKEND-ARCHITECTUUR

Doel: 1x bouwen, herbruikbaar voor alle 52 templates via configuratie, niet code-duplicatie.

### Backend stack (te bevestigen in research)
- Database/CMS: Supabase of Pocketbase (gratis tier, self-host mogelijk)
- Auth: ingebouwd in Supabase/Pocketbase
- Forms: Formspree of Web3Forms voor contactformulieren
- Media: Cloudflare R2 / Bunny.net voor foto/video opslag
- Hosting: Vercel (al in gebruik)

### Generieke data-modellen (herbruikbaar over templates)
1. **content_blocks** - voor landing/portfolio/blog/bedrijf/saas (tekst/afbeelding secties per pagina)
2. **products** - voor ecommerce/marketplace/hybride-retail (naam, prijs, voorraad, levertijd, categorie)
3. **bookings/services** - voor booking/hybride-retail kalender (diensten, openingstijden, sloten)
4. **listings** - voor directory/marketplace/community (entries met categorie, contact, locatie)
5. **users/accounts** - voor community/dashboard/marketplace (login, profiel)
6. **api_resources** - voor api-type (CRUD resources, FastAPI achtig zoals al gebouwd)

Elke template-type mapt naar 1-3 van deze modellen. EEN backend-laag, per project geconfigureerd welke modellen actief zijn.

### Admin/CMS laag (klant-zelfbeheer)
- Eenvoudig admin-paneel (gekoppeld aan Supabase/Pocketbase auth)
- Klant kan: content_blocks bewerken, products toevoegen, bookings beheren, listings updaten
- 1x bouwen, herbruikbaar via dezelfde data-modellen

---

## DEEL 3: FLOWCHART 1 — VAN VERZOEK NAAR TEMPLATE-KEUZE
[Klant verzoek via Telegram/Nova]

  |

v

[Intake Wizard - Nova]

Welk type website? (1 van 13 types)
Welke stijl/sfeer? (toon 4 varianten van dat type)

|

v

[Klant kiest 1 van 4 templates]
Klant ziet 4 live previews (V1-V4 van gekozen type)
Kiest op basis van look & feel

|

v

[PROJECT_BRIEF.json gegenereerd]
type, gekozen variant (V1-V4), stijl-kleuren, content-info

|

      v

[Door naar FLOWCHART 2]
[Klant verzoek via Telegram/Nova]

  |

v

[Intake Wizard - Nova]

Welk type website? (1 van 13 types)
Welke stijl/sfeer? (toon 4 varianten van dat type)

|

v

[Klant kiest 1 van 4 templates]
Klant ziet 4 live previews (V1-V4 van gekozen type)
Kiest op basis van look & feel

|

v

[PROJECT_BRIEF.json gegenereerd]
type, gekozen variant (V1-V4), stijl-kleuren, content-info

|

      v

[Door naar FLOWCHART 2]
[PROJECT_BRIEF.json]

|

v

[Forge: clone_template.py]

Kloon gekozen variant (bv. ecommerce-V2-shopify)
Injecteer stijl-variabelen
Personaliseer placeholders (naam, beschrijving)

|

v

[Axon: Backend koppelen]
Activeer relevante data-modellen (zie Deel 2)
Setup Supabase/Pocketbase project-instance
Vul met placeholder/demo-content

|

v

[Ventura/Clio: Content invullen]
Klant-aangeleverde teksten/foto's verwerken
Stockfoto's indien nodig (Unsplash/Pexels API)
SEO basis (meta tags, alt-teksts)

|

v

[Forge: Responsive QA]
Test op 375/768/1280px
Fix breakpoint-issues

|

v

[Forge: Deploy naar Vercel]
Live URL
Domein koppelen

|

v

[Cortexia -> Nova: Overdracht]
Documentatie + admin-toegang aan klant
Edit-request systeem uitleggen

|

v

[LIVE MVP VOOR KLANT]

|

v

[Fase 8: Nazorg via EDIT_REQUEST_SYSTEM.md]
---

## DEEL 5: 4-MAANDEN PLANNING

### Maand 1: Backend-architectuur + eerste 13 templates (V1 van elk type)
- Week 1-2: Backend-stack kiezen + bouwen (Deel 2)
- Week 3-4: 13 V1-templates herbouwen volgens hun referentie (clone-proces, fase 1-5 uit pipeline)

### Maand 2: V1-templates koppelen aan backend + eerste end-to-end MVP
- Week 1-2: Backend koppelen aan alle 13 V1-templates
- Week 3-4: 1 volledige end-to-end test (intake -> live site) met 1 V1-template, proces verfijnen

### Maand 3: V2 en V3 templates (26 templates)
- Week 1-2: 13 V2-templates bouwen
- Week 3-4: 13 V3-templates bouwen
- Doorlopend: backend-koppeling per template

### Maand 4: V4-templates (13) + hybride-retail 4 varianten + afronding
- Week 1-2: 13 V4-templates bouwen
- Week 3: Hybride-retail 4 sectorvarianten (incl. Kwik-Fit kalender-techniek)
- Week 4: Eindtest alle 52, documentatie compleet, sportsite Fea als bonus-project

---

## OPEN ONDERZOEKSVRAGEN (voor te bevestigen)

1. Supabase vs Pocketbase - welke past beter bij onze stack/agenten?
2. Kwik-Fit kalender-component - hoe technisch op te bouwen (vanilla JS vs library)?
3. Admin/CMS UI - bouwen wij zelf of gebruiken we Pocketbase's ingebouwde admin?
4. Stockfoto-pipeline - Unsplash API integratie in clone_template.py?

---

## VOLGENDE SESSIE PRIORITEIT
1. Backend-stack keuze maken (Supabase vs Pocketbase) - research
2. Eerste V1-template (welke?) volledig herbouwen volgens clone-proces als pilot
3. Kwik-Fit kalender onderzoeken
