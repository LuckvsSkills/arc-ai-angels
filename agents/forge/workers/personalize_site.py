#!/usr/bin/env python3
"""
personalize_site.py — Forge worker
Personaliseert een gekloonde template op basis van PROJECT_BRIEF.json
Gebruik: python3 personalize_site.py /pad/naar/PROJECT_BRIEF.json
"""
import os, sys, json
from datetime import datetime

def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    print(f'[{ts}] {msg}')

def load_brief(path):
    with open(path) as f:
        return json.load(f)

def personalize(brief, code_dir):
    naam = brief['project_naam']
    beschrijving = brief['beschrijving']
    features = brief.get('features', [])
    kleur = brief.get('kleurenschema', 'goud en zwart')
    domein = brief.get('domein', f'{naam.lower()}.vercel.app')

    kleur_map = {
        'goud en zwart': {'accent': '#c9a84c', 'bg': '#0a0a0f', 'text': '#e2e8f0'},
        'blauw en wit':  {'accent': '#3b82f6', 'bg': '#ffffff', 'text': '#1e293b'},
        'groen en wit':  {'accent': '#10b981', 'bg': '#ffffff', 'text': '#1e293b'},
        'rood en zwart': {'accent': '#ef4444', 'bg': '#0a0a0f', 'text': '#e2e8f0'},
        'paars en wit':  {'accent': '#8b5cf6', 'bg': '#ffffff', 'text': '#1e293b'},
    }
    kleuren = kleur_map.get(kleur.lower(), kleur_map['goud en zwart'])

    replacements = {
        'PROJECT_NAAM':        naam,
        'PROJECT_BESCHRIJVING': beschrijving,
        'PROJECT_DOMEIN':      domein,
        'ACCENT_COLOR':        kleuren['accent'],
        'BG_COLOR':            kleuren['bg'],
        'TEXT_COLOR':          kleuren['text'],
        '{{naam}}':            naam,
        '{{beschrijving}}':    beschrijving,
        '{{domein}}':          domein,
    }

    files_changed = 0
    for root, dirs, files in os.walk(code_dir):
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__']]
        for fname in files:
            if not fname.endswith(('.html', '.css', '.js', '.jsx', '.ts', '.tsx', '.md', '.json', '.py', '.env.example')):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                original = content
                for placeholder, value in replacements.items():
                    content = content.replace(placeholder, value)
                if content != original:
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    files_changed += 1
            except Exception:
                pass

    log(f'✅ {files_changed} bestanden gepersonaliseerd')

    # Schrijf features naar een JSON bestand voor gebruik door de frontend
    features_path = f'{code_dir}/features.json'
    with open(features_path, 'w') as f:
        json.dump({'naam': naam, 'beschrijving': beschrijving, 'features': features, 'kleuren': kleuren}, f, indent=2)

    return files_changed

def update_brief(brief_path, brief):
    brief['sentinels']['forge'] = 'PERSONALIZED'
    brief['personalized_at'] = datetime.now().isoformat()
    with open(brief_path, 'w') as f:
        json.dump(brief, f, indent=2, ensure_ascii=False)

def main():
    if len(sys.argv) < 2:
        print('Gebruik: python3 personalize_site.py /pad/naar/PROJECT_BRIEF.json')
        sys.exit(1)

    brief_path = sys.argv[1]
    brief = load_brief(brief_path)
    code_dir = brief.get('code_dir')

    if not code_dir or not os.path.exists(code_dir):
        print(f'❌ code_dir niet gevonden in brief of bestaat niet: {code_dir}')
        print('   Voer eerst clone_template.py uit')
        sys.exit(1)

    log(f'🎨 Personalisatie starten: {brief["project_naam"]}')
    log(f'   Kleurenschema: {brief.get("kleurenschema", "goud en zwart")}')
    log(f'   Features: {len(brief.get("features", []))} stuks')

    changed = personalize(brief, code_dir)
    update_brief(brief_path, brief)

    print('\n' + '='*50)
    print('✅ FORGE PERSONALISATIE KLAAR')
    print(f'   Bestanden: {changed} bijgewerkt')
    print(f'   Map: {code_dir}')
    print(f'   Volgende: Nero security scan')
    print('='*50)

if __name__ == '__main__':
    main()
