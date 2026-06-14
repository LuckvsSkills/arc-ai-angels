#!/usr/bin/env python3
"""
clone_template.py — Forge worker
Kloont een GitHub template repo en personaliseert het voor een klant.
Gebruik: python3 clone_template.py /pad/naar/PROJECT_BRIEF.json
"""
import os, sys, json, subprocess, shutil
from datetime import datetime

def _load_github_token():
    env_path = "/home/prime/.openclaw/.env"
    try:
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("GITHUB_TOKEN"):
                    return line.split("=", 1)[1].strip().strip('"')
    except Exception:
        pass
    return ""

GITHUB_TOKEN = _load_github_token()

GITHUB_ORG = "LuckvsSkills"

TEMPLATE_MAP = {
    'landing':     'template-landing',
    'portfolio':   'template-portfolio',
    'blog':        'template-blog',
    'bedrijf':     'template-bedrijf',
    'ecommerce':   'template-ecommerce',
    'booking':     'template-booking',
    'marketplace': 'template-marketplace',
    'saas':        'template-saas',
    'community':   'template-community',
    'dashboard':   'template-dashboard',
    'directory':   'template-directory',
    'api':         'template-api',
    'bakkerij':    'template-bakkerij',
}

STIJL_VARS = {
    'minimalistisch': {
        'bg': '#ffffff', 'bg2': '#f8f9fa', 'accent': '#000000',
        'text': '#1a1a1a', 'textMuted': '#6b7280', 'border': 'rgba(0,0,0,0.08)',
        'fontHeading': 'DM Sans', 'fontBody': 'Inter'
    },
    'luxe': {
        'bg': '#0a0a0f', 'bg2': '#111118', 'accent': '#c9a84c',
        'text': '#e2e8f0', 'textMuted': '#94a3b8', 'border': 'rgba(255,255,255,0.08)',
        'fontHeading': 'Playfair Display', 'fontBody': 'Cormorant Garamond'
    },
    'zakelijk': {
        'bg': '#ffffff', 'bg2': '#f1f5f9', 'accent': '#1e40af',
        'text': '#1e293b', 'textMuted': '#64748b', 'border': 'rgba(0,0,0,0.08)',
        'fontHeading': 'Roboto', 'fontBody': 'Source Sans Pro'
    },
    'speels': {
        'bg': '#ffffff', 'bg2': '#faf5ff', 'accent': '#7c3aed',
        'text': '#1a1a2e', 'textMuted': '#6b7280', 'border': 'rgba(124,58,237,0.12)',
        'fontHeading': 'Poppins', 'fontBody': 'Nunito'
    },
    'organisch': {
        'bg': '#faf7f2', 'bg2': '#f0ebe3', 'accent': '#2d6a4f',
        'text': '#2d2926', 'textMuted': '#6b6560', 'border': 'rgba(45,106,79,0.12)',
        'fontHeading': 'Lora', 'fontBody': 'Merriweather'
    },
    'tech': {
        'bg': '#0d0d14', 'bg2': '#13131f', 'accent': '#00ff88',
        'text': '#e2e8f0', 'textMuted': '#64748b', 'border': 'rgba(0,255,136,0.12)',
        'fontHeading': 'Space Grotesk', 'fontBody': 'JetBrains Mono'
    },
}

def log(msg):
    print(f'[{datetime.now().strftime("%H:%M:%S")}] {msg}')

def kloon_template(template_naam, code_dir):
    if os.path.exists(code_dir):
        shutil.rmtree(code_dir)
    url = f'https://{GITHUB_TOKEN}@github.com/{GITHUB_ORG}/{template_naam}.git'
    result = subprocess.run(['git', 'clone', url, code_dir], capture_output=True, text=True)
    if result.returncode != 0:
        log(f'❌ Clone mislukt: {result.stderr.strip()}')
        return False
    shutil.rmtree(f'{code_dir}/.git', ignore_errors=True)
    import time
    time.sleep(0.5)
    log(f'✅ Template gekloond: {template_naam}')
    return True

