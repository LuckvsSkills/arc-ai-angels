from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import json
import os
from pathlib import Path
from datetime import datetime

router = APIRouter()

PROJECTS_BASE = Path('/home/prime/arc_ai_angels/projects')
WEBSITE_BUILDS = PROJECTS_BASE / 'website_builds'
INTERN_DIR = PROJECTS_BASE / 'intern'

# PIN opgeslagen in memory per sessie (niet persistent)
_unlocked_projects = set()
DEFAULT_PIN = "1234"  # Fea kan dit wijzigen via .env


def get_pin():
    return os.environ.get('MCC_PROJECT_PIN', DEFAULT_PIN)


def scan_projects() -> list:
    """Scan alle project-mappen en laad PROJECT_STATUS.json."""
    projects = []

    for base_dir in [WEBSITE_BUILDS, INTERN_DIR]:
        if not base_dir.exists():
            continue
        for project_dir in sorted(base_dir.iterdir()):
            status_file = project_dir / 'PROJECT_STATUS.json'
            brief_file = project_dir / 'PROJECT_BRIEF.json'
            if not status_file.exists():
                continue
            try:
                with open(status_file) as f:
                    status = json.load(f)

                # Voeg extra meta toe
                status['_dir'] = str(project_dir)
                status['_has_brief'] = brief_file.exists()

                # Docs inventariseren
                docs_dir = project_dir / 'docs'
                status['_docs'] = []
                if docs_dir.exists():
                    status['_docs'] = [f.name for f in docs_dir.iterdir()
                                       if f.is_file() and f.suffix in ['.md', '.json', '.pdf']]

                projects.append(status)
            except Exception as e:
                projects.append({
                    'project_id': project_dir.name,
                    'naam': project_dir.name,
                    'status': 'fout',
                    '_error': str(e),
                    '_dir': str(project_dir)
                })

    return projects


@router.get('/projects')
def get_projects(filter: str = 'alle'):
    """Haal alle projecten op. Locked projecten tonen alleen metadata."""
    projects = scan_projects()
    result = []

    for p in projects:
        project_id = p.get('project_id', '')
        is_locked = p.get('locked', False)
        is_unlocked = project_id in _unlocked_projects

        if is_locked and not is_unlocked:
            # Alleen metadata tonen, geen task-details
            result.append({
                'project_id': project_id,
                'naam': p.get('naam', project_id),
                'type': p.get('type', 'onbekend'),
                'locked': True,
                'lock_hint': p.get('lock_hint', ''),
                'status': 'locked',
                'fase': p.get('fase', 0),
                'fase_naam': p.get('fase_naam', ''),
            })
        else:
            # Volledige data
            if filter == 'klant' and p.get('type') != 'klant':
                continue
            if filter == 'intern' and p.get('type') != 'intern':
                continue
            result.append(p)

    return result


@router.get('/projects/{project_id}')
def get_project(project_id: str):
    """Haal een specifiek project op."""
    projects = scan_projects()
    for p in projects:
        if p.get('project_id') == project_id:
            is_locked = p.get('locked', False)
            is_unlocked = project_id in _unlocked_projects
            if is_locked and not is_unlocked:
                raise HTTPException(status_code=403, detail='Project is vergrendeld')
            return p
    raise HTTPException(status_code=404, detail='Project niet gevonden')


@router.post('/projects/{project_id}/unlock')
def unlock_project(project_id: str, body: dict):
    """Ontgrendel een project met PIN."""
    pin = body.get('pin', '')
    if pin != get_pin():
        raise HTTPException(status_code=401, detail='Onjuiste PIN')
    _unlocked_projects.add(project_id)
    return {'success': True, 'project_id': project_id}


@router.post('/projects/{project_id}/lock')
def lock_project(project_id: str):
    """Vergrendel een project opnieuw."""
    _unlocked_projects.discard(project_id)

    # Update PROJECT_STATUS.json
    projects = scan_projects()
    for p in projects:
        if p.get('project_id') == project_id:
            status_file = Path(p['_dir']) / 'PROJECT_STATUS.json'
            try:
                with open(status_file) as f:
                    data = json.load(f)
                data['locked'] = True
                data['laatste_update'] = datetime.now().isoformat()
                with open(status_file, 'w') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
            return {'success': True}
    raise HTTPException(status_code=404, detail='Project niet gevonden')


@router.patch('/projects/{project_id}')
def update_project(project_id: str, body: dict):
    """Update PROJECT_STATUS.json velden (voor agents en MCC)."""
    projects = scan_projects()
    for p in projects:
        if p.get('project_id') == project_id:
            status_file = Path(p['_dir']) / 'PROJECT_STATUS.json'
            try:
                with open(status_file) as f:
                    data = json.load(f)

                # Toegestane velden om te updaten
                allowed = ['status','fase','fase_naam','locked','lock_hint',
                           'live_url','notion_page_url','notities','fases_voltooid','tasks']
                for key, val in body.items():
                    if key in allowed:
                        data[key] = val

                data['laatste_update'] = datetime.now().isoformat()

                with open(status_file, 'w') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                return data
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    raise HTTPException(status_code=404, detail='Project niet gevonden')


@router.post('/projects/{project_id}/notitie')
def add_notitie(project_id: str, body: dict):
    """Voeg een notitie toe aan een project."""
    tekst = body.get('tekst', '').strip()
    agent = body.get('agent', 'fea')
    if not tekst:
        raise HTTPException(status_code=400, detail='Notitie mag niet leeg zijn')

    projects = scan_projects()
    for p in projects:
        if p.get('project_id') == project_id:
            status_file = Path(p['_dir']) / 'PROJECT_STATUS.json'
            try:
                with open(status_file) as f:
                    data = json.load(f)
                if 'notities' not in data:
                    data['notities'] = []
                data['notities'].append({
                    'tekst': tekst,
                    'agent': agent,
                    'timestamp': datetime.now().isoformat()
                })
                data['laatste_update'] = datetime.now().isoformat()
                with open(status_file, 'w') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                return {'success': True, 'notities': data['notities']}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    raise HTTPException(status_code=404, detail='Project niet gevonden')
