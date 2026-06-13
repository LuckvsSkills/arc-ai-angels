#!/usr/bin/env python3
"""
generate_sop.py — Clio worker
Genereert Standard Operating Procedures voor website beheer
Gebruik: python3 generate_sop.py /pad/naar/PROJECT_BRIEF.json
"""
import os, sys, json
from datetime import datetime

def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    print(f'[{ts}] {msg}')

def load_brief(path):
    with open(path) as f:
        return json.load(f)

def generate_sop(brief, docs_dir):
    naam = brief['project_naam']
    ptype = brief['type']
    deploy = brief.get('deploy', {})
    live_url = deploy.get('url', 'https://uw-website.vercel.app')
    admin_url = f'{live_url}/admin'
    ts = datetime.now().strftime('%Y-%m-%d')

    type_sops = {
        'ecommerce': """
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
""",
        'saas': """
## SOP-003: Abonnement beheer

### Nieuw abonnement activeren
1. Ga naar admin panel → Subscriptions
2. Zoek gebruiker op email
3. Controleer Stripe status
4. Activeer indien nodig handmatig

### Abonnement opzeggen
1. Admin panel → Subscriptions
2. Open abonnement
3. Klik "Opzeggen"
4. Kies direct of einde periode
""",
        'booking': """
## SOP-003: Reservering beheer

### Nieuwe reservering bevestigen
1. Admin panel → Reserveringen
2. Open nieuwe reservering (status: "pending")
3. Controleer beschikbaarheid
4. Zet status op "confirmed"
5. Klant ontvangt bevestigingsmail

### Reservering annuleren
1. Open reservering
2. Klik "Annuleren"
3. Voer reden in
4. Verwerk eventuele terugbetaling
""",
    }

    type_specific = type_sops.get(ptype, """
## SOP-003: Content beheer

### Content bijwerken
1. Log in op admin panel
2. Ga naar het relevante onderdeel
3. Klik "Bewerken"
4. Maak wijzigingen
5. Klik "Opslaan"
6. Controleer op de live website
""")

    sop = f"""# Standard Operating Procedures — {naam}
**Versie:** 1.0
**Datum:** {ts}
**Opgesteld door:** ARC AI Agents — Clio

---

## Overzicht

Dit document beschrijft de standaard procedures voor het beheren van **{naam}**.

| SOP | Omschrijving | Frequentie |
|-----|-------------|-----------|
| SOP-001 | Dagelijks beheer | Dagelijks |
| SOP-002 | Wekelijks onderhoud | Wekelijks |
| SOP-003 | Type-specifieke procedures | Op aanvraag |
| SOP-004 | Noodprocedures | Bij incident |

---

## SOP-001: Dagelijks beheer

### Ochtend check (5 minuten)
1. Open {live_url} — is de website bereikbaar?
2. Open {admin_url} — werkt het admin panel?
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
{type_specific}

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
*{ts}*
"""

    sop_path = f'{docs_dir}/SOP.md'
    with open(sop_path, 'w') as f:
        f.write(sop)
    log(f'✅ SOP geschreven: {sop_path}')
    return sop_path

def update_brief(brief_path, brief, sop_path):
    if 'docs' in brief:
        brief['docs']['sop'] = sop_path
    brief['sentinels']['clio'] = 'DONE'
    brief['status'] = 'OPGELEVERD'
    brief['opgeleverd_op'] = datetime.now().isoformat()
    with open(brief_path, 'w') as f:
        json.dump(brief, f, indent=2, ensure_ascii=False)

def main():
    if len(sys.argv) < 2:
        print('Gebruik: python3 generate_sop.py /pad/naar/PROJECT_BRIEF.json')
        sys.exit(1)

    brief_path = sys.argv[1]
    brief = load_brief(brief_path)
    project_dir = os.path.dirname(brief_path)
    docs_dir = f'{project_dir}/docs'
    os.makedirs(docs_dir, exist_ok=True)

    log(f'📋 SOP genereren: {brief["project_naam"]} ({brief["type"]})')
    sop_path = generate_sop(brief, docs_dir)
    update_brief(brief_path, brief, sop_path)

    print('\n' + '='*50)
    print('✅ CLIO SOP KLAAR')
    print(f'   SOP: {sop_path}')
    print(f'   Project status: OPGELEVERD')
    print('='*50)

if __name__ == '__main__':
    main()
