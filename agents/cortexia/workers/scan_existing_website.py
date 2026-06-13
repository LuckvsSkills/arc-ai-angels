#!/usr/bin/env python3
"""
scan_existing_website.py — Cortexia worker
Scrapet en analyseert een bestaande website, genereert AI-readiness adviesrapport.
Gebruik: python3 scan_existing_website.py /pad/naar/intake.json
"""
import os, sys, json, subprocess
from datetime import datetime

BUILDS_DIR = '/home/prime/arc_ai_angels/projects/website_builds'

def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    print(f'[{ts}] {msg}')

def load_intake(path):
    with open(path) as f:
        return json.load(f)

def create_scan_dir(intake):
    naam = intake['naam'].lower().replace(' ', '-')
    scan_dir = f'{BUILDS_DIR}/{naam}-scan'
    os.makedirs(scan_dir, exist_ok=True)
    return scan_dir

def detect_tech_stack(url):
    """Detecteer tech stack op basis van URL en response headers"""
    indicators = {
        'WordPress':  ['wp-content', 'wp-includes', 'xmlrpc.php'],
        'Shopify':    ['shopify', 'myshopify.com', 'cdn.shopify'],
        'Wix':        ['wix.com', 'wixstatic.com'],
        'Squarespace':['squarespace.com', 'sqspcdn.com'],
        'React':      ['react', '_next', '__NEXT_DATA__'],
        'Vue':        ['vue', 'nuxt', '__nuxt'],
        'Angular':    ['angular', 'ng-version'],
        'Next.js':    ['_next/static', '__NEXT_DATA__'],
        'FastAPI':    ['fastapi', 'openapi.json'],
        'Django':     ['csrftoken', 'django'],
        'Laravel':    ['laravel_session', 'laravel'],
    }
    detected = []
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '--max-time', '10', '-I', url],
            capture_output=True, text=True
        )
        headers = result.stdout.lower()
        result2 = subprocess.run(
            ['curl', '-s', '-L', '--max-time', '15', url],
            capture_output=True, text=True
        )
        content = result2.stdout.lower()
        combined = headers + content
        for tech, signs in indicators.items():
            if any(sign.lower() in combined for sign in signs):
                detected.append(tech)
    except Exception as e:
        log(f'⚠️ Tech detectie fout: {e}')
    return detected if detected else ['Onbekend']

def calculate_ai_readiness(intake, tech_stack):
    """Bereken AI-readiness score 0-100"""
    score = 0
    findings = []

    upgrade_wensen = intake.get('upgrade_wensen', [])
    wensen_lower = [w.lower() for w in upgrade_wensen]

    # Heeft chatbot
    if any('chat' in w or 'bot' in w for w in wensen_lower):
        findings.append({'punt': 'Chatbot gewenst', 'score': 0, 'max': 20, 'status': 'MISSING'})
    else:
        score += 5
        findings.append({'punt': 'Chatbot', 'score': 5, 'max': 20, 'status': 'BASIC'})

    # API aanwezig
    if any(t in tech_stack for t in ['FastAPI', 'Django', 'Laravel']):
        score += 20
        findings.append({'punt': 'API aanwezig', 'score': 20, 'max': 20, 'status': 'OK'})
    else:
        findings.append({'punt': 'API', 'score': 0, 'max': 20, 'status': 'MISSING'})

    # Modern framework
    if any(t in tech_stack for t in ['React', 'Vue', 'Angular', 'Next.js']):
        score += 15
        findings.append({'punt': 'Modern framework', 'score': 15, 'max': 15, 'status': 'OK'})
    else:
        findings.append({'punt': 'Modern framework', 'score': 0, 'max': 15, 'status': 'VEROUDERD'})

    # Personalisatie gewenst
    if any('personali' in w or 'ai' in w for w in wensen_lower):
        findings.append({'punt': 'AI personalisatie gewenst', 'score': 0, 'max': 20, 'status': 'MISSING'})
    else:
        score += 5
        findings.append({'punt': 'Personalisatie', 'score': 5, 'max': 20, 'status': 'BASIC'})

    # Automatisering
    if any('automat' in w or 'agent' in w or 'order' in w for w in wensen_lower):
        findings.append({'punt': 'Automatisering gewenst', 'score': 0, 'max': 25, 'status': 'MISSING'})
    else:
        score += 5
        findings.append({'punt': 'Automatisering', 'score': 5, 'max': 25, 'status': 'BASIC'})

    return score, findings

