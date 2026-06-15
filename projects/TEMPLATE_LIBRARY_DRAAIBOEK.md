# Hoofdproject: Website Template Library — 52 Templates in 4 Maanden

**Hoofduitvoerder: Forge** (alle 52 templates, bouwproces stappen 1-7, GitHub repos, clone_template.py integratie)

## DOEL
Forge bouwt een library van 52 kant-en-klare, high-end website-templates
(12 types x 4 stijlvarianten + 1 hybride-retail type x 4 sectorvarianten).
Resultaat: als een klantverzoek binnenkomt, kiest Forge het juiste type + stijl
uit de library en personaliseert deze SNEL naar een MVP voor de klant.

Tot de library compleet is, is elk klantverzoek nog handmatig/intensief werk
voor Forge (zoals nu). Na 4 maanden is het grotendeels kiezen + personaliseren.

---

## BOUWVOLGORDE: 4 MAANDEN, PER MAAND 13 TYPES IN 1 STIJL

### MAAND 1 — Stijl/Variant 1 (V1) van alle 13 types
| # | Type | Referentie (clone) |
|---|---|---|
| 1 | landing | notion |
| 2 | portfolio | pentagram |
| 3 | blog | stripe blog |
| 4 | bedrijf | ikea |
| 5 | ecommerce | patagonia |
| 6 | booking | opentable |
| 7 | marketplace | etsy |
| 8 | saas | linear |
| 9 | community | discourse |
| 10 | dashboard | vercel |
| 11 | directory | yelp |
| 12 | api | stripe docs |
| 13 | hybride-retail | bakkerij (Kwik-Fit kalender + voorraad) |

### MAAND 2 — Stijl/Variant 2 (V2) van alle 13 types
| # | Type | Referentie (clone) |
|---|---|---|
| 1 | landing | linear |
| 2 | portfolio | brittanychiang |
| 3 | blog | theverge |
| 4 | bedrijf | basecamp |
| 5 | ecommerce | shopify |
| 6 | booking | calendly |
| 7 | marketplace | vinted |
| 8 | saas | figma |
| 9 | community | dev.to |
| 10 | dashboard | tremor.so |
| 11 | directory | g2 |
| 12 | api | github docs |
| 13 | hybride-retail | bloemist (kalender + voorraad) |

### MAAND 3 — Stijl/Variant 3 (V3) van alle 13 types
| # | Type | Referentie (clone) |
|---|---|---|
| 1 | landing | raycast |
| 2 | portfolio | ueno |
| 3 | blog | seths.blog |
| 4 | bedrijf | mailchimp |
| 5 | ecommerce | gymshark |
| 6 | booking | fresha |
| 7 | marketplace | airbnb |
| 8 | saas | slack |
| 9 | community | producthunt |
| 10 | dashboard | stripe dashboard |
| 11 | directory | producthunt/topics |
| 12 | api | notion developers |
| 13 | hybride-retail | slagerij/traiteur (kalender + voorraad) |

### MAAND 4 — Stijl/Variant 4 (V4) van alle 13 types
| # | Type | Referentie (clone) |
|---|---|---|
| 1 | landing | superhuman |
| 2 | portfolio | basicagency |
| 3 | blog | buffer resources |
| 4 | bedrijf | monograph |
| 5 | ecommerce | glossier |
| 6 | booking | resy |
| 7 | marketplace | marktplaats |
| 8 | saas | airtable |
| 9 | community | indiehackers |
| 10 | dashboard | notion workspace |
| 11 | directory | clutch.co |
| 12 | api | anthropic docs |
| 13 | hybride-retail | wijnhandel/delicatessen (kalender + voorraad) |

EXTRA (los van de 52, apart project): sportsite Fea op basis van oddsportal.com

---

## SPECIAAL: HYBRIDE-RETAIL TYPE (#13, elke maand)

