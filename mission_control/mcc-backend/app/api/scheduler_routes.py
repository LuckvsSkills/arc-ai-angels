from fastapi import APIRouter
import os, json, re
from app.config import AGENTS_DIR

router = APIRouter()

AGENT_IDS = ["nova","flux","cortexia","nero","forge","axon","ventura","clio",
             "finoria","kairo","kenzo","odis","vector","zion","saelia","arix",
             "daxio","enki","sora","tharos","lumeria","elora","kresta","luvia",
             "nura","vondra","fluentia","draven","orizon","solis","unia","zena"]

def get_agent_health():
    agents = []
    for aid in AGENT_IDS:
        clog = f"{AGENTS_DIR}/{aid}/consolidation.log"
        health = "idle"
        missed = 0
        if os.path.exists(clog):
            content = open(clog, errors="ignore").read()
            if "Consolidation complete" in content:
                health = "active"
            if "ERROR" in content or "failed" in content.lower():
                health = "warning"
                missed = 1
        agents.append({"agent_id": aid, "health": health, "active": 1 if health=="active" else 0,
                       "missed": missed, "retry": 0, "escalations": 0, "last_event": "", "last_activity_at": ""})
    return agents

@router.get("/scheduler/overview")
async def get_overview():
    agents = get_agent_health()
    active = sum(1 for a in agents if a["health"]=="active")
    missed = sum(a["missed"] for a in agents)
    return {"active_count": active, "missed_count": missed, "escalation_count": 0,
            "dispatch_candidate_count": 0, "total_agents": len(agents)}

@router.get("/scheduler/agent-health")
async def get_agent_health_route():
    return {"agents": get_agent_health(), "count": len(AGENT_IDS)}

@router.get("/scheduler/active-tasks")
async def get_active():
    return {"tasks": [], "count": 0}

@router.get("/scheduler/missed-tasks")
async def get_missed():
    return {"tasks": [], "count": 0}

@router.get("/scheduler/journal")
async def get_journal():
    events = []
    journal_dir = f"{AGENTS_DIR}/nova/JOURNAL/open"
    if os.path.exists(journal_dir):
        for f in sorted(os.listdir(journal_dir))[:10]:
            if f.endswith(".md"):
                events.append({"timestamp":"","agent":"nova","event_type":"unknown",
                               "task_id":"","title":"","journal_file":f,
                               "file_path":f"{journal_dir}/{f}"})
    return {"events": events, "count": len(events)}

@router.get("/scheduler/logs")
async def get_logs():
    return {"logs": [], "count": 0}

@router.get("/scheduler/alerts")
async def get_alerts():
    return {"alerts": [], "count": 0}

@router.get("/scheduler/pipeline")
async def get_pipeline():
    return {"pipeline": [], "count": 0}

@router.get("/scheduler/full")
async def get_full():
    return {"agents": get_agent_health(), "overview": {"active_count": 0}}

@router.get("/scheduler/due-tasks")
async def get_due():
    return {"tasks": [], "count": 0}

@router.get("/scheduler/escalations")
async def get_escalations():
    return {"escalations": [], "count": 0}

@router.get("/scheduler/dispatch-candidates")
async def get_dispatch():
    return {"candidates": [], "count": 0}

@router.get("/scheduler/execution-requests")
async def get_execution():
    return {"requests": [], "count": 0}

@router.get("/scheduler/retry-state")
async def get_retry():
    return {"retries": [], "count": 0}
