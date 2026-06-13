from fastapi import APIRouter, HTTPException
import os
from app.config import AGENTS_DIR

router = APIRouter()

REQUIRED_FILES = ["IDENTITY.md","SOUL.md","TOOLS.md","HEARTBEAT.md","AGENTS.md",
                  "MEMORY.md","README.md","BOOTSTRAP.md","AGENT_RULES.md","MODEL.md","USER.md"]

AGENT_IDS = ["nova","flux","cortexia","nero","forge","axon","ventura","clio",
             "finoria","kairo","kenzo","odis","vector","zion","saelia","arix",
             "daxio","enki","sora","tharos","lumeria","elora","kresta","luvia",
             "nura","vondra","fluentia","draven","orizon","solis","unia","zena"]

def audit_agent(agent_id):
    base = f"{AGENTS_DIR}/{agent_id}"
    files = []
    found = 0
    for f in REQUIRED_FILES:
        path = f"{base}/{f}"
        exists = os.path.exists(path)
        size = os.path.getsize(path) if exists else 0
        if exists: found += 1
        files.append({"name": f, "exists": exists, "size": size, "path": path})
    score = round(found / len(REQUIRED_FILES) * 100)
    issues = [f["name"] for f in files if not f["exists"]]
    return {"id": agent_id, "name": agent_id.capitalize(), "score": score,
            "files": files, "issues": issues, "found": found, "total": len(REQUIRED_FILES),
            "layer": "gateway" if agent_id=="nova" else "orchestrator" if agent_id=="flux" else
                     "lead" if agent_id in ["cortexia","finoria","saelia","lumeria","fluentia"] else "sentinel",
            "domain": next((d for d,ag in {"helix":["cortexia","nero","forge","axon","ventura","clio"],
                "finix":["finoria","kairo","kenzo","odis","vector","zion"],
                "matrix":["saelia","arix","daxio","enki","sora","tharos"],
                "quantix":["lumeria","elora","kresta","luvia","nura","vondra"],
                "zenix":["fluentia","draven","orizon","solis","unia","zena"]}.items() if agent_id in ag), "core")}

@router.get("/md-audit/overview")
async def get_overview():
    agents = [audit_agent(a) for a in AGENT_IDS]
    total = len(agents)
    complete = sum(1 for a in agents if a["score"]==100)
    overall = round(sum(a["score"] for a in agents) / total)
    return {"agents": agents, "total_agents": total, "complete_count": complete,
            "incomplete_count": total-complete, "overall_score": overall}

@router.get("/md-audit/agent/{agent_id}")
async def get_agent_audit(agent_id: str):
    return audit_agent(agent_id)

@router.get("/md-audit/agent/{agent_id}/all-files")
async def get_agent_files(agent_id: str):
    base = f"{AGENTS_DIR}/{agent_id}"
    if not os.path.exists(base):
        raise HTTPException(404, f"Agent {agent_id} niet gevonden")
    files = []
    for f in REQUIRED_FILES:
        path = f"{base}/{f}"
        files.append({"name": f, "exists": os.path.exists(path),
                      "size": os.path.getsize(path) if os.path.exists(path) else 0})
    return {"agent_id": agent_id, "files": files}

@router.get("/md-audit/agent/{agent_id}/file")
async def read_file(agent_id: str, path: str):
    base = f"{AGENTS_DIR}/{agent_id}"
    full = os.path.normpath(f"{base}/{path}")
    if not full.startswith(base): raise HTTPException(403, "Pad niet toegestaan")
    if not os.path.exists(full): raise HTTPException(404, "Bestand niet gevonden")
    return {"agent_id": agent_id, "path": path, "content": open(full, errors="ignore").read()}

@router.post("/md-audit/agent/{agent_id}/create-file")
async def create_file(agent_id: str, body: dict):
    base = f"{AGENTS_DIR}/{agent_id}"
    path = body.get("path","")
    content = body.get("content","")
    if not path.endswith(".md"): raise HTTPException(400, "Alleen .md bestanden")
    full = os.path.normpath(f"{base}/{path}")
    if not full.startswith(base): raise HTTPException(403, "Pad niet toegestaan")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full,"w").write(content)
    return {"agent_id": agent_id, "path": path, "created": True}

@router.get("/md-audit/incomplete")
async def get_incomplete():
    agents = [audit_agent(a) for a in AGENT_IDS if audit_agent(a)["score"] < 100]
    return {"agents": agents, "count": len(agents)}

@router.get("/md-audit/missing-files")
async def get_missing():
    result = {}
    for a in AGENT_IDS:
        audit = audit_agent(a)
        if audit["issues"]: result[a] = audit["issues"]
    return {"missing": result, "count": len(result)}
