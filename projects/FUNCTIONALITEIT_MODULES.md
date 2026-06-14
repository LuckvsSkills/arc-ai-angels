# Functionaliteit Modules — ARC AI Agents Website Fabriek

Aanvullende modules die per website-type aangeboden kunnen worden tijdens de Nova intake wizard. Deze modules zijn optioneel en verhogen de prijs (zie WEBSITE_FABRIEK_COMPLEET.md voor prijsmodel).

---

## 1. Leverplanner / Afleverkalender
**Wat:** Klant kiest een leverdatum bij checkout, met minimale levertijd en blokkeerbare dagen.

**Varianten:**
- Vaste levertijd per product (bv. taarten = 7 dagen)
- Eén leverdatum voor hele bestelling (langste levertijd geldt)
- Per product eigen leverdatum
- Admin kan dagen/weekdagen blokkeren (bv. geen levering op zondag, feestdagen)
- Tijdvak-selectie (ochtend/middag/avond)

**Toepasbaar op:** ecommerce, bakkerij, booking, marketplace

---

## 2. Voorraadbeheer
**Wat:** Producten hebben een voorraadaantal; bij 0 wordt "niet beschikbaar" getoond.

**Varianten:**
- Simpele teller (aantal in voorraad)
- Lage-voorraad waarschuwing ("nog maar 3 op voorraad")
- Automatische "uitverkocht" badge
- Backorder mogelijkheid (bestellen ondanks 0 voorraad, met wachttijd)

**Toepasbaar op:** ecommerce, bakkerij, marketplace, directory

---

## 3. Afspraken/Booking Systeem
**Wat:** Klant boekt een tijdslot voor een dienst (kapper, consult, repair).

**Varianten:**
- Vaste tijdslots (elk uur, elke 30 min)
- Meerdere medewerkers/resources met eigen agenda
- Annulering/verplaatsing door klant
- Herinnering via e-mail/SMS

**Toepasbaar op:** booking, dienstverlening (bedrijf), gezondheid

---

## 4. Abonnementen/Herhaalbestellingen
**Wat:** Klant abonneert op periodieke levering (bv. wekelijks brood).

**Varianten:**
- Vaste frequentie (wekelijks/maandelijks)
- Pauzeren/wijzigen door klant zelf
- Automatische herhaalbetaling

**Toepasbaar op:** ecommerce, bakkerij, saas

---

## 5. Multi-categorie Winkelwagen
**Wat:** Verschillende productsoorten in één winkelwagen met eigen regels (zoals bakkerij vers vs. materiaal).

**Varianten:**
- Gemengde levertijden — langste geldt
- Gesplitste levering (apart afrekenen per categorie)
- Categorie-specifieke kortingen

**Toepasbaar op:** ecommerce, bakkerij, marketplace

---

## 6. Personalisatie/Aanpassingen
**Wat:** Klant kan een product personaliseren (bv. tekst op taart, naam op product).

**Varianten:**
- Vrije tekstinvoer per product
- Voorgedefinieerde opties (smaak, kleur, maat)
- Extra kosten per personalisatie

**Toepasbaar op:** ecommerce, bakkerij, marketplace

---

## 7. Loyaliteit/Punten Systeem
**Wat:** Klanten verdienen punten bij aankopen, inwisselbaar voor korting.

**Toepasbaar op:** ecommerce, bakkerij, community

---

## 8. Reviews & Beoordelingen
**Wat:** Klanten kunnen producten/diensten beoordelen met sterren + tekst.

**Toepasbaar op:** ecommerce, bakkerij, marketplace, directory, booking

---

## 9. Locatie/Bezorggebied Check
**Wat:** Klant vult postcode in, systeem checkt of bezorging mogelijk is in dat gebied.

**Varianten:**
- Postcode-range whitelist
- Afstand-gebaseerd (radius vanaf winkel)
- Verschillende levertijden per gebied

**Toepasbaar op:** ecommerce, bakkerij, booking

---

## 10. Multi-vestiging
**Wat:** Bedrijf met meerdere locaties; klant kiest vestiging voor levering/afhalen.

**Toepasbaar op:** ecommerce, bakkerij, booking, directory

---

## 11. Cadeaubonnen/Vouchers
**Wat:** Kortingscodes of cadeaubonnen inwisselbaar bij checkout.

**Toepasbaar op:** ecommerce, bakkerij, booking, saas

---

## 12. Afhalen vs. Bezorgen
**Wat:** Klant kiest tussen zelf afhalen (geen levertijd-restrictie) of laten bezorgen (met planner).

**Toepasbaar op:** ecommerce, bakkerij, booking

---

## Matrix: Module × Template Type

| Module | landing | portfolio | blog | bedrijf | ecommerce | bakkerij | booking | marketplace | saas | community | dashboard | directory |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Leverplanner | | | | | ✓ | ✓ | ✓ | ✓ | | | | |
| Voorraadbeheer | | | | | ✓ | ✓ | | ✓ | | | | ✓ |
| Booking systeem | | | | ✓ | | | ✓ | | | | | |
| Abonnementen | | | | | ✓ | ✓ | | | ✓ | | | |
| Multi-categorie cart | | | | | ✓ | ✓ | | ✓ | | | | |
| Personalisatie | | | | | ✓ | ✓ | | ✓ | | | | |
| Loyaliteit | | | | | ✓ | ✓ | | | | ✓ | | |
| Reviews | | | | | ✓ | ✓ | ✓ | ✓ | | | | ✓ |
| Bezorggebied check | | | | | ✓ | ✓ | ✓ | | | | | |
| Multi-vestiging | | | | ✓ | ✓ | ✓ | ✓ | | | | | ✓ |
| Vouchers | | | | | ✓ | ✓ | ✓ | | ✓ | | | |
| Afhalen/Bezorgen | | | | | ✓ | ✓ | ✓ | | | | | |

---

## Gebruik in Nova Intake Wizard

Na stap 7 (functies kiezen) toont Nova relevante modules op basis van het gekozen type, met korte uitleg + prijsindicatie per module. Klant kan 0 of meerdere modules selecteren.
