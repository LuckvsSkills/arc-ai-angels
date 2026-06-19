#!/usr/bin/env python3
"""
init_project.py — Cortexia Worker
Initialiseert een nieuw project volgens PROJECT_SOP.md.
Maakt mapstructuur, PROJECT_STATUS.json en task-files aan.
"""
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

AGENTS_DIR = Path('/home/prime/arc_ai_angels/agents')
PROJECTS_DIR = Path('/home/prime/arc_ai_angels/projects')

# Welke agents betrokken zijn per template-type
AGENT_MATRIX = {
    'ecommerce': ['cortexia','forge','axon','nero','ventura','clio'],
    'landing':   ['cortexia','forge','nero','ventura','clio'],
    'portfolio': ['cortexia','forge','nero','ventura','clio'],
    'blog':      ['cortexia','forge','nero','ventura','clio'],
    'bedrijf':   ['cortexia','forge','nero','ventura','clio'],
    'bakkerij':  ['cortexia','forge','axon','nero','ventura','clio'],
    'booking':   ['cortexia','forge','axon','nero','ventura','clio'],
    'marketplace':['cortexia','forge','axon','nero','ventura','clio'],
    'saas':      ['cortexia','forge','nero','ventura','clio'],
    'community': ['cortexia','forge','axon','nero','ventura','clio'],
    'dashboard': ['cortexia','forge','axon','nero','ventura','clio'],
    'directory': ['cortexia','forge','nero','ventura','clio'],
    'api':       ['cortexia','forge','axon','nero','ventura','clio'],
    'intern':    ['cortexia','forge'],
}

# Dependency-matrix: wie wacht op wie
DEPENDENCIES = {
    'cortexia': [],
    'forge':    [],
    'nero':     [],
    'axon':     ['forge'],
    'ventura':  ['forge','axon'],
    'clio':     ['ventura'],
}

# Parallel met
PARALLEL = {
    'nero': ['forge'],
}

def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{ts}] [Cortexia/init_project] {msg}')

def init_project(brief_path: str):
    brief_path = Path(brief_path)
    if not brief_path.exists():
        log(f'ERROR: PROJECT_BRIEF.json niet gevonden: {brief_path}')
        sys.exit(1)

    with open(brief_path) as f:
        brief = json.load(f)

    project_id = brief.get('project_naam', 'onbekend').lower().replace(' ', '-')
    naam = brief.get('project_naam', 'Onbekend')
    template_type = brief.get('type', 'landing')
    project_type = brief.get('project_type', 'klant')

    # Project-map
    if project_type == 'intern':
        project_dir = PROJECTS_DIR / 'intern' / project_id
    else:
        project_dir = PROJECTS_DIR / 'website_builds' / project_id

    for subdir in ['tasks', 'code', 'docs', 'database']:
        (project_dir / subdir).mkdir(parents=True, exist_ok=True)

    log(f'Project-map aangemaakt: {project_dir}')

    # Agents bepalen
    agents = AGENT_MATRIX.get(template_type, AGENT_MATRIX['landing'])
    nu = datetime.now()
    sla = nu + timedelta(hours=24)

    # Task-statussen bepalen
    tasks = {}
    for agent in agents:
        deps = [d for d in DEPENDENCIES.get(agent, []) if d in agents]
        parallel = [p for p in PARALLEL.get(agent, []) if p in agents]

        if not deps and not parallel:
            status = 'open'
        elif parallel:
            status = 'parallel_met'
        else:
            status = 'wacht_op'

        entry = {
            'status': status,
            'gestart': None,
            'voltooid': None,
            'notitie': ''
        }
        if deps:
            entry['wacht_op'] = deps
        if parallel:
            entry['parallel_met'] = parallel

        tasks[agent] = entry

    # Cortexia zelf direct op done
    tasks['cortexia']['status'] = 'done'
    tasks['cortexia']['gestart'] = nu.isoformat()
    tasks['cortexia']['voltooid'] = nu.isoformat()
    tasks['cortexia']['notitie'] = 'Project geïnitialiseerd via init_project.py'

    # PROJECT_STATUS.json
    status_data = {
        'project_id': project_id,
        'naam': naam,
        'type': project_type,
        'template_type': template_type,
        'locked': False,
        'lock_hint': '',
        'status': 'in_uitvoering',
        'fase': 2,
        'fase_naam': 'Uitvoering',
        'aangemaakt': nu.isoformat(),
        'laatste_update': nu.isoformat(),
        'sla_deadline': sla.isoformat(),
        'lead_agent': 'cortexia',
        'agents': agents,
        'tasks': tasks,
        'live_url': None,
        'notion_page_url': None,
        'notities': [],
        'fases_voltooid': [0, 1]
    }

    status_path = project_dir / 'PROJECT_STATUS.json'
    with open(status_path, 'w') as f:
        json.dump(status_data, f, indent=2, ensure_ascii=False)
    log(f'PROJECT_STATUS.json aangemaakt')

    # Task-files per agent
    for agent in agents:
        task = tasks[agent]
        task_content = f"""# Task — {agent.upper()} — {naam}

Task ID: {agent.upper()}-{project_id.upper()}-001
Project ID: {project_id}
Project Naam: {naam}
Template Type: {template_type}
Priority: HIGH
Status: {task['status'].upper()}
Owner: {agent}
Assigned By: cortexia
Created At: {nu.strftime('%Y-%m-%d')}
Project Dir: {project_dir}
Brief: {project_dir}/PROJECT_BRIEF.json
Status File: {project_dir}/PROJECT_STATUS.json

Dependencies: {task.get('wacht_op', 'geen')}
Parallel Met: {task.get('parallel_met', 'geen')}

## Next Step
Lees PROJECT_STATUS.json, check of dependencies done zijn, voer taak uit, update status.

## Taakomschrijving
Zie PROJECT_SOP.md voor agent-verantwoordelijkheden per fase.

Result Summary:
Completion Validated By:
"""
        task_path = project_dir / 'tasks' / f'{agent}_task.md'
        with open(task_path, 'w') as f:
            f.write(task_content)

    log(f'{len(agents)} task-files aangemaakt')
    log(f'Project {naam} ({project_id}) klaar voor uitvoering')
    log(f'SLA deadline: {sla.strftime("%Y-%m-%d %H:%M")}')

    return str(project_dir)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Gebruik: python3 init_project.py <PROJECT_BRIEF.json>')
        sys.exit(1)
    init_project(sys.argv[1])
