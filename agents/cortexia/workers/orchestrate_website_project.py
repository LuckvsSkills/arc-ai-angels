#!/usr/bin/env python3
"""
orchestrate_website_project.py — Cortexia worker
Orkestreert een volledig website bouwproject van intake tot oplevering.
Gebruik: python3 orchestrate_website_project.py /pad/naar/intake.json
"""
import os, sys, json, subprocess
from datetime import datetime

BUILDS_DIR = '/home/prime/arc_ai_angels/projects/website_builds'
AGENTS_DIR = '/home/prime/arc_ai_angels/agents'

TEMPLATE_MAP = {
    'landing':     {'stack': 'HTML/CSS/JS',              'admin': False, 'agent': False},
    'portfolio':   {'stack': 'HTML/CSS/JS',              'admin': False, 'agent': False},
    'blog':        {'stack': 'Next.js+Markdown',         'admin': True,  'agent': False},
    'saas':        {'stack': 'React+FastAPI+PostgreSQL', 'admin': True,  'agent': True},
    'ecommerce':   {'stack': 'React+FastAPI+Stripe',     'admin': True,  'agent': True},
    'directory':   {'stack': 'React+FastAPI+PostgreSQL', 'admin': True,  'agent': True},
    'marketplace': {'stack': 'React+FastAPI+Stripe',     'admin': True,  'agent': True},
    'dashboard':   {'stack': 'React+FastAPI+WebSockets', 'admin': True,  'agent': True},
    'community':   {'stack': 'React+FastAPI+WebSockets', 'admin': True,  'agent': True},
    'booking':     {'stack': 'React+FastAPI+Stripe',     'admin': True,  'agent': True},
}

PRICING = {
    'landing':     {'tier': 1, 'min': 500,   'max': 2000},
    'portfolio':   {'tier': 1, 'min': 500,   'max': 2000},
    'blog':        {'tier': 1, 'min': 800,   'max': 2500},
    'saas':        {'tier': 2, 'min': 3000,  'max': 8000},
    'ecommerce':   {'tier': 2, 'min': 3000,  'max': 8000},
    'directory':   {'tier': 2, 'min': 3500,  'max': 8000},
    'marketplace': {'tier': 2, 'min': 4000,  'max': 10000},
    'dashboard':   {'tier': 2, 'min': 3000,  'max': 7000},
    'community':   {'tier': 2, 'min': 3500,  'max': 8000},
    'booking':     {'tier': 2, 'min': 2500,  'max': 6000},
}

def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    print(f'[{ts}] {msg}')

def load_intake(path):
    with open(path) as f:
        return json.load(f)

def validate_intake(intake):
    required = ['naam', 'type', 'beschrijving', 'features']
    missing = [f for f in required if f not in intake]
    if missing:
        print(f'❌ Intake mist verplichte velden: {missing}')
        sys.exit(1)
    if intake['type'] not in TEMPLATE_MAP:
        print(f'❌ Onbekend type: {intake["type"]}')
        print(f'   Beschikbare types: {list(TEMPLATE_MAP.keys())}')
        sys.exit(1)
    return True

def create_project_structure(intake):
    naam = intake['naam'].lower().replace(' ', '-')
    project_dir = f'{BUILDS_DIR}/{naam}'
    os.makedirs(project_dir, exist_ok=True)

    brief = {
        'project_naam': intake['naam'],
        'type': intake['type'],
        'beschrijving': intake['beschrijving'],
        'features': intake['features'],
        'kleurenschema': intake.get('kleurenschema', 'ARC default'),
        'domein': intake.get('domein', f'{naam}.vercel.app'),
        'template': f'template-{intake["type"]}',
        'stack': TEMPLATE_MAP[intake['type']]['stack'],
        'admin_panel': TEMPLATE_MAP[intake['type']]['admin'],
        'website_agent': TEMPLATE_MAP[intake['type']]['agent'],
        'pricing': PRICING[intake['type']],
        'aangemaakt': datetime.now().isoformat(),
        'status': 'GESTART',
        'sentinels': {
            'forge':   'PENDING',
            'axon':    'PENDING',
            'nero':    'PENDING',
            'ventura': 'PENDING',
            'clio':    'PENDING',
        }
    }

    with open(f'{project_dir}/PROJECT_BRIEF.json', 'w') as f:
        json.dump(brief, f, indent=2, ensure_ascii=False)

    log(f'✅ Project structuur aangemaakt: {project_dir}')
    return project_dir, brief

