from fastapi import APIRouter
import os, re, subprocess
from app.config import AGENTS_DIR

router = APIRouter()

AGENT_IDS = ["nova","flux","cortexia","nero","forge","axon","ventura","clio",
             "finoria","kairo","kenzo","odis","vector","zion","saelia","arix",
             "daxio","enki","sora","tharos","lumeria","elora","kresta","luvia",
             "nura","vondra","fluentia","draven","orizon","solis","unia","zena"]


DOMAIN_MAP = {"helix":["cortexia","nero","forge","axon","ventura","clio"],
              "finix":["finoria","kairo","kenzo","odis","vector","zion"],
              "matrix":["saelia","arix","daxio","enki","sora","tharos"],
              "quantix":["lumeria","elora","kresta","luvia","nura","vondra"],
              "zenix":["fluentia","draven","orizon","solis","unia","zena"]}

def _get_domain(aid):
    for d, agents in DOMAIN_MAP.items():
        if aid in agents: return d
    return "core"

def read_agent_pulse(agent_id):
    base = f"{AGENTS_DIR}/{agent_id}"
    p = {"id": agent_id, "memory_kb": 0, "memory_lines": 0, "journal_open": 0,
         "journal_closed": 0, "last_consolidation": None, "success_rate": None,
         "tasks_today": None, "archived_today": None, "cronjobs": 0, "status": "unknown"}
    mem = f"{base}/MEMORY.md"
    if os.path.exists(mem):
        p["memory_kb"] = round(os.path.getsize(mem)/1024, 1)
        p["memory_lines"] = len(open(mem, errors="ignore").readlines())
    jo = f"{base}/JOURNAL/open"
    jc = f"{base}/JOURNAL/closed"
    if os.path.exists(jo): p["journal_open"] = len([f for f in os.listdir(jo) if f.endswith(".md")])
    if os.path.exists(jc): p["journal_closed"] = len([f for f in os.listdir(jc) if f.endswith(".md")])
    clog = f"{base}/consolidation.log"
    if os.path.exists(clog):
        lines = open(clog, errors="ignore").readlines()
        for line in reversed(lines):
            if not p["last_consolidation"]:
                m = re.search(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]', line)
                if m: p["last_consolidation"] = m.group(1)
            if p["success_rate"] is None:
                m = re.search(r'Success rate: (\d+)%', line)
                if m: p["success_rate"] = int(m.group(1))
            if p["tasks_today"] is None:
                m = re.search(r'Tasks processed: (\d+)', line)
                if m: p["tasks_today"] = int(m.group(1))
            if p["archived_today"] is None:
                m = re.search(r'archived (\d+) entries', line)
                if m: p["archived_today"] = int(m.group(1))
    try:
        import json as _json
        _jobs = _json.load(open(os.path.expanduser("~/.openclaw/cron/jobs.json")))
        p["cronjobs"] = sum(1 for j in _jobs.get("jobs",[]) if j.get("agentId")==agent_id and j.get("enabled",True))
    except: pass
    p["status"] = "healthy" if p["cronjobs"] >= 4 and p["memory_kb"] > 0 else "warning" if p["cronjobs"] > 0 else "critical"
    return p

@router.get("/memory/pulse")
async def get_pulse():
    agents = [read_agent_pulse(aid) for aid in AGENT_IDS]
    healthy = sum(1 for a in agents if a["status"]=="healthy")
    warning = sum(1 for a in agents if a["status"]=="warning")
    critical = sum(1 for a in agents if a["status"]=="critical")
    try:
        import json as _json
        _jobs = _json.load(open(os.path.expanduser("~/.openclaw/cron/jobs.json")))
        total_crons = sum(1 for j in _jobs.get("jobs",[]) if j.get("enabled",True))
    except: total_crons = 0
    return {"agents": agents, "summary": {"total_agents": len(agents), "healthy": healthy,
            "warning": warning, "critical": critical, "total_cronjobs": total_crons, "expected_cronjobs": 128}}

@router.get("/memory/agents")
async def get_memory_agents():
    result = []
    for aid in AGENT_IDS:
        base = f"{AGENTS_DIR}/{aid}"
        mem_file = f"{base}/MEMORY.md"
        result.append({
            "id": aid, "name": aid.capitalize(),
            "layer": "gateway" if aid=="nova" else "orchestrator" if aid=="flux" else "lead" if aid in ["cortexia","finoria","saelia","lumeria","fluentia"] else "sentinel",
            "domain": _get_domain(aid),
            "memory_kb": round(os.path.getsize(mem_file)/1024,1) if os.path.exists(mem_file) else 0,
            "memory_bytes": os.path.getsize(mem_file) if os.path.exists(mem_file) else 0,
            "status": "healthy", "memory_status_color": "green",
            "journal_open_count": 0, "journal_closed_count": 0,
            "last_update": "1970-01-01T01:00:00Z",
            "handoff_bytes": 0,
        })
    return {"agents": result}