def generate_recommendations(score, findings, tech_stack, upgrade_wensen):
    """Genereer concrete aanbevelingen op basis van analyse"""
    recs = []

    missing = [f for f in findings if f['status'] == 'MISSING']
    verouderd = [f for f in findings if f['status'] == 'VEROUDERD']

    if verouderd:
        recs.append({
            'prioriteit': 1,
            'titel': 'Tech stack moderniseren',
            'beschrijving': f'Huidige stack ({", ".join(tech_stack)}) upgraden naar React + FastAPI voor betere AI-integratie.',
            'impact': 'HOOG',
            'type': 'upgrade',
            'kostenraming': '€3.000 – €8.000',
            'doorlooptijd': '2-4 weken'
        })

    if any(f['punt'] == 'API' for f in missing):
        recs.append({
            'prioriteit': 2,
            'titel': 'REST API toevoegen',
            'beschrijving': 'FastAPI backend bouwen voor data-uitwisseling met AI agents en externe services.',
            'impact': 'HOOG',
            'type': 'uitbreiding',
            'kostenraming': '€1.500 – €3.000',
            'doorlooptijd': '1-2 weken'
        })

    if any('chat' in w.lower() or 'bot' in w.lower() for w in upgrade_wensen):
        recs.append({
            'prioriteit': 3,
            'titel': 'AI Chatbot integreren',
            'beschrijving': 'Klantenservice chatbot toevoegen via OpenClaw agent. Beantwoordt vragen 24/7 autonoom.',
            'impact': 'HOOG',
            'type': 'ai-agent',
            'kostenraming': '€2.000 – €4.000 + €300/mnd',
            'doorlooptijd': '1-2 weken'
        })

    if any('order' in w.lower() or 'bestel' in w.lower() for w in upgrade_wensen):
        recs.append({
            'prioriteit': 4,
            'titel': 'Order automatisering via AI agent',
            'beschrijving': 'AI agent die bestellingen verwerkt, leveranciers informeert en klanten updates stuurt.',
            'impact': 'ZEER HOOG',
            'type': 'ai-agent',
            'kostenraming': '€3.000 – €6.000 + €500/mnd',
            'doorlooptijd': '2-3 weken'
        })

    if score < 40:
        recs.append({
            'prioriteit': 5,
            'titel': 'Volledige AI-ready rebuild',
            'beschrijving': 'Website volledig herbouwen met moderne stack + admin panel + AI agents. Maximale toekomstbestendigheid.',
            'impact': 'MAXIMAAL',
            'type': 'rebuild',
            'kostenraming': '€8.000 – €15.000 + €500/mnd',
            'doorlooptijd': '4-6 weken'
        })

    return recs[:4]

