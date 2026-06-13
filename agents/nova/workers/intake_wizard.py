#!/usr/bin/env python3
"""
intake_wizard.py — Nova worker
Gebruik: python3 intake_wizard.py /pad/naar/antwoorden.json
"""
import os, sys, json
from datetime import datetime

BUILDS_DIR = '/home/prime/arc_ai_angels/projects/website_builds'

DOEL_TYPE_MAP = {'A':'landing','B':'ecommerce','C':'booking','D':'saas','E':'blog','F':'directory','G':'marketplace','H':'dashboard','I':'community','J':'landing'}
STIJL_KLEUR_MAP = {'A':'wit en grijs','B':'goud en zwart','C':'blauw en wit','D':'blauw en grijs','E':'groen en wit','F':'goud en zwart'}
FUNCTIE_MAP = {'A':'contactformulier','B':'online betaling','C':'gebruikersaccounts','D':'zoekfunctie','E':'nieuwsbrief','F':'reviews','G':'agenda','H':'productcatalogus','I':'chat support','J':'standaard functies'}
PRIJZEN = {
    'landing':{'tier':1,'min':500,'max':2000,'tijd':'1-2 uur'},
    'portfolio':{'tier':1,'min':500,'max':2000,'tijd':'1-2 uur'},
    'blog':{'tier':1,'min':800,'max':2500,'tijd':'1-2 uur'},
    'saas':{'tier':2,'min':3000,'max':8000,'tijd':'4-8 uur'},
    'ecommerce':{'tier':2,'min':3000,'max':8000,'tijd':'4-8 uur'},
    'directory':{'tier':2,'min':3500,'max':8000,'tijd':'4-8 uur'},
    'marketplace':{'tier':2,'min':4000,'max':10000,'tijd':'6-10 uur'},
    'dashboard':{'tier':2,'min':3000,'max':7000,'tijd':'4-6 uur'},
    'community':{'tier':2,'min':3500,'max':8000,'tijd':'6-10 uur'},
    'booking':{'tier':2,'min':2500,'max':6000,'tijd':'4-6 uur'},
}

def main():
    if len(sys.argv) < 2:
        print('Gebruik: python3 intake_wizard.py /pad/naar/antwoorden.json')
        sys.exit(1)

    with open(sys.argv[1]) as f:
        a = json.load(f)

    ptype = DOEL_TYPE_MAP.get(a.get('stap1','A').upper(), 'landing')
    naam = a.get('stap2', 'MijnWebsite')
    beschrijving = a.get('stap3', '')
    kleurenschema = STIJL_KLEUR_MAP.get(a.get('stap5','F').upper(), 'goud en zwart')
    functies_raw = a.get('stap6', ['J'])
    if isinstance(functies_raw, str):
        functies_raw = [functies_raw]
    features = [FUNCTIE_MAP.get(f.upper(), f) for f in functies_raw]
    domein_keuze = a.get('stap7', 'B')
    domein = a.get('stap7_domein', '') if domein_keuze == 'A' else f'{naam.lower().replace(" ","-")}.vercel.app'
    admin_panel = a.get('stap8', 'D').upper() in ['A','B','D']
    website_agent = a.get('stap9', 'C').upper() in ['A','B']
    prijs = PRIJZEN.get(ptype, PRIJZEN['landing'])
    prijs_min = prijs['min'] + (3000 if website_agent else 0)
    prijs_max = prijs['max'] + (3000 if website_agent else 0)

    brief = {
        'naam': naam,
        'type': ptype,
        'beschrijving': beschrijving,
        'features': features,
        'kleurenschema': kleurenschema,
        'domein': domein,
        'admin_panel': admin_panel,
        'website_agent': website_agent,
        'prijs_min': prijs_min,
        'prijs_max': prijs_max,
        'bouwtijd': prijs['tijd'],
        'intake_datum': datetime.now().isoformat(),
        'intake_via': 'nova_telegram_wizard'
    }

    naam_slug = naam.lower().replace(' ','-')
    project_dir = f'{BUILDS_DIR}/{naam_slug}'
    os.makedirs(project_dir, exist_ok=True)
    intake_path = f'{project_dir}/intake.json'
    with open(intake_path, 'w') as f:
        json.dump(brief, f, indent=2, ensure_ascii=False)

    print(f'\n{"="*60}')
    print(f'✅ INTAKE VERWERKT')
    print(f'   Type:     {ptype}')
    print(f'   Naam:     {naam}')
    print(f'   Stijl:    {kleurenschema}')
    print(f'   Features: {", ".join(features[:3])}...')
    print(f'   Admin:    {"Ja" if admin_panel else "Nee"}')
    print(f'   Agent:    {"Ja" if website_agent else "Nee"}')
    print(f'   Prijs:    €{prijs_min:,} – €{prijs_max:,}')
    print(f'   Tijd:     {prijs["tijd"]}')
    print(f'{"="*60}')
    print(f'\n📋 Telegram bevestiging:')
    print(f'-'*60)
    print(f'🌐 Type: {ptype.title()}')
    print(f'✏️  Naam: {naam}')
    print(f'📝 {beschrijving}')
    print(f'🎨 Stijl: {kleurenschema}')
    print(f'⚙️  Functies: {", ".join(features[:4])}')
    print(f'🌍 Domein: {domein}')
    print(f'🔧 Admin: {"✅ Ja" if admin_panel else "❌ Nee"}')
    print(f'🤖 Agent: {"✅ Ja" if website_agent else "❌ Nee"}')
    print(f'💶 Prijs: €{prijs_min:,} – €{prijs_max:,}')
    print(f'⏱️  Bouwtijd: {prijs["tijd"]}')
    print(f'-'*60)
    print(f'\nVolgende stap:')
    print(f'python3 /home/prime/arc_ai_angels/agents/cortexia/workers/orchestrate_website_project.py {intake_path}')

if __name__ == '__main__':
    main()