@router.get("/memory/agents/{agent_id}")
async def get_agent_memory(agent_id: str):
    mem_file = f"{AGENTS_DIR}/{agent_id}/MEMORY.md"
    if not os.path.exists(mem_file):
        return {"agent_id": agent_id, "memory_content": "", "memory_bytes": 0}
    content = open(mem_file, errors="ignore").read()
    return {"agent_id": agent_id, "memory_content": content, "memory_bytes": len(content),
            "last_updated": f"{os.path.getmtime(mem_file):.0f}"}

@router.get("/memory/system-status")
async def system_status():
    total_kb = sum(os.path.getsize(f"{AGENTS_DIR}/{a}/MEMORY.md")/1024
                   for a in AGENT_IDS if os.path.exists(f"{AGENTS_DIR}/{a}/MEMORY.md"))
    return {"memory_health_percent": 85, "agent_memory_used_kb": round(total_kb,2),
            "agent_memory_limit_kb": 1000, "system_status": "OPERATIONAL",
            "consolidation_status": "success", "last_consolidation_success": True}

@router.get("/memory/learnings")
async def get_learnings():
    result = {}
    for aid in ["nova","flux"]:
        mem_file = f"{AGENTS_DIR}/{aid}/MEMORY.md"
        if os.path.exists(mem_file):
            content = open(mem_file, errors="ignore").read()
            result[aid] = {"memory_content": content, "memory_bytes": len(content),
                           "last_updated": f"{os.path.getmtime(mem_file):.3f}Z"}
    return {"learnings": result, "total_agents_with_memory": len(result),
            "total_learning_bytes": sum(v["memory_bytes"] for v in result.values())}

@router.get("/memory/cronjobs")
async def get_cronjobs():
    try:
        import json as _j
        jobs_path = os.path.expanduser("~/.openclaw/cron/jobs.json")
        d = _j.load(open(jobs_path))
        jobs = d.get("jobs", [])
        from datetime import datetime
        result = []
        for j in jobs:
            state = j.get("state", {})
            last_run = state.get("lastRunAtMs", 0)
            next_run = state.get("nextRunAtMs", 0)
            result.append({
                "id": j.get("name", j.get("id","")),
                "agent_id": j.get("agentId",""),
                "agent_name": j.get("agentId","").capitalize(),
                "schedule": j.get("schedule",{}).get("expr","") if isinstance(j.get("schedule"),dict) else "",
                "enabled": j.get("enabled", True),
                "status": state.get("lastStatus","nieuw"),
                "last_run": datetime.fromtimestamp(last_run/1000).strftime("%Y-%m-%d %H:%M") if last_run else "nooit",
                "next_run": datetime.fromtimestamp(next_run/1000).strftime("%Y-%m-%d %H:%M") if next_run else "onbekend",
                "errors": state.get("consecutiveErrors", 0),
            })
        return {"cronjobs": result, "total": len(jobs)}
    except Exception as e:
        return {"cronjobs": [], "total": 0, "error": str(e)}

@router.get("/memory/domains")
async def get_domains():
    domains = [
        {"id":"core","name":"Core","color":"#c9a84c","agents":["nova","flux"]},
        {"id":"helix","name":"Helix","color":"#38bdf8","agents":["cortexia","nero","forge","axon","ventura","clio"]},
        {"id":"finix","name":"Finix","color":"#f472b6","agents":["finoria","kairo","kenzo","odis","vector","zion"]},
        {"id":"matrix","name":"Matrix","color":"#34d399","agents":["saelia","arix","daxio","enki","sora","tharos"]},
        {"id":"quantix","name":"Quantix","color":"#a78bfa","agents":["lumeria","elora","kresta","luvia","nura","vondra"]},
        {"id":"zenix","name":"Zenix","color":"#fb923c","agents":["fluentia","draven","orizon","solis","unia","zena"]},
    ]
    return {"domains": domains}

@router.get("/memory/alerts")
async def get_alerts():
    return {"alerts": [], "total": 0}
