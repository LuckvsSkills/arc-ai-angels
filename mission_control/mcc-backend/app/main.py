from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os, json
from datetime import datetime

app = FastAPI(title="ARC AI AGENTS MCC Backend", version="2.0.0")

app.add_middleware(CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"])

# Routes importeren
from app.api.agents_routes  import router as agents_router
from app.api.memory_routes  import router as memory_router
from app.api.canon_routes   import router as canon_router
from app.api.diagrams_routes import router as diagrams_router
from app.api.todo_routes    import router as todo_router
from app.api.scheduler_routes import router as scheduler_router
from app.api.openclaw_routes import router as openclaw_router
from app.api.md_audit_routes import router as md_audit_router
from app.api.tools_routes   import router as tools_router
from app.api.skills_routes  import router as skills_router
from app.api.auth_routes    import router as auth_router
from app.api.model_routes   import router as model_router
from app.api.system_routes  import router as system_router
from app.api.cost_routes    import router as cost_router
from app.api.tasks_api_routes import router as tasks_api_router
from app.api.skills_approval_routes import router as skills_approval_router

app.include_router(agents_router,   prefix="/api")
app.include_router(memory_router,   prefix="/api")
app.include_router(canon_router,    prefix="/api")
app.include_router(diagrams_router, prefix="/api")
app.include_router(todo_router,     prefix="/api")
app.include_router(scheduler_router,prefix="/api")
app.include_router(openclaw_router, prefix="/api")
app.include_router(md_audit_router, prefix="/api")
app.include_router(tools_router,    prefix="/api")
app.include_router(skills_router,   prefix="/api")
app.include_router(system_router, prefix="/api")
app.include_router(cost_router, prefix="/api")
app.include_router(tasks_api_router, prefix="/api")
app.include_router(skills_approval_router, prefix="/api")
app.include_router(auth_router)
app.include_router(model_router,    prefix="")

BASE_DIR = "/home/prime/arc_ai_angels"
AGENTS_DIR = f"{BASE_DIR}/agents"

@app.get("/api/health")
async def health():
    return {"status":"healthy","timestamp":datetime.now().isoformat(),
            "task_count_active":0,"agent_count_active":0,"alert_count_critical":0}

@app.get("/api/stats")
async def stats():
    return {"task_count_total":1,"task_count_by_status":{"TaskStatus.COMPLETED":1},
            "agent_count":32,"agent_count_active":32,"event_count_total":4,
            "last_update":datetime.now().isoformat()}

@app.get("/api/tasks")
async def tasks():
    return {"tasks":[{"task_id":"TASK-001","project_id":"PROJ-alpha","status":"COMPLETED",
            "owner_agent":"nova","owner_layer":"nova","assigned_to":"flux",
            "domain":None,"created_at":"2026-04-21T10:00:00Z","completed_at":"2026-04-21T10:15:00Z",
            "event_history":["evt_001","evt_002"],"last_updated":"2026-04-21T10:15:00Z",
            "is_overdue":False,"error_message":None}],"total_count":1}

@app.get("/api/tasks/{task_id}")
async def get_task(task_id: str):
    return {"task_id":task_id,"status":"COMPLETED","owner_agent":"nova"}

@app.get("/api/alerts")
async def alerts():
    return {"alerts":[],"total_count":0}

@app.get("/api/projects")
async def projects():
    import glob, re
    projects_dir = f"{BASE_DIR}/projects"
    projects = []
    for f in sorted(glob.glob(f"{projects_dir}/PROJECT_[0-9]*.md")):
        if "IDEAS" in f: continue
        try:
            content = open(f).read()
            title = re.search(r"^#\s+PROJECT\s+\d+\s+[—-]\s+(.+)$", content, re.MULTILINE)
            status = re.search(r"Status:\s*(.*)", content)
            revenue = re.search(r"Revenue:\s*(.*)", content)
            lead = re.search(r"Lead:\s*(.*)", content)
            pid = os.path.basename(f).replace(".md","")
            projects.append({
                "id": pid,
                "title": title.group(1).strip() if title else pid,
                "status": status.group(1).strip() if status else "ONBEKEND",
                "revenue": revenue.group(1).strip() if revenue else "-",
                "lead": lead.group(1).strip() if lead else "-",
                "file": os.path.basename(f),
                "content": content[:500]
            })
        except: pass
    return {"projects": projects, "total_count": len(projects)}

@app.get("/api/reload")
async def reload():
    return {"ok":True,"message":"Systeem herladen"}

@app.get("/system/health")
async def system_health():
    return {"status":"healthy","services":{"vite":"running","openclaw":"running"}}

@app.get("/system/logs/{service_name}")
async def system_logs(service_name: str):
    log_map = {"vite":"/tmp/vite.log","backend":"/tmp/mcc-backend.log"}
    path = log_map.get(service_name)
    if path and os.path.exists(path):
        lines = open(path,errors="ignore").readlines()[-50:]
        return {"service":service_name,"logs":[l.strip() for l in lines]}
    return {"service":service_name,"logs":[]}

@app.get("/system/service/{service_name}")
async def service_status(service_name: str):
    return {"service":service_name,"status":"running"}

@app.post("/system/service/{service_name}/restart")
async def service_restart(service_name: str):
    return {"ok":True,"service":service_name,"action":"restart"}

@app.post("/system/service/{service_name}/start")
async def service_start(service_name: str):
    return {"ok":True,"service":service_name,"action":"start"}

@app.post("/system/service/{service_name}/stop")
async def service_stop(service_name: str):
    return {"ok":True,"service":service_name,"action":"stop"}

@app.get("/api/chat/sessions")
async def chat_sessions():
    return {"sessions":[]}

@app.get("/api/chat/history/{session_id}")
async def chat_history(session_id: str):
    return {"session_id":session_id,"messages":[]}

@app.post("/api/chat/multi-agent")
async def multi_agent_chat(body: dict):
    return {"ok":True,"responses":[]}

@app.get("/api/audit/agents")
async def audit_agents():
    return {"agents":[],"count":0}

@app.get("/api/audit/agent/{agent_name}")
async def audit_agent(agent_name: str):
    return {"agent":agent_name,"status":"ok"}

@app.get("/api/audit/dashboard")
async def audit_dashboard():
    return {"status":"ok","total":32,"healthy":32}

@app.get("/api/audit/health")
async def audit_health():
    return {"status":"healthy"}

@app.get("/auth/2fa/qr")
async def twofa_qr():
    return {"qr":""}

@app.post("/auth/2fa/verify")
async def twofa_verify(body: dict):
    return {"ok":True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