def generate_rapport(intake, scan_dir, tech_stack, score, findings, recommendations):
    """Genereer professioneel adviesrapport"""
    naam = intake['naam']
    url = intake.get('url', 'onbekend')
    ts = datetime.now().strftime('%Y-%m-%d %H:%M')

    score_label = 'KRITIEK' if score < 25 else 'LAAG' if score < 50 else 'MATIG' if score < 75 else 'GOED'

    findings_md = '\n'.join([
        f"| {f['punt']} | {f['score']}/{f['max']} | {'✅' if f['status']=='OK' else '🟡' if f['status']=='BASIC' else '❌'} {f['status']} |"
        for f in findings
    ])

    recs_md = ''
    for r in recommendations:
        recs_md += f"""
### Aanbeveling {r['prioriteit']} — {r['titel']}
**Impact:** {r['impact']} | **Type:** {r['type']} | **Kosten:** {r['kostenraming']} | **Doorlooptijd:** {r['doorlooptijd']}

{r['beschrijving']}
"""

    rapport = f"""# Website Adviesrapport — {naam}
**Datum:** {ts}
**URL:** {url}
**Analyse door:** Cortexia / ARC AI Agents

---

## Samenvatting

| Onderdeel | Score |
|-----------|-------|
| AI-readiness | {score}/100 ({score_label}) |
| Tech stack | {', '.join(tech_stack)} |
| Aanbevelingen | {len(recommendations)} concrete acties |

---

## AI-Readiness Analyse

| Punt | Score | Status |
|------|-------|--------|
{findings_md}

**Totaal: {score}/100 — {score_label}**

{'⚠️ De website heeft urgente modernisering nodig om AI-klaar te zijn.' if score < 50 else '✅ De website heeft een goede basis maar kan verder geoptimaliseerd worden voor AI-integratie.'}

---

## Gedetecteerde Tech Stack

{', '.join(tech_stack)}

---

## Aanbevelingen
{recs_md}

---

## Volgende Stappen

1. **Bespreek** de aanbevelingen met uw team
2. **Prioriteer** op basis van budget en impact
3. **Neem contact op** met ARC AI Agents voor uitvoering
4. **Bouwtijd:** Wij kunnen starten binnen 5 werkdagen

---

## Kostenoverzicht

| Aanbeveling | Investering | Maandelijks |
|-------------|-------------|-------------|
{''.join([f"| {r['titel']} | {r['kostenraming'].split('+')[0].strip()} | {r['kostenraming'].split('+')[1].strip() if '+' in r['kostenraming'] else '-'} |" + chr(10) for r in recommendations])}

---

*Rapport gegenereerd door ARC AI Agents — Cortexia*
*Versie 1.0 — {ts}*
"""

    rapport_path = f'{scan_dir}/ADVIES_RAPPORT.md'
    with open(rapport_path, 'w') as f:
        f.write(rapport)

    scan_result = {
        'naam': naam,
        'url': url,
        'tech_stack': tech_stack,
        'ai_readiness_score': score,
        'ai_readiness_label': score_label,
        'findings': findings,
        'recommendations': recommendations,
        'rapport_path': rapport_path,
        'datum': ts
    }
    with open(f'{scan_dir}/SCAN_RESULT.json', 'w') as f:
        json.dump(scan_result, f, indent=2, ensure_ascii=False)

    return rapport_path

def main():
    if len(sys.argv) < 2:
        print('Gebruik: python3 scan_existing_website.py /pad/naar/intake.json')
        print()
        print('Intake JSON formaat:')
        print(json.dumps({
            'intake_type': 'scan',
            'naam': 'KlantWebsite',
            'url': 'https://www.klantwebsite.nl',
            'beschrijving': 'Webshop voor handgemaakte producten',
            'upgrade_wensen': ['AI chatbot', 'order automatisering', 'betere SEO']
        }, indent=2, ensure_ascii=False))
        sys.exit(1)

    intake_path = sys.argv[1]
    if not os.path.exists(intake_path):
        print(f'❌ Intake niet gevonden: {intake_path}')
        sys.exit(1)

    intake = load_intake(intake_path)
    url = intake.get('url', '')
    if not url:
        print('❌ URL verplicht in intake voor scan')
        sys.exit(1)

    log(f'🔍 Website scan gestart: {intake["naam"]}')
    log(f'   URL: {url}')

    scan_dir = create_scan_dir(intake)

    log('🔎 Tech stack detecteren...')
    tech_stack = detect_tech_stack(url)
    log(f'   Gevonden: {", ".join(tech_stack)}')

    log('📊 AI-readiness berekenen...')
    score, findings = calculate_ai_readiness(intake, tech_stack)
    log(f'   Score: {score}/100')

    log('💡 Aanbevelingen genereren...')
    recommendations = generate_recommendations(score, findings, tech_stack, intake.get('upgrade_wensen', []))

    log('📝 Adviesrapport schrijven...')
    rapport_path = generate_rapport(intake, scan_dir, tech_stack, score, findings, recommendations)

    print('\n' + '='*60)
    print('✅ WEBSITE SCAN VOLTOOID')
    print('='*60)
    print(f'  Website:    {intake["naam"]}')
    print(f'  URL:        {url}')
    print(f'  Tech stack: {", ".join(tech_stack)}')
    print(f'  AI-score:   {score}/100')
    print(f'  Rapport:    {rapport_path}')
    print('='*60)

if __name__ == '__main__':
    main()
