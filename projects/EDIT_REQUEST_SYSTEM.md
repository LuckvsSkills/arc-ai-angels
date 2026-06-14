# Edit Request System — Klant Wijzigingsverzoeken

Systeem waarmee klanten na levering van hun website zelf wijzigingen kunnen aanvragen, zonder dat ze technische kennis nodig hebben.

---

## 1. Element-ID Systeem

Elk belangrijk HTML-element op elke pagina krijgt een unieke, leesbare `data-edit-id`.

**Naamconventie:** `[pagina]-[sectie]-[element]-[volgnummer]`

Voorbeelden:
- `home-hero-titel-01`
- `home-hero-knop-01`
- `producten-card-afbeelding-03`
- `contact-form-submit-01`
- `footer-logo-01`

Forge voegt deze ID's automatisch toe tijdens `personalize_site.py` — elk element dat aanpasbaar is (tekst, afbeelding, knop, kleur-sectie) krijgt een ID.

---

## 2. Bewerk-modus in de live site

Een knop "Bewerk-modus" (alleen zichtbaar voor de klant, via wachtwoord of verborgen URL-parameter `?edit=true`) toont:
- Een dunne gekleurde rand om elk element met `data-edit-id`
- Bij hover: een klein label met het ID (bv. `home-hero-titel-01`)
- Klikken op het element kopieert het ID naar het klembord

Implementatie: kleine JS-module (`edit-mode.js`) die wordt meegeleverd in elke template, alleen actief bij `?edit=true`.

---

## 3. Overzicht-document per pagina

Bij levering krijgt de klant een PDF/markdown document per pagina:
- Screenshot van de pagina
- Genummerde markers die corresponderen met de element-ID's
- Korte beschrijving per element ("Titel hoofdsectie", "Foto productcard 3")

Gegenereerd door: nieuwe Forge-worker `generate_edit_overview.py` (te bouwen)

---

## 4. Wijzigingsformulier

Eén algemeen formulier, gehost op een vaste URL per klant (bv. `[domein]/wijzigen` of via MCC-link):

**Velden:**
- Klantnaam / projectnaam
- Pagina (dropdown, automatisch gevuld op basis van site-structuur)
- Element-ID (tekstveld — klant plakt ID uit bewerk-modus of overzicht-document)
- Gewenste wijziging (vrije tekst: "verander deze tekst naar...", "vervang deze foto", "verwijder dit blok")
- Foto-upload (optioneel, voor foto-vervangingen)
- Contactgegevens voor terugkoppeling

**Output:** JSON-bestand in `projects/website_builds/[klant]/edit_requests/[datum]-[id].json`:
```json
{
  "klant": "Bloemenshop Amsterdam",
  "pagina": "home",
  "element_id": "home-hero-titel-01",
  "wijziging": "Verander 'Welkom bij onze winkel' naar 'Verse bloemen, elke dag vers bezorgd'",
  "foto": null,
  "status": "open",
  "ingediend_op": "2026-06-14T10:00:00Z"
}
```

---

## 5. Verwerking van wijzigingsverzoeken

**Routing:**
1. Edit request komt binnen → Cortexia ziet nieuwe taak in `edit_requests/`
2. Cortexia herleidt `element_id` naar bestand + regelnummer via een **element-index** (gegenereerd tijdens build, `element_index.json`)
3. Cortexia routeert naar de juiste sentinel:
   - Tekst/kleur wijziging → Forge
   - Foto vervangen → eerst security-check (Nero) → dan optimalisatie (nader te bepalen agent) → Forge plaatst nieuwe afbeelding
   - Layout/element verwijderen → Forge
4. Forge past aan, commit + push naar GitHub, deploy update
5. Cortexia rapporteert "klaar" terug naar klant (via Nova/Telegram of e-mail)

---

## 6. Element-Index (technisch fundament)

Tijdens `personalize_site.py` wordt automatisch `element_index.json` gegenereerd per project:
```json
{
  "home-hero-titel-01": {
    "bestand": "frontend/index.html",
    "regel": 14,
    "type": "tekst",
    "huidige_waarde": "Welkom bij Bloemenshop Amsterdam"
  },
  "producten-card-afbeelding-03": {
    "bestand": "frontend/index.html",
    "regel": 87,
    "type": "afbeelding",
    "huidige_waarde": "images/product-3.jpg"
  }
}
```

Dit bestand is de "vertaaltabel" tussen wat de klant invult en wat Forge moet aanpassen.

---

## 7. Multi-pagina sites

Voor sites met meerdere pagina's (bv. Home, Over ons, Producten, Contact):
- Elke pagina heeft eigen element-index, samengevoegd in `element_index.json` met pagina als top-level key
- Overzicht-document wordt per pagina gegenereerd
- Wijzigingsformulier dropdown toont alle pagina's van het specifieke project (uit `PROJECT_BRIEF.json`)

---

## 8. Foto-uploads (nog te bepalen agent)

- Klant kan foto's uploaden via het wijzigingsformulier
- **Stap 1 — Security check (Nero):** malware-scan, content-check (geen ongepaste afbeeldingen)
- **Stap 2 — Optimalisatie (TBD agent):** resize naar juiste afmetingen per element-type, compressie, WebP-conversie
- **Stap 3 — Plaatsing (Forge):** vervangt de afbeelding op de juiste plek, update `element_index.json`

*Welke agent de optimalisatie-stap doet wordt in een latere sessie bepaald — mogelijk een nieuwe Helix sentinel of een Matrix/Quantix domein-agent met beeldbewerkings-skills.*

---

## STATUS: Concept vastgelegd — nog te bouwen

- [ ] `edit-mode.js` — bewerk-modus JS module voor templates
- [ ] `generate_edit_overview.py` — Forge worker voor overzicht-documenten
- [ ] `element_index.json` generatie tijdens personalize_site.py
- [ ] Wijzigingsformulier (waar gehost? MCC tab of losse pagina per klant?)
- [ ] Cortexia routing-logica voor edit_requests/
- [ ] Foto-optimalisatie agent/worker bepalen
