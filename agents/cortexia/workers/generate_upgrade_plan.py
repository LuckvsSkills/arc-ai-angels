#!/usr/bin/env python3
"""
generate_upgrade_plan.py — Cortexia worker
Genereert een upgrade plan op basis van ADVIES_RAPPORT of directe intake.
Gebruik: python3 generate_upgrade_plan.py /pad/naar/intake.json
"""
import os, sys, json
from datetime import datetime

BUILDS_DIR = '/home/prime/arc_ai_angels/projects/website_builds'

def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    print(f'[{ts}] {msg}')

def load_intake(path):
    with open(path) as f:
        return json.load(f)

def load_scan_result(scan_dir):
    scan_path = f'{scan_dir}/SCAN_RESULT.json'
    if os.path.exists(scan_path):
        with open(scan_path) as f:
            return json.load(f)
    return None

def determine_upgrade_scope(scan_result, intake):
    """Bepaal upgrade scope: klein/middel/groot/rebuild"""
    wensen = intake.get('upgrade_wensen', [])
    score = scan_result.get('ai_readiness_score', 0) if scan_result else 50

    if score < 30 or any('rebuild' in w.lower() for w in wensen):
        return 'rebuild', 'Volledige herbouw met nieuwe stack + admin + AI agents'
    elif score < 60 or len(wensen) > 3:
        return 'groot', 'Grote uitbreiding — nieuwe features + AI integraties'
    elif len(wensen) > 1:
        return 'middel', 'Middelgrote upgrade — nieuwe modules toevoegen'
    else:
        return 'klein', 'Kleine upgrade — aanpassingen en optimalisaties'

def build_upgrade_plan(intake, scan_result, scope, scope_desc):
    """Bouw concreet upgrade plan per sentinel"""
    naam = intake['naam']
    wensen = intake.get('upgrade_wensen', [])
    ts = datetime.now().strftime('%Y-%m-%d')

    plan = {
        'project_naam': naam,
        'intake_type': 'upgrade',
        'scope': scope,
        'scope_beschrijving': scope_desc,
        'upgrade_wensen': wensen,
        'aangemaakt': ts,
        'status': 'GEPLAND',
        'sentinels': {}
    }

    if scope == 'klein':
        plan['sentinels'] = {
            'forge': {
                'taak': 'Code aanpassingen doorvoeren',
                'acties': ['CSS/JS updates', 'content wijzigingen', 'performance optimalisaties'],
                'worker': 'personalize_site.py',
                'status': 'PENDING'
            },
            'nero': {
                'taak': 'Security check na aanpassingen',
                'acties': ['code review', 'security scan'],
                'worker': 'scan_template_security.py',
                'status': 'PENDING'
            },
            'ventura': {
                'taak': 'Deploy bijgewerkte versie',
                'acties': ['deploy naar Vercel', 'health check'],
                'worker': 'provision_cloud_service.sh',
                'status': 'PENDING'
            },
            'clio': {
                'taak': 'Changelog en update docs',
                'acties': ['changelog schrijven', 'docs updaten'],
                'worker': 'generate_client_handoff.py',
                'status': 'PENDING'
            }
        }
        plan['doorlooptijd'] = '3-5 werkdagen'
        plan['kostenraming'] = '€500 – €1.500'

    elif scope == 'middel':
        plan['sentinels'] = {
            'forge': {
                'taak': 'Nieuwe features bouwen',
                'acties': ['nieuwe componenten', 'integraties', 'UI verbeteringen'],
                'worker': 'clone_template.py',
                'status': 'PENDING'
            },
            'axon': {
                'taak': 'Database uitbreidingen',
                'acties': ['nieuwe tabellen', 'API endpoints', 'data migratie'],
                'worker': 'provision_database.py',
                'status': 'PENDING'
            },
            'nero': {
                'taak': 'Security audit',
                'acties': ['volledige security scan', 'OWASP check'],
                'worker': 'scan_template_security.py',
                'status': 'PENDING'
            },
            'ventura': {
                'taak': 'Deploy uitgebreide versie',
                'acties': ['deploy', 'domein check', 'SSL'],
                'worker': 'provision_cloud_service.sh',
                'status': 'PENDING'
            },
            'clio': {
                'taak': 'Volledige documentatie update',
                'acties': ['README', 'API docs', 'changelog'],
                'worker': 'generate_client_handoff.py',
                'status': 'PENDING'
            }
        }
        plan['doorlooptijd'] = '1-2 weken'
        plan['kostenraming'] = '€2.000 – €5.000'

    else:  # groot of rebuild
        plan['sentinels'] = {
            'forge': {
                'taak': 'Volledige herbouw frontend + backend',
                'acties': ['nieuwe React frontend', 'FastAPI backend', 'admin panel', 'content migratie'],
                'worker': 'clone_template.py',
                'status': 'PENDING'
            },
            'axon': {
                'taak': 'Nieuwe database + pipelines',
                'acties': ['database ontwerp', 'migratie bestaande data', 'payment integratie', 'webhooks'],
                'worker': 'provision_database.py',
                'status': 'PENDING'
            },
            'nero': {
                'taak': 'Volledige security audit',
                'acties': ['OWASP scan', 'penetration test', 'secrets check', 'hardening'],
                'worker': 'scan_template_security.py',
                'status': 'PENDING'
            },
            'ventura': {
                'taak': 'Cloud deploy + domein migratie',
                'acties': ['VPS of Vercel setup', 'domein migratie', 'SSL', 'monitoring'],
                'worker': 'provision_cloud_service.sh',
                'status': 'PENDING'
            },
            'clio': {
                'taak': 'Volledige documentatie + client handoff',
                'acties': ['README', 'API docs', 'deployment guide', 'gebruikershandleiding', 'AI agent docs'],
                'worker': 'generate_client_handoff.py',
                'status': 'PENDING'
            }
        }
        plan['doorlooptijd'] = '3-6 weken'
        plan['kostenraming'] = '€5.000 – €15.000 + €500/mnd'

    # AI agent toevoegen als gewenst
    if any('agent' in w.lower() or 'ai' in w.lower() for w in wensen):
        plan['website_agent'] = True
        plan['agent_taken'] = [w for w in wensen if 'agent' in w.lower() or 'automat' in w.lower() or 'order' in w.lower()]

    return plan

