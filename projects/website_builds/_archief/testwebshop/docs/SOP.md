# Standard Operating Procedures — TestWebshop
**Versie:** 1.0
**Datum:** 2026-06-13
**Opgesteld door:** ARC AI Agents — Clio

---

## Overzicht

Dit document beschrijft de standaard procedures voor het beheren van **TestWebshop**.

| SOP | Omschrijving | Frequentie |
|-----|-------------|-----------|
| SOP-001 | Dagelijks beheer | Dagelijks |
| SOP-002 | Wekelijks onderhoud | Wekelijks |
| SOP-003 | Type-specifieke procedures | Op aanvraag |
| SOP-004 | Noodprocedures | Bij incident |

---

## SOP-001: Dagelijks beheer

### Ochtend check (5 minuten)
1. Open https://uw-website.vercel.app — is de website bereikbaar?
2. Open https://uw-website.vercel.app/admin — werkt het admin panel?
3. Check nieuwe berichten of orders
4. Verwerk urgente zaken

### Einde van de dag
1. Verwerk openstaande items
2. Check of er fouten zijn gemeld

---

## SOP-002: Wekelijks onderhoud

### Iedere maandag
1. Check website statistieken in admin panel
2. Verwerk openstaande zaken van vorige week
3. Plan content of updates voor deze week
4. Backup controleren (automatisch via Vercel)

### Maandelijks
1. Wachtwoorden controleren en wijzigen indien nodig
2. Gebruikersaccounts reviewen
3. Ongebruikte accounts verwijderen
4. Performance check — laadtijd website meten

---

## SOP-003: Order beheer

### Nieuwe order verwerken
1. Log in op admin panel → Orders
2. Open nieuwe order (status: "pending")
3. Controleer betaling in Stripe dashboard
4. Zet status op "processing"
5. Verwerk de bestelling
6. Zet status op "shipped" met trackingnummer
7. Klant ontvangt automatisch email update

### Terugbetaling verwerken
1. Open order in admin panel
2. Klik "Terugbetaling"
3. Voer bedrag in
4. Bevestig — Stripe verwerkt automatisch

### Voorraad bijwerken
1. Admin panel → Producten
2. Open product
3. Wijzig "Voorraad" veld
4. Sla op


---

## SOP-004: Noodprocedures

### Website is niet bereikbaar
1. Wacht 5 minuten — kan tijdelijk zijn
2. Controleer Vercel status: https://www.vercel-status.com
3. Controleer uw domein DNS instellingen
4. Neem contact op met ARC AI Agents als probleem aanhoudt

### Admin panel werkt niet
1. Wis browser cache (Ctrl+Shift+Delete)
2. Probeer incognito modus
3. Probeer andere browser
4. Neem contact op met ARC AI Agents

### Gehackt of beveiligingsincident
1. Verander direct alle wachtwoorden
2. Neem contact op met ARC AI Agents
3. Documenteer wat er is gebeurd (tijd, wat u zag)
4. Zet website offline indien nodig via Vercel dashboard

### Data verlies
1. Neem direct contact op met ARC AI Agents
2. Vercel bewaart automatische backups van de laatste 30 dagen
3. Herstel is mogelijk tot 30 dagen terug

---

## Contactgegevens

| Contact | Beschikbaar |
|---------|-------------|
| ARC AI Agents — Telegram | Urgente zaken, direct |
| ARC AI Agents — Email | Normale zaken, 24u |

---

*Opgesteld door Clio — ARC AI Agents Documentation*
*2026-06-13*
