from fastapi import APIRouter, Request
import json, os, subprocess
from datetime import datetime

router = APIRouter()
SW_DIR = '/home/prime/.openclaw/skill-workshop'
AGENTS_DIR = '/home/prime/arc_ai_angels/agents'

def parse_skill_file(filepath):
    """Parse een skill-workshop JSONL file"""
    skill = None
    session_id = None
    agent_id = None
    timestamp = None
    
    try:
        with open(filepath) as f:
            for line in f:
                line = line.strip()
                if not line: continue
                try:
                    d = json.loads(line)
                    
                    # Session info
                    if d.get('type') == 'session':
                        session_id = d.get('id','')
                        timestamp = d.get('timestamp','')
                        cwd = d.get('cwd','')
                        # Extract agent from cwd
                        if '/agents/' in cwd:
                            agent_id = cwd.split('/agents/')[1].split('/')[0]
                    
                    # Skill voorstel van assistant
                    if d.get('type') == 'message' and d.get('message',{}).get('role') == 'assistant':
                        for part in d['message'].get('content',[]):
                            if part.get('type') == 'text':
                                text = part['text'].strip()
                                if text.startswith('{') and 'skillName' in text:
                                    try:
                                        s = json.loads(text)
                                        if s.get('action','') != 'none':
                                            skill = s
                                    except: pass
                except: pass
    except: pass
    
    if not skill:
        return None
    
    return {
        'id': os.path.basename(filepath).replace('skill-workshop-review-','').replace('.approved.json','').replace('.rejected.json','').replace('.json',''),
        'file': filepath,
        'agent_id': agent_id or 'unknown',
        'timestamp': timestamp or '',
        'action': skill.get('action','create'),
        'skill_name': skill.get('skillName',''),
        'title': skill.get('title',''),
        'description': skill.get('description',''),
        'reason': skill.get('reason',''),
        'body': skill.get('body',''),
        'section': skill.get('section','Workflow'),
        'status': 'pending',
    }

@router.get("/skills/pending")
async def get_pending_skills():
    """Alle pending skills ter goedkeuring"""
    files = [f for f in os.listdir(SW_DIR)
             if f.startswith('skill-workshop-review')
             and f.endswith('.json')
             and 'trajectory' not in f
             and '.approved.' not in f
             and '.rejected.' not in f]
    
    skills = []
    for f in sorted(files, reverse=True):
        s = parse_skill_file(f'{SW_DIR}/{f}')
        if s:
            skills.append(s)
    
    # Dedup op skill_name — bewaar nieuwste
    seen = {}
    for s in skills:
        name = s['skill_name']
        if name not in seen:
            seen[name] = s
    
    unique = list(seen.values())
    unique.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return {
        'ok': True,
        'total': len(skills),
        'unique': len(unique),
        'skills': unique,
    }

@router.post("/skills/approve/{skill_id}")
async def approve_skill(skill_id: str):
    """Keur een skill goed — schrijf naar agent skills map"""
    # Zoek het file
    filepath = f'{SW_DIR}/skill-workshop-review-{skill_id}.json'
    if not os.path.exists(filepath):
        return {'ok': False, 'error': 'Skill niet gevonden'}
    
    skill = parse_skill_file(filepath)
    if not skill:
        return {'ok': False, 'error': 'Kon skill niet lezen'}
    
    agent_id = skill['agent_id']
    skill_name = skill['skill_name']
    
    # Schrijf skill naar agent skills map
    skills_dir = f'{AGENTS_DIR}/{agent_id}/skills'
    os.makedirs(skills_dir, exist_ok=True)
    skill_path = f'{skills_dir}/{skill_name}.md'
    
    # Bouw skill file
    skill_content = f"""---
name: {skill_name}
description: "{skill['description'][:100]}"
metadata: {{ "openclaw": {{ "emoji": "⭐", "approved_by": "Supreme Fea", "approved_at": "{datetime.now().strftime('%Y-%m-%d')}" }} }}
---
# {skill['title']}

{skill['description']}

## {skill['section']}

{skill['body']}
"""
    
    with open(skill_path, 'w') as f:
        f.write(skill_content)
    
    # Markeer als goedgekeurd — rename file
    approved_path = filepath.replace('.json', '.approved.json')
    os.rename(filepath, approved_path)
    # Verwijder trajectory files ook
    for ext in ['.trajectory-path.json', '.trajectory.jsonl']:
        traj = filepath.replace('.json', ext)
        if os.path.exists(traj):
            os.rename(traj, traj.replace('.json', '.approved.json').replace('.jsonl', '.approved.jsonl'))
    
    return {
        'ok': True,
        'message': f'Skill {skill_name} goedgekeurd voor {agent_id}',
        'skill_path': skill_path,
    }

@router.post("/skills/reject/{skill_id}")
async def reject_skill(skill_id: str, request: Request):
    """Wijs een skill af"""
    data = await request.json()
    reason = data.get('reason', 'Afgewezen door Supreme Fea')
    
    filepath = f'{SW_DIR}/skill-workshop-review-{skill_id}.json'
    if not os.path.exists(filepath):
        return {'ok': False, 'error': 'Skill niet gevonden'}
    
    # Markeer als afgewezen
    rejected_path = filepath.replace('.json', '.rejected.json')
    os.rename(filepath, rejected_path)
    
    return {
        'ok': True,
        'message': f'Skill afgewezen: {reason}',
    }

@router.get("/skills/approved")
async def get_approved_skills():
    """Alle goedgekeurde skills per agent"""
    result = {}
    for agent in os.listdir(AGENTS_DIR):
        skills_dir = f'{AGENTS_DIR}/{agent}/skills'
        if os.path.exists(skills_dir):
            skills = []
            for f in os.listdir(skills_dir):
                if f.endswith('.md'):
                    skills.append(f.replace('.md',''))
            if skills:
                result[agent] = skills
    
    return {'ok': True, 'by_agent': result}

@router.get("/skills/content/{agent_id}/{skill_name}")
async def get_skill_content(agent_id: str, skill_name: str):
    """Lees de inhoud van een skill file"""
    skill_path = f"{AGENTS_DIR}/{agent_id}/skills/{skill_name}.md"
    if not os.path.exists(skill_path):
        return {"ok": False, "content": "Skill niet gevonden"}
    with open(skill_path) as f:
        content = f.read()
    return {"ok": True, "content": content}
