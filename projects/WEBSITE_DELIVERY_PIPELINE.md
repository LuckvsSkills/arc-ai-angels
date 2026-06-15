# Website Delivery Pipeline — A tot Z

Dit document beschrijft ALLE stappen van klantverzoek tot live website + nazorg.
Een template (zie WEBSITE_TAXONOMIE.md) is slechts ÉÉN bouwsteen binnen deze pipeline.
Doel: een herhaalbaar, voorspelbaar proces waarbij elke agent weet wat zijn rol is en wanneer.

---

## FASE 0 — INTAKE
**Wie:** Nova (Telegram intake wizard)
**Input:** Klantverzoek
**Output:** PROJECT_BRIEF.json
**Status:** Bestaat (INTAKE_WIZARD.md)

Stappen:
1. Type website (12 templates + bakkerij-variant)
2. Stijl (6 vaste opties naar STIJL_VARS)
3. Functionaliteit-modules (FUNCTIONALITEIT_MODULES.md, 12 modules)
4. Aantal pagina's / sitemap
5. Content-aanlevering (tekst, foto's, logo's)
6. Domeinnaam + hosting-voorkeur
7. Prijsindicatie + bouwtijd
8. Akkoord klant

OPEN VRAGEN:
- Hoe levert klant content aan (upload-portaal, e-mail, formulier)?
- Wie bepaalt sitemap/aantal pagina's bij multi-pagina templates?

---

## FASE 1 — PROJECT SETUP
**Wie:** Flux naar Cortexia (Helix Omni Lead)
**Input:** PROJECT_BRIEF.json
**Output:** Project directory + GitHub repo + taakverdeling
**Status:** Deels (Flux routing herschreven, Cortexia routing nog niet compleet)

Stappen:
1. Project directory aanmaken (projects/website_builds/[klant]/)
2. GitHub repo aanmaken voor het project (apart van templates)
3. Taken verdelen naar Forge/Axon/Nero/Ventura/Clio
4. Tijdlijn/planning vastleggen

---

## FASE 2 — BOUW (CODE)
**Wie:** Forge (lead), Axon (database), Nero (security/backend)
**Input:** PROJECT_BRIEF.json + template
**Output:** Werkende codebase
**Status:** clone_template.py klaar, 13/13 templates beschikbaar

Stappen:
1. Template klonen + stijl injecteren (clone_template.py)
2. Personalisatie placeholders
3. Database/CMS opzetten (Axon) - NOG TE ONTWERPEN
4. Backend/API koppelen waar nodig (Nero)
5. Multi-pagina structuur opbouwen indien van toepassing - NOG TE ONTWERPEN

---

## FASE 3 — CONTENT
**Wie:** Ventura (content/copy), Clio
**Input:** Klant-aangeleverd materiaal + PROJECT_BRIEF
**Output:** Ingevulde website (echte teksten, foto's, video's)
**Status:** NOG TE ONTWERPEN - grootste gat

Stappen:
1. Tekst schrijven/aanpassen per pagina-sectie
2. Foto's verwerken: ontvangen, optimaliseren (resize/compressie/WebP), plaatsen
3. Video's verwerken: ontvangen, comprimeren, hosten
4. Logo/branding verwerken
5. SEO basis (meta tags, alt-teksts, sitemap.xml)

OPEN VRAGEN:
- Welke agent doet foto/video optimalisatie? (EDIT_REQUEST_SYSTEM.md punt 8, nog TBD)
- Stockfoto's nodig als klant niks aanlevert - welke bron (Unsplash/Pexels API, gratis)?

---

## FASE 4 — DESIGN POLISH (ANIMATIE & INTERACTIE)
**Wie:** Forge / nieuwe sentinel
**Input:** Statische template
**Output:** Levendige, professionele website
**Status:** NOG TE ONTWERPEN

Huidige templates zijn functioneel maar statisch. Toevoegen:
1. Scroll-animaties (fade-in, reveal bij scrollen)
2. Hover-effecten op kaarten/knoppen (deels aanwezig)
3. Micro-interacties (loading states, transities)
4. Hero-animaties (subtiel, geen overdaad)

Aanpak: lichte CSS/JS-library, onderzoek nodig (zie RESEARCH sectie)

---

## FASE 5 — RESPONSIVE QA
**Wie:** Forge / Nero (testen)
**Input:** Volledige website
**Output:** Geverifieerd werkend op mobiel/tablet/desktop
**Status:** NOG TE ONTWERPEN - geen template formeel getest op viewport-breedtes

Stappen:
1. Test op 3 breakpoints: mobiel 375px, tablet 768px, desktop 1280px+
2. Check navigatie/menu op mobiel
3. Check tabellen/grids herschikken correct
4. Check touch-targets minimaal 44px
5. Performance check (Lighthouse score)

KRITIEK GAT: geen van de 13 templates heeft een mobiel hamburger-menu voor de nav. Dit moet toegevoegd worden aan ALLE templates.

---

## FASE 6 — DEPLOY
**Wie:** Forge
**Input:** Voltooide website
**Output:** Live URL
**Status:** Workflow bestaat (Vercel via LuckvsSkills account)

Stappen:
1. Build + deploy naar Vercel
2. Domeinnaam koppelen
3. SSL automatisch via Vercel
4. DNS-instructies aan klant indien eigen domein

---

## FASE 7 — OVERDRACHT
**Wie:** Cortexia naar Nova (rapportage)
**Input:** Live website
**Output:** Klant heeft toegang + documentatie
**Status:** NOG TE ONTWERPEN

Stappen:
1. Overzicht-document per pagina (EDIT_REQUEST_SYSTEM.md punt 3)
2. Inloggegevens indien CMS/admin-panel
3. Uitleg edit-modus + wijzigingsformulier
4. Factuur/betaling afronden