Dit type is GEEN directe clone - moet zelf gebouwd worden (zie WEBSITE_DELIVERY_PIPELINE.md
sectie "TEMPLATE-CATEGORIEEN"). Dit is de TECHNISCH MEEST UITDAGENDE template:
- Kalender/agenda-component (Kwik-Fit-stijl: dienst kiezen, beschikbare dagen tonen, reserveren)
- Voorraad-retail component (bestaande ecommerce-logica)
- BELANGRIJK: deze techniek (kalender-component) wordt 1x GOED gebouwd in Maand 1 (#13),
  en in Maand 2-4 alleen qua STIJL aangepast (zelfde techniek, andere look/sector).
  Dus Maand 1 #13 is het zwaarste werk; Maand 2-4 #13 is veel sneller.

---

## PER-TEMPLATE BOUWPROCES (wat Forge per template doet)

1. **Referentie-analyse**: sectie-structuur van de clone-referentie in kaart brengen
   (desktop + mobiel layout, welke componenten, volgorde)
2. **HTML/CSS herbouwen**: bestaande template-skelet aanpassen naar die sectie-structuur,
   met onze STIJL_VARS (kleuren/fonts blijven ons systeem, layout volgt de referentie)
3. **JS-functionaliteit**: eigen lichte vanilla-JS (zoals nu al gedaan voor cart/booking/filters)
4. **Backend-koppeling-punten markeren**: welke data komt straks uit de generieke backend
   (content_blocks/products/bookings/listings) - nog niet implementeren, wel voorbereiden
5. **Responsive QA**: testen op 375/768/1280px, hamburger/scroll-fixes waar nodig
   (zoals vanavond gedaan)
6. **Naar GitHub repo**: template-[type]-v[1-4] of vergelijkbare naming
7. **Testen met clone_template.py**: 1 voorbeeldproject genereren, checken of personalisatie werkt

---

## PARALLEL TRAJECT: BACKEND-ARCHITECTUUR

Terwijl Forge de 52 templates bouwt, loopt parallel (andere agent, bv. Axon):
- Backend-stack keuze (Supabase vs Pocketbase) - ZIE OPEN VRAGEN
- Generieke data-modellen bouwen (content_blocks, products, bookings, listings, users, api_resources)
- Admin/CMS laag

Dit hoeft niet per-template te gebeuren - 1x bouwen, aansluiten op de "koppel-punten"
die Forge per template markeert (stap 4 in bouwproces hierboven).

---

## MCC PROJECT-TAB: HOE DIT PROJECT ERIN KOMT

Dit hoofdproject ("Website Template Library - 52 Templates") wordt 1 INTERN PROJECT
in de MCC Project-tab, met:
- Hoofdstatus: In Progress (Maand 1 bezig)
- Subtaken: 52 templates, elk als checklist-item met status (Open/Bezig/Klaar)
- Voortgang: X/52 templates klaar, huidige maand, huidige type
- Per template-subtaak: klikbaar naar detail (referentie, GitHub repo link, status bouwproces stappen 1-7)

Daarnaast: backend-architectuur traject als eigen subtaak/project binnen dit hoofdproject.

TE BOUWEN (volgende sessie): data-model voor dit project + subtaken, Kanban-weergave in MCC.

---

## HUIDIGE STAND VAN ZAKEN (start Maand 1)

- 13/13 "oude" templates bestaan al (gebouwd eerdere sessies) - dit zijn de BASIS-SKELETTEN
  (HTML/CSS/JS structuur, STIJL_VARS systeem, clone_template.py werkt)
- Deze oude 13 worden NIET weggegooid - ze worden HERBOUWD/herzien naar de clone-referenties
  als Maand 1 V1-set (of als uitgangspunt/skelet voor de nieuwe structuur)
- Responsive QA al gedaan voor 5/13 (dashboard, bakkerij, marketplace, community, directory)
  vanavond - deze fixes blijven relevant, ook na herbouw

## VOLGENDE SESSIE PRIORITEIT
1. MCC Project-tab data-model + basis-UI (Kanban: Open/Bezig/Klaar, klant vs intern filter)
2. Dit hoofdproject + 52 subtaken erin laden
3. Start Maand 1 #1: landing-V1 (notion) - referentie-analyse + herbouw als pilot
3b. Parallel: backend-stack keuze (Supabase vs Pocketbase) - kort onderzoek

---

## ROADMAP (NIET NU BOUWEN - toekomstige stappen)

Deze punten zijn bewust NOG NIET in uitvoering. Ze staan hier zodat ze niet vergeten
worden en op het juiste moment opgepakt kunnen worden.

### Roadmap-item 1: MCC Project-tab
Status: IDEE / TOEKOMST, geen bouwwerk gepland voor nu.
Wat het moet worden (als het wordt opgepakt):
- Kanban-overzicht (Open/Bezig/Klaar) voor projecten
- Filter: Klant-projecten vs Interne projecten
- Dit Template Library project als 1 kaart met 52 subtaken
- Per project: detailpagina met type, stappen, voortgang, voortgangsbalk/flowchart
- Fea kan hier instructies achterlaten die Forge oppikt (alternatief voor Telegram bij dit project)

Trigger om dit op te pakken: zodra de huidige prioriteiten (Maand 1 templates, backend-stack
keuze, Kwik-Fit kalender) voldoende voortgang hebben, OF wanneer het missen van een
projectoverzicht echt gaat knellen in de dagelijkse workflow.

### Roadmap-item 2: 24-uur klant-MVP flow (DEEL A oorspronkelijk draaiboek)
Status: DOEL/EINDRESULTAAT van dit hele project, niet iets om nu te bouwen.
Wordt relevant zodra de 52-template library compleet is (eind Maand 4) of grotendeels
(bv. na Maand 1, met 13 templates als interim-aanbod).
