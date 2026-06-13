from fastapi import APIRouter
import os, re
from datetime import datetime

router = APIRouter()

AGENTS_DIR = '/home/prime/arc_ai_angels/agents'
ALL_AGENTS = [
    'nova','flux','cortexia','nero','forge','axon','ventura','clio',
    'finoria','kairo','kenzo','odis','vector','zion',
    'saelia','tharos','sora','arix','enki','daxio',
    'lumeria','kresta','elora','luvia','nura','vondra',
    'fluentia','draven','solis','orizon','unia','zena'
]
DOMAIN_MAP = {
    'nova':'core','flux':'core',
    'cortexia':'helix','nero':'helix','forge':'helix','axon':'helix','ventura':'helix','clio':'helix',
    'finoria':'finix','kairo':'finix','kenzo':'finix','odis':'finix','vector':'finix','zion':'finix',
    'saelia':'matrix','tharos':'matrix','sora':'matrix','arix':'matrix','enki':'matrix','daxio':'matrix',
    'lumeria':'quantix','kresta':'quantix','elora':'quantix','luvia':'quantix','nura':'quantix','vondra':'quantix',
    'fluentia':'zenix','draven':'zenix','solis':'zenix','orizon':'zenix','unia':'zenix','zena':'zenix',
}

def parse_tasks_md(agent_id):
    path = f'{AGENTS_DIR}/{agent_id}/TASKS.md'
    if not os.path.exists(path):
        return []
    
    with open(path) as f:
        content = f.read()
    
    tasks = []
    # Split op ### Task: of ## blokken
    blocks = re.split(r'\n### Task:', content)
    
    for block in blocks[1:]:
        task = {'agent_id': agent_id, 'domain': DOMAIN_MAP.get(agent_id, 'unknown')}
        lines = block.strip().split('\n')
        
        # Task ID is eerste regel
        task['id'] = lines[0].strip()
        
        # Parse key-value regels
        for line in lines[1:]:
            line = line.strip()
            if line.startswith('- ') and ': ' in line:
                key, val = line[2:].split(': ', 1)
                key = key.strip().lower().replace(' ', '_')
                val = val.strip()
                task[key] = val
        
        # Verplichte velden met defaults
        task.setdefault('title', task['id'])
        task.setdefault('status', 'UNKNOWN')
        task.setdefault('priority', 'NORMAL')
        task.setdefault('assigned_by', 'unknown')
        task.setdefault('created_at', '')
        task.setdefault('result_summary', '')
        task.setdefault('next_step', '')
        
        tasks.append(task)
    
    return tasks

@router.get("/tasks/all")
async def get_all_tasks():
    """Alle taken van alle agents"""
    all_tasks = []
    errors = []
    
    for agent_id in ALL_AGENTS:
        try:
            tasks = parse_tasks_md(agent_id)
            all_tasks.extend(tasks)
        except Exception as e:
            errors.append(f'{agent_id}: {str(e)}')
    
    # Sorteer op status prioriteit
    status_order = {'IN_PROGRESS': 0, 'BLOCKED': 1, 'OPEN': 2, 'UNKNOWN': 3, 'DONE': 4, 'CLOSED': 5}
    all_tasks.sort(key=lambda t: status_order.get(t.get('status','UNKNOWN'), 3))
    
    return {
        'ok': True,
        'total': len(all_tasks),
        'tasks': all_tasks,
        'errors': errors,
        'by_status': {
            'in_progress': len([t for t in all_tasks if t.get('status') == 'IN_PROGRESS']),
            'blocked':     len([t for t in all_tasks if t.get('status') == 'BLOCKED']),
            'open':        len([t for t in all_tasks if t.get('status') in ['OPEN','UNKNOWN']]),
            'done':        len([t for t in all_tasks if t.get('status') in ['DONE','CLOSED']]),
        }
    }

@router.get("/tasks/agent/{agent_id}")
async def get_agent_tasks(agent_id: str):
    """Taken van een specifieke agent"""
    tasks = parse_tasks_md(agent_id)
    return {'ok': True, 'agent_id': agent_id, 'tasks': tasks}

@router.get("/tasks/domain/{domain}")
async def get_domain_tasks(domain: str):
    """Taken van een domein"""
    agents = [a for a, d in DOMAIN_MAP.items() if d == domain]
    all_tasks = []
    for agent_id in agents:
        all_tasks.extend(parse_tasks_md(agent_id))
    return {'ok': True, 'domain': domain, 'tasks': all_tasks}

@router.get("/tasks/active")
async def get_active_tasks():
    """Alleen actieve taken — IN_PROGRESS en BLOCKED"""
    all_tasks = []
    for agent_id in ALL_AGENTS:
        try:
            tasks = parse_tasks_md(agent_id)
            active = [t for t in tasks if t.get('status') in ['IN_PROGRESS','BLOCKED','OPEN']]
            all_tasks.extend(active)
        except:
            pass
    return {'ok': True, 'total': len(all_tasks), 'tasks': all_tasks}