---

## FASE 8 — NAZORG / ONDERHOUD
**Wie:** Cortexia (routing), Forge (uitvoering)
**Input:** Edit requests, bugmeldingen
**Output:** Bijgewerkte live website
**Status:** Concept klaar (EDIT_REQUEST_SYSTEM.md), implementatie nog niet

Stappen:
1. Edit request binnenkomst, element_index lookup, routing
2. Uitvoering + redeploy
3. Periodieke check: uptime, broken links, security updates
4. Optioneel: analytics-rapportage aan klant

---

## RESEARCH AGENDA — Tools/Apps/Services (gratis of goedkoop)

| Categorie | Fase | Voorbeelden om te onderzoeken |
|---|---|---|
| Stockfoto/video API's gratis | 3 | Unsplash API, Pexels API, Pixabay |
| Beeld-optimalisatie tools | 3 | Sharp Node, squoosh, TinyPNG API |
| Animatie-libraries lichtgewicht | 4 | AOS, GSAP free tier, CSS-only |
| Responsive testing tools | 5 | Browserstack gratis tier, Lighthouse CI, Playwright |
| Headless CMS gratis tier | 2/3 | Supabase, Pocketbase, Strapi self-host, Sanity |
| Video hosting gratis/goedkoop | 3 | Cloudflare Stream, Bunny.net, YouTube unlisted embed |
| Form-handling | 2 | Formspree, Web3Forms gratis |
| Analytics privacy-vriendelijk gratis | 8 | Plausible self-host, Umami |

---

## STRATEGIE: CLONE-FIRST (i.p.v. vibe-coding)

Kernprincipe: Wij zijn geen Replit/Lovable. De klant komt naar ons voor een AFGEWERKT product, niet om zelf te tweaken. Daarom:

1. Per template-type zoeken we 1-3 ECHTE, succesvolle websites in dat genre
2. Fea bekijkt deze referenties en geeft feedback: structuur, secties, flow, wat werkt
3. Onze template wordt 1-op-1 aangepast/herbouwd naar die structuur, binnen onze stijl-variabelen
4. Resultaat: templates die al bewezen aanvoelen, geen experimentele eigen ontwerpen

Per template een benchmark-referentie vinden (volgende sessie):

| Template | Benchmark referentie | Status |
|---|---|---|
| bakkerij | bisschopsmolenwebshop.nl - vlaaipakket+cadeau, 2-dagen bestellen, merk-overzicht | Gevonden, nog te verwerken |
| landing | TBD | Open |
| portfolio | TBD | Open |
| blog | TBD | Open |
| bedrijf | TBD | Open |
| ecommerce | TBD | Open |
| booking | TBD | Open |
| marketplace | TBD | Open |
| saas | TBD | Open |
| community | TBD | Open |
| dashboard | TBD | Open |
| directory | TBD | Open |
| api | TBD - minder relevant, geen consumer-benchmark | Open |

Werkwijze volgende sessie:
1. Per template: zoek 1-2 referenties, deel links + korte analyse
2. Fea bekijkt op laptop/tablet/mobiel, geeft feedback
3. Template herbouwen: secties/structuur clonen, content/stijl blijft onze personalisatie
4. KRITIEK punt al geidentificeerd: mobiel hamburger-menu ontbreekt in ALLE 13 templates

---

## VOLGENDE STAPPEN (prioriteit)

1. Mobiel hamburger-menu toevoegen aan alle 13 templates (KRITIEK)
2. Database/CMS-laag ontwerpen (fase 2/3)
3. Foto/video pipeline + agent toewijzen (fase 3)
4. Animatie-laag toevoegen (fase 4)
5. Responsive QA-checklist + uitvoeren op alle templates
6. Live previews deployen (Vercel) voor visuele review

---

## TEMPLATE-CATEGORIEËN: CLONE-FÄHIG vs HYBRIDE-RETAIL

Na onderzoek blijkt 12 van de 13 templates direct 1-op-1 te clonen zijn vanuit bestaande high-end referentiesites. Eén type (bakkerij) is een COMPOSIET van twee winkelconcepten en heeft geen directe clone-referentie.

### CLONE-FÄHIG (12 types)
Elk type krijgt 4 high-end referentiesites. Klant kiest uit 4 kant-en-klare designs.
Status: research loopt (batch 1-2 grotendeels bepaald, batch 3-4 nog te doen).

### HYBRIDE-RETAIL (1 type — was "bakkerij")
Dit type combineert TWEE concepten in één site:
1. KALENDER/AGENDA-component (referentie: Kwik-Fit afsprakensysteem — dienst kiezen, kalender met beschikbare dagen tonen, reserveren)
2. VOORRAAD-RETAIL component (bestaande ecommerce-logica: direct besteld, geen wachttijd)

Dit type bestaat NIET als directe clone en moet zelf ontworpen worden door de twee componenten te combineren.

4 sector-varianten voor dit hybride-type:
1. Bakkerij — taarten/vlaaien op bestelling (kalender) + brood/bakingrediënten (voorraad)
2. Bloemist — boeketten op bezorgdag (kalender) + cadeauartikelen/vazen (voorraad)
3. Slagerij/traiteur — bestelschotels voor feesten (kalender) + vleeswaren kant-en-klaar (voorraad)
4. Wijnhandel/delicatessen — geschenkpakketten op bestelling (kalender) + losse flessen (voorraad)

BELANGRIJKSTE OPEN TAAK: Kwik-Fit kalender-component onderzoeken (hoe toont het beschikbare dagen, hoe werkt de UI) en deze techniek bouwen — ontbreekt nog volledig in huidige template-bakkerij.