def create_sentinel_tasks(brief, project_dir):
    naam = brief['project_naam']
    ptype = brief['type']
    ts = datetime.now().strftime('%Y-%m-%d')

    tasks = {
        'forge': f"""
Task ID: FORGE-WEBSITE-{naam.upper()}-001
Title: Website bouwen — {naam}
Summary: Clone template-{ptype}, personaliseer op basis van PROJECT_BRIEF.json, bouw admin panel indien vereist.
Priority: HIGH
Status: OPEN
Assigned By: cortexia
Created At: {ts}
Project Dir: {project_dir}
Brief: {project_dir}/PROJECT_BRIEF.json
Next Step: python3 /home/prime/arc_ai_angels/agents/forge/workers/clone_template.py {project_dir}/PROJECT_BRIEF.json
Result Summary:
Completion Validated By:
""",
        'axon': f"""
Task ID: AXON-DATABASE-{naam.upper()}-001
Title: Database + pipeline opzetten — {naam}
Summary: Database provisionen, schema aanmaken, payment integratie indien vereist.
Priority: HIGH
Status: OPEN
Assigned By: cortexia
Created At: {ts}
Project Dir: {project_dir}
Brief: {project_dir}/PROJECT_BRIEF.json
Next Step: python3 /home/prime/arc_ai_angels/agents/axon/workers/provision_database.py {project_dir}/PROJECT_BRIEF.json
Result Summary:
Completion Validated By:
""",
        'nero': f"""
Task ID: NERO-SECURITY-{naam.upper()}-001
Title: Security audit — {naam}
Summary: Template scannen op security issues, hardening uitvoeren, groen licht geven voor deploy.
Priority: HIGH
Status: PENDING — wacht op Forge
Assigned By: cortexia
Created At: {ts}
Project Dir: {project_dir}
Brief: {project_dir}/PROJECT_BRIEF.json
Next Step: python3 /home/prime/arc_ai_angels/agents/nero/workers/scan_template_security.py {project_dir}
Result Summary:
Completion Validated By:
""",
        'ventura': f"""
Task ID: VENTURA-DEPLOY-{naam.upper()}-001
Title: Deploy naar Vercel — {naam}
Summary: Website deployen, domein koppelen, SSL activeren, health check uitvoeren.
Priority: HIGH
Status: PENDING — wacht op Nero groen licht
Assigned By: cortexia
Created At: {ts}
Project Dir: {project_dir}
Brief: {project_dir}/PROJECT_BRIEF.json
Next Step: bash /home/prime/arc_ai_angels/agents/ventura/workers/provision_cloud_service.sh {project_dir}/PROJECT_BRIEF.json
Result Summary:
Completion Validated By:
""",
        'clio': f"""
Task ID: CLIO-DOCS-{naam.upper()}-001
Title: Documentatie + oplevering — {naam}
Summary: README, API docs, deployment guide en client handoff package genereren.
Priority: NORMAL
Status: PENDING — wacht op Ventura
Assigned By: cortexia
Created At: {ts}
Project Dir: {project_dir}
Brief: {project_dir}/PROJECT_BRIEF.json
Next Step: python3 /home/prime/arc_ai_angels/agents/clio/workers/generate_client_handoff.py {project_dir}/PROJECT_BRIEF.json
Result Summary:
Completion Validated By:
"""
    }

    tasks_dir = f'{project_dir}/tasks'
    os.makedirs(tasks_dir, exist_ok=True)

    for agent, task in tasks.items():
        with open(f'{tasks_dir}/{agent}_task.md', 'w') as f:
            f.write(task.strip())
        log(f'  📋 Taak aangemaakt voor {agent}')

    return tasks_dir

def print_project_summary(brief, project_dir):
    pricing = brief['pricing']
    print('\n' + '='*60)
    print(f'🚀 WEBSITE PROJECT GESTART')
    print('='*60)
    print(f'  Naam:      {brief["project_naam"]}')
    print(f'  Type:      {brief["type"]}')
    print(f'  Template:  {brief["template"]}')
    print(f'  Stack:     {brief["stack"]}')
    print(f'  Admin:     {"Ja" if brief["admin_panel"] else "Nee"}')
    print(f'  AI Agent:  {"Ja" if brief["website_agent"] else "Nee"}')
    print(f'  Tier:      {pricing["tier"]}')
    print(f'  Prijs:     €{pricing["min"]} – €{pricing["max"]}')
    print(f'  Dir:       {project_dir}')
    print('='*60)
    print('📋 Sentinel taken aangemaakt:')
    print('  → Forge:   clone + personaliseren + admin panel')
    print('  → Axon:    database + pipeline + betaling')
    print('  → Nero:    security scan (na Forge)')
    print('  → Ventura: deploy (na Nero groen licht)')
    print('  → Clio:    documentatie + oplevering')
    print('='*60)
    print(f'📁 Project brief: {project_dir}/PROJECT_BRIEF.json')
    print(f'📋 Taken: {project_dir}/tasks/')
    print('='*60)

def main():
    if len(sys.argv) < 2:
        print('Gebruik: python3 orchestrate_website_project.py /pad/naar/intake.json')
        print()
        print('Intake JSON formaat:')
        print(json.dumps({
            'naam': 'MijnWebshop',
            'type': 'ecommerce',
            'beschrijving': 'Online winkel voor handgemaakte sieraden',
            'features': ['productcatalogus', 'winkelwagen', 'checkout', 'orderhistorie'],
            'kleurenschema': 'goud en zwart',
            'domein': 'mijnwebshop.nl'
        }, indent=2, ensure_ascii=False))
        sys.exit(1)

    intake_path = sys.argv[1]
    if not os.path.exists(intake_path):
        print(f'❌ Intake bestand niet gevonden: {intake_path}')
        sys.exit(1)

    log('📥 Intake laden...')
    intake = load_intake(intake_path)

    log('✅ Intake valideren...')
    validate_intake(intake)

    log('📁 Project structuur aanmaken...')
    project_dir, brief = create_project_structure(intake)

    log('📋 Sentinel taken aanmaken...')
    create_sentinel_tasks(brief, project_dir)

    print_project_summary(brief, project_dir)

if __name__ == '__main__':
    main()
