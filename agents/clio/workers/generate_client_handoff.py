#!/usr/bin/env python3
"""
generate_client_handoff.py — Clio worker
Genereert een volledig client handoff package op basis van PROJECT_BRIEF.json
Gebruik: python3 generate_client_handoff.py /pad/naar/PROJECT_BRIEF.json
"""
import os, sys, json
from datetime import datetime

def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    print(f'[{ts}] {msg}')

def load_brief(path):
    with open(path) as f:
        return json.load(f)

def generate_handoff(brief, docs_dir):
    naam = brief['project_naam']
    ptype = brief['type']
    stack = brief.get('stack', 'HTML/CSS/JS')
    features = brief.get('features', [])
    deploy = brief.get('deploy', {})
    live_url = deploy.get('url', 'Nog niet beschikbaar')
    admin_url = deploy.get('admin_url', f'{live_url}/admin')
    domein = brief.get('domein', live_url)
    ts = datetime.now().strftime('%Y-%m-%d')

    features_list = '\n'.join([f'- {f}' for f in features])
    admin_modules = brief.get('admin_modules', ['dashboard', 'instellingen'])
    admin_list = '\n'.join([f'- {m.title()}' for m in admin_modules])

    handoff = f"""# Client Handoff — {naam}
**Datum oplevering:** {ts}
**Opgeleverd door:** ARC AI Agents
**Type:** {ptype.title()}
**Tech stack:** {stack}

---

## Welkom bij uw nieuwe website

Gefeliciteerd met de oplevering van **{naam}**. Dit document bevat alles wat u nodig heeft om uw website te beheren en te gebruiken.

---

## Toegangsgegevens

| Omgeving | URL |
|----------|-----|
| Live website | {live_url} |
| Admin panel | {admin_url} |
| Domein | {domein} |

**Admin inloggegevens (wijzig dit direct):**
- Email: admin@{naam.lower().replace(' ','')}.nl
- Wachtwoord: admin123 (wijzig dit direct na eerste login!)

---

## Uw website

### Wat uw website kan
{features_list if features_list else '- Zie live website voor alle functies'}

### Admin panel modules
{admin_list}

---

## Admin panel gebruiken

### Inloggen
1. Ga naar {admin_url}
2. Vul uw email en wachtwoord in
3. Klik op "Inloggen"

### Dashboard
Het dashboard toont een overzicht van:
- Recente activiteit
- Statistieken en cijfers
- Openstaande acties

### Wachtwoord wijzigen
1. Klik rechtsboven op uw naam
2. Kies "Profiel"
3. Vul uw nieuwe wachtwoord in
4. Klik op "Opslaan"

---

## Veelgestelde vragen

**Hoe voeg ik nieuwe content toe?**
Log in op het admin panel en ga naar het relevante onderdeel.

**Wat als de website niet bereikbaar is?**
Neem contact op met ARC AI Agents via Telegram of email.

**Hoe maak ik een backup?**
Zie het SOP document voor backup instructies.

---

## Contact en support

Bij vragen of problemen:
- **ARC AI Agents** — uw website partner
- Telegram: beschikbaar voor urgente zaken
- Reactietijd: binnen 24 uur op werkdagen

---

*Opgeleverd door ARC AI Agents — Gebouwd met liefde en AI*
*Versie 1.0 — {ts}*
"""

    handoff_path = f'{docs_dir}/HANDOFF.md'
    with open(handoff_path, 'w') as f:
        f.write(handoff)
    log(f'✅ Client handoff geschreven: {handoff_path}')
    return handoff_path

def generate_deployment_guide(brief, docs_dir):
    naam = brief['project_naam']
    stack = brief.get('stack', 'HTML/CSS/JS')
    deploy = brief.get('deploy', {})
    github_url = deploy.get('github', 'https://github.com/LuckvsSkills/' + naam.lower().replace(' ','-'))

    guide = f"""# Deployment Guide — {naam}

## Tech stack
{stack}

## GitHub repository
{github_url}

## Vercel deployment

### Eerste keer deployen
```bash
npm install -g vercel
vercel --token $VERCEL_TOKEN --yes --name {naam.lower().replace(' ','-')}
```

### Updates deployen
```bash
git add -A
git commit -m "Update: beschrijving van wijziging"
git push origin main
```
Vercel deployt automatisch na elke push naar main.

## Environment variables
Kopieer `.env.example` naar `.env` en vul in:
STRIPE_SECRET_KEY=sk_live_...

STRIPE_PUBLISHABLE_KEY=pk_live_...

DATABASE_URL=postgresql://...

SECRET_KEY=willekeurige-lange-string

## Lokaal draaien
```bash
# Backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8001

# Frontend
npm install
npm run dev
```

## Backup
Database backup dagelijks automatisch via Vercel.
Handmatige backup: exporteer via admin panel → Instellingen → Backup.
"""

    guide_path = f'{docs_dir}/DEPLOYMENT.md'
    with open(guide_path, 'w') as f:
        f.write(guide)
    log(f'✅ Deployment guide geschreven: {guide_path}')
    return guide_path

def update_brief(brief_path, brief, docs_dir):
    brief['docs'] = {
        'dir': docs_dir,
        'handoff': f'{docs_dir}/HANDOFF.md',
        'deployment': f'{docs_dir}/DEPLOYMENT.md',
        'generated_at': datetime.now().isoformat()
    }
    brief['sentinels']['clio'] = 'HANDOFF_DONE'
    with open(brief_path, 'w') as f:
        json.dump(brief, f, indent=2, ensure_ascii=False)

def main():
    if len(sys.argv) < 2:
        print('Gebruik: python3 generate_client_handoff.py /pad/naar/PROJECT_BRIEF.json')
        sys.exit(1)

    brief_path = sys.argv[1]
    brief = load_brief(brief_path)
    project_dir = os.path.dirname(brief_path)
    docs_dir = f'{project_dir}/docs'
    os.makedirs(docs_dir, exist_ok=True)

    log(f'📝 Client handoff: {brief["project_naam"]}')
    handoff_path = generate_handoff(brief, docs_dir)
    deployment_path = generate_deployment_guide(brief, docs_dir)
    update_brief(brief_path, brief, docs_dir)

    print('\n' + '='*50)
    print('✅ CLIO HANDOFF KLAAR')
    print(f'   Handoff: {handoff_path}')
    print(f'   Deployment: {deployment_path}')
    print(f'   Volgende: generate_sop.py')
    print('='*50)

if __name__ == '__main__':
    main()