def save_upgrade_plan(plan, project_dir):
    plan_path = f'{project_dir}/UPGRADE_PLAN.json'
    with open(plan_path, 'w') as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)

    md_path = f'{project_dir}/UPGRADE_PLAN.md'
    with open(md_path, 'w') as f:
        f.write(f"""# Upgrade Plan — {plan['project_naam']}
**Scope:** {plan['scope'].upper()} — {plan['scope_beschrijving']}
**Doorlooptijd:** {plan['doorlooptijd']}
**Kostenraming:** {plan['kostenraming']}
**Aangemaakt:** {plan['aangemaakt']}

---

## Gewenste verbeteringen
{chr(10).join([f'- {w}' for w in plan['upgrade_wensen']])}

---

## Sentinel taakverdeling

""")
        for agent, details in plan['sentinels'].items():
            f.write(f"""### {agent.upper()}
**Taak:** {details['taak']}
**Acties:** {', '.join(details['acties'])}
**Worker:** {details['worker']}
**Status:** {details['status']}

""")
        if plan.get('website_agent'):
            f.write(f"""---

## AI Agent integratie
Website agent wordt toegevoegd voor:
{chr(10).join([f'- {t}' for t in plan.get('agent_taken', [])])}

Agent draait op OpenClaw, volledig autonoom.
Maandelijkse kosten: €300 – €500/mnd
""")

    return plan_path, md_path

def main():
    if len(sys.argv) < 2:
        print('Gebruik: python3 generate_upgrade_plan.py /pad/naar/intake.json')
        sys.exit(1)

    intake_path = sys.argv[1]
    if not os.path.exists(intake_path):
        print(f'❌ Intake niet gevonden: {intake_path}')
        sys.exit(1)

    intake = load_intake(intake_path)
    naam = intake['naam'].lower().replace(' ', '-')
    project_dir = f'{BUILDS_DIR}/{naam}-scan'
    os.makedirs(project_dir, exist_ok=True)

    log(f'📋 Upgrade plan genereren: {intake["naam"]}')

    scan_result = load_scan_result(project_dir)
    if scan_result:
        log(f'   Scan gevonden — AI score: {scan_result["ai_readiness_score"]}/100')
    else:
        log('   Geen scan gevonden — plan op basis van intake wensen')

    scope, scope_desc = determine_upgrade_scope(scan_result, intake)
    log(f'   Scope: {scope.upper()} — {scope_desc}')

    plan = build_upgrade_plan(intake, scan_result, scope, scope_desc)
    plan_path, md_path = save_upgrade_plan(plan, project_dir)

    print('\n' + '='*60)
    print('✅ UPGRADE PLAN GEGENEREERD')
    print('='*60)
    print(f'  Project:      {intake["naam"]}')
    print(f'  Scope:        {scope.upper()}')
    print(f'  Doorlooptijd: {plan["doorlooptijd"]}')
    print(f'  Kosten:       {plan["kostenraming"]}')
    print(f'  AI Agent:     {"Ja" if plan.get("website_agent") else "Nee"}')
    print(f'  Plan:         {md_path}')
    print('='*60)
    print('📋 Sentinels klaar:')
    for agent in plan['sentinels']:
        print(f'   → {agent}')
    print('='*60)

if __name__ == '__main__':
    main()