def injecteer_stijl(code_dir, stijl_key, naam):
    vars = STIJL_VARS.get(stijl_key, STIJL_VARS['minimalistisch'])
    theme_css = f'''/* theme.css — Gegenereerd door Forge — ARC AI Agents */
/* Stijl: {stijl_key} | Project: {naam} */

@import url('https://fonts.googleapis.com/css2?family={vars["fontHeading"].replace(" ", "+")}:wght@400;700&family={vars["fontBody"].replace(" ", "+")}:wght@400;600&display=swap');

:root {{
  --bg:          {vars["bg"]};
  --bg2:         {vars["bg2"]};
  --accent:      {vars["accent"]};
  --text:        {vars["text"]};
  --text-muted:  {vars["textMuted"]};
  --border:      {vars["border"]};
  --font-heading: '{vars["fontHeading"]}', sans-serif;
  --font-body:    '{vars["fontBody"]}', sans-serif;
  --radius:      8px;
  --radius-lg:   16px;
  --shadow:      0 4px 24px rgba(0,0,0,0.08);
}}
'''
    theme_path = f'{code_dir}/styles/theme.css'
    os.makedirs(os.path.dirname(theme_path), exist_ok=True)
    with open(theme_path, 'w') as f:
        f.write(theme_css)
    log(f'✅ Stijl geïnjecteerd: {stijl_key} → accent {vars["accent"]}, font {vars["fontHeading"]}')

def personaliseer(code_dir, naam, beschrijving):
    vervangingen = {
        '{{PROJECT_NAAM}}': naam,
        '{{PROJECT_NAAM_SLUG}}': naam.lower().replace(' ', '-'),
        '{{PROJECT_BESCHRIJVING}}': beschrijving,
        '{{JAAR}}': str(datetime.now().year),
    }
    count = 0
    for root, dirs, files in os.walk(code_dir):
        dirs[:] = [d for d in dirs if d not in ['node_modules', '.git']]
        for fname in files:
            if not fname.endswith(('.html', '.jsx', '.js', '.ts', '.tsx', '.md', '.json', '.css')):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                original = content
                for placeholder, value in vervangingen.items():
                    content = content.replace(placeholder, value)
                if content != original:
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1
            except Exception:
                pass
    log(f'✅ Gepersonaliseerd: {count} bestanden bijgewerkt')

def main():
    if len(sys.argv) < 2:
        print('Gebruik: python3 clone_template.py /pad/naar/PROJECT_BRIEF.json')
        sys.exit(1)

    brief_path = sys.argv[1]
    with open(brief_path) as f:
        brief = json.load(f)

    naam = brief.get('naam') or brief.get('project_naam', 'MijnWebsite')
    naam_slug = naam.lower().replace(' ', '-')
    ptype = brief.get('type', 'landing')
    stijl = (brief.get('kleurenschema') or brief.get('stijl', 'minimalistisch')).lower().split()[0]
    beschrijving = brief.get('beschrijving', '')

    project_dir = os.path.dirname(brief_path)
    code_dir = f'{project_dir}/code'

    template_naam = TEMPLATE_MAP.get(ptype, 'template-landing')
    log(f'🔨 Forge bouwt: {naam} ({ptype}) → {template_naam} | stijl: {stijl}')

    if not kloon_template(template_naam, code_dir):
        sys.exit(1)

    injecteer_stijl(code_dir, stijl, naam)
    personaliseer(code_dir, naam, beschrijving)

    # Retry personalisatie als 0 bestanden zijn bijgewerkt (intermitterend timing-issue)
    test_file = f'{code_dir}/frontend/index.html'
    if os.path.exists(test_file):
        with open(test_file) as f:
            if '{{PROJECT_NAAM}}' in f.read():
                log('⚠️  Placeholders nog aanwezig, retry personalisatie...')
                personaliseer(code_dir, naam, beschrijving)

    brief['code_dir'] = code_dir
    brief.setdefault('sentinels', {})['forge'] = 'CLONE_DONE'
    with open(brief_path, 'w') as f:
        json.dump(brief, f, indent=2, ensure_ascii=False)

    print(f'\n{"="*60}')
    print(f'✅ FORGE KLAAR')
    print(f'   Project: {naam}')
    print(f'   Type:    {ptype} → {template_naam}')
    print(f'   Stijl:   {stijl}')
    print(f'   Code:    {code_dir}')
    print(f'{"="*60}')

if __name__ == '__main__':
    main()
