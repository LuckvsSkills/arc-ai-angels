#!/usr/bin/env python3
"""
onboard_website_agent.py — Clio worker
Genereert een gebonden website agent config voor opgeleverde websites
Gebruik: python3 onboard_website_agent.py /pad/naar/PROJECT_BRIEF.json
"""
import os, sys, json
from datetime import datetime

def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    print(f'[{ts}] {msg}')

def load_brief(path):
    with open(path) as f:
        return json.load(f)

def generate_agent_config(brief, docs_dir):
    naam = brief['project_naam']
    naam_slug = naam.lower().replace(' ', '-')
    ptype = brief['type']
    deploy = brief.get('deploy', {})
    live_url = deploy.get('url', f'https://{naam_slug}.vercel.app')
    admin_url = f'{live_url}/admin'
    ts = datetime.now().strftime('%Y-%m-%d')

    agent_tasks = {
        'ecommerce': [
            'Nieuwe bestellingen verwerken en bevestigingsmail sturen',
            'Leveranciers informeren bij lage voorraad',
            'Klantenvragen beantwoorden via email',
            'Wekelijks omzetrapport sturen aan eigenaar',
            'Verlaten winkelwagens opvolgen met reminder email',
        ],
        'saas': [
            'Nieuwe gebruikers welkom sturen',
            'Verlopen abonnementen opvolgen',
            'Maandelijks gebruiksrapport sturen',
            'Support tickets afhandelen',
            'Churn signalen detecteren en opvolgen',
        ],
        'booking': [
            'Nieuwe reserveringen bevestigen',
            'Herinneringen sturen 24u voor afspraak',
            'No-shows opvolgen',
            'Wekelijks agenda rapport sturen',
            'Reviews opvragen na afspraak',
        ],
        'directory': [
            'Nieuwe listings reviewen en goedkeuren',
            'Verlopen listings opvolgen',
            'Maandelijks traffic rapport sturen',
            'Spam listings verwijderen',
        ],
        'community': [
            'Nieuwe leden welkom sturen',
            'Moderatie van nieuwe posts',
            'Wekelijks community digest sturen',
            'Inactieve leden re-engagen',
        ],
    }

    taken = agent_tasks.get(ptype, [
        'Dagelijks systeem check uitvoeren',
        'Wekelijks rapport sturen aan eigenaar',
        'Klantenvragen beantwoorden',
    ])

    taken_list = '\n'.join([f'- {t}' for t in taken])

    agent_config = f"""# Website Agent Config — {naam}
**Website:** {live_url}
**Type:** {ptype}
**Aangemaakt:** {ts}
**Door:** Clio — ARC AI Agents

---

## Agent identiteit

**Naam:** {naam_slug}-agent
**Rol:** Website beheer agent voor {naam}
**Platform:** OpenClaw (eigen instantie of ARC systeem)

---

## Taken van deze agent

{taken_list}

---

## Configuratie

### OpenClaw setup
```bash
# Installeer OpenClaw op de doelserver
curl -fsSL https://openclaw.ai/install.sh | bash

# Configureer agent
openclaw agent create {naam_slug}-agent \\
  --role "Website beheer agent voor {naam}" \\
  --model "gpt-4o-mini"
```

### Environment variables
WEBSITE_URL={live_url}

ADMIN_URL={admin_url}

WEBSITE_TYPE={ptype}

OWNER_EMAIL=eigenaar@{naam_slug}.nl

TELEGRAM_CHAT_ID=VUL_IN

### Cronjobs
Dagelijkse check
0 9 * * * openclaw task {naam_slug}-agent "Voer dagelijkse website check uit"
Wekelijks rapport
0 10 * * 1 openclaw task {naam_slug}-agent "Maak wekelijks rapport voor eigenaar"

---

## Kosten schatting

| Gebruik | Model | Kosten/maand |
|---------|-------|-------------|
| Lichte taken | gemini-flash | ~€5-15 |
| Normale taken | gpt-4o-mini | ~€15-30 |
| Intensieve taken | gpt-4o | ~€30-80 |

**Aanbeveling:** gpt-4o-mini (~€15-30/maand)

---

*Gegenereerd door Clio — ARC AI Agents*
"""

    config_path = f'{docs_dir}/AGENT_CONFIG.md'
    with open(config_path, 'w') as f:
        f.write(agent_config)
    log(f'✅ Agent config geschreven: {config_path}')
    return config_path

def main():
    if len(sys.argv) < 2:
        print('Gebruik: python3 onboard_website_agent.py /pad/naar/PROJECT_BRIEF.json')
        sys.exit(1)

    brief_path = sys.argv[1]
    brief = load_brief(brief_path)

    if not brief.get('website_agent'):
        log(f'ℹ️  Type {brief["type"]} heeft geen website agent — overgeslagen')
        sys.exit(0)

    project_dir = os.path.dirname(brief_path)
    docs_dir = f'{project_dir}/docs'
    os.makedirs(docs_dir, exist_ok=True)

    log(f'🤖 Agent config: {brief["project_naam"]} ({brief["type"]})')
    config_path = generate_agent_config(brief, docs_dir)

    print('\n' + '='*50)
    print('✅ CLIO AGENT CONFIG KLAAR')
    print(f'   Config: {config_path}')
    print('='*50)

if __name__ == '__main__':
    main()
